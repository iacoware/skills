# S0 — Repository, CI e conti da spendere

← [Register](../roadmap.md#now)

**Outcome:** Un repository che compila con CI verde su build, lint, typecheck e test, e tutti i conti
e i segreti che il resto della mappa spenderà già aperti e in mano.

**Requested by:** Prerequisito repository, contro `tech-choices.md` (stack) e `arch-choices.md`
(Riepilogo costi), che elencano i servizi che ogni riga successiva presuppone.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi lavora al progetto. Da qui in poi ogni riga si apre su un repository che compila e su credenziali
che esistono davvero, invece di fermarsi a metà per aprire un conto.

## Includes

- Repository Next.js in App Router e TypeScript, con Effect, Drizzle, React Query e Vitest
  installati, e la formattazione decisa una volta sola.
- Pipeline CI che a ogni push gira build, lint, typecheck e test, e blocca il merge quando è rossa.
- Progetto Google Cloud con client OAuth e i redirect di sviluppo e di staging registrati.
- Database Postgres creato presso il provider scelto, sul piano gratuito.
- Bucket Cloudflare R2 con un token di sola scrittura per l'applicazione.
- Chiavi API per i candidati embedding che `S2` metterà a confronto e per il provider di estrazione
  LLM, ognuna con un tetto di spesa impostato sul cruscotto del provider.
- Un solo posto dove i segreti vivono: `.env` locale non versionato e secrets di CI e di Fly,
  entrambi elencati in un `.env.example` versionato.

## Verification

- La CI è verde su un commit qualunque e rossa su un commit con un errore di tipo introdotto apposta:
  i quattro passi girano davvero e non sono decorativi.
- Ogni voce di `.env.example` ha un valore reale in CI, e un controllo eseguibile fallisce quando ne
  manca una.
- Il piano gratuito del database scelto espone `pgvector`: `CREATE EXTENSION vector` gira a mano
  sulla console del provider e ritorna senza errore.
- Sul cruscotto del provider LLM e di quello embedding il limite di spesa è un numero, non "nessuno".

## Learning target

Che tutte le credenziali che l'MVP richiede si ottengano a costo zero e che il piano gratuito del
provider Postgres scelto offra davvero `pgvector` — che è il pezzo su cui poggia il differenziatore e
il primo posto dove un piano gratuito può deludere.

## Excludes

- Ogni provisioning e ogni deploy → `S1`. Qui si aprono conti, non si accende niente.
- Lo schema di dominio e le migrazioni applicative → `S3`.
- La configurazione di produzione, il dominio e la schermata di consenso Google per utenti esterni →
  `S10`.

## Open questions

- Neon o Supabase. `arch-choices.md` li nomina in alternativa e non ne sceglie uno. La scelta decide
  dove si apre il conto, quale driver e quale modalità di connessione `S1` valida, quali limiti di
  connessione l'app dovrà rispettare e come si fa il backup — e smette di essere reversibile a costo
  zero appena ci sono dentro le prime ricette.
