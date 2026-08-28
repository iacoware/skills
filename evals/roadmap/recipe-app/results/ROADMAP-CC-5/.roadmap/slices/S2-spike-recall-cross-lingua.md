# S2 — Spike: recall cross-lingua degli embedding

← [Register](../roadmap.md#now)

**Outcome:** Numeri di recall cross-lingua su testo di ricetta vero per i modelli di embedding
candidati, e il nome del modello che vince con il suo costo.

**Requested by:** `arch-choices.md` (*Embeddings*) nomina `text-embedding-3-small` come esempio e non
sceglie, mentre `goal.md` (*Differenziatore*) fa della ricerca cross-lingua l'unica cosa che
distingue il prodotto.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

—

## Includes

- Un corpus di semi di circa 150 ricette vere prese da blog di cucina, metà in italiano e metà in
  inglese, salvate come testo grezzo nel repository.
- Una tabella di prova sul Postgres di staging, separata da qualunque tabella di dominio, con una
  colonna `vector` per modello candidato.
- Almeno due modelli di embedding cloud dichiarati multilingue, fra cui quello che le fonti
  nominano, ciascuno con il proprio costo per milione di token.
- Un insieme di query in italiano con gli hit attesi etichettati a mano, che contiene tre categorie:
  query il cui unico hit atteso è una ricetta in inglese ("pomodoro"), query di intento che non
  compaiono letteralmente in nessun testo ("cena leggera"), e query il cui segnale sta solo in un
  tag derivato ("vegano") e non nel testo della ricetta.
- Le stesse misure ripetute con e senza `tags` e `prepTime` concatenati al testo indicizzato.
- Confronto fra scan esatto e indice HNSW alla dimensione del corpus.

## Verification

Recall@5 e MRR sono dichiarati come numeri, per modello e per categoria di query, e la differenza
fra le due varianti del testo indicizzato è dichiarata anch'essa. Il tempo di una chiamata di
embedding di una query è misurato. Il modello scelto è nominato con il suo costo, e il documento
dice quale numero lo ha fatto scegliere. Se nessun candidato porta la ricetta in inglese nei primi
cinque per la query italiana, il risultato lo dice invece di scegliere comunque.

## Learning target

Se un modello di embedding cloud multilingue recupera davvero una ricetta scritta in inglese a
partire da una query in italiano su testo di ricetta reale — cioè se il differenziatore su cui posa
tutto il prodotto esiste — e se la sua tenuta dipende dai `tags` derivati, che sulle ricette scritte
a mano non ci sono.

## Excludes

- Nessun endpoint di ricerca, nessuna UI, nessuna scrittura sulle tabelle di dominio: S4 costruisce
  la ricerca vera.
- Nessuna riga della tabella `Recipe`: il corpus vive in una tabella di prova che sparisce con lo
  spike.
- Del codice dello spike non sopravvive niente tranne l'insieme di query etichettate, che S4 riusa
  come corpo di regressione.

## Open questions

- —
