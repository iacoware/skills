# Calibration mutation: silent contradiction

Use `strong-reference-aligned.md`, remove its query-embedding open question, and assert runtime query
embedding unconditionally although product sources disagree. Leave the dependent search slices
unblocked.

## Ordering criteria

- Treat runtime query embedding as decided and leave dependent search work unblocked.

## Themes

| Theme | Desired outcome | First validation |
|---|---|---|
| Search | Users find cross-language recipes by meaning. | Runtime query embedding |

## Cross-functional concerns

- Preserve every unmentioned concern and slice from the classified reference.

## NOW

### 1. Runtime query embedding *(Enabler: Search)*

---

**Includes**

- Unconditionally embed every query at runtime despite the conflicting product sources.

**Verification**

- Runtime query embeddings retrieve foreign-language fixtures.

**Outcome**

- Search slices proceed without a blocking decision.

### 2. Semantic search *(Theme: Search)*

---

**Includes**

- Preserve the classified reference semantic-search behavior.

**Verification**

- Cross-language paraphrases retrieve relevant recipes.

**Outcome**

- Users search by meaning.

## LATER

- Preserve the classified reference horizon.

## OUT-OF-SCOPE

- Preserve the classified reference exclusions.
