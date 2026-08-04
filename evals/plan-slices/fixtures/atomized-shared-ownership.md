# Calibration mutation: atomized shared ownership

Use `strong-reference-aligned.md`, but split remote photo ingestion from manual photo upload. Let
both slices establish the same storage adapter and single-cover invariant, and place collaboration
between them.

## Ordering criteria

- Preserve the classified reference order except for the deliberately separated photo slices.

## Themes

| Theme | Desired outcome | First validation |
|---|---|---|
| Photos | Members obtain a valid recipe cover from remote or manual input. | Remote photo ingestion |
| Collaboration | Members share recipes. | Collaboration |

## Cross-functional concerns

- Preserve every unmentioned concern and slice from the classified reference.

## NOW

### 1. Remote photo ingestion *(Theme: Photos)*

---

**Includes**

- Establish the photo storage adapter and the single-cover invariant for remote images.

**Verification**

- A remote image becomes the only cover through the new adapter.

**Outcome**

- Members obtain covers from remote pages.

### 2. Collaboration *(Theme: Collaboration)*

---

**Includes**

- Preserve the classified reference collaboration behavior.

**Verification**

- Invited members can access shared recipes within scope.

**Outcome**

- Members collaborate on recipes.

### 3. Manual photo upload *(Theme: Photos)*

---

**Includes**

- Re-establish the same photo storage adapter and single-cover invariant for uploads.

**Verification**

- An upload replaces the cover through independently established adapter logic.

**Outcome**

- Members manually replace recipe covers.

## LATER

- Preserve the classified reference horizon.

## OUT-OF-SCOPE

- Preserve the classified reference exclusions.
