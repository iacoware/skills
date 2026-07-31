# Recipe App — Piano di delivery

- **Sources:** `sources/goal.md`, `sources/concepts.md`, `sources/arch-choices.md`, `sources/tech-choices.md`.
- **Current state:** Greenfield; modello, stack e servizi scelti, nessun repository applicativo o percorso runtime esistente.

## Ordering criteria

- Separare prerequisito repository e walking skeleton; mantenere inizialmente piccole le slice per revisionare presto convenzioni e delivery.
- Validare prima il differenziatore esistenziale: ricerca semantica cross-lingua su persistenza, embedding e ambiente reali.
- Usare ricette controllate normalizzate per provare la ricerca senza attendere i flussi di acquisizione.
- Approfondire poi l'acquisizione dal caso frequente ai fallback; sostituire infine lo scope configurato con identità e membership reali.

## Themes

| Theme | Desired outcome | First validation |
|---|---|---|
| A. Ricerca semantica | Trovare nel ricettario corrente ricette pertinenti anche tra lingue diverse. | Ricerca cross-lingua nel ricettario corrente |
| B. Consultazione | Consultare rapidamente il contenuto del ricettario corrente. | Home e dettaglio ricetta |
| C. Acquisizione e manutenzione | Salvare con attrito minimo ricette da fonti diverse e correggerle dopo. | Import da URL con JSON-LD |
| D. Accesso e collaborazione | Usare più ricettari privati e condividerli tra membri paritari. | Accesso Google a un ricettario privato |

## Cross-functional concerns

- **Authorization:** Ogni query e mutazione è vincolata a `cookbookId`; un unico resolver passa dallo scope configurato non pubblico alla membership della sessione Google.
- **Validation and errors:** Schema valida input, JSON-LD e output LLM; gli errori sono tipizzati e gli import mostrano fase reale e causa precisa senza review obbligatoria.
- **Operability:** Log correlati per richiesta e fase, timeout/retry sugli adapter esterni, metriche su latenza, errori, costo LLM e cold start; nessun segreto nei log.
- **Accessibility and security:** Flussi da tastiera, stato/progresso annunciato, campi opzionali espliciti, URL e upload non fidati limitati per tipo/dimensione e protetti da SSRF.
- **Data integrity:** Una sola cover per ricetta; embedding rigenerato dopo ogni modifica indicizzata; duplicati consentiti deliberatamente.

## NOW

### 0. Repository verificabile *(Enabler: delivery)*

---

**Includes**

- Applicazione TypeScript/Next.js con Effect, formattazione e struttura minima per test automatici.
- CI con build, lint, typecheck e test, senza provisioning o deploy.

**Verification**

- La CI esegue con successo build, lint, typecheck e test da checkout pulito.

**Outcome**

- Gli sviluppatori possono integrare incrementi su una baseline riproducibile e revisionabile.

### 1. Walking skeleton in ambiente non produttivo *(Enabler: delivery)*

---

**Includes**

- Container Docker stateless e configurazione Fly.io con `suspend` e scale-to-zero.
- CI/CD, provisioning minimo e route diagnostica reale in un ambiente non produttivo rappresentativo.
- Configurazione e segreti separati dall'immagine, senza autenticazione, tenancy o CRUD di dominio.

**Verification**

- Un commit produce e distribuisce l'immagine; la route diagnostica risponde dopo deploy e risveglio da sospensione.
- Log e misura del cold start sono consultabili nell'ambiente.

**Outcome**

- Gli sviluppatori verificano il percorso completo da commit a runtime Fly.io.

### 2. Pipeline vettoriale su ricette controllate *(Enabler: ricerca semantica)*

---

**Includes**

- Neon o Supabase con Postgres, pgvector e schema minimo `Cookbook`/`Recipe` tramite Drizzle.
- Resolver unico di uno scope configurato non pubblico, applicato a scritture e letture.
- Fixture normalizzate attraversano validazione, embedding cloud multilingue, persistenza e indice HNSW reali.

