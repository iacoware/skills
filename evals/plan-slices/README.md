# `plan-slices` evaluation

One structural validator and one human reading list, kept to notice that a change to
`skills/plan-slices/SKILL.md` improved one thing while breaking another. The two automated
evaluations that preceded them are retired — see [`POST-MORTEM-EVALS.md`](POST-MORTEM-EVALS.md) for
why, and for how to recover them.

**Audience: a human reviewer, or an agent in a review session.** Never a generation session — the
three documents below are the answer key, which is why they live here and not beside the skill,
where an agent exploring the directory could pick them up.

## What is live

| Path | Role |
|---|---|
| `../../skills/plan-slices/scripts/validate_plan.py` | Structural validator. Deterministic, free, one second. The only real regression test in the project. |
| `make validate PLAN=<path>` | Runs it, from the repository root. `PLAN` is a path. |
| `REVIEW-WORKFLOW.md` | How to run one review: the five steps and the generation prompt. |
| `EVALUATION-RULES.md` | What to look for, as numbered checks. Rules about the skill, portable to any scenario. |
| `recipe-app/sources/` | The only inputs a candidate plan is generated from. |
| `recipe-app/EVALUATION-BRIEF.md` | Facts about those sources: what the plan must contain, where it may differ, what it must leave open, what only looks like a defect. Verifiable, no taste. Read at step 3. |
| `recipe-app/REFERENCE-PLAN.md` | One good answer, hand-written from the sources before any candidate existed. Taste, not verifiable. Read at step 5, never earlier. |
| `recipe-app/REFERENCE-PLAN-RATIONALE.md` | Why each reference slice sits where it sits — the reasoning `SKILL.md` § 5 forbids publishing in a plan. |
| `../AGENTS.md` | Authorization rules for provider runs. Still binding for the one generation call. |

Four jobs, no overlap: a **procedure**, **rules** that hold across scenarios, **facts** about this
scenario's sources, **one worked answer** for this scenario with its reasoning. Add a second
scenario and the rules travel unchanged, the procedure travels with a directory substituted, and
the last two are written anew.

**Why the brief is not enough on its own.** It is the reference plan with the answer removed:
everything mechanically checkable kept, everything requiring judgement dropped. That amputation
existed to give an automated grader an oracle. With no machine judge left, what it removed is the
only artifact carrying the author's own judgement about how this product should be sliced — and the
only defence against the failure mode of pure manual review, the reviewer's sense of "good" drifting
toward whatever the model last produced. A frozen reference costs nothing per run and does not
drift.

## Language

English is the project language since 2026-08-06. Two permanent exclusions: `recipe-app/sources/`,
because converting them is a new scenario rather than a translation, and the historical artifacts
under `recipe-app/results/`, because they are the record of what was generated. `REFERENCE-PLAN.md`
is Italian because `SKILL.md` writes a plan in the user's language and the sources are Italian.
Quotations stay in the original language inside quotation marks, wherever they appear, because they
are evidence.
