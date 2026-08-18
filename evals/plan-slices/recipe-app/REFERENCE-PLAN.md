# Recipe App — Reference plan

- **Sources:** `sources/goal.md`, `sources/concepts.md`, `sources/arch-choices.md`, `sources/tech-choices.md`.
- **Current state:** Greenfield, nessun repository né infrastruttura esistente. Stack chiuso (TypeScript, Next.js App Router, Effect, Drizzle, Auth.js + Google OAuth, React Query); infrastruttura decisa nella forma (Postgres + pgvector, object storage R2, Fly.io con scale-to-zero `suspend`) ma con provider e modelli non ancora selezionati (vedi `Open questions`).

## Ordering criteria

- Prima il percorso di consegna minimo, poi le convenzioni di dominio e UI su comportamento reale ma minuscolo, poi il rischio esistenziale.
- Lo skeleton prova che l'infrastruttura già decisa è connessa e gira; gli adapter usati da una sola slice restano in quella slice.
- Il differenziatore è la ricerca semantica cross-lingua: va validato prima di qualunque slice di acquisizione, perché senza di esso il prodotto è una riscrittura di Mealie.
- Slice iniziali minuscole finché le convenzioni di delivery, dominio, test e UI richiedono revisione umana frequente; più grandi dopo, solo perché i pattern esistono già nella codebase.
- Confine di scope dalla prima slice che persiste dati, con un resolver unico dello scope corrente; ogni slice precedente all'identità dichiara un'audience di sviluppatore o tester sull'ambiente non pubblico.
- Import automatico dal caso più frequente ai fallback, senza aprire adapter nuovi finché il tema non è chiuso.

## Themes

Un tema è una promessa di prodotto che si può rinviare o cancellare per intero, da sola.
L'ordine qui sotto è per importanza — prima i differenzianti; l'ordine di costruzione lo danno
i numeri in `First validation`.

| Theme             | Desired outcome                                                                               | First validation                       |
| ----------------- | --------------------------------------------------------------------------------------------- | -------------------------------------- |
| Ricerca semantica | Descrivo un piatto a parole mie e trovo la ricetta giusta anche se scritta in un'altra lingua | 4. Ricerca semantica cross-lingua      |
| Import automatico | Aggiungere una ricetta trovata online costa un incollaggio, senza riscriverla a mano          | 8. Import da URL con JSON-LD           |
| Consultazione     | Vedo il contenuto del ricettario corrente e apro una ricetta per cucinarla                    | 5. Lettura della ricetta               |
| Scrittura manuale | Salvo e correggo una ricetta a mano, senza passi obbligatori                                  | 7. Inserimento manuale e modifica      |
| Foto              | Ogni ricetta è riconoscibile a colpo d'occhio senza lavoro manuale                            | 11. Foto della ricetta                 |
| Autenticazione    | Entro con il mio account Google e vedo solo il mio ricettario                                 | 6. Accesso Google e ricettario privato |
| Condivisione      | Famiglia e amici contribuiscono allo stesso ricettario da pari                                | 12. Invito e collaborazione paritaria  |

## Cross-functional concerns

- **Authorization:** Un resolver unico possiede il ricettario corrente; ogni lettura e scrittura è filtrata su di esso e un id fuori scope risponde 404. La slice 6 è il seam in cui lo scope configurato viene sostituito dalla membership autenticata. Nessun permesso granulare: essere membro significa leggere ed editare tutto, unico ruolo è `Cookbook.creatorId`.
- **Validation and errors:** Ogni input non fidato — HTML remoto, JSON-LD, output LLM, payload di form — è decodificato con `Schema` e mai asserito; una decodifica fallita non produce salvataggi parziali; gli errori applicativi sono `Data.TaggedError` gestiti con `catchTag` ai boundary.
- **Operability:** Timeout e retry espliciti su fetch pagina, embedding e LLM; log strutturato per passo con esito, durata, token e costo; il progresso mostrato all'utente riflette i passi realmente eseguiti e nomina il passo fallito.
- **Accessibility and security:** URL forniti dall'utente protetti da SSRF con host e schemi consentiti; upload limitati per tipo e dimensione; segreti solo a runtime; token di invito ad alta entropia; flussi percorribili da tastiera, stato e progresso annunciati, campi facoltativi marcati `(optional)` e nessun asterisco sugli obbligatori.
- **Data integrity and recovery:** `embedding` è indice derivato e non dato canonico, rigenerato a ogni salvataggio indicizzato; una sola cover per ricetta; duplicati consentiti deliberatamente; un fallimento su embedding o foto non fa perdere la ricetta.
- **Cost:** Ogni slice resta nel free tier; LLM ed embedding delle ricette operano solo in add o edit; il costo dell'embedding della query resta subordinato alla decisione aperta.

