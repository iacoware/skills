# Strong fixture — Delivery plan

## Ordering criteria

- Prove delivery, semantic search, safe acquisition, then release.

## Themes

| Theme | Desired outcome | First validation |
|---|---|---|
| Search | Users find cross-language recipes by meaning. | Semantic search |
| Acquisition | Members add recipes from a URL with automatic recovery. | URL import |

## Cross-functional concerns

- One scope resolver filters all persisted reads and writes; untrusted data is decoded.
- External calls use timeout, retry, SSRF protection, structured logs, and spend limits.

## NOW

### 0. Repository and CI *(Enabler: delivery)*

---

**Includes**

- Build, lint, typecheck, and tests in CI.

**Verification**

- CI passes; an intentional type error and failed test make it fail.

**Outcome**

- Developers get trustworthy change feedback.

### 1. Walking skeleton *(Enabler: delivery)*

---

**Includes**

- Deploy, real database driver, and non-domain migration runner.

**Verification**

- A diagnostic query succeeds after deploy and wake; no domain CRUD, auth, or tenancy exists.

**Outcome**

- Developers verify the decided runtime path.

### 2. Semantic indexing pipeline *(Enabler: search)*

---

**Includes**

- Validated multilingual fixtures traverse real embedding, persistence, and ranking.

**Verification**

- Top-k quality, latency, cost, and scope isolation are observed without precomputed vectors.

**Outcome**

- Developers can decide whether retrieval is viable.

### 3. Semantic search *(Theme: Search)*

---

**Includes**

- Browser search across languages within the current scope and without LLM calls.

**Verification**

- Paraphrases retrieve relevant foreign-language fixtures and never another scope.

**Outcome**

- Test users find recipes by meaning.

### 4. URL import with recovery *(Theme: Acquisition)*

---

**Includes**

- JSON-LD import, automatic validated LLM fallback, then pasted-text escape.

**Verification**

- Invalid output, timeout, SSRF target, and failed parsing create no partial recipe.

**Outcome**

- Members capture recipes even when the source page does not cooperate.

### 5. Pilot release *(Release: delivery)*

---

**Includes**

- Production release, restored backup proof, spend caps, and alarms.

**Verification**

- Selected users complete search and acquisition within the measured budget.

**Outcome**

- Selected users can safely use the coherent release.

## LATER

- Structured filters — promote when semantic-only retrieval misses repeated real queries.

## OUT-OF-SCOPE

- Shopping lists — excluded because structured ingredients are not in scope.

## Open questions

- Query embedding conflict blocks slices 2–3; provider and model choices block slices 1–4.
