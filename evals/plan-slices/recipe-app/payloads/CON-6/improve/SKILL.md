---
name: plan-slices
description: High-level planning for greenfield products and major capabilities — create, review, split, merge, and reorder delivery roadmaps into value-first, risk-first vertical slices.
license: MIT
disable-model-invocation: true
---

# Plan Delivery Slices

Produce a multi-session delivery map, not an implementation plan or task backlog. Treat each slice
as an independently schedulable outcome; do not decompose slices into implementation tasks.

Plan for early validated learning, short feedback loops, and cheap reprioritization. Treat a
result as valuable when it helps either an end user or a developer test the real product while
building it.

## Choose the branch

- **Create:** execute steps 1–5 and satisfy every completion criterion.
- **Review:** execute steps 1–2, then follow `Review an existing plan`.
- **Split, merge, or reorder:** execute steps 1–2 for the affected scope, then follow `Split, merge,
  or reorder an existing plan`.

Modify an existing plan only when requested.

## 1. Build the evidence inventory

Inspect designated goals, decisions, plans, and relevant repository state. Record every statement
capable of changing scope, order, architecture, or a go/no-go decision as:

- differentiating value;
- user or developer outcome;
- business assumption or risk;
- technical uncertainty;
- existing foundation;
- candidate dependency;
- delivery-maturity or review-cadence constraint;
- candidate `NOW`, `LATER`, or `OUT-OF-SCOPE` behaviour;
- explicit exclusion.

Retain sources. Mark unsupported conclusions as assumptions.

Reconcile the inventory before mapping. Sweep the sources for two separate categories and list each
entry with a reference for every side:

- **conflicts:** pairs of incompatible statements;
- **undecided choices:** a provider, model, service, or adapter named without a source that selects
  it. A qualifying adjective — `cheap`, `multilingual`, `managed` — is not a choice.

Do not silently pick a side or reopen a decision that a source declares closed. Expose every material
entry either with an `Open questions` item naming the slices it blocks, or with a spike before the
first blocked slice.

Exposing is not resolving. Only a source that selects resolves an entry; a published question and a
scheduled spike both leave it open, because neither has produced its answer when the plan is written.
While an entry is open, no `Includes` or `Verification` bullet of a slice it blocks may assert a
side: only conditional wording that defers to the pending decision is allowed.

**Proceed when:** every sequencing-relevant statement has applicable classifications and a source;
unsupported conclusions are assumptions; exclusions have explicit rationale; every material conflict
and undecided choice is resolved, exposed with the slices it blocks, or assigned to a spike.

## 2. Map themes, outcomes, and dependencies

List independently useful outcomes. Create a separate product theme when capabilities differ
materially in any of:

- user job or intent;
- business value or usage frequency;
- primary business or technical risk;
- external adapter or operational profile;
- ability to defer or reorder independently.

Do not optimize for fewer themes. Merge themes only when neither can produce independent feedback
or move independently. A user-facing identity or access capability may be a theme; an authentication
library or database layer is not.

Run both tests explicitly:

- **Split test:** split when either capability can be cancelled, deferred, or reordered without
  invalidating the other's evidence. A shared entity, form, pipeline, or implementation is not a
  sufficient reason to merge independently schedulable value.
- **Merge test:** merge when the capabilities share the same interaction, invariant, and learning
  target, and neither produces useful feedback alone. Separate names or modes are not sufficient
  reasons to split one coherent behaviour.

Give every theme:

- one desired outcome in product language;
- its first `NOW` product slice that validates the complete desired outcome.

An enabler may precede that validator but cannot substitute for it unless the theme's desired
outcome is itself for a developer; a theme claiming that exception appends `*(Developer outcome)*`
to its desired outcome in the published table, so the claim stands next to the enabler it
authorises. A slice that validates only one capability inside a broader theme outcome is not that
theme's first validator.

