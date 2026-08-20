# S12 — Ricettario condiviso su invito

← [Register](../roadmap.md#now)

**Outcome:** Un link d'invito fa entrare un'altra persona nel ricettario, con gli stessi diritti.

**Requested by:** `sources/goal.md` § Condivisione, `sources/concepts.md` § Modello di condivisione
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

La famiglia e gli amici che il creatore del ricettario invita.

## Includes

- `Cookbook`, `Membership` e `Invitation`, con `creatorId` come unico ruolo.
- La creazione di un ricettario e il link o codice d'invito che, aperto da loggati, dà
  l'appartenenza.
- L'appartenenza a più ricettari e il concetto di ricettario corrente.
- Elenco, ricerca e aggiunta vincolati al ricettario corrente.

## Verification

Due account diversi vedono e modificano le stesse ricette dopo che il secondo ha aperto il link
d'invito; l'id di un ricettario di cui non si è membri risponde 404.

## Learning target

Che l'appartenenza al ricettario sia l'unico concetto di condivisione necessario, e che nessuna
delle righe già consegnate debba essere ripensata per accoglierlo.

## Excludes

- Ruoli e permessi granulari: sono fuori scope.
- Gruppi sopra i ricettari e ricettari pubblici: sono candidate.
- La ricerca su più ricettari.

## Open questions

—
