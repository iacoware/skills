# Recipe App — Scelte di stack tecnico

Decisioni su linguaggio, framework e librerie. Per infrastruttura e servizi vedi
`arch-choices.md`.

## Linguaggio e framework — TypeScript + Next.js

- **TypeScript** end-to-end.
- **Next.js** come framework applicativo (App Router). Deploy come container Docker su
  Fly.io (vedi `arch-choices.md`) → runtime Node completo, nessun vincolo di adapter.

## Business logic — Effect

- **Effect** per la logica applicativa: gestione errori tipizzata, composizione via
  layer/servizi, integrazione con Next.js.
- Convenzioni di progetto (dai global instructions):
  - **Servizi**: `Context.Tag` per la porta (interfaccia pura), `Layer.effect` per
    l'adapter. Mai `Effect.Service`.
  - **Errori**: solo `Data.TaggedError`; gestione ai boundary con `catchTag`.
  - **HttpClient** di Effect per il fetch delle pagine ricetta; decode con
    `HttpClientResponse.schemaBodyJson` + `Schema`, mai cast.
  - **Schema** per validare (non castare) l'output dell'estrazione LLM e le risposte API.
  - `Effect.gen` per la logica sequenziale, `pipe` per decorazione (retry, timeout).

## Auth — Auth.js (NextAuth v5) + Google OAuth

- **Auth.js (NextAuth v5)**: standard de facto per Next.js, gratis, self-hosted su Postgres.
- Provider: **Google OAuth**. Niente password, niente invio email, niente flusso reset —
  Google gestisce identità e recupero account. (Dettaglio decisione in `goal.md`.)
- `family`/condivisione **non** sono gestiti da Auth.js: sono tabelle applicative
  (`Cookbook`, `Membership`, `Invitation` — vedi `concepts.md`). Auth.js copre solo
  identità e sessione.

## Data fetching client — TanStack React Query

- **@tanstack/react-query** per il data fetching dai client component.

## Persistenza / ORM — Drizzle

- **Drizzle** per l'accesso a Postgres: leggero, SQL-first, tipizzazione forte.
- Supporto **pgvector** di prima classe (tipo colonna `vector` + operatori di distanza),
  perfetto per la ricerca semantica.
- Connessione via driver standard (`postgres.js` / `node-postgres`) su TCP verso Neon —
  possibile perché su Fly gira Node completo (nessun driver serverless richiesto).
- Scartato Prisma: più pesante.

## Convenzioni UI (React)

Dai global instructions di progetto:

- Componenti piccoli (≤100 LOC); estrarre inner component / custom hook quando crescono.
- `const Component: React.FC<Props> = ({ ... }) => {}`; props come `type`, non `interface`.
- Handler con prefisso `on` (es. `onGoNext`).
- Stati multipli (≥3): discriminated union con `useState`/`useReducer`; state machine
  (xstate) se si complica (utile per il flusso di add con progress a step).
- Form: campi obbligatori non marcati con "*"; marcare gli **opzionali** come "optional".

## Decisioni di stack aperte

- Nessuna.