## NOW

### 0. Repository e CI *(Enabler: delivery)*

---

**Includes**

- App Next.js App Router in TypeScript, con lint, formattazione, typecheck e test runner configurati.
- Pipeline CI che esegue build, lint, typecheck e test a ogni push.
- Esempi minimi delle convenzioni: servizio Effect con `Context.Tag` e `Layer`, errore `Data.TaggedError`, test co-locato.
- Nessun provisioning, nessun deploy, nessuna entità di dominio.

**Verification**

- CI verde su un PR di prova, con build, lint, typecheck e test tutti eseguiti.
- Un errore di tipo e un test rotto introdotti ad arte fanno fallire la pipeline.

**Outcome**

- Ogni push produce un verdetto automatico su cui ogni slice successiva è revisionabile e revertibile.

### 1. Walking skeleton in ambiente dev *(Enabler: delivery)*

---

**Includes**

- Immagine Docker dell'app e deploy da CI/CD su Fly.io via `fly.toml`, con `auto_stop` in modalità `suspend`.
- Migration runner con una migrazione non di dominio applicata al Postgres del provider selezionato (decisione aperta).
- Estensione pgvector abilitata da migrazione, senza alcuna entità di dominio.
- Route diagnostica che raggiunge il database a runtime attraverso il driver reale su TCP.
- Nessuna entità di dominio, nessuna autenticazione, nessuna tenancy, nessun object storage, nessuna promozione in produzione.

**Verification**

- Un commit costruisce l'immagine e la distribuisce sull'ambiente non pubblico senza intervento manuale.
- La route diagnostica risponde con il risultato di una query reale, dopo deploy e dopo risveglio da `suspend`.
- La migrazione risulta applicata e la connessione regge il primo accesso dopo scale-to-zero.
- Cold start e riconnessione al database misurati e registrati come baseline.

**Learning / risk**

- Driver, modalità di connessione e pooling attraverso lo scale-to-zero sono la prima incognita infrastrutturale: scoprirli dentro una slice di dominio confonderebbe un fallimento di connessione con uno di dominio.

**Outcome**

- Uno sviluppatore verifica che runtime, database e pipeline di migrazione siano connessi e funzionanti nell'app deployata.

### 2. Contesto del ricettario corrente *(Enabler: domain conventions)*

---

**Includes**

- Entità `Cookbook` con `name` e `visibility`, e migrazione Drizzle.
- Resolver unico del ricettario corrente, per ora da configurazione, attraversato da ogni lettura e scrittura.
- Shell dell'app che mostra il ricettario corrente e il suo contenuto vuoto.
- Input controllato che crea il ricettario attraverso il percorso di produzione, non con SQL diretto.
- Nessuna ricetta, nessuna ricerca, nessuna identità, nessuna creazione da UI.

**Verification**

- Il ricettario creato dall'input controllato persiste e la shell lo legge attraverso il resolver.
- Un id di ricettario fuori dallo scope corrente risponde 404.
- I dati sopravvivono a un redeploy.

**Outcome**

- Uno sviluppatore crea il ricettario configurato tramite il percorso di produzione e ne apre la shell vuota.

### 3. Pipeline di indicizzazione su fixture *(Enabler: ricerca semantica)*

---

**Includes**

- Entità `Recipe` con nome, ingredienti e preparazione come testo libero, più `tags` e `prepTime` opzionali.
- Colonna `embedding` pgvector e indice HNSW.
- Seed di ricette fixture italiane e inglesi che attraversa validazione, embedding via API cloud e persistenza, senza vettori precalcolati.
- Comando diagnostico che ranka le ricette persistite per una frase in linguaggio naturale, stampando score, latenza e costo.
- Nessuna UI, nessuna acquisizione da fonti esterne.

**Verification**

