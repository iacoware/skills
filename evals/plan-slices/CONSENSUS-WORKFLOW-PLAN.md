# Ciclo di consenso — piano di implementazione

Piano per separare il ciclo di consenso dal grading system abbandonato e automatizzarlo. Ogni fase è
pensata per una **sessione fredda separata**: dichiara le proprie precondizioni, le attività, come si
verifica e cosa produce. Una fase non presume il contesto conversazionale in cui la precedente è
stata svolta.

Lo strumento e la sua ragione stanno in `CONSENSUS-WORKFLOW.md`; qui c'è solo il lavoro da fare.

Le fasi chiuse sono uscite da questo file il 2026-08-06 e stanno in `CONSENSUS-WORKFLOW-PLAN-CLOSED.md`
con la loro cronaca. Non serve aprirlo per lavorare: ciò che le fasi aperte usano è ripetuto dove
serve.

## Rotta

Cosa aprire, per fase. Una sessione legge questa tabella, le *Decisioni già prese* e la propria fase.

| Fase | Stato | Oltre a questo file, apri |
|---|---|---|
| 0a, 0, 0c, 1a | **chiuse** — `f659c8b`, `f659c8b`, `88a4e9b`, `278edfd` | `CONSENSUS-WORKFLOW-PLAN-CLOSED.md`, solo per sapere *perché* |
| 0d — split dei documenti | **chiusa** — 2026-08-06 | come sopra |
| 0b — conversione | aperta, senza dipendenze | i documenti da convertire |
| 1b-i — prompt | **chiusa** — 2026-08-06 | `prompts/`, che è il record |
| 1b-ii — mappa generatori | **chiusa** — 2026-08-07 | `support/AGENT-PLAN-MAP.md`, che è il record |
| 1c — registro, mappa e report | **chiusa** — 2026-08-07 | `assets/report-template.md`, `support/CLAUSE-ROW-MAP.md` e `REGRESSION-LEDGER.md`, che sono il record |
| **2 — CON-6** | **aperta** — S1, S2 e S2b chiuse 2026-08-07; i due `IMPROVEMENT` sono conformi, 4 e 7 voci; **S3 è preparata** — payload, proiezioni e prompt resi — e restano le sue **5 chiamate**, con autorizzazione propria | `prompts/`, `assets/`, `../AGENTS.md`, `support/AGENT-PLAN-MAP.md` |
| 2b, 4 | aperte, dopo CON-6 | `recipe-app/EVALUATION-BRIEF.md` (2b); `support/CLAUSE-ROW-MAP.md` (4) |
| 3, 5, 6, 7 | aperte, codice | `scripts/`, `Makefile` |

## Decisioni già prese

Non si ridiscutono all'inizio di ogni sessione.

- L'obiettivo si regge su **due meccanismi disgiunti**: il registro rileva il peggioramento ex-post
  sulle dimensioni che copre; l'intersezione `improve` + `review` previene ex-ante l'ingresso di
  regole false. Una falsificazione dell'ipotesi sull'intersezione **non fa cadere l'obiettivo**.
- Il ciclo attivo si chiama **consenso**. Le fasi sono **quattro**: `improve`, `review`, `verdetto`,
  `recidiva`. `ledger` indica solo il registro, mai una fase.
- Il grading system è **abbandonato dal 2026-08-06**, non sospeso. Non torna. Il codice resta in git e
  non è mantenuto. **Non si spende tempo a curarne i documenti interni.**
- Dal ciclo CON-6 i payload di `improve` **e di `review`** sono **ciechi e simmetrici**.
- Il ciclo è un **falsificatore, non un confermatore**. Lo stato del registro è `non smentita ×k`.
  Non si aumenta il numero di generazioni per lato: la leva è il tempo, non il campione.
- **`improve` è bidirezionale**, con i campi `Regola esistente che non ha impedito il difetto` e
  `Costo`, e con la regola dura: se una clausola esistente è nominata, il rimedio di default è
  riformularla, e aggiungere righe richiede una ragione scritta.
- **Il contratto di conformità è un template più un validator**, non prosa dentro un prompt: un
  contratto in prosa è ciò che entrambi i lati hanno ignorato in CON-4. La specificità è una **forma**
  che il generico non riempie, non un giudizio con una soglia. **Niente soglie.** Una voce non
  conforme si **scarta e si registra**, con **un solo tentativo**, e un lato a zero voci conformi non
  blocca il ciclo. Forma, scarto, codice di uscita e cosa il gate *non* misura stanno in
  `workflow/CONFORMANCE.md` e in `assets/improvement-template.md`; qui non si duplicano.
- **`Origine` ha quattro valori**: `intersezione`, `intersezione-tema`, `giudizio`, `potatura`.
  **I nomi canonici sono inglesi** dal 2026-08-06, perché li scrivono il registro migrato, i prompt e
  il validator: `intersection`, `intersection-theme`, `judgement`, `pruning`. Stessa cosa per
  `Verifica`: `validator` e `reading`. I termini italiani di questo piano, di
  `CONSENSUS-WORKFLOW.md` e di `workflow/` restano leggibili finché la Fase 0b non li converte, e la
  mappa fra i due
  insiemi è dichiarata nelle regole d'uso del registro. Prompt e validator non emettono mai gli
  italiani.
