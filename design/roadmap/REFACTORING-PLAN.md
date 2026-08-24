# Roadmap skill — refactoring plan

What to change in `skills/roadmap/SKILL.md`, and why, so that a later session can execute it without
reopening the argument. `ROADMAP-GOAL.md` stays the authority on intent and `CONTEXT.md` on
vocabulary; this document is a work order against them, and it is disposable once the work is done.

The lens throughout is **execution, not linear reading**: the document is a decision procedure a model
runs, not an essay a person reads once. Where the two conflict, execution wins.

## The problem

`CONTEXT-MAP.md` already declares the intended architecture — *the router in `SKILL.md`, the rules in
`references/`*. `SKILL.md` is not a router today. It is a router plus a summary of the rules plus the
rationale, at 227 lines, of which roughly 50-60 are restated from the two references and another 10
are the same invariant written four times.

Three structural faults compound it:

- **The branch condition is evaluated three times** (preamble, § 3, § 5), each time in different
  words, so the same decision is spread across the document.
- **§ 2 and § 5 reference each other in a cycle**: § 2 says the coverage question of § 5 is what
  surfaces its question; § 5 says it is asked because it triggers § 2's.
- **§ 3 and § 4 contradict each other**: § 3 says the first round of revision happens during drawing;
  § 4 opens with *every session after*.

## Target shape

```
  preamble          what a roadmap is · .roadmap/ layout · row = slice | spike
                    reference-loading policy · the write-vs-propose invariant (once)
  1  Establish the situation
  2  Choose the door
  3  Draw the map                    the Drawing door
  4  Operations on the map           the Revising door, and the argument round that follows a draw
  5  Close the session               write · validate · report
     Hand over a ready row           unnumbered: on demand, not in the progression
     The session holds when          one checklist per altitude; this is the session's
```

Target size ~150 lines (−35%). The saving is de-duplication and structure, not rationale.

## Decisions

Settled in discussion. Each is load-bearing; a session that wants to depart from one should say so
rather than drift.

**D1 — `SKILL.md` is a router.** Row-level and map-level rules stay in `references/`. Where the router
and a reference say the same thing, the router points and the reference keeps it.

**D2 — Rationale is kept where it is generative, cut where it is justificatory.** The test: *does
removing this sentence change what the agent would do on a case the document does not cover?* If yes
it stays. Generative rationale is what lets the model act in the intended direction without an
explicit instruction, and this file is mostly that — *cost and altitude are unrelated*, *a document
invites specifying and a candidate is vague on purpose*, *`archive/` means delivered and would start
lying*, *the tracker has no notion of done*. Justificatory rationale defends a rule against a human
objection and changes no decision — *a wrong branch then costs a proposal and not a record*. Cut that
without mercy; it is roughly 8-12 lines.

**D3 — Two doors, one operation table, one close.** What varies between sessions is only where the
operations come from. What they are, and how the session closes, never varies.

| Door | Condition | Operations come from | Section |
|---|---|---|---|
| `Drawing` | no map stands against a declared goal, **or** the input contradicts the recorded `Goal` | `references/drawing-the-map.md` | *Draw the map* |
| `Revising` | everything else — the goal stands; the default, by a wide margin | the five | *Operations on the map* |

`Revising` replaces `Re-truing`, which was the earlier candidate and failed on its leading word: to
*true* a wheel is to bring it back into alignment, but the first reading is *check it is still true*,
and the arm's work is mutation — it closes rows, mints ids, deletes documents. A name that reads as a
check invites under-acting. `Revising` leads with change, and its breadth matches the arm's: half of
what happens here changes membership rather than form, and *revising a document* covers both.

