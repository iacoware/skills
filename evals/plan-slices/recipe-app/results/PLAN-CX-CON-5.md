# Recipe App — Piano di delivery

- **Sources:** `sources/goal.md`, `sources/arch-choices.md`, `sources/concepts.md`, `sources/tech-choices.md`.
- **Current state:** Greenfield documentato; nessuna implementazione applicativa esistente, stack deciso salvo i provider indicati nel lavoro non-prodotto.

## Ordering criteria

- Validare prima ricerca semantica cross-lingua ed estrazione fallback, i due differenziatori rispetto alle alternative mature.
- Usare ricette controllate e uno scope configurato finché l’identità non serve; Google OAuth sostituisce quel resolver in un solo punto prima degli altri flussi end-user.
- Dare precedenza all’import da URL, caso più frequente, e consegnarne subito i fallback prima di aprire temi meno rischiosi.
- Introdurre R2 con il primo percorso foto reale; separare download remoto e gestione multi-foto perché hanno failure mode indipendenti.
- Mantenere slice iniziali strette e review frequenti finché delivery, Effect, UI e confini di ricettario non sono provati.

## Themes

| Theme | Desired outcome | First validation |
|---|---|---|
| A. Scoperta semantica | Trovare nel ricettario corrente ricette pertinenti anche tra lingue diverse | 2. Indicizzazione multilingue osservabile |
| B. Accesso e ricettari | Entrare con Google e lavorare solo nei ricettari di cui si è membri | 4. Accesso Google e ricettario corrente |
| C. Acquisizione e correzione | Salvare subito una ricetta da input manuale, URL o testo e correggerla dopo | 5. Inserimento manuale, elenco ed edit |
| D. Foto | Conservare foto affidabili con una cover controllabile | 9. Foto importata senza hotlink |
| E. Condivisione | Invitare persone in un ricettario e collaborare da pari | 10. Invito e adesione al ricettario |

## Cross-functional concerns

- **Authorization:** Ogni lettura, scrittura e ricerca usa un solo `CurrentCookbookResolver`; lo scope configurato delle slice 2–3 è sostituito da sessione e membership nella slice 4, mentre solo il creator crea inviti.
- **Validation and errors:** Schema decodifica input non fidati, JSON-LD e output LLM; errori Effect tipizzati diventano messaggi precisi associati allo step reale fallito.
- **Operability:** Log correlati per richiesta e step; timeout, retry limitati e metriche di latenza/costo per fetch, embedding, LLM e R2; cold start Fly osservato separatamente.
- **Accessibility and security:** Progress e form sono fruibili da tastiera e screen reader, i campi opzionali sono espliciti, OAuth protegge le sessioni e il fetch URL blocca SSRF anche dopo redirect.
- **Data integrity and recovery:** La ricetta è canonica, embedding e metadati sono derivati e rigenerabili, i duplicati sono ammessi, una sola foto è cover e i side effect esterni sono ritentabili senza corrompere il salvataggio.

## NOW

### 0. Repository e quality gate *(Enabler: delivery)*

---

**Includes**

- Repository TypeScript/Next.js con configurazione condivisa di lint, typecheck e test.
- Build Docker riproducibile e CI che esegue build, lint, typecheck e test senza provisioning né deploy.
- Convenzioni minime per Effect, Schema, Drizzle, React Query e test automatizzati.

**Verification**

- Da checkout pulito, CI e gli stessi comandi locali completano build, lint, typecheck e test.

**Outcome**

- Gli sviluppatori possono integrare incrementi su una baseline eseguibile e verificata.

### 1. Runtime e Postgres connessi *(Enabler: delivery)*

---

**Includes**

- Container Next.js stateless distribuito via CI/CD su Fly.io in un ambiente non produttivo rappresentativo con `suspend` e scale-to-zero.
- Provider Postgres selezionato dal lavoro non-prodotto, `pgvector`, driver TCP reale e configurazione di pooling compatibile con cold start.
- Migration runner che applica una migrazione non-domain e runtime che esegue un round trip non-domain sul datastore.
- Provisioning minimo tramite `fly.toml` e CLI Fly; nessuna entità ricetta, autenticazione, tenancy o integrazione R2.

