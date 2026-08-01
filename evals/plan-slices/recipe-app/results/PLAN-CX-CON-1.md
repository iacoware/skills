# Recipe App — Piano di delivery ad alto livello

## Obiettivo e criteri

Consegnare l'MVP come sequenza di slice verticali, ciascuna deployabile e verificabile da
un utente. La ricerca semantica cross-lingua resta il differenziatore e viene introdotta
appena esistono ricette importabili, non come rifinitura finale.

Assunzioni:

- repository greenfield: al momento contiene solo la documentazione;
- un solo deploy Next.js e un solo Postgres; nessun microservizio;
- confini applicativi coesi per identità/accesso, ricettari, ricette, acquisizione,
  ricerca e media;
- provider esterni dietro porte Effect e adapter separati, perché sono le dipendenze più
  distanti e sostituibili;
- ogni slice include autorizzazione, validazione, errori tipizzati, logging e
  osservabilità minimi reali richiesti dal comportamento;
- niente funzionalità fuori MVP: ricettari pubblici, ruoli granulari, gruppi, filtri,
  ricerca ibrida e ricerca cross-ricettario.

## Prerequisito — Setup del repository

Preparare solo la fondazione necessaria alla walking skeleton:

- Next.js App Router, TypeScript, Effect 3, Drizzle e Postgres;
- configurazione validata per ambiente e segreti;
- migrazioni DB e database isolato per i test;
- Vitest, controlli di formato, lint, typecheck e build;
- CI su ogni modifica;
- container Docker, `fly.toml` con suspend/scale-to-zero e pipeline di deploy;
- struttura iniziale per test di integrazione ed end-to-end.

Esito verificabile: applicazione vuota compilata, testata e raggiungibile su un ambiente
Fly rappresentativo tramite pipeline ripetibile.

## Slice 1 — Walking skeleton: dal login alla prima ricetta

Un utente accede con Google, crea un ricettario privato, aggiunge manualmente una ricetta
tramite il form canonico e la vede nella home del ricettario corrente.

Include:

- Auth.js con Google OAuth e persistenza dell'identità;
- creazione e selezione del ricettario;
- membership automatica del creator;
- modello normalizzato minimo di ricetta;
- form condivisibile di review/edit, inizialmente vuoto per l'inserimento manuale;
- salvataggio e lista server-side delle ricette;
- controllo membership su ogni lettura e scrittura.

Verifica: percorso end-to-end sul deploy; un non membro non può leggere o modificare dati
del ricettario; errori di validazione e persistenza sono comprensibili e osservabili.

## Slice 2 — Import da URL con JSON-LD

Un membro incolla un URL supportato, vede avanzare i passi realmente completati, rivede
la ricetta estratta e la salva nello stesso elenco della slice precedente.

Include:

- download server-side con timeout e limiti;
- estrazione e validazione di `schema.org/Recipe`;
- normalizzazione nello stesso modello e nello stesso form della modalità manuale;
- progress reale dalla lettura della pagina alla preparazione della review e al
  salvataggio;
- acquisizione su object storage della foto sorgente scelta come cover, senza hotlink;
- messaggi specifici per URL non valido, pagina irraggiungibile, contenuto non
  riconosciuto e foto non salvabile.

Verifica: import end-to-end da fixture HTTP realistica e smoke test con una pagina
controllata; nessuna chiamata LLM quando il JSON-LD è valido.

## Slice 3 — Ricerca semantica cross-lingua

Un membro cerca nel ricettario corrente con parole in una lingua diversa da quella della
ricetta e ottiene risultati ordinati per similarità.

Include:

- testo canonico indicizzato da nome, tag, ingredienti, preparazione e tempo;
- generazione e persistenza dell'embedding su creazione;
- backfill delle ricette già esistenti;
- embedding della query e confronto pgvector, sempre vincolato al `cookbookId`;
- indice HNSW e gestione esplicita di ricette prive di embedding;
- rigenerazione predisposta per le future modifiche della ricetta.

Verifica: test deterministici di ordinamento e isolamento tra ricettari con adapter fake;
test di integrazione pgvector; smoke test reale multilingue con il provider scelto.

## Slice 4 — Inviti e più ricettari

