# Inbound references to `SKILL.md`

Everything outside `skills/roadmap/SKILL.md` that points into it, and where each pointer lands after
the restructuring in [`REFACTORING-PLAN.md`](./REFACTORING-PLAN.md). A burn-down list: it exists to be
worked through and then deleted.

## The convention this establishes

**Anchor on the section title, never on the number.** `EVALUATION-RULES.md` already cites most
sections as number *plus* title — `§ 4, *Retirement*` — so dropping the number costs nothing and buys
immunity from the next restructuring. Numbers stay inside `SKILL.md`, where they signal that steps 1
to 5 run in order; they do not travel.

Write `*Operations on the map*, *Retirement*` — the section title, then the sub-heading when the
reference is to one.

## Sub-headings that must survive verbatim

The rewrite may move these, but not rename them: something outside cites each one by name.

`Destination or path` · `When the input cannot be reconciled` · `Close-out` · `Promotion` ·
`Admission` · `Revision` · `Retirement` · `Then absorb the evidence` · `Run the validator`

## Section mapping

| Now | After |
|---|---|
| § 1 *Establish the situation* | 1. *Establish the situation* — unchanged |
| § 2 *Read what the input claims about* | 2. *Choose the door* |
| § 3 *Draw the map* | 3. *Draw the map* — unchanged |
| § 4 *Re-true the map* | 4. *Operations on the map* |
| § 5 *Close the session* | 5. *Close the session* — the coverage question leaves for § 4 |
| § 6 *Hand over a ready row* | *Hand over a ready row* — unnumbered |

## The references

### `evals/roadmap/EVALUATION-RULES.md` — 19 references

| Line | Cites | Becomes |
|---|---|---|
| 40 | § 1 | *Establish the situation* |
| 42 | § 1, § 4 | **retarget** → `slice-rules.md` *Identity* only; id minting leaves the router |
| 48 | § 2, *Destination or path* | *Choose the door*, *Destination or path* |
| 54 | § 2, *Destination or path* | *Choose the door*, *Destination or path* |
| 57 | § 2, *When the input cannot be reconciled* | *Choose the door*, same sub-heading |
| 64 | § 4, *Promotion* and *Admission* | *Operations on the map*, same sub-headings |
| 67 | § 2, *Slice or spike* | **retarget** → *Operations on the map*, *Admission* (see D15) |
| 79 | § 3 | *Draw the map* |
| 125 | § 3 | *Draw the map* |
| 155 | § 4 *Admission* | *Operations on the map*, *Admission* |
| 165 | § 4 | *Operations on the map*, *Close-out* |
| 170 | § 4, *Then absorb the evidence* | *Operations on the map*, same sub-heading |
| 173 | § 4, *Retirement* | *Operations on the map*, *Retirement* |
| 176 | § 4 *Admission* | *Operations on the map*, *Admission* |
| 182 | § 5 | *Close the session* |
| 186 | § 5 | **retarget** → the preamble; the write-vs-propose invariant moves there (D7) |
| 188 | § 5, *Run the validator* | *Close the session*, same sub-heading |
| 195 | § 6 | *Hand over a ready row* |
| 199 | § 5 | *Close the session* |

Line 24 also states the rule this plan follows — *never in `SKILL.md` by default, which is how a
router grows back into a monolith*. Nothing to change; it is the standard the result is judged by.

### `evals/roadmap/REVIEW-WORKFLOW.md` — 5 references

| Line | Cites | Becomes |
|---|---|---|
| 13 | § 1, § 3, § 5 | *Establish the situation*, *Draw the map*, *Close the session* |
| 16 | § 2, § 4 | *Choose the door*, *Operations on the map* |
| 19 | § 6 | *Hand over a ready row* |
| 75 | § 1 obliges the session to ask what was delivered | *Establish the situation* — D5 makes this the only place it is asked |
| 96 | the validator at § 5 | *Close the session*, *Run the validator* |

### `evals/roadmap/README.md` — 1 reference

Line 33: *§ 6 has never been asked for* → *Hand over a ready row*. The observation stands: no prompt
requests a handover and no fixture holds an open `ready` row, which is why D12 shrinks it rather than
elaborating it.

### `design/roadmap/WORKFLOWS.md` — 3 references, all deleted with the file

Lines 12, 17 and 27 cite § 3, § 4 and § 6. The file goes (D16), so the pointers go with it and nothing
is patched.

### `CONTEXT-MAP.md` — 1 sentence

Line 11 cites `WORKFLOWS.md` as the map of the four session shapes. Rewrite it to point at
`SKILL.md` *Choose the door*, which is where the doors are stated normatively.

### No section anchors

`design/roadmap/CONTEXT.md` points at files, not sections, and at the router/rules
split that this work restores. `scripts/validate_roadmap.ts:612` mentions the invocation `SKILL.md`
prescribes; the command does not change. `evals/roadmap/PROMPTS.md:65` forbids editing `SKILL.md`
during an evaluation session, which is a constraint on running the evals, not a pointer.
