# S2 — Quale modello di embedding regge il cross-lingua

← [Register](../roadmap.md#now)

**Outcome:** Sapere quale modello di embedding disponibile a costo trascurabile trova una
ricetta inglese cercando in italiano, con quale recall, quale dimensione di vettore e quale
costo per diecimila ricette.

**Requested by:** `goal.md` § Differenziatore, che dichiara la ricerca semantica cross-lingua
il vero elemento distintivo; `arch-choices.md` § Embeddings, che nomina un modello per
esempio e non lo sceglie.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

—

## Includes

- Un corpus seed di circa quaranta ricette reali prese da blog veri, metà in italiano e metà
  in inglese, con nome, ingredienti e preparazione.
- Circa venti query in italiano del tipo che le fonti citano ("cena leggera", "pomodoro",
  "senza forno"), con i risultati attesi annotati a mano prima di misurare.
- Almeno due modelli multilingue candidati a costo trascurabile, indicizzando per ciascuno lo
  stesso testo (`nome + ingredienti + preparazione`).
- Misura, per modello: recall@5 delle query italiane sulle ricette inglesi e viceversa,
  dimensione del vettore, costo dell'indicizzazione riportato a diecimila ricette, latenza
  dell'embedding di una query.

## Verification

Una tabella con una riga per modello e quelle quattro colonne, più una riga finale che dice
quale si prende e su quale numero si è deciso. Le query e i risultati attesi restano nel
repository, in modo che `S8` possa rifare la stessa misura sui dati veri.

## Learning target

Se il cross-lingua senza traduzione regga davvero sul linguaggio delle ricette con un modello
a costo trascurabile — cioè se il differenziatore su cui la mappa poggia esiste.

## Excludes

- Indice HNSW, colonna in tabella e integrazione applicativa: sono di `S8`.
- Nessun codice di questo spike sopravvive, tranne corpus e query, che restano come fixture
  di misura.
- Ricerca ibrida o full-text come alternativa: candidato, non oggetto di questa misura.

## Open questions

- —
