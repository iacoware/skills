# Workflow di valutazione di `plan-slices`

## Stato

`scripts/orchestrate_grading.py` espone i target `grade`, `compare` e `calibrate` descritti qui.

Eseguire tutti i comandi dalla directory `evals/plan-slices`.

## Ruoli

- **Generatori:** Codex e Claude producono manualmente i piani. L'orchestrator non genera piani.
- **Grader:** Codex e Claude valutano ciascun piano quando `PROVIDER=both`, valore predefinito.
- **Orchestrator:** valida input, invoca i grader, deriva gli score, confronta iterazioni, prepara
  eventuale adjudication e gestisce resume/output immutabili.

## Workflow

### 1. Generare manualmente il baseline

Eseguire lo stesso prompt e usare le stesse fonti con entrambi i generatori. Salvare gli output in
`recipe-app/results/` senza modificarli, con agente e iterazione nel nome:

```text
PLAN-CX-CON-5.md  # generato da Codex
PLAN-CC-CON-5.md  # generato da Claude
```

Annotare il commit esatto di `skills/plan-slices` usato per ogni generazione. Il commit non deve
essere inferito dal `HEAD` corrente.

### 2. Controllare localmente i piani

Il preflight dell'orchestrator ripete la validazione. Il comando diretto resta utile per correggere
il processo di generazione prima di autorizzare provider esterni:

```bash
make validate PLAN=PLAN-CX-CON-5.md
make validate PLAN=PLAN-CC-CON-5.md
```

I piani salvati sono artefatti immutabili: una failure richiede una nuova generazione, non la
correzione manuale del file.

### 3. Ispezionare il grading assoluto

Eseguire sempre prima il dry-run:

```bash
make grade \
  PLANS='PLAN-CX-CON-5.md PLAN-CC-CON-5.md' \
  SKILL_COMMITS='PLAN-CX-CON-5.md=<commit> PLAN-CC-CON-5.md=<commit>' \
  DRY_RUN=1
```

Controllare file trasmessi, provider, modelli, effort e nomi degli artefatti. Il dry-run non verifica
autenticazione, non chiama provider e non scrive file.

### 4. Eseguire il grading assoluto

Dopo aver approvato il dry-run:

```bash
make grade \
  PLANS='PLAN-CX-CON-5.md PLAN-CC-CON-5.md' \
  SKILL_COMMITS='PLAN-CX-CON-5.md=<commit> PLAN-CC-CON-5.md=<commit>' \
  CONFIRM_SEND=1
```

Senza `CONFIRM_SEND=1`, l'orchestrator richiede di digitare `SEND` su un terminale interattivo. Per
ogni piano vengono prodotti grade e score Codex/Claude:

```text
<piano>.codex.v2.GRADE.json
<piano>.codex.v2.SCORE.json
<piano>.claude.v2.GRADE.json
<piano>.claude.v2.SCORE.json
```

### 5. Modificare lo skill e generare la nuova iterazione

Dopo una modifica a `plan-slices`, ripetere manualmente il punto 1 nelle stesse condizioni:

```text
PLAN-CX-CON-6.md
PLAN-CC-CON-6.md
```

Non confrontare piani prodotti da generatori, prompt o condizioni differenti come se isolassero il
cambiamento dello skill.

### 6. Confrontare le iterazioni Codex

Il confronto avviene tra iterazioni dello stesso generatore. Prima ispezionare la run:

```bash
make compare \
  BEFORE=PLAN-CX-CON-5.md \
  AFTER=PLAN-CX-CON-6.md \
  SKILL_COMMITS='PLAN-CX-CON-5.md=<commit-5> PLAN-CX-CON-6.md=<commit-6>' \
  RESUME=1 \
  DRY_RUN=1
```

Poi eseguirla:

```bash
make compare \
  BEFORE=PLAN-CX-CON-5.md \
  AFTER=PLAN-CX-CON-6.md \
  SKILL_COMMITS='PLAN-CX-CON-5.md=<commit-5> PLAN-CX-CON-6.md=<commit-6>' \
  RESUME=1 \
  CONFIRM_SEND=1
```

