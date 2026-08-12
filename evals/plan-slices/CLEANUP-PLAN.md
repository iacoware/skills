# Cleanup plan — remove the grading and consensus apparatus

Delete everything that existed only to run the two retired evaluation systems, keep the scenario,
the three review documents, the generated plans, and the structural validator. This file is
scaffolding: it is deleted by the last step of its own plan.

**Nothing blocks it.** The skill is already self-contained, verified before writing this:

- `skills/plan-slices/scripts/validate_plan.py` imports only stdlib — `argparse`, `re`, `sys`,
  `dataclasses`, `pathlib`, `typing`. No dependency on `evals/`.
- Its test lives with the skill, `skills/plan-slices/scripts/test_validate_plan_v3.py`. Six tests,
  green.
- `SKILL.md` never names `evals/`, `recipe-app`, the ledger, or the cycle.

The whole risk is in four live documents that point at files about to disappear. Phase 1 repairs
them; only then does Phase 2 delete. In the opposite order there is a commit where
`MANUAL-REVIEW.md` points at nothing.

## Counts

`git ls-files evals` is **187**, this file included. After this plan it is **35**.

| Kept | Files |
|---|---|
| `recipe-app/sources/` | 4 |
| `recipe-app/results/` minus `calibration-*` | 25 |
| `recipe-app/EVALUATION-BRIEF.md`, `recipe-app/REFERENCE-PLAN.md` | 2 |
| `README.md`, `MANUAL-REVIEW.md` | 2 |
| `../AGENTS.md` | 1 |
| `Makefile` | 1 → deleted, see Phase 3 |

| Deleted | Files |
|---|---|
| `scripts/` — grading orchestrator, graders, scoring, adjudication, `consensus/` | 22 |
| `recipe-app/payloads/` — CON-6 payloads and discarded attempts | 33 |
| `fixtures/` — labeled calibration fixtures, v1 and v3 manifests | 21 |
| `recipe-app/results/calibration-{legacy,v2,v3}/` | 50 |
| `prompts/` — the four phase prompts. See *Why `prompts/` goes too* | 4 |
| `workflow/` (5), `support/` (3), `assets/` (2) | 10 |
| `CONSENSUS-WORKFLOW{,-PLAN,-PLAN-CLOSED}.md`, `GRADING-{EVAL-WORKFLOW,IMPROVEMENTS,IMPROVEMENTS-PLAN}.md`, `NOTES.md`, `PROMPTS.md`, `REGRESSION-LEDGER.md` | 9 |
| `grader-rubric.json`, `grader-rubric.v3.json` | 2 |
| `CLEANUP-PLAN.md` — this file | 1 |

**Everything deleted stays in git.** Phase 0 makes that pointer permanent instead of implicit.

## Why `prompts/` goes too

Decided 2026-08-12, recorded here so it is not reopened. The four phase prompts are the most
reusable-looking thing in the apparatus — 498 lines of blind allowlists, filled contracts and
self-check criteria — and keeping them was considered. Every one of their inputs is on the deletion
list:

| Prompt | Lines | Inputs that disappear |
|---|---|---|
| `improve` | 123 | `CLAUSE-INDEX.md`, `LEDGER-CLAIMS.md`, `assets/improvement-template.md` |
| `review` | 141 | `REPORT-A.md`, `REPORT-B.md` |
| `verdict` | 137 | `LEDGER-ROWS.md`, `CANDIDATE-A/B.md`; cites `workflow/LEDGER.md` and `REGRESSION-LEDGER.md` |
| `recidiva` | 97 | `ROWS.md`, `REPORT-A.md`, `REPORT-B.md` |

`CLAUSE-INDEX`, `LEDGER-*`, `ROWS` and `REPORT-*` are payload projections under
`recipe-app/payloads/CON-6/`, which this plan deletes.

`improve.prompt.md` is the decisive case rather than a marginal one. It names
`assets/improvement-template.md` four times and calls it *«the contract»* — line 23 puts it in the
payload allowlist, line 79 reads *«Fill exactly the fields it declares»*. Keeping the prompt while
deleting the template leaves a prompt instructing a model to satisfy a contract that does not exist:
not a broken link, an inoperable prompt.

