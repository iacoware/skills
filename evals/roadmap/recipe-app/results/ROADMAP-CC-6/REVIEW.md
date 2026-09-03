# Review — ROADMAP-CC-6

Mappa: `.roadmap/` (11 righe, 6 temi, primo disegno, `archive/` vuoto). Transcript presente
(`TRANSCRIPT.jsonl`, 97 righe, 16 richieste), quindi nessuna regola di sessione resta *inconclusive*.
Nessun punteggio aggregato. La mappa è un reperto e non è stata toccata.

## Validator

`make validate-roadmap ROADMAP=evals/roadmap/recipe-app/results/ROADMAP-CC-6/.roadmap` → `OK`.
Nessun `ERROR`, nessun `WARNING` (11 righe, dentro floor 3 e cap 20).

Nella sessione il validator era partito rosso: tre `ERROR` su `S0`, `S1`, `S2` («`Depends on` names
'—', which is not a row of this register»), causati dal backtick attorno al trattino. Corretti con
un `sed` e rilanciato fino a `OK` (transcript righe 87–92). È il comportamento che R-033 chiede.

## Brief

Le otto righe `H` sono tutte ticcate; le prove stanno sotto, in *Verde, con la prova*. I rilievi sono
sulle uscite dalla sweep, e tutti e tre istanziano R-015.

- **C1** — `slices/S4-estrazione-llm.md` *Excludes*, «L'inserimento a mano: è di S8, insieme alla
  modifica, perché condivide con essa il form **e non la pipeline**», più `slices/S8-…md` *Includes*,
  dove il form manuale scrive testo libero senza attraversare estrattore né schema. La mappa prende il
  lato di `concepts.md` § *Pipeline di estrazione* (`[Input manuale] → (form vuoto) → (salta
  l'estrazione)`, riga 126) contro `arch-choices.md` § *Estrazione contenuto*, punto 3 («Copia-incolla
  / manuale: saltano il JSON-LD, riusano lo stesso motore e schema», riga 43).
  **Quel che lo falsifica:** nessuna riga di `Assumptions`, nessuna di `Open questions`, nessuno
  spike nomina C1 — il lato è preso solo in un bullet. È il tell meccanico che `drawing-the-map.md`
  chiama *Taken in a row and nowhere else*, e la forma che il brief marca come difetto («taking a side
  is allowed; taking it silently is the defect»). *Corroborazione, non regge il verdetto:* né `S4` né
  `S8` citano `arch-choices.md` fra i loro `Requested by`, quindi la fonte contraria non compare da
  nessuna parte nella mappa.

- **C2** — `roadmap.md:93-97`, `Assumptions` riga `ricerca, S5`. L'**uscita è giusta** — linea di
  `Assumptions`, tracciata a tema e id, che atterra in un bullet di `S5` («Embedding della query al
  momento della ricerca») e che la consegna può smentire. È la **ragione** che non regge: «La mappa
  legge il divieto come un divieto di ri-embeddare il corpus a ogni ricerca, non come un divieto di
  embeddare la query».
  **Quel che lo falsifica:** la frase citata ha per soggetto le query. `arch-choices.md:33` — «Usato
  **solo in fase di add** e all'edit, mai a runtime sulle query di ricerca» — non nomina il corpus, e
  `goal.md:110-111` ripete lo stesso divieto («LLM/embedding usati solo in fase di add … mai a runtime
  sulle query di ricerca»). È esattamente il caso che `drawing-the-map.md` § *Its reason survives its
  citations* chiama misreading: «a reading that leaves the sentence standing and gives it a different
  subject». La lettura che regge — vincolo di **costo**, smentito come architetturale da «le query
  sono irrilevanti» quattro righe sopra — la riga la cita e poi non la usa.
  *Corroborazione:* la riga nomina solo `arch-choices.md`, mentre due fonti dichiarano il vincolo
  insieme, e «splitting them needs a source that splits them». Il **lato scelto** (una chiamata per
  query) resta pienamente ammesso dal brief: il difetto è la ragione, non la risoluzione.

- **U4** — il hit-rate del JSON-LD non esce dalla sweep per nessuna delle tre uscite.
  **Quel che lo falsifica:** non c'è spike, non c'è riga in `Assumptions`, non c'è riga in
  `Open questions`; e la strada che A9 licenzia in alternativa — consegnare il percorso strutturato e
  leggere il tasso di miss come learning target di una riga ordinaria — non è presa: il
  `Learning target` di `S3` parla di tempo di risposta e distinzione dei passi, quello di `S4` della
  qualità del modello economico. Nessuna `Verification` conta quante pagine hanno il JSON-LD.
  *Corroborazione:* `S4` *Verification* misura il costo e l'accuratezza dell'LLM (che è U5, uscita
  correttamente da `needs-decision` più `Open questions` di riga), quindi la misura vicina c'è ed è
  un'altra.

