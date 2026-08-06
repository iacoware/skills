# Recipe App — Piano di delivery

- **Sources:** `goal.md`, `arch-choices.md`, `tech-choices.md`, `concepts.md`.
- **Current state:** Greenfield assunto: le fonti definiscono prodotto e decisioni, ma non dichiarano una base implementata.

## Ordering criteria

- Separare bootstrap, infrastruttura reale e valore prodotto; mantenere piccoli i primi incrementi per revisionare presto convenzioni e deploy.
- Validare prima il differenziatore esistenziale — ricerca semantica cross-lingua — con input controllati che attraversano embedding, persistenza e query reali.
- Stabilire il confine `cookbookId` e un unico resolver dello scope con il primo dato di dominio; Google OAuth sostituisce poi qualsiasi scope configurato in un solo seam.
- Consegnare correzione, fallback automatico e copia-incolla prima di aprire altri temi dopo l'import da URL.
- Dopo i rischi distintivi, preferire ampiezza prima della profondità; completare con una release per famiglia e amici selezionati.

## Themes

| Theme | Desired outcome | First validation |
|---|---|---|
| A. Accesso e scope | Una persona accede e opera solo nel ricettario corrente | 2 |
| B. Ricerca semantica | Un membro ritrova ricette del ricettario con query cross-lingua | 4 |
| C. Inserimento e correzione | Un membro salva manualmente e corregge una ricetta senza review obbligatoria | 5 |
| D. Importazione da URL | Un membro importa con poco attrito anche senza dati strutturati | 7 |
| E. Acquisizione da testo | Un membro recupera una ricetta incollando il testo quando il sito non è leggibile | 8 |
| F. Consultazione | Un membro vede le ricette del ricettario corrente dalla home | 9 |
| G. Foto | Un membro gestisce più foto e sceglie la cover | 10 |
| H. Condivisione | Creator e invitati collaborano da pari in uno o più ricettari | 11 |

## Cross-functional concerns

- **Authorization:** Ogni lettura e modifica usa membership e `cookbookId` risolto centralmente; nessuna query ricetta o ricerca è globale.
- **Validation and errors:** Schema valida input esterni e output LLM; errori tipizzati distinguono fetch, parsing, modello, embedding, storage e persistenza.
- **Operability:** Passi reali, durata, timeout e fallimenti sono osservabili senza registrare URL firmati, token, testo sensibile o segreti.
- **Accessibility and security:** Flussi da tastiera, focus e annunci di stato accessibili; URL, upload, OAuth e inviti sono validati contro abuso e accessi indebiti.
- **Data integrity and recovery:** Ricetta è canonica, embedding è rigenerabile a ogni edit, una sola foto è cover e i fallimenti parziali non lasciano riferimenti o oggetti orfani.

## NOW

### 0. Repository verificabile *(Enabler: delivery)*

---

**Includes**

- Applicazione TypeScript/Next.js containerizzabile con formattazione coerente.
- CI per build, lint, typecheck e test, senza provisioning o deploy.

**Verification**

- Una pull request pulita esegue con successo build, lint, typecheck e test.
- Un errore intenzionale in ciascun controllo rende la CI rossa.

**Outcome**

- Gli sviluppatori hanno una base minima, ripetibile e revisionabile per ogni slice successiva.

### 1. Runtime connesso in ambiente non produttivo *(Enabler: delivery)*

---

**Includes**

- CI/CD, provisioning minimo e deploy Docker su Fly.io con `suspend` e scale-to-zero.
- Postgres+pgvector sul provider e driver scelti, raggiunto a runtime con un'operazione non di dominio.
- Migration runner che applica una migrazione non di dominio; nessuna entità, auth o tenancy.

**Verification**

- Da ambiente rappresentativo, deploy e rollback sono ripetibili e la migration parte da database vuoto.
- Dopo sospensione, una richiesta completa un round trip Postgres via connessione reale e registra cold start e latenza.

**Learning / risk**

- Verifica compatibilità tra Fly suspend, connessione TCP/pooling, pgvector e migrazioni prima del dominio.

**Outcome**

- Gli sviluppatori osservano il runtime minimo deciso, con datastore e migrazioni realmente funzionanti.

### 2. Accesso al primo ricettario privato *(Theme: A)*

---

**Includes**

- Login e sessione con Auth.js v5 e Google OAuth.
- Creazione del primo ricettario privato, creator e membership atomici.
- Resolver unico del ricettario corrente usato da ogni accesso applicativo.

