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
    restano come riga propria.
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
  cui si decidono sette righe su undici.
- **L'inglese è la lingua del progetto dal 2026-08-06.** Le fonti in `recipe-app/sources/` e gli
  artefatti storici — `PLAN-*`, `IMPROVEMENT`, `REVIEW`, report — **non si convertono mai**.
- Un confine di strumento **si attraversa una volta sola, deliberatamente, e si registra.**
- La decisione su cosa applicare allo `SKILL.md` resta umana in ogni fase, in forma di veto.
- **Le 15 unità di calibrazione già pagate non vanno conservate.** I 30 file sono tracciati in git.

## Fase 0a — L'inglese è la lingua del progetto

**Precondizioni:** nessuna. **Chiamate provider:** zero. **Va per prima.**

Solo la decisione e la regola. La conversione dei documenti esistenti è Fase 0b e non blocca niente;
separarle è ciò che evita di scrivere in italiano tutto ciò che nasce dalla Fase 0 in poi.

- [ ] Dichiarare in `CONSENSUS-WORKFLOW.md` e in `evals/plan-slices/README.md` che **ogni artefatto
  nuovo nasce in inglese**: prompt, template, validator, report, righe di registro, commit.
- [ ] Dichiarare le **due esclusioni permanenti**, con la ragione:
  - `recipe-app/sources/` — convertirle è un **nuovo scenario**, non una traduzione. Invaliderebbe i
    cinque piani, le righe misurate su di essi e le citazioni del brief, che puntano a titoli di
    sezione italiani (`sources/goal.md`, "Vincoli e scala").
  - `PLAN-*`, `*.IMPROVEMENT.md`, `*.REVIEW.md` e i report già prodotti — sono il record di ciò che è
    stato generato. Tradurli è falsificarlo.
- [ ] Registrare che `EVALUATION-BRIEF.md` è già in inglese e che i titoli di sezione italiani che
  contiene sono **puntatori alle fonti**, non prosa da tradurre. `SKILL.md` è già in inglese.

**Verifica:** la regola e le due esclusioni sono scritte in entrambi i documenti.

## Fase 0 — Separazione dei due strumenti

**Precondizioni:** Fase 0a. **Chiamate provider:** zero.

L'ambizione di questa fase è stata **ridotta** il 2026-08-06: la versione precedente prescriveva di
riscrivere internamente `GRADING-IMPROVEMENTS-PLAN.md` (52 KB). Con il grading abbandonato quella è
manutenzione di un documento morto e non si fa.

Fatto il 2026-08-06: rinomina di `EVAL-WORKFLOW.md` in `GRADING-EVAL-WORKFLOW.md` (`570e929`) e
`CONSENSUS-WORKFLOW.md`, creato e riscritto due volte sull'esito delle sessioni di grilling. Il
documento è il record; qui restano i due residui.

- [ ] **Banner in testa a `GRADING-IMPROVEMENTS-PLAN.md`, `GRADING-IMPROVEMENTS.md` e
  `GRADING-EVAL-WORKFLOW.md`:** «Abbandonato il 2026-08-06. Documento non mantenuto, conservato per
  la storia. Lo strumento attivo è `CONSENSUS-WORKFLOW.md`.» Nient'altro: **il corpo di quei
  documenti non si tocca**.
- [ ] Creare `evals/plan-slices/README.md` **in inglese** come punto d'ingresso della directory, con
  **due** gruppi di artefatti:
  - **attivo** — `CONSENSUS-WORKFLOW.md`, `CONSENSUS-WORKFLOW-PLAN.md`, `prompts/`, `assets/`,
    `support/`, `REGRESSION-LEDGER.md`, `NOTES.md`, `recipe-app/sources/`,
    `recipe-app/EVALUATION-BRIEF.md`, `recipe-app/results/PLAN-*` e i report di ciclo,
    `validate_plan.py` che vive nella skill, `evals/AGENTS.md`, il target `validate`;
  - **archiviato** — `GRADING-*.md`, `grader-rubric*.json`, `fixtures/`, `results/calibration-*/`,
    gli script di grading e i target `grade`/`compare`/`calibrate*`.

**Verifica:** i tre documenti di grading aprono con il banner; nessun file di codice è stato toccato,
quindi `make test` resta quello di prima.

**Output:** un commit per il banner, uno per il README.

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

## Fase 1a — Contratto: template e validator degli `IMPROVEMENT`

**Precondizioni:** Fase 0a; la mappa clausola → riga che questa fase consuma **esiste dal
2026-08-06**, quindi 1a non è più bloccata. **Chiamate provider:** zero.