**Verification**

- Un test in ambiente inserisce fixture tramite la pipeline di produzione e ne verifica vettore, dati canonici e isolamento tra due cookbook.
- Il rerun è osservabile e non richiede scritture dirette di embedding precalcolati.

**Learning / risk**

- Verifica compatibilità Drizzle/pgvector, qualità del modello e affidabilità dell'adapter prima della UI di ricerca.

**Outcome**

- Gli sviluppatori dispongono di evidenza eseguibile che ricette reali sono indicizzabili nello scope corretto.

### 3. Ricerca cross-lingua nel ricettario corrente *(Theme: A)*

---

**Includes**

- Campo di ricerca semantica e risultati essenziali ordinati per similarità nel cookbook risolto.
- Indice composto da nome, ingredienti e preparazione, più tag e tempo quando presenti.
- Query pgvector scoped, contenuto essenziale del risultato e stati vuoto/errore.

**Verification**

- In ambiente, la query italiana `pomodoro` trova la fixture inglese pertinente e non restituisce ricette dell'altro cookbook.
- Test di accettazione coprono pertinenza minima, nessun risultato e guasto del provider di embedding.

**Learning / risk**

- Misura se il differenziatore cross-lingua è abbastanza rilevante e rapido da giustificare il prodotto rispetto a Mealie.

**Outcome**

- Un utente trova ricette pertinenti nel ricettario corrente senza conoscere lingua o parole esatte della fonte.

### 4. Home e dettaglio ricetta *(Theme: B)*

---

**Includes**

- Home con elenco delle ricette del cookbook corrente, cover disponibile e stato vuoto.
- Dettaglio con titolo, ingredienti e preparazione in testo libero, foto e metadati best-effort disponibili.

**Verification**

- Test di accettazione naviga da home a dettaglio e conferma che nessun dato di un altro cookbook sia visibile.
- Controllo accessibilità copre tastiera, gerarchia dei titoli, immagini e stato vuoto.

**Outcome**

- Un utente consulta dall'inizio alla fine le ricette del ricettario corrente.

### 5. Import da URL con JSON-LD *(Theme: C)*

---

**Includes**

- Input URL, fetch sicuro, pulizia e parsing validato di `schema.org/Recipe` senza LLM.
- Salvataggio immediato di campi canonici, tag/tempo opzionali, embedding e immagine sorgente copiata su R2.
- Progresso sincrono basato su eventi reali e messaggio specifico per la fase fallita.

**Verification**

- Un URL fixture con JSON-LD produce una ricetta ricercabile e una foto servita da R2 senza schermata di review.
- Test coprono URL invalido, host vietato, timeout, JSON-LD malformato e fallimento foto senza corrompere i dati.

**Learning / risk**

- Misura copertura, latenza e affidabilità del percorso gratuito sul caso di acquisizione più frequente.

**Outcome**

- Un utente incolla un URL supportato e trova subito la ricetta salvata nel proprio ricettario.

### 6. Correzione dopo il salvataggio *(Theme: C)*

---

**Includes**

- Form di modifica per titolo, ingredienti e preparazione liberi, con tag e tempo derivati non obbligatori.
- Salvataggio nello stesso cookbook e rigenerazione dell'embedding dal contenuto aggiornato.

**Verification**

- Test di accettazione corregge una ricetta importata e la ritrova con termini presenti solo dopo la modifica.
- Validazione conferma che un errore di reindicizzazione non esponga uno stato canonico incoerente.

**Outcome**

- Un utente corregge un'estrazione imperfetta quando serve, senza attrito durante l'import.

### 7. Inserimento manuale *(Theme: C)*

---

**Includes**

- Lo stesso form di modifica si apre vuoto per creare una ricetta con i soli campi canonici.
- Salvataggio immediato e indicizzazione; tag e tempo derivati restano non bloccanti e best-effort.

