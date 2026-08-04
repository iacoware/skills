# Recipe App — Delivery plan

- **Sources:** `sources/goal.md`, `sources/concepts.md`, `sources/arch-choices.md`, `sources/tech-choices.md`.
- **Current state:** greenfield, nessun repository esistente; stack e infrastruttura decisi salvo le voci in `Open questions`.

## Ordering criteria

- Prima la catena minima di consegna (repository, poi runtime deployato con datastore reale): ogni slice successiva ne dipende e la revisione umana è ancora frequente.
- Subito dopo il differenziatore: la ricerca semantica cross-lingua è validata sull'input reale più economico (ricette inserite a mano), prima di qualsiasi approfondimento sull'import.
- Identità rimandata solo finché serve a quella validazione: fino allo slice 4 lo scope è risolto da `currentCookbook` configurato e il pubblico è sviluppatori/tester sull'ambiente non pubblico; nessuna behaviour rivolta a utenti reali precede lo slice 5.
- Il recupero richiesto batte l'ampiezza: gli slice 7 e 8 sono i rimedi dichiarati dalle sorgenti per i fallimenti nominati dallo slice 6 e lo seguono prima di aprire un altro tema.
- Le pipeline condivise seguono i loro produttori e hanno un solo owner: l'indice semantico è generato dall'unico punto di persistenza della ricetta; lo storage foto apre dopo tutti i percorsi che lo alimentano.
- Sui temi rimanenti, una slice sottile per tema prima di approfondirne uno; nessuna slice è più grande solo perché arriva più tardi.

## Themes

| Theme | Desired outcome | First validation |
|---|---|---|
| A. Ricettario e cattura manuale | Chi conosce una ricetta la scrive e la ritrova in un elenco consultabile | 2. Ricette a mano nel ricettario corrente |
| B. Import automatico dal web | Aggiungere una ricetta trovata online costa un incolla di URL | 6. Aggiunta da link con dati strutturati |
| C. Ricerca semantica cross-lingua | Si trova una ricetta per significato, anche se scritta in un'altra lingua | 4. Ricerca semantica nel ricettario corrente |
| D. Foto delle ricette | Ogni ricetta ha immagini proprie e una copertina | 10. Foto delle ricette |
| E. Identità e accesso | Ogni persona entra con Google e possiede il proprio ricettario | 5. Accesso con Google e ricettario personale |
| F. Condivisione del ricettario | Famiglia e amici collaborano su uno stesso ricettario | 9. Ricettari condivisi su invito |

## Cross-functional concerns

- **Authorization:** ogni lettura e scrittura passa dall'unico risolutore `currentCookbook`; è configurato fino allo slice 4 e diventa derivato dalla sessione allo slice 5, che è il seam unico del passaggio; essere membro significa leggere ed editare tutto, nessun ruolo.
- **Validation and errors:** l'output di estrazione LLM e le risposte esterne si validano con `Schema`, mai con cast; errori come `Data.TaggedError`, gestiti solo ai boundary; ogni passo del progress ha un messaggio di fallimento specifico, mai generico.
- **Operability:** timeout e limiti di dimensione su fetch pagina, LLM ed embedding; log strutturati di esito, passo fallito, latenza e costo di ogni estrazione; retry solo dove idempotente; cold start da scale-to-zero accettato e misurato.
- **Accessibility and security:** URL forniti dall'utente trattati come ostili (guard SSRF, no indirizzi interni, content-type e dimensione limitati); segreti solo in Fly secrets; nei form i campi obbligatori non marcati e gli opzionali etichettati `(optional)`; progress e stati di errore esposti alle assistive technology.
- **Data integrity and recovery:** l'embedding è indice derivato, rigenerato a ogni write dall'unico owner della persistenza ricetta; un suo fallimento non blocca il salvataggio ma marca la ricetta da reindicizzare; una sola cover per ricetta; duplicati consentiti, nessuna deduplica.

## NOW

### 0. Fondamenta di repository *(Enabler: delivery)*

---

**Includes**

