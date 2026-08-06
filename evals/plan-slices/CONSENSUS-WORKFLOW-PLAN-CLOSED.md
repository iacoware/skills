# Ciclo di consenso — fasi chiuse

Archivio delle fasi già svolte di `CONSENSUS-WORKFLOW-PLAN.md`. **Nessuna sessione ha bisogno di
aprire questo file per lavorare:** le regole che le fasi chiuse hanno prodotto vivono nei documenti
che le portano — template, validator, mappa, registro, `CONSENSUS-WORKFLOW.md` — e le fasi aperte
ripetono per esteso i fatti che usano, invece di rimandare qui.

Si apre per una sola domanda: **perché una decisione è stata presa così.** Ciò che sta qui è cronaca
e ragione; ciò che è normativo sta altrove, e dove le due copie divergessero **vince il record**, mai
questo file.

Lingua: italiano come il piano da cui è estratto. La Fase 0b lo converte insieme agli altri.

## Fase 0a — L'inglese è la lingua del progetto

**Precondizioni:** nessuna. **Chiamate provider:** zero. **Andava per prima.**

**Fatta il 2026-08-06.** La regola, le due esclusioni permanenti con la loro ragione e la nota su
`EVALUATION-BRIEF.md` e `SKILL.md` vivono in `README.md` § *Language*, che è il record; qui non si
duplicano. La copia italiana che `CONSENSUS-WORKFLOW.md` ne portava è stata ridotta a un puntatore
nella Fase 0d.

La conversione dei documenti esistenti è Fase 0b e non blocca niente; separarle è ciò che evita di
scrivere in italiano tutto ciò che nasce dalla Fase 0 in poi.

## Fase 0 — Separazione dei due strumenti

**Precondizioni:** Fase 0a. **Chiamate provider:** zero.

L'ambizione di questa fase è stata **ridotta** il 2026-08-06: la versione precedente prescriveva di
riscrivere internamente `GRADING-IMPROVEMENTS-PLAN.md` (52 KB). Con il grading abbandonato quella è
manutenzione di un documento morto e non si è fatta.

Fatto il 2026-08-06: rinomina di `EVAL-WORKFLOW.md` in `GRADING-EVAL-WORKFLOW.md` (`570e929`) e
`CONSENSUS-WORKFLOW.md`, creato e riscritto due volte sull'esito delle sessioni di grilling.

**Chiusa il 2026-08-06.** I due residui sono stati fatti insieme alla Fase 0a: il banner di
abbandono in testa a `GRADING-IMPROVEMENTS-PLAN.md`, `GRADING-IMPROVEMENTS.md` e
`GRADING-EVAL-WORKFLOW.md`, corpo non toccato; e `README.md`, in inglese, con i gruppi *Active* e
*Archived*. Il banner è **in inglese** anche nei due documenti italiani: è testo nuovo, quindi cade
sotto la regola della Fase 0a, e una lapide uniforme sui tre vale più dell'allineamento alla lingua
del documento ospite.

## Fase 0c — Una riga, una affermazione

**Precondizioni:** nessuna. **Chiamate provider:** zero. **Andava prima della Fase 1a e della Fase
2.**

**Fatta il 2026-08-06.** La regola sta in `REGRESSION-LEDGER.md` § *How to use*, accanto a «binary
and falsifiable» e a «quantify over a generated plan»; la meccanica dello split — eredità del
contatore, id, `Absorbs`, commit non attribuiti — in § *Splitting a row that carries several claims*.
Registro e `support/CLAUSE-ROW-MAP.md` sono il record; qui non si duplicano.

Cosa ha prodotto:

- **Le quattro righe multi-affermazione sono diventate dieci.** `R-001` → `R-001` + `R-012`; `R-004`
  → `R-004` + `R-013` + `R-014`; `R-006` → `R-006` + `R-015` + `R-016`; `R-009` → `R-009` + `R-017`.
  Il primo membro conserva l'id, i successivi lo prendono in coda, ogni figlio eredita il contatore
  del padre e porta la sua provenienza in `Absorbs`. **Righe attive 11 → 17, senza una previsione in
  più**, e il registro lo dichiara perché il report legge `righe attive N → M` come misura di
  accumulo.
