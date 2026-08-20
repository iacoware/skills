# Roadmap skill — inputs to the implementation plan

Material that belongs to *building* the `roadmap` skill rather than to deciding what it is for. It
accumulates here as it comes up, and the plan session consumes it.

[`ROADMAP-GOAL.md`](./ROADMAP-GOAL.md) is the authority on intent and
[`CONTEXT.md`](./CONTEXT.md) on vocabulary; nothing here overrides either, and a rule that turns out
to be about intent moves back there.

## Where things live

- `design/roadmap/` — this document set: the goal, the vocabulary, the worked examples, these notes.
  Already applied.
- The skill folder — `SKILL.md` as the router, `assets/roadmap-template.md`,
  `scripts/validate_roadmap.py`, and the roadmap rules as a reference file the drawing branch loads
  on its own. One folder, because `skills add` copies one at a time.
- `evals/roadmap/` — mirrors the structure `evals/plan-slices/` already has: a scenario directory
  with `sources/` and `results/`, an evaluation brief, the rules, and the review workflow.

## The validator

Grows from checking one file to checking a graph:

- every register row resolves to a slice document, and every slice document back to a row;
- every `Depends on` resolves to a row;
- no id recycled or non-monotonic across `slices/` and `archive/`;
- no candidate and no exclusion carries an id;
- `readiness` and `executor` hold legal values.

It counts the register and warns past the cap without failing — exceeding it is a signal to the
author, and failing on it would be grading the map instead of checking it. It stays a script, invoked
automatically at the end of a session and callable by hand; a skill whose body is "run this script"
adds surface and nothing else.

## Evals

The `recipe-app` sources carry over unchanged — they are input, not `plan-slices` output — and the
three sessions in [`WORKFLOWS.md`](./WORKFLOWS.md) are what the scenarios are derived from.

Two scenarios exist specifically for router misfires, the two directions in which it can go wrong:
the theme ceremony fired on a routine session, and a session spent re-truing a map whose goal had
changed under it. Neither is expensive — every branch ends in a proposed block of changes and one
confirmation, so a wrong turn costs a proposal, not a record — which is why they are eval scenarios
and not a reason for a second skill.

## Reviewing the skill itself

Manual, half an hour after a change believed substantive, in the shape already written down for
`plan-slices` in [`evals/plan-slices/REVIEW-WORKFLOW.md`](../../evals/plan-slices/REVIEW-WORKFLOW.md):
generate, validate, read against the brief, walk the rules, and only then open the reference. Its
roadmap counterpart lands under `evals/roadmap/`, beside the scenarios.

## Coexistence with `plan-slices`

`plan-slices` keeps its own template, validator, tests and the 33 payload files under
`evals/plan-slices/recipe-app/`. The new skill is built beside it and it is retired once the new one
stands. Until the retirement lands, `slice` unqualified means the roadmap unit, and the `plan-slices`
unit is a **plan slice**.
