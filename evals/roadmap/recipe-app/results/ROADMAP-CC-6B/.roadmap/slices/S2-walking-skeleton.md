# S2 — Walking skeleton: Next.js su Fly con Postgres e migrazioni

← [Register](../roadmap.md#now)

**Outcome:** L'app deployata su Fly risponde a una rotta che legge e scrive su Postgres
attraverso il driver vero, e le migrazioni sono girate in quel deploy.

**Requested by:** Prerequisito del walking skeleton (`drawing-the-map.md`); hosting e datastore
da `sources/arch-choices.md`, driver e ORM da `sources/tech-choices.md`.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi sviluppa: da qui in poi ogni riga può assumere che deploy, connessione al database e
migrazioni funzionino, e un guasto in quei tre punti non si presenta più dentro una riga di
dominio.

## Includes

- Dockerfile e `fly.toml` con `auto_stop` in modalità `suspend` e scale-to-zero; container
  senza volumi.
- Connessione a Neon via `postgres.js` e Drizzle su TCP, con il numero di connessioni scelto
  per una macchina che si sospende.
- Runner di migrazioni Drizzle, eseguito nel deploy, con una migrazione non di dominio: una
  tabella `heartbeat` e `CREATE EXTENSION vector`.
- Una rotta `/health` che scrive e rilegge una riga di `heartbeat` e dichiara la versione
  di migrazione applicata e la presenza dell'estensione `vector`.
- Deploy dalla CI di `S0` sul push su `main`, verso un ambiente non di produzione.

## Verification

- Dopo un deploy pulito, `/health` risponde con la riga riscritta, la versione di migrazione e
  `vector` presente.
- Dopo un periodo di inattività sufficiente a far sospendere la macchina, la prima richiesta a
  `/health` risponde correttamente, e il tempo che ci ha messo è dichiarato.
- Una migrazione aggiunta e pushata risulta applicata dopo il deploy, senza interventi a mano.
- Il log di una richiesta è leggibile da `fly logs`.

## Learning target

Che la combinazione decisa dalle fonti — container su Fly che si sospende, Postgres gestito
raggiunto in TCP, migrazioni nel deploy — stia insieme, e in particolare che la ripresa da
`suspend` non lasci connessioni morte a carico del primo utente.

## Excludes

- Entità di dominio, autenticazione e ricettari: `S3` e `S7`.
- R2 e i provider LLM: sono adapter che una riga sola usa, e li valida quella riga — `S10`,
  `S4`, `S6`.
- Dominio, ambiente di produzione e macchina sempre calda: `S11`.

## Open questions

- —
