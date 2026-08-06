# Ciclo di consenso — piano di implementazione

Piano per separare il ciclo di consenso dal grading system abbandonato e automatizzarlo. Ogni fase è
pensata per una **sessione fredda separata**: dichiara le proprie precondizioni, le attività, come si
verifica e cosa produce. Una fase non presume il contesto conversazionale in cui la precedente è
stata svolta.

Lo strumento e la sua ragione stanno in `CONSENSUS-WORKFLOW.md`; qui c'è solo il lavoro da fare.

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
  che il generico non riempie, non un giudizio con una soglia. **Niente soglie.**
- Una voce non conforme si **scarta e si registra**, con **un solo tentativo**. Il documento non si
  rigenera mai. Un errore di trasporto è un ritentativo della *chiamata*, non del documento. Un lato
  a zero voci conformi non blocca il ciclo.
- **`Origine` ha quattro valori**: `intersezione`, `intersezione-tema`, `giudizio`, `potatura`.
  **I nomi canonici sono inglesi** dal 2026-08-06, perché li scrivono il registro migrato, i prompt e
  il validator: `intersection`, `intersection-theme`, `judgement`, `pruning`. Stessa cosa per
  `Verifica`: `validator` e `reading`. I termini italiani di questo piano e di
  `CONSENSUS-WORKFLOW.md` restano leggibili finché la Fase 0b non li converte, e la mappa fra i due
  insiemi è dichiarata nelle regole d'uso del registro. Prompt e validator non emettono mai gli
  italiani.
- **Una voce che tocca una clausola coperta o ri-ancora la riga, o la assorbe.** Due regole, non una,
  perché **le righe quantificano su un piano generato, non sul testo dello skill** — è il criterio con
  cui il registro è stato scritto (`0273a73`: *«each stated over a generated plan rather than over the
  skill text»*). Ne discende che una riformulazione **non falsifica** la riga: rompe l'attribuzione.
  - **Cambia il testo, non la portata → ri-ancoraggio, automatico.** La riga resta, prende il commit
    nuovo, contatore a **`×0`**. Vale anche per una riga regredita, e la smentita resta scritta nella
    cella di stato con il commit contro cui era stata misurata.
  - **Cambia la portata → assorbimento.** Una riga sola afferma tutto, `×0`, e l'affermazione che
    sostituisce esce dal file: git conserva il testo, il registro conserva solo ciò che è ancora
    previsto. La scrive `improve`, la edita il veto. Due vincoli: si assorbe solo se la fusione resta
    decidibile in una lettura, e **una riga = una affermazione**, quindi i membri che nessuno rileva
    restano come riga propria. Dal 2026-08-06 il secondo vincolo è **regola di scrittura di ogni
    riga**, promossa dalla Fase 0c, che ha splittato le quattro righe multi-affermazione
    preesistenti: nessuna riga ha più membri, e il vincolo resta come regola di ciò che accade a una
    riga che una voce futura riportasse a più affermazioni.
  Regole e vincoli vivono in `REGRESSION-LEDGER.md` § *Re-anchoring and absorption*; qui non si
  duplicano. **Applicato il 2026-08-06** a `R-002` m1 → `R-010` e alla clausola `Enabler` di `R-008`
  → `R-011`: erano ancorate alla stessa clausola dopo `87150d3` e `eb926bb`, quindi contavano due
  volte una sola evidenza. L'assorbimento sostituisce il superamento con `superata da R-NNN`, che
  teneva in vita una riga fuori dall'insieme verificato per conservarne la storia — che ora sta in una
  cella.
- **Una voce vale `intersezione` o `intersezione-tema` solo se entrambi i `REVIEW` la classificano
  condivisa.** Classificazione unilaterale → `giudizio`, e nessuna applicazione automatica.
- **Il workflow applica al working tree e non committa mai.** Applica solo ciò che il filtro
  licenzia. Una voce = un hunk di `SKILL.md` + una riga di registro, stesso id, riga con
  `Commit: (pending)`. Il veto umano legge i **contatori in testa al report**, poi `git diff`.
- **`recidiva` è una chiamata sola**, modello fisso `claude-opus-5`, e produce l'**elenco delle
  coppie** `voce improve → riga | nessuna`, non uno scalare. Controargomento ed eventi di inversione
  sono in `CONSENSUS-WORKFLOW.md` § *Perché `recidiva` è una sola chiamata*.
- **Dormienza a `non smentita ×3`**, verifica 1 ciclo su 3, risveglio immediato da `recidiva`.
  Sostituisce il pensionamento, che era rinviato senza trigger osservabile.
