# Ciclo di consenso — piano di implementazione

Piano per separare il ciclo di consenso dal grading system abbandonato e automatizzarlo. Ogni fase è
pensata per una **sessione fredda separata**: dichiara le proprie precondizioni, le attività, come si
verifica e cosa produce. Una fase non presume il contesto conversazionale in cui la precedente è
stata svolta.

Lo strumento e la sua ragione stanno in `CONSENSUS-WORKFLOW.md`; qui c'è solo il lavoro da fare.

## Decisioni già prese

Non si ridiscutono all'inizio di ogni sessione.

- Il ciclo attivo si chiama **consenso**; `review` resta il nome della sola fase 5 e dei suoi
  artefatti.
- Il grading system è **abbandonato dal 2026-08-06**, non sospeso: non è sostenibile per il ritmo di
  evoluzione di uno skill e non è preciso al livello a cui servirebbe. Non torna. Il codice resta in
  git e non è mantenuto. **Non si spende tempo a curarne i documenti interni.**
- Dal ciclo CON-6 il payload di `improve` è **cieco e simmetrico**: entrambi i modelli valutano
  entrambi i candidati senza sapere quale hanno generato.
- Il ciclo è un **falsificatore, non un confermatore**. Lo stato del registro è `non smentita ×k`,
  non `tiene`. Non si aumenta il numero di generazioni per lato: la leva è il tempo, non il campione.
- **`improve` è bidirezionale**, con i campi `Regola esistente che non ha impedito il difetto` e
  `Costo`, e con la regola dura: se una clausola esistente è nominata, il rimedio di default è
  riformularla, e aggiungere righe richiede una ragione scritta.
- Un `IMPROVEMENT` non conforme al contratto del prompt si **rigenera** prima di `review`. Blocco
  duro, non warning.
- La fase `ledger` entra nel ciclo automatizzato **insieme** a `improve` e `review`, non dopo.
- I prompt escono da `PROMPTS.md` e diventano l'unica sorgente sotto `prompts/`; `PROMPTS.md` resta
  scratchpad umano senza valore normativo.
- `support/AGENT-PLAN-MAP.md` tiene la mappa alias → piano → generatore ed è escluso da ogni payload.
- `CON-N` resta il contatore di ciclo negli artefatti; non si rinominano artefatti storici. **CON-5
  non si riusa** nonostante sia un ciclo parziale: nove righe del registro e due citazioni testuali lo
  referenziano. Il prossimo ciclo è **CON-6**.
- **Modelli ed effort:** `gpt-5.6-sol` e `claude-opus-5`, entrambi a **`medium`**. È un confine di
  strumento rispetto a `high`, e va nella colonna `Misurato su`.
- La decisione su cosa applicare allo `SKILL.md` resta umana in ogni fase.
- **Le 15 unità di calibrazione già pagate non vanno conservate**, e più in generale nessun vincolo
  nato per proteggerle vincola più niente. I 30 file sono tracciati in git.
- **Pensionamento delle righe del registro: rinviato** il 2026-08-06. Il costo della fase `ledger`
  cresce in modo monotono; si affronta quando il contatore di recidiva lo rende visibile.

## Fase 0 — Separazione dei due strumenti

**Precondizioni:** nessuna. **Chiamate provider:** zero.

L'ambizione di questa fase è stata **ridotta** il 2026-08-06: la versione precedente prescriveva di
riscrivere internamente `GRADING-IMPROVEMENTS-PLAN.md` (52 KB) in tre sezioni curate, conservando i
due test, la pre-registrazione delle coppie, il budget residuo e la stop rule. Con il grading
abbandonato quella è manutenzione di un documento morto e non si fa.

- [x] Rinominare `EVAL-WORKFLOW.md` in `GRADING-EVAL-WORKFLOW.md` e seguire i riferimenti — commit
  `570e929`.
- [x] Creare `CONSENSUS-WORKFLOW.md` estraendo dal `Riesame del 2026-08-04` obiettivo, diagnosi,
  ciclo, buco e registro, gate e limiti.
- [x] Riscrivere `CONSENSUS-WORKFLOW.md` sull'esito della sessione di grilling del 2026-08-06:
  obiettivo asimmetrico, stato dell'evidenza, rischio di non-conformità, cricchetto misurato,
  confini di strumento, lapide del grading.
- [ ] **Banner in testa a `GRADING-IMPROVEMENTS-PLAN.md`, `GRADING-IMPROVEMENTS.md` e
  `GRADING-EVAL-WORKFLOW.md`:** «Abbandonato il 2026-08-06. Documento non mantenuto, conservato per
  la storia. Lo strumento attivo è `CONSENSUS-WORKFLOW.md`.» Nient'altro: **il corpo di quei
  documenti non si tocca**, incluse le loro `Open questions` e i riferimenti interni al `Riesame del
  2026-08-04`, che restano leggibili come documento storico.
