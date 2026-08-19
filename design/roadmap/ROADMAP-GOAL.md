# Where the roadmap skill is going — a roadmapping tool

Written 2026-08-13 from a design conversation, then revised three times on 2026-08-19: after a
nomenclature grilling; when `roadmap-review` was dropped, because nobody audits a roadmap they are
handed and reviewing the skill itself is a manual procedure; and after the author walked through the
workflow the skill has to reproduce, which bound `NOW` to a declared goal, capped its size, gave the
update path the two operations it lacked, and collapsed the create/update split into a single
`roadmap` skill.
This is the goal and the reasoning behind it, not a plan. The plan comes next, in its own session,
and this document is its source.

The vocabulary this document fixes lives in [`CONTEXT.md`](./CONTEXT.md) and is binding.
`plan` never names the roadmap, its parts, or any file under `.roadmap/`; it survives only as a verb
and in `plan-slices`, the skill being replaced.

## The problem

`plan-slices` is a **one-shot document generator**. It reads sources, cuts a delivery plan into
vertical slices, validates the structure, and stops. Its three branches — create, review,
split/merge/reorder — all assume the plan is written once and then corrected. Its plan slices are
numbered by position, so every edit renumbers them; step 5 says so explicitly, and calls repairing
the dangling references part of the job.

That is the wrong shape for how the work actually goes. A plan is not for ever. What is wanted is a
**roadmap**: a living artifact that gets planned a bit at a time, where `LATER` is deliberately vague
and becomes specified only when it is promoted, where delivered work is closed out and the evidence
it produced feeds the next decision, and where new work can enter at any point.

Five things follow from that, none of which the skill has today:

- **Identity.** A slice needs a stable id (`S0`, `S1`, …) that survives promotion, reordering and
  insertion, and is never recycled. Position-based numbering makes every revision a rename.
- **Readiness.** A slice can be blocked on a decision the author has not made, or on information
  somebody else holds. Today the plan carries one global `Open questions` section and no per-slice
  state.
- **Human work.** Credentials, cloud consoles, DNS, billing, app-store enrolment. The skill assumes a
  single executor and cannot say "this one is not delegable".
- **Readability.** One dense document holding the whole map, the cross-functional concerns and every
  slice body at once. The overview and the detail want different files.
- **Coverage.** Nothing ties the plan to a declared goal, so nothing can answer *do these slices
  arrive anywhere*, and nothing reports which parts of the vision had to be guessed to draw it.

## What the tool is for

A roadmap that is **easy to read, visible, and evolvable**. Visible because the overview fits on one
screen; evolvable because a single slice can be expanded, promoted, or closed without touching
anything else.

It is a **sense-making tool, not a precision instrument**. Its job is to let the author say *these are
the twelve slices that get me to the goal*, and then argue with that sentence. Whatever buys precision
at the cost of that sentence is a non-goal, and stays out on purpose:

- no dates, no estimates, no percentage complete, no velocity;
- no field nobody re-reads — promotion triggers and decision checkpoints were dropped for exactly this
  reason, and anything of that family gets dropped the same way;
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
`roadmap-update`, by what each reads — sources and a goal on one side, what delivery taught on the
other. That split asks the author to pick the verb before describing the situation, which is exactly
what the skill refuses to do one level down, with its operations. And the situation is legible without
asking: `.roadmap/` exists or it does not, the goal is new or it is not.

The cost the split was avoiding is real but misattributed. Dragging the theme ceremony into a routine
update would make the tool unbearable where it should be lightest — but that is fixed by keeping the
roadmap rules in a reference file loaded on one branch only, not by a second skill name. Two skills
would instead have created a problem of their own: `skills add` copies one folder at a time, so
anything shared between them either gets duplicated or breaks when one is installed alone.

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

Clarification happens in the **conversation**, upstream of `to-spec`, which is a capture step and
says so: *do not interview the user, synthesise what you already know*. Very small work — a copy
change, a minor refactor — goes from the conversation straight to `implement`, skipping both `to-spec`
and `to-tickets`.

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

