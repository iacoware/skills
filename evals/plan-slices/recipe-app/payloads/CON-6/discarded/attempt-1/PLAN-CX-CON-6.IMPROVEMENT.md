# Improvement report — cycle CON-6

## Inputs

- **Candidate A:** `CANDIDATE-A.md`
- **Candidate B:** `CANDIDATE-B.md`

## Entries

### 1. Unresolved-decision exposure omits a known conflict and, in one plan, downstream blocked slices

---

**Evidence — candidate A**

- `CANDIDATE-A.md:351-355` — the exhaustive `Open questions` section lists three unresolved items but omits the brief-listed conflict over the manual-input path; this omission is observed.
- `CANDIDATE-A.md:145-162` — slice 5 publishes the complete manual-input path without a pending-decision condition; that the omitted conflict blocks this slice is inferred from the brief.

**Evidence — candidate B**

- `CANDIDATE-B.md:330-335` — the exhaustive `Open questions` section omits the same brief-listed conflict; it also names only slices 3–4 for the semantic choice and slice 6 for the extraction choice, although later `NOW` slices invoke those capabilities. The omissions and named slice sets are observed; downstream dependence is inferred from the cited slice fields.
- `CANDIDATE-B.md:194-204` — slice 7 invokes semantic indexing after edit, and `CANDIDATE-B.md:276-286` verifies a release using search and link capture, but neither slice is named as blocked by the corresponding open choice.

**Existing rule that failed to prevent the defect**

- **Clause:** `SKILL.md:50-52` — `§ 1 Build the evidence inventory` — «Do not silently pick a side or reopen a decision that a source declares closed. Expose every material entry either with an `Open questions` item naming the slices it blocks, or with a spike before the first blocked slice.»
- **Covering rows:** `R-002`, `R-003`

**Remedy**

- `reformulation`

**Change to the skill**

- **Section:** `§ 1 Build the evidence inventory`
- **Change:** For each material conflict and undecided choice, publish one `Open questions` item or one spike before the first blocked slice. Identify the unresolved entry and enumerate every `NOW` slice whose `Includes` or `Verification` directly invokes, or later reuses, a capability that needs its answer. Before mapping, compare the conflict-and-choice inventory with the published questions, spikes, and slice fields; a category label, range-free phrase such as “subsequent verification,” or only the first blocked slice does not name all blocked slices.

**Binary test**

- Every material conflict or undecided external choice not selected by a citable source, or by the plan among alternatives the brief accepts, appears in an `Open questions` item or a preceding spike that names every `NOW` slice whose `Includes` or `Verification` directly invokes or reuses the unsettled capability.

**Cost**

- none; the existing inventory and exposure pass are merged into one completeness check, with only explicit slice references added to the published plan.

### 2. A theme's first validation points to a slice whose Outcome omits part of the desired outcome

---

**Evidence — candidate A**

- `CANDIDATE-A.md:16-18` — theme A's desired outcome includes access and operating only within the current scope, and its `First validation` points to slice 2.
- `CANDIDATE-A.md:93-95` — slice 2's `Outcome` states only that an authenticated person has a persistent private scope for future content; the omitted operation and exclusivity elements are observed by comparing the two fields.

**Evidence — candidate B**

- `not manifested` — `CANDIDATE-B.md:16-18` points theme A to slice 2, and `CANDIDATE-B.md:94-96` names both seeing and reading content from the configured current scope in that slice's `Outcome`.

**Existing rule that failed to prevent the defect**

- **Clause:** `SKILL.md:95-96` — `§ 2 Map themes, outcomes, and dependencies` — «A slice that validates only one capability inside a broader theme outcome is not that theme's first validator.»
- **Covering rows:** `R-008`

**Remedy**

- `reformulation`

**Change to the skill**

- **Section:** `§ 2 Map themes, outcomes, and dependencies`
- **Change:** Set `Themes.First validation` only when that slice's `Outcome`, without relying on its `Includes` or `Verification`, names every user capability and boundary named by the theme's `Desired outcome`. Otherwise narrow the desired outcome, choose a later validator, or change the slice outcome; evidence elsewhere in the slice does not complete a partial `Outcome`.

**Binary test**

- Every user capability and boundary named in a `Themes.Desired outcome` cell is named in the `Outcome` of the existing `NOW` slice referenced by that row's `First validation` cell.

**Cost**

- none; this makes the existing first-validator comparison field-local and may add only omitted outcome terms.

### 3. A later slice reuses a shared adapter without declaring reuse

---

**Evidence — candidate A**

- `CANDIDATE-A.md:168-178` — slice 6 first copies source photos to the named object-storage adapter and assigns a cover.
- `CANDIDATE-A.md:254-263` — slice 10 later adds and removes photos through the same named adapter but does not state that it reuses the capability established by slice 6. Repetition of the adapter is observed; reuse of the earlier capability is inferred from that repetition.

**Evidence — candidate B**

- `not manifested` — `CANDIDATE-B.md:8-10` declares one owner for the photo and object-storage capability, and `CANDIDATE-B.md:214-225` opens its link-copy, upload, and cover behavior together in that owning slice rather than consuming an earlier opening.

**Existing rule that failed to prevent the defect**

- **Clause:** `SKILL.md:167-168` — `§ 3 Cut valuable vertical slices` — «Co-locate the behaviour, or make the first slice establish a complete stable capability that later slices consume without reopening ownership.»
- **Covering rows:** uncovered

**Remedy**

- `reformulation`

**Change to the skill**

- **Section:** `§ 3 Cut valuable vertical slices`
- **Change:** Co-locate the behavior, or make the first slice establish a complete stable capability. Every later `NOW` slice that consumes the same pipeline or adapter must state in `Includes` that it reuses the established capability; merely repeating the pipeline or adapter name does not distinguish reuse from reopened ownership.

**Binary test**

- A `NOW` slice that reuses a pipeline or adapter opened by an earlier `NOW` slice declares that reuse in its `Includes` field.

**Cost**

- none; later consumers gain one short reuse phrase, while ownership and slice boundaries remain unchanged.