`compare` esegue in ordine:

1. grade assoluti di BEFORE e AFTER con entrambi i grader;
2. paired BEFORE→AFTER con Codex grader;
3. paired BEFORE→AFTER con Claude grader;
4. eventuale adjudication se scatta un trigger normativo.

`RESUME=1` riusa il baseline e qualunque altro artefatto completo, valido e compatibile; produce
quelli mancanti. Un artefatto parziale o stale interrompe il preflight senza overwrite.

### 7. Confrontare le iterazioni Claude

Ripetere lo stesso workflow sulla linea generata da Claude:

```bash
make compare \
  BEFORE=PLAN-CC-CON-5.md \
  AFTER=PLAN-CC-CON-6.md \
  SKILL_COMMITS='PLAN-CC-CON-5.md=<commit-5> PLAN-CC-CON-6.md=<commit-6>' \
  RESUME=1 \
  DRY_RUN=1

make compare \
  BEFORE=PLAN-CC-CON-5.md \
  AFTER=PLAN-CC-CON-6.md \
  SKILL_COMMITS='PLAN-CC-CON-5.md=<commit-5> PLAN-CC-CON-6.md=<commit-6>' \
  RESUME=1 \
  CONFIRM_SEND=1
```

### 8. Interpretare i risultati

- `.PAIRED.json`: fonte autorevole per la direzione `better`, `same` o `worse`.
- `.v2.SCORE.json`: qualità assoluta, soglie e critical-failure cap.
- `.v2.GRADE.json`: evidenza criterion-level da cui lo score è derivato in codice.
- `.ADJUDICATION.json`: disaccordo materiale da sottoporre a revisione cieca; non è una media.

Gli artefatti delle iterazioni precedenti alla rubrica v2 sono archiviati come `*.GRADE.old.json` e
`*.SCORE.old.json`: sono immutabili, prodotti da una rubrica diversa e non confrontabili con gli
score `.v2`.

Non dichiarare miglioramento usando soltanto la differenza tra score assoluti. Cercare coerenza della
direzione sia nella linea Codex sia nella linea Claude e registrare eventuali eccezioni adjudicate.

### 9. Riprendere una run interrotta

Rieseguire lo stesso comando con `RESUME=1`. Non cambiare input, modelli, effort o configurazione:

```bash
make compare BEFORE=PLAN-CX-CON-5.md AFTER=PLAN-CX-CON-6.md RESUME=1
```

La run verifica schema, scoring, metadata e hash prima di riusare un artefatto. Nessun risultato
viene sovrascritto o corretto automaticamente.

### 10. Calibrare l'evaluator quando cambia

Eseguire la calibrazione dopo modifiche a rubric, prompt, parser, scoring o CLI provider; non serve
per ogni nuova generazione dello skill.

```bash
make calibrate DRY_RUN=1
make calibrate CONFIRM_SEND=1
```

Il comando usa entrambi i grader, espande fixture e coppie da `fixtures/manifest.json` e scrive
`recipe-app/results/CALIBRATION.json`. Le metriche sono diagnostiche e non costituiscono gate finché
non vengono calibrate.

## Configurazione Make

I default vengono sempre materializzati nelle CLI provider:

```text
PROVIDER=both
CODEX_MODEL=gpt-5.6-sol
CODEX_EFFORT=high
CLAUDE_MODEL=claude-opus-5
CLAUDE_EFFORT=high
TIMEOUT=900
```

Override esplicito, per esempio:

```bash
make grade PLANS='PLAN-CX-CON-5.md' CODEX_MODEL=<model> CODEX_EFFORT=high DRY_RUN=1
```

Usare `SCENARIO=<directory>` per uno scenario diverso da `recipe-app` e
`CALIBRATION_REPORT=<path>` per cambiare il path del report. Non usare default impliciti delle CLI.

## Verifica locale

La suite non effettua chiamate di rete:

```bash
make test
```