U1, U2, U3 e U5 escono correttamente: U1 su `S1` come `needs-decision` più `Open questions` di riga —
collocazione che A1 licenzia esplicitamente; U2 nella riga `Assumptions` `goal, S1, S10` più le due
osservazioni su `S1` e `S10`; U3 con lo spike `S2` prima delle righe che blocca (A8); U5 su `S4` come
`needs-decision` più `Open questions` di riga.

## Regole

- **R-009** — `roadmap.md:21`, tema `condivisione`, promessa «Mando un link a mia sorella e da quel
  momento aggiungiamo **e correggiamo** le stesse ricette», primo validatore `S7`.
  **Quel che lo falsifica:** la `Verification` di `S7` (`slices/S7-invito-ricettario.md`) ha cinque
  bullet — il secondo account diventa membro e aggiunge, la ricerca dell'invitato pesca le ricette
  altrui, un non-invitato riceve un rifiuto, un token manomesso è nominato, un doppio invito non crea
  una seconda `Membership` — e **nessuno osserva una correzione**. La capacità è di `S8`, che nel
  registro sta due posizioni dopo e non dipende da `S7`. È la forma che `drawing-the-map.md` § *Themes*
  descrive alla lettera: «A promise names only what its first validator delivers … the promise is
  holding two: either the validator is the wrong row, or the capability is a theme the table
  compressed».
  *Corroborazione:* l'`Outcome` di `S7` afferma «aggiunge, cerca **e corregge** le stesse ricette»
  quando l'edit non esiste ancora; e `Theme boundaries` (`roadmap.md:27-38`) registra sei verdetti e
  **non** quello su `condivisione` / `correzione`, che è l'unico confine che la promessa attraversa.

- **R-012** — `roadmap.md:52`, `S8` (tema `correzione`) in posizione 9, dopo che `S5` apre `ricerca`,
  `S6` apre `accesso` e `S7` apre `condivisione`.
  **Quel che lo falsifica:** `drawing-the-map.md` § *Ordering for learning*, fra le quattro cose che
  non sono soggette a ranking: «**Required recovery outranks breadth.** … the remedy comes before a
  different theme opens». `goal.md:70-71` fa dell'edit il recupero dichiarato del salvataggio senza
  review («Nessuna review obbligatoria: l'estratto si salva subito. La correzione è sempre disponibile
  dopo»), e lo stato recuperabile nasce con `S3`, in posizione 4.
  *Corroborazione, non regge il verdetto:* la mappa lo dice due volte da sé — il `Learning target` di
  `S4` («ricette abbastanza buone da essere salvate senza review, che è la scommessa su cui poggia il
  "nessun passo obbligatorio prima del salvataggio"») e l'`Audience` di `S8` («è quello che rende
  accettabile il salvataggio senza review»); e `slice-rules.md` § *Splitting and merging a row* chiede
  di «deliver a required correction, retry or escape path **before or with** the first behaviour that
  can create the recoverable state».
  La deroga che invece **è** licenziata è `S4` subito dopo `S3`: `S3` nomina il vicolo cieco nella sua
  `Verification` («è il fallimento che S4 rimedia») e `S4` è il rimedio automatico.

- **R-020** — `slices/S9-foto-e-copertina.md`, `Learning target`: «… e **se lo fa dentro il tempo
  della pipeline sincrona di S3**».
  **Quel che lo falsifica:** nessuno dei cinque bullet di `Verification` osserva un tempo. Coprono la
  copertina servita dal proprio storage, il salvataggio della ricetta quando l'immagine non è
  scaricabile, lo scambio di copertina, lo scope del ricettario e il rifiuto di un file troppo grande.
  La riga aggiunge un download e un upload in coda a una pipeline che `S3` misura esplicitamente
  («Il tempo … è misurato su una decina di siti reali»), e la sua metà di quella misura non ha
  osservazione. `slice-rules.md` § *Verification maps to the learning target*: ogni claim materiale
  mappa su un'osservazione, e verificare che il dato esista non ne dimostra la latenza.

