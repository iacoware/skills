# S9 — Invito al ricettario

← [Register](../roadmap.md#now)

**Outcome:** Si manda un link a un familiare, quello entra nel ricettario e da lì in poi i due
leggono e scrivono le stesse ricette da pari.

**Requested by:** `goal.md` (*Condivisione*) e `concepts.md`
(*Modello di condivisione: cookbook-centrico*, *Entità principali — Invitation*).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Le famiglie e gli amici a cui l'app è destinata: è il punto in cui il ricettario smette di essere
personale e la collaborazione promessa esiste davvero.

## Includes

- Tabella `Invitation` (`cookbookId`, `token`, `expiresAt` opzionale) e migrazione.
- Il creator genera dal ricettario un link condivisibile, riusabile da più persone finché non viene
  revocato o non scade.
- Chi lo apre già autenticato ottiene una `Membership`; chi lo apre da sloggato passa
  dall'accesso Google e poi entra, atterrando sul ricettario e non su una pagina vuota.
- Revoca e rigenerazione del link, e rimozione di un membro, entrambe riservate al creator
  identificato da `Cookbook.creatorId`: sono la via d'uscita per un link che è finito dove non
  doveva.
- Elenco dei membri del ricettario.
- Un token sconosciuto, scaduto o revocato è rifiutato con un messaggio che dice quale dei tre.

## Verification

Due account Google finiscono nello stesso ricettario attraverso il link; una ricetta scritta dal
primo viene corretta dal secondo e trovata dalla ricerca del secondo. Riaprire lo stesso link con
l'account che è già membro non crea una seconda `Membership`. Un token revocato e uno scaduto sono
rifiutati con messaggi distinti. Rimosso un membro, le sue richieste al ricettario tornano a essere
rifiutate. Un account che non ha mai aperto il link e chiede il ricettario per id è rifiutato.

## Learning target

Se un token condivisibile è tutta la condivisione che serve all'MVP — cioè se il fatto che dentro un
ricettario siano tutti pari regge all'uso vero, o se la prima famiglia chiede un ruolo prima ancora
di aver riempito il ricettario.

## Excludes

- Nessun concetto di gruppo sopra i ricettari: `LATER`, ed è il costo dichiarato del modello
  cookbook-centrico.
- Nessun ruolo oltre alla distinzione creator/membro che `creatorId` già dà: `OUT-OF-SCOPE`.
- Nessun invito per email: le fonti escludono ogni provider email dall'MVP; il link si condivide
  come si vuole.
- Nessun ricettario pubblico: `LATER`.

## Open questions

- —