- **Una voce che tocca una clausola coperta o ri-ancora la riga, o la assorbe** — due regole, non
  una, perché **le righe quantificano su un piano generato, non sul testo dello skill**. Ne discende
  che una riformulazione **non falsifica** la riga: rompe l'attribuzione. Testo che cambia a portata
  invariata → ri-ancoraggio, automatico; portata che cambia → assorbimento, e un'affermazione **esce**
  dal registro. Regole, vincoli e cronaca degli assorbimenti già fatti vivono in
  `REGRESSION-LEDGER.md` § *Re-anchoring and absorption* e nelle celle `Absorbs`; qui non si
  duplicano. Ciò che va saputo senza aprirle: **una riga = una affermazione** è regola di scrittura
  dal 2026-08-06, l'assorbimento è **la sola mossa che toglie una previsione**, e il ciclo che ne
  emette uno lo mette in cima a ciò che il veto rilegge.
- **Una voce vale `intersezione` o `intersezione-tema` solo se entrambi i `REVIEW` la classificano
  condivisa.** Classificazione unilaterale → `giudizio`, e nessuna applicazione automatica.
- **Il workflow applica al working tree e non committa mai.** Applica solo ciò che il filtro
  licenzia. Una voce = un hunk di `SKILL.md` + una riga di registro, stesso id, riga con
  `Commit: (pending)`. Il veto umano legge i **contatori in testa al report**, poi `git diff`.
- **`recidiva` è una chiamata sola**, modello fisso `claude-opus-5`, e produce l'**elenco delle
  coppie** `voce improve → riga | nessuna`, non uno scalare. Controargomento ed eventi di inversione
  sono in `workflow/LEDGER.md` § *Perché `recidiva` è una sola chiamata*.
- **Dormienza a `non smentita ×3`**, verifica 1 ciclo su 3, risveglio immediato da `recidiva`.
  Sostituisce il pensionamento, che era rinviato senza trigger osservabile.
- I prompt escono da `PROMPTS.md` e diventano l'unica sorgente sotto `prompts/`; `PROMPTS.md` resta
  scratchpad umano senza valore normativo.
- `support/AGENT-PLAN-MAP.md` tiene le due mappe alias → artefatto e il generatore di ciascuno, ed è
  escluso da ogni payload.
- `CON-N` resta il contatore di ciclo negli artefatti; non si rinominano artefatti storici. **CON-5
  non si riusa.** Il prossimo ciclo è **CON-6**.
- **Modelli: `gpt-5.6-sol` e `claude-opus-5`.** L'**effort è due variabili, non una**, e la decisione
  che le teneva insieme — «entrambi a `high` in CON-6» — è stata splittata alla chiusura di S1, dopo
  che i due candidati sono nati a `medium` su entrambi i lati. **La generazione di CON-6 è a
  `medium`**, registrata e non rigenerata; **le quattro fasi del ciclo restano a `high`**, perché è
  lì che vive la variabile testata — la specificità degli `IMPROVEMENT` — e cambiarle nello stesso
  ciclo la confonderebbe con una scelta di costo indipendente. `medium` sulle fasi è il confine
  isolato in **CON-7**. Le ragioni per non rigenerare stanno in `support/AGENT-PLAN-MAP.md` § CON-6.
- **La lingua dei candidati non è decisa qui.** La decide `SKILL.md`, che scrive il contenuto nella
  lingua dell'utente e la struttura in quella del template: i piani CON-6 sono in **italiano** con
  heading inglesi, e la regola «ogni nuovo artefatto nasce in inglese» non li raggiunge, perché la
  loro lingua è l'effetto di una clausola **sotto test**, non una scelta editoriale.
- **La revisione di `EVALUATION-BRIEF.md` sta dopo CON-6**, per la stessa ragione: è l'autorità contro
  cui si decidono quattordici righe su diciassette.
- **L'inglese è la lingua del progetto dal 2026-08-06.** Le fonti in `recipe-app/sources/` e gli
  artefatti storici — `PLAN-*`, `IMPROVEMENT`, `REVIEW`, report — **non si convertono mai**.
- Un confine di strumento **si attraversa una volta sola, deliberatamente, e si registra.**
- La decisione su cosa applicare allo `SKILL.md` resta umana in ogni fase, in forma di veto.
- **Le 15 unità di calibrazione già pagate non vanno conservate.** I 30 file sono tracciati in git.

## Fase 0b — Conversione dei documenti umani

**Precondizioni:** Fase 0a. **Chiamate provider:** zero. **Nessuna fase dipende da questa.**

Documenti che nessun modello legge durante un ciclo. La conversione è lavoro bruto senza rischio e
senza dipendenze: può stare per ultima, o essere fatta a pezzi, o slittare indefinitamente.

