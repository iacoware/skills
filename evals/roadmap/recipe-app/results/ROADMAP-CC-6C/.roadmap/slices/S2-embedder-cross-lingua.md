# S2 — Quale embedder regge la ricerca cross-lingua

← [Register](../roadmap.md#now)

**Outcome:** Sappiamo quale modello di embedding multilingue trova una ricetta inglese da una query
italiana, con che qualità, a che costo, con che latenza e con che dimensione di vettore.

**Requested by:** `goal.md` §§ Differenziatore, Ricerca; `arch-choices.md` § Embeddings, che nomina
`text-embedding-3-small` come esempio e pone la multilinguità come vincolo, senza scegliere.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

—

## Includes

- Un corpus seed di circa 30 ricette reali raccolte a mano dai blog che l'app dovrà importare, metà
  in italiano e metà in inglese.
- Un set di circa 20 query in italiano scritte come le scriverebbe un utente, di cui almeno metà
  devono trovare ricette scritte in inglese: "pomodoro", "cena leggera", "torta senza burro".
- Almeno tre candidati confrontati, fra cui `text-embedding-3-small`, un modello più grande della
  stessa famiglia e un multilingue di un'altra famiglia.
- Il testo indicizzato è quello che `concepts.md` prescrive: nome, ingredienti e preparazione, più
  tag e tempo dove presenti.
- Similarità coseno calcolata fuori dal database: qui si misura il modello, non pgvector.

## Verification

- Per ciascun candidato sono scritti recall@5 e recall@10 sulle query cross-lingua, il costo per
  10.000 ricette, la latenza p95 della chiamata di embedding di una singola query e la dimensione
  del vettore.
- Il corpus, le query e il risultato atteso di ciascuna restano nel repository, così la misura è
  ripetibile e `S5` può rieseguirla dentro l'app.
- Il confronto dice esplicitamente se e di quanto la qualità cala fra query nella stessa lingua
  della ricetta e query in lingua diversa.

## Learning target

Se un embedder multilingue di mercato trova una ricetta inglese da una query italiana con qualità
sufficiente e a un prezzo trascurabile — cioè se il differenziatore su cui poggia l'intero prodotto
esiste, o se senza di esso resterebbe una riscrittura di Mealie.

## Excludes

- pgvector, indice HNSW e la ricerca vera: sono di `S5`.
- Traduzione delle query o delle ricette: mai, il punto è ottenerla senza tradurre niente.
- Ricerca ibrida e full-text come termine di paragone: candidato in `LATER`.
- Del codice dell'esperimento non sopravvive niente oltre al corpus, alle query e ai numeri.

## Open questions

- —