- [ ] Creare `evals/plan-slices/README.md` come punto d'ingresso della directory, con **due** gruppi
  di artefatti invece di tre:
  - **attivo** — `CONSENSUS-WORKFLOW.md`, `CONSENSUS-WORKFLOW-PLAN.md`, `prompts/`, `support/`,
    `REGRESSION-LEDGER.md`, `NOTES.md`, `recipe-app/sources/`, `recipe-app/EVALUATION-BRIEF.md`,
    `recipe-app/results/PLAN-*` e i report di ciclo, `validate_plan.py` che vive nella skill,
    `evals/AGENTS.md`, il target `validate`;
  - **archiviato** — `GRADING-*.md`, `grader-rubric*.json`, `fixtures/`, `results/calibration-*/`,
    gli script di grading e i target `grade`/`compare`/`calibrate*`. Non mantenuti, non prerequisito
    di niente.

**Verifica:** `grep -rn "EVAL-WORKFLOW"` non trova riferimenti al vecchio nome; i tre documenti di
grading aprono con il banner; nessun file di codice è stato toccato, quindi `make test` resta quello
di prima.

**Output:** un commit per il banner, uno per il README.

## Fase 1 — Prompt e procedura eseguibile

**Precondizioni:** Fase 0. **Chiamate provider:** zero.

- [ ] Creare `prompts/improve.prompt.md` estraendo da `PROMPTS.md` § *CREATE IMPROVEMENTS* e
  riscrivendolo su: `EVALUATION-BRIEF.md` al posto di `REFERENCE-PLAN.md`, eliminato da `6476f32`;
  payload cieco simmetrico; un solo documento per valutatore sull'unione dei difetti dei due
  candidati; divieto esplicito di leggere `support/`; **i due campi bidirezionali** `Regola esistente
  che non ha impedito il difetto` e `Costo`; l'esclusione del walking skeleton, che oggi vive solo
  nel prompt e va dichiarata come restrizione di scope del ciclo.
- [ ] **Specificare il contratto di conformità in modo controllabile**: la lista esatta dei campi
  obbligatori per voce, e la regola che un documento privo di un campo si rigenera. Il contratto va
  scritto una volta e citato dal prompt, non duplicato.
- [ ] Creare `prompts/review.prompt.md` da § *CREATE REVIEW 2*, adattato ai nuovi nomi degli
  artefatti e con il campo aggiuntivo, per ogni voce condivisa, **quale dei due lati porta la
  formulazione operativa**. È il dato su cui si decide se la voce vale `intersezione` o `giudizio`.
- [ ] Creare `prompts/ledger.prompt.md`: per ogni riga di `REGRESSION-LEDGER.md`, verdetto più
  **citazione obbligatoria** del punto pubblicato (piano, slice, sezione) nella forma già usata dalle
  righe del ciclo CON-5. Nessun verdetto senza citazione.
- [ ] Aggiungere in testa a `PROMPTS.md` la nota che è uno scratchpad umano e che la sorgente
  normativa è `prompts/`.
- [ ] Creare `support/AGENT-PLAN-MAP.md` con le righe di CON-1…CON-5 e il formato per i cicli futuri.
- [ ] **Migrare `REGRESSION-LEDGER.md` alla nuova semantica**: stato `tiene` → `non smentita ×k` (le
  righe attuali partono da `×1`, misurate sul solo CON-5); colonna `Misurato su` estesa a modello ed
  effort; nuova `Origine: potatura`; annotare sulle righe `R-002`…`R-007` che l'origine `intersezione`
  è stata prodotta con prompt diversi da quelli di `prompts/` e con un lato non conforme.
- [ ] Rendere eseguibile la sezione *Il ciclo* di `CONSENSUS-WORKFLOW.md`: comandi esatti, nomi degli
  artefatti attesi, ordine, e cosa fare quando le due fasi `improve` divergono.
- [ ] Decidere e documentare la struttura di `recipe-app/results/CONSENSUS-CON-N.REPORT.md`: esito del
  validator, esito del gate di conformità, intersezione e disaccordi con il lato operativo di ogni
  voce condivisa, verdetti del registro, **i tre contatori** (righe di `SKILL.md`, difetti distinti,
  recidiva), elenco dei punti che richiedono lettura umana.

