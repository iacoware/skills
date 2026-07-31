# Recipe App — Piano di rilascio

- **Sources:** `sources/goal.md` (visione, MVP, posizionamento, auth, fuori scope), `sources/concepts.md` (entità, pipeline di estrazione, ricerca), `sources/arch-choices.md` (Postgres+pgvector, R2, embeddings, estrazione a cascata, Fly.io, costi), `sources/tech-choices.md` (Next.js, Effect, Auth.js+Google, React Query, Drizzle, convenzioni UI).
- **Current state:** greenfield — nessun repository, nessun ambiente, nessun dato. Le scelte di stack sono decise; restano aperti solo i fornitori elencati in `Open questions`. Scala attesa ≤10k ricette totali, centinaia per ricettario.

## Ordering criteria

- Il differenziatore è la ricerca semantica cross-lingua: va validato per primo, perché senza di esso il prodotto è una riscrittura di Mealie.
- L'input reale più economico batte l'input più comodo: il motore di ricerca si valida con fixture multilingue attraverso persistenza ed embedding reali, non aspettando la UI di inserimento.
- Vincolo di costo permanente: ogni slice resta nel free tier; LLM ed embedding solo in fase di add o edit, mai a runtime sulle query.
- Attrito minimo in aggiunta: nessun passo di review obbligatorio prima del salvataggio; la correzione è una capability separata, non un passo del flusso di add.
- Prima il percorso di consegna minimo, poi il rischio esistenziale, poi le capability per frequenza d'uso; slice iniziali strette finché convenzioni di delivery, test, Effect e UI non sono consolidate.

## Themes

| Theme | Desired outcome | First validation |
|---|---|---|
| A. Ricerca semantica cross-lingua | Descrivo un piatto a parole mie e trovo la ricetta giusta anche se è scritta in un'altra lingua | 3. Ricerca semantica cross-lingua nel ricettario |
| B. Ricettario leggibile e curabile a mano | Le ricette sono consultabili per cucinare e correggibili in qualsiasi momento | 4. Elenco e lettura della ricetta |
| C. Accesso e ricettario proprio | Entro con il mio account Google e vedo solo le ricette che mi riguardano | 5. Accesso con Google e ricettario personale |
| D. Cattura automatica da fonti esterne | Aggiungere una ricetta trovata online costa un incollaggio, anche quando il sito non collabora | 7. Aggiunta da link con dati strutturati |
| E. Foto delle ricette | Ogni ricetta è riconoscibile a colpo d'occhio senza lavoro manuale | 10. Foto della ricetta e cover |
| F. Condivisione del ricettario | Famiglia e amici contribuiscono allo stesso ricettario da pari | 12. Condivisione del ricettario tramite invito |

## Cross-functional concerns

- **Authorization:** ogni lettura e scrittura di ricette, foto e inviti è filtrata per `cookbookId` su cui l'utente ha `Membership`; un id fuori scope risponde 404. Nessun ruolo oltre `Cookbook.creatorId`, che abilita solo la generazione degli inviti.
- **Validation and errors:** ogni input non fidato (HTML remoto, output LLM, risposte API, payload di form) è decodificato con `Schema`, mai asserito; errori applicativi come `Data.TaggedError` gestiti con `catchTag` al boundary; nessun salvataggio parziale quando la decodifica fallisce.
- **Operability:** timeout e retry espliciti su fetch pagina, LLM ed embedding; log strutturato per ogni passo della pipeline di add con esito, durata e token consumati; l'avanzamento mostrato all'utente riflette i passi reali e nomina il passo fallito.
- **Accessibility and security:** campi obbligatori non marcati con asterisco, opzionali marcati `(optional)` ed esposti alle tecnologie assistive; chiavi LLM, embedding e storage solo come secret di runtime; token di invito ad alta entropia con `expiresAt`.

## NOW

### 0. Prerequisito repository e CI *(Enabler: delivery)*

---

**Includes**

- Repository Next.js (App Router) e TypeScript, con Prettier ed ESLint secondo le convenzioni di progetto.
- Vitest con un test co-locato di esempio (`test`, niente `describe`/`it`).
- Workflow CI che esegue build, lint, typecheck e test.
- Nessun provisioning, nessun deploy, nessuna entità di dominio.

**Verification**

