# S9 — Ricettari condivisi: invito via link e più ricettari

← [Register](../roadmap.md#now)

**Outcome:** Si invita qualcuno in un ricettario con un link, chi lo apre da loggato entra e modifica
tutto, e ognuno passa dai ricettari di cui è membro.

**Requested by:** `sources/goal.md` (Condivisione), `sources/concepts.md` (Modello di condivisione
cookbook-centrico, Membership, Invitation).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Famiglia e amici: ricevono un link, entrano in un ricettario che non hanno creato, e ci scrivono
dentro come chi li ha invitati.

## Includes

- `Membership` come relazione N:N fra `User` e `Cookbook`, senza campo `role`.
- `Invitation` con token imprevedibile e `expiresAt` opzionale, e la sua revoca.
- Creazione di un nuovo ricettario con un nome.
- Selettore del ricettario corrente, che alimenta `CurrentCookbook` e quindi anche lo scope della
  ricerca di `S7`.

## Verification

Un invitato che apre il link vede una ricetta scritta da un altro, la modifica, e la modifica è
visibile a chi lo ha invitato. Un token revocato o scaduto non fa entrare e lo dice. Un membro di due
ricettari cerca in uno e non trova quello che sta nell'altro, e cambiando ricettario trova l'altro e
non il primo. Chi non è membro non apre un ricettario nemmeno conoscendone l'id. Il creator non ha
nessun potere che gli altri membri non abbiano, tranne comparire in `creatorId`.

## Learning target

Se la sola membership, senza ruoli e senza permessi per azione, basta come unico concetto di
condivisione — o se la prima famiglia che la usa chiede subito qualcosa in più.

## Excludes

- Un concetto di gruppo sopra i ricettari, ricettari pubblici tematici, ricerca cross-ricettario:
  restano candidati.
- Permessi in sola lettura: esclusi dalla mappa, con il prezzo dichiarato.
- Invio dell'invito per email: escluso, il link lo consegna chi invita.

## Open questions

- —
