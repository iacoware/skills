# Recipe App — Piano MVP per slice

## Obiettivo

Consegnare un ricettario condiviso che permetta di acquisire ricette da più sorgenti,
correggerle, organizzarne le foto e ritrovarle con ricerca semantica multilingue.

Il differenziatore da proteggere è la combinazione tra:

- ricerca semantica cross-lingua;
- acquisizione resiliente: JSON-LD quando disponibile, LLM e copia-incolla come fallback.

## Assunzioni e confini

- Un solo deploy Next.js/Node e un solo datastore Postgres con pgvector.
- Ogni accesso a ricette, foto, inviti e ricerca è autorizzato e filtrato per ricettario.
- Tutti i membri di un ricettario possono leggere e modificare tutto; solo il creator genera
  inviti.
- Duplicati consentiti.
- Estrazione sincrona; nessuna coda o worker nell'MVP.
- Ricettari privati, ricerca nel solo ricettario corrente, nessun ruolo granulare.
- Filtri strutturati, ricerca ibrida, ricettari pubblici e gruppi restano fuori scope.

## Impostazione architetturale

Partire con un monolite modulare: i flussi di catalogo, acquisizione e ricerca condividono
molto modello e cambieranno insieme, quindi tenerli vicini riduce il costo di coordinamento.
Mantenere invece contratti espliciti verso Google OAuth, Postgres, object storage, fetch HTTP,
LLM ed embeddings: sono dipendenze esterne e sostituibili.

Le porte applicative sono `Context.Tag`; gli adapter sono `Layer` separati. Input esterni,
JSON-LD, output LLM e risposte HTTP sono decodificati con Schema. Gli errori attesi sono valori
taggati e diventano messaggi utente solo ai boundary.

## Ordine delle slice

### Slice 0 — Walking skeleton autenticato

**Risultato utente:** l'utente apre l'app, accede con Google, vede una home protetta e può
disconnettersi.

**Include:**

- shell Next.js e deploy containerizzato su Fly.io con scale-to-zero;
- Google OAuth tramite Auth.js e persistenza `User`/sessione su Postgres;
- configurazione, migrazioni, health check e gestione degli errori di avvio;
- primo percorso end-to-end browser → applicazione → database.

**Verifica:** login, persistenza della sessione, logout, rifiuto dell'accesso anonimo e smoke
test sull'ambiente distribuito.

### Slice 1 — Primo ricettario e contesto corrente

**Risultato utente:** al primo accesso l'utente crea un ricettario, lo seleziona e ne vede la
home vuota.

**Include:**

- `Cookbook` e `Membership`, con il creator membro dalla stessa transazione;
- creazione, elenco e selezione del ricettario corrente;
- guardia applicativa riusabile che verifica membership e `cookbookId`;
- empty state con azioni di aggiunta ricetta.

**Verifica:** creazione atomica, accesso del membro, isolamento da ricettari non autorizzati e
persistenza della selezione corrente.

### Slice 2 — Ricetta manuale: crea, consulta e correggi

**Risultato utente:** l'utente inserisce una ricetta a mano, la rivede nello stesso form
destinato alle importazioni, la salva, la vede nell'elenco e la modifica.

**Include:**

- modello normalizzato `Recipe`;
- form condiviso di review/edit con nome, ingredienti, preparazione, tempo, tag e URL sorgente
  opzionale;
- validazione, salvataggio, elenco, dettaglio e modifica;
- autorizzazione sempre derivata dalla membership, mai dal solo ID ricetta.

**Verifica:** ciclo create/read/update, campi opzionali, errori di validazione, ricettario vuoto
e tentativi di lettura/modifica cross-ricettario.

### Slice 3 — Inviti e collaborazione multi-ricettario

**Risultato utente:** il creator condivide un invito; un altro utente lo accetta, seleziona il
nuovo ricettario e può leggere e modificare le sue ricette.

**Include:**

- creazione e revoca/scadenza degli inviti condivisibili;
- accettazione dopo login e creazione idempotente della membership;
- selettore tra più ricettari;
- stessi poteri di lettura e modifica per tutti i membri;
- generazione inviti riservata al creator.

**Verifica:** invito valido, scaduto/revocato, riutilizzo controllato, doppia accettazione,
utente non membro e isolamento completo tra ricettari.

### Slice 4 — Foto multiple e cover

**Risultato utente:** durante creazione o modifica l'utente carica più foto e sceglie una sola
cover, poi la vede in elenco e nel dettaglio.

**Include:**

- `Photo` e invariante di una sola cover per ricetta;
- upload su Cloudflare R2 e persistenza dei soli riferimenti nel DB;
- aggiunta, rimozione e cambio cover;
- gestione compensativa di upload falliti e oggetti orfani.

**Verifica:** tipi/dimensioni non validi, upload parziale, cambio cover atomico, eliminazione
della cover e accesso cross-ricettario.

### Slice 5 — Importazione URL con JSON-LD

