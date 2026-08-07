# Recipe App — Delivery plan

- **Sources:** `sources/goal.md`, `sources/concepts.md`, `sources/arch-choices.md`, `sources/tech-choices.md`.
- **Current state:** Greenfield, nessun repository né infrastruttura esistente. Stack chiuso (TypeScript, Next.js App Router, Effect, Drizzle, Auth.js + Google OAuth, React Query); infrastruttura decisa nella forma (Postgres + pgvector, object storage R2, Fly.io con scale-to-zero `suspend`) ma con provider e modelli non ancora selezionati (vedi `Open questions`).

## Ordering criteria

- Prima la catena di delivery minima (0–1), poi la validazione del differenziatore con l'input reale più economico (3–4), poi una sola slice sottile per ciascun tema rimanente.
- Il rimedio dichiarato dalle fonti precede l'apertura di un altro tema: il copia-incolla con estrazione LLM (6) segue immediatamente i fallimenti nominati dall'aggiunta da link (5).
- Ogni pipeline o adapter condiviso segue tutti i suoi produttori `NOW` e ha un unico proprietario: estrattore LLM in (6), foto e object storage in (8).
- Identità dopo cattura e ricerca: nessuna delle loro evidenze dipende da proprietà o membership reale. Fino alla slice 9 lo scope è un ricettario configurato risolto da un unico risolutore, e l'audience dichiarata di ogni slice precedente è sviluppatore/tester sull'ambiente non pubblico.
- Slice iniziali strette finché convenzioni di delivery, dominio, test e UI richiedono revisione umana frequente; dimensione crescente solo dopo che i pattern esistono.

## Themes

| Theme | Desired outcome | First validation |
|---|---|---|
| A. Consultazione del ricettario | Chi apre l'app vede l'elenco delle ricette del ricettario corrente e ne legge una | 2 |
| B. Ricerca semantica cross-lingua | Si trova una ricetta per intento e in un'altra lingua, dentro il ricettario corrente | 4 |
| C. Cattura da link | Incollare un URL salva la ricetta senza passi obbligatori né review | 5 |
| D. Estrazione senza structured data | Anche da paywall, siti JS-heavy o pagine senza JSON-LD la ricetta si salva | 6 |
| E. Scrittura e correzione | Si inserisce a mano o si corregge una ricetta con lo stesso form | 7 |
| F. Foto della ricetta | Ogni ricetta è riconoscibile a colpo d'occhio e le sue foto non si rompono | 8 |
| G. Accesso | L'utente entra con il proprio account Google e l'app lo riconosce | 9 |
| H. Ricettario condiviso | Il creator invita familiari e amici e tutti lavorano da pari sullo stesso ricettario | 10 |

## Cross-functional concerns

- **Authorization:** Nessun permesso granulare: essere membro di un ricettario significa leggere ed editare tutto; unico ruolo è `Cookbook.creatorId`. Ogni lettura e scrittura passa da un unico risolutore del ricettario corrente; alla slice 9 quel risolutore è il seam in cui lo scope configurato viene sostituito dai ricettari dell'utente autenticato.
- **Validation and errors:** Errori applicativi come `Data.TaggedError`, gestiti con `catchTag` ai boundary; `Schema` valida (mai cast) l'output dell'estrazione LLM e le risposte delle API esterne; ogni fallimento di estrazione produce un messaggio riferito al passo reale che è fallito.
- **Operability:** Timeout e retry su fetch pagina, embedding e LLM; log per estrazione e per indicizzazione con esito, latenza e costo; nessun segreto lato client; scale-to-zero in modalità `suspend` con cold start atteso sub-secondo.
- **Accessibility and security:** URL e testo incollato trattati come input non fidato (schemi/host consentiti, limiti di dimensione, nessuna richiesta verso rete interna); form senza asterischi sui campi obbligatori e campi facoltativi marcati "(optional)".
- **Data integrity and recovery:** `embedding` è indice derivato, rigenerato a ogni salvataggio; una sola cover per ricetta; duplicati consentiti senza dedup; il salvataggio non è mai bloccato da campi derivati mancanti e un fallimento parziale (embedding, foto) non fa perdere la ricetta.

## NOW

