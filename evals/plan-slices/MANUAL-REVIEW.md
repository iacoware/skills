# Manual review of a generated plan

What to read on a plan produced by `skills/plan-slices/SKILL.md`, to notice that a change to the
skill broke something it used to get right.

This list is the distillation of `REGRESSION-LEDGER.md`, which retired on 2026-08-11 together with
the consensus cycle — see `README.md`. Each check was a falsifiable claim implied by a change
actually applied to the skill, verified across five cycles. What is gone is the apparatus around
them: counters, provenance, `Measured on`, absorption, dormancy. What stays is the list.

**Ids are inherited** from the ledger, so that `results/CONSENSUS-CON-*.REPORT.md` and the commit
history keep resolving. They are labels, not a sequence: a new check takes the next free number and
no id is ever reused.

**This is not a grading rubric and produces no score.** A check that fails is a question — did the
skill stop asking for this, or did the model have a bad day? One plan cannot tell you. Two plans in
a row can.

**These are rules about the skill, not about recipes.** They carry over to any scenario. What is
specific to `recipe-app` lives in two files that a review opens at different moments:
`recipe-app/EVALUATION-BRIEF.md` before the checks, `recipe-app/REFERENCE-PLAN.md` strictly after.

## The loop

Half an hour, one provider call.

1. Generate one plan from `recipe-app/sources/` alone, in a fresh session with no other context.
   The prompt is in `PROMPTS.md` § `GENERATE PLAN`; it must activate the skill explicitly, or the
   candidate is born without it.
2. `make validate PLAN=<plan.md>` — structural, deterministic, free. `PLAN` is a bare filename
   under `recipe-app/results/`. If it is red, stop and fix before reading.
3. Read the plan against `recipe-app/EVALUATION-BRIEF.md`, opening `sources/` only to verify a
   citation. **The brief is the authority**, not the sources: it decides which conflicts exist,
   which alternatives are accepted, which uncertainties are material. Skipping this step is how the
   ledger used to produce false positives.
4. Walk the checks below.
5. **Only now** open `recipe-app/REFERENCE-PLAN.md` and compare. Forming your verdict first is what
   keeps the reference a memory aid instead of a diff target — the order is the whole discipline,
   and it is one rule rather than four authority classes. Differences in titles, numbering, theme
   count, ordering, and example detail are all allowed; on each one ask which of the two has the
   better reason. What you are hunting is what you forgot, not what you did differently.

Run it after a change you believe is substantive. Not after every commit — a net you skip is worse
than a net you sized honestly.

**If a check fails against a rule the skill no longer states, the defect is in the check.** Rewrite
it or delete it. The list describes the skill, it does not govern it.

## Horizon and admission

- **R-004** — No `NOW` slice delivers a behaviour the sources do not request.
- **R-013** — Every `LATER` entry states a `Promotion trigger`. *Automatable; `validate_plan.py`
  today checks only that the section carries a list.*
- **R-014** — Every `OUT-OF-SCOPE` entry states an exclusion rationale. *Same.*

## Undecided choices and source conflicts

- **R-002** — Every choice the plan declares open names the `NOW` slices it blocks, in whatever
  section it declares it. *Automatable: every entry cites at least one existing slice number.*
- **R-003** — No `NOW` slice depends on an external choice — provider, model, service, adapter —
  that is not made by a citable source, made among the alternatives the brief declares acceptable,
  or declared open together with the slice it blocks. A qualifying adjective (`cheap`,
  `multilingual`, `managed`) is not a choice.
- **R-010** — No `Includes` or `Verification` bullet asserts, in non-conditional form, one side of
  an unresolved choice. Unresolved covers the brief's `Known conflicts`, any conflict demonstrable
  by citing two sources in disagreement, and — inside the slices that choice blocks — any choice the
  plan does not resolve by citing a selecting source. Declaring it under open questions or assigning
  a spike does not resolve it.
  ⚠ **Watch the opposite failure.** This rule was written from a violation on one model only. The
  risk is not assertive wording coming back but plans that defer everything to a pending decision
  and publish nothing verifiable. If that appears, the defect is in R-010.
