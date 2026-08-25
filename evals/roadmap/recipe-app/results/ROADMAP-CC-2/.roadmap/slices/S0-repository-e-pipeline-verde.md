# S0 — Repository e pipeline verde

← [Register](../roadmap.md#now)

**Outcome:** Il repository esiste con l'app Next.js e TypeScript inizializzata, e ogni commit fa
girare in CI build, lint, typecheck e test; gli account e i segreti che il resto della mappa spende
sono aperti e raggiungibili.

**Requested by:** Prerequisito di repository per il lavoro greenfield; stack da `tech-choices.md`
(TypeScript, Next.js App Router, Effect, Drizzle, Vitest), account da `arch-choices.md` (§ Riepilogo
costi) e da `tech-choices.md` (§ Auth).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi sviluppa. Dopo questa riga può fare un commit e sapere entro pochi minuti se ha rotto qualcosa,
e può deployare in S1 senza fermarsi ad aprire account.

## Includes

- Repository git con Next.js (App Router) e TypeScript, Prettier configurato secondo le convenzioni
  di progetto, e Vitest con un test che gira davvero.
- Pipeline CI che esegue, su ogni push, build, lint, typecheck e test, e che è rossa quando uno dei
  quattro fallisce.
- `Dockerfile` che costruisce l'immagine dell'app, costruito in CI ma non ancora deployato.
- Apertura degli account e raccolta dei segreti che le righe successive spendono: provider Postgres,
  Fly.io, Cloudflare R2, Google Cloud per le credenziali OAuth, provider LLM ed embedding. I segreti
  sono in un `.env.example` documentato e nei secret della CI, mai nel repository.
- Un `README` che dice come far girare l'app in locale e quali variabili servono.

## Verification

Un push su un branch fa girare i quattro passi e la pipeline è verde. Introducendo di proposito un
errore di tipo la pipeline diventa rossa sul typecheck; introducendo un test che fallisce diventa
rossa sui test; rimuovendoli torna verde. Il `Dockerfile` costruisce l'immagine in CI. Ogni account
della lista è aperto e il relativo segreto è presente nella CI, verificato leggendone il nome, non il
valore.

## Learning target

La pipeline decisa — Next.js in container, con lint, typecheck e test — sta in piedi e dà un segnale
onesto prima che ci sia dominio da rompere: quando in S1 il deploy fallirà, non potrà essere colpa
del build.

## Excludes

- Qualunque provisioning e qualunque deploy: sono di S1, che è una riga a sé perché una CI verde non
  dice nulla sull'ipotesi di hosting.
- Lo schema del database e le migration: nascono in S1 con la prima migration non di dominio.
- La scelta del modello LLM e del modello di embedding: si apre l'account presso il provider, il
  modello lo scelgono S5 e S2.

## Open questions

- —