**Verification**

- Test di accettazione crea una ricetta manuale, la vede in home e la trova con ricerca semantica.
- Test di validazione copre campi obbligatori, errori di salvataggio e isolamento del cookbook.

**Outcome**

- Un utente memorizza una ricetta conosciuta senza strutturare ingredienti o quantità.

### 8. Fallback LLM per URL non strutturati *(Theme: C)*

---

**Includes**

- In assenza di JSON-LD, il contenuto pulito passa a un modello economico con output strutturato validato.
- Retry/timeout limitati, budget osservabile e nessun fallback LLM quando il parsing diretto riesce.
- Salvataggio, indicizzazione, foto e progresso riusano il percorso di import già verificato.

**Verification**

- Un URL fixture senza JSON-LD produce una ricetta ricercabile; metriche distinguono parser diretto e fallback pagato.
- Test coprono output invalido, contenuto insufficiente, limite di costo e indisponibilità del modello.

**Learning / risk**

- Misura qualità e costo del vantaggio competitivo sui siti che gli importatori tradizionali non leggono.

**Outcome**

- Un utente salva automaticamente una ricetta da una pagina leggibile priva di dati strutturati.

### 9. Import da testo incollato *(Theme: C)*

---

**Includes**

- Input testo per contenuti da paywall o siti JS-heavy, senza fetch né tentativo JSON-LD.
- Pulizia, estrazione LLM, validazione, salvataggio, embedding e progresso riusano il motore esistente.

**Verification**

- Test di accettazione incolla testo rumoroso e ottiene una ricetta ricercabile senza chiamate HTTP alla fonte.
- Test coprono testo vuoto, output incompleto, errore LLM e messaggio di recupero specifico.

**Outcome**

- Un utente aggira un URL illeggibile incollando il contenuto e salva comunque la ricetta.

### 10. Galleria e cover della ricetta *(Theme: C)*

---

**Includes**

- Upload di più foto su R2 durante creazione o modifica.
- Prima foto come cover predefinita, selezione di una nuova cover e rimozione sicura.

**Verification**

- Test di accettazione aggiunge più foto, cambia cover e verifica home e dettaglio dopo ricaricamento.
- Test di concorrenza e vincolo dati conferma una sola cover; test storage copre upload/rimozione falliti.

**Outcome**

- Un utente conserva più immagini e sceglie quella rappresentativa della ricetta.

### 11. Accesso Google a un ricettario privato *(Theme: D)*

---

**Includes**

- Auth.js v5 con Google OAuth, sessione Postgres e onboarding del primo cookbook privato.
- Il resolver di scope passa dalla configurazione alla membership della sessione in un solo seam.
- Route, query e mutazioni richiedono sessione e appartenenza, senza ruoli granulari.

**Verification**

- Test di accettazione autentica due account e dimostra isolamento completo tra i rispettivi cookbook.
- Test di sicurezza coprono sessione assente/scaduta, cookbook manipolato e accesso non membro.

**Learning / risk**

- Verifica che la dipendenza da Google e l'onboarding mantengano basso l'attrito per famiglia e amici.

**Outcome**

- Un utente Google accede al proprio ricettario privato senza password o provider email.

### 12. Più ricettari per utente *(Theme: D)*

---

**Includes**

- Creazione di cookbook privati e selezione esplicita del ricettario corrente.
- Elenco membership dell'utente; ogni home, ricerca e mutazione segue lo scope selezionato.

**Verification**

- Test di accettazione crea e alterna due cookbook, verificando elenchi e risultati di ricerca distinti.
- Test di autorizzazione rifiuta selezione e mutazione di un cookbook senza membership.

**Outcome**

- Un utente organizza e usa più ricettari senza mescolarne ricette o ricerca.

### 13. Invito e collaborazione paritaria *(Theme: D)*

---

**Includes**

