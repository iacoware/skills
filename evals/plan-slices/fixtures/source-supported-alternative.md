# Accepted alternative fixture — Delivery plan

## Ordering criteria

- Prove the existential search risk before capture; keep each recovery chain cohesive.

## Themes

| Theme | Desired outcome | First validation |
|---|---|---|
| Discovery and cooking | Users find and open a relevant cross-language recipe in one interaction. | Search and open |
| Capture | Members capture structured or unstructured web recipes. | Cohesive URL capture |

## Cross-functional concerns

- A single resolver owns current scope; Schema decodes untrusted input; external calls use timeout,
  retry, SSRF protection, cover integrity, and `(optional)` field labels.

## NOW

### 0. Repository and CI *(Enabler: delivery)*

---

**Includes**

- Build, lint, typecheck, and tests.

**Verification**

- Intentional type and test failures fail CI.

**Outcome**

- Developers receive reliable feedback.

### 1. Deployed runtime and datastore *(Enabler: delivery)*

---

**Includes**

- Runtime deploy, real datastore query, and non-domain migration.

**Verification**

- Deploy and wake both reconnect; domain CRUD, identity, and tenancy remain absent.

**Outcome**

- Developers validate delivery and persistence mechanics.

### 2. Search engine proof *(Enabler: discovery)*

---

**Includes**

- Real multilingual embedding, persistence, scoped retrieval, and diagnostic ranking.

**Verification**

- Quality, latency, and cost are measured on representative controlled inputs.

**Outcome**

- Developers decide whether discovery is viable.

### 3. Search and open *(Theme: Discovery and cooking)*

---

**Includes**

- One browser interaction searches by meaning and opens the matching recipe detail.

**Verification**

- Cross-language paraphrases resolve to readable ingredients and preparation within scope, without LLM calls.

**Outcome**

- Test users find and cook a relevant recipe.

### 4. Cohesive URL capture *(Theme: Capture)*

---

**Includes**

- JSON-LD first, automatic LLM recovery second, and pasted text from a paywall as manual escape.

**Verification**

- Invalid output, timeout, or unsafe URL creates no partial record and names the failed step.

**Outcome**

- Members capture recipes through one resilient interaction.

### 5. Selected-user release *(Release: delivery)*

---

**Includes**

- Production delivery, backup restore, spend cap, and external-adapter alarms.

**Verification**

- Selected users complete discovery and capture within budget; first access is idempotent and an
  expired or revoked invitation grants no membership.

**Outcome**

- Selected users receive a coherent safe release.

## LATER

- Split discovery and cooking only if usage evidence shows independent scheduling value.

## OUT-OF-SCOPE

- Structured ingredients, shopping list, portion scaling, mandatory review, and deduplication — excluded by sources.
- Granular roles and email/password or magic link — excluded by sources.
- Dedicated vector DB and IaC/Terraform/SST — excluded by sources.

## Open questions

- Query embedding conflict blocks slices 2–3; Neon or Supabase provider Postgres blocks slice 1;
  embedding model and LLM model selections block slices 2–4.
