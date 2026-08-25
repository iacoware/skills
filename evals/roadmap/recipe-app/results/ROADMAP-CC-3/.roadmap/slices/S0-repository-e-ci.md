# S0 — Repository e CI verde

← [Register](../roadmap.md#now)

**Outcome:** Il repository esiste con la toolchain decisa dentro, la CI gira build, lint, typecheck
e test a ogni push, e tutti gli account e i segreti che la mappa spenderà sono aperti e in mano al
team.

**Requested by:** Prerequisito di repository richiesto dal metodo prima di qualunque promessa. Che
cosa mettere dentro lo dicono `sources/tech-choices.md` per lo stack e `sources/arch-choices.md`
§ Riepilogo costi per i servizi da aprire.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi lavorerà su tutte le righe successive, persone e agenti. Dopo questa riga possono aprire una
modifica e sapere in pochi minuti se rompe qualcosa, senza chiedere credenziali a nessuno.

## Includes

- Repository git con Next.js in App Router e TypeScript, Effect, Drizzle, vitest e la
  configurazione Prettier del progetto.
- Convenzione di test co-locati accanto al sorgente, e la cartella dei test di integrazione.
- Pipeline CI su ogni push: build, lint, typecheck, test. Nessun deploy.
- Account aperti e credenziali generate: client OAuth su Google Cloud, progetto Neon, bucket e
  chiavi Cloudflare R2, organizzazione Fly, chiavi del provider di embeddings e del provider LLM.
- Elenco versionato dei segreti che l'applicazione richiede, con il valore custodito fuori dal
  repository e registrato come secret di CI e della piattaforma.

## Verification

Un push su un branch fa girare la pipeline e la porta a verde. Un errore di tipo introdotto apposta
la porta a rosso, e un test rotto anche: la CI fallisce per la ragione giusta e non solo quando
compila. L'elenco dei segreti è nel repository e per ogni voce esiste un valore reale utilizzabile,
che nel repository non compare. Nessun ambiente viene creato e nessun deploy parte.

## Learning target

Che la toolchain decisa — Next.js, Effect, Drizzle, vitest — stia in piedi insieme in CI senza
attriti, e che ogni servizio previsto dalla mappa sia apribile adesso: nessuno richiede verifiche,
carte di credito bloccanti o approvazioni che si scoprirebbero solo mentre serve.

## Excludes

- Ogni provisioning e ogni deploy: appartengono allo scheletro, che è una riga a sé perché una CI
  verde non dice niente su un ambiente che si accende.
- Ogni entità di dominio e ogni schema applicativo.
- L'autenticazione funzionante: qui si generano solo le credenziali Google, l'accesso arriva molto
  più avanti.

## Open questions

- —
