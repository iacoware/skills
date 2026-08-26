# Review — ROADMAP-CC-4

Mappa: `.roadmap/` (12 righe, 5 temi, `archive/` vuoto). Sessione: headless, un solo prompt, 20
richieste, nessuna parola all'autore. `TRANSCRIPT.jsonl` presente e letto: le regole di sessione
sono giudicate sul transcript, non inferite dai file.

## Validator

`make validate-roadmap ROADMAP=…/ROADMAP-CC-4/.roadmap` → **`OK`**, nessun `ERROR`, nessun
`WARNING`. Il conteggio righe sta fra floor e cap (nessuna warning sui due bound).

Dal transcript (righe 92–100): la prima esecuzione dava 4 `ERROR` (`Depends on` con backtick e
`—` non risolvibili), corretti con un `perl -0pi` e ri-validati fino a `OK`.

## Violazioni

- **R-009** — `roadmap.md:18`, tema `ricettario`: la promessa dice «Scrivo a mano una ricetta …
  **con le sue foto**, e la ritrovo nell'elenco», il `First validator` è `S3`. Falsificata da `S3`
  stesso: `Excludes` → «Foto: sono di `S4`», e la `Verification` non nomina mai una foto. Il
  validatore copre metà promessa — esattamente la forma segnata `⚠ failed` sulla regola.
- **R-008** — `roadmap.md:24-33`: i verdetti sotto la tabella coprono 4 confini adiacenti più il
  merge di `import-testo`; il merge delle foto dentro `ricettario` non è mai argomentato. Falsificato
  dal test di split applicato a `S3`/`S4`: `S4` è cancellabile intera senza invalidare l'evidenza di
  `S3` (la `Verification` di `S3` sta in piedi da sola) — area di valore schedulabile
  indipendentemente, cioè theme compression. È la causa a monte di R-009.
- **R-015 / C1** — conflitto C1 (inserimento manuale vs motore di estrazione) risolto in silenzio.
  Preso in `S3` § Includes («un solo form … nessun parsing») e in `S3` § Excludes, senza una riga in
  `Assumptions`, senza una in `Open questions` e senza spike. Falsificato da
  `sources/arch-choices.md` § Estrazione contenuto, punto 3: «Copia-incolla / manuale: saltano il
  JSON-LD, riusano lo stesso motore e schema». La lettura presa è legittima (C1 ammette entrambe);
  è l'assenza della riga il difetto, ed è la forma già segnata `⚠ failed` sulla regola.
- **R-017 (dropped edge)** — `roadmap.md:50`, `S11` porta `Depends on —`. Falsificato dalla sua
  `Verification`: «Una persona non tecnica invitata entra dal dominio pubblico, aggiunge una ricetta
  da link e la ritrova cercandola a parole sue» — richiede `S10` (invito), `S5` (add da link) e `S8`
  (ricerca), e nessun input controllato può sostituirli in una riga che è la messa in mano a utenti
  veri. È il mirror costoso della regola: il riordino che si rompe senza che nessuno se ne accorga.
- **R-017 (published order)** — `roadmap.md:40` (`S1` → `S0`) e `:42` (`S3` → `S1`) pubblicano
  «dopo il repository» e «dopo lo scheletro». Falsificati da `drawing-the-map.md` § Hard
  dependencies: «What every row depends on is not published». Forma lieve (due archi, non quindici),
  ma sono i due che la regola nomina per esteso.
