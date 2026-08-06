# Ledger of falsifiable claims about `plan-slices`

Every change applied to `skills/plan-slices/SKILL.md` comes from a defect observed in a generated
plan and implies a prediction: *at the next cycle that defect does not reappear*. This ledger keeps
the predictions in one place, so that the eval cycle verifies them instead of forgetting them.

It serves two purposes:

- **Predicted regressions.** At every cycle the active rows are re-read and each claim is checked
  against the plan just generated.
- **Unpredicted regressions.** If an improvement report raises a defect that a row of this ledger
  declared closed, the row goes to `regressed`. No second artifact is needed: it is the same index
  read backwards.

**Language.** This file is in English since 2026-08-06. Verbatim quotations from historical
artifacts stay in Italian between guillemets: they are evidence, and translating them would
falsify the record.

**Cycle narrative is not here.** Regressions detected, rewritten formulations, decided diagnoses and
corrections applied live in the report of their own cycle —
`recipe-app/results/CONSENSUS-CON-N.REPORT.md`. The CON-5 narrative moved to
`recipe-app/results/CONSENSUS-CON-5.REPORT.md` on 2026-08-06.

## How to use

- One row per change applied to `SKILL.md`, added at the same moment as the change.
- The claim must be **binary and falsifiable** on a generated plan. «The plan is clearer» is not a
  claim; «every `NOW` slice cites the source sentence that requires it» is.
- Claims quantify **over a generated plan, not over the text of the skill**. This is the criterion
  the ledger was written with (`0273a73`: *«each stated over a generated plan rather than over the
  skill text»*), and it is why reformulating a clause does not falsify the row that covers it.
- **One row, one claim.** A row states exactly one thing a generated plan can falsify on its own.
  Where two requirements can fail independently, they are two rows. A row carrying several claims
  cannot hold a counter — one falsified member would carry `×k` for the others — and disaggregating
  a verdict afterwards means reconstructing predictions backwards, the defect this file declares of
  itself in `0273a73`. **Applied on 2026-08-06** to the four rows written before the rule existed:
  `R-001`, `R-004`, `R-006`, `R-009`. See *Splitting a row that carries several claims*.

### `Origin`

How the change was decided. **Four** values:

| Value | Meaning |
|---|---|
| `intersection` | both models raised the same defect **and** the same remedy |
| `intersection-theme` | both saw the same defect but the wording comes from one side only |
| `judgement` | a human found the defect on the generated plan and applied a point raised by one model or by none |
| `pruning` | the row claims that removing a clause does not bring a defect back |

They fail differently — the first misses things, the others can apply false ones — and telling them
apart is the only way to notice after the fact. The Italian plan documents name these
`intersezione`, `intersezione-tema`, `giudizio`, `potatura`; the values above are the same four.

**Reclassification of 2026-08-06.** Rows `R-002`…`R-008` carried `intersection` and moved to
`intersection-theme`. The CON-4 `REVIEW`s say so themselves, field `Differences`, repeated on every
shared entry: *«questo report è operativo […]; l'altro report propone il meccanismo generico»*.
`PLAN-CX-CON-4.IMPROVEMENT.md` is 8 generic bullets without any of the eight required fields, so
none of those seven rows can have had two formulations to intersect. The two rows falsified in
CON-5 — `R-002` and `R-008` — fall exactly where this category predicts: theme seen by two models,
remedy written by one. Those seven rows were moreover produced with prompts different from the ones
now under `prompts/`.

### `Provenance` and the initial `k`

How the row itself came to exist. **No row starts at `×1` by default**: the ledger was populated
retroactively — see `workflow/EVIDENCE.md` — so the initial counter
descends from this cell.

| Value | Meaning | Initial `k` |
|---|---|---|
| `ex-ante` | row written in the same minute as the commit it verifies. The pairing is recorded, not inferred. | `×0` |
| `reconstructed` | row written backwards onto a commit already made, but not touched during the measurement. | `×1` — CON-5 is a valid test |
| `reconstructed and re-tuned` | row rewritten between 22:20 and 22:41 on 2026-08-04, after the 22:02 CON-5 verdicts had shown what the plans said. | `×0` — the row was adapted to the plan that should have falsified it; CON-6 is its first real test |