- **I quattro ancoraggi `unresolved` restano quattro**, ma solo due erano affermazioni: sono ora le
  righe `R-001` e `R-015`, e la Fase 4 le nomina per id. Gli altri due sono la componente `9aa2586`
  della cella `Commit` di `R-005` e di `R-006` — commit che nessuna affermazione rivendica, quindi lo
  split non li ha attribuiti a un figlio e li ha lasciati dove l'id è rimasto.
- **Il formato non prevede più membri.** § *Commit `SKILL.md`* diceva che una cella nomina i membri
  ancorati a commit diversi; ora una seconda voce in `Commit` significa solo un commit il cui testo
  la mappa non identifica. Il vincolo dell'assorbimento «una riga con più membri si assorbe membro per
  membro» resta come regola residuale, per una riga che una voce futura riportasse a più affermazioni.

**Residuo dichiarato:** gli artefatti storici — `recipe-app/results/CONSENSUS-CON-5.REPORT.md` in
testa — continuano a nominare i membri nella forma pre-split. Non si toccano: sono il record di ciò
che è stato misurato allora. Nella mappa restano per la stessa ragione le note che raccontano
l'assorbimento di `R-002` m1.

## Fase 1a — Contratto: template e validator degli `IMPROVEMENT`

**Precondizioni:** Fasi 0a e 0c. **Chiamate provider:** zero.

**Fatta il 2026-08-06.** Il contratto è `assets/improvement-template.md` più
`scripts/consensus/validate_improvement.py`, con `scripts/consensus/extract_clause_map.py` che
proietta la mappa nei record che il validator legge. I documenti sono il record: il template dichiara
la forma, la mappa dichiara la separazione dati/prosa in § *Where the records live*, e la misura del
gate su CON-4, il codice di uscita e i tre residui stanno in `workflow/CONFORMANCE.md`. Qui non si
duplicano.

Cosa è stato deciso mentre si scriveva, e non si legge dagli artefatti:

- **Un campo in più: `Remedy`, con tre valori — `reformulation`, `reach-change`, `addition`.** Senza
  di esso la condizionalità degli altri due campi non è decidibile da uno strumento: `Merged claim`
  serve «quando la voce cambia la portata» e la riformulazione scartata «quando la voce aggiunge
  righe», e nessuna delle due condizioni si legge dal testo dei campi presenti. Dichiarata dalla
  voce, la condizionalità diventa forma. È anche il campo che la Fase 5 legge per sapere se una voce
  si applica da sé.
- **Il commit dell'ultima riscrittura non è rigenerabile, e si verifica invece di riscriverlo.** Una
  clausola è una frase e una riga ne porta spesso due — `SKILL.md:43` porta `C-013` e l'inizio di
  `C-014` — quindi ogni derivazione basata sullo span attribuisce a una clausola la riscrittura della
  vicina: riprodotto in sede, dà 27 divergenze su 205 e sono esattamente le divergenze di blame che
  la mappa registra. Lo script emette la sede, emette `site_last` accanto a `last` invece che al suo
  posto, e verifica l'unico invariante che git può decidere: `last` non può essere più recente
  dell'ultima modifica al testo che circonda la clausola. **Le 205 clausole lo rispettano.**
- **`intersezione` fra template e validator sui riferimenti:** la forma `slice N più il nome del
  campo` si risolve contro il candidato dichiarato in `## Inputs`, non solo contro una sintassi. Una
  slice inesistente o un campo che quella slice non ha sono scarti, come una riga fuori range.
- **I tre riferimenti stali della mappa sono stati riparati**, già che il file si riapriva lì: le
  note di `C-157` e di `R-015` rimandano ora a `recipe-app/results/CONSENSUS-CON-5.REPORT.md` con la
  sezione nominata, e quella di `C-106` a *To populate*.

