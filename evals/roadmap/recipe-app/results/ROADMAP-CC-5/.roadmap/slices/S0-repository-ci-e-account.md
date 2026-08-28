# S0 — Repository, CI e account

← [Register](../roadmap.md#now)

**Outcome:** Il repository esiste, la CI gira verde su ogni push, e tutti gli account e i segreti che
il resto della mappa spende sono aperti e raggiungibili.

**Requested by:** Prerequisito di repository della skill; gli account escono dalle scelte già prese
in `arch-choices.md` (*Datastore*, *Object storage*, *Hosting*, *Embeddings*) e in `tech-choices.md`
(*Auth*).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi sviluppa: da qui in poi ogni riga trova un posto dove committare, una pipeline che la boccia se
si rompe, e le credenziali dei servizi che deve chiamare.

## Includes

- Repository TypeScript con Next.js (App Router), Effect, Drizzle e Vitest installati.
- CI che su ogni push esegue build, lint, typecheck e test, e fallisce il push se uno dei quattro
  fallisce.
- Progetto Postgres aperto sul provider scelto, con l'estensione `vector` disponibile, e stringa di
  connessione a disposizione della CI e dello sviluppo locale.
- Bucket Cloudflare R2 e relative credenziali.
- Client OAuth Google creato, con i redirect URI dell'ambiente di staging.
- Chiavi per il provider di embedding e per il provider LLM.
- Tutti i segreti in un unico posto documentato, e nessuno di essi nel repository.

## Verification

Un push su un branch pulito fa passare i quattro job della CI; un push che introduce un errore di
tipo o un test rosso viene bocciato. Uno script eseguito dalla macchina di sviluppo si connette al
Postgres del provider, esegue `CREATE EXTENSION IF NOT EXISTS vector` e la trova disponibile. Uno
script scrive e rilegge un oggetto di prova su R2. Il client OAuth Google restituisce una pagina di
consenso invece di un errore di configurazione. Una ricerca dei segreti nel repository non trova
nulla.

## Learning target

Se i servizi gratuiti su cui la mappa poggia si aprono davvero e sono raggiungibili come le fonti
assumono — in particolare se il provider Postgres scelto espone `pgvector` sul suo piano gratuito
senza richiedere un upgrade.

## Excludes

- Nessun deploy e nessun provisioning dell'app: sono di S1.
- Nessuno schema di dominio e nessuna migrazione applicativa: la prima migrazione, non di dominio,
  è di S1.
- IaC versionata: le fonti scelgono `fly.toml` più CLI per l'MVP; Terraform e SST sono in `LATER`.

## Open questions

- `arch-choices.md` dice "Neon **o** Supabase" e non sceglie. La riga non può aprire l'account
  finché non è deciso quale dei due, e la scelta si porta dietro il modo di connessione e i limiti
  del piano gratuito su cui S1 poggia.
