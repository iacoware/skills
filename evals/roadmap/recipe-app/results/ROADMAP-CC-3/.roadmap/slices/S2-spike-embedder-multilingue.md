# S2 — Quale embedder regge la ricerca cross-lingua

← [Register](../roadmap.md#now)

**Outcome:** Sappiamo quale modello di embedding multilingue adottare, con numeri su qualità
cross-lingua, latenza e costo alla scala dichiarata — oppure sappiamo che nessuno dei candidati
regge, che è una risposta altrettanto utile e molto più urgente.

**Requested by:** `sources/goal.md` § Differenziatore, che dichiara la ricerca semantica
cross-lingua il vero elemento distintivo, e `sources/arch-choices.md` § Embeddings, che pretende un
embedder «multilingue» ma ne nomina uno solo per esempio, senza sceglierlo.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

—

## Includes

- Un corpus seed di circa cento ricette reali, metà in italiano e metà in inglese, raccolte una
  volta e versionate come fixture.
- Un insieme di query in italiano con, per ciascuna, le ricette che dovrebbero comparire, incluse
  query che devono pescare ricette scritte in inglese: «pomodoro», «cena leggera», «dolce senza
  forno».
- Una soglia di qualità dichiarata prima di misurare, così che il verdetto non venga scelto dopo
  aver visto i numeri.
- Almeno tre candidati messi a confronto, fra cui quello che le sorgenti nominano come esempio.
- La misura eseguita su Postgres con pgvector e indice HNSW, non in memoria: la struttura è quella
  che il prodotto userà.

## Verification

Per ogni candidato sono scritti: recall@10 e MRR sulle query cross-lingua, la latenza p95 della
query di similarità sul corpus, e il costo per mille ricette indicizzate più il costo di una
singola query. C'è un candidato raccomandato con la ragione della scelta. Se nessuno supera la
soglia dichiarata, è scritto anche quello, con i numeri che lo dicono: è il risultato, non un
fallimento dello spike.

## Learning target

Se un embedder multilingue di commodity trovi davvero una ricetta scritta in inglese partendo da
una query in italiano, con quale qualità e a quale costo — cioè se il differenziatore su cui poggia
l'intero prodotto esiste, prima che cinque temi ci si appoggino sopra.

## Excludes

- Ogni integrazione nell'applicazione e ogni comportamento per un utente: la ricerca vera è una
  riga di prodotto a sé.
- Del codice di questo spike non sopravvive nulla oltre a due cose che la ricerca riusa: il corpus
  seed con le sue query attese, e il modello scelto con i suoi numeri.

## Open questions

- —
