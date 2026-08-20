# Where the roadmap skill is going — a roadmapping tool

The goal of a new `roadmap` skill and the reasoning behind it. This is not a plan: the plan comes
next, in its own session, and this document is its source.

Around it: [`CONTEXT.md`](./CONTEXT.md) fixes the vocabulary and is binding — where a term is defined
there, this document argues about it rather than redefining it. [`WORKFLOWS.md`](./WORKFLOWS.md) walks
three sessions end to end on the `recipe-app` scenario; it illustrates and never rules.
[`PLAN-INPUTS.md`](./PLAN-INPUTS.md) collects what belongs to the implementation plan rather than to
the goal.

## The problem

`plan-slices` is a **one-shot document generator**. It reads sources, cuts a delivery plan into
vertical slices, validates the structure, and stops. Its three branches — create, review,
split/merge/reorder — all assume the plan is written once and then corrected, and its slices are
numbered by position, so every edit renumbers them and repairing the dangling references is part of
the job.

That is the wrong shape for how the work actually goes. A plan is not for ever. What is wanted is a
**roadmap**: a living artifact planned a bit at a time, where `LATER` is deliberately vague and gets
specified only when promoted, where delivered work is closed out and the evidence it produced feeds
the next decision, and where new work can enter at any point.

Five things follow from that, none of which the skill has today:

- **Identity** — an id that survives promotion, reordering and insertion. Position-based numbering
  makes every revision a rename.
- **Readiness** — a slice can be blocked on a decision the author has not made, or on information
  somebody else holds. Today there is one global `Open questions` section and no per-slice state.
- **Human work** — credentials, cloud consoles, DNS, billing, app-store enrolment. The skill assumes
  a single executor and cannot say "this one is not delegable".
- **Readability** — one dense document holding the whole map, the cross-functional concerns and every
  slice body at once. The overview and the detail want different files.
- **Coverage** — nothing ties the plan to a declared goal, so nothing can answer *do these slices
  arrive anywhere*, and nothing reports which parts of the vision had to be guessed to draw it.

## What the tool is for

A roadmap that is **easy to read, visible, and evolvable**. Visible because the overview fits on one
screen; evolvable because a single slice can be expanded, promoted, or closed without touching
anything else.

It is a **sense-making tool, not a precision instrument**. Its job is to let the author say *these are
the twelve slices that get me to the goal*, and then argue with that sentence. Whatever buys precision
at the cost of that sentence is a non-goal, and stays out on purpose:

- no dates, no estimates, no percentage complete, no velocity;
- no field nobody re-reads. Promotion triggers and decision checkpoints were dropped for exactly this
  reason: both recorded *when this evidence arrives, change this decision*, which a human re-reading a
  living roadmap can already see. Anything of that family gets dropped the same way;
- the validator checks referential coherence, never judgement: it may not demand that a field be
  filled *well*. A validator that grades content turns the tool into a form.

This is the constraint most likely to erode one revision at a time, which is why it is written down.

### What does not go through the roadmap

Vertical slicing earns its cost whenever a goal is declared and the way to it is unknown — at the
start of a greenfield project, and again at every goal after that. It does not earn it on a copy
change, a small refactor, or an idea that does not serve the current goal. Those go from the
conversation into the existing chain, `to-spec` onwards, with no roadmap involved. That is not an
escape hatch to be written into the skill; it is the chain used without it.

### Two rule sets, and when each fires

- **Roadmap rules** — themes, first validator per theme, breadth before depth, repository
  prerequisite and walking skeleton, ordering for learning. They answer *in what order do we discover
  things*, and they fire when a goal is declared and the map is drawn against it.
- **Slice rules** — what makes a valid slice, split and merge tests, verification mapping to the
  learning target, readiness, executor, id. They hold for ever, on every operation.

The two do not run in sequence, greenfield then steady state. They **alternate**: a goal is declared,
the map is drawn, the map is delivered and re-trued a session at a time, the goal is reached, the next
one is declared and the roadmap rules fire again. Nothing goes inert; it comes back round.

This is why there is **one skill, not two**. An earlier draft split it into `roadmap-create` and
`roadmap-update`, by what each reads. That split asks the author to pick the verb before describing
the situation, which is exactly what the skill refuses to do one level down, with its operations — and
the situation is legible without asking: `.roadmap/` exists or it does not, the goal is new or it is
not. The cost the split was avoiding is real but misattributed: dragging the theme ceremony into a
routine update would make the tool unbearable where it should be lightest, and that is fixed by
keeping the roadmap rules in a reference file loaded on one branch only. Two skills would have created
a problem of their own — `skills add` copies one folder at a time, so anything shared either gets
duplicated or breaks when one is installed alone.