- Progetto Next.js App Router in TypeScript strict, con Effect e Drizzle installati e convenzioni di progetto attive.
- Lint, format, typecheck e Vitest con un test di esempio co-locato.
- CI su ogni push che esegue build, lint, typecheck e test.
- Nessun provisioning e nessun deploy.

**Verification**

- La CI passa su una PR e fallisce se un test o il typecheck falliscono.
- Gli stessi comandi sono riproducibili in locale con un solo script.

**Outcome**

- Gli sviluppatori hanno una base di consegna verificabile su cui aprire la prima slice di prodotto.

### 1. Runtime deployato con Postgres reale *(Enabler: delivery)*

---

**Includes**

- Dockerfile e `fly.toml` con `suspend` e scale-to-zero; deploy dalla CI su un ambiente non pubblico.
- Migration runner Drizzle che applica una migrazione non di dominio (tabella tecnica di health).
- Endpoint di health che scrive e rilegge quella tabella sul Postgres gestito scelto, attraverso il driver e la modalità di connessione reali (vedi `Open questions`).
- Nessuna entità di dominio, nessuna autenticazione, nessun adapter esterno.

**Verification**

- Deploy eseguito dalla CI; l'endpoint risponde includendo l'esito del round trip sul database.
- Le migrazioni si applicano da zero su un database pulito e sono idempotenti a una seconda esecuzione.
- Latenza del primo accesso dopo scale-to-zero misurata e registrata come baseline.

**Outcome**

- L'infrastruttura decisa è connessa e in esecuzione, con rischio di driver, connessione e migrazioni separato dal dominio.

### 2. Ricette a mano nel ricettario corrente *(Theme: A)*

---

**Includes**

- Schema e migrazioni per `Cookbook` e `Recipe`; risolutore `currentCookbook` configurato su un ricettario di seed.
- Form condiviso creazione ed edit: titolo, ingredienti e preparazione come testo libero, nessun parsing di quantità e unità.
- Elenco delle ricette del ricettario corrente e pagina di dettaglio.

**Verification**

- Creare, editare e riaprire una ricetta sull'ambiente non pubblico; il testo libero sopravvive intatto al round trip.
- Con due ricettari di seed, elenco e dettaglio restano confinati a quello risolto, incluso l'accesso diretto per id.
- Due ricette identiche coesistono senza deduplica.

**Outcome**

- Sviluppatori e tester memorizzano e rileggono ricette reali sull'ambiente non pubblico, producendo il corpus che serve alla validazione della ricerca.

### 3. Indice semantico sulle ricette reali *(Enabler: ricerca semantica)*

---

**Includes**

- Colonna `embedding` pgvector con indice HNSW e generazione dell'embedding dall'unico punto di persistenza della ricetta, su create e su edit.
- Testo indicizzato da nome, ingredienti e preparazione, con tag e tempo quando presenti.
- Comando diagnostico che ordina per similarità le ricette del ricettario corrente data una query testuale.
- Rigenerazione on-demand delle ricette marcate come non indicizzate.

**Verification**

- Su ricette reali italiane e inglesi dello slice 2, una query italiana porta in top-k la ricetta inglese corrispondente.
- L'edit di una ricetta cambia il ranking di conseguenza; una ricetta salvata con embedder non disponibile risulta marcata e viene recuperata dalla rigenerazione.
- Costo e latenza della generazione per ricetta misurati sul corpus.

**Learning / risk**

- Il recall cross-lingua dell'embedder multilingue scelto è il rischio esistenziale del prodotto: senza di esso il piano riscrive alternative già mature.

**Outcome**

- Gli sviluppatori osservano la qualità reale del recupero cross-lingua prima di investire in interfaccia.

### 4. Ricerca semantica nel ricettario corrente *(Theme: C)*

---

**Includes**

- Campo di ricerca in home con risultati ordinati per similarità e stato vuoto esplicito.
- Query embeddata e confrontata in una sola interrogazione Postgres, con scope al ricettario risolto.
- Strumentazione di latenza, numero di chiamate esterne e costo per query.

**Verification**

