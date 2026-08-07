# Recidiva — cycle CON-6

## Inputs

- **Report A:** `REPORT-A.md` — 4 entries
- **Report B:** `REPORT-B.md` — 7 entries
- **Rows considered:** 17

## Pairs

### `A#1` → `R-010`

- **Entry:** A slice's `Includes` asserts, in non-conditional form, one side of the manual-entry behaviour that the brief declares the sources describe incompatibly, and the plan does not carry that behaviour among its open entries.
- **Row claim:** No `Includes` or `Verification` bullet asserts in non-conditional form one side of an unresolved choice. Unresolved covers a conflict between the sources — those listed under `Known conflicts` in the brief, plus those demonstrable by citing two sources in disagreement — and, in the slices that choice blocks, any other choice the plan does not resolve by citing a selecting source. Declaring the choice under `Open questions` or assigning it a spike does not resolve it.
- **Why the defect falsifies the claim:** The claim covers exactly a conflict the brief lists under `Known conflicts`, and states that no `Includes` bullet may assert one of its sides unconditionally. The entry publishes an `Includes` bullet that does assert one side of that declared conflict with no wording deferring to a pending decision, and the claim's own escape — declaring it open — is absent, so the bullet cannot be read as covered by the resolution the claim allows.
- **Other rows considered:** `R-003` — its subject is an external choice of provider, model, service, or adapter; the manual-entry conflict names no such component, so that claim can hold on this plan while this defect occurs. | `R-002` — it governs choices the plan does declare open; here the behaviour is never declared open at all, so nothing it asserts about blocked-slice naming is contradicted.

### `B#1` → `R-010`

- **Entry:** The manual-entry conflict declared by the authority is absent from the published questions, and both plans' slice wording commits unconditionally to one interpretation of it.
- **Row claim:** No `Includes` or `Verification` bullet asserts in non-conditional form one side of an unresolved choice. Unresolved covers a conflict between the sources — those listed under `Known conflicts` in the brief, plus those demonstrable by citing two sources in disagreement — and, in the slices that choice blocks, any other choice the plan does not resolve by citing a selecting source. Declaring the choice under `Open questions` or assigning it a spike does not resolve it.
- **Why the defect falsifies the claim:** The defect is slice wording that specifies one interpretation of a conflict the authority declares unresolved, with no selecting source cited. That is precisely the state the claim predicts away: an unresolved conflict whose side an `Includes` bullet asserts in non-conditional form.
- **Other rows considered:** `R-002` — the omission is of a conflict the plan never declares open, so the claim about declared-open entries naming their blocked slices is untouched. | `R-003` — restricted to external component choices; the entry's conflict is about a path's behaviour, so both can hold together.

### `B#2` → `R-002`

- **Entry:** An open entry's blocked-slice list omits slices whose `Includes` require the pending answer, and in the other plan spans slices that do not depend on it.
- **Row claim:** Every choice the plan declares open names the `NOW` slices it blocks, in whatever section it declares it.
- **Why the defect falsifies the claim:** The choice is declared open and the plan does publish a blocked-slice list, so the claim's antecedent is met; the under-inclusive half of the defect shows `NOW` slices that the open answer blocks and that the declaration does not name, which is the exact state the claim asserts cannot occur.
- **Other rows considered:** `R-003` — a slice left out of the blocked list does depend on an undecided external choice, so the claim is implicated, but the located fault is in what the open declaration names rather than in the slice's dependency, and the claim's other limbs are not what the entry examines.

### `B#3` → `R-008`

- **Entry:** A theme's `First validation` points to a slice that validates only a narrower mode than the theme's `Desired outcome` states, with the missing recovery mode appearing in a later slice.
- **Row claim:** Every theme's `First validation` points to a slice whose `Outcome` covers the theme's entire desired outcome.
- **Why the defect falsifies the claim:** The claim requires the pointed-to slice to cover the whole desired outcome; the entry locates a `First validation` whose slice treats a case the unqualified desired outcome promises as an error, with the promised handling delivered only afterwards, so the covering relation the claim asserts does not hold.
- **Other rows considered:** `R-011` — it constrains what kind of slice the pointer resolves to, an unannotated `NOW` product slice; the pointer here does resolve to a product slice, so that claim holds while this defect occurs.

### `B#5` → `R-006`

- **Entry:** External photo storage and its invariants are opened in one slice and opened again in a later slice, after intervening slices of other themes.
- **Row claim:** A pipeline or adapter shared by several paths is opened in the `Includes` of a single `NOW` slice.
- **Why the defect falsifies the claim:** The adapter is shared by several paths and its opening work is split across the `Includes` of separate `NOW` slices, which is a direct denial of the single-slice ownership the claim asserts.
- **Other rows considered:** `R-016` — it fixes where the opening slice sits relative to the slices feeding it; the defect here is that ownership is split at all, and a split cannot be repaired by placement, so this row is implicated only through the first opener's position rather than through the fault the entry locates. | `R-015` — about declaring reuse of an already-opened adapter; the second slice reopens rather than reuses, so the claim's subject does not arise.

### `B#6` → `R-001`

- **Entry:** Identity and private scope are delivered before the differentiator's first validating slice, and `Ordering criteria` records no identity dependency for that validation.
- **Row claim:** The plan places identity after the differentiator.
- **Why the defect falsifies the claim:** The claim is an ordering prediction about identity and the differentiator; the entry locates identity delivered in an earlier slice than the differentiator's enabler and product validation, which is the ordering the claim says does not come back.
- **Other rows considered:** `R-017` — it applies when identity is deferred behind several user-facing slices and asks for a justification of that deferral; here identity is early, so its antecedent never arises. | `R-009` — it constrains the audience named by slices preceding identity; almost nothing precedes identity in this plan, so it can hold while this defect occurs.

### `B#7` → `R-015`

- **Entry:** Later slices invoke embedding generation or regeneration established by an earlier slice without identifying the invocation as reuse of that owner.
- **Row claim:** A `NOW` slice that reuses a pipeline or adapter opened by an earlier slice declares it as reuse.
- **Why the defect falsifies the claim:** The entry locates `NOW` slices that consume a pipeline an earlier slice opened and whose `Includes` carry no reuse declaration, which is the omission the claim predicts away.
- **Other rows considered:** `R-006` — the pipeline is opened in a single slice here, so its single-owner claim holds; the fault is in the consumers' wording, not in the opening. | `R-016` — concerns the opener's position relative to its feeders, which the entry does not examine.

## Entries with no row

- `A#2` — A slice's `Learning / risk` claims a rate or duration that no `Verification` bullet of the same slice measures, nor states the set of cases it is measured over.
- `A#3` — A `Decision checkpoints` entry names coverage, quality, cost, or hit-rate evidence that the `Verification` of the slice it follows does not produce.
- `A#4` — A published spike states neither a time box nor the decision its answer enables, so nothing can end it or let the plan continue without its answer.
- `B#4` — A source-defined correction path for successfully saved but imperfect content arrives in a later slice than the first `NOW` behaviour that creates that state.
