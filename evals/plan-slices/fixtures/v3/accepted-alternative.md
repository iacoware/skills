# Recipe app — Accepted alternative fixture

- **Sources:** Recipe-app goals and architecture choices.
- **Current state:** Greenfield; Supabase selected for Postgres after a free-tier review.

## Ordering criteria

- Validate the multilingual semantic engine through the cheapest real path.

## Themes

| Theme | Desired outcome | First validation |
|---|---|---|
| Semantic retrieval | A tester retrieves recipes across languages within one cookbook. | 1 |

## Cross-functional concerns

- **Authorization:** A configured cookbook resolver scopes the non-public test.
- **Validation and errors:** Decode provider output and distinguish timeouts.
- **Operability:** Measure latency and cost.
- **Accessibility and security:** Restrict diagnostics to testers.
- **Data integrity and recovery:** Regenerate embeddings from canonical recipe text.

## NOW

### 1. Supabase multilingual retrieval proof *(Theme: Semantic retrieval)*

---

**Includes**

- Use Supabase Postgres with pgvector and a multilingual cloud embedding adapter on normalized fixtures.

**Verification**

- Italian queries rank labeled English recipes within the configured cookbook; record quality, latency, and cost.

**Learning / risk**

- Evidence selects whether Supabase and the embedding adapter satisfy free-tier and quality constraints.

**Outcome**

- A tester validates the differentiator using a source-accepted datastore alternative.

## LATER

- **Structured filters**
  - **Promotion trigger:** Retrieval evidence exposes precision gaps addressable by tags or time.
  - **Expected value:** Improve result narrowing.

## OUT-OF-SCOPE

- **Cross-cookbook search** — Excluded from MVP.

