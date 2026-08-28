# S8 — Accesso con Google e ricettari propri

← [Register](../roadmap.md#now)

**Outcome:** Si entra con il proprio account Google e si vedono soltanto le ricette e i risultati di
ricerca dei ricettari di cui si fa parte.

**Requested by:** `goal.md` (*Auth — decisione presa: Google OAuth*, *Condivisione*),
`tech-choices.md` (*Auth — Auth.js + Google OAuth*) e `concepts.md`
(*Entità principali — User, Cookbook, Membership*).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chiunque abbia un account Google: da qui l'app smette di essere un ambiente di prova con un
proprietario implicito e diventa una cosa che due persone diverse possono usare senza vedersi
addosso.

## Includes

- Auth.js (NextAuth v5) con il solo provider Google, sessione e `User` persistiti su Postgres
  tramite l'adapter Drizzle; nessuna password, nessun invio di email.
- Tabella `Membership` e migrazione, e `Cookbook.creatorId` valorizzato.
- Creazione di un ricettario, e un ricettario creato in automatico al primo accesso, così che
  nessuno arrivi su uno stato vuoto senza uno scope.
- L'adapter dietro il resolver `CurrentCookbook` che S3 ha stabilito sostituito: lo scope diventa un
  ricettario in cui chi è autenticato ha una `Membership`, e la selezione fra i propri ricettari è
  persistita per sessione.
- Ogni rotta di ricetta, ricerca e foto richiede una sessione; una richiesta per un ricettario di
  cui non si è membri è rifiutata, non svuotata.
- Uscita dall'account.
- Migrazione del ricettario seminato da S3 a un ricettario con un creator vero.

## Verification

Una richiesta senza sessione a una qualsiasi rotta di ricetta, ricerca o foto è rifiutata. Due
account Google diversi vedono ciascuno solo l'elenco e solo i risultati di ricerca del proprio
ricettario, e una ricetta dell'uno non compare fra i risultati dell'altro nemmeno quando è il match
migliore. Chiedere per id il ricettario di un altro utente ottiene un rifiuto e non una lista vuota.
Il diff della riga mostra che sono cambiati il `Layer` del resolver e le rotte, e nessun punto di
query scritto da S3, S4, S5 e S7. Un primo accesso atterra su un ricettario vuoto ma usabile, in cui
si può salvare subito.

## Learning target

Se il giunto ha tenuto: se scambiare il ricettario configurato con quello dell'utente autenticato ha
toccato davvero un solo adapter e nessun punto di query, come S3 aveva scommesso.

## Excludes

- Nessun invito e nessun secondo membro: è di S9.
- Nessun ruolo e nessun permesso granulare: `OUT-OF-SCOPE`; il creator è solo `Cookbook.creatorId`.
- Nessuna passkey e nessun accesso con email e password: `OUT-OF-SCOPE` e `LATER`.
- Nessun ricettario pubblico: il campo `visibility` esiste ma resta `private`; i ricettari tematici
  sono in `LATER`.

## Open questions

- —
