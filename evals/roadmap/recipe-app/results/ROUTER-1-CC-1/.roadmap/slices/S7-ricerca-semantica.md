# S7 — Ricerca semantica cross-lingua nel ricettario corrente

← [Register](../roadmap.md#now)

**Outcome:** Si cerca con parole proprie dentro il ricettario corrente e si trovano anche ricette
scritte in un'altra lingua.

**Requested by:** `sources/goal.md` (Differenziatore, Ricerca), `sources/concepts.md` (Ricerca —
MVP), `sources/arch-choices.md` (Datastore, Embeddings). Lo spike `S2` ne produce l'evidenza.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi prova l'app sull'ambiente non pubblico: scrive "cena leggera" o "pomodoro" e ritrova ricette che
non contengono quelle parole, e nemmeno quella lingua.

## Includes

- Colonna `vector` su `Recipe` con indice HNSW, e la migrazione che li crea.
- Generazione dell'embedding a ogni salvataggio, da `nome + ingredienti + preparazione` più `tags` e
  `prepTime` quando ci sono, per tutte e tre le vie d'ingresso: manuale, da link, da testo incollato.
- Backfill una tantum delle ricette già salvate dalle righe precedenti.
- Embedding della sola stringa cercata a ogni query; il corpus non viene mai ri-embeddato a runtime.
- Campo di ricerca in home, con i risultati scoped a `cookbookId` dal resolver `CurrentCookbook`.

## Verification

Una ricetta salvata in inglese esce cercando "pomodoro", e una ricetta senza la parola "leggera" nel
testo esce cercando "cena leggera": entrambe le query sono nell'elenco di prova di `S2`, misurate qui
su ricette vere salvate dalle righe precedenti. Una ricetta di un altro ricettario non esce: lo scope
si allarga in `S12` e non prima. Se
la generazione dell'embedding fallisce, la ricetta si salva comunque e resta invisibile alla sola
ricerca, e il log lo dice. La latenza della query di similarità sul corpus reale è dichiarata, e il
costo per ricerca è quello di una sola chiamata di embedding sulla query.

## Learning target

Se il cross-lingua misurato su corpus di prova regge su ricette vere, salvate dagli utenti con le
tre vie d'ingresso e non scelte da noi.

## Excludes

- Filtri per tag e tempo e ricerca ibrida: restano candidati. I campi si popolano già da `S4` e
  `S5`, così i filtri non chiederanno una migrazione.
- La ricerca che attraversa più ricettari: è di `S12`, che ne ha bisogno delle membership di `S9`.
- La ricerca non è mai scoped all'utente ma al ricettario corrente: chi sia l'utente lo decide `S8`,
  e lo scope per membership arriva con `S12`.

## Open questions

- Quale modello di embedding, sulla base di quanto `S2` misura. La scelta è dell'autore e le
  sorgenti citano un esempio, non una decisione.