Identify hard dependencies only: a predecessor is hard when no controlled input or narrower real
precursor can make the dependent outcome realistically verifiable. Convenient reuse, a fuller demo,
or a preferred order is not a hard dependency — leave those to the ordering rules in step 4.

Controlled inputs may replace unfinished UI or administration. They must still traverse every
production path whose correctness materially affects the outcome. Fixtures that inject derived
data directly do not remove a dependency on the production computation of that data.

Hard dependencies constrain the slice order and nothing else. Do not grade them, do not write
counterfactuals for them, and do not publish them.

For greenfield work, add:

1. a repository prerequisite with CI build, lint, typecheck, and tests; no provisioning or deploy;
2. the smallest deployed walking skeleton that proves the decided infrastructure is connected and
   running, through build, CI/CD, provisioning, and a representative non-production environment.

The skeleton must exercise every already-decided stateful or managed dependency that has no thinner
real validator later — at minimum the datastore, reached at runtime through the real driver and
connection mode by one non-domain operation, plus the migration runner applying one non-domain
migration. Connection mode, pooling, migration mechanics, and their interaction with cold start
cannot be validated more cheaply, and discovering them inside a risky domain slice confounds two
failures.

Keep the skeleton free of domain entities, domain CRUD, authentication, and tenancy, and leave out
external adapters used by only one later slice: validate those in that slice. Make independently
useful access and domain behaviour later slices.

**Proceed when:** every goal maps to an outcome, theme, and horizon; theme split/merge decisions
pass the independence tests; hard dependencies are limited to outcomes no controlled input can
verify; greenfield prerequisites are present and separate. Keep this map in reasoning, not in the
published plan.

## 3. Cut valuable vertical slices

Give each slice one primary valuable outcome and one learning target. End users and developers
testing the product both count as users.

Make each slice:

- independently deployable, verifiable, reviewable, and revertible;
- complete through every production layer required by its outcome;
- safe enough for its stated users and environment;
- the smallest coherent path that produces useful evidence.

### Product slices

Prefer a thin real capability followed by explicit deepening slices. Treat these as split warnings:

- distinct user capabilities joined with “and”;
- more than one product theme;
- multiple independent material risks;
- a basic flow mixed with an independently valuable fallback, variant, bulk behaviour, or lifecycle;
- independent acceptance demonstrations that could change priorities separately.

Keep behaviours together when they share the same theme, interaction or pipeline, adapter,
invariant, and learning target, and separation would create a temporary contract or no useful
feedback. Shared create/edit review or multiple inputs to one established media pipeline may
therefore remain cohesive. Defer independently optional interactions to `LATER`.

After the first cut, audit adjacent slices in both directions and record the verdict for each pair.
Merge slices that duplicate the same interaction and invariant without changing a decision. Split
independently testable fallbacks, external adapters, lifecycle operations, or failure profiles.
Split whenever either part can be deferred independently, or when one slice can fail for two
independent causes that would change different decisions: a shared failure hides its own cause.
Deliver a required correction, retry, or escape path before or with the first behaviour that can
create the recoverable state.

Different failure profiles do not justify non-adjacent partial ownership of one adapter or
invariant. Co-locate the behaviour, or make the first slice establish a complete stable capability
that later slices consume without reopening ownership. Never interleave another theme while shared
adapter or invariant ownership remains partial.

### Developer enablers

Allow an explicit `Enabler` slice when its primary user is a developer and it:

- exercises a real end-to-end production path, not one isolated layer;
- produces executable evidence needed by the next product slice;
- resolves one material uncertainty or establishes one high-leverage delivery pattern;
- is immediately followed by, or explicitly tied to, the product outcome it enables;
- contains no speculative foundation beyond that path.

Examples include processing normalized fixtures through the real embedding and persistence
pipeline before semantic retrieval, or deploying the minimum runtime before authentication.

An enabler may include the smallest diagnostic consumer needed to observe its uncertainty, such as
a command that ranks persisted vectors. Keep product interaction and business feedback in the
successor, and ensure the successor adds a user outcome rather than merely repackaging the enabler.
Do not add a domain dependency to the walking skeleton only because the next slice will need it;
infrastructure connectivity is not a domain dependency.

