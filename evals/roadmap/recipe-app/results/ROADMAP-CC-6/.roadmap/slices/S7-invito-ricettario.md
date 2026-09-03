# S7 — Invito condivisibile a un ricettario

← [Register](../roadmap.md#now)

**Outcome:** Chi ha creato un ricettario genera un link da mandare su una chat; chi lo apre dopo
essere entrato con Google diventa membro e da quel momento aggiunge, cerca e corregge le stesse
ricette.
**Requested by:** `goal.md` § Condivisione; `concepts.md` § Modello di condivisione cookbook-centrico
e § Invitation.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi userà l'app con la propria famiglia o i propri amici. Dopo questa riga il ricettario smette di
essere personale ed è la cosa attorno a cui il gruppo collabora.

## Includes

- Tabella `Invitation` con `cookbookId`, `token` e `expiresAt` opzionale.
- Generazione del link o codice d'invito dalla pagina del ricettario, con il token non indovinabile.
- Pagina che accetta l'invito: chi non è autenticato passa prima dall'accesso Google, poi ottiene la
  `Membership`.
- Il resolver del ricettario corrente comincia a poter restituire un ricettario di cui l'utente è
  membro senza esserne creator.
- Rifiuti nominati: invito scaduto, invito inesistente, invito già usato da chi è già membro.

## Verification

- Un secondo account Google che apre il link diventa membro, vede le ricette già presenti e ne
  aggiunge una che il primo account vede comparire nel proprio elenco.
- La ricerca del membro invitato pesca le ricette aggiunte dall'altro membro, cioè lo scope è il
  ricettario e non chi ha scritto la riga.
- Un account che non ha mai aperto l'invito non vede quel ricettario e riceve un rifiuto se ne chiede
  l'URL.
- Un token manomesso o scaduto porta a un messaggio che dice quale dei due casi è, non a una
  `Membership`.
- Chi è già membro e riapre il link non ottiene una seconda `Membership`.

## Learning target

Se la membership legata alla risorsa basta da sola a far collaborare un gruppo, senza che serva una
nozione di famiglia o di gruppo sopra i ricettari.

## Excludes

- Elenco dei membri, rimozione di un membro e revoca di un invito: nessuna fonte li chiede per l'MVP.
- Inviti per email: fuori, perché l'MVP non ha provider email.
- Gruppi sopra i ricettari e ruoli: restano candidati.

## Open questions

- Nessuna.