### `Verification`

Declares who checks: `validator` if the check is or can become structural in
`skills/plan-slices/scripts/validate_plan.py`, `reading` if it requires human judgement.

### `Measured on`

Declares **against what** the verdict was produced. Grammar, five slots separated by `·`:

```
cycle · plans · tools · gen <model and effort per side> · verdict <instrument>
```

- **tools** are `plans` when the generated artifacts suffice, plus `sources`, `brief` and
  `validator` when needed.
- **gen** is the model and effort that generated each candidate. `CC`/`CX` name the harness, not the
  model. For CON-1…CON-5 the model and the effort were **never recorded and cannot be
  reconstructed**: every cell of those cycles reads `gen unrecorded`, and that is the true value, not
  a gap left to fill. `support/AGENT-PLAN-MAP.md` states once where it was looked for — the artifacts,
  the generation prompt, every grading artifact, the commit messages — and why the grading defaults
  are not copied in. It carries the harness and the mode, which *are* reconstructable. From CON-6 the
  cell is filled before the call.
- **verdict** is the instrument that produced the verdict. CON-5 was a partial cycle: its verdicts
  come from offline human reading, not from a `verdetto` call.

Without this column a verdict looks more solid than the way it was obtained: the regression
withdrawn on `R-006` had been measured on the sources alone, ignoring the brief, and the cell did
not say so. A row whose anchor moved carries the boundary here too — see *Re-anchoring*.

### `Watch for`

What to look for at the next `verdetto` **beyond** the claim. It is the only place where the ledger
says what to hunt for other than the assertion itself, and it enters the `verdetto` prompt as an
extra instruction for that row. Present only where a row has one; `—` otherwise.

### `Commit SKILL.md`

The commit whose text the claim is measured against. A row applied by the workflow is born with
`(pending)`: the workflow applies to the working tree and never commits, so the id exists only after
the human veto. A row still carrying `(pending)` has not been committed yet.

A cell carrying two commits means the claim is measured against both texts. Since 2026-08-06 no row
states more than one claim, so a second commit no longer names a second member: on `R-005` and
`R-006` it is a commit whose clause `support/CLAUSE-ROW-MAP.md` could not identify at all, recorded
there under *Unresolved anchors*.

### `State`

| Value | Meaning |
|---|---|
| `to verify` | no cycle has run against the change yet; equivalent to `×0` |
| `not falsified ×k` | `k` consecutive cycles have failed to falsify it on **either** plan. `×0` here means cycles have run but none of them counts as a test — see `Provenance` and *Re-anchoring* |
| `regressed on <side> (date)` | a cycle disproved it |
| `dormant` | reached `×3`; verified 1 cycle in 3 instead of every cycle |

`not falsified` is not confirmation. A claim holds only if it holds on both plans: **1 violation out
of 2** falsifies, **0 out of 2** are needed to survive a cycle. The second is absence of a
counterexample on a sample of two, and improvement is inferred only from accumulated absence of
disproof, never from a single round.

A `regressed` row is not deleted: the correction row is added and both are kept. A sequence of
regressions on the same theme is the signal that the rule is badly worded, not that it must be
rewritten again.

**Dormancy.** A row at `not falsified ×3` goes dormant and is verified 1 cycle in 3. Nothing is
deleted, and it becomes active again immediately if `recidiva` raises it. Dormancy replaces
retirement, which was deferred with no observable trigger.

### Re-anchoring and absorption

When an `IMPROVEMENT` entry touches a clause a row covers, one of two things happens. They are two
rules and not one because the claims quantify over a generated plan, not over the skill text: a
reformulation therefore **does not falsify** the row and does not make its claim undecidable — it
breaks the attribution only.

- **Re-anchoring — automatic.** The clause changes wording, the rule keeps its reach. The row stays,
  takes the new commit in `Commit` and records the boundary in `Measured on`, and the counter goes to
  **`not falsified ×0`**: `×k` counts cycles against a text, and the text changed. The claim is not
  rewritten; it stays valid and decidable.
