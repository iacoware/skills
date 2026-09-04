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
per open row, `archive/S<id>-<slug>.md` one per delivered row, and `log.md` the model's memory of the
theme verdicts and of the sweep of the sources — read at the start of every session, appended by
whatever touches the themes, never reported to the author. One roadmap per project, serving one
declared `Goal` at a time. A row is a slice or a spike.

**Two references carry the rules.** [references/slice-rules.md](references/slice-rules.md) says what
makes a row valid; read it at the start of every session, whatever the input asks for.
[references/drawing-the-map.md](references/drawing-the-map.md) says what makes a map; it is loaded on
the `Drawing` door and on no other.

**Nothing on disk is written unasked, and nothing that stands is overwritten unconfirmed.** The
discriminator is not the door but whether a record already stands. With no `.roadmap/` there is
nothing to lose and nothing to describe: the author argues with the file far faster than with an
account of it, so it goes down straight away. Where a record stands, everything that would overwrite
or delete it is proposed in one block and confirmed once — a session rewrites rows other sessions
wrote, and deletes documents, and that is worth a round trip.

**A session against a standing map stops twice, and the two stops have different jobs.** The
situation round trip gathers facts, writes nothing, and is skipped when the input already answers it.
The confirmation round trip presents one block of proposed writes and collects one yes; *one
confirmation, never split across several questions* governs that block, not the number of times the
session speaks to the author. Neither stands in for the other: the delivery question cannot wait for
the close, because `Close-out` is the first operation and everything after it is decided against a
register already trued up, and the confirmation cannot come early, because the block it confirms does
not exist yet. A session that finds nothing to change never reaches the second. The one further
question licensed to block is the reconciliation question of *Choose the door*, where proceeding
under either reading would destroy a standing record; nothing else here may stop the session.

## 1. Establish the situation

Read before deciding anything:

- whether `.roadmap/roadmap.md` is there, and if it is, its `Goal`, its themes, its register,
  `LATER`, `OUT-OF-SCOPE`, `Assumptions`, `Open questions` and `Cross-functional concerns`;
- `.roadmap/slices/` and `.roadmap/archive/`, which give the open documents and what was delivered;
- `.roadmap/log.md`, the verdicts on the theme boundaries as the last session left them — a pair
  decided twice is decided by its lowest entry — and the entries of the sweep: every conflict and
  undecided choice the drawing found, with the exit it took. Nothing else carries them: a session
  that skips the log re-litigates every boundary from scratch;
- the sources the input points at, and `docs/agents/issue-tracker.md` when it is there.

**What has been delivered since the last session is asked, never read off a tracker.** A local
tracker has no notion of *done*: nothing writes it, and a board of open tickets says nothing about
what shipped. Close-out is an explicitly manual resynchronisation, and asking is the only thing that
works. It is asked here, in one round trip with everything else the situation raises, and skipped
when the input already answers it.

When there is no `.roadmap/` and no goal in the input either, the goal is what to ask for first.
There is nothing to draw a map against and nothing to ask *do these rows arrive anywhere* of.

## 2. Choose the door

One door, chosen from the input at the start and never reopened mid-session. It decides two things:
which reference is loaded, and which section runs next.

| Door | Taken when | Section |
|---|---|---|
| `Drawing` | no map stands against a declared goal, **or** the input contradicts the recorded `Goal` | *Draw the map* |
| `Revising` | everything else — the goal stands. The default, by a wide margin | *Operations on the map* |

The first condition is a filesystem check. The second is the reading below.

**Destination or path.** A claim about *where we are going* that contradicts the recorded `Goal`
draws the map again. A claim about *how we get there* is work, and leaves the goal alone. Work is the
default and by a wide margin: admission, promotion, reshaping, close-out and retirement all leave the
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

**When the input cannot be reconciled with the recorded goal** — it does not serve it, and it is not
an exclusion either — **ask.** State the goal on file, state what the input looks like from where the
map sits, ask which of the two holds. A question with a short answer, never an inference.

## 3. Draw the map

The `Drawing` door. Follow [references/drawing-the-map.md](references/drawing-the-map.md) — themes,
the two prerequisites, ordering, the identity seam, what the map reports about its own input, and
what carries when a map already stands.

Write `log.md` first — the theme verdicts and the entries of the sweep, in the shape and order the
reference gives, before `roadmap.md` exists; on a redraw the log starts again. Then `roadmap.md` from
[assets/roadmap-template.md](assets/roadmap-template.md) and one document per `NOW` row from
[assets/slice-template.md](assets/slice-template.md). Keep the headings, field names and order; write
the content in the author's language.

