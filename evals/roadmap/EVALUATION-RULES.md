# Evaluation rules

What to look for in a map produced by `skills/roadmap/SKILL.md`, and in the session that produced it.
Walked when reading a run — [`REVIEW-WORKFLOW.md`](REVIEW-WORKFLOW.md) — and cited card by card in
[`recipe-app/SCENARIOS.md`](recipe-app/SCENARIOS.md). These are rules about the skill: they travel to
a new scenario unchanged, where `EVALUATION-BRIEF.md` and `reference-roadmap/` do not.

**Half the evidence is not in the files** — what the session asked, what it declined to write, what it
put to the author. Several rules below have no artifact at all: read the transcript.

**No score, and no verdict from one run.** A failed check is a question: did the skill stop asking for
this, or did the model have a bad day? Two runs in a row answer it. *Inconclusive* is a result —
record what the run did and did not do, cite the id, leave the mark off.

**A check is admitted only while the skill states the clause it guards**, which is why every rule
names one. If a check fails against a clause the skill no longer states, the defect is in the check:
rewrite it or delete it. The list describes the skill, it does not govern it.

**A red check is not permission to edit the skill.** Only one of three cases touches a clause — the
skill states it and the session ignored it, where one run records and two mean the clause is not doing
its job. The others are a check to rewrite, or a clause saying two things that overlap, which is a
writing failure reading like a model failure. The fix lands in the artifact that owns it — a rule
applied badly is a defect in `references/`, a field nobody can fill is a defect in the template —
never in `SKILL.md` by default, which is how a router grows back into a monolith.

**Never change the skill, the fixtures or the oracle to make a scenario pass.** This is what quietly
destroys an eval: the reviewer's sense of *good* drifts toward whatever the model last produced, and
the net ends up shaped like the thing it was meant to catch. A fixture moves when the state it stands
for moves; the oracle is rewritten when the sources change.

**Ids are labels and are never reused.** `⚠ failed` marks a check the skill has gone red on and has
not since been shown to pass; `⚠ opposite` marks the rules whose overcorrection would cost more than
the failure they guard.

## The situation

- **R-001** — The session **asked** what was delivered and established the standing state —
  `roadmap.md` with its goal, themes, register, `Assumptions`, `Open questions`,
  `Cross-functional concerns`, both horizons, plus `slices/` and `archive/` — rather than reading it
  off a tracker or inferring it from the working tree. § 1
- **R-002** — Every id minted by increment from the high-water mark across `slices/` and `archive/`,
  and none recycled: not after a retirement, not across a redraw. § 1, § 4; `slice-rules.md`
  *Identity*. *Validator: recycling. Reading: that the mint was the high-water mark plus one.*

## What the input claims about

- **R-003** — An input that widens the reach of a capability the goal already promises is treated as
  work: `Goal`, themes and `Ordering criteria` untouched, nothing redrawn. § 2, *Destination or path*.
  *⚠ opposite — work is the default by a wide margin, and a session that reads everything as work
  never redraws anything. What distinguishes the two is what the input contradicts, never how large it
  sounds.*
- **R-004** — An input contradicting an invariant under `Cross-functional concerns` or an exclusion
  under `OUT-OF-SCOPE` is not admitted as a row on the strength of how small the change is. Cost and
  altitude are unrelated. § 2, *Destination or path*.
- **R-005** — An input that cannot be reconciled with the recorded goal produces a question — the goal
  on file, what the input looks like from where the map sits, which of the two holds — never an
  inference and never a unilateral redraw. § 2, *When the input cannot be reconciled*.
  *⚠ opposite — a session that asks on every input turns a re-truing into an interview; the
  slice-or-spike reading never owes a question. The mild form to watch for is an owed question asked
  correctly with a second, hedged, unasked-for one attached.*
- **R-006** — A capability already in `LATER` is **promoted**, not admitted anew: the candidate line
  goes, the row takes the next id, its document appears in `slices/`, `Requested by` records what
  produced it. A candidate is a licence to schedule, never a licence to skip *does it serve the goal*.
  § 4, *Promotion* and *Admission*.
- **R-007** — Work whose honest `Verification` states a measurement rather than a capability somebody
  can exercise is minted as a spike, and proposed in the block without a question, since nothing about
  the destination is in doubt. § 2, *Slice or spike*; `slice-rules.md` *The spike test*.
  *⚠ failed three times out of three on scenario 3, never green: the reading fires and the routing
  does not — the measurement is recognised and then left inside the row it blocks. The fix is written
  in `slice-rules.md` *The spike test* and has never been demonstrated; the card says not to run it
  again.*
  *⚠ opposite — every uncertain row turning into a spike. Uncertainty is the learning target of an
  ordinary row; what makes a spike is that there is no outcome to deliver.*

