# Reference roadmap — why each row is a row, and why it sits where it sits

`reference-roadmap/` is the map as it stands the moment it is first drawn against the MVP goal:
nothing delivered, `archive/` empty, ids starting at `S0`. It publishes the decisions and not the
reasoning behind them — the register's order and `Ordering criteria` carry that silently, which is
the whole point of a map that fits on one screen. This document is the other half: what the published
roadmap deliberately does not carry.

It is written for a reviewer comparing a generated roadmap against the reference and asking, on every
difference, which of the two has the better reason. A reason you have to re-derive from `sources/` is
a reason you will not weigh.

**Language.** The map is in Italian and this document is in English, mirroring
`../../plan-slices/recipe-app/`: the skill writes in the author's language and the sources are
Italian, while the reasoning about the skill belongs to the project's language. Field names, column
names and state values stay English everywhere, because they are format and not prose.

## The register's columns

Each column had to survive one question: is it used to *compare rows and decide what comes first*? A
field used only while reasoning inside one row belongs to that row's document.

| Column | Why it compares rows |
|---|---|
| `Id` | Identity. It is what `Depends on` points at and what survives promotion and reordering. |
| `Titolo` | The row's name, and the link into its document. It is what the eye reads down fifteen rows, which is why it sits second and not last. |
| `Theme` | Breadth. You cannot ask *has every promise got a first validator yet* without reading themes across rows. |
| `Kind` | Routing, and the one check the format makes on the map's shape: an enabler may not be a theme's first validator. |
| `Size` | Routes what happens downstream — `large` goes through `to-tickets`, the rest goes straight to `to-spec`. |
| `Readiness` | What can be picked up today, as opposed to what is on the path. |
| `Executor` | Who can do it. Separate from readiness because `S0`, `S1`, `S6` and `S14` are all mixed. |
| `Depends on` | The constraint that order alone would not restore after a reorder. |

Eight columns, no ninth. Five fields were considered and rejected, each because it is read inside one
row and never across rows: `Outcome`, `Learning target`, `Audience`, `Verification`, `Requested by`.
All five are on the slice document.

`Outcome` is the one that had to be argued rather than assumed. An earlier draft of this map put the
one-line outcome in the register instead of the title, and the table it produced was fifteen
sentences in a column: the six columns beside them stopped being scannable, which is the whole
function they exist for. The outcome is not dropped — it opens the slice document, where a sentence
is the right shape for the medium — and the register names the row the way a person names it out
loud.

Two conventions the columns needed and the sources did not settle:

- **`theme: —` is legal, and three rows use it.** A theme is a product promise that can be deferred
  or cancelled whole. `S0`, `S1` and `S14` serve every promise and can be cancelled with none of
  them, so attaching them to one theme would be a lie that makes the breadth question unanswerable.
- **Navigation is two links and no index.** The title in the register links to the slice document,
  the slice document opens with a link back to the register. Nothing else links: ids stay plain text
  in the `Id` column and in `Depends on`, because the same identity rendered as a link twice in one
  row is noise and the filename carries it anyway. There is no table of contents and no index file —
  the register is the index, and a second one would age out of step with it.
- **The two prerequisites are not published as `Depends on` edges.** Every row depends on the
  repository and on the skeleton; publishing fifteen edges that all say the same thing would bury the
  four that carry information. What is published is what a reorder could break without anyone
  noticing: `S3 → S2`, `S4 → S3`, `S5 → S3`, `S7 → S6`, `S9 → S8`, `S10 → S9`, `S11 → S8`,
  `S12 → S6`, `S13 → S9`, `S14 → S12`.

## The shape of the map

**Fifteen rows.** The cap runs from three or four to twenty, with fifteen the number to aim at, and
the cap binds granularity rather than count: this problem fits at this granularity without either
fattening rows or splitting them, so nothing was forced. Had it not fitted, the finding would have
been about the goal's width, not about the list's length.

**Order of the criteria.** `Ordering criteria` puts the minimum delivery path first, then conventions,
then existential risk, then breadth. The skill's rule set names *breadth before depth* and *ordering
for learning* as siblings without ranking them, and a map that declares its own criteria is where the
ranking belongs. Here breadth loses exactly once, and the exception is named in the criterion itself
rather than left for the reader to notice.

**The differentiator goes first, on seeded data.** `S3` and `S4` land before there is any way for a
user to add a recipe — manual entry is `S7`, import is `S8`. That looks backwards and is deliberate:
`goal.md` calls cross-language semantic search *il vero elemento distintivo* and says that without it
the project is largely a rewrite of an existing tool. Everything else on this map exists in three
mature free alternatives. The seed corpus is the scaffolding that lets the one uncertain promise be
validated before four themes are built on top of it, and it costs one line of `Includes` in `S3` and
one line of `Excludes` in `S14`.

## Row by row

