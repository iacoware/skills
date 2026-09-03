# S6 — Ricerca semantica cross-lingua nel ricettario

← [Register](../roadmap.md#now)

**Outcome:** Scrivo "cena leggera" o "pomodoro" e ottengo le ricette pertinenti del ricettario
corrente, comprese quelle scritte in un'altra lingua.

**Requested by:** `sources/goal.md` § Ricerca e § Differenziatore; `sources/concepts.md` §
Ricerca (MVP); modello scelto da `S1`.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi prova l'app sull'ambiente non di produzione: con qualche decina di ricette in italiano e in
inglese, le ritrova per intento invece che scorrendo l'elenco.

## Includes

- Colonna `embedding` di tipo `vector` su `Recipe` con indice HNSW, in migrazione.
- Generazione dell'embedding dentro la pipeline di add, come passo suo nella progress bar, da
  `nome + ingredienti + preparazione` più `tag + tempo` quando ci sono; questa riga possiede
  quel passo per tutti gli ingressi — link, testo, e ogni ingresso futuro.
- Backfill delle ricette salvate prima di questa riga, eseguibile a comando.
- Una ricetta il cui embedding fallisce si salva lo stesso, resta leggibile, ed è recuperabile
  dal backfill: l'indice non blocca il dato.
- Ricerca: embedding della query a runtime, similarità su pgvector filtrata dal
  `currentCookbook`, risultati ordinati per distanza con una soglia oltre la quale non si mostra
  nulla.
- Campo di ricerca in home, con lo stato vuoto che dice che non è stato trovato niente.

## Verification

- Una ricetta salvata in inglese esce cercando "pomodoro" in italiano, senza che niente sia
  stato tradotto.
- Una query di intento — "cena leggera" — restituisce ricette plausibili e non l'intero
  ricettario.
- Una ricetta di un altro ricettario non compare mai fra i risultati.
- È dichiarato il tempo della ricerca a schermo, comprensivo della chiamata di embedding della
  query, misurato anche sulla prima richiesta dopo una sospensione della macchina.
- Una ricetta appena aggiunta è ricercabile senza nessun passo manuale; una salvata con
  embedding fallito compare dopo il backfill.
- Il log delle chiamate mostra una chiamata di embedding per ricerca e nessuna per l'apertura
  dell'elenco o di una ricetta.

## Learning target

Che la sola ricerca semantica basti a ritrovare le ricette del proprio ricettario, cross-lingua
compreso, con la latenza di una chiamata esterna dentro ogni query — è il differenziatore che
`S1` ha misurato in laboratorio, qui messo davanti a un utente e alla ricerca come unico modo
di trovare qualcosa.

## Excludes

- Filtri per tag e tempo e ricerca full-text ibrida: candidati, non MVP. I campi si popolano da
  `S4`, così restano abilitabili senza migrazione.
- Ricerca su più ricettari: candidato; qui lo scope è sempre e solo quello corrente.
- Rigenerazione dell'embedding dopo una modifica: `S9`, che apre la modifica.

## Open questions

- —