La domanda che bloccava questa fase — cosa succede alla riga quando una voce riformula la clausola
che la copre — è decisa: vedi *Decisioni già prese*, ri-ancoraggio automatico se cambia il testo,
assorbimento se cambia la portata.

La dipendenza dalla mappa nasce dalla decisione stessa. Il validator controlla che le righe coprenti
dichiarate da una voce **coincidano con la mappa**, e senza mappa quel controllo non distingue una
voce che dichiara `uncovered` per ignoranza da una che lo dichiara con ragione — cioè esattamente il
caso che la regola dura esiste per intercettare. È l'unico pezzo di 1c che serve a 1a: traduzione,
split della narrativa e migrazione semantica del registro non entrano.

È il pezzo che decide tutti gli altri, ed è l'unico che è codice. Replica l'architettura che nello
skill ha retto cinque cicli: `skills/plan-slices/assets/plan-template.md` +
`skills/plan-slices/scripts/validate_plan.py`. **Gli omonimi dello strumento stanno altrove:**
`evals/plan-slices/assets/` e `evals/plan-slices/scripts/consensus/`. Due `assets/` e due `scripts/`
sono una trappola per una sessione fredda, quindi qui i path sono pieni.

- [ ] Creare `evals/plan-slices/assets/improvement-template.md` **in inglese**, con i campi
  obbligatori per voce:
  - `Evidence — candidate A` e `Evidence — candidate B`, **due celle separate**: un riferimento
    localizzabile (`PLAN-…-CON-N.md:NN`, oppure `slice N` più il nome del campo) oppure la
    dichiarazione esplicita che quel candidato non manifesta il difetto;
  - `Existing rule that failed to prevent the defect` — clausola di `SKILL.md` con la sua sezione,
    **più le righe di registro che la coprono, oppure `uncovered`**, oppure `none` se nessuna
    clausola è nominata. Le righe dichiarate sono ciò che il workflow **ri-ancora**, o ciò che la
    voce deve **assorbire**, ed è l'unico modo per rendere meccanicamente rilevabile un caso che
    prima era invisibile: `R-002` portava `Commit: d977043` mentre la sua clausola era stata
    riscritta da `87150d3`, senza nessun link in avanti;
  - `Change to the skill` — sezione precisa e modifica normativa concreta;
  - `Merged claim` — obbligatorio quando la voce **cambia la portata** di una regola coperta: la riga
    unica che sostituisce le righe dichiarate, nella grammatica di `Binary test`. È l'assorbimento, e
    il template è il posto dove `improve` lo scrive. Assente quando la voce riformula soltanto: lì
    il ri-ancoraggio è automatico e non c'è niente da scrivere;
  - `Reformulation attempted and discarded, and why` — obbligatorio quando il campo precedente nomina
    una clausola **e** la voce aggiunge righe. **«La clausola è coperta da una riga del registro» non
    è una ragione ammissibile**, ed è il vincolo che tiene in piedi la regola dura: le clausole
    coperte sono le poche già accusate — quattro clausole di corpo portano sei righe su undici — cioè
    le candidate più probabili alla riformulazione. Ammettere la copertura come esenzione le
    renderebbe permanentemente non riformulabili e restituirebbe il cricchetto intatto;
  - `Binary test` — nella grammatica delle righe del registro, decidibile su un piano generato;
  - `Cost` — cosa si toglie o si fonde se questa entra.
- [ ] Creare `scripts/consensus/validate_improvement.py` con i controlli:
  - presenza di ogni campo obbligatorio per voce;
  - **i riferimenti si risolvono**: il file esiste e il numero di riga è nel range. Intercetta le
    citazioni allucinate, che è un rischio reale in un artefatto che nessuno rilegge riga per riga;
  - **le righe dichiarate coprenti si risolvono** in `REGRESSION-LEDGER.md` e coincidono con la mappa
    clausola → riga della Fase 1c; una clausola che la mappa dichiara coperta e la voce dichiara
    `uncovered` è uno scarto;
  - `Binary test` presente e non vuoto, con una grammatica minima;
  - `Merged claim`, quando c'è, sta nella stessa grammatica e la voce dichiara almeno una riga
    coprente: una fusione che non nomina cosa fonde non è verificabile. Che la fusione resti
    decidibile in una lettura non lo decide il validator — è lettura, e sta nel veto.