**`Redraw` is a condition, not a door.** A door determines exactly two things: which reference is
loaded, and which section runs. On both, a redraw answers identically to a first draw, so a third door
would branch on nothing. What genuinely differs on a redraw is keyed elsewhere and by a different
discriminator: the extra input — archive, id high-water mark, exclusions, concerns, candidates, open
rows — on *a map stands*, in `references/drawing-the-map.md`; propose-instead-of-write on *a record
stands*, per D7. Making it a door would re-evaluate a discriminator two other places already evaluate,
which is the fault this plan opens with.

The two conditions stay visible as two, because they are tested in completely different ways: the
first is a filesystem check, the second is the destination-vs-path judgement, the most error-prone
reading in the document. Two lines in the condition column, one door.

One asymmetry is real and survives: *Operations on the map* is consulted by `Drawing` too, for the
argument round. Doors are not sections. A door is a purpose and carries a purpose name; a section is a
content and carries a content name. Never use one for the other.

`Redraw` survives as the name of the case and never of a door. `CONTEXT.md:144` already defines it that
way — *il ramo di disegno che riparte con più input* — and `EVALUATION-RULES.md` R-018 and the
`fixtures/redrawn/` scenario go on using the word.

**D4 — Handover is not a door.** A session changes the map, hands over a row, or does both in that
order. A handover-only session writes nothing, so it has no close, no validator and no report.

**D5 — There is one delivery question, and it belongs to *Establish the situation*.** Today it is
written twice: § 1 (*what has been delivered is asked, never read off a tracker*) and § 4 (*ask what
was delivered*). It is asked once, at the situation step, together with anything else the situation
raises, in one round trip, and skipped when the input already answers it. Close-out then stops being
a question and is what it always was: an operation triggered by the answer. The *close-out first*
ordering rule survives untouched.

**D6 — The coverage question moves into *Operations on the map*.** On the `Drawing` door it is
vacuous: the theme ceremony, the first validators and `The map holds when` in
`references/drawing-the-map.md` *are* that door's coverage check. It earns its keep only where `NOW`
mutated under a fixed goal. Moving it also kills the § 2 ↔ § 5 cycle, because the question and the
destination-vs-path question it triggers end up in the same place.

**D7 — Write-vs-propose is one invariant, stated once in the preamble.** Its discriminator is not the
door but *does a record already stand* — nothing on disk is written unasked, anything that would
overwrite or delete a standing record is proposed in one block and confirmed once. `Close the
session` applies it and does not restate it.

**D8 — Operations are derived from the situation, or named by the author.** `ROADMAP-GOAL.md` §
*Roads not taken* currently asserts the stronger claim, that the skill refuses to ask the author to
pick the verb, and § 4 turns it into a claim about the input — *the author names none of them* —
which real sessions falsify: authors do say *split S12*, *merge these two*, *move S9 after S12*. The
accurate rule: the verb is never **required**, and when it is **given** it is a shortcut through the
same derivation, under the same rules and the same close. Update `ROADMAP-GOAL.md` in the same pass.

**D9 — `Re-true the map` becomes `Operations on the map`, and the operation `Revision` becomes
`Reshaping`.** The old section name is a purpose name where the content is a lookup table; it is rare
vocabulary, so lexical retrieval is weak; and under D3 it is simply wrong, because `Drawing` consults
the same table for its argument round. The five sub-headings — `Close-out`, `Promotion`,
`Admission`, `Retirement` — stay verbatim: they are the
anchors the evaluation rules cite. `Revision` is the exception, and it is renamed rather than kept:
nothing outside cites it — it appears at `CONTEXT.md:134` and `SKILL.md:139` and nowhere else — and it
would otherwise collide with the branch name `Revising` one altitude up. `Reshaping` is already the
verb `SKILL.md:139` defines it with, *reshapes rows without adding or closing any*, so the rename
introduces no concept. The two words then match their altitudes: `Reshaping` denotes a change of form
and that is exactly and only what the operation does, while `Revising` is broad enough to cover the
changes of membership — a row closed out, a row admitted — that the branch also holds. `Re-truing` is
dropped entirely.