- **Absorption — written by `improve`, edited in the veto.** The rule changes reach: extended,
  restricted, or corrected. Then **one row states all of it**, and the claim it replaces leaves the
  file. The surviving row starts at **`×0`** and carries `Absorbs R-NNN …` naming the absorbed
  claim's regressions. The signal this ledger declares load-bearing — *a sequence of regressions on
  the same theme means the rule is worded badly* — therefore survives the merge as a cell instead of
  as a row. Git keeps the old wording; the ledger keeps only what is still predicted.

Two constraints on absorption, both load-bearing:

- **Absorb only if the merged claim stays decidable on a generated plan in one reading.** Two claims
  that cross rather than nest can merge into something broader and vaguer, and a vaguer claim is less
  falsifiable — the opposite of what this file is for. Where the merge would blur, the two rows stay
  and the overlap is declared in `Absorbs`.
- **One row, one claim.** Since 2026-08-06 this is a writing rule for every row — see *How to
  use* — so no row has members to absorb one at a time. It stays here as the rule for a row that a
  future entry brings back to several claims: such a row is absorbed member by member, and the
  members no new claim takes over stay, as their own row. Dropping a whole row because one member
  was absorbed deletes a live prediction.

An absorbing row goes to `not falsified ×0`, never to `to verify`, as soon as a cycle has run
against any absorbed limb: cycles have run, and none of them tested the merged wording.

### Splitting a row that carries several claims

The inverse move of absorption, and recorded in the same column.

- **The first claim keeps the row's id; the others take new ids at the end.** An id is never reused.
- **Every child inherits `Origin`, `Provenance`, `Verification`, `Measured on`, `Last check` and the
  parent's counter.** The cycle that failed to falsify the row failed to falsify each of its claims,
  so restarting the children at `to verify` would erase a measurement actually obtained. Where the
  parent is disproved on one claim only, that child takes `regressed` and the others keep the
  counter. Provenance is inherited whole and not re-adjudicated per claim: deciding after the fact
  which member a re-tuning touched is the backwards reconstruction the split exists to prevent.
- **`Absorbs` carries the structural history**, as `Split from R-NNN mK (date)` on a child and
  `Split (date)` on the row that keeps the id. One column for «this row has not always had this
  shape» costs less than a twelfth, and the two moves are each other's inverse.
- **A commit no claim resolves to stays with the row that keeps the id.** By rule, not by judgement:
  attributing it to the child whose claim looks closest would resolve an anchor the map records as a
  failure.
- **A split adds no prediction.** The active-row count grows without the covered surface growing by
  one clause — `support/CLAUSE-ROW-MAP.md` counts covered clauses, not rows — and the counters are
  inherited instead of restarting. A cycle report reads `active rows N → M` as a measure of
  accumulation, so a split must never be read there as new rules entering the skill.

### Authority and rewritten formulations

- **The check is made against the scenario's `EVALUATION-BRIEF.md` before the sources.** The brief is
  the authority on which conflicts exist, which alternatives are accepted and which uncertainties are
  material; the sources are opened only to verify a citation. The ledger sits above individual
  scenarios and its rows do not know the brief: without this step it produces false positives against
  the authority of the scenario.
- **If a row contradicts an entry of `Accepted alternatives`, the defect is in the row.** It is
  rewritten to admit the alternative; no regression is recorded. Same for a claim that is not
  decidable from what the plan publishes, or is decidable only by choosing between two readings. In
  all three cases the reason, the date and the plans on which it emerged are recorded in the cycle's
  report, under *Rewritten formulations*.

## The ledger