**Verifica:** i tre prompt non nominano `REFERENCE-PLAN.md`, `support/`, né i path o i nomi dei
generatori; i nomi degli artefatti citati coincidono con quelli della struttura del report; il
contratto di conformità elenca campi verificabili senza giudizio.

**Rischio:** i prompt riscritti non sono mai stati eseguiti. È esattamente ciò che la Fase 2 misura.

## Fase 2 — Ciclo CON-6 manuale

**Precondizioni:** Fase 1. **Chiamate provider:** **6** — due per `improve`, `review` e `ledger` —
più **2 di generazione**. Richiede **autorizzazione esplicita** dopo il dry-run e il conteggio, per
`evals/AGENTS.md`.

I piani CON-5 **non si riusano**: sono delle 11:57 del 2026-08-04, mentre `87150d3` è delle 23:11 e
`eb926bb` delle 23:30. Precedono entrambi i commit, quindi non possono verificare `R-010` e `R-011` —
le due righe ancora `da verificare`, ed entrambe correzioni di regressioni già occorse.

- [ ] Generare i due candidati con lo `SKILL.md` corrente e registrarli in
  `support/AGENT-PLAN-MAP.md`.
- [ ] `make validate` su entrambi.
- [ ] Eseguire `improve`, il gate di conformità, `review` e `ledger` a mano, copiando i prompt da
  `prompts/`.
- [ ] Scrivere `recipe-app/results/CONSENSUS-CON-6.REPORT.md` nella struttura decisa in Fase 1,
  contatori inclusi.
- [ ] Applicare allo `SKILL.md` ciò che si decide di applicare, una riga di registro per modifica,
  rispettando la regola dura di `improve` bidirezionale.
- [ ] Correggere `prompts/` e `CONSENSUS-WORKFLOW.md` dove la procedura documentata non ha retto.

**Verifica — due criteri distinti, ed è il secondo quello che conta:**

1. *Completamento.* Il ciclo si chiude producendo tutti gli artefatti previsti senza intervento non
   documentato. Ogni scostamento è annotato.
2. *Validità della tesi.* I due `IMPROVEMENT` hanno **specificità comparabile**, cioè l'intersezione
   è letterale e non una mappatura generico → operativo. È il primo test dell'ipotesi di *Lo stato
   dell'evidenza*; se fallisce, il filtro di consenso non ha la proprietà che gli si attribuisce, e
   automatizzarlo sarebbe automatizzare un'illusione. Vedi `Open questions`.

**Output:** il ciclo eseguito, la procedura corretta, e il primo dato sulla tesi. È il gate della
Fase 4 e della Fase 5.

## Fase 3 — Riorganizzazione del codice

**Precondizioni:** Fase 0; indipendente dalla Fase 2, che non tocca codice. **Chiamate provider:**
zero.

L'ambizione di questa fase è stata **ridotta** il 2026-08-06: `scripts/runtime/` esisteva per ospitare
il codice *condiviso fra i due strumenti*. Con un solo strumento in servizio non c'è niente da
condividere.

- [ ] Spostare in `scripts/consensus/` **solo** ciò che il ciclo di consenso userà davvero:
  invocazione provider, hashing, scrittura atomica e resume, estratti da `grader_runtime.py` e
  `orchestrator_artifacts.py`.
- [ ] Lasciare il resto del grading dov'è, come archivio, con i suoi test e i suoi target. Non si
  riorganizza codice non mantenuto.
- [ ] Aggiornare import, test, `Makefile` e documentazione di ciò che è stato spostato.

**Verifica:** `make test` verde; nessun artefatto sotto `recipe-app/results/` modificato.

La riprendibilità delle 15 unità di calibrazione **non è un vincolo di questa fase**.

## Fase 4 — Modularizzazione e pruning dello skill

**Precondizioni:** Fase 2. **Chiamate provider:** zero per la fase; la verifica costa un ciclo
(CON-7).

Va **dopo CON-6**, non prima. Potare prima significa scegliere cosa togliere in base a quanto una
clausola sembra ridondante leggendola, che è esattamente il tipo di giudizio che il ciclo esiste per
non fare. E anticipare la sola modularizzazione «tanto è neutra» è falso: sposta ciò che il modello ha
in contesto al momento di generare, quindi sposterebbe il confine di strumento **prima** del ciclo che
deve decidere `R-010` e `R-011`.