- **R-035** — chiusura di sessione, transcript riga 95. Il messaggio apre con «`.roadmap/` scritta e
  validata (`OK`, nessun warning).» prima delle quattro parti.
  **Quel che lo falsifica:** *Close the session* dice «report the written map, **and nothing else**»,
  e mette dopo le quattro solo quello che chiede una risposta — una `WARNING` o una domanda dovuta.
  Qui non c'era nessuna `WARNING`. Le quattro parti ci sono tutte e nell'ordine giusto (tabella
  `Themes`, registro `NOW`, `Open questions`, percorso a `roadmap.md`), senza retelling dei documenti
  né narrazione delle operazioni. Rilievo identico a quello registrato su CC-4 e CC-5, e come lì va
  letto insieme a R-033, che chiede invece che si veda che il validator ha girato: due clausole che si
  sovrappongono più di quanto il modello sbagli.

## Verde, con la prova

**Brief.** **H1** — `S2` misura il recall cross-lingua e sceglie il modello, `S5` consegna la ricerca
semantica nel prodotto, entrambe in `NOW`. **H2** — un solo resolver del ricettario corrente introdotto
in `S3`, sostituito in `S6`, pubblicato in *Cross-functional concerns* → *Authorization*; `S5` scopa la
query di similarità, `S8` scopa la modifica, `S7` verifica che l'invitato veda e modifichi le ricette
altrui. **H3** — cascata JSON-LD (`S3`) prima del fallback LLM validato con `Schema` (`S4`); il testo
incollato entra in `S4` «riusando lo stesso motore e lo stesso schema di output»; l'inserimento a mano
usa il form condiviso di `S8`. **H4** — nessun passo di review (esclusione dedicata in `OUT-OF-SCOPE`
e invariante in *Validation and errors*), edit come recupero in `S8` che rigenera l'embedding, con
l'invariante in *Data integrity and recovery*. **H5** — Google OAuth/Auth.js in `S6`, Postgres con
pgvector in `S1`, R2 in `S9`, embedding multilingue cloud in `S2`/`S3`, Next.js su Fly in `S0`/`S1`,
Effect, TanStack React Query e Drizzle installati e importati in `S0`. È la voce che CC-4 e CC-5
lasciavano *inconclusive* per assenza di React Query da ogni riga: qui il tick c'è, testuale.
**H6** — ricettari pubblici, filtri strutturati, ricerca cross-ricettario, gruppi e ruoli stanno tutti
in `LATER`, nessuno è riga `NOW`. **H7** — `S1` porta driver TCP scelto, runner di migrazioni al
deploy, rotta di salute che legge davvero, e la `Verification` include il ciclo sospensione-risveglio
due volte di seguito «cioè la connessione non resta appesa allo stato precedente», che è
l'osservazione sul pooling; il `Learning target` la nomina. **H8** — `S10` mette l'app in mano a
famiglia e amici, con audience e ambiente dichiarati.

**Regole.** **R-001** — la domanda su cosa è stato consegnato è saltata perché l'input la risponde
(nessun `.roadmap/`, «crea la directory prima»); la porta `Drawing` è scelta sul check di filesystem
(transcript riga 61) e lo stato è dichiarato in `Current state`. **R-002** — `S0`–`S10` contigui,
`archive/` vuoto, nessun id riciclato. **R-007** — l'unica `Verification` che è una misura e non una
capacità è quella di `S2`, ed è coniata come spike; nessuna misura resta dentro la riga che blocca.
**R-008** — sei promesse in lingua di prodotto e in prima persona, sei verdetti di confine ciascuno con
il fatto che lo decide; elenco e lettura dentro `cattura` non è compressione, perché la promessa nomina
entrambe le metà e `S3` le consegna entrambe. **R-010** — `S0`, `S1` e `S10` portano `theme: —` (N5).
**R-011** — repository e scheletro separati; `S1` raggiunge il datastore col driver reale, applica una
migrazione non di dominio, e tiene fuori entità, auth, tenancy e l'adapter R2 che solo `S9` usa.
**R-013** — il confine di scope entra con `S3`, prima riga che persiste; il seam è in
*Cross-functional concerns*; `Assumptions` riga `S3, S4, S5` dice cosa le righe precedenti possono
ignorare e che non andranno riscritte. **R-014** — ogni riga prima dell'identità nomina il proprio
pubblico («chi sviluppa e chi prova il prodotto, sull'ambiente non pubblico»), nessun `Outcome`
promette un utente che non può esistere, `S2` lascia `Audience` vuoto. **R-016** — l'unico `enabler` è
`S0` e non risolve nessuna incertezza della tabella. **R-017** — nove edge pubblicati, tutti superano
il test di sostituzione (`S3→S2` porta modello e dimensione della colonna; `S4`, `S5`, `S6`, `S8`, `S9`
costruiscono su tabella, pipeline o resolver che `S3` consegna; `S7→S6`; `S10→S7` è la riga da cui
entra la sua prova, come chiede la clausola sulle righe `release`); nessuna cella nomina `S0` o `S1`;
nessuna riga che costruisce su un artefatto altrui porta `—`. **R-019** — `S2`: `kind: spike`,
`Audience` vuoto, dipendente (`S3` lo nomina), nessun timebox. **R-021** — `S0` è il prerequisito di
repository che `drawing-the-map.md` prescrive, «the accounts and secrets the rest of the map spends»
compresi: non è enabler camouflage per quella clausola. **R-022** — `S1` e `S4` sono `needs-decision`
e i loro `Includes` deferiscono («il fornitore scelto», «il driver TCP scelto», «il modello LLM
scelto»); `S3` è `ready` perché la sua decisione la prende `S2`, che la precede. **R-023** — nessuna
delle failure nominate: lo scope entra con la prima scrittura, il corpus di semina di `S2` è A5/N3,
`LATER` non contiene comportamento obbligatorio non finito. **R-024** — ogni comportamento dell'MVP ha
un proprietario o un'esclusione: link (`S3`/`S4`), testo incollato (`S4`), a mano ed edit (`S8`,
merge con verdetto registrato — A10), foto e copertina (`S9`, che possiede R2 da solo), elenco e
dettaglio (`S3`), ricerca (`S5`), invito (`S7`); il passo «salvo foto» della progress bar è escluso da
`S3` e rivendicato da `S9`. **R-025** — otto candidati, nessun id, nessuna colonna, nessun documento.
**R-026** — le quattro esclusioni sono scritte come licenza, ciascuna col suo prezzo. **R-032** — nessun
`.roadmap/` all'inizio, mappa scritta subito senza chiedere conferma, in cinque scritture batch e non
un file per volta con una domanda in mezzo. **R-033** — validator girato dopo la scrittura, tre `ERROR`
corretti, nessuna `WARNING` da girare all'autore.

