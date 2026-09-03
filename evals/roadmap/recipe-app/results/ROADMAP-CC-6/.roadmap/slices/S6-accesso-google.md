# S6 — Accesso con Google e ricettario proprio

← [Register](../roadmap.md#now)

**Outcome:** Si entra con il proprio account Google e si trova il proprio ricettario: le ricette che
si aggiungono e si cercano sono le proprie, e quelle di un altro utente non si vedono.
**Requested by:** `goal.md` § Auth — decisione presa: Google OAuth; `concepts.md` § User, § Cookbook,
§ Membership; sostituisce lo scope configurato introdotto in S3.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi userà l'app davvero, per la prima volta con la propria identità. Dopo questa riga ha un ricettario
che è suo, invece di lavorare sull'unico ricettario seminato dell'ambiente di prova.

## Includes

- Auth.js (NextAuth v5) con provider Google, sessione e tabelle di Auth.js su Postgres.
- Tabelle `Cookbook` con `creatorId` e `visibility`, e `Membership` come relazione N:N; migrazione
  che collega le ricette esistenti al cookbook seminato.
- Creazione automatica di un ricettario personale al primo accesso, di cui l'utente è creator e
  membro, senza schermata di creazione.
- Il resolver del ricettario corrente di S3 smette di leggere la configurazione e restituisce un
  ricettario di cui l'utente autenticato è membro: è l'unico punto che cambia.
- Rotte e azioni protette: chi non è autenticato viene mandato all'accesso; chi lo è ma non è membro
  del ricettario chiesto non lo vede.
- Uscita dalla sessione.

## Verification

- Due account Google diversi vedono due elenchi diversi, e nessuna ricetta dell'uno compare
  nell'elenco o fra i risultati di ricerca dell'altro.
- Chiedendo l'URL di dettaglio di una ricetta di un altro utente si ottiene un rifiuto, non la
  ricetta: la protezione è sulla lettura dei dati e non solo sulla navigazione.
- Aggiunta, ricerca ed elenco continuano a funzionare come prima di questa riga, con il ricettario
  vero al posto di quello configurato, e nessuna riga di S3, S4 o S5 è stata riscritta oltre al
  resolver.
- Un utente che accede per la prima volta trova un ricettario vuoto e può aggiungerci subito una
  ricetta, senza passaggi intermedi.
- Le ricette esistenti nell'ambiente di prova sono ancora raggiungibili dopo la migrazione, dal loro
  ricettario.

## Learning target

Se il confine di scope aperto in S3 regge davvero la sostituzione promessa — scope configurato
scambiato con scope autenticato in un solo punto — o se l'identità si è infiltrata altrove.

## Excludes

- Inviti e ricettari con più membri: sono di S7.
- Ruoli e permessi dentro un ricettario: restano candidati; qui l'unica domanda è "sei membro?".
- Passkeys, email e password: fuori per decisione di `goal.md`.
- Schermata di scelta fra più ricettari: qui l'utente ne ha esattamente uno; è la domanda aperta
  della mappa.

## Open questions

- Nessuna.
