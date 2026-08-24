# Reference roadmap — the reasons it does not publish

`reference-roadmap/` is the map as it stands the moment it is first drawn against the MVP goal:
nothing delivered, `archive/` empty, ids starting at `S0`. It publishes decisions and not reasoning,
which is what lets it fit on one screen. Here are the reasons — only the ones a reviewer cannot
re-derive from the map and `sources/` together.

Read last, with the reference itself, when the verdict on the candidate is already formed. On every
difference, ask which of the two has the better reason; this file holds the reference's. **The
reference is frozen**: rewritten when the sources change, never because a candidate argued well.

**Language.** The map is in Italian, because the skill writes in the author's language and the sources
are Italian; the reasoning about the skill is in the project's. Field, column and state names are
English everywhere, being format rather than prose.

## The register

**Eight columns, and one test for each: is it used to compare rows and decide what comes first?**
`Id`, `Title`, `Theme` (breadth), `Kind` (routing, and the one shape check the format makes),
`Size` (routes what happens downstream), `Readiness`, `Executor` (separate from readiness because
four rows are `mixed`), `Depends on` (the constraint a reorder would not restore). `Outcome`,
`Learning target`, `Audience`, `Verification` and `Requested by` are read inside one row and never
across rows: all five live on the slice document.

`Outcome` is the one that had to be argued. An earlier draft put it in the register instead of the
title, and the table became fifteen sentences in a column, which stops the other columns being
scannable at all. The register names the row the way a person names it out loud.

- **`theme: —` is legal, and three rows use it.** `S0`, `S1` and `S14` serve every promise and can be
  cancelled with none, so pinning them to one theme would make *has every promise got a first
  validator* unanswerable.
- **Navigation is two links and no index.** Title → slice document, slice document → register. Ids stay
  plain text; there is no table of contents, because the register is the index and a second one would
  age out of step with it.
- **The two prerequisites are not published as `Depends on` edges.** Every row depends on the
  repository and the skeleton; fifteen edges saying the same thing would bury the ten that carry
  information.

## The shape

**Fifteen rows** because the problem fits at this granularity, not because fifteen is a target. The cap
binds granularity: had it not fitted, the finding would have been about the goal's width.

**`Ordering criteria` ranks what the skill leaves as siblings** — minimum delivery path, conventions,
existential risk, breadth. Breadth loses exactly once, and the exception is named inside the criterion
that concedes it.

**The differentiator goes first, on seeded data.** `S3` and `S4` land before any user can add a recipe
— manual entry is `S7`, import `S8`. `goal.md` calls cross-language semantic search *il vero elemento
distintivo* and says the project is otherwise largely a rewrite of tools that exist; the seed corpus
lets the one uncertain promise be validated before four themes lean on it, and costs one line of
`Includes` in `S3` and one of `Excludes` in `S14`.

## The calls a candidate is likely to make differently

| Row | The call | Why |
|---|---|---|
| `S0` / `S1` | Repository and skeleton kept apart | `S0` is where free-tier accounts and secrets are opened — human work with a different failure mode from a deploy that does not come up. `arch-choices.md` argues hosting at length, and none of it is settled by a green CI |
| `S2` | A spike, not a row | `text-embedding-3-small` is written as *es.* and multilingual behaviour is required without evidence. Its honest `Verification` is a measurement, `Audience` is empty, and if no cheap model works, `S3` and `S4` are different slices |
| `S3` / `S4` | Indexing split from search | An enabler may not validate a promise, which is why `S4` is `ricerca-semantica`'s first validator. The split lets the index exist against real data before there is a search box to argue about |
| `S7` | Manual entry **merged** with edit | One form, and one learning target: whether that form can serve both is exactly what makes saving an imperfect extraction acceptable. Split, the two rows verify on the same screen |
| `S9` | A slice, not a spike — the closest call on the map | It delivers a capability people use, and the JSON-LD miss rate is a by-product of delivery rather than of a throwaway script. It is also the one place breadth loses to learning |
| `S10` | Kept apart from `S9`, though both end in the same LLM call | Different learning targets — how often the structured path misses, versus whether a model extracts from unstructured text within budget — and different audiences |
| `S11` | Photos as one row | Upload and photo-from-import share the storage decision, which is the learning target. Cover choice and which photos to keep are excluded and left to be admitted later |
| `S12` | Sharing late | Everything before it runs on one implicit cookbook, recorded as an assumption; membership adds a boundary rather than changing what a recipe is. Early, it would buy a shared cookbook nobody can put a recipe in |

## The horizons, the assumptions, the questions

**The line between `LATER` and `OUT-OF-SCOPE` is *does the solution declare it will never solve this*,
never *how far away is it*.** Public cookbooks sit in `LATER` although `goal.md` files them under
future work, because `concepts.md` models `visibility`: nothing is declared unsolvable. No candidate
gets a document — a document invites specifying, and a candidate is vague on purpose.

**Every `OUT-OF-SCOPE` entry is written as the licence it gives**, not as a line saying what will not
be done: granular roles licenses the absence of a role model, structured ingredients licenses
free-text fields and the loss of shopping lists, and so on. Written as a graveyard they stop being
useful the moment somebody asks why a trade-off was allowed.

**Both conflicts are taken, and both are stated.** The reference resolves C2 — queries embedded at
runtime — by reading the constraint as being about cost, where `arch-choices.md` also puts it; and C1
— manual entry reusing the extraction engine — by having `S7` reuse the edit form and never the
extractor. A candidate resolving either the other way is fine; one resolving silently is worse than
one resolving wrongly and saying so.

**Three open questions sit at map altitude because each changes the map's shape.** The Postgres
provider is not among them: it blocks `S1` alone, so it lives on `S1` and shows as `needs-decision`.
Scope is the only thing that separates the two altitudes.

## Deliberately absent

Not defects, and a candidate carrying them is the thing to question: position numbering in ids;
`(Theme: …)` tags in titles; theme, kind, size, readiness or executor repeated inside a slice
document; `Learning / risk` as one field, risk being the learning target where it is material;
promotion triggers and decision checkpoints, which are what close-out does anyway; dates, estimates,
percentages and velocity.
