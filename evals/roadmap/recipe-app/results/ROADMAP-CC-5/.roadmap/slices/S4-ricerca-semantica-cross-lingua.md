# S4 — Ricerca semantica cross-lingua

← [Register](../roadmap.md#now)

**Outcome:** Si scrive "pomodoro" o "cena leggera" nella ricerca e tornano le ricette del ricettario
corrente ordinate per significato, comprese quelle scritte in un'altra lingua.

**Requested by:** `goal.md` (*Differenziatore*, *Ricerca (MVP: solo semantica)*) e `concepts.md`
(*Ricerca (MVP)*); il modello lo nomina S2.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi prova l'app su staging: da qui ritrova una ricetta senza ricordarne il titolo, ed è la prima
volta che la promessa che distingue il prodotto è osservabile fuori da una misura.

## Includes

- Colonna `Recipe.embedding` di tipo `vector` e migrazione, mappata da Drizzle.
- Una porta Effect `Embedder` con l'adapter del modello che S2 ha scelto, così che il modello resti
  sostituibile senza toccare i punti di chiamata.
- L'embedding scritto alla creazione e riscritto a ogni modifica della ricetta, calcolato su
  `nome + ingredienti + preparazione`, più `tags` e `prepTime` quando presenti; è indice derivato,
  quindi un suo fallimento non impedisce il salvataggio della ricetta e lascia la ricetta
  ricercabile solo dopo la rigenerazione.
- Backfill delle ricette già scritte a mano in S3.
- Ricerca: una chiamata di embedding sulla query a ogni richiesta, poi similarità su Postgres con
  scan esatto filtrato dal resolver `CurrentCookbook`; nessun indice HNSW.
- Barra di ricerca in Home, stato vuoto e stato "nessun risultato" distinti.
- L'insieme di query etichettate che S2 lascia, girato come test di regressione contro l'app in
  esecuzione.

## Verification

Sulle query che S2 lascia, una query in italiano riporta la ricetta scritta in inglese fra le prime
cinque, chiesta all'app in esecuzione e non a uno script. Il p95 della richiesta di ricerca, chiamata
di embedding compresa, è misurato e dichiarato: se la chiamata esterna lo spinge oltre il tollerabile
il numero lo dice. Modificata una ricetta, la ricerca successiva ne cambia la posizione di
conseguenza. Una ricetta che sta in un altro ricettario non compare mai, neanche quando è il match
migliore in assoluto. Se l'embedding fallisce, la ricetta si salva lo stesso e non compare fra i
risultati finché non viene rigenerato.

## Learning target

Se la recall cross-lingua che S2 ha misurato sopravvive al testo di produzione — ricette come
arrivano davvero, e in questa riga senza `tags` derivati — e se embeddare la query dentro la
richiesta tiene la ricerca in una latenza accettabile.

## Excludes

- Nessun indice HNSW: le fonti dicono che a queste dimensioni lo scan è già di pochi millisecondi;
  l'indice è in `LATER`.
- Nessun filtro per tag o tempo e nessuna ricerca ibrida: le fonti li rimandano, e stanno in `LATER`.
- Nessuna ricerca su più ricettari: `LATER`.
- Nessun ordinamento configurabile e nessuna paginazione: centinaia di ricette per ricettario non li
  chiedono.

## Open questions

- —
