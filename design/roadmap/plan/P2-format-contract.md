# P2 — The format contract

**Depends on** P1. **Produces** the two templates the skill writes against and the validator checks.

Read [`../PLAN.md`](../PLAN.md) first.

## Reads

- `evals/roadmap/recipe-app/reference-roadmap/` and its rationale;
- [`../ROADMAP-GOAL.md`](../ROADMAP-GOAL.md) § *Decisions taken*;
- `skills/plan-slices/assets/plan-template.md`, for the five cross-functional entries and for the
  placeholder style.

## Produces

- `skills/roadmap/assets/roadmap-template.md`;
- `skills/roadmap/assets/slice-template.md`.

## Work

The templates are read off the oracle, not invented: section names and order, the register header and
column order, the slice fields and their order, the file naming rule `S<id>-<slug>.md`, and
placeholder text that says what each part is for rather than showing a filled example.

Two files because the two artifacts are edited at different moments and by different operations: the
overview changes on almost every session, a slice document only when its own row is touched.

Where template and oracle disagree, fix whichever has the worse reason — and if the better reason is
not sanctioned by `ROADMAP-GOAL.md`, amend the goal document before the template.

## Done when

- the oracle can be restated as a strict instance of the two templates with nothing lost and nothing
  invented;
- `roadmap.md` carries, in this order: the goal, sources, current state, ordering criteria, the theme
  table, `Assumptions`, `Open questions`, `Cross-functional concerns`, then `NOW`, `LATER`,
  `OUT-OF-SCOPE`;
- the five cross-functional entries of the `plan-slices` template survive unchanged;
- the slice template carries `Requested by`, `Spec`, `Tickets`, `ADRs`, `Audience`, `Includes`,
  `Verification`, `Learning target`, `Excludes`, `Open questions`, and says which of them a spike
  leaves empty;
- no register column is repeated inside a slice document.