- **R-012** — `roadmap.md:43`, `S4` è la seconda riga di `ricettario` e sta in posizione 5, prima
  della prima riga di `ricerca` (`S8`), `accesso` (`S9`) e `condivisione` (`S10`). Nessuna delle
  quattro licenze è leggibile dalla riga: il `Learning target` di `S4` è l'upload verso R2 — non un
  altro differenziatore, non un rischio materiale della mappa, non un recupero dovuto, non un
  comportamento a frequenza materialmente più alta. (`S6` e `S7` sono invece licenziate: le fonti le
  dichiarano fallback del percorso da link, e «required recovery outranks breadth» impone proprio
  quell'ordine.)
- **R-012 (ranking)** — `S8`, la ricerca semantica, è nona. La mappa dichiara da sé che è
  esistenziale (`Open questions` → «se `S2` mostrasse che nessun modello … cade il differenziatore
  … la mappa va ridisegnata»), e ordina davanti quattro righe che quel ridisegno toccherebbe.
  Falsificato da `drawing-the-map.md` § Ordering for learning: il differenziatore e il rischio
  esistenziale stanno sopra «one thin outcome from each remaining theme», e «a seed corpus that lets
  the one uncertain promise be measured before four themes lean on it costs a line of `Includes` and
  buys the whole order» — corpus che la mappa ha già, dentro `S2`, e che usa solo per lo spike.
  A difesa: «a row that opens a pipeline shared by several paths follows every `NOW` row that feeds
  it» è una delle quattro cose non negoziabili, e `S8` apre la pipeline di embedding. Ma quel
  vincolo è conseguenza di una scelta di forma della candidata — indicizzazione e ricerca in una
  riga sola — non un dato: vedi la differenza con la reference più sotto.
- **H5** — `React Query` (`sources/tech-choices.md` § Data fetching client) non compare in nessuna
  riga né nei `Cross-functional concerns`; `grep -i "react.query\|tanstack"` su `.roadmap/` non dà
  nulla. Tutto il resto di H5 c'è (Google OAuth/Auth.js, Postgres+pgvector, R2, embedding cloud
  multilingue, Next.js su Fly, Effect, Drizzle). **Attenzione: nemmeno `reference-roadmap/` nomina
  React Query** (né Effect) — il sospetto è sulla voce H5, non sulla mappa; per la premessa di
  `EVALUATION-RULES.md` («se un check fallisce contro una clausola che l'artefatto non chiede più,
  il difetto è nel check») questa è da riscrivere o da restringere prima di contarla contro un run.
- **H7 (parziale) / R-011** — `S1` § Includes esercita driver TCP reale, runner di migrazioni,
  `CREATE EXTENSION vector` e scale-to-zero cronometrato, ma non nomina mai la modalità di
  connessione né il pooling. Falsificato dall'`Assumptions` line `S0, S1` della mappa stessa, che
  mette «i limiti di connessione» fra le condizioni che la rifiutano: la prova che la refuterebbe
  non ha nessuna osservazione in nessuna `Verification`. `drawing-the-map.md` § The two prerequisites
  dice che pooling e modalità di connessione non si validano più a buon mercato altrove. Gap minore
  e la reference qui è più debole della candidata.
- **R-022 (minore)** — `S11` è `needs-decision` e la sua `Open questions` dice che la risposta
  «decide se il tetto di spesa e l'avviso vadano accesi prima o possano aspettare»; il suo `Includes`
  li mette dentro entrambi senza condizione. Falsificato dal confronto fra le due sezioni della
  stessa riga: `Includes` decide ciò che `Open questions` dichiara non deciso.
- **R-035 (minore, discutibile)** — il messaggio di chiusura (transcript riga 103) apre con «Mappa
  scritta e validata (`OK`, nessun warning).» prima dei quattro pezzi. I quattro ci sono tutti e
  nell'ordine giusto; la regola dice «the four-part report and nothing else», e non c'era nessuna
  `WARNING` da riportare. Da leggere insieme a R-033, che chiede invece che si veda che il validator
  ha girato: due clausole che si sovrappongono, più che un errore del modello.

## Verde, con la prova

- **R-002** — `S0`…`S11` per incremento, nessun riuso; `archive/` vuoto, quindi high-water mark = 0.
- **R-010** — `theme: —` su `S0`, `S1`, `S11` (N5).
- **R-011** — repository e scheletro sono due righe; `S0` § Verification chiude con «Nessun deploy
  parte da questa riga», `S1` non porta entità di dominio, auth né tenancy.
- **R-013 / R-014** — il seam di scope viaggia con la prima riga che persiste (`S3`, risolutore
  unico), è dichiarato sotto `Cross-functional concerns` → Authorization, e `Assumptions`
  (`goal, S3, S9`) registra cosa le righe prima possono ignorare. Ogni riga prima di `S9` nomina la
  propria audience e nessun `Outcome` promette un utente che non può esistere.
