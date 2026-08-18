# Manual review of a generated plan

What to read on a plan produced by `skills/plan-slices/SKILL.md`, to notice that a change to the
skill broke something it used to get right.

**This is not a grading rubric and produces no score.** A check that fails is a question — did the
skill stop asking for this, or did the model have a bad day? One plan cannot tell you. Two plans in
a row can.

**These are rules about the skill, not about recipes.** They carry over to any scenario. What is
specific to `recipe-app` lives in files a review opens at different moments: `EVALUATION-BRIEF.md`
before the checks, `REFERENCE-PLAN.md` and its rationale strictly after.

**A check is admitted when `SKILL.md` states the clause it guards** — not when a model was once
observed failing. Most of the list was distilled from a ledger of falsifiable claims that retired
on 2026-08-11 with the consensus cycle; `POST-MORTEM-EVALS.md` says where the ledger is and which
of its rows are debts rather than checks. **Ids are inherited** from it, so that
`results/CONSENSUS-CON-*.REPORT.md` and the commit history keep resolving. They are labels, not a
sequence: a new check takes the next free number and no id is ever reused.

**If a check fails against a rule the skill no longer states, the defect is in the check.** Rewrite
it or delete it. The list describes the skill, it does not govern it.

## The loop

Half an hour, one provider call. Run it after a change you believe is substantive — not after every
commit, since a net you skip is worse than a net you sized honestly.

1. Generate one plan from `recipe-app/sources/` alone, in a fresh session with no other context.

   The skill is **invoked explicitly** — `/plan-slices` on Claude Code, `$plan-slices` on Codex.
   Neither harness activates it on its own: `skills/plan-slices/agents/openai.yaml` sets
   `allow_implicit_invocation: false` and the skill's frontmatter sets
   `disable-model-invocation: true`. Drop the prefix and the candidate is born without the skill,
   which means you are reviewing the model instead.

   **Claude Code**, one message, replacing `<N>`:

   ```
   /plan-slices Read the markdown documents in @evals/plan-slices/recipe-app/sources/, starting from @evals/plan-slices/recipe-app/sources/goal.md, and produce a high-level delivery plan cut into slices. Write it to evals/plan-slices/recipe-app/results/PLAN-CC-<N>.md. Read nothing else in this repository, in this session or in any session you delegate to: the sources are the only input, and the existing plans under results/ are off limits.
   ```

   **Codex**, one message:

   ```
   $plan-slices Read the markdown documents in evals/plan-slices/recipe-app/sources/, starting from evals/plan-slices/recipe-app/sources/goal.md, and produce a high-level delivery plan cut into slices. Write it to evals/plan-slices/recipe-app/results/PLAN-CX-<N>.md. Read nothing else in this repository, in this session or in any session you delegate to: the sources are the only input, and the existing plans under results/ are off limits.
   ```

   The two differ only in the `@` prefixes, Claude Code's file-reference syntax, which has no Codex
   equivalent. Model and effort are set in the session, never in the prompt: check what the session
   actually says before sending, and write down what it said rather than what you intended.
2. `make validate PLAN=<path>` from the repository root — structural, deterministic, free. `PLAN`
   is a path, not a bare filename: `make validate PLAN=evals/plan-slices/recipe-app/results/PLAN-CC-CON-7.md`.
   If it is red, stop and fix before reading.
3. Read the plan against `recipe-app/EVALUATION-BRIEF.md`, opening `sources/` only to verify a
   citation. **The brief is the authority**, not the sources: it decides which conflicts exist,
   which alternatives are accepted, which uncertainties are material. Skipping this step is how the
   ledger used to produce false positives.
4. Walk the checks below.
5. **Only now** open `recipe-app/REFERENCE-PLAN.md`, and its rationale, and compare. Forming your
   verdict first is what keeps the reference a memory aid instead of a diff target — the order is
   the whole discipline. What you are hunting is what you forgot, not what you did differently.

   The reference was hand-written from the sources before any candidate existed, and is frozen: it
   is rewritten only when the sources change, never because a candidate convinced. How binding each
   part of it is:

   - Where reference and `sources/` diverge, the defect is in the reference.
   - Titles, numbering, theme count, order and worked detail may all differ. On each difference, ask
     which of the two has the better reason — the rationale file holds the reference's.
   - Each `Verification` bullet illustrates how a slice could be demonstrated; it is one way, not
     the only one. The same holds for the operational detail of `Cross-functional concerns`, whose
     six entries are owed but not their wording, and for `Decision checkpoints`, which are advice
     rather than an exact precedence.
   - A source may support a `LATER` or `OUT-OF-SCOPE` classification other than the reference's.

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
  an unresolved choice. Unresolved covers the conflicts under the brief's *What it must leave open*,
  any conflict demonstrable by citing two sources in disagreement, and — inside the slices that
  choice blocks — any choice the plan does not resolve by citing a selecting source. Declaring it
  under open questions or assigning a spike does not resolve it.
  ⚠ **Watch the opposite failure.** This rule was written from a violation on one model only. The
  risk is not assertive wording coming back but plans that defer everything to a pending decision
  and publish nothing verifiable. If that appears, the defect is in R-010.
- **R-018** — Every behaviour two sources describe incompatibly appears among the plan's open
  entries with the `NOW` slices it blocks, whether or not either source names a provider, model,
  service, or adapter. The brief lists only some of the cases this covers.
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
  feeds it input — except when it validates controlled inputs traversing the production computation,
  which the brief admits under *Where it may differ*.
  ⚠ **Has failed.** CON-6, `CX`: the LLM extraction adapter opened at slice 7, before the paste path
  feeding it at slice 8.
- **R-007** — No `Enabler` slice validates uncertainties across more than one subsystem: its
  `Verification` cannot fail for causes belonging to different `Subsystem`s in the brief's
  uncertainty table. Several entries of the same subsystem are one uncertainty, even when the
  answer invalidates the choice being verified. An `Enabler` spanning two subsystems is more than
  one cold implementation session can carry.

## The two ends of NOW

- **R-020** — The greenfield prerequisites are two separate slices: repository and CI with no
  provisioning or deploy, then a walking skeleton that reaches the datastore at runtime through the
  real driver and applies one non-domain migration, carrying no domain entity, authentication, or
  tenancy. One slice doing both, or a skeleton that answers without touching the datastore, are the
  `Oversized` and `Hollow walking skeleton` anti-patterns.
- **R-019** — When `NOW` delivers to end users, its last slice promotes the release to its intended
  environment and is tagged `*(Release: delivery)*`, carrying only source-backed operational
  readiness. A plan that ends `NOW` without it, or tags it `Enabler`, states instead — explicitly —
  that `NOW` ends at developer validation, and names that audience and environment. *Tag presence is
  automatable; whether the readiness is source-backed is reading.*
