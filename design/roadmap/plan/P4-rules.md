# P4 — The rules

**Depends on** P1. Drafts alongside P2 and P3, publishes after P2 so it can cite the template.
**Produces** the two reference files that keep `SKILL.md` a router.

Read [`../PLAN.md`](../PLAN.md) first.

## Reads

- [`../ROADMAP-GOAL.md`](../ROADMAP-GOAL.md), [`../CONTEXT.md`](../CONTEXT.md);
- `skills/plan-slices/SKILL.md`, steps 2–4 and its anti-patterns;
- `evals/roadmap/recipe-app/REFERENCE-NOTES.md`.

## Produces

- `skills/roadmap/references/drawing-the-map.md`;
- `skills/roadmap/references/slice-rules.md`.

## Work

`drawing-the-map.md` holds what fires only when a map is drawn against a declared goal: themes with
their split and merge tests, one first validator per theme, hard dependencies, the repository
prerequisite and the walking skeleton with its hollow-skeleton failure, ordering for learning,
breadth before depth, the identity seam, and how `Assumptions` and `Open questions` report on the
input. A redraw loads the same file: what the previous goal leaves behind — archive, id high-water
mark, exclusions, concerns, candidates — enters as input, not as a separate mode.

`slice-rules.md` holds what is true on every operation: what makes a valid slice, the split and merge
tests, verification mapping to the learning target, the spike test — *when the verification is a
measurement rather than a capability, it is a spike* — the dependent requirement for a spike,
readiness, executor, `kind`, `size`, id minting, what a split does to identity, and the anti-patterns
that survive the format change.

## Done when

- every rule traces to a clause of `ROADMAP-GOAL.md`, `CONTEXT.md`, or a `plan-slices` clause the new
  format keeps; a rule with no such source is dropped, and one whose source is intent moves into the
  goal document instead;
- nothing is stated in both files;
- every `plan-slices` clause that does *not* carry over — position numbering, promotion triggers,
  decision checkpoints, the unpublished dependency map, the title tags — is accounted for in P1's
  rationale or abandoned explicitly here;
- no rule asks the validator for a judgement.
