# S6 — Accedi con Google e vedi i tuoi ricettari

← [Register](../roadmap.md#now)

**Outcome:** L'utente entra con il suo account Google, crea i suoi ricettari, e ogni lettura e
scrittura passa dalla sua appartenenza invece che da un ricettario configurato.

**Requested by:** `goal.md` § Auth — decisione presa: Google OAuth; `concepts.md` §§ User,
Cookbook, Membership; è il seam che `S3` ha lasciato aperto.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Le prime persone reali sullo staging — l'autore e chi gli sta intorno: ognuna entra con la propria
identità e vede solo i ricettari di cui fa parte.

## Includes

- Auth.js (NextAuth v5) con provider Google e adapter su Postgres via Drizzle; client OAuth
  configurato sulla console Google.
- Tabelle `User`, `Cookbook` con `creatorId` e `visibility` a `private`, e `Membership` come N:N,
  con la migrazione che porta il ricettario seed e le sue ricette dentro il nuovo modello.
- Il resolver `currentCookbook` passa da configurato ad autenticato: è l'unico punto che cambia.
- Creazione di un ricettario, elenco dei propri ricettari e selettore di quello corrente.
- Ogni rotta che legge o scrive ricette rifiuta chi non è membro del ricettario che sta toccando.
- Login e logout.

## Verification

- Un utente non autenticato che apre l'elenco o una ricetta finisce sul login.
- Due account Google diversi non vedono i ricettari l'uno dell'altro, né in elenco né in ricerca.
- Chi chiama a mano l'URL di una ricetta di un ricettario di cui non è membro riceve un rifiuto e
  non il contenuto: il controllo è sul server, non solo sulla navigazione.
- Le ricette salvate prima di questa riga si ritrovano nel ricettario del creator dopo la
  migrazione, con embedding intatti.
- Un utente con due ricettari cambia il corrente e l'elenco e la ricerca lo seguono.
- Il numero di punti del codice modificati per sostituire lo scope configurato con quello
  autenticato è contato: è la prova o la smentita dell'assunzione sul seam.

## Learning target

Se il seam lasciato da `S3` regge davvero — sostituire lo scope configurato con quello autenticato
tocca un solo resolver e nessuna riga precedente va riscritta — e se Google OAuth via Auth.js copre
identità e sessione senza obbligare a nient'altro.

## Excludes

- Inviti e membership di altre persone: sono di `S7`.
- Ruoli e permessi dentro il ricettario: esclusione dichiarata, non c'è nessun campo ruolo.
- Passkeys, magic link, email e password: fuori, esclusi nelle fonti.
- Ricettari pubblici: candidato in `LATER`, il campo `visibility` esiste già.
- Cancellare un ricettario: candidato in `LATER`.

## Open questions

- —
