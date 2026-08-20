# S2 — Quanto regge il cross-lingua un embedder multilingue nel budget

← [Register](../roadmap.md#now)

**Outcome:** Sappiamo quale modello di embedding dentro il budget trova una ricetta scritta in
inglese quando si cerca "pomodoro", e quale no.

**Requested by:** `sources/goal.md` (Differenziatore, nota strategica), `sources/arch-choices.md`
(Embeddings — API cloud multilingue).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

—

## Includes

- Un corpus di prova di ricette reali, metà in italiano e metà in inglese, con un elenco di query
  attese e il risultato che ognuna dovrebbe restituire.
- Due o tre modelli multilingue candidati, fra cui `text-embedding-3-small` che le sorgenti citano
  come esempio, misurati sullo stesso corpus caricato in pgvector.
- Le stesse query poste sia nella lingua della ricetta sia nell'altra.

## Verification

Per ogni candidato sono dichiarati: recall@10 cross-lingua sulle query attese, recall@10 nella stessa
lingua come termine di paragone, latenza della query di similarità sul corpus, e costo per indicizzare
10.000 ricette. La tabella dice quale candidato passa e quale no, e su quali query fallisce.

## Learning target

Se un embedder multilingue a questo costo regge il cross-lingua, che è l'unica cosa che distingue
questo progetto da Mealie.

## Excludes

- Nessun codice dello spike sopravvive: restano il corpus di prova e la tabella dei risultati, che
  `S7` riusa come banco di prova.
- La ricerca ibrida e i filtri strutturati non entrano nella misura: restano candidati.

## Open questions

- —
