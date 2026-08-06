# `review` — prompt for step 5 of the consensus cycle

Normative source for the `review` phase. The cycle is `CONSENSUS-WORKFLOW.md` § *Il ciclo*; what the
workflow does with the four categories is `workflow/CYCLE.md` § *Cosa il workflow applica da sé e
cosa no*.

**Everything below the rule is the prompt. Everything above it is not sent.**

**Slots the runner fills:** `{{cycle}}` — the cycle number; `{{output}}` — the path the review is
written to.

**Payload, as an allowlist:** `REPORT-A.md` and `REPORT-B.md`, the two conforming `improve`
documents, renamed. Nothing else — not the plans, not the sources, not the brief, not `SKILL.md`,
not the ledger. The payload is **symmetric**: the two executions of this phase receive the same two
files under the same two names, and neither is told which one it wrote. `Report A` here need not be
the same side as `Candidate A` in `improve`; the mapping is held outside every payload.

The one field the rest of the cycle cannot do without is `Same remedy`. It is what separates
`intersection` from `intersection-theme`, and an entry classified shared by only one of the two
executions is the instability measure the report publishes.

---

Two improvement reports on the same skill were written independently, from the same pair of
generated delivery plans. They are `REPORT-A.md` and `REPORT-B.md`. **Neither of them is yours**: do
not try to work out who wrote which, and do not write about either from the inside.

Compare them and classify every entry of both into exactly one of four categories.

## What you may read

`REPORT-A.md` and `REPORT-B.md`, and nothing else, in this session or in any session you delegate
to. Do not open the plans they cite, the sources, the brief, the skill, the ledger, or any earlier
review.

**The entries are already verified.** Do not re-adjudicate whether an entry is correct, whether its
evidence holds, or whether the change it proposes is a good idea. This phase decides one thing:
what the two reports agree on. Nothing here licenses a judgement on the merits.

## How to classify

Compare by meaning, not by wording. Normalize each entry to the defect it raises and the rule it
proposes, then place it.

1. **Present in both reports** — both raise the same defect.
2. **Only in report A.**
3. **Only in report B.**
4. **Contradictory** — both raise the same defect and propose remedies that cannot both be applied.

Rules, each of which has produced a misclassification before:

- Different wording is not by itself a unilateral entry.
- A greater level of detail is not by itself a unilateral entry.
- Implementation differences that can coexist are not a contradiction.
- Same defect, compatible remedies → shared, and the differences are described.
- Same defect, remedies that cannot both hold → contradictory, and **only** contradictory.
- Every entry lands in exactly one category. Never repeat an entry across sections.

**Entry ids.** Entries are numbered in their own report. Refer to them as `A#N` and `B#N`, and make
every id of both reports appear exactly once across the five sections below. The ids are what the
rest of the cycle pairs on.

**`Same remedy`, for every shared entry.** `yes` when the two reports' `Change to the skill` fields
would produce the same normative rule — same reach, same thing required of a plan — even if worded
differently. `no` when the two see the same defect and propose different rules. When `no`, name
which side carries the remedy that a human would apply, and why that one. Detail is not a reason;
being decidable on a generated plan is.

**Out of scope.** The walking skeleton is excluded from this cycle. If an entry raises a
walking-skeleton defect, do not classify it: list its id under `## Out of scope` so the accounting
stays complete, and say nothing else about it.

## Output

Write exactly one file, at `{{output}}`, in exactly this structure. Create or modify nothing else.

```
# Review of the improvement reports — cycle CON-{{cycle}}

## Inputs

- **Report A:** `REPORT-A.md` — N entries
- **Report B:** `REPORT-B.md` — N entries

## Entries present in both reports

### [the normalized entry, one line]

- **Entries:** `A#N`, `B#N`
- **In report A:** …
- **In report B:** …
- **Shared defect:** …
- **Same remedy:** `yes` | `no` — [why]
- **Remedy carried by:** `A` | `B` — [why that side] | `both` when `Same remedy` is `yes`
- **Differences:** …

## Entries present only in report A

### [the entry, one line]

- **Entry:** `A#N`
- **What it raises:** …
- **What report B does instead at that point:** …

## Entries present only in report B

### [the entry, one line]

- **Entry:** `B#N`
- **What it raises:** …
- **What report A does instead at that point:** …

## Contradictory entries

### [the area of the conflict]

- **Entries:** `A#N`, `B#N`
- **Report A:** …
- **Report B:** …
- **Conflict:** [why the two remedies cannot both be applied]
- **Suggested resolution:** …

## Out of scope

- `A#N` — walking skeleton

## Summary

- **Shared:** N — of which same remedy: N
- **Only in report A:** N
- **Only in report B:** N
- **Contradictory:** N
- **Out of scope:** N
```

For a section with nothing in it, write exactly `None identified.` and no more. Add no further
sections.

Before finishing, check that: every entry id of both reports appears exactly once; the counts in
`Summary` match the sections; no entry sits in two categories; no report is described as yours; and
no plan, source, skill or improvement document has been read or modified.
