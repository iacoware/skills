# Eval `plan-slices` / recipe-app

Scenario di riferimento: pianificazione greenfield di un ricettario privato condiviso, con ricerca
semantica cross-lingua come differenziatore.

## Struttura

| Percorso | Ruolo |
| --- | --- |
| `sources/` | input passati all'agent: `goal.md`, `concepts.md`, `arch-choices.md`, `tech-choices.md` |
| `IDEAL-SLICES.md` | oracolo: slice e ordine desiderati, scritti a mano |
| `CRITERI-GIUDIZIO.md` | oracolo: criteri di valutazione e osservazioni per piano |
| `expectations.json` | oracolo eseguibile (ancora da scrivere: la skill è in iterazione) |
| `results/` | piani generati, uno per esecuzione |

Input, oracolo e output sono separati; i tre file di oracolo stanno alla root dello scenario perché
si aggiornano insieme quando cambia l'intento.

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
| `PLAN-CC-SENZA.md` | Claude Code | no |
| `PLAN-CX-CON.md` | Codex | sì, versione pre-repo |
| `PLAN-CX-CON-2.md` | Codex | sì, versione pre-repo |
| `PLAN-CX-CON-3.md` | Codex | sì, versione pre-repo |
| `PLAN-CX-SENZA.md` | Codex | no |

Dalla prossima esecuzione annota il commit esatto, altrimenti i confronti non sono riproducibili.

## Note

I piani in `results/` sono artefatti immutabili: non correggerli. I link relativi al loro interno
(es. `../goal.md`) puntavano al progetto originale e qui non risolvono.
