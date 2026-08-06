# `verdict` — prompt for step 6 of the consensus cycle

Normative source for the `verdetto` phase. The cycle is `CONSENSUS-WORKFLOW.md` § *Il ciclo*; what
the ledger does with a falsified row, and why a discarded verdict is the thermometer of dilution, is
`workflow/LEDGER.md`. The cells this prompt renders are defined in `REGRESSION-LEDGER.md` § *How to
use*.

**Everything below the rule is the prompt. Everything above it is not sent.**

**Slots the runner fills:** `{{cycle}}` — the cycle number; `{{output}}` — the path the verdicts are
written to.

**Payload, as an allowlist:** `CANDIDATE-A.md` and `CANDIDATE-B.md` (the two generated plans,
renamed), `EVALUATION-BRIEF.md`, `sources/`, and `LEDGER-ROWS.md` — the rows to verify this cycle,
projected to `id · claim · watch for`. The projection carries **no state and no counter**: a model
told a row has survived three cycles is a model looking for it to survive a fourth. Which rows are
in the file is the runner's decision — every active row, plus the dormant ones on the one cycle in
three where they enter.

The `Watch for` cell enters as an extra instruction for its own row, and only for that row. This is
the only place the ledger says what to hunt for other than the claim itself.

---

You are checking falsifiable claims about generated delivery plans. Each claim is one row of a
ledger: it predicts something a plan either does or does not do, and it was written to be decided by
reading the plan, not by judging it.

`LEDGER-ROWS.md` holds the rows to verify. Verify **exactly those**: add none, skip none, merge
none.

`CANDIDATE-A.md` and `CANDIDATE-B.md` are the two plans just generated from the same sources.

## What you may read

`LEDGER-ROWS.md`, `CANDIDATE-A.md`, `CANDIDATE-B.md`, `EVALUATION-BRIEF.md`, the files under
`sources/`. Nothing else, in this session or in any session you delegate to.

**Authority order.** Check against `EVALUATION-BRIEF.md` first: it declares which conflicts exist,
which alternatives are acceptable and which uncertainties are material. Open the sources only to
verify a citation the brief points at. A row does not know the scenario; the brief does, and
checking a row against the sources alone has already produced a false positive that had to be
withdrawn.

## What to produce

**Two verdicts per row** — one for `CANDIDATE-A.md`, one for `CANDIDATE-B.md`. Judge each plan on
its own. Do not aggregate the two, do not conclude anything about the row overall, do not compare
the plans: a claim holds only if it holds on both, and that arithmetic is done elsewhere.

Three values, and only three:

- **`holds`** — this plan does not violate the claim.
- **`falsified`** — this plan violates it.
- **`row-defect`** — the defect is in the row, not in the plan. Admissible for exactly three
  reasons, and the one that applies must be named:
  - `not decidable from what the plan publishes`;
  - `decidable only by choosing between two readings`;
  - `contradicts the brief` — the claim denies something `EVALUATION-BRIEF.md` § *Accepted
    alternatives* allows. Quote the entry it contradicts.

`row-defect` is a real outcome, not an escape hatch: a claim that cannot be decided from a published
plan is a badly written claim, and saying so is worth more than a guess. It is not a verdict about
the plan, and it never records a regression.

## Citations are mandatory

**Every verdict cites a published point of the plan it judges — `holds` included.** A verdict whose
citation does not resolve is discarded and logged; a discarded verdict measures nothing.

Admissible forms:

- `CANDIDATE-A.md:NN` or `CANDIDATE-A.md:NN-MM`;
- `slice N Includes`, `slice N Verification`, `slice N Outcome`, `slice N Learning / risk` — a slice
  number the plan has and a field that slice carries;
- a published section and the entry inside it: `Themes`, row *«…»*; `LATER`, entry *«…»*;
  `Ordering criteria`; `Cross-functional concerns`; `Open questions`; `Decision checkpoints`;
  `Non-product work`; `OUT-OF-SCOPE`.

For `falsified`, cite the point that violates the claim. For `holds`, cite the point the verdict
rests on — the place where the violation would appear if there were one, or the point that came
closest to violating it. «I read the whole plan and saw nothing» is not a citation. For
`row-defect`, cite the point where the claim stops being decidable, or the brief entry it
contradicts.

## `Watch for`

Some rows carry a `Watch for` note. Report on it in its own field, with its own citation, separately
from the claim verdict. **A watch-for observation never changes the verdict**: it is a second thing
to look at, often the opposite failure from the one the claim describes, and it exists so that a
rule that overcorrected becomes visible. Rows without a note get `no note on this row`.

## What not to do

Do not judge the quality of either plan. Do not propose changes to the skill or to the ledger. Do
not rewrite a claim — if it is wrong, that is `row-defect` with a reason. Do not report on anything
that is not one of the rows you were given.

## Output

Write exactly one file, at `{{output}}`, in exactly this structure. Create or modify nothing else —
in particular, not the plans and not the ledger.

```
# Verdicts — cycle CON-{{cycle}}

## Inputs

- **Candidate A:** `CANDIDATE-A.md`
- **Candidate B:** `CANDIDATE-B.md`
- **Rows verified:** N

## R-NNN

- **Claim:** [copied verbatim from `LEDGER-ROWS.md`]
- **Candidate A:** `holds` | `falsified` | `row-defect — <reason>`
  - **Citation:** `…`
  - **What it shows:** [what the cited text says, and why that settles the claim]
- **Candidate B:** `holds` | `falsified` | `row-defect — <reason>`
  - **Citation:** `…`
  - **What it shows:** …
- **Watch for:** [what was found, with its own citation] | `not observed` | `no note on this row`
```

One `## R-NNN` section per row, in the order `LEDGER-ROWS.md` gives them.

Before finishing, check that: every row given has exactly two verdicts; every verdict has a citation
that resolves against the plan it judges; every `row-defect` names one of the three reasons; no
verdict aggregates the two plans; and no row absent from `LEDGER-ROWS.md` has been invented.
