# Where the roadmap skill is going — a roadmapping tool

Written 2026-08-13 from a design conversation, revised 2026-08-19 after a nomenclature grilling.
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

Four things follow from that, none of which the skill has today:

- **Identity.** A slice needs a stable id (`S0`, `S1`, …) that survives promotion, reordering and
  insertion, and is never recycled. Position-based numbering makes every revision a rename.
- **Readiness.** A slice can be blocked on a decision the author has not made, or on information
  somebody else holds. Today the plan carries one global `Open questions` section and no per-slice
  state.
- **Human work.** Credentials, cloud consoles, DNS, billing, app-store enrolment. The skill assumes a
  single executor and cannot say "this one is not delegable".
- **Readability.** One dense document holding the whole map, the cross-functional concerns and every
  slice body at once. The overview and the detail want different files.

## What the tool is for

A roadmap that is **easy to read, visible, and evolvable**. Visible because the overview fits on one
screen; evolvable because a single slice can be expanded, promoted, or closed without touching
anything else.

### Two regimes, and the line between them

Vertical slicing earns its cost at the **start of a greenfield project**: it delivers value early and
attacks the technical challenges at the right moment. Once the project is standing, work arrives as
an **idea** that needs clarifying, and which may then split into slices — or may simply be
implemented, with no roadmap involvement at all.

So the durable separation is not create/update/review. It is:

- **Roadmap rules** — themes, first validator per theme, breadth before depth, repository
  prerequisite and walking skeleton, ordering for learning. These answer *in what order do we
  discover things*. They matter at the start and go inert afterwards.
- **Slice rules** — what makes a valid slice, split and merge tests, verification mapping to the
  learning target, readiness, executor, id. These hold for ever, in both regimes.

The shared reference is the format contract plus the slice rules. The roadmap heuristics live only in
the creating skill. Otherwise every post-greenfield idea drags the theme ceremony behind it, and the
tool becomes unbearable exactly where it should be lightest.

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
/roadmap-update            promote S7, mark it ready, hand over
/grill-with-docs S7        the slice document is the subject of the conversation
/to-spec                   captures that conversation; record the spec on the slice
/to-tickets <spec>         only if the work exceeds one session
/implement <ticket>        one at a time, working the frontier
/roadmap-update            close S7 out, absorb what it taught
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

The post-greenfield path — an idea arrives, gets clarified, gets built — is already covered end to
end by that chain, with no roadmap involved. That is not an escape hatch to be written into the
skill; it is the existing chain used without it.

## Decisions taken

**Artifact layout.** `.roadmap/roadmap.md` is the readable overview: sources, current state, ordering
criteria, the theme table, `Cross-functional concerns`, then the three horizons — the register under
`NOW`, the candidate list under `LATER`, the exclusions under `OUT-OF-SCOPE`. `.roadmap/slices/`
holds one document per open slice, `.roadmap/archive/` one per delivered slice, both named
`S<id>-<slug>.md`.

**One roadmap per project, not per initiative.** A new capability extends the existing roadmap.

**Three horizons, three shapes, and only `NOW` has identity.** The register **is** `NOW`: a table,
one row per slice, and having an id is the same fact as having a row. `LATER` is a list of
candidates and `OUT-OF-SCOPE` a list of exclusions — neither carries ids, columns, or documents.
`horizon` is a collective word in prose, never a field: a value that is constant down a column is not
information.

**The register holds the comparison metadata; the slice document holds the rest.** A field earns a
column when it is used to *compare slices and decide what comes first* — id, theme, kind, size,
readiness, executor, `Depends on`, and the one-line outcome. A field that only makes sense while
reasoning inside one slice belongs to that slice's document. Repeating register fields inside the
document is what made the current output feel cluttered in the first place.

**The register is the queue of open work.** Close-out removes the row and moves the document to the
archive. The register answers *what can I pick up now*; the archive answers *what did we deliver*.

**Stable ids, minted at promotion by monotonic increment.** The next id is the highest found across
`.roadmap/slices/` and `.roadmap/archive/`, plus one — the filenames carry it, so it is two directory
listings and no counter to keep in sync. Ids are identity, not position: register order carries the
delivery order.

**A `LATER` entry is a candidate: a line, never a file, and it has no id.** `LATER` is a focus tool —
everything it is not important to concentrate on now — not a backlog. From there a candidate dies or
is promoted, and promotion is what mints its id, its row, and its document. Giving a candidate a
document invites specifying it, and a candidate is vague by design.

**No promotion triggers and no decision checkpoints.** Both recorded the same shape — *when this
evidence arrives, change this decision* — and both state something a human reading the roadmap can
already see. A living roadmap is re-read at every update; the condition does not need storing.

**`OUT-OF-SCOPE` declares the boundaries of the solution.** It is not a graveyard: several trade-offs
the implementation takes are defensible *precisely because* those problems are declared unsolved.
Recording the exclusion is recording the licence for the trade-off.

**Dependencies get published**, as a `Depends on` column holding ids. The current skill forbids this
— order carries the constraint — which holds only while the plan is written once. A later session
that promotes or reorders would otherwise violate a constraint recorded nowhere.

**Traceability gets published too.** Source-to-slice tracing and adjacent split/merge verdicts
currently live "in reasoning, not in the published plan". In a living roadmap the previous session's
reasoning no longer exists. Where exactly it lands is still open — see below.

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

**The slice carries three outbound references.** `Spec` and `Tickets`, filled at promotion, and
`ADRs`, filled at close-out. They point and hold no content, so they do not reopen the rule above.