- I prompt escono da `PROMPTS.md` e diventano l'unica sorgente sotto `prompts/`; `PROMPTS.md` resta
  scratchpad umano senza valore normativo.
- `support/AGENT-PLAN-MAP.md` tiene la mappa alias → piano → generatore ed è escluso da ogni payload.
- `CON-N` resta il contatore di ciclo negli artefatti; non si rinominano artefatti storici. **CON-5
  non si riusa.** Il prossimo ciclo è **CON-6**.
- **Modelli ed effort: `gpt-5.6-sol` e `claude-opus-5`, entrambi a `high` in CON-6.** `medium` è un
  confine di strumento isolato in **CON-7**: cambiarlo in CON-6 confonderebbe la variabile testata —
  la specificità degli `IMPROVEMENT` — con una scelta di costo indipendente.
- **La revisione di `EVALUATION-BRIEF.md` sta dopo CON-6**, per la stessa ragione: è l'autorità contro
  cui si decidono quattordici righe su diciassette.
- **L'inglese è la lingua del progetto dal 2026-08-06.** Le fonti in `recipe-app/sources/` e gli
  artefatti storici — `PLAN-*`, `IMPROVEMENT`, `REVIEW`, report — **non si convertono mai**.
- Un confine di strumento **si attraversa una volta sola, deliberatamente, e si registra.**
- La decisione su cosa applicare allo `SKILL.md` resta umana in ogni fase, in forma di veto.
- **Le 15 unità di calibrazione già pagate non vanno conservate.** I 30 file sono tracciati in git.

## Fase 0a — L'inglese è la lingua del progetto

**Precondizioni:** nessuna. **Chiamate provider:** zero. **Va per prima.**

**Fatta il 2026-08-06.** La regola, le due esclusioni permanenti con la loro ragione e la nota su
`EVALUATION-BRIEF.md` e `SKILL.md` vivono in `CONSENSUS-WORKFLOW.md` § *La lingua del progetto* e in
`evals/plan-slices/README.md` § *Language*. I due documenti sono il record; qui non si duplicano.

La conversione dei documenti esistenti è Fase 0b e non blocca niente; separarle è ciò che evita di
scrivere in italiano tutto ciò che nasce dalla Fase 0 in poi.

## Fase 0 — Separazione dei due strumenti

**Precondizioni:** Fase 0a. **Chiamate provider:** zero.

L'ambizione di questa fase è stata **ridotta** il 2026-08-06: la versione precedente prescriveva di
riscrivere internamente `GRADING-IMPROVEMENTS-PLAN.md` (52 KB). Con il grading abbandonato quella è
manutenzione di un documento morto e non si fa.

Fatto il 2026-08-06: rinomina di `EVAL-WORKFLOW.md` in `GRADING-EVAL-WORKFLOW.md` (`570e929`) e
`CONSENSUS-WORKFLOW.md`, creato e riscritto due volte sull'esito delle sessioni di grilling.

**Chiusa il 2026-08-06.** I due residui sono stati fatti insieme alla Fase 0a: il banner di
abbandono in testa a `GRADING-IMPROVEMENTS-PLAN.md`, `GRADING-IMPROVEMENTS.md` e
`GRADING-EVAL-WORKFLOW.md`, corpo non toccato; e `evals/plan-slices/README.md`, in inglese, con i
gruppi *Active* e *Archived*. Il banner è **in inglese** anche nei due documenti italiani: è testo
nuovo, quindi cade sotto la regola della Fase 0a, e una lapide uniforme sui tre vale più
dell'allineamento alla lingua del documento ospite.

## Fase 0b — Conversione dei documenti umani

**Precondizioni:** Fase 0a. **Chiamate provider:** zero. **Nessuna fase dipende da questa.**

Documenti che nessun modello legge durante un ciclo. La conversione è lavoro bruto senza rischio e
senza dipendenze: può stare per ultima, o essere fatta a pezzi, o slittare indefinitamente.

- [ ] `CONSENSUS-WORKFLOW.md`, `CONSENSUS-WORKFLOW-PLAN.md`, `NOTES.md`, `PROMPTS.md`.
- [ ] Non toccare i documenti di grading: sono archivio.
- [ ] Riparare `CONSENSUS-WORKFLOW.md:128`, che rimanda a *Formulazioni riscritte* del registro: la
  sezione è in `recipe-app/results/CONSENSUS-CON-5.REPORT.md` dalla Fase 1c.

