# S0 — Repository, CI, account e segreti

← [Register](../roadmap.md#now)

**Outcome:** Esiste il repository con la catena di strumenti che tutta la mappa dà per scontata, una
CI che la tiene verde a ogni push, e gli account con i loro segreti pronti per essere spesi dalle
righe successive.

**Requested by:** `references/drawing-the-map.md`, il prerequisito del repository; le scelte di stack
di `sources/tech-choices.md` e i servizi di `sources/arch-choices.md`.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi costruisce l'app. Dopo questa riga può aprire un branch, spingere e vedere in due minuti se ha
rotto qualcosa, senza avere ancora deployato niente e senza dover aprire un account nel mezzo di
un'altra riga.

## Includes

- Progetto Next.js con App Router e TypeScript end-to-end, Effect, Drizzle e Vitest installati e con
  un esempio minimo di ciascuno che gira: un servizio `Context.Tag` con il suo `Layer`, uno schema
  Drizzle vuoto, un test.
- Prettier ed ESLint configurati secondo le convenzioni di progetto, e i comandi `build`, `lint`,
  `typecheck`, `test` come script.
- Pipeline CI che esegue quei quattro comandi a ogni push e a ogni pull request.
- Gli account che la mappa spende, aperti: Neon, Cloudflare R2 con il bucket e il token, Fly.io,
  Google Cloud per il futuro client OAuth, il provider di embedding e di LLM.
- I segreti raccolti nel secret store della CI e del deploy, e uno script di smoke che, girando in
  locale con quei segreti, tocca ogni provider una volta e dice quali rispondono.
- `.env.example` che elenca ogni variabile senza portarne nessun valore.

## Verification

Un push con un errore di tipo deliberato fa fallire la CI sul passo `typecheck` e non su un altro; un
push verde mostra nel log che tutti e quattro i comandi sono girati davvero. Lo script di smoke
elenca, per ciascuno dei cinque provider, se la credenziale è valida — e fallisce nominando il
provider quando non lo è. Nessun segreto compare nel repository: una scansione del contenuto versato
non trova nessuna delle chiavi. Il progetto parte in locale con `dev` e serve una pagina.

## Learning target

La catena di strumenti che l'intera mappa presuppone — Next.js con TypeScript, Effect, Drizzle e
Vitest sotto CI — compila e gira verde tutta insieme prima che ci sia sopra una riga di codice di
prodotto, e le cinque credenziali che serviranno esistono e rispondono.

## Excludes

- Nessun provisioning dello schema, nessuna migrazione, nessun deploy: sono dello scheletro, che è la
  riga successiva proprio perché una CI verde non dice niente sull'hosting.
- Nessuna entità di dominio e nessun componente di prodotto: le convenzioni nascono nella prima riga
  che ne ha bisogno, non qui.
- Nessun client OAuth configurato: le callback URL esistono solo dopo che esiste un'URL deployata, e
  appartengono alla riga dell'identità.

## Open questions

—
