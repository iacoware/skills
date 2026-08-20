# S6 — Accesso con Google

← [Register](../roadmap.md#now)

**Outcome:** Si entra con il proprio account Google e le pagine dell'app sono private.

**Requested by:** `sources/goal.md` § Auth, `sources/tech-choices.md` § Auth
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chiunque apra l'app: da qui in poi le ricette appartengono a qualcuno.

## Includes

- Auth.js con il provider Google e la sessione su Postgres.
- Il client OAuth e la schermata di consenso creati sulla console Google.
- Le pagine dell'app dietro sessione.

## Verification

Da disconnessi le pagine rimandano al login; entrando con un account Google si torna esattamente
dove si era.

## Learning target

Che delegare identità e recupero account a Google tolga davvero dall'MVP email, password e flusso di
reset, e non li sposti da un'altra parte.

## Excludes

- Passkey, email e password: la prima è una candidate, le altre sono escluse.
- Ruoli: l'unico è `creatorId`, e arriva con `S12`.

## Open questions

—