- Una frase in linguaggio naturale restituisce top-k con score, scoped al ricettario corrente.
- Il ranking proviene da embedding generati dalla pipeline reale, verificabile ricostruendo l'indice da zero.
- Costo in token dell'indicizzazione dell'intero corpus e latenza di ranking misurati contro il target.

**Learning / risk**

- La ricerca semantica cross-lingua è il differenziatore dichiarato: se il recall non regge, il prodotto ricade su alternative già mature e la scelta del modello va rifatta prima di costruirvi sopra.

**Outcome**

- Uno sviluppatore carica ricette fixture multilingue e ottiene da riga di comando un ranking per similarità prodotto dalla pipeline reale.

**Precondizione**

- La contraddizione sull'embedding della query va risolta prima di implementare e verificare il ranking.

### 4. Ricerca semantica cross-lingua *(Theme: Ricerca semantica)*

---

**Includes**

- Campo di ricerca e pagina risultati basati sulla similarità, scoped al ricettario corrente.
- Path di embedding della query conforme alla decisione aperta, con timeout e messaggio esplicito se quella modalità dipende da un servizio esterno indisponibile.
- Testo indicizzato pari a nome + ingredienti + preparazione, più tag e tempo quando presenti.
- Nessun filtro strutturato, nessuna ricerca ibrida, nessun dettaglio ricetta.

**Verification**

- Da browser, `pomodoro` e `cena leggera` trovano fixture scritte in inglese.
- Le ricette di un altro ricettario non compaiono mai tra i risultati.
- Nessuna chiamata LLM compare nei log di ricerca.
- Latenza percepita misurata sul path effettivamente scelto, cold start incluso.

**Outcome**

- Chi testa l'app descrive un piatto a parole proprie e ottiene le ricette pertinenti del ricettario configurato, anche se scritte in un'altra lingua.

### 5. Lettura della ricetta *(Theme: Consultazione)*

---

**Includes**

- Elenco delle ricette del ricettario corrente.
- Pagina di dettaglio con ingredienti e preparazione resi come testo a righe.
- Collegamento dal risultato di ricerca al dettaglio corrispondente.
- Nessuna modifica, nessuna foto.

**Verification**

- Un risultato di ricerca apre il dettaglio corrispondente.
- Ricette prive di tag e tempo si elencano e si aprono senza degradare la vista.
- L'id di una ricetta di un altro ricettario risponde 404.

**Outcome**

- Chi testa l'app vede l'elenco delle ricette del ricettario configurato e ne apre una per cucinarla.

### 6. Accesso Google e ricettario privato *(Theme: Autenticazione)*

---

**Includes**

- Auth.js (NextAuth v5) con provider Google OAuth e sessione persistita su Postgres.
- Entità `Membership` N:N e sostituzione, nell'unico resolver dello scope, del ricettario configurato con quelli dell'utente autenticato.
- Creazione idempotente del ricettario personale al primo accesso, con `creatorId` valorizzato.
- Tutte le rotte di prodotto richiedono una sessione valida.
- Nessun invito, nessun ruolo, nessun ricettario multiplo, nessuna creazione esplicita di altri ricettari.

**Verification**

- L'utente A non vede né cerca le ricette di B.
- L'accesso anonimo alle rotte di prodotto reindirizza al login.
- Un secondo accesso dello stesso utente non crea un secondo ricettario.

**Outcome**

- Al primo accesso un utente crea automaticamente il proprio ricettario privato e lo vede al posto dello scope configurato.

### 7. Inserimento manuale e modifica *(Theme: Scrittura manuale)*

---

**Includes**

- Un solo form per inserimento manuale, a campi vuoti, e per la modifica di qualsiasi ricetta del ricettario.
- Nome, ingredienti e preparazione come testo libero, senza parsing di quantità e unità.
- Tag e tempo modificabili e mai obbligatori.
- Rigenerazione dell'embedding a ogni salvataggio.
- Nessuna foto, nessuna review obbligatoria prima del salvataggio.

**Verification**

- La stessa form appare vuota in creazione e precompilata in modifica.
- Il salvataggio non richiede campi oltre al nome.
- Una ricetta creata a mano è trovabile con una query che non ne ripete le parole.
- Una modifica cambia il ranking, a conferma della reindicizzazione.

**Outcome**

- Un membro salva una ricetta che conosce e corregge in seguito qualsiasi ricetta del ricettario.

### 8. Import da URL con JSON-LD *(Theme: Import automatico)*

---