- CI verde su un PR di prova.
- Un errore di tipo e un test rotto introdotti ad arte fanno fallire la pipeline.

**Outcome**

- Uno sviluppatore ottiene su ogni push un verdetto automatico di build, lint, typecheck e test.

### 1. Scheletro deployato su Fly.io con Postgres e pgvector *(Enabler: delivery)*

---

**Includes**

- Dockerfile e `fly.toml` con `suspend` e scale-to-zero; container stateless.
- Postgres gestito con estensione `pgvector`, Drizzle su driver TCP e prima migrazione.
- Rotta `/health` che esegue una query reale e riporta la versione di migrazione applicata.
- Deploy eseguito dalla CI con secret gestiti da Fly.
- Nessuna autenticazione, nessuna entità di dominio, nessuna UI di prodotto.

**Verification**

- Dopo un deploy da CI, `/health` risponde 200 con l'esito della query e la versione di migrazione.
- Tempo di risveglio dopo scale-to-zero misurato e annotato come baseline.

**Learning / risk**

- Latenza reale del cold start con `suspend` e tenuta della connessione TCP Node → Postgres gestito.

**Outcome**

- Uno sviluppatore raggiunge l'app deployata su un ambiente non di produzione e ne verifica la connessione reale al database.

### 2. Indicizzazione semantica di ricette fixture *(Enabler: ricerca semantica)*

---

**Includes**

- Schema Drizzle di `Cookbook` e `Recipe` (nome, ingredienti, steps, `prepTime?`, `tags`, `sourceUrl?`), colonna `vector` e indice HNSW.
- Servizio `Embeddings` come `Context.Tag` con layer adapter verso l'API cloud multilingue.
- Comando di seed che ingerisce fixture normalizzate attraverso persistenza ed embedding reali, senza vettori precalcolati.
- Comando di query che embedda una frase in linguaggio naturale e stampa i top-k con score, scoped a un `cookbookId`.

**Verification**

- Seed di ricette in almeno tre lingue; "cena leggera" e "pomodoro" restituiscono nelle prime posizioni fixture scritte in inglese.
- Le ricette di un secondo cookbook di fixture non compaiono nei risultati scoped.
- Costo in token dell'ingest e latenza della query registrati.

**Learning / risk**

- Rischio esistenziale: se il retrieval cross-lingua non regge, il differenziatore non esiste e il prodotto va rimesso in discussione.
- Qualità dell'embedder multilingue scelto e comportamento dell'indice HNSW alla scala prevista.

**Outcome**

- Uno sviluppatore carica ricette fixture multilingue e ottiene da riga di comando un ranking per similarità prodotto dalla pipeline reale.

### 3. Ricerca semantica cross-lingua nel ricettario *(Theme: A)*

---

**Includes**

- Home con campo di ricerca e lista risultati ordinata per similarità (titolo ed estratto degli ingredienti).
- Endpoint server che embedda la query e interroga pgvector, scoped al `cookbookId` corrente, in questa slice selezionato per configurazione.
- Data fetching client con React Query; stati vuoto, in corso ed errore dell'API di embedding.

**Verification**

- Da browser, una query in italiano restituisce una ricetta seed in inglese.
- Ricette di un altro cookbook non compaiono mai nei risultati.
- Latenza percepita misurata; nessuna chiamata LLM nei log della ricerca.

**Learning / risk**

- La sola ricerca semantica basta senza filtri strutturati? La risposta decide la promozione dei filtri da `LATER`.

**Outcome**

- Chi usa l'app descrive un piatto a parole proprie e ottiene le ricette pertinenti del ricettario corrente, anche se scritte in un'altra lingua.

### 4. Elenco e lettura della ricetta *(Theme: B)*

---

**Includes**

- Home con elenco delle ricette del ricettario corrente.
- Pagina di dettaglio con nome, ingredienti e preparazione resi come testo libero a righe.
- Collegamento dai risultati di ricerca al dettaglio.
- Risposta 404 per una ricetta fuori dal ricettario corrente.

**Verification**

- L'elenco mostra le ricette seed e il dettaglio rende correttamente righe di ingredienti e passi.
- Un risultato di ricerca apre il dettaglio corrispondente.
- L'id di una ricetta di un altro cookbook restituisce 404.

**Outcome**

- Chi usa l'app vede l'elenco delle ricette del ricettario e ne apre una per cucinarla.

