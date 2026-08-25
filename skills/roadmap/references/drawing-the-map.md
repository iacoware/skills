# Drawing the map

Loaded on the `Drawing` door, whether or not a map already stands. Everything here decides the shape
of the whole map — themes, prerequisites, order, the seam, and what the map reports about its own
input — and none of it fires on `Revising`.

The rules for a single row hold here too, and they are in [`slice-rules.md`](./slice-rules.md).

## What carries when a map already stands

A new goal declared against a map that already exists is drawn here. What the previous goal leaves
behind enters as input, exactly the way a source document does.

- **`.roadmap/archive/`.** The only durable record of what was delivered, because the tracker has no
  notion of *done*. Drawing without reading it is drawing as if the project had never started, and a
  promise the archive already kept is not a theme.
- **The id high-water mark**, which the archive and `slices/` carry in their filenames. The counter
  does not restart, so the first row of a redrawn map is rarely `S0`.
- **`OUT-OF-SCOPE` and `Cross-functional concerns`.** Both are constraints the shipped code already
  obeys, and forgetting a trade-off does not un-ship it. They carry. Where the new goal contradicts
  one, lift it explicitly and say what it costs: the exclusion was the licence for a trade-off that is
  already in production, and lifting it in the open is what makes the bill visible.
- **`LATER` survives as a file and not as a reading.** Every candidate is re-read one at a time
  against the new goal and gets a verdict — promoted, kept as speculation, or killed. Focus is
  relative to a goal, so a candidate nobody re-read is a candidate nobody chose.
- **Rows still open in `NOW`.** Each is re-justified against the new goal; the ones that still serve
  it keep their ids, the rest are retired.

Redrawn from nothing: the `Goal`, the themes, the register, the ordering criteria, `Assumptions` and
`Open questions`. No history of superseded goals is kept — `Current state` has room for the sentence
that matters, and git has the rest.

## Themes

A theme is a product promise that can be deferred or cancelled whole, stated in product language: what
somebody can do once it holds.

Run both tests explicitly, and record the verdict:

- **Split test.** Two capabilities are two themes when either can be cancelled, deferred or reordered
  without invalidating the other's evidence. A shared entity, form, pipeline or implementation is not
  a reason to merge independently schedulable value.
- **Merge test.** They are one theme when they share the same interaction, invariant and learning
  target, and neither produces useful feedback alone. Separate names or modes are not a reason to
  split one coherent promise.

**Theme compression** is the failure to watch for: merging independently schedulable value areas to
keep the theme count small. Do not optimise for fewer themes. A user-facing identity or access
capability is a theme; an authentication library or a database layer is not — those are rows.

**Every theme names one first validator**: the `NOW` row that validates the *complete* promise. A row
that validates one capability inside a broader promise is not it, and neither is a `kind: enabler`
row — an enabler may precede the validator and may never substitute for it. The one exception is a
theme whose promise is itself to a developer; then the enabler that validates it is the first
validator, and the `Promise` column says whose promise it is.

**`theme: —` is legal and carries information.** A row that serves every promise and can be cancelled
with none — the repository, the skeleton, the release into users' hands — attaches to no theme.
Pinning it to one would be a lie that makes *has every promise got a validator yet* unanswerable.

## The cap is a finding, not a budget

`NOW` is capped, and the cap binds granularity rather than count: a bigger problem does not buy more
rows, it buys fatter rows. When the map will not fit, that is the finding — either the goal is too
wide and wants an intermediate one declared, or the slicing is specifying work it cannot yet know.
Below the floor the roadmap does not repay its cost: that is an idea, and the existing chain handles
it without a map.

## Hard dependencies

Identify hard dependencies only. A predecessor is hard when no controlled input and no narrower real
precursor can make the dependent outcome realistically verifiable. Convenient reuse, a fuller demo or
a preferred order is not a hard dependency — that is order, and order is decided below.

