# S7 — Aggiunta da testo incollato

← [Register](../roadmap.md#now)

**Outcome:** Quando il link non è leggibile — paywall, sito che non dà niente — si incolla il
testo della pagina e la ricetta entra lo stesso.

**Requested by:** `goal.md` § Visione, che dichiara il copia-incolla il fallback per pagine
non leggibili; `concepts.md` § Pipeline di estrazione, dove il testo incollato salta il
JSON-LD e riusa lo stesso motore.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Sviluppatori e tester sull'ambiente di staging: nessuna pagina resta fuori dal ricettario per
colpa di un paywall, senza trascriverla a mano.

## Includes

- Ingresso a testo libero nel flusso di aggiunta, accanto al link.
- Lo stesso motore di `S6` — pulizia, modello, validazione con `Schema` — senza fetch e senza
  JSON-LD.
- Gli stessi passi di progresso di `S5` meno "scarico pagina", con gli stessi errori
  tipizzati.
- `sourceUrl` valorizzato solo se l'utente lo incolla, nessuna foto automatica: si aggiunge
  dalla pipeline di `S4`.

## Verification

Incollato il testo di una pagina a paywall, la ricetta si salva con gli stessi campi che
produce il percorso da link. Un testo che non è una ricetta produce un messaggio preciso e
nessun salvataggio. Il percorso non emette nessuna richiesta HTTP verso il sito d'origine,
verificabile dal log. Le voci di menu di aggiunta — link, testo, a mano — portano tutte a una
ricetta salvata.

## Learning target

Che il motore di estrazione regga input senza HTML attorno, cioè che link e incolla siano
davvero un motore solo e non due che si somigliano.

## Excludes

- OCR da fotografia di un libro: candidato.
- Import da file esportati da altre app: candidato.
- Riconoscimento automatico di ciò che l'utente incolla (link o testo): non serve, sono due
  campi distinti.

## Open questions

- —
