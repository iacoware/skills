# Where `plan-slices` is going — a roadmapping tool

Written 2026-08-13, from a design conversation. This is the goal and the reasoning behind it, not a
plan. The plan comes next, in its own session, and this document is its source.

## The problem

`plan-slices` is a **one-shot document generator**. It reads sources, cuts a delivery plan into
vertical slices, validates the structure, and stops. Its three branches — create, review,
split/merge/reorder — all assume the plan is written once and then corrected. Slices are numbered by
position, so every edit renumbers them; step 5 says so explicitly, and calls repairing the dangling
references part of the job.

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
- **Readability.** One dense document holding roadmap, cross-functional contracts and every slice
  body at once. The overview and the detail want different files.

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
.planning/plan.md         ROADMAP   themes, horizons, order for learning        ← the gap
.planning/slices/S3-*.md  SLICE     one outcome, one learning target, a trigger ← the gap
      ↓
conversation              CLARIFY   free, /grilling, /grill-with-docs; /wayfinder when big and foggy
      ↓ to-spec                     captures the conversation — it does not interview
spec, on the issue tracker  HOW     seams, user stories, implementation decisions
      ↓ to-tickets                  only when the work exceeds one session
tickets                     EXECUTION  blocking edges, one context window each
      ↓ implement                   one open ticket at a time, working the frontier
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
`needs-decision` and no `needs-info` open. Then the conversation happened, it just happened earlier,
and `@slice.md` with `/to-spec` is honest. Telling those two cases apart is what the readiness states
are for.

`to-tickets` produces a flat dependency graph with no themes, no horizons, no promotion triggers, no
learning targets and no replanning: it is deliberately **ephemeral**, and a ticket dies when it
closes. The roadmap is **durable** and decides *what to do next*, not *how*. Nothing at that altitude
exists in the installed set, and that is the whole of what gets built here.

The post-greenfield path — an idea arrives, gets clarified, gets built — is already covered end to
end by that chain, with no roadmap involved. That is not an escape hatch to be written into the
skill; it is the existing chain used without it.

## Decisions taken

**Artifact layout.** `.planning/plan.md` is the readable overview: sources, ordering criteria, theme
table, the slice index, `LATER`, `OUT-OF-SCOPE`, decision checkpoints, open questions.
`.planning/slices/` holds one document per slice, expandable at will. Delivered slices move to an
archive; their ids stay burned for ever.

**One plan per project, not per initiative.** A new capability extends the existing `plan.md`.

**The slice index is the only place the metadata lives** — id, theme, horizon, readiness, executor,
depends-on, one-line outcome, one row each. Repeating those fields inside the slice document is what
made the current output feel cluttered in the first place.

**Stable ids, assigned on entry to the register.** Including `LATER` entries, so references are
stable before promotion. Ids are identity, not position: document order carries the delivery order.

**A `LATER` entry is a line in `plan.md`, not a file.** Its file is born at promotion. Giving a
`LATER` entry a document invites specifying it, and `LATER` is vague by design.

**Dependencies get published.** `Depends on: S1, S3`. The current skill forbids this — order carries
the constraint — which holds only while the plan is written once. A later session that promotes or
reorders would otherwise violate a constraint recorded nowhere.

**Traceability gets published too.** Source-to-slice tracing and adjacent split/merge verdicts
currently live "in reasoning, not in the published plan". In a living roadmap the previous session's
reasoning no longer exists.

**Two axes of state, not one.** *Readiness* reuses the canonical `triage` vocabulary —
`ready-for-agent`, `ready-for-human`, `needs-info` — plus one roadmap-only state, `needs-decision`,
for a choice the author owns and has not made (`needs-info` means waiting on somebody else).
*Executor* is separate — `agent` | `human` | `mixed` — because most infrastructure slices are mixed:
a human creates the project and the secrets, an agent writes the IaC.

Each state has its tool downstream: `needs-info` is what `to-questionnaire` consumes,
`needs-decision` what `wayfinder` consumes — its decision tickets are questions whose resolution is a
decision — and `human` or `mixed` executors are what `wizard` consumes.

**No token budget on a slice.** Sizing to a single context window is `to-tickets`' job, and it does
it better because by then a spec exists. The slice keeps a coarse size signal whose only effect is
routing: large goes through `to-tickets`, otherwise straight to `to-spec`. A token count no validator
can check is a hollow ritual.