`to-spec` takes no argument: it has no `argument-hint` and no fetch clause, unlike `to-tickets`, which
does accept *a spec path, an issue number or URL*. It reads the current conversation. So the hook back
into the chain is **the conversation, not a file reference** — dropping the slice document into
context and running `/to-spec` is mechanically possible and usually wrong.

The slice document is thin by design; a spec wants seams, an extensive list of user stories,
implementation and testing decisions. The delta between the two is precisely what the conversation
produces. Skip it and `to-spec` has to invent that delta — user stories and implementation decisions
nobody decided, published to the tracker labelled `ready-for-agent` with *no need for additional
triage*.

The exception is a slice already clarified in an earlier session, with the outcome recorded on it: no
`needs-decision` and no `needs-info` on its readiness. Then the conversation happened, it just
happened earlier, and `@slice.md` with `/to-spec` is honest. Telling those two cases apart is what
the readiness states are for.

`to-tickets` produces a flat dependency graph with no themes, no horizons, no learning targets and no
replanning: it is deliberately **ephemeral**, and a ticket dies when it closes. The roadmap is
**durable** and decides *what to do next*, not *how*. Nothing at that altitude exists in the
installed set, and that is the whole of what gets built here.

## Decisions taken

**Artifact layout.** `.roadmap/roadmap.md` is the readable overview: the goal, sources, current state,
ordering criteria, the theme table, `Assumptions and gaps`, `Cross-functional concerns`, then the
three horizons — the register under `NOW`, the candidate list under `LATER`, the exclusions under
`OUT-OF-SCOPE`. `.roadmap/slices/` holds one document per open slice, `.roadmap/archive/` one per
delivered slice, both named `S<id>-<slug>.md`.

**One roadmap per project, not per initiative.** A new capability extends the existing roadmap.

**The roadmap serves one declared `Goal`, and records it.** The input is a goal document, or the
equivalent stated in the invocation; `roadmap.md` restates it at the top. Without it there is nothing
to ask *do these slices arrive anywhere* against, and that question has to stay askable at every
update, not only at creation. Reaching the goal empties `NOW`; declaring the next one is a
redrawing, on the same `.roadmap/`, with the roadmap rules firing again.

**Three horizons, separated by their relation to the goal.** `NOW` is what it takes to reach the
declared goal. `LATER` is what does not serve *this* goal — speculation, or material for the next one.
`OUT-OF-SCOPE` is what the solution declares it will never solve. The axis is not how much attention
each deserves, which is unfalsifiable, but whether it is on the path — which turns promotion into a
real moment of sense-making: *this thing I filed as peripheral is on the path after all*.

**Three shapes, and only `NOW` has identity.** The register **is** `NOW`: a table, one row per slice,
and having an id is the same fact as having a row. `LATER` is a list of candidates and `OUT-OF-SCOPE`
a list of exclusions — neither carries ids, columns, or documents. `horizon` is a collective word in
prose, never a field: a value that is constant down a column is not information.

**`NOW` is capped, and the cap binds granularity rather than count.** Between three or four slices and
twenty, fifteen the number to aim at. A bigger problem does not buy more rows, it buys fatter slices;
a small one gets small slices. Not fitting under the cap is a finding, not an inconvenience: either
the goal is too wide and wants an intermediate one declared, or the slicing is specifying work it
cannot yet know. Below three or four the roadmap does not repay its cost — that is an idea, and the
existing chain handles it with no roadmap involved.

The cap binds every later session too. An admission that would take `NOW` to eighteen forces a merge
or a deferral instead of growing the list, which is what stops a living roadmap from silting up.

**No gradient of detail inside `NOW`.** The last slice on the path is genuinely foggier than the
first, but the fog has nowhere to accumulate: the slice document is thin for `S1` exactly as it is for
`S12`, because the detail of `S1` is born downstream, in the clarifying conversation and the spec, and
never in the roadmap. What differs between near and far is confidence, and confidence already has its
expression — a fuller `Open decisions`, and `readiness: needs-decision`. No new field, no new rule,
nothing to keep in sync.