- [ ] `CONSENSUS-WORKFLOW.md`, i cinque file di `workflow/`, `CONSENSUS-WORKFLOW-PLAN.md`,
  `CONSENSUS-WORKFLOW-PLAN-CLOSED.md`, `NOTES.md`, `PROMPTS.md`. Dopo la Fase 0d sono unità
  indipendenti: si converte un file per volta, senza attraversare tutto il documento.
- [ ] Non toccare i documenti di grading: sono archivio.

**Verifica:** i documenti convertiti non citano artefatti con nomi diversi da quelli reali; le
citazioni testuali dagli artefatti storici restano **in italiano fra virgolette**, perché sono prove.

## Fase 2 — Ciclo CON-6 manuale

**Precondizioni:** Fasi 0c, 1a, 1b-i, 1b-ii, 1c. `0c` è esplicita e non solo transitiva: un ciclo eseguito su
righe multi-affermazione produce verdetti che lo split dovrebbe poi disaggregare a posteriori.
**Chiamate provider:** **9** in un ciclo che non ripete — 2 generazione, 2 `improve`,
2 `review`, 2 `verdetto`, 1 `recidiva`. CON-6 ne spende **11**: le due `improve` del primo S2 sono
state scartate al gate per un difetto del payload, e la ripetizione è S2b. Effort **`high` sulle sette chiamate delle fasi**; le due di
generazione sono già state fatte, a `medium`. Richiede **autorizzazione esplicita** dopo
il dry-run e il conteggio, per `evals/AGENTS.md`, **una per sessione** e non una per la fase.

I piani CON-5 **non si riusano**: esistevano già il 2026-08-02 alle 17:03 — `support/AGENT-PLAN-MAP.md`
§ *When each artifact was generated* — mentre `87150d3` è delle 23:11 del 2026-08-04 e `eb926bb` delle
23:30. Precedono entrambi i commit, quindi non possono verificare `R-010` e `R-011`. Le 11:57 del
2026-08-04 che questo piano portava prima sono l'ora del commit `515e0a3`, non della generazione: il
divario è più largo, non più stretto.

### Quattro sessioni, non una

La fase **non si esegue in una sessione sola**, e non per comodità. Tre vincoli la tagliano da sé:

- **La sessione di regia non può essere una delle nove.** Ogni esecuzione riceve un payload da
  allowlist; una sessione che ha già letto i piani con i nomi reali, le due assegnazioni alias e il
  registro non può poi *essere* l'`improve` o il `review` senza rompere cecità e allowlist insieme.
- **Metà delle esecuzioni non parte da qui.** `CX` è Codex CLI — `support/AGENT-PLAN-MAP.md` — quindi
  le quattro esecuzioni di quel lato le lancia l'umano altrove e lo stato passa comunque per il
  filesystem. *Assunzione dichiarata:* CON-6 resta in **sessioni interattive** su entrambi i lati,
  come CON-1…CON-5; la modalità headless è la Fase 6 ed è un confine di strumento a sé.
- **Il gate è un punto di decisione che cambia la rotta a metà.** Uno dei tre esiti dice di
  **fermarsi e ripetere**; una sessione che ha già lanciato `review` ha speso due chiamate su un ramo
  da abbandonare.

L'autorizzazione di `evals/AGENTS.md` si chiede **per sessione**, con il conteggio di quella
sessione — 2, 2, 5 — mai una volta sola per nove: un'autorizzazione unica coprirebbe anche il ramo in
cui S2 dice di fermarsi.

**S1 — generazione. 2 chiamate. Chiusa il 2026-08-07.**

- [x] Assegnare `CANDIDATE-A`/`CANDIDATE-B` ai due lati e `REPORT-A`/`REPORT-B` ai due `IMPROVEMENT`
  che nasceranno. **Le due assegnazioni non devono coincidere.** `CANDIDATE-A` = `CX`,
  `CANDIDATE-B` = `CC`, `REPORT-A` = `CC`, `REPORT-B` = `CX`.
- [x] Scrivere la riga di `support/AGENT-PLAN-MAP.md` — harness, modalità, modello, effort —
  **prima** della chiamata. È l'unico momento in cui `gen` si registra senza ricostruirlo.
- [x] Correggere il prompt di generazione, che non attivava più lo skill: da `3658187`
  `disable-model-invocation: true` e `allow_implicit_invocation: false`, quindi senza `/plan-slices`
  e `$plan-slices` i candidati nascevano **senza lo skill**. I due prompt da inviare sono in
  `PROMPTS.md` § `GENERATE PLAN`, il confine in `workflow/CYCLE.md`.
- [x] Generare i due candidati dallo `SKILL.md` corrente — `28b5460` — e dalle sole fonti. Le due
  sessioni le lancia l'umano, una per lato, nuove e senza altro contesto.
- [x] `make validate PLAN=PLAN-CC-CON-6.md` e `PLAN=PLAN-CX-CON-6.md`. Verdi entrambi, quindi lo
  skill era attivo su entrambi i lati: la correzione del prompt ha tenuto.