**Risultato utente:** l'utente incolla un URL compatibile, segue l'avanzamento reale, corregge
la ricetta estratta e la salva con le foto importate.

**Include:**

- fetch server-side con timeout e limiti di dimensione;
- lettura e validazione di `schema.org/Recipe`;
- normalizzazione nello stesso modello e form della slice manuale;
- progress basato sugli stati reali del flusso, non su timer;
- download e re-upload delle immagini sorgente su R2 dopo conferma;
- errori precisi per URL invalido, rete, contenuto non leggibile e dati non validi.

**Verifica:** import riuscito senza chiamata LLM, correzione prima del salvataggio, errori per
ogni fase e assenza di ricette/foto parziali.

### Slice 6 — Fallback LLM e copia-incolla

**Risultato utente:** se una pagina non contiene JSON-LD il sistema prova l'estrazione LLM; per
paywall o siti non leggibili l'utente incolla il testo e ottiene la stessa review.

**Include:**

- pulizia del contenuto HTML o incollato;
- output strutturato LLM decodificato con lo stesso schema della ricetta;
- fallback automatico al LLM solo quando JSON-LD manca;
- ingresso copia-incolla diretto al LLM;
- proposta esplicita del copia-incolla quando il fetch non può leggere la pagina;
- limiti, timeout e distinzione tra errori di provider, output invalido e contenuto
  insufficiente.

**Verifica:** fallback attivato solo quando previsto, nessuna chiamata LLM sul percorso JSON-LD,
output invalido rifiutato e equivalenza del form di review tra i tre ingressi.

### Slice 7 — Ricerca semantica cross-lingua

**Risultato utente:** nel ricettario corrente l'utente cerca per significato; una query italiana
può trovare una ricetta inglese pertinente.

**Include:**

- testo indicizzato composto da nome, tag, ingredienti, preparazione e tempo;
- generazione e rigenerazione dell'embedding su create/edit;
- backfill delle ricette create prima della slice;
- embedding della query e ordinamento per similarità in Postgres/pgvector;
- filtro `cookbookId` applicato nella stessa query vettoriale;
- stato vuoto, errori del provider e soglia/limite risultati iniziali configurabili.

**Verifica:** casi cross-lingua fissati, ordinamento per pertinenza, aggiornamento dopo edit,
nessuna fuga tra ricettari e comportamento con indice mancante o provider indisponibile.

### Slice 8 — Chiusura MVP

**Risultato utente:** i percorsi principali sono affidabili nell'ambiente di produzione e gli
errori indicano come proseguire.

**Include:**

- test end-to-end dei percorsi login, manuale, URL JSON-LD, fallback, copia-incolla, foto,
  invito e ricerca;
- accessibilità dei form, avanzamento annunciato e convenzione chiara sui campi opzionali;
- osservabilità minima senza registrare token, contenuto ricette o dati OAuth sensibili;
- migrazioni e rollback verificati, backup/restore documentato;
- controllo dei costi e dei limiti per fetch, LLM, embedding e storage.

**Verifica:** suite automatica verde, smoke test post-deploy, scenari di failure provati e
checklist di rilascio completata.

## Dipendenze e parallelizzazione

Ordine minimo: `0 → 1 → 2`. Dopo la slice 2, inviti e foto possono avanzare separatamente.
L'import URL dipende dal form ricetta e dal supporto foto; il fallback LLM dipende
dall'import URL. La ricerca dipende dal modello ricetta, ma può essere sviluppata in parallelo
all'estrazione. La chiusura MVP segue tutte le slice funzionali.

## Criterio di completamento di ogni slice

Una slice è completa quando:

- il comportamento è utilizzabile dalla UI nell'ambiente distribuito;
- autorizzazione e isolamento per ricettario sono coperti;
- casi felici, errori attesi e confini esterni hanno test proporzionati al rischio;
- migrazione dati, configurazione e osservabilità necessarie sono incluse;
- non richiede dati preparati manualmente o una futura slice per funzionare come descritto.

## Rischi da sorvegliare

- SSRF e payload eccessivi nel fetch di URL esterni.
- Output LLM plausibile ma errato: la review umana resta obbligatoria.
- Coerenza tra DB e R2 in caso di fallimenti parziali.
- Cold start durante importazioni sincrone e timeout dei provider.
- Qualità cross-lingua e dimensione vettoriale legate al modello embedding scelto.
- Token di invito inoltrabili: devono essere non prevedibili, revocabili e non finire nei log.

## Open questions

- I documenti vietano embeddings a runtime sulle query, ma la ricerca semantica di testo libero
  richiede di generare l'embedding della query al momento della ricerca. Confermare che il
  vincolo intenda vietare l'LLM generativo sulle query, consentendo invece l'API di embedding.
- Un invito è monouso o riutilizzabile fino a revoca/scadenza? La scelta cambia modello,
  sicurezza e test della slice 3.
