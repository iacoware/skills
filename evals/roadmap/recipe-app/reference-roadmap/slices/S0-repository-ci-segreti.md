# S0 — Repository, CI e segreti

← [Register](../roadmap.md#now)

**Outcome:** Il progetto vive in un repository con la CI verde e i segreti dei servizi gratuiti a
posto.

**Requested by:** `sources/tech-choices.md`, `sources/arch-choices.md`
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi lavora al progetto, compreso l'agente: è la prima riga perché tutto il resto si consegna da qui.

## Includes

- Repository con l'applicazione Next.js in TypeScript e le convenzioni di progetto già scelte.
- Una CI che a ogni push installa, compila e lancia i test.
- Gli account dei servizi gratuiti — Fly.io, provider Postgres, Cloudflare R2, chiave per gli
  embedding — e i loro segreti in un solo posto, disponibili in locale e alla CI.

## Verification

Un push su un branch fa passare la CI; un checkout pulito parte in locale con i soli segreti
documentati e nessun passaggio a voce.

## Learning target

Quanto della catena gratuita si accende davvero senza carta di credito, e dove invece serve.

## Excludes

- Infrastruttura versionata (Terraform, SST): per l'MVP bastano `fly.toml` e la CLI di Fly.
- Ambienti di staging.
- Il deploy, che è `S1`.

## Open questions

—
