# S7 — Accesso con Google e ricettario dell'utente

← [Register](../roadmap.md#now)

**Outcome:** Si entra con Google, senza password da inventare né da recuperare, e si vede il proprio
ricettario: lo scope che fino a qui veniva dalla configurazione ora viene dalla sessione e
dall'appartenenza, sostituito in quell'unico punto.

**Requested by:** `goal.md` (§ Auth — decisione presa: Google OAuth), `tech-choices.md` (§ Auth:
Auth.js NextAuth v5) e `concepts.md` (§ Entità principali: `User`, `Cookbook`, `Membership`).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chiunque abbia un account Google. È la prima riga il cui pubblico non è più chi sviluppa: da qui in
avanti le ricette sono di qualcuno.

## Includes

- Auth.js (NextAuth v5) con il solo provider Google, sessione su Postgres tramite l'adapter Drizzle,
  entrata e uscita.
- Schema e migration per `User`, `Membership` e per il `creatorId` di `Cookbook`.
- Creazione automatica del primo ricettario dell'utente al primo accesso, con la relativa
  `Membership`: nessun passo di onboarding da attraversare prima di salvare qualcosa.
- Sostituzione del risolutore di scope: il ricettario corrente viene ora dalla sessione e dalla
  `Membership`, e non più da una variabile d'ambiente. È il solo punto che cambia.
- Chiusura dell'accesso non autenticato: le pagine di dominio richiedono una sessione, e una risorsa
  fuori dal proprio scope risponde come una risorsa inesistente.
- Migrazione dei dati esistenti dell'ambiente di prova sotto un utente reale, o loro cancellazione
  dichiarata.

## Verification

Due account Google diversi entrano e vedono due elenchi disgiunti; nessuno dei due vede le ricette
dell'altro, né nell'elenco né nei risultati di ricerca. L'URL diretto di una ricetta di un altro
utente risponde come per una ricetta inesistente e non rivela né titolo né esistenza. L'uscita
azzera l'accesso: ricaricando, le pagine di dominio riportano all'entrata. Al primo accesso di un
account nuovo esiste già un ricettario vuoto e ci si può salvare subito una ricetta. Il diff mostra
che, a parte il risolutore di scope, nessuna query di dominio scritta in S3, S4, S5 e S6 è stata
riscritta: è l'evidenza che il seam ha retto.

## Learning target

Il seam di scope disegnato in S3 regge davvero alla sostituzione: passare da un ricettario
configurato a uno derivato dall'identità è un cambio localizzato e non una riscrittura del dominio.
E Google OAuth da solo, senza alcun provider di posta, basta a far entrare una persona reale dal suo
telefono.

## Excludes

- Inviti, `Invitation` e membri diversi dal creator: sono di S9. Qui ogni utente sta nel proprio
  ricettario, da solo.
- La creazione di ricettari ulteriori e il cambio di ricettario corrente: sono di S10.
- Passkeys e qualunque provider alternativo: candidati dichiarati fuori MVP.
- Ruoli e permessi: esclusi per scelta dichiarata; l'unica domanda di autorizzazione è l'esistenza
  della `Membership`.

## Open questions

- —
