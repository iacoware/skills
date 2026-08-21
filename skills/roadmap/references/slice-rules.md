# Slice rules

True on every operation — drawing, promotion, admission, revision, close-out, retirement. Nothing here
goes inert between goals.

The register holds **rows**, and a row is a slice or a spike. Themes, the two prerequisites, order,
hard dependencies and the identity seam are the shape of the map rather than the rules of a row;
[`drawing-the-map.md`](./drawing-the-map.md) holds them, and a session that changes the shape reaches
for it.

## What makes a slice

One vertical outcome, one learning target. Both singular, both mandatory. End users and developers
testing the real product both count as users.

- **Independently deployable, verifiable, reviewable and revertible.**
- **Complete through every production layer its outcome requires.** A row that stops at one layer is
  not thin, it is unfinished.
- **Safe enough for the audience and environment it names.**
- **The smallest coherent path that produces useful evidence.** Prefer a thin real capability followed
  by explicit deepening rows.

Risk is not a field: where a risk is material it *is* the learning target, and every row has exactly
one.

## Verification maps to the learning target

Every material claim in `Learning target` maps to an observation in `Verification`, stated so that
delivery can refute it. Checking that data exists does not demonstrate its quality, usability, latency
or cost.

Include the behaviour-specific validation, authorization, failure handling, logging, observability,
accessibility, security and data integrity the outcome requires. Expectations repeated across rows are
stated once under `Cross-functional concerns` and verified in the first row that crosses each trust
boundary or performs each external side effect; name the abuse, timeout, invalid-output and
partial-failure modes that actually apply, because a generic cross-functional sentence is not
evidence.

## The spike test

**When the verification is a measurement rather than a capability, it is a spike.** Write the honest
`Verification` out and read it: *we can state recall and p95 latency for a shared index at that
volume* is a number, not a thing somebody can do. A spike has a learning target and no vertical
outcome, so *What makes a slice* does not apply to it.

**The measurement becomes its own row**, and the row it came from depends on it. Widening that row,
or minting only the row that makes the measurement possible, leaves the unknown where it was.

A spike carries `kind: spike`, and:

- **it leaves `Audience` empty** — the one field it does not fill. It has no user, and who consumes
  its answer is named by what depends on it;
- **it must have a dependent.** Either a row names it in `Depends on`, or its own row claims
  `theme: goal`, which declares that it validates the goal's feasibility. A spike nobody is waiting on
  is curiosity;
- **it competes for a row under the cap** like everything else in `NOW`. Research displacing a slice
  is the cost showing up where it can be argued with;
- **it carries no timebox.** It is timeboxed in the doing, downstream, and a duration nothing can
  check is a hollow ritual. What the map can see is the row that has not closed for three sessions,
  which is a conversation.

Everything else it shares with a slice: the same id sequence and minting, `Depends on`, readiness,
executor, a document in `slices/`, and close-out into `archive/` — a spike that answers its question
was delivered. Its `Excludes` says what becomes of the experimental code, which is usually that none
of it survives the spike.

Downstream a spike goes to `/prototype` when the question needs something built to answer it and to
`/wayfinder` when it is a choice to be made; never to `/to-spec`, which has no spec to write.

Scheduling a spike does not resolve a conflict between sources. It schedules the work that will.

## Splitting and merging a row

**Split warnings.** Each is resolved by splitting or by naming the cohesion that holds the row
together:

- distinct user capabilities joined with *and*;
- more than one theme;
- more than one independent material risk;
- a basic flow mixed with an independently valuable fallback, variant, bulk behaviour or lifecycle;
- independent acceptance demonstrations that could change priorities separately;
- one row that can fail for two independent causes that would change different decisions — a shared
  failure hides its own cause.

**Cohesion that holds.** Keep behaviours in one row when they share the theme, the interaction or
pipeline, the adapter, the invariant and the learning target, and separating them would create a
temporary contract or produce no useful feedback alone. Shared create-and-edit review, or several
inputs into one established pipeline, may therefore stay one row.

**Merge test.** Merge two rows when they share the same interaction, invariant and learning target and
neither produces useful feedback alone. Separate names or modes are not sufficient reason to split one
coherent behaviour, and size, tidiness and preference are not reasons to do either. After a first cut,
read adjacent rows against both tests in both directions, and record the verdict for each pair.

**Deliver a required correction, retry or escape path before or with the first behaviour that can
create the recoverable state.**

**One owner per behaviour.** Every in-scope behaviour, and every producer feeding a shared pipeline or
adapter, has one owning row or an explicit exclusion. Different failure profiles do not justify
non-adjacent partial ownership of one adapter or invariant: co-locate the behaviour, or let the first
row establish a complete stable capability that later rows consume without **re-opening ownership**.

**Conserve the behaviour set.** A split distributes the original outcome across the resulting rows and
introduces none; a merge yields one outcome and one learning target; a reorder changes positions only.
A behaviour that loses its owner moves to `LATER` as a candidate or to `OUT-OF-SCOPE` as an exclusion.
It never simply disappears.

## Identity

Ids are minted at promotion by monotonic increment: the highest id across `.roadmap/slices/` and
`.roadmap/archive/`, plus one. The filenames carry it, so it is two directory listings and no counter
to keep in sync.

