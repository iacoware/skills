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
- **`.roadmap/log.md` does not carry.** The themes are drawn from nothing, and a verdict on a theme
  that no longer exists is dead weight re-read on every later operation; the sources are swept again
  against the new goal, and the entries of the old sweep go with the verdicts. The redraw starts the
  log again with its own H2 alone.

Redrawn from nothing: the `Goal`, the themes, the register, `Assumptions` and `Open questions`. No
history of superseded goals is kept — `Current state` has room for the sentence that matters, and git
has the rest.

## Themes

A theme is a product promise that can be deferred or cancelled whole, stated in product language: what
somebody can do once it holds.

Run both tests explicitly on every boundary between adjacent themes:

- **Split test.** Two capabilities are two themes when either can be cancelled, deferred or reordered
  without invalidating the other's evidence. A shared entity, form, pipeline or implementation is not
  a reason to merge independently schedulable value.
- **Merge test.** They are one theme when they share the same interaction, invariant and learning
  target, and neither produces useful feedback alone. Separate names or modes are not a reason to
  split one coherent promise.

The split test decides. Where it holds, the merge test is not asked: a promise that can be deferred
alone is a theme however little it is worth on its own. The merge test applies only to a boundary the
split test leaves standing.

**Record each verdict in `.roadmap/log.md` before the `Themes` table is written**, one bullet per
boundary: the pair in table order, `split` or `merge`, and the one fact that decided it. An
`Argument:` line of at most two may follow the fact — the log has room for it, the map does not. The
order is the point: a verdict written after the table is the table's rationalisation, and the table
then carries whatever compression the verdict would have caught.

The log is the model's memory, not the author's document. `roadmap.md` never repeats a verdict — two
copies of one decision are guaranteed drift — and where the two disagree the map wins. It is
append-only: one H2 per session, dated and named after the door, bullets beneath. A session writes
under its own H2 and leaves the earlier ones as they stand; a pair decided twice is decided by the
lower bullet.

```markdown
## 2026-09-03 — Drawing

- `capture` / `search` — **split.** Search defers whole without invalidating the capture evidence.
  Argument: [optional, two lines at most].
```

**Theme compression** is the failure to watch for: merging independently schedulable value areas to
keep the theme count small. Do not optimise for fewer themes. A user-facing identity or access
capability is a theme; an authentication library or a database layer is not — those are rows.

**Every theme names one first validator**: the `NOW` row that validates the *complete* promise. A row
that validates one capability inside a broader promise is not it, and neither is a `kind: enabler`
row — an enabler may precede the validator and may never substitute for it. The one exception is a
theme whose promise is itself to a developer; then the enabler that validates it is the first
validator, and the `Promise` column says whose promise it is.

**A promise names only what its first validator delivers.** Where that row excludes a capability the
promise names, the promise is holding two: either the validator is the wrong row, or the capability
is a theme the table compressed.

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

Before publishing an edge, name the stand-in: an input the row can control, or a narrower real
precursor already in `NOW`. Naming one settles it — there is no edge, and the sequence is order, not
dependency. The default cell is `—`.

The stand-in has to be nameable, not merely conceivable. Where the dependent's `Includes` builds on a
table, a migration, a resolver or an adapter that another `NOW` row delivers, no fixture supplies it
without bypassing the production path: the edge is hard and stays published — **except where the
deliverer is one of the two prerequisites.** The repository row and the skeleton are what every row
depends on; their edges carry no information and are never published, however hard they are.

Read the dependent's `Verification` as well as its `Includes`, and ask of it the same question:
could this row be built before that capability exists? Where the evidence that a row is done is
*made of* capabilities other `NOW` rows deliver — a `kind: release` row has no proof of its own —
nothing controlled stands in, and putting those capabilities there by hand is the fixture that
bypasses the production path, so the row does not carry `—`. What it publishes is the row its
evidence enters through, not one edge per capability the evidence touches: otherwise a release row
restates half the map and buries the edges that carry information.

Where a row's proof stands on its own and one clause reaches downstream to observe that what the row
produces arrives somewhere else, that clause is order, not dependency. A reorder moves it or drops
it and breaks nothing else, and publishing the edge would claim the row cannot be built first, which
is false.

`Depends on` publishes what a reorder would otherwise break with nobody noticing, and it holds ids and
nothing else — no grades, no counterfactuals. What every row depends on is not published: fifteen
edges that all say *after the skeleton* bury the four that carry information.

