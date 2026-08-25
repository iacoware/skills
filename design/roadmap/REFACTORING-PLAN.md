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
     Hand over a ready row           unnumbered: runs after the close when asked for, not in the progression
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

**The round consults two of the five, and `SKILL.md:100` overstates it.** *The argument produces
exactly the operations of § 4* is false: `Close-out` never fires on a draw, and `Reshaping` and
`Retirement` are already answered one altitude down, by `slice-rules.md` § *Splitting and merging a
row* and § *Identity*, both loaded on this door anyway. What the table alone holds is `Admission` —
the two questions *does it serve the goal* and *path or speculation*, stated nowhere else — and, on a
redraw, `Promotion`: `drawing-the-map.md` gives the verdict on a `LATER` candidate and not the
mechanics of minting it. Write the pointer without *exactly*, and name the exclusion.

The alternative is to make the doors disjoint by moving what the round needs into
`drawing-the-map.md`. That duplicates `Admission` and `Promotion` across two documents, which is the
fault the de-duplication list exists to close. A one-line pointer costs less.

`Redraw` survives as the name of the case and never of a door. `CONTEXT.md:144` already defines it that
way — *il ramo di disegno che riparte con più input* — and `EVALUATION-RULES.md` R-018 and the
`fixtures/redrawn/` scenario go on using the word.

**D4 — Handover is not a door; it composes with one.** A session changes the map,
hands over a row, or does both in that order. Handover therefore **composes**, where a door is an
**exclusive alternative**, and the composed case has nowhere to sit in a three-door table: either it is
lost, or it runs through `Revising` and ends in handover, and the same activity is then reached two
ways — the fault this plan opens with. Handover also decides neither of the two things D3 says a door
decides: it loads no reference — no new file per D12, and `slice-rules.md` is loaded every session
regardless — and it is not an alternative to the map-changing section.

So *Choose the door* picks a door, always, and handover is a second and independent reading of the
same input: **does it ask for a row to hand over?** If yes, *Hand over a ready row* runs **after** the
close, never instead of it.

**There is no handover-only arm.** An earlier draft of this decision routed a session that changes
nothing straight to the handover, skipping the close, the validator and the report. It is cut, and the
ground is the one `ROADMAP-GOAL.md` states about promotion triggers and decision checkpoints — *no
field nobody re-reads*, and anything of that family gets dropped the same way. A routing branch no
prompt exercises and no fixture can exercise is that defect in routing form. What it bought comes free
anyway: a session that finds nothing to change **writes nothing**, so there is no block to confirm and
nothing for the validator to check, and the close degrades on its own — the *degrades cleanly*
property `ROADMAP-GOAL.md` already claims for the skill. The saving was one round trip; the cost was a
row handed over against a register nobody resynchronised, when `Close-out` **asking** is the only
resynchronisation the skill has.

**Handover stays uncovered by the evaluation net either way.** `evals/roadmap/README.md:33` records
that no prompt has ever requested a handover and no fixture holds an open row to hand over, so the run
at the end of the order of work will not exercise this section. That is the reason D12 shrinks it
rather than elaborating it. Declared, not discovered later.

**D5 — There is one delivery question, and it belongs to *Establish the situation*.** Today it is
written twice: § 1 (*what has been delivered is asked, never read off a tracker*) and § 4 (*ask what
was delivered*). It is asked once, at the situation step, together with anything else the situation
raises, in one round trip, and skipped when the input already answers it. Close-out then stops being
a question and is what it always was: an operation triggered by the answer. The *close-out first*
ordering rule survives untouched.

**D6 — The coverage question moves into *Operations on the map*.** On the `Drawing` door it is
vacuous: the theme ceremony, the first validators and `The map holds when` in
`references/drawing-the-map.md` *are* that door's coverage check. It earns its keep only where `NOW`
mutated under a fixed goal. Moving it does not by itself kill the § 2 ↔ § 5 cycle. The
destination-vs-path question stays in *Choose the door* — D3's table, D14's first item and
`REFACTORING-POINTERS.md` lines 48, 54 and 57 all put it there — so an unqualified move renames the
cycle *Operations on the map* ↔ *Choose the door* and changes nothing else.

What kills it is a rule on the backward edge: **a failed coverage check never reopens the door
mid-session.** It produces a question, the question is delivered at the close, and the next session
picks `Drawing` if the answer requires it. The door is decided once, on the input, at the start.
*Operations on the map* may then cite *Choose the door* for where the criterion comes from, and
*Choose the door* cites nothing forward.

**The question runs last in *Operations on the map*, after all five operations**, because it
interrogates the state `NOW` was left in. That section is the only one with a declared internal order
— *Close-out first* — so the position of a question arriving into it is stated rather than left to
fall where it may.

**D7 — Write-vs-propose is one invariant, stated once in the preamble.** Its discriminator is not the
door but *does a record already stand* — nothing on disk is written unasked, anything that would
overwrite or delete a standing record is proposed in one block and confirmed once. `Close the
session` applies it and does not restate it.

