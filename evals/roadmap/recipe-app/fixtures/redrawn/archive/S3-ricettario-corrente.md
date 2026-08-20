# S3 — Il ricettario corrente: elenco, dettaglio e un solo form

← [Register](../roadmap.md#now)

**Outcome:** Nel ricettario corrente si vede l'elenco delle ricette, si apre una ricetta, e con lo
stesso form la si scrive a mano o la si corregge.

**Requested by:** `sources/goal.md` (Home, Aggiunta ricetta — stesso form per edit e inserimento
manuale), `sources/concepts.md` (Recipe, Cookbook).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi prova l'app sull'ambiente Fly non pubblico: può scrivere una ricetta che conosce, ritrovarla in
elenco e correggerla. È l'unico pubblico che questa riga può avere, perché l'identità reale arriva
in `S8`.

## Includes

- Tabelle `Cookbook` e `Recipe` con `cookbookId`, e le migrazioni che le creano.
- Il resolver `CurrentCookbook`, unico punto da cui passa lo scope: qui restituisce un ricettario
  configurato, e ogni lettura e ogni scrittura ci passano attraverso.
- Elenco delle ricette del ricettario corrente e pagina di dettaglio.
- Un solo form, con i campi vuoti in creazione e pieni in modifica: titolo, ingredienti e
  preparazione come testo libero, senza parsing di quantità e unità, senza asterischi sugli
  obbligatori e con gli opzionali marcati "optional".

## Verification

Una ricetta scritta a mano compare in elenco e si riapre identica nel dettaglio; una modifica al
testo è visibile subito. Una ricetta salvata in un altro ricettario non compare mai nell'elenco
corrente. Un test fallisce se una query raggiunge le ricette senza passare da `CurrentCookbook`: lo
scope non ha una seconda strada.

## Learning target

Se testo libero e correzione sempre disponibile bastano a rendere accettabile un'aggiunta senza
review, che è l'ipotesi su cui l'intero flusso di cattura è costruito.

## Excludes

- Estrazione da URL o da testo incollato: sono di `S4`, `S5` e `S6`.
- Foto e copertina: sono di `S10`, che possiede da solo il confine dello storage.
- Identità reale, membership e inviti: sono di `S8` e `S9`; qui il proprietario è uno e implicito.
- Embedding e ricerca: sono di `S7`, che possiede la pipeline e fa il backfill di quanto salvato qui.

## Open questions

- —