- Query come "cena leggera" o "pomodoro" recuperano ricette scritte in un'altra lingua sull'ambiente non pubblico.
- Nessun risultato proviene da un altro ricettario, nemmeno per termini che vi compaiono.
- Embedder non raggiungibile produce un messaggio comprensibile e nessun crash della home.
- Latenza p95 e chiamate per query registrate e confrontate con il costo atteso.

**Learning / risk**

- Le sorgenti si contraddicono sull'ammissibilità di una chiamata di embedding a runtime per query (vedi `Open questions`): la strumentazione fornisce l'evidenza per decidere cache o pre-calcolo senza anticipare la decisione.

**Outcome**

- Chi prova l'app sull'ambiente non pubblico ritrova ricette per significato, non per parola chiave.

### 5. Accesso con Google e ricettario personale *(Theme: E)*

---

**Includes**

- Auth.js con Google OAuth e sessione persistita su Postgres.
- `Membership` e `Cookbook.creatorId`; al primo accesso viene creato il ricettario personale dell'utente.
- Il risolutore `currentCookbook` passa da configurato ad autenticato in quell'unico seam; le rotte applicative richiedono una sessione.
- Trattamento esplicito delle ricette di seed pre-identità: assegnate a un account reale o rimosse.

**Verification**

- Due account Google reali vedono, cercano ed editano solo le ricette del proprio ricettario.
- L'accesso diretto per id a una ricetta altrui è negato e non distingue "inesistente" da "non tuo".
- La sessione sopravvive a un redeploy e il logout la invalida.

**Outcome**

- Le persone entrano con il proprio account Google e possiedono il proprio ricettario, senza password né email da gestire.

### 6. Aggiunta da link con dati strutturati *(Theme: B)*

---

**Includes**

- Input URL, fetch della pagina e pulizia del contenuto, con progress sincrona sui passi realmente eseguiti.
- Parse del JSON-LD `schema.org/Recipe` senza chiamate LLM, con `sourceUrl` conservato.
- Salvataggio immediato senza review; tag e tempo derivati best-effort quando presenti, mai richiesti.

**Verification**

- Un URL con JSON-LD produce in una sola interazione una ricetta salvata, apribile e già ricercabile.
- Ogni passo mostrato nel progress corrisponde a lavoro eseguito e il passo fallito è quello riportato all'utente.
- Un URL senza JSON-LD termina con un messaggio preciso che indirizza al fallback degli slice 7 e 8.
- Timeout, host irraggiungibile e URL verso indirizzi interni non lasciano ricette parziali salvate.

**Learning / risk**

- L'hit-rate del JSON-LD sui blog realmente usati determina quanto peso e quanto costo avrà il fallback LLM.

**Outcome**

- Il caso d'uso più frequente è coperto end-to-end senza spesa di LLM.

### 7. Estrazione LLM quando mancano i dati strutturati *(Theme: B)*

---

**Includes**

- Estrazione con modello a output strutturato validato contro lo schema Recipe, invocata solo quando il JSON-LD manca.
- Stesso motore di pulizia, stesso schema e stesso salvataggio del percorso JSON-LD.
- Costo, latenza ed esito di ogni estrazione registrati per ricetta.

**Verification**

- Una pagina priva di JSON-LD produce una ricetta salvata con titolo, ingredienti e preparazione utilizzabili.
- Un output non conforme allo schema viene rifiutato senza salvare dati inventati e senza lasciare la ricetta a metà.
- Il costo medio per ricetta su un campione reale resta nell'ordine dei centesimi.
- Pagine paywall o JS-heavy terminano con il messaggio che indirizza al copia-incolla.

**Outcome**

- I siti senza dati strutturati smettono di essere un vicolo cieco per l'aggiunta da link.

### 8. Copia-incolla come fallback definitivo *(Theme: B)*

---

**Includes**

- Input di testo incollato che salta il JSON-LD e riusa il motore di estrazione e lo schema già esistenti.
- Stesso salvataggio immediato senza review e stesso progress sui passi reali.

**Verification**