**`S0` — Repository, CI and secrets.** The repository prerequisite, kept as its own row and not
folded into the skeleton because it is where the free-tier accounts and their secrets are opened, and
that is human work with a different failure mode from a deploy that does not come up. `enabler`,
because it validates no product promise. `mixed`: a person opens accounts, an agent writes the
workflow.

**`S1` — Walking skeleton in production.** The thinnest path through every layer, deployed. Separate
from `S0` by rule and by evidence: `arch-choices.md` argues hosting at length — scale-to-zero,
`suspend` versus `stop`, containers over workers — and none of that argument is settled by a green
CI. `release`, because what it delivers is a deployment and not a capability. Its `needs-decision` is
the Postgres provider, which the sources leave as *Neon o Supabase* and nobody has picked.

**`S2` — Spike: which embedding holds up across languages.** The one row where the map admits it does
not know. `arch-choices.md` names `text-embedding-3-small` as *es.* — an example, not a decision —
and states multilingual behaviour as a requirement without evidence. If no cheap cloud model finds an
English recipe from an Italian query, `S3` and `S4` are different slices and hybrid search comes back
from `LATER`; specifying either shape now is specifying work the map cannot know. The tell is the
honest `Verification`: it reads *we can say, for each candidate model, how many of the expected
recipes come back* — a measurement, not something a user can do. `Audience` is empty for the same
reason, and who consumes the answer is named by the dependency rather than by a field. Its
`needs-info` is real: the corpus that makes the measurement worth anything is a handful of recipes and
queries the pilot users hold.

It competes for a row under the cap like everything else, and it earns it: the alternative is building
the pipeline on a guess and discovering the guess at `S4`, with two themes already leaning on it.

**`S3` — Semantic indexing.** An `enabler`, and the reason the theme table names `S4` as
`ricerca-semantica`'s first validator: an enabler may not validate a promise. It stays separate from
`S4` because it carries the seed corpus, the `vector` column and the HNSW index — the things the spike
measured on a throwaway script and that now have to survive an edit — and because splitting them lets
the index exist against real data before there is a search box to argue about.

**`S4` — Cross-language semantic search.** The theme's first validator and the row the whole map is
ordered around. Its verification is stated as two searches a person can perform, which is what keeps
it a slice and not a second spike.

**`S5` — Listing and reading a recipe.** `consultazione`'s first validator, and the first row that
answers *what is this app* to somebody who is not building it. It depends on `S3` because without the
seed there is nothing to list. Its learning target is the one thing the minimal model could get wrong:
whether free-text ingredients and steps are enough to actually cook from, given that the exclusion of
structured ingredients is permanent.

**`S6` — Google sign-in.** `autenticazione`'s first validator, placed here and not first because
nothing before it owns data. `mixed`: the OAuth client and the consent screen are console work. The
decision itself is not open — `goal.md` takes it and records what it discarded — so the row is
`ready`.

**`S7` — Writing and correcting by hand.** `inserimento-manuale`'s first validator, and the first way
a user creates a recipe. It **merges** manual entry with edit, which the sources present as two
things: they share one form, and the merge test holds because they share the learning target too —
whether one form can serve both is exactly what makes it acceptable to save an imperfect extraction
without a review step. Splitting them would leave two rows whose verification is the same screen.

**`S8` — Import from a URL with JSON-LD.** `import-automatico`'s first validator and the most used
path in the product. `large`, because it is the first row with a pipeline: fetch, parse, save, and the
progress bar over real steps with a precise message on failure. The progress bar is included rather
than deferred because `goal.md` treats the honest failure message as part of what the import is, and
a fake progress bar is not a smaller version of a real one.

**`S9` — LLM fallback for pages without structured data.** The one place breadth loses to learning:
it takes the row that would otherwise have gone to `foto` or `condivisione`. Its learning target is a
measurement obtained by delivering — how often JSON-LD actually covers the sites these users paste —
and the answer resizes and reshapes the rows after it. Shipping URL import to real users while
knowing nothing about the miss rate is the version of this map that discovers its main path by
accident.

It is a slice and not a spike, and the distinction is worth stating because it is the closest call
here: it delivers a capability people use, and the measurement is a by-product of delivery rather
than the product of a throwaway script.

**`S10` — Pasting a page's text.** Kept apart from `S9` although both end in the same LLM call. The
split test is the learning target: `S9` asks how often the structured path misses, `S10` asks whether
a model extracts a recipe from unstructured text within budget. They also serve different audiences —
a page that will not download is a different problem from a page with no metadata. `small`, on the
assumption that it is the last fallback and rarely used, which is exactly the kind of assumption
`S9`'s delivery is going to test.

**`S11` — Recipe photos.** `foto`'s first validator. One row and not two: photo upload and
photo-from-import share the storage decision, which is the learning target — URL in the database,
bytes on object storage, no volume, so the machine can still go to sleep. Cover choice and *which*
photos to keep from an import are excluded here and left to be admitted later if anybody asks; both
are refinements of delivered work, and a map that pre-empts them is specifying what it cannot know.