- **R-018** — Every behaviour two sources describe incompatibly appears among the plan's open
  entries with the `NOW` slices it blocks, whether or not either source names a provider, model,
  service, or adapter. The brief's `Known conflicts` lists only some of the cases this covers.
  ⚠ **Watch the opposite failure.** A plan that lists non-conflicts among its open entries to
  satisfy the rule, deferring slices nothing leaves open. Never yet tested on a real cycle.

## Ordering, identity, audience

- **R-001** — The plan places identity after the differentiator.
  ⚠ **Has failed.** CON-6, `CX`, unanimously: identity at slice 2, differentiator at 3–4.
- **R-009** — No `Outcome` of a `NOW` slice preceding identity promises a real user. Every slice
  before identity that delivers a behaviour names its own audience — developer or tester, on the
  declared non-public environment.
- **R-017** — If more than two `NOW` slices deliver behaviour to an end user before identity,
  `Ordering criteria` justifies the residual deferral once, naming the evidence that requires it.
- **R-012** — `Cross-functional concerns` declares the single seam from which the current scope
  resolves.

## Themes and their first validation

- **R-008** — Every theme's `First validation` points to a slice whose `Outcome` covers the theme's
  entire desired outcome. *Reference existence is automatable; outcome coverage is reading.*
  ⚠ **Has failed.** CON-5, `CX`, on partial coverage.
- **R-011** — Every `Themes` row has its `First validation` resolve to a `NOW` slice not annotated
  `*(Enabler: …)*`, unless its `Desired outcome` cell carries `*(Developer outcome)*`. *Automatable
  — both facts are published by the plan.*
  ⚠ **Watch the opposite failure.** The marker is declarative and the validator cannot know whether
  the outcome really is a developer's. The failure is the marker attached to get past the check, not
  its absence.

## Pipelines, adapters, theme continuity

- **R-005** — If a `NOW` slice names a failure mode in its own `Verification` and another `NOW`
  slice is its remedy, no slice of a different theme sits between the two. *Theme interposition is
  automatable on the `*(Theme: X)*` annotation; the failure→remedy coupling is reading.*
- **R-006** — A pipeline or adapter shared by several paths is opened in the `Includes` of a single
  `NOW` slice. *Partly automatable: the same name in two slices is structural, recognising that two
  names denote one adapter is reading.*
- **R-016** — The `NOW` slice that opens a shared pipeline or adapter follows every `NOW` slice that
  feeds it input — except when it validates controlled inputs traversing the production computation
  and the brief admits early validation (`Accepted alternatives`, last entry).
  ⚠ **Has failed.** CON-6, `CX`: the LLM extraction adapter opened at slice 7, before the paste path
  feeding it at slice 8.
- **R-007** — No `Enabler` slice validates uncertainties across more than one subsystem: its
  `Verification` cannot fail for causes belonging to different `Subsystem`s in the brief's
  `Material uncertainties`. Several entries of the same subsystem are one uncertainty, even when the
  answer invalidates the choice being verified. An `Enabler` spanning two subsystems is more than
  one cold implementation session can carry.

## Open — not checks

Do not run these. They are decisions the retired program left owing, and until each is decided a
failure against it looks like a skill regression without being one.

- **R-015 — reuse declaration.** *«A `NOW` slice that reuses a pipeline or adapter opened by an
  earlier slice declares it as reuse.»* Regressed unanimously in CON-6, exactly as predicted: **no
  clause of `SKILL.md` states this**. It was added to the ledger after CON-5 *because* a model
  failed to do it — a rule invented backwards from one observation. Either the skill acquires the
  clause, or the check dies. It is currently outside the list.
- **Three anchors with no clause.** `R-001`'s, and the `9aa2586` component that `R-005` and `R-006`
  carried. Recorded in `support/CLAUSE-ROW-MAP.md` § *Unresolved anchors*. Same decision, same
  owner: the scope reduction of the skill.
- **Two agreed improvements that never reached the skill** — semantic checks in `validate_plan.py`
  (interrupted themes, duplicated adapters, open questions ignored by the slices), and versioned
  evaluation sets for quality claims. Both raised by two independent reviews in CON-4. The first
  would move R-002, R-005 and R-006 from reading to validator, which is the only direction in which
  this list gets cheaper. `REGRESSION-LEDGER.md` § *Agreed improvements that never reached the
  skill* has the detail.