**The register holds the comparison metadata; the slice document holds the rest.** A field earns a
column when it is used to *compare slices and decide what comes first* — id, theme, kind, size,
readiness, executor, `Depends on`, and the one-line outcome. A field that only makes sense while
reasoning inside one slice belongs to that slice's document. Repeating register fields inside the
document is what made the current output feel cluttered in the first place.

**The register is the whole path, not the pickable subset.** Most of its rows are not actionable
today, and that is the point: the reader has to see the twelve slices standing between here and the
goal on one screen. *What is the path* is the register's question; *what can I pick up* is
`readiness`'s; *what did we deliver* is the archive's. Close-out removes the row and moves the
document to the archive, so `NOW` shrinks toward the goal — which is as much progress reporting as
this tool does.

**Stable ids, minted at promotion by monotonic increment.** The next id is the highest found across
`.roadmap/slices/` and `.roadmap/archive/`, plus one — the filenames carry it, so it is two directory
listings and no counter to keep in sync. Ids are identity, not position: register order carries the
delivery order.

**A split keeps the id on the half that keeps the learning target.** The other half is minted new.
Retiring the original and minting two is cleaner in principle and worse in practice: it invalidates
every `Depends on` pointing at the original, for no gain. The learning target is already the invariant
the split test rests on, so identity following it costs nothing extra to explain.

**Retirement spends the id and deletes the document.** A slice leaving `NOW` for `LATER` becomes a
candidate, and candidates have no id — the number is spent and never comes back, which monotonic
minting already allows for. Its document does not go to `archive/`: the archive means *delivered*, and
would start lying the moment it held something that was not. It is deleted, and git is the archive for
things that never happened.

**A `LATER` entry is a candidate: a line, never a file, and it has no id.** `LATER` is a focus tool —
everything it is not important to concentrate on now — not a backlog. From there a candidate dies or
is promoted, and promotion is what mints its id, its row, and its document. Giving a candidate a
document invites specifying it, and a candidate is vague by design.

**No promotion triggers and no decision checkpoints.** Both recorded the same shape — *when this
evidence arrives, change this decision* — and both state something a human reading the roadmap can
already see. A living roadmap is re-read at every update; the condition does not need storing.

**`Assumptions and gaps` reports on the input.** Drawing the map forces the skill to resolve things
the goal document left open; the section says which ones, so the author gets a second reading of the
vision's completeness. Two kinds of line, each traced to what it touches — a theme or a slice id:

- **assumed** — taken as true in order to draw the map; correct it,
- **unresolved** — could not be settled; decide it.

Assumptions come first, because one taken silently does more damage than a question left visibly open.

What lands here rather than on a slice is decided by what it blocks. A gap that puts the *shape of the
map* in doubt — an undefined theme, a self-contradicting ambition, an unnamed audience — cannot live
on a slice, because it questions whether that slice exists at all. A gap that blocks one slice is that
slice's `Open decisions`, with `readiness: needs-decision`. The section is not a work queue and mints
nothing: an entry dies when it is answered.

**`OUT-OF-SCOPE` declares the boundaries of the solution.** It is not a graveyard: several trade-offs
the implementation takes are defensible *precisely because* those problems are declared unsolved.
Recording the exclusion is recording the licence for the trade-off.

**Dependencies get published**, as a `Depends on` column holding ids. The current skill forbids this
— order carries the constraint — which holds only while the plan is written once. A later session
that promotes or reorders would otherwise violate a constraint recorded nowhere.

**Traceability gets published too.** Source-to-slice tracing and adjacent split/merge verdicts
currently live "in reasoning, not in the published plan". In a living roadmap the previous session's
reasoning no longer exists, so it lands on the slice, as `Requested by` — see below.

