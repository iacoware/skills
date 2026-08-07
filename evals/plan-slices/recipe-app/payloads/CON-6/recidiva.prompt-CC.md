Every file you may read is under `/Users/iacoware/projects/iacoware/skills/evals/plan-slices/recipe-app/payloads/CON-6/recidiva/`, under the names used below.
Read nothing outside that directory; write nothing outside the output path below.

Two improvement reports were written this cycle, from defects observed in two freshly generated
delivery plans. `ROWS.md` holds a ledger of falsifiable claims about such plans: every row is a
prediction that a defect, once corrected, does not come back.

**Pair every entry of both reports with the row whose claim its defect would falsify, or with
`none`.** That is the whole task.

A pair means the ledger predicted that defect away and a report raised it anyway. The reports were
written with these claims in front of them, so a pair is a defect raised **despite** the claim being
visible — evidence, not an oversight.

## What you may read

`REPORT-A.md`, `REPORT-B.md`, `ROWS.md`. Nothing else, in this session or in any session you
delegate to — not the plans the reports cite, not the sources, not the brief, not the skill.

## How to pair

- **Pair by defect, not by wording.** An entry pairs with a row when the defect the entry describes,
  occurring on a generated plan, would falsify that row's claim. Shared vocabulary is not a pairing;
  a shared theme with claims that could both hold is not a pairing.
- **At most one row per entry.** Where several rows are candidates, pair with the one whose claim
  the defect most directly falsifies, and list the others under `Other rows considered` with why
  they are not the pair. Rows listed there are not pairs.
- **`none` is the expected answer for most entries**, and is not a failure of anything. An entry
  raising a defect no row predicted away is the ordinary case: the ledger covers a fraction of the
  skill.
- **Every entry of both reports is accounted for**, exactly once, either as a pair or under
  `Entries with no row`. Use the ids the reports number their entries with: `A#N`, `B#N`.

## What not to do

Do not judge whether an entry is correct, whether its evidence holds, or whether its remedy is a
good idea. Do not judge whether a row is well written. Do not propose changes to the skill or to the
ledger. Do not compare the two reports with each other. Do not count the pairings, do not compute a
rate over them, do not state a total of them anywhere — the three sizes the `Inputs` block asks for
are the only numbers this document carries.

## Output

Write exactly one file, at `/Users/iacoware/projects/iacoware/skills/evals/plan-slices/recipe-app/payloads/CON-6/out-recidiva/CONSENSUS-CON-6.RECIDIVA.md`, in exactly this structure. Create or modify nothing else.

```
# Recidiva — cycle CON-6

## Inputs

- **Report A:** `REPORT-A.md` — N entries
- **Report B:** `REPORT-B.md` — N entries
- **Rows considered:** N

## Pairs

### `A#N` → `R-NNN`

- **Entry:** [the defect the entry raises, one line]
- **Row claim:** [copied verbatim from `ROWS.md`]
- **Why the defect falsifies the claim:** …
- **Other rows considered:** `R-NNN` — [why not the pair] | `none`

## Entries with no row

- `A#N` — [the defect, one line]
- `B#N` — [the defect, one line]
```

For a section with nothing in it, write exactly `None identified.` and no more.

Before finishing, check that: every entry id of both reports appears exactly once across the two
sections; every pair names a row that `ROWS.md` holds; no entry carries more than one pair; and no
number other than the three sizes of the `Inputs` block appears anywhere in the document.
