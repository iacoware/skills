# Recipe App — Delivery plan

- **Sources:** `sources/goal.md`, `sources/concepts.md`, `sources/arch-choices.md`, `sources/tech-choices.md`.
- **Current state:** Greenfield, nessun repository. Stack deciso e chiuso (TypeScript, Next.js App Router, Effect, Drizzle, Auth.js + Google OAuth, React Query); infrastruttura decisa (Neon Postgres + pgvector, Cloudflare R2, embedding API multilingue, LLM cheap solo in fallback, Fly.io container con suspend + scale-to-zero). Scala attesa ≤10.000 ricette totali, centinaia per ricettario.
- **Assunzioni:** (a) `goal.md` dice "tutto entro free tier" mentre `arch-choices.md` dichiara che Fly non ha più free tier: si assume `arch-choices.md` (costo a consumo, centesimi/mese con suspend, ~$3/mese se sempre-calda). (b) Il modello di embedding è indicato come esempio, non come decisione: la slice 2 lo seleziona per misura.

## Ordering criteria

- Prerequisiti greenfield prima di tutto: repo con CI, poi il più sottile runtime deployato, senza auth, tenancy né dominio.
- Il differenziatore (ricerca semantica cross-lingua) è validato per primo sull'input reale più economico — fixture normalizzate — prima di costruirci sopra UI e import.
- Il boundary di scope (`cookbookId`) esiste dalla prima slice che persiste dati, risolto da un unico resolver; l'identità autenticata sostituisce lo scope configurato in quel seam alla slice 9.
- Eccezione a breadth-before-depth: il tema Import riceve tre slice consecutive (5–7) perché il link è il caso d'uso dichiarato più frequente e il fallback LLM è il secondo differenziatore.
- Correzione ed escape path prima dello stato che li richiede: l'edit (3) precede ogni estrazione automatica; l'errore preciso della 5 rimanda all'inserimento manuale finché la 7 non consegna il copia-incolla.
- `NOW` si chiude con la promozione in produzione perché gli utenti target sono familiari e amici, non solo sviluppatori.

## Themes

| Theme | Desired outcome | First validation |
|---|---|---|
| A. Cattura e consultazione ricette | Salvare una ricetta a mano e ritrovarla nell'elenco del ricettario | 3. Ricette a mano nel ricettario corrente |
| B. Ricerca semantica cross-lingua | Trovare una ricetta con parole proprie, anche in lingua diversa da quella della ricetta | 2. Motore semantico cross-lingua su corpus di fixture |
| C. Import a basso attrito | Aggiungere una ricetta da un link (o dal testo di una pagina) in pochi secondi | 5. Aggiunta da link con estrazione JSON-LD |
| D. Foto delle ricette | Riconoscere una ricetta a colpo d'occhio grazie a foto e cover | 8. Foto delle ricette e cover |
| E. Identità e ricettario condiviso | Familiari e amici accedono e collaborano sullo stesso ricettario | 9. Accesso con Google e ricettario di proprietà |

## Cross-functional concerns

- **Authorization:** ogni lettura e scrittura di ricette, foto e inviti passa da un unico resolver di scope corrente (`cookbookId`); nessuna query priva di scope, in nessuna slice.
- **Validation and errors:** ogni input non fidato (form, HTML remoto, output LLM, risposte API) è decodificato con `Schema`; errori attesi come `Data.TaggedError`, gestiti con `catchTag` solo al boundary; nessun cast di tipo.
- **Operability:** timeout e retry limitati su fetch pagina, LLM, embedding e R2; log strutturato per ogni passo della pipeline di add con esito ed errore; contatore di chiamate ed euro spesi su LLM/embedding.
- **Accessibility and security:** campi obbligatori non marcati, opzionali etichettati `(optional)`; progress e messaggi d'errore annunciati agli assistive tech; segreti solo server-side; URL fornito dall'utente validato contro fetch verso rete interna.
- **Data integrity and recovery:** l'embedding è indice derivato, rigenerato a ogni salvataggio; il fallimento di embedding o foto non blocca il salvataggio della ricetta (best-effort con retry e rigenerazione successiva); una sola cover per ricetta; duplicati consentiti per scelta.

## NOW

### 0. Repository e pipeline di verifica *(Enabler: delivery)*

---

**Includes**

- Monorepo Next.js + TypeScript con Effect, Drizzle e configurazione Prettier/ESLint di progetto.
- CI su push e PR: build, lint, typecheck, test (Vitest) come gate obbligatori.
- Un test verticale minimo (una route che risponde) per rendere la CI significativa.
- Nessun provisioning, nessun deploy, nessun segreto di ambiente.

**Verification**

- Una PR con errore di tipo, di lint o un test rosso fa fallire la CI; una PR sana passa.

**Outcome**