**Verifica:** i documenti convertiti non citano artefatti con nomi diversi da quelli reali; le
citazioni testuali dagli artefatti storici restano **in italiano fra virgolette**, perché sono prove.

## Fase 0c — Una riga, una affermazione

**Precondizioni:** nessuna. **Chiamate provider:** zero. **Andava prima della Fase 1a e della Fase
2.**

**Fatta il 2026-08-06.** La regola sta in `REGRESSION-LEDGER.md` § *How to use*, accanto a «binary
and falsifiable» e a «quantify over a generated plan»; la meccanica dello split — eredità del
contatore, id, `Absorbs`, commit non attribuiti — in § *Splitting a row that carries several claims*.
Registro e `support/CLAUSE-ROW-MAP.md` sono il record; qui non si duplicano.

Cosa ha prodotto, perché le fasi seguenti ci si appoggiano:

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

**Residuo dichiarato:** gli artefatti storici — `CONSENSUS-CON-5.REPORT.md` in testa — continuano a
nominare i membri nella forma pre-split. Non si toccano: sono il record di ciò che è stato misurato
allora. Nella mappa restano per la stessa ragione le note che raccontano l'assorbimento di `R-002` m1.

## Fase 1a — Contratto: template e validator degli `IMPROVEMENT`

**Precondizioni:** Fasi 0a e 0c. **Chiamate provider:** zero.

**Fatta il 2026-08-06.** Il contratto è
`evals/plan-slices/assets/improvement-template.md` più
`evals/plan-slices/scripts/consensus/validate_improvement.py`, con
`extract_clause_map.py` che proietta la mappa nei record che il validator legge. I documenti sono il
record: il template dichiara la forma, la mappa dichiara la separazione dati/prosa in
§ *Where the records live*, e qui non si duplicano.

Cosa è stato deciso mentre si scriveva, perché le fasi seguenti ci si appoggiano:

- **Un campo in più: `Remedy`, con tre valori — `reformulation`, `reach-change`, `addition`.** Senza
  di esso la condizionalità degli altri due campi non è decidibile da uno strumento: `Merged claim`
  serve «quando la voce cambia la portata» e la riformulazione scartata «quando la voce aggiunge
  righe», e nessuna delle due condizioni si legge dal testo dei campi presenti. Dichiarata dalla
  voce, la condizionalità diventa forma: `Merged claim` obbligatorio e solo con `reach-change`,
  riformulazione scartata obbligatoria e solo con `addition` accanto a una clausola nominata. È
  anche il campo che la Fase 5 legge per sapere se una voce si applica da sé.
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
- **Il gate legge le voci anche fuori da `## Entries`.** Un documento che numera le voci altrove
  deve comunque un log degli scarti per voce: «nessun `## Entries`» e «nessuna voce» sono due fatti
  diversi, e collassarli avrebbe reso invisibile proprio l'asimmetria di CON-4.
- **I tre riferimenti stali della mappa sono riparati**, già che il file si riapriva qui: le note di
  `C-157` e di `R-015` rimandano ora a `recipe-app/results/CONSENSUS-CON-5.REPORT.md` con la sezione
  nominata, e quella di `C-106` a *To populate*.
- **Codice di uscita:** una voce scartata non è un errore. Lo script esce con 1 solo quando il
  documento non è leggibile come insieme di voci; un lato a zero voci conformi esce con 0, coerente
  con «un lato a zero voci conformi non blocca il ciclo».

**Verificato sui due artefatti di CON-4, con l'asimmetria attesa:** `PLAN-CC-CON-4.IMPROVEMENT.md`
dà **10 voci, 0 conformi**, ognuna con l'elenco dei campi mancanti; `PLAN-CX-CON-4.IMPROVEMENT.md`
dà **0 voci**, perché non ne contiene nessuna. È la stessa misura della tabella di
`CONSENSUS-WORKFLOW.md` § *Il contratto di conformità* — «sezione per miglioramento: sì, 10 |
nessuna: 8 bullet» — ottenuta ora da uno strumento. Precisazione sul senso di «parzialmente
conformi»: nessuna voce di `CC` supera il contratto, perché il documento di CON-4 non ha nessuno dei
campi nuovi; la conformità parziale sta nell'essere leggibile **come voce**, cioè nel produrre uno
scarto diagnosticabile invece di sparire.

`make test` verde: 80 test sotto `evals/plan-slices/scripts`, 28 dei quali sul contratto.

**Residui dichiarati, tutti della stessa spaccatura `validator`/`lettura` delle righe del registro:**

- il validator verifica **che** un riferimento esista, non che **sostenga** l'affermazione;
- verifica che una fusione sia scritta nella grammatica delle righe, non che resti **decidibile in
  una lettura**;
