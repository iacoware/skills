# Review — ROADMAP-CC-5

Mappa: `.roadmap/` (11 righe, 6 temi, primo disegno, `archive/` vuoto). Transcript presente
(`TRANSCRIPT.jsonl`, 133 righe, 26 richieste), quindi nessuna regola di sessione resta *inconclusive*.
Nessun punteggio. La mappa è un reperto e non è stata toccata.

## Validator

`make validate-roadmap ROADMAP=evals/roadmap/recipe-app/results/ROADMAP-CC-5/.roadmap` → `OK`.
Nessun `ERROR`, nessun `WARNING` (11 righe, dentro floor 3 e cap 20).

## Brief

- **C1** — `slices/S3` *Excludes*, «Nessuna estrazione da link o da testo: sono di S5 e S6». La mappa
  prende il lato di `concepts.md` (*Pipeline di estrazione*: `[Input manuale] → (form vuoto) → (salta
  l'estrazione)`) contro `arch-choices.md` (*Estrazione contenuto*, punto 3: «Copia-incolla /
  manuale: saltano il JSON-LD, riusano lo stesso motore e schema»), e non c'è nessuna riga in
  `Assumptions` né in `Open questions` che lo dica. È la forma esatta che il brief chiama difetto —
  *taking a side is allowed; taking it silently is the defect* — e che R-015 marca `⚠ failed`.
  `S6` condivide lo `Schema` di output con `S5`, non con il form manuale di `S3`: la conciliazione
  parziale non è la riga dovuta.
- **C2** — `roadmap.md` *Assumptions*, riga `ricerca, S4`: l'uscita è corretta (linea di
  `Assumptions`, risoluzione per-query, ammessa dal brief) ma **la ragione non regge le sue
  citazioni**. La riga legge il divieto «come riferito all'LLM e alla ri-indicizzazione del corpus»;
  la frase citata (`arch-choices.md`, *Embeddings*: «Usato **solo in fase di add** e all'edit, mai a
  runtime sulle query di ricerca») ha per soggetto gli embedding, non l'LLM, e `goal.md` *Vincoli e
  scala* ripete lo stesso divieto nominando entrambi — fonte che la riga non cita e che
  `drawing-the-map.md` (*Its reason survives its citations*, «two sources state a constraint
  together») obbliga a trattare insieme. La ragione che regge — vincolo di costo smentito quattro
  righe sopra da «le query sono irrilevanti» — la riga la sfiora («poche righe sopra conta il costo
  delle query») senza farne il fondamento.
- **H5** — `slices/S0` *Includes* enumera lo stack («Next.js (App Router), Effect, Drizzle e Vitest»)
  e omette React Query, che `tech-choices.md` (*Data fetching client — TanStack React Query*) decide
  e che H5 elenca. Nessuna altra riga lo nomina. Difetto minore e da tenere sotto osservazione: anche
  `reference-roadmap/` non lo nomina (dice «le convenzioni di progetto già scelte»), quindi il difetto
  potrebbe stare nella granularità di H5 più che nella mappa.