| ID | Commit `SKILL.md` | Origin | Provenance | Falsifiable claim | Verification | Watch for | Last check | Measured on | Absorbs | State |
|---|---|---|---|---|---|---|---|---|---|---|
| R-001 | `2c89e7f` | `judgement` — `NOTES.md` § *Confine di scope vs identità* | reconstructed | The plan places identity after the differentiator. | reading | — | 2026-08-04 | CON-5 · `CC`+`CX` · brief+plans · gen unrecorded · verdict offline reading | Split (2026-08-06): the seam claim became `R-012` | not falsified ×1 |
| R-002 | `d977043` | `intersection-theme` — `REVIEW` CON-4 § *Sweep sistematico delle contraddizioni* ≡ *Explicit handling of source contradictions* | reconstructed and re-tuned | Every choice the plan declares open names the `NOW` slices it blocks, in whatever section it declares it. | validator-automatable on the open-choices section, whatever its title: every entry cites at least one existing `NOW` slice number | — | 2026-08-04 | CON-5 · `CC`+`CX` · brief+sources · gen unrecorded · verdict offline reading | first member absorbed into `R-010` on 2026-08-06 | not falsified ×0 — re-tuned on 2026-08-04 after the CON-5 verdicts; CON-6 is its first test |
| R-003 | `d977043` | `intersection-theme` — `REVIEW` CON-4 § *Decisioni mai prese distinte dalle decisioni prese* ≡ *Explicit handling of undecided choices* | reconstructed and re-tuned | No `NOW` slice depends on an external choice — provider, model, service, or adapter — that is not made by a citable source, or made by the plan among the alternatives the brief declares acceptable, or declared open together with the slice it blocks, in whatever section it declares it; a qualifying adjective — `cheap`, `multilingual`, `managed` — does not count as a choice. | reading: the inventory of external dependencies requires comparison with the sources and with the brief's `Accepted alternatives` | — | 2026-08-04 | CON-5 · `CC`+`CX` · brief+sources · gen unrecorded · verdict offline reading | — | not falsified ×0 — re-tuned on 2026-08-04 after the CON-5 verdicts; CON-6 is its first test |
| R-004 | `d977043` | `intersection-theme` — `REVIEW` CON-4 § *Ammissione in NOW subordinata a una domanda delle fonti* ≡ *Trace scope and horizon ownership* | reconstructed | No `NOW` slice delivers a behaviour the sources do not request. | reading — the skill places the tracing in reasoning, not in the plan | — | 2026-08-04 | CON-5 · `CC`+`CX` · brief+sources · gen unrecorded · verdict offline reading | Split (2026-08-06): the `LATER` claim became `R-013`, the `OUT-OF-SCOPE` claim `R-014` | not falsified ×1 |
| R-005 | `d977043`, `9aa2586` | `intersection-theme` — `REVIEW` CON-4 § *Continuità del tema* ≡ *Keep a theme and its recovery path contiguous* | reconstructed | If a `NOW` slice names a failure mode in its own `Verification` and another `NOW` slice is its remedy, no slice of a different theme is placed between the two. | reading for the failure→remedy coupling; theme interposition is automatable on the slices' `*(Theme: X)*` annotation | — | 2026-08-04 | CON-5 · `CC`+`CX` · plans · gen unrecorded · verdict offline reading | — | not falsified ×1 |
| R-006 | `d977043`, `9aa2586` | `intersection-theme` — `REVIEW` CON-4 § *Pipeline o adapter condiviso con un solo proprietario* ≡ *Open shared pipelines and adapters once, after their producers* | reconstructed and re-tuned | A pipeline or adapter shared by several paths is opened in the `Includes` of a single `NOW` slice. | partly automatable — the same adapter named in the `Includes` of two slices is structural, recognizing that two names denote one adapter is reading | — | 2026-08-04 | CON-5 · `CC`+`CX` · brief+plans · gen unrecorded · verdict offline reading | Split (2026-08-06): the reuse claim became `R-015`, the ordering claim `R-016`; the `9aa2586` component of `Commit` stays here unattributed, no claim resolves to it | not falsified ×0 — re-tuned on 2026-08-04 after the CON-5 verdicts; CON-6 is its first test |
| R-007 | `d977043` | `intersection-theme` — `REVIEW` CON-4 § *Audit esplicito di split* ≡ *Split capabilities and enablers with independent risks* | reconstructed and re-tuned | No `Enabler` slice validates uncertainties across more than one subsystem: its `Verification` cannot fail for causes that, in the brief's `Material uncertainties`, belong to different `Subsystem`s. Several entries of the same subsystem are one uncertainty, even when the answer invalidates the choice being verified. | reading: the per-pair split verdict lives in the unpublished ledger, only the outcome stays observable on the plan; the list of uncertainties, subsystems, and decisions that change is published by the brief | — | 2026-08-04 | CON-5 · `CC`+`CX` · brief+plans · gen unrecorded · verdict offline reading — the brief's `Material uncertainties` table was rewritten at 22:41 on 2026-08-04, in the same minute as this row | — | not falsified ×0 — re-tuned on 2026-08-04 after the CON-5 verdicts, together with the brief; CON-6 is its first test |
| R-008 | `9aa2586` | `intersection-theme` — `REVIEW` CON-4 § *Use repeatable, decision-changing verification*, part «each theme has a first validation» | reconstructed | Every theme's `First validation` points to a slice whose `Outcome` covers the theme's entire desired outcome. | validator for the existence of the reference; reading for outcome coverage | — | 2026-08-04 | CON-5 · `CC`+`CX` · brief+plans · gen unrecorded · verdict offline reading | `Enabler` clause and its exception absorbed into `R-011` on 2026-08-06 | regressed on `CX` in CON-5 (2026-08-04) against `9aa2586` — rows C and D of that regression; row A left with the absorption |
| R-009 | `a06a5cc` | `judgement` — commit message of `a06a5cc`, defect observed on a graded plan | reconstructed | No `Outcome` of a `NOW` slice preceding identity promises a real user: every slice that precedes identity and delivers a behaviour names its own audience, developer or tester on the declared non-public environment. | reading: the audience is read from the `Outcome`s, but deciding whether a slice delivers to an end user requires judgement | — | 2026-08-04 | CON-5 · `CC`+`CX` · plans · gen unrecorded · verdict offline reading | Split (2026-08-06): the deferral-threshold claim became `R-017` | not falsified ×1 |
| R-010 | `87150d3` | `judgement` — correction of `R-002`, first member, regressed on `CC` in CON-5 | ex-ante (own limb); reconstructed (absorbed limb) | No `Includes` or `Verification` bullet asserts in non-conditional form one side of an unresolved choice. Unresolved covers a conflict between the sources — those listed under `Known conflicts` in the brief, plus those demonstrable by citing two sources in disagreement — and, in the slices that choice blocks, any other choice the plan does not resolve by citing a selecting source. Declaring the choice under `Open questions` or assigning it a spike does not resolve it. | reading: recognizing which slices an open choice blocks requires comparing the declaration with the bullets | The correction comes from a violation on one model only: `CX` violated neither member of `R-002` and already used conditional wording. That is the typical way `judgement` applies a false rule. The failure to watch for is not the return of assertive wording but its opposite: plans that defer everything to the pending decision and publish nothing verifiable any more. If it appears, the defect is in `R-010`, not in the plans. | — | merged wording untested; the absorbed limb: CON-5 · `CC`+`CX` · brief+sources · gen unrecorded · verdict offline reading | `R-002` first member (2026-08-06) — that limb regressed on `CC` in CON-5 against `d977043` | not falsified ×0 — merged on 2026-08-06; the absorbed limb was falsified in CON-5, the own limb has never been tested |
| R-011 | `eb926bb` | `judgement` — correction of `R-008`, `Enabler` clause, regressed on `CX` in CON-5 | ex-ante (own claim); reconstructed (absorbed clause) | Every row of the `Themes` table has its `First validation` resolve to a `NOW` slice not annotated `*(Enabler: …)*`, unless its `Desired outcome` cell carries the `*(Developer outcome)*` marker. | validator: the check crosses two facts the plan already publishes, the slice number resolved by the cell and the title tag of that slice | The marker is declarative: a plan can attach it to a desired outcome that is not a developer's. The validator cannot know, and that residue is `reading`. The failure to watch for is the marker attached to get past the check, not its absence. | — | merged wording untested; the absorbed clause: CON-5 · `CC`+`CX` · brief+plans · gen unrecorded · verdict offline reading | `R-008`'s `Enabler` clause and its exception (2026-08-06) — that clause regressed on `CX` in CON-5 against `9aa2586`, row A | not falsified ×0 — merged on 2026-08-06; the absorbed clause was falsified in CON-5, the own wording has never been tested |
| R-012 | `2c89e7f` | `judgement` — `NOTES.md` § *Confine di scope vs identità* | reconstructed | The plan declares under `Cross-functional concerns` the single seam from which the current scope resolves. | reading, partly automatable on the presence of the declaration under `Cross-functional concerns` | — | 2026-08-04 | CON-5 · `CC`+`CX` · brief+plans · gen unrecorded · verdict offline reading | Split from `R-001` m2 (2026-08-06) | not falsified ×1 |
| R-013 | `d977043` | `intersection-theme` — `REVIEW` CON-4 § *Ammissione in NOW subordinata a una domanda delle fonti* ≡ *Trace scope and horizon ownership* | reconstructed | Every `LATER` entry states a `Promotion trigger`. | validator-automatable on the template's structure; not implemented — `validate_plan.py` checks only that the section carries a list | — | 2026-08-04 | CON-5 · `CC`+`CX` · brief+sources · gen unrecorded · verdict offline reading | Split from `R-004` m2 (2026-08-06) | not falsified ×1 |
| R-014 | `d977043` | `intersection-theme` — `REVIEW` CON-4 § *Ammissione in NOW subordinata a una domanda delle fonti* ≡ *Trace scope and horizon ownership* | reconstructed | Every `OUT-OF-SCOPE` entry states an exclusion rationale. | validator-automatable on the template's structure; not implemented — `validate_plan.py` checks only that the section carries a list | — | 2026-08-04 | CON-5 · `CC`+`CX` · brief+sources · gen unrecorded · verdict offline reading | Split from `R-004` m3 (2026-08-06) | not falsified ×1 |
| R-015 | `d977043` | `intersection-theme` — `REVIEW` CON-4 § *Pipeline o adapter condiviso con un solo proprietario* ≡ *Open shared pipelines and adapters once, after their producers* | reconstructed and re-tuned | A `NOW` slice that reuses a pipeline or adapter opened by an earlier slice declares it as reuse. | reading | The requirement was added to the parent row after CON-5 *because* `CX` never declared reuse, and `support/CLAUSE-ROW-MAP.md` records the anchor as `unresolved`: no clause of `SKILL.md` states it. A verdict against this row looks like a skill regression without being one until Fase 4 decides it. | 2026-08-04 | CON-5 · `CC`+`CX` · brief+plans · gen unrecorded · verdict offline reading | Split from `R-006` m1, second half (2026-08-06) | not falsified ×0 — re-tuned on 2026-08-04 after the CON-5 verdicts; CON-6 is its first test |
| R-016 | `d977043` | `intersection-theme` — `REVIEW` CON-4 § *Pipeline o adapter condiviso con un solo proprietario* ≡ *Open shared pipelines and adapters once, after their producers* | reconstructed and re-tuned | The `NOW` slice that opens a pipeline or adapter shared by several paths follows every `NOW` slice that feeds it input, except when it validates controlled inputs that traverse the production computation and the scenario's brief admits early validation. | reading for identifying the producers | The exception resolves to the scenario's brief, § `Accepted alternatives`, not to `SKILL.md` — see `support/CLAUSE-ROW-MAP.md` § *Anchors that resolve outside `SKILL.md`*. | 2026-08-04 | CON-5 · `CC`+`CX` · brief+plans · gen unrecorded · verdict offline reading | Split from `R-006` m2 (2026-08-06) | not falsified ×0 — re-tuned on 2026-08-04 after the CON-5 verdicts; CON-6 is its first test |
| R-017 | `a06a5cc` | `judgement` — commit message of `a06a5cc`, defect observed on a graded plan | reconstructed | If more than two `NOW` slices deliver behaviour to an end user before identity, `Ordering criteria` justifies the residual deferral once, naming the evidence that requires it. | reading: the justification is read from `Ordering criteria`, but deciding whether a slice delivers to an end user requires judgement | — | 2026-08-04 | CON-5 · `CC`+`CX` · plans · gen unrecorded · verdict offline reading | Split from `R-009` m2 (2026-08-06) | not falsified ×1 |