## Where it sits

The roadmap is the top of a chain whose lower halves already exist as installed skills
(`to-spec`, `to-tickets`, `implement`, `triage`, `to-questionnaire`, `wizard`).

```
.roadmap/roadmap.md         ROADMAP   themes, the register, order for learning     ← the gap
.roadmap/slices/S3-*.md     SLICE     one outcome, one learning target             ← the gap
      ↓
conversation                CLARIFY   free, /grilling, /grill-with-docs; /wayfinder when big and foggy
      ↓ to-spec                       captures the conversation — it does not interview
spec, on the issue tracker  HOW       seams, user stories, implementation decisions
      ↓ to-tickets                    only when the work exceeds one session
tickets                     EXECUTION blocking edges, one context window each
      ↓ implement                     one open ticket at a time, working the frontier
```

Very small work — a copy change, a minor refactor — goes from the conversation straight to
`implement`, skipping both `to-spec` and `to-tickets`.

Run end to end, a slice leaving the roadmap looks like this:

```
/roadmap                   promote S7, mark it ready, hand over
/grill-with-docs S7        the slice document is the subject of the conversation
/to-spec                   captures that conversation; record the spec on the slice
/to-tickets <spec>         only if the work exceeds one session
/implement <ticket>        one at a time, working the frontier
/roadmap                   close S7 out, absorb what it taught
```

### The handover into `to-spec`

`to-spec` takes no argument and reads the current conversation, so the hook back into the chain is
**the conversation, not a file reference**. Dropping the slice document into context and running
`/to-spec` is mechanically possible and usually wrong: the slice is thin by design, a spec wants seams,
user stories and implementation decisions, and the delta between the two is precisely what the
clarifying conversation produces. Skip it and `to-spec` has to invent that delta — decisions nobody
took, published to the tracker labelled `ready-for-agent` with *no need for additional triage*.

The exception is a slice already clarified in an earlier session, with the outcome recorded on it: no
`needs-decision` and no `needs-info` on its readiness. Then the conversation happened, it just happened
earlier, and `@slice.md` with `/to-spec` is honest. Telling those two cases apart is what the readiness
states are for.

Downstream, `to-tickets` produces a flat dependency graph with no themes, no horizons, no learning
targets and no replanning: it is deliberately **ephemeral**, and a ticket dies when it closes. The
roadmap is **durable** and decides *what to do next*, not *how*. Nothing at that altitude exists in the
installed set, and that is the whole of what gets built here.

## Decisions taken

**Artifact layout.** `.roadmap/roadmap.md` is the readable overview: the goal, sources, current state,
ordering criteria, the theme table, `Assumptions`, `Open questions`, `Cross-functional concerns`,
then the three horizons — the register under `NOW`, the candidate list under `LATER`, the exclusions
under `OUT-OF-SCOPE`. `.roadmap/slices/` holds one document per open slice, `.roadmap/archive/` one
per delivered slice, both named `S<id>-<slug>.md`.

**One roadmap per project, serving one declared `Goal` at a time.** The goal comes from a goal
document or from the invocation, and `roadmap.md` restates it at the top; without it there is nothing
to ask *do these slices arrive anywhere* against, and that question has to stay askable at every
session, not only the first. A new capability extends the existing roadmap rather than opening a
second one. Concurrency is what would force one, and every way of buying it — a `Goal` column,
`.roadmap/<goal>/`, two maps side by side — pays in the focus the tool exists to impose: `NOW` becomes
the union of two paths, coverage has to be asked twice, and the register stops answering *what is the
path* because there are two. If the author cannot say which of two goals comes first, that is the
decision the roadmap is there to force, not to record: either they are one goal at a higher altitude,
or one of them is `LATER`.

**A redraw rebuilds the map and keeps the ledger.** `.roadmap/` holds two kinds of thing, and only one
of them is an opinion about the future. Redrawn from nothing: `Goal`, the themes, the register, the
ordering criteria, `Assumptions` and `Open questions`. Carried over: `archive/`, because a local
tracker has no notion of *done* and it is the only durable record of what was delivered; the id
high-water mark,
because restarting at `S0` would make one number mean two things inside one archive;
`OUT-OF-SCOPE`
and `Cross-functional concerns`, because both are constraints the shipped code already obeys and
forgetting a trade-off does not un-ship it — where the new goal contradicts one, it is lifted
deliberately and in the open, which is the whole reason it was written down.

