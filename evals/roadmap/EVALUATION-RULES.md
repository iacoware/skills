# Evaluation rules

What to look for in a map produced by `skills/roadmap/SKILL.md`, and in the session that produced it,
to notice that a change to the skill broke something it used to get right. How to run one review is
in [`REVIEW-WORKFLOW.md`](REVIEW-WORKFLOW.md); these rules are walked at its step 4, and by the router
scenarios that follow it.

**These are rules about the skill, not about any one scenario.** They carry over unchanged to a new
one. What is specific to a scenario lives beside its sources — for `recipe-app`, in
`recipe-app/EVALUATION-BRIEF.md`, which the workflow opens before these rules, and in
`recipe-app/reference-roadmap/`, which it opens strictly after.

**Half the evidence is not in the files.** The skill is a conversation that ends in one proposed
block, so what it asked, what it declined to write and what it put to the author are as readable as
what it wrote — and several rules below have no artifact at all. Read the transcript.

**This is not a grading rubric and produces no score.** A check that fails is a question — did the
skill stop asking for this, or did the model have a bad day? One run cannot tell you. Two in a row
can.

**A check is admitted when the skill states the clause it guards**, and every rule below names that
clause. Where the clause lives in `references/`, the reference is named with the section of
`SKILL.md` that loads it: those files are the skill's, and § 3 and the opening of the router send the
session to them. **If a check fails against a clause the skill no longer states, the defect is in the
check.** Rewrite it or delete it. The list describes the skill, it does not govern it.

**The ids are a fresh sequence and inherit nothing.** `evals/plan-slices/EVALUATION-RULES.md` carries
its own `R-` numbers, inherited from a ledger that retired on 2026-08-11 and that was about a plan
document; nothing in it was about this format. The two lists are unrelated and must be cited with
their file when both are open. Here ids are labels, not an order: a new check takes the next free
number and no id is ever reused.

**A `⚠ Has failed` mark carries the runs a check has already gone red on**, and a
`⚠ Watch the opposite failure` mark sits on the rules whose overcorrection would cost more than the
failure they guard. The first evidence arrived on 2026-08-20: one drawing and three router scenarios,
recorded below on R-005, R-007, R-009 and R-015. One run is still a question — a mark says a check
went red once, not that the skill is broken there.

## The situation

- **R-001** — The session established the situation before deciding anything: `.roadmap/roadmap.md`
  if it is there with its goal, themes, register, `Assumptions`, `Open questions`,
  `Cross-functional concerns` and both horizons, plus `slices/` and `archive/`. What was delivered
  was **asked**, never read off a tracker or inferred from the working tree. `SKILL.md` § 1.
- **R-002** — Every id was minted by increment from the high-water mark across `slices/` and
  `archive/`, and none was recycled — not after a retirement, not across a redraw. `SKILL.md` § 1 and
  § 4; `references/slice-rules.md`, *Identity*. *Recycling across both directories is checked by the
  validator; that the mint was the high-water mark plus one is reading.*

## What the input claims about

- **R-003** — An input that widens the reach of a capability the goal already promises is treated as
  work: the `Goal` line, the themes and `Ordering criteria` are untouched, and nothing is redrawn.
  `SKILL.md` § 2, *Destination or path*, first trap.
  ⚠ **Watch the opposite failure.** Work is the default by a wide margin, and a session that reads
  everything as work never redraws anything. What distinguishes the two is what the input
  contradicts, never how large it sounds.
- **R-004** — An input contradicting an invariant under `Cross-functional concerns` or an exclusion
  under `OUT-OF-SCOPE` is not admitted as a row on the strength of how small the change is. Cost and
  altitude are unrelated. `SKILL.md` § 2, *Destination or path*, second trap.
- **R-005** — An input that cannot be reconciled with the recorded goal — it does not serve it, and it
  is not an exclusion either — produces a question: the goal on file, what the input looks like from
  where the map sits, which of the two holds. Never an inference, and never a redraw taken
  unilaterally. `SKILL.md` § 2, *When the input cannot be reconciled*.
  ⚠ **Watch the opposite failure.** A session that asks on every input turns a re-truing into an
  interview. The question is owed exactly when the reconciliation fails, and the slice-or-spike
  reading never owes one. **Observed, in its mildest form, on all three router scenarios of
  2026-08-20**: each owed question was asked correctly and each arrived with a second one attached to
  it — conditional, hedged, and unasked for. Nothing was inferred and no session asked instead of
  deciding, so no check went red; it is the direction to watch, not yet a failure.
- **R-006** — A capability already sitting in `LATER` is **promoted**, not admitted anew: the
  candidate line goes, the row takes the next id, its document appears in `slices/`, and
  `Requested by` records what produced it. A candidate's presence is a licence to schedule and never
  a licence to skip *does it serve the goal*. `SKILL.md` § 4, *Promotion* and *Admission*.
