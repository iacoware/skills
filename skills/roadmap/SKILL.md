---
name: roadmap
description: The living roadmap of a project against a declared goal — the vertical slices and spikes that reach it, kept true as work is delivered, discovered, reshaped and dropped.
license: MIT
disable-model-invocation: true
---

# Roadmap

A roadmap is a sense-making tool, not a precision instrument. It lets the author say *these are the
rows that get me to the goal*, and then argue with that sentence. No dates, no estimates, no
percentage complete, no field nobody re-reads.

It lives in `.roadmap/`: `roadmap.md` is the readable overview, `slices/S<id>-<slug>.md` one document
per open row, `archive/S<id>-<slug>.md` one per delivered row. One roadmap per project, serving one
declared `Goal` at a time.

The register holds rows, and a row is a slice or a spike. What makes a row valid is in
[references/slice-rules.md](references/slice-rules.md); read it at the start of every session,
whatever the input asks for.

**A first map is written; a map that already stands is proposed.** With no `.roadmap/` there is
nothing to lose and nothing to describe: the author argues with the file far faster than with an
account of it, so it gets written straight away. Once a map exists, every change waits for one
confirmation before it touches the record — a session rewrites rows other sessions wrote, and deletes
documents, and that is worth a round trip.

## 1. Establish the situation

Read before deciding anything:

- whether `.roadmap/roadmap.md` is there, and if it is, its `Goal`, its themes, its register,
  `Assumptions`, `Open questions`, `Cross-functional concerns`, `LATER` and `OUT-OF-SCOPE`;
- `.roadmap/slices/` and `.roadmap/archive/`, which give the open documents, what was delivered, and
  the id high-water mark — the highest id across both, and the next id is that plus one;
- the sources the input points at, and `docs/agents/issue-tracker.md` when it is there.

**What has been delivered since the last session is asked, never read off a tracker.** A local
tracker has no notion of *done*: nothing writes it, and a board of open tickets says nothing about
what shipped. Close-out is an explicitly manual resynchronisation, and asking is the only thing that
works.

When there is no `.roadmap/` and no goal in the input either, the goal is what to ask for first.
There is nothing to draw a map against and nothing to ask *do these rows arrive anywhere* of.

## 2. Read what the input claims about

Two readings run on the same input.

**Destination or path.** A claim about *where we are going* that contradicts the recorded `Goal`
draws the map again. A claim about *how we get there* is work, and leaves the goal alone. Work is the
default and by a wide margin: admission, promotion, revision, close-out and retirement all leave the
goal where it is. A new capability extends the existing roadmap; it does not open a second one.

Two traps, one in each direction:

- **Widening the reach of a capability the goal already promises sounds structural and is work.** The
  destination has not moved; how far the promise reaches is a detail of the path, and is often
  already sitting in `LATER` as a candidate.