## Drawing the map

- **R-008** — Every theme is a product promise in product language, every boundary carries a recorded
  split or merge verdict, and no two independently schedulable value areas were merged to keep the
  count down. § 3 → `drawing-the-map.md` *Themes*.
- **R-009** — Every theme's `First validator` is an existing `NOW` row that validates the theme's
  *complete* promise, and is not `kind: enabler` unless `Promise` says the promise is to a developer.
  `drawing-the-map.md` *Themes*. *Validator: that the reference resolves to a row. Reading: coverage
  and kind.*
  *⚠ failed — the shape to look for is a promise written with two halves whose first validator covers
  one of them. Either half was one too many, or the validator is the wrong row.*
- **R-010** — A row serving every promise and cancellable with none carries `theme: —` rather than
  being pinned to one. `drawing-the-map.md` *Themes*; `assets/roadmap-template.md`.
- **R-011** — Greenfield draws the repository row and the walking skeleton as two rows. The skeleton
  reaches the datastore at runtime through the real driver and connection mode and applies one
  non-domain migration; it carries no domain entity, no authentication, no tenancy.
  `drawing-the-map.md` *The two prerequisites* — the `Oversized` and `Hollow skeleton` failures.
- **R-012** — `Ordering criteria` is a ranked numbered list, and every departure from breadth before
  depth is named in the criterion that concedes it rather than left for the reader to notice.
  `drawing-the-map.md` *Ordering for learning*.
- **R-013** — The scope boundary ships with the first row that persists data, one named resolver owns
  the current scope, the seam is stated under `Cross-functional concerns`, and `Assumptions` records
  what the rows before it may ignore. Identity deferred past the second row delivering behaviour to an
  end user is justified once in `Ordering criteria`, against named evidence. `drawing-the-map.md`
  *The identity seam*.
- **R-014** — Every row preceding identity names its own audience, and no `Outcome` before it promises
  a user who cannot exist yet. `drawing-the-map.md` *The identity seam*; `slice-rules.md`
  *What makes a slice*.
- **R-015** — Every conflict and every undecided choice the brief lists left the sweep by exactly one
  of the three doors — an `Assumptions` line naming the reading taken and why, an `Open questions`
  line, or a spike before the first row it blocks — and every line traces to the themes and ids it
  touches, or to `goal` where it touches the whole map.
  Exposing is not resolving; scope is the only thing that routes an entry between map altitude and a
  row. `drawing-the-map.md` *What the map reports about its input*.
  *⚠ failed — C1, manual entry and the extraction engine, is the entry easiest to walk past: the side
  gets taken in an `Excludes` bullet with no line anywhere.*
  *⚠ opposite — a map that takes no reading and publishes everything as an open question. An
  assumption is what makes the map drawable.*
- **R-016** — No `kind: enabler` row resolves uncertainties belonging to more than one `Subsystem` of
  the brief's uncertainty table: a verification that can fail for two of them would not say which
  decision to revisit. Several entries of one subsystem are one question. `slice-rules.md`
  *The columns* → `kind: enabler`.
- **R-017** — Every published `Depends on` names a predecessor no controlled input and no narrower real
  precursor can stand in for, and what every row depends on — the repository, the skeleton — is not
  published. `drawing-the-map.md` *Hard dependencies*. *Validator: that the ids resolve and close no
  cycle. Reading: that the edge is hard.*
- **R-018** — A redraw leaves `archive/` untouched, carries `OUT-OF-SCOPE` and
  `Cross-functional concerns` forward, lifts explicitly and with its cost stated any the new goal
  contradicts, gives every candidate its own verdict one at a time, re-justifies every row still open,
  and does not restart the counter. Goal, themes, register, ordering criteria, `Assumptions` and
  `Open questions` are drawn from nothing. § 3 and `drawing-the-map.md`, *A redraw is this branch with
  more input*.

## What makes a row

- **R-019** — A spike carries `kind: spike`, leaves `Audience` empty, has a dependent — a row naming it
  in `Depends on`, or `theme: goal` on its own row — and carries no timebox. `slice-rules.md`
  *The spike test*. *Validator: the dependent, and a non-spike leaving `Audience` unfilled. Reading: a
  spike that fills `Audience`, and the timebox.*