### 5. Accesso con Google e ricettario personale *(Theme: C)*

---

**Includes**

- Auth.js (NextAuth v5) con provider Google e tabelle di sessione su Postgres via Drizzle; login e logout.
- Creazione al primo accesso di un `Cookbook` con `creatorId` e della relativa `Membership`.
- Scope di elenco, dettaglio e ricerca derivato dalla membership dell'utente autenticato; rotte di prodotto protette con redirect al login.
- Credenziali OAuth per l'ambiente non di produzione.

**Verification**

- L'utente A non vede né cerca le ricette dell'utente B.
- L'accesso anonimo alle rotte di prodotto reindirizza al login.
- Un secondo accesso dello stesso utente non crea un secondo ricettario.

**Learning / risk**

- Coesione deliberata: identità e scope sono un unico esito osservabile, perché un utente autenticato senza ricettario non produce comportamento verificabile.

**Outcome**

- Un utente entra con il proprio account Google e vede il proprio ricettario privato al posto dei dati di fixture.

### 6. Aggiunta manuale e modifica della ricetta *(Theme: B)*

---

**Includes**

- Un unico form per creazione (campi vuoti) e modifica (precompilato): nome, ingredienti e preparazione come testo libero, senza parsing di quantità e unità.
- Salvataggio immediato senza passi obbligatori; nome come unico campo richiesto.
- Rigenerazione dell'embedding a ogni salvataggio da nome, ingredienti, preparazione e, se presenti, tag e tempo.

**Verification**

- Una ricetta creata a mano compare in elenco ed è trovabile con una query semantica che non ne ripete le parole.
- La modifica del testo cambia il ranking della stessa query, a conferma della reindicizzazione.
- Il salvataggio non richiede alcun campo oltre al nome.

**Outcome**

- Un membro salva una ricetta che conosce e corregge in seguito qualsiasi ricetta del ricettario.

### 7. Aggiunta da link con dati strutturati *(Theme: D)*

---

**Includes**

- Fetch della pagina con `HttpClient` di Effect (timeout, retry, user-agent).
- Parse del JSON-LD `schema.org/Recipe` validato con `Schema` e mappato su `Recipe`, con `prepTime`, `tags` e `sourceUrl` best-effort.
- Salvataggio ed embedding sul percorso della slice 6, senza passo di review.
- Avanzamento sui passi reali (`Scarico pagina → Leggo ricetta → Salvo`) con messaggio specifico per il passo fallito: timeout, 403 o paywall, JSON-LD assente.

**Verification**

- URL con JSON-LD: ricetta salvata e apribile, `sourceUrl` valorizzato, zero chiamate LLM nei log.
- URL protetto da paywall: messaggio preciso sul passo di download e nessuna ricetta creata.
- URL senza JSON-LD: messaggio che indirizza al copia-incolla finché il fallback non esiste.

**Learning / risk**

- Hit-rate reale del JSON-LD sui siti effettivamente usati dal gruppo: determina quanto pesa il fallback LLM sul costo.

**Outcome**

- Un membro incolla l'URL di un food blog e ottiene la ricetta salvata senza review, con avanzamento sui passi reali.

### 8. Estrazione LLM in fallback *(Theme: D)*

---

**Includes**

- Servizio `Extraction` come `Context.Tag` con layer verso un LLM cheap a output strutturato, validato con `Schema`.
- Pulizia del contenuto HTML in testo prima del prompt.
- Innesto del fallback nel passo `Leggo ricetta` della pipeline esistente, senza nuovo flusso.
- Log di token e costo per estrazione; errore tipizzato quando l'output non valida.

**Verification**

- Su un campione annotato di URL senza JSON-LD, la ricetta salvata contiene ingredienti e preparazione corretti.
- Output LLM non conforme allo schema: messaggio preciso, nessun salvataggio parziale.
- Costo medio per estrazione registrato e confrontato con la soglia di budget.

**Outcome**

- Anche le pagine senza dati strutturati producono una ricetta salvata, senza intervento dell'utente.

### 9. Aggiunta da testo incollato *(Theme: D)*

---

**Includes**

- Ingresso "testo incollato" nel flusso di add, che salta fetch e JSON-LD e riusa il motore di estrazione della slice 8.
- Avanzamento ridotto ai passi realmente eseguiti.
- `sourceUrl` opzionale compilabile a mano.

