# S7 — Scrittura e correzione a mano

← [Register](../roadmap.md#now)

**Outcome:** Una ricetta si scrive a mano e si corregge in qualsiasi momento.

**Requested by:** `sources/goal.md` § Aggiunta ricetta
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi la ricetta la conosce già, e chi deve correggere un'estrazione imperfetta.

## Includes

- Un solo form, vuoto per l'inserimento e precompilato per la modifica.
- Nome, ingredienti e preparazione come testo libero, salvataggio immediato senza passi obbligatori.
- Il ricalcolo dell'embedding a ogni salvataggio.

## Verification

Si scrive una ricetta a mano, la si ritrova cercandola a parole proprie, la si modifica e la ricerca
segue la modifica.

## Learning target

Che lo stesso form regga inserimento e correzione: è la condizione che rende accettabile salvare
subito un'estrazione imperfetta invece di far rivedere l'estratto all'utente.

## Excludes

- Il motore di estrazione: quello che si scrive nel form si salva così com'è, senza JSON-LD e senza LLM.
- Parsing di quantità e unità: gli ingredienti strutturati sono fuori scope.
- Un passo di review dentro il flusso di aggiunta.
- Le foto, che sono `S11`.

## Open questions

—