- Il testo di una pagina paywall che aveva fatto fallire il percorso da link viene salvato come ricetta ricercabile.
- Un testo che non è una ricetta produce un errore comprensibile senza salvare nulla.
- Il percorso completo link fallito → copia-incolla riuscito è dimostrato end-to-end.

**Outcome**

- Nessuna pagina resta inaccessibile: ogni ricetta trovata online può entrare nel ricettario.

### 9. Ricettari condivisi su invito *(Theme: F)*

---

**Includes**

- Creazione di ricettari aggiuntivi e selettore del ricettario corrente per chi appartiene a più di uno.
- `Invitation` con token condivisibile via link o codice e scadenza opzionale.
- Adesione da utente loggato che crea la `Membership`; tutti i membri sono pari.

**Verification**

- Due account Google diversi collaborano sullo stesso ricettario: entrambi vedono ed editano le stesse ricette.
- Un token scaduto, già consumato oltre le sue regole o manomesso viene rifiutato senza creare membership.
- Un non membro non accede al ricettario né in lettura né in scrittura, nemmeno per id diretto.
- Cambiando ricettario corrente, elenco e ricerca cambiano scope coerentemente.

**Outcome**

- Famiglia e amici usano un ricettario comune senza permessi da configurare.

### 10. Foto delle ricette *(Theme: D)*

---

**Includes**

- Upload multiplo su object storage con solo l'URL persistito in database, più eliminazione della foto.
- Copertina impostata sulla prima foto e modificabile, con l'invariante di una sola cover per ricetta.
- Acquisizione dell'immagine della pagina durante l'import e ricarica sul nostro storage, come passo reale del progress.

**Verification**

- Le foto caricate restano visibili dopo un redeploy e la loro eliminazione non lascia riferimenti rotti.
- Cambiando copertina la precedente perde il flag, verificato anche con richieste concorrenti.
- Una ricetta importata mostra un'immagine servita dal nostro storage e non dal sito originale.
- Un fallimento dell'upload non impedisce il salvataggio della ricetta e lo dichiara all'utente.

**Outcome**

- Le ricette hanno immagini proprie e stabili, con una copertina scelta.

### 11. Rilascio a familiari e amici *(Release: delivery)*

---

**Includes**

- App su dominio stabile con `suspend` e scale-to-zero, database, bucket e credenziali OAuth di produzione separati dall'ambiente di prova.
- Redirect URI di produzione configurati e segreti gestiti fuori dal repository.
- Log ed errori consultabili e procedura di rollback tramite redeploy.

**Verification**

- Una persona invitata completa in produzione il percorso login → aggiunta da link → ricerca → apertura ricetta.
- Il primo accesso dopo un periodo di inattività rientra nella latenza misurata allo slice 1.
- Il costo mensile osservato dopo il primo periodo d'uso è coerente con il target dichiarato.
- Un rollback riporta l'app alla versione precedente senza perdita di dati.

**Outcome**

- Familiari e amici usano il ricettario condiviso in produzione.

## LATER

- **Filtri strutturati per tag e tempo**
  - **Promotion trigger:** la ricerca semantica sbaglia o diluisce risultati su vincoli espliciti osservati nelle query reali.
  - **Expected value:** i campi sono già popolati best-effort dallo slice 6, quindi il filtro si abilita senza migrazione né lavoro retroattivo.
- **Ricerca ibrida semantica più full-text**
  - **Promotion trigger:** ricerche per termini esatti (nome proprio, ingrediente raro) falliscono nelle sessioni reali.
  - **Expected value:** copre i casi lessicali dove l'embedding è debole senza rinunciare al cross-lingua.
- **Derivazione di tag e tempo per le ricette inserite a mano**
  - **Promotion trigger:** i filtri vengono promossi e le ricette manuali risultano sistematicamente escluse.
  - **Expected value:** uniforma il segnale disponibile a ricerca e filtri su tutte le fonti.
- **Ricerca cross-ricettario**
  - **Promotion trigger:** utenti con più ricettari cercano ripetutamente nel ricettario sbagliato.
  - **Expected value:** elimina il cambio manuale di scope quando la memoria dell'utente è per ricetta, non per ricettario.