- **An id never means position.** `kind` says what the row is, the register's order says when it is
  delivered, and the id says only which row this is. A spike minted late and delivered first is
  ordinary.
- **An id is never recycled**: not after a retirement, not across a redraw.
- **A split keeps the id on the half that keeps the learning target**, and mints a new one for the
  other half. Every `Depends on` pointing at the original still resolves, which is exactly why
  identity follows the learning target rather than the cut. A merge follows the same rule: the
  surviving row keeps the id of the learning target that survives, and the other id is spent.
- **Retirement spends the id and deletes the document.** `archive/` means *delivered* and would start
  lying the moment it held something that was not; git is the archive for what never happened.

## The columns

A field earns a column when it is used to compare rows and decide what comes first. A field read only
while reasoning inside one row lives in that row's document, and a column is never repeated there.

**`kind`** — what the row is.

- **`product`** delivers a capability to somebody who is not building it.
- **`enabler`** is a **stepping stone**: an intermediate row for a developer that exists to make
  later rows cost less. It earns the kind only when it exercises a real end-to-end production path
  rather than one isolated layer, leaves the row depending on it the executable evidence it needs,
  and carries no speculative foundation beyond that. Horizontal setup wearing the label without those
  is **enabler camouflage**.

  One enabler may answer several questions about a single subsystem — a datastore with its driver and
  migrations, an inference engine, one adapter family — never questions whose answers change decisions
  in two: a verification that can fail for either would not say which decision to revisit. It may
  include the smallest diagnostic consumer needed to observe its uncertainty, while product
  interaction and business feedback belong to the successor, which adds a user outcome instead of
  repackaging the enabler. A separate domain-convention enabler is allowed only when it independently
  validates the scope, persistence, UI or test conventions a materially riskier row needs first; reuse
  by later work is not enough.
- **`release`** delivers a deployment rather than a capability: the walking skeleton, and the row that
  puts the coherent release into its intended environment.
- **`spike`** produces knowledge instead of an outcome, and the test that recognises one is above.

**`size`** — `small`, `medium`, `large`. A coarse signal whose only effect is routing downstream:
`large` goes through `to-tickets`, everything else goes straight to `to-spec`. It is not a token
budget and not an estimate; on a spike it decides nothing, because `kind` routes there.

Cut early rows narrow while the delivery, testing, domain and UI patterns still need frequent human
review, and grow them once those patterns exist and the combined work stays cohesive. A row is never
sized larger merely because it comes later.

**`readiness`** — whether the row can be picked up today, as opposed to whether it is on the path.

- `ready` — nothing blocks it.
- `needs-decision` — a choice the author owns and has not made.
- `needs-info` — it is waiting on somebody else.

What blocks this row alone is written in the row's own `Open questions` and shows here; an entry that
questions the shape of the map is at map altitude instead, and scope is the only thing that routes the
two. A row whose decision the sources leave open is `needs-decision`, and its `Includes` and
`Verification` are worded to defer to the pending decision rather than picking a side — publishing it
unconditionally is **silent contradiction**.

Readiness never names an actor. The `triage` labels are derived at handover by combining it with
`executor` — `ready` + `agent` → `ready-for-agent`, `ready` + `human` or `mixed` → `ready-for-human` —
and never stored.

**`executor`** — `agent`, `human`, `mixed`. Separate from readiness because almost every
infrastructural row is `mixed`: a person opens the accounts and clicks through a console, an agent
writes the code. It is what makes undelegable work visible before it blocks a session.

## Named failures

Shapes that can pass every rule above and still be wrong:

- **Layer slices** — *design the schema*, *build the API*, *build the UI*, then *integrate*.
- **Infrastructure by accumulation** — provisioning a service or adding an abstraction without
  exercising the real path an adjacent outcome needs.
- **Fake verticality** — mocks or precomputed fixtures that bypass the material production
  transformation, authorization, persistence or adapter under test.
- **Atomization** — splitting one cohesive interaction or invariant only to make a row look smaller.
- **Deferred safety** — a generic error-handling, authorization, accessibility, observability or
  security row for behaviour the earlier rows need in order to be safe at all. Replacing a configured
  scope with an authenticated one at a declared seam is not this; shipping rows whose reads are
  unscoped is.
- **Horizon dumping** — unfinished mandatory behaviour filed as a candidate, or speculation admitted
  into `NOW`. A candidate is what does not serve *this* goal, never what is merely unfinished; and a
  capability merely compatible with the data model, or convenient once an entity exists, was never
  asked for, so it is a candidate however cheap it looks.

## A row holds when

- it is a slice with one vertical outcome and one learning target, or a spike with a learning target,
  an empty `Audience` and a dependent;
- its honest `Verification` names a capability somebody can check, or the row carries `kind: spike`;
- every material claim in `Learning target` has an observation in `Verification`;
- every split warning was resolved by splitting or by a named cohesion, and every behaviour it touches
  has one owner or an explicit exclusion;
- `kind`, `size`, `readiness` and `executor` are set, and an `enabler` passes every enabler test;
- what blocks it is in its own `Open questions` and shows in its readiness, and no bullet asserts a
  side of a decision nobody has taken;
- its id was minted by increment, stayed with the learning target through any split or merge, and was
  recycled from nothing;
- it is none of the named failures.
