# S1 — Scheletro deployato su Fly con Postgres

← [Register](../roadmap.md#now)

**Outcome:** L'app gira su Fly in un ambiente non pubblico, si spegne da sola e si risveglia, e una
sua rotta legge da Postgres attraverso Drizzle e il driver reale una tabella non di dominio creata da
una migrazione applicata dal runner.
**Requested by:** Prerequisito dello scheletro, dalla skill `roadmap`; infrastruttura da
`arch-choices.md` (§ Datastore, § Hosting) e `tech-choices.md` (§ Persistenza / ORM).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi sviluppa. Dopo questa riga può spedire una modifica e vederla in un ambiente vero che parla col
database vero, invece di scoprire dentro la prima riga di dominio se il problema è il driver, la
connessione, la migrazione o il risveglio della macchina.

## Includes

- `Dockerfile` e `fly.toml` con `auto_stop` in modalità `suspend` e scale-to-zero, come raccomanda
  `arch-choices.md`.
- Database Postgres con l'estensione pgvector abilitata presso il fornitore scelto.
- Drizzle configurato sul driver TCP scelto, con runner di migrazioni eseguito al deploy.
- Una migrazione non di dominio e una rotta di salute che legge quella tabella attraverso il driver
  reale e restituisce quello che ha letto.
- Deploy da CI sull'ambiente non pubblico, con i segreti presi da S0.

## Verification

- Un deploy da CI porta la modifica online e la rotta di salute risponde con il dato letto dal
  database, non con una costante.
- Dopo un periodo di inattività la macchina risulta sospesa; la prima richiesta successiva riceve la
  stessa risposta, e il tempo di risveglio è misurato e scritto.
- Una seconda migrazione non di dominio viene applicata dal runner al deploy senza intervento a mano,
  e la rotta di salute ne mostra l'effetto.
- La rotta di salute continua a rispondere dopo che la macchina è stata sospesa e risvegliata due
  volte di seguito, cioè la connessione non resta appesa allo stato precedente.

## Learning target

Che il fornitore Postgres scelto, il driver TCP e il pooling reggono il ciclo sospensione-risveglio
di Fly, e quanto costa in tempo la prima richiesta dopo il silenzio — le due incertezze che dentro
una riga di dominio non si saprebbe a chi attribuire.

## Excludes

- Entità di dominio, CRUD, autenticazione e nozione di ricettario: la prima tabella di dominio e il
  suo confine di scope sono di S3.
- L'adapter Cloudflare R2, che serve solo a S9, e gli adapter di embedding ed estrazione, che S2, S3
  e S4 validano dove servono.
- Dominio personalizzato, ambiente di produzione e apertura agli utenti: sono di S10.
- IaC versionata: `arch-choices.md` la dichiara over-engineering per l'MVP, bastano `fly.toml` e CLI.

## Open questions

- Neon o Supabase? `arch-choices.md` li nomina entrambi come free tier con pgvector e non sceglie.
  La differenza che conta qui è il comportamento della connessione con una macchina che si sospende.
- `postgres.js` o `node-postgres`? `tech-choices.md` li nomina entrambi come driver standard su TCP e
  non sceglie.