- Il creator genera un link/codice non prevedibile, opzionalmente in scadenza, per un singolo cookbook.
- Un utente autenticato accetta l'invito e ottiene membership; tutti i membri leggono e modificano allo stesso modo.
- Accettazione idempotente per membro, validità condivisibile fino a scadenza/revoca e audit minimo.

**Verification**

- Test end-to-end invita un secondo account, che modifica una ricetta condivisa senza accedere agli altri cookbook del creator.
- Test coprono token invalido, scaduto o revocato, riapertura dallo stesso membro e uso da più invitati.

**Outcome**

- Familiari e amici collaborano come pari in uno specifico ricettario condiviso.

## LATER

- **Filtri strutturati per tag e tempo**
  - **Promotion trigger:** Le sessioni NOW mostrano ricerche frequenti per vincoli esatti che la similarità non soddisfa.
  - **Expected value:** Usa i metadati già popolati per restringere risultati senza migrazione retroattiva.
- **Ricerca ibrida full-text e semantica**
  - **Promotion trigger:** Le misure di pertinenza NOW mostrano fallimenti sistematici su nomi o ingredienti esatti.
  - **Expected value:** Migliora precisione senza perdere richiamo cross-lingua.
- **Ricettari pubblici tematici**
  - **Promotion trigger:** Utenti chiedono scoperta o condivisione oltre i membri invitati.
  - **Expected value:** Abilita cataloghi pubblici tramite `visibility=public` già modellata.
- **Gruppi sopra i ricettari**
  - **Promotion trigger:** Telemetria e interviste mostrano reinviti ripetuti come attrito materiale.
  - **Expected value:** Riusa una membership di gruppo su più cookbook.
- **Ricerca cross-ricettario**
  - **Promotion trigger:** Utenti con più cookbook cambiano spesso scope per ritrovare la stessa ricetta.
  - **Expected value:** Trova contenuti autorizzati senza selezionare prima un ricettario.
- **Passkeys**
  - **Promotion trigger:** La dipendenza da Google limita adozione e Auth.js offre recupero account maturo.
  - **Expected value:** Riduce la dipendenza dal provider mantenendo accesso senza password.

## OUT-OF-SCOPE

- **Lista della spesa e scaling porzioni** — Richiedono ingredienti strutturati, esclusi per minimizzare l'attrito MVP.
- **Parsing di quantità e unità** — Il testo libero è una scelta deliberata e sufficiente per lettura e ricerca semantica.
- **Ruoli e permessi granulari** — Nell'MVP tutti i membri sono pari; `creatorId` identifica solo chi invita.
- **Review obbligatoria durante l'import** — Contrasta il salvataggio immediato; le correzioni avvengono dopo.
- **Email/password e magic link** — Richiedono invio email e recupero credenziali, incompatibili con costo e semplicità MVP.
- **Vector database dedicato e IaC multi-cloud** — Scala prevista e singolo deploy non ne giustificano costo e complessità.

## Decision checkpoints

- **After slice 3:** Pertinenza cross-lingua, latenza e costo reali → fermare o riposizionare il prodotto, oppure cambiare modello/composizione dell'indice prima degli altri temi.
- **After slice 5:** Copertura JSON-LD e fallimenti per fonte → cambiare pulizia/progressione o anticipare il fallback che copre il rischio dominante.
- **After slice 8:** Qualità, latenza e costo LLM su pagine reali → cambiare modello, limiti o trattamento degli errori prima del copia-incolla.
- **After slice 13:** Tasso di invito, collaborazione e reinviti → promuovere gruppi o riordinare gli approfondimenti di accesso.

## Open questions

- Come viene vettorializzata la query? La ricerca definisce `embedding(query)`, ma `goal.md` e `arch-choices.md` vietano esplicitamente l'uso di embedding a runtime sulle query; la decisione cambia costo, adapter e fattibilità della slice 3.
