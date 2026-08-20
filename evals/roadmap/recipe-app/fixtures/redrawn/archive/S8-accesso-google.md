# S8 — Accesso con Google e ricettario dell'utente

← [Register](../roadmap.md#now)

**Outcome:** Si entra con il proprio account Google e il ricettario corrente diventa quello
dell'utente autenticato.

**Requested by:** `sources/goal.md` (Auth — decisione presa: Google OAuth),
`sources/tech-choices.md` (Auth.js NextAuth v5), `sources/concepts.md` (User, Cookbook).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

La prima persona reale: entra con Google, senza password e senza email, e quello che vede è suo.

## Includes

- Auth.js con provider Google e sessione persistita su Postgres.
- Tabella `User` con `id` ed `email`.
- La sostituzione, dentro il solo `CurrentCookbook`, del ricettario configurato con quello del membro
  autenticato: il seam dichiarato in `S3` viene chiuso qui e in nessun altro punto.
- `Cookbook` con `creatorId` e `visibility` privata, pronta al valore pubblico che resta candidato.

## Verification

Due account Google diversi vedono due elenchi diversi, e nessuno dei due vede le ricette dell'altro,
nemmeno cercando. Nessuna rotta risponde con dati senza una sessione valida. Il codice che risolveva
il ricettario configurato non esiste più: un `grep` non trova una seconda strada per lo scope, e i
test di `S3` passano invariati senza che le righe precedenti siano state riscritte.

## Learning target

Se il seam dichiarato in `S3` regge davvero la sostituzione, cioè se rimandare l'identità è costato
solo quello che la mappa aveva messo a preventivo.

## Excludes

- Inviti, membership multipla e passaggio da un ricettario all'altro: sono di `S9`.
- Passkeys, ruoli e permessi per azione: restano candidati o esclusi.
- Consent screen di produzione e redirect del dominio finale: sono di `S11`.

## Open questions

- Al primo accesso il ricettario personale nasce da solo, o lo crea l'utente scegliendone il nome?
  Le sorgenti dicono che ogni ricettario ha un creator, ma non dicono chi crea il primo.
