---
name: plan-slices
description: Create, review, split, merge, and reorder delivery plans for greenfield products and major capabilities. Use for risk-first vertical slicing, explicit NOW/LATER/OUT-OF-SCOPE horizons, independently schedulable product themes, and user-useful developer enablers. Reject horizontal layer-by-layer plans. Reserve isolated fixes and routine refactors for ordinary task planning unless delivery slicing is explicitly requested.
license: MIT
---

# Plan Delivery Slices

Plan for early validated learning, short feedback loops, and cheap reprioritization. Treat a
result as user-useful when it helps either an end user or a developer test the real product while
building it.

## Choose the branch

- **Create:** execute steps 1–5 and satisfy every completion criterion.
- **Review:** execute steps 1–2, audit against steps 3–5, then report findings.
- **Split, merge, or reorder:** execute steps 1–2 for the affected scope, apply steps 3–4, then
  republish through step 5.

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

Reconcile the inventory before mapping. Do not silently choose between conflicting statements or
reopen a decision that a source declares closed. When a conflict changes feasibility, scope, or
order, publish it under `Open questions` or place a spike before the affected slice. Do not state an
unconditional outcome while its enabling decision remains unresolved.

**Proceed when:** every sequencing-relevant statement has applicable classifications and a source;
unsupported conclusions are assumptions; exclusions have explicit rationale; material source
conflicts are resolved, exposed, or assigned to a spike.

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
- its first validating `NOW` slice.

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
2. the smallest deployed walking skeleton through build, CI/CD, provisioning, and a representative
   non-production environment.

Keep the walking skeleton free of authentication, tenancy, and domain CRUD when a thinner real
runtime path can validate delivery. Make independently useful access and domain behaviour later
slices.

**Proceed when:** every goal maps to an outcome, theme, and horizon; theme split/merge decisions
pass the independence tests; hard dependencies are limited to outcomes no controlled input can
verify; greenfield prerequisites are present and separate. Keep this map in reasoning, not in the
published plan.

## 3. Cut user-useful vertical slices

Give each slice one primary user-useful outcome and one learning target. End users and developers
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

After the first cut, audit adjacent slices in both directions. Merge slices that duplicate the same
interaction and invariant without changing a decision. Split independently testable fallbacks,
external adapters, lifecycle operations, or failure profiles. Deliver a required correction,
retry, or escape path before or with the first behaviour that can create the recoverable state.

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
Do not add a domain dependency to the walking skeleton only because the next slice will need it.

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
user-useful vertical result.

**Proceed when:** every slice has one outcome and learning target; every enabler passes all enabler
tests; every split warning is resolved by splitting or a concrete cohesion reason; every in-scope
behaviour has one owner or explicit exclusion.

## ANTI-PATTERNS

- **Layer slices:** “design schema”, “build API”, “build UI”, then “integrate” as separate slices.
- **Infrastructure by accumulation:** provision services or add abstractions without exercising the
  real path needed by an adjacent outcome.
- **Enabler camouflage:** call horizontal setup an enabler without a developer-useful result,
  executable verification, and named product successor.
- **Oversized walking skeleton:** combine deploy, login, tenancy, and first CRUD when each can be
  validated independently.
- **Fake verticality:** use mocks or precomputed fixtures that bypass the material production
  transformation, authorization, persistence, or adapter under test.
- **Theme compression:** merge independently schedulable value areas to keep the theme count small.
- **Atomization:** split one cohesive interaction or invariant only to reduce apparent slice size.
- **Silent contradiction:** publish an unconditional slice while its sources disagree about a
  decision required to implement or verify it.
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

Respect hard dependencies, then order `NOW` by:

1. minimum delivery path and early human review needs;
2. differentiating value and existential business risk;
3. irreversible, expensive, or architecture-changing uncertainty;
4. real enablers required to test those risks;
5. business frequency and one thin outcome from remaining themes;
6. cohesive variants and deeper workflows in risk order.

Use the cheapest real input capable of validating a risky engine. Do not front-load commodity work
for reuse alone.

After validating existential risks, prefer breadth before depth: deliver one thin validating slice
from each remaining `NOW` theme before a second slice from one theme. Depart only for another
differentiator, a material risk, required recovery, or materially higher-frequency behaviour, and
state that exception once under `Ordering criteria`.

Separate a boundary from the identity behind it. Ship the tenancy, ownership, or scope boundary with
the first slice that persists data, and let a single named resolver own the current scope; then a
later slice can replace a configured scope with an authenticated one at one seam. State that seam
under `Cross-functional concerns`. Never defer the boundary itself, and never defer identity when no
such seam exists.

Once the evidence that justified deferring identity exists, deliver identity before further
user-facing slices whose acceptance depends on real ownership or membership.

When `NOW` targets selected end users, end it with the smallest release slice that makes the
coherent release usable in its intended environment. Tag it `(Release: delivery)`, not `Enabler`,
and include only source-backed operational readiness. When `NOW` intentionally ends at developer
validation, state that audience and environment explicitly instead.

When a real slice cannot resolve a material uncertainty, define a time-boxed spike with question,
evidence, enabled decision, exit criterion, and treatment of experimental code.

Add checkpoints only where evidence can cancel, promote from `LATER`, reorder, split, or change
unfinished work.

**Proceed when:** every differentiator and material risk has a first validator; all horizon
assignments are exclusive; every `LATER` item has a trigger; order respects dependencies and
delivery maturity; checkpoints name evidence and decisions they can change.

## 5. Publish and audit

Read and follow [assets/plan-template.md](assets/plan-template.md). Preserve its heading hierarchy,
section names, field names, and order; write content in the user's language.

- Use bullets or tables for technical sections; avoid prose blocks.
- Keep `Cross-functional concerns`, `NOW`, `LATER`, and `OUT-OF-SCOPE` as exact labels.
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

When an eval specification exists, run:

```bash
python3 <skill-dir>/scripts/validate_plan.py path/to/plan.md --expectations path/to/expectations.json
```

Fix every structural failure. Treat expectation failures as eval evidence: inspect the plan and
skill before changing the expectation.

**Complete when:** the validator passes; themes trace to first validators; `NOW` is a coherent
user-useful release; enablers are vertical and adjacent to their product outcome; `LATER` is
evidence-dependent; the slice order respects every hard dependency; every source behaviour has one
horizon; end-user `NOW` reaches its intended environment; only implementation-changing questions
remain.

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
