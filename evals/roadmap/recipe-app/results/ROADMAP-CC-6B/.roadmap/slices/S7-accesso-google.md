# S7 — Accesso con Google e scope autenticato

← [Register](../roadmap.md#now)

**Outcome:** Entro con il mio account Google e vedo il mio ricettario: lo scope non è più
configurato, viene dalla sessione e dalla membership.

**Requested by:** `sources/goal.md` § Auth — decisione presa: Google OAuth;
`sources/concepts.md` § User, Membership.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi userà l'app: entra col proprio account Google, e da qui in poi quello che vede è suo e non
di chi ha configurato il server.

## Includes

- Auth.js (NextAuth v5) con il solo provider Google, sessione persistita su Postgres via
  Drizzle, tabelle in migrazione.
- Al primo accesso l'utente ottiene un ricettario personale e la propria `Membership`.
- Il resolver `currentCookbook` introdotto in `S3` smette di leggere la configurazione e ricava
  il ricettario dalla sessione e dalle membership dell'utente; nessuna query di ricetta cambia.
- Ogni pagina e ogni azione richiedono una sessione; chi non è autenticato vede la schermata di
  accesso.
- Schermata di consenso OAuth e redirect URI configurati per gli ambienti in uso.

## Verification

- Due utenti Google diversi entrano e ognuno vede solo il proprio ricettario, in elenco e in
  ricerca.
- Un URL diretto a una ricetta di un altro utente risponde come se non esistesse, non con un
  errore che ne rivela l'esistenza.
- Un utente non autenticato non raggiunge nessuna pagina se non l'accesso.
- Il diff di questa riga tocca il resolver, non le query di ricetta: nessuna query ha dovuto
  aggiungere un filtro che prima non aveva.
- La sessione sopravvive alla sospensione e al riavvio della macchina.

## Learning target

Che il seam scelto in `S3` regga: sostituire uno scope configurato con uno autenticato è un
cambio in un punto solo, e le righe scritte prima non vanno riscritte. Se questa riga si allarga
alle query, il seam era finto e ogni riga futura pagherà lo stesso prezzo.

## Excludes

- Inviti, membri multipli e ricettari multipli: `S8`.
- Ruoli e permessi: fuori scope, l'unico controllo è la membership.
- Passkeys, email e password: fuori scope dichiarato.

## Open questions

- —