**Two axes of state, and neither names an actor.** *Readiness* is `ready`, `needs-decision` (a choice
the author owns and has not made) or `needs-info` (waiting on somebody else). *Executor* is separate
— `agent` | `human` | `mixed` — because most infrastructure slices are mixed: a human creates the
project and the secrets, an agent writes the IaC. The canonical `triage` labels are **derived** at
handover, not stored: `ready` + `agent` → `ready-for-agent`, `ready` + `human` or `mixed` →
`ready-for-human`. Reusing the label strings as slice states would have made
`ready-for-agent` + `mixed` writable and meaningless.

Each state has its tool downstream: `needs-info` is what `to-questionnaire` consumes,
`needs-decision` what `wayfinder` consumes — its decision tickets are questions whose resolution is a
decision — and `human` or `mixed` executors are what `wizard` consumes.

**No token budget on a slice.** Sizing to a single context window is `to-tickets`' job, and it does
it better because by then a spec exists. `size` is `small` or `large`, and its only effect is
routing: `large` goes through `to-tickets`, otherwise straight to `to-spec`. A token count no
validator can check is a hollow ritual.

**`kind` replaces the title tags.** `product`, `enabler` or `release`, as a column. The current skill
writes `(Theme: …)`, `(Enabler: …)` and `(Release: delivery)` into the slice title, which hides
metadata in prose and puts the theme in two places at once; as a column it also makes "an enabler may
not be a theme's first validator" checkable instead of parseable.

**The slice document holds no spec.** Its fields are `Audience`, `Includes`, `Verification`,
`Learning target`, `Excludes`, `Open decisions`. Seams, user stories and contracts are born in
`to-spec` and live on the tracker. Duplicating them yields two truths that diverge at the first
ticket. There is no `Outcome` field: the one-line outcome is a register column, and the register is
where outcomes get compared.

**One `Learning target`, mandatory and singular.** It is what the slice must teach, and it is the
invariant the split test rests on. Risk stops being a field of its own — material risk *is* the
learning target, and immaterial risk does not deserve a line.

**Its fields are chosen as what `to-spec` cannot invent** — audience, learning target, verification
evidence, open decisions, exclusions. Those are also the ones that carry across: `Audience` and
`Learning target` become the spec's *Problem Statement*, `Excludes` becomes its *Out of Scope*, and
`Verification` constrains its *Testing Decisions*. Anything a capture step could plausibly have
written by itself does not need to be on the slice.

**The slice carries four references: one inbound, three outbound.** `Requested by` points back at
whatever produced the slice — a source document, or, for work admitted later, the delivered slice that
made it visible. Those are the same question asked at two different times, so one field answers both;
`Sources` is taken at roadmap level, which is why it is not called that. `Spec` and `Tickets` are
filled at promotion, `ADRs` at close-out. All four point and hold no content, so they do not reopen
the rule above.

**`Cross-functional concerns` survives, with the template's five entries.** It is the only place a
rule holds for *every* slice — authorization, validation and errors, operability, accessibility and
security, data integrity and recovery — and the anchor for the identity seam. Without it each slice
restates the same paragraph, which is the repetition this format exists to remove.

## The skill

**`roadmap`.** One entry point, one folder. `SKILL.md` is a router: it establishes what it is looking
at — whether `.roadmap/` exists, whether a goal has just been declared, what has been delivered since
the last session — and takes one of two branches.

**Drawing the map**, when there is a goal and no map against it. Full ceremony, and the roadmap rules
that carry it live in a reference file loaded only here: themes, a first validator per theme, breadth
before depth, the repository prerequisite and the walking skeleton, ordering for learning. It extends
an existing roadmap rather than starting a second one.

It **does not end when the files are written**. A first map is a proposal to argue with, and the
argument produces exactly the operations the other branch performs — split this one, drop that part,
swap the order. So the first round of revision happens right there, in the same session.

**Re-truing the map**, every session after. Five operations: **close-out** (remove the delivered slice
from the register, archive its document, absorb the evidence it produced), **promotion** (a candidate
becomes a slice), **admission** (new work enters), **revision** (split, merge, reword, reorder) and
**retirement** (a slice that should not have been one leaves `NOW`, dead or demoted to candidate). The
first three were the original set; revision is the split/merge/reorder branch of `plan-slices`,
dropped earlier without a replacement; retirement was simply missing — every arrow pointed forward,
`LATER → NOW → archive`, with no way back.

