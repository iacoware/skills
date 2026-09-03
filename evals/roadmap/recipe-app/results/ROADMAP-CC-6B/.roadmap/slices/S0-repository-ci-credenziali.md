# S0 — Repository, CI e credenziali

← [Register](../roadmap.md#now)

**Outcome:** Un repository Next.js + TypeScript che passa build, lint, typecheck e test su CI a
ogni push, e tutti gli account e i segreti che le righe successive spendono, già in mano.

**Requested by:** Prerequisito del repository (`drawing-the-map.md`); stack da
`sources/tech-choices.md`, servizi da `sources/arch-choices.md`.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi sviluppa: da qui in poi può aprire una PR e vedere il verde o il rosso, e nessuna riga
successiva si ferma per un account da aprire o una chiave da chiedere.

## Includes

- Repository con Next.js (App Router), TypeScript, Effect e Drizzle installati; Prettier e
  linting con la configurazione del progetto.
- Vitest configurato, con un test che dimostra che la pipeline gira davvero.
- CI su ogni push: build, lint, typecheck, test.
- Account aperti e chiavi in mano, ognuna verificata da una chiamata minima: Neon (o Supabase),
  Fly.io, Cloudflare R2 con il bucket delle foto creato, Google Cloud con il client OAuth,
  e la chiave del provider di embedding.
- Segreti come variabili d'ambiente, presenti in locale e su CI; nessuna chiave nel
  repository, e un `.env.example` che dice quali servono.

## Verification

- Una PR con un errore di tipo, una violazione di lint e un test rosso viene bloccata da CI,
  ognuno con il proprio messaggio.
- Un comando per ogni servizio, eseguito con i segreti di CI, risponde: query banale su
  Postgres, `fly auth whoami`, put e get di un oggetto su R2, embedding di una stringa.
- Il repository clonato pulito si avvia in locale seguendo solo il README.

## Learning target

Che ogni servizio deciso dalle fonti sia davvero apribile e usabile con le credenziali che
abbiamo — l'account che chiede una carta, la regione senza free tier o il client OAuth che
serve una verifica si scoprono qui e non dentro la riga che ne dipende.

## Excludes

- Qualunque provisioning o deploy: è il walking skeleton `S2`.
- Lo schema del dominio e le migrazioni: `S2` per il meccanismo, `S3` per le entità.
- La configurazione della schermata di consenso OAuth per un ambiente reale: `S7`.

## Open questions

- —
