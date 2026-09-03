# S1 — Scheletro camminante: container su Fly, Postgres e migrazioni

← [Register](../roadmap.md#now)

**Outcome:** Un container Next.js deployato su Fly dalla CI che, alla prima richiesta dopo un periodo
di silenzio, si risveglia, apre una connessione TCP reale al Postgres gestito e risponde con qualcosa
che ha appena letto dal database.

**Requested by:** Prerequisito scheletro, contro `arch-choices.md` (Hosting — Fly.io, Datastore —
Postgres + pgvector) e `tech-choices.md` (connessione via driver standard su TCP).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi lavora al progetto. Da qui si deploya con un comando, e il costo del risveglio è un numero scritto
invece di una promessa.

## Includes

- `Dockerfile` per Next.js in modalità standalone e `fly.toml` con `auto_stop_machines = "suspend"`,
  `min_machines_running = 0` e una sola macchina `shared-cpu-1x` da 512MB.
- Deploy dalla CI su un'app Fly di staging, non pubblica e non indicizzabile.
- Migration runner Drizzle eseguito al deploy, con due migrazioni non di dominio:
  `CREATE EXTENSION IF NOT EXISTS vector` e una tabella `deploy_probe`.
- Un endpoint di salute che apre la connessione con il driver TCP standard, legge una riga da
  `deploy_probe` e restituisce sia il valore letto sia il risultato di una `select` su un vettore
  letterale.
- Uno script che lascia la macchina ferma abbastanza da farla sospendere e poi cronometra la prima
  richiesta.

## Verification

- Dopo un deploy dalla CI, l'endpoint risponde con un valore che viene dal database e non dalla
  memoria del processo: cambiando la riga a mano sulla console del provider, la risposta cambia.
- Il vettore letterale torna dall'endpoint: `pgvector` è attiva sul database di staging, non solo
  disponibile sul piano.
- Aggiungendo una migrazione e deployando, la migrazione risulta applicata al database di staging
  senza nessun comando eseguito a mano.
- Dopo il periodo di inattività configurato la macchina risulta sospesa, e la prima richiesta
  successiva è cronometrata: il numero è scritto nel repository.
- Nel repository non esiste nessuna tabella di dominio, nessuna sessione e nessun `cookbookId`.

## Learning target

Che un container Node su Fly con `suspend` e scale-to-zero regga una connessione TCP diretta al
Postgres gestito e applichi le migrazioni al deploy — e quanto costa davvero il primo colpo dopo il
silenzio, che `arch-choices.md` dà per sub-secondo e che nessuna riga successiva può misurare più a
buon mercato.

## Excludes

- L'adapter R2 e l'adapter LLM → `S9` e `S5`, cioè le righe che li usano per prime: metterli qui
  sarebbe rischio senza consumatore.
- Autenticazione, entità di dominio e scope del ricettario → `S3` e `S7`.
- Dominio pubblico, database di produzione e schermata di consenso Google → `S10`.
- La macchina sempre calda → `LATER`, ed è un flag da cambiare, non una riscrittura.

## Open questions

- —