**No subcommands, on either branch.** Nobody arrives saying *perform a promotion*. They arrive saying
*we closed S2 and S3, I found out X, and there is this screenshot idea*. The skill derives which
operations apply from that. The five names are its internal vocabulary — enough to order the work,
close-out first, since everything else is decided against a register that has already been trued up —
not verbs the author types. `/roadmap promote S7` is precision where sense-making was wanted.

Both branches end the same way: re-ask the coverage question — *does what is left in `NOW` still reach
the goal* — which is what recording the goal is for. And all of it is conversation, not generation:
the skill proposes a block of changes and asks for confirmation once.

The router is the one thing that can fail quietly, in two directions: the theme ceremony fired on a
routine session, or a session spent re-truing a map when the goal had actually changed and it wanted
redrawing. Those are two eval scenarios, not two skills.

There is no second skill, and an audit command would have no audience: whoever reads a roadmap takes
it as it stands, and the one check that does not rest on judgement is the validator, which the skill
already runs.

The review that does exist is the review of **the skill itself**, and it is manual — half an
hour after a change believed substantive, in the shape already written down for `plan-slices` in
[`evals/plan-slices/REVIEW-WORKFLOW.md`](../../evals/plan-slices/REVIEW-WORKFLOW.md): generate,
validate, read against the brief, walk the rules, and only then open the reference. Its roadmap
counterpart lands under `evals/roadmap/`, beside the scenarios.

The validator stays a script, invoked automatically at the end of a session and callable by hand. A
skill whose body is "run this script" adds surface and nothing else.

## The integration boundary

Reuse the installed chain; do not rebuild it. Rebuilding `to-spec` and `to-tickets` would replace two
mature skills with something answering a different question.

Couple loosely, on purpose:

- **Close-out asks.** It does not interrogate the tracker for what is closed. Interrogating would
  bind the skill to whichever tracker is configured and would depend on slice references being
  reliable; asking is more robust, and close-out is an explicitly manual resynchronisation step. On a
  local tracker there is also nothing to interrogate — see below.
- **The skill hands over, it does not drive.** It updates the roadmap, marks the slice ready,
  and suggests the next step if it is available on the system — the clarifying conversation,
  `/grill-with-docs` normally or `/wayfinder` when the slice is big and foggy, never `/to-spec`
  directly, since a capture step has nothing to capture yet. The two stacks stay independent.
- **Degrade cleanly.** Read `docs/agents/issue-tracker.md` when it is there; when it is not, say so
  and carry on, as the installed skills do.
- **Do not extend the triage label vocabulary.** `needs-decision` is a roadmap readiness state, never
  a tracker label; `ready` and `needs-info` are roadmap states that happen to share spelling with
  tracker labels, and the mapping runs one way, at handover.

### What the tracker does not tell us

A local markdown tracker has **no notion of done**. `issue-tracker-local.md` records triage state as a
`Status:` line whose vocabulary is the five triage roles — `needs-triage`, `needs-info`,
`ready-for-agent`, `ready-for-human`, `wontfix` — and none of them means delivered. On GitHub closing
is native and orthogonal to the labels; on files there is no equivalent. Nor does anything write it:
`implement` never mentions the ticket it implements.

Observed on a real board of fourteen local tickets: every one still reads as open, thirteen
`ready-for-agent` and one `ready-for-human`, several of them delivered. The same specification does
define a full lifecycle — `claimed` / `resolved`, frontier scan, claim before work — but only under
*Wayfinding operations*, for decision tickets. It was never extended to implementation tickets.

Two consequences:

- **Close-out asking is not merely the loosely-coupled choice, it is the only possible one.** There is
  no delivered state to read back.
