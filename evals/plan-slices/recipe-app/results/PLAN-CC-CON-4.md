# Recipe App — Delivery plan

- **Sources:** `sources/goal.md`, `sources/concepts.md`, `sources/arch-choices.md`, `sources/tech-choices.md`.
- **Current state:** Greenfield — nessun codice, nessun ambiente, nessun servizio provisionato; tutte le scelte di stack e infrastruttura sono già decise.

## Ordering criteria

- Prima il percorso di consegna reale minimo, poi il differenziatore: la ricerca semantica cross-lingua è il rischio esistenziale ("senza di essa staremmo riscrivendo Mealie").
- Il motore di ricerca si valida con l'input reale più economico (corpus fixture attraverso persistenza ed embedding di produzione) prima di costruirne l'UI.
- Il percorso di correzione precede la prima slice che può creare stati imperfetti: l'edit arriva prima dell'estrazione automatica.
- Il confine di ricettario nasce con la prima slice che persiste dati, dietro un unico resolver `CurrentCookbook`; l'identità lo sostituisce a quel solo seam.
- Ampiezza prima di profondità dopo i differenziatori; unica eccezione: il fallback di estrazione LLM segue subito l'add-da-link perché è il secondo differenziatore dichiarato.

## Themes

| Theme | Desired outcome | First validation |
|---|---|---|
| A. Consultazione del ricettario | Un lettore apre l'app e legge le ricette del ricettario corrente | 3. Elenco e dettaglio ricetta |
| B. Ricerca semantica cross-lingua | Un utente trova una ricetta cercandola nella propria lingua, qualunque sia quella della ricetta | 4. Ricerca semantica in Home |
| C. Scrittura e correzione | Un utente scrive una ricetta da zero e corregge qualsiasi ricetta salvata | 5. Form unico di creazione ed edit |
| D. Cattura da web | Un utente porta dentro una ricetta trovata online con attrito minimo | 6. Aggiunta da link con JSON-LD |
| E. Foto della ricetta | Le ricette hanno foto proprie, stabili nel tempo | 8. Foto multiple e cover |
| F. Identità utente | Ogni utente entra con Google e vede solo ciò che gli appartiene | 9. Accesso con Google |
| G. Ricettario condiviso | Famiglia e amici collaborano da pari sullo stesso ricettario | 10. Ricettari e ricettario corrente |

## Cross-functional concerns

- **Authorization:** ogni lettura e scrittura di `Recipe` e `Photo` passa dall'unico resolver `CurrentCookbook`; nessuna query senza `cookbookId`. Lo scope è configurato dalla slice 2, derivato dalla sessione dalla slice 9 (seam unico), verificato contro `Membership` dalla slice 11.
- **Validation and errors:** errori applicativi solo come `Data.TaggedError`, gestiti con `catchTag` ai boundary; output LLM e risposte esterne validati con `Schema`, mai castati; ogni fallimento di estrazione produce un messaggio riferito al passo reale.
- **Operability:** timeout e retry espliciti su fetch pagina, LLM ed embedding; log strutturato per passo di estrazione con esito, durata e costo; cold start Fly misurato a ogni deploy in ambiente rappresentativo.
- **Accessibility and security:** progress annunciato con `aria-live`, campi obbligatori non marcati con asterisco e opzionali etichettati "optional"; fetch limitato a http/https con blocco degli indirizzi non pubblici (SSRF) e tetto di dimensione; gli ambienti precedenti alla slice 9 non sono pubblicamente raggiungibili.
- **Data integrity and recovery:** `embedding` è indice derivato, rigenerato a ogni scrittura da nome + ingredienti + preparazione + tag/tempo; il fallimento di embedding o foto non deve perdere il testo della ricetta; `prepTime` e `tags` restano opzionali; una sola cover per ricetta.

## NOW

### 0. Repository e pipeline di verifica *(Enabler: delivery)*

---

**Includes**

- Progetto Next.js (App Router) + TypeScript con Effect, Drizzle e Vitest configurati; nessun provisioning, nessun deploy.
- CI su push e PR: build, lint, typecheck, test.
- Un test verticale minimo su logica di dominio pura, per fissare le convenzioni di test.

**Verification**

- La CI fallisce su un errore di tipo e su una violazione di lint introdotti di proposito, e torna verde dopo il fix.

**Outcome**

- Uno sviluppatore riceve feedback automatico e ripetibile su ogni commit.

### 1. Walking skeleton deployato su Fly *(Enabler: delivery)*

---

**Includes**

- Dockerfile e `fly.toml` con `suspend` + scale-to-zero; deploy da CI su ambiente non-produzione non pubblicamente raggiungibile.
- Postgres provisionato con `pgvector` abilitato e prima migrazione Drizzle eseguita dalla pipeline.
- Route `/health` che esegue una query reale sul database via driver TCP.
- Nessuna autenticazione, nessuna entità di dominio.