**Verification**

- Un deploy da CI applica la migrazione e il runtime conferma scrittura/lettura Postgres tramite connessione reale.
- Arresto, risveglio da `suspend`, nuova connessione e redeploy preservano il round trip; tempi e failure sono osservabili.

**Outcome**

- Gli sviluppatori sanno che deploy, migrazioni, pgvector e connessioni funzionano insieme nell’ambiente target.

### 2. Indicizzazione multilingue osservabile *(Enabler: ricerca semantica)*

---

**Includes**

- Ricette normalizzate controllate attraversano il percorso reale di embedding deciso dal lavoro non-prodotto e persistenza pgvector.
- Ogni ricetta appartiene a un ricettario controllato risolto dal `CurrentCookbookResolver` configurato per l’ambiente non pubblico.
- Un consumer diagnostico genera la query secondo la decisione presa e restituisce il ranking tramite indice HNSW, senza UI prodotto.
- Testo indicizzato composto da nome, ingredienti e preparazione, più tag e tempo quando presenti, alla scala prevista fino a 10.000 ricette.

**Verification**

- Un corpus curato multilingue dimostra che query italiane recuperano le ricette inglesi attese e non ricette di un altro ricettario.
- Esecuzioni ripetute misurano qualità del ranking, latenza e costo del percorso reale e segnalano errori o output non validi.

**Learning / risk**

- Verifica che la qualità cross-lingua, vero differenziatore, sia sufficiente alla scala e al budget previsti.

**Outcome**

- Gli sviluppatori dispongono di evidenza eseguibile per decidere se il motore semantico merita una UX prodotto.

### 3. Ricerca semantica nel ricettario *(Theme: A)*

---

**Includes**

- Home di test con campo di ricerca e risultati ordinati solo per similarità semantica nel ricettario corrente.
- Query generata secondo la decisione della spike, senza filtri strutturati, full-text o traduzione del contenuto.
- Stati accessibili per inattività, caricamento, nessun risultato, timeout e indisponibilità del provider.
- Audience limitata a tester autorizzati nell’ambiente non pubblico con scope configurato.

**Verification**

- I tester trovano dal browser le ricette controllate attese con query cross-lingua e giudicano pertinenza e comprensibilità dei risultati.
- Query equivalenti non espongono ricette fuori scope; timeout e provider failure producono uno stato recuperabile e log correlati.

**Learning / risk**

- Misura rilevanza percepita, latenza end-to-end e utilità della ricerca prima di costruire i flussi commodity.

**Outcome**

- Un tester può valutare il principale differenziatore nel prodotto reale distribuito.

### 4. Accesso Google e ricettario corrente *(Theme: B)*

---

**Includes**

- Login e logout con Auth.js v5 e Google OAuth, sessioni persistite in Postgres e nessuna credenziale applicativa.
- Creazione di ricettari privati con creator e membership iniziale, elenco dei propri ricettari e selezione di quello corrente.
- Sostituzione del resolver configurato con un resolver basato su sessione e membership, mantenendo un solo seam di scope.
- Home vuota o con le ricette controllate del ricettario selezionato; `visibility=private` nell’MVP.

**Verification**

- Un utente entra con Google, crea e cambia ricettario; logout e nuova sessione conservano memberships e selezione prevista.
- Utenti anonimi e non membri non possono leggere, cercare o modificare un ricettario neppure chiamando direttamente i boundary.

**Outcome**

- Un utente identificato può entrare e lavorare entro confini di ricettario verificabili.

### 5. Inserimento manuale, elenco ed edit *(Theme: C)*

---

**Includes**

- Home con elenco delle ricette del ricettario corrente e form condiviso per creazione manuale ed edit.
- Titolo, ingredienti e preparazione come testo libero; salvataggio immediato senza review obbligatoria.
- Embedding rigenerato su creazione e modifica; trattamento di tag e tempo conforme alla decisione del lavoro non-prodotto.
- Controlli membership su ogni operazione e nessuna deduplica automatica.

**Verification**

