# P8 — First runs, fixtures, deprecation

**Depends on** every other phase. **Produces** the first evidence that the skill works, and closes
the plan.

Read [`../PLAN.md`](../PLAN.md) first, and `evals/AGENTS.md`: this is the phase that spends provider
calls, and each one needs explicit authorization before it is sent.

## Reads

`evals/roadmap/REVIEW-WORKFLOW.md`, and then, in its order and no other, the validator's output, the
brief, the rules, and only at the end the oracle.

## Produces

- one generated roadmap under `evals/roadmap/recipe-app/results/`;
- `evals/roadmap/recipe-app/fixtures/` filled — the mid-flight and redrawn starting states the
  scenarios of P7 point at;
- whatever fixes the run forces, each landing in the phase that owns the defect;
- the deprecation of `plan-slices`.

## Work

Run the skill in a fresh session on `evals/roadmap/recipe-app/sources/` alone. Validate, read against
the brief, walk the rules, and only then open the oracle — the order is the whole discipline, since
forming the verdict first is what keeps the oracle a memory aid instead of a diff target.

Fix what the run exposes **in the phase that owns it**, not in `SKILL.md` by default: a rule the
skill applied badly may be a defect in P4, a field nobody could fill may be a defect in P2. One run
is a question, not a verdict.

Then cut the mid-flight and redrawn states out of that output, freeze them under `fixtures/`, and run
scenarios 1 and 3 against them.

Deprecation is the last act and it is minimal: a line in `README.md` marking `plan-slices` superseded
by `roadmap`, and a line in the body of `skills/plan-slices/SKILL.md` saying the same. The frontmatter
is not touched — `name` and `description` decide how an installed skill is invoked, and breaking a
live installation is not what a deprecation notice is for. Nothing is deleted, and `evals/plan-slices/`
keeps working as the yardstick for the first roadmaps.

## Done when

- one run is green on the validator and has been read against the brief and the oracle;
- the three router scenarios reach their stated verdicts, or the divergence is recorded as a finding
  against the phase that owns it;
- `fixtures/` holds the states the scenarios name, and no scenario points at a path that does not
  exist;
- the deprecation is recorded in both places.