**`S12` — Cookbook shared by invitation.** `condivisione`'s first validator, and `large` because it
introduces three entities and retrofits scoping onto everything already delivered. Late on purpose:
the assumption that everything before it runs on one implicit cookbook is recorded, and it holds
because membership adds a boundary rather than changing what a recipe is. Putting it early would have
bought a shared cookbook nobody could yet put a recipe in.

**`S13` — Derived tags and time.** An `enabler` on `ricerca-semantica`, deliberately after the import
rows because deriving tags is nearly free once the LLM path exists and merely parsing when JSON-LD is
there. It is the smallest row on the map and it survives as a row because `goal.md` gives it a reason
that is not a filter: tags carry signal the recipe text does not contain. Its learning target is
therefore falsifiable — the fields could add noise instead — which is what keeps it from being
scope filling.

**`S14` — Handing it to the first users.** A `release`, and the row where the goal is reached: family
and friends actually using it. It exists because the human work in it is real and undelegable — domain,
consent-screen review, a restore somebody has actually tried — and because `NOW` emptying toward the
goal is the only progress reporting this tool does. Its learning target doubles as the evidence that
decides the always-warm-machine candidate.

## Horizons

**`LATER` holds six candidates and no ids.** Five come from `goal.md`'s own list of future work, one
— the always-warm machine — from the cost argument in `arch-choices.md`, which presents it as a
reversible flag. None gets a document: a document invites specifying, and a candidate is vague on
purpose.

**`OUT-OF-SCOPE` holds four exclusions, and each is written as a licence.** That is what the section
is for: granular roles licenses the absence of a role model, structured ingredients licenses free-text
fields and the loss of shopping lists, deduplication licenses the absence of natural keys, and
delegated identity licenses having no mail infrastructure at all. Written as *we will not do X* they
would read as a graveyard; written as *and therefore the code may do Y* they stay useful when
somebody later asks why the trade-off was allowed.

The line between the two horizons is *does the solution declare it will never solve this*, not *how
far away is it*. Public cookbooks sit in `LATER` and not in `OUT-OF-SCOPE` although `goal.md` files
them under future work, because `concepts.md` models `visibility` for them: nothing is being declared
unsolvable.

## `Assumptions` and `Open questions`

Both are traced to a theme or an id, and both report on the input rather than queueing work.

The first assumption is the one that matters: the sources contradict each other. `goal.md` and
`arch-choices.md` say embeddings are used *mai a runtime sulle query di ricerca*, while
`concepts.md` writes the search as `similarity(Recipe.embedding, embedding(query))`, which embeds the
query at runtime by construction. The map takes the constraint as being about cost — where
`arch-choices.md` also puts it, calling query cost irrelevant — and says so, because an assumption
taken silently does more damage than a question left visibly open. A generated roadmap that resolves
this the other way and drops semantic search is wrong; one that resolves it silently is worse than one
that resolves it wrongly and says so.

The three open questions are at map altitude because each changes the *shape* of the map: whether `S3`
and `S4` exist as drawn, whether a row is needed for recovering from a failed import, whether moving
recipes between cookbooks is a row or an exclusion. The provider question is not among them — it
blocks `S1` alone, so it lives on `S1` and shows in the register as `needs-decision`. Scope is the
only thing that separates the two altitudes, and it is the only thing that should.

## `plan-slices` habits dropped on purpose

- **Position numbering.** Ids are minted in draw order here because it is the first draw, and they
  stop meaning position the moment anything is reordered. Delivery order is carried by the register's
  order alone.
- **Title tags.** No `(Theme: …)`, `(Enabler: …)`, `(Release: delivery)` in any title. Theme and kind
  are columns, which is also what makes *an enabler may not be a theme's first validator* checkable.
- **Metadata repeated inside the slice document.** A slice document carries no theme, kind, size,
  readiness or executor. It carries a link back to the register, four references and seven fields,
  and nothing that is already a column.
- **`Learning / risk` as one field.** Risk is not a field: where it is material it is the learning
  target, and every row has exactly one.
- **A global `Open questions` catch-all.** The name is reused at slice altitude on purpose, and what
  an entry blocks is the only thing that routes it.
- **Promotion triggers and decision checkpoints.** Nowhere on this map, in any spelling. What they
  recorded — *when this evidence arrives, change this decision* — is what a human re-reading a living
  map already sees, and what close-out does anyway.
- **Dates, estimates, percentages, velocity.** Nowhere. `S9`'s learning target is a measurement to be
  taken, not a number predicted here.

## One thing this phase changed outside its own output

`../../../design/roadmap/WORKFLOWS.md` recapped the `recipe-app` starting states with concrete ids,
and its recap of the archived state listed eight rows before the LLM fallback. This map has nine,
because `S2` is a spike the recap did not anticipate. The examples were shifted by one id rather than
the spike being dropped: the spike is the honest reading of `arch-choices.md`, and `WORKFLOWS.md`
illustrates rather than rules. Everything else in the three examples — which row keeps its id on a
split, which candidate is promoted at the redraw, why the counter does not restart — is unchanged.
