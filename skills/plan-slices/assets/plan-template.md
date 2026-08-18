# [Product or capability] — Delivery plan

- **Sources:** [Designated goals, decisions, plans, and relevant repository state.]
- **Current state:** [Existing foundation and constraints.]

## Ordering criteria

- [Only rules that materially determine slicing, horizons, or order.]

## Themes

A theme is a product promise that can be deferred or cancelled whole, on its own. The order below is
by importance, differentiators first; the build order is the one the `First validation` numbers give.

| Theme | Desired outcome | First validation |
|---|---|---|
| [A. Independently schedulable value area] | [User-useful outcome] | [NOW slice number] |

[Append `*(Developer outcome)*` to the desired outcome only when that outcome is itself for a
developer; it is the only case in which `First validation` may name an `Enabler` slice.]

## Cross-functional concerns

- **Authorization:** [Shared rule.]
- **Validation and errors:** [Shared rule.]
- **Operability:** [Logging, observability, timeout, and failure expectations.]
- **Accessibility and security:** [Shared rule.]
- **Data integrity and recovery:** [Invariants, derived data, and partial-failure recovery.]

[Keep all five. Add a further concern — cost, privacy, compliance, latency, auditability, data
migration — only when a source makes it a constraint that several slices must respect; a concern
one slice owns stays in it.]

## NOW

### 0. [Repository prerequisite] *(Enabler: delivery)*

---

**Includes**

- [Minimum repository and CI scope; no provisioning or deployment.]

**Verification**

- [Executable evidence.]

**Outcome**

- [Developer-useful delivery foundation.]

### 1. [Walking skeleton] *(Enabler: delivery)*

---

**Includes**

- [Minimum real path through CI/CD, provisioning, deploy, and runtime.]
- [Datastore reached at runtime by one non-domain operation; migration runner applied.]

**Verification**

- [Evidence from the representative environment, including the datastore round trip.]

**Outcome**

- [Smallest deployed runtime proving the decided infrastructure is connected and running.]

### 2. [Stable descriptive slice name] *(Theme: [A])*

---

**Includes**

- [Minimum real vertical scope.]

**Verification**

- [Acceptance evidence for the outcome and primary learning.]

**Learning / risk**

- [Optional material learning or risk; omit when unnecessary.]

**Outcome**

- [One valuable behaviour.]

**[Additional annotation]**

- [Optional slice-specific note this plan needs; place after the standard fields.]

[Repeat one numbered H3 section per NOW slice.]

[When NOW targets selected end users, finish with a `*(Release: delivery)*` slice that promotes the
coherent release to its intended environment. Omit it for explicitly developer-only validation.]

## LATER

- **[Candidate capability]**: [NOW evidence that would promote it; why it may become useful.]

[One line per entry. Use `- None identified.` when empty.]

## OUT-OF-SCOPE

- **[Excluded capability]**: [Source-backed rationale.]

[Use `- None identified.` when empty.]

## Decision checkpoints

- **After [slice]:** [Evidence] → [cancel, promote, reorder, split, or change decision.]

## Non-product work

- **[Spike, migration, or operation]:** [Question, evidence, exit criterion, and code treatment.]

[Omit when empty.]

## Open questions

- [Only unresolved issues that block or materially change implementation.]

[Omit when empty.]