## Rilievi minori, sotto la soglia della violazione

- **Il resolver non ha un nome.** `drawing-the-map.md` § *The identity seam* chiede «one **named**
  resolver». La mappa lo descrive sempre come «il resolver del ricettario corrente» e mai con un
  identificatore. La singolarità e l'identificabilità — quello che la clausola compra — ci sono
  comunque, e `S6` dice «è l'unico punto che cambia». Non lo conto contro R-013.
- **Testo indicizzato.** `goal.md:81-82` mette `tag + tempo` nel testo indicizzato quando derivati.
  `S2` misura se convenga («è quello che decide se vale la pena derivarli») ma i suoi `Excludes`
  dicono che a `S3` passano «la scelta del modello, la dimensione della colonna e la definizione
  dell'indice» — non quella risposta. Il comportamento non resta però orfano: *Data integrity and
  recovery* impegna ogni scrittura di `tags` o `prepTime` a rigenerare l'embedding, il che presuppone
  che ci siano dentro. Resta una tensione fra un invariante che ha già deciso e uno spike che
  misurerà, non un buco di proprietà: non lo conto contro R-024.
- **`S8` e `S9` verificano l'appartenenza portando `Depends on: S3`.** Le due `Verification` hanno un
  bullet ciascuna che parla di «chi non ne è membro», cosa che esiste da `S6`. Nel registro `S6` le
  precede entrambe, l'`Outcome` di entrambe sta in piedi senza appartenenza, e l'invariante di
  autorizzazione è verificata dove il boundary si attraversa la prima volta. Edge non dovuto: R-017
  resta verde.

## Riferimento

Letto per ultimo. Non è un target di diff: id, titoli e numero di righe differiscono e N6 lo licenzia.
Su ogni differenza, chi ha la ragione migliore.

- **C1 e C2 sono le due differenze che contano.** Il riferimento pubblica entrambe le letture in
  `Assumptions` — C2 come «vincolo di costo, non di architettura … la mappa sceglie la lettura
  economica», C1 come «`concepts.md` fa saltare l'estrazione … la mappa legge il diagramma». Ragione
  migliore al riferimento su tutte e due: stesso lato su C1, stessa risoluzione su C2, ma dette.
- **U4.** Il riferimento la fa uscire da due lati — riga `Assumptions` `import-automatico, S9` e
  `Learning target` di `S9` («Quanto spesso il JSON-LD copra davvero i siti che i nostri utenti
  incollano: è la misura che decide se il fallback è un caso limite o la strada principale»). È
  precisamente la strada che A9 licenzia e che il candidato non prende. Ragione migliore al
  riferimento.
