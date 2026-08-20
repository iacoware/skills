# S13 — Tag e tempo derivati per la ricerca

← [Register](../roadmap.md#now)

**Outcome:** Cercando «vegano» escono ricette che quella parola non la contengono.

**Requested by:** `sources/goal.md` § Ricerca (MVP), `sources/concepts.md` § Recipe
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi cerca «vegano» e si aspetta ricette che quella parola non la scrivono da nessuna parte.

## Includes

- La derivazione best-effort di tag e tempo dal JSON-LD quando c'è e dal modello quando non c'è.
- Campi opzionali, mai chiesti all'utente, la cui assenza non blocca niente.
- Il testo indicizzato esteso a tag e tempo quando ci sono.

## Verification

Una ricetta che non contiene la parola «vegano» compare cercando «vegano» quando il tag è stato
derivato; una ricetta senza tag continua a essere trovata come prima.

## Learning target

Che i campi derivati aggiungano alla ricerca segnale e non rumore.

## Excludes

- I filtri strutturati per tag e tempo: sono una candidate, e questi campi esistono perché diventino
  abilitabili senza migrazione.
- Chiedere o far correggere i tag all'utente.

## Open questions

—
