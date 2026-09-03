# S1 — Spike: la ricerca cross-lingua regge su ricette vere?

← [Register](../roadmap.md#now)

**Outcome:** Un numero, non un'opinione: quale modello di embedding economico trova la ricetta
giusta quando la query è in una lingua diversa dal testo, misurato su ricette vere, e quanto
costa per ricetta e per query.

**Requested by:** `sources/goal.md` § Differenziatore — "la ricerca semantica cross-lingua è il
vero elemento distintivo… va tenuto come nord"; `sources/arch-choices.md` § Embeddings nomina
`text-embedding-3-small` come esempio ma pone "deve essere multilingue" come vincolo.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Includes

- Un corpus seed di ricette vere, raccolte dagli URL che useremmo davvero: metà in italiano,
  metà in inglese, con qualche piatto presente in entrambe le lingue.
- Un set di query scritte come le scriverebbe la famiglia: ingrediente singolo ("pomodoro"),
  intento vago ("cena leggera"), piatto per nome, e la stessa query nelle due lingue.
- Almeno due candidati confrontati, tra cui `text-embedding-3-small` che le fonti citano e un
  modello dichiaratamente multilingue.
- Uno script che embedda il corpus, esegue le query e stampa la posizione della ricetta attesa;
  nessuna app, nessuna UI.

## Verification

- Per ogni candidato è dichiarato il recall a 5 e a 10 sulle query cross-lingua, separato dal
  recall sulle query nella stessa lingua del testo.
- È dichiarato il costo per 1000 ricette indicizzate e la latenza dell'embedding di una query.
- È dichiarato quale candidato passa e quale no, con la soglia usata scritta prima di guardare
  i numeri.

## Learning target

Che un embedder economico trovi una ricetta in inglese quando la query è in italiano, con
qualità sufficiente a essere l'unico modo di cercare — è la promessa senza cui, dicono le
fonti, staremmo riscrivendo Mealie, e va confutata prima di costruirci sopra.

## Excludes

- Postgres e pgvector: qui il confronto si fa in memoria, l'indice HNSW è di `S6`.
- La UI di ricerca e lo scope al ricettario: `S6`.
- Il codice dello spike: non sopravvive nulla se non il corpus seed, riusabile come dato di
  prova, e la scelta del modello che `S6` eredita.

## Open questions

- —