`LATER` survives as a file and not as a reading: every candidate is re-read one at a time against the
new goal — promoted, kept as speculation, or killed. Focus is relative to a goal, so when the goal
changes the whole list is stale by definition, and a candidate that survives without being re-read is
one nobody chose. Slices still open in `NOW` are **not** carried automatically either: each is
re-justified, the ones that still serve the goal keep their ids, the rest are retired. That is what
makes it a redraw and not a patch — the map is re-derived, not mended, and no new machinery is
involved, only the operations that already exist applied in one block.

No history of superseded goals is kept. Nobody re-reads it and git has it; if the context matters,
`Current state` already has room for a sentence.

**Three horizons, separated by their relation to the goal, and only `NOW` has identity.** `NOW` is
what it takes to reach the goal, `LATER` what does not serve *this* goal, `OUT-OF-SCOPE` what the
solution declares it will never solve. The axis is not how much attention each deserves, which is
unfalsifiable, but whether it is on the path — which turns promotion into a real moment of
sense-making: *this thing I filed as peripheral is on the path after all*. From that axis follow the
shapes: the register **is** `NOW`, so having an id is the same fact as having a row, while candidates
and exclusions carry no ids, columns or documents — giving a candidate a document would invite
specifying it, and a candidate is vague by design. `OUT-OF-SCOPE` is not a graveyard either: several
trade-offs the implementation takes are defensible *precisely because* those problems are declared
unsolved, so recording the exclusion is recording the licence for the trade-off.

**`NOW` is capped, and the cap binds granularity rather than count.** A bigger problem does not buy
more rows, it buys fatter slices. Not fitting under the cap is a finding, not an inconvenience: either
the goal is too wide and wants an intermediate one declared, or the slicing is specifying work it
cannot yet know. Below the floor the roadmap does not repay its cost — that is an idea, and the
existing chain handles it. The cap binds every later session too: an admission that would overflow it
forces a merge or a deferral instead of growing the list, which is what stops a living roadmap from
silting up.

**No gradient of detail inside `NOW`.** The last slice on the path is genuinely foggier than the
first, but the fog has nowhere to accumulate: the detail of `S1` is born downstream, in the clarifying
conversation and the spec, never in the roadmap. What differs between near and far is confidence, and
confidence already has its expression — a fuller `Open questions`, and `readiness: needs-decision`. No
new field, no new rule, nothing to keep in sync.

**The register holds the comparison metadata; the document holds the rest.** A field earns a column
when it is used to *compare rows and decide what comes first*. A field that only makes sense while
reasoning inside one row belongs to that row's document — repeating register fields inside the
document is what made the current output feel cluttered in the first place. Close-out removes the
row and moves the document to the archive, so `NOW` shrinks toward the goal, which is as much progress
reporting as this tool does.

**The row is named by its title, and the two artifacts link to each other.** The register carries the
descriptive title, not the one-line outcome: a title is what the eye reads down a column of fifteen
rows, while a sentence per row turns the table into prose and makes the columns beside it unreadable.
The outcome is not lost, it moves — it is the slice document's opening line, above everything else,
so the two artifacts each carry the form of the answer they are read for. The title in the register
links to the slice document and the slice document links back to the register, because a map whose
detail is one directory away is only readable if getting there and back costs a click. Ids stay plain
text on both sides, in the `Id` column and in `Depends on`: an identity that renders as a link twice
in one row is noise, and it is the filename that resolves it anyway.

**Ids are minted at promotion by monotonic increment.** The next one is the highest found across
`.roadmap/slices/` and `.roadmap/archive/`, plus one — the filenames carry it, so it is two directory
listings and no counter to keep in sync. Two operations follow from that. A **split** keeps the id on
the half that keeps the learning target: retiring the original and minting two is cleaner in principle
and worse in practice, since it invalidates every `Depends on` pointing at the original for no gain,
and the learning target is already the invariant the split test rests on. **Retirement** spends the id
and deletes the document: the archive means *delivered* and would start lying the moment it held
something that was not, and git is the archive for things that never happened.

