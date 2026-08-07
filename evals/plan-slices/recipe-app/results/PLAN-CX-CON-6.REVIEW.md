# Review of the improvement reports — cycle CON-6

## Inputs

- **Report A:** `REPORT-A.md` — 4 entries
- **Report B:** `REPORT-B.md` — 7 entries

## Entries present in both reports

### An omitted manual-entry conflict permits unconditional slice wording

- **Entries:** `A#1`, `B#1`
- **In report A:** The reconciliation sweep misses a behavior-level source conflict because it is framed too narrowly, so both plans assert one manual-entry path and omit the behavior from their open entries.
- **In report B:** Both plans fail to carry an authority-declared manual-entry conflict into the inventory, then assert one interpretation without resolving or exposing it.
- **Shared defect:** A known conflict about the manual-entry behavior is absent from the plan's open inventory, allowing blocked slice wording to choose a side unconditionally.
- **Same remedy:** `no` — A requires sweeping every sliced behavior for incompatible source statements; B requires copying every authority-declared conflict into the inventory before an additional sweep.
- **Remedy carried by:** `B` — its declared-conflict-to-inventory rule gives a finite, decidable chain to check in a generated plan: listed conflict, blocked `NOW` slices, and conditional wording.
- **Differences:** A gives the rule broader reach to conflicts discovered by behavior comparison even when no authority declares them. B makes authority-declared conflicts mandatory seed items, retains every cited side, and names the affected decision before auditing blocked bullets. The remedies are compatible, but not normatively identical.

## Entries present only in report A

### Learning or risk measures lack matching verification observations

- **Entry:** `A#2`
- **What it raises:** Both plans claim rates, duration, reliability, or cost-relevant quality under `Learning / risk` without a same-slice `Verification` bullet that measures the claim over a stated case set.
- **What report B does instead at that point:** It does not raise learning-to-verification measurement linkage; its URL-import entries instead address the theme's first-validation pointer and the timing of the correction path.

### Decision checkpoints name evidence their preceding slices do not produce

- **Entry:** `A#3`
- **What it raises:** Each plan has a checkpoint that depends on coverage, cost, or hit-rate evidence absent from the preceding slice's `Verification` bullets.
- **What report B does instead at that point:** It does not assess checkpoint evidence production; its evidence-inventory entries address conflict carry-forward and exact open-choice blocker sets.

### Published spikes omit required termination and decision fields

- **Entry:** `A#4`
- **What it raises:** Report A's cited plan publishes spikes without time boxes, and one lacks the decision enabled by its answer, leaving no complete stopping rule.
- **What report B does instead at that point:** It contains no spike-field entry; its ordering entries concern shared-adapter ownership and identity precedence.

## Entries present only in report B

### Open-choice blocker sets are not exact

- **Entry:** `B#2`
- **What it raises:** One plan overstates an embedding choice's blocked range while the other omits direct downstream consumers, motivating exact blocked-set publication.
- **What report A does instead at that point:** It does not assess blocker-set precision; its inventory entry addresses a missing behavioral conflict and unconditional wording.

### A theme points first validation to a slice that delivers only part of its outcome

- **Entry:** `B#3`
- **What it raises:** One plan's URL-import theme points to structured-data-only validation although the stated outcome also requires a fallback delivered later.
- **What report A does instead at that point:** It does not assess theme-to-first-validation completeness; its URL-import entries address unmeasured learning claims and unsupported checkpoint evidence.

### A required correction path follows the first successful output that may need it

- **Entry:** `B#4`
- **What it raises:** One plan can save imperfect imported content before delivering the source-defined edit and correction path.
- **What report A does instead at that point:** It does not raise correction-path ordering; its related import entry concerns whether claimed measures appear in verification.

### A shared adapter is opened in separate non-adjacent slices

- **Entry:** `B#5`
- **What it raises:** One plan opens photo storage and its invariants early, then reopens photo writes after intervening themes instead of assigning one owner after all producer paths.
- **What report A does instead at that point:** It does not assess shared-adapter ownership or non-adjacent reopening; its ordering-related entry concerns incomplete spike fields.

### Identity precedes differentiating value without a stated hard dependency

- **Entry:** `B#6`
- **What it raises:** One plan schedules identity before the differentiator's enabler and validator without documenting identity as their hard dependency.
- **What report A does instead at that point:** It does not assess identity-versus-differentiator ordering; its ordering entry is limited to spike termination and enabled-decision fields.

### Downstream consumers do not declare reuse of an earlier shared capability

- **Entry:** `B#7`
- **What it raises:** Both plans invoke an embedding capability in later slices without explicitly declaring reuse of the earlier slice that opened it.
- **What report A does instead at that point:** It does not raise downstream reuse declarations; its embedding-related entries concern blocker wording, learning measurement, checkpoint evidence, and spike completeness.

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