**Verification**

- Un nuovo utente Google crea e riapre il proprio ricettario; sessione scaduta richiede nuovo accesso.
- Un utente non membro non può leggere o modificare lo scope di un altro ricettario, anche forzando identificativi.

**Outcome**

- Una persona autenticata dispone di uno scope privato persistente per le ricette future.

### 3. Pipeline embedding multilingue osservabile *(Enabler: ricerca semantica)*

---

**Includes**

- Fixture normalizzate attraversano API/modello multilingue selezionati, Drizzle, Postgres e pgvector reali.
- Testo vettoriale composto da nome, ingredienti, preparazione e metadati opzionali disponibili.
- Diagnostica minima ordina ricette persistite per similarità, senza UI prodotto.

**Verification**

- Query italiane classificano ricette inglesi pertinenti sopra esempi non pertinenti su un corpus rappresentativo.
- Retry, timeout, output invalido, dimensione errata e indisponibilità del provider producono errori distinti e nessun dato incoerente.
- L'esecuzione misura qualità relativa, latenza e costo per decidere se il differenziatore è sostenibile.

**Learning / risk**

- Verifica che la strategia scelta renda davvero utile la similarità cross-lingua entro il budget minimo.

**Outcome**

- Gli sviluppatori possono valutare con evidenza eseguibile la parte più rischiosa del prodotto.

### 4. Ricerca semantica nel ricettario corrente *(Theme: B)*

---

**Includes**

- Campo di ricerca che genera il vettore query secondo la decisione aperta e interroga solo il ricettario corrente.
- Risultati ordinati per similarità su nome, ingredienti, preparazione, tag e tempo quando presenti.
- Nessun filtro strutturato, full-text o ricerca tra ricettari.

**Verification**

- Un membro cerca in italiano e trova una ricetta inglese pertinente nel proprio ricettario.
- Ricette semanticamente vicine di altri ricettari non compaiono; provider lento o indisponibile restituisce uno stato recuperabile.
- Sessioni rappresentative registrano rilevanza percepita, latenza e costo per query.

**Learning / risk**

- Stabilisce se la ricerca cross-lingua è abbastanza utile da giustificare il prodotto rispetto alle alternative mature.

**Outcome**

- Un membro ritrova ricette per significato, indipendentemente dalla lingua e senza uscire dal proprio ricettario.

### 5. Inserimento manuale e correzione immediata *(Theme: C)*

---

**Includes**

- Un unico form accessibile per inserimento manuale ed edit di titolo, ingredienti e preparazione come testo libero.
- Salvataggio immediato senza review; tag e tempo sono opzionali e best-effort.
- Creazione ed edit rigenerano l'embedding mediante la pipeline stabilita, con recupero da fallimenti parziali.

**Verification**

- Un membro crea una ricetta con i soli campi necessari, la corregge e la nuova versione sostituisce i risultati obsoleti di ricerca.
- Input invalidi, conflitto di edit e fallimento embedding preservano una versione canonica coerente e recuperabile.

**Outcome**

- Un membro può registrare ciò che conosce e correggere ogni acquisizione successiva senza passaggio obbligatorio di review.

### 6. Import economico da URL strutturato *(Theme: D)*

---

**Includes**

- URL valido attraversa fetch, pulizia e parsing `schema.org/Recipe`, senza chiamata LLM.
- Titolo, ingredienti, preparazione, metadati disponibili ed embedding sono salvati subito.
- Foto sorgente disponibili sono copiate su Cloudflare R2; la prima diventa cover.
- UI sincrona mostra progress sui passi reali e un errore preciso per fetch, schema, embedding, foto o salvataggio.

**Verification**

- Un food blog con JSON-LD produce una ricetta ricercabile, modificabile e senza hotlink; nessuna chiamata LLM viene osservata.
- Paywall, URL ostile, redirect anomalo, timeout, immagine invalida e scrittura parziale lasciano stato coerente e messaggio specifico.

**Learning / risk**

- Misura hit-rate, durata e affidabilità del percorso gratuito sul caso d'uso più frequente.

**Outcome**

- Un tester nel ricettario privato importa con un URL una ricetta strutturata pronta all'uso.

### 7. Fallback LLM automatico per URL *(Theme: D)*

---

**Includes**