- **Ricettari pubblici tematici**
  - **Promotion trigger:** richiesta esplicita di condividere un ricettario oltre la cerchia invitata.
  - **Expected value:** abilitabile come `visibility=public` sul modello esistente, senza migrazione.
- **Concetto di gruppo sopra i ricettari**
  - **Promotion trigger:** gli stessi membri vengono re-invitati su più ricettari e lo segnalano come attrito.
  - **Expected value:** rimuove l'unico svantaggio accettato del modello cookbook-centrico, in modo additivo.
- **Macchina sempre calda invece dello scale-to-zero**
  - **Promotion trigger:** la latenza del primo accesso misurata agli slice 1 e 11 risulta fastidiosa nell'uso reale.
  - **Expected value:** elimina il cold start al costo dichiarato di pochi dollari al mese, con un flag reversibile.

## OUT-OF-SCOPE

- **Ingredienti strutturati con quantità e unità** — l'attrito minimo in aggiunta impone testo libero; la ricerca è semantica e chi legge interpreta il testo.
- **Lista della spesa e scaling delle porzioni** — dipendono dagli ingredienti strutturati e le sorgenti li dichiarano già fuori scope come trade-off accettato.
- **Review obbligatoria dell'estratto prima del salvataggio** — scelta deliberata: si salva subito e si corregge dopo con l'edit.
- **Deduplica delle ricette** — i duplicati nello stesso ricettario sono consentiti per scelta.
- **Autenticazione con email e password o magic-link** — entrambe richiedono un provider email, in conflitto con l'assenza di invii email nell'MVP.
- **Passkeys** — recupero account complesso e supporto Auth.js ancora acerbo.
- **Ruoli e permessi granulari** — nell'MVP il solo ruolo è `creatorId` e tutti i membri sono pari.
- **Vector database dedicato** — a ≤10.000 ricette Postgres con pgvector e indice HNSW è sufficiente: sarebbe infrastruttura e costo senza beneficio.
- **IaC versionata con SST o Terraform** — `fly.toml` più CLI bastano all'MVP; il resto è over-engineering dichiarato.

## Decision checkpoints

- **Dopo lo slice 3:** recall cross-lingua misurato sul corpus reale → sostituire l'embedder, cambiare il testo indicizzato, promuovere la ricerca ibrida da `LATER` o riconsiderare il differenziatore e con esso il senso del prodotto.
- **Dopo lo slice 4:** latenza, numero di chiamate e costo per query → chiudere la contraddizione sull'embedding a runtime scegliendo cache, pre-calcolo o nessuna azione.
- **Dopo lo slice 6:** hit-rate del JSON-LD sui siti realmente usati → ridimensionare, anticipare o posticipare l'estrazione LLM.
- **Dopo lo slice 8:** costo e qualità dell'estrazione LLM su ricette reali → cambiare modello, restringere i casi in cui viene invocata o accettare il costo.
- **Dopo lo slice 11:** cold start e costo osservati in produzione → promuovere la macchina sempre calda da `LATER`.

## Open questions

- Provider Postgres gestito: le sorgenti nominano Neon o Supabase senza sceglierne uno. Blocca lo slice 1 e ogni slice che persiste dati.
- Driver Postgres e modalità di connessione: `postgres.js` o `node-postgres`, con pooling e interazione con lo scale-to-zero da definire. Blocca lo slice 1.
- Embedder multilingue: il modello citato è un esempio, non una scelta; il vincolo vincolante è la qualità cross-lingua. Blocca gli slice 3 e 4.
- Modello di estrazione LLM: le sorgenti indicano solo una classe di costo, non un modello o un provider. Blocca gli slice 7 e 8.
- Embedding a runtime sulle query: le sorgenti vietano chiamate a runtime sulle query di ricerca ma descrivono la ricerca come similarità con l'embedding della query. Blocca l'accettazione dello slice 4 finché non si decide fra chiamata per query, cache o pre-calcolo.