Il creator genera un link/codice; un utente autenticato lo usa per entrare nel ricettario,
lo seleziona e può leggere e modificare le stesse ricette degli altri membri.

Include:

- token di invito non prevedibile e memorizzazione sicura;
- creazione invito riservata al creator;
- adesione idempotente e creazione della membership;
- elenco e cambio del ricettario corrente;
- parità dei membri sulle operazioni delle ricette;
- scope del ricettario preservato in lista, import e ricerca.

Verifica: percorso end-to-end creator → invitato; riapertura del link senza membership
duplicate; impossibilità di usare un token invalido o accedere a un altro ricettario.

## Slice 5 — Fallback LLM e copia-incolla

Un URL senza JSON-LD passa al fallback LLM; in alternativa l'utente incolla il testo
della pagina. Entrambi producono la stessa review correggibile e lo stesso salvataggio.

Include:

- pulizia del contenuto prima dell'invio;
- output strutturato LLM decodificato con Schema, mai assunto valido;
- fallback automatico solo dopo l'assenza di JSON-LD;
- copia-incolla diretto allo stesso motore di estrazione;
- progress reale differenziato per URL e testo;
- limiti di dimensione, timeout, errori provider e controllo dei costi osservabili.

Verifica: fixture senza JSON-LD, testo incollato e output LLM malformato; conferma che
entrambi i percorsi convergano sul medesimo modello e form senza salvare dati non rivisti.

## Slice 6 — Modifica completa e foto multiple

Un membro modifica una ricetta salvata, aggiunge più foto e sceglie una sola cover. La
ricerca riflette i contenuti aggiornati.

Include:

- riuso del form canonico per modifica post-salvataggio;
- rigenerazione dell'embedding dopo ogni modifica indicizzabile;
- upload e import di più foto su R2;
- selezione atomica di una sola cover;
- coerenza tra DB e object storage in caso di fallimento parziale;
- concorrenza gestita senza perdere silenziosamente modifiche o cover.

Verifica: modifica end-to-end immediatamente ricercabile; test dell'invariante della cover;
fallimenti simulati di embedding e storage senza stato canonico incoerente.

## Slice 7 — Varianti critiche e rilascio MVP

Completare i casi di rischio emersi dai percorsi già funzionanti, senza ampliare lo scope.

Include:

- protezioni SSRF, redirect e content type per il fetch degli URL;
- retry solo per errori transitori e timeout espliciti dei provider;
- accessibilità e uso mobile di form, progress, errori e selettore ricettario;
- telemetria di latenza, fallimenti e costo per import, embedding e storage, senza
  registrare contenuti sensibili;
- test end-to-end dei tre ingressi, ricerca cross-lingua, invito e isolamento tenant;
- verifica di migrazioni, backup/ripristino, cold start e deploy/rollback;
- budget e smoke test post-deploy come gate di rilascio.

Esito verificabile: checklist MVP soddisfatta nell'ambiente rappresentativo e percorso
completo osservabile dal login alla condivisione e ricerca della ricetta.

## Ordine e dipendenze

Le slice 1–4 introducono breadth-first un comportamento core per gestione ricette,
acquisizione, scoperta e collaborazione. Le slice 5–7 approfondiscono varianti e rischi.

Ordine previsto:

`Setup → 1 → 2 → 3 → 4 → 5 → 6 → 7`

Le slice 3 e 4 possono avanzare in parallelo dopo la 2 solo se migrazioni e contratti
della ricetta sono stabilizzati. La 5 riusa il contratto di acquisizione della 2; la 6
riusa form e indicizzazione delle slice 1 e 3.

## Open questions

- I documenti richiedono `embedding(query)` per la ricerca, ma dichiarano anche che gli
  embeddings non devono essere chiamati a runtime sulle query. La ricerca semantica
  libera richiede quella chiamata oppure un embedder locale: va scelta una delle due
  opzioni prima della slice 3.
- Va scelto Neon o Supabase prima di fissare provisioning, driver e pipeline delle
  migrazioni.
- Vanno fissati provider, modello e dimensione vettoriale per embeddings, oltre a
  provider/modello LLM per l'estrazione, prima delle rispettive migrazioni e degli adapter.
- Va definito il ciclo di vita degli inviti MVP: riutilizzabili o monouso, con o senza
  scadenza e revoca.
