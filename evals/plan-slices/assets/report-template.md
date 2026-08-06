# Consensus cycle CON-[N] — report

[The structure of `recipe-app/results/CONSENSUS-CON-N.REPORT.md`. One report per cycle, written at
step 9 by joining the artifacts the cycle produced — no call of its own, every number below is
composition. The cycle is `../CONSENSUS-WORKFLOW.md` § *Il ciclo*; the detail rules are
`../workflow/CYCLE.md`; the gate is `../workflow/CONFORMANCE.md`.]

[Paragraphs in square brackets are the template speaking. They are **not** copied into an instance.
Everything else is copied and filled.]

[**Language.** The frame is English. Verbatim quotations from historical artifacts stay in Italian
between guillemets: they are evidence, and translating them falsifies the record.]

[**`n/a — partial cycle`.** A counter has a value only where the cycle produced one. Where a phase
did not run, write `n/a — partial cycle` and what was missing, never `0`: a zero reads as a
measurement that was taken and came out empty. Same rule for a phase that ran and produced nothing —
that one *is* a `0`.]

[One line of frame: when the cycle ran, whether it was complete, and — if it was not — which phases
are missing. A report not written at the cycle it describes says so here, with where its content
comes from and exactly what changed in moving it: a narrative moved is a record, and a record whose
provenance is unstated is a reconstruction.]

## Inputs

- **`SKILL.md` at generation:** `[commit]`, [N] lines
- **Candidates:** `recipe-app/results/PLAN-CC-CON-[N].md`, `recipe-app/results/PLAN-CX-CON-[N].md`
- **Improvement reports:** `PLAN-CC-CON-[N].IMPROVEMENT.md`, `PLAN-CX-CON-[N].IMPROVEMENT.md`
- **Reviews:** `PLAN-CC-CON-[N].REVIEW.md`, `PLAN-CX-CON-[N].REVIEW.md`
- **Verdicts:** `PLAN-CC-CON-[N].VERDICTS.md`, `PLAN-CX-CON-[N].VERDICTS.md`
- **Recidiva:** `CONSENSUS-CON-[N].RECIDIVA.md`
- **Models and effort:** generation `[model]`/`[effort]` per side; `improve`, `review` and `verdict`
  `[model]`/`[effort]` per side; `recidiva` `claude-opus-5`/`[effort]`
- **`Measured on`:** `CON-[N] · CC+CX · [tools] · gen [model and effort per side] · verdict [instrument]`

[The `Measured on` line is written **once here** and copied verbatim into every ledger row the cycle
touches. Its grammar is `REGRESSION-LEDGER.md` § *`Measured on`*, five slots, the fifth included. A
row whose anchor moved carries the boundary in its own cell as well.]

[The blind mapping — which alias holds which candidate and which report — is **not** in this file.
It lives in `support/AGENT-PLAN-MAP.md`, which is excluded from every payload. The report names real
artifacts because the cycle is over; it does not restate the mapping the map owns.]

### What produced the verdicts

