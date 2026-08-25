# S8 — Invito a un ricettario con link condivisibile

← [Register](../roadmap.md#now)

**Outcome:** Un membro genera un link per il ricettario corrente; chi lo apre da loggato diventa
membro pari e da quel momento vede e corregge le stesse ricette.

**Requested by:** `sources/goal.md` § Condivisione, che dà al creator il potere di invitare via
link o codice; `sources/concepts.md` § Invitation e § Modello di condivisione.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Famiglia e amici. Dopo questa riga il ricettario è davvero condiviso: chi entra dal link lavora
sulle stesse ricette senza che nessuno debba passargli qualcosa a mano.

## Includes

- Tabella `invitation` con `token` e scadenza opzionale.
- Generazione del link dal ricettario corrente da parte di un membro.
- Pagina di accettazione che, per un utente autenticato, crea la `Membership`, ed è idempotente su
  aperture ripetute.
- Rifiuto esplicito di un token scaduto o inesistente; chi non è autenticato passa dal login e
  torna all'invito.
- La semantica del token resta quella che l'autore deciderà: `Includes` e verifica sono scritti
  per reggere sia il link aperto sia il link vincolato a un indirizzo, e nessuno dei due è dato per
  scelto qui.

## Verification

Due account Google distinti, dopo che il secondo ha aperto il link, vedono lo stesso elenco e la
stessa ricerca, e una correzione fatta dall'uno è visibile all'altro. Aprire il link due volte non
crea due membership. Un token scaduto o inventato viene rifiutato con un messaggio che dice perché.
Chi non ha mai aperto quell'invito continua a non vedere nulla di quel ricettario, nemmeno andando
diritto per URL. Quando la decisione dell'autore sarà presa, la prova che la distingue — un
indirizzo diverso da quello invitato accetta oppure viene respinto — si aggiunge qui.

## Learning target

Che l'appartenenza per invito basti come unico meccanismo di condivisione — nessun ruolo, nessun
permesso, tutti pari — senza che serva subito revoca o gestione degli inviti perché qualcuno resti
fuori da dove non deve stare.

## Excludes

- Revoca di un invito ed elenco degli inviti attivi: candidati in `LATER`, e la loro necessità è
  proprio ciò che questa riga misura.
- Uscire da un ricettario, che nessuna sorgente chiede.
- Ogni nozione di gruppo o team sopra i ricettari, dichiarata fuori dall'MVP.

## Open questions

- L'invito è un link aperto, e chiunque abbia il token entra, oppure è vincolato all'indirizzo di
  chi è stato invitato? `sources/concepts.md` modella solo `token` e scadenza, e le due letture
  cambiano la verifica e cambiano quanto presto servirà una gestione degli inviti. È una decisione
  dell'autore.
