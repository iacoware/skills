# Recipe App — Piano di delivery

- **Fonti:** `sources/goal.md`, `sources/arch-choices.md`, `sources/concepts.md`, `sources/tech-choices.md`.
- **Stato attuale:** prodotto greenfield; stack e modello di dominio decisi, ma nessuna fondazione applicativa dichiarata e una contraddizione aperta sulla generazione dell'embedding di ricerca.

## Ordering criteria

- Separare repository e delivery reale; mantenere il walking skeleton privo di autenticazione e CRUD di dominio.
- Validare per primo il differenziatore esistenziale, la ricerca semantica cross-lingua, con fixture reali e il percorso di produzione minimo.
- Introdurre Google OAuth e lo scope del ricettario prima delle ulteriori funzionalità la cui accettazione dipende da ownership reale.
- Consegnare poi ampiezza MVP: manutenzione manuale, import URL frequente, fallback LLM, copia-incolla, collaborazione e gestione foto.
- Tenere edit e recupero disponibili prima degli import imperfetti; promuovere agli utenti solo dopo verifica operativa dell'insieme coerente.

## Themes

| Theme | Desired outcome | First validation |
|---|---|---|
| A. Scoperta semantica | Trovare nel ricettario ricette pertinenti anche quando query e contenuto usano lingue diverse | Motore semantico multilingue verificabile |
| B. Accesso ai ricettari | Entrare con Google e lavorare solo nei propri ricettari privati | Accesso Google e ricettari privati |
| C. Manutenzione delle ricette | Salvare, consultare e correggere una ricetta con il minimo attrito | Ricette manuali subito correggibili |
| D. Acquisizione da fonti esterne | Trasformare link o testo in una ricetta salvata, con costi e fallimenti comprensibili | Import URL strutturato |
| E. Collaborazione | Condividere un ricettario con altri utenti paritari | Inviti e modifica condivisa |
| F. Raccolta fotografica | Conservare più foto e scegliere la cover senza dipendere dalla sorgente | Foto multiple e cover |

## Cross-functional concerns

- **Autorizzazione:** ogni accesso passa da un unico resolver del ricettario corrente; solo i membri leggono e modificano, il creator emette inviti, e nessuna query o similarità attraversa lo scope.
- **Validazione ed errori:** Schema valida input non fidati, JSON-LD e output LLM; timeout, sito irraggiungibile, paywall, HTML non valido e output incompleto producono errori specifici e azionabili.
- **Operabilità:** log correlati per step di import, latenza, provider e costo; retry limitati sugli effetti idempotenti; metriche per cold start, fallback LLM, embedding, R2 e fallimenti parziali.
- **Accessibilità e sicurezza:** form e progress espongono stato e errori alle tecnologie assistive; OAuth, sessioni, URL remoti e token d'invito sono protetti contro CSRF, SSRF, abuso e divulgazione nei log.
- **Integrità e recupero:** ricette e membership restano consistenti in transazione; embedding e metadati sono rigenerabili; upload orfani sono rimossi e ogni fallimento successivo al salvataggio offre retry senza duplicare la ricetta.

## NOW

### 0. Repository verificabile *(Enabler: delivery)*

---

**Includes**

- Applicazione Next.js TypeScript, convenzioni Effect/Schema/Drizzle e configurazione di test e formattazione.
- CI su build, lint, typecheck e test, senza provisioning o deploy.
- Test locale minimo del runtime e delle porte applicative senza adapter speculativi.

**Verification**

- Una checkout pulita installa dipendenze ed esegue build, lint, typecheck e test in locale e CI.
- Una modifica intenzionalmente non valida dimostra che ciascun gate pertinente blocca la pipeline.

**Outcome**

- Gli sviluppatori dispongono di una base riproducibile e reviewabile per incrementi verticali.

### 1. Runtime minimo in ambiente non produttivo *(Enabler: delivery)*

---

**Includes**

- Container Docker stateless Next.js su Fly.io con `suspend` e scale-to-zero.
- Pipeline CI/CD, configurazione e segreti minimi per un ambiente rappresentativo non produttivo.
- Endpoint runtime innocuo con log e health check, senza auth, tenancy, database o CRUD di ricette.

**Verification**

- Un commit attraversa CI/CD e rende raggiungibile la versione attesa nell'ambiente non produttivo.
- Health check, log, rollback e risveglio da sospensione sono provati; latenza del cold start e consumo Fly sono registrati.

**Outcome**

- Gli sviluppatori possono verificare il percorso reale da commit a runtime e il compromesso operativo scale-to-zero.

### 2. Motore semantico multilingue verificabile *(Enabler: scoperta semantica)*

---

**Includes**

