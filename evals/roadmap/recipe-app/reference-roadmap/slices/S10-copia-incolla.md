# S10 — Copia-incolla del testo di una pagina

← [Register](../roadmap.md#now)

**Outcome:** Si incolla il testo di una pagina che l'app non riesce a scaricare e la ricetta si
salva.

**Requested by:** `sources/goal.md` § Visione, `sources/concepts.md` § Pipeline di estrazione
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi ha davanti una pagina che l'app non riesce a scaricare: paywall, siti che si disegnano in
JavaScript.

## Includes

- Il campo in cui incollare il testo e la pulizia del contenuto.
- Lo stesso motore e lo stesso schema di output di `S9`, senza passare dal JSON-LD.

## Verification

Incollando il testo di una pagina dietro paywall la ricetta si salva, e la si trova cercandola.

## Learning target

Che un modello estragga una ricetta da testo non strutturato restando dentro il budget di centesimi
per ricetta.

## Excludes

- OCR e foto di pagine di carta.
- L'estrazione da PDF.

## Open questions

—