### 0. Prerequisito repository *(Enabler: delivery)*

---

**Includes**

- Applicazione Next.js App Router in TypeScript con lint, typecheck, formattazione e test runner configurati.
- Pipeline CI che esegue build, lint, typecheck e test a ogni push.
- Convenzioni codificate in esempi minimi: Effect (`Context.Tag` + `Layer`, `Data.TaggedError`), React (`React.FC`, props come `type`), test co-locati.
- Nessun provisioning e nessun deploy.

**Verification**

- CI rossa su un test volutamente fallito e verde dopo la correzione, con build, lint, typecheck e test tutti eseguiti.

**Outcome**

- Base di delivery su cui ogni slice successiva è revisionabile e revertibile.

### 1. Walking skeleton deployato *(Enabler: delivery)*

---

**Includes**

- Immagine Docker dell'app e deploy da CI/CD su Fly.io via `fly.toml`, con scale-to-zero in modalità `suspend`.
- Migration runner con una migrazione non di dominio applicata al database del provider Postgres selezionato (decisione aperta).
- Estensione pgvector abilitata da migrazione, senza alcuna entità di dominio.
- Endpoint non di dominio che raggiunge il datastore a runtime tramite il driver reale su TCP.
- Nessuna entità di dominio, nessuna autenticazione, nessun tenant.

**Verification**

- Sull'ambiente non pubblico l'endpoint risponde leggendo dal database: round-trip reale, non risposta statica.
- La migrazione risulta applicata e la connessione regge al primo accesso dopo scale-to-zero; cold start misurato e registrato.
- Un secondo push produce un deploy completo senza intervento manuale.

**Outcome**

- L'infrastruttura decisa è connessa e in esecuzione, verificabile a ogni push.

### 2. Elenco e dettaglio del ricettario corrente *(Theme: A)*

---

**Includes**

- Schema `Cookbook` e `Recipe` (nome, ingredienti e preparazione come testo libero; tag e tempo opzionali) con migrazioni.
- Risolutore unico del ricettario corrente, per ora da configurazione, attraversato da ogni lettura.
- Home con elenco delle ricette del ricettario corrente e pagina di dettaglio.
- Seed controllato di ricette in italiano e in inglese come unico input, in assenza del flusso di aggiunta.

**Verification**

- Elenco e dettaglio mostrano solo le ricette del ricettario corrente; una ricetta di un altro ricettario non compare mai.
- Ricette prive di tag e tempo si aprono e si elencano senza degradare la vista.

**Outcome**

- Chi testa l'app sull'ambiente non pubblico vede e legge le ricette del ricettario configurato.

### 3. Motore semantico su corpus controllato *(Enabler: ricerca semantica)*

---

**Includes**

- Colonna `embedding` pgvector, indice HNSW e generazione degli embedding del corpus seedato tramite API cloud reale.
- Confronto dei candidati multilingue sullo stesso corpus, senza preselezione, per chiudere la scelta del modello.
- Comando diagnostico che ranka le ricette persistite per una query stampando punteggi, latenza e costo.

**Verification**

- Query in italiano recuperano nelle prime posizioni ricette scritte in inglese; recall registrato su un set fisso di query di controllo.
- Costo dell'indicizzazione dell'intero corpus e latenza di ranking misurati e confrontati con il target di ~$0.

**Learning / risk**

- La ricerca semantica cross-lingua è il differenziatore dichiarato: se il recall cross-lingua non regge, il prodotto ricade su alternative già mature e la scelta va rifatta prima di costruirvi sopra.

**Outcome**

- Evidenza eseguibile che il motore semantico cross-lingua funziona e costa quanto previsto, e modello di embedding selezionato su dati.

### 4. Ricerca semantica nel ricettario corrente *(Theme: B)*

---

**Includes**

- Campo di ricerca in home e pagina risultati basati sulla similarità, scoped al ricettario corrente.
- Path di embedding della query secondo la decisione aperta, con timeout e messaggio esplicito se quella modalità dipende da un servizio esterno indisponibile.
- Testo indicizzato pari a nome + ingredienti + preparazione, più tag e tempo quando presenti.
- Nessun filtro strutturato e nessuna ricerca full-text.

