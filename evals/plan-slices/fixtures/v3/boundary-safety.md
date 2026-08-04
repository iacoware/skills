# Recipe app — Safety boundary fixture

- **Sources:** Recipe-app goals and concepts.
- **Current state:** Greenfield demo.

## Ordering criteria

- Defer identity and ownership until after recipe workflows stabilize.

## Themes

| Theme | Desired outcome | First validation |
|---|---|---|
| Recipe capture | A tester saves and reads recipes. | 1 |

## Cross-functional concerns

- **Authorization:** Authentication and cookbook scoping arrive in a later access slice.
- **Validation and errors:** Validate recipe text.
- **Operability:** Log failures.
- **Accessibility and security:** Non-public environment only.
- **Data integrity and recovery:** Persist recipes in Postgres.

## NOW

### 1. Unscoped recipe storage *(Theme: Recipe capture)*

---

**Includes**

- Persist recipes and list every stored recipe without a cookbook key or resolver.

**Verification**

- Two seeded cookbooks can read the same global recipe list.

**Outcome**

- Testers can create and browse recipes before access work.

## LATER

- **Cookbook membership and query scoping**
  - **Promotion trigger:** The recipe workflow is stable.
  - **Expected value:** Prevent cross-cookbook access.

## OUT-OF-SCOPE

- **Granular roles** — Excluded from MVP.

