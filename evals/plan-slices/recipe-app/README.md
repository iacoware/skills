# Eval `plan-slices` / recipe-app

Scenario di riferimento: pianificazione greenfield di un ricettario privato condiviso, con ricerca
semantica cross-lingua come differenziatore.

## Struttura

| Percorso | Ruolo |
| --- | --- |
| `sources/` | input passati all'agent: `goal.md`, `concepts.md`, `arch-choices.md`, `tech-choices.md` |
| `REFERENCE-PLAN.md` | unico oracolo semantico: temi, slice, confini, invarianti e tolleranze |
| `expectations.json` | artefatto generato dagli invarianti machine-readable del reference |
| `EVAL-NOTES.md` | diario delle valutazioni e delle modifiche provate nello skill |
| `results/` | piani generati, uno per esecuzione |

Input, riferimento, note e output sono separati. L'agent che genera il piano riceve solo `sources/`;
reference e note restano nascosti per non contaminare il forward-test.

`REFERENCE-PLAN.md` resta l'unica fonte normativa. Non modificare `expectations.json` direttamente:
la sezione `Machine-readable expectations` del reference lo genera e il suo hash rileva ogni drift.

## Riesecuzione

1. Copia `sources/` in un progetto vuoto come `docs/`.
2. Chiedi all'agent un piano di delivery ad alto livello a partire da quei documenti.
3. Salva l'output in `results/` con la convenzione `PLAN-<agent>-<CON|SENZA>[-n].md`, dove
   `CON`/`SENZA` indica se la skill era installata.
4. Dalla directory `evals/plan-slices`, verifica expectations, struttura e invarianti:

   ```bash
   make validate PLAN=PLAN-....md
   ```

   Usa `make help` per struttura soltanto, rigenerazione delle expectations, grader e test.

## Grader qualitativo

Il grader usa la rubric condivisa `grader-rubric.json`. Con Codex:

```bash
make grade PLAN=PLAN-....md GRADER=codex
```

Con Claude Code:

```bash
make grade PLAN=PLAN-....md GRADER=claude
```

Per eseguirli entrambi:

```bash
make grade-all PLAN=PLAN-....md
```

Entrambi eseguono il grader in una directory temporanea isolata, senza tool né permessi di scrittura,
e salvano `PLAN-....<grader>.GRADE.json` e `PLAN-....<grader>.SCORE.json`, senza sovrascriversi. Con
`grade` usa `MODEL=<modello>` per fissarlo; con `grade-all` usa `CODEX_MODEL` e `CLAUDE_MODEL`. Se
omessi vengono usati i default delle CLI. `grader-prompt` e `grader-score` restano disponibili per
debug o valutazioni prodotte esternamente.

Confronta versioni dello skill con stesso modello e configurazione e almeno 3–5 generazioni per
versione. Conserva score per asse, totale, critical failures e pass-rate deterministico: il solo
totale non spiega una regressione. Se cambia reference o rubric, rivaluta tutti i baseline.

## Esecuzioni

`Skill` è il commit di `skills/plan-slices` usato per generare il piano.

| Risultato | Agent | Skill |
| --- | --- | --- |
| `PLAN-CC-CON.md` | Claude Code | sì, versione pre-repo |
| `PLAN-CC-CON-2.md` | Claude Code | sì, commit non annotato |
| `PLAN-CC-SENZA.md` | Claude Code | no |
| `PLAN-CX-CON.md` | Codex | sì, versione pre-repo |
| `PLAN-CX-CON-2.md` | Codex | sì, versione pre-repo |
| `PLAN-CX-CON-3.md` | Codex | sì, versione pre-repo |
| `PLAN-CX-CON-4.md` | Codex | sì, commit non annotato |
| `PLAN-CX-SENZA.md` | Codex | no |

Dalla prossima esecuzione annota il commit esatto, altrimenti i confronti non sono riproducibili.

## Note

I piani in `results/` sono artefatti immutabili: non correggerli. I link relativi al loro interno
(es. `../goal.md`) puntavano al progetto originale e qui non risolvono.
