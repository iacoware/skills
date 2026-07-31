# Note di valutazione

Diario empirico per iterare su `plan-slices`. Il riferimento semantico unico è
[`REFERENCE-PLAN.md`](REFERENCE-PLAN.md); questo file non introduce criteri normativi.

## Valutazioni

| Piano | Deviazione osservata | Giudizio | Causa ipotizzata nello skill |
|---|---|---|---|
| `PLAN-CX-CON-4.md` | Themes compresse; create/edit atomizzati; auth e release troppo tardi o assenti | Da correggere | Split/merge e chiusura di `NOW` non abbastanza vincolanti |
| `PLAN-CC-CON-2.md` | Walking skeleton include Postgres; contraddizione embedding non esposta; SSRF e integrità mancanti; release marcata enabler | Da correggere | Enabler, conflitti nelle fonti e boundary safety non abbastanza espliciti |

## Iterazioni dello skill

| Evidenza | Modifica provata | Esito |
|---|---|---|
| Confronto `PLAN-CX-CON-4.md` / `PLAN-CC-CON-2.md` | Aggiunti audit split/merge, recovery, enabler diagnostici, breadth-before-depth, conflitti espliciti, safety verificabile e `Release: delivery` | Da verificare con nuove generazioni indipendenti |

## Schema per le prossime valutazioni

- **Piano:** artefatto immutabile in `results/` e versione esatta dello skill.
- **Deviazione:** differenza rispetto a temi, confini o invarianti di `REFERENCE-PLAN.md`.
- **Giudizio:** difetto, alternativa accettabile o dubbio dell'oracolo.
- **Causa:** istruzione mancante, ambigua o troppo prescrittiva nello skill.
- **Modifica:** cambiamento minimo provato nello skill.
- **Esito:** comportamento osservato nella generazione indipendente successiva.
