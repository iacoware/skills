# S9 — Aggiungi una ricetta incollando il testo

← [Register](../roadmap.md#now)

**Outcome:** Quando il link non è leggibile — paywall, sito che monta tutto in JavaScript — incolli
il testo della pagina e ottieni la stessa ricetta salvata.

**Requested by:** `goal.md` § Visione (copia-incolla come fallback); `concepts.md` § Pipeline di
estrazione, dove il testo incollato salta il JSON-LD.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi aggiunge ricette nel ricettario: è la via d'uscita a mano quando l'aggiunta da link non ce la
fa.

## Includes

- Campo di testo nel form di aggiunta, accanto al campo URL.
- Pulizia del testo incollato e instradamento diretto all'LLM di `S4`, saltando il JSON-LD.
- Stesso schema di output, stesso salvataggio, stesso embedding delle altre strade; `sourceUrl`
  resta vuoto.
- Progress con i soli passi che questa strada percorre.
- L'errore di `S3` su una pagina non leggibile propone il copia-incolla e porta lì l'utente.

## Verification

- Il testo copiato da una pagina dietro paywall produce una ricetta salvata con gli stessi campi
  dell'aggiunta da link.
- Un testo che non è una ricetta produce un errore, non una ricetta inventata.
- Un link fallito porta al copia-incolla senza far ricominciare l'utente da capo.
- La ricetta salvata per questa strada è trovata dalla ricerca semantica come tutte le altre.

## Learning target

Se lo stesso motore di estrazione regge un input incollato, senza HTML e senza structured data, e
se il rimando dal link fallito al copia-incolla chiude davvero il buco di paywall e siti
JS-heavy.

## Excludes

- OCR da foto e import da PDF: candidati in `LATER`.
- Import da file di altre app: candidato in `LATER`.
- Un motore di estrazione dedicato al testo: escluso, le fonti vogliono un solo motore.

## Open questions

- —