- [x] Nessuno dei due cita un piano precedente o un artefatto sotto `results/`. L'allowlist del
  prompt è scritta, non imposta, e ha retto.

**I due scostamenti di S1, per il report S4.** Nessuno dei due ha fatto rigenerare; entrambi sono
simmetrici sui due lati, ed è la simmetria a renderli innocui per ciò che il ciclo misura.

1. **Effort `medium` invece di `high` in generazione.** Registrato correggendo le due celle di
   `support/AGENT-PLAN-MAP.md` — una riga `declared` sbagliata è peggio di `unrecorded` — e la
   decisione sull'effort qui sopra è stata splittata in due variabili. La conseguenza da tenere per
   S3: una **smentita** misurata su questi piani è ambigua fra skill ed effort e va letta con lo slot
   `gen` della riga che la registra; una **non smentita** no, perché l'effort minore è una condizione
   più dura.
2. **I piani sono in italiano**, non in inglese come questo blocco prevedeva. La previsione era
   sbagliata sullo skill, non sui piani: `SKILL.md:335` scrive nella lingua dell'utente e in inglese
   esce la sola struttura, che viene dal template. Un confine previsto che **non è stato
   attraversato**.

S2 è una sessione a sé e chiede la propria autorizzazione — 2 chiamate.

**S2 — `improve` e gate. 2 chiamate. Finisce con una decisione.**

- [x] Comporre i payload: candidati rinominati, più `CLAUSE-INDEX.md` e `LEDGER-CLAIMS.md` proiettati
  **a mano** dalla mappa e dal registro. Il produttore è Fase 5 e scriverlo qui sarebbe iniziarla da
  un'altra porta. **Verificare entrambe le proiezioni su un campione prima di inviare:** un indice
  sbagliato scarta al gate ogni voce che nomina una clausola, e il log si leggerebbe come «il modello
  non sa fare il lavoro» quando è un errore di payload. È il punto più fragile del ciclo.
  Il payload è una **directory** — `recipe-app/payloads/CON-6/improve/` — che contiene l'allowlist e
  nient'altro; i due prompt resi stanno un livello sopra, fuori dal payload. La verifica non è stata
  un campione: tutte e 200 le celle-sito dell'indice sono state date al gate nella forma in cui una
  voce le scriverebbe, e tutte e 200 passano con le righe che l'indice stampa. Ha trovato **due
  difetti, entrambi negli strumenti e nessuno nella mappa**, ed entrambi avrebbero scartato al gate
  voci corrette:
  1. **La proiezione `.tsv` copriva quattro clausole che la mappa dichiara scoperte.** `C-071`,
     `C-119`, `C-120` e `C-129` portano nella cella `Rows` la riga *candidata* che un ancoraggio
     `unresolved` ha **rifiutato**; `extract_clause_map.py` la leggeva come copertura, cioè risolveva
     nei record un fallimento che la mappa registra come fallimento. Le clausole coperte tornano da
     44 a **40**, il totale che la mappa dichiara.
  2. **Il gate rispondeva per tutte le clausole che un sito attraversa.** Una riga di `SKILL.md`
     porta spesso due clausole normative, quindi citare un sito **esattamente come l'indice lo
     stampa** faceva pretendere anche le righe delle clausole vicine: 36 siti su 205, fra cui i gate
     `Complete when` di § 5, dove vive metà del registro. Ora un sito che è **lo span esatto** di una
     clausola risponde per quella sola, e l'unione resta la risposta per un sito che non coincide con
     nessuna. Resta un solo sito genuinamente ambiguo — `SKILL.md:369`, dove `C-171` e `C-172`
     condividono la riga — e l'indice lo stampa una volta con l'unione, che è ciò che il gate chiede.
- [x] Eseguire `improve` sui due lati, copiando `prompts/improve.prompt.md`. **Verificare l'effort
  `high` nella sessione prima di inviare:** è la cella che S1 ha sbagliato dichiarandola senza
  guardarla. Fatto a `high` su entrambi i lati, verificato in sessione.
- [x] `make validate-improvement` su entrambi, e conservare il log degli scarti per voce e campo.
  `REPORT-A` **5 conformi su 5**; `REPORT-B` **0 su 3**, e i tre scarti portano lo stesso campo e lo
  stesso messaggio: ``` `Clause` must name its section as § `section title` ```.
- [x] **Scegliere il ramo** fra i tre esiti qui sotto. Il ramo «si corregge il campo e si ripete»
  torna a S2, non prosegue. **È il ramo scelto**, e non per il conteggio: per la concentrazione degli
  scarti su un campo solo.

**Perché il primo tentativo non conta come dato sulla tesi.** Il difetto è il terzo degli strumenti trovato a S2,
e come i due della composizione del payload avrebbe scartato voci corrette.
`CLAUSE-INDEX.md` stampava i titoli numerati come `## § 1 …` mentre il template chiede `§ ` più il
titolo *come marcatore del campo*: la forma conforme era un `§` doppio. Un lato l'ha scritta, l'altro
ha assorbito il marcatore nel titolo ed è caduto per intero. Le tre voci di `REPORT-B` nominano sito,
sezione e citazione **correttamente**: rimettendo il solo separatore, tutte e tre passano — verificato
su copia in scratchpad, senza toccare l'artefatto. Un conteggio 5 contro 0 letto come specificità
comparata direbbe una cosa che il gate non ha misurato.

