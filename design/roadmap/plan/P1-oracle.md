# P1 — The oracle

**Depends on** nothing. **Produces** the first artifact anything else is derived from.

Read [`../PLAN.md`](../PLAN.md) first: it carries the premises, the target layout and the rules every
phase obeys.

## Reads

- [`../ROADMAP-GOAL.md`](../ROADMAP-GOAL.md), [`../CONTEXT.md`](../CONTEXT.md),
  [`../WORKFLOWS.md`](../WORKFLOWS.md);
- `evals/plan-slices/recipe-app/sources/` — `goal.md`, `concepts.md`, `arch-choices.md`,
  `tech-choices.md`.

Never `evals/plan-slices/recipe-app/REFERENCE-PLAN.md`. It is `plan-slices` output, and reading it
imports its slicing wholesale instead of cutting the map from the sources.

## Produces

- `evals/roadmap/recipe-app/sources/` — the four documents copied verbatim, not converted;
- `evals/roadmap/recipe-app/reference-roadmap/` — `roadmap.md` and one document per row under
  `slices/`;
- `evals/roadmap/recipe-app/REFERENCE-NOTES.md`.

## Work

Write the map as it stands the moment it is first drawn against the MVP goal: nothing delivered,
`archive/` empty, ids starting at `S0`. Hand-written, from the sources, before any template exists —
the template is read off this in P2, so a column invented here is a column the format will carry.

The register's columns are decided here, and each one has to survive the question the goal document
sets: is it used to *compare rows and decide what comes first*? If it is only used while reasoning
inside one row, it belongs to that row's document.

The rationale is the other half. It holds what the published roadmap deliberately does not carry: why
each row is a row, why it sits where it sits, which split or merge test was applied, and which
`plan-slices` habit was dropped on purpose.

## Done when

- every register column and every slice field carries content a reader would use, and each traces to
  a decision in `ROADMAP-GOAL.md`; a field nobody re-reads is deleted, not filled;
- the map exercises the states the format has to survive: at least one `kind: spike` with its
  dependent, at least one `needs-decision` and one `needs-info`, at least one `mixed` executor, at
  least one `Depends on` edge, `Assumptions` and `Open questions` both non-empty with every line
  traced to a theme or an id;
- `NOW` sits inside the cap, every theme has its first validator among the rows, and the repository
  prerequisite and the walking skeleton are separate rows;
- no dates, estimates, percentages, promotion triggers or decision checkpoints appear anywhere;
- the rationale answers, for every row, why it is a row and why it is there.
