# Review of the improvement reports — cycle CON-6

## Inputs

- **Report A:** `REPORT-A.md` — 4 entries
- **Report B:** `REPORT-B.md` — 7 entries

## Entries present in both reports

### A slice asserts one side of an unresolved conflict about the manual path, and the plan's open entries never list that conflict

- **Entries:** `A#1`, `B#1`
- **In report A:** the manual-entry form is published unconditionally in a slice's `Includes` in both candidates, while the published open entries in both plans list only the provider and model choices; the failing clause is the prohibition on asserting a side while an entry is open, whose precondition («while an entry is open») both candidates satisfied vacuously by never listing the behaviour. The proposed rule removes that precondition and redefines the sweep: two sources describing the same behaviour incompatibly leave it open even when no component is named, so the sweep runs per behaviour the plan will slice rather than per component named; a bullet touching such a behaviour must use conditional wording, and the behaviour must be listed among the open entries with the slices it blocks.
- **In report B:** the same manual-entry form is observed in both candidates alongside published questions that omit the declared manual-path conflict, and the plan is read as committing to one interpretation without carrying the conflict; the failing clause is the reconciliation sweep itself. The proposed rule seeds reconciliation from the designated authority: copy every conflict that authority declares into the inventory as a separate item, retaining every cited side and naming the decision it affects, then sweep the sources for additional conflicts and undecided choices, then account for every copied conflict with a selecting source or an open item and audit each blocked bullet for conditional wording.
- **Shared defect:** a behaviour the sources describe incompatibly is asserted on one side, in non-conditional form, in slice `Includes`, and does not appear among the plan's open entries.
- **Same remedy:** `no` — the two rules bind on different triggers. Report A's rule fires on a property of the sources themselves (two sources describing the same behaviour, path, or invariant incompatibly), and reaches any such behaviour whether or not anything listed it. Report B's rule fires on a conflict named by a designated authority document, and is a procedural ordering of the reconciliation pass (copy first, then sweep, then account). A conflict that no authority document names is inside A's reach and outside B's; a plan can satisfy B's copy-and-account procedure and still assert a side of a conflict the authority never declared.
- **Remedy carried by:** `A` — its test is decidable against the artefacts a delivery plan is generated from: compare the sources for incompatible descriptions of a behaviour, then check the bullets that touch it. Report B's test is conditioned on «a designated authority explicitly names an unresolved conflict», which is decidable only where such a document exists and, where it does, checks the plan against a pre-supplied conflict list rather than against the sources the plan was cut from.
- **Differences:** report A locates the evidence at the exact `Includes` line and the exact open-entries lines of each candidate and quotes them; report B cites line ranges and separates observation from inference explicitly. Report A also states the diagnosis of why the existing clause failed (the vacuous precondition) and anchors the covering row `R-010`; report B anchors `R-003` and reads the failure as the reconciliation pass not being mechanical. Report B's remedy adds an ordering of steps within reconciliation that report A does not address; report A's remedy adds a definition of what leaves a behaviour open that report B does not state.

## Entries present only in report A

### A `Learning / risk` claim states a measure that no `Verification` bullet of the same slice measures

- **Entry:** `A#2`
- **What it raises:** in both candidates a slice's `Learning / risk` names a rate or hit-rate measure while that same slice's `Verification` holds one successful case and a list of handled failure cases, stating neither the measure nor the set of cases it would be measured over. The proposed rule requires that, when a `Learning / risk` claim is a rate, proportion, cost, latency, or quality judgement, a `Verification` bullet of the same slice states that measurement and the set of cases it is measured over, and rules out one success, a failure list, or the existence of the data as that observation.
- **What report B does instead at that point:** report B raises nothing about the relation between `Learning / risk` and `Verification`; none of its seven entries takes `Learning / risk` as its subject, and its `Verification`-related entries concern coverage of a theme's stated modes (`B#3`) and the blocked-set computation (`B#2`) instead.

### A `Decision checkpoints` entry names evidence that the slice it follows does not produce

- **Entry:** `A#3`
- **What it raises:** in both candidates a checkpoint placed after a slice names coverage, quality, cost, or hit-rate evidence that the same slice's `Verification` does not state, so the decision arrives with nothing to decide on. The proposed rule adds a condition to the existing checkpoint clause: a checkpoint may be added only where a `Verification` bullet of the slice it follows produces the evidence the checkpoint names, and an unsupported checkpoint is dropped or moved behind the slice that measures it.
- **What report B does instead at that point:** report B raises nothing about `Decision checkpoints`; the section is not the subject of any of its entries, and its ordering entries (`B#5`, `B#6`) address slice sequence and adapter ownership rather than what the checkpoints between slices can decide on.

### A published spike carries no time box and no decision its answer enables, so nothing can end it