- **R-007** — Work whose honest `Verification` states a measurement rather than a capability somebody
  can exercise is minted as a spike, and proposed in the block without a question, since nothing
  about the destination is in doubt. `SKILL.md` § 2, *Slice or spike*;
  `references/slice-rules.md`, *The spike test*.
  ⚠ **Has failed.** Router scenario 3, 2026-08-20. The session read the input correctly, found the
  unknown, and split it out of the row that could not carry it — then minted it `kind: enabler`. The
  row it wrote has a spike's `Verification` (every clause a declared number), a spike's
  `Learning target`, and an `Audience` naming the people building it. Only the column disagreed. The
  enabler definition in `references/slice-rules.md` also promises to *resolve one material
  uncertainty*, which is the overlap to watch on the next run before anything is rewritten.
  ⚠ **Watch the opposite failure.** Every uncertain row turning into a spike. Uncertainty is the
  learning target of an ordinary row; what makes a spike is that there is no outcome to deliver.

## Drawing the map

- **R-008** — Every theme is a product promise in product language, and every boundary carries a
  recorded split or merge verdict. No two independently schedulable value areas were merged to keep
  the count down. `SKILL.md` § 3 → `references/drawing-the-map.md`, *Themes*.
- **R-009** — Every theme's `First validator` is an existing `NOW` row that validates the theme's
  *complete* promise, and is not `kind: enabler` unless the `Promise` cell says the promise is to a
  developer. `references/drawing-the-map.md`, *Themes*. *That the reference resolves to a row is
  checked by the validator; coverage and kind are reading.*
  ⚠ **Has failed.** First drawing, 2026-08-20. The `cattura` promise was written with two halves —
  paste a link and the recipe is in, and an escape hatch for pages that will not be read — and its
  first validator was the link row alone. The escape hatch was two rows further down. Either half of
  the promise was one half too many, or the validator was the wrong row; the map said neither.
- **R-010** — A row serving every promise and cancellable with none carries `theme: —` rather than
  being pinned to one. `references/drawing-the-map.md`, *Themes*; `assets/roadmap-template.md`.
- **R-011** — Greenfield draws the repository row and the walking skeleton as two rows. The skeleton
  reaches the datastore at runtime through the real driver and connection mode and applies one
  non-domain migration, and carries no domain entity, no authentication and no tenancy.
  `references/drawing-the-map.md`, *The two prerequisites* — the `Oversized` and `Hollow skeleton`
  failures.
- **R-012** — `Ordering criteria` is a ranked numbered list, and every departure from breadth before
  depth is named in the criterion that concedes it rather than left for the reader to notice.
  `references/drawing-the-map.md`, *Ordering for learning*.
- **R-013** — The scope boundary ships with the first row that persists data, one named resolver owns
  the current scope, the seam is stated under `Cross-functional concerns`, and `Assumptions` records
  what the rows before it may ignore. Identity deferred past the second row delivering behaviour to
  an end user is justified once in `Ordering criteria`, against named evidence.
  `references/drawing-the-map.md`, *The identity seam*.
- **R-014** — Every row preceding identity names its own audience, and no `Outcome` before it
  promises a user who cannot exist yet. `references/drawing-the-map.md`, *The identity seam*;
  `references/slice-rules.md`, *What makes a slice*.
- **R-015** — Every conflict and every undecided choice the brief lists left the sweep by exactly one
  of the three doors — an `Assumptions` line that names the reading taken and why, an `Open questions`
  line, or a spike before the first row it blocks — and every line traces to a theme or an id.
  Exposing is not resolving, and scope is the only thing that routes an entry between map altitude
  and a row: what blocks one row alone lives on that row and shows in its readiness.
  `references/drawing-the-map.md`, *What the map reports about its input*.
  ⚠ **Has failed.** First drawing, 2026-08-20. The sweep found the embedding-at-runtime conflict and
  named its reading; it missed the second one — manual entry skipping extraction against manual entry
  reusing the extraction engine and schema — and took the first side in an `Excludes` bullet with no
  line anywhere. The hand-written reference had the same hole, closed in the same pass, which says
  the entry is easy to walk past rather than that the clause is weak.
  ⚠ **Watch the opposite failure.** A map that takes no reading and publishes everything as an open
  question. An assumption is what makes the map drawable; a map that assumes nothing has deferred its
  own shape.
- **R-016** — No `kind: enabler` row resolves uncertainties belonging to more than one `Subsystem` of
  the brief's uncertainty table: a verification that can fail for two of them would not say which
  decision to revisit. Several entries of one subsystem are one question.
  `references/slice-rules.md`, *The columns* → `kind: enabler`.
- **R-017** — Every published `Depends on` names a predecessor no controlled input and no narrower
  real precursor can stand in for, and what every row depends on — the repository, the skeleton — is
  not published. `references/drawing-the-map.md`, *Hard dependencies*. *That the ids resolve and close
  no cycle is checked by the validator; that the edge is hard is reading.*
- **R-018** — A redraw leaves `archive/` untouched, carries `OUT-OF-SCOPE` and
  `Cross-functional concerns` forward, lifts explicitly and with its cost stated any of them the new
  goal contradicts, gives every candidate its own verdict one at a time, re-justifies every row still
  open, and does not restart the counter. The goal, the themes, the register, the ordering criteria,
  `Assumptions` and `Open questions` are drawn from nothing.
  `SKILL.md` § 3, *A redraw is this branch with more input*; `references/drawing-the-map.md`, same
  heading.