Active rows: **17**. Dormant: **0**.

**The split of 2026-08-06 took the count from 11 to 17 and added no prediction.** `R-001`, `R-004`,
`R-006` and `R-009` each stated more than one independently falsifiable requirement; each became one
row per claim, the first claim keeping the parent's id. The covered surface did not move by one
clause — `support/CLAUSE-ROW-MAP.md` counts covered clauses, not rows, and its totals are unchanged —
and every child carries its parent's counter. A cycle report must not read `active rows 11 → 17` as
six new rules entering the skill.

**Two absorptions applied on 2026-08-06, by hand.** `R-010` absorbed the first member of `R-002`,
`R-011` the `Enabler` clause of `R-008` and its exception; both pairs anchored on the same clause
after `87150d3` and `eb926bb` rewrote it, so keeping them apart counted one piece of evidence twice.
The rule says `improve` writes the merged claim and the veto edits it — here there was no `improve`
run to write it, and the merge is human. The remaining members stayed as their own rows and kept
their own history: `R-002` its open-choices requirement, `R-008` the outcome-coverage requirement
with rows C and D of its CON-5 regression. The row count is unchanged: nothing entered, nothing left.

## Agreed improvements that never reached the skill

Extracted from the `Improvements also present in the other report` sections of the two CON-4
`REVIEW`s and verified against the diffs of `d88328f`, `b0d6dc5`, `d977043`, `a06a5cc` and
`9aa2586`. They stay here until applied or explicitly discarded with a reason.

