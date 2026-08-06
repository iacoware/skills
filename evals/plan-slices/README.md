# `plan-slices` evaluation

Two tools have lived in this directory. Only one is in service.

- **Consensus cycle — active.** Decides whether a change to `skills/plan-slices/SKILL.md` made the
  skill worse. Entry point: `CONSENSUS-WORKFLOW.md`, which is self-contained.
- **Grading system — abandoned on 2026-08-06.** Not suspended, not behind a gate. The code and its
  documents stay in git and are recoverable from history; they are not maintained.

## Language

English is the project language as of 2026-08-06. **Every new artifact is born in English**:
prompts, templates, validators, reports, ledger rows, commit messages.

Human documents still written in Italian — `CONSENSUS-WORKFLOW.md`, `CONSENSUS-WORKFLOW-PLAN.md`,
`NOTES.md`, `PROMPTS.md` — are a backlog, not an exception. Phase 0b converts them and blocks
nothing. `REGRESSION-LEDGER.md` is already migrated.

**Two exclusions are permanent** and do not expire with Phase 0b:

- **`recipe-app/sources/`.** Converting them is a **new scenario**, not a translation. It would
  invalidate the five plans generated from them, the ledger rows measured over those plans, and the
  citations in `EVALUATION-BRIEF.md`, which point at Italian section titles (`sources/goal.md`,
  “Vincoli e scala”).
- **Historical artifacts** — `PLAN-*`, `*.IMPROVEMENT.md`, `*.REVIEW.md` and the reports already
  produced. They are the record of what was generated. Translating them falsifies it.

Already English, nothing to do: `EVALUATION-BRIEF.md` — the Italian section titles it carries are
**pointers into the sources**, not prose to translate, and translating them would break the pointer
— and `skills/plan-slices/SKILL.md`.

Textual quotations from historical artifacts stay in Italian inside quotation marks, wherever they
appear, because they are evidence.

## Active

| Path | Role |
|---|---|
| `CONSENSUS-WORKFLOW.md` | The tool and why it exists. Read this first. |
| `CONSENSUS-WORKFLOW-PLAN.md` | The work left to do, one cold session per phase. Opens with a routing table. |
| `CONSENSUS-WORKFLOW-PLAN-CLOSED.md` | Closed phases, kept for *why* a decision was taken. No session needs it to work. |
| `REGRESSION-LEDGER.md` | Falsifiable claims implied by applied changes, with state `not refuted ×k`. |
| `prompts/` | Normative source of the four phase prompts. Created in Phase 1b-i. |
| `assets/improvement-template.md` | The conformance contract an `IMPROVEMENT` entry fills. Phase 1a. |
| `support/` | `CLAUSE-ROW-MAP.md` with its extracted `clause-row-map.tsv`, and `AGENT-PLAN-MAP.md`. **Excluded from every payload.** |
| `scripts/consensus/` | Cycle code. `validate_improvement.py` and `extract_clause_map.py` exist; provider invocation and orchestrator are Phases 3 and 5. |
| `NOTES.md` | Observations from running the evals, each self-contained. |
| `PROMPTS.md` | Human scratchpad, no normative value once `prompts/` exists. |
| `recipe-app/sources/` | The only inputs a candidate plan is generated from. |
| `recipe-app/EVALUATION-BRIEF.md` | Authority classes, hard constraints, accepted alternatives, known conflicts. |
| `recipe-app/results/PLAN-*.md` | Candidate plans and their `IMPROVEMENT` / `REVIEW` artifacts. |
| `recipe-app/results/CONSENSUS-CON-*.REPORT.md` | Cycle reports. |
| `../../skills/plan-slices/scripts/validate_plan.py` | Structural validator. Lives in the skill, not here. |
| `../AGENTS.md` | Authorization rules for provider runs. |
| `make validate PLAN=…` | Structural check of a candidate plan. |
| `make validate-improvement IMPROVEMENT=…` | The conformance gate, entry by entry. |
| `make clause-map` | Regenerate `support/clause-row-map.tsv` from `CLAUSE-ROW-MAP.md`. |

`prompts/` does not exist yet: Phase 1b creates it. `assets/report-template.md` is Phase 1c.

`recipe-app/README.md` and `recipe-app/EVAL-NOTES.md` predate the split and still describe grading
artifacts. They are scenario documentation, not grading documents, and are corrected when the
scenario changes.

## Archived

Kept for history, not maintained. Nothing in the active list depends on any of it.

| Path | Role |
|---|---|
| `GRADING-IMPROVEMENTS-PLAN.md`, `GRADING-IMPROVEMENTS.md`, `GRADING-EVAL-WORKFLOW.md` | The abandoned tool's documents. Each opens with an abandonment banner. |
| `grader-rubric.json`, `grader-rubric.v3.json` | Rubrics v1 and v3. |
| `fixtures/` | Labeled calibration fixtures and manifests. |
| `recipe-app/results/calibration-legacy/`, `calibration-v2/`, `calibration-v3/` | Immutable grading artifacts and calibration reports. |
| `scripts/*.py` at the top level of `scripts/` | Grading orchestrator, graders, scoring, adjudication, and their tests. |
| `make grade`, `make compare`, `make calibrate`, `make calibrate-critical`, `make calibrate-critical-report` | Grading targets. |

`make test` still runs the grading tests and is expected to stay green: archived means unmaintained,
not deleted.
