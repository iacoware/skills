# Why the roadmap skill is shaped this way

The reasoning behind [`skills/roadmap`](../../skills/roadmap). The skill is the authority on what it
does — `SKILL.md` routes, `references/` holds the rules with the reasons that bear on applying them,
`assets/` fixes the format, and the validator checks what is checkable. What is left here is what the
payload has no room to carry: the constraints that hold the tool to its purpose, and the roads not
taken. A rule that a session needs while working belongs in the payload, not on this page.
[`CONTEXT.md`](./CONTEXT.md) fixes the vocabulary and is binding.

## What the tool is for

A roadmap that is easy to read, visible and evolvable. Visible because the overview fits on one
screen; evolvable because a single row can be expanded, promoted or closed without touching anything
else.

It is a **sense-making tool, not a precision instrument**. Its job is to let the author say *these
are the twelve rows that get me to the goal*, and then argue with that sentence. Whatever buys
precision at the cost of that sentence is a non-goal, and stays out on purpose:

- no dates, no estimates, no percentage complete, no velocity, and no token budget — sizing to a
  context window is `to-tickets`' job, which does it better because by then a spec exists, and a
  number nothing can check is a hollow ritual;
- no field nobody re-reads. Promotion triggers and decision checkpoints were dropped for exactly this
  reason: both recorded *when this evidence arrives, change this decision*, which a human re-reading a
  living roadmap can already see. Anything of that family gets dropped the same way;
- the validator checks referential coherence, never judgement: it may not demand that a field be
  filled *well*. A validator that grades content turns the tool into a form.

This is the constraint most likely to erode one revision at a time, which is why it is written down.

**What does not go through the roadmap.** Vertical slicing earns its cost whenever a goal is declared
and the way to it is unknown — at the start of a greenfield project, and again at every goal after
that. It does not earn it on a copy change, a small refactor, or an idea that does not serve the
current goal. Those go from the conversation into `to-spec` onwards, with no roadmap involved. That
is not an escape hatch to be written into the skill; it is the chain used without it.

## Roads not taken

**One skill, not two.** An earlier draft split it into `roadmap-create` and `roadmap-update`, by what
each reads. That split asks the author to pick the verb before describing the situation, which is
what the skill refuses to do one level down with its five operations — and the situation is legible
without asking: `.roadmap/` exists or it does not, the goal is new or it is not. The cost the split
was avoiding is real but misattributed: dragging the theme ceremony into a routine update would make
the tool unbearable where it should be lightest, and that is fixed by loading the roadmap rules on
one branch only. Two skills would also have created a problem of their own, since `skills add` copies
one folder at a time.

**No concurrency, so no machinery to buy it.** Every way of serving two goals at once — a `Goal`
column, `.roadmap/<goal>/`, two maps side by side — pays in the focus the tool exists to impose:
`NOW` becomes the union of two paths, coverage has to be asked twice, and the register stops
answering *what is the path* because there are two. If the author cannot say which of two goals comes
first, that is the decision the roadmap is there to force, not to record: either they are one goal at
a higher altitude, or one of them is `LATER`.

**The horizons are separated by their relation to the goal, not by how much attention each
deserves**, which is unfalsifiable. That axis is what turns promotion into a real moment of
sense-making — *this thing I filed as peripheral is on the path after all* — and the shapes follow
from it: the register **is** `NOW`, so having an id is the same fact as having a row, and a candidate
gets no id, no column and no document, because a document would invite specifying it and a candidate
is vague by design.

**No gradient of detail inside `NOW`.** The last row on the path is genuinely foggier than the first,
but the fog has nowhere to accumulate: the detail of `S1` is born downstream, in the clarifying
conversation and the spec, never in the roadmap. What differs between near and far is confidence, and
confidence already has its expression — a fuller `Open questions`, and `readiness: needs-decision`.
No new field, nothing to keep in sync.

