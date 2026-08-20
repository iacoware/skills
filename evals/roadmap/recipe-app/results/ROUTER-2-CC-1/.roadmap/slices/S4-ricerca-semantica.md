# S4 — Ricerca semantica cross-lingua

← [Register](../roadmap.md#now)

**Outcome:** Si cerca a parole proprie e la ricetta esce anche se è scritta in un'altra lingua.

**Requested by:** `sources/goal.md` § Ricerca (MVP: solo semantica), § Differenziatore
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi ricorda cosa vuole mangiare ma non come si chiama la ricetta, e chi ha salvato ricette in una
lingua che non è quella in cui cerca.

## Includes

- Il campo di ricerca in home.
- L'embedding della query a ogni ricerca, con lo stesso modello usato per indicizzare.
- I risultati ordinati per similarità, con il testo che spiega perché sono lì.

## Verification

Cercando «cena leggera» compaiono ricette che quelle parole non le contengono; cercando «pomodoro»
compare una ricetta scritta in inglese, senza che nulla sia stato tradotto.

## Learning target

Che una ricetta si trovi descrivendola, anche fra lingue diverse: è la promessa su cui l'intero
prodotto si differenzia da quelli che esistono già.

## Excludes

- Filtri per tag e tempo, e ricerca full-text o ibrida: sono candidate.
- La ricerca oltre il ricettario corrente.

## Open questions

—
