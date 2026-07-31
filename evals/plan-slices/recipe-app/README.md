# Eval `plan-slices` / recipe-app

Scenario di riferimento: pianificazione greenfield di un ricettario privato condiviso, con ricerca
semantica cross-lingua come differenziatore.

## Struttura

| Percorso | Ruolo |
| --- | --- |
| `sources/` | input passati all'agent: `goal.md`, `concepts.md`, `arch-choices.md`, `tech-choices.md` |
| `REFERENCE-PLAN.md` | unico oracolo semantico: temi, slice, confini, invarianti e tolleranze |
| `EVAL-NOTES.md` | diario delle valutazioni e delle modifiche provate nello skill |
| `results/` | piani generati, uno per esecuzione |

Input, riferimento, note e output sono separati. L'agent che genera il piano riceve solo `sources/`;
reference e note restano nascosti per non contaminare il forward-test.

In questa fase non esiste `expectations.json`: verrà derivato dagli invarianti stabili di
`REFERENCE-PLAN.md` dopo più generazioni indipendenti soddisfacenti. Il validator controlla soltanto
la struttura finché l'oracolo semantico continua a evolvere.

## Riesecuzione

1. Copia `sources/` in un progetto vuoto come `docs/`.
2. Chiedi all'agent un piano di delivery ad alto livello a partire da quei documenti.
3. Salva l'output in `results/` con la convenzione `PLAN-<agent>-<CON|SENZA>[-n].md`, dove
   `CON`/`SENZA` indica se la skill era installata.
4. Valida la struttura:

   ```bash
   python3 ../../../skills/plan-slices/scripts/validate_plan.py results/PLAN-....md
   ```

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