- verifica che una riformulazione scartata sia stata scritta, non che la ragione sia **ammissibile**.
  Il divieto — «la clausola è coperta da una riga del registro» non è una ragione — vive nel
  template e sta al veto. La forma lo rende costoso da violare: il campo chiede la riformulazione
  *effettivamente scritta*, e una dichiarazione di copertura non riempie quella cella.

Restano fuori, e sono di altre fasi: la mappa non registra ancora ciò che CON-6 cambierà (Fase 4) e
i quattro ancoraggi `unresolved` restano fallimenti registrati, non celle da riempire.

## Fase 1b — I quattro prompt

**Precondizioni:** Fase 1a. **Chiamate provider:** zero.

I prompt **citano** il template, non lo duplicano.

- [ ] `prompts/improve.prompt.md`: payload cieco simmetrico, un solo documento per valutatore
  sull'unione dei difetti dei due candidati, divieto esplicito di leggere `support/`, i due campi
  bidirezionali, l'esclusione del walking skeleton dichiarata come restrizione di scope del ciclo,
  `EVALUATION-BRIEF.md` al posto di `REFERENCE-PLAN.md` eliminato da `6476f32`.
- [ ] `prompts/review.prompt.md`: payload **cieco e simmetrico** — i due `IMPROVEMENT` come
  `Report A`/`Report B`, mai «il tuo report». Sezioni simmetriche: condivisa, unica ad A, unica a B,
  contraddittoria. Per ogni voce condivisa, il campo che dichiara se i due lati portano **lo stesso
  rimedio** o solo lo stesso tema — è il dato che separa `intersezione` da `intersezione-tema`.
- [ ] `prompts/verdict.prompt.md`: per ogni riga attiva, verdetto più **citazione obbligatoria** del
  punto pubblicato (piano, slice, sezione). Nessun verdetto senza citazione; una citazione che non si
  risolve è uno scarto. La cella `Da sorvegliare` della riga entra nel prompt come istruzione
  aggiuntiva per quella riga.
- [ ] `prompts/recidiva.prompt.md`: una sola chiamata, input i due `IMPROVEMENT` più **tutte** le
  righe, dormienti incluse. Output l'elenco delle coppie `voce → riga | nessuna`. Nessuno scalare.
- [ ] Aggiungere in testa a `PROMPTS.md` la nota che è uno scratchpad umano e che la sorgente
  normativa è `prompts/`.
- [ ] Creare `support/AGENT-PLAN-MAP.md` con le righe di CON-1…CON-5 e il formato per i cicli futuri.
- [ ] **Riempire lo slot `gen` di `Misurato su` in tutte le righe del registro** dai dati della
  mappa — sono diciassette dopo lo split della Fase 0c. Oggi portano tutte `gen unrecorded`: modello
  ed effort di CON-1…CON-5 non esistono in nessun artefatto, e `CC`/`CX` nominano l'harness, non il
  modello. Se la mappa non riesce a ricostruirli, le celle restano `unrecorded` e lo si dichiara una
  volta invece di lasciarlo sembrare una svista.

**Verifica:** nessun prompt nomina `REFERENCE-PLAN.md`, `support/`, i path o i nomi dei generatori;
`review` non contiene la parola «tuo»; i nomi degli artefatti citati coincidono con quelli della
struttura del report.

**Rischio:** i prompt riscritti non sono mai stati eseguiti. È esattamente ciò che la Fase 2 misura.

## Fase 1c — Registro, mappa e report

**Precondizioni:** Fase 0a. Indipendente da 1a e 1b: la mappa che 1a consuma è già consegnata.
**Chiamate provider:** zero.

**Due deliverable su tre sono fatti** il 2026-08-06, in un solo attraversamento del confine:

- **la mappa clausola → riga** — `support/CLAUSE-ROW-MAP.md`: 205 clausole normative, 40 coperte
  (20%), di cui 20 restatement, 165 scoperte. Dichiara per ogni voce come l'ancoraggio è stato
  ottenuto — `declared`, `reconstructed`, `unresolved` — più regola di conteggio, divergenze di blame
  e verifica del campione. Quattro ancoraggi restano `unresolved` e li decide la Fase 4;
- **il registro** — estrazione della narrativa in `recipe-app/results/CONSENSUS-CON-5.REPORT.md`,
  traduzione, migrazione semantica, riclassificazione a `intersection-theme`, ri-ancoraggio di
  `R-002` e `R-008`, e i due assorbimenti del 2026-08-06. Le regole d'uso del registro sono il
  record: non si riassumono qui.

