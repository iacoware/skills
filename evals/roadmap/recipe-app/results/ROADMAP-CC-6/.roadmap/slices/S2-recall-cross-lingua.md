# S2 — Recall cross-lingua degli embedding multilingue

← [Register](../roadmap.md#now)

**Outcome:** Sappiamo quale modello di embedding a listino trova una ricetta scritta in inglese
quando la query è in italiano, con quale recall, a quale costo e con quale latenza sul Postgres che
useremo — e quel modello è scelto.
**Requested by:** `goal.md` § Differenziatore ("la ricerca semantica cross-lingua è il vero elemento
distintivo … senza di essa staremmo riscrivendo Mealie") e `arch-choices.md` § Embeddings, che nomina
`text-embedding-3-small` come esempio e vincola solo il requisito "multilingue".
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

—

## Includes

- Un corpus di semina di alcune decine di ricette reali, prese da siti veri, per metà in italiano e
  per metà in inglese, con qualche altra lingua per campionare i limiti.
- Un elenco di query in italiano con i risultati attesi già scritti, comprese quelle che devono
  pescare oltre la lingua ("pomodoro" su ricette inglesi) e quelle vaghe che il differenziatore
  promette ("cena leggera").
- Due o tre modelli candidati a listino, fra cui `text-embedding-3-small`, embeddati sullo stesso
  testo che l'app indicizzerà: nome più ingredienti più preparazione, e la variante con tag e tempo
  in coda.
- Tabella di prova su Postgres con colonna `vector` e indice HNSW, dove misurare la query di
  similarità che l'app farà davvero.

## Verification

- Per ciascun candidato è scritto il recall sulle query cross-lingua e su quelle vaghe, con le
  query dove sbaglia riportate per esteso.
- È scritto se aggiungere tag e tempo al testo indicizzato cambia il recall, e di quanto: è quello
  che decide se vale la pena derivarli.
- È scritta la latenza della query di similarità con indice HNSW sulla scala prevista, e quanto ci
  mette la chiamata di embedding della query, che sta dentro il tempo di risposta della ricerca.
- È scritto il costo di embeddare diecimila ricette col modello scelto, confrontato con i ~$0.10 una
  tantum che `arch-choices.md` mette a bilancio.
- Il modello è scelto, con la dimensione della colonna `vector` che ne consegue.

## Learning target

Se un modello di embedding a listino tiene davvero la promessa cross-lingua sul testo di una ricetta
— che è il differenziatore su cui poggia l'intero prodotto — e quale.

## Excludes

- Qualunque interfaccia di ricerca e qualunque scrittura sulle tabelle di dominio: la ricerca vera è
  di S5, la scrittura dell'embedding in fase di add è di S3.
- La ricerca ibrida e i filtri strutturati, che restano candidati.
- Il corpus di semina e il codice di misura non sopravvivono allo spike: quello che passa in S3 è la
  scelta del modello, la dimensione della colonna e la definizione dell'indice.

## Open questions

- Nessuna.
