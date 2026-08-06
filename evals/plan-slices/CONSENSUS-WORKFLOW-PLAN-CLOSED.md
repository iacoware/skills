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
`EVALUATION-BRIEF.md` e `SKILL.md` vivono in `CONSENSUS-WORKFLOW.md` § *La lingua del progetto* e in
`README.md` § *Language*. I due documenti sono il record; qui non si duplicano.

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
gate su CON-4, il codice di uscita e i tre residui stanno in `CONSENSUS-WORKFLOW.md` § *Il contratto
di conformità*. Qui non si duplicano.

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