`make test` verde alla chiusura: 80 test sotto `scripts/`, 28 dei quali sul contratto.

**Restano fuori, e sono di altre fasi:** la mappa non registra ancora ciò che CON-6 cambierà (Fase 4)
e i quattro ancoraggi `unresolved` restano fallimenti registrati, non celle da riempire.

## Fase 1b-i — I quattro prompt

**Precondizioni:** Fase 1a. **Chiamate provider:** zero.

**Fatta il 2026-08-06.** I quattro prompt sono `prompts/improve.prompt.md`, `review.prompt.md`,
`verdict.prompt.md`, `recidiva.prompt.md`, e **sono il record**: forma, divieti e struttura di output
stanno lì e qui non si duplicano. `PROMPTS.md` porta in testa la nota che è scratchpad senza valore
normativo. **Nessuno dei quattro è mai stato eseguito** — è ciò che la Fase 2 misura.

Ogni file ha una **testata non inviata** sopra una riga orizzontale: payload come allowlist, slot che
il runner riempie, e la ragione delle scelte che il prompt stesso non può portare. Sotto la riga c'è
solo il testo che va al modello. È la convenzione che la Fase 5 rende, ed è testabile.

Cosa è stato deciso mentre si scriveva, e non si legge dai quattro file:

- **Il payload di `improve` è più grande di quanto l'hub dichiarasse**, e la voce 3 di
  `CONSENSUS-WORKFLOW.md` § *Il ciclo* è stata corretta di conseguenza. Al brief, alle fonti e ai due
  candidati si aggiungono `SKILL.md`, un **indice delle clausole** (sede · sezione · righe coprenti,
  senza il testo delle affermazioni) e le **affermazioni del registro**. Non è generosità: il
  contratto chiuso in Fase 1a chiede `Covering rows` — che la mappa decide, non la lettura dello
  skill — e `Merged claim`, che sostituisce righe che vanno lette. Senza l'indice ogni voce che nomina
  una clausola è uno scarto su un campo che il modello non può indovinare; senza le affermazioni
  `reach-change` è irraggiungibile e l'assorbimento, unica mossa che toglie una previsione, smette di
  succedere in silenzio.
- **Conseguenza dichiarata sulla `recidiva`, non nascosta.** Chi scrive gli `IMPROVEMENT` ha visto le
  affermazioni del registro, quindi una coppia è un difetto sollevato **nonostante** la riga fosse
  visibile. Rende una coppia evidenza più forte e uno zero evidenza più debole. Va in `Misurato su` al
  primo ciclo che lo esercita.
- **I candidati arrivano rinominati `CANDIDATE-A.md`/`CANDIDATE-B.md`.** I nomi reali portano l'alias
  del generatore: lasciarli avrebbe reso l'etichetta `Candidate A` decorativa, e la cecità nominale
  dichiarata in `workflow/CYCLE.md` copre il riconoscimento dello stile, non un'etichetta esplicita.
  `assets/improvement-template.md` è stato allineato in due punti — `## Inputs` e gli esempi di
  riferimento — perché citava i nomi reali. Stessa cosa per `REPORT-A`/`REPORT-B` in `review` e
  `recidiva`, con le due assegnazioni che non devono coincidere.
- **Il divieto è un'allowlist, non un elenco di file proibiti.** Nominare la mappa alias → generatore
  per vietarla è dire al modello dove sta la risposta. I prompt elencano ciò che si può leggere e
  aggiungono «nient'altro, né in questa sessione né in una delegata».
- **`review` legge i due report e nient'altro.** Il prompt legacy concedeva `SKILL.md` «se serve per
  chiarire terminologia»; è caduto. La fase decide una cosa sola — su cosa i due concordano — e ogni
  file in più è un invito a rigiudicare il merito, che il prompt vieta esplicitamente.
