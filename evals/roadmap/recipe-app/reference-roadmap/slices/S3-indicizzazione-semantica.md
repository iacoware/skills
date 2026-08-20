# S3 — Indicizzazione semantica delle ricette

← [Register](../roadmap.md#now)

**Outcome:** Ogni ricetta salvata porta con sé il proprio embedding, aggiornato a ogni modifica.

**Requested by:** `sources/concepts.md` § Recipe, § Ricerca (MVP)
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi cercherà una ricetta: qui non lo vede ancora, ed è il motivo per cui questa riga non è il
validatore del tema.

## Includes

- Il modello `Recipe` con l'embedding come colonna `vector` e l'indice HNSW.
- Il calcolo dell'embedding al salvataggio e a ogni modifica, a partire da nome, ingredienti e
  preparazione.
- Il seed di ricette reali italiane e inglesi già raccolto per `S2`.

## Verification

Dopo il seed ogni ricetta ha il proprio embedding, e una query di similarità lanciata a mano
restituisce i vicini attesi.

## Learning target

Che l'embedding resti allineato al testo da solo, come indice derivato, senza un lavoro di
sincronizzazione da mantenere a parte.

## Excludes

- L'interfaccia di ricerca, che è `S4`.
- Tag e tempo nel testo indicizzato, che sono `S13`.
- Lo scoping al ricettario corrente, che arriva con `S12`.

## Open questions

—
