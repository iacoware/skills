# S10 — Scrivi una ricetta a mano

← [Register](../roadmap.md#now)

**Outcome:** Apri un form vuoto, scrivi la ricetta che sai a memoria e la salvi come tutte le
altre.

**Requested by:** `goal.md` § Visione (aggiunta a mano) e § Aggiunta ricetta, che vuole lo stesso
form dell'edit con campi vuoti; `concepts.md` § Pipeline di estrazione.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi aggiunge ricette nel ricettario: il caso meno frequente, quello in cui non c'è niente da
estrarre.

## Includes

- Voce "a mano" nel form di aggiunta, che apre il form di edit di `S3` con i campi vuoti.
- Nessun campo obbligatorio marcato con asterisco; gli opzionali marcati come "optional" e lo
  stato richiesto esposto anche alle tecnologie assistive.
- Solo il titolo è richiesto: ingredienti e preparazione possono restare vuoti e riempirsi dopo.
- Salvataggio con embedding come le altre strade; `sourceUrl` resta vuoto.

## Verification

- Una ricetta scritta a mano compare in elenco, in dettaglio e fra i risultati della ricerca
  semantica.
- Il form è davvero lo stesso dell'edit: una modifica al form si vede in entrambi i percorsi.
- Un salvataggio con il solo titolo riesce, e la ricetta si completa dopo con l'edit.
- Un salvataggio con ingredienti su più righe le conserva così come sono state scritte, senza
  interpretarle.

## Learning target

Se il form condiviso fra correzione e inserimento manuale regge entrambi gli usi senza doversi
sdoppiare in due form con due validazioni.

## Excludes

- Parsing di quantità e unità: esclusione dichiarata, gli ingredienti restano testo libero.
- Duplicare una ricetta esistente come punto di partenza: candidato in `LATER`.

## Open questions

- —