- **Gli id delle voci sono portanti.** `A#N` e `B#N`, ogni id esattamente una volta su cinque sezioni,
  con `## Out of scope` per le voci sul walking skeleton, che altrimenti sparirebbero rompendo il
  conteggio. Sono gli id su cui la `recidiva` accoppia e su cui il report di Fase 1c calcola le **voci
  classificate condivise da un solo `REVIEW`** — la misura di instabilità che sblocca la Fase 7.
- **`Same remedy` più `Remedy carried by`** sono il separatore fra `intersection` e
  `intersection-theme`, con la regola che il dettaglio non è una ragione per preferire un lato:
  esserlo decidibile su un piano generato sì.
- **`verdetto` ha tre valori, non due.** `holds`, `falsified`, `row-defect`. Il terzo porta una delle
  tre sole ragioni ammesse, prese da `REGRESSION-LEDGER.md` § *Authority and rewritten formulations*:
  non decidibile da ciò che il piano pubblica, decidibile solo scegliendo fra due letture, contraddice
  gli `Accepted alternatives` del brief. Senza il terzo valore il modello tira a indovinare dove il
  registro prescrive di riscrivere la riga.
- **Due verdetti per riga, e il modello non aggrega.** «Regge solo se regge su entrambi» è aritmetica
  del report. La citazione è obbligatoria anche su `holds` — è la sede su cui il verdetto poggia,
  cioè dove la violazione comparirebbe — perché senza è la lettura che degrada in silenzio.
- **I payload di `verdetto` e `recidiva` non portano stato né contatori.** Un modello a cui dici che
  una riga ha superato tre cicli cerca il quarto. Dormienza e conteggi restano decisioni del runner e
  del report.
- **`recidiva` accoppia al massimo una riga per voce**, con `Other rows considered` per le altre, e
  non emette nessun totale. Il divieto è scritto nel prompt: uno scalare nasconde l'instabilità che
  autorizzerebbe l'inversione a due chiamate.

**I due prompt sostituiti sono stati cancellati il 2026-08-07**, non lasciati sotto una nota di
supersessione. La prima stesura li aveva tenuti perché `workflow/CONFORMANCE.md` e
`CONSENSUS-WORKFLOW.md` li citavano come prova. L'argomento è caduto su un fatto già scritto nel
piano: **la Fase 0b prevede di tradurre `PROMPTS.md` in inglese**, e un documento che il piano si
impegna a riscrivere non è il record di niente — è la ragione per cui `recipe-app/results/` non si
tocca mai. Verificato invece di assunto: `be3daac` aveva già potato quel file di 193 righe poche ore
dopo l'arrivo degli artefatti CON-4, e nessuno l'ha letto come una perdita.

Quindi le due sezioni sono uscite dal working tree e **i due riferimenti in ingresso sono stati
riancorati a git** — `472233d:PROMPTS.md`, che porta il testo esattamente come CON-4 lo ha ricevuto,
byte per byte. Nessun fatto è stato spostato in `prompts/`: ciò che le due sezioni portavano di vivo
era già nei quattro prompt, e il resto — selezione del suffisso numerico, identità del proprio piano,
il reference plan cancellato, il contratto in prosa — è ciò che la riscrittura esiste per disfare.

Un solo residuo era vivo e non stava in nessuno dei due posti: **quante deleghe fa un'esecuzione.**
La qualifica dell'unità in `CONSENSUS-WORKFLOW.md` la deduceva dai prompt legacy, che delegavano a
due sub-agent ciascuno. I quattro nuovi non prescrivono nessuna delega, quindi il numero lo decide
l'harness; il vincolo che regge è ora scritto in tutti e quattro — una sessione delegata legge la
stessa allowlist e niente altro — e la tabella conta esecuzioni, che la Fase 5 riporta in chiamate.

**Residui dichiarati, e sono di altre fasi:**

