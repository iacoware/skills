# Ciclo di consenso — piano di implementazione

Piano per separare il ciclo di consenso dal grading system e automatizzarlo. Ogni fase è pensata per
una **sessione fredda separata**: dichiara le proprie precondizioni, le attività, come si verifica e
cosa produce. Una fase non presume il contesto conversazionale in cui la precedente è stata svolta.

Lo strumento e la sua ragione stanno in `CONSENSUS-WORKFLOW.md`; qui c'è solo il lavoro da fare.

## Decisioni già prese

Non si ridiscutono all'inizio di ogni sessione.

- Il ciclo attivo si chiama **consenso**; `review` resta il nome della sola fase 4 e dei suoi
  artefatti. Il grading system è **sospeso**, non cancellato.
- Dal ciclo CON-6 il payload di `improve` è **cieco e simmetrico**: entrambi i modelli valutano
  entrambi i candidati senza sapere quale hanno generato.
- La fase `ledger` entra nel ciclo automatizzato **insieme** a `improve` e `review`, non dopo.
- Il codice condiviso fra i due strumenti si estrae in `scripts/runtime/`.
- I prompt escono da `PROMPTS.md` e diventano l'unica sorgente sotto `prompts/`; `PROMPTS.md` resta
  scratchpad umano senza valore normativo.
- `support/AGENT-PLAN-MAP.md` tiene la mappa alias → piano → generatore ed è escluso da ogni payload.
- `CON-N` resta il contatore di ciclo negli artefatti; non si rinominano artefatti storici.
- La decisione su cosa applicare allo `SKILL.md` resta umana in ogni fase.
- **Le 15 unità di calibrazione già pagate non vanno conservate.** Riprenderle costerebbe più di
  quanto valgono: nessuna decisione attiva dipende da loro. Smettono quindi di essere un vincolo su
  qualunque fase, e possono essere cancellate quando sono d'intralcio; i 30 file sono tracciati in
  git, quindi restano recuperabili dalla storia.

## Fase 0 — Separazione dei due strumenti

**Precondizioni:** nessuna. **Chiamate provider:** zero.

- [x] Rinominare `EVAL-WORKFLOW.md` in `GRADING-EVAL-WORKFLOW.md` e seguire i riferimenti — commit
  `570e929`.
- [x] Creare `CONSENSUS-WORKFLOW.md` estraendo dal `Riesame del 2026-08-04` obiettivo, diagnosi,
  ciclo, buco e registro, gate e limiti.
- [ ] In `GRADING-IMPROVEMENTS-PLAN.md`, sostituire la sezione `Riesame del 2026-08-04` con un rimando
  a `CONSENSUS-WORKFLOW.md` più una sezione `Gate di ripresa` che **conserva** ciò che appartiene al
  grading: cosa congelare, test nullo, test di sensibilità, pre-registrazione, budget residuo, stop
  rule e varianza di generazione.
- [ ] Marcare la sospensione in testa a `GRADING-IMPROVEMENTS-PLAN.md` e sulle slice 3 e 5-8, e
  annotare che i vincoli nati per proteggere le 15 unità pagate — invalidazione retroattiva del
  resume, archiviazione sotto prefisso pilota prima di cambiare il prompt — non vincolano più niente.
- [ ] Creare `evals/plan-slices/README.md`: quale strumento è attivo, quale è sospeso, e la mappa dei
  tre gruppi di artefatti — grading, consenso, condivisi.

**Verifica:** `grep -rn "EVAL-WORKFLOW"` non trova riferimenti al vecchio nome; nessun file di codice
è stato toccato, quindi `make test` resta quello di prima.

**Output:** commit separati per rename, estrazione e README.

## Fase 1 — Prompt e procedura eseguibile

**Precondizioni:** Fase 0. **Chiamate provider:** zero.

- [ ] Creare `prompts/improve.prompt.md` estraendo da `PROMPTS.md` § *CREATE IMPROVEMENTS* e
  riscrivendolo su: `EVALUATION-BRIEF.md` al posto di `REFERENCE-PLAN.md`, eliminato da `6476f32`;
  payload cieco simmetrico; un solo documento per valutatore sull'unione dei difetti dei due
  candidati; divieto esplicito di leggere `support/`.
- [ ] Creare `prompts/review.prompt.md` da § *CREATE REVIEW 2*, adattato ai nuovi nomi degli
  artefatti.
- [ ] Creare `prompts/ledger.prompt.md`: per ogni riga di `REGRESSION-LEDGER.md`, verdetto più
  **citazione obbligatoria** del punto pubblicato (piano, slice, sezione) nella forma già usata dalle
  righe del ciclo CON-5. Nessun verdetto senza citazione.
- [ ] Aggiungere in testa a `PROMPTS.md` la nota che è uno scratchpad umano e che la sorgente
  normativa è `prompts/`.
- [ ] Creare `support/AGENT-PLAN-MAP.md` con le righe di CON-1…CON-5 e il formato per i cicli futuri.
- [ ] Rendere eseguibile la sezione *Il ciclo* di `CONSENSUS-WORKFLOW.md`: comandi esatti, nomi degli
  artefatti attesi, ordine, e cosa fare quando le due fasi `improve` divergono.