**The slice document holds no spec.** It holds why now, for whom, what evidence settles the doubt,
what blocks it. Seams, user stories and contracts are born in `to-spec` and live on the tracker.
Duplicating them yields two truths that diverge at the first ticket.

**Its fields are chosen as what `to-spec` cannot invent** — audience, learning target, verification
evidence, open decisions, exclusions. Those are also the ones that carry across: audience and learning
target become the spec's *Problem Statement*, exclusions become its *Out of Scope*, and the
verification evidence constrains its *Testing Decisions*. Anything a capture step could plausibly have
written by itself does not need to be on the slice.

**The slice carries outbound references.** `Spec:` and `Tickets:`, filled at promotion, so close-out
knows what was delivered instead of reconstructing it by hand every cycle.

## The skills

- **`roadmap-create`** — greenfield, or a capability large enough to have themes of its own. Full
  ceremony. Writes `.planning/plan.md` and `.planning/slices/`; extends an existing plan rather than
  starting a second one.
- **`roadmap-update`** — the only mutating skill afterwards. Reconcile first (close out what was
  delivered, absorb the evidence it produced), then promote from `LATER`, then admit new work. Both
  of its jobs are conversations, not generations: it proposes a block of changes and asks for
  confirmation once.
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
- **`roadmap-update` hands over, it does not drive.** It updates the plan, marks the slice ready, and
  suggests the next step if it is available on the system — the clarifying conversation,
  `/grill-with-docs` normally or `/wayfinder` when the slice is big and foggy, never `/to-spec`
  directly, since a capture step has nothing to capture yet. The two stacks stay independent.
- **Degrade cleanly.** Read `docs/agents/issue-tracker.md` when it is there; when it is not, say so
  and carry on, as the installed skills do.
- **Do not extend the triage label vocabulary.** `needs-decision` is a roadmap state, never a tracker
  label.

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
- **The slice archive under `.planning/` becomes the only durable register of what was delivered and
  what it taught.** That raises close-out from hygiene to the point of the exercise, and justifies
  keeping it rich rather than a status line.

The boundary still holds: the roadmap records that a **slice** is closed and what it produced. The
state of individual tickets stays the tracker's business, badly kept though it currently is. A fix for
that belongs in `docs/agents/issue-tracker.md`, which the setup skill declares hand-editable — not in
these skills.

Adjacent and deliberately out of scope: there is no skill for *capture and park* — filing one small
item you do not intend to do now. `to-spec` captures a whole conversation, `to-tickets` breaks work
into many, `triage` advances issues that already exist, `wayfinder` files decisions. On GitHub the gap
is one `gh issue create`; on a local tracker it is a hand-written file following a convention that is
easy to get wrong. Worth its own small skill one day. It is not roadmapping, and nothing that lands in
it belongs in `plan.md`.

### Frictions accepted

- **Two dependency models.** Roadmap `Depends on` orders *outcomes*; ticket blocking edges order
  *edits*. Both are needed, at different granularities. They are not synchronised, and
  `roadmap-update` does not generate ticket edges.
- **Two sources of truth about state.** Reality lives on the tracker; `plan.md` is a copy that ages.
  Close-out is the resynchronisation, not a background automatism.
- **A vocabulary collision.** `to-tickets` calls its tickets "tracer-bullet vertical slices". Keep
  *slice* for the roadmap unit and never call a ticket a slice in these documents.

## What this invalidates

The format contract changes: stable ids, published dependencies, readiness and executor fields, and
a multi-file layout. That breaks `assets/plan-template.md`, `scripts/validate_plan.py` and its tests,
and the 33 payload files under `evals/plan-slices/recipe-app/`. The validator also grows from
checking one file to checking a graph: every index row resolves to a slice document and back, every
`Depends on` resolves, no id is recycled, every `LATER` trigger names a slice that exists.

The evals are rebuilt once the format has settled, not before.

## Open questions

- Where the shared reference lives, and whether the three skills carry it by reference or by copy.
- Whether `roadmap-review` is worth a skill of its own from day one, or starts as a mode of
  `roadmap-update` and separates once its criteria diverge.
