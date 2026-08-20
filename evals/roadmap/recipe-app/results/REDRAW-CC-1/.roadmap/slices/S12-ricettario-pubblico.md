# S12 — Ricettario pubblico, leggibile senza account

← [Register](../roadmap.md#now)

**Outcome:** Chi ha creato un ricettario lo rende pubblico e tematico, e chiunque apre il link e lo
legge senza account; i ricettari privati restano irraggiungibili e togliere la visibilità è
immediato.

**Requested by:** La nuova meta dichiarata dall'autore (ricettari tematici pubblici leggibili senza
account), `sources/concepts.md` (Cookbook — `visibility` private | public), `sources/goal.md` (Fuori
scope MVP — ricettari pubblici tematici, abilitabili come Cookbook con `visibility=public` senza
migrazione).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi ha creato un ricettario: lo apre al mondo con un gesto e se lo riprende con lo stesso gesto. E
chiunque abbia il link: legge le ricette senza account, senza registrazione e senza sapere che
esiste un login.

## Includes

- Il valore pubblico di `Cookbook.visibility`, che `S8` aveva già portato inutilizzato, e il gesto
  che lo cambia nei due sensi dalla scheda del ricettario.
- Una descrizione breve del ricettario accanto al nome, che è il modo in cui chi pubblica dichiara
  di che tema parla: la sola cosa che rende "tematico" un ricettario.
- L'autorità di lettura risolta in un solo punto, quello che oggi risolve lo scope: membership per il
  privato, `visibility=public` per l'anonimo. Nessuna seconda strada, e le scritture continuano a
  passare dalla sola membership.
- Le pagine pubbliche del ricettario e della ricetta, raggiungibili senza sessione, con
  l'attribuzione e il link a `sourceUrl` dove esiste.
- Nessun dato personale di un membro sulla pagina pubblica.

## Verification

Un browser senza sessione apre un ricettario pubblico e le sue ricette; lo stesso browser su un
ricettario privato non ottiene niente, nemmeno conoscendone gli id, e nemmeno chiamando l'API che
serve la pagina. Un membro di un ricettario privato continua a vederlo esattamente come prima: i test
di membership consegnati passano invariati e nessuna riga precedente è stata riscritta. Togliere la
visibilità pubblica rende la stessa pagina inaccessibile all'anonimo alla richiesta successiva. Ogni
tentativo di scrittura da anonimo viene rifiutato, su ogni rotta. Nessuna pagina pubblica contiene
l'email di un membro: un `grep` sulla risposta non ne trova.

## Learning target

Se il seam dello scope regge un secondo percorso di lettura, questa volta anonimo — cioè se la
modalità privata sopravvive intatta all'apertura al pubblico, o se l'autorizzazione va rifatta da
capo adesso che le autorità sono due.

## Excludes

- La ricerca sul corpus pubblico, la vetrina e i metadati per i motori: sono di `S13`, `S15` e `S14`,
  che leggono attraverso il confine stabilito qui e non lo riaprono.
- Il seed di ricettari pubblici veri su cui la scoperta ha senso: è di `S13`, che è la riga a cui la
  dimensione del corpus serve.
- Moderazione, segnalazione e curatela: restano candidate; la sola via d'uscita è togliere dal
  pubblico, e la possiede questa riga.
- Pubblicare una singola ricetta senza il suo ricettario: escluso dalla mappa, con il prezzo scritto.

## Open questions

- Cosa può mostrare la pagina pubblica del materiale estratto da una pagina altrui — l'immagine
  ripresa e ricaricata sul nostro storage in particolare. È la domanda aperta a livello di mappa:
  `Includes` e `Verification` qui sono scritte per non anticiparne la risposta.
- Chi ha il diritto di pubblicare: qualunque membro, o soltanto chi ha creato il ricettario, o
  nessuno senza un passaggio da noi. Anche questa è aperta a livello di mappa, e questa riga non ne
  sceglie una.