**Two sections report on the input: `Assumptions`, then `Open questions`.** Drawing the map forces
the skill to resolve things the goal document left open, and these say which ones, so the author gets
a second reading of the vision's completeness. They are separate because they ask different things and
close differently: an assumption was taken as true *in order to* draw the map and asks to be
corrected, and it usually dies at close-out, when delivery confirms or refutes it; an open question
could not be settled and asks to be answered, and it dies when the author answers it. The order is
fixed, which carries structurally what used to be a rule in prose — an assumption taken silently does
more damage than a question left visibly open.

Every line is traced to what it touches, a theme or a slice id. Neither section is a work queue and
neither mints anything.

**`Open questions` is also the slice's field, and only scope tells the two apart.** What blocks the
*shape of the map* cannot live on a slice, because it questions whether that slice exists at all;
what blocks one slice lives on it, and shows in the register as `readiness: needs-decision` or
`needs-info`. Sharing the name is deliberate: with two names the author can route by feel — *this one
sounds like a decision, so it goes on the slice* — while with one, the only thing that decides is what
the entry blocks, which is the rule. The name is safe to reuse because that per-slice state now
exists: in `plan-slices` `Open questions` was the global catch-all precisely because there was nowhere
else to send anything. It also stops the field from under-describing itself, since a slice waiting on
somebody else records what it waits for in the same place, and that is a question, not a decision
anybody owns.

`Assumptions` has no counterpart on the slice, and should not get one: it reports on the input to
*drawing the map*, and a slice draws nothing.

**Dependencies get published**, as a `Depends on` column holding ids. The current skill forbids this —
order carries the constraint — which holds only while the plan is written once. A later session that
promotes or reorders would otherwise violate a constraint recorded nowhere.

**Two axes of state, and neither names an actor.** *Readiness* and *executor* stay separate because
most infrastructure slices are mixed: a human creates the project and the secrets, an agent writes the
IaC. The canonical `triage` labels are **derived** at handover, not stored: `ready` + `agent` →
`ready-for-agent`, `ready` + `human` or `mixed` → `ready-for-human`. Reusing the label strings as slice
states would have made `ready-for-agent` + `mixed` writable and meaningless. Each state has its tool
downstream: `needs-info` is what `to-questionnaire` consumes, `needs-decision` what `wayfinder`
consumes — its decision tickets are questions whose resolution is a decision — and `human` or `mixed`
executors are what `wizard` consumes.

**No token budget on a slice.** Sizing to a single context window is `to-tickets`' job, and it does it
better because by then a spec exists. A token count no validator can check is a hollow ritual. `size`
routes what gets delivered; `kind: spike` routes ahead of it, since a spike has no spec to write.

**`kind` replaces the title tags.** `product`, `enabler`, `release`, `spike`. The current skill writes
`(Theme: …)`, `(Enabler: …)` and `(Release: delivery)` into the slice title, which hides metadata in
prose and puts the theme in two places at once; as a column it also makes "an enabler may not be a
theme's first validator" checkable instead of parseable.

**Research gets a row: `kind: spike`.** A spike is timeboxed investigation whose product is knowledge,
so it has a learning target and no vertical outcome. Keeping it out of the register — as a
`wayfinder` decision alone — would hide work that takes real time and blocks real slices, and the
register would then answer *what is the path* on partial information, which is the one thing this tool
exists not to do. Sense-making on a map that omits the research is sense-making on a lie.

A spike is therefore **not a slice**, and the word does not stretch to cover it: the vertical outcome,
the split test and verification-mapped-to-the-learning-target are what *slice* means, and a spike
fails all three by design. The register holds rows, and a row is a slice or a spike. Everything else
is shared, because none of it depends on the outcome being vertical: same id sequence and same
minting, same `Depends on`, same readiness and executor, same document in `slices/`, same close-out
into `archive/` — a spike that answers its question was delivered. The one field that does not apply
is `Audience`; a spike has no user, and who consumes its answer is named by what depends on it.

Two things keep it from becoming the polite way to defer a decision — the failure `plan-slices`
already had to write an eval rule against, that assigning a spike does not resolve a conflict between
sources:

- **A spike must have a dependent.** Either a slice lists it in `Depends on`, or its row declares that
  it validates the goal's feasibility. A spike nobody is waiting on is curiosity, and the check is
  referential, so the validator can make it.
- **It competes for a row under the cap**, like everything else in `NOW`. Research displacing a slice
  is the cost showing up where it can be argued with.

There is no timebox field. A spike is timeboxed in the doing, downstream, and a duration no validator
can check is the same hollow ritual as a token budget. What the roadmap can see is the row that has
not closed for three sessions, which is a conversation, not a field.

