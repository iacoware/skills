# Calibration mutation: hard dependency violation

Use `strong-reference-aligned.md`, but place browser semantic search before the real indexing and
embedding path it must exercise. Verify search with precomputed vectors that bypass production
transformation.

## Ordering criteria

- Deliver browser search before validating the production indexing dependency.

## Themes

| Theme | Desired outcome | First validation |
|---|---|---|
| Search | Users find cross-language recipes by meaning. | Browser semantic search |

## Cross-functional concerns

- Preserve every unmentioned concern and slice from the classified reference.

## NOW

### 1. Browser semantic search *(Theme: Search)*

---

**Includes**

- Browser search backed by precomputed vectors that bypass production transformation.

**Verification**

- Controlled precomputed vectors return expected fixtures.

**Outcome**

- Users appear able to search by meaning.

### 2. Production indexing path *(Enabler: Search)*

---

**Includes**

- Real embedding, transformation, persistence, and ranking after browser search.

**Verification**

- Production inputs traverse the real indexing path.

**Outcome**

- Developers finally learn whether the delivered search path is viable.

## LATER

- Preserve the classified reference horizon.

## OUT-OF-SCOPE

- Preserve the classified reference exclusions.