- In assenza di JSON-LD, contenuto pulito passa al provider/modello economico selezionato con output strutturato validato.
- Lo stesso flusso di progress, persistenza, embedding, foto e correzione resta invariato.
- Timeout, retry limitato, output invalido e contenuto insufficiente terminano con esito preciso e recuperabile.

**Verification**

- Pagine senza structured data producono ricette utilizzabili; JSON-LD continua a evitare ogni chiamata LLM.
- Corpus rappresentativo confronta completezza utile, errori, latenza e costo dei due percorsi.
- Allucinazione o risposta malformata non viene persistita come ricetta valida e non lascia foto orfane.

**Learning / risk**

- Verifica se il fallback distintivo amplia davvero la copertura a costo e qualità accettabili.

**Outcome**

- Un tester importa da URL anche quando il sito non espone una ricetta strutturata.

### 8. Recupero tramite copia-incolla *(Theme: E)*

---

**Includes**

- Input testo riusa pulizia, schema validato e adapter LLM stabiliti, saltando fetch e JSON-LD.
- Salvataggio, embedding, progress reale e successiva correzione seguono gli stessi invarianti dell'import URL.
- Il fallimento di un URL propone il canale copia-incolla senza duplicare ricette o pipeline.

**Verification**

- Testo da pagina paywall o JS-heavy genera una ricetta ricercabile e modificabile.
- Testo vuoto, enorme, non pertinente, output invalido e timeout producono esiti distinti senza side effect parziali.

**Outcome**

- Un membro recupera la ricetta quando l'acquisizione diretta dal sito non è possibile.

### 9. Home del ricettario corrente *(Theme: F)*

---

**Includes**

- Elenco delle ricette del ricettario corrente con cover quando presente.
- Accesso ai tre ingressi di aggiunta e al dettaglio modificabile.
- Stati vuoto, caricamento, errore e assenza foto accessibili e recuperabili.

**Verification**

- Un membro vede solo le proprie ricette correnti dopo creazione manuale, URL e copia-incolla.
- Cambio scope, sessione scaduta e rete lenta non mostrano dati del ricettario precedente.

**Outcome**

- Un membro consulta e raggiunge le azioni principali del proprio ricettario da una home coerente.

### 10. Foto multiple e cover controllabile *(Theme: G)*

---

**Includes**

- Aggiunta e rimozione di più foto per ricetta su Cloudflare R2.
- Prima foto come cover predefinita e selezione esplicita di un'altra cover.
- Aggiornamenti DB/storage recuperabili mantengono esattamente una cover quando esistono foto.

**Verification**

- Un membro aggiunge più foto, cambia cover e vede l'aggiornamento in home e dettaglio.
- Upload invalido o abusivo, timeout, cancellazione cover e fallimento parziale non creano riferimenti o oggetti orfani.

**Outcome**

- Un membro documenta una ricetta con più immagini e controlla quella rappresentativa.

### 11. Invito e collaborazione tra ricettari *(Theme: H)*

---

**Includes**

- Il creator genera link/codice condivisibile per il proprio ricettario; apertura autenticata crea membership.
- Tutti i membri leggono e modificano da pari; solo il creator genera inviti.
- Un utente appartiene a più ricettari e cambia quello corrente senza mescolare dati o ricerca.

**Verification**

- Un invitato entra, modifica una ricetta condivisa e alterna due ricettari con risultati correttamente isolati.
- Token invalido, scaduto o riusato, utente non autenticato e accesso non membro non elevano privilegi né trapelano dati.

**Outcome**

- Famiglia e amici collaborano da pari nei ricettari a cui sono stati invitati.

### 12. Release MVP a utenti selezionati *(Release: delivery)*

---

**Includes**

- Deploy nell'ambiente destinato a famiglia e amici con Fly suspend, Postgres+pgvector, R2, Google OAuth e provider selezionati.
- Configurazione segreti, callback OAuth, migrazioni e rollback ripetibili per la release.
- Telemetria minima per cold start, costi provider e fallimenti dei flussi distintivi.

**Verification**

- Utenti selezionati completano login, invito, aggiunta nei tre modi, edit, foto, home e ricerca cross-lingua.
- Smoke test dopo deploy e suspend verifica isolamento, datastore, storage e adapter esterni; rollback ripristina la versione precedente.
- Consumi osservati restano confrontabili con il target di centesimi mensili e rendono visibili eventuali superamenti.

**Outcome**