**D10 — Numbers mark the progression; anchors are titles.** Steps 1-5 run in order and carry numbers;
`Hand over a ready row` and `The session holds when` carry none, which is how the reader knows they
are not in the sequence. Every reference from outside `SKILL.md` anchors on the section title and
never on the number, so the next restructuring does not cascade. See `REFACTORING-POINTERS.md`.

**D11 — `/wayfinder` goes; `/prototype` stays.** The distinction it carried is generative and stays,
the name does not: a spike goes to `/prototype` when the question needs something built to answer it;
when it is a choice to be made rather than an experiment to run, it is a conversation with the author
and no skill carries it. Applies in `SKILL.md` and in `references/slice-rules.md` § *The spike test*.

**D12 — Handover is reduced to the bone and stays in `SKILL.md`.** No new reference file. It is
descriptive, not generative, except for one clause. What survives, ~6 lines: the `readiness: ready`
precondition; a slice goes to the clarifying conversation and **not** straight to `/to-spec` — the one
generative clause, it stops the capture step inventing decisions nobody took — with the exception of a
slice already clarified in an earlier session with the outcome recorded on it; a spike goes to
`/prototype`; read `docs/agents/issue-tracker.md` when it is there. Cut: the `triage` derivation
(in `slice-rules.md` § readiness), the spike routing (`slice-rules.md` § *The spike test*), the
`size: large` routing (`slice-rules.md` § `size`).

**D13 — Do not redefine the downstream chain.** `CONTEXT-MAP.md`: *the terms of that chain are defined
by the installed skills and are not redefined here*. So `/to-spec`, `/to-tickets`, `/grill-with-docs`
and `/prototype` are named and never explained. Cut *a spec wants seams, user stories and decisions*.

**D14 — `Complete when` becomes `The session holds when`, with five items.** Three checklists look
like duplication until they have a principle; the principle is **one checklist per altitude** — the
row in `slice-rules.md` (`A row holds when`), the map in `drawing-the-map.md` (`The map holds when`),
the session here — each in the document that owns that altitude, and the rule that says where a new
item goes. What survives is only what nothing else checks: the validator checks structure, the two
references check rows and maps, and neither checks a session.

- the door was chosen by what the input claims about, work by default, and an input that cannot be
  reconciled with the recorded goal produced a question rather than an inference;
- what was delivered was asked, never read off a tracker;
- a first map was written unasked, and a standing record was proposed in one block and confirmed once
  before being written;
- the coverage question was re-asked;
- the session closed on the four-part report — themes, register, open questions, path — and nothing
  else.

**D15 — The slice-or-spike reading moves out of § 2.** It is a reading of the work, not of the
destination, so it has no business in *Choose the door*. It belongs to *Operations on the map* under
`Admission`, where a new row is created, and it is one line plus a pointer: the test itself is
`references/slice-rules.md` § *The spike test*. The note that this reading needs no confirmation —
nothing about the destination is in doubt — travels with it.

**D16 — `design/roadmap/WORKFLOWS.md` is deleted.** After the restructuring it holds nothing of its
own: the doors are the table in `SKILL.md` *Choose the door*, the scenario mapping is already at
the head of `evals/roadmap/recipe-app/SCENARIOS.md`, the intent is `ROADMAP-GOAL.md` and the terms are
`CONTEXT.md`. It declares itself non-normative, so nothing fails when it rots — it is a fourth place
describing the same structure, with no test on it. Deleting it leaves one edit: the sentence at
`CONTEXT-MAP.md:11` that cites it.