**The preamble also separates the two round trips, by purpose and not by count.** A `Revising` session
against a standing map stops twice, and must: the delivery question of D5 cannot wait for the close,
because `Close-out` is the first operation and everything else is decided against a register already
trued up; and the confirmation cannot come early, because the block it confirms does not exist yet.
Stated as *one confirmation* alone, the invariant reads as *one interaction* and fails silently in
either direction — the delivery question folded into the closing block, so the whole session was
decided against a stale register; or the situation round trip taken for the confirmation, so a
standing record is overwritten with nobody having said yes. So: **the situation round trip gathers
facts, writes nothing, and is skipped when the input already answers it; the confirmation round trip
presents one block of proposed writes and collects one yes.** *One confirmation, never split across
several questions* governs the second, not the number of times the session speaks to the author. A
session that finds nothing to change never reaches the second, because it has no block to confirm.

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

**D10 — Numbers mark position; anchors are titles.** They mark position in the document and reading
order, **not a sequence every session runs**: steps 3 and 4 are the two doors' alternatives, so nothing
executes 1-2-3-4-5. `Drawing` runs 1, 2, 3, consults 4 for the argument round, then 5; `Revising` runs
1, 2, 4, 5 and never enters 3; a handover, when the input asks for one, follows 5. *Choose the door* is what says
which of 3 and 4 runs. Steps carry numbers; `Hand over a ready row` and `The session holds when` carry
none, which is how the reader knows they are not in the sequence. Every reference from outside `SKILL.md` anchors on the section title and
never on the number, so the next restructuring does not cascade. See `REFACTORING-POINTERS.md`.

**D11 — `/wayfinder` goes; `/prototype` stays.** The distinction it carried is generative and stays,
the name does not: a spike goes to `/prototype` when the question needs something built to answer it;
when it is a choice to be made rather than an experiment to run, it is a conversation with the author
and no skill carries it.

**It applies in four files, not two.** `SKILL.md` and `references/slice-rules.md` § *The spike test*
are the obvious pair. The other two are `evals/roadmap/EVALUATION-RULES.md` R-034, which names
`/wayfinder` twice — for the big-and-foggy slice and for the spike that is a choice rather than an
experiment — and which judges the handover, so leaving it would fail the rewritten `SKILL.md` at the
evaluation run and read as a defect of the work; and `design/roadmap/ROADMAP-GOAL.md` at line 78
(*`needs-decision` feeds `wayfinder`*) and line 103 (the downstream chain diagram).

**D12 — Handover is reduced to the bone and stays in `SKILL.md`.** No new reference file. **What it
produces is a message to the author: it suggests and never drives** — say so, because this decision
moves the message's own parts out. The destination by `kind` comes from `slice-rules.md` § *The spike
test*, the destination by `size` from § `size`, the `triage` label from § `readiness`; the delegation
is safe only because that file is loaded on every session, and what has to survive in `SKILL.md` is
the instruction to assemble them into one message. It is descriptive, not generative, except for one
clause. What survives, ~6 lines: the `readiness: ready`
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
- on `Revising`, the coverage question was asked, and it produced a question rather than a change of
  door;
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

**D18 — `references/drawing-the-map.md` states its scope by door, and its first section stops arguing
routing.** Three edits, all small, all consequences of D3.

- **The preamble contradicts its own second section.** Line 3 says *loaded when a goal is declared and
  no map stands against it*; line 10 says *a new goal declared against a map that already exists is
  drawn here*. The declared condition excludes half the cases that load the file, and that — not the
  file boundary — is what makes the redraw content read as foreign matter in a document named for
  drawing. Restate it by door: loaded on `Drawing`, whether or not a map stands; everything here
  decides the shape of the whole map, and none of it fires on `Revising`.
- **`## A redraw is this branch with more input` becomes `## What carries when a map already stands`.**
  The old title argues a routing decision inside a content document — router vocabulary one altitude
  down — and under D3 the router already settles the condition. Cut *There is no separate mode and no
  reconciliation logic* in the same pass: justificatory under D2. The rest of the section is generative
  and stays verbatim, the word *redraw* in its body included.
- **`door` is the router's word now, so the reference stops using it for something else.** *What the
  map reports about its input* has *every entry then leaves by one of three doors* for a disposition —
  an `Assumptions` line, an `Open questions` line, a spike. Same word, two altitudes, two files, one
  skill. Say *exits* there.

**The file is not split.** The redraw content is not a parallel procedure but a modifier of the inputs
of every section downstream — the archive constrains the themes, the high-water mark constrains the
ids, `OUT-OF-SCOPE` and the concerns constrain the ordering, `LATER` constrains promotion, the open
rows constrain retirement. A cross-cutting preface extracted into a sibling raises distance on high
integration strength, and the sibling would never be loaded alone: the `Drawing` door would load both
files every time, which makes it a chapter and not a module. Distributing it into the five sections it
modifies is worse still — one check read once becomes five checks scattered. Conditional sections are
already the norm in that file: *The two prerequisites* fires only on greenfield.