**Verification**

- `/health` risponde dal deploy in cloud riportando l'esito della query.
- Cold start misurato e registrato dopo un periodo di inattività.

**Learning / risk**

- Il risveglio `suspend` è tollerabile e il container Node regge la connessione TCP verso il Postgres scelto senza driver serverless?

**Outcome**

- Percorso di consegna reale end-to-end, deployato e osservabile.

### 2. Pipeline di embedding e ranking vettoriale su corpus reale *(Enabler: ricerca semantica)*

---

**Includes**

- Schema `Cookbook` e `Recipe` (nome, ingredienti, preparazione, tag, tempo, `cookbookId`, `embedding`) con indice HNSW.
- Resolver unico `CurrentCookbook` a scope configurato, attraversato da ogni query.
- Servizio di embedding come `Context.Tag` + layer adapter cloud, invocato solo in scrittura.
- Corpus di ricette reali in italiano e inglese importato attraverso il path di produzione di persistenza ed embedding.
- Comando diagnostico che classifica una query e stampa punteggi, latenza e costo.

**Verification**

- "pomodoro" porta in cima ricette scritte in inglese; "cena leggera" restituisce piatti coerenti, senza tradurre nulla.
- Il comando riporta latenza di ranking e costo totale di embedding del corpus, confrontabile col target di centesimi.
- La stessa query eseguita con un altro `cookbookId` non restituisce alcuna ricetta del corpus.

**Learning / risk**

- Rischio esistenziale: se il ranking cross-lingua non è utilizzabile, il prodotto perde il suo unico differenziatore.
- Verifica che l'embedder scelto sia realmente multilingue e non solo multilingue nominalmente.

**Outcome**

- Uno sviluppatore misura qualità, latenza e costo della ricerca cross-lingua sul path di produzione.

### 3. Elenco e dettaglio ricetta *(Theme: A)*

---

**Includes**

- Home con l'elenco delle ricette del ricettario corrente restituito dal resolver.
- Pagina di dettaglio con nome, ingredienti, preparazione, tag e tempo se presenti, link alla fonte se presente.
- Stato vuoto quando il ricettario non contiene ricette.

**Verification**

- Dal deploy, l'elenco mostra le ricette del corpus e il dettaglio ne apre una.
- Cambiando il ricettario configurato, elenco e dettaglio cambiano di conseguenza.

**Outcome**

- Un lettore consulta le ricette del proprio ricettario dall'app deployata.

### 4. Ricerca semantica in Home *(Theme: B)*

---

**Includes**

- Campo di ricerca in Home: la query viene embeddata a runtime e classificata su pgvector nello scope del ricettario corrente.
- Risultati ordinati per similarità, apribili in dettaglio, con stato "nessun risultato".
- Nessun filtro strutturato e nessuna ricerca full-text.

**Verification**

- Dal deploy, cercando "pomodoro" compaiono ricette in inglese senza alcuna traduzione.
- Le ricette di un altro ricettario non compaiono mai tra i risultati.
- Latenza end-to-end della ricerca misurata sull'ambiente deployato, incluso il caso post-cold-start.

**Learning / risk**

- Il ranking regge query vaghe ("cena leggera") su un ricettario reale, o serviranno filtri o ricerca ibrida?

**Outcome**

- Un utente trova una ricetta cercandola nella propria lingua, qualunque sia quella della ricetta.

### 5. Scrittura e correzione della ricetta *(Theme: C)*

---

**Includes**

- Un solo form, usato per l'inserimento manuale (campi vuoti) e per l'edit: nome, ingredienti e preparazione come testo libero.
- Salvataggio con rigenerazione dell'embedding; nessun campo accessorio richiesto, opzionali etichettati "optional".
- Nessun parsing di quantità e unità.

**Verification**

- Una ricetta scritta a mano compare in elenco ed è trovata dalla ricerca semantica.
- Correggendo il testo di una ricetta importata, la ricerca riflette il nuovo contenuto.
- Se il servizio di embedding non risponde, il testo della ricetta viene comunque salvato e l'indice risulta rigenerabile.

**Outcome**

- Un utente scrive una ricetta da zero e corregge qualsiasi ricetta salvata, in qualsiasi momento.

### 6. Aggiunta da link con dati strutturati *(Theme: D)*

---

**Includes**

- Input URL in Home con estrazione sincrona e progress sui passi reali (`Scarico pagina → Leggo ricetta → Salvo`).
- Fetch della pagina con Effect `HttpClient`: timeout, tetto di dimensione, blocco di schemi e indirizzi non pubblici.
- Parse del JSON-LD `schema.org/Recipe` validato con `Schema`, con `sourceUrl` persistito.
- Salvataggio immediato senza alcun passo di review; messaggio d'errore riferito al passo fallito (paywall, timeout, ricetta assente).

