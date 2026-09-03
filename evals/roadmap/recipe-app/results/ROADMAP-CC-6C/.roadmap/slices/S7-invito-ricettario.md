# S7 — Invita nel ricettario con un link

← [Register](../roadmap.md#now)

**Outcome:** Il creator genera un link e chi lo apre, entrando con Google, diventa membro pari del
ricettario.

**Requested by:** `goal.md` § Condivisione; `concepts.md` §§ Modello di condivisione, Invitation.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Famiglia e amici sullo staging: da qui un ricettario è davvero condiviso, e più persone lavorano
sulle stesse ricette.

## Includes

- Tabella `Invitation` con `cookbookId`, `token` e `expiresAt` opzionale, e la sua migrazione.
- Generazione del link dalla pagina del ricettario, con token casuale crittografico non
  indovinabile: è la sola credenziale che circola fuori dall'app, e viaggia per il canale che il
  creator sceglie.
- Pagina di accettazione: chi non è loggato passa dal login e torna sull'invito, non in home.
- Accettare crea la `Membership`; riaprire il link non ne crea una seconda.
- Elenco dei membri del ricettario.

## Verification

- Un secondo account Google che apre il link diventa membro, vede le ricette del ricettario, ne
  edita una creata da un altro, e la modifica è visibile a entrambi.
- Un token manomesso, sconosciuto o scaduto non crea nessuna membership e lo dice.
- Chi apre il link da non loggato finisce sul login e, subito dopo, sull'invito.
- Lo stesso utente che riapre il link resta con una sola membership.
- Un utente che non ha mai aperto il link non vede il ricettario nemmeno conoscendone l'URL.

## Learning target

Se il modello cookbook-centrico basta come unico concetto di condivisione: un link girato a mano,
senza email e senza ruoli, porta una persona dentro il ricettario e la mette alla pari con chi
c'era già.

## Excludes

- Invio dell'invito per email: esclusione dichiarata, nessun provider email nell'MVP.
- Revoca della membership e rimozione di un membro: candidati in `LATER`.
- Un concetto di gruppo sopra i ricettari: candidato in `LATER`, è il prezzo accettato del modello.

## Open questions

- —