- **A change of one line can move the destination.** How cheap something is to implement says nothing
  about whether it moves the destination: cost and altitude are unrelated, and only the second is the
  roadmap's business. The tell is what it contradicts — an invariant under `Cross-functional
  concerns`, or an exclusion under `OUT-OF-SCOPE`, neither of which a small feature is entitled to
  overrule on its own.

**Slice or spike.** Work that produces an outcome is a slice; work that produces knowledge is a
spike. The tell is the honest `Verification`: when it states a measurement rather than a capability
somebody can exercise, it is a spike. `references/slice-rules.md` holds the test and what a spike
owes — an empty `Audience`, and a dependent.

**When the input cannot be reconciled with the recorded goal — it does not serve it, and it is not an
exclusion either — ask.** State the goal on file, state what the input looks like from where the map
sits, ask which of the two holds. A question with a short answer, never an inference. The coverage
question in § 5 is what surfaces this, and it runs every session.

The slice-or-spike reading needs no question: nothing about the destination is in doubt, so the spike
goes in with the rest of the session's changes.

## 3. Draw the map

When a goal is declared and no map stands against it. Load
[references/drawing-the-map.md](references/drawing-the-map.md) — themes, the two prerequisites,
ordering, the identity seam, and what the map reports about its own input — and follow it.

A **redraw** is this branch with more input, not a separate mode: what the previous goal left behind
— the archive, the id high-water mark, the exclusions, the concerns, the candidates, the rows still
open — enters as a constraint exactly the way a source document does. That reference says what
carries and what is redrawn from nothing.

Write `roadmap.md` from [assets/roadmap-template.md](assets/roadmap-template.md) and one document per
`NOW` row from [assets/slice-template.md](assets/slice-template.md). Keep the headings, field names
and order; write the content in the author's language.

**A first draw writes them; a redraw waits.** With nothing on disk the map goes down unasked. A redraw
has a standing map underneath it — rows it retires, documents it deletes, a goal it replaces — so it
is proposed under § 5 like any other change to an existing record, and written once confirmed.

**Drawing does not end when the map is down.** A first map is a draft to argue with, and the
argument produces exactly the operations of § 4 — split this one, drop that part, swap the order. So
the first round of revision happens here, in the same session, before § 5.

## 4. Re-true the map

Every session after. Five operations, and **the author names none of them**: they arrive with a
situation — *that one is finished, it turned out the numbers are nothing like we assumed, and here is
something nobody had thought of* — and which of the five apply is derived from it. The names below
are internal vocabulary, enough to order the work. Nothing here is a verb anybody types.

**Close-out first**, because everything else is decided against a register already trued up. Ask what
was delivered. Its row leaves the register, its document moves to `.roadmap/archive/` unchanged, and
its `ADRs` reference is filled when the work produced a decision that cleared the bar: hard to
reverse, surprising without context, the result of a real trade-off.

Then absorb the evidence, which is a state change and never a summary. Three questions:

1. **Does it settle a line in `Assumptions` or `Open questions`?** The line then dies rather than
   being annotated — it has been answered.
2. **Does it change another row?** A size that was wrong, a readiness that can flip, a `Depends on`
   gone moot, a shape that has to split. This is where the value is.
3. **Does it produce a decision that clears the ADR bar?** That is what the archived document's
   `ADRs` reference is for.

**Three noes write nothing.** A paragraph produced to prove the step happened is the ceremony this
tool refuses. On a spike three noes mean it taught nothing, and that is a finding about the spike.

**Promotion** turns a candidate into a row: it mints the next id, writes the row into the register
and the document into `slices/`, and `Requested by` records what produced it. `Spec` and `Tickets`
are filled here when they exist and read `—` until then.

**Admission** is new work entering, and it asks two questions in order. *Does it serve the goal?* If
not, it is an `OUT-OF-SCOPE` line with its licence, or nothing at all. *Is it on the path, or is it
speculation?* Speculation is a `LATER` line and nothing more — no id, no columns, no document,
because a document invites specifying and a candidate is vague on purpose, and no `Requested by`
either, since provenance is recorded at promotion. On the path, it is admitted straight into `NOW`
with an id. Then check the cap: an admission that would overflow it forces a merge or a deferral, and
the list does not grow.

**Revision** reshapes rows without adding or closing any: split, merge, rewrite, reorder. The id
stays with the learning target through a split or a merge, and the behaviour set is conserved — see
`references/slice-rules.md`.

**Retirement** takes a row out of `NOW` undelivered: it dies, or it goes back to `LATER` as a
candidate. The id is spent and never returns, and the document is **deleted, not archived** —
`archive/` means delivered and would start lying the moment it held something that was not.

## 5. Close the session

Both branches close here, and only the writing step tells them apart.

**Re-ask the coverage question:** does what is left in `NOW` still reach the goal? Usually the answer
is one line. It is asked anyway, because it is also the trigger for the question in § 2.

**Then write, or propose and write — according to what stood at the start of the session.**

- **Nothing stood.** § 3 has already written the map. There is nothing to confirm; go straight to the
  validator.
- **A map stood** — a re-true, or a redraw against a new goal. Propose every operation the session
  found in one block, ask for confirmation once, and write the block only then. Not five files written
  one at a time with a question between each, and never one proposal split across several questions. A
  wrong branch then costs a proposal and not a record.

**Run the validator** after writing. Resolve `<skill-dir>` to the absolute path of the directory
holding this `SKILL.md`; the working directory is the author's project.

```bash
node <skill-dir>/scripts/validate_roadmap.ts .roadmap
```

Node 23.6 and later run it as is; 22.6 to 23.5 need `--experimental-strip-types`. It checks
structure and references — that every row resolves to its document and back, that `Depends on`
resolves, that no id was recycled, that a spike has a dependent — and never judgement. Fix every
`ERROR`. A `WARNING` is a signal to the author: the cap and the floor are findings to discuss, not
defects to silence.

**Then report the written map, and nothing else.** Four things, in this order, read off the files as
they now stand:

1. the `Themes` table;
2. the `NOW` register;
3. `Open questions`, or one line saying there are none;
4. the path to `roadmap.md`.

No retelling of what the documents already say, and no narration of the operations the session ran —
the tables are the diff the author reads. Anything that genuinely needs an answer is a `WARNING` from
the validator or a question from § 2, and it goes after the four.

## 6. Hand over a ready row

Only for a row whose readiness is `ready`. The skill hands over; it does not drive.

**Derive the `triage` label, never store it.** `ready` + `agent` → `ready-for-agent`; `ready` +
`human` or `mixed` → `ready-for-human`. The register keeps readiness and executor apart, and the
label is computed here and written nowhere. Do not extend the vocabulary in either direction:
`needs-decision` is a roadmap state and never a tracker label.

Suggest the next step when it is available on the system, and stop there:

- **a slice** goes to the clarifying conversation — `/grill-with-docs` normally, `/wayfinder` when it
  is big and foggy. Not `/to-spec` directly: the slice is thin by design, a spec wants seams, user
  stories and decisions, and the delta between the two *is* that conversation. Skip it and the
  capture step has to invent decisions nobody took. The one exception is a slice already clarified in
  an earlier session with the outcome recorded on it — no `needs-decision` and no `needs-info` — and
  then `@slice.md` with `/to-spec` is honest, because the conversation happened, it just happened
  earlier. Further down, `size: large` is what routes through `/to-tickets`;
- **a spike** goes to `/prototype` when the question needs something built to answer it, and to
  `/wayfinder` when it is a choice to be made rather than an experiment to run. Never to `/to-spec`,
  which has no spec to write.

Read `docs/agents/issue-tracker.md` when it is there, to know where the spec and the tickets will
live. When it is not, say so and carry on.

## Complete when

- the situation was established from `.roadmap/` and from asking what was delivered, never from a
  tracker;
- the branch follows what the input claims about, work by default, and an input that cannot be
  reconciled with the recorded goal produced a question rather than an inference;
- a drawn map obeys `references/drawing-the-map.md` and was argued with in the same session;
- every row obeys `references/slice-rules.md`, and every id was minted by increment and never
  recycled;
- close-out asked the three questions of absorption, and wrote nothing where all three answered no;
- the coverage question was re-asked, a first map was written unasked, and a session that found a map
  already standing proposed one block and got one confirmation before writing;
- the validator reports no `ERROR`, and every `WARNING` was put to the author;
- the session closed on the four-part report — themes, register, open questions, path — and nothing
  else.