### Never applied

- **Semantic checks in the validator.** Both reports asked that the rules become tool-checkable: the
  `CX` report, bullet 7, proposes extending the validator with configurable semantic checks —
  interrupted themes, duplicated adapters, questions declared but ignored by the slices — and the
  `CC` report recognizes the two sites as compatible. Only the textual site was applied: `d977043`
  adds the checks to the `Proceed when` and `Complete when` gates, that is, to a gate evaluating
  whoever writes the plan. `validate_plan.py` is untouched by all five commits and stays structural:
  sections, slice fields, order, themes table. The three proposed checks are exactly the ones that
  today make `R-002`, `R-005` and `R-006` `reading`.
- **Versioned evaluation sets for quality claims.** The `CX` `REVIEW` classifies *Use repeatable,
  decision-changing verification* as shared and hangs on it the `CC` report's request for
  «set di valutazione versionati con casi positivi e negativi» for every quality, relevance or
  accuracy claim. No occurrence of it exists in `SKILL.md`: of the theme's two members only the
  first theme validator was taken up (`R-008`). Without this rule, a slice can verify that a
  semantic engine answers, not that it answers well.

### Taken up in the reasoning, therefore not observable on a plan

They are not ledger rows because no claim about a generated plan can falsify them: the skill
requires the output and then forbids publishing it. The improvement is applied, its verifiability is
not.

