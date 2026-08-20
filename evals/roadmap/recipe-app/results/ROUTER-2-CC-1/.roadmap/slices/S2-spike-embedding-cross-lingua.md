# S2 — Spike: quale embedding regge la ricerca cross-lingua

← [Register](../roadmap.md#now)

**Outcome:** Sappiamo quale modello di embedding multilingue trova una ricetta inglese da una query
italiana.

**Requested by:** `sources/goal.md` § Differenziatore, `sources/arch-choices.md` § Embeddings
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

—

## Includes

- Uno script usa e getta, fuori dall'applicazione.
- Due o tre modelli di embedding multilingue raggiungibili via API a basso costo.
- Un corpus di poche decine di ricette reali, metà in italiano e metà in inglese.
- Un elenco di query in italiano che devono trovare ricette inglesi, e viceversa.

## Verification

Possiamo dire, per ogni modello candidato, quante delle ricette attese compaiono fra i primi
risultati e quanto costa indicizzare il corpus previsto dai sorgenti.

## Learning target

Se un modello di embedding cloud multilingue trova davvero una ricetta inglese partendo da una query
italiana, e quale.

## Excludes

- Qualunque codice destinato a sopravvivere allo spike.
- L'indice HNSW e la colonna sul modello, che sono `S3`.
- La ricerca ibrida, che è una candidate.

## Open questions

- Servono dai primi utenti una manciata di ricette e di query reali. Senza, il corpus lo scegliamo
  noi e la misura vale meno di quanto sembri.
