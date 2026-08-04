# Authority

- Product scope and priority come from `sources/goal.md` sections “Visione”, “Differenziatore”, “Cosa fa (MVP)” and “Fuori scope MVP”.
- Domain invariants come from `sources/concepts.md` sections “Modello di condivisione: cookbook-centrico”, “Entità principali”, “Pipeline di estrazione” and “Ricerca (MVP)”.
- Infrastructure decisions come from `sources/arch-choices.md` sections “Datastore”, “Object storage foto”, “Embeddings”, “Estrazione contenuto” and “Hosting”.
- Stack decisions come from `sources/tech-choices.md` sections “Linguaggio e framework”, “Business logic”, “Auth”, “Data fetching client” and “Persistenza / ORM”.

# Hard constraints

- NOW must validate multilingual semantic search; it is the differentiator (`sources/goal.md`, “Differenziatore” and “Ricerca”).
- Every recipe read, write, and semantic query is scoped to the current cookbook; members can edit all cookbook content (`sources/goal.md`, “Condivisione”; `sources/concepts.md`, “Cookbook” and “Membership”).
- URL extraction tries JSON-LD before a validated LLM fallback; pasted text uses the extraction schema; manual input uses the shared edit form (`sources/goal.md`, “Aggiunta ricetta”; `sources/concepts.md`, “Pipeline di estrazione”).
- Add saves without mandatory review; edit is the recovery path and regenerates derived embeddings (`sources/goal.md`, “Aggiunta ricetta”; `sources/concepts.md`, “Recipe”).
- MVP uses Google OAuth, Postgres with pgvector, R2, multilingual cloud embeddings, Next.js on Fly.io, Effect, React Query, and Drizzle (`sources/goal.md`, “Auth”; `sources/arch-choices.md`; `sources/tech-choices.md`).
- Public cookbooks, structured filters, cross-cookbook search, groups, and granular roles are excluded from MVP (`sources/goal.md`, “Fuori scope MVP”).

# Accepted alternatives

- Neon or Supabase may provide Postgres because the source leaves that provider undecided (`sources/arch-choices.md`, “Datastore”).
- A cheap multilingual cloud embedding model may replace the named example if it preserves cross-language behavior and the cost constraint (`sources/arch-choices.md`, “Embeddings”).
- A cheap structured-output LLM may implement extraction fallback; the source specifies a class, not a provider (`sources/arch-choices.md`, “Estrazione contenuto”).
- Fly.io may start suspended or always warm; the former is preferred and the latter is an evidence-triggered operational change (`sources/arch-choices.md`, “Hosting”).
- Controlled inputs may validate extraction, embeddings, or search before their final user entry point when they traverse the production computation (`sources/goal.md`, “Principi guida”; `sources/concepts.md`, “Pipeline di estrazione”).

# Known conflicts

- Manual input skips extraction in `sources/concepts.md`, “Pipeline di estrazione”, while `sources/arch-choices.md`, “Estrazione contenuto”, says manual input reuses the extraction engine and schema; implementation must defer to a resolved interpretation before asserting the manual path.