**Correzione applicata, e il suo confine.** L'indice stampa quei titoli **senza** `§` e dichiara la
regola del campo; il template resta com'è. Nessuna cella della mappa né del `.tsv` cambia, e il gate
non legge l'indice: la correzione è nel payload, cioè in ciò che il modello legge. `_comparable`
toglie `§` da entrambi i lati del confronto, quindi **entrambe le forme restano accettate** — le
cinque voci conformi di `REPORT-A` rivalidano verdi con l'indice nuovo, e tutti e dieci i titoli
dell'indice risolvono a una sezione del `.tsv`. I due `IMPROVEMENT` scartati stanno in
`recipe-app/payloads/CON-6/discarded/attempt-1/`, perché sono la prova di questa lettura — **fuori
da `out/`**, che è la sola directory in cui le due esecuzioni scrivono: lasciarveli avrebbe messo
l'output del primo tentativo a un `ls` dalla sessione che ripete.

**S2b — ripetizione. 2 chiamate, autorizzazione propria.**

- [x] Ripetere `improve` sui due lati **alla stessa configurazione** — `high`, stessi modelli, stesse
  assegnazioni alias — con il payload corretto. È il vincolo di riga «un S2 ripetuto si ripete alla
  stessa configurazione»: l'unica variabile che cambia è l'indice. Il payload è stato verificato prima
  delle chiamate — `support/AGENT-PLAN-MAP.md` § CON-6: le 204 forme-sito che l'indice corretto induce
  passano tutte il gate, `out/` era vuota, e il primo tentativo è stato spostato fuori di lì.
- [x] `make validate-improvement` su entrambi, log degli scarti conservato.
- [x] Riscegliere il ramo. **`REPORT-A` 4 su 4, `REPORT-B` 0 su 7 e poi 7 su 7** dopo la correzione
  descritta qui sotto: entrambi i lati operativi, S3 parte.

**L'indice era il difetto giusto, e ne è emerso un quarto.** Il campo `Clause` non ha scartato più
niente, su nessuno dei due lati: la lettura di S2 ha retto e non va rifatta. Ma `REPORT-B` è caduto
di nuovo per intero, su un campo diverso — le due celle `Evidence`, tutte e sette le voci, stesso
motivo. `CX` cita gli insiemi di siti in una cella sola — `CANDIDATE-A.md:149-153,351-355` — e
`LINE_REFERENCE_PATTERN` accettava un intervallo solo. Non è un caso limite ma la convenzione
costante di quel lato: **10 celle su 10** con riferimento diretto la usano, contro **0 su 7** di
`CC`. Spezzando i soli riferimenti in un bullet per intervallo, verificato su copia in scratchpad,
tutte e sette passavano già prima della correzione.

**Il difetto stava nel validator, non nel payload, ed è ciò che ha deciso il ramo.** Il template
elenca *esempi* di riferimento localizzabile e non dice «uno solo per cella»: la restrizione viveva
solo nel controllo. `workflow/CONFORMANCE.md` § *La specificità è una forma* dichiara che quella cella
esiste per escludere **il bullet generico**, e due siti citati sono più specifici di uno. E il gate
leggeva comunque **solo il primo bullet** di ogni cella, quindi «due siti in due bullet» passava già
con il secondo mai verificato: accettare la lista **e risolvere ogni intervallo** stringe il gate
invece di allentarlo. Poiché ciò che i due modelli hanno letto non cambia, non c'era niente da
rigenerare — a differenza di S2b, dove l'indice difettoso stava **dentro** il payload. Quindi
correzione del validator, un test per la lista e uno per lo span fuori intervallo in mezzo alla lista,
e rivalidazione degli artefatti già prodotti: **zero chiamate**.

**Il confine di questa correzione, dichiarato.** È stata decisa **a risultato noto**, cioè sapendo
quale lato cadeva, ed è il terzo aggiustamento di strumento in due tentativi. Ciò che la tiene
onesta e che va riletto se un giorno sembra comoda: non tocca nessun altro campo, rende il controllo
più severo e non più permissivo, e il template è stato corretto **solo alla sorgente** —
`assets/improvement-template.md` — mentre la copia dentro `recipe-app/payloads/CON-6/improve/assets/`
resta com'era, perché è la prova di ciò che i due lati hanno effettivamente letto.

**Conseguenza per il report S4, e non è piccola.** Il conteggio `4` contro `7` **non è specificità
comparata pulita**: il gate è stato corretto due volte dentro S2, e le voci di `REPORT-B` sono state
lette sotto una regola resa esplicita dopo essere state scritte. Il ciclo dice che entrambi i lati
producono voci ancorate — non dice quanto bene, e non va scritto come se lo dicesse.