**Verification**

- Un URL con JSON-LD produce una ricetta salvata, visibile e ricercabile, senza alcuna chiamata LLM.
- Un URL paywall mostra il messaggio dello step fallito, non un errore generico, e non salva una ricetta vuota.
- Un URL che risolve a un indirizzo privato viene rifiutato prima del fetch.

**Learning / risk**

- Hit-rate reale del JSON-LD su un campione dei siti effettivamente usati dalla famiglia: determina quanto peserà il fallback a pagamento.

**Outcome**

- Un utente salva una ricetta incollando un link, con progresso reale e a costo zero.

### 7. Fallback di estrazione LLM *(Theme: D)*

---

**Includes**

- Estrazione con LLM cheap a output strutturato validato da `Schema`, attivata solo quando manca il JSON-LD; stesso schema Recipe del path diretto.
- Passo di progress dedicato, timeout, retry limitato e costo per estrazione loggato.
- Derivazione best-effort di `tags` e `prepTime`, mai richiesta all'utente e mai bloccante.

**Verification**

- Un URL privo di JSON-LD produce una ricetta salvata con nome, ingredienti e preparazione corretti su un campione controllato.
- Un output LLM non conforme allo schema non persiste dati parziali e produce un errore comprensibile.
- Costo medio per estrazione registrato sul campione e confrontato col target di frazioni di cent.

**Learning / risk**

- Secondo differenziatore: le pagine senza structured data — dove il benchmark Mealie fallisce — diventano davvero utilizzabili?

**Outcome**

- Un utente salva ricette anche da siti privi di dati strutturati.

### 8. Foto della ricetta *(Theme: E)*

---

**Includes**

- Upload di più foto su Cloudflare R2 con limiti di tipo e dimensione; nel database solo l'`url`.
- Cover: prima foto per default, cambiabile; invariante di una sola cover per ricetta.
- Durante l'add da link, download dell'immagine da `og:image` o JSON-LD e ricarica su R2 per evitare hotlinking.

**Verification**

- Una ricetta importata da link mostra la cover servita da R2 e non dal sito originale.
- Il fallimento del download immagine non impedisce il salvataggio della ricetta.
- Cambiando cover, elenco e dettaglio mostrano la nuova miniatura.

**Outcome**

- Le ricette hanno foto proprie che non si rompono quando la fonte cambia.

### 9. Accesso con Google *(Theme: F)*

---

**Includes**

- Auth.js (NextAuth v5) con Google OAuth e sessioni su Postgres.
- Al primo accesso, creazione del ricettario personale con `creatorId` e relativa `Membership`.
- Sostituzione, al solo seam del resolver `CurrentCookbook`, dello scope configurato con quello derivato dalla sessione.
- Tutte le route e le API applicative richiedono una sessione valida.

**Verification**

- Un utente non autenticato non raggiunge alcuna ricetta né alcuna API, nemmeno per URL diretto.
- Due account distinti vedono ricettari distinti senza alcuna variabile di configurazione residua.

**Outcome**

- Ogni utente entra con Google e vede solo il proprio ricettario.

### 10. Ricettari e ricettario corrente *(Theme: G)*

---

**Includes**

- Creazione di nuovi ricettari con nome e `visibility` privata.
- Selettore del ricettario corrente; elenco, ricerca e aggiunta operano sullo scope selezionato.

**Verification**

- Una ricetta aggiunta a un secondo ricettario non compare nella ricerca del primo.
- Il ricettario selezionato persiste tra navigazioni e nuove sessioni.

**Outcome**

- Un utente organizza le ricette in più ricettari e passa dall'uno all'altro.

### 11. Invito e ingresso in un ricettario *(Theme: G)*

---

**Includes**

- Generazione di un invito con token condivisibile via link o codice, con `expiresAt` opzionale.
- Apertura dell'invito da utente loggato che crea una `Membership`; chi non è loggato passa da Google e ritorna all'invito.
- Gestione esplicita di invito non valido, scaduto o revocato.

**Verification**

- Un secondo account che apre il link vede il ricettario tra i propri, ne legge e ne edita le ricette da pari.
- Un token manomesso o scaduto non crea alcuna membership.
- Un non membro che chiama direttamente l'API del ricettario riceve un rifiuto.

**Outcome**

- Il creator condivide un ricettario con un link e i membri collaborano da pari.

### 12. Aggiunta da testo incollato *(Theme: D)*

---

**Includes**