- Un membro crea, vede e corregge una ricetta; il salvataggio non richiede campi accessori né parsing di quantità o unità.
- Dopo un edit, la ricerca riflette il nuovo testo; un altro ricettario e un non membro non vedono né modificano la ricetta.
- Input non valido o embedding fallito non produce dati apparentemente completi e offre un retry comprensibile.

**Learning / risk**

- Verifica che il modello testuale minimo e la correzione post-salvataggio riducano davvero l’attrito.

**Outcome**

- Un membro può mantenere e ritrovare ricette conosciute senza normalizzazione fine.

### 6. Import URL con JSON-LD *(Theme: C)*

---

**Includes**

- Inserimento URL, fetch server-side protetto da SSRF e parsing di `schema.org/Recipe` validato.
- Salvataggio immediato di titolo, ingredienti, preparazione, `sourceUrl` e metadati best-effort, seguito dall’embedding.
- Progress sincrono accessibile basato su `Scarico pagina`, `Leggo ricetta` e `Trovo ingredienti` realmente attraversati, senza percentuali simulate.
- Errori precisi per URL non valido, fetch, redirect, paywall, JSON-LD assente o malformato; nessuna chiamata LLM in questo percorso.

**Verification**

- Pagine campione con JSON-LD diventano ricette ricercabili e modificabili, mostrando in ordine solo gli step reali.
- JSON-LD assente e host privati, link-local o raggiunti via redirect sono rifiutati con causa precisa e senza salvataggi parziali.
- Telemetria conferma zero chiamate LLM e costo di estrazione nullo per il percorso strutturato.

**Learning / risk**

- Misura hit-rate e variabilità reale del percorso gratuito per il caso d’uso più frequente.

**Outcome**

- Un membro importa con minimo attrito ricette dai siti che espongono dati strutturati.

### 7. Copia-incolla come fallback *(Theme: C)*

---

**Includes**

- Input di testo incollato che salta fetch e JSON-LD e usa il provider LLM selezionato con output strutturato validato.
- Stesso salvataggio immediato, embedding, metadati best-effort, progress reale ed edit post-salvataggio degli altri ingressi.
- Fallback esplicito per paywall, pagine JS-heavy e altri fallimenti di lettura URL.
- Timeout, limite input e gestione di rifiuto, output incompleto o non valido senza inventare campi obbligatori.

**Verification**

- Testi rappresentativi di pagine illeggibili producono ricette ricercabili e correggibili con costo, latenza e qualità osservati.
- Output LLM malformato, timeout e contenuto non-ricetta danno un errore recuperabile senza persistenza incoerente.

**Learning / risk**

- Verifica qualità e costo dell’estrazione LLM sulla recovery che copre i limiti degli scraper concorrenti.

**Outcome**

- Un membro può salvare una ricetta anche quando il sito sorgente non è leggibile automaticamente.

### 8. Fallback LLM automatico da URL *(Theme: C)*

---

**Includes**

- Le pagine leggibili prive di JSON-LD passano automaticamente al motore LLM già validato, senza nuovo input utente.
- Pulizia HTML, schema di output, salvataggio, embedding e progress sono condivisi con i percorsi già stabiliti.
- La cascata resta JSON-LD-first e non invoca LLM quando il dato strutturato valido è disponibile.
- Errori di entrambe le strategie indicano lo step fallito e propongono il copia-incolla già disponibile.

**Verification**

- URL campione senza JSON-LD producono ricette ricercabili; gli stessi contenuti incollati rispettano lo stesso contratto estratto.
- Telemetria distingue hit JSON-LD, fallback LLM, latenza e costo; failure combinati terminano nel fallback manuale senza loop.

**Learning / risk**

- Misura copertura incrementale e costo della cascata per decidere se l’import automatico è competitivo.

**Outcome**

- Un membro incolla un URL e ottiene una ricetta anche quando mancano dati strutturati.

### 9. Foto importata senza hotlink *(Theme: D)*

---

**Includes**

- La prima immagine valida da JSON-LD o `og:image` viene scaricata e caricata su Cloudflare R2 durante l’import URL.
- Nel database resta solo l’URL R2 e la prima foto diventa cover; nessuna dipendenza dal sito sorgente dopo il salvataggio.
- Il progress aggiunge `Salvo foto` solo quando lo step è reale.
- Download o upload fallito preserva la ricetta, segnala la foto mancante e consente retry idempotente.

