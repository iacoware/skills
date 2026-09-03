# Review — ROADMAP-CC-7

Carta 0 (`Drawing` greenfield, headless), mappa a 11 righe e 6 temi. Rule set fissato a `3fc0293`,
lo stesso commit che `PROMPT.md` dichiara per il run: mappa e regole sono coetanee.

`TRANSCRIPT.jsonl` c'è (118 righe, 21 richieste): nessun check resta *inconclusive* per mancanza di
sessione.

**Validator.** `make validate-roadmap` sulla mappa come sta oggi: `OK`, nessun `ERROR` e nessun
`WARNING` — 11 righe stanno fra il floor di 3 e il cap di 20. Il transcript mostra che alla prima
esecuzione (idx 102) il validator aveva dato 7 `ERROR` — backtick dentro le celle `Id` e
`Depends on`, che facevano leggere `` `S2 `` e `S3` `` come nomi di riga e lasciavano lo spike senza
dipendente — corretti a mano (idx 106) e ri-eseguito pulito (idx 110). È il comportamento che R-033
chiede; l'artefatto non porta traccia del passaggio.

Ordine di lettura seguito: brief → regole → riferimento.

---

## 1. Il brief

### Vincoli duri

Tutte e otto le righe `H` si spuntano. Dove:

| ID | Dove si spunta |
|---|---|
| H1 | `S6` in `NOW`, tema `ricerca`, con `S2` che ne misura prima il recall cross-lingua |
| H2 | resolver unico in `S3`, scope della ricerca in `S6` (`Verification` con due ricettari), membri pari in `S8` (`Verification`: il secondo cancella una ricetta del primo) |
| H3 | cascata `S4` (JSON-LD) → `S5` (LLM validato con lo stesso `Schema`, mai castato); testo incollato in `S5`; form condiviso in `S3` |
| H4 | `S4` «Nessun passo di conferma»; `OUT-OF-SCOPE` «Il passo di review nel flusso di aggiunta»; rigenerazione in `S6` `Includes` e in `Cross-functional concerns` → Integrità |
| H5 | Google OAuth `S7`, Postgres+pgvector `S0`/`S1`, R2 `S9`, embedding cloud multilingue `S2`/`S6`, Next.js su Fly `S1`, Effect+React Query+Drizzle `S3` |
| H6 | tutte e cinque le voci in `LATER`, nessuna riga `NOW`; `visibility=public` esiste nel tipo di `S7` e non ha strada, che è la modellazione di N2 e non una consegna |
| H7 | `S1` apre una connessione TCP reale col driver standard, applica migrazioni al deploy e cronometra il primo colpo dopo la sospensione |
| H8 | `S10`, con audience «famiglia e amici, sull'app vera» e ≥3 persone che non hanno scritto il codice |

### Conflitti e incertezze

**R-015 · C1 — `slices/S5-estrazione-llm.md:56` (`Excludes`).** Il lato di C1 è preso lì e in nessun
altro posto: «L'inserimento manuale a form vuoto: è già in `S3`, perché le sorgenti lo danno come lo
stesso form dell'edit e non come un terzo motore».

*Il fatto che regge il verdetto:* `Assumptions` porta cinque righe (costo, embedding della query,
passi della barra, scope pre-login, ricettario al primo login) e `Open questions` due (tetto di
aggiunte, uscita da un ricettario); nessuna delle sette nomina C1, e nessuno spike lo copre. È il
tell meccanico di `drawing-the-map.md` § *What the map reports about its input*: la lettura è
*applicata* in un bullet e non è *riportata* da nessuna parte, e chi legge non distingue una
decisione da una svista.

*Corroborazione, non il verdetto:* il bullet presenta le sorgenti come concordi («le sorgenti lo
danno come…»), mentre `arch-choices.md`, “Estrazione contenuto”, punto 3 dice l'opposto —
«Copia-incolla / **manuale**: saltano il JSON-LD, riusano lo stesso motore e schema». Il lato scelto
è legittimo (lo sceglie anche il riferimento); il modo in cui è scritto trasforma un conflitto in
un'unanimità che le sorgenti non hanno.

Il resto della tavola esce bene, e va detto per non lasciare il rosso da solo:

- **C2** — riga di `Assumptions` (`ricerca`, `S6`) che nomina la lettura, la motiva e cita proprio la
  riga che il brief indica come prova: «`arch-choices.md`, poche righe sotto il divieto, conta
  comunque il costo delle query e lo chiama irrilevante». Atterra in `S6` `Includes` e in
  `Cross-functional concerns` → Costo. Nessun rilievo.
- **U1** — `S0` `readiness: needs-decision` più la riga nelle `Open questions` della riga. Su riga e
  non ad altitudine di mappa, come vuole lo scope.
- **U2** — `S1` `Learning target` la misura, `S10` la rimisura su una persona vera, `LATER` tiene
  pronta la macchina calda come flag. È esattamente la forma che A4 licenzia.
- **U3** — spike `S2` prima di `S6`, che lo nomina in `Depends on`. Uscita 3 di A8.
- **U4** — `S4` `Verification`: «La quota di URL coperti dal solo JSON-LD, su quei dieci, è contata e
  scritta». Uscita che A9 licenzia esplicitamente.
- **U5** — `S5` `needs-decision` più la riga nelle sue `Open questions`, e il costo per ricetta
  misurato in `Verification`.

---

## 2. Le regole

Saltate come da istruzioni: la sezione *Revising an existing map* (R-027…R-031, R-038), R-006,
R-018. Non applicabili su questa carta: R-003, R-004, R-005 (non c'è input oltre alle sorgenti e non
c'è mappa in piedi) e R-034 (nessun handover chiesto, nessuno fatto — che è il comportamento giusto,
ma non c'è niente da misurare).

### Rilievi

**R-020 — `slices/S4-aggiunta-da-link.md:51` (`Learning target`).** La seconda metà della riga —
«che un'estrazione sincrona con progress reale sia un'attesa che una persona sopporta senza un passo
di conferma alla fine» — è la scommessa che giustifica l'assenza del passo di review, ed è materiale.

*Il fatto che regge il verdetto:* nessuno dei cinque bullet di `Verification` la osserva. Contano
dieci ricette entrate, contano gli stop della barra, contano la quota JSON-LD, controllano che la
ricetta sia nel database prima che l'utente tocchi qualcosa. Nessuno misura l'attesa e nessuno mette
davanti una persona. È il caso nominato in `slice-rules.md` § *Verification maps to the learning
target*: «Checking that data exists does not demonstrate its quality, **usability**, **latency** or
cost».

*Corroborazione:* `S6` misura la p95 e la misura a macchina appena risvegliata, quindi la mappa sa
scrivere l'osservazione dove la vuole — qui non l'ha scritta.

**R-024 — derivazione di tag e tempo: comportamento senza proprietario.** Il primo bullet di
`Excludes` in `slices/S6-ricerca-semantica.md:63` la butta fuori: «La derivazione dei tag quando
l'estrazione non li dà: restano vuoti».

*Il fatto che regge il verdetto:* non compare né in `LATER` né in `OUT-OF-SCOPE`, e nessun `Includes`
di nessuna riga la porta. `slice-rules.md` § *Conserve the behaviour set* è esplicito: «A behaviour
that loses its owner moves to `LATER` as a candidate or to `OUT-OF-SCOPE` as an exclusion. It never
simply disappears». `LATER` porta i *filtri* strutturati, che sono un'altra cosa: i filtri sono
lettura, la derivazione è scrittura.

*Corroborazione 1:* i due bullet di `Excludes` di `S6` si contraddicono a due righe di distanza —
quello sui filtri dice «I campi si popolano già da `S4` e `S5`, quindi i filtri si accenderanno senza
migrazione né lavoro retroattivo», quello sui tag dice che restano vuoti. `S4` prende tag e tempo
solo «quando ci sono» nel JSON-LD.

*Corroborazione 2:* `goal.md`, “Principi guida” — «Campi accessori (tag, tempo) sono derivati
automaticamente, best-effort, mai richiesti» — e “Ricerca (MVP)” — «i campi si popolano da subito in
automatico, così i filtri diventano abilitabili senza migrazione né lavoro retroattivo», con la
ragione per cui contano: «i tag portano segnale che il testo non contiene, es. "vegano"». Il segnale
è per la ricerca, cioè per il differenziatore, non per i filtri rimandati.

**R-024 — cancellazione di una ricetta: verificata due volte, consegnata da nessuno.**
`slices/S8-invito-e-membri.md:35` («Il secondo membro può aggiungere una ricetta, **cancellare una
ricetta del primo**…») e `slices/S9-foto-ricetta.md:43` («Cancellando una ricetta, i suoi oggetti su
R2 non restano orfani»).

*Il fatto che regge il verdetto:* `S3` `Includes` elenca «Elenco delle ricette del ricettario
corrente, dettaglio di una ricetta, creazione e modifica» — niente cancellazione — e nessun `Excludes`
della mappa la nomina. Due `Verification` che nessuno può eseguire, o un comportamento che entra da
una porta di servizio: in entrambi i casi non ha proprietario.

*Nota, non corroborazione:* le sorgenti non chiedono la cancellazione da nessuna parte. È la mappa
stessa a metterla in scope, ed è per questo che il rilievo sta in piedi: fosse fuori scope, le due
`Verification` non l'avrebbero esercitata.

**R-035 — la chiusura non apre sulle quattro parti.** Ultimo messaggio della sessione (transcript idx
114), prima riga: «Mappa scritta. Validator pulito, nessun `WARNING`.»

*Il fatto che regge il verdetto:* `SKILL.md` § *Close the session* mette la notizia del validator
**dopo** le quattro — «Anything that genuinely needs an answer goes after the four: a `WARNING` from
the validator» — e chiude la lista con «and nothing else». Qui sta prima, ed è la prima cosa che
l'autore legge. Le quattro parti ci sono tutte e nell'ordine giusto (`Themes`, register, `Open
questions`, path).

*Corroborazione:* le due `Open questions` sono riscritte più corte invece di essere lette dal file
come sta («Se si può, è una riga che manca» contro «Se la risposta è che si può, è una riga che oggi
la mappa non ha»), dove la regola dice *read off the files as they now stand*.

### Verdi, e su cosa

- **R-001** — `ls -la` sulla project root e su `.roadmap` (idx 33), niente in piedi → porta
  `Drawing`, e la domanda su cosa è stato consegnato non è dovuta perché non c'è niente da
  consegnare. `Current state` lo dice sulla mappa.
- **R-002** — `S0`…`S10` per incremento, `archive/` vuoto, nessun id riciclato (confermato dal
  validator).
- **R-007** — la lettura dello spike test scatta dove deve: l'unica domanda la cui verifica onesta è
  un numero (il recall cross-lingua) è `S2`, `kind: spike`. Il hit-rate JSON-LD resta su riga
  ordinaria, che A9 licenzia. La metà *proposed in the block* della regola è roba della porta
  `Revising` e qui non gira.
- **R-008** — sei temi, sei promesse in lingua di prodotto, cinque confini adiacenti e cinque
  verdetti in `log.md`, uno per confine, con il fatto che decide.
- **R-009** — ogni primo validatore è una riga `NOW` esistente, nessuno è `enabler`, e nessuna
  promessa ha una metà che il suo validatore esclude — inclusa `foto`, la più esposta, dove `S9`
  copre sia la copertina scelta sia la foto che arriva dal link.
- **R-010** — `S0`, `S1`, `S10` con `theme: —` (N5).
- **R-011** — repository e scheletro separati; `S1` raggiunge il datastore col driver TCP reale, gira
  il migration runner al deploy e lascia fuori gli adapter che una sola riga dopo usa («metterli qui
  sarebbe rischio senza consumatore»). Le migrazioni non di dominio sono due invece di una: è il
  minimo della regola superato di uno, non lo scheletro sovradimensionato.
- **R-012** — `S5` è la seconda riga di `import` prima che si aprano `ricerca`, `identita`,
  `condivisione` e `foto`, e la partenza è quella che la skill non solo licenzia ma *impone*:
  «Required recovery outranks breadth» — `S4` nomina due modi di fallire in `Verification` e scrive
  due volte «Il rimedio è `S5`». `S6` apre l'adapter di embedding e segue tutti i suoi feeder
  (`S3`, `S4`, `S5`), come vuole *A row that opens a pipeline or adapter*; `S9` fa lo stesso con R2.
- **R-013** — il boundary parte con `S3`, resolver unico dietro `Context.Tag`, seam sotto
  `Cross-functional concerns` → Autorizzazione, e la riga di `Assumptions` che dice cosa le righe
  prima possono ignorare. L'identità è rimandata oltre la seconda riga di comportamento, e la riga
  che produce l'evidenza del rinvio (`S3`, il cui `Learning target` è proprio quella scommessa) la
  precede.
- **R-014** — `S3`, `S4`, `S5`, `S6` nominano un'audience di staging; nessun `Outcome` prima di `S7`
  promette un utente che non può esistere.
- **R-016** — l'unico `enabler` è `S0`, che porta una sola incertezza del brief (U1, Delivery
  infrastructure). Il bullet sui tetti di spesa tocca due provider di due sottosistemi, ma non
  risolve né U3 né U5: quelle stanno in `S2` e `S5`.
- **R-017** — otto edge pubblicati, tutti passano il test di sostituzione, nessuno nomina i due
  prerequisiti, e i quattro `—` sono righe che non costruiscono su niente di `NOW`. Due casi che
  sembrano edge mancanti e non lo sono: `S10` è `kind: release` e pubblica «the row its evidence
  enters through» (`S8`) invece di un edge per capacità toccata; e il bullet di `S8` che guarda la
  ricerca è una clausola che arriva a valle su una prova che sta in piedi da sola — ordine, non
  dipendenza. Entrambe le letture sono scritte in `drawing-the-map.md` § *Hard dependencies*.
- **R-019** — `S2`: `kind: spike`, `Audience` `—`, dipendente (`S6`), nessun timebox.
- **R-021** — vedi la nota sul rule set più sotto: l'unico `enabler` della mappa è la riga repository
  che R-011 impone, e il suo contenuto (conti e segreti che il resto della mappa spende) è alla
  lettera quello che `drawing-the-map.md` § *The two prerequisites* le assegna. Nessun rilievo, ma il
  check non è stato messo alla prova.
- **R-022** — le due righe `needs-decision` differiscono davvero: `S0` scrive «presso il provider
  scelto» e «del database scelto», `S5` scrive «un modello cheap con output strutturato» e misura il
  costo invece di nominare un fornitore.
- **R-023** — nessuna delle sei forme nominate. In particolare non *deferred safety*: le letture sono
  scoped da `S3`, e sostituire uno scope configurato con uno autenticato a un seam dichiarato è
  esplicitamente escluso dalla forma.
- **R-025** — sette candidati, nessun id, nessuna colonna, nessun documento, tutti fuori dal goal
  dichiarato e non semplicemente non finiti.
- **R-026** — quattro esclusioni, tutte nella forma della licenza: *perché non c'è X*, *cosa
  l'implementazione può quindi non fare*, *il prezzo*.
- **R-032** — niente in piedi, mappa scritta subito, nessuna conferma chiesta, e i file giù in blocco
  (idx 69→98) senza domande in mezzo.
- **R-033** — validator dopo la scrittura, `ERROR` corretti e ri-eseguito, e il `WARNING` — che non
  c'era — riportato come assente.
- **R-036** — `Write` di `log.md` a idx 69, `Write` di `roadmap.md` a idx 74. L'ordine regge, ed è
  l'ordine che è tutta la ragione per cui il log esiste.
- **R-037** — nessuna etichetta `Theme boundaries` e nessun bullet di forma coppia-e-verdetto in
  `roadmap.md`.

---

## 3. Contro il riferimento

Non è un target di diff. Quattro righe di differenza (11 contro 15), temi diversi, id diversi: N6
licenzia il conteggio. Quello che il riferimento fa trovare:

**La derivazione di tag e tempo è una riga intera nel riferimento** (`S13`, `enabler`, dipendente da
`S8` e `S9`). È la conferma indipendente del rilievo R-024 sopra: il riferimento le dà un
proprietario, il candidato la fa sparire in un `Excludes`. Ragione migliore: il riferimento, e non
perché sia una riga — perché `goal.md` fa poggiare il rinvio dei filtri sulla popolazione automatica
dei campi, e il candidato eredita il rinvio senza la popolazione che lo rende gratuito.

**Il differenziatore prima di tutto, su dati seminati** (riferimento: `S3` indicizzazione e `S4`
ricerca prima di qualunque modo di aggiungere una ricetta; candidato: `S6` in settima posizione,
dopo `S3`/`S4`/`S5`). Due clausole della skill tirano in direzioni opposte e ognuna delle due mappe
ne segue una: il riferimento *the cheapest real input that can validate a risky engine*, il candidato
*a row that opens a pipeline or adapter shared by several paths follows every `NOW` row that feeds
it*. Il candidato paga il rischio esistenziale con lo spike `S2` in terza posizione, misurato sul
Postgres di staging e non su un mock, e `S6` mette nero su bianco cosa fare se i due numeri
divergono («se qui è molto peggio, il colpevole è l'integrazione e non il modello»). Nessuna delle
due ragioni batte l'altra; la differenza è reale e va registrata come tale.

**Consultazione separata da inserimento manuale** (riferimento: temi `consultazione` e
`inserimento-manuale`, `S5` e `S7`; candidato: un solo tema `ricettario`, `S3`). Il riferimento può
separarli perché il corpus seme di `S3` resta nell'app e dà a `S5` qualcosa da sfogliare. Nel
candidato il corpus seme muore con lo spike (`S2` `Excludes`: la tabella si droppa), quindi senza
scrittura a mano non c'è niente da elencare e il test di split non passa. Data la sua sequenza, il
merge del candidato regge: la ragione è sua.

**Fallback LLM e copia-incolla: due righe o una** (riferimento `S9` + `S10`, candidato `S5`). Il
riferimento le tiene apart per learning target e audience diversi. Il candidato ha già messo il miss
rate del JSON-LD in `S4`, quindi a `S5` resta una sola domanda — il modello cheap estrae bene e a
frazioni di cent — e due ingressi nella stessa pipeline, che `slice-rules.md` § *Cohesion that holds*
nomina per esteso come motivo per stare in una riga. Ragione adeguata da entrambe le parti.

**Dove vive U1** (riferimento: su `S1`, che è `needs-decision`; candidato: su `S0`, che è
`needs-decision`, con `S1` `ready`). A1 dice «it blocks the skeleton alone». Nel candidato `S0` apre
il conto e crea il database, quindi la decisione va presa lì e non una riga dopo — e siccome `S0`
precede `S1`, quando `S1` viene presa in mano la decisione esiste. Ragione almeno pari, forse
migliore: la readiness segna la riga che il buco blocca davvero per prima.

**Copertina della ricetta** — il riferimento la esclude da `S11` e la lascia da ammettere dopo, il
candidato la tiene dentro `S9`. A6 licenzia entrambe alla lettera. Nessun rilievo.

**Accessibilità fra i `Cross-functional concerns`** — il riferimento porta «i campi obbligatori non
si marcano, si marcano gli opzionali»; il candidato non ha una dimensione accessibilità e mette la
stessa convenzione dentro `S3` `Includes` («tempo e tag sono editabili e marcati come opzionali, mai
richiesti»). La skill dice che una dimensione in cui lo sweep non trova niente non porta riga, e che
un'aspettativa ripetuta su più righe si scrive una volta sola nella sezione: qui la convenzione si
ripete su `S3`, `S4`, `S5` e `S9`, quindi la ragione migliore è del riferimento. Nessuna regola del
set copre questo, quindi non entra nel tally.

**Domande aperte diverse.** Il riferimento chiede cosa succede quando l'estrazione fallisce del tutto
e se una ricetta si sposti fra ricettari; il candidato chiede il tetto di aggiunte per utente e
l'uscita da un ricettario. La prima del riferimento il candidato la *decide* — «ciò che non valida
contro lo schema non viene salvato» in `Cross-functional concerns` → Validazione, e `S5`
`Verification` — ma la decide dove un lettore la trova, non in un bullet di riga: è una scelta
riportata, non silenziosa. Nessun rilievo; sono quattro buchi diversi, tutti reali.

---

## Nota sul rule set, non sulla mappa

R-021 chiede a ogni `kind: enabler` un percorso di produzione end-to-end reale. R-011 impone la riga
repository, che per costruzione non ne ha uno — `drawing-the-map.md` le dice esplicitamente «No
provisioning, no deploy» — e la tassonomia di `kind` non le lascia altra casella che `enabler`. Sulle
carte greenfield senza altri enabler, come questa, R-021 è vero alla lettera contro una riga che la
skill obbliga a scrivere. È il terzo caso del preambolo — una clausola che dice due cose che si
sovrappongono, che si legge come un difetto del modello — e la decisione su cosa cambiare non è di
questo report.

---

## Tally

Check ammessi da questa carta: le regole più le righe `H` del brief. Un check è rosso se almeno un
rilievo gli sta contro, per quanti convergano; i rilievi C e U contano una volta sotto la regola che
istanziano (C1 → R-015); le voci A e N non si contano.

- **Verdi (30)** — H1, H2, H3, H4, H5, H6, H7, H8, R-001, R-002, R-007, R-008, R-009, R-010, R-011,
  R-012, R-013, R-014, R-016, R-017, R-019, R-021, R-022, R-023, R-025, R-026, R-032, R-033, R-036,
  R-037
- **Rossi (4)** — R-015, R-020, R-024, R-035
- **Inconclusive (0)** — nessuno: il transcript c'è e copre R-001, R-032, R-033, R-035 e R-036
- **Non applicabili o saltati (12)** — R-003, R-004, R-005, R-034 (non applicabili); R-006, R-018,
  R-027, R-028, R-029, R-030, R-031, R-038 (saltati)

**Pass rate: 30/34 = 88%.** Rule set: `3fc02930f77c60b7e6fc25a2fd02e0ec799110df`.

Il numero è una linea di tendenza fra run della stessa carta sullo stesso rule set, non un verdetto
sulla mappa: il giudizio resta per check, su due run.