**Verification**

- Il testo copiato da una pagina con paywall produce una ricetta salvata e trovabile.
- Un testo che non è una ricetta produce un errore preciso senza salvataggio.

**Outcome**

- Quando il link non è leggibile, un membro incolla il testo della pagina e ottiene la stessa ricetta salvata.

### 10. Foto della ricetta e cover *(Theme: E)*

---

**Includes**

- Servizio `Storage` come `Context.Tag` con layer verso l'object storage; upload lato server e URL salvato su `Photo`.
- Upload multiplo dal form di modifica; prima foto cover per default, cover cambiabile, invariante di una sola cover per ricetta.
- Cover mostrata in elenco e in dettaglio, con placeholder quando assente.
- Limiti di tipo e dimensione con errore specifico.

**Verification**

- Caricando due foto la prima diventa cover e il cambio di cover si riflette in elenco.
- Un file oltre il limite viene rifiutato con messaggio comprensibile e nessuna riga `Photo` creata.
- Le foto restano servibili dopo un redeploy, a conferma del container stateless.

**Outcome**

- Un membro carica una o più foto di una ricetta e sceglie quale la rappresenta in elenco.

### 11. Foto acquisita automaticamente dall'import *(Theme: E)*

---

**Includes**

- Estrazione dell'immagine da `schema.org/Recipe` o `og:image`, download e ricarica sul proprio storage come cover, senza hotlinking.
- Passo `Salvo foto` aggiunto all'avanzamento reale.
- Fallimento del download non bloccante: la ricetta si salva comunque.

**Verification**

- Import di un URL con immagine: la cover è servita dal proprio storage, non dal dominio di origine.
- Immagine irraggiungibile o oltre limite: ricetta salvata senza foto e avviso non bloccante.

**Outcome**

- Le ricette importate da link arrivano già con la foto, senza alcun lavoro dell'utente.

### 12. Condivisione del ricettario tramite invito *(Theme: F)*

---

**Includes**

- Generazione e rigenerazione di `Invitation` (token, `expiresAt`) dal ricettario.
- Pagina di accettazione che richiede login e crea la `Membership`; link riusabile finché valido.
- Selettore di ricettario quando l'utente appartiene a più di uno; elenco, ricerca e aggiunta seguono il ricettario selezionato.
- Errori specifici per token scaduto, sconosciuto o già usato dallo stesso utente.

**Verification**

- B accetta l'invito di A, vede ed edita le ricette del ricettario di A, e A vede le modifiche di B.
- B passa dal proprio ricettario a quello condiviso e i risultati di ricerca cambiano scope di conseguenza.
- Token scaduto: nessuna `Membership` creata e messaggio preciso.

**Outcome**

- Il creator condivide un link e chi lo apre entra nel ricettario come membro pari, leggendo ed editando tutto.

### 13. Rilascio in produzione al gruppo pilota *(Enabler: delivery)*

---

**Includes**

- App di produzione con dominio e certificato, promossa dalla CI dopo la pipeline verde.
- Credenziali OAuth Google di produzione, bucket storage e database separati dall'ambiente di verifica.
- Secret e chiavi LLM ed embedding di produzione con tetto di spesa e allarme di superamento.
- Backup del database con prova di ripristino; `suspend` e scale-to-zero attivi.

**Verification**

- Due utenti reali completano in produzione add da link, ricerca semantica, modifica e condivisione.
- Costo del primo mese misurato e confrontato con il target di centesimi al mese.
- Ripristino di un backup verificato su ambiente non di produzione.

**Outcome**

- Famiglia e amici usano l'app su un ambiente di produzione stabile, entro il budget dichiarato.

## LATER

- **Filtri strutturati di ricerca (tag, tempo) e ricerca ibrida semantica + full-text**
  - **Promotion trigger:** query reali che la sola semantica sbaglia sistematicamente, tipo "senza glutine" o "meno di 30 minuti", osservate dopo la slice 3.
  - **Expected value:** `tags` e `prepTime` sono già popolati dalla slice 2 in poi, quindi attivabili senza migrazione né lavoro retroattivo.
- **Ricerca cross-ricettario**
  - **Promotion trigger:** utenti con più ricettari che cercano ripetutamente nello scope sbagliato dopo la slice 12.
  - **Expected value:** elimina il cambio di contesto manuale quando i ricettari si moltiplicano.
