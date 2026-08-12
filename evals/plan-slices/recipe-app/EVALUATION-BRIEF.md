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

# Material uncertainties

What this scenario does not know yet, and the decision each answer changes. A plan is free to place
these where it wants. `Subsystem` groups uncertainties that a single slice may validate together:
two rows of the same subsystem are one question asked twice, two subsystems are two questions.

| ID | Subsystem | Uncertainty | Decision it changes | Source |
|---|---|---|---|---|
| U1 | Delivery infrastructure | Does the chosen Postgres provider sustain a real TCP driver, pooling and migrations across scale-to-zero? | Neon or Supabase, and the driver and connection mode | `sources/arch-choices.md`, “Datastore”; `sources/tech-choices.md`, “Persistenza / ORM” |
| U2 | Delivery infrastructure | Is the first request after inactivity slow enough to bother a real user? | Keep `suspend` with scale-to-zero, move to an always-warm machine at ~$3/month, or — if the target itself fails — reconsider the hosting choice | `sources/arch-choices.md`, “Hosting” |
| U3 | Semantic engine | Is the multilingual embedder's cross-language recall good enough on real recipes, at the expected scale and cost? | Replace the model, change the indexed text, or abandon the differentiator and with it the product's reason to exist | `sources/goal.md`, “Differenziatore”; `sources/arch-choices.md`, “Embeddings” |
| U4 | Extraction | What is the JSON-LD hit rate on the blogs actually used? | How much weight and cost the LLM fallback carries, and whether it moves earlier or later | `sources/arch-choices.md`, “Estrazione contenuto” |
| U5 | Extraction | Is a cheap structured-output model accurate enough per recipe, at fractions of a cent? | Which model implements the fallback, or narrowing the cases that invoke it | `sources/arch-choices.md`, “Estrazione contenuto” |

# Known conflicts

- Manual input skips extraction in `sources/concepts.md`, “Pipeline di estrazione”, while `sources/arch-choices.md`, “Estrazione contenuto”, says manual input reuses the extraction engine and schema; implementation must defer to a resolved interpretation before asserting the manual path.
- Search queries are never embedded at runtime in `sources/goal.md`, “Vincoli e scala”, and `sources/arch-choices.md`, “Embeddings”, while `sources/concepts.md`, “Ricerca (MVP)”, defines search as `similarity(Recipe.embedding, embedding(query))`, which requires embedding the query. The sources admit three resolutions and select none: a per-query call, a cache, or precomputation.

# Not conflicts

Differences a reader may mistake for a conflict, resolved here so each cycle does not re-litigate them.

- Cost. `sources/goal.md`, “Scelte tecniche”, says everything fits “entro free tier … target ~$0/mese”; `sources/arch-choices.md`, “Hosting”, says Fly has no real free tier and costs cents per month. Both describe the same target: `arch-choices.md` holds the authoritative figures, `goal.md` states the intent.
