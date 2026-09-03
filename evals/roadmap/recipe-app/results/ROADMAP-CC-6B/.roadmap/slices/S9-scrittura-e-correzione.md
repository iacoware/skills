# S9 — Scrittura a mano e correzione

← [Register](../roadmap.md#now)

**Outcome:** Scrivo una ricetta che conosco partendo da un form vuoto, e correggo qualunque
ricetta salvata nello stesso form; dopo il salvataggio la ricerca la trova aggiornata.

**Requested by:** `sources/goal.md` § Aggiunta ricetta — "stesso form per edit e inserimento
manuale", "la correzione è sempre disponibile dopo".
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

I membri del ricettario: aggiungono ricette di famiglia che non stanno su nessun sito, e
sistemano quello che l'estrazione ha preso male senza dover rifare l'aggiunta.

## Includes

- Un solo form — nome, ingredienti, preparazione come testo libero — usato con i campi vuoti per
  l'inserimento a mano e precompilato per la modifica.
- Nessun campo obbligatorio oltre al nome; `tag` e tempo restano modificabili ma mai richiesti,
  e gli opzionali sono marcati come tali.
- Salvataggio che rigenera l'embedding dal testo nuovo, riusando il passo che `S6` possiede.
- Se la rigenerazione fallisce, la modifica resta salvata e la ricetta resta leggibile; il
  recupero è quello di `S6`.
- Ogni membro può modificare qualunque ricetta del ricettario.

## Verification

- Una ricetta scritta a mano compare nell'elenco e nella ricerca come una importata.
- Correggendo il nome o gli ingredienti di una ricetta importata male, la ricerca la trova con
  il testo nuovo e non più con quello vecchio.
- Un membro diverso da chi l'ha aggiunta può modificarla e il risultato è visibile a entrambi.
- Salvare senza toccare niente non cambia il contenuto della ricetta.
- Un salvataggio con embedding fallito lascia la ricetta leggibile e modificabile.

## Learning target

Che la correzione dopo il fatto basti a rendere accettabile un'estrazione imperfetta — la
scommessa delle fonti è che nessuno debba passare da un form prima di salvare, e regge solo se
sistemare dopo è abbastanza comodo da essere fatto davvero.

## Excludes

- Parsing di quantità e unità: fuori scope dichiarato, gli ingredienti restano testo.
- Cronologia delle modifiche e chi ha modificato: fuori scope, non c'è traccia per ricetta.
- Cancellazione di una ricetta: nessuna fonte la chiede.
- Le foto nel form: `S10`.

## Open questions

- —
