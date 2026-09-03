# S8 — Invito via link e ricettari condivisi

← [Register](../roadmap.md#now)

**Outcome:** Mando un link, chi lo apre entra nel ricettario, e da lì in poi vediamo e
modifichiamo le stesse ricette; chi sta in più ricettari passa dall'uno all'altro.

**Requested by:** `sources/goal.md` § Condivisione; `sources/concepts.md` § Modello di
condivisione cookbook-centrico, § Invitation.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Famiglia e amici: uno crea il ricettario e manda il link, gli altri entrano e aggiungono le
loro ricette allo stesso ricettario. Chi ne ha più di uno sceglie su quale sta lavorando.

## Includes

- Tabella `Invitation` con un token non indovinabile e una scadenza opzionale, in migrazione.
- Generazione del link di invito e revoca; chi può generarlo e se il token scade sono un solo
  punto di policy, che applica la decisione della domanda aperta qui sotto.
- Apertura del link: chi non è autenticato passa dall'accesso e torna all'invito; chi è
  autenticato ottiene la `Membership` ed entra nel ricettario.
- Creazione di ricettari ulteriori e selettore del ricettario corrente, che alimenta il resolver
  di `S7`: elenco, ricerca e aggiunta seguono la selezione.
- Un token già consumato, revocato o scaduto non concede niente e lo dice.

## Verification

- Due account diversi, dopo l'invito, vedono lo stesso elenco; una ricetta aggiunta dall'uno
  compare all'altro e ognuno può modificarla.
- Un utente che appartiene a due ricettari vede, cambiando selezione, due elenchi e due insiemi
  di risultati di ricerca distinti; nessuna ricetta attraversa il confine.
- Un utente autenticato che non è membro non raggiunge il ricettario, nemmeno per URL diretto.
- Un token revocato, uno scaduto e uno inventato vengono rifiutati, ognuno senza rivelare
  l'esistenza del ricettario.
- Chi non è autorizzato a generare un invito, secondo la policy scelta, non ci riesce nemmeno
  chiamando l'azione direttamente.

## Learning target

Che la membership sia davvero l'unico confine di cui l'app ha bisogno: con più membri e più
ricettari niente esce dal ricettario a cui appartiene, e non serve nessun ruolo per farlo
reggere.

## Excludes

- Ruoli e permessi granulari: fuori scope, tutti i membri sono pari.
- Un concetto di gruppo sopra i ricettari: candidato, con il costo di ri-invitare accettato.
- Ricettari pubblici e ricerca cross-ricettario: candidati; `visibility` resta un campo che
  non cambia comportamento.
- Uscire da un ricettario o rimuovere un membro: nessuna fonte lo chiede.

## Open questions

- Chi può invitare: `goal.md` dice che il creator invita gli altri, e due righe dopo che dentro
  un ricettario tutti i membri sono pari. La scelta decide se serve un controllo sul
  `creatorId` o basta la membership.
- Se il link di invito scade: `concepts.md` segna `expiresAt` come opzionale senza dire quando
  valorizzarlo.