**Includes**

- Form "aggiungi da link", fetch reale della pagina e parse del JSON-LD `schema.org/Recipe`.
- Progress sincrono sui passi realmente eseguiti, con messaggio preciso sul passo fallito.
- Salvataggio immediato senza review, con `sourceUrl` valorizzato e tag e tempo derivati best-effort.
- Nessuna chiamata LLM, nessuna foto, nessun testo incollato.

**Verification**

- Un URL con JSON-LD produce una ricetta salvata con `sourceUrl` valorizzato e zero chiamate LLM.
- Paywall e JSON-LD assente producono un messaggio specifico sul passo fallito e nessuna ricetta creata.
- Hit-rate del JSON-LD sul campione reale di siti registrato.

**Learning / risk**

- L'hit-rate reale del JSON-LD sui siti effettivamente usati determina quanto peserà il fallback a pagamento.

**Outcome**

- Un membro incolla l'URL di un food blog e ottiene la ricetta salvata senza review.

### 9. Fallback LLM per URL non strutturati *(Theme: Import automatico)*

---

**Includes**

- Estrattore LLM con output strutturato validato da `Schema`, innestato nel passo `Leggo ricetta` esistente quando il JSON-LD manca.
- Metriche per estrazione che distinguono parse diretto e fallback pagato, con modello, costo, latenza ed esito.
- Nessun nuovo flusso di add: l'estrattore ha un unico proprietario.

**Verification**

- Su un campione annotato la ricetta salvata contiene ingredienti e preparazione corretti.
- Un output non conforme allo schema non produce salvataggi parziali.
- Costo medio per estrazione misurato e confrontato con la soglia dichiarata.

**Learning / risk**

- L'accuratezza di un modello cheap a frazioni di cent per ricetta decide se il fallback resta automatico o va ristretto ai casi espliciti.

**Outcome**

- Anche le pagine senza dati strutturati producono una ricetta salvata, senza intervento dell'utente.

### 10. Import da testo incollato *(Theme: Import automatico)*

---

**Includes**

- Ingresso "incolla testo" che, dopo pulizia del contenuto, riusa motore e schema di output della slice 9.
- Limite di dimensione del testo incollato e progresso ridotto ai passi realmente eseguiti.
- Nessun OCR, nessun import da file.

**Verification**

- Il testo di una pagina con paywall produce una ricetta salvata e trovabile, senza alcuna chiamata HTTP verso la fonte.
- Un testo che non è una ricetta produce un errore preciso senza salvataggio.

**Outcome**

- Quando il link non è leggibile, un membro incolla il testo della pagina e ottiene la stessa ricetta salvata.

### 11. Foto della ricetta *(Theme: Foto)*

---

**Includes**

- Bucket Cloudflare R2 e upload multiplo dal form condiviso, con il solo `url` persistito in Postgres.
- Download dell'immagine da `schema.org/Recipe` o `og:image` e ricarica sullo storage proprio, in tutti i path di import.
- Passo "salvo foto" aggiunto al progress, con la prima foto come cover.
- Nessuna scelta manuale della cover, nessuna selezione delle foto durante l'import.

**Verification**

- L'immagine della pagina è servita dallo storage proprio, mai in hotlink.
- L'upload manuale accetta più foto e la prima risulta cover.
- Un file oltre limite o un download fallito non blocca il salvataggio della ricetta.
- Le foto restano servibili dopo un redeploy.

**Outcome**

- Le ricette importate arrivano già con la foto e un membro può aggiungerne altre a mano.

### 12. Invito e collaborazione paritaria *(Theme: Condivisione)*

---

**Includes**

- `Invitation` con token condivisibile come link o codice e scadenza opzionale; l'adesione da loggato crea una `Membership`.
- Elenco dei propri ricettari e selezione di quello corrente, risolto dal resolver unico.
- Membri pari: ogni membro legge ed edita tutte le ricette del ricettario.
- Nessun ruolo, nessun permesso granulare, nessuna creazione di ricettari aggiuntivi dall'interfaccia.

**Verification**

- B accetta l'invito di A, legge e modifica le ricette di A, e A vede le modifiche.
- L'accettazione è idempotente per lo stesso membro.
- Un token scaduto o revocato non crea `Membership`.
- Con più ricettari, elenco e ricerca seguono quello selezionato.

**Outcome**