[Required whenever the fifth `Measured on` slot is not a `verdetto` call — offline human reading, a
partial cycle, a one-off instrument. Say what was read against what, and **what the cycle is
therefore not evidence of**. The slot records the instrument; this paragraph records the
consequence, and without it a verdict looks more solid than the way it was obtained. Omit the
section when the instrument is the cycle's own `verdetto`.]

## Counters

```
SKILL.md                        [N] → [M]   ([+d])
entries applied                  [N]
  reformulations                 [N]
  reach-changes                  [N]
  additions                      [N]   ← each with the reason the reformulation was discarded
new ledger rows                  [N]
    [N] intersection · [N] intersection-theme · [N] judgement · [N] pruning
re-anchored rows                 [N]   (counter reset to ×0)
absorbed claims                  [N]
active rows                     [N] → [M]
entries discarded by the gate    [N]   ([the fields they fell on])
discarded verdicts               [N]   (citation does not resolve)
recidiva                         [N] pairs over [M] entries
structural validator             [outcome per candidate]
```

[**Read `absorbed claims` first.** It is the only counter that says a prediction has **left** the
file, and every absorption is reread in the veto because a merge can widen what the surviving row
claims. `../workflow/LEDGER.md` § *Cosa il registro registra*.]

[**`active rows N → M` is the counter that bites on accumulation**, the way `0 reformulations out of
5 additions` bites on the skill. Re-anchoring adds no row; absorption removes one when the absorbed
claim was the whole row; a split adds rows without adding a prediction and must be declared as such
in *Consequences carried into the ledger*, never read here as new rules. Growth in `active rows`
that is not a split therefore accuses the additions and nothing else.]

[**The three remedies sum to `entries applied`.** `reformulation`, `reach-change` and `addition` are
the three values `improvement-template.md` allows; a cycle whose sub-counters do not add up has lost
an entry between the gate and the application.]

### Reading of the counters

[Two or three lines, for the record: what shape this cycle had, and what the numbers accuse. Not a
verdict on the hypothesis — a cycle emits none, consistently with `not falsified ×k`.]

## Structural validator

[`make validate PLAN=…` on both candidates, step 2. Outcome per candidate, and the failures with the
rule that produced them. The validator expresses no semantic judgement, so a failure here is a fact
about the plan's form, not about its quality.]

## Entries applied

[Only what the filter licenses: entries **both** `REVIEW`s classify as shared. One entry = one hunk
of `SKILL.md` + one ledger row, same id, row born with `Commit SKILL.md: (pending)`. The workflow
applies to the working tree and **never commits**. `../workflow/CYCLE.md` § *Cosa il workflow
applica da sé e cosa no*.]

### `[A#N]` / `[B#N]` — [the defect, one line]

- **Origin:** `intersection` | `intersection-theme` — [when `intersection-theme`, which side carries
  the wording and why]
- **Remedy:** `reformulation` | `reach-change` | `addition`
- **Hunk:** `SKILL.md:[NN]-[MM]` § `[section title]`
- **Ledger row:** `R-[NNN]` — [the claim, verbatim as written into the row]
- **Covering rows declared:** `R-[NNN]` | `uncovered`
- **Discarded reformulation:** [required when the remedy is `addition` and a clause was named;
  `n/a` otherwise]

[`Origin` is `intersection` or `intersection-theme` **only if both `REVIEW`s classify the entry as
shared**. Unilateral classification is `judgement` and never applies automatically — it goes to
*Points requiring human reading*, and the row that may be born from it cites the defect observed on
the plan, not the report that proposed it.]

## Consequences carried into the ledger

[Everything this cycle changed in `REGRESSION-LEDGER.md` besides adding rows. Re-anchoring and
absorption are recorded apart because only one of them removes a prediction. Rules in
`REGRESSION-LEDGER.md` § *Re-anchoring and absorption* and § *Splitting a row that carries several
claims*.]

**Re-anchored rows** — [automatic: the clause changed wording, the reach held.]

- `R-[NNN]` — new commit `[commit]`, counter to `×0`, claim unchanged.

**Absorbed claims** — [never automatic: emitted by `improve`, decided in the veto.]

- `R-[NNN]` absorbs `R-[NNN]` — **merged claim:** […]; **regressions carried over:** […]; **claims
  that left the file:** […]

**Splits** — [when a row carrying several claims was split this cycle.]

- `R-[NNN]` → `R-[NNN]` — `Split from R-[NNN] m[K] ([date])`. Adds no prediction.

**Other consequences** — [anything else the cycle wrote into a row and that the counters do not
show: a `Provenance` decided, a `Watch for` cell filled from a correction, a state changed to
`dormant`. One line each, with the row.]

## Classification instability

[**The measure that unblocks Phase 7**, and the one nobody produced before: entries **one** `REVIEW`
classified as shared and the other did not. Published as a list, per cycle, so that the instability
of the classification becomes observable instead of being asserted.]

[N] of [M] entries classified shared by at least one review.

- `[A#N` / `B#N]` — shared according to `[which review]`, `[what the other review called it]`.
  [What the divergence is about.]

## Points requiring human reading

[Everything the filter does not license: entries shared according to one review only, entries unique
to one side, contradictory entries, and entries that break the hard rule of bidirectional `improve`
— a named clause plus added rules without a written reason for discarding the reformulation. None of
these is applied by the workflow.]

- `[A#N` / `B#N]` — [the defect] — **why it is not applied:** [one of the four cases] — **what to
  check on the plan:** [the point to reread]

## Discard log

[Step 4, one attempt per entry, no regeneration. Every discard carries the entry, the field and the
reason, as `validate_improvement.py` renders them. A side at zero conforming entries does not block
the cycle and is a fact of the cycle, not a fault to repair.]

| Report | Entry | Field | Reason |
|---|---|---|---|
| `[A` / `B]` | [N] | `[field]` | [reason] |

[**The distribution is the diagnosis.** Discards concentrated on a single field accuse the template,
and that field is corrected. Discards spread across fields accuse the model, and the specificity
hypothesis takes a `×1` disproof. Say which of the two this cycle shows.]

**Discarded verdicts** — [step 6: a verdict whose citation does not resolve is discarded and logged.
A discarded verdict measures nothing, and the discard rate is the thermometer of dilution.]

| Row | Candidate | Citation as written | Why it does not resolve |
|---|---|---|---|
| `R-[NNN]` | `[A` / `B]` | `[citation]` | [reason] |

## Verdicts

[One line per row per candidate, from the two `VERDICTS` artifacts. **Two verdicts per row**, never
aggregated: a claim holds only if it holds on both, and that arithmetic is done here, not by the
model. Dormant rows enter 1 cycle in 3 and are marked as such.]

| Row | Candidate A | Candidate B | Resulting state | Watch for |
|---|---|---|---|---|
| `R-[NNN]` | `holds` / `falsified` / `row-defect — <reason>` + citation | idem | `not falsified ×k` / `regressed on <side>` / — | [what was found] / `not observed` / `no note on this row` |

[`row-defect` records no regression and is not a verdict about the plan: it says the claim is badly
written, and the row goes to *Rewritten formulations*.]

[A row that needed re-measuring — first passed over, or measured against the wrong authority — gets
its own paragraph under the table, naming what it was re-measured on and whether the verdict moved.
The table holds the verdict; the paragraph holds why it can be trusted.]

## Regressions detected

[The rows a candidate falsified, with the published point that falsifies them. One entry per row,
naming the side. A regressed row is not deleted; the correction row is added and both are kept.]

## Rewritten formulations

[**Mandated by `REGRESSION-LEDGER.md` § *Authority and rewritten formulations*.** Rows the cycle
could not decide, decided only by choosing between two readings, or that contradicted the scenario's
`EVALUATION-BRIEF.md`. In all three cases the defect is in the row: it is rewritten, no regression
is recorded, and the reason, the date and the plans on which it emerged stay here — otherwise the
rewriting is lost in the file's history.]

- **`R-[NNN]` — [what was wrong with it], rewritten, verdict `[outcome]`.** [The reason, over the
  plans that produced it.]

## Diagnoses decided

[When a verdict falsifies a row, the move is the qualitative investigation: which clause of
`SKILL.md` let the defect through. It counts only if it names a specific clause and generates a
falsifiable prediction — *«remove or reformulate this clause and the defect does not come back»*.
A diagnosis whose seat is a clause that already forbids the case ends here with **no rule added**,
and saying so is the point of the section.]

## Corrections applied after the cycle

[Changes made to `SKILL.md` outside the automatic application — after a regression, after a
diagnosis. Each with its commit, what it changes, and why a second textual prohibition was not the
move. The `Watch for` instruction that comes out of a correction does **not** stay here: it goes
into the `Watch for` cell of its row, which is where the next `verdetto` reads it.]

## Recidiva

[Step 7, one execution, model fixed at `claude-opus-5`. The output is the **list of pairs**, not a
scalar: a bare number hides exactly the instability that would authorise splitting the phase in two.
Every entry of both reports appears exactly once, as a pair or under the entries with no row.]

| Entry | Row | Why the defect falsifies the claim | Other rows considered |
|---|---|---|---|
| `[A#N]` | `R-[NNN]` | […] | `R-[NNN]` — [why not] / `none` |

**Entries with no row:** [`A#N` — the defect, one line. `none` is the expected answer for most
entries: the ledger covers a fraction of the skill.]

**Rows woken up:** [a dormant row raised by `recidiva` goes active again immediately. `none` if none
was.]

[A pairing is evidence, not an oversight: the reports were written with the ledger's claims in front
of them, so a pair is a defect raised **despite** the claim being visible.]

## Artifact defects with no row

[Real defects of the generated artifacts that no cycle had recorded. They are **not** regressions:
no ledger row declared them closed, so nothing was falsified. The artifacts are not modified. Say
what the defect measures on and why it is not attributable to an existing row.]

## Deviations from the procedure

[Every departure from `CONSENSUS-WORKFLOW.md` § *Il ciclo* made during this cycle, with what forced
it. A cycle that closes without documented deviations says so explicitly: *«none»* is a claim about
the procedure, and silence is not.]

---

[**How each counter is derived.** Not copied into an instance. Every line is composition over the
cycle's artifacts — no call, no judgement.]

| Counter | Derived from |
|---|---|
| `SKILL.md N → M` | `git show <commit>:skills/plan-slices/SKILL.md \| wc -l` before, working tree after |
| `entries applied` | the entries both `REVIEW`s classify as shared, minus those held back by the hard rule of bidirectional `improve` |
| `reformulations` / `reach-changes` / `additions` | the `Remedy` field of each applied entry |
| `new ledger rows` and their split by origin | the rows added to `REGRESSION-LEDGER.md` with this cycle's id, cell `Origin` |
| `re-anchored rows` | *Consequences carried into the ledger*, first list |
| `absorbed claims` | the `Absorbs` cells written this cycle |
| `active rows N → M` | rows in `REGRESSION-LEDGER.md` § *The ledger* not in state `dormant`, before and after |
| `entries discarded by the gate` | `validate_improvement.py --json`, `discards`, distinct entries over both reports |
| `discarded verdicts` | the citations of the two `VERDICTS` artifacts that do not resolve against the plan they judge |
| `recidiva` | pairs and entries of `CONSENSUS-CON-N.RECIDIVA.md` |
| `structural validator` | `make validate PLAN=…` on both candidates |

[**Artifact names.** `IMPROVEMENT` and `REVIEW` follow the convention CON-4 established.
`VERDICTS` and `RECIDIVA` are named here for the first time: no cycle has produced them yet, and the
prompts leave the path to the runner's `{{output}}` slot. Phase 5 fixes them in the orchestrator; a
cycle run by hand before then uses these.]