- **R-015 (resto)** — C2 esce da una `Assumptions` line (`ricerca, S8`) che legge il divieto come
  vincolo di costo e cita la riga «le query sono irrilevanti»: è la lettura che il brief indica come
  non falsificata. U3 esce da `S2` + `Open questions`, U4 dal `Learning target` di `S5` (A9), U5
  dall'assunzione `import, S6`. Ogni riga di `Assumptions`/`Open questions` traccia a tema, id o
  `goal`, e ognuna porta la condizione che la rifiuta.
- **R-016** — l'unico `kind: enabler` è `S0`, che non risolve nessuna delle U1–U5.
- **R-019** — `S2`: `kind: spike`, `Audience` `—`, dipendente `S8`, nessun timebox.
- **R-021** — `S0` è la riga-prerequisito che `drawing-the-map.md` licenzia esplicitamente («the
  accounts and secrets the rest of the map spends»): aprire il client OAuth e le chiavi API lì non è
  fondazione speculativa.
- **R-023 / R-025** — nessuna delle sei forme nominate; `LATER` non contiene lavoro obbligatorio non
  finito (il ridimensionamento foto è convenienza mai chiesta dalle fonti, quindi candidato corretto).
- **R-024** — ogni produttore della pipeline di embedding ha il suo proprietario e `S8` la possiede
  da sola, con backfill delle ricette precedenti; `tags`/`prepTime` hanno proprietario esplicito
  (create in `S3`, popolate da `S5`/`S6`/`S7`).
- **R-026** — sette voci `OUT-OF-SCOPE`, tutte nella forma «perché … ; il prezzo è …». È la parte
  meglio scritta della mappa.
- **R-030** — 12 righe, validator senza warning sui due bound.
- **R-032** — transcript: nessun `.roadmap/` esistente (la project root è stata creata dalla
  sessione), mappa e dodici documenti scritti di seguito, nessuna conferma chiesta, nessun file
  scritto una domanda alla volta.
- **R-033** — validator lanciato dopo la scrittura (riga 92), quattro `ERROR` corretti, ri-eseguito
  fino a `OK` (riga 99–100), nessuna `WARNING` da girare all'autore.
- **H1** (`S8` in `NOW`), **H2** (risolutore in `S3`, query vincolata in `S8`, appartenenza in
  `S10`, membri pari), **H3** (`S5` JSON-LD → `S6` fallback validato; `S7` stesso schema; `S3` form
  condiviso), **H4** (salvataggio senza review, edit come recupero, embedding rigenerato in `S8`),
  **H6** (filtri, cross-ricettario, ricettari pubblici e gruppi in `LATER`; ruoli granulari in
  `OUT-OF-SCOPE`), **H8** (`S11` chiude su famiglia e amici, non su validazione da sviluppatore).
- **A1–A11** — nessuna licenziata come violazione: A5/N3 non si applicano (la candidata non consegna
  su seed), A6 esercitata (cover in `NOW`), A7 esercitata (nessun passo di scelta foto), A10
  esercitata (manuale ed edit una riga sola, verdetto scritto), A11 esercitata (identità dopo, con
  audience nominate).

## Inconclusive

- **R-001** — headless: nessun autore a cui chiedere. Lo stato è stato stabilito per costruzione (la
  sessione ha creato la project root) e `Current state` lo registra. La domanda dovuta in
  interattivo resta non messa alla prova da questo run, come `PROMPT.md` già dichiara.
- **R-003, R-004, R-005, R-006, R-007, R-018, R-027–R-031** — porta `Drawing`, prima mappa: non
  esercitate. Della metà di R-007 leggibile qui, nulla in rosso: nessuna riga ordinaria si tiene
  dentro una misura che avrebbe dovuto essere uno spike (`S1` è licenziata dallo scheletro, `S5`/`S6`
  da A9/U4).
- **R-034** — nessuna consegna richiesta né offerta nella sessione.
- **R-031** — vacua su `Drawing`; da notare che il check di copertura che quella porta possiede — la
  cerimonia dei temi e i first validator — è esattamente dove la mappa ha ceduto (R-009).

## Contro la reference

