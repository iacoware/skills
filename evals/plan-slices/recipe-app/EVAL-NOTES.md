# Note di valutazione

Diario empirico per iterare su `plan-slices`. Il riferimento semantico unico è
[`REFERENCE-PLAN.md`](REFERENCE-PLAN.md); questo file non introduce criteri normativi.

## Valutazioni

| Piano | Deviazione osservata | Giudizio | Causa ipotizzata nello skill |
|---|---|---|---|
| `PLAN-CX-CON-4.md` | Themes compresse; create/edit atomizzati; auth e release troppo tardi o assenti | Da correggere | Split/merge e chiusura di `NOW` non abbastanza vincolanti |
| `PLAN-CC-CON-2.md` | Contraddizione embedding non esposta; SSRF e integrità mancanti; release marcata enabler | Da correggere | Enabler, conflitti nelle fonti e boundary safety non abbastanza espliciti |
| `PLAN-CC-CON-4.md` | Contraddizione sull'embedding della query non esposta e asserita nella slice 4; copia-incolla separato dal fallimento che recupera; foto prima della chiusura dell'acquisizione; creazione di ricettari in `NOW` | Da correggere | Sweep delle contraddizioni assente; breadth-before-depth prevale sulla via di recupero; nessuna regola "un adapter si apre una volta sola" |
| `PLAN-CX-CON-4.md` | Skeleton senza database, con provisioning spostato nell'enabler rischioso; tema Consultazione compresso e mai consegnato; pipeline foto aperta in due slice; stesso concetto in `LATER` e `OUT-OF-SCOPE` | Da correggere | Skeleton descritto come "minimo" senza dire cosa deve attraversare; copertura inversa dei temi ed esclusività degli orizzonti non verificate |

## Iterazioni dello skill

| Evidenza | Modifica provata | Esito |
|---|---|---|
| Confronto `PLAN-CX-CON-4.md` / `PLAN-CC-CON-2.md` | Aggiunti audit split/merge, recovery, enabler diagnostici, breadth-before-depth, conflitti espliciti, safety verificabile e `Release: delivery` | Da verificare con nuove generazioni indipendenti |
| Confronto `PLAN-CC-CON-4.md` / `PLAN-CX-CON-4.md` | Skeleton ridefinito come prova di connettività dell'infrastruttura decisa (datastore via driver reale + migrazione non di dominio), anti-pattern `Hollow walking skeleton`, invariante 1 e slice 1 del reference riscritti | Da verificare con nuove generazioni indipendenti |

## Schema per le prossime valutazioni

- **Piano:** artefatto immutabile in `results/` e versione esatta dello skill.
- **Deviazione:** differenza rispetto a temi, confini o invarianti di `REFERENCE-PLAN.md`.
- **Giudizio:** difetto, alternativa accettabile o dubbio dell'oracolo.
- **Causa:** istruzione mancante, ambigua o troppo prescrittiva nello skill.
- **Modifica:** cambiamento minimo provato nello skill.
- **Esito:** comportamento osservato nella generazione indipendente successiva.
