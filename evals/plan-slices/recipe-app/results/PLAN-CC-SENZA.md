# Recipe App — Pianificazione di alto livello (slice verticali)

Fonte: `goal.md` (obiettivi), `concepts.md` (modello), `arch-choices.md` (infra),
`tech-choices.md` (stack).

## Criteri di slicing

- Ogni slice **attraversa tutti i layer** (UI → logica Effect → Postgres/servizi esterni) e
  termina con un **comportamento dimostrabile** dall'utente reale, non con un layer completo.
- Ogni slice è **deployata in produzione** su Fly prima di iniziare la successiva: il
  deploy non è una fase finale.
- Ordine guidato da due priorità: (a) sbloccare presto il **differenziatore** (ricerca
  semantica cross-lingua), (b) rimandare tutto ciò che costa soldi o rischio esterno
  (LLM, storage foto) finché il nucleo non è verificabile.
- Il **form di review** è l'artefatto centrale: nasce nella slice 2 come form di
  inserimento manuale e viene poi **riusato** (non riscritto) da link e copia-incolla.

## Mappa delle slice

| # | Slice | Valore utente dimostrabile | Nuove dipendenze esterne |
|---|---|---|---|
| 0 | Walking skeleton in prod | l'app risponde su un dominio pubblico | Fly, Neon/Supabase |
| 1 | Login e ricettario personale | entro con Google e vedo il mio ricettario vuoto | Google OAuth |
| 2 | Ricetta a mano + elenco + edit | inserisco, vedo, correggo una ricetta | — |
| 3 | Ricerca semantica cross-lingua | cerco "cena leggera" e trovo la ricetta giusta | API embeddings |
| 4 | Add da link (JSON-LD) + progress | incollo un URL e ottengo la ricetta precompilata | — |
| 5 | Fallback LLM + copia-incolla | funziona anche su siti senza structured data | API LLM |
| 6 | Foto multiple + cover | la ricetta ha immagini, scelgo la copertina | Cloudflare R2 |
| 7 | Condivisione via invito | invito mia sorella, editiamo lo stesso ricettario | — |
| 8 | Rifinitura e messa a regime | l'app regge l'uso quotidiano della famiglia | — |

---

## Slice 0 — Walking skeleton in produzione

**Obiettivo**: una pagina banale servita da Fly che legge un dato da Postgres. Serve a
pagare subito il costo di setup infrastrutturale, non a fine progetto.

**Contenuto**
- Next.js App Router + TypeScript, Dockerfile, `fly.toml` con `auto_stop = suspend` e
  scale-to-zero.
- Postgres gestito (Neon o Supabase) con estensione `pgvector` **abilitata da subito**,
  anche se ancora inutilizzata.
