# Evaluation brief — recipe-app

Facts about `sources/`, answered once so that no review re-litigates them. One stable id per entry —
`A` accepted alternative, `C` conflict, `U` uncertainty, `N` non-defect, `H` hard constraint — never
reused, a new entry taking the next free number in its letter. **Cite the id, never a paraphrase.**
Themes, row ids, register order, the cap and where a spike goes are the skill's business, checked by
the rules and the validator, not here.

## Tick off (hard constraints)

A candidate that misses one of these has a defect, wherever it places it. Tick the row, or record the
miss with its id.

| ID | The map contains | Source |
|---|---|---|
| H1 | `NOW` validates multilingual semantic search; it is the differentiator, and no map reaches the goal without it | `sources/goal.md`, “Differenziatore” and “Ricerca” |
| H2 | Every recipe read, write and semantic query is scoped to the current cookbook; members can edit all cookbook content | `sources/goal.md`, “Condivisione”; `sources/concepts.md`, “Cookbook” and “Membership” |
| H3 | URL extraction tries JSON-LD before a validated LLM fallback; pasted text uses the extraction schema; manual input uses the shared edit form | `sources/goal.md`, “Aggiunta ricetta”; `sources/concepts.md`, “Pipeline di estrazione” |
| H4 | Add saves without mandatory review; edit is the recovery path and regenerates derived embeddings | `sources/goal.md`, “Aggiunta ricetta”; `sources/concepts.md`, “Recipe” |
| H5 | The stack is Google OAuth, Postgres with pgvector, R2, multilingual cloud embeddings, Next.js on Fly.io, Effect, React Query and Drizzle | `sources/goal.md`, “Auth”; `sources/arch-choices.md`; `sources/tech-choices.md` |
| H6 | Public cookbooks, structured filters, cross-cookbook search, groups and granular roles are off the MVP path — candidates or exclusions, never `NOW` rows | `sources/goal.md`, “Fuori scope MVP” |
| H7 | The deployed skeleton reaches Postgres through the real driver and connection mode: scale-to-zero, pooling and migrations are argued at length and none of it is settled by a green CI | `sources/arch-choices.md`, “Datastore” and “Hosting”; `sources/tech-choices.md`, “Persistenza / ORM” |
| H8 | `NOW` ends where the goal is reached — family and friends actually using it — or states instead that it ends at developer validation, and names that audience and environment | `sources/goal.md`, “Visione” and “Condivisione” |

## Verify the exit (conflicts and uncertainties)

**Taking a side is allowed; taking it silently is the defect.** The exits out of the sweep, and what
counts as taking one, are R-015's business ([`../EVALUATION-RULES.md`](../EVALUATION-RULES.md)).
Which side and which exit are free choices, judged on their stated reason; the `Licences` column of
the uncertainty table points at the entries that say how free.

Two conflicts, each with both sides citable:

- **C1** — Manual input skips extraction in `sources/concepts.md`, “Pipeline di estrazione”, while `sources/arch-choices.md`, “Estrazione contenuto”, says manual input reuses the extraction engine and schema. Either reading may be taken; neither may be assumed.
- **C2** — Search queries are never embedded at runtime in `sources/goal.md`, “Vincoli e scala”, and `sources/arch-choices.md`, “Embeddings”, while `sources/concepts.md`, “Ricerca (MVP)”, defines search as `similarity(Recipe.embedding, embedding(query))`, which requires embedding the query. The same section of `sources/arch-choices.md` also contradicts itself four lines above the ban: “le query sono irrilevanti” prices query tokens as negligible, which presupposes that queries are embedded at all. The ban is a cost constraint wearing the grammar of an architectural one, and the nearest evidence for that sits inside a single file rather than across two. The sources admit three resolutions and select none: a per-query call, a cache, or precomputation. Resolving it by dropping semantic search contradicts H1, and is the one resolution that is not open. A resolution restating the ban as architectural is falsified by that line, not merely unresolved.

Five uncertainties, which a map may place where it likes. `Subsystem` exists for R-016: two rows of
the same subsystem are one question asked twice, two subsystems are two questions and no single
enabler may answer both.

| ID | Subsystem | Uncertainty | Decision it changes | Licences | Source |
|---|---|---|---|---|---|
| U1 | Delivery infrastructure | Does the chosen Postgres provider sustain a real TCP driver, pooling and migrations across scale-to-zero? | Neon or Supabase, and the driver and connection mode | A1 | `sources/arch-choices.md`, “Datastore”; `sources/tech-choices.md`, “Persistenza / ORM” |
| U2 | Delivery infrastructure | Is the first request after inactivity slow enough to bother a real user? | Keep `suspend` with scale-to-zero, move to an always-warm machine at ~$3/month, or — if the target itself fails — reconsider the hosting choice | A4 | `sources/arch-choices.md`, “Hosting” |
| U3 | Semantic engine | Is the multilingual embedder's cross-language recall good enough on real recipes, at the expected scale and cost? | Replace the model, change the indexed text, or abandon the differentiator and with it the product's reason to exist | A2 A8 | `sources/goal.md`, “Differenziatore”; `sources/arch-choices.md`, “Embeddings” |
| U4 | Extraction | What is the JSON-LD hit rate on the blogs actually used? | How much weight and cost the LLM fallback carries, and whether it moves earlier or later | A9 | `sources/arch-choices.md`, “Estrazione contenuto” |
| U5 | Extraction | Is a cheap structured-output model accurate enough per recipe, at fractions of a cent? | Which model implements the fallback, or narrowing the cases that invoke it | A3 | `sources/arch-choices.md`, “Estrazione contenuto” |

