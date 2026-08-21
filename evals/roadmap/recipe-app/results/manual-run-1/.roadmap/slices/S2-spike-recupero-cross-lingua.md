# S2 — Spike: recupero cross-lingua misurato su corpus reale

← [Register](../roadmap.md#now)

**Outcome:** Sappiamo quale modello di embedding multilingue entro budget recupera davvero una
ricetta in inglese da una query in italiano, con quale recall e quale latenza su pgvector alla scala
prevista, e quanto costa indicizzare diecimila ricette una volta sola.

**Requested by:** `sources/goal.md`, la nota strategica «la ricerca semantica cross-lingua è il vero
elemento distintivo»; `sources/arch-choices.md`, che nomina `text-embedding-3-small` come esempio e
non come scelta.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

—

## Includes

- Un corpus di circa duecento ricette vere, raccolte da pagine pubbliche, metà in italiano e metà in
  inglese, con qualche coppia che è la stessa ricetta nelle due lingue.
- Un insieme di circa trenta query in italiano e in inglese, ciascuna con le ricette che una persona
  giudica pertinenti — comprese quelle descrittive che le fonti citano: «cena leggera», «pomodoro»,
  «vegano».
- Due o tre modelli multilingue candidati entro budget, fra cui `text-embedding-3-small` che le fonti
  nominano, misurati sullo stesso corpus e sulle stesse query.
- Il corpus caricato in una tabella usa-e-getta sul Neon deployato, con indice HNSW, indicizzando
  `nome + ingredienti + preparazione` come farà il prodotto.
- Recall@5, MRR e latenza p95 della query per ciascun modello; il costo di indicizzazione
  estrapolato a diecimila ricette.

## Verification

Per ogni candidato si sanno recall@5, MRR e p95 sullo stesso corpus e sullo stesso insieme di query,
e si sa quale modello è scelto e perché. Il rapporto dice esplicitamente se una query in italiano
recupera ricette scritte in inglese a un livello che una persona chiamerebbe funzionante, mostrando i
casi in cui non lo fa. Dice quanto costa indicizzare diecimila ricette una volta sola, e quanto costa
embeddare una query. Dice se la latenza cambia in modo apprezzabile fra scan sequenziale e HNSW a
questa scala, e a quale volume l'indice comincia a servire davvero.

## Learning target

Un modello di embedding multilingue entro budget fa funzionare il recupero cross-lingua abbastanza
bene da essere il differenziatore del prodotto, su pgvector alla scala prevista — che è l'affermazione
su cui poggia l'obiettivo intero.

## Excludes

- Nessuna interfaccia, nessuna entità `Recipe`, nessun embedding alla scrittura: sono della riga di
  ricerca, che consegna la promessa nel prodotto.
- Del codice dello spike non sopravvive niente tranne il corpus e l'insieme di query, che diventano la
  fixture di regressione che la riga di ricerca riusa; tabella usa-e-getta e script di misura vengono
  buttati.
- Nessuna ricerca ibrida e nessun filtro: sono candidati, e misurarli qui allargherebbe la domanda
  senza rispondere a quella che blocca.

## Open questions

—
