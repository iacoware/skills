# S8 — Ricerca semantica nel ricettario corrente

← [Register](../roadmap.md#now)

**Outcome:** Si cerca a parole proprie e si trovano le ricette pertinenti del ricettario
corrente, anche quando sono scritte in un'altra lingua.

**Requested by:** `goal.md` §§ Differenziatore, Ricerca; `concepts.md` § Ricerca (MVP);
`arch-choices.md` § Embeddings. La misura che la rende possibile è `S2`.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Sviluppatori e tester sull'ambiente di staging: possono ritrovare una ricetta senza ricordarne
il titolo, ed è la promessa su cui l'intero prodotto si distingue.

## Includes

- Colonna vettoriale della dimensione decisa da `S2` e indice HNSW.
- Calcolo dell'embedding al salvataggio e rigenerazione a ogni modifica, su
  `nome + ingredienti + preparazione` più `tags` e `prepTime` quando ci sono: un solo punto di
  scrittura, alimentato da tutti i percorsi di aggiunta già consegnati.
- Backfill delle ricette salvate prima di questa riga.
- Embedding della query calcolato alla ricerca: è l'unica chiamata a pagamento in lettura, ed
  è misurata.
- Query di similarità sempre vincolata al ricettario corrente dal risolutore di `S3`.
- Ricerca in home con stato vuoto e nessun risultato distinguibili.
- Un fallimento dell'embedding non fa perdere la ricetta: resta salvata e ricalcolabile.

## Verification

Salvata una ricetta in inglese ("San Marzano tomato sauce"), la query "pomodoro" la riporta
nei primi cinque risultati; le venti query del corpus di `S2` riproducono su Postgres il
recall@5 misurato nello spike entro un margine dichiarato prima di misurare. Una ricetta di un
altro ricettario non compare mai, nemmeno chiamando direttamente l'API. La p95 della ricerca,
embedding della query incluso, è misurata sull'ambiente deployato e confrontata con il costo
per query letto dal log. Modificata una ricetta, il suo posizionamento cambia coerentemente al
testo nuovo. Simulato un fallimento dell'embedding al salvataggio, la ricetta esiste comunque
nell'elenco.

## Learning target

Che il recall misurato dallo spike sopravviva su dati veri dentro Postgres con HNSW, e che
l'unica chiamata a pagamento in lettura resti trascurabile per costo e per latenza.

## Excludes

- Filtri per tag e tempo: candidato; i campi si popolano già, quindi non servirà migrazione.
- Ricerca ibrida semantica più full-text: candidato.
- Ricerca che attraversa più ricettari: candidato; qui lo scope è il ricettario corrente.

## Open questions

- —
