# S0 — Repository, CI e account dei servizi

← [Register](../roadmap.md#now)

**Outcome:** Il repository esiste, la CI gira su ogni push, e tutti gli account e i segreti che la
mappa spenderà sono aperti e raggiungibili.

**Requested by:** Prerequisito di repository della skill `roadmap`; i servizi da aprire vengono da
`arch-choices.md` § Riepilogo costi e da `tech-choices.md` § Auth.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Gli sviluppatori del progetto: da qui in poi ogni riga parte da un albero verde e da credenziali
già disponibili, invece di fermarsi ad aprire un account a metà di un'altra riga.

## Includes

- Repository Git con progetto Next.js (App Router) in TypeScript, Effect e Drizzle installati.
- Pipeline CI su ogni push: build, lint, typecheck, test.
- Account aperti e verificati: Fly.io, Neon, Cloudflare R2, Google Cloud con un client OAuth in
  modalità test, il provider di embeddings e il provider LLM.
- Segreti nel secret store della CI, e `.env.example` che elenca ogni variabile che le righe
  successive useranno.
- Nessun provisioning e nessun deploy.

## Verification

- Un push con un errore di tipo fa fallire la CI; un push pulito la fa passare, con un test di
  esempio che gira davvero.
- `.env.example` elenca ogni variabile prevista dalla mappa e il repository non contiene nessun
  segreto.
- Ogni account risponde a una chiamata di verifica autenticata (CLI o richiesta) fatta da una
  persona del team, e nessuno di essi ha richiesto un piano a pagamento per essere aperto.

## Learning target

Se la catena scelta — TypeScript, Next.js, Effect, Drizzle — sta in piedi insieme in CI, e se i
servizi previsti si aprono tutti senza carta di credito obbligatoria o vincoli che
`arch-choices.md` non aveva previsto.

## Excludes

- Deploy e provisioning: sono di `S1`.
- Schema e migrazioni di dominio: sono di `S3`.
- IaC versionata: candidato in `LATER`, per l'MVP bastano `fly.toml` e la CLI.

## Open questions

- —
