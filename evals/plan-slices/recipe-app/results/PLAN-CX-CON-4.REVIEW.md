# Review of `PLAN-CX-CON-4.IMPROVEMENT.md`

## Inputs

- **Reviewed report:** `PLAN-CX-CON-4.IMPROVEMENT.md`
- **Compared with:** `PLAN-CC-CON-4.IMPROVEMENT.md`

## Improvements also present in the other report

### Explicit handling of source contradictions

- **In this report:** Require a systematic search for incompatible claims and turn each unresolved conflict into a question or spike before affected slices.
- **In the other report:** Require a cited conflict sweep, prohibit silently asserting either side, and make affected slices conditional on a question or time-boxed spike.
- **Common improvement:** Prevent plans from silently choosing between incompatible source statements.
- **Differences:** The other report specifies citations, conditional wording, blocked-slice references, and completion checks; this report proposes broader automated checks for ignored questions.

### Explicit handling of undecided choices

- **In this report:** Detect decisions that remain placeholders rather than treating them as settled.
- **In the other report:** Track undecided providers, models, and external dependencies separately from source contradictions, with either a selecting source or an open question naming the blocked slice.
- **Common improvement:** Expose decisions that sources have not made before dependent work is planned.
- **Differences:** The other report defines a separate category and a concrete completeness rule for external dependencies; this report includes them in a broader reconciliation sweep.

### Split capabilities and enablers with independent risks

- **In this report:** Require split/merge audits based on whether capabilities can be deferred independently.
- **In the other report:** Split an enabler when independent failure causes would change different decisions, limiting each enabler to one material uncertainty.
- **Common improvement:** Separate work whose capabilities, risks, or decisions can vary independently.
- **Differences:** This report applies a general scheduling-independence test; the other report adds an enabler-specific causal-attribution test and a minimal domain precursor.

### Keep a theme and its recovery path contiguous

- **In this report:** Keep enablers close to validators and prevent a theme from reopening after independent themes without justification.
- **In the other report:** Deliver a required remedy for a recoverable failure before opening another theme.
- **Common improvement:** Finish a coherent path locally before diverting to independently schedulable work.
- **Differences:** This report states a general adjacency rule and proposes detecting interrupted themes; the other report gives required recovery explicit precedence over breadth-first ordering.

### Open shared pipelines and adapters once, after their producers

- **In this report:** Use ownership mapping, an out-of-slice ledger, and semantic checks to prevent premature or duplicated adapters.
- **In the other report:** Open a shared pipeline only after all `NOW` producer paths and assign it one owner, covering every producer-to-pipeline combination.
- **Common improvement:** Prevent shared infrastructure from being introduced early, duplicated, or left without an owner.
- **Differences:** This report proposes cross-cutting internal controls; the other report defines precise ordering and path-coverage rules.

### Trace scope and horizon ownership

- **In this report:** Map each behavior to its theme, horizon, and owning slice, and keep `LATER` behavior out of `NOW`.
- **In the other report:** Require every `NOW` slice to cite a source that requests it; merely fitting the data model is insufficient.
- **Common improvement:** Prevent speculative capability and scope leakage into `NOW`.
- **Differences:** This report emphasizes an internal matrix and ledger; the other report requires positive source traceability for each `NOW` slice.

### Use repeatable, decision-changing verification

- **In this report:** Center plans on outcomes, risks, boundaries, and evidence capable of changing a decision, including checks that each theme has a first validation.
- **In the other report:** Require versioned evaluation sets with positive and negative cases for quality, relevance, or accuracy claims.
- **Common improvement:** Verify the material risk rather than merely proving that data or a path exists.
- **Differences:** This report states the general evidence criterion and proposes semantic enforcement; the other report makes quality evidence repeatable through a specific evaluation artifact.

## Improvements unique to this report

### Distinguish technical enablement from product validation

- **Improvement:** Record separately the first technical enabler and the first product validation for every theme, and detect missing first validations.
- **Difference from the other report:** The other report improves enabler sizing and ordering but does not require this conceptual distinction for each theme.

### Reduce published implementation detail

- **Improvement:** Favor outcomes, risks, boundaries, and decision-relevant evidence over implementation detail in the published plan.
- **Difference from the other report:** The other report strengthens verification and structure without proposing a general reduction in published implementation detail.

## Improvements present only in the other report

### Bound identity deferral and declare pre-identity audiences

- **Other report:** Deliver identity before the second end-user product slice unless justified, and declare a compatible audience and environment inside every earlier slice.
- **Missing from this report:** No identity deadline or per-slice audience rule is proposed.

### Cover all source-backed operational constraints in the release slice

- **Other report:** Trace every declared operational constraint into release readiness, including durability, restore testing, spending limits, and alerts where applicable.
- **Missing from this report:** No release-completeness rule for operational constraints is proposed.

### Separate and classify `LATER` and `OUT-OF-SCOPE` items

- **Other report:** Use one item per horizon bullet and classify trigger-dependent work as `LATER` while reserving `OUT-OF-SCOPE` for source-backed exclusions.
- **Missing from this report:** It prevents `LATER` leakage into `NOW` but does not define this horizon boundary or bullet granularity.

### Verify repeat, idempotency, and residue failure modes

- **Other report:** Test repeated operations, idempotency, and leftover artifacts for external writes and membership creation.
- **Missing from this report:** Its general evidence guidance does not name these failure modes.

## Contradictory improvements

- None identified.

## Summary

- **Shared:** `7`
- **Unique to this report:** `2`
- **Only in the other report:** `4`
- **Contradictions:** `0`