Resta il terzo.

- [ ] **`evals/plan-slices/assets/report-template.md`**, in inglese: la struttura di
  `recipe-app/results/CONSENSUS-CON-N.REPORT.md`. Sta in `assets/` accanto a
  `improvement-template.md`, non dentro `CONSENSUS-WORKFLOW.md`, perché il join `report` della Fase 5
  lo rende come rende gli altri template. **Contatori in testa:**

  ```
  SKILL.md   417 → 451   (+34)
  voci applicate         5
    riformulazioni       0
    aggiunte             5   ← ognuna con la ragione della riformulazione scartata
  righe di registro nuove 5   (2 intersezione, 1 intersezione-tema, 2 giudizio)
  righe ri-ancorate       0   (contatore riportato a ×0)
  affermazioni assorbite  0
  righe attive           17 → 22
  voci scartate dal gate  3   (per campo mancante)
  verdetti scartati       0   (citazione non risolta)
  recidiva                2 coppie su 9 voci
  ```

  `righe attive N → M` è per il registro ciò che `0 riformulazioni su 5 aggiunte` è per lo skill: il
  contatore che morde sull'accumulo invece che sul merito. Ri-ancoraggio e assorbimento non aggiungono
  righe — l'assorbimento anzi ne toglie una se il membro assorbito era tutta la riga — quindi una
  crescita di `righe attive` accusa sempre e solo le aggiunte. `affermazioni assorbite` è ciò che il
  veto deve leggere per primo: è l'unico contatore che dice che una previsione è **uscita** dal file,
  e ogni assorbimento va riletto perché la fusione può aver allargato ciò che la riga afferma.

  Poi: esito del validator strutturale; voci applicate con id, hunk e origine; **voci classificate
  condivise da un solo `REVIEW`** — la misura di instabilità che sblocca la Fase 7 e che oggi nessuno
  produce; elenco dei punti che richiedono lettura umana; log degli scarti; coppie di recidiva;
  verdetti con le loro citazioni.

  Il report CON-5 è già un'istanza parziale della struttura, non un modello: è un ciclo parziale,
  quindi i contatori senza valore portano `n/a — partial cycle` invece di uno zero che si leggerebbe
  come misura. Il template dichiara quella convenzione.

**Verifica:** il template rende ogni contatore derivabile dagli artefatti del ciclo senza una
chiamata, e il report CON-5 riscritto nella sua forma non perde nessuno dei dati che porta oggi.

## Fase 2 — Ciclo CON-6 manuale

**Precondizioni:** Fasi 0c, 1a, 1b, 1c. `0c` è esplicita e non solo transitiva: un ciclo eseguito su
righe multi-affermazione produce verdetti che lo split dovrebbe poi disaggregare a posteriori.
**Chiamate provider:** **9** — 2 generazione, 2 `improve`,
2 `review`, 2 `verdetto`, 1 `recidiva`. Effort **`high`**. Richiede **autorizzazione esplicita** dopo
il dry-run e il conteggio, per `evals/AGENTS.md`.

I piani CON-5 **non si riusano**: sono delle 11:57 del 2026-08-04, mentre `87150d3` è delle 23:11 e
`eb926bb` delle 23:30. Precedono entrambi i commit, quindi non possono verificare `R-010` e `R-011`.

- [ ] Generare i due candidati con lo `SKILL.md` corrente e registrarli in
  `support/AGENT-PLAN-MAP.md`.
- [ ] `make validate` su entrambi.
- [ ] Eseguire `improve`, il gate, `review`, `verdetto` e `recidiva` a mano, copiando i prompt da
  `prompts/`.
- [ ] Scrivere `CONSENSUS-CON-6.REPORT.md` nella struttura di Fase 1c, contatori in testa.
- [ ] Applicare le sole voci che il filtro licenzia, una riga di registro per voce, `Commit:
  (pending)`. **Non committare dal workflow.** Leggere i contatori, poi `git diff`, poi decidere.
- [ ] Correggere `prompts/`, `assets/` e `CONSENSUS-WORKFLOW.md` dove la procedura non ha retto.

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
il ciclo non interpretabile, per la stessa ragione per cui l'effort resta a `high`.

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

La condizione di sblocco è ora **osservabile**: il report di Fase 1c pubblica le voci classificate
condivise da un solo `REVIEW`. Prima la fase diceva «si valuta se due cicli mostrano che la
classificazione è instabile», ma niente misurava quell'instabilità, quindi la condizione non poteva
verificarsi.