**Verification**

- Rimuovendo l’accesso alla sorgente, la cover resta visibile da R2 e appartiene alla ricetta e al ricettario corretti.
- Timeout, risposta non-immagine e failure R2 non duplicano oggetti né cancellano la ricetta; il retry completa la foto.

**Learning / risk**

- Verifica affidabilità, costo e failure profile del confine object-storage sul percorso più frequente.

**Outcome**

- Una ricetta importata conserva una cover stabile senza hotlink fragile.

### 10. Invito e adesione al ricettario *(Theme: E)*

---

**Includes**

- Il creator genera un link o codice non prevedibile associato a un solo ricettario.
- Un destinatario autenticato accetta l’invito e ottiene una membership paritaria per lettura, ricerca ed edit.
- Lo stesso utente può aderire a più ricettari e cambiare ricettario corrente dalla home.
- Utenti già membri, token invalidi e accessi anonimi hanno esiti idempotenti o recuperabili senza elevazione di privilegi.

**Verification**

- Due account Google condividono una ricetta nello stesso ricettario e vedono reciprocamente gli edit, senza accesso agli altri ricettari.
- Solo il creator crea inviti; token alterati o destinati a un altro ricettario non concedono membership.

**Learning / risk**

- Verifica se il modello cookbook-centrico è comprensibile e sufficiente per famiglia e amici.

**Outcome**

- Il creator può rendere collaborativo un ricettario tramite un invito condivisibile.

### 11. Foto multiple e scelta cover *(Theme: D)*

---

**Includes**

- I membri aggiungono più foto a una ricetta esistente e vedono lo stato di ciascun upload.
- La prima foto resta cover di default e un membro può sceglierne un’altra.
- Aggiornamento cover mantiene l’invariante di una sola cover; cancellazioni e retry non lasciano riferimenti o oggetti orfani.
- Tipi, dimensioni e contenuti non validi sono rifiutati prima o durante il confine R2 con feedback accessibile.

**Verification**

- Upload multipli, cambio cover e reload conservano ordine e unica cover per la ricetta corretta.
- Failure parziali e retry non duplicano foto, non cambiano cover per errore e non impediscono l’uso della ricetta.

**Outcome**

- I membri possono documentare una ricetta con più foto e controllarne l’immagine principale.

### 12. Release privata per famiglia e amici *(Release: delivery)*

---

**Includes**

- Ambiente previsto per gli utenti selezionati su Fly.io con `suspend`, datastore e R2 scelti, callback Google, segreti e migrazioni configurati.
- Controlli operativi minimi su errori esterni, cold start e consumo rispetto al budget di centesimi mensili.
- Percorsi help essenziali indicano copia-incolla dopo un import fallito ed edit dopo un’estrazione imperfetta.
- Nessun filtro strutturato, ricettario pubblico o permesso granulare viene aperto nella release.

**Verification**

- Da account nuovi, creator e invitato completano in produzione login, invito, import URL, fallback, edit, foto e ricerca cross-lingua scoped.
- Smoke test post-migrazione e dopo `suspend` conferma disponibilità; failure simulate dei provider restano osservabili e recuperabili.
- Misure iniziali confermano costi, latenza e tasso errori entro i trade-off dichiarati o producono una decisione esplicita.

**Outcome**

- Famiglia e amici possono usare in sicurezza un ricettario condiviso che dimostra i due differenziatori.

## LATER

- **Filtri strutturati per tag/tempo e ricerca ibrida**
  - **Promotion trigger:** Le query e i metadati di NOW mostrano bisogni ricorrenti non soddisfatti dal ranking semantico e qualità sufficiente di tag/tempo.
  - **Expected value:** Controllo preciso senza migrazione o backfill dei dati già derivati.
- **Ricettari pubblici tematici**
  - **Promotion trigger:** Utenti chiedono scoperta o condivisione oltre cerchie invitate e i confini di moderazione sono definiti.
  - **Expected value:** Raccolte pubbliche tramite la `visibility` già prevista.