**Verification**

- Query come "cena leggera" e "pomodoro" restituiscono ricette pertinenti, incluse quelle scritte in inglese.
- Nessun risultato proviene da un ricettario diverso da quello corrente.
- Latenza della ricerca misurata sul path effettivamente scelto, cold start incluso.

**Outcome**

- Chi testa l'app trova per intento e cross-lingua le ricette del ricettario configurato.

### 5. Aggiunta da link con estrazione JSON-LD *(Theme: C)*

---

**Includes**

- Form "aggiungi da link", fetch reale della pagina con timeout e parse del JSON-LD `schema.org/Recipe`.
- Progress sincrono sui passi realmente eseguiti (scarico pagina → leggo ricetta → trovo ingredienti), con messaggio preciso sul passo fallito.
- Salvataggio immediato senza review, `sourceUrl` valorizzato, tag e tempo derivati best-effort e mai richiesti.
- Generazione dell'embedding al salvataggio con retry automatico: se fallisce, la ricetta resta salvata, marcata come non indicizzata e ri-indicizzabile.

**Verification**

- Da un food blog con JSON-LD la ricetta compare in elenco e in dettaglio con nome, ingredienti e preparazione, e diventa trovabile in ricerca.
- Paywall, timeout e assenza di JSON-LD producono tre messaggi distinti sul passo fallito, senza salvare ricette parziali.
- Un embedding fallito lascia la ricetta salvata e visibile in elenco; dopo il retry compare anche in ricerca.
- Un URL verso host non consentito o una pagina oltre il limite di dimensione vengono rifiutati prima del fetch.

**Learning / risk**

- L'hit-rate reale del JSON-LD sui siti effettivamente usati determina quanto peserà il fallback a pagamento.

**Outcome**

- Chi testa l'app salva una ricetta incollando un URL, senza alcun passo obbligatorio prima del salvataggio.

### 6. Copia-incolla ed estrazione LLM *(Theme: D)*

---

**Includes**

- Ingresso "incolla testo" che, dopo pulizia del contenuto, riusa lo stesso motore e lo stesso schema di output dell'aggiunta da link.
- Estrattore LLM con modello cheap selezionato (decisione aperta) e output strutturato validato con `Schema`, mai castato.
- Fallback automatico a LLM sul path URL quando il JSON-LD manca: l'estrattore LLM ha un unico proprietario.
- Log per estrazione di modello, costo, latenza ed esito; limite di dimensione del testo incollato.

**Verification**

- Una pagina con paywall, copiata e incollata, produce una ricetta salvata, visibile in dettaglio e trovabile in ricerca.
- Un URL senza JSON-LD si salva passando dal fallback, con il passo LLM visibile nel progress.
- Un output LLM non conforme allo schema fallisce con messaggio preciso e non salva ricette parziali.
- Costo medio per ricetta estratta via LLM misurato su un campione reale.

**Outcome**

- Chi testa l'app salva ricette anche dai siti che il path da link non riesce a leggere.

### 7. Inserimento manuale e correzione *(Theme: E)*

---

**Includes**

- Un solo form per inserimento manuale (campi vuoti) ed edit, con nome, ingredienti e preparazione come testo libero, senza parsing di quantità e unità.
- Rigenerazione dell'embedding a ogni salvataggio, coerente con la natura derivata dell'indice.
- Tag e tempo modificabili ma mai obbligatori, marcati come facoltativi.

**Verification**

- Una ricetta inserita a mano e una estratta e poi corretta risultano indistinguibili in elenco, dettaglio e ricerca.
- Dopo una correzione del testo la ricerca riflette il nuovo contenuto e non più il precedente.
- Una ricetta rimasta non indicizzata torna trovabile dopo un salvataggio dell'edit.

**Outcome**

- Chi testa l'app corregge un'estrazione imperfetta o inserisce da zero una ricetta che già conosce.

### 8. Foto e cover della ricetta *(Theme: F)*

---

**Includes**

