# Recipe app — Pre-decided conflict fixture

- **Sources:** Recipe-app goals, concepts, and evaluation brief.
- **Current state:** Greenfield; the manual path is resolved to use the shared edit form and skip extraction.

## Ordering criteria

- Keep the resolved manual path conditional on the documented decision; validate extraction separately.

## Themes

| Theme | Desired outcome | First validation |
|---|---|---|
| Manual capture | A member saves known recipes without extraction. | 1 |

## Cross-functional concerns

- **Authorization:** Cookbook membership scopes writes.
- **Validation and errors:** Manual fields use the edit schema.
- **Operability:** Record save failures.
- **Accessibility and security:** The form is keyboard and screen-reader accessible.
- **Data integrity and recovery:** Saving and editing regenerate derived embeddings.

## NOW

### 1. Manual recipe form *(Theme: Manual capture)*

---

**Includes**

- Use the shared edit form with empty fields and bypass the extraction adapter per the recorded resolution.

**Verification**

- A member saves and edits free-text ingredients and preparation without an extraction call.

**Outcome**

- Members record recipes they already know with minimal friction.

## LATER

- None identified.

## OUT-OF-SCOPE

- **Ingredient parsing** — Explicitly excluded by the source model.

