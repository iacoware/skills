# S1 — Scheletro deployato su Fly con Postgres

← [Register](../roadmap.md#now)

**Outcome:** L'app gira su Fly in un ambiente non di produzione, raggiunge Postgres su Neon con il
driver reale e applica una migrazione al deploy.

**Requested by:** Prerequisito dello scheletro della skill `roadmap`; l'infrastruttura da esercitare
viene da `arch-choices.md` §§ Datastore, Hosting.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Gli sviluppatori del progetto: da qui in poi una riga si considera fatta quando è deployata, e non
quando gira in locale.

## Includes

- Dockerfile e `fly.toml` con `auto_stop` in modalità `suspend` e scale-to-zero, senza volumi.
- Deploy dalla CI verso un'app Fly di staging, su ogni push su `main` che passa.
- Database Neon di staging, raggiunto via TCP con `postgres.js` e Drizzle — nessun driver
  serverless, nessun pooler HTTP.
- Migration runner Drizzle eseguito al deploy, che applica una migrazione non di dominio (una
  tabella `deploy_check`).
- Una rotta che scrive e rilegge quella tabella e restituisce l'esito.
- Verifica che l'estensione `vector` sia installabile sul database, senza creare tabelle di dominio.

## Verification

- Dopo un push su `main` la CI deploya e la rotta risponde 200 con il valore appena scritto e
  riletto dal database di staging.
- La migrazione risulta applicata sul database, e un secondo deploy non la riapplica.
- Dopo un periodo di inattività la prima richiesta risponde, e il tempo di risveglio è misurato e
  scritto: è il numero contro cui `S11` si confronterà.
- `pg_extension` mostra `vector` sul database di staging.
- La macchina non monta nessun volume e sopravvive a uno stop/start senza perdere niente.

## Learning target

Se un container Next.js su Fly con `suspend` e scale-to-zero regge una connessione TCP diretta a
Neon e un migration runner al deploy, e quanto costa in latenza il risveglio del primo utente.

## Excludes

- Entità di dominio, autenticazione e tenancy: sono di `S3` e `S6`.
- Cloudflare R2 e l'adapter di storage: è di `S8`, la sola riga che lo usa.
- Adapter di embedding e LLM: sono di `S3` e `S4`.
- Ambiente di produzione, dominio e backup: sono di `S11`.

## Open questions

- —
