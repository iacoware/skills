# Recipe App — Piano di alto livello (slice verticali)

Deriva da `goal.md`, `concepts.md`, `arch-choices.md`, `tech-choices.md`.
Il repo contiene oggi **solo documentazione**: nessun codice, nessuna infra.

## Criteri di ordinamento

- **Slice verticali**: ogni slice attraversa input → dominio → persistenza → output e
  produce comportamento osservabile e verificabile da solo.
- **Breadth-first**: un comportamento core per tema prima di approfondire un tema.
- **Rischio in alto**: il differenziatore (ricerca semantica cross-lingua) e l'estrazione
  da link arrivano presto, non alla fine.
- Ogni slice include la **vera** authz (membership sul cookbook), validazione, gestione
  errori tipizzata e log minimo. Mai stub, mai rimandato.

## Temi

| Tema | Perché in questa posizione |
|---|---|
| A. Identità & sessione | prerequisito di tutto |
| B. Ricettari | scope di ogni altra entità e della authz |
| C. Ricette (CRUD manuale) | il dato canonico; sblocca ricerca ed estrazione |
| D. Ricerca semantica | differenziatore: va validato prima di investire sul resto |
| E. Estrazione da link | caso d'uso più frequente, rischio tecnico alto |
| F. Condivisione | il prodotto è condiviso per definizione |
| G. Foto | valore alto, rischio basso, indipendente |

---

## 0. Repository setup (prerequisito, non slice)

Solo il minimo che serve alla slice 1 per essere implementata e verificata.

- Next.js (App Router) + TypeScript strict, Prettier/ESLint secondo global instructions.
- Vitest + Testing Library; test co-locati.
- Effect installato con la struttura a `Context.Tag` + `Layer` già impostata (una porta
  reale, non un placeholder).
- Drizzle + migrazioni versionate; `docker-compose` con Postgres+pgvector per il dev locale.
- `Dockerfile` + `fly.toml` (suspend + scale-to-zero).
- Gestione config/segreti tipizzata (`Config` di Effect).

**Fatto quando**: `pnpm test`, `pnpm build`, `docker build` passano in locale.

---

## 1. Walking skeleton — login Google e vedo la mia home (vuota)

Il più piccolo comportamento utente end-to-end, più la CI/CD minima.

- Utente non loggato → landing con "Accedi con Google".
- Login via Auth.js + Google OAuth; sessione persistita su Postgres (adapter Drizzle).
- Post-login: home autenticata che dice "non hai ancora ricettari".
- Logout.
- CI: lint + test + build su push; CD: deploy su Fly.io da `main`.
- DB Neon (o Supabase) provisionato, estensione `pgvector` abilitata già ora, migrazioni
  applicate in fase di deploy.

**Verifica**: dall'URL pubblico di produzione, login con account Google reale, vedo la home,
faccio logout. Rotte protette rispondono 401/redirect senza sessione.

**Rischi**: callback URL OAuth per ambiente; migrazioni in fase di release su Fly.

---

## 2. Creo un ricettario e lo vedo nella mia lista *(tema B)*

