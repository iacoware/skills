# P3 — The validator

**Depends on** P2, and on P1 for the map it has to pass on. **Produces** the only mechanical check in
the project.

Read [`../PLAN.md`](../PLAN.md) first.

## Reads

- the two templates from P2 and the oracle from P1;
- [`../PLAN-INPUTS.md`](../PLAN-INPUTS.md) § *The validator*;
- `skills/plan-slices/scripts/validate_plan.py` — for what a structural check looks like here, not to
  port it.

## Produces

- `skills/roadmap/scripts/validate_roadmap.ts`;
- `skills/roadmap/scripts/validate_roadmap.test.ts`;
- `evals/roadmap/recipe-app/fixtures/` — one minimal mutation of the oracle per check.

## Work

TypeScript run natively: `node <skill-dir>/scripts/validate_roadmap.ts <roadmap-dir>`, the directory
defaulting to `.roadmap`. No build step, no dependencies, type annotations only — no enums, no
namespaces, no parameter properties, explicit `.ts` on relative imports. Node 23.6 and later run it
as is; 22.6 to 23.5 need `--experimental-strip-types`, and P5 states that floor where it states the
command.

Checks:

- section presence and order in `roadmap.md`, list-only sections, the register header and column
  order, the theme table;
- one slice document per register row and one row per document; filename, id and title in agreement;
- slice field presence and order per the template, with `Audience` optional only on `kind: spike`;
- `Depends on` resolves to a row of the same register; no cycle;
- ids monotonic and never recycled across `slices/` and `archive/`;
- no candidate and no exclusion carries an id;
- `kind`, `readiness`, `executor` and `size` hold legal values;
- every `kind: spike` row is named in some row's `Depends on`, or declares on its own row that it
  validates the goal's feasibility.

A failed check exits non-zero. The register count is a **warning** and exits zero: past twenty rows
it says so, below three it says so in the other direction. Exceeding the cap is a signal to the
author, and failing on it would be grading the map instead of checking it.

## Done when

- green on the oracle, red on every fixture;
- every check has a test named after the behaviour it guards, runnable with `node --test`;
- no check requires a judgement about whether a field is filled *well*.