- **Gruppi sopra i ricettari**
  - **Promotion trigger:** Le prove di invito mostrano reinviti ripetuti come attrito materiale.
  - **Expected value:** Riutilizzo della stessa membership su più ricettari.
- **Ricerca cross-ricettario**
  - **Promotion trigger:** Membri di più ricettari cambiano spesso scope per trovare la stessa ricetta.
  - **Expected value:** Scoperta globale mantenendo visibili i confini di provenienza.
- **Ruoli e permessi granulari**
  - **Promotion trigger:** La collaborazione paritaria produce abusi o richieste ricorrenti di sola lettura.
  - **Expected value:** Governance più fine senza anticipare complessità nell’MVP.
- **Passkeys**
  - **Promotion trigger:** Il vincolo dell’account Google blocca utenti reali e il supporto Auth.js al recupero è maturo.
  - **Expected value:** Accesso ricorrente semplice senza dipendenza esclusiva da Google.
- **Fly sempre caldo**
  - **Promotion trigger:** La release misura cold-start fastidiosi rispetto al costo aggiuntivo di circa $3/mese.
  - **Expected value:** Prima richiesta più rapida con un flag operativo reversibile.
- **IaC estesa**
  - **Promotion trigger:** Più ambienti o drift manuale rendono insufficiente `fly.toml` con CLI.
  - **Expected value:** Provisioning versionato quando la complessità operativa lo giustifica.

## OUT-OF-SCOPE

- **Normalizzazione di quantità/unità, lista della spesa e scaling porzioni** — Contraddicono il modello testuale minimo e richiedono un dominio ingrediente deliberatamente escluso.
- **Review obbligatoria durante l’aggiunta** — Aumenta l’attrito; la correzione avviene sempre dopo il salvataggio.
- **Deduplica automatica** — I duplicati nello stesso ricettario sono esplicitamente ammessi.
- **Email/password e magic-link** — Richiedono provider email e flussi account esclusi dalla decisione Google OAuth.
- **Vector DB dedicato, embedding self-hosted e hosting alternativi scartati** — Aggiungono costo o rischio senza beneficio alla scala prevista.

## Decision checkpoints

- **After 2. Indicizzazione multilingue osservabile:** Qualità cross-lingua, latenza e costo reali → proseguire, cambiare modello/percorso o fermare il prodotto che altrimenti replicherebbe Mealie.
- **After 3. Ricerca semantica nel ricettario:** Giudizi dei tester sui risultati → cambiare UX/ranking o mantenere la ricerca semantica come unico percorso MVP.
- **After 8. Fallback LLM automatico da URL:** Copertura JSON-LD+LLM, qualità, failure e costo → cambiare modello/cascata o ridurre i siti supportati prima delle foto.
- **After 10. Invito e adesione al ricettario:** Comprensione e attrito dei reinviti → promuovere gruppi da LATER o mantenere il modello cookbook-centrico.
- **After 12. Release privata per famiglia e amici:** Uso, cold-start e costo reali → promuovere filtri, macchina sempre calda o altre estensioni motivate.

## Non-product work

- **Selezione Postgres, prima della slice 1 (1 giorno):** Confrontare Neon e Supabase su pgvector, TCP/TLS, pooling, migrazioni, suspend Fly e free tier; exit con provider e connection mode registrati, prove eliminate.
- **Decisione semantica, prima della slice 2 (2 giorni):** Risolvere il conflitto tra `embedding(query)` e divieto di embedding runtime, selezionare provider/modello cloud multilingue con corpus e stime; exit con percorso autorizzato o stop, codice sperimentale eliminato.
- **Arricchimento manuale, prima della slice 5 (mezza giornata):** Risolvere se il manuale salta ogni estrazione o usa il motore per tag/tempo, preservando salvataggio immediato e costo minimo; exit con decisione registrata, nessun codice.
- **Selezione LLM estrazione, prima della slice 7 (2 giorni):** Confrontare modelli cheap compatibili su output strutturato, qualità, timeout e costo per testo/HTML; exit con provider/modello e soglie registrati, harness conservato come test e adapter sperimentali eliminati.