**S3 — `review`, `verdetto`, `recidiva`. 5 chiamate.**

- [x] I tre payload sono disgiunti e le esecuzioni indipendenti: `review` legge i due `IMPROVEMENT`
  conformi, `verdetto` i due candidati più le righe attive, `recidiva` i due `IMPROVEMENT` più tutte
  le righe, dormienti incluse. Composti il 2026-08-07 come tre directory —
  `recipe-app/payloads/CON-6/{review,verdict,recidiva}/` — ciascuna esattamente l'allowlist del suo
  prompt.
- [x] Le righe dormienti entrano 1 ciclo su 3; a CON-6 non ce ne sono, e se ce ne fossero si dichiara
  perché entrano o no. **Diciassette attive, zero dormienti**: i due file portano gli stessi 17 id, e
  la regola non morde in questo ciclo.
- [ ] Ogni cella `Misurato su` scritta da questo ciclo porta `gen claude-opus-5 medium + gpt-5.6-sol
  medium`. È il primo ciclo in cui lo slot `gen` dice qualcosa, ed è `medium` perché lo è stata la
  generazione, non perché lo siano le chiamate di questa sessione.
- [ ] Eseguire le cinque chiamate a `high`, due per `review`, due per `verdetto`, una per `recidiva`
  su `CC` a modello fisso. I cinque prompt resi stanno un livello sopra i payload, come a S2. Le
  quattro directory di output — una per fase e per lato — sono vuote prima delle chiamate; nessuna
  esecuzione scrive in `out/`, dove stanno i due `IMPROVEMENT` con i nomi veri.

**Cosa la preparazione ha verificato, e cosa ha deciso.** Zero chiamate; il dettaglio sta in
`support/AGENT-PLAN-MAP.md` § *decided at S3*, che è il record, e qui c'è solo ciò che serve a
rileggere il ciclo.

- **Le due proiezioni sono verbatim.** I 17 claim di `LEDGER-ROWS.md` e di `ROWS.md` sono stati
  estratti dal registro e confrontati cella per cella: identici, senza stato, contatore, origine né
  provenienza. È l'analogo della verifica che a S2 ha trovato tre difetti negli strumenti, sull'unico
  punto in cui questa fase ha un payload derivato.
- **Le celle `Watch for` sono una proiezione, non una copia.** Quattro righe ne portano una: `R-011`
  entra intera, `R-010` senza la frase che nomina un harness e ripercorre la storia della riga,
  `R-016` senza il rimando a `support/`, `R-015` non entra affatto — la sua nota parla della
  provenienza della riga e della decisione di Fase 4, non di un piano generato. È una decisione
  editoriale presa **a risultato ignoto** e registrata perché cambia ciò che due delle cinque
  esecuzioni leggono.
- **Un difetto del prompt `recidiva`, corretto prima delle chiamate.** Vietava qualunque conteggio
  «anywhere» mentre la sua stessa struttura di output ne chiede tre. Il divieto ora nomina ciò per cui
  esiste: le coppie. È il quarto aggiustamento di strumento del ciclo ed è il primo deciso senza
  sapere cosa produrrà nessuno dei due lati.
- **Le due righe `VERDICTS` entrano nel formato della mappa**, con alias `—`: CON-6 è il primo ciclo
  i cui verdetti nascono da una chiamata invece che da lettura umana offline, e senza quelle righe il
  quinto slot di `Misurato su` nominerebbe uno strumento di cui nessuno registra modello ed effort.

**S4 — report, applicazione, veto. Zero chiamate.**

- [ ] Scrivere `CONSENSUS-CON-6.REPORT.md` nella forma di `assets/report-template.md`, contatori in
  testa. È la prima istanza del template: ogni punto in cui non regge si corregge **nel template**,
  non nel report.
- [ ] Applicare le sole voci che il filtro licenzia, una riga di registro per voce, `Commit:
  (pending)`. **Non committare dal workflow.** Leggere i contatori, poi `git diff`, poi decidere.
- [ ] Correggere `prompts/`, `assets/`, `CONSENSUS-WORKFLOW.md` e `workflow/` dove la procedura non
  ha retto, e annotare ogni scostamento nella sezione che il report ha per questo.

**Verifica — due criteri distinti, ed è il secondo quello che conta:**

1. *Completamento.* Il ciclo si chiude producendo tutti gli artefatti previsti senza intervento non
   documentato. Ogni scostamento è annotato.
2. *Validità della tesi.* I due `IMPROVEMENT` hanno **specificità comparabile**, misurata in modo
   descrittivo: quante voci sopravvivono al gate per lato. Nessuna soglia — un ciclo non emette un
   verdetto su un'ipotesi, coerentemente con `non smentita ×k`.

**Cosa si fa in ciascuno dei tre esiti — deciso prima di eseguire:**

- **Un lato a ~0 voci operative.** Decide il log degli scarti. Scarti concentrati **tutti sullo stesso
  campo** → il template è scritto male, si corregge quel campo e si ripete. Scarti **sparsi** → il
  modello non sa fare il lavoro, l'ipotesi prende una smentita `×1`, la Fase 5 non parte e si decide a
  CON-7.
