# S9 — Accesso con Google

← [Register](../roadmap.md#now)

**Outcome:** Si entra con il proprio account Google e il ricettario corrente diventa quello
dell'utente autenticato, senza che le righe già consegnate cambino.

**Requested by:** `goal.md` § Auth — decisione presa: Google OAuth; `tech-choices.md` § Auth;
il seam di ricettario corrente aperto da `S3`.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi userà l'app: da qui le ricette sono sue, riconosciute a ogni accesso da qualunque
dispositivo.

## Includes

- Auth.js con provider Google, sessioni e tabelle di Auth.js su Postgres.
- Il risolutore del ricettario corrente passa da configurato ad autenticato: stesso punto,
  sorgente diversa.
- Al primo accesso l'utente ottiene un ricettario personale senza che gli venga chiesto nulla.
- Ogni rotta e ogni azione su ricette e foto richiede una sessione.
- Uscita dall'account, e dismissione del ricettario seed usato fino a qui.

## Verification

Due account Google diversi vedono due elenchi diversi sull'ambiente deployato. Senza sessione
ogni rotta di ricetta e di foto rifiuta, verificato chiamando direttamente l'API e non solo
dall'interfaccia. Un test dimostra che la sessione è nominata solo dal risolutore e da nessuna
query di ricette, cioè che la sostituzione è avvenuta in un punto solo. Dopo il primo accesso
esiste un ricettario dell'utente, e la ricerca al suo interno continua a comportarsi come in
`S8`.

## Learning target

Che sostituire uno scope configurato con uno autenticato costi un solo punto di codice — cioè
che il seam messo in `S3` fosse nel posto giusto.

## Excludes

- Inviti, appartenenze e ricettari multipli: sono di `S10`.
- Ruoli e permessi granulari: fuori scope dichiarato.
- Passkeys, email e password, magic link: fuori scope o candidati.

## Open questions

- —
