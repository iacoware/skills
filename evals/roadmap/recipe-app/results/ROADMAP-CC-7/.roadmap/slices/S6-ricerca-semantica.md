# S6 — Ricerca semantica cross-lingua nel ricettario

← [Register](../roadmap.md#now)

**Outcome:** Si scrive "cena leggera" o "pomodoro" nella home ed escono le ricette giuste del
ricettario corrente, comprese quelle scritte in un'altra lingua.

**Requested by:** `goal.md` (Ricerca — MVP: solo semantica; Differenziatore), `concepts.md`
(Ricerca), e l'esito di `S2`, che sceglie il modello e i parametri dell'indice.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi prova l'app su staging. Da qui il ricettario si interroga invece di scorrerlo, che è la ragione
per cui questa app esiste invece di essere Mealie.

## Includes

- L'adapter di embedding dietro `Context.Tag`, con il modello che `S2` ha scelto. È l'unico punto del
  codice che chiama il provider, e da qui in poi ogni percorso di salvataggio ci passa.
- Generazione dell'embedding a ogni salvataggio e a ogni modifica, su tutti i percorsi che già
  esistono — a mano, da link, da LLM e da testo incollato — a partire da nome, ingredienti e
  preparazione, più tag e tempo quando ci sono.
- Backfill delle ricette già salvate senza embedding, come comando da eseguire una volta.
- Indice HNSW sulla colonna dell'embedding, con i parametri che `S2` ha misurato.
- Campo di ricerca nella home: la query viene embeddata al momento e confrontata per similarità, con
  scope al ricettario del resolver di `S3` e a nient'altro.
- Uno stato vuoto che distingue "non ho trovato niente" da "il ricettario è ancora vuoto".

## Verification

- Una ricetta scritta in inglese — importata da un blog o incollata a mano — esce cercando
  "pomodoro" in italiano, senza che niente sia stato tradotto: è la promessa che `goal.md` chiama il
  differenziatore, ed è la prima volta che qualcuno la vede su uno schermo.
- Una query per intenzione ("cena leggera") restituisce ricette che non contengono quelle parole, e
  le query del corpus seme di `S2` danno un recall coerente con quello che lo spike aveva misurato:
  se qui è molto peggio, il colpevole è l'integrazione e non il modello.
- La ricerca non vede le ricette di un altro ricettario: un test con due ricettari popolati lo
  verifica.
- Cambiando il titolo di una ricetta e cercandola col titolo nuovo, la ricetta esce: l'embedding si è
  rigenerato alla modifica.
- La p95 della ricerca è misurata sulla macchina Fly appena risvegliata dalla sospensione, non a
  caldo, e il numero è scritto: è il costo dell'unica chiamata a pagamento su un percorso di lettura
  che questa mappa ammette.
- Una ricetta il cui embedding manca resta nell'elenco e apribile: esce dai risultati, non dal
  ricettario.

## Learning target

Che la ricerca semantica su pgvector, con l'embedding generato solo in scrittura e la query embeddata
al volo, dia risultati che una persona riconosce come giusti sul proprio ricettario — e che la
latenza regga anche quando la macchina si sta svegliando, che è il momento in cui la ricerca verrà
usata più spesso.

## Excludes

- I filtri strutturati su tag e tempo e la ricerca ibrida col full-text → `LATER`. I campi si
  popolano già da `S4` e `S5`, quindi i filtri si accenderanno senza migrazione né lavoro
  retroattivo.
- La ricerca che attraversa più ricettari → `LATER`.
- La derivazione dei tag quando l'estrazione non li dà: restano vuoti, e l'embedding si regge sul
  testo.

## Open questions

- —