- [ ] Decidere e documentare la struttura di `results/CONSENSUS-CON-N.REPORT.md`: esito del validator,
  intersezione e disaccordi, verdetti del registro, elenco dei punti che richiedono lettura umana.

**Verifica:** i tre prompt non nominano `REFERENCE-PLAN.md`, `support/`, né i path o i nomi dei
generatori; i nomi degli artefatti citati coincidono con quelli della struttura del report.

**Rischio:** i prompt riscritti non sono mai stati eseguiti. È esattamente ciò che la Fase 2 misura.

## Fase 2 — Ciclo CON-6 manuale

**Precondizioni:** Fase 1. **Chiamate provider:** 6 se si generano i piani, 4 se si riusano i CON-5
esistenti (vedi `Open questions`). Richiede **autorizzazione esplicita** dopo il conteggio, per
`evals/AGENTS.md`.

- [ ] Generare o selezionare i due candidati e registrarli in `support/AGENT-PLAN-MAP.md`.
- [ ] `make validate` su entrambi.
- [ ] Eseguire `improve`, `review` e `ledger` a mano, copiando i prompt da `prompts/`.
- [ ] Scrivere `results/CONSENSUS-CON-6.REPORT.md` nella struttura decisa in Fase 1.
- [ ] Applicare allo `SKILL.md` ciò che si decide di applicare, una riga di registro per modifica.
- [ ] Correggere `prompts/` e `CONSENSUS-WORKFLOW.md` dove la procedura documentata non ha retto.

**Verifica:** il ciclo si chiude producendo tutti gli artefatti previsti senza intervento non
documentato. Ogni scostamento dalla procedura è annotato, perché è il difetto che la fase cerca.

**Output:** il ciclo eseguito, e la procedura corretta da automatizzare. È il gate della Fase 4:
automatizzare prima significa automatizzare una procedura non verificata.

## Fase 3 — Riorganizzazione del codice

**Precondizioni:** nessuna oltre la Fase 0; indipendente dalla Fase 2, che non tocca codice.
**Chiamate provider:** zero.

- [ ] Spostare `grader_runtime.py` e `orchestrator_artifacts.py` in `scripts/runtime/`; il resto del
  grading in `scripts/grading/`; aggiornare import, test, `Makefile` e documentazione.

**Verifica:** `make test` verde; nessun artefatto sotto `results/` modificato.

La riprendibilità delle 15 unità di calibrazione **non è un vincolo di questa fase**: se la
riorganizzazione la rompesse, non cambierebbe niente di ciò che si sta costruendo.

## Fase 4 — Orchestratore del ciclo

**Precondizioni:** Fasi 2 e 3. **Chiamate provider:** 6 per ciclo, dietro dry-run e `CONFIRM_SEND`.

- [ ] `scripts/consensus/` con il comando che rende i prompt da `prompts/`, compone i payload ciechi
  da una allowlist esplicita, invoca i due provider e scrive gli artefatti.
- [ ] Target `make consensus N=… PHASE=improve|review|ledger|report`, con `DRY_RUN`, `RESUME`,
  `CONFIRM_SEND` e registrazione degli hash come nel grading.
- [ ] Il join `report` è deterministico: nessuna chiamata, solo composizione degli artefatti prodotti.
- [ ] Test che nessun path sotto `support/` compaia in un prompt renderizzato.
- [ ] Test che il dry-run mostri esattamente due chiamate per fase e i target attesi.

**Verifica:** dry-run di tutte e quattro le fasi; un ciclo completo eseguito e ripreso con `RESUME=1`
senza nuove chiamate; confronto degli artefatti con quelli prodotti a mano nella Fase 2.

## Fase 5 — Generazione automatizzata

**Precondizioni:** Fase 4. **Chiamate provider:** 2 in più per ciclo.

- [ ] `PHASE=generate` produce i due candidati dalle sole fonti, con hash e resume, e aggiorna
  `support/AGENT-PLAN-MAP.md`.
- [ ] Annotare nel registro che lo strumento di generazione è cambiato: i piani CON-1…CON-N-1 nascono
  da sessioni interattive, non da chiamate headless.

## Fase 6 — Intersezione deterministica, opzionale

**Precondizioni:** almeno due cicli completi in Fase 4. **Da decidere dopo, non ora.**

Far produrre alla fase `review` un output strutturato minimo — id, titolo, categoria — così che
l'intersezione la calcoli il codice invece del modello, e il disaccordo sulla classificazione diventi
visibile. Riporta il rischio di non-conformità che il markdown libero elimina: si valuta solo se due
cicli mostrano che la classificazione fatta dai modelli è instabile.

## Open questions

- **In Fase 2 si generano due piani nuovi o si riusano `PLAN-CC-CON-5.md` e `PLAN-CX-CON-5.md`?**
  Riusarli costa due chiamate in meno e chiude il ciclo CON-5, che si era fermato alla generazione;
  ma sono stati generati prima di `87150d3` e `eb926bb`, quindi non possono verificare R-010 e R-011,
  le due righe che quei commit hanno introdotto e che sono ancora `da verificare`.
- **Quali modelli ed effort per le tre fasi?** In assenza di decisione si usano i default del
  grading — `gpt-5.6-sol`/`high` e `claude-opus-5`/`high` — che sono gli unici già esercitati contro
  provider reali.
