# `recidiva` — prompt for step 7 of the consensus cycle

Normative source for the `recidiva` phase. Why it is a single call, on a fixed model, and the two
events that would reverse that decision: `workflow/LEDGER.md` § *Perché `recidiva` è una sola
chiamata*.

**Everything below the rule is the prompt. Everything above it is not sent.**

**Slots the runner fills:** `{{cycle}}` — the cycle number; `{{output}}` — the path the pairings are
written to.

**One execution per cycle**, model fixed at `claude-opus-5`, declared in the `Measured on` cell of
every row it touches. Changing the model is a tool boundary. This phase is a thermometer, not a
filter: it decides nothing that enters the skill, so it does not get the two-sided consensus rule.

**Payload, as an allowlist:** `REPORT-A.md` and `REPORT-B.md`, the two conforming `improve`
documents, and `ROWS.md` — **every** ledger row, dormant included, projected to `id · claim`. No
state, no counter, no dormancy flag: which rows are dormant is what the report decides afterwards
from the pairings, and a model told a row is asleep has been told which answer is cheap.

The output is the **list of pairs**, never a number. A bare scalar would hide exactly the
instability — same entry, same row, different verdict across cycles with unchanged artifacts — that
is one of the two events that would turn this phase into two calls.

---

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
ledger. Do not compare the two reports with each other. Do not count, do not compute a rate, do not
state a total anywhere.

## Output

Write exactly one file, at `{{output}}`, in exactly this structure. Create or modify nothing else.

```
# Recidiva — cycle CON-{{cycle}}

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
count, rate or total appears anywhere in the document.
