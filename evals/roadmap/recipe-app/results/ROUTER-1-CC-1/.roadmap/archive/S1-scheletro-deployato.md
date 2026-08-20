# S1 — Scheletro deployato su Fly con Postgres e migrazioni

← [Register](../roadmap.md#now)

**Outcome:** Un container Docker su Fly risponde da un ambiente non pubblico, raggiunge Neon con il
driver reale su TCP e mostra il risultato di una migrazione applicata dal runner.

**Requested by:** `sources/arch-choices.md` (Hosting — Fly.io, Datastore — Postgres + pgvector),
`sources/tech-choices.md` (Persistenza / ORM — Drizzle).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi sviluppa: da qui in poi ogni riga successiva si deploya su una strada già percorsa, e un
fallimento di connessione o di migrazione non può più nascondersi dentro una riga di dominio.

## Includes

- Dockerfile e `fly.toml` con `auto_stop` in modalità `suspend` e scale-to-zero.
- Connessione a Neon con il driver Postgres standard su TCP, senza driver serverless.
- Runner di migrazioni Drizzle e una migrazione non di dominio che scrive un valore.
- Un endpoint che legge dal database quel valore e lo restituisce.

## Verification

Dopo un periodo di inattività la prima richiesta risponde con il valore letto da Postgres, e il
tempo di risveglio misurato è sotto il secondo; la stessa richiesta ripetuta subito dopo è
istantanea. La migrazione applicata due volte non fa danni e il runner lo dichiara. Il deploy parte
dalla CI senza che nessun segreto passi da un file.

## Learning target

Se connessione, pooling e migrazioni reggono lo scale-to-zero come le sorgenti danno per scontato, e
quanto costa davvero il primo utente dopo il silenzio.

## Excludes

- Entità di dominio, CRUD, autenticazione e tenancy: sono di `S3` e di `S8`.
- Object storage, LLM ed embedding: li validano `S10`, `S5` e `S7`, che sono i soli a usarli.
- Dominio pubblico, consent screen e tetti di spesa: sono di `S11`.

## Open questions

- —