So the four are not a portable technique but the wiring diagram of a machine with no parts left,
and keeping them produces precisely what this cleanup exists to remove — files that look
operational and are not. The craft in them stays reachable by name through the `evals-final` tag:
`git show evals-final:evals/plan-slices/prompts/review.prompt.md`. That tag is what makes deleting
safe enough to be aggressive here.

## Phase 0 — Make the history reachable

Zero deletions. Without this, recovering a deleted file means knowing that `evals/` was once large
and hunting for the commit where it still was.

- [ ] `git tag evals-final` on the current `HEAD`, before any deletion. A tag is a permanent,
  human-readable pointer: `git show evals-final:evals/plan-slices/REGRESSION-LEDGER.md` works
  forever, `git log` archaeology does not.
- [ ] Nothing to push — the tag is local unless the repo gains a remote.

## Phase 1 — Repair the live documents, before deleting anything

Four dependencies of surviving files on files about to go. All four are resolved by moving content
in, not by adding a new file: a new file would be new baggage.

- [ ] **`PROMPTS.md` § `GENERATE PLAN` → `MANUAL-REVIEW.md`.** This is the only hard dependency.
  `MANUAL-REVIEW.md` step 1 and `README.md` both cite it as live, and `PROMPTS.md` is otherwise a
  consensus scratchpad, 48 lines. Inline the prompt into step 1 of *The loop*, as a fenced block.
  It must keep the explicit skill activation — `/plan-slices` and `$plan-slices` — because
  `agents/openai.yaml` sets `allow_implicit_invocation: false` and the skill's frontmatter sets
  `disable-model-invocation: true`. Without it the candidate is born without the skill, which is the
  defect S1 of CON-6 found and fixed.
- [ ] **`support/CLAUSE-ROW-MAP.md` § *Unresolved anchors*.** Cited by `MANUAL-REVIEW.md` § *Open*.
  Drop the pointer only: the four anchors are already named in the text — `R-001`, `R-015`, and the
  `9aa2586` component that `R-005` and `R-006` carried.
- [ ] **`REGRESSION-LEDGER.md` § *Agreed improvements that never reached the skill*.** Same
  treatment: drop the pointer, keep the two improvements already summarised in place.
- [ ] **`README.md` § *What is archive*.** The whole table goes, and with it the sentence about
  `make test` staying green on the grading tests.

**What `README.md` must not lose.** The *why* is the only defence against rebuilding this in six
months, and it is the part with no other copy once `workflow/EVIDENCE.md` is gone: the volume ratio,
the 131-to-15 commit split, the CON-6 arithmetic, the abandonment threshold that had already
tripped, and the coupling defect — claims quantifying over a generated plan rather than over the
text of the skill. Rewrite *What is archive* into a short *Recovering the apparatus* naming the
`evals-final` tag and what lived where.

**Commit this phase on its own**, so the deletion commit is a pure deletion readable from
`--stat` alone.

## Phase 2 — Delete

One commit. It is one decision and splitting it would make each part look unmotivated.

```
git rm -r --cached  # not needed; these are plain deletions
git rm -r evals/plan-slices/scripts \
          evals/plan-slices/fixtures \
          evals/plan-slices/workflow \
          evals/plan-slices/prompts \
          evals/plan-slices/support \
          evals/plan-slices/assets \
          evals/plan-slices/recipe-app/payloads \
          'evals/plan-slices/recipe-app/results/calibration-*'
git rm evals/plan-slices/CONSENSUS-WORKFLOW.md \
       evals/plan-slices/CONSENSUS-WORKFLOW-PLAN.md \
       evals/plan-slices/CONSENSUS-WORKFLOW-PLAN-CLOSED.md \
       evals/plan-slices/GRADING-EVAL-WORKFLOW.md \
       evals/plan-slices/GRADING-IMPROVEMENTS.md \
       evals/plan-slices/GRADING-IMPROVEMENTS-PLAN.md \
       evals/plan-slices/NOTES.md \
       evals/plan-slices/PROMPTS.md \
       evals/plan-slices/REGRESSION-LEDGER.md \
       evals/plan-slices/grader-rubric.json \
       evals/plan-slices/grader-rubric.v3.json
rm -rf evals/plan-slices/scripts  # __pycache__ is gitignored, so git rm leaves it on disk
```

- [ ] Run the above and confirm `git status` shows deletions only.

## Phase 3 — Detach the two remaining hooks

Both break if left alone.

