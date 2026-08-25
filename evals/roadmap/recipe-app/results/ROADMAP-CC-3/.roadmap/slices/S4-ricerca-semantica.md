# S4 — Ricerca semantica cross-lingua nel ricettario

← [Register](../roadmap.md#now)

**Outcome:** Si cerca a parole proprie e si ottengono le ricette del ricettario corrente ordinate
per pertinenza, comprese quelle scritte in un'altra lingua e che quella parola non la contengono.

**Requested by:** `sources/goal.md` § Ricerca e § Differenziatore; `sources/concepts.md` § Ricerca
per la forma della query; il modello scelto dallo spike sull'embedder.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi sviluppa e chi collauda, sull'ambiente di staging non pubblico. È la prima volta che il
differenziatore si può usare invece che misurare fuori dall'applicazione.

## Includes

- Colonna `embedding` di tipo `vector` con indice HNSW, in migrazione.
- Generazione dell'embedding al salvataggio e a ogni correzione, da `nome + ingredienti +
  preparazione`, più `tag` e `tempo` quando ci sono.
- Embedding della query al momento della ricerca, una chiamata per ricerca, dietro la stessa porta
  del modello scelto dallo spike.
- Query di similarità in una sola istruzione, filtrata dal resolver `currentCookbook`.
- Backfill degli embedding per le ricette già salvate, e il corpus seed dello spike caricato nel
  ricettario di staging.
- Comportamento dichiarato quando l'embedding manca: la ricetta esiste ed è leggibile, non è
  cercabile, e si rigenera senza perdere nulla.

## Verification

Cercando «pomodoro» compaiono ricette il cui testo è in inglese e non contiene quella parola.
Il recall misurato dentro l'applicazione, sul corpus e sulle query dello spike, è pari o migliore
di quello che lo spike aveva misurato fuori. Una ricetta di un altro ricettario non compare mai fra
i risultati. La latenza p95 della ricerca end-to-end, compresa la chiamata di embedding sulla
query, è misurata e scritta. Correggendo una ricetta, la ricerca successiva riflette il testo
nuovo.

## Learning target

Che il numero dello spike sopravviva all'applicazione reale — indice HNSW, filtro per ricettario e
chiamata di embedding sulla query compresi — e che quella chiamata a runtime non domini la latenza
della ricerca: è la lettura che questa mappa ha preso contro il divieto letterale delle sorgenti, e
questa riga la può smentire.

## Excludes

- I filtri strutturati su tag e tempo e la ricerca ibrida con il full-text: rimandati dalle
  sorgenti stesse, restano candidati in `LATER`. I campi però si popolano da subito, così
  abilitarli non chiederà migrazioni né lavoro retroattivo.
- La ricerca che attraversa più ricettari, fuori dall'MVP.
- La derivazione di tag e tempo, che appartiene alle righe di estrazione: questa riga li indicizza
  soltanto quando ci sono.

## Open questions

- —