- **The archive under `.roadmap/` becomes the only durable register of what was delivered.** Not of
  what it *taught*: the learning crystallises in the code and, when it clears the ADR bar — hard to
  reverse, surprising without context, the result of a real trade-off — in `docs/adr/`. The archived
  slice keeps the thread by pointing: `Spec`, `Tickets`, `ADRs`.

The boundary still holds: the roadmap records that a **slice** is closed and what it produced. The
state of individual tickets stays the tracker's business, badly kept though it currently is. A fix for
that belongs in `docs/agents/issue-tracker.md`, which the setup skill declares hand-editable — not in
this skill.

Adjacent and deliberately out of scope: there is no skill for *capture and park* — filing one small
item you do not intend to do now. `to-spec` captures a whole conversation, `to-tickets` breaks work
into many, `triage` advances issues that already exist, `wayfinder` files decisions. On GitHub the gap
is one `gh issue create`; on a local tracker it is a hand-written file following a convention that is
easy to get wrong. Worth its own small skill one day. It is not roadmapping, and nothing that lands in
it belongs in the roadmap.

### Frictions accepted

- **Two dependency models.** Roadmap `Depends on` orders *outcomes*; ticket blocking edges order
  *edits*. Both are needed, at different granularities. They are not synchronised, and
  the roadmap skill does not generate ticket edges.
- **Two sources of truth about state.** Reality lives on the tracker; the register is a copy that
  ages. Close-out is the resynchronisation, not a background automatism.
- **A vocabulary collision.** `to-tickets` calls its tickets "tracer-bullet vertical slices". Keep
  *slice* for the roadmap unit and never call a ticket a slice in these documents.

## What changes relative to `plan-slices`

`plan-slices` is not invalidated: it keeps its own template, validator, tests and the 33 payload
files under `evals/plan-slices/recipe-app/`. The new skill is built **beside** it, and it is retired
once the new one stands. The two are never used together on the same project; the one intended
overlap is transitional — `plan-slices` as a yardstick against which to judge the first roadmaps.
Until the retirement lands, `slice` unqualified means the roadmap unit, and the `plan-slices` unit is
a **plan slice**.

The format diverges on every axis, which is why nothing is shared:

| | `plan-slices` | roadmap |
|---|---|---|
| Artifact | one file, written once | `.roadmap/`, living |
| Goal | implicit in the sources | declared, recorded, re-checked at every update |
| Scale | unbounded | `NOW` capped at ~15; granularity absorbs the problem's size |
| Identity | position number, renamed on every edit | id minted at promotion, never recycled |
| Metadata | inline in the slice body and title tags | register columns, comparison fields only |
| Dependencies | unpublished, carried by order | `Depends on` column |
| State | none | readiness × executor |
| Horizons | three sections of slices | register + candidates + exclusions |
| Deferral | `LATER` entry with a promotion trigger | candidate, no trigger, no id |
| Slice fields | `Includes` / `Verification` / `Learning / risk` / `Outcome` | `Audience` / `Includes` / `Verification` / `Learning target` / `Excludes` / `Open decisions` + `Requested by` / `Spec` / `Tickets` / `ADRs` |

The validator also grows from checking one file to checking a graph: every register row resolves to a
slice document and back, every `Depends on` resolves to a row, no id is recycled or non-monotonic
across `slices/` and `archive/`, no candidate or exclusion carries an id, readiness and executor hold
legal values. It counts the register and warns past the cap without failing — exceeding it is a signal
to the author, and failing on it would be grading the map instead of checking it.

New homes: `design/roadmap/` for this document and its glossary — already applied — `evals/roadmap/`
for the scenarios, and inside the skill `assets/roadmap-template.md`,
`scripts/validate_roadmap.py`, and the roadmap rules as a reference file the drawing branch loads on
its own.

## Open questions

- Where a spike sits in a living roadmap. The practice is wanted, the location is not settled:
  `kind: spike` in the register makes it visible and schedulable but demands the vertical outcome a
  spike by definition lacks; leaving it to `wayfinder` under `needs-decision` keeps it out of the
  comparison view; a `Non-product work` section reintroduces a second place to look.
