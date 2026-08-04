# Recipe app — Boundary pass fixture

- **Sources:** Recipe-app goals, concepts, architecture, and stack decisions.
- **Current state:** Greenfield; developer validation in a non-public environment.

## Ordering criteria

- Validate multilingual semantic retrieval before commodity product breadth.

## Themes

| Theme | Desired outcome | First validation |
|---|---|---|
| Semantic retrieval | A tester finds English recipes with an Italian query inside one cookbook. | 2 |

## Cross-functional concerns

- **Authorization:** A configured cookbook resolver scopes every read and write until identity replaces it at one seam.
- **Validation and errors:** Typed invalid inputs and adapter failures remain distinguishable.
- **Operability:** Record latency, provider cost, timeouts, and correlation identifiers.
- **Accessibility and security:** The diagnostic is restricted to the non-public environment.
- **Data integrity and recovery:** Recipe text is canonical; embeddings are regenerated derived data.

## NOW

### 1. Connected runtime *(Enabler: delivery)*

---

**Includes**

- Deploy the runtime, apply a non-domain migration, and execute a Postgres round trip.

**Verification**

- CI and the representative environment prove migration, driver, connection, and runtime health.

**Outcome**

- Developers can deploy and observe the decided infrastructure.

### 2. Cross-language retrieval proof *(Theme: Semantic retrieval)*

---

**Includes**

- Process scoped recipe fixtures through real multilingual embedding, pgvector persistence, and similarity query paths.

**Verification**

- Italian queries rank relevant English recipes in the agreed labeled set; capture recall, latency, and cost.
- Invalid provider output, timeout, and cross-cookbook result leakage fail with distinct observable errors.

**Learning / risk**

- Ranking quality and cost determine whether the selected embedding adapter remains viable.

**Outcome**

- A tester can validate the product differentiator in a non-public environment.

## LATER

- **Structured filters**
  - **Promotion trigger:** Semantic-search evidence shows users need precision unavailable from embeddings.
  - **Expected value:** Narrow results by derived tags and time.

## OUT-OF-SCOPE

- **Cross-cookbook search** — MVP sources restrict search to the current cookbook.

