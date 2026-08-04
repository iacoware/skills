# Calibration mutation: missing safe scope boundary

Use `strong-reference-aligned.md`, persist indexed recipes before any scope resolver exists, omit
scope filters from search, and defer ownership isolation to a later identity slice.

## Ordering criteria

- Persist and search recipes before introducing ownership isolation.

## Themes

| Theme | Desired outcome | First validation |
|---|---|---|
| Search | Users find any indexed recipe by meaning. | Unscoped semantic search |
| Identity | Owners isolate their recipes. | Deferred ownership isolation |

## Cross-functional concerns

- Preserve every unmentioned concern from the classified reference, except the scope resolver.

## NOW

### 1. Persist indexed recipes *(Enabler: Search)*

---

**Includes**

- Persist indexed recipes before a scope resolver or ownership model exists.

**Verification**

- Indexed recipes survive a restart.

**Outcome**

- Search data is available without ownership isolation.

### 2. Unscoped semantic search *(Theme: Search)*

---

**Includes**

- Search persisted recipes without scope filters.

**Verification**

- Queries return relevant recipes regardless of owner.

**Outcome**

- Users search the shared index.

## LATER

- Add identity, ownership isolation, and the shared scope resolver.

## OUT-OF-SCOPE

- Preserve the classified reference exclusions.