**`Cross-functional concerns` survives, with the template's five entries.** It is the only place a
rule holds for *every* slice — authorization, validation and errors, operability, accessibility and
security, data integrity and recovery — and the anchor for the identity seam. Without it each slice
restates the same paragraph, which is the repetition this format exists to remove.

## The skills

- **`roadmap-create`** — greenfield, or a capability large enough to have themes of its own. Full
  ceremony. Writes `.roadmap/roadmap.md` and `.roadmap/slices/`; extends an existing roadmap rather
  than starting a second one.
- **`roadmap-update`** — the only mutating skill afterwards. Its three operations have one name each:
  **close-out** (remove the delivered slice from the register, archive its document, absorb the
  evidence it produced), **promotion** (a candidate becomes a slice), **admission** (new work
  enters). Close-out runs first. All three are conversations, not generations: the skill proposes a
  block of changes and asks for confirmation once.
- **`roadmap-review`** — read-only audit, running the validator first.

The validator stays a script, invoked automatically at the end of all three and callable by hand. A
skill whose body is "run this script" adds surface and nothing else.

## The integration boundary

Reuse the installed chain; do not rebuild it. Rebuilding `to-spec` and `to-tickets` would replace two
mature skills with something answering a different question.

Couple loosely, on purpose:

- **Close-out asks.** It does not interrogate the tracker for what is closed. Interrogating would
  bind these skills to whichever tracker is configured and would depend on slice references being
  reliable; asking is more robust, and close-out is an explicitly manual resynchronisation step. On a
  local tracker there is also nothing to interrogate — see below.
- **`roadmap-update` hands over, it does not drive.** It updates the roadmap, marks the slice ready,
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
these skills.

Adjacent and deliberately out of scope: there is no skill for *capture and park* — filing one small
item you do not intend to do now. `to-spec` captures a whole conversation, `to-tickets` breaks work
into many, `triage` advances issues that already exist, `wayfinder` files decisions. On GitHub the gap
is one `gh issue create`; on a local tracker it is a hand-written file following a convention that is
easy to get wrong. Worth its own small skill one day. It is not roadmapping, and nothing that lands in
it belongs in the roadmap.

### Frictions accepted

- **Two dependency models.** Roadmap `Depends on` orders *outcomes*; ticket blocking edges order
  *edits*. Both are needed, at different granularities. They are not synchronised, and
  `roadmap-update` does not generate ticket edges.
- **Two sources of truth about state.** Reality lives on the tracker; the register is a copy that
  ages. Close-out is the resynchronisation, not a background automatism.
- **A vocabulary collision.** `to-tickets` calls its tickets "tracer-bullet vertical slices". Keep
  *slice* for the roadmap unit and never call a ticket a slice in these documents.

## What changes relative to `plan-slices`

`plan-slices` is not invalidated: it keeps its own template, validator, tests and the 33 payload
files under `evals/plan-slices/recipe-app/`. The new skills are built **beside** it, and it is
retired once they stand. The two are never used together on the same project; the one intended
overlap is transitional — `plan-slices` as a yardstick against which to judge the first roadmaps.
Until the retirement lands, `slice` unqualified means the roadmap unit, and the `plan-slices` unit is
a **plan slice**.

The format diverges on every axis, which is why nothing is shared:

| | `plan-slices` | roadmap |
|---|---|---|
| Artifact | one file, written once | `.roadmap/`, living |
| Identity | position number, renamed on every edit | id minted at promotion, never recycled |
| Metadata | inline in the slice body and title tags | register columns, comparison fields only |
| Dependencies | unpublished, carried by order | `Depends on` column |
| State | none | readiness × executor |
| Horizons | three sections of slices | register + candidates + exclusions |
| Deferral | `LATER` entry with a promotion trigger | candidate, no trigger, no id |
| Slice fields | `Includes` / `Verification` / `Learning / risk` / `Outcome` | `Audience` / `Includes` / `Verification` / `Learning target` / `Excludes` / `Open decisions` + `Spec` / `Tickets` / `ADRs` |

The validator also grows from checking one file to checking a graph: every register row resolves to a
slice document and back, every `Depends on` resolves to a row, no id is recycled or non-monotonic
across `slices/` and `archive/`, no candidate or exclusion carries an id, readiness and executor hold
legal values.

New homes: `design/roadmap/` for this document and its glossary — already applied — `evals/roadmap/`
for the scenarios, and inside each skill `assets/roadmap-template.md` and
`scripts/validate_roadmap.py`.

## Open questions

- Whether three skills is the right shape at all. `roadmap-create` / `roadmap-update` /
  `roadmap-review` is the split assumed above, and its efficacy has not been tested; it wants its own
  session before any of it is written.
- Where the shared reference lives, and whether the three skills carry it by reference or by copy.
  `skills add` copies one skill folder at a time, so a shared file either gets duplicated or breaks
  when a single skill is installed alone.
- Where published traceability lands. Source-to-slice tracing is per-slice reasoning, so by the
  register rule it belongs in the slice document — but the six fields fixed above have no room for
  it, and a seventh field named `Sources` would collide with the roadmap-level `Sources`.
  `Requested by` is the leading candidate, undecided.
- Where a spike sits in a living roadmap. The practice is wanted, the location is not settled:
  `kind: spike` in the register makes it visible and schedulable but demands the vertical outcome a
  spike by definition lacks; leaving it to `wayfinder` under `needs-decision` keeps it out of the
  comparison view; a `Non-product work` section reintroduces a second place to look.
