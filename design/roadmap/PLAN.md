# Roadmap skill — implementation plan

How the `roadmap` skill gets built. This document is the register and the common ground: the phases
themselves live one per file under [`plan/`](./plan/), and each is written to be executed in its own
session by someone who has read this page and nothing else of the plan.

[`ROADMAP-GOAL.md`](./ROADMAP-GOAL.md) is the authority on intent, [`CONTEXT.md`](./CONTEXT.md) on
vocabulary, [`WORKFLOWS.md`](./WORKFLOWS.md) illustrates, [`PLAN-INPUTS.md`](./PLAN-INPUTS.md) is the
material this plan consumes. Where this plan and any of those disagree, they win and the disagreement
is a defect here.

## The register

| Phase | Produces | Depends on |
|---|---|---|
| [P1 — The oracle](./plan/P1-oracle.md) | The reference roadmap for `recipe-app`, hand-written from the sources, and its rationale | — |
| [P2 — The format contract](./plan/P2-format-contract.md) | `assets/roadmap-template.md`, `assets/slice-template.md`, read off the oracle | P1 |
| [P3 — The validator](./plan/P3-validator.md) | `scripts/validate_roadmap.ts`, its tests, and one broken fixture per check | P2 |
| [P4 — The rules](./plan/P4-rules.md) | `references/drawing-the-map.md`, `references/slice-rules.md` | P1 |
| [P5 — The router](./plan/P5-router.md) | `SKILL.md` and `agents/openai.yaml` | P2, P3, P4 |
| [P6 — Repository wiring](./plan/P6-repository-wiring.md) | `Makefile` targets, `README.md` row, `CONTEXT-MAP.md` entry | P3, P5 |
| [P7 — The evaluation harness](./plan/P7-evaluation-harness.md) | `evals/roadmap/`: workflow, rules, brief, three router scenarios | P1, P5, P6 |
| [P8 — First runs, fixtures, deprecation](./plan/P8-first-runs.md) | One real run, the frozen fixtures, the `plan-slices` deprecation | all |

P4 may be drafted alongside P2 and P3 and published after P2, which is the only concurrency the order
allows. Everything else is a chain.

## Premises

Settled in the planning session. They are premises, not choices to reopen inside a phase.

- **Oracle first.** The reference roadmap is written before the template exists, and the template is
  derived from it. Format born from a worked example, not from a specification of a format.
- **The oracle covers one state**, the initial map. Mid-flight and redrawn states are not
  hand-written; the fixtures that need them are cut out of a real run in P8.
- **Payload layout:** router, two references, two assets. `SKILL.md` stays a router; the roadmap
  rules and the slice rules each get their own reference file.
- **Validator in TypeScript, run natively.** `node scripts/validate_roadmap.ts <dir>`, no build step
  and no dependencies. Type-annotation-only TypeScript: no enums, no namespaces, no parameter
  properties, explicit `.ts` on relative imports. Node 23.6 and later run it as is; 22.6 to 23.5 need
  `--experimental-strip-types`.
- **Tests with `node:test`**, beside the script, where `plan-slices` already keeps its Python tests.
- **Verification during construction is structural** — the validator and a reading against the
  oracle. Real runs of the skill arrive only in P8, one provider call each, authorised as
  [`evals/AGENTS.md`](../../evals/AGENTS.md) requires.
- **`plan-slices` is deprecated, not removed.** Its skill, validator, tests and evals stay in the
  repository and installable; P8 records the deprecation and nothing else.
- **English**, as `plan-slices` and the design documents. `README.md`, `CONTEXT-MAP.md` and
  `CONTEXT.md` stay as they are; the `recipe-app` sources carry over unconverted, for the reason
  [`evals/plan-slices/README.md`](../../evals/plan-slices/README.md) already gives. The reference
  roadmap itself is the other exception, in Italian as `REFERENCE-PLAN.md` is and for the same
  reason: the skill writes in the author's language and these sources are Italian. Its rationale
  stays English, as `REFERENCE-PLAN-RATIONALE.md` does, and field names, column names and state
  values are English everywhere because they are format rather than prose.

## Rules every phase obeys

- **A phase that discovers a rule the goal document does not state stops**, amends
  `ROADMAP-GOAL.md` first, and only then continues. That is the discipline that kept the design
  documents coherent so far.
- **A defect lands in the phase that owns it.** A rule applied badly is a defect in P4, a field
  nobody can fill is a defect in P2. Fixing it in `SKILL.md` because that is where it showed up is
  how a router grows back into `plan-slices`.
- **Nothing is deleted from `plan-slices` before P8**, and P8 deletes nothing either. It stays the
  yardstick the first roadmaps are read against.
- **The answer key stays out of generation sessions.** The oracle, its rationale and the brief live
  under `evals/roadmap/`, never beside the skill, for the reason
  `evals/plan-slices/README.md` states.

## What gets built

```
skills/roadmap/
  SKILL.md                          router: situation, branch, five operations, handover
  references/drawing-the-map.md     roadmap rules, loaded on the drawing branch only
  references/slice-rules.md         slice and spike rules, valid on every operation
  assets/roadmap-template.md        .roadmap/roadmap.md skeleton
  assets/slice-template.md          .roadmap/slices/S<id>-<slug>.md skeleton
  scripts/validate_roadmap.ts       structural and referential validator
  scripts/validate_roadmap.test.ts  node:test suite
  agents/openai.yaml                allow_implicit_invocation: false

evals/roadmap/
  README.md                         what is live, and for whom
  REVIEW-WORKFLOW.md                the five steps and the generation prompts
  EVALUATION-RULES.md               checks about the skill, portable across scenarios
  recipe-app/
    sources/                        copied verbatim from evals/plan-slices/recipe-app/sources/
    EVALUATION-BRIEF.md             facts about those sources, for a roadmap rather than a plan
    reference-roadmap/              the oracle: roadmap.md + slices/
    REFERENCE-ROADMAP-RATIONALE.md  why each row sits where it sits
    fixtures/                       starting states for the router scenarios, frozen in P8
    results/                        generated output, never read by a generation session
```

The skill is invoked explicitly, as `plan-slices` is: `disable-model-invocation: true` in the
frontmatter and `allow_implicit_invocation: false` in `agents/openai.yaml`. A roadmap redrawn because
an agent thought it was being helpful is the failure those settings exist to prevent.

## Risks

- **The oracle and the template drift.** P2 derives one from the other, and nothing afterwards keeps
  them in step. The validator is the only mechanical link: it runs on the oracle in P3 and again in
  P8, and a template change that does not keep it green is a change that broke the oracle.
- **`SKILL.md` grows back into `plan-slices`.** The rules have somewhere else to live now; the router
  will still attract them. The length check in P5 is crude on purpose, because it is checkable.
- **The Node floor.** Machines below 22.6 cannot run the validator, and the skill says so where it
  says how to run it. If that bites, the fallback is emitting JavaScript into the payload, which
  costs a build step and a second artifact to keep in sync.
- **One run is not a signal.** As `evals/plan-slices/EVALUATION-RULES.md` says, a failed check is a
  question, not a verdict. P8 fixes what it can trace to a clause and records the rest.
