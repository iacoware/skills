# Recipe App — Delivery plan

- **Sources:** `sources/goal.md`, `sources/arch-choices.md`, `sources/concepts.md`, `sources/tech-choices.md`.
- **Current state:** Greenfield; requisiti, dominio e stack sono decisi, ma non risulta una base applicativa esistente.

## Ordering criteria

- Separare repository e walking skeleton; introdurre Postgres, pgvector e provider esterni solo nel primo percorso che li esercita davvero.
- Validare prima ricerca semantica cross-lingua ed estrazione LLM, i due differenziatori che decidono se costruire il prodotto.
- Stabilire un unico resolver dello scope ricettario dal primo dato persistito e sostituirne l'origine configurata con sessione e membership a un solo seam.
- Consegnare il form di correzione prima delle importazioni automatiche; anticipare i fallback LLM alla normale breadth-first perché sono rischio e valore distintivo.
- Terminare `NOW` con una release per un gruppo selezionato di familiari e amici, mantenendo scale-to-zero e servizi entro il budget dichiarato.

## Themes

| Theme | Desired outcome | First validation |
|---|---|---|
| A. Scoperta semantica | Trovare nel ricettario corrente ricette pertinenti anche tra lingue diverse | Prova eseguibile della ricerca multilingue |
| B. Accesso e ricettari privati | Accedere ai propri ricettari e passare dall'uno all'altro senza commistioni | Accedere e gestire ricettari privati |
| C. Acquisizione e correzione manuale | Salvare rapidamente una ricetta conosciuta e correggerla in seguito | Aggiungere e correggere una ricetta manuale |
| D. Importazione web | Salvare da un link una ricetta e le sue informazioni utili con minimo attrito | Importare da link con JSON-LD |
| E. Estrazione resiliente | Recuperare ricette prive di dati strutturati o provenienti da pagine illeggibili | Estrarre da link senza JSON-LD |
| F. Condivisione del ricettario | Invitare altre persone e collaborare alla pari sullo stesso ricettario | Condividere un ricettario tramite invito |
| G. Presentazione fotografica | Conservare più foto e scegliere quella che identifica la ricetta | Gestire foto multiple e copertina |

## Cross-functional concerns

- **Authorization:** Ogni lettura, scrittura e ricerca usa il `cookbookId` fornito da un solo resolver; dalla slice 4 il resolver deriva esclusivamente da sessione e membership.
- **Validation and errors:** Schema valida input esterni, JSON-LD e output LLM; il flusso di acquisizione espone passo corrente e causa precisa senza presentare avanzamenti fittizi.
- **Operability:** Fetch, embedding, LLM e R2 hanno timeout, retry solo sicuri, log correlati e misure di latenza/costo; segreti e contenuto delle ricette non finiscono nei log.
- **Accessibility and security:** Form, errori e progress sono fruibili da tastiera e tecnologie assistive; input HTML è sanificato, URL remoti protetti da SSRF e campi opzionali indicati senza asterischi sui richiesti.
- **Data integrity and recovery:** La ricetta resta canonica, l'embedding si rigenera dopo ogni modifica, esiste al massimo una cover e i fallimenti parziali non lasciano ricette incomplete o oggetti R2 orfani.

## NOW

### 0. Repository verificabile *(Enabler: delivery)*

---

**Includes**

- Applicazione Next.js TypeScript minima con Effect, Drizzle, convenzioni di test e formattazione già decise.
- CI con installazione riproducibile, build, lint, typecheck e test, senza provisioning né deploy.

**Verification**

- Una pull request pulita esegue con successo build, lint, typecheck e test in CI.
- Gli stessi comandi passano localmente da checkout pulito con la versione Node dichiarata.

**Outcome**

- Gli sviluppatori hanno una base piccola, riproducibile e protetta da controlli automatici.

### 1. Walking skeleton su Fly.io *(Enabler: delivery)*

---

**Includes**

- Container stateless Next.js con endpoint diagnostico minimo, configurazione `fly.toml` e deploy automatico in un ambiente non di produzione rappresentativo.
- Provisioning della sola applicazione Fly con `suspend` e scale-to-zero; nessuna autenticazione, tenancy o CRUD di dominio.

**Verification**

- Un commit attraversa CI/CD e rende raggiungibile la nuova versione dell'endpoint diagnostico nell'ambiente rappresentativo.
- Arresto, resume e rollback della macchina sono provati, registrando tempo di risveglio e consumo minimo.

**Outcome**

- Gli sviluppatori possono verificare il percorso reale da commit a runtime Fly e il compromesso del cold start.

