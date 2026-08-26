# S10 — Ricettari condivisi per invito

← [Register](../roadmap.md#now)

**Outcome:** Chi crea un ricettario invita gli altri con un link, i membri leggono e
modificano le stesse ricette, e chi sta in più ricettari sceglie quello corrente.

**Requested by:** `goal.md` § Condivisione; `concepts.md` §§ Modello di condivisione
cookbook-centrico, Entità principali (`Membership`, `Invitation`).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Famiglia e amici: da qui il ricettario è di tutti quelli che sono stati invitati, e ognuno può
tenerne più di uno.

## Includes

- Migrazioni `Membership` e `Invitation` (token, scadenza opzionale).
- Creazione di un ricettario con un nome, con chi lo crea registrato come `creatorId`.
- Generazione di un link o codice d'invito condivisibile fuori dall'app.
- Apertura del link da autenticati: chi entra ottiene l'appartenenza al ricettario.
- Selettore del ricettario corrente, che alimenta il risolutore di `S3` e `S9`: elenco,
  aggiunta e ricerca lo seguono.
- Nessun ruolo oltre `creatorId`: essere membro è l'unico controllo.

## Verification

Un secondo account Google apre il link d'invito, vede le ricette del ricettario e ne modifica
una che ha scritto il primo; il primo vede la modifica. Un token inventato o scaduto non dà
accesso e non lascia tracce di appartenenza. Un utente membro di due ricettari cambia il
corrente e vede cambiare insieme elenco, aggiunta e risultati di ricerca. Un utente non membro
che chiama direttamente l'API con l'identificatore del ricettario riceve un rifiuto, non una
lista vuota.

## Learning target

Che l'appartenenza al ricettario basti come unico controllo di autorizzazione per tutta
l'app, senza introdurre ruoli.

## Excludes

- Revoca di un invito e uscita da un ricettario: domanda aperta della mappa, non decisa qui.
- Un concetto di gruppo sopra i ricettari: candidato.
- Ricettari pubblici tematici e ricerca cross-ricettario: candidati.

## Open questions

- —
