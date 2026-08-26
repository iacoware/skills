# S1 — Scheletro deployato su Fly con Postgres

← [Register](../roadmap.md#now)

**Outcome:** Un percorso deployato minimo prova che il container Next.js su Fly parla con
Neon attraverso il driver reale, applica una migrazione e si riaddormenta.

**Requested by:** `arch-choices.md` §§ Hosting, Datastore; la regola della mappa che chiede
uno scheletro camminante prima di qualunque promessa.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi costruisce l'app: da qui in poi ogni riga si verifica sull'ambiente vero invece che sul
portatile.

## Includes

- Dockerfile e `fly.toml` con `auto_stop` in modalità `suspend` e nessuna macchina minima
  accesa, come raccomandato dalle fonti.
- Deploy dalla CI su push del ramo principale.
- Drizzle con driver Postgres su TCP verso Neon, connessione aperta a runtime dal container.
- Una migrazione non di dominio: una tabella tecnica di prova e `CREATE EXTENSION vector`.
- Un endpoint di salute che scrive e rilegge una riga di quella tabella ed esegue una query
  che tocca il tipo `vector`.
- Misura del tempo della prima richiesta dopo un periodo di silenzio, annotata nel
  repository.

## Verification

Dopo un push, l'ambiente risponde riportando l'esito di scrittura, rilettura e query
vettoriale su Neon. Su una macchina appena creata la migrazione risulta applicata dal runner,
non a mano. Dopo trenta minuti di inattività la prima richiesta viene cronometrata e il
numero è scritto accanto alla soglia che le fonti dichiarano accettabile (risveglio
sub-secondo con `suspend`); se non la rispetta, il numero è il risultato.

## Learning target

Che container su Fly, connessione TCP a Neon, runner di migrazioni e scale-to-zero con
`suspend` reggano insieme, e quanto costi davvero la prima richiesta dopo il silenzio.

## Excludes

- Entità di dominio, CRUD, autenticazione e ricettari: nulla di tutto questo entra qui, la
  prima è `S3`.
- Dominio pubblico, TLS e apertura agli utenti: sono di `S11`.
- Adapter verso storage foto e modelli: li validano le righe che li usano.

## Open questions

- —