Controlled inputs may stand in for unfinished UI or administration, and they must still traverse every
production path whose correctness materially affects the outcome. A fixture that injects derived data
directly does not remove the dependency on the production computation of that data.

`Depends on` publishes what a reorder would otherwise break with nobody noticing, and it holds ids and
nothing else — no grades, no counterfactuals. What every row depends on is not published: fifteen
edges that all say *after the skeleton* bury the four that carry information.

**What used to stay in reasoning is published now.** A one-shot delivery plan can keep its dependency
map, its horizon ledger and its row-to-source traceability out of the document, which works exactly
once — the session that writes the plan holds them. A living map cannot: the previous session's
reasoning no longer exists. So dependencies are a column and provenance is `Requested by` on the
row's document. What stays unpublished is the reasoning *behind* the order: `Ordering criteria`
states the rules once and the register's order carries the rest.

## The two prerequisites

Greenfield work draws two rows before any promise, and draws them separately:

1. **The repository prerequisite** — the repository with CI running build, lint, typecheck and tests,
   and the accounts and secrets the rest of the map spends. No provisioning, no deploy.
2. **The walking skeleton** — the smallest deployed path that proves the decided infrastructure is
   connected and running, through build, CI/CD, provisioning and a representative non-production
   environment.

They are two rows because a green CI settles nothing the hosting argument raises, and because opening
accounts is human work with a different failure mode from a deploy that does not come up.

The skeleton exercises every already-decided stateful or managed dependency that has no thinner real
validator later: at minimum the datastore, reached at runtime through the real driver and connection
mode by one non-domain operation, plus the migration runner applying one non-domain migration.
Connection mode, pooling, migration mechanics and their interaction with cold start cannot be
validated more cheaply anywhere else.

Keep it free of domain entities, domain CRUD, authentication and tenancy, and leave out any external
adapter only one later row uses — that row validates it.

Two failures have names:

- **Oversized skeleton** — deploy, sign-in, tenancy and the first CRUD in one row, when each validates
  independently.
- **Hollow skeleton** — a deployed runtime answering a static response without reaching the datastore
  or running a migration. Driver, connection and migration risk then arrive inside a domain row, where
  a failure could be either and says nothing about which decision to revisit.

## Ordering for learning

**The map declares its own ranking.** `Ordering criteria` is a numbered list because the ranking
between criteria is itself a decision this map takes, and the criteria below are what it ranks:

- the minimum delivery path — until something is delivered, nothing is learned;
- conventions born inside the first row that needs them, never in a workshop of their own;
- the differentiator and the existential business risk;
- irreversible, expensive or architecture-changing uncertainty;
- the real enablers those risks need in order to be tested;
- business frequency, and one thin outcome from each remaining theme;
- cohesive variants and deeper workflows, in risk order.

Where one criterion loses to another, the criterion that loses says so in itself, rather than leaving
the reader to notice a row out of place.

Four things are not up for ranking:

- **Breadth before depth.** Once the existential risks are validated, deliver one thin validating row
  from each remaining theme before a second row from one theme. Depart only for another
  differentiator, a material risk, required recovery, or a materially higher-frequency behaviour, and
  state the departure once in `Ordering criteria`.
- **Required recovery outranks breadth.** When a row names a failure mode in its `Verification` and
  another `NOW` row is its remedy, the remedy comes before a different theme opens. A remedy the
  sources declare a fallback of a delivered path closes that path; it is not optional depth. Where the
  sources define a recovery chain, the primary interaction gains its required automatic recovery
  before a separate manual escape is drawn.
- **A row that opens a pipeline or adapter shared by several paths follows every `NOW` row that feeds
  it**, and owns it alone.
- **The cheapest real input that can validate a risky engine is the right one.** A seed corpus that
  lets the one uncertain promise be measured before four themes lean on it costs a line of `Includes`
  and buys the whole order. Do not front-load commodity work for reuse alone.

