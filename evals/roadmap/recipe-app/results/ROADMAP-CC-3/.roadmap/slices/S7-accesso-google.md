# S7 — Accesso Google e ricettari reali

← [Register](../roadmap.md#now)

**Outcome:** Si entra con il proprio account Google, si vedono i ricettari di cui si è membri e si
passa dall'uno all'altro; da qui in avanti elenco e ricerca hanno lo scope di chi è entrato, non
uno configurato.

**Requested by:** `sources/goal.md` § Auth, che sceglie Google OAuth, e § Condivisione;
`sources/tech-choices.md` § Auth per Auth.js su Postgres; `sources/concepts.md` § User, § Cookbook
e § Membership.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Familiari e amici: è la prima riga con un utente finale vero. Dopo, ognuno entra con la propria
identità e vede i propri ricettari, e nessuno vede quelli degli altri.

## Includes

- Auth.js v5 con provider Google e adapter Drizzle, sessione su Postgres.
- Tabelle `user` e `membership`, e `creatorId` su `cookbook`.
- Il resolver `currentCookbook` sostituisce lo scope configurato con quello autenticato: è il solo
  punto della base di codice che cambia.
- Creazione di un ricettario, e creazione automatica di un ricettario di default al primo accesso
  di chi non ne ha nessuno, con lui come creator.
- Selettore del ricettario corrente, che sopravvive alla sessione.
- Ogni percorso non autenticato porta al login; il ricettario seed viene rimosso o assegnato.

## Verification

Due account Google diversi vedono elenchi e risultati di ricerca disgiunti. Chi chiede una ricetta
di un ricettario di cui non è membro riceve un rifiuto esplicito, non una pagina vuota che si può
scambiare per «non ci sono ricette». Cambiando ricettario corrente, elenco e ricerca cambiano
scope, e la scelta resta dopo un nuovo accesso. Al primo accesso di un account nuovo esiste già un
ricettario suo. Fuori dal resolver e dalla sua registrazione, il codice delle righe precedenti non
cambia: è la prova che il punto di sutura ha tenuto, ed è verificabile leggendo il diff.

## Learning target

Che il seam di identità dichiarato dalla mappa regga davvero: sostituire uno scope configurato con
uno autenticato in un posto solo, senza riscrivere elenco, form, estrazione e ricerca costruiti
prima che l'identità esistesse.

## Excludes

- Gli inviti e ogni membership creata da qualcuno che non sia il proprietario dell'account: sono la
  riga della condivisione.
- Ruoli e permessi oltre a `creatorId`, esclusi dalle sorgenti.
- Passkeys, email e password, tutti scartati dalle sorgenti con la loro ragione.

## Open questions

- —
