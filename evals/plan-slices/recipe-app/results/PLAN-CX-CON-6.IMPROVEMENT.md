# Improvement report — cycle CON-6

## Inputs

- **Candidate A:** `CANDIDATE-A.md`
- **Candidate B:** `CANDIDATE-B.md`

## Entries

### 1. Authority-declared conflicts disappear before slice wording is audited

---

**Evidence — candidate A**

- `CANDIDATE-A.md:149-153,351-355` — Observed: manual entry is specified as a shared empty/edit form followed directly by embedding regeneration, while the published questions omit the declared manual-path conflict. Inference: the plan commits to one interpretation without first resolving or carrying that conflict.

**Evidence — candidate B**

- `CANDIDATE-B.md:194-198,330-335` — Observed: manual entry is likewise specified as an empty/edit form followed by embedding regeneration, while the published questions omit the declared manual-path conflict. Inference: the plan commits to one interpretation without first resolving or carrying that conflict.

**Existing rule that failed to prevent the defect**

- **Clause:** `SKILL.md:43-48` § `1 Build the evidence inventory` — «Reconcile the inventory before mapping. Sweep the sources for two separate categories and list each entry with a reference for every side: conflicts: pairs of incompatible statements; undecided choices: a provider, model, service, or adapter named without a source that selects it. A qualifying adjective — `cheap`, `multilingual`, `managed` — is not a choice.»
- **Covering rows:** `R-003`

**Remedy**

- `reformulation`

**Change to the skill**

- **Section:** `1 Build the evidence inventory`
- **Change:** Start reconciliation by copying every conflict declared by the designated authority into the inventory as a separate item, retaining every cited side and naming the decision it affects. Then sweep the sources for additional conflicts and undecided choices. Before cutting slices, account for every copied conflict with a selecting source or an open item, and audit each blocked `Includes` and `Verification` bullet for conditional wording.

**Binary test**

- If a designated authority explicitly names an unresolved conflict, the plan lists it with every blocked `NOW` slice and no `Includes` or `Verification` bullet in those slices asserts either side in non-conditional form.

**Cost**

- none — this makes the existing reconciliation pass mechanical; it removes only premature unconditional wording.

### 2. Open-choice blocker lists are over-inclusive in one plan and under-inclusive in the other

---

**Evidence — candidate A**

- `CANDIDATE-A.md:231-286,354` — Observed: the embedding question claims to block slices 3–12, while slices 9–11 publish consultation, photo, and collaboration outcomes without an embedding-choice dependency. Inference: the ordinal range includes unaffected slices.

**Evidence — candidate B**

- `CANDIDATE-B.md:148-151,194-197,333` — Observed: the embedding question names only slices 3 and 4, while slices 5 and 7 require embedding generation or regeneration. Inference: direct consumers are absent from the blocker list.

**Existing rule that failed to prevent the defect**

- **Clause:** `SKILL.md:50-52` § `1 Build the evidence inventory` — «Do not silently pick a side or reopen a decision that a source declares closed. Expose every material entry either with an `Open questions` item naming the slices it blocks, or with a spike before the first blocked slice.»
- **Covering rows:** `R-002`, `R-003`

**Remedy**

- `reformulation`

**Change to the skill**

- **Section:** `1 Build the evidence inventory`
- **Change:** For every open entry, compute the exact blocked set from each `NOW` slice's `Includes`, `Verification`, and release acceptance: include every direct or transitive consumer whose result cannot be satisfied before the answer, and exclude slices that can complete independently. Publish explicit slice numbers; use a range only when every slice in it is blocked. A prior planned spike does not remove downstream consumers from this publication-time set.

**Binary test**

- Every open entry names exactly the `NOW` slices whose `Includes`, `Verification`, or release acceptance depends on its answer.

**Cost**

- none — imprecise ranges become exact slice sets; no planned behaviour is removed or merged.

### 3. A theme's first validation precedes the slice that completes its stated outcome

---

**Evidence — candidate A**

- `not manifested` — `CANDIDATE-A.md:21,188-210` points the broad URL-import outcome to slice 7, where the missing-structured-data fallback is included and verified.

**Evidence — candidate B**

- `CANDIDATE-B.md:20,142-166,168-188` — Observed: the theme says an URL saves the item without qualification and points to slice 5, but slice 5 treats missing structured data as an error; automatic fallback first appears in slice 6. Inference: slice 5 validates only a narrower mode than the desired outcome states.

**Existing rule that failed to prevent the defect**

- **Clause:** `SKILL.md:87`, `SKILL.md:90` § `2 Map themes, outcomes, and dependencies` — «Give every theme: its first `NOW` product slice that validates the complete desired outcome.»
- **Covering rows:** `R-008`, `R-011`

**Remedy**

- `reformulation`

**Change to the skill**

- **Section:** `2 Map themes, outcomes, and dependencies`
- **Change:** After filling `Themes`, compare every mode, qualifier, and recovery promise in each `Desired outcome` with the referenced slice's `Includes` and `Verification`. If any part first appears later, point `First validation` to that later product slice, or narrow and split the theme only when the independence tests support separate value.

**Binary test**

- Every `Themes.First validation` points to a `NOW` slice whose `Includes` and `Verification` cover every mode and qualifier stated in that theme's `Desired outcome`.

**Cost**

- none — only an inaccurate table pointer or an over-broad theme statement changes.

### 4. A source-defined correction path arrives after the first behaviour that can require it

---

**Evidence — candidate A**

- `not manifested` — `CANDIDATE-A.md:145-162,164-186` delivers edit and correction before the first import slice can save content needing correction.

