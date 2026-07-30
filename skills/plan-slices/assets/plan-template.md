# [Product or capability] — Delivery plan

- **Sources:** [Designated goals, decisions, plans, and relevant repository state.]
- **Current state:** [Existing foundation and constraints.]

## Ordering criteria

- [Only rules that materially determine slicing, horizons, or order.]

## Themes

| Theme | Desired outcome | First validation |
|---|---|---|
| [A. Independently schedulable value area] | [User-useful outcome] | [NOW slice name] |

## Cross-functional concerns

- **Authorization:** [Shared rule.]
- **Validation and errors:** [Shared rule.]
- **Operability:** [Logging, observability, timeout, and failure expectations.]
- **Accessibility and security:** [Shared rule.]

## NOW

### 0. [Repository prerequisite] *(Enabler: delivery)*

**Outcome**

- [Developer-useful delivery foundation.]

**Includes**

- [Minimum repository and CI scope; no provisioning or deployment.]

**Verification**

- [Executable evidence.]

### 1. [Walking skeleton] *(Enabler: delivery)*

**Outcome**

- [Smallest deployed runtime useful to developers testing delivery.]

**Includes**

- [Minimum real path through CI/CD, provisioning, deploy, and runtime.]

**Verification**

- [Evidence from the representative environment.]

### 2. [Stable descriptive slice name] *(Theme: [A])*

**Outcome**

- [One user-useful behaviour.]

**Why now**

- [Optional soft dependency or priority preference; omit when unnecessary.]

**Includes**

- [Minimum real vertical scope.]

**Verification**

- [Acceptance evidence for the outcome and primary learning.]

**Learning / risk**

- [Optional material learning or risk; omit when unnecessary.]

[Repeat one numbered H3 section per NOW slice.]

## LATER

- **[Candidate capability]**
  - **Promotion trigger:** [NOW evidence that would justify implementation.]
  - **Expected value:** [Why it may become useful.]

[Use `- None identified.` when empty.]

## OUT-OF-SCOPE

- **[Excluded capability]** — [Source-backed rationale.]

[Use `- None identified.` when empty.]

## Hard dependencies

```text
[Prerequisite]
└── [Slice name]
    ├── [Slice name]
    └── [Slice name]
```

## Sequencing notes

- **[Soft dependency | Priority preference]:** [A before B] — [terse reason.]

## Decision checkpoints

- **After [slice]:** [Evidence] → [cancel, promote, reorder, split, or change decision.]

## Non-product work

- **[Spike, migration, or operation]:** [Question, evidence, exit criterion, and code treatment.]

[Omit when empty.]

## Open questions

- [Only unresolved issues that block or materially change implementation.]

[Omit when empty.]