- **Source citation for every `NOW` slice.** Asked by both reports — «ogni slice `NOW` cita la frase
  delle fonti che ne richiede il comportamento» / «require every `NOW` slice to cite a source that
  requests it». `d977043` introduces the admission test but prescribes `Trace each NOW slice to the
  requesting statement in reasoning, not in the published plan`.
- **References to both sides of every conflict, and a split verdict for every adjacent pair.**
  `d977043` asks for the sweep with one reference per side and the per-pair verdict; `9aa2586`
  places both in the ledger and closes with `Keep the ledger in reasoning, not the published plan`.

This is a design choice — the published plan stays a roadmap, not an audit log — but it has a
measurable cost: three of the six shared improvements taken up produce, on the plan, only an
indirect consequence. If the ledger were a separate artifact versioned next to the plan, `R-003`,
`R-004` and `R-007` would become checkable without touching the template.

## To populate

- **Correction for the CON-5 regression of `R-008`, partial.** Row A left with the absorption into
  `R-011`. Rows C and D stay with `R-008` and stay uncorrected: row C's site is the § 2 split test,
  not `R-008`, and row D is already forbidden by the outcome-coverage claim, which no tool can decide
  in place of a reading. The three diagnoses are in
  `recipe-app/results/CONSENSUS-CON-5.REPORT.md` § *Diagnosi decise dopo il ciclo CON-5*.