**Evidence — candidate B**

- `CANDIDATE-B.md:148-166,190-208` — Observed: slice 5 saves extracted content immediately without review, while edit and correction first appear in slice 7 after another slice. Inference: successfully saved imperfect content lacks its declared recovery path when first created.

**Existing rule that failed to prevent the defect**

- **Clause:** `SKILL.md:163-164` § `3 Cut valuable vertical slices` — «Deliver a required correction, retry, or escape path before or with the first behaviour that can create the recoverable state.»
- **Covering rows:** uncovered

**Remedy**

- `reformulation`

**Change to the skill**

- **Section:** `3 Cut valuable vertical slices`
- **Change:** Deliver a source-defined correction, retry, or escape path before or with the first `NOW` behaviour whose successful output can create the state that needs it. A fallback for failed creation does not satisfy recovery for a successfully created state. When the recovery shares a broader later interaction, move only its minimum recovery portion forward.

**Binary test**

- If sources define a correction, retry, or escape path for a state a `NOW` slice can create, that path appears in the same or an earlier `NOW` slice.

**Cost**

- The minimum recovery portion moves into or before its producer; unrelated capabilities remain in their own slice.

### 5. A shared adapter is opened early and reopened after intervening themes

---

**Evidence — candidate A**

- `CANDIDATE-A.md:168-173,188-248,254-263` — Observed: slice 6 opens external photo storage and the cover rule; after slices 7–9, slice 10 opens photo writes and the cover/storage invariants again. Inference: a shared adapter has partial, non-adjacent ownership.

**Evidence — candidate B**

- `not manifested` — `CANDIDATE-B.md:10,142-225` states the single-owner rule and opens photo storage and cover handling once, after the preceding input paths.

**Existing rule that failed to prevent the defect**

- **Clause:** `SKILL.md:284-286` § `4 Assign horizons and order for learning` — «Likewise, a slice that opens a pipeline or adapter shared by several paths follows every `NOW` slice that feeds it, and owns it alone.»
- **Covering rows:** `R-006`, `R-016`

**Remedy**

- `reformulation`

**Change to the skill**

- **Section:** `4 Assign horizons and order for learning`
- **Change:** Before ordering, enumerate every `NOW` producer path for each shared pipeline or adapter. Put one opening owner after all producer slices and make its `Includes` establish the common adapter and invariants together. Permit an earlier owner only for an explicitly admitted controlled-input validation; otherwise no producer-specific slice may open part of the adapter first.

**Binary test**

- A pipeline or adapter shared by several paths is opened in one `NOW` slice that follows every `NOW` slice feeding it, unless its `Verification` uses an admitted controlled input through the production computation.

**Cost**

- Adapter-specific work is removed from earlier producer slices and merged into the single owner; producer outcomes remain separate.

### 6. Identity precedes the differentiator without a hard-dependency exception

---

**Evidence — candidate A**

- `CANDIDATE-A.md:8-12,78-95,97-143` — Observed: identity and private scope are delivered in slice 2, while the differentiator's enabler and product validation are slices 3 and 4; `Ordering criteria` names no identity dependency for that validation.

**Evidence — candidate B**

- `not manifested` — `CANDIDATE-B.md:8-11,98-140,231-250` validates the differentiator in slices 3–4 and places identity in slice 9.

**Existing rule that failed to prevent the defect**

- **Clause:** `SKILL.md:261-268` § `4 Assign horizons and order for learning` — «Respect hard dependencies, then order `NOW` by: 1. minimum delivery path and early human review needs; 2. differentiating value and existential business risk; 3. irreversible, expensive, or architecture-changing uncertainty; 4. real enablers required to test those risks; 5. business frequency and one thin outcome from remaining themes; 6. cohesive variants and deeper workflows in risk order.»
- **Covering rows:** uncovered

**Remedy**

- `reformulation`

**Change to the skill**

- **Section:** `4 Assign horizons and order for learning`
- **Change:** Apply the ordering list as precedence after hard dependencies: after the minimum delivery path, place each differentiator's first validator before non-differentiating identity or access work. If identity is a hard dependency of that validator, state the exception once under `Ordering criteria` and put only the minimum identity path first.

**Binary test**

- If identity precedes a differentiator's first `NOW` validator, `Ordering criteria` names identity as a hard dependency of that validator.

**Cost**

- none — the plan reorders existing slices or records the hard-dependency exception; no behaviour is removed or merged.

### 7. Downstream consumers invoke an earlier shared capability without declaring reuse

---

**Evidence — candidate A**

- `CANDIDATE-A.md:101-105,168-173` — Observed: slice 3 establishes embedding generation and persistence, while slice 6 invokes embedding on save without identifying that invocation as reuse of the earlier capability.

**Evidence — candidate B**

- `CANDIDATE-B.md:102-106,146-151,194-197` — Observed: slice 3 establishes embedding generation and persistence, while slices 5 and 7 invoke generation or regeneration without identifying reuse of that owner.

**Existing rule that failed to prevent the defect**

- **Clause:** none
- **Covering rows:** none

**Remedy**

- `addition`

**Change to the skill**

- **Section:** `3 Cut valuable vertical slices`
- **Change:** When a later `NOW` slice invokes a pipeline or adapter opened by an earlier slice, state in that later slice's `Includes` that it reuses the named earlier capability; do not restate opening or ownership work.

**Binary test**

- A `NOW` slice that reuses a pipeline or adapter opened by an earlier slice declares it as reuse.

**Cost**

- none — each downstream consumer gains one short ownership reference; no behaviour is removed or merged.