Stato di partenza: `SKILL.md` monolitico a **417 righe**, con tre rami d'ingresso — `Choose the
branch`, `Review an existing plan`, `Split, merge, or reorder an existing plan` — che caricano tutte e
417 comunque. La disclosure progressiva esiste già, ma solo per `assets/plan-template.md` e
`scripts/validate_plan.py`.

- [ ] **Precondizione non negoziabile: la mappa clausola → riga di registro**, con le clausole
  scoperte marcate come tali. Undici righe coprono 417 righe di skill, e il registro traccia i
  **commit**, non le clausole: dopo 18 commit di riscritture non è dato per scontato che la clausola
  introdotta da `d977043` esista ancora nella forma che la riga afferma. La mappa è anche l'output
  più utile della fase, indipendentemente da quanto si pota: dice quale parte dello skill non è
  sostenuta da nessuna previsione mai verificata.
- [ ] Modularizzare per ramo d'ingresso, così che un ramo non caricato non occupi contesto.
- [ ] Potare e fondere. **Ogni rimozione è coperta o scoperta:** coperta → la riga di registro
  esistente si riscrive e la previsione resta; scoperta → nasce una riga `Origine: potatura` con
  l'affermazione «la rimozione di X non fa ricomparire il difetto Y». Nessuna rimozione senza una
  delle due.
- [ ] Registrare il confine di strumento in `Misurato su` per tutte le righe attive.

**Verifica:** **CON-7**. La fase non si chiude quando lo `SKILL.md` è più corto: si chiude quando
CON-7 non ha smentito le righe di potatura.

## Fase 5 — Orchestratore del ciclo

**Precondizioni:** Fasi 2 e 3. **Chiamate provider:** 6 per ciclo, dietro dry-run e `CONFIRM_SEND`.

- [ ] `scripts/consensus/` con il comando che rende i prompt da `prompts/`, compone i payload ciechi
  da una allowlist esplicita, invoca i due provider e scrive gli artefatti.
- [ ] Target `make consensus N=… PHASE=improve|review|ledger|report`, con `DRY_RUN`, `RESUME`,
  `CONFIRM_SEND` e registrazione degli hash, del modello e dell'effort.
- [ ] **Il gate di conformità è codice, non giudizio**: un `IMPROVEMENT` privo di un campo
  obbligatorio fallisce la fase e va rigenerato prima che `review` possa partire.
- [ ] Il join `report` è deterministico: nessuna chiamata, solo composizione degli artefatti prodotti,
  contatori inclusi.
- [ ] Test che nessun path sotto `support/` compaia in un prompt renderizzato.
- [ ] Test che il dry-run mostri esattamente due chiamate per fase e i target attesi.

**Verifica:** dry-run di tutte e quattro le fasi; un ciclo completo eseguito e ripreso con `RESUME=1`
senza nuove chiamate; confronto degli artefatti con quelli prodotti a mano nella Fase 2.

## Fase 6 — Generazione automatizzata

**Precondizioni:** Fase 5. **Chiamate provider:** 2 in più per ciclo.

- [ ] `PHASE=generate` produce i due candidati dalle sole fonti, con hash e resume, e aggiorna
  `support/AGENT-PLAN-MAP.md`.
- [ ] Annotare nel registro che lo strumento di generazione è cambiato: i piani CON-1…CON-N-1 nascono
  da sessioni interattive, non da chiamate headless. È un confine di strumento.

## Fase 7 — Intersezione deterministica, opzionale

**Precondizioni:** almeno due cicli completi in Fase 5. **Da decidere dopo, non ora.**

Far produrre alla fase `review` un output strutturato minimo — id, titolo, categoria, lato operativo —
così che l'intersezione la calcoli il codice invece del modello, e il disaccordo sulla
classificazione diventi visibile. Si valuta solo se due cicli mostrano che la classificazione fatta
dai modelli è instabile.

## Open questions

- **Come si decide che due `IMPROVEMENT` hanno «specificità comparabile»?** È il criterio 2 della
  verifica di Fase 2, cioè il test dell'ipotesi portante, e oggi è formulato come giudizio. Serve
  almeno una regola grossolana e dichiarata prima di eseguire CON-6 — per esempio: una voce è
  operativa se cita un punto specifico di un candidato **e** enuncia un test binario. Deciderla
  *dopo* aver visto gli artefatti significa sceglierla per farla tornare.
- **Cosa si fa se CON-6 falsifica l'ipotesi**, cioè se i due lati restano asimmetrici anche con il
  gate di conformità? Le opzioni non sono equivalenti e cambiano tutto il piano a valle: (a) alzare
  la specificità richiesta nel prompt e ripetere, pagando un altro ciclo; (b) accettare che il
  consenso certifichi solo il **tema** e che ogni formulazione entri sempre come `giudizio`, il che
  rende `review` molto meno utile e ne mette in discussione le due chiamate; (c) cambiare uno dei due
  modelli. Va decisa **prima** di eseguire, altrimenti la si decide sotto l'influenza del risultato.