## Never flag (licences)

**No finding stands against an entry of this section.** The map cannot fail these; only the review
can, by flagging what they license. A candidate that chooses otherwise than an `A` entry is not
wrong — judge it on its stated reason. An `N` entry names what only looks like a defect.

- **A1** — Neon or Supabase may provide Postgres, because the source leaves that provider undecided (`sources/arch-choices.md`, “Datastore”). It blocks the skeleton alone, so it belongs on that row as `needs-decision` rather than at map altitude.
- **A2** — A cheap multilingual cloud embedding model may replace the named example if it preserves cross-language behaviour and the cost constraint (`sources/arch-choices.md`, “Embeddings”): `text-embedding-3-small` is written as *es.*, an example and not a decision.
- **A3** — A cheap structured-output LLM may implement the extraction fallback; the source specifies a class, not a provider (`sources/arch-choices.md`, “Estrazione contenuto”).
- **A4** — Fly.io may start suspended or always warm; the former is preferred and the latter is an evidence-triggered operational change (`sources/arch-choices.md`, “Hosting”).
- **A5** — Controlled inputs may validate extraction, embeddings or search before their final user entry point when they traverse the production computation (`sources/goal.md`, “Principi guida”; `sources/concepts.md`, “Pipeline di estrazione”). A seed corpus that lets semantic search be measured before anybody can add a recipe is this entry, not fake verticality.
- **A6** — A changeable cover may sit in `NOW` inside the photo row, or in `LATER` as a candidate. The source declares it without making it MVP-mandatory (`sources/goal.md:74`).
- **A7** — Choosing which photos to keep during import may be deferred, or kept in `NOW` only as an optional step: a mandatory one would contradict “nessun passo di review nel flusso di add” (`sources/concepts.md:143`).
- **A8** — The cross-language embedding uncertainty (U3) may leave by any of the three exits: a spike before the rows it blocks, an `Open questions` line at map altitude, or an `Assumptions` line naming the reading taken. Which exit was taken is a choice to judge on its stated reason, not a defect. Naming a model as decided is not one of the exits.
- **A9** — The same holds for the JSON-LD hit rate (U4): it may be measured by a spike, or by delivering the structured path and reading the miss rate at close-out, which makes the fallback an ordinary row with a measurable learning target.
- **A10** — Manual entry and edit may be one row or two. They share one form (`sources/goal.md`, “Aggiunta ricetta”; `sources/concepts.md`, “Pipeline di estrazione”), which is a merge argument and not a merge obligation; what is owed is a recorded verdict, either way — in `log.md` when the two are themes, in the row's document when they are rows.
- **A11** — A capability the sources describe may be delivered before or after identity, provided the rows before it name their own audience. Nothing in `sources/` fixes where Google sign-in lands.
- **N1 — Cost.** `sources/goal.md`, “Scelte tecniche”, says everything fits “entro free tier … target ~$0/mese”; `sources/arch-choices.md`, “Hosting”, says Fly has no real free tier and costs cents per month. Both describe the same target: `sources/arch-choices.md` holds the authoritative figures, `sources/goal.md` states the intent.
- **N2 — Public cookbooks in `LATER`.** `sources/goal.md`, “Fuori scope MVP”, files them under future work, but `sources/concepts.md`, “Cookbook”, models `visibility` for them: nothing is declared unsolvable, so the candidate horizon is admissible. `OUT-OF-SCOPE` is admissible too when the entry is written as the licence it gives. The defect is only a bare *we will not do this*, and the same holds for every other entry of that list.
- **N3 — The differentiator delivered on seeded data.** Semantic indexing and search landing before any way for a user to add a recipe looks backwards and is A5 plus the ranking the map declares: `sources/goal.md`, “Differenziatore”, calls cross-language search “il vero elemento distintivo” and says the project is otherwise largely a rewrite of tools that exist.
- **N4 — A spike whose id is higher than the row waiting on it.** Ids are identity and the register's order is delivery order; a spike minted late and delivered first is ordinary.
- **N5 — `theme: —`.** The repository row, the skeleton and the release into users' hands attach to no theme, and pinning them to one would make *has every promise got a validator yet* unanswerable.
- **N6 — A row count well away from the reference's fifteen.** The cap binds granularity rather than count, and anything between the floor and the cap is a shape decision, not a finding. What is a finding is the map not fitting at all.
