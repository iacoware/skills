# Post-mortem — the two automated evaluations

Two automated evaluation systems were built here between 2026-07 and 2026-08, and both are retired.
The goal they served — noticing that a change to `skills/plan-slices/SKILL.md` improved one thing
while breaking another — is now met by a structural validator and a human reading list.

- **Grading system** — abandoned 2026-08-06. A rubric, calibrated graders, adjudication between two
  providers, immutable artifacts in three versions.
- **Consensus cycle** — abandoned 2026-08-11. Two models, four blind phases (`improve`, `review`,
  `verdetto`, `recidiva`), a conformance gate, and a ledger of falsifiable claims.

Everything they were built from was deleted on 2026-08-12, and every byte of it is recoverable.

## Why they were abandoned

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

The consensus plan had written an abandonment threshold, to be evaluated at CON-8. Its first
condition was *procedure maintenance has not fallen below one skill change per cycle*. CON-6 came in
at four tool fixes against one applied change. The condition had already failed; CON-7 and CON-8
would have cost eighteen more calls to confirm it.

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

## What would justify reopening

Left observable on purpose, so that "closed" stays a decision instead of becoming a habit.

**The manual net leaks twice.** If a regression reaches a commit and is only noticed two changes
later — and it happens a second time — then reading is no longer catching what it was kept to catch,
and the answer is either a cheaper automated check or a smaller skill. In that order.

Rebuilding a model-judged cycle is not on that list. If it ever is, the thing to fix first is the
coupling described above, not the orchestration.

## Debts the retired program left owing

Not checks — do not run them. Until each is decided, a failure against it looks like a skill
regression without being one.

- **R-015 — reuse declaration.** *«A `NOW` slice that reuses a pipeline or adapter opened by an
  earlier slice declares it as reuse.»* Regressed unanimously in CON-6, exactly as predicted: **no
  clause of `SKILL.md` states this**. It was added to the ledger after CON-5 *because* a model
  failed to do it — a rule invented backwards from one observation. Either the skill acquires the
  clause, or the check dies.
- **Three anchors with no clause.** `R-001`'s, and the `9aa2586` component that `R-005` and `R-006`
  carried. Same decision, same owner: the scope reduction of the skill.
- **Two agreed improvements that never reached the skill** — semantic checks in `validate_plan.py`
  (interrupted themes, duplicated adapters, open questions ignored by the slices), and versioned
  evaluation sets for quality claims. Both raised by two independent reviews in CON-4. The first
  would move R-002, R-005 and R-006 from reading to validator, which is the only direction in which
  the check list gets cheaper. The second exists because no clause of `SKILL.md` asks a quality,
  relevance or accuracy claim to name a versioned evaluation set with positive and negative cases:
  a slice can verify that a semantic engine answers, not that it answers well.

## Recovering the apparatus

It was deleted rather than archived, because a file that looks operational and is not costs more
than it saves — the same reason `recipe-app/README.md` and `recipe-app/EVAL-NOTES.md` went earlier,
being a path index and a note on grader inputs that both described a layout no longer there. An
index that lies is worse than no index.

Everything is reachable by name through the **`evals-final`** tag, on `origin` and local, pointing
at `2abb8ab`, the last commit where the apparatus was whole:

```
git show evals-final:evals/plan-slices/REGRESSION-LEDGER.md
git ls-tree -r --name-only evals-final evals/plan-slices/
```

| What lived at | Was |
|---|---|
| `CONSENSUS-WORKFLOW.md`, `CONSENSUS-WORKFLOW-PLAN*.md`, `workflow/` | The consensus tool and its plan. `workflow/EVIDENCE.md` is the honest record of what the cycle actually measured. |
| `REGRESSION-LEDGER.md` | 18 rows with counters, provenance and absorption history. `EVALUATION-RULES.md` is its distillation; the ledger keeps the *why* of each row. |
| `prompts/` | The four blind phase prompts — `improve`, `review`, `verdict`, `recidiva`. 498 lines of allowlists, filled contracts and self-check criteria. |
| `assets/`, `support/`, `scripts/consensus/` | Conformance template, clause→row map and its *Unresolved anchors*, `validate_improvement.py`. |
| `recipe-app/payloads/` | The CON-6 payload projections the four prompts read. |
| `GRADING-*.md`, `grader-rubric*.json`, `fixtures/`, `scripts/*.py`, `recipe-app/results/calibration-*/` | The grading system in full. |
| `PROMPTS.md`, `NOTES.md` | Consensus scratchpads. The generation prompt one of them held is now inlined in `REVIEW-WORKFLOW.md` step 1, which is the only part of either that was live. |
| `Makefile` targets `grade`, `compare`, `calibrate*`, `validate-improvement`, `clause-map` | Their entry points. |

**The cycle reports under `recipe-app/results/` keep their dangling citations, deliberately.** The
three `CONSENSUS-CON-*` files cite `support/`, `workflow/` and ledger rows heavily, and every one of
those paths is now gone. They are the record of a cycle as it ran: rewriting their references would
falsify what the cycle actually read. Do not tidy them — resolve them against the tag instead.