## What makes a row

- **R-019** — A spike carries `kind: spike`, leaves `Audience` empty, has a dependent — a row naming
  it in `Depends on`, or `theme: goal` on its own row — and carries no timebox.
  `references/slice-rules.md`, *The spike test*. *The dependent is checked by the validator, and so
  is a non-spike leaving `Audience` unfilled; a spike that fills `Audience`, and the timebox, are
  reading.*
- **R-020** — Every slice has one vertical outcome and one learning target, both singular, and every
  material claim in `Learning target` has an observation in `Verification` stated so that delivery
  can refute it. Checking that data exists does not demonstrate its quality, latency or cost.
  `references/slice-rules.md`, *What makes a slice* and *Verification maps to the learning target*.
- **R-021** — Every `kind: enabler` passes the enabler tests: a real end-to-end production path,
  evidence the next product row needs, one material uncertainty or one high-leverage delivery
  pattern, tied to the product outcome it enables, and no speculative foundation beyond it.
  Horizontal setup wearing the label is enabler camouflage. `references/slice-rules.md`,
  *The columns* → `kind`.
- **R-022** — A row whose decision the sources leave open reads `needs-decision`, and its `Includes`
  and `Verification` are worded to defer to the pending decision rather than picking a side.
  Publishing one side unconditionally is silent contradiction. `references/slice-rules.md`,
  *The columns* → `readiness`.
- **R-023** — No row is one of the named failures: layer slices, infrastructure by accumulation, fake
  verticality, atomization, deferred safety, horizon dumping. `references/slice-rules.md`,
  *Named failures*.
- **R-024** — Every in-scope behaviour and every producer feeding a shared pipeline or adapter has one
  owning row or an explicit exclusion; a split distributes the original outcome and introduces none, a
  merge yields one outcome and one learning target, and the id stays with the learning target through
  either. `references/slice-rules.md`, *Splitting and merging a row*, *Identity*.

## The horizons

- **R-025** — A `LATER` line is what does not serve *this* goal, never what is merely unfinished, and
  it carries no id, no columns and no document. `SKILL.md` § 4, *Admission*;
  `references/slice-rules.md`, *Named failures* → horizon dumping. *Ids in the horizon sections are
  checked by the validator.*
- **R-026** — Every `OUT-OF-SCOPE` entry is written as the licence it gives — because this stays
  unsolved, the implementation may do without X, and this is the price — rather than as a line saying
  what will not be done. `references/drawing-the-map.md`, *What the map reports about its input*.

## Re-truing an existing map

- **R-027** — Close-out ran first, before anything else was decided: the row left the register, its
  document moved to `archive/` unchanged, and `ADRs` was filled only for a decision that cleared the
  bar — hard to reverse, surprising without context, the result of a real trade-off. `SKILL.md` § 4,
  *Close-out first*.
- **R-028** — Absorption produced a state change or nothing. A line of `Assumptions` or
  `Open questions` that delivery answered **died** rather than being annotated; a row whose size,
  readiness, dependency or shape the evidence changed was changed. Three noes wrote nothing, and on a
  spike three noes were reported as a finding about the spike. `SKILL.md` § 4, *Then absorb the
  evidence* and *Three noes write nothing*.
- **R-029** — Retirement spent the id and **deleted** the document; nothing undelivered reached
  `archive/`. `SKILL.md` § 4, *Retirement*.
- **R-030** — The cap was checked whenever a row was added, and an addition that would overflow it
  forced a merge or a deferral instead of a longer list. Below the floor and past the cap are
  findings put to the author, not defects silenced. `SKILL.md` § 4, *Admission*;
  `references/drawing-the-map.md`, *The cap is a finding, not a budget*. *Both bounds are checked by
  the validator, as warnings.*

## Closing the session, and handing over

- **R-031** — The coverage question was re-asked — does what is left in `NOW` still reach the goal —
  on both branches and whatever the input was. `SKILL.md` § 5.
- **R-032** — One block of changes was proposed and one confirmation asked, with every operation the
  session found in it. Not files written one at a time with a question between each, and nothing
  written before the confirmation. `SKILL.md` § 5.
- **R-033** — The validator was run after writing, every `ERROR` was fixed, and every `WARNING` was
  put to the author rather than silenced. `SKILL.md` § 5, *Run the validator*.
- **R-034** — Handover happens only for a `ready` row, derives the `triage` label from readiness and
  executor and stores it nowhere, and routes by kind: a slice to the clarifying conversation —
  `/grill-with-docs`, or `/wayfinder` when it is big and foggy — and straight to `/to-spec` only when
  an earlier session already clarified it and left no `needs-decision` and no `needs-info`; a spike
  to `/prototype` or `/wayfinder`, never to `/to-spec`. What the system does not have is said rather
  than invented. `SKILL.md` § 6.