- Postgres con pgvector e recipe fixture normalizzate, persistite nel ricettario indicato da un resolver configurato.
- Pipeline reale che compone nome, ingredienti, preparazione, tag e tempo disponibili, genera embedding e lo persiste.
- Piccolo comando diagnostico che vettorializza una query secondo la decisione dello spike e ordina solo le ricette dello stesso ricettario.
- Set di valutazione bilingue italiano/inglese con query di intenti, ingredienti e casi negativi.

**Verification**

- Il set versionato misura ranking cross-lingua e isolamento tra due ricettari usando provider, schema e query di produzione.
- Retry e rigenerazione sostituiscono l'embedding senza duplicare ricette; errori e output provider non validi restano tipizzati.
- Latenza e costo osservati sono confrontati con soglie concordate nello spike.

**Learning / risk**

- Verifica che il differenziatore trovi risultati utili alla scala prevista e chiarisce il costo inevitabile della query semantica.

**Outcome**

- Gli sviluppatori hanno evidenza eseguibile che la ricerca cross-lingua e lo scope per ricettario funzionano sul percorso reale.

### 3. Ricerca semantica nel ricettario di prova *(Theme: A. Scoperta semantica)*

---

**Includes**

- Home di prova con elenco ricette e campo di ricerca solo semantica sul ricettario configurato.
- Stati accessibili per vuoto, caricamento, nessun risultato, timeout e indisponibilità del provider.
- Risultati ordinati per similarità senza filtri, full-text o traduzione del contenuto.

**Verification**

- Tester non produttivi trovano una ricetta inglese con query italiane rappresentative e confrontano pertinenza con il set di valutazione.
- Ricette fixture di un secondo ricettario non compaiono né nell'elenco né nei risultati, inclusi errori e query manipolate.
- Telemetria conferma latenza, chiamate e costo del percorso completo osservati dal browser.

**Learning / risk**

- Misura se la pertinenza percepita giustifica il prodotto prima di investire nei flussi commodity di acquisizione e condivisione.

**Outcome**

- Un tester può usare il vero differenziatore su dati realistici in ambiente non produttivo.

### 4. Accesso Google e ricettari privati *(Theme: B. Accesso ai ricettari)*

---

**Includes**

- Auth.js con Google OAuth, sessione Postgres e logout.
- Creazione di un ricettario privato con creator e membership atomici; selezione tra più ricettari dell'utente.
- Sostituzione del ricettario configurato con il resolver basato sulla membership autenticata.
- Home vuota e accesso negato non rivelatore per ricettari estranei.

**Verification**

- Un nuovo utente entra con Google, crea un ricettario, torna con la stessa identità e può passare tra due ricettari propri.
- Accessi diretti e chiamate mutate verso un ricettario non membro falliscono senza fuga di metadati.
- La suite semantica continua a provare isolamento usando il nuovo resolver, senza cambiare la pipeline di ricerca.

**Outcome**

- Un utente dispone di uno o più spazi privati e ogni funzionalità successiva eredita un confine di ownership reale.

### 5. Ricette manuali subito correggibili *(Theme: C. Manutenzione delle ricette)*

---

**Includes**

- Form condiviso fra inserimento manuale ed edit per titolo, ingredienti e preparazione in testo libero.
- Salvataggio immediato, dettaglio e comparsa nell'elenco del ricettario corrente senza review intermedia.
- Rigenerazione dell'embedding a ogni modifica; tag e tempo restano best-effort e mai obbligatori.
- Gestione di conflitto, errore di salvataggio ed errore di reindicizzazione con retry sicuro.

**Verification**

- Un membro crea, consulta e corregge una ricetta; la nuova formulazione cambia coerentemente i risultati semantici.
- Campi mancanti o invalidi sono annunciati accessibilmente e non producono record parziali o duplicati.
- Un secondo ricettario e un non membro non possono vedere o modificare la ricetta.

**Outcome**

- Un membro può costruire e correggere il proprio ricettario senza struttura superflua, disponendo già della via di recupero per import futuri.

### 6. Import URL strutturato *(Theme: D. Acquisizione da fonti esterne)*

---

**Includes**

- Inserimento URL, fetch protetto da SSRF e parsing validato di `schema.org/Recipe` senza chiamata LLM.
- Progress sincrono basato sui passi reali fino al salvataggio immediato di testo, metadati, embedding e prima foto su R2.
- `sourceUrl`, tag e tempo best-effort; prima foto impostata come cover e duplicati esplicitamente consentiti.
- Errori precisi per URL non valido, timeout, pagina irraggiungibile, JSON-LD assente/non valido, foto e indicizzazione.

**Verification**

- Siti fixture con JSON-LD rappresentativi producono una ricetta ricercabile e correggibile senza invocare il provider LLM.
- Il browser mostra solo transizioni confermate dal backend; timeout e fallimenti di ogni step indicano causa e recupero possibile.
- La foto è servita da R2, non hotlinkata; retry e cleanup non duplicano ricetta, embedding o oggetti.