**What used to stay in reasoning is published now.** A one-shot delivery plan can keep its dependency
map, its horizon ledger and its row-to-source traceability out of the document, which works exactly
once — the session that writes the plan holds them. A living map cannot: the previous session's
reasoning no longer exists. So dependencies are a column and provenance is `Requested by` on the
row's document. The reasoning *behind* the order stays unpublished entirely: the register's order
carries it, and a reader is free to take a different one wherever no hard edge forbids it.

**Published order** is the failure to watch for: an edge that records the sequence the author prefers
rather than an outcome nothing else can make verifiable. Its tell is the substitution test itself — a
controlled input or a narrower real precursor could stand in, and the edge is published because
someone preferred that sequence. A shared pipeline already follows every row that feeds it; the edge
from the pipeline row to the last feeder adds nothing, and forbids a reorder no hard edge forbids.

**Dropped edge** is its mirror, and the more expensive half: an edge too many is noise a reader
discounts, a missing one is the reorder that breaks with nobody noticing.

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

**The map declares its own ranking.** The ranking between the criteria is itself a decision this map
takes, and the register's order is where the ranking shows. The criteria it ranks:

- the minimum delivery path — until something is delivered, nothing is learned;
- conventions born inside the first row that needs them, never in a workshop of their own;
- the differentiator and the existential business risk;
- irreversible, expensive or architecture-changing uncertainty;
- the real enablers those risks need in order to be tested;
- business frequency, and one thin outcome from each remaining theme;
- cohesive variants and deeper workflows, in risk order.

Four things are not up for ranking:

- **Breadth before depth.** Once the existential risks are validated, deliver one thin validating row
  from each remaining theme before a second row from one theme. Depart only for another
  differentiator, a material risk, required recovery, or a materially higher-frequency behaviour: the
  departure has to be one of the four, and the order is what shows it.
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
rows whose acceptance depends on real ownership or membership. Where identity is deferred past the
second `NOW` row that delivers behaviour to an end user, the rows that produce the evidence the
deferral rests on come before it in the register. Every row preceding identity names its own
audience: an `Outcome` promising *a user* who cannot exist yet belongs to a developer or to a tester
on the declared non-public environment.

## What the map reports about its input

Drawing forces the map to resolve things the sources left open. `Assumptions` and `Open questions` say
which ones, so the author gets a second reading of the vision's completeness. Neither is a work queue,
neither mints anything, and every line is traced to the themes and the ids it touches, or to `goal`
where what it touches is the whole map and no theme or row owns it.

Sweep the sources for two categories before the map is drawn, and give each entry a reference on both
sides:

- **conflicts** — pairs of incompatible statements, whether or not either names a provider, model,
  service or adapter. Sweep per behaviour the map will cut, not per component named, and sweep within
  a document as well as across two: the sharpest pair is often a reason contradicting its own
  conclusion a few lines below it;
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

**Record each entry in `.roadmap/log.md` before `Assumptions` is written**, under the session's H2
and below the theme verdicts, one bullet per entry the sweep found and not only per exit taken: the
citations on both sides — the one naming the choice, for an undecided one — then `assumption`,
`question` or `spike`, the one fact that decided it, and after an arrow where the entry went: the
trace of the line at map altitude, the row's id when the question lives on the row, the spike's id.
An `Argument:` line of at most two may follow the fact. An entry with no destination is an entry
that never left. The line carries the reading and its reason in full; the entry carries the pair,
the exit and one line, and where the two disagree the map wins.

```markdown
- `concepts.md` § Extraction / `architecture.md` § Manual entry — **assumption.** The manual form
  saves without entering the extractor; *same engine* names the schema, not the path. → `capture, S5`
- `architecture.md` § Search — **spike.** No source selects the embedding model. → `S2`
```

**Taken in a row and nowhere else** is the failure to watch for, and its tell is a lookup, not a
memory of the sweep. After the first cut, read every `Includes` and `Excludes` bullet that says
**how** a behaviour works or does not — *it skips the extractor*, *it shares the form and not the
pipeline* — or that gives its reason as what the sources hold — *the sources give it as the same
form* — and look that behaviour up in the sources. Where two of them describe it differently and no
line of `Assumptions`, no line of `Open questions` and no spike names that entry, the bullet is a
side taken, whether or not the entry was ever on the sweep's list; a bullet reading the sources as
agreeing is making the very claim the lookup checks. The bullet is where the reading is *applied*,
never where it is *reported*, and a reader who finds only the bullet cannot tell a decision from an
oversight. A neighbouring row that shares the schema, the pipeline or the form is not the report
either: it says what was built, not which side was taken and why. A bullet that only says which row
or which horizon a behaviour belongs to owes nothing. What the lookup turns up is an entry the sweep
missed: it goes into the log with its exit before the line is written, never into `Assumptions`
alone.

