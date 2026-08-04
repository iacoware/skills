# Recipe app — Local correction fixture

- **Sources:** Recipe-app goals and concepts.
- **Current state:** The runtime and scoped recipe persistence already exist.

## Ordering criteria

- Validate semantic retrieval with the production embedding path.

## Themes

| Theme | Desired outcome | First validation |
|---|---|---|
| Semantic retrieval | A tester finds cross-language recipes in one cookbook. | 1 |

## Cross-functional concerns

- **Authorization:** Every query is scoped by the current cookbook resolver.
- **Validation and errors:** Provider errors are typed.
- **Operability:** Capture query latency.
- **Accessibility and security:** Diagnostic access is non-public.
- **Data integrity and recovery:** Embeddings regenerate after edits.

## NOW

### 1. Semantic retrieval *(Theme: Semantic retrieval)*

---

**Includes**

- Embed recipe fixtures and query them through pgvector.

**Verification**

- A relevant English fixture exists after an Italian query.

**Learning / risk**

- Retrieval quality determines model viability.

**Outcome**

- A tester exercises cross-language retrieval.

## LATER

- None identified.

## OUT-OF-SCOPE

- **Structured filters** — Deferred by MVP sources.

