# Eval `plan-slices` / recipe-app

Scenario di riferimento: pianificazione greenfield di un ricettario privato condiviso, con ricerca
semantica cross-lingua come differenziatore.

## Struttura

| Percorso | Ruolo |
| --- | --- |
| `sources/` | input passati all'agent: `goal.md`, `concepts.md`, `arch-choices.md`, `tech-choices.md` |
| `REFERENCE-PLAN.md` | reference classificato: vincoli duri, preferenze, alternative ed esempi |
| `expectations.json` | artefatto generato dai soli vincoli duri meccanicamente verificabili |
| `EVAL-NOTES.md` | diario delle valutazioni e delle modifiche provate nello skill |
| `results/` | piani generati, uno per esecuzione |

Input, riferimento, note e output sono separati. L'agent che genera il piano riceve solo `sources/`;
reference e note restano nascosti per non contaminare il forward-test.

Le fonti definiscono la verità fattuale e prevalgono sul reference. Non modificare
`expectations.json` direttamente: la sezione `Machine-readable expectations` lo genera e il suo
hash rileva ogni drift.

## Riesecuzione

1. Copia `sources/` in un progetto vuoto come `docs/`.
2. Chiedi all'agent un piano di delivery ad alto livello a partire da quei documenti.
3. Salva l'output in `results/` con la convenzione `PLAN-<agent>-<CON|SENZA>[-n].md`, dove
   `CON`/`SENZA` indica se la skill era installata.
4. Dalla directory `evals/plan-slices`, verifica expectations, struttura e invarianti:

   ```bash
   make validate PLAN=PLAN-....md
   ```

   Usa `make help` per grading, confronti, calibrazione e test.

## Grader qualitativo

Il workflow canonico è documentato in [`../EVAL-WORKFLOW.md`](../EVAL-WORKFLOW.md). I comandi
principali sono:

```bash
make grade PLANS='PLAN-CX-CON-5.md PLAN-CC-CON-5.md' DRY_RUN=1
make compare BEFORE=PLAN-CX-CON-5.md AFTER=PLAN-CX-CON-6.md RESUME=1 DRY_RUN=1
make calibrate DRY_RUN=1
```

L'orchestrator usa entrambi i grader per default, rende modello ed effort espliciti, rifiuta
overwrite e gestisce preflight, resume, paired e adjudication. Il dry-run non richiede credenziali
e non scrive file; una run reale richiede `CONFIRM_SEND=1` oppure `SEND` su TTY.

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