- Gli sviluppatori hanno un ciclo di feedback automatico su ogni modifica.

### 1. Scheletro deployato su Fly *(Enabler: delivery)*

---

**Includes**

- Dockerfile e `fly.toml` con `suspend` + scale-to-zero; app deployata in ambiente non-production.
- Deploy automatico dalla CI sul merge; rollback documentato al deploy precedente.
- Endpoint di health che espone versione del commit servito.
- Nessuna autenticazione, nessun database, nessun dominio applicativo.

**Verification**

- Un merge produce un'app raggiungibile via URL Fly che espone il commit atteso.
- Dopo inattività, la prima richiesta risponde e il tempo di risveglio viene misurato e registrato.

**Learning / risk**

- Conferma che il cold start con `suspend` sia tollerabile senza macchina sempre-calda.

**Outcome**

- Gli sviluppatori possono promuovere qualunque commit in un ambiente reale in un passo.

### 2. Motore semantico cross-lingua su corpus di fixture *(Enabler: ricerca semantica)*

---

**Includes**

- Schema Drizzle di `Cookbook` e `Recipe` su Neon con colonna `vector` e indice HNSW; migrazioni versionate.
- Servizio di embedding (porta `Context.Tag` + adapter Layer) che indicizza `nome + ingredients + steps` (+ `tags`/`prepTime` se presenti).
- Corpus di fixture con ricette reali in italiano e inglese, caricate attraverso la pipeline di persistenza di produzione.
- Comando diagnostico che, data una query, restituisce le ricette ordinate per similarità con score.
- Confronto di almeno due modelli multilingue candidati sullo stesso corpus, con scelta motivata.

**Verification**

- Query italiane ("pomodoro", "cena leggera") restituiscono in testa ricette in inglese pertinenti, e viceversa.
- Latenza della query di similarità e costo di indicizzazione per ricetta misurati e riportati.

**Learning / risk**

- Rischio esistenziale: senza cross-lingua utile il prodotto è una riscrittura di Mealie; qui si scopre al costo minimo, prima di qualunque UI.

**Outcome**

- Gli sviluppatori sanno se e con quale modello la ricerca semantica cross-lingua funziona alla scala prevista.

### 3. Ricette a mano nel ricettario corrente *(Theme: A)*

---

**Includes**