- **Corrections deferred pending a second cycle.** Three proposals born from the same two
  regressions were written and not applied, because each extends a perimeter or adds a constraint on
  the basis of a single observation, on a single model. The ledger exists to tell this case apart:
  they are `judgement` candidates, and a second cycle makes them `intersection` in fact or discards
  them. The pattern common to `R-002` and `R-008` is not that rules are missing — both violated rules
  existed — but that the gates ask for assertions instead of comparisons: adding further textual
  prohibitions has a non-small probability of not biting, like the two already present.
  - **Picking a side by placing it in another horizon.** `R-010`'s prohibition covers `Includes` and
    `Verification`. `CC` picked the `concepts.md` side of the manual/extraction conflict by putting
    tag and time derivation for manual recipes in a `LATER` entry, a site outside the perimeter. The
    extension — placing in `LATER` or `OUT-OF-SCOPE` a behaviour that only one side of the conflict
    requires is picking it — must be applied together with the alignment of the *Silent contradiction*
    anti-pattern, which today names only the non-conditional slice. **Unblocks:** the same
    pick-by-placement observed on a generation other than `CC`.
  - **`First validation` pointing at an `Enabler`, checked by the validator. — Applied, `R-011`
    (2026-08-04).** Unblocked by the first of the two routes the entry indicated: the explicit
    `*(Developer outcome)*` marker in the template. The «single observation on a single model»
    condition fell with `CC` CON-3 row B, which carries the same defect.
  - **Desired-outcome coverage, term-by-term comparison. — Not applied, diagnosis decided
    (2026-08-04).** The alternative diagnosis the entry asked to decide is the right one on row C:
    `Theme compression`, site the § 2 split test, which already forbids it. On row D the enumerative
    diagnosis holds instead, and it is already covered by `R-008`'s outcome-coverage claim, the only
    one that row still carries after the 2026-08-06 absorption. The two rows
    have different causes, so a single new rule next to `R-008` would have missed both. No rule
    added. **Unblocks a new rule:** a partial coverage observed on a theme that passes the split
    test, that is not reducible to compression, on a generation other than `CX` CON-5.
- **Anchors that do not resolve to a clause of `SKILL.md`.** `support/CLAUSE-ROW-MAP.md` records
  four, and after the 2026-08-06 split two of them are whole rows: `R-001` and `R-015`, plus the
  `9aa2586` component of `R-005`'s and `R-006`'s `Commit` cells, which no claim of either row
  resolves to. The failures are recorded there, not here; what belongs here is the decision they
  force, which is open: for each, either the skill gains the clause the row assumes, or the row is
  rewritten to stop demanding something the skill does not say. `R-015` is the sharpest — the
  requirement was added to `R-006` after CON-5 *because* `CX` never declared reuse, so the row
  demands what the skill never asked for. Until this is decided, a verdict against them can look
  like a skill regression without being one.
- **Changes of the five commits with no ledger row.** `d88328f` (non-hollow walking skeleton) and
  `b0d6dc5` (restriction to high-level roadmaps) are not reconstructable from the intersection of
  the two `REVIEW`s: the first appears in neither `also present` section, the second has no verified
  correspondence. They are changes that entered by judgement on an observed defect and their
  prediction must be reconstructed from there, not from the `REVIEW`s. `a06a5cc` (threshold on
  identity deferral) was in the same condition and is now `R-009`, reconstructed from its own commit
  message, which names the observed defect.
- **Changes preceding `d88328f`.** They come from conversations between human and agent on generated
  plans, before the comparison between models: no artifact exists from which to reconstruct a
  prediction. They are recorded only if a future cycle raises a regression on them.
