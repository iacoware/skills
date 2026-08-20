# S9 — Fallback LLM per le pagine senza dati strutturati

← [Register](../roadmap.md#now)

**Outcome:** Anche una pagina senza dati strutturati diventa una ricetta.

**Requested by:** `sources/arch-choices.md` § Estrazione contenuto,
`sources/goal.md` § Differenziatore
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi incolla il link di un sito che non pubblica dati strutturati, e che oggi su ogni altra app di
questo tipo non riceve niente.

## Includes

- Il rilevamento dell'assenza di JSON-LD sul percorso URL.
- La chiamata a un modello economico con output strutturato, validato con Schema e mai castato.
- Lo stesso salvataggio e la stessa barra di avanzamento di `S8`.

## Verification

Incollando l'URL di una pagina senza JSON-LD la ricetta si salva lo stesso, e le pagine che prima
producevano un errore ora producono una ricetta.

## Learning target

Quanto spesso il JSON-LD copra davvero i siti che i nostri utenti incollano: è la misura che decide
se il fallback è un caso limite o la strada principale.

## Excludes

- Il copia-incolla, che è `S10`.
- La scelta definitiva del modello: si cambia senza toccare la forma di questa riga.

## Open questions

—