- Il creator condivide un link e chi lo apre entra nel ricettario come membro pari.

### 13. Rilascio agli utenti pilota *(Release: delivery)*

---

**Includes**

- Ambiente di produzione su Fly con dominio, segreti (OAuth, embedding, LLM, storage) e callback Google configurati.
- Tetto di spesa e allarme su LLM ed embedding.
- Nessuna nuova capability di prodotto.

**Verification**

- Due utenti reali completano in produzione import, ricerca, modifica e condivisione.
- Costo del primo mese misurato contro il target di centesimi.

**Outcome**

- Famiglia e amici usano l'app in produzione, entro il budget dichiarato.

## LATER

- **Scelta manuale della cover** — se gli utenti pilota segnalano la prima foto come rappresentazione sbagliata; rifinitura di un default già spedito.
- **Scelta di quali foto tenere durante l'import** — se gli import portano immagini irrilevanti in modo sistematico; qualità della galleria senza reintrodurre una review obbligatoria.
- **Filtri strutturati (tag, tempo) e ricerca ibrida semantica + full-text** — se query reali tipo "senza glutine" o "meno di 30 minuti" sbagliano sistematicamente; `tags` e `prepTime` sono già popolati, quindi attivabili senza migrazione.
- **Ricerca cross-ricettario** — se utenti con più ricettari cercano ripetutamente nello scope sbagliato; elimina il cambio di contesto manuale.
- **Creazione di ricettari aggiuntivi dall'interfaccia** — se un gruppo chiede di separare i contenuti oltre al ricettario creato al primo accesso; il modello N:N esiste già.
- **Ricettari pubblici tematici** — se arriva la richiesta di condividere fuori dal gruppo invitato; `visibility=public` è già modellato.
- **Concetto di gruppo sopra i ricettari** — se ri-invitare gli stessi membri a ogni nuovo ricettario diventa attrito segnalato; additivo sopra `Membership`.
- **Macchina Fly sempre calda** — se il cold start risulta fastidioso agli utenti pilota; un flag reversibile in `fly.toml` al costo noto di ~$3/mese.
- **Passkeys** — se la dipendenza da Google limita l'adozione e il recupero account in Auth.js matura; accesso senza password senza introdurre un provider email.

## OUT-OF-SCOPE

- **Ingredienti strutturati (quantità e unità)** — trade-off accettato in `goal.md`: la ricerca è semantica e chi legge interpreta il testo.
- **Lista della spesa e scaling delle porzioni** — dipendono dagli ingredienti strutturati.
- **Review obbligatoria prima del salvataggio** — bloccare l'utente a ogni aggiunta è il costo che il prodotto elimina; la correzione resta disponibile come edit.
- **Deduplica delle ricette** — duplicati consentiti per scelta esplicita in `concepts.md`.
- **Ruoli e permessi granulari** — nell'MVP basta `creatorId` e tutti i membri sono pari.
- **Email + password e magic link** — richiedono comunque un provider email.
- **Vector DB dedicato** — a ≤10k ricette pgvector con HNSW è già istantaneo.
- **IaC versionata (SST, Terraform)** e **hosting su Vercel o Cloudflare Workers** — scartati in `arch-choices.md` per costo e complessità.

## Decision checkpoints

- **Dopo la 4:** qualità del ranking cross-lingua, latenza e costo → cambiare modello di embedding, oppure rimettere in discussione la proposta di valore.
- **Dopo la 8:** hit-rate del JSON-LD sui siti realmente usati → restringere o anticipare il fallback LLM.
- **Dopo la 9:** costo medio per estrazione → cambiare modello o limitare il fallback ai casi espliciti.
- **Dopo la 13:** cold start e costo misurati sugli utenti pilota → promuovere la macchina sempre calda o restare su scale-to-zero.

## Open questions

- **Embedding della query a runtime:** `goal.md:110` e `arch-choices.md:33` lo vietano, mentre `concepts.md:153` richiede `embedding(query)`; blocca implementazione e verifica delle slice 3 e 4.
- **Provider Postgres:** Neon o Supabase; blocca lo skeleton della slice 1, perché determina driver, modalità di connessione e limiti del free tier.
- **Modello di embedding:** deve essere multilingue; blocca la pipeline della slice 3.
- **Modello LLM:** deve supportare output strutturato entro il budget; blocca il fallback della slice 9.