- Bucket Cloudflare R2 e upload multiplo dal form condiviso, con il solo `url` persistito in Postgres.
- Download dell'immagine della pagina (`og:image` / JSON-LD) e ricarica sullo storage proprio in tutti i path di aggiunta da link, con il passo "salvo foto" aggiunto al progress.
- Cover pari alla prima foto per default e cambiabile, con invariante di una sola cover per ricetta.
- Limiti di tipo e dimensione; il fallimento sulla foto non blocca il salvataggio della ricetta.

**Verification**

- Elenco e dettaglio mostrano la cover; cambiando cover l'elenco si aggiorna e resta esattamente una cover.
- Un'immagine remota non scaricabile lascia la ricetta salvata con messaggio sul passo foto.
- Le foto restano servite dallo storage proprio anche modificando o rimuovendo la pagina originale.

**Outcome**

- Le ricette sono riconoscibili a colpo d'occhio e le loro foto non si rompono nel tempo.

### 9. Accesso con Google *(Theme: G)*

---

**Includes**

- Auth.js (NextAuth v5) con provider Google OAuth e sessione persistita su Postgres.
- Sostituzione, nell'unico risolutore del ricettario corrente, dello scope configurato con i ricettari dell'utente autenticato.
- Creazione del ricettario personale al primo accesso, con `creatorId` valorizzato.
- Tutte le rotte di lettura e scrittura richiedono una sessione valida.

**Verification**

- Un utente non autenticato non raggiunge nessuna ricetta né rotta di scrittura; autenticato vede solo i ricettari di cui è membro.
- Le ricette create prima del seam risultano assegnate a un ricettario con creator, senza perdita di dati.
- Logout e nuovo accesso restituiscono lo stesso utente e gli stessi ricettari.

**Outcome**

- L'utente entra con il proprio account Google e l'app lo riconosce come proprietario dei suoi ricettari.

### 10. Ricettario condiviso e inviti *(Theme: H)*

---

**Includes**

- Creazione di più ricettari, elenco dei propri ricettari e selezione di quello corrente.
- `Invitation` con token condivisibile come link/codice e scadenza opzionale; l'adesione da loggato crea una `Membership`.
- Membri pari: ogni membro legge ed edita tutte le ricette del ricettario, senza alcun ruolo oltre `creatorId`.

**Verification**

- Un secondo account apre il link di invito, entra nel ricettario e ne edita una ricetta; un non membro riceve un rifiuto e nessun dato.
- Token scaduto, già consumato o manomesso non concede alcun accesso.
- Un utente appartenente a più ricettari vede in elenco e in ricerca solo quello corrente.

**Outcome**

- Il creator invita familiari e amici e tutti lavorano da pari sullo stesso ricettario.

### 11. Rilascio agli utenti selezionati *(Release: delivery)*

---

**Includes**

- Ambiente di produzione su Fly con dominio, segreti (OAuth, embedding, LLM, storage) e callback Google configurati.
- Modalità `suspend` + scale-to-zero attiva, con il flag di macchina sempre calda documentato come reversibile.
- Rilevazione del costo mensile reale rispetto al target (~$0 di infrastruttura + centesimi di LLM).

**Verification**

- Un membro della famiglia, dal proprio dispositivo, completa accesso → aggiunta da link → ricerca → apertura ricetta.
- Cold start dopo un periodo di inattività misurato in produzione e giudicato accettabile o meno.
- Consumo reale di Fly, storage ed embedding dei primi giorni confrontato con il target di costo.

**Outcome**

- L'MVP è usabile da famiglia e amici sul dominio di produzione.

## LATER

- **Filtri di ricerca strutturati (tag, tempo) e ricerca ibrida semantica + full-text**
  - **Promotion trigger:** dalle slice 4–7 emergono query in cui la sola semantica non ritrova ricette che l'utente sa esserci.
  - **Expected value:** i campi derivati si popolano già da ora, quindi i filtri diventano abilitabili senza migrazione né lavoro retroattivo.
- **Concetto di gruppo/team sopra i ricettari**
  - **Promotion trigger:** dopo la slice 10, ri-invitare gli stessi membri su ogni nuovo ricettario risulta fastidioso nell'uso reale.
  - **Expected value:** rimuove l'unico svantaggio accettato del modello cookbook-centrico, in modo additivo.
