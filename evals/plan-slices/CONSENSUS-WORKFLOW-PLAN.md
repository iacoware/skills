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
- [ ] **Sostituire in `GRADING-IMPROVEMENTS-PLAN.md` la sezione `Riesame del 2026-08-04`**, che oggi
  occupa dalla riga `### Riesame del 2026-08-04 — quale strumento serve davvero` fino a `**Limiti che
  restano in ogni percorso.** … guarda quali criteri, non quanti.`, esclusa la successiva `### Verifiche
  completate`. Sostituire l'intervallo per confine dichiarato, non a occhio. Al suo posto tre sezioni:
  - `### Perché è sospeso` — i numeri della sproporzione al 2026-08-04: `SKILL.md` a 13 commit contro
    i 33 di `evals/plan-slices`, 3.477 righe di Python, 1.466 di documenti, 26 criteri di rubric,
    21 chiamate già pagate, e nessun miglioramento allo `SKILL.md` derivato da uno score. La diagnosi
    completa rimanda a `CONSENSUS-WORKFLOW.md`.
  - `### Cosa resta congelato` — scala a cinque verdetti e severità del grade contract; matrice di
    calibrazione e metriche (slice 7); formula di scoring e cap (slice 8); adjudication (slice 6).
    Il codice resta in git: se il gate viene superato si riprende, altrimenti non è stato mantenuto.
  - `### Gate di ripresa` — il trigger, cioè una regressione realmente sfuggita al registro, e non
    l'ipotesi che possa sfuggirne una; poi, **conservati dalla sezione rimossa**, i due test nel loro
    ordine — test nullo dei falsi positivi e test di sensibilità dei falsi negativi — la
    pre-registrazione obbligatoria delle coppie, il budget residuo, la stop rule e la nota sulla
    varianza di generazione.
- [ ] Aggiornare la citazione che apre `## Stato implementazione — 2026-08-04`: rimanda al `Riesame`
  come nome del gate, che dopo la sostituzione non esiste più.
- [ ] Aggiungere un banner di sospensione dopo il titolo di `GRADING-IMPROVEMENTS-PLAN.md`: strumento
  attivo, data della sospensione, e l'istruzione di leggere prima questo piano. Estendere alla
  slice 3 il marcatore che oggi copre le sole slice 5-8.
- [ ] Annotare che i vincoli nati per proteggere le 15 unità pagate non vincolano più niente:
  `Rischio — invalidazione retroattiva` e `Vincolo operativo se il prompt cambia` nella slice 3, più
  ogni punto che subordina una modifica di prompt, rubric o contratto alla riprendibilità del resume.
- [ ] Ripulire le `Open questions` del piano di grading: la prima — se accettare il percorso del
  `Riesame` — è **decisa** il 2026-08-06; la seconda — quanti cicli valgono come gate — è **nulla**,
  perché il gate non è più un numero di cicli ma una regressione sfuggita. Le restanti sono dormienti
  dietro il gate. Aggiungere la conseguenza della rinuncia alle unità pagate: una ripresa
  ricollezionerebbe da zero, quindi la domanda sulle chiamate residue va riformulata su una matrice
  intera, non sulle 21 unità mancanti.
- [ ] Creare `evals/plan-slices/README.md` come punto d'ingresso della directory: quale strumento è
  attivo e quale sospeso, e la mappa dei tre gruppi di artefatti — **grading** (`GRADING-*.md`,
  `grader-rubric*.json`, `fixtures/`, `results/calibration-*/`, gli script di grading e i target
  `grade`/`compare`/`calibrate*`); **consenso** (`CONSENSUS-*.md`, `prompts/`, `support/`,
  `REGRESSION-LEDGER.md`, `NOTES.md`, `results/PLAN-*` e i report di ciclo); **condivisi** (`sources/`,
  `EVALUATION-BRIEF.md`, `validate_plan.py` che vive nella skill, `evals/AGENTS.md`, e il runtime che
  la Fase 3 estrarrà).

**Verifica:** `grep -rn "EVAL-WORKFLOW"` non trova riferimenti al vecchio nome; `grep -rn "Riesame del
2026-08-04"` non trova rimandi orfani; nessun file di codice è stato toccato, quindi `make test` resta
quello di prima.

**Output:** commit separati per rename, estrazione dal piano di grading e README.

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