Allow a separate domain-convention enabler only when it independently validates new scope,
persistence, UI, or test conventions needed before a materially riskier slice. Reuse by later work
or presence in an example plan is insufficient.

### Size calibration

- Keep early slices narrow while delivery, testing, domain, and UI conventions need frequent human
  review.
- Increase size only after relevant patterns exist and the combined work remains cohesive.
- Never make later slices larger merely because they occur later.

Include behaviour-specific validation, authorization, failure handling, logging, observability,
accessibility, security, and data integrity where required. State repeated expectations once under
`Cross-functional concerns`, but verify them in the first slice that crosses each trust boundary or
performs each external side effect. Name relevant abuse, timeout, invalid-output, and partial-failure
modes; a generic cross-functional statement is not evidence. Do not defer production-required
failures to generic hardening.

Every material claim under `Learning / risk` must map to an observation in `Verification`. Checking
that data exists does not demonstrate its quality, usability, latency, or cost.

Classify risk spikes, migrations, and operational work separately when they cannot produce a
valuable vertical result.

**Proceed when:** every slice has one outcome and learning target; every enabler passes all enabler
tests and validates no more than one material uncertainty; every split warning is resolved by
splitting or a concrete cohesion reason; every in-scope behaviour, and every producer feeding a
shared pipeline or adapter, has one owner or explicit exclusion.

## ANTI-PATTERNS

- **Layer slices:** “design schema”, “build API”, “build UI”, then “integrate” as separate slices.
- **Infrastructure by accumulation:** provision services or add abstractions without exercising the
  real path needed by an adjacent outcome.
- **Enabler camouflage:** call horizontal setup an enabler without a developer-useful result,
  executable verification, and named product successor.
- **Oversized walking skeleton:** combine deploy, login, tenancy, and first CRUD when each can be
  validated independently.
- **Hollow walking skeleton:** a deployed runtime that answers a static response without reaching
  the datastore or running a migration, deferring driver, connection, and migration risk into a
  later domain slice.
- **Fake verticality:** use mocks or precomputed fixtures that bypass the material production
  transformation, authorization, persistence, or adapter under test.
- **Premature or split shared pipeline:** open a pipeline or adapter shared by several paths before
  its `NOW` producers exist, or let a second slice re-open what another slice already owns.
- **Theme compression:** merge independently schedulable value areas to keep the theme count small.
- **Atomization:** split one cohesive interaction or invariant only to reduce apparent slice size.
- **Silent contradiction:** publish an unconditional slice while its sources disagree about, or
  never make, a decision required to implement or verify it.
- **Deferred safety:** create generic error-handling, authorization, accessibility, observability,
  or security slices for behaviour required safely in earlier `NOW` slices. Replacing a configured
  scope with an authenticated one at a declared seam is not deferred safety; shipping slices whose
  reads are unscoped is.
- **Horizon dumping:** place unfinished mandatory behaviour in `LATER`, or speculative ideas in
  `NOW`, without an evidence-based reason.

## 4. Assign horizons and order for learning

Assign every behaviour to exactly one horizon:

- **NOW:** the smallest coherent release useful to selected end users or developers; includes the
  essential value hypothesis, material risk validation, and safe-operation baseline.
- **LATER:** a candidate variant or deepening whose value, shape, or priority depends on `NOW`
  evidence. Record its promotion trigger.
- **OUT-OF-SCOPE:** an explicit exclusion. Record its rationale; do not plan implementation.

Admission test: `NOW` requires a source that asks for the behaviour, `LATER` a promotion trigger,
`OUT-OF-SCOPE` a declared exclusion. Trace each `NOW` slice to the requesting statement in
reasoning, not in the published plan. A capability merely compatible with the data model, or
convenient once an entity exists, was never requested: it belongs in `LATER` with its trigger.

