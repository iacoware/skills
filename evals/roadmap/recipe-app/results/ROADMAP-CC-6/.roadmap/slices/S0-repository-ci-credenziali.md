# S0 — Repository, CI e credenziali

← [Register](../roadmap.md#now)

**Outcome:** Il repository esiste con l'app Next.js che compila, e una pipeline che su ogni push
esegue build, lint, typecheck e test; gli account e i segreti che il resto della mappa spende sono
aperti e depositati.
**Requested by:** Prerequisito del repository, dalla skill `roadmap`; le credenziali sono l'elenco
dei servizi scelti in `arch-choices.md` e `tech-choices.md`.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi sviluppa. Dopo questa riga può clonare, far girare l'app in locale e vedere una pipeline rossa o
verde su una pull request, invece di scoprire i problemi di configurazione dentro la prima riga di
dominio.

## Includes

- Repository con progetto Next.js in TypeScript (App Router) che parte in locale.
- Effect, Drizzle, TanStack React Query e il runner dei test installati e importati almeno una volta,
  perché la pipeline ne dimostri la compilazione.
- Pipeline CI su push e pull request: build, lint, typecheck, test.
- Un test che passa e uno strumento di lint che ha qualcosa da dire, così che il verde non sia vuoto.
- Apertura degli account e deposito dei segreti come segreti di CI e come `.env.example`: Fly, il
  fornitore Postgres, Cloudflare R2, credenziali OAuth Google, chiave API per embedding ed
  estrazione.
- `README` con i comandi per far girare l'app e per rigenerare l'ambiente locale.

## Verification

- Una pull request che rompe il typecheck fa fallire la pipeline; una che passa tutti e quattro i
  passi la fa diventare verde.
- Un clone pulito, seguendo solo il `README` e `.env.example`, avvia l'app in locale.
- Ogni segreto elencato in `.env.example` ha una controparte depositata in CI e nessun valore reale è
  committato nel repository.

## Learning target

Che lo stack scelto sulla carta — Next.js con Effect, Drizzle e i test — compila e gira insieme, e
che tutti i servizi a pagamento o a registrazione della mappa sono effettivamente ottenibili con gli
account che abbiamo.

## Excludes

- Qualunque provisioning e qualunque deploy: sono di S1, che è una riga separata perché una CI verde
  non dice niente su una macchina che non si accende.
- Schema di dominio, migrazioni e connessione a Postgres: sono di S1.
- Qualunque schermata: le prime sono in S3.

## Open questions

- Nessuna.