- [ ] **Root `Makefile`, target `test`.** Its second line is
  `cd evals/plan-slices/scripts && python3 -m unittest`, and that directory is gone. Remove the
  line. The first line, which runs the skill's own tests, stays.
- [ ] **`evals/plan-slices/Makefile` → deleted, `validate` moves to the root `Makefile`.** Of its
  eleven targets only `validate` and `test` survive the deletion, and `test` duplicates the root's.
  Keeping a 140-line Makefile whose variables name a rubric, a fixture manifest, an orchestrator and
  four provider knobs, to run one `python3` invocation, is exactly the baggage this plan exists to
  remove. The root target:

  ```make
  validate:
  	@test -n "$(PLAN)" || { echo "usage: make validate PLAN=<plan.md>"; exit 2; }
  	python3 skills/plan-slices/scripts/validate_plan.py $(PLAN)
  ```

  Note the changed contract: `PLAN` becomes a **path**, not a bare filename resolved against
  `recipe-app/results/`. Update the invocation in `MANUAL-REVIEW.md` step 2 and in `README.md`.
- [ ] **`AGENTS.md`.** The root file contains one line — *«See `evals/AGENTS.md`…»* — and
  `evals/AGENTS.md` holds the provider-run authorization rule, which still binds: the manual loop
  spends one generation call. Fold the rule into the root `AGENTS.md` and delete `evals/AGENTS.md`.
  One file, no indirection.

## Phase 4 — Optional, same spirit

Neither blocks anything.

- [ ] **`test_validate_plan_v3.py` → `test_validate_plan.py`.** The `_v3` is grading vocabulary
  — *evaluator v3* — and `__pycache__` still holds a `test_validate_plan.cpython-314.pyc` from
  before the rename. Baggage left in a filename. `git mv`, no content change.
- [ ] **Leave `evals/` named `evals/`.** Deliberate, not forgotten: moving the scenario was offered
  and declined. The name is now inaccurate — what is left is a scenario, three review documents and
  a sample of generated plans — and renaming it later costs one `git mv`.

## Phase 5 — Verify, then delete this file

- [ ] `make test` → green. Proves Phase 3's first hook is detached.
- [ ] `make validate PLAN=evals/plan-slices/recipe-app/results/PLAN-CC-CON-6.md` → `OK`. Proves the
  new target and the new path contract.
- [ ] `git ls-files evals | wc -l` → **35**, or **34** after `evals/AGENTS.md` folds into the root.
- [ ] **No live document points at a deleted path.** The three live documents are `README.md`,
  `MANUAL-REVIEW.md` and `recipe-app/REFERENCE-PLAN.md`:

  ```
  grep -nE 'workflow/|prompts/|support/|assets/|payloads/|fixtures/|scripts/consensus|REGRESSION-LEDGER|CONSENSUS-WORKFLOW|PROMPTS\.md|grader-rubric|calibration-' \
    evals/plan-slices/README.md evals/plan-slices/MANUAL-REVIEW.md evals/plan-slices/recipe-app/*.md
  ```

  Expect only intentional mentions — the *Recovering the apparatus* section naming what once lived
  where.
- [ ] **Do not repair `recipe-app/results/`.** The three `CONSENSUS-CON-*` reports cite `support/`,
  `workflow/` and ledger rows heavily, and those citations are now dangling. Leave every one of
  them. They are the record of a cycle as it ran, and rewriting their references would falsify what
  the cycle actually read. State this once in `README.md` so a later session does not tidy them.
- [ ] `git rm evals/plan-slices/CLEANUP-PLAN.md` in the final commit.

## Open questions

- **Do the CON-1…CON-6 `IMPROVEMENT`, `REVIEW` and `VERDICTS` artifacts stay?** Keeping `results/`
  was decided, but the 25 files split **12 generated plans** against **13 pieces of cycle machinery
  output** — 4 `IMPROVEMENT`, 4 `REVIEW`, 2 `VERDICTS`, 3 `CONSENSUS-CON-*` reports. The 13 are the
  evidence behind every claim in `MANUAL-REVIEW.md`'s
  *has failed* markers, which argues for keeping them; they are also unreadable without the prompts
  and templates being deleted, which argues the other way. Default if unanswered: keep all 25.
- **Does `evals/AGENTS.md` fold into the root, or stay?** Phase 3 assumes it folds. Staying is
  defensible if more scenarios are expected under `evals/` later.
