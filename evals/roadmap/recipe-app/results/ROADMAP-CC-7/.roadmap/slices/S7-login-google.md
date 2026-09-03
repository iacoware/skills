# S7 — Login Google e il ricettario di chi entra

← [Register](../roadmap.md#now)

**Outcome:** Si entra con Google e si trova il proprio ricettario: lo scope smette di essere
configurato e diventa quello dell'utente autenticato, cambiando un solo layer.

**Requested by:** `goal.md` (Auth — decisione presa: Google OAuth), `tech-choices.md` (Auth.js con
NextAuth v5 e provider Google) e `concepts.md` (`User`, `Cookbook`, `Membership`).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi userà l'app davvero. Da qui le ricette che vede sono le sue, e non quelle di chiunque conosca
l'URL.

## Includes

- Auth.js con il solo provider Google, sessioni e utenti su Postgres tramite l'adapter Drizzle.
- Tabelle `User` e `Membership`, e i campi `creatorId` e `visibility` su `Cookbook`: `private` è
  l'unico valore raggiungibile in questa riga, `public` esiste nel tipo e non ha nessuna strada che
  ci porti.
- Al primo login, creazione automatica di un ricettario personale con chi entra come creator e primo
  membro: nessun passo di setup fra il login e il primo salvataggio.
- Sostituzione del layer del resolver del ricettario corrente: al posto della configurazione, il
  ricettario dell'utente in sessione, verificato contro `Membership`. Le query di `S3`, `S4`, `S5` e
  `S6` non si toccano.
- Ogni pagina e ogni mutazione richiedono una sessione; senza, si atterra sul login.

## Verification

- Due account Google diversi vedono due elenchi diversi, e nessuno dei due riesce ad aprire il
  dettaglio di una ricetta dell'altro conoscendone l'identificativo.
- Il diff di questa riga non tocca nessuna query di dominio: cambia il layer del resolver e nient'
  altro sotto il livello dell'applicazione. È la prova che il seam di `S3` era davvero uno solo.
- Uscendo e rientrando si ritrova il proprio ricettario con dentro le stesse ricette.
- Chi non è loggato e apre l'URL di una ricetta finisce sul login senza vederne titolo né contenuto.
- Lo stesso test di scope di `S6` gira con lo scope autenticato al posto di quello configurato e
  passa senza modifiche.
- Il flusso non manda nessuna email e non chiede nessuna password: non esiste un provider email in
  configurazione.

## Learning target

Che il seam introdotto configurato in `S3` regga la sostituzione con l'identità reale senza
riscrivere le righe già consegnate — è la scommessa su cui poggia tutto il rinvio del login — e che
Auth.js con il solo Google OAuth non chieda niente che le sorgenti hanno escluso.

## Excludes

- L'invito, i membri e il passaggio da un ricettario all'altro → `S8`. Qui l'utente ne ha esattamente
  uno.
- Passkeys e ogni secondo metodo di accesso → `LATER`, come dice `goal.md`.
- Ruoli e permessi dentro il ricettario → `LATER`: qui l'unica domanda di autorizzazione è se esista
  una `Membership`.
- Cancellazione dell'account e uscita da un ricettario: nessuna sorgente le chiede, e la mappa le
  tiene in `Open questions`.

## Open questions

- —