- Form unico crea/modifica: titolo, ingredienti, preparazione come testo libero, nessun parsing di quantità e unità.
- Elenco delle ricette del ricettario corrente e pagina di dettaglio.
- Resolver unico dello scope corrente, alimentato da un `cookbookId` configurato (seam per l'identità).
- Rigenerazione dell'embedding a ogni salvataggio tramite la pipeline della slice 2.

**Verification**

- Una ricetta creata compare nell'elenco e nel dettaglio; una modifica è visibile e ne aggiorna l'embedding.
- Una richiesta con `cookbookId` diverso da quello corrente non restituisce né modifica quelle ricette.

**Outcome**

- Un utente può inserire e correggere ricette e rivederle nel proprio ricettario.

### 4. Ricerca semantica nel ricettario *(Theme: B)*

---

**Includes**

- Campo di ricerca in home; risultati ordinati per similarità, scoped al ricettario corrente.
- Embedding della query calcolato a runtime solo sul testo digitato; nessuna chiamata LLM.
- Stati espliciti di ricerca vuota, nessun risultato ed errore del servizio di embedding.

**Verification**

- Con ricette reali IT ed EN nel ricettario, una query in italiano trova la ricetta inglese pertinente.
- Le ricette di un altro ricettario non compaiono mai tra i risultati.
- Tempo di risposta della ricerca misurato sull'ambiente deployato.

**Learning / risk**

- Verifica su dati inseriti dagli utenti, non su fixture, che la qualità del ranking regga fuori dal laboratorio.

**Outcome**

- Un utente ritrova una ricetta descrivendola con parole proprie, in qualsiasi lingua.

### 5. Aggiunta da link con estrazione JSON-LD *(Theme: C)*

---

**Includes**

- Incolla URL → fetch della pagina con `HttpClient`, timeout e retry, pulizia del contenuto.
- Parse del JSON-LD `schema.org/Recipe` validato con `Schema`; salvataggio immediato senza review.
- Progress sui passi reali (`Scarico pagina → Leggo ricetta → Trovo ingredienti → Salvo`) con stato per passo.
- Errori precisi e distinti per irraggiungibile, timeout, paywall e assenza di structured data, con rimando al form manuale.
- Persistenza di `sourceUrl`, `tags` e `prepTime` quando presenti nel JSON-LD.

**Verification**

- Un blog con JSON-LD produce una ricetta salvata e ricercabile senza alcuna chiamata LLM.
- Una pagina senza JSON-LD e una in timeout mostrano due messaggi distinti e corretti, senza record parziali.
- Hit-rate del JSON-LD misurato su un campione di siti realmente usati.

**Learning / risk**

- Il percorso gratuito copre la maggioranza dei casi: la misura decide quanto pesa il fallback a pagamento.

**Outcome**

- Un utente aggiunge una ricetta incollando un link, nel caso d'uso più frequente.

### 6. Fallback LLM quando manca lo structured data *(Theme: C)*

---

**Includes**

- Adapter LLM cheap con output strutturato validato con `Schema` sullo stesso modello Recipe dell'estrazione JSON-LD.
- Attivazione automatica del fallback nella cascata, con passo dedicato visibile nel progress.
- Gestione di output non conforme, troncato o vuoto: errore preciso, nessun salvataggio parziale.
- Tetto di token per richiesta e log di costo per estrazione.

**Verification**

- Una pagina priva di JSON-LD produce titolo, ingredienti e preparazione coerenti con la pagina.
- Un output LLM non conforme allo schema fallisce in modo esplicito e non crea ricette.
- Costo medio e latenza per estrazione misurati su un campione e confrontati con il target di spesa.

**Learning / risk**

- Secondo differenziatore rispetto a Mealie: qui si scopre se copre davvero i siti senza structured data, e a che prezzo.

**Outcome**

- Un utente aggiunge da link anche siti che nessuno scraper basato su structured data riesce a leggere.

### 7. Aggiunta da testo incollato *(Theme: C)*

---

**Includes**

- Ingresso alternativo che accetta il testo di una pagina e riusa motore, schema e progress dell'estrazione LLM.
- Salto esplicito del passo JSON-LD nel progress, perché non applicabile.
- Limite di lunghezza del testo con messaggio chiaro quando superato.

**Verification**

- Il testo copiato da una pagina paywall o JS-heavy produce una ricetta salvata e ricercabile.
- Il testo incollato e la stessa pagina via URL producono ricette equivalenti quando entrambe le vie sono possibili.

**Outcome**

- Un utente sblocca da solo i siti che il fetch automatico non può leggere.

### 8. Foto delle ricette e cover *(Theme: D)*

---

**Includes**

- Upload di foto multiple per ricetta su Cloudflare R2; nel DB solo l'URL.
- Cover: prima foto per default, cambiabile; una sola cover per ricetta.
- Cattura best-effort dell'immagine remota (`og:image` / JSON-LD) durante l'add da link, ricaricata su R2 per evitare hotlinking.
- Miniature cover nell'elenco e nei risultati di ricerca.
- Validazione di tipo e dimensione del file; fallimento della foto che non annulla il salvataggio della ricetta.

**Verification**

- Una ricetta con più foto mostra la cover attesa nell'elenco, e il cambio di cover si riflette subito.
- Un'immagine remota irraggiungibile lascia la ricetta salvata senza foto e senza errore bloccante.
- Le foto restano servite dopo che il sito di origine ha rimosso l'immagine.

**Outcome**

- Le ricette diventano riconoscibili a colpo d'occhio nell'elenco e nella ricerca.

### 9. Accesso con Google e ricettario di proprietà *(Theme: E)*

---

**Includes**

- Auth.js (NextAuth v5) con Google OAuth su Postgres; login, logout e sessione.
- Creazione automatica del primo `Cookbook` con `creatorId` e `Membership` del creator al primo accesso.
- Sostituzione, nell'unico resolver di scope, del `cookbookId` configurato con quello derivato dalla sessione e dalla membership.
- Redirect a login per ogni rotta applicativa; nessuna rotta di ricette raggiungibile da anonimo.

**Verification**

- Un utente non autenticato non accede ad alcuna ricetta, né via UI né via richiesta diretta.
- Due utenti Google distinti vedono ricettari distinti; nessuno vede le ricette dell'altro.
- Le ricette create prima dell'autenticazione restano associate al ricettario di destinazione atteso.

**Outcome**

- Ogni persona accede con il proprio account Google e lavora sul proprio ricettario reale.

### 10. Inviti e ricettari condivisi *(Theme: E)*

---

**Includes**

- Creazione di ricettari aggiuntivi e generazione di un `Invitation` con token condivisibile (link/codice) e scadenza opzionale.
- Apertura dell'invito da utente loggato → creazione della `Membership`; tutti i membri pari in lettura e scrittura.
- Selettore del ricettario corrente per utenti appartenenti a più ricettari, con scope propagato a elenco, ricerca e add.
- Gestione di invito scaduto, già usato o revocato con messaggi distinti.

**Verification**

- Un secondo utente apre il link e vede, modifica e cerca le ricette del ricettario condiviso.
- Un utente in due ricettari cambia scope e ottiene elenchi e risultati di ricerca disgiunti.
- Un token scaduto o revocato non crea membership e non espone alcuna ricetta.

**Outcome**

- Famiglia e amici collaborano sullo stesso ricettario partendo da un link.

### 11. Promozione in produzione per famiglia e amici *(Release: delivery)*

---

**Includes**

- App di produzione su Fly con `suspend` + scale-to-zero, dominio e HTTPS; credenziali Google OAuth di produzione.
- Segreti di produzione separati (Neon, R2, LLM, embedding) e migrazioni eseguite in modo controllato.
- Backup del database e verifica del ripristino; monitoraggio dei limiti dei free tier di Neon e R2.
- Dashboard o report minimo di spesa mensile su Fly, LLM ed embedding.

**Verification**

- Un familiare accede dal dominio pubblico, aggiunge una ricetta da link e la ritrova con la ricerca semantica.
- Un ripristino di backup su ambiente non-production restituisce ricette e foto coerenti.
- La spesa reale del primo periodo d'uso è misurata e confrontata con il target di centesimi/mese.

**Outcome**

- Il ricettario condiviso è utilizzabile in produzione dagli utenti reali previsti.

## LATER

- **Filtri di ricerca strutturati (tag, tempo) e ricerca ibrida semantica + full-text**
  - **Promotion trigger:** query reali che la sola semantica sbaglia o non discrimina, osservate dopo le slice 4 e 6.
  - **Expected value:** precisione su intenti espliciti; i campi si popolano già dalla slice 5, quindi nessuna migrazione né lavoro retroattivo.
- **Macchina Fly sempre-calda (`min_machines_running=1`)**
  - **Promotion trigger:** cold start misurato nelle slice 1 e 11 percepito come fastidioso dagli utenti reali.
  - **Expected value:** latenza costante al primo accesso, al costo di ~$3/mese; è un flag reversibile in `fly.toml`.
- **Concetto di gruppo sopra i ricettari**
  - **Promotion trigger:** dopo la slice 10, ri-invitare le stesse persone su più ricettari risulta ripetitivo nell'uso reale.
  - **Expected value:** riduce l'attrito di condivisione senza toccare il modello cookbook-centrico, in modo additivo.
- **Ricettari pubblici tematici (`visibility=public`)**
  - **Promotion trigger:** richiesta di condividere un ricettario oltre la cerchia invitata.
  - **Expected value:** abilitabile sul campo `visibility` già previsto, senza migrazione.
- **Passkeys come metodo di accesso**
  - **Promotion trigger:** supporto Auth.js maturo e percorso di recupero account su dispositivo perso definito.
  - **Expected value:** accesso più rapido per l'utente ricorrente, senza dipendenza da Google.

## OUT-OF-SCOPE

- **Ricerca cross-ricettario** — lo scope della ricerca è il ricettario corrente per scelta di semplicità.
- **Ruoli e permessi granulari** — nell'MVP il solo "ruolo" è `Cookbook.creatorId` e i membri sono pari.
- **Lista della spesa e scaling porzioni** — richiedono ingredienti strutturati in quantità/unità, trade-off esplicitamente accettato.
- **Normalizzazione di ingredienti e passi** — la ricerca è semantica e chi legge interpreta il testo libero.
- **Review obbligatoria prima del salvataggio** — l'estratto si salva subito, la correzione avviene dopo tramite edit.
- **Email+password e magic-link** — entrambi richiedono un provider email, in conflitto con il vincolo di costo dell'MVP.
- **Deduplica delle ricette** — due membri possono linkare la stessa ricetta nello stesso ricettario, per scelta.
- **Vector DB dedicato (Pinecone/Qdrant/Weaviate)** — a ≤10k ricette pgvector con HNSW basta; sarebbe infra e costo in più.
- **IaC versionata (Terraform/SST)** — `fly.toml` + CLI Fly bastano per l'MVP.

## Decision checkpoints

- **Dopo 2:** qualità del ranking cross-lingua e costo di indicizzazione → cambiare modello di embedding, oppure promuovere la ricerca ibrida da `LATER` prima della slice 4, o fermare l'investimento sul differenziatore.
- **Dopo 4:** ranking su ricette inserite da utenti reali → riordinare il resto di `NOW` se serve prima un miglioramento della ricerca che nuove sorgenti di import.
- **Dopo 5:** hit-rate misurato del JSON-LD sui siti realmente usati → se alto, ridurre l'ambizione della slice 6; se basso, tenerla immediatamente adiacente e ampliarne i test.
- **Dopo 6:** costo, latenza e tasso di output non conforme dell'LLM → conferma o revisione del modello scelto e del target di spesa.
- **Dopo 10:** attrito osservato del ri-invito su più ricettari → promuovere o archiviare il concetto di gruppo.
- **Dopo 11:** cold start e spesa reali in produzione → attivare la macchina sempre-calda o restare a scale-to-zero.
