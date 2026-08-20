# S1 — Walking skeleton in produzione

← [Register](../roadmap.md#now)

**Outcome:** Una pagina servita da Fly.io legge una riga da Postgres, anche a macchina spenta.

**Requested by:** `sources/arch-choices.md` § Hosting, § Datastore
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Nessun utente finale ancora: serve a tutte le righe che vengono dopo, che consegnano su questa catena.

## Includes

- L'app Next.js in container su Fly.io, con `suspend` e scale-to-zero.
- Postgres del provider scelto, con `pgvector` abilitato e Drizzle sopra.
- Una pagina che legge una riga scritta da una migrazione.

## Verification

Aprendo l'URL pubblico dopo un periodo di silenzio la pagina mostra il dato letto dal database, e il
risveglio della macchina non è un errore ma un'attesa.

## Learning target

Che la catena Next.js in container → Fly.io con la macchina che si spegne → Postgres del provider
regga end-to-end, cold start compreso.

## Excludes

- Dominio proprio, che arriva con `S14`.
- Autenticazione e qualunque contenuto di prodotto.
- Macchina sempre calda: è una candidate, non una riga.

## Open questions

- Neon o Supabase? Entrambi hanno `pgvector` nel piano gratuito e i sorgenti lasciano la scelta
  aperta. È una decisione dell'autore e non è stata presa.