### 2. Prova eseguibile della ricerca multilingue *(Enabler: semantic discovery)*

---

**Includes**

- Postgres con pgvector, adapter cloud per embedding multilingue e scope ricettario ottenuto da un resolver configurato per l'ambiente di prova.
- Fixture normalizzate attraversano il percorso di produzione che calcola e persiste gli embedding; un comando diagnostico incorpora una query e ordina i risultati.
- Corpus piccolo ma reale con ricette italiane e inglesi, termini equivalenti tra lingue e ricette di controllo in un altro ricettario.

**Verification**

- Query italiane recuperano le ricette inglesi attese e viceversa; una revisione umana confronta ranking e falsi positivi sul corpus dichiarato.
- Nessun risultato dell'altro ricettario compare e nessun vettore precalcolato viene iniettato dalle fixture.
- L'esecuzione nell'ambiente rappresentativo registra latenza, token e costo di indicizzazione e query.

**Learning / risk**

- Stabilisce se qualità cross-lingua, isolamento, latenza e costo dell'embedder sostengono il principale differenziatore.

**Outcome**

- Gli sviluppatori dispongono di evidenza ripetibile sul motore semantico reale prima di costruire i flussi commodity.

### 3. Cercare ricette nel ricettario corrente *(Theme: A)*

---

**Includes**

- Home non di produzione per utenti di prova con campo di ricerca semantica, risultati ordinati e dettaglio della ricetta dal corpus persistito.
- Solo ricerca vettoriale nello scope configurato; nessun filtro strutturato, full-text o ricerca tra ricettari.

**Verification**

- Utenti di prova completano ricerche cross-lingua rappresentative e aprono la ricetta ritenuta pertinente.
- Stati vuoto, caricamento ed errore sono comprensibili e accessibili; risultati fuori scope restano assenti.
- Telemetria osserva rilevanza giudicata, latenza end-to-end e costo per query senza registrare il testo cercato.

**Learning / risk**

- Verifica che il ranking tecnicamente valido della slice 2 produca scoperta percepita come utile nell'interazione reale.

**Outcome**

- Sviluppatori e tester selezionati possono valutare il valore distintivo della ricerca nell'ambiente rappresentativo.

### 4. Accedere e gestire ricettari privati *(Theme: B)*

---

**Includes**

- Google OAuth con Auth.js, sessione persistita in Postgres e creazione del relativo utente applicativo.
- Creazione, elenco e cambio del ricettario; il creator diventa membro e un utente può appartenere a più ricettari.
- Sostituzione del resolver configurato con il resolver autenticato di membership, senza modificare i consumer.

**Verification**

- Un nuovo utente accede con Google, crea due ricettari e cambia quello corrente.
- Utenti anonimi sono respinti e due account non possono leggere, cercare o modificare ricettari senza membership.
- I test di integrazione dimostrano che ogni accesso dati passa dal resolver autenticato.

**Outcome**

- Ogni utente lavora in uno o più ricettari privati con isolamento applicato end-to-end.

### 5. Aggiungere e correggere una ricetta manuale *(Theme: C)*

---

**Includes**

- Un unico form per inserimento manuale ed edit con nome, ingredienti e preparazione come testo libero.
- Salvataggio immediato senza review, elenco e dettaglio nella home del ricettario corrente.
- Calcolo dell'embedding alla creazione e rigenerazione dopo ogni modifica; tag e tempo possono restare assenti.

**Verification**

- Un membro crea una ricetta, la vede in elenco e dettaglio, la modifica e ritrova il testo aggiornato tramite ricerca.
- Un secondo ricettario dello stesso utente e un utente non membro non vedono né possono mutare la ricetta.
- Errori di validazione o del provider non producono stati parziali e il form conserva input recuperabili.

**Outcome**

- Un membro può memorizzare una ricetta conosciuta e correggere qualsiasi contenuto senza normalizzare ingredienti o passaggi.

### 6. Importare da link con JSON-LD *(Theme: D)*

---

**Includes**

- Inserimento URL, fetch della pagina e parsing validato di `schema.org/Recipe` senza chiamare il LLM.
- Progress sincrono legato ai passi reali di download, lettura, individuazione ingredienti e salvataggio foto.
- Salvataggio immediato di testo, URL sorgente, tag e tempo disponibili; foto copiate su R2 con la prima come cover.

**Verification**