Ticcate senza riserve: **H1** (`S4`), **H2** (`S3` resolver + `S4` scope + `S9` pari), **H3**
(`S5`→`S6` a cascata, form condiviso in `S3`), **H4** (`S5` salva senza revisione, `S4` rigenera
l'embedding a ogni modifica), **H6** (`LATER` + `OUT-OF-SCOPE`), **H8** (`S10`).
**H7** è ticcata in sostanza (`S1`: driver standard su TCP, migrazione non di dominio applicata al
deploy, `suspend` + scale-to-zero, risveglio misurato) ma non nomina il *pooling*; il rischio compare
solo come «senza connessioni morte» nel *Learning target*. Non lo conto come miss.

A1, A2, A3, A4, A5, A6, A7, A8, A9, A11 sono tutte esercitate e nessuna è violata. U1 (`S0`
`needs-decision`), U2 (`S1`+`S10`), U3 (`S2`), U5 (`S6`) escono per un'uscita legittima. **U4 esce per
la strada di A9 — riga ordinaria con learning target misurabile — ma la misura non c'è: vedi R-020 su
`S5`.** N1–N6 non producono rilievi.

Credito, fuori tabella: la mappa trova un conflitto che il brief non elenca e lo risolve con una riga
(`Assumptions`, `estrazione, S5`) — i quattro passi della progress bar di `goal.md` non sono gli stadi
della pipeline di `concepts.md`. È lo sweep dentro un solo documento che `drawing-the-map.md` chiede.

## Regole

- **R-020** — `slices/S5`. Il *Learning target* afferma «se il solo JSON-LD copre abbastanza pagine
  reali da valere come il percorso gratuito che le fonti assumono», ma la *Verification* esercita
  «Tre URL veri di blog di cucina **che espongono JSON-LD**» più un URL senza: URL scelti perché
  hanno il dato non possono misurare quanto spesso manca. La consegna non può smentire l'affermazione,
  e questa è anche la misura che A9 pretende quando U4 esce senza spike.
- **R-020** — `slices/S7`. La seconda metà del *Learning target* («o se in pratica la allunga oltre il
  budget di richiesta») non ha osservazione: la *Verification* prova che la ricetta si salva con R2
  irraggiungibile, non misura quanto lo stadio foto allunghi l'aggiunta. Il budget era stato misurato
  in `S5` sul flusso senza immagini.
- **R-020** — `slices/S9`. Il *Learning target* chiede «se il fatto che dentro un ricettario siano
  tutti pari regge all'uso vero, o se la prima famiglia chiede un ruolo»; la *Verification* gira su due
  account Google di prova su staging. Le persone vere arrivano in `S10`: la consegna di `S9` non può
  smentire la sua stessa affermazione.
- **R-017** (*dropped edge*) — `roadmap.md` *NOW*, riga `S5`, `Depends on: S3`. L'ultima frase della
  *Verification* di `S5` — «Le ricette salvate qui compaiono nella ricerca di `S4`» — esercita una
  capacità che `S4` consegna, e `drawing-the-map.md` (*Hard dependencies*, «Read the dependent's
  `Verification` as well as its `Includes`») dice che allora la riga non porta quell'assenza. Un
  riordino che spostasse `S4` dopo `S5` romperebbe quella prova senza che nessuno se ne accorga.
  Lettura contraria da registrare: l'asserzione è marginale rispetto al resto della prova di `S5` e si
  potrebbe togliere; l'edge sarebbe allora ordine e non dipendenza.
- **R-035** — chiusura di sessione, ultimo turno del transcript. Il messaggio apre con «Mappa scritta
  e validata (`OK`, nessun `WARNING`).» prima delle quattro parti: è narrazione di un'operazione, che
  *Close the session* esclude. Le quattro parti ci sono tutte e nell'ordine, e la domanda dovuta su
  `S0` (Neon o Supabase) sta **dopo** le quattro, dove la regola la vuole.

Rilievi minori, sotto la soglia della violazione ma da registrare:

- `slices/S2` *Includes* porta «Confronto fra scan esatto e indice HNSW alla dimensione del corpus»,
  che non ha né un'affermazione nel *Learning target* né un'osservazione nella *Verification*, e che
  duplica quello che la riga `ricerca, S4` di `Assumptions` dice che sarà il p95 di `S4` a smentire.
- **A10** — il verdetto sulla fusione fra inserimento manuale ed edit è implicito: `slices/S3`
  *Includes* enuncia il fatto («Un solo form, usato sia per scrivere una ricetta nuova sia per
  correggerne una esistente») ma non lo registra come verdetto. `slice-rules.md` licenzia
  esplicitamente la coesione («Shared create-and-edit review … may therefore stay one row»), quindi
  il difetto è di registrazione, non di forma.

Verificate e verdi: **R-002** (`S0`–`S10` per incremento, nessun riciclo, greenfield), **R-007**
(la misura è `S2`, minted come spike; nessun'altra riga nasconde una misura al posto di una capacità),
**R-008** (sei promesse in linguaggio di prodotto, cinque verdetti di confine, uno per coppia
adiacente), **R-009** (ogni first validator è una riga `NOW` esistente e nessuno è `enabler`),
**R-010** (`theme: —` su `S0`, `S1`, `S10`), **R-011** (repository e scheletro separati; `S1` tocca
Postgres col driver reale, applica una migrazione non di dominio, non porta dominio né auth né
tenancy), **R-012** (l'unica deroga a breadth-before-depth è `S6` dopo `S5`, ed è *required recovery*:
`S5` nomina il vicolo cieco nella sua *Verification* e `S6` è il rimedio), **R-013** e **R-014**
(seam su `S3` con `CurrentCookbook`, pubblicato in *Cross-functional concerns*, registrato in
`Assumptions`; ogni riga prima dell'identità nomina la sua audience e nessun `Outcome` promette un
utente che non può esistere), **R-016** (l'unica riga `enabler` è `S0`, e non risolve incertezze di
due sottosistemi del brief), **R-017** per gli edge *pubblicati* (tutti superano il test di
sostituzione; nessuna cella nomina `S0` o `S1`), **R-019** (`S2`: `kind: spike`, `Audience` vuota,
dipendente `S4`, nessun timebox), **R-021**, **R-022** (`S0` è `needs-decision` e `Includes` e
`Verification` dicono «il provider scelto»; `S1` può restare `ready` perché `tech-choices.md`
*Persistenza / ORM* decide driver e modo di connessione), **R-023** (nessuno dei fallimenti nominati;
lo scope non è differito, il corpus di seed è licenziato da A5/N3), **R-024**, **R-025**, **R-026**
(tutte e cinque le voci scritte come licenza, con il prezzo).

Dal transcript: **R-001** — non c'è un controllo esplicito di `.roadmap/` prima della scelta della
porta (`ls -la sources/ && mkdir -p .../ROADMAP-CC-5`), e la porta `Drawing` è dichiarata più che
verificata; è però vera per costruzione, dato che la sessione ha creato lei la project root, e il
prompt risponde da sé alla domanda su cosa è stato consegnato. **R-032** — nessuna `.roadmap/` in
piedi, mappa scritta subito e senza chiedere conferma, nessuna domanda fra un file e l'altro: verde.
**R-033** — validator girato dopo la scrittura, primo giro rosso (id e `—` scritti fra backtick nella
colonna `Depends on`), errori corretti, secondo giro `OK`, nessun `WARNING` da girare all'autore:
verde.

Non applicabili su questo run: R-003, R-004, R-005 (nessun input che contraddica un goal registrato),
R-034 (nessuna richiesta di handover). Saltate su richiesta: sezione *Revising an existing map*
(R-027–R-031), R-006, R-018.

Un caso da rimandare al proprietario del check, non alla mappa: **R-021 vs R-011**. `S0` è la riga di
repository che `drawing-the-map.md` impone, e nella tassonomia di `kind` non c'è una casella per lei —
`enabler` è l'unica che resta, e poi `S0` fallisce i test dell'enabler («a real end-to-end production
path»). È una clausola che dice due cose che si sovrappongono, non un difetto della mappa.

## Contro `reference-roadmap/`

Non è un target di diff: 11 righe contro 15, sei temi contro sette, id e titoli diversi — tutto
licenziato da N6. Le differenze che meritano una domanda su chi ha la ragione migliore:

- **C1 pubblicato o no.** Il riferimento porta la riga (`Assumptions`, `inserimento-manuale, S7`) e
  dice quale lato prende e perché; il candidato prende lo stesso lato e tace. Ragione migliore al
  riferimento — è la violazione già registrata sopra.
- **Dove sta l'identità.** Riferimento: `S6`, settima di quindici, prima della scrittura a mano e
  dell'import. Candidato: `S8`, dopo cinque righe che consegnano comportamento a un utente finale.
  A11 licenzia entrambe e ognuna nomina la sua audience. Ragione migliore al riferimento, di poco:
  R-013 vuole che, differita l'identità oltre la seconda riga di comportamento, davanti le stiano *le
  righe che producono l'evidenza su cui la deroga si regge* — `S5`, `S6` e `S7` non producono quella
  evidenza, e la loro accettazione resta appesa a uno staging non pubblico. Il candidato però paga la
  deroga con qualcosa che il riferimento non ha: `S8` verifica il giunto («il diff mostra che sono
  cambiati il `Layer` del resolver e le rotte, e nessun punto di query»), che è la scommessa di `S3`
  chiusa esplicitamente.
- **Fallback LLM e copia-incolla, una riga o due.** Riferimento: `S9` e `S10` separate, «different
  learning targets — how often the structured path misses, versus whether a model extracts from
  unstructured text within budget». Candidato: fuse in `S6`. Ragione migliore al riferimento, e si
  vede nell'esito: fondendole, la domanda sul tasso di miss è rimasta a carico di `S5`, dove non ha
  osservazione (R-020 sopra). `slice-rules.md` licenzia la coesione «several inputs into one
  established pipeline», quindi la fusione in sé non è un difetto — la misura persa sì.
- **Indicizzazione separata dalla ricerca.** Riferimento: `S3` enabler + `S4` prodotto. Candidato:
  tutto in `S4`. Pari: il riferimento compra l'indice su dati veri prima che ci sia una barra di
  ricerca da discutere, il candidato evita di coniare un enabler che non può validare la promessa.
- **Dove sta il `needs-decision` sul provider Postgres.** Riferimento su `S1`, candidato su `S0`.
  A1 dice che blocca lo scheletro da solo; il candidato lo mette dove l'account si apre e lo scrive
  nelle `Open questions` di `S0` («la riga non può aprire l'account finché non è deciso quale»).
  Ragione migliore al candidato: è la riga che il blocco ferma per prima, e resta ad altitudine di
  riga come A1 chiede.
- **Gli edge della riga di rilascio.** Riferimento: `S14` nomina `S12` da sola, per non riscrivere
  mezza mappa. Candidato: `S10` nomina `S6`, `S7`, `S9` — e `S6` e `S7` non sono antenati di `S9`,
  quindi senza quegli archi un riordino romperebbe la prova di `S10`. Ragione migliore al candidato:
  tre archi su undici righe non seppelliscono niente, e il *dropped edge* costa più del rumore.
- **`consultazione` come tema a sé.** Il riferimento separa sfogliare/leggere dallo scrivere a mano;
  il candidato li tiene nel tema `ricettario`. È il punto dove guardare la *theme compression*: la
  lettura è schedulabile contro ricette seminate o importate senza che esista la scrittura a mano.
  Ragione migliore al riferimento sul test di split; il candidato però non nasconde niente — la sua
  promessa nomina entrambe le metà e `S3` le consegna entrambe, quindi R-009 tiene.
- **Cosa succede se l'estrazione fallisce del tutto.** Il riferimento la lascia come domanda aperta;
  il candidato la decide e la registra in *Cross-functional concerns* («Un errore che il flusso non sa
  nominare non salva una ricetta parziale»), e la fa verificare da `S6` («non lascia niente nel
  database»). Ragione migliore al candidato: il brief non la elenca fra le C, e una decisione presa e
  scritta è meglio di una domanda pubblicata.
- **Spostare o copiare una ricetta fra ricettari.** Il riferimento la pubblica come domanda aperta; il
  candidato non ne parla né come riga né come esclusione. Ragione migliore al riferimento — le fonti
  davvero tacciono — ma non è una voce del brief e non è una violazione di R-024, perché non è un
  comportamento che le fonti descrivano.
- **`tags` e `prepTime` derivati.** Riferimento: `S13`, enabler proprio, con due archi. Candidato:
  derivazione dentro `S5` e `S6`, consumo dentro `S4`. Pari: il riferimento dà alla derivazione un
  proprietario unico, il candidato la tiene dentro il percorso di estrazione che la produce e chiude
  con un'esclusione esplicita in `S3`.

Due cose che il candidato ha e il riferimento no, entrambe legittime: la riga **Cost** in
*Cross-functional concerns* (sesta dimensione, licenziata quando una fonte ne fa un vincolo di più
righe) e il conflitto sulla progress bar trovato dentro un solo documento.

## Tally

Backfill: la sezione non c'era quando il report è stato scritto, ed è derivata dai rilievi sopra
senza rileggere la mappa. I check che la carta 0 ammette sono le 28 regole — tutte meno R-006,
R-018 e *Revising an existing map* (R-027–R-031) — più H1–H8: 36.

- **Verdi (27)** — R-001, R-002, R-007, R-008, R-009, R-010, R-011, R-012, R-013, R-014, R-016,
  R-019, R-021, R-022, R-023, R-024, R-025, R-026, R-032, R-033, H1, H2, H3, H4, H6, H7, H8.
  R-001 è vera per costruzione, come il report registra; H7 è «ticcata in sostanza» e il report
  sceglie di non contare il pooling come miss.
- **Rossi (4)** — R-015, R-017, R-020, R-035. C1 conta una volta sotto R-015 e C2 la corrobora; i
  tre rilievi R-020 (`S5`, `S7`, `S9`) contano una volta.
- **Inconclusive (1)** — H5: rilievo registrato (React Query assente da ogni riga), marchio
  sospeso — nemmeno `reference-roadmap/` lo nomina, e il report di CC-4 chiede di riscrivere o
  restringere la voce prima di contarla contro un run.
- **Non applicabili o saltati (4)** — R-003, R-004, R-005 (nessun input contro un goal registrato),
  R-034 (nessun handover richiesto né offerto).

Pass rate: 27/31 ≈ 87%. Rule set: `7d3c34c`.