Exposing is not resolving. Only a source that selects resolves an entry: a published question and a
scheduled spike both leave it open, because neither has produced its answer when the map is drawn.
The reverse costs as much — an entry a source selects is answered, and publishing it as an open
question leaves the map less drawable than its own input.

Three tests on an `Assumptions` line once it is written:

- **Delivery can refute it.** A line restating what a source already says is true by construction and
  resolves nothing: either it quotes the source, and goes, or it holds a constraint whose mechanism is
  still missing, and the entry is still open.
- **It lands in a row.** A reading about *how* something works appears as a bullet of the row it is
  traced to. An assumption landing nowhere either was not needed or was not applied, and the row is
  where the map says what it assumed.
- **Its reason survives its citations.** Read each cited line inside the section that holds it: a
  reading the cited text will not bear is a misreading, not an assumption, and delivery cannot refute
  what the sources already refuted. The section names the subject of what it states, and that is a
  lookup, not a judgement: a reading that leaves the sentence standing and gives it a different
  subject — the ban is about *that* mechanism, not this one — is a misreading however the rest of the
  sources read. Where sources genuinely conflict, the line chooses between them and says which it
  took; it does not make the conflict go away by re-describing what one of them is about. Where two
  sources state a constraint together, splitting them needs a source that splits them. When the text
  will not bear the reading, either the entry is still open or another reading is available — and the
  one the sources support is usually a few lines from the quote already taken.

`OUT-OF-SCOPE` holds what the solution declares it will never solve, never what is merely far off, and
each exclusion is written as the licence it gives: *because this stays unsolved, the implementation
may do without X, and this is the price it pays*. Written as *we will not do X* the section reads as a
graveyard; written as a licence it still answers the question somebody asks a year later, which is why
the trade-off was allowed.

## Cross-functional concerns

Five dimensions are swept on every map: authorization, validation and errors, operability,
accessibility and security, data integrity and recovery. A sixth is swept when a source makes it a
constraint several rows must respect — cost, privacy, compliance, latency, auditability, data
migration. The sweep is not the section: it is what has to be thought before the section is written,
and the list is fixed here so a later session can re-run it.

**A concern is published when a `NOW` row could plausibly have done otherwise.** A rule the rows
would obey whether or not the map named it — a house convention, a framework default, a standing
instruction the project already carries — is not a constraint this map decided. Publishing it costs
twice: it drifts against the document that really governs it, and it leaves the reader unable to tell
what binds because the map chose it from what binds anyway.

**Ambient restatement** is the failure to watch for, and its tell is mechanical: the line survives
being moved to another project unchanged. A dimension the sweep finds nothing in carries no line, and
the absence is information — nothing about it was decided here.

## The map holds when

- every theme has a promise in product language and one first validator that is an existing `NOW` row,
  and no enabler validates a theme whose promise is not to a developer;
- every theme boundary has a split or merge verdict in `log.md`, written before the `Themes` table
  and repeated nowhere in the map, and no first validator excludes a capability its own theme's
  promise names;
- greenfield draws the repository row and the skeleton separately, and the skeleton reaches the
  datastore through the real driver and runs a migration;
- every published `Depends on` survives the substitution test — no controlled input and no narrower
  real precursor already in `NOW` can stand in — and no row that builds on a table, resolver or
  adapter another `NOW` row delivers, or whose evidence is made of capabilities other `NOW` rows
  deliver, carries `—`;
- no `Depends on` cell names the repository row or the skeleton;
- every departure from breadth before depth is one of the four the skill licenses;
- the scope boundary ships with the first row that persists data, and identity deferred past the
  second end-user row is preceded in the register by the rows producing the evidence for it;
- every conflict and every undecided choice is an entry in `log.md` written before `Assumptions`,
  every entry names the exit it left by and where the line or the spike is, and every bullet stating
  how a behaviour works, or reading the sources as agreeing on it, was looked up in the sources
  before the map was written;
- every line of `Assumptions` and `Open questions` traces to a theme, an id or `goal`;
- delivery can refute every `Assumptions` line, every reading about how something works lands in a
  bullet of the row it is traced to, and no reading is contradicted by the lines it cites or gives
  one a subject its section does not name;
- no published cross-functional concern survives being moved to another project unchanged, and a
  dimension the sweep found nothing in carries no line;
- `NOW` fits under the cap without inventing detail the map cannot yet know.