- Su blog reali con JSON-LD, i passi avanzano solo al completamento effettivo e la ricetta diventa visibile e ricercabile senza review.
- L'adapter LLM non viene invocato, i dati opzionali mancanti non bloccano e la foto servita proviene da R2, non dal sito sorgente.
- Timeout, URL non sicuro, pagina invalida e upload fallito mostrano la causa corretta senza ricetta parziale né oggetto orfano.

**Learning / risk**

- Misura copertura e qualità del percorso gratuito, oltre ad affidabilità del fetch e del trasferimento foto sui siti reali scelti.

**Outcome**

- Un membro salva con un link una ricetta strutturata, già ricercabile e con foto, senza trascrizione manuale.

### 7. Estrarre da link senza JSON-LD *(Theme: E)*

---

**Includes**

- Pulizia del contenuto pagina e fallback a un LLM economico quando non esiste JSON-LD utilizzabile.
- Output strutturato validato nello stesso schema ricetta, con tag e tempo best-effort e salvataggio immediato.
- Stesso progress reale e stessi percorsi di persistenza, embedding, foto ed edit della normale importazione.

**Verification**

- Un campione dichiarato di pagine reali senza JSON-LD produce ricette che una revisione umana confronta con nome, ingredienti e preparazione sorgente.
- Output malformato, contenuto insufficiente, timeout e rifiuto del provider generano errori precisi senza persistenza parziale.
- Per ogni campione sono registrati percorso scelto, latenza e costo; le pagine con JSON-LD continuano a non invocare il LLM.

**Learning / risk**

- Verifica se copertura, fedeltà, latenza e costo del fallback LLM rendono l'importazione superiore alle alternative mature.

**Outcome**

- Un membro può importare automaticamente anche da una pagina priva di dati Recipe strutturati.

### 8. Recuperare una ricetta da testo incollato *(Theme: E)*

---

**Includes**

- Ingresso copia-incolla che salta fetch e JSON-LD, pulisce il testo e riusa il motore LLM validato.
- Salvataggio immediato nello scope corrente, embedding e successiva correzione tramite il form condiviso.
- Indicazione esplicita di questo percorso quando l'importazione URL fallisce per paywall o pagina JS-heavy.

**Verification**

- Testi copiati da pagine non leggibili dal server diventano ricette ricercabili e modificabili senza reinserimento manuale dei campi.
- Il test di integrazione dimostra il riuso dell'estrattore e l'assenza di fetch remoto nel percorso copia-incolla.
- Input vuoto, rumore non riconoscibile e output LLM invalido producono feedback recuperabile senza dati parziali.

**Learning / risk**

- Osserva se il fallback mantiene il basso attrito quando limiti tecnici o paywall impediscono l'importazione diretta.

**Outcome**

- Un membro conserva una ricetta da una pagina illeggibile incollandone il testo in un solo flusso alternativo.

### 9. Condividere un ricettario tramite invito *(Theme: F)*

---

**Includes**

- Il creator genera un link o codice non prevedibile riferito a un solo ricettario.
- Un utente autenticato accetta l'invito e ottiene una membership in modo idempotente.
- Tutti i membri possono leggere, cercare, aggiungere e modificare le ricette; solo il creator crea inviti.

**Verification**

- Un secondo account accetta il link, modifica una ricetta e il primo vede la modifica nello stesso ricettario.
- Riaccettare l'invito non duplica la membership; token alterati o riferiti ad altro ricettario non concedono accesso.
- Un membro continua a non vedere gli altri ricettari del creator e non può generare inviti.

**Outcome**

- Familiari e amici collaborano alla pari su un ricettario senza introdurre gruppi o ruoli granulari.

### 10. Gestire foto multiple e copertina *(Theme: G)*

---

**Includes**

- Caricamento di più foto su R2 per una ricetta manuale o importata e visualizzazione nel dettaglio.
- Prima foto come cover predefinita e selezione atomica di una diversa cover da parte di qualsiasi membro.
- Validazione di tipo e dimensione prima dell'upload, con recupero dei fallimenti parziali.

**Verification**

- Un membro aggiunge più foto, cambia cover e home e dettaglio mostrano coerentemente la nuova scelta.
- Accessi non autorizzati, file non validi e upload interrotto non mutano la cover né lasciano riferimenti o oggetti orfani.
- Test concorrenti preservano l'invariante di una sola cover per ricetta.

**Outcome**

- I membri documentano visivamente una ricetta con più foto e controllano quale la rappresenta.

### 11. Rilasciare l'MVP al gruppo pilota *(Release: delivery)*

---

**Includes**

