Every file you may read is under `/Users/iacoware/projects/iacoware/skills/evals/plan-slices/recipe-app/payloads/CON-6/verdict/`, under the names used below.
Read nothing outside that directory; write nothing outside the output path below.

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

Write exactly one file, at `/Users/iacoware/projects/iacoware/skills/evals/plan-slices/recipe-app/payloads/CON-6/out-verdict/CC/PLAN-CC-CON-6.VERDICTS.md`, in exactly this structure. Create or modify nothing else —
in particular, not the plans and not the ledger.

```
# Verdicts — cycle CON-6

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