- [ ] **Dare alla mappa il formato che il validator consuma: dati separati dalla prosa.** La Fase 1c
  consegna `support/CLAUSE-ROW-MAP.md`, 205 clausole in tabelle markdown più un centinaio di righe di
  prosa. Il validator non deve parsare markdown: estrarre i record — id, sede, commit d'introduzione,
  commit dell'ultima riscrittura, righe coprenti, ancoraggio — in un file tabellare sotto `support/`,
  e lasciare nel `.md` regola di conteggio, ancoraggi irrisolti, ancoraggi che risolvono sul brief,
  verifica del campione e divergenze di blame, che nessuno script legge. Il taglio è **dati contro
  prosa, non per sezione di `SKILL.md`**: le due interrogazioni sono «quali righe coprono questa
  clausola» e «quali clausole sono scoperte», e nessuna delle due è per sezione. Da fare qui e non in
  1c, perché il formato lo detta il consumatore e il consumatore è questo validator.
  - **Sede e commit sono rigenerabili da git**, quindi li emette lo script invece di fidarsi delle
    celle scritte a mano. Il commit dell'ultima riscrittura è quello che ha cambiato il **testo** della
    clausola, **non `git blame` della riga**: le 16 divergenze in fondo alla mappa sono righe
    rimandate a capo da una modifica vicina, e un ri-ancoraggio dedotto dal blame azzererebbe `×k` su
    righe che nessuno ha toccato.
  - **L'ancoraggio non è rigenerabile** e si mantiene a mano: per nove righe su undici è un'inferenza,
    e i quattro `unresolved` sono fallimenti registrati, non celle da riempire.
  - **Riparare i tre riferimenti che la migrazione del registro ha reso stali**, già che il file si
    riapre qui: la nota di `C-157` e quella su `R-006` m1 negli *Unresolved anchors* rimandano a
    *Difetti degli artefatti mai registrati* e *Formulazioni riscritte*, che ora vivono in
    `CONSENSUS-CON-5.REPORT.md`; la nota di `C-106` rimanda a *Da popolare*, ora *To populate*. La
    Fase 1c non poteva toccarli senza attraversare due volte lo stesso confine.
- [ ] Implementare lo **scarto per voce**: la voce cade, il documento resta, ogni scarto esce con il
  campo mancante e il motivo in forma leggibile dal report. **Nessuna rigenerazione.**
- [ ] Test del validator su artefatti reali: `PLAN-CC-CON-4.IMPROVEMENT.md` deve produrre voci
  parzialmente conformi, `PLAN-CX-CON-4.IMPROVEMENT.md` deve produrre **zero** voci conformi. Sono la
  fixture negativa che il progetto già possiede.

**Verifica:** `make test` verde; il validator sui due artefatti di CON-4 dà l'asimmetria attesa; il
residuo dichiarato è che il validator verifica **che** il riferimento esista, non che **sostenga**
l'affermazione — stessa spaccatura `validator`/`lettura` delle righe del registro.

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
- [ ] **Riempire lo slot `gen` di `Misurato su` nelle undici righe del registro** dai dati della
  mappa. Oggi portano tutte `gen unrecorded`: modello ed effort di CON-1…CON-5 non esistono in nessun
  artefatto, e `CC`/`CX` nominano l'harness, non il modello. Se la mappa non riesce a ricostruirli, le
  celle restano `unrecorded` e lo si dichiara una volta invece di lasciarlo sembrare una svista.

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
  righe attive           11 → 16
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

**Precondizioni:** Fasi 1a, 1b, 1c. **Chiamate provider:** **9** — 2 generazione, 2 `improve`,
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
undici, e toccarlo prima del ciclo che verifica per la prima volta `R-010` e `R-011` aggiungerebbe un
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
- [ ] **Decidere i quattro ancoraggi `unresolved`** che la mappa registra come fallimenti: `R-001` m1,
  la componente `9aa2586` di `R-005`, la seconda metà di `R-006` m1 e la componente `9aa2586` di
  `R-006`. Per ciascuno una sola delle due mosse: lo skill acquista la clausola che la riga
  presuppone, oppure la riga si riscrive per smettere di pretendere ciò che lo skill non dice. È
  lavoro di questa fase perché è la stessa decisione della potatura letta al contrario — lì si toglie
  testo coperto da una riga, qui c'è una riga che copre testo inesistente. Il caso netto è `R-006` m1:
  il requisito è stato aggiunto alla riga dopo CON-5 **perché** `CX` non dichiarava il riuso, quindi
  un verdetto contro quel membro sembra una regressione dello skill senza esserlo.
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