- **Ordine della correzione.** Il riferimento mette `S7` (scrittura e correzione a mano) in posizione
  8, **prima** di `S8` (import da URL), e ne dà la ragione nel `Learning target`: «è la condizione che
  rende accettabile salvare subito un'estrazione imperfetta». Il candidato dice la stessa frase
  nell'`Audience` di `S8` e poi consegna la riga sei posizioni dopo lo stato che la richiede. Ragione
  migliore al riferimento: è la conferma indipendente del rilievo R-012.
- **Fallback LLM e copia-incolla.** Riferimento: due righe (`S9`, `S10`), con learning target e
  audience distinti. Candidato: una riga (`S4`). Pari — `slice-rules.md` § *Cohesion that holds*
  licenzia esplicitamente «several inputs into one established pipeline may therefore stay one row», e
  il candidato nomina la coesione («riusando lo stesso motore e lo stesso schema di output»).
- **Consultazione come tema proprio.** Riferimento: `consultazione` con primo validatore `S5`, elenco
  e lettura schedulabili contro ricette seminate. Candidato: elenco e dettaglio dentro `S3`, sotto
  `cattura`. Ragione migliore al riferimento sul test di split, ma il candidato non nasconde niente —
  la promessa nomina entrambe le metà e `S3` le consegna entrambe — quindi R-009 tiene lì e cade
  altrove, su `condivisione`.
- **Il differenziatore su dati seminati.** Il riferimento consegna indicizzazione e ricerca (`S3`,
  `S4`) prima che esista un modo di aggiungere una ricetta. Il candidato valida il rischio esistenziale
  nello spike `S2` e porta la ricerca nel prodotto in posizione 6, dopo l'import. Pari: A5 e N3
  licenziano il riferimento, e «the map declares its own ranking» licenzia il candidato, che il rischio
  esistenziale lo chiude comunque per primo.
- **Cosa succede se l'estrazione fallisce del tutto.** Il riferimento la pubblica come domanda aperta;
  il candidato la decide in un bullet di `Verification` di `S4` («la ricetta non viene salvata a
  metà»). Non è una voce del brief e non entra nel tally; fra le due, una decisione presa e scritta
  vale la domanda pubblicata.
- **Domanda aperta sullo switcher fra ricettari.** Solo il candidato ce l'ha, ed è ben posta: cambia
  la forma della mappa («è una riga che questa mappa non ha»), quindi sta ad altitudine di mappa dove
  lo scope la manda. Ragione migliore al candidato — `goal.md:92` dice che un utente può stare in più
  ricettari e nessuna fonte dice come si sceglie il corrente.
- **Riga `Cost` in *Cross-functional concerns*.** Solo il candidato ce l'ha ed è la sesta dimensione,
  licenziata quando una fonte ne fa un vincolo di più righe. Nessuna delle sei righe sopravvive a
  essere spostata in un altro progetto: nessuna *ambient restatement*.

## Tally

I check che la carta 0 ammette sono le 28 regole — tutte meno R-006, R-018 e *Revising an existing
map* (R-027–R-031) — più H1–H8: 36.

- **Verdi (27)** — R-001, R-002, R-007, R-008, R-010, R-011, R-013, R-014, R-016, R-017, R-019,
  R-021, R-022, R-023, R-024, R-025, R-026, R-032, R-033, H1, H2, H3, H4, H5, H6, H7, H8.
  H5 è verde qui e *inconclusive* su CC-4 e CC-5 per una ragione testuale, non per un cambio di
  lettura: `S0` nomina TanStack React Query, che in quelle mappe non compariva.
- **Rossi (5)** — R-009, R-012, R-015, R-020, R-035. R-015 raccoglie tre rilievi — C1, C2, U4 — e
  conta una volta; R-009 conta una volta anche col verdetto di confine mancante, che è corroborazione
  dello stesso difetto e lascia R-008 verde.
- **Inconclusive (0)** — il transcript c'è, e nessuna regola di sessione resta senza prova.
- **Non applicabili o saltati (4)** — R-003, R-004, R-005 (nessun input contro un goal registrato:
  greenfield), R-034 (nessun handover richiesto né offerto, e la sessione non ne ha inventato uno).

Pass rate: 27/32 ≈ 84%. Rule set: `fb29812`.

Il tally è una linea di tendenza fra run della stessa carta sullo stesso rule set, non un verdetto
sulla mappa. Il giudizio resta per check, su due run: **R-015, R-020 e R-035** sono rossi su due run
consecutivi (CC-5, CC-6), e su R-015 e R-035 è la stessa clausola due volte — C1 presa in un bullet
e taciuta, e la riga di stato prima delle quattro parti. **R-009 e R-012** sono rossi qui e verdi su
CC-5: un run solo non decide. **R-017** è rosso su CC-5 e verde qui.