- Form "nuovo ricettario" (solo `name`); `creatorId` = utente corrente.
- `Membership` del creator creata nella stessa transazione della `Cookbook`.
- Lista dei ricettari di cui sono membro; selezione del **ricettario corrente**
  (nell'URL: `/cookbooks/[id]`, così lo stato è condivisibile e bookmarkabile).
- Accesso a un cookbook di cui non sono membro → 404 (non 403: non rivelo l'esistenza).

**Verifica**: due utenti diversi vedono liste disgiunte; l'URL del cookbook altrui è 404.

---

## 3. Aggiungo una ricetta a mano e la rivedo *(tema C)*

- Form di review a campi vuoti: `name`, `ingredients[]`, `steps[]`, `prepTime?`, `tags[]`.
  È lo **stesso componente** che le slice 5/9/10 riuseranno pre-popolato.
- Salvataggio nel cookbook corrente (authz per membership).
- Lista ricette del cookbook + pagina di dettaglio.

**Verifica**: creo, vedo in lista, apro il dettaglio; un non membro non può creare né leggere.

**Nota di design**: il form di review è il punto di riuso più importante dell'app —
la sua API va disegnata qui pensando a "valori iniziali + origine (manuale/estratta)".

---

## 4. Cerco una ricetta e la trovo per significato *(tema D — differenziatore)*

- Al salvataggio: calcolo embedding multilingue da `name + tags + ingredients + steps +
  prepTime`, salvato in colonna `vector`; indice HNSW.
- Barra di ricerca in home: query → embedding → similarità, **scoped al cookbook corrente**.
- Ranking per distanza, con soglia/limite; stato vuoto esplicito.
- Backfill degli embedding per le ricette già create (script di migrazione dati).

**Verifica cross-lingua** (criterio di accettazione del differenziatore): salvo una ricetta
in inglese, cerco "pomodoro" in italiano, la trovo. Se questo test fallisce, il modello di
embedding va cambiato **prima** di proseguire.

**Rischi**: qualità cross-lingua del modello scelto; costo/latenza dell'embedding sulla
query (una chiamata per ricerca — accettabile, ma va misurata e cacheata per query ripetute).

---

## 5. Aggiungo una ricetta incollando un link *(tema E)*

Solo il **percorso felice** JSON-LD, per non mescolare due rischi in una slice.

- Input URL → fetch HTML con `HttpClient` (timeout, redirect, User-Agent, limite di size).
- Parsing `schema.org/Recipe` (JSON-LD) → decode con `Schema` verso il modello di dominio.
- **Progress reale** sui passi effettivi (`Scarico pagina → Leggo ricetta → Trovo
  ingredienti`), guidato dallo stato del flusso, non da un timer.
- Esito → stesso form di review della slice 3, pre-popolato; salvo con `sourceUrl`.
- Errori tipizzati e messaggi precisi già ora: URL non valido, fetch fallito, JSON-LD assente
  (per ora: "usa copia-incolla o inserisci a mano").

**Verifica**: 3 food blog reali con JSON-LD → ricetta corretta e correggibile; un sito senza
JSON-LD → messaggio preciso, nessun crash.

**Rischi**: la modellazione del progresso a step guida la forma del flusso di add — se emerge
guardia/concorrenza (annulla, retry, step falliti), è il punto in cui valutare XState.

---

## 6. Invito qualcuno nel mio ricettario *(tema F)*

- Il creator genera un invito (`token`, `expiresAt?`) e ottiene un link condivisibile.
- Chi apre il link da loggato ottiene una `Membership`; se non loggato → login e poi
  redirect all'accettazione.
- Da quel momento vede ed edita tutto il ricettario (nessun ruolo).
- Casi gestiti già ora: token inesistente/scaduto, utente già membro.

**Verifica**: due account reali, secondo utente accede al ricettario via link e crea una
ricetta visibile al primo.

---

## 7. Aggiungo una foto alla ricetta *(tema G)*

- Upload di **una** foto verso Cloudflare R2 (upload diretto con URL presigned);
  nel DB solo `url`; prima foto = cover implicita.
- Visualizzazione in lista (cover) e dettaglio.
- Validazione reale: tipo MIME, dimensione massima.

**Verifica**: carico una foto, la vedo in lista e dettaglio dopo un reload; file troppo grande
o non immagine → errore chiaro.

---

# Dopo i temi core — varianti, edge case e percorsi di errore (in ordine di rischio)

## 8. Modifico una ricetta esistente

Stesso form di review in modalità edit; ricalcolo dell'embedding a ogni salvataggio
(l'embedding è indice derivato, non dato canonico). Copre "review anche dopo il salvataggio".

## 9. Estrazione LLM quando manca il JSON-LD

Fallback su modello cheap con **structured output validato con `Schema`** (mai cast);
pulizia dell'HTML prima del prompt; timeout, retry con backoff e costo per chiamata loggato.
Il progresso mostra lo step reale ("Leggo ricetta con AI").

## 10. Aggiungo una ricetta incollando il testo

Terzo ingresso sullo stesso motore: salta JSON-LD, va sempre su LLM, stessa review.
Fallback dichiarato per paywall e siti JS-heavy.

## 11. Foto multiple e scelta della cover

N foto per ricetta, selezione esplicita della cover (invariante: una sola per ricetta),
eliminazione foto. Download automatico di `og:image`/`schema.org` all'add da link e
re-upload su R2 (evita hotlink che si rompono).

## 12. Errori di estrazione precisi

Messaggi distinti e azionabili per paywall/403, timeout, contenuto non-ricetta, JSON-LD
malformato — ciascuno con la via d'uscita giusta (copia-incolla / manuale).

## 13. Ciclo di vita di inviti e membership

Revoca invito, rigenerazione token, elenco membri, abbandono ricettario, rinomina/eliminazione
ricettario (con effetto su ricette e foto).

## 14. Hardening operativo

Rate limit sugli endpoint che spendono (estrazione, embedding), tetto di spesa,
health check per Fly, log strutturati con correlazione per richiesta, verifica del
comportamento a freddo con `suspend` + scale-to-zero.

---

## Fuori scope (confermato da `goal.md`)

Filtri strutturati e ricerca ibrida, ricerca cross-ricettario, ricettari pubblici,
gruppi sopra i cookbook, ruoli granulari, passkeys.

## Open questions

1. **Modello di embedding**: `text-embedding-3-small` è indicato in `arch-choices.md`, ma la
   qualità cross-lingua non è verificata. La slice 4 vive o muore su questo — serve un
   confronto (es. contro `multilingual-e5` / Cohere multilingual) prima di implementarla,
   o accettare di poterlo sostituire (astrarre la porta `Embedder` e versionare gli
   embedding già scritti).
2. **Provider Postgres**: Neon o Supabase. Scelta da chiudere prima della slice 1: cambia
   il modo di provisionare `pgvector`, le connection string e il pooling.
3. **Ricettario corrente con più ricettari**: dopo la slice 2, la home mostra la lista o
   entra nell'ultimo usato? Impatta la navigazione di tutte le slice successive.
4. **Dimensione del corpus per validare la ricerca**: servono ~30-50 ricette reali per dire
   che la semantica funziona. Va previsto un seed/import manuale prima della slice 4, oppure
   la slice 4 si sposta dopo la 5 (che popola più in fretta).