- Drizzle + migrazioni versionate, eseguite nel deploy.
- Runtime Effect minimo: un `Context.Tag` per il servizio DB, il `Layer` che lo fornisce,
  e il boundary Next↔Effect (dove l'errore tipizzato diventa risposta HTTP/UI).
- Health check che fa una query reale.

**Fuori slice**: auth, entità di dominio, UI vera.

**Verifica**: URL pubblico raggiungibile; health check verde; deploy ripetibile da CLI;
misurato il cold start reale dopo inattività (dato che serve alla slice 8).

**Rischi**: nessuno tecnico; il rischio è *saltarla* e scoprire i problemi di
container/migrazioni quando c'è già codice di dominio da debuggare sopra.

---

## Slice 1 — Login Google e ricettario personale

**Obiettivo**: l'utente entra con Google e atterra su una Home con il proprio ricettario
(vuoto). È la prima slice con uno stato per-utente.

**Contenuto**
- Auth.js (NextAuth v5) + Google OAuth, sessione persistita su Postgres.
- Tabelle `User`, `Cookbook`, `Membership` (senza `role`, come da `concepts.md`).
- Al primo login: creazione del ricettario di default e della `Membership` del creator.
- Concetto di **ricettario corrente** in sessione/URL — introdotto ora anche se ce n'è uno
  solo, perché ogni query successiva (elenco, ricerca) deve essere scoped fin dall'inizio.
- Regola di autorizzazione unica e centralizzata: *si accede a una risorsa solo se esiste
  una Membership sul suo cookbook*. Applicata nel boundary, non sparsa nelle pagine.

**Fuori slice**: inviti, cambio ricettario, gestione multi-ricettario in UI.

**Verifica**: login/logout funzionanti; due account Google diversi vedono ricettari
diversi; accesso diretto all'URL di un ricettario altrui → negato.

**Rischi**: il modello di autorizzazione introdotto tardi è il classico buco di sicurezza
retroattivo; per questo entra qui e non nella slice 7.

---

## Slice 2 — Ricetta a mano, elenco e correzione

**Obiettivo**: primo giro completo del dato di dominio senza alcun servizio esterno.

**Contenuto**
- Tabella `Recipe` (senza `embedding` e senza foto): nome, ingredienti, passi, tag,
  `prepTime?`, `sourceUrl?`.
- **Form di review** (campi vuoti): l'unico form di editing dell'app, progettato per
  essere riempito da un estrattore nelle slice 4–5.
- Elenco ricette del ricettario corrente + dettaglio.
- Edit e cancellazione di una ricetta esistente.

**Fuori slice**: ricerca, estrazione, foto.

**Verifica**: inserisco una ricetta a mano, la vedo in elenco, la apro, la correggo, la
correzione persiste; un membro di un altro ricettario non la vede.

**Rischi**: la forma di ingredienti e passi (lista di stringhe vs struttura ricca) va
decisa qui — cambiarla dopo la slice 5 significa toccare schema LLM, embedding e UI
insieme. Scelta di default: liste di stringhe, coerenti con `concepts.md`.

---

## Slice 3 — Ricerca semantica cross-lingua

**Obiettivo**: il differenziatore, il prima possibile e su dati inseriti a mano.

**Contenuto**
- Colonna `embedding` (pgvector) + indice HNSW.
- Servizio di embedding (porta `Context.Tag`, adapter su API cloud multilingue) invocato
  **al salvataggio e a ogni edit**, mai in lettura sulla ricerca.
- Testo indicizzato: `nome + tag + ingredienti + preparazione + tempo`, come da `goal.md`.
- Ricerca: embedding della query + similarità, **scoped al ricettario corrente**.
- Backfill degli embedding per le ricette già inserite (script di migrazione dati) —
  esiste da qui in avanti come pattern riusabile.

**Fuori slice**: filtri strutturati, ricerca ibrida, ricerca cross-ricettario (tutti
esplicitamente post-MVP).

**Verifica**: inserita a mano una ricetta **in inglese**, la query italiana "pomodoro" la
trova; query concettuale ("cena leggera") restituisce risultati sensati; la ricerca non
attraversa i confini del ricettario.

**Rischi**: è la slice che può **invalidare la premessa del prodotto**. Se la qualità
cross-lingua non convince, va scoperto ora — quando l'unica cosa costruita sopra è un
form — non dopo la pipeline di estrazione. Include un mini-benchmark manuale (10–15
ricette bilingui, query attese) da conservare come regressione.

---

## Slice 4 — Aggiunta da link con JSON-LD e progress reale

**Obiettivo**: il caso d'uso più frequente, sul percorso gratuito e deterministico.

**Contenuto**
- Fetch della pagina con `HttpClient` di Effect (timeout, retry, user-agent, limite
  dimensione), errori come `Data.TaggedError` distinti (`FetchFailed`, `NotHtml`,
  `NoStructuredData`, …).
- Parsing `schema.org/Recipe` da JSON-LD → `Recipe` normalizzata validata con `Schema`.
- **Progress sui passi reali** (`Scarico pagina → Leggo ricetta → Trovo ingredienti`):
  ogni step riflette una fase effettiva della pipeline e, in caso di errore, il messaggio
  dice *quale* step è fallito e perché (es. paywall).
- L'estratto atterra nel form di review della slice 2; salvataggio → embedding (slice 3).
- `sourceUrl` valorizzato.

**Fuori slice**: LLM, copia-incolla, download immagini.

**Verifica**: su 5–10 food blog reali con structured data, l'import produce ricette
corrette e cercabili; un URL senza JSON-LD produce un errore **preciso e azionabile**
(che nella slice 5 diventerà un fallback automatico).

**Rischi**: la scelta "sincrona con progress" vincola la durata dell'operazione a stare
dentro i limiti di richiesta di Fly/browser; va verificata su siti lenti e definito un
timeout complessivo esplicito.

---

## Slice 5 — Fallback LLM e copia-incolla

**Obiettivo**: coprire i siti senza structured data — insieme alla ricerca semantica è
l'altro elemento in cui l'app supera il benchmark (Mealie).

**Contenuto**
- Pulizia contenuto (HTML → testo leggibile).
- Estrattore LLM (modello cheap, output strutturato **validato con `Schema`**, mai cast)
  dietro la stessa porta dell'estrattore JSON-LD: la UI e il form di review non cambiano.
- **Copia-incolla**: nuovo ingresso che salta il JSON-LD e va sempre su LLM, riusando
  motore, schema e review.
- Innesto del fallback nel flusso della slice 4: JSON-LD assente → LLM, con lo step di
  progress corrispondente.
- Controlli di costo: cap sulla dimensione del testo inviato, nessuna chiamata LLM fuori
  dalla fase di add.

**Fuori slice**: OCR/foto/PDF (non in MVP).

**Verifica**: un sito JS-heavy o dietro paywall importato via copia-incolla produce una
ricetta corretta; costo per estrazione misurato e coerente con "frazioni di cent";
l'output malformato dell'LLM produce un errore gestito, non una ricetta corrotta.

**Rischi**: dipendenza da provider a pagamento e non deterministica. Mitigazione: schema
di validazione stretto, e il form di review come rete di sicurezza (l'utente corregge
sempre prima di salvare).

---

## Slice 6 — Foto multiple e cover

**Obiettivo**: la ricetta diventa presentabile; primo servizio con stato binario esterno.

**Contenuto**
- Tabella `Photo` (solo `url` nel DB) + Cloudflare R2.
- Upload di foto dall'utente e **ri-hosting** dell'immagine trovata all'import
  (`og:image` / `schema.org`) sul proprio storage, per non dipendere da hotlink che si
  rompono.
- Scelta della **cover** (una sola per ricetta) e uso della cover in elenco/dettaglio.
- Step `Salvo foto` aggiunto al progress dell'add.

**Fuori slice**: ridimensionamento/CDN avanzati, galleria ricca.

**Verifica**: ricetta con più foto, cover scelta e visibile in elenco; cancellando la
ricetta gli oggetti su R2 non restano orfani.

**Rischi**: il ciclo di vita degli oggetti storage (upload abbandonati, cancellazioni) è
la fonte tipica di sporcizia; va definito ora, non dopo.

---

## Slice 7 — Condivisione via invito

**Obiettivo**: da app personale ad app di famiglia. Arriva tardi di proposito: fino a qui
il modello di membership esiste già (slice 1) ed è stato esercitato su ogni query.

**Contenuto**
- Tabella `Invitation` (token, `expiresAt?`) e generazione del link/codice da parte di un
  membro del ricettario.
- Accettazione invito da utente loggato → `Membership`; utente non loggato → login Google
  e poi accettazione.
- UI multi-ricettario: creazione di nuovi ricettari, elenco dei propri, **switch** del
  ricettario corrente.
- Elenco membri del ricettario.

**Fuori slice**: ruoli/permessi granulari, rimozione membri, ricettari pubblici — tutti
esplicitamente post-MVP.

**Verifica**: due account Google reali condividono un ricettario, entrambi aggiungono ed
editano; un token scaduto o già speso viene rifiutato; le ricerche di ciascuno restano
scoped al ricettario selezionato.

**Rischi**: il link di invito è una credenziale — token non indovinabile, scadenza,
nessun leak in log/referrer.

---

## Slice 8 — Rifinitura e messa a regime

**Obiettivo**: l'app regge l'uso quotidiano senza sorprese di costo o affidabilità.

**Contenuto**
- Decisione finale su cold start: restare su `suspend` + scale-to-zero oppure macchina
  sempre calda (~$3/mese), sulla base della latenza misurata dalla slice 0 in poi.
- Limiti di abuso sugli endpoint che spendono soldi (add da link/LLM/embedding).
- Errori utente coerenti su tutti i percorsi di fallimento della pipeline.
- Backup/ripristino DB verificato almeno una volta.
- Verifica costi reali contro il target (~$0 + centesimi) e passata di accessibilità/UX
  sui form (campi opzionali marcati "optional", stati esposti alle assistive technology).

**Verifica**: uso reale della famiglia per un periodo, senza intervento manuale;
consuntivo costi in linea con `arch-choices.md`.

---

## Ordine e dipendenze

```
0 skeleton
 └─ 1 auth + cookbook + autorizzazione
     └─ 2 ricetta a mano + form di review          ← base riusata da 4 e 5
         ├─ 3 ricerca semantica (differenziatore)  ← validazione della premessa
         └─ 4 add da link (JSON-LD) + progress
             └─ 5 fallback LLM + copia-incolla
                 └─ 6 foto + cover
                     └─ 7 condivisione
                         └─ 8 messa a regime
```

Le slice 3 e 4 sono indipendenti tra loro e potrebbero procedere in parallelo; se si
lavora in sequenza, **3 prima di 4**: valida il differenziatore quando il costo di
cambiare idea è ancora minimo.

## Invarianti che attraversano tutte le slice

- **Un solo datastore** (Postgres) e **un solo motore di estrazione** dietro una porta.
- **Un solo form di review** per manuale, link e copia-incolla, usabile prima e dopo il
  salvataggio.
- `embedding` è **dato derivato**: rigenerato a ogni edit, mai fonte di verità, mai
  calcolato in lettura.
- Ogni query di dominio è **scoped al cookbook** e passa dal controllo di membership.
- Costi variabili solo in **fase di add**, mai a runtime sulle ricerche.

## Open questions

- **Provider Postgres**: Neon o Supabase — non deciso in `arch-choices.md`. Impatta la
  slice 0 (connessione, migrazioni, backup) e va chiuso prima di iniziarla.
- **Provider e modello LLM per l'estrazione**: `arch-choices.md` dice "Haiku-class" senza
  fissare il vendor; con OpenAI già presente per gli embeddings c'è un trade-off tra un
  solo fornitore e il modello migliore. Blocca la slice 5.
- **Modello di embedding**: `text-embedding-3-small` è indicato come esempio, ma la
  qualità **cross-lingua** è il requisito che regge il prodotto. Va scelto (ed
  eventualmente confrontato con alternative multilingue dedicate) entro la slice 3, perché
  la dimensione del vettore fissa schema e indice.
- **Creazione del primo ricettario**: automatica al primo login o esplicita? Cambia la UI
  della slice 1 e cosa vede un utente appena registrato.
- **Upload foto da dispositivo nell'MVP**: `goal.md` parla di "foto multiple" senza
  specificare se l'utente carica le proprie o se ci si limita a ri-ospitare quella
  dell'import. Determina l'ampiezza della slice 6.
- **Cancellazione di un ricettario e uscita di un membro**: non coperte da `concepts.md`;
  se restano fuori MVP va detto esplicitamente, perché toccano il ciclo di vita dei dati
  condivisi (slice 7).