- **Entry:** `A#4`
- **What it raises:** manifested by one candidate only — three `Non-product work` spikes placed before slices, each stating an activity and an exit but no time box, and one stating no decision its answer enables; the other candidate publishes no spike at all. The proposed rule requires that every published spike carry all of time box, question, evidence collected, enabled decision, exit criterion, and treatment of experimental code, on the ground that a spike missing the time box and the enabled decision cannot be ended, cancelled, or judged to have failed.
- **What report B does instead at that point:** report B does not treat spike fields as a defect; its only mention of spikes is a clause inside the blocked-set rule of `B#2` («a prior planned spike does not remove downstream consumers from this publication-time set»), which constrains what a spike's presence licenses in an open entry's blocker list, not what a spike must publish about itself.

## Entries present only in report B

### Open-choice blocker lists are over-inclusive in one plan and under-inclusive in the other

- **Entry:** `B#2`
- **What it raises:** one candidate's embedding question claims an ordinal range of blocked slices that includes slices publishing outcomes with no embedding dependency; the other names only two slices while further slices require embedding generation or regeneration. The proposed rule requires the blocked set to be computed from each `NOW` slice's `Includes`, `Verification`, and release acceptance — every direct or transitive consumer in, every independently completable slice out — published as explicit slice numbers, with a range allowed only when every slice in it is blocked.
- **What report A does instead at that point:** report A requires an open entry to be listed «with the slices it blocks» as part of `A#1`'s rule, but takes the existence of the listing as the object of that rule and says nothing about whether a published blocker set is exact; it raises no defect about the two candidates' existing blocker ranges.

### A theme's first validation precedes the slice that completes its stated outcome

- **Entry:** `B#3`
- **What it raises:** manifested by one candidate only — a theme states an unqualified URL-import outcome and points `First validation` at a slice that treats missing structured data as an error, with the automatic fallback first appearing a slice later. The proposed rule requires comparing every mode, qualifier, and recovery promise in each `Desired outcome` against the referenced slice's `Includes` and `Verification`, and either moving the pointer to the later slice or narrowing and splitting the theme where the independence tests support separate value.
- **What report A does instead at that point:** report A raises nothing about the `Themes` table or `First validation`; its entries stay inside slice fields (`Includes`, `Verification`, `Learning / risk`), `Decision checkpoints`, and `Non-product work`.

### A source-defined correction path arrives after the first behaviour that can require it

- **Entry:** `B#4`
- **What it raises:** manifested by one candidate only — a slice saves extracted content immediately without review while edit and correction first appear two slices later. The proposed rule tightens the existing recovery clause: the path must precede or accompany the first `NOW` behaviour whose *successful* output can create the state needing it, a fallback for failed creation does not satisfy it, and where the recovery sits inside a broader later interaction only its minimum recovery portion moves forward.
- **What report A does instead at that point:** report A raises no ordering defect about recovery or correction paths; it treats the manual edit form only as the site of the unconditional assertion in `A#1`, not as a recovery capability whose position relative to its producer matters.

### A shared adapter is opened early and reopened after intervening themes

- **Entry:** `B#5`
- **What it raises:** manifested by one candidate only — a slice opens external photo storage and the cover rule, and after three intervening slices a later slice opens photo writes and the same cover and storage invariants again. The proposed rule requires enumerating every `NOW` producer path for each shared pipeline or adapter before ordering, placing a single opening owner after all producer slices with its `Includes` establishing adapter and invariants together, and permitting an earlier owner only for an explicitly admitted controlled-input validation.
- **What report A does instead at that point:** report A raises nothing about shared adapter ownership or the ordering of a slice that opens a shared pipeline relative to the slices feeding it.

### Identity precedes the differentiator without a hard-dependency exception

- **Entry:** `B#6`
- **What it raises:** manifested by one candidate only — identity and private scope are delivered before the differentiator's enabler and product validation, and `Ordering criteria` names no identity dependency for that validation. The proposed rule reads the ordering list as precedence after hard dependencies: each differentiator's first validator goes before non-differentiating identity or access work, and where identity is a genuine hard dependency the exception is stated once under `Ordering criteria` with only the minimum identity path brought forward.
- **What report A does instead at that point:** report A raises no defect about the `NOW` ordering rationale or `Ordering criteria`; its one ordering-section entry (`A#4`) concerns the fields a published spike must carry, not the sequence of product slices.

### Downstream consumers invoke an earlier shared capability without declaring reuse

- **Entry:** `B#7`
- **What it raises:** in both candidates a slice establishes embedding generation and persistence and later slices invoke generation or regeneration without identifying the invocation as reuse of that earlier owner. It is the report's only `addition` — no existing clause is named as having failed — and it proposes that a later `NOW` slice invoking a pipeline or adapter opened earlier state in its `Includes` that it reuses the named earlier capability, without restating opening or ownership work.
- **What report A does instead at that point:** report A proposes no addition to the skill at all; all four of its remedies are reformulations of existing clauses, and it raises nothing about how a later slice refers to a capability an earlier slice owns.

## Contradictory entries

None identified.

## Out of scope

None identified.

## Summary

- **Shared:** 1 — of which same remedy: 0
- **Only in report A:** 3
- **Only in report B:** 6
- **Contradictory:** 0
- **Out of scope:** 0
