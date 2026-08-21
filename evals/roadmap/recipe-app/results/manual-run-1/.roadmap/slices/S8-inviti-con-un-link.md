# S8 — Inviti con un link: membri pari nello stesso ricettario

← [Register](../roadmap.md#now)

**Outcome:** Chi ha creato un ricettario manda un link, e chi lo apre da entrato si ritrova dentro con
gli stessi diritti di tutti gli altri; chi sta in più ricettari passa dall'uno all'altro e la ricerca
lo segue.

**Requested by:** `sources/goal.md`, «Condivisione»; `sources/concepts.md`, il modello
cookbook-centrico, `Invitation` e la `Membership` N:N.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Famiglia e amici. Dopo questa riga ricevono un link, lo aprono, e sono dentro il ricettario a leggere
e modificare come chiunque altro — senza che nessuno debba dare loro una password o aggiungerli a
mano.

## Includes

- `Invitation` con il suo token e la sua scadenza facoltativa, come le fonti la definiscono.
- La generazione del link condivisibile a partire da un ricettario, e la sua accettazione che crea
  una `Membership`.
- L'appartenenza a più ricettari e il passaggio dall'uno all'altro, letto dallo stesso risolutore del
  ricettario corrente.
- La creazione di un nuovo ricettario da parte di un utente entrato.
- Il comportamento di un link già usato o scaduto secondo la decisione ancora aperta qui sotto: la
  riga non pubblica nessuna delle due strade finché non è presa.

## Verification

Due account sull'ambiente deployato finiscono nello stesso ricettario attraverso il link, e ciascuno
vede e modifica le ricette dell'altro: nessuno dei due ha un diritto che l'altro non ha. Un token
inesistente, scaduto o non valido riceve un messaggio e non crea nessuna appartenenza. Un utente che
sta in due ricettari non vede mai le ricette dell'uno mentre è nell'altro, e la ricerca cambia
risultati quando cambia ricettario. Una persona che non è membro e conosce l'URL di una ricetta è
rifiutata. Il link non contiene niente che permetta di indovinare gli altri link. Chi crea un
ricettario ne è `creatorId` e resta membro come gli altri.

## Learning target

La condivisione aggregata attorno al ricettario, con tutti i membri pari, basta a una famiglia: il
link d'invito è tutto quello che serve a entrare, e nessuno chiede un ruolo o un permesso più fine.

## Excludes

- Nessun ruolo, nessun permesso granulare: esclusione dichiarata, e `creatorId` è l'unico ruolo che
  esiste.
- Nessuna rimozione di un membro e nessuna uscita volontaria da un ricettario: sono candidate.
- Nessun gruppo sopra i ricettari: è candidato, e il suo prezzo — ri-invitare le stesse persone in
  ogni ricettario — è accettato qui.
- Nessun invito spedito per email: non esiste un canale email, e il link lo consegna chi invita.

## Open questions

- Il link d'invito è a uso singolo o riusabile da chiunque lo riceva, e chi apre un link scaduto o
  già consumato cosa vede? Le fonti definiscono `token` ed `expiresAt?` senza dire né l'una né
  l'altra cosa, e la risposta cambia sia la forma di `Invitation` sia cosa questa riga deve mostrare;
  finché è aperta la riga non ne pubblica nessuna delle due.