**The slice document holds no spec.** Its fields are `Outcome`, `Audience`, `Includes`,
`Verification`, `Learning target`, `Excludes`, `Open questions`. Seams, user stories and contracts
are born in `to-spec` and live on the tracker; duplicating them yields two truths that diverge at the
first ticket. `Outcome` is one line and it opens the document, because the register names the row by
its title and the sentence that says what the row delivers has to live somewhere; it is the one field
whose place moved rather than whose content is new.

**Its fields are chosen as what `to-spec` cannot invent.** Those are also the ones that carry across:
`Audience` and `Learning target` become the spec's *Problem Statement*, `Excludes` becomes its *Out of
Scope*, and `Verification` constrains its *Testing Decisions*. Anything a capture step could plausibly
have written by itself does not need to be on the slice.

**The slice carries four references: one inbound, three outbound.** `Requested by` points back at
whatever produced the slice — a source document, or, for work admitted later, the delivered slice that
made it visible; same question asked at two different times, so one field answers both. It also
publishes the traceability that currently lives "in reasoning, not in the published plan", which a
living roadmap cannot rely on: the previous session's reasoning no longer exists. `Spec` and `Tickets`
are filled at promotion, `ADRs` at close-out. All four point and hold no content, so they do not
reopen the rule above.

**`Cross-functional concerns` survives, with the template's five entries** — authorization, validation
and errors, operability, accessibility and security, data integrity and recovery. It is the only place
a rule holds for *every* slice, and the anchor for the identity seam. Without it each slice restates
the same paragraph, which is the repetition this format exists to remove.

## The skill

**`roadmap`.** One entry point, one folder. `SKILL.md` is a router: it establishes what it is looking
at — whether `.roadmap/` exists, what the recorded goal is, what has been delivered since the last
session — and takes one of two branches.

The branch is decided by **what the input makes a claim about**. A claim about *where we are going*
that contradicts the recorded `Goal` means the map is drawn again; a claim about *how we get there* is
work, and only the second branch touches it. That is the common case by a wide margin, and it is the
default: new work is admission, promotion or revision, and it leaves the goal alone.

Nothing has to be divined. The coverage question runs every session anyway, and it is the trigger:
when what the author brings cannot be reconciled with the recorded goal — it does not serve it, and it
is not an exclusion either — the skill states the goal it has on file, says what the input looks like
to it, and asks which one holds. A question with a short answer, not an inference.

**Drawing the map**, when there is a goal and no map standing against it. Full ceremony, and the
roadmap rules that carry it live in a reference file loaded only here. A redraw is not a separate
mode: it is this same branch with more input, since what the previous goal leaves behind — the
archive, the id high-water mark, the exclusions, the concerns, the candidates — enters as a constraint
exactly the way sources do. There is no reconciliation logic to write.

It **does not end when the files are written**. A first map is a proposal to argue with, and the
argument produces exactly the operations the other branch performs — split this one, drop that part,
swap the order. So the first round of revision happens right there, in the same session.

**Re-truing the map**, every session after. Five operations: **close-out**, **promotion**,
**admission**, **revision** and **retirement**. The first three were the original set; revision is the
split/merge/reorder branch of `plan-slices`, dropped earlier without a replacement; retirement was
simply missing — every arrow pointed forward, `LATER → NOW → archive`, with no way back.

**No subcommands, on either branch.** Nobody arrives saying *perform a promotion*. They arrive saying
*we closed S2 and S3, I found out X, and there is this screenshot idea*. The skill derives which
operations apply from that. The five names are its internal vocabulary — enough to order the work,
close-out first, since everything else is decided against a register that has already been trued up —
not verbs the author types. `/roadmap promote S7` is precision where sense-making was wanted.

**Absorbing the evidence is a state change, not a summary.** Closing a slice asks three questions of
the map: whether the delivery settles a line in `Assumptions` or `Open questions`, which then dies
rather than being annotated; whether it changes another row — a size that was wrong, a readiness
that can flip, a `Depends on` gone moot; and whether it produced a decision clearing the ADR bar,
which is what the archived slice's `ADRs` reference is for. When all three answers are no, nothing is
written. A paragraph produced to prove the step happened is the ceremony this tool refuses. A spike
is the exception that proves it: three noes on a spike mean it taught nothing, which is a finding
about the spike.

Both branches end the same way: re-ask the coverage question — *does what is left in `NOW` still reach
the goal* — which is what recording the goal is for. And all of it is conversation, not generation:
the skill proposes a block of changes and asks for confirmation once.