**Learning / risk**

- Misura compatibilità, latenza e hit-rate del percorso gratuito sul caso di aggiunta più frequente.

**Outcome**

- Un membro incolla un link strutturato e ottiene con poco attrito una ricetta salvata, visibile e ricercabile.

### 7. Fallback LLM per link non strutturati *(Theme: D. Acquisizione da fonti esterne)*

---

**Includes**

- Pulizia del contenuto e fallback automatico al modello economico quando una pagina leggibile non offre JSON-LD valido.
- Output strutturato validato nello stesso schema Recipe e nello stesso percorso di salvataggio, foto e indicizzazione.
- Timeout, limite dimensionale e trattamento esplicito di output invalido, contenuto non pertinente e provider indisponibile.
- Telemetria separata per invocazioni, costo, latenza, qualità e tasso di correzione successiva.

**Verification**

- Corpus versionato di pagine senza dati strutturati misura completezza utile di titolo, ingredienti e preparazione.
- Output inventato, incompleto o fuori schema non viene accettato silenziosamente; il messaggio propone edit, retry o copia-incolla secondo il caso.
- Le pagine con JSON-LD continuano a non chiamare il modello e i costi osservati rispettano il budget concordato.

**Learning / risk**

- Verifica qualità e costo del secondo differenziatore rispetto ai fallimenti tipici degli importatori tradizionali.

**Outcome**

- Un membro importa automaticamente molte ricette leggibili anche quando il sito non pubblica `schema.org/Recipe`.

### 8. Import da testo incollato *(Theme: D. Acquisizione da fonti esterne)*

---

**Includes**

- Area di copia-incolla che salta fetch e JSON-LD e riusa pulizia, schema LLM, salvataggio, indicizzazione e progress reali.
- Limiti e messaggi specifici per testo vuoto, troppo lungo, non pertinente o estrazione insufficiente.
- Accesso esplicito al percorso dalla schermata di errore per paywall, siti JS-heavy o fetch bloccato.

**Verification**

- Testi fixture rumorosi producono ricette salvate, ricercabili ed editabili tramite lo stesso motore già valutato.
- Da un import URL illeggibile, il membro raggiunge il fallback, incolla il testo e completa senza reinserire dati non necessari.
- Nessuna richiesta di rete viene fatta verso l'URL originale e invocazioni/costi LLM restano osservabili.

**Outcome**

- Un membro recupera una ricetta da contenuto accessibile solo a lui senza perdere il flusso di aggiunta.

### 9. Inviti e modifica condivisa *(Theme: E. Collaborazione)*

---

**Includes**

- Il creator genera e condivide un link/codice non prevedibile per il proprio ricettario.
- Un utente autenticato accetta l'invito e ottiene una membership; accettazioni ripetute sono idempotenti.
- Tutti i membri leggono, aggiungono ed editano le ricette senza ruoli ulteriori; un utente può appartenere a più ricettari.
- Stato chiaro per token invalido e accesso già acquisito, senza rivelare ricettari estranei.

**Verification**

- Due account Google accettano l'invito e osservano le modifiche reciproche nello stesso ricettario.
- Un non creator non genera inviti; token alterati, cookbook mutato e replay non elevano privilegi né duplicano membership.
- Le ricerche dei due membri coincidono nello stesso scope e nessun dato passa a un altro ricettario condiviso dagli stessi utenti.

**Learning / risk**

- Verifica che la collaborazione cookbook-centrica sia comprensibile senza un concetto di famiglia o ruoli granulari.

**Outcome**

- Familiari e amici mantengono insieme un ricettario privato con permessi paritari.

### 10. Foto multiple e cover *(Theme: F. Raccolta fotografica)*

---

**Includes**

- Aggiunta di più foto a una ricetta tramite il flusso di modifica, con storage su R2 e soli URL nel database.
- Prima foto come cover predefinita e selezione atomica di una diversa cover.
- Validazione di tipo e dimensione, stato accessibile di upload e recupero da fallimenti parziali.

**Verification**

- Un membro aggiunge più foto, cambia cover e vede la scelta stabile in elenco e dettaglio dopo una nuova sessione.
- Upload fallito non lascia riferimenti rotti; retry non duplica oggetti e il cleanup elimina gli orfani noti.
- Modifiche concorrenti preservano al massimo una cover e autorizzazione per ricettario.

**Outcome**

- Il ricettario conserva una raccolta fotografica controllata dagli utenti e indipendente dai siti sorgente.

### 11. MVP disponibile agli utenti selezionati *(Release: delivery)*

---

**Includes**