- **Entrambi operativi, voci condivise con lo stesso rimedio.** `Origine: intersezione`, applicazione
  automatica.
- **Entrambi operativi, stesso tema e rimedi diversi.** `Origine: intersezione-tema`: il tema porta
  l'evidenza d'intersezione, la formulazione viene dal lato che la fornisce ed è decisa dall'umano.
  Non è una ritirata: è la classificazione per voce di ciò che è già successo in CON-4, e mantiene
  `review` portante — è la fase che separa questo esito dal precedente.

**Fuori dal tavolo per CON-6:** cambiare uno dei due modelli. È un confine di strumento e renderebbe
il ciclo non interpretabile, per la stessa ragione per cui l'effort delle quattro fasi resta a
`high`. Vale anche per il ramo «si ripete»: un S2 ripetuto si ripete alla stessa configurazione.

**Output:** il ciclo eseguito, la procedura corretta, e il primo dato sulla tesi. È il gate delle
Fasi 2b, 4 e 5.

## Fase 2b — Revisione del brief

**Precondizioni:** Fase 2. **Chiamate provider:** zero; si verifica su CON-7.

Dopo CON-6, mai prima: `EVALUATION-BRIEF.md` è l'autorità contro cui si decidono sette righe su
diciassette — sono le righe che lo portano in `Misurato su` — e toccarlo prima del ciclo che verifica
per la prima volta `R-010` e `R-011` aggiungerebbe un
confine al verdetto.

- [ ] Verificare duplicazioni. Il file è 51 righe e già asciutto; il candidato reale non è ridondanza
  di token ma una **separazione di responsabilità sporca**: `Known conflicts`, secondo bullet,
  riscrive quasi verbatim la regola di `R-002` (*«no `Includes` or `Verification` bullet may assert
  either side»*), cioè mette una regola di scrittura del piano dentro il documento che descrive lo
  scenario. Il brief dovrebbe dichiarare il conflitto, non come si scrive il piano.
- [ ] Modularizzare solo se la lettura lo giustifica; non inseguire token che non ci sono.
- [ ] Registrare il confine in `Misurato su` per tutte le righe che citano il brief.

**Verifica:** CON-7. Le righe che citano il brief non cambiano verdetto per effetto della revisione;
se cambiano, il brief ha cambiato significato e la revisione va rifatta.

## Fase 3 — Riorganizzazione del codice

**Precondizioni:** Fase 0; indipendente dalla Fase 2, che non tocca codice. **Chiamate provider:**
zero.

L'ambizione di questa fase è stata **ridotta** il 2026-08-06: `scripts/runtime/` esisteva per ospitare
il codice *condiviso fra i due strumenti*. Con un solo strumento in servizio non c'è niente da
condividere.

- [ ] Spostare in `scripts/consensus/` **solo** ciò che il ciclo userà davvero: invocazione provider,
  hashing, scrittura atomica e resume, estratti da `grader_runtime.py` e `orchestrator_artifacts.py`.
  `validate_improvement.py` ci vive già dalla Fase 1a.
- [ ] Lasciare il resto del grading dov'è, come archivio, con i suoi test e i suoi target.
- [ ] Aggiornare import, test, `Makefile` e documentazione di ciò che è stato spostato.

**Verifica:** `make test` verde; nessun artefatto sotto `recipe-app/results/` modificato.

## Fase 4 — Modularizzazione e pruning dello skill

**Precondizioni:** Fase 2, e la mappa prodotta in Fase 1c. **Chiamate provider:** zero per la fase; la
verifica costa un ciclo (CON-7).

Va **dopo CON-6**, non prima. Potare prima significa scegliere cosa togliere in base a quanto una
clausola sembra ridondante leggendola, che è esattamente il tipo di giudizio che il ciclo esiste per
non fare. E anticipare la sola modularizzazione «tanto è neutra» è falso: sposta ciò che il modello ha
in contesto al momento di generare.

