# `plan-slices` evaluation — closed

Two automated evaluation systems were built here between 2026-07 and 2026-08. **Both are retired.**
The goal they served — noticing that a change to `skills/plan-slices/SKILL.md` improved one thing
while breaking another — is now met by a structural validator and a human reading list.

- **Grading system** — abandoned 2026-08-06. A rubric, calibrated graders, adjudication between two
  providers, immutable artifacts in three versions.
- **Consensus cycle** — abandoned 2026-08-11. Two models, four blind phases (`improve`, `review`,
  `verdetto`, `recidiva`), a conformance gate, and a ledger of falsifiable claims.

**Everything they were built from was deleted on 2026-08-12, and every byte of it is recoverable.**
The `evals-final` tag points at the last commit where the apparatus was whole — see *Recovering the
apparatus*.

## Why

Not because the idea was wrong. Because the measured cost of running it never fell, and the reason
it never fell is structural rather than incidental.

**The numbers, at closure.** The apparatus was 4.872 lines of Python and 18.927 lines of Markdown
across 108 files, against the 421 lines of `SKILL.md` and 309 of `validate_plan.py` it existed to
protect — roughly 25× the artifact under measurement. Between 2026-08-01 and closure, `evals/` took
131 commits and the skill took 15.

**CON-6, the only complete consensus cycle.** Eleven provider calls. Four tool defects found and
fixed *during* the cycle — two in the payload projection, one in the conformance validator, one in a
prompt. One entry applied to the skill. Four rows out of seventeen left undecided because the two
`verdetto` instruments disagreed on how to read them.

The consensus plan had written an abandonment threshold, to be evaluated at CON-8. Its
first condition was *procedure maintenance has not fallen below one skill change per cycle*. CON-6
came in at four tool fixes against one applied change. The condition had already failed; CON-7 and
CON-8 would have cost eighteen more calls to confirm it.

**The structural reason, which matters more than the arithmetic.** The regression ledger stated its
own founding rule: *claims quantify over a generated plan, not over the text of the skill*.
Everything expensive descends from there — re-anchoring, absorption, the `Absorbs` column, the
unresolved anchors, the whole clause→row map. It means **every edit to the skill costs maintenance
to the measuring apparatus**, and the cost grows with the size of the skill. The measurement was
coupled to the artefact at the worst available joint: not to the text, which is stable and
diffable, but to the behaviour of a non-deterministic generator, judged by a second
non-deterministic generator.

Reducing the scope of the skill attacks the same cause: less surface to regress, and a manual net
becomes sufficient rather than a consolation.

## What is live

| Path | Role |
|---|---|
| `../../skills/plan-slices/scripts/validate_plan.py` | Structural validator. Deterministic, free, one second. The only real regression test in the project. |
| `make validate PLAN=<path>` | Runs it, from the repository root. `PLAN` is a path. |
| `MANUAL-REVIEW.md` | The loop, the generation prompt, seventeen checks distilled from the retired ledger, and what stays open. Rules about the skill, portable to any scenario. |
| `recipe-app/sources/` | The only inputs a candidate plan is generated from. |
| `recipe-app/EVALUATION-BRIEF.md` | Facts about the sources: what they require, what they leave open, where they disagree, and which differences are *not* disagreements. Verifiable, no taste. |
| `recipe-app/REFERENCE-PLAN.md` | One good answer, hand-written from the sources before any candidate existed. Taste, not verifiable. Restored 2026-08-11. |
| `../AGENTS.md` | Authorization rules for provider runs. Still binding for the one generation call. |

Three documents, three jobs, no overlap: **rules** that hold across scenarios, **facts** about this
scenario's sources, **one worked answer** for this scenario. Add a second scenario and only the
first travels.