Respect hard dependencies, then order `NOW` by:

1. minimum delivery path and early human review needs;
2. differentiating value and existential business risk;
3. irreversible, expensive, or architecture-changing uncertainty;
4. real enablers required to test those risks;
5. business frequency and one thin outcome from remaining themes;
6. cohesive variants and deeper workflows in risk order.

Use the cheapest real input capable of validating a risky engine. Do not front-load commodity work
for reuse alone.

Controlled cheap inputs may validate shared machinery in an enabler, but do not reorder
independently useful product flows. When sources define a recovery chain, extend the primary
interaction with required automatic recovery before adding a separate manual escape.

After validating existential risks, prefer breadth before depth: deliver one thin validating slice
from each remaining `NOW` theme before a second slice from one theme. Depart only for another
differentiator, a material risk, required recovery, or materially higher-frequency behaviour, and
state that exception once under `Ordering criteria`.

Required recovery outranks breadth. When a slice names a failure mode in its `Verification` and
another `NOW` slice is its remedy, deliver the remedy before opening a different theme; a remedy the
sources declare a fallback of a delivered path closes that path and is not optional depth. Likewise,
a slice that opens a pipeline or adapter shared by several paths follows every `NOW` slice that
feeds it, and owns it alone.

Separate a boundary from the identity behind it. Ship the tenancy, ownership, or scope boundary with
the first slice that persists data, and let a single named resolver own the current scope; then a
later slice can replace a configured scope with an authenticated one at one seam. State that seam
under `Cross-functional concerns`. Never defer the boundary itself, and never defer identity when no
such seam exists.

Once the evidence that justified deferring identity exists, deliver identity before further
user-facing slices whose acceptance depends on real ownership or membership. Past the second `NOW`
slice that delivers behaviour to an end user, justify the remaining deferral once under `Ordering
criteria`, naming the evidence that still requires it. Every `NOW` slice preceding identity states
its own audience: an `Outcome` promising "a user" who cannot exist yet belongs to a developer or a
tester on the declared non-public environment.

When `NOW` targets selected end users, end it with the smallest release slice that makes the
coherent release usable in its intended environment. Tag it `(Release: delivery)`, not `Enabler`,
and include only source-backed operational readiness. When `NOW` intentionally ends at developer
validation, state that audience and environment explicitly instead.

When a real slice cannot resolve a material uncertainty, define a time-boxed spike with question,
evidence, enabled decision, exit criterion, and treatment of experimental code.

Add checkpoints only where evidence can cancel, promote from `LATER`, reorder, split, or change
unfinished work.

**Proceed when:** every differentiator and material risk has a first validator; all horizon
assignments are exclusive and pass the admission test; every `LATER` item has a trigger; every
named failure mode whose remedy is in `NOW` gets it before a different theme starts; every shared
pipeline follows its producers; every slice preceding identity names an audience compatible with a
configured scope; order respects dependencies and delivery maturity; checkpoints name evidence and
decisions they can change.

## 5. Publish and audit

Before publication, complete an unpublished ledger mapping:

- every source behaviour to its theme, horizon, and owning slice or explicit exclusion;
- every theme to its complete product outcome and first product validator;
- every shared adapter and invariant to one complete owner;
- every named failure to its recovery and required position;
- every unresolved decision to blocked slices and its prior spike or open question;
- every adjacent slice pair to its split/merge verdict.

Reject the draft when a mapping is missing, conflicting, duplicated incompatibly, or points to
partial ownership or a partial theme validator. Keep the ledger in reasoning, not the published
plan.

Read and follow [assets/plan-template.md](assets/plan-template.md). Preserve its heading hierarchy,
section names, field names, and order; write content in the user's language.

- Use bullets or tables for technical sections; avoid prose blocks.
- Keep `Cross-functional concerns`, `NOW`, `LATER`, and `OUT-OF-SCOPE` as exact labels.
- Set every `Themes.First validation` cell to the number of an existing `NOW` slice.
- Detail numbered `NOW` slices only. Tag them `(Theme: …)`, `(Enabler: …)`, or
  `(Release: delivery)`. Keep `LATER` conditional and compact.