## De-duplication list

Cut from `SKILL.md`, keep where it already lives. Line numbers are against the current file and are
anchors, not addresses.

| Cut from `SKILL.md` | Kept in |
|---|---|
| 22-26, 95-97, 154-161, 224 — write-vs-propose, four times | preamble, once (D7) |
| 34-36 — id minting, high-water mark | `slice-rules.md` § *Identity* |
| 67-71 — the spike test | `slice-rules.md` § *The spike test* |
| 86-89 — a redraw is this branch with more input | `drawing-the-map.md` § *What carries when a map already stands* (D18) |
| 136-137 — the cap | `drawing-the-map.md` § *The cap is a finding, not a budget* |
| 139-141 — split/merge, id follows the learning target | `slice-rules.md` § *Splitting and merging a row* |
| 143-146 — retirement deletes and does not archive | `slice-rules.md` § *Identity* |
| 192-196 — `triage` derivation | `slice-rules.md` § `readiness` |
| 206-208 — spike routing | `slice-rules.md` § *The spike test* |
| 213-227 — the part of `Complete when` the reference checklists already cover | `A row holds when`, `The map holds when` |
| 18 — the sentence introducing the register, minus the row vocabulary | `slice-rules.md`:6 says the rest |

**Two things in this section are not cuts, and the table no longer implies they are.** *The tracker
has no notion of `done`* at 39-42 stays in the router: it is the reason D5 puts the delivery question
at *Establish the situation*, and no reference states it. And *a row is a slice or a spike* stays in
the preamble rather than being pointed at, per *Target shape*: it is the vocabulary the door table and
the operations are written in, needed before any reference is loaded, and one sentence of duplication
is cheaper than the pointer that would replace it. What leaves 18 is only the surrounding sentence
about the register, which `slice-rules.md`:6 already carries.

The reference-loading policy is stated once in the preamble: `slice-rules.md` on every session
whatever the input asks for, `drawing-the-map.md` on the `Drawing` door only.

## Order of work

1. `skills/roadmap/SKILL.md` — the restructuring, D1 to D15.
2. `skills/roadmap/references/drawing-the-map.md` — D18: the preamble, the section title, *exits*.
3. `skills/roadmap/references/slice-rules.md` — D11 only (`/wayfinder`).
4. `design/roadmap/ROADMAP-GOAL.md` — § *Roads not taken* for D8, and lines 78 and 103 for D11.
5. `evals/roadmap/EVALUATION-RULES.md` — R-034 for D11, which names `/wayfinder` twice and is the rule
   that judges the handover.
6. Delete `design/roadmap/WORKFLOWS.md` and fix the sentence citing it at `CONTEXT-MAP.md:11` — D16.
7. `design/roadmap/CONTEXT.md` — add `Drawing` and `Revising` beside `Redraw`, adjust `Redraw`'s
   `_Avoid_`, and rename `Revision` to `Reshaping`, per D17.
8. The inbound references, per `REFACTORING-POINTERS.md`, its own line 13 included: it repeats the
   *steps 1-5 run in order* claim D10 now corrects.
9. `node skills/roadmap/scripts/validate_roadmap.ts` against an existing fixture, to confirm the
   documented invocation still matches.
10. One evaluation run per `evals/roadmap/REVIEW-WORKFLOW.md`, since every section it names moved.

## Done when

- `SKILL.md` names no rule that a reference already states, and every cut in the de-duplication list
  is either gone or has its reason recorded here;
- the branch condition is evaluated once, at *Choose the door*, and nowhere else;
- no section of `SKILL.md` references another by number, and no cycle remains between sections;
- the delivery question appears once, and `Close-out` is an operation and not a question;
- the coverage question is last in *Operations on the map*, and a failed one produces a question and
  never a change of door;
- *Hand over a ready row* runs after the close and never instead of it, and a session that changes
  nothing writes nothing, so no confirmation and no validator fire;
- generative rationale is intact — spot-check the four examples named in D2;
- no reference from outside `SKILL.md` cites a section number;
- `SKILL.md` ends on `The session holds when`, and no item in it is checked by a reference checklist
  or by the validator;
- `WORKFLOWS.md` is gone and nothing points at it;
- the two doors carry the names `CONTEXT.md` defines, `Redraw` names a case and never a door, no
  section title is used as a branch name, and no word names both a branch and an operation;
- the pointer from *Draw the map* to *Operations on the map* names the operation the argument round
  excludes, and does not claim it runs all five;
- `drawing-the-map.md` opens by naming the door it serves, its first section no longer contradicts
  that opening, and `door` appears in the skill at one altitude only;
- the validator runs clean and one evaluation was run against the new file.