**The reference plan is the reason the brief is not enough.** `EVALUATION-BRIEF.md` was created by
`6476f32` — the commit calls it a *blind* brief — precisely to give an automated grader an oracle
that withheld the answer. It is the reference plan with the answer removed: everything mechanically
checkable kept, everything requiring judgement dropped. With no machine judge left, that amputation
has no purpose, and what it removed is the only artifact in the repository carrying the author's own
judgement about how this product should be sliced. It is also the only defence against the failure
mode of pure manual review: the reviewer's sense of "good" drifting toward whatever the model last
produced. A frozen reference costs nothing per run and does not drift.

**None of these three may enter a generation session.** They are the answer key — which is why the
checklist lives here and not beside the skill, where an agent exploring the directory could pick it
up.

## Recovering the apparatus

It was deleted rather than archived, because a file that looks operational and is not costs more
than it saves — the same reason `recipe-app/README.md` and `recipe-app/EVAL-NOTES.md` went earlier,
being a path index and a note on grader inputs that both described a layout no longer there. An
index that lies is worse than no index. This file is the index now.

Everything is reachable by name through the **`evals-final`** tag, on `origin` and local, pointing
at `2abb8ab`, the last commit where the apparatus was whole:

```
git show evals-final:evals/plan-slices/REGRESSION-LEDGER.md
git ls-tree -r --name-only evals-final evals/plan-slices/
```

| What lived at | Was |
|---|---|
| `CONSENSUS-WORKFLOW.md`, `CONSENSUS-WORKFLOW-PLAN*.md`, `workflow/` | The consensus tool and its plan. `workflow/EVIDENCE.md` is the honest record of what the cycle actually measured. |
| `REGRESSION-LEDGER.md` | 18 rows with counters, provenance and absorption history. `MANUAL-REVIEW.md` is its distillation; the ledger keeps the *why* of each row. |
| `prompts/` | The four blind phase prompts — `improve`, `review`, `verdict`, `recidiva`. 498 lines of allowlists, filled contracts and self-check criteria. |
| `assets/`, `support/`, `scripts/consensus/` | Conformance template, clause→row map and its *Unresolved anchors*, `validate_improvement.py`. |
| `recipe-app/payloads/` | The CON-6 payload projections the four prompts read. |
| `GRADING-*.md`, `grader-rubric*.json`, `fixtures/`, `scripts/*.py`, `recipe-app/results/calibration-*/` | The grading system in full. |
| `PROMPTS.md`, `NOTES.md` | Consensus scratchpads. The generation prompt one of them held is now inlined in `MANUAL-REVIEW.md` step 1, which is the only part of either that was live. |
| `Makefile` targets `grade`, `compare`, `calibrate*`, `validate-improvement`, `clause-map` | Their entry points. |

**The cycle reports under `recipe-app/results/` keep their dangling citations, deliberately.** The
three `CONSENSUS-CON-*` files cite `support/`, `workflow/` and ledger rows heavily, and every one of
those paths is now gone. They are the record of a cycle as it ran: rewriting their references would
falsify what the cycle actually read. Do not tidy them — resolve them against the tag instead.

## What would justify reopening

Left observable on purpose, so that "closed" stays a decision instead of becoming a habit.

**The manual net leaks twice.** If a regression reaches a commit and is only noticed two changes
later — and it happens a second time — then reading is no longer catching what it was kept to catch,
and the answer is either a cheaper automated check or a smaller skill. In that order: the two
agreed improvements listed at the end of `MANUAL-REVIEW.md` move three checks from reading to the
validator, and cost nothing per run.

Rebuilding a model-judged cycle is not on that list. If it ever is, the thing to fix first is the
coupling described above, not the orchestration.

## Language

English is the project language since 2026-08-06. Two permanent exclusions: `recipe-app/sources/`,
because converting them is a new scenario rather than a translation, and the historical artifacts
under `recipe-app/results/`, because they are the record of what was generated. Quotations from them
stay in Italian inside quotation marks, wherever they appear, because they are evidence.

Everything still live is in English. The Italian that survived the conversion sat in the consensus
documents, which a Phase 0b was going to translate and never did; the deletion settled it.