- **Ricettari pubblici tematici (`visibility=public`)**
  - **Promotion trigger:** dopo la slice 10, richiesta esplicita di condividere un ricettario oltre i membri invitati.
  - **Expected value:** abilitabile sul modello esistente senza migrazione.
- **Ricerca cross-ricettario**
  - **Promotion trigger:** utenti in più ricettari cercano ripetutamente nel ricettario sbagliato dopo la slice 10.
  - **Expected value:** riduce l'attrito di chi tiene ricettari separati.
- **Macchina Fly sempre calda (`min_machines_running=1`)**
  - **Promotion trigger:** il cold start misurato nelle slice 1 e 11 risulta fastidioso all'uso.
  - **Expected value:** elimina la latenza iniziale al costo di ~$3/mese, con un flag reversibile.

## OUT-OF-SCOPE

- **Lista della spesa e scaling porzioni** — precluse dalla scelta di non strutturare gli ingredienti; entrambe dichiarate già fuori scope.
- **Ruoli e permessi granulari** — un solo concetto di condivisione e nessun permesso granulare; nell'MVP basta `creatorId`.
- **Autenticazione email+password, magic-link e passkeys** — le prime due richiedono un provider email, escluso dall'MVP; le passkeys hanno recupero account complesso e supporto Auth.js acerbo.
- **Passo di review obbligatorio nel flusso di aggiunta** — bloccare l'utente a ogni aggiunta è un costo esplicitamente rifiutato: si salva subito e si corregge dopo.
- **Deduplica delle ricette e normalizzazione di quantità/unità** — duplicati consentiti e normalizzazione deliberatamente minima.
- **Vector DB dedicato ed embedding self-hosted** — infra e costo in più senza beneficio alla scala prevista (≤10k ricette).
- **Hosting alternativi (Vercel, Cloudflare Workers + OpenNext, AWS Fargate)** — rispettivamente costi crescenti oltre l'Hobby, vincoli del modello fat-worker, assenza di scale-to-zero.
- **IaC versionata (SST, Terraform)** — over-engineering per l'MVP: bastano `fly.toml` e la CLI Fly.

## Decision checkpoints

- **Dopo 3:** recall cross-lingua, latenza e costo del modello di embedding → confermare il differenziatore e chiudere la scelta del modello, oppure fermarsi e riconsiderare la ricerca semantica prima di costruire la ricerca di prodotto.
- **Dopo 4:** query reali che la sola semantica non soddisfa → promuovere o meno i filtri strutturati e la ricerca ibrida da `LATER`.
- **Dopo 5:** hit-rate reale del JSON-LD sui siti effettivamente usati → dimensionare il peso del fallback LLM e il budget di estrazione.
- **Dopo 6:** costo e qualità dell'estrazione LLM per ricetta → decidere se estendere l'LLM anche a pagine con JSON-LD povero o restringerlo.
- **Dopo 10:** attrito reale del ri-invito tra ricettari → promuovere o meno il concetto di gruppo da `LATER`.
- **Dopo 11:** cold start e costo mensile misurati in produzione → promuovere o meno la macchina sempre calda.

## Open questions

- **Provider Postgres e driver:** le fonti elencano Neon *o* Supabase e `postgres.js` *o* `node-postgres` senza selezionarne uno; la scelta determina modalità di connessione, pooling e interazione con lo scale-to-zero. Blocca la slice 1 e ogni verifica di connessione successiva.
- **Modello di embedding multilingue:** indicato solo come esempio ("es. OpenAI `text-embedding-3-small`") con il vincolo di essere multilingue; nessuna fonte lo seleziona. Blocca le slice 3 e 4; la slice 3 lo chiude con evidenza.
- **Modello LLM per l'estrazione di fallback:** descritto come "cheap, Haiku-class" senza provider né modello selezionato. Blocca la slice 6 e il calcolo del costo per ricetta.
- **Embedding della query a runtime:** `goal.md` dichiara embedding usati "solo in fase di add, mai a runtime sulle query di ricerca", mentre `concepts.md` definisce la ricerca come `similarity(Recipe.embedding, embedding(query))` e `arch-choices.md` considera trascurabile il costo delle query. La differenza cambia se il path di lettura dipende da un servizio esterno, con relativi timeout e fallback. Blocca la slice 4.