**The register names the row by its title, and the outcome moves to the document.** A title is what
the eye reads down a column of fifteen rows, while a sentence per row turns the table into prose and
makes the columns beside it unreadable. The outcome is not lost: it opens the slice document, so each
artifact carries the form of the answer it is read for. The title links to the document and the
document links back; ids stay plain text on both sides, because an identity that renders as a link
twice in one row is noise, and it is the filename that resolves it anyway.

**Readiness and executor do not reuse the `triage` label strings.** Deriving `ready-for-agent` and
`ready-for-human` at handover keeps `ready` + `mixed` meaningful; storing the labels instead would
have made `ready-for-agent` + `mixed` writable and meaningless. Each state also has its own tool
downstream — `needs-info` feeds `to-questionnaire`, `needs-decision` feeds `wayfinder`, a `human` or
`mixed` executor feeds `wizard`.

**The slice document holds no spec.** Seams, user stories and contracts are born in `to-spec` and
live on the tracker; duplicating them yields two truths that diverge at the first ticket. Its fields
are chosen as what `to-spec` cannot invent, which is also what carries across: `Audience` and
`Learning target` become the spec's *Problem Statement*, `Excludes` its *Out of Scope*, and
`Verification` constrains its *Testing Decisions*. Anything a capture step could plausibly have
written by itself is not on the slice. Its four references — `Requested by` inbound, `Spec`,
`Tickets`, `ADRs` outbound — point and hold no content, so they do not reopen the rule;
`Requested by` publishes traceability that a living roadmap cannot leave in reasoning, because the
previous session's reasoning no longer exists.

**`Cross-functional concerns` is the only place a rule holds for *every* row**, and the anchor for
the identity seam. Without it each slice restates the same paragraph, which is the repetition this
format exists to remove.

## The integration boundary

The roadmap is the top of a chain whose lower halves already exist as installed skills. Reuse them:
rebuilding `to-spec` and `to-tickets` would replace two mature skills with something answering a
different question.

```
.roadmap/                   ROADMAP   themes, the register, order for learning
      ↓                     CLARIFY   conversation: /grill-with-docs, /wayfinder when big and foggy
spec, on the issue tracker  HOW       seams, user stories, implementation decisions
      ↓ to-tickets                    only when the work exceeds one session
tickets                     EXECUTION blocking edges, one context window each
```

What `to-tickets` produces is deliberately **ephemeral**, and a ticket dies when it closes. The
roadmap is **durable** and decides *what to do next*, not *how*. Nothing at that altitude existed in
the installed set, which is the whole of what this skill adds.

Couple loosely, on purpose. Close-out **asks** what was delivered rather than interrogating the
tracker, which would bind the skill to whichever tracker is configured. The skill **hands over and
does not drive**: it marks the row ready and suggests the next step, never `/to-spec` directly,
because the delta between a thin row and a spec is precisely what the clarifying conversation
produces. It **degrades cleanly**, reading `docs/agents/issue-tracker.md` when it is there and saying
so when it is not. And it does not extend the `triage` vocabulary in either direction.

**A local tracker has no notion of *done*.** Its `Status:` vocabulary is the five triage roles, none
of which means delivered, and nothing writes it — `implement` never mentions the ticket it
implements. So close-out asking is not merely the loosely-coupled choice but the only possible one,
and `.roadmap/archive/` is the only durable register of what was delivered. Not of what it *taught* —
that crystallises in the code and, when it clears the bar, in `docs/adr/` — which is why the archived
document keeps the thread by pointing.

**Frictions accepted.** Roadmap `Depends on` orders *outcomes* while ticket edges order *edits*: both
are needed, at different granularities, and they are not synchronised. Reality lives on the tracker
and the register is a copy that ages: close-out is the resynchronisation, not a background
automatism. And `to-tickets` calls its tickets "tracer-bullet vertical slices": keep *slice* for the
roadmap unit and never call a ticket a slice in these documents.

Adjacent and deliberately out of scope: there is no skill for *capture and park* — filing one small
item you do not intend to do now. Worth its own small skill one day; it is not roadmapping, and
nothing that lands in it belongs in the roadmap.