- **Creazione di ricettari aggiuntivi dall'interfaccia**
  - **Promotion trigger:** un gruppo chiede di separare i contenuti oltre al ricettario creato al primo accesso.
  - **Expected value:** il modello N:N esiste già, serve solo l'interazione di creazione.
- **Cancellazione della ricetta**
  - **Promotion trigger:** import errati o duplicati che degradano elenco e ricerca durante il pilota.
  - **Expected value:** igiene del ricettario senza intervento diretto sul database.
- **Macchina sempre calda (`min_machines_running=1`)**
  - **Promotion trigger:** cold start misurato nelle slice 1 e 13 percepito come fastidioso dagli utenti pilota.
  - **Expected value:** elimina la latenza del primo accesso al costo noto di ~$3/mese, con un flag reversibile in `fly.toml`.
- **Ricettari pubblici tematici (`visibility=public`)**
  - **Promotion trigger:** richiesta di condividere un ricettario fuori dal gruppo invitato.
  - **Expected value:** il campo `visibility` esiste dalla slice 2, quindi è abilitabile senza migrazione.
- **Concetto di gruppo o team sopra i ricettari**
  - **Promotion trigger:** ri-invitare gli stessi membri a ogni nuovo ricettario diventa un attrito segnalato.
  - **Expected value:** additivo sopra `Membership`, senza riscrivere il modello.

## OUT-OF-SCOPE

- **Ingredienti strutturati (quantità e unità)** — trade-off accettato in `goal.md`: la ricerca è semantica e chi legge interpreta il testo, quindi la normalizzazione fine non paga l'attrito che introduce.
- **Lista della spesa e scaling delle porzioni** — dipendono dagli ingredienti strutturati, già esclusi.
- **Review obbligatoria dell'estratto prima del salvataggio** — bloccare l'utente a ogni aggiunta è esattamente il costo che il prodotto elimina; la correzione resta disponibile come edit.
- **Deduplica delle ricette** — duplicati consentiti per scelta esplicita in `concepts.md`.
- **Email + password e magic link** — richiedono comunque un provider email, in conflitto con "niente provider email in MVP".
- **Passkeys** — recupero account su dispositivo perso complesso e supporto Auth.js ancora acerbo.
- **Ruoli e permessi granulari** — nell'MVP basta `creatorId` e tutti i membri sono pari.
- **Vector DB dedicato (Pinecone, Qdrant, Weaviate)** — a ≤10k ricette pgvector con HNSW è già istantaneo: sarebbe infra e costo senza beneficio.
- **IaC versionata (SST, Terraform)** — over-engineering per l'MVP: bastano `fly.toml` e la CLI.
- **Hosting su Vercel o Cloudflare Workers** — costi oltre l'Hobby nel primo caso, vincoli di bundle e driver serverless nel secondo.

## Decision checkpoints

- **Dopo la 2:** qualità del ranking cross-lingua sulle fixture → se debole, spike su un embedder alternativo prima di costruire la UI di ricerca; se irrecuperabile, cade il differenziatore e va rimessa in discussione la proposta di valore.
- **Dopo la 3:** query reali e loro esito → promuovere i filtri strutturati da `LATER` oppure confermare la sola semantica per l'MVP.
- **Dopo la 7:** hit-rate del JSON-LD sul campione realmente usato → se alto, la slice 8 si restringe al minimo; se basso, anticipare 8 e 9 rispetto a foto e condivisione.
- **Dopo la 8:** costo medio per estrazione → se sopra soglia, cambiare modello o limitare il fallback ai casi espliciti.
- **Dopo la 13:** cold start e costo misurati sugli utenti pilota → promuovere la macchina sempre calda da `LATER` o restare su scale-to-zero.

## Open questions

- Provider Postgres: Neon o Supabase. Blocca la slice 1, perché differiscono per connessione, limiti di free tier e strumenti di backup.
- Modello di embedding: `text-embedding-3-small` è indicato per costo, ma la qualità cross-lingua richiesta dal differenziatore non è verificata. Blocca la slice 2 e può introdurre un provider diverso da quello dell'LLM.
- Modello LLM per l'estrazione in fallback: la classe è decisa (cheap, Haiku-class con output strutturato), il provider concreto no. Blocca la slice 8 e il tetto di spesa della slice 13.