- Il MVP coerente è utilizzabile nel suo ambiente reale da famiglia e amici selezionati.

## LATER

- **Filtri strutturati per tag/tempo e ricerca ibrida**
  - **Promotion trigger:** Evidenza dalle slice 4 e 12 che la sola semantica non offre controllo o precisione sufficienti.
  - **Expected value:** Raffinare risultati usando metadati già popolati senza lavoro retroattivo.
- **Ricettari pubblici tematici**
  - **Promotion trigger:** Domanda osservata dopo la slice 12 per scoprire collezioni oltre la cerchia invitata.
  - **Expected value:** Condividere raccolte pubbliche tramite la futura visibility già prevista.
- **Gruppi sopra i ricettari**
  - **Promotion trigger:** Evidenza dalla slice 11 che reinvitare le stesse persone è un attrito ricorrente.
  - **Expected value:** Riutilizzare membership tra più ricettari senza alterare il modello MVP.
- **Ricerca cross-ricettario**
  - **Promotion trigger:** Utenti multi-ricettario della slice 11 chiedono spesso una ricerca unificata.
  - **Expected value:** Ritrovare contenuti senza cambiare scope manualmente.
- **Ruoli e permessi granulari**
  - **Promotion trigger:** Collaborazioni reali mostrano modifiche indesiderate non gestibili con membri pari e creator.
  - **Expected value:** Controllare capacità diverse senza anticipare complessità.
- **Passkeys**
  - **Promotion trigger:** Auth.js offre supporto maturo e gli utenti richiedono accesso ricorrente senza Google.
  - **Expected value:** Ridurre attrito preservando un recupero account affidabile.

## OUT-OF-SCOPE

- **Lista della spesa e scaling porzioni** — Richiederebbero ingredienti strutturati, esclusi per mantenere minimo l'attrito.
- **Deduplicazione ricette** — Le fonti consentono esplicitamente duplicati nello stesso ricettario.
- **Email/password e magic-link** — Scartati perché introdurrebbero invio email e recupero account nell'MVP.
- **Vector database dedicato o embedding self-hosted** — Costo e infrastruttura non giustificati alla scala prevista.
- **Hosting Vercel, Workers/OpenNext o Fargate** — Scartato a favore del runtime Docker Fly.io deciso.
- **IaC Terraform/SST nell'MVP** — Sovradimensionato rispetto a `fly.toml` e CLI; rivalutabile solo con futura esigenza multi-cloud/versionata.

## Decision checkpoints

- **After slice 1:** Cold start, pooling e migrazioni reali → cambiare provider/driver o strategia Fly prima del dominio.
- **After slice 4:** Rilevanza cross-lingua, latenza e costo → procedere, cambiare modello/query strategy o fermare il prodotto indifferenziato.
- **After slice 8:** Copertura, qualità, errori e costo dei tre ingressi → cambiare cascata, soglie o priorità dei flussi restanti.
- **After slice 11:** Uso multi-ricettario e attrito degli inviti → promuovere gruppi, ricerca cross-scope o ruoli solo con evidenza.

## Non-product work

- **Prima della slice 1 — scelta Postgres:** Confrontare Neon/Supabase e `postgres.js`/`node-postgres` sul percorso Fly reale; uscita: provider, driver, pooling e migrazioni registrati, codice esplorativo eliminato o assorbito nella slice 1.
- **Prima della slice 3 — spike embedding:** Selezionare API/modello multilingue e risolvere il conflitto sul vettore query con corpus, latenza e costo; uscita: decisione esplicita, esperimenti eliminati o assorbiti nella slice 3.
- **Prima della slice 7 — spike estrazione LLM:** Confrontare modelli economici su pagine senza JSON-LD e output malformati; uscita: provider/modello, timeout e soglie scelti, esperimenti eliminati o assorbiti nella slice 7.

## Open questions

- Neon o Supabase, e quale driver/pooling TCP? Blocca le slice 1–12; lo spike prima della slice 1 deve selezionare la combinazione.
- Quale API/modello embedding multilingue, e come conciliare “solo in add/edit” con la query che richiede `embedding(query)`? Blocca le slice 3–12; lo spike prima della slice 3 deve produrre una decisione accettata.
- Quale provider/modello LLM economico soddisfa qualità, schema, latenza e costo? Blocca le slice 7, 8 e 12; lo spike prima della slice 7 deve selezionarlo.