- Le tre proiezioni che i payload nominano — indice delle clausole, affermazioni del registro, righe
  da verificare — **non esistono come file**. La Fase 2 le ricava a mano da `support/clause-row-map.tsv`
  e da `REGRESSION-LEDGER.md`; la Fase 5 le genera.
- **`## GENERATE PLAN` non ha successore.** È l'unica cosa rimasta in `PROMPTS.md`: la Fase 6 la
  prende e il file sparisce con lei.

## Fase 0d — Split di `CONSENSUS-WORKFLOW.md`

**Precondizioni:** nessuna. **Chiamate provider:** zero. **Non è un confine di strumento:** nessuno
di questi documenti entra in un payload, che si compone da allowlist — brief, fonti, candidati.

**Fatta il 2026-08-06.** Il documento era **707 righe** rilette a ogni sessione fredda per lavorare su
fasi che ne usano un quinto ciascuna. Ora l'hub è **121 righe** — procedura, vocabolario, tabella di
rotta — e il resto sta in `workflow/`: `CYCLE.md` 91, `CONFORMANCE.md` 130, `LEDGER.md` 126,
`RATIONALE.md` 157, `EVIDENCE.md` 104. Una sessione 1b-i legge 212 righe invece di 707.

Cosa è stato deciso mentre si eseguiva:

- **Due sezioni sono state cancellate, non spostate**, perché erano duplicati già divergenti.
  § *La lingua del progetto* ripeteva in italiano `README.md` § *Language*, che è il record dichiarato;
  § *Stato dell'automazione* ripeteva l'elenco delle fasi del piano e portava già la Fase 1c come una
  voce sola quando il piano ne registrava due deliverable su tre consegnati, e la Fase 3 senza
  l'ambizione ridotta. Restano due puntatori.
- **Il taglio è per consumatore, non per argomento.** `CYCLE.md`, `CONFORMANCE.md` e `LEDGER.md` sono
  i tre file che una fase apre per **fare**; `RATIONALE.md` e `EVIDENCE.md` non servono a nessuna fase
  e si aprono per sapere perché una decisione poggia su cosa. `EVIDENCE.md` è isolato anche per una
  seconda ragione: è l'unico blocco che ogni ciclo riscrive, e mescolato alla prosa normativa rendeva
  invisibile quale parte del documento è misura e quale è regola.
- **Cade l'invariante «autoconsistente: si legge in una sessione nuova senza altro contesto».** Lo
  sostituisce la tabella *Cosa aprire* dell'hub, cioè la stessa forma della *Rotta* del piano, che
  regge già. Il rischio dichiarato: una tabella di rotta sbagliata è una sessione che decide senza
  sapere perché — lo stesso modo di fallimento che il registro chiama *«porta con nessuno alla
  maniglia»*.
- **Solo spostamenti, salvo tre punti.** Le due cancellazioni qui sopra; la compressione di
  § *L'obiettivo* in *Cosa decide, e con quale errore*, con l'originale conservato in `RATIONALE.md`;
  e la lapide del grading fusa in `RATIONALE.md` § *Perché il grading system è abbandonato*, che il
  testo stesso indicava come sede delle sue due ragioni.
- **Otto riferimenti in ingresso puntavano per titolo di sezione** e sono stati corretti nello stesso
  passaggio, incluso quello del report CON-5: un artefatto storico non si traduce e non si riscrive,
  ma un puntatore stale si ripara, come già fatto sui tre della mappa in Fase 1a. Con l'occasione è
  caduto il residuo di Fase 0b su `CONSENSUS-WORKFLOW.md:128`, che rimandava a *Formulazioni
  riscritte* del registro invece che del report CON-5.

**Conseguenza sulla Fase 0b:** la conversione in inglese diventa incrementale, un file per volta,
invece di un blocco da 707 righe. Ed è la ragione dell'ordine: split prima, traduzione poi. Fatti
insieme, il diff non avrebbe distinto gli spostamenti dalle riscritture.