Stato di partenza: `SKILL.md` monolitico a **417 righe**, con tre rami d'ingresso — `Choose the
branch`, `Review an existing plan`, `Split, merge, or reorder an existing plan` — che caricano tutte e
417 comunque. La disclosure progressiva esiste già, ma solo per `assets/plan-template.md` e
`scripts/validate_plan.py`.

- [ ] Aggiornare la mappa clausola → riga prodotta in Fase 1c con ciò che CON-6 ha cambiato.
- [ ] Modularizzare per ramo d'ingresso, così che un ramo non caricato non occupi contesto.
- [ ] Potare e fondere. **Ogni rimozione è coperta o scoperta:** coperta → la riga di registro
  esistente si riscrive e la previsione resta; scoperta → nasce una riga `Origine: potatura` con
  l'affermazione «la rimozione di X non fa ricomparire il difetto Y». Nessuna rimozione senza una
  delle due.
- [ ] **Decidere i quattro ancoraggi `unresolved`** che la mappa registra come fallimenti. Dopo la
  Fase 0c due sono **righe intere** e si nominano per id — `R-001` e `R-015` — e due sono componenti
  `9aa2586` delle celle `Commit` di `R-005` e `R-006`, commit di cui nessuna affermazione rivendica
  una clausola. Per ciascuno una sola delle due mosse: lo skill acquista la clausola che la riga
  presuppone, oppure la riga si riscrive per smettere di pretendere ciò che lo skill non dice — per i
  due commit, la terza è toglierli dalla cella. È lavoro di questa fase perché è la stessa decisione
  della potatura letta al contrario — lì si toglie testo coperto da una riga, qui c'è una riga che
  copre testo inesistente. Il caso netto è `R-015`: il requisito è stato aggiunto a `R-006` dopo CON-5
  **perché** `CX` non dichiarava il riuso, quindi un verdetto contro quella riga sembra una
  regressione dello skill senza esserlo.
- [ ] Registrare il confine di strumento in `Misurato su` per tutte le righe attive.

**Verifica:** **CON-7**. La fase non si chiude quando lo `SKILL.md` è più corto: si chiude quando
CON-7 non ha smentito le righe di potatura, e nessuna riga attiva ha un ancoraggio `unresolved`.

## Fase 5 — Orchestratore del ciclo

**Precondizioni:** Fasi 2 e 3. **Chiamate provider:** 7 per ciclo dopo la generazione, dietro dry-run
e `CONFIRM_SEND`.

- [ ] `scripts/consensus/` con il comando che rende i prompt da `prompts/`, compone i payload ciechi
  da una allowlist esplicita, invoca i provider e scrive gli artefatti.
- [ ] Target `make consensus N=… PHASE=improve|review|verdict|recidiva|report`, con `DRY_RUN`,
  `RESUME`, `CONFIRM_SEND` e registrazione degli hash, del modello e dell'effort.
- [ ] **Il gate di conformità è `validate_improvement.py`**, invocato dalla fase: le voci non conformi
  cadono e finiscono nel log degli scarti, `review` parte comunque.
- [ ] **L'applicazione è codice:** una voce licenziata dal filtro produce un hunk di `SKILL.md` e una
  riga di registro con lo stesso id e `Commit: (pending)`. **Nessun commit.** Un target
  `make consensus-reject ID=…` toglie una voce sola, hunk e riga insieme.
- [ ] **Ri-ancoraggio e assorbimento sono codice, con confini diversi.** Una voce che riformula
  ri-ancora da sé le righe che dichiara coprenti: commit nuovo, `×0`, nessuna riscrittura. Una voce
  con `Merged claim` **non si applica da sé**: emette la riga fusa, l'`Absorbs` con le regressioni
  assorbite, e il diff che toglie le affermazioni sostituite — e passa all'elenco umano, perché è
  l'unica mossa del ciclo che fa **uscire** una previsione dal registro.
- [ ] **Emettere `Misurato su` in tutti e cinque gli slot**, quinto incluso: `verdict <strumento>`.
  Esiste perché i verdetti CON-5 vengono da lettura umana offline, e senza lo slot quel fatto sparisce
  al primo ciclo automatizzato — cioè esattamente ciò che la colonna esiste per non far sparire.
- [ ] Il join `report` è deterministico: nessuna chiamata, solo composizione degli artefatti prodotti.
  I contatori sono composizione; la **recidiva no** — è la fase 7, ed è per questo che esiste come
  fase invece che come calcolo del report.
- [ ] Test che nessun path sotto `support/` compaia in un prompt renderizzato.
- [ ] Test che il dry-run mostri esattamente le esecuzioni attese per fase e i target attesi.

**Verifica:** dry-run di tutte le fasi; un ciclo completo eseguito e ripreso con `RESUME=1` senza
nuove chiamate; confronto degli artefatti con quelli prodotti a mano nella Fase 2.

## Fase 6 — Generazione automatizzata

**Precondizioni:** Fase 5. **Chiamate provider:** 2 in più per ciclo.

- [ ] `PHASE=generate` produce i due candidati dalle sole fonti, con hash e resume, e aggiorna
  `support/AGENT-PLAN-MAP.md`.
- [ ] Annotare nel registro che lo strumento di generazione è cambiato: i piani CON-1…CON-N-1 nascono
  da sessioni interattive, non da chiamate headless. È un confine di strumento.

## Fase 7 — Intersezione deterministica, opzionale

**Precondizioni:** almeno due cicli completi in Fase 5. **Da decidere dopo, non ora.**

Far produrre alla fase `review` un output strutturato minimo — id, titolo, categoria, lato che porta
il rimedio — così che l'intersezione la calcoli il codice invece del modello.

La condizione di sblocco è ora **osservabile**: ogni report pubblica le voci classificate condivise
da un solo `REVIEW` — sezione *Classification instability* di `assets/report-template.md`. Prima la fase diceva «si valuta se due cicli mostrano che la
classificazione è instabile», ma niente misurava quell'instabilità, quindi la condizione non poteva
verificarsi.