- Ingresso "incolla testo" in Home: pulizia del contenuto e stessa estrazione LLM, senza fetch e senza JSON-LD.
- Suggerimento esplicito di questo percorso quando l'add da link fallisce per paywall o pagina non leggibile.

**Verification**

- Il testo copiato da una pagina paywall produce una ricetta salvata e ricercabile.
- Un testo che non è una ricetta produce un errore comprensibile senza salvare nulla.

**Outcome**

- Nessuna pagina resta irraggiungibile: l'utente ha sempre una via per salvare la ricetta.

### 13. Rilascio a famiglia e amici *(Release: delivery)*

---

**Includes**

- Ambiente di produzione su Fly con dominio, secret gestiti e credenziali Google OAuth di produzione.
- Migrazioni Drizzle eseguite dalla pipeline verso il Postgres di produzione.
- Configurazione `suspend` + scale-to-zero attiva e reversibile da `fly.toml`.

**Verification**

- Un membro della famiglia, dal proprio dispositivo, entra con Google, salva una ricetta da link e la ritrova cercandola.
- Cold start e costo del primo periodo misurati in produzione e confrontati col target di centesimi al mese.

**Outcome**

- Famiglia e amici usano l'app in produzione al costo previsto.

## LATER

- **Filtri strutturati per tag e tempo**
  - **Promotion trigger:** nella slice 4 il solo ranking semantico non basta a restringere risultati su un ricettario reale.
  - **Expected value:** i campi si popolano già dalla slice 7, quindi il filtro si abilita senza migrazione né lavoro retroattivo.
- **Ricerca ibrida semantica + full-text**
  - **Promotion trigger:** ricerche per nome esatto o per singolo ingrediente non trovano la ricetta attesa.
  - **Expected value:** copre le query lessicali dove il solo embedding perde precisione.
- **Macchina Fly sempre calda**
  - **Promotion trigger:** il cold start misurato nelle slice 1 e 13 risulta fastidioso per i primi utenti.
  - **Expected value:** latenza costante al costo noto di circa $3/mese, con un solo flag in `fly.toml`.
- **Cancellazione della ricetta**
  - **Promotion trigger:** estrazioni fallite o duplicati accumulano rumore nel ricettario dopo l'uso reale.
  - **Expected value:** ripulisce il ricettario senza introdurre deduplica automatica.
- **Ricettari pubblici tematici e concetto di gruppo**
  - **Promotion trigger:** richiesta di condividere fuori dai membri, o fastidio nel re-invitare le stesse persone in ogni ricettario.
  - **Expected value:** entrambi additivi su `visibility` e sopra `Membership`, senza migrazione.

## OUT-OF-SCOPE

- **Ingredienti strutturati, lista della spesa e scaling porzioni** — trade-off accettato: la ricerca è semantica e chi legge interpreta il testo, quindi la normalizzazione fine non paga.
- **Review obbligatoria prima del salvataggio** — esplicitamente rifiutata: un'estrazione imperfetta è un costo accettabile, bloccare l'utente a ogni aggiunta no.
- **Deduplica delle ricette** — i duplicati nello stesso ricettario sono consentiti per scelta.
- **Email+password, magic-link e passkeys** — i primi due richiedono un provider email; le passkeys hanno recupero account complesso e supporto Auth.js acerbo.
- **Ruoli e permessi granulari, ricerca cross-ricettario, vector DB dedicato, IaC versionata** — nell'MVP bastano `creatorId`, lo scope al ricettario corrente, pgvector con HNSW e `fly.toml` + CLI.

## Decision checkpoints

- **Dopo la slice 2:** qualità del ranking cross-lingua sul corpus → se insufficiente, cambiare embedder, anticipare la ricerca ibrida o rimettere in discussione il differenziatore prima di costruirne l'UI.
- **Dopo la slice 4:** comportamento su query vaghe con ricette reali → promuovere filtri strutturati o ricerca ibrida da `LATER`.
- **Dopo la slice 6:** hit-rate JSON-LD misurato sui siti realmente usati → se basso, aumentare priorità e budget del fallback LLM; se alto, ridimensionarlo.
- **Dopo la slice 7:** costo e accuratezza dell'estrazione LLM → confermare o sostituire il modello prima di estenderlo al copia-incolla.
- **Dopo la slice 13:** cold start e costo reali in produzione → promuovere la macchina sempre calda da `LATER`.

## Open questions

- Provider Postgres: `arch-choices.md` lascia aperta la scelta tra Neon e Supabase; la decisione va presa prima della slice 1 perché determina provisioning, driver e limiti del free tier.
- Modello di embedding: `arch-choices.md` cita `text-embedding-3-small` come esempio ma impone il vincolo multilingue; se la slice 2 mostrasse un ranking cross-lingua debole occorre un embedder multilingue dedicato, con impatto su costo e dimensione del vettore.
