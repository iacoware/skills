# S0 — Repository, CI verde e account aperti

← [Register](../roadmap.md#now)

**Outcome:** Il repository esiste, la CI gira build, lint, typecheck e test a ogni push, e tutti gli
account e i segreti che il resto della mappa spenderà sono aperti e in mano al team.

**Requested by:** `sources/tech-choices.md` (stack), `sources/arch-choices.md` (riepilogo costi e
servizi), `sources/goal.md` (Auth — decisione presa: Google OAuth).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi sviluppa: da qui in poi una modifica sbagliata viene fermata prima di arrivare in main, e nessuna
riga successiva si ferma ad aspettare che qualcuno apra un account.

## Includes

- Repository con Next.js in App Router e TypeScript end-to-end, Effect, Drizzle, React Query,
  Prettier con la configurazione del progetto.
- Workflow di CI che esegue build, lint, typecheck e test su ogni push e su ogni pull request.
- Account aperti e credenziali emesse: Neon, Cloudflare R2, Fly.io, Google Cloud con il client OAuth,
  il provider di embedding e il provider del modello di fallback.
- I segreti registrati come Fly secrets e come secret della CI, mai in un file versionato.

## Verification

Una pull request che introduce un errore di tipo e un test rosso viene bloccata dalla CI, e il
messaggio dice quale dei quattro passi ha fallito. Ogni segreto che le righe successive spenderanno è
leggibile dal comando di deploy e da nessun file del repository: un `grep` sul repository non ne
trova nemmeno uno.

## Learning target

Se la toolchain scelta dalle sorgenti — Next.js, Effect, Drizzle, TypeScript stretto — sta in piedi
insieme in una CI verde senza compromessi che nessuno ha dichiarato.

## Excludes

- Nessun provisioning e nessun deploy: il primo ambiente vivo è `S1`.
- Nessuna entità di dominio, nessuna migrazione applicativa: sono di `S3`.
- IaC versionata: resta candidata, qui bastano `fly.toml` e la CLI.

## Open questions

- —
