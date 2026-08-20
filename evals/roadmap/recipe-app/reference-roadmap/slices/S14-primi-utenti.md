# S14 — Messa in mano ai primi utenti

← [Register](../roadmap.md#now)

**Outcome:** Famiglia e amici usano l'app sul dominio definitivo, ognuno sul proprio ricettario.

**Requested by:** `sources/goal.md` § Visione, § Principi guida
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Famiglia e amici, ognuno sul proprio ricettario e dal proprio telefono.

## Includes

- Il dominio definitivo.
- Il client OAuth Google fuori dalla modalità di test, con la schermata di consenso approvata.
- La rimozione del corpus di seed.
- Un salvataggio del database che qualcuno ha provato a ripristinare almeno una volta.

## Verification

Una persona che non ha mai visto l'app entra dal link d'invito, aggiunge una ricetta da un URL e la
ritrova cercandola a parole sue.

## Learning target

Che l'app regga l'uso reale con la macchina che si spegne: che il cold start sia un fastidio e non
un limite, il che è anche ciò che decide la candidate della macchina sempre calda.

## Excludes

- La macchina sempre calda.
- Monitoraggio e avvisi.
- L'apertura oltre le persone invitate: i ricettari pubblici sono una candidate.

## Open questions

—