**Where `NOW` ends.** When `NOW` targets selected end users, it ends with the smallest `kind: release`
row that makes the coherent release usable in its intended environment, carrying source-backed
operational readiness and nothing else. When `NOW` intentionally ends at developer validation, the map
states that audience and that environment instead.

## The identity seam

Ship the tenancy, ownership or scope boundary with the first row that persists data, and let one named
resolver own the current scope. A later row then replaces a configured scope with an authenticated one
at that single seam. State the seam under `Cross-functional concerns`, and record in `Assumptions`
what the rows before it are allowed to ignore — the implicit single owner they run on, and that they
will not have to be rewritten when the real one arrives.

Never defer the boundary itself, and never defer identity when no such seam exists.

Once the evidence that justified deferring identity exists, identity comes before further user-facing
rows whose acceptance depends on real ownership or membership. Past the second `NOW` row that delivers
behaviour to an end user, justify the remaining deferral once in `Ordering criteria`, naming the
evidence that still requires it. Every row preceding identity names its own audience: an `Outcome`
promising *a user* who cannot exist yet belongs to a developer or to a tester on the declared
non-public environment.

## What the map reports about its input

Drawing forces the map to resolve things the sources left open. `Assumptions` and `Open questions` say
which ones, so the author gets a second reading of the vision's completeness. Neither is a work queue,
neither mints anything, and every line is traced to the themes and the ids it touches, or to `goal`
where what it touches is the whole map and no theme or row owns it.

Sweep the sources for two categories before the map is drawn, and give each entry a reference on both
sides:

- **conflicts** — pairs of incompatible statements, whether or not either names a provider, model,
  service or adapter. Sweep per behaviour the map will cut, not per component named;
- **undecided choices** — a provider, model, service or adapter named without a source that selects
  it. A qualifying adjective — *cheap*, *multilingual*, *managed* — is not a choice.

Every entry then leaves by one of three exits, and no other:

- **An `Assumptions` line.** The map takes a reading in order to be drawable, and says which reading
  and why. This is what an assumption is: taken as true *in order to* draw the map, asking to be
  corrected, and usually dying at close-out when delivery confirms or refutes it. `Assumptions` comes
  before `Open questions` because an assumption taken silently does more damage than a question left
  visibly open, and a map that resolves a contradiction silently is worse than one that resolves it
  wrongly and says so.
- **An `Open questions` line.** The entry could not be settled and asks to be answered. It belongs at
  map altitude when the answer changes the *shape* of the map — whether a row exists at all, whether a
  theme is drawn as drawn. Scope is the only thing that routes it; what blocks one row alone lives on
  that row.
- **A spike**, before the first row the entry blocks.

Exposing is not resolving. Only a source that selects resolves an entry: a published question and a
scheduled spike both leave it open, because neither has produced its answer when the map is drawn.

`OUT-OF-SCOPE` holds what the solution declares it will never solve, never what is merely far off, and
each exclusion is written as the licence it gives: *because this stays unsolved, the implementation
may do without X, and this is the price it pays*. Written as *we will not do X* the section reads as a
graveyard; written as a licence it still answers the question somebody asks a year later, which is why
the trade-off was allowed.

## The map holds when

- every theme has a promise in product language and one first validator that is an existing `NOW` row,
  and no enabler validates a theme whose promise is not to a developer;
- every theme boundary has a recorded split or merge verdict, and no two value areas were merged to
  keep the count down;
- greenfield draws the repository row and the skeleton separately, and the skeleton reaches the
  datastore through the real driver and runs a migration;
- every published `Depends on` names a predecessor no controlled input can stand in for;
- `Ordering criteria` is ranked, and every departure from breadth is named in the criterion that
  concedes it;
- the scope boundary ships with the first row that persists data, and any identity deferred past the
  second end-user row is justified in `Ordering criteria` against named evidence;
- every conflict and every undecided choice left the sweep by one of the three exits;
- every line of `Assumptions` and `Open questions` traces to a theme, an id or `goal`;
- `NOW` fits under the cap without inventing detail the map cannot yet know.
