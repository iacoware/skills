# S8 — Invito al ricettario e membri pari

← [Register](../roadmap.md#now)

**Outcome:** Il creatore di un ricettario genera un link, lo manda a chi vuole, e chi lo apre da
loggato entra dentro e da lì legge ed edita tutto come lui.

**Requested by:** `goal.md` (Condivisione — cookbook-centrica, creator che invita per link o codice,
membri pari) e `concepts.md` (Modello di condivisione, `Membership`, `Invitation`).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Famiglia e amici. Da qui il ricettario è di più persone e non di una sola, che è il punto dell'app.

## Includes

- Tabella `Invitation` con ricettario, token e scadenza opzionale, e generazione di un link
  condivisibile dalla pagina del ricettario.
- Apertura del link: chi non è loggato passa dal login e torna sull'invito; chi è loggato ottiene una
  `Membership` e atterra sul ricettario.
- Creazione di un nuovo ricettario e selettore del ricettario corrente, perché da qui un utente può
  starne in più d'uno; il selettore scrive lo stesso resolver che `S7` ha reso autenticato, e non ne
  apre un secondo.
- Revoca di un invito, e scadenza quando è stata impostata.
- Un invito già usato resta valido finché non scade o non viene revocato: le sorgenti lo chiamano
  link o codice condivisibile, non invito personale.

## Verification

- Due account Google diversi e un link: il secondo entra, vede le ricette del primo, ne modifica una,
  e il primo vede la modifica.
- Il secondo membro può aggiungere una ricetta, cancellare una ricetta del primo e generare a sua
  volta un invito: dentro il ricettario i membri sono pari, come dicono le sorgenti, e non c'è nessun
  gesto riservato al creator.
- Un token revocato o scaduto porta a un messaggio che dice che l'invito non vale più, e non crea
  nessuna `Membership`.
- Un token inventato a mano non entra in nessun ricettario, e provarne molti di fila non rivela quali
  esistono.
- Il token non compare in nessun log applicativo.
- Chi sta in due ricettari li vede entrambi nel selettore, ed elenco e ricerca cambiano insieme al
  ricettario scelto: cercando dal ricettario A non escono ricette di B.

## Learning target

Che il modello cookbook-centrico — membership N:N, nessun ruolo oltre al creator, un invito che è un
link e basta — basti a far collaborare una famiglia senza che serva un concetto di gruppo sopra; e
che il selettore del ricettario corrente non apra buchi di scope nelle righe già consegnate.

## Excludes

- L'invito spedito via email: non esiste un provider email in questa mappa, e il link lo inoltra chi
  invita.
- Uscire da un ricettario, rimuovere un membro, cancellare un ricettario: nessuna sorgente li chiede,
  e la mappa li tiene in `Open questions` invece di deciderli qui.
- Un concetto di gruppo sopra i ricettari e i ricettari pubblici tematici → `LATER`.

## Open questions

- —