There is no second skill and no audit command: whoever reads a roadmap takes it as it stands, and the
one check that does not rest on judgement is the validator, which the skill already runs.

## The integration boundary

Reuse the installed chain; do not rebuild it. Rebuilding `to-spec` and `to-tickets` would replace two
mature skills with something answering a different question.

Couple loosely, on purpose:

- **Close-out asks.** It does not interrogate the tracker for what is closed. Interrogating would bind
  the skill to whichever tracker is configured and would depend on slice references being reliable;
  asking is more robust, and close-out is an explicitly manual resynchronisation step.
- **The skill hands over, it does not drive.** It updates the roadmap, marks the row ready, and
  suggests the next step if it is available on the system — the clarifying conversation,
  `/grill-with-docs` normally or `/wayfinder` when the slice is big and foggy, never `/to-spec`
  directly, since a capture step has nothing to capture yet. A spike goes elsewhere: `/prototype`
  when the question needs something built to answer it, `/wayfinder` when it is a choice to be made
  rather than an experiment to run. The two stacks stay independent.
- **Degrade cleanly.** Read `docs/agents/issue-tracker.md` when it is there; when it is not, say so
  and carry on, as the installed skills do.
- **Do not extend the triage label vocabulary.** `needs-decision` is a roadmap readiness state, never
  a tracker label; `ready` and `needs-info` are roadmap states that happen to share spelling with
  tracker labels, and the mapping runs one way, at handover.

**A local tracker has no notion of *done*.** Its `Status:` vocabulary is the five triage roles, none
of which means delivered, nothing writes it — `implement` never mentions the ticket it implements —
and a real board of fourteen local tickets read as entirely open with several of them delivered. Two
consequences: close-out asking is not merely the loosely-coupled choice but the only possible one,
since there is no delivered state to read back; and the archive under `.roadmap/` becomes the only
durable register of what was delivered. Not of what it *taught* — that crystallises in the code and,
when it clears the ADR bar, in `docs/adr/` — which is why the archived slice keeps the thread by
pointing: `Spec`, `Tickets`, `ADRs`. The state of individual tickets stays the tracker's business,
badly kept though it currently is; fixing that belongs in `docs/agents/issue-tracker.md`, which the
setup skill declares hand-editable, not in this skill.

Adjacent and deliberately out of scope: there is no skill for *capture and park* — filing one small
item you do not intend to do now. Worth its own small skill one day; it is not roadmapping, and
nothing that lands in it belongs in the roadmap.

### Frictions accepted

- **Two dependency models.** Roadmap `Depends on` orders *outcomes*; ticket blocking edges order
  *edits*. Both are needed, at different granularities. They are not synchronised, and the roadmap
  skill does not generate ticket edges.
- **Two sources of truth about state.** Reality lives on the tracker; the register is a copy that
  ages. Close-out is the resynchronisation, not a background automatism.
- **A vocabulary collision.** `to-tickets` calls its tickets "tracer-bullet vertical slices". Keep
  *slice* for the roadmap unit and never call a ticket a slice in these documents.

## What changes relative to `plan-slices`

`plan-slices` is not invalidated. The new skill is built **beside** it, and it is retired once the new
one stands. The two are never used together on the same project; the one intended overlap is
transitional — `plan-slices` as a yardstick against which to judge the first roadmaps.

The format diverges on every axis, which is why nothing is shared:

| | `plan-slices` | roadmap |
|---|---|---|
| Artifact | one file, written once | `.roadmap/`, living |
| Goal | implicit in the sources | declared, recorded, re-checked at every update |
| Scale | unbounded | `NOW` capped; granularity absorbs the problem's size |
| Identity | position number, renamed on every edit | id minted at promotion, never recycled |
| Metadata | inline in the slice body and title tags | register columns, comparison fields only |
| Dependencies | unpublished, carried by order | `Depends on` column |
| State | none | readiness × executor |
| Horizons | three sections of slices | register + candidates + exclusions |
| Deferral | `LATER` entry with a promotion trigger | candidate, no trigger, no id |
| Slice fields | `Includes` / `Verification` / `Learning / risk` / `Outcome` | `Outcome` / `Audience` / `Includes` / `Verification` / `Learning target` / `Excludes` / `Open questions` + `Requested by` / `Spec` / `Tickets` / `ADRs` |
| Navigation | one file, so none | register title links to the slice, slice links back to the register |

The validator also grows from checking one file to checking a graph.