Non un diff: id, titoli, 7 temi contro 5 e 15 righe contro 12 non sono differenze da contare (N6, N4).

Dove la reference ha la ragione migliore:

- **Differenziatore per primo, su dati seed.** La reference spacca indicizzazione (`S3`, enabler) da
  ricerca (`S4`, product) e li mette prima di qualunque via d'ingresso; la candidata li fonde in `S8`
  e così si autoimpone il vincolo «la riga che apre la pipeline segue tutti i suoi alimentatori»,
  che la spinge in nona posizione. La ragione della reference è più forte perché è quella che il
  goal dichiara («il vero elemento distintivo … senza, staremmo riscrivendo Mealie») ed è quella che
  paga meno se `S2` va male.
- **Le foto come tema proprio** (`S11` reference) invece che dentro la promessa di `ricettario`: è
  la scelta che alla candidata costa R-008 e R-009.
- **C1 dichiarata.** La reference prende la stessa lettura della candidata — il form manuale non
  attraversa l'estrattore — ma la scrive in `Assumptions`. Stessa decisione, una riga di differenza,
  ed è quella riga la violazione.
- **Il provider Postgres sta su `S1` come `needs-decision`** (reference), non in `Assumptions` a
  quota mappa (candidata, riga 99–101, con `S1` `ready`). A1 e `REFERENCE-NOTES.md` sono espliciti:
  blocca una riga sola, quindi vive su quella riga. La candidata però ha *deciso* (Neon, con motivo e
  con condizione di rifiuto), e una decisione presa non blocca più niente: chiamata discutibile, non
  la conto fra le violazioni, ma la lettura della reference è la più pulita.

Dove la candidata ha la ragione migliore:

- **Il seam di scope viaggia con la prima riga che persiste.** `S3` porta il risolutore e un test che
  dimostra che nessuna query di ricette lo scavalca; nella reference lo scoping al ricettario arriva
  con `S12` e le righe prima leggono e scrivono non vincolate. R-013 dice «never defer the boundary
  itself»: qui la candidata è più aderente della reference.
- **`S1` è più esplicito** su driver reale, runner di migrazioni ed estensione `vector` di quanto lo
  sia `S1` della reference, che si ferma a «una pagina che legge una riga scritta da una migrazione».
- **`OUT-OF-SCOPE`**: sette licenze contro quattro, tutte nella forma giusta, incluse quelle — lavoro
  asincrono, provider email, vector DB dedicato — che la reference non scrive.

Differenza neutra: la reference apre una `Open questions` sul fallimento totale dell'estrazione; la
candidata decide in `S5` («nessuna ricetta parziale resta salvata»). Il brief non elenca quella fra
le incertezze materiali, quindi non è un difetto — la candidata ha preso una decisione che le fonti
lasciano libera, ed è visibile nella riga.

## Osservazioni sull'eval, non sulla mappa

- **H5 contro la reference.** Vedi sopra: la voce chiede React Query, che nessuno dei due artefatti
  nomina. O H5 si restringe a ciò che una mappa deve davvero contenere, o la reference è incompleta;
  finché non è deciso, quel mezzo rosso non dice niente sulla skill.
- **R-021 contro `drawing-the-map.md` § The two prerequisites.** Il test dell'enabler chiede «a real
  end-to-end production path»; la riga-repository è licenziata a non averne nessuno («No
  provisioning, no deploy»). Due clausole che si sovrappongono: un revisore che applica R-021 alla
  lettera segna rosso `S0` di qualunque run greenfield. Da chiarire in `references/`, non in
  `SKILL.md`.
- **R-020 contro R-013.** Il `Learning target` di `S3` porta due affermazioni indipendenti — che la
  normalizzazione minima regga il giro, e che un solo risolutore basti — che è un split warning di
  `slice-rules.md` («one row that can fail for two independent causes»). Ma R-013 *impone* che il
  boundary di scope viaggi con la prima riga che persiste. La coesione c'è ed è imposta dalla skill:
  non l'ho contata contro la mappa, ma è il posto dove il singolare di R-020 e l'obbligo di R-013 si
  pestano i piedi.

Nessun punteggio. Un run solo: ogni rosso qui è una domanda, non un verdetto sulla skill.