## Fase 1b-ii — Mappa dei generatori e slot `gen`

**Precondizioni:** nessuna; era indipendente dalla 1b-i. **Chiamate provider:** zero.

**Fatta il 2026-08-07.** Il record è `support/AGENT-PLAN-MAP.md`: quattordici artefatti, il formato
per i cicli futuri, e la dichiarazione di ciò che non si è ricostruito. Qui non si duplica.

Cosa è stato deciso mentre si eseguiva:

- **Modello ed effort di CON-1…CON-5 sono `unrecorded` e restano tali.** Non è una casella vuota: è
  il valore vero. Cercati negli artefatti, nel prompt di generazione superstite, in ogni artefatto di
  grading sotto `results/calibration-*`, nei messaggi dei cinque commit e in
  `GRADING-IMPROVEMENTS-PLAN.md`. Il grading registra `grader.requested_model` e `grader.effort` — del
  **grader**; i v1 scrivono `"model": "cli-default"`, che nomina il default della CLI al momento della
  run e non si risolve all'indietro; nessun campo nomina il generatore del candidato, che compare come
  path e senza hash. **Copiare i default di grading — `gpt-5.6-sol`/`high`, `claude-opus-5`/`high` —
  era la tentazione da rifiutare:** avrebbe messo un numero plausibile nell'unica colonna che esiste
  per dire come un verdetto è stato ottenuto davvero. Le diciassette celle del registro restano
  `gen unrecorded` e la ragione è dichiarata una volta, in § *`Measured on`*, che punta alla mappa. La
  voce che il registro teneva in *To populate* è caduta: non è più un lavoro da fare.
- **Harness e modalità invece si ricostruiscono, e la mappa li porta.** `CC` è Claude Code, `CX` è
  Codex; nessun documento lo dichiarava, e le quattro evidenze che concordano stanno nella mappa. La
  modalità è **sessione interattiva**, non chiamata headless — è il confine che la Fase 6 già si
  impegna a registrare. Da qui la distinzione che il file impone: `CC`/`CX` nominano l'harness, e una
  cella `Misurato su` che li porta non dice **niente** sul modello. Era la confusione da chiudere.
- **Due assegnazioni per ciclo, e non devono coincidere.** La ragione scritta è che se il lato che
  tiene `CANDIDATE-A` tiene anche `REPORT-A`, chi rompe la cecità in una fase la rompe nell'altra
  gratis, e le due fasi smettono di fallire indipendentemente. La cecità resta nominale: lo scopo non
  è renderla a tenuta, è impedire che una falla ne diventi due.
- **`1e466f4` non è un rename, ed è il ritrovamento che cambia la tabella.** Il commit — messaggio
  *renaming* — cancella due generazioni `CX` pre-ristrutturazione, ne rinumera una terza e ne aggiunge
  quattro nuove. Confronto degli hash dei blob: l'attuale `PLAN-CX-CON-2.md` è il blob aggiunto il
  2026-07-31 alle 17:08 sotto il nome `PLAN-CX-CON-4.md`. Letta senza il confronto, la sua storia git
  lo data al 2026-08-01: un ciclo intero di scarto. Da lì la regola che la mappa dichiara — **`CON-N`
  è il ciclo, non l'ordinale di run del lato** — e il fatto che due generazioni `CX` esistano nella
  storia e in nessun ciclo.
- **I piani CON-5 esistevano il 2026-08-02 alle 17:03, non il 2026-08-04 alle 11:57.** `f00d75d`
  committa i loro `SCORE` v1, che li hanno graduati. Le 11:57 sono l'ora di `515e0a3`, cioè del
  commit dei piani. La correzione **rafforza** l'argomento della Fase 2 per cui i piani CON-5 non si
  riusano, e il piano è stato corretto di conseguenza. Il limite dichiarato: i metadata v1 non portano
  hash del candidato, quindi il vincolo è sull'**esistenza**, non sull'identità del testo committato
  due giorni dopo.
