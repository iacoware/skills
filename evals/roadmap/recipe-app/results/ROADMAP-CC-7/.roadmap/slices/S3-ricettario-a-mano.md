# S3 — Il ricettario a mano: elenco, dettaglio, form

← [Register](../roadmap.md#now)

**Outcome:** Su staging si apre un ricettario, si vede l'elenco delle sue ricette, se ne apre una, se
ne scrive una nuova a mano e la si corregge — con lo stesso form, che è quello dell'edit con i campi
vuoti.

**Requested by:** `goal.md` (Home, e Aggiunta ricetta — stesso form per edit e inserimento manuale) e
`concepts.md` (entità `Recipe` e la sua normalizzazione minima).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi sviluppa e chi prova l'app sull'ambiente di staging non pubblico. Non c'è ancora un login: il
ricettario corrente è quello configurato, e l'utente vero arriva con `S7`.

## Includes

- Schema Drizzle di `Cookbook` e `Recipe` con `cookbookId`, nome, ingredienti, preparazione, tempo e
  tag opzionali, `sourceUrl` opzionale e la colonna `embedding` creata e lasciata nulla: la riempie
  `S6`.
- Un unico resolver del ricettario corrente, definito come porta con `Context.Tag` e fornito da un
  layer che in questa riga legge l'identificativo da configurazione. È il seam che `S7` sostituisce,
  e l'unico posto da cui una query di dominio può sapere in che ricettario si trova.
- Elenco delle ricette del ricettario corrente, dettaglio di una ricetta, creazione e modifica con lo
  stesso componente di form.
- Tre campi di testo libero — titolo, ingredienti, preparazione — senza nessun parsing di quantità e
  unità e senza nessun campo obbligatorio oltre al titolo; tempo e tag sono editabili e marcati come
  opzionali, mai richiesti.
- Lettura dai client component con React Query, e mutazioni che invalidano l'elenco.

## Verification

- Salvando una ricetta con il solo titolo compilato, la ricetta esiste ed è nell'elenco: nessun altro
  campo può bloccare il salvataggio.
- Nessuna query di dominio prende l'identificativo del ricettario da un parametro di richiesta:
  cambiando la configurazione l'elenco cambia, cambiando l'URL no. Un test lo verifica su elenco,
  dettaglio, creazione e modifica.
- Riaprendo una ricetta salvata, il form mostra esattamente il testo che era stato scritto, a capo
  compresi: il testo libero non viene normalizzato di nascosto.
- Ogni ricetta salvata ha `embedding` nullo e niente si rompe: elenco e dettaglio non lo leggono.

## Learning target

Che le convenzioni di questo progetto — porta con `Context.Tag` e layer per l'adapter Drizzle,
React Query sul client, un solo seam per lo scope — reggano una funzionalità completa; e che il
resolver del ricettario sia davvero l'unico punto da cambiare quando arriverà l'autenticazione,
perché è su questa scommessa che poggia il permesso di rimandare il login.

## Excludes

- Le foto → `S9`. Qui la ricetta è solo testo.
- L'aggiunta da link e da testo incollato → `S4` e `S5`.
- La generazione dell'embedding → `S6`, che apre l'adapter di embedding, lo possiede da solo e fa il
  backfill delle ricette salvate qui.
- Creare un ricettario e passare da un ricettario all'altro → `S7` e `S8`. Qui ce n'è uno solo,
  seminato da una migrazione.

## Open questions

- —