- Separate every numbered `NOW` slice title from its fields with a `---` rule.
- Give every `NOW` slice bullet lists under `Includes`, `Verification`, and `Outcome`, in that
  order.
- Add `Learning / risk` between `Verification` and `Outcome` only when material.
- Add other slice-specific annotations only when the plan needs them, as `**Label**` blocks after
  the standard fields.
- Publish no dependency graph, no sequencing section, and no per-slice ordering rationale: the slice
  order carries it, and `Ordering criteria` states the rules once.
- Always publish all three horizon sections; use `- None identified.` when `LATER` or
  `OUT-OF-SCOPE` is empty.
- Omit empty optional sections, including `Non-product work` and `Open questions`.

Keep the document short enough to be read in one pass: at most five bullets per slice field, one
line per bullet, no restating of `Cross-functional concerns` inside slices.

After publishing, run the validator. It checks section presence and order, the themes table, the
slice numbering, the slice tag, the `---` rule, field presence, field order, and list-only content —
so publish first and let it find structural defects instead of reading its source. Resolve
`<skill-dir>` to the absolute path of the directory containing this `SKILL.md`; the working
directory is the user's project, not the skill.

```bash
python3 <skill-dir>/scripts/validate_plan.py path/to/plan.md
```

Fix every structural failure.

**Complete when:** the validator passes; themes trace to first validators; `NOW` is a coherent
valuable release; enablers are vertical and adjacent to their product outcome; `LATER` is
evidence-dependent; the slice order respects every hard dependency; every source behaviour has one
horizon; no slice asserts a side of a listed conflict or undecided choice; every external
dependency invoked in `NOW` has a selecting source or an `Open questions` entry, and every published
question names the slices it blocks; end-user `NOW` reaches its intended environment; only
implementation-changing questions remain.

## Review an existing plan

Apply every applicable criterion from steps 2–5. For each failure, state:

- target;
- failed criterion or anti-pattern;
- delivery consequence;
- concrete change.

Keep passing verdicts internal. Modify the plan only when requested.

**Complete when:** every applicable criterion has a pass, fail, or not-applicable verdict; every
differentiator, material risk, horizon assignment, theme boundary, slice, and ordering constraint is
traceable to a verdict.

## Split, merge, or reorder an existing plan

Reopen only the affected scope: the named slices, their theme, and any slice whose position depends
on them. Leave the rest of the plan untouched. An edit is not a rewrite; unrelated churn hides what
actually moved and costs the reader the ability to review the change.

Justify the edit against the test that owns it — the split and merge tests in step 2, the ordering
rules in step 4, or a `Decision checkpoints` entry whose evidence has arrived. Size, tidiness, and
preference are not justifications. When no test supports the requested edit, say so and stop.

Conserve the behaviour set. A split distributes the original outcome across the resulting slices and
introduces none; a merge yields one primary outcome and one learning target; a reorder changes
positions only. A behaviour that loses its owner moves to `LATER` with a promotion trigger or to
`OUT-OF-SCOPE` with a rationale, never disappears.

Apply steps 3–4 to the affected scope, then republish through step 5, validator included. Repair
every reference the edit invalidates: renumbering `NOW` slices moves the targets of
`Themes.First validation`, `Decision checkpoints`, `Open questions`, and any `LATER` trigger naming
a slice. A checkpoint whose evidence triggered this edit records the decision it produced.

**Complete when:** every applicable step-5 criterion still holds; the edit traces to a split test,
merge test, ordering rule, or checkpoint; each resulting slice has one outcome and one learning
target and passes the independence tests; the behaviour set changed only through a recorded horizon
move; every reference to a slice number resolves to the slice it meant; slices outside the affected
scope are unchanged; any new departure from breadth before depth is stated once under `Ordering
criteria`.