- **R-020** — Every slice has one vertical outcome and one learning target, both singular, and every
  material claim in `Learning target` has an observation in `Verification` stated so that delivery can
  refute it. Checking that data exists does not demonstrate its quality, latency or cost.
  `slice-rules.md` *What makes a slice*, *Verification maps to the learning target*.
- **R-021** — Every `kind: enabler` is a stepping stone — a row that makes later rows cost less — and
  passes the enabler tests: a real end-to-end production path, the executable evidence the row
  depending on it needs, and no speculative foundation beyond that. Horizontal setup wearing the label
  is enabler camouflage. `slice-rules.md` *The columns* → `kind`.
- **R-022** — A row whose decision the sources leave open reads `needs-decision`, and its `Includes`
  and `Verification` defer to the pending decision rather than picking a side. Publishing one side
  unconditionally is silent contradiction. `slice-rules.md` *The columns* → `readiness`.
- **R-023** — No row is one of the named failures: layer slices, infrastructure by accumulation, fake
  verticality, atomization, deferred safety, horizon dumping. `slice-rules.md` *Named failures*.
- **R-024** — Every in-scope behaviour and every producer feeding a shared pipeline or adapter has one
  owning row or an explicit exclusion; a split distributes the original outcome and introduces none, a
  merge yields one outcome and one learning target, and the id stays with the learning target through
  either. `slice-rules.md` *Splitting and merging a row*, *Identity*.

## The horizons

- **R-025** — A `LATER` line is what does not serve *this* goal, never what is merely unfinished, and
  it carries no id, no columns and no document. § 4 *Admission*; `slice-rules.md` *Named failures* →
  horizon dumping. *Validator: ids in the horizon sections.*
- **R-026** — Every `OUT-OF-SCOPE` entry is written as the licence it gives — because this stays
  unsolved, the implementation may do without X, and this is the price — rather than as a line saying
  what will not be done. `drawing-the-map.md` *What the map reports about its input*.

## Re-truing an existing map

- **R-027** — Close-out ran first, before anything else was decided: the row left the register, its
  document moved to `archive/` unchanged, and `ADRs` was filled only for a decision that cleared the
  bar — hard to reverse, surprising without context, the result of a real trade-off. § 4,
  *Close-out first*.
- **R-028** — Absorption produced a state change or nothing. A line of `Assumptions` or
  `Open questions` that delivery answered **died** rather than being annotated; a row whose size,
  readiness, dependency or shape the evidence changed was changed. Three noes wrote nothing, and on a
  spike three noes were reported as a finding about the spike. § 4, *Then absorb the evidence*,
  *Three noes write nothing*.
- **R-029** — Retirement spent the id and **deleted** the document; nothing undelivered reached
  `archive/`. § 4, *Retirement*.
- **R-030** — The cap was checked whenever a row was added, and an addition that would overflow it
  forced a merge or a deferral instead of a longer list. Below the floor and past the cap are findings
  put to the author, not defects silenced. § 4 *Admission*; `drawing-the-map.md` *The cap is a finding,
  not a budget*. *Validator: both bounds, as warnings.*

## Closing the session, and handing over

- **R-031** — The coverage question was re-asked — does what is left in `NOW` still reach the goal — on
  both branches and whatever the input was. § 5
- **R-032** — Writing followed what stood at the start of the session. With no `.roadmap/`, the map was
  written straight away and no confirmation was asked for. With a map already standing, one block was
  proposed with every operation the session found, one confirmation was asked, and nothing was written
  before it came. Not files written one at a time with a question between each, on either branch. § 5
- **R-033** — The validator was run after writing, every `ERROR` fixed, every `WARNING` put to the
  author rather than silenced. § 5, *Run the validator*. *What this reads is that it ran and what it
  did with the `WARNING`s, never where it pointed.*
- **R-034** — Handover happens only for a `ready` row, derives the `triage` label from readiness and
  executor and stores it nowhere, and routes by kind: a slice to the clarifying conversation —
  `/grill-with-docs`, or `/wayfinder` when it is big and foggy — and straight to `/to-spec` only when
  an earlier session already clarified it and left no `needs-decision` and no `needs-info`; a spike to
  `/prototype` or `/wayfinder`, never to `/to-spec`. What the system does not have is said rather than
  invented. § 6
- **R-035** — The session closed on the four-part report and nothing else: the `Themes` table, the
  `NOW` register, `Open questions` or a line saying there are none, and the path to `roadmap.md`. No
  retelling of what the documents say, no narration of the operations run; a `WARNING` or an owed
  question comes after the four. § 5