**Drawing does not end when the map is down.** A first map is a draft to argue with, and the argument
runs operations from *Operations on the map* — split this one, drop that part, swap the order — here,
in the same session, before the close. Two things in that section do not fire on this door:
`Close-out`, which has nothing to resynchronise against a map just drawn, and the coverage question
that closes it, which the theme ceremony and `The map holds when` have already asked.

## 4. Operations on the map

Five operations, derived from the situation the author arrives with — *that one is finished, it
turned out the numbers are nothing like we assumed, and here is something nobody had thought of*. The
verb is never required of the author; when one is given — *split S12*, *merge these two* — it is a
shortcut through the same derivation, under the same rules and the same close.

**Close-out first**, because everything else is decided against a register already trued up. What was
delivered was asked at *Establish the situation*; this is the operation the answer triggers. The row
leaves the register, its document moves to `.roadmap/archive/` unchanged, and its `ADRs` reference is
filled when the work produced a decision that cleared the bar: hard to reverse, surprising without
context, the result of a real trade-off.

**Then absorb the evidence**, which is a state change and never a summary. Three questions:

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
with an id, and an admission that would put `NOW` over the cap forces a merge or a deferral.

Whether the row admitted is a slice or a spike is read here, by `slice-rules.md` § *The spike test*.
That reading needs no question: nothing about the destination is in doubt, so it goes in with the
rest of the session's changes.

**Reshaping** changes the form of existing rows without adding or closing any: split, merge, rewrite,
reorder.

**Retirement** takes a row out of `NOW` undelivered: it dies, or it goes back to `LATER` as a
candidate.

**An operation that touches the themes appends to `log.md`** — a reshaping that splits or merges a
theme, an admission that opens one — under an H2 of its own, dated and named `Revising`, one bullet
per boundary it decided in the shape the entries above already have: the pair, `split` or `merge`,
the one fact. A verdict is never rewritten; the entry that supersedes it goes below, and the earlier
H2s stay as they are.

**A section the format no longer has** — `Ordering criteria`, left by a session that wrote the map
under an older format — is deleted with the rest of the block. The validator rejects it as a section
the roadmap does not have, and what it held is the register's order.

**Last, the coverage question:** does what is left in `NOW` still reach the goal? Usually the answer
is one line; it is asked anyway, because `NOW` moved under a fixed goal. A failed check never reopens
the door mid-session — it produces a question, the question is delivered at the close, and the next
session takes `Drawing` if the answer requires it. What makes an answer a failure is the criterion in
*Choose the door*.

## 5. Close the session

Both doors close here, and the same way: what varies is only whether a record already stood.

**Write.** A first map goes down as it was drawn. Everything that would touch a standing record is
proposed in one block, confirmed once, and written then, per the invariant in the preamble. A session
that found nothing to change writes nothing, and the rest of this section degrades with it: no block
to confirm, and nothing for the validator to check.

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
the tables are the diff the author reads. `log.md` is not among the four: it is the model's memory,
and the author contests the map from the `Themes` table. Anything that genuinely needs an answer goes
after the four: a `WARNING` from the validator, or a question the session produced rather than
answered.

## Hand over a ready row

Runs after the close when the input asks for it, never instead of it, and only for a row whose
`readiness` is `ready`. It produces one message to the author: it suggests and never drives.

`slice-rules.md` holds the parts — the `triage` label at § `readiness`, where a spike goes at § *The
spike test*, what `size: large` routes through at § `size` — and this step assembles them into the
message. A slice goes to the clarifying conversation, `/grill-with-docs` where the system has it, and
**not** straight to `/to-spec`: skip the conversation and the capture step has to invent decisions
nobody took. The exception is a slice already clarified in an earlier session with the outcome
recorded on it — no `needs-decision` and no `needs-info` — where `@slice.md` with `/to-spec` is
honest, because the conversation happened, it just happened earlier.

## The session holds when

One checklist per altitude: the row in `slice-rules.md` (*A row holds when*), the map in
`drawing-the-map.md` (*The map holds when*), the session here. A new item goes into the document that
owns its altitude.

- the door was chosen by what the input claims about, work by default, and an input that cannot be
  reconciled with the recorded goal produced a question rather than an inference;
- what was delivered was asked, never read off a tracker;
- a first map was written unasked, and a standing record was proposed in one block and confirmed once
  before being written;
- on `Revising`, the coverage question was asked, and it produced a question rather than a change of
  door;
- `log.md` was read on entry, the verdicts a drawing produced went down before the `Themes` table
  and its sweep entries before `Assumptions`, and an operation that touched the themes appended
  under its own H2;
- the session closed on the four-part report — themes, register, open questions, path — and nothing
  else.