- Promozione dell'insieme NOW su Fly.io con database pgvector, bucket R2, OAuth e provider AI configurati per l'ambiente destinato agli utenti.
- Migrazioni, segreti, redirect OAuth, health check, rollback e procedure di rigenerazione embedding verificate.
- Scale-to-zero con `suspend`, limiti di consumo e dashboard minima per errori, latenza, costi e capacità dei free tier.
- Guida essenziale in-app su campi obbligatori, tre modalità di aggiunta, collaborazione e cold start iniziale.

**Verification**

- Utenti selezionati completano login, creazione/invito, tre modalità di add, edit, foto e ricerca cross-lingua sul deployment finale.
- Smoke test dopo deploy e rollback provano integrità, isolamento, storage e ricerca; allarmi sintetici coprono dipendenze esterne.
- Un periodo pilota registra pertinenza, correzioni post-import, hit-rate JSON-LD, fallback, cold start e costo per ricetta/query.

**Outcome**

- Familiari e amici selezionati possono usare in sicurezza l'MVP coerente nel suo ambiente previsto e fornire evidenza per le priorità successive.

## LATER

- **Filtri strutturati per tag e tempo**
  - **Promotion trigger:** gli utenti non ritrovano ricette pertinenti con la sola semantica e i metadati best-effort hanno copertura e qualità sufficienti.
  - **Expected value:** restringere rapidamente risultati numerosi senza migrazione o backfill.
- **Ricerca ibrida semantica e full-text**
  - **Promotion trigger:** le eval e le query reali mostrano fallimenti ricorrenti su nomi esatti o ingredienti che il ranking vettoriale non recupera.
  - **Expected value:** aumentare precisione sui termini esatti mantenendo la scoperta cross-lingua.
- **Ricettari pubblici tematici**
  - **Promotion trigger:** il pilota dimostra domanda per scoprire e curare raccolte oltre la cerchia invitata.
  - **Expected value:** rendere consultabili raccolte vegane, regionali o tematiche sfruttando `visibility`.
- **Gruppi sopra i ricettari**
  - **Promotion trigger:** gli stessi utenti vengono reinvitati spesso e il modello cookbook-centrico genera attrito misurabile.
  - **Expected value:** riusare membership fra più ricettari senza cambiare la collaborazione interna.
- **Macchina Fly sempre attiva**
  - **Promotion trigger:** cold start misurati causano abbandono o reclami tali da giustificare circa $3/mese.
  - **Expected value:** eliminare la latenza del primo accesso dopo inattività.

## OUT-OF-SCOPE

- **Lista della spesa e scaling porzioni** — richiedono quantità e unità strutturate, escluse deliberatamente per ridurre l'attrito.
- **Ricerca cross-ricettario** — l'MVP ricerca esclusivamente nel ricettario corrente.
- **Ruoli e permessi granulari** — tutti i membri sono pari; il solo creator è sufficiente per gli inviti MVP.
- **Famiglia/team come contenitore** — la collaborazione resta cookbook-centrica finché il reinvito non dimostra attrito.
- **Password, magic link e passkey** — Google OAuth evita provider email e recupero account applicativo; passkey immature per questo MVP.
- **Deduplicazione ricette** — duplicati della stessa sorgente sono esplicitamente consentiti.
- **Vector database dedicato, self-host degli embedding e IaC generalista** — scala, costo e semplicità favoriscono Postgres, API cloud e configurazione Fly minimale.

## Decision checkpoints

- **Dopo la slice 3:** qualità cross-lingua, latenza e costo percepiti → interrompere il prodotto, cambiare embedder/eval o confermare il resto dell'MVP.
- **Dopo la slice 7:** hit-rate JSON-LD, qualità LLM, correzioni e costo → cambiare modello/prompt, separare casi difficili o confermare il copia-incolla.
- **Dopo la slice 9:** comprensione degli inviti e frequenza multi-ricettario → mantenere il modello semplice o promuovere i gruppi da LATER.
- **Dopo la slice 11:** query senza risultato, uso metadati, cold start e costi reali → promuovere ricerca ibrida, filtri o macchina sempre attiva.

## Non-product work

- **Spike query embedding, massimo 2 giorni prima della slice 2:** chiarire come ottenere `embedding(query)` mentre `goal.md` e `arch-choices.md` vietano embedding a runtime sulle query; confrontare una chiamata cloud query-time e alternative compatibili sul medesimo set bilingue, misurando pertinenza, latenza, costo e complessità; uscire con una decisione documentata e soglie per le slice 2–3; scartare il codice sperimentale salvo fixture ed eval riusabili.

## Open questions

- Come viene generato il vettore della query? `concepts.md` richiede `embedding(query)`, ma `goal.md` e `arch-choices.md` vietano embedding a runtime sulle query; la decisione blocca le slice 2–3.