**D17 — `design/roadmap/CONTEXT.md` gains the two door terms it is missing, and renames one entry.**
The vocabulary defines the five operations and `Redraw`, whose definition already agrees with D3 —
*non è un'operazione fra le cinque: è il ramo di disegno che riparte con più input*: the drawing
branch, not one of its own. It has no term for the drawing door itself or for the default one, so
every document that needs one invents it, which is the drift `CONTEXT.md` exists to stop. Add
`Drawing` and `Revising` beside `Redraw`, in the same form as the entries around them, with the
`_Avoid_` line each needs: `Revising` is not *update*, the name of the skill split this project
rejected, and not *maintenance*. Add *porta* to `Redraw`'s own `_Avoid_` line, since under D3 it names
a case and never a door. In the same pass rename the
entry at line 134 from `Revision` to `Reshaping`, keeping its definition and its `_Avoid_` line, and
add *revision* to that `_Avoid_` line — it is now the branch one altitude up.

## De-duplication list

Cut from `SKILL.md`, keep where it already lives. Line numbers are against the current file and are
anchors, not addresses.

| Cut from `SKILL.md` | Kept in |
|---|---|
| 22-26, 95-97, 154-161, 224 — write-vs-propose, four times | preamble, once (D7) |
| 34-36 — id minting, high-water mark | `slice-rules.md` § *Identity* |
| 39-42 — the tracker has no notion of *done* | keep in the router; it is the reason for D5 |
| 67-71 — the spike test | `slice-rules.md` § *The spike test* |
| 86-89 — a redraw is this branch with more input | `drawing-the-map.md`, same title |
| 136-137 — the cap | `drawing-the-map.md` § *The cap is a finding, not a budget* |
| 139-141 — split/merge, id follows the learning target | `slice-rules.md` § *Splitting and merging a row* |
| 143-146 — retirement deletes and does not archive | `slice-rules.md` § *Identity* |
| 192-196 — `triage` derivation | `slice-rules.md` § `readiness` |
| 206-208 — spike routing | `slice-rules.md` § *The spike test* |
| 213-227 — the part of `Complete when` the reference checklists already cover | `A row holds when`, `The map holds when` |
| 18 — *the register holds rows, and a row is a slice or a spike* | said again at `slice-rules.md`:6 — keep one |

The reference-loading policy is stated once in the preamble: `slice-rules.md` on every session
whatever the input asks for, `drawing-the-map.md` on the `Drawing` door only.

## Order of work

1. `skills/roadmap/SKILL.md` — the restructuring, D1 to D15 and D17.
2. `skills/roadmap/references/slice-rules.md` — D11 only (`/wayfinder`).
3. `design/roadmap/ROADMAP-GOAL.md` § *Roads not taken* — D8.
4. Delete `design/roadmap/WORKFLOWS.md` and fix the sentence citing it at `CONTEXT-MAP.md:11`.
5. `design/roadmap/CONTEXT.md` — add `Drawing` and `Revising` beside `Redraw`, and rename `Revision`
   to `Reshaping`, per D17.
6. The inbound references, per `REFACTORING-POINTERS.md`.
7. `node skills/roadmap/scripts/validate_roadmap.ts` against an existing fixture, to confirm the
   documented invocation still matches.
8. One evaluation run per `evals/roadmap/REVIEW-WORKFLOW.md`, since every section it names moved.

## Done when

- `SKILL.md` names no rule that a reference already states, and every cut in the de-duplication list
  is either gone or has its reason recorded here;
- the branch condition is evaluated once, at *Choose the door*, and nowhere else;
- no section of `SKILL.md` references another by number, and no cycle remains between sections;
- the delivery question appears once, and `Close-out` is an operation and not a question;
- the coverage question is in *Operations on the map*;
- generative rationale is intact — spot-check the four examples named in D2;
- no reference from outside `SKILL.md` cites a section number;
- `SKILL.md` ends on `The session holds when`, and no item in it is checked by a reference checklist
  or by the validator;
- `WORKFLOWS.md` is gone and nothing points at it;
- the two doors carry the names `CONTEXT.md` defines, `Redraw` names a case and never a door, no
  section title is used as a branch name, and no word names both a branch and an operation;
- the validator runs clean and one evaluation was run against the new file.