- Ambiente destinato a familiari e amici selezionati su Fly con `suspend`, Postgres+pgvector gestito, R2 e credenziali Google/AI configurate come segreti.
- Migrazioni applicate dal percorso di rilascio, smoke test post-deploy e procedura provata di rollback applicativo.
- Dashboard minima per errori, tempi dei provider e costo di Fly, embedding e LLM entro il budget dichiarato.

**Verification**

- Due utenti Google completano creazione e invito, tutti i tre ingressi ricetta, modifica, foto e ricerca cross-lingua nell'ambiente destinato.
- Un deploy e un rollback preservano ricette, membership, vettori e foto; il resume da sospensione supera lo smoke test.
- Una finestra pilota conferma errori diagnosticabili e rende visibili consumo e costo effettivi dei servizi.

**Outcome**

- Un gruppo pilota usa in sicurezza l'intero MVP condiviso nel suo ambiente reale, fornendo evidenza per le priorità successive.

## LATER

- **Filtri strutturati per tag e tempo**
  - **Promotion trigger:** Le sessioni `NOW` mostrano richieste ricorrenti di restringimento che la sola semantica non soddisfa.
  - **Expected value:** Sfrutta i campi già derivati senza migrazione o compilazione retroattiva.
- **Ricerca ibrida semantica e full-text**
  - **Promotion trigger:** Le valutazioni rilevano fallimenti sistematici su nomi o ingredienti esatti non risolvibili regolando l'indice semantico.
  - **Expected value:** Migliora precisione sui termini esatti mantenendo il recupero cross-lingua.
- **Ricettari pubblici tematici**
  - **Promotion trigger:** Il pilota richiede scoperta o condivisione oltre membri invitati.
  - **Expected value:** Riusa `Cookbook.visibility` per collezioni consultabili pubblicamente.
- **Gruppi sopra i ricettari**
  - **Promotion trigger:** Gli stessi utenti vengono reinvitati spesso e il costo osservato supera la semplicità del modello cookbook-centrico.
  - **Expected value:** Consente membership condivise tra più ricettari senza alterare quelle esistenti.
- **Ricerca cross-ricettario**
  - **Promotion trigger:** Utenti con più ricettari chiedono frequentemente una vista unificata e ne sono definiti i confini di autorizzazione.
  - **Expected value:** Riduce il cambio di contesto preservando lo scope esplicito dei risultati.
- **Permessi granulari o passkeys**
  - **Promotion trigger:** Il modello paritario causa problemi di controllo oppure la dipendenza da Google impedisce l'adozione o il recupero account atteso.
  - **Expected value:** Aggiunge controllo o un accesso alternativo solo quando il relativo costo di prodotto è giustificato.

## OUT-OF-SCOPE

- **Ingredienti strutturati, scaling porzioni e lista della spesa** — Il modello accetta deliberatamente ingredienti testuali per minimizzare l'attrito; queste funzioni richiederebbero una diversa source of truth.
- **Deduplicazione delle ricette** — Le fonti consentono esplicitamente duplicati anche nello stesso ricettario.
- **Importazione da file, PDF, foto o OCR** — L'MVP definisce esclusivamente link, testo incollato e inserimento manuale.
- **Email/password e magic link** — Richiedono invio email e recupero account, contrari alla decisione chiusa su Google OAuth e al budget minimo.
- **Vector DB dedicato, embedding self-hosted e infrastruttura multi-cloud** — Scala e costi previsti non giustificano datastore o IaC aggiuntivi rispetto alle scelte architetturali fissate.

## Decision checkpoints

- **After Prova eseguibile della ricerca multilingue:** Ranking revisionato, isolamento, latenza e costo → confermare embedder e indice oppure cambiare provider/configurazione prima della UI.
- **After Cercare ricette nel ricettario corrente:** Utilità percepita delle ricerche pilota → proseguire, affinare corpus/indicizzazione o fermare il prodotto se il differenziatore non regge.
- **After Estrarre da link senza JSON-LD:** Copertura, fedeltà, latenza e costo sui siti campione → mantenere il fallback URL, restringerne l'ambito o dare priorità al copia-incolla.
- **After Rilasciare l'MVP al gruppo pilota:** Uso della ricerca, reinviti e richieste di controllo → promuovere, riordinare o scartare le candidate `LATER`.

## Non-product work

- **Prima della slice 2 — spike time-boxed sulla query semantica:** Chiarire come produrre `embedding(query)`, richiesto dal modello di ricerca, rispetto al vincolo che colloca gli embedding solo in add/edit; confrontare una chiamata cloud a query con alternative praticabili su latenza, costo e coerenza vettoriale; uscire con decisione registrata e fonti allineate, eliminando ogni codice esplorativo non scelto.
