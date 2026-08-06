# Clause → ledger row map

Which normative clause of `skills/plan-slices/SKILL.md` each row of `REGRESSION-LEDGER.md` is
attached to, and which clauses no row covers. Produced for Fase 1c, first deliverable; consumed by
Fase 1a, where `validate_improvement.py` checks that the covering rows an `IMPROVEMENT` entry
declares coincide with this map. Fase 4 updates it with whatever CON-6 changes.

The map does not touch the ledger. `R-NNN` references are stable across the ledger's translation and
semantic migration, so this file survives them.

**Measured on:** `SKILL.md` at `28b5460`, 417 lines, whole file. Commit attribution from
`git blame` plus the diff of each of the 19 commits that ever touched the file.

## What a clause is here

One entry per **normative sentence**: a sentence that imposes an obligation, a prohibition, or a
conditional permission. Consequences:

- Pure rationale, examples, and headings are not clauses and are not listed. Where a paragraph mixes
  a rule with its justification, the entry covers the rule and the site spans only its sentence.
- A bulleted list counts as **one** entry together with its stem sentence when the bullets supply
  categories, symptoms, or factors of a single rule — the nine evidence categories
  (`SKILL.md:31-39`), the five theme criteria (`65-72`), the five split warnings (`147-151`), the six
  ordering factors (`263-268`), the five spike components (`306-307`).
- A bullet gets its **own** entry when it carries a requirement its stem does not — the four slice
  properties (`138-141`), the five enabler tests (`175-179`), the three horizon bullets (`250-254`),
  the six ledger mappings (`323-328`), the ten publishing rules (`337-352`), the twelve anti-patterns
  (`221-244`).
- **Every member of a `Proceed when` / `Complete when` gate is its own entry.** Gates restate body
  clauses one member at a time, and a row that lands on a gate member lands on that member only.
  This is the main reason the count below is finer than the 2026-08-06 sample's — see
  *Verification of the 2026-08-06 sample*.
- Frontmatter (`1-6`) is excluded: it configures invocation, it does not govern a generated plan.
  `disable-model-invocation: true` (`3658187`) is therefore absent from the count.

## Columns

- **Site** — `SKILL.md:NN-MM` at `28b5460`.
- **In** — commit that introduced the obligation, from the diffs. When a later commit reformulated
  the same obligation the earlier commit still owns this cell; when a commit replaced a *different*
  rule with this one, this cell is that commit and the note says so.
- **Last** — commit that last changed the clause's **wording**. Where `git blame` attributes the line
  to a later commit that only re-wrapped it around a neighbouring edit, this cell holds the wording
  commit and the clause is listed under *Blame divergences*.
- **Rows** — covering ledger rows, or `uncovered`. `(r)` marks a **restatement**: the clause repeats
  in a gate, an anti-pattern, or the unpublished ledger an obligation stated in a body clause.
- **Anchoring** — how the anchor was obtained, per row:
  - `declared` — the ledger row was written together with the commit that introduced the clause, so
    the pairing is recorded, not inferred. True for `R-010` and `R-011` only.
  - `reconstructed` — the row was written backwards onto a commit already made. The clause was never
    recorded: the row is anchored to a commit, not to a text, and this map is inferring the pairing.
    Nine rows out of eleven are in this state.
  - `unresolved` — the anchor does not resolve. Recorded as a failure instead of resolved by picking
    the most similar clause.
  - `—` for uncovered clauses.

## The map

### Preamble — `SKILL.md:10-15`

| ID | Site | Clause | In | Last | Rows | Anchoring |
|---|---|---|---|---|---|---|
| C-001 | `SKILL.md:10-11` | Produce a multi-session delivery map, not an implementation plan or task backlog | `b0d6dc5` | `b0d6dc5` | uncovered | — |
| C-002 | `SKILL.md:11` | Treat each slice as independently schedulable; do not decompose into implementation tasks | `b0d6dc5` | `b0d6dc5` | uncovered | — |
| C-003 | `SKILL.md:13` | Plan for early validated learning, short feedback loops, cheap reprioritization | `c001780` | `c001780` | uncovered | — |
| C-004 | `SKILL.md:13-15` | Treat a result as valuable when it helps an end user or a developer test the real product | `c001780` | `e0049d9` | uncovered | — |

### Choose the branch — `SKILL.md:17-24`

| ID | Site | Clause | In | Last | Rows | Anchoring |
|---|---|---|---|---|---|---|
| C-005 | `SKILL.md:19` | Create: execute steps 1–5 and satisfy every completion criterion | `c001780` | `c001780` | uncovered | — |
| C-006 | `SKILL.md:20` | Review: execute steps 1–2, then follow `Review an existing plan` | `c001780` | `28b5460` | uncovered | — |
| C-007 | `SKILL.md:21-22` | Split, merge, or reorder: steps 1–2 for the affected scope, then that section | `c001780` | `28b5460` | uncovered | — |
| C-008 | `SKILL.md:24` | Modify an existing plan only when requested | `c001780` | `c001780` | uncovered | — |

### § 1 Build the evidence inventory — `SKILL.md:26-61`

| ID | Site | Clause | In | Last | Rows | Anchoring |
|---|---|---|---|---|---|---|
| C-009 | `SKILL.md:28` | Inspect designated goals, decisions, plans, and relevant repository state | `c001780` | `c001780` | uncovered | — |
| C-010 | `SKILL.md:28-39` | Record every statement capable of changing scope, order, architecture, or a go/no-go decision under the nine categories | `c001780` | `c001780` | uncovered | — |
| C-011 | `SKILL.md:41` | Retain sources | `c001780` | `c001780` | uncovered | — |
| C-012 | `SKILL.md:41` | Mark unsupported conclusions as assumptions | `c001780` | `c001780` | uncovered | — |
| C-013 | `SKILL.md:43` | Reconcile the inventory before mapping | `745192f` | `745192f` | uncovered | — |
| C-014 | `SKILL.md:43-48` | Sweep the sources for conflicts and undecided choices, listing each entry with a reference for every side | `d977043` | `d977043` | R-003 | reconstructed |
| C-015 | `SKILL.md:47-48` | A qualifying adjective — `cheap`, `multilingual`, `managed` — is not a choice | `d977043` | `d977043` | R-003 | reconstructed |
| C-016 | `SKILL.md:50` | Do not silently pick a side or reopen a decision that a source declares closed | `745192f` | `d977043` | uncovered | — |
| C-017 | `SKILL.md:50-52` | Expose every material entry with an `Open questions` item naming the slices it blocks, or a spike before the first blocked slice | `745192f` | `87150d3` | R-002 (m2), R-003 | reconstructed |
| C-018 | `SKILL.md:54-55` | Exposing is not resolving; only a source that selects resolves an entry | `87150d3` | `87150d3` | R-010 | **declared** |
| C-019 | `SKILL.md:56-57` | While an entry is open, no `Includes` or `Verification` bullet of a slice it blocks may assert a side | `d977043` | `87150d3` | R-002 (m1), R-010 | R-002 reconstructed; R-010 **declared** |
| C-020 | `SKILL.md:59-60` | Gate: every sequencing-relevant statement has applicable classifications and a source | `c001780` | `c001780` | uncovered | — |
| C-021 | `SKILL.md:60` | Gate: unsupported conclusions are assumptions | `c001780` | `c001780` | uncovered | — |
| C-022 | `SKILL.md:60` | Gate: exclusions have explicit rationale | `c001780` | `c001780` | uncovered | — |
| C-023 | `SKILL.md:60-61` | Gate: every material conflict and undecided choice is resolved, exposed with the slices it blocks, or assigned to a spike | `745192f` | `d977043` | R-002 (r), R-003 (r) | reconstructed |

`87150d3` rewrote `SKILL.md:50-57` (`+7/-3`, verified against the diff). It hit **C-017** (`Close` →
`Expose`), **C-019** (rewritten), and introduced **C-018**. It did not hit the second member of
`R-002`, which quantifies over `SKILL.md:51` — the `naming the slices it blocks` requirement, intact
since `d977043`. Confirms the plan's *«di `R-002` la riformulazione tocca il solo primo membro»*.

### § 2 Map themes, outcomes, and dependencies — `SKILL.md:63-129`

| ID | Site | Clause | In | Last | Rows | Anchoring |
|---|---|---|---|---|---|---|
| C-024 | `SKILL.md:65` | List independently useful outcomes | `c001780` | `c001780` | uncovered | — |
| C-025 | `SKILL.md:65-72` | Create a separate product theme when capabilities differ materially on any of the five criteria | `c001780` | `c001780` | uncovered | — |
| C-026 | `SKILL.md:74` | Do not optimize for fewer themes | `c001780` | `c001780` | uncovered | — |
| C-027 | `SKILL.md:74-75` | Merge themes only when neither can produce independent feedback or move independently | `c001780` | `c001780` | uncovered | — |
| C-028 | `SKILL.md:75-76` | A user-facing identity or access capability may be a theme; an authentication library or database layer is not | `c001780` | `c001780` | uncovered | — |
| C-029 | `SKILL.md:78` | Run both tests explicitly | `745192f` | `745192f` | uncovered | — |
| C-030 | `SKILL.md:80-82` | Split test: split when either capability can be cancelled, deferred, or reordered without invalidating the other's evidence; a shared entity, form, pipeline, or implementation is not a sufficient reason to merge | `745192f` | `745192f` | **uncovered** | — |
| C-031 | `SKILL.md:83-85` | Merge test: merge when the capabilities share interaction, invariant, and learning target and neither produces useful feedback alone | `745192f` | `745192f` | uncovered | — |
| C-032 | `SKILL.md:87-89` | Give every theme one desired outcome in product language | `c001780` | `c001780` | uncovered | — |
| C-033 | `SKILL.md:87`, `SKILL.md:90` | Give every theme its first `NOW` product slice that validates the complete desired outcome | `c001780` | `9aa2586` | R-008 | reconstructed |
| C-034 | `SKILL.md:92-93` | An enabler may precede that validator but cannot substitute for it unless the theme's desired outcome is itself for a developer | `9aa2586` | `eb926bb` | R-008 | reconstructed |
| C-035 | `SKILL.md:93-95` | A theme claiming that exception appends `*(Developer outcome)*` to its desired outcome in the published table | `eb926bb` | `eb926bb` | R-011 | **declared** |
| C-036 | `SKILL.md:95-96` | A slice that validates only one capability inside a broader theme outcome is not that theme's first validator | `9aa2586` | `9aa2586` | R-008 | reconstructed |
| C-037 | `SKILL.md:98-99` | Identify hard dependencies only: a predecessor is hard when no controlled input or narrower real precursor can make the outcome verifiable | `c001780` | `fb1ec51` | uncovered | — |
| C-038 | `SKILL.md:99-100` | Convenient reuse, a fuller demo, or a preferred order is not a hard dependency | `c001780` | `fb1ec51` | uncovered | — |
| C-039 | `SKILL.md:102` | Controlled inputs may replace unfinished UI or administration | `c001780` | `c001780` | uncovered | — |
| C-040 | `SKILL.md:102-103` | They must still traverse every production path whose correctness materially affects the outcome | `c001780` | `c001780` | uncovered | — |
| C-041 | `SKILL.md:103-104` | Fixtures that inject derived data directly do not remove a dependency on the production computation | `c001780` | `c001780` | uncovered | — |
| C-042 | `SKILL.md:106` | Hard dependencies constrain the slice order and nothing else | `fb1ec51` | `fb1ec51` | uncovered | — |
| C-043 | `SKILL.md:106-107` | Do not grade them, do not write counterfactuals for them, and do not publish them | `fb1ec51` | `fb1ec51` | uncovered | — |
| C-044 | `SKILL.md:109-111` | Greenfield: add a repository prerequisite with CI build, lint, typecheck, and tests, no provisioning or deploy | `c001780` | `c001780` | uncovered | — |
| C-045 | `SKILL.md:109`, `SKILL.md:112-113` | Greenfield: add the smallest deployed walking skeleton that proves the decided infrastructure is connected and running | `c001780` | `d88328f` | uncovered | — |
| C-046 | `SKILL.md:115-118` | The skeleton must exercise every already-decided stateful or managed dependency with no thinner real validator later | `d88328f` | `d88328f` | uncovered | — |
| C-047 | `SKILL.md:122-123` | Keep the skeleton free of domain entities, CRUD, authentication, tenancy, and single-use external adapters | `c001780` | `d88328f` | uncovered | — |
| C-048 | `SKILL.md:123-124` | Make independently useful access and domain behaviour later slices | `c001780` | `c001780` | uncovered | — |
| C-049 | `SKILL.md:126` | Gate: every goal maps to an outcome, theme, and horizon | `c001780` | `c001780` | uncovered | — |
| C-050 | `SKILL.md:126-127` | Gate: theme split/merge decisions pass the independence tests | `c001780` | `c001780` | uncovered | — |
| C-051 | `SKILL.md:127-128` | Gate: hard dependencies are limited to outcomes no controlled input can verify | `fb1ec51` | `fb1ec51` | uncovered | — |
| C-052 | `SKILL.md:128` | Gate: greenfield prerequisites are present and separate | `c001780` | `c001780` | uncovered | — |
| C-053 | `SKILL.md:128-129` | Keep this map in reasoning, not in the published plan | `fb1ec51` | `fb1ec51` | uncovered | — |

`eb926bb` rewrote `SKILL.md:92-96` (`+4/-2`, verified against the diff). The split of that sentence
into **C-034** and **C-035** is deliberate: the two obligations are semicolon-joined in one sentence
but were introduced by different commits and carry different rows, `R-008` reconstructed and `R-011`
declared. Collapsing them would hide exactly the difference the map exists to show. **C-051** is a
replacement, not a reformulation: `fb1ec51` deleted `every predecessor is classified; every hard edge
has a valid counterfactual` and wrote this criterion in their place.

### § 3 Cut valuable vertical slices — `SKILL.md:131-217`

| ID | Site | Clause | In | Last | Rows | Anchoring |
|---|---|---|---|---|---|---|
| C-054 | `SKILL.md:133` | Give each slice one primary valuable outcome and one learning target | `c001780` | `e0049d9` | uncovered | — |
| C-055 | `SKILL.md:133-134` | End users and developers testing the product both count as users | `c001780` | `c001780` | uncovered | — |
| C-056 | `SKILL.md:138` | Each slice independently deployable, verifiable, reviewable, and revertible | `c001780` | `c001780` | uncovered | — |
| C-057 | `SKILL.md:139` | Each slice complete through every production layer required by its outcome | `c001780` | `c001780` | uncovered | — |
| C-058 | `SKILL.md:140` | Each slice safe enough for its stated users and environment | `c001780` | `c001780` | uncovered | — |
| C-059 | `SKILL.md:141` | Each slice the smallest coherent path that produces useful evidence | `c001780` | `c001780` | uncovered | — |
| C-060 | `SKILL.md:145-151` | Prefer a thin real capability followed by deepening slices; treat the five listed conditions as split warnings | `c001780` | `c001780` | uncovered | — |
| C-061 | `SKILL.md:153-155` | Keep behaviours together when they share theme, interaction or pipeline, adapter, invariant, and learning target and separation yields no useful feedback | `c001780` | `c001780` | uncovered | — |
| C-062 | `SKILL.md:155-156` | Shared create/edit review or multiple inputs to one established media pipeline may remain cohesive | `c001780` | `c001780` | uncovered | — |
| C-063 | `SKILL.md:156` | Defer independently optional interactions to `LATER` | `c001780` | `c001780` | uncovered | — |
| C-064 | `SKILL.md:158` | After the first cut, audit adjacent slices in both directions and record the verdict for each pair | `745192f` | `d977043` | uncovered | — |
| C-065 | `SKILL.md:158-159` | Merge slices that duplicate the same interaction and invariant without changing a decision | `745192f` | `745192f` | uncovered | — |
| C-066 | `SKILL.md:159-160` | Split independently testable fallbacks, external adapters, lifecycle operations, or failure profiles | `745192f` | `745192f` | uncovered | — |
| C-067 | `SKILL.md:161-162` | Split whenever either part can be deferred independently, or when one slice can fail for two decision-changing causes | `d977043` | `d977043` | uncovered | — |
| C-068 | `SKILL.md:163-164` | Deliver a required correction, retry, or escape path before or with the first behaviour that can create the recoverable state | `745192f` | `745192f` | uncovered | — |
| C-069 | `SKILL.md:166-167` | Different failure profiles do not justify non-adjacent partial ownership of one adapter or invariant | `9aa2586` | `9aa2586` | uncovered | — |
| C-070 | `SKILL.md:167-168` | Co-locate the behaviour, or make the first slice establish a complete stable capability later slices consume | `9aa2586` | `9aa2586` | uncovered | — |
| C-071 | `SKILL.md:168-169` | Never interleave another theme while shared adapter or invariant ownership remains partial | `9aa2586` | `9aa2586` | uncovered — candidate for `R-005`'s `9aa2586`, see *Unresolved anchors* | — |
| C-072 | `SKILL.md:173` | Allow an explicit `Enabler` slice only when its primary user is a developer | `c001780` | `c001780` | uncovered | — |
| C-073 | `SKILL.md:175` | Enabler test: exercises a real end-to-end production path, not one isolated layer | `c001780` | `c001780` | uncovered | — |
| C-074 | `SKILL.md:176` | Enabler test: produces executable evidence needed by the next product slice | `c001780` | `c001780` | uncovered | — |
| C-075 | `SKILL.md:177` | Enabler test: resolves one material uncertainty or establishes one high-leverage delivery pattern | `c001780` | `c001780` | R-007 | reconstructed |
| C-076 | `SKILL.md:178` | Enabler test: immediately followed by, or explicitly tied to, the product outcome it enables | `c001780` | `c001780` | uncovered | — |
| C-077 | `SKILL.md:179` | Enabler test: contains no speculative foundation beyond that path | `c001780` | `c001780` | uncovered | — |
| C-078 | `SKILL.md:184-185` | An enabler may include the smallest diagnostic consumer needed to observe its uncertainty | `745192f` | `745192f` | uncovered | — |
| C-079 | `SKILL.md:185-186` | Keep product interaction and business feedback in the successor; the successor adds a user outcome | `745192f` | `745192f` | uncovered | — |
| C-080 | `SKILL.md:187-188` | Do not add a domain dependency to the walking skeleton only because the next slice will need it | `745192f` | `d88328f` | uncovered | — |
| C-081 | `SKILL.md:190-192` | Allow a separate domain-convention enabler only when it independently validates conventions before a riskier slice | `9aa2586` | `9aa2586` | uncovered | — |
| C-082 | `SKILL.md:191-192` | Reuse by later work or presence in an example plan is insufficient | `9aa2586` | `9aa2586` | uncovered | — |
| C-083 | `SKILL.md:196-197` | Keep early slices narrow while conventions need frequent human review | `c001780` | `c001780` | uncovered | — |
| C-084 | `SKILL.md:198` | Increase size only after relevant patterns exist and the combined work remains cohesive | `c001780` | `c001780` | uncovered | — |
| C-085 | `SKILL.md:199` | Never make later slices larger merely because they occur later | `c001780` | `c001780` | uncovered | — |
| C-086 | `SKILL.md:201-202` | Include behaviour-specific validation, authorization, failure handling, logging, observability, accessibility, security, and data integrity where required | `c001780` | `745192f` | uncovered | — |
| C-087 | `SKILL.md:202-204` | State repeated expectations once under `Cross-functional concerns`, but verify them in the first slice that crosses each trust boundary or performs each external side effect | `c001780` | `745192f` | uncovered | — |
| C-088 | `SKILL.md:204-205` | Name relevant abuse, timeout, invalid-output, and partial-failure modes; a generic statement is not evidence | `745192f` | `745192f` | uncovered | — |
| C-089 | `SKILL.md:205-206` | Do not defer production-required failures to generic hardening | `c001780` | `c001780` | uncovered | — |
| C-090 | `SKILL.md:208-209` | Every material claim under `Learning / risk` must map to an observation in `Verification` | `745192f` | `745192f` | uncovered | — |
| C-091 | `SKILL.md:208-209` | Checking that data exists does not demonstrate its quality, usability, latency, or cost | `745192f` | `745192f` | uncovered | — |
| C-092 | `SKILL.md:211-212` | Classify risk spikes, migrations, and operational work separately when they cannot produce a valuable vertical result | `c001780` | `e0049d9` | uncovered | — |
| C-093 | `SKILL.md:214` | Gate: every slice has one outcome and learning target | `c001780` | `c001780` | uncovered | — |
| C-094 | `SKILL.md:214-215` | Gate: every enabler passes all enabler tests and validates no more than one material uncertainty | `c001780` | `d977043` | R-007 | reconstructed |
| C-095 | `SKILL.md:215-216` | Gate: every split warning is resolved by splitting or a concrete cohesion reason | `c001780` | `c001780` | uncovered | — |
| C-096 | `SKILL.md:216-217` | Gate: every in-scope behaviour, and every producer feeding a shared pipeline or adapter, has one owner or explicit exclusion | `c001780` | `d977043` | R-006 (r) | reconstructed |

### ANTI-PATTERNS — `SKILL.md:219-244`

| ID | Site | Clause | In | Last | Rows | Anchoring |
|---|---|---|---|---|---|---|
| C-097 | `SKILL.md:221` | Layer slices | `c001780` | `c001780` | uncovered | — |
| C-098 | `SKILL.md:222-223` | Infrastructure by accumulation | `c001780` | `c001780` | uncovered | — |
| C-099 | `SKILL.md:224-225` | Enabler camouflage | `c001780` | `c001780` | uncovered | — |
| C-100 | `SKILL.md:226-227` | Oversized walking skeleton | `c001780` | `c001780` | uncovered | — |
| C-101 | `SKILL.md:228-230` | Hollow walking skeleton | `d88328f` | `d88328f` | uncovered | — |
| C-102 | `SKILL.md:231-232` | Fake verticality | `c001780` | `c001780` | uncovered | — |
| C-103 | `SKILL.md:233-234` | Premature or split shared pipeline | `d977043` | `d977043` | R-006 (r) | reconstructed |
| C-104 | `SKILL.md:235` | Theme compression | `c001780` | `c001780` | **uncovered** | — |
| C-105 | `SKILL.md:236` | Atomization | `c001780` | `c001780` | uncovered | — |
| C-106 | `SKILL.md:237-238` | Silent contradiction | `745192f` | `d977043` | R-002 (m1, r, partial), R-010 (r, partial) | R-002 reconstructed; R-010 **declared** |
| C-107 | `SKILL.md:239-242` | Deferred safety, with the declared-seam exemption | `c001780` | `2c89e7f` | uncovered | — |
| C-108 | `SKILL.md:243-244` | Horizon dumping | `c001780` | `c001780` | uncovered | — |

**C-106 is a partial restatement.** It names only the unconditional slice, not the choice made by
placing a behaviour in another horizon — the gap the ledger's *Da popolare* already records as a
pending extension of `R-010`. A voice reformulating `C-019` must re-anchor `C-106` too or the two
sites drift apart again.

**C-104 is the anti-pattern the CON-5 row-C diagnosis lands on**, together with `C-030`. Neither has
a row.

### § 4 Assign horizons and order for learning — `SKILL.md:246-317`

| ID | Site | Clause | In | Last | Rows | Anchoring |
|---|---|---|---|---|---|---|
| C-109 | `SKILL.md:248` | Assign every behaviour to exactly one horizon | `c001780` | `c001780` | uncovered | — |
| C-110 | `SKILL.md:250-251` | `NOW` is the smallest coherent release including the value hypothesis, material risk validation, and safe-operation baseline | `c001780` | `c001780` | uncovered | — |
| C-111 | `SKILL.md:252-253` | `LATER` depends on `NOW` evidence; record its promotion trigger | `c001780` | `c001780` | R-004 (m2) | reconstructed |
| C-112 | `SKILL.md:254` | `OUT-OF-SCOPE` records its rationale; do not plan implementation | `c001780` | `c001780` | R-004 (m2) | reconstructed |
| C-113 | `SKILL.md:256-257` | Admission test: `NOW` requires a source that asks for the behaviour, `LATER` a trigger, `OUT-OF-SCOPE` a declared exclusion | `d977043` | `d977043` | R-004 (m1) | reconstructed |
| C-114 | `SKILL.md:257-258` | Trace each `NOW` slice to the requesting statement in reasoning, not in the published plan | `d977043` | `d977043` | uncovered | — |
| C-115 | `SKILL.md:258-259` | A capability merely compatible or convenient was never requested: it belongs in `LATER` with its trigger | `d977043` | `d977043` | R-004 (m1) | reconstructed |
| C-116 | `SKILL.md:261-268` | Respect hard dependencies, then order `NOW` by the six listed factors | `c001780` | `c001780` | uncovered | — |
| C-117 | `SKILL.md:270` | Use the cheapest real input capable of validating a risky engine | `c001780` | `c001780` | uncovered | — |
| C-118 | `SKILL.md:270-271` | Do not front-load commodity work for reuse alone | `c001780` | `c001780` | uncovered | — |
| C-119 | `SKILL.md:273-274` | Controlled cheap inputs may validate shared machinery in an enabler, but do not reorder independently useful product flows | `9aa2586` | `9aa2586` | uncovered — candidate for `R-006`'s `9aa2586`, see *Unresolved anchors* | — |
| C-120 | `SKILL.md:274-275` | When sources define a recovery chain, extend the primary interaction with automatic recovery before a separate manual escape | `9aa2586` | `9aa2586` | uncovered — candidate for `R-005`'s `9aa2586`, see *Unresolved anchors* | — |
| C-121 | `SKILL.md:277-278` | After validating existential risks, prefer breadth before depth | `745192f` | `745192f` | uncovered | — |
| C-122 | `SKILL.md:278-280` | Depart from breadth only for a differentiator, material risk, required recovery, or higher frequency, stated once under `Ordering criteria` | `745192f` | `745192f` | uncovered | — |
| C-123 | `SKILL.md:282-284` | Required recovery outranks breadth: deliver the remedy of a named failure mode before opening a different theme | `d977043` | `d977043` | R-005 | reconstructed |
| C-124 | `SKILL.md:283-284` | A remedy the sources declare a fallback of a delivered path closes that path and is not optional depth | `d977043` | `d977043` | uncovered | — |
| C-125 | `SKILL.md:284-286` | A slice that opens a pipeline or adapter shared by several paths follows every `NOW` slice that feeds it, and owns it alone | `d977043` | `d977043` | R-006 (m1, m2) | reconstructed |
| C-126 | `SKILL.md:288-289` | Ship the tenancy, ownership, or scope boundary with the first slice that persists data; a single named resolver owns the current scope | `2c89e7f` | `2c89e7f` | R-001 (m2) | reconstructed |
| C-127 | `SKILL.md:289-291` | A later slice may replace a configured scope with an authenticated one at one seam; state that seam under `Cross-functional concerns` | `2c89e7f` | `2c89e7f` | R-001 (m2) | reconstructed |
| C-128 | `SKILL.md:291-292` | Never defer the boundary itself, and never defer identity when no such seam exists | `2c89e7f` | `2c89e7f` | uncovered | — |
| C-129 | `SKILL.md:294-295` | Once the evidence that justified deferring identity exists, deliver identity before further user-facing slices | `745192f` | `745192f` | uncovered — candidate for `R-001` m1, see *Unresolved anchors* | — |
| C-130 | `SKILL.md:295-297` | Past the second `NOW` slice delivering to an end user, justify the remaining deferral once under `Ordering criteria` | `a06a5cc` | `a06a5cc` | R-009 (m2) | reconstructed |
| C-131 | `SKILL.md:297-299` | Every `NOW` slice preceding identity states its own audience | `a06a5cc` | `a06a5cc` | R-009 (m1) | reconstructed |
| C-132 | `SKILL.md:301-302` | When `NOW` targets selected end users, end it with the smallest release slice usable in its intended environment | `745192f` | `745192f` | uncovered | — |
| C-133 | `SKILL.md:302-303` | Tag it `(Release: delivery)`, not `Enabler`, and include only source-backed operational readiness | `745192f` | `745192f` | uncovered | — |
| C-134 | `SKILL.md:303-304` | When `NOW` ends at developer validation, state that audience and environment explicitly | `745192f` | `745192f` | uncovered | — |
| C-135 | `SKILL.md:306-307` | When a real slice cannot resolve a material uncertainty, define a time-boxed spike with its five components | `c001780` | `c001780` | uncovered | — |
| C-136 | `SKILL.md:309-310` | Add checkpoints only where evidence can cancel, promote, reorder, split, or change unfinished work | `c001780` | `c001780` | uncovered | — |
| C-137 | `SKILL.md:312` | Gate: every differentiator and material risk has a first validator | `c001780` | `c001780` | uncovered | — |
| C-138 | `SKILL.md:312-313` | Gate: all horizon assignments are exclusive and pass the admission test | `c001780` | `d977043` | R-004 (r) | reconstructed |
| C-139 | `SKILL.md:313` | Gate: every `LATER` item has a trigger | `c001780` | `c001780` | R-004 (r) | reconstructed |
| C-140 | `SKILL.md:313-314` | Gate: every named failure mode whose remedy is in `NOW` gets it before a different theme starts | `d977043` | `d977043` | R-005 (r) | reconstructed |
| C-141 | `SKILL.md:315` | Gate: every shared pipeline follows its producers | `d977043` | `d977043` | R-006 (r) | reconstructed |
| C-142 | `SKILL.md:315-316` | Gate: every slice preceding identity names an audience compatible with a configured scope | `a06a5cc` | `a06a5cc` | R-009 (r) | reconstructed |
| C-143 | `SKILL.md:316` | Gate: order respects dependencies and delivery maturity | `c001780` | `c001780` | uncovered | — |
| C-144 | `SKILL.md:316-317` | Gate: checkpoints name evidence and the decisions they can change | `c001780` | `c001780` | uncovered | — |

### § 5 Publish and audit — `SKILL.md:319-375`

| ID | Site | Clause | In | Last | Rows | Anchoring |
|---|---|---|---|---|---|---|
| C-145 | `SKILL.md:321` | Before publication, complete an unpublished ledger | `9aa2586` | `9aa2586` | uncovered | — |
| C-146 | `SKILL.md:323` | Ledger: every source behaviour to its theme, horizon, and owning slice or explicit exclusion | `9aa2586` | `9aa2586` | R-004 (r) | reconstructed |
| C-147 | `SKILL.md:324` | Ledger: every theme to its complete product outcome and first product validator | `9aa2586` | `9aa2586` | R-008 (r) | reconstructed |
| C-148 | `SKILL.md:325` | Ledger: every shared adapter and invariant to one complete owner | `9aa2586` | `9aa2586` | R-006 (r) | reconstructed |
| C-149 | `SKILL.md:326` | Ledger: every named failure to its recovery and required position | `9aa2586` | `9aa2586` | R-005 (r) | reconstructed |
| C-150 | `SKILL.md:327` | Ledger: every unresolved decision to blocked slices and its prior spike or open question | `9aa2586` | `9aa2586` | R-002 (m2, r), R-003 (r) | reconstructed |
| C-151 | `SKILL.md:328` | Ledger: every adjacent slice pair to its split/merge verdict | `9aa2586` | `9aa2586` | uncovered | — |
| C-152 | `SKILL.md:330-331` | Reject the draft when a mapping is missing, conflicting, duplicated incompatibly, or partial | `9aa2586` | `9aa2586` | uncovered | — |
| C-153 | `SKILL.md:331-332` | Keep the ledger in reasoning, not the published plan | `9aa2586` | `9aa2586` | uncovered | — |
| C-154 | `SKILL.md:334-335` | Read and follow the template; preserve hierarchy, section names, field names, and order; write in the user's language | `c001780` | `c001780` | uncovered | — |
| C-155 | `SKILL.md:337` | Use bullets or tables for technical sections; avoid prose blocks | `c001780` | `fb1ec51` | uncovered | — |
| C-156 | `SKILL.md:338` | Keep `Cross-functional concerns`, `NOW`, `LATER`, `OUT-OF-SCOPE` as exact labels | `c001780` | `c001780` | uncovered | — |
| C-157 | `SKILL.md:339` | Set every `Themes.First validation` cell to the number of an existing `NOW` slice | `6476f32` | `6476f32` | **uncovered** | — |
| C-158 | `SKILL.md:340-341` | Detail numbered `NOW` slices only; tag them; keep `LATER` conditional and compact | `c001780` | `745192f` | uncovered | — |
| C-159 | `SKILL.md:342` | Separate every numbered `NOW` slice title from its fields with a `---` rule | `fb1ec51` | `fb1ec51` | uncovered | — |
| C-160 | `SKILL.md:343-344` | Give every `NOW` slice bullet lists under `Includes`, `Verification`, `Outcome`, in that order | `c001780` | `fb1ec51` | uncovered | — |
| C-161 | `SKILL.md:345` | Add `Learning / risk` between `Verification` and `Outcome` only when material | `c001780` | `fb1ec51` | uncovered | — |
| C-162 | `SKILL.md:346-347` | Add other slice-specific annotations only as `**Label**` blocks after the standard fields | `fb1ec51` | `fb1ec51` | uncovered | — |
| C-163 | `SKILL.md:348-349` | Publish no dependency graph, no sequencing section, no per-slice ordering rationale | `fb1ec51` | `fb1ec51` | uncovered | — |
| C-164 | `SKILL.md:350-351` | Always publish all three horizon sections; use `- None identified.` when empty | `c001780` | `c001780` | uncovered | — |
| C-165 | `SKILL.md:352` | Omit empty optional sections, including `Non-product work` and `Open questions` | `c001780` | `c001780` | uncovered | — |
| C-166 | `SKILL.md:354-355` | Keep the document readable in one pass: at most five bullets per field, one line per bullet, no restating of `Cross-functional concerns` | `fb1ec51` | `fb1ec51` | uncovered | — |
| C-167 | `SKILL.md:357` | After publishing, run the validator | `c001780` | `ed35cb7` | uncovered | — |
| C-168 | `SKILL.md:358-359` | Publish first and let the validator find structural defects instead of reading its source | `fb1ec51` | `745192f` | uncovered | — |
| C-169 | `SKILL.md:359-361` | Resolve `<skill-dir>` to the absolute path of the directory containing this `SKILL.md` | `ed35cb7` | `ed35cb7` | uncovered | — |
| C-170 | `SKILL.md:367` | Fix every structural failure | `c001780` | `c001780` | uncovered | — |
| C-171 | `SKILL.md:369` | Complete when: the validator passes | `c001780` | `c001780` | uncovered | — |
| C-172 | `SKILL.md:369` | Complete when: themes trace to first validators | `c001780` | `c001780` | R-008 (r) | reconstructed |
| C-173 | `SKILL.md:369-370` | Complete when: `NOW` is a coherent valuable release | `c001780` | `e0049d9` | uncovered | — |
| C-174 | `SKILL.md:370` | Complete when: enablers are vertical and adjacent to their product outcome | `c001780` | `c001780` | uncovered | — |
| C-175 | `SKILL.md:370-371` | Complete when: `LATER` is evidence-dependent | `c001780` | `c001780` | R-004 (r) | reconstructed |
| C-176 | `SKILL.md:371` | Complete when: the slice order respects every hard dependency | `fb1ec51` | `fb1ec51` | uncovered | — |
| C-177 | `SKILL.md:371-372` | Complete when: every source behaviour has one horizon | `c001780` | `c001780` | R-004 (r) | reconstructed |
| C-178 | `SKILL.md:372` | Complete when: no slice asserts a side of a listed conflict or undecided choice | `d977043` | `d977043` | R-002 (m1, r), R-010 (r) | R-002 reconstructed; R-010 **declared** |
| C-179 | `SKILL.md:372-374` | Complete when: every external dependency invoked in `NOW` has a selecting source or an `Open questions` entry, and every published question names the slices it blocks | `d977043` | `d977043` | R-003 (r), R-002 (m2, r) | reconstructed |
| C-180 | `SKILL.md:374` | Complete when: end-user `NOW` reaches its intended environment | `745192f` | `745192f` | uncovered | — |
| C-181 | `SKILL.md:374-375` | Complete when: only implementation-changing questions remain | `c001780` | `c001780` | uncovered | — |

**C-157 has no row and is the precondition of `R-011`.** `R-011` quantifies over rows of the `Themes`
table *whose `First validation` resolves* to a slice; the ledger records 17 unresolvable cells in
`CX` CON-2…CON-4 under *Difetti degli artefatti mai registrati*, explicitly noting the defect is not
attributable to any existing row. `C-157` is the clause that would carry it.

### Review an existing plan — `SKILL.md:377-390`

| ID | Site | Clause | In | Last | Rows | Anchoring |
|---|---|---|---|---|---|---|
| C-182 | `SKILL.md:379` | Apply every applicable criterion from steps 2–5 | `c001780` | `c001780` | uncovered | — |
| C-183 | `SKILL.md:379-384` | For each failure state target, failed criterion or anti-pattern, delivery consequence, concrete change | `c001780` | `c001780` | uncovered | — |
| C-184 | `SKILL.md:386` | Keep passing verdicts internal | `c001780` | `c001780` | uncovered | — |
| C-185 | `SKILL.md:386` | Modify the plan only when requested | `c001780` | `c001780` | uncovered | — |
| C-186 | `SKILL.md:388` | Complete when: every applicable criterion has a pass, fail, or not-applicable verdict | `c001780` | `c001780` | uncovered | — |
| C-187 | `SKILL.md:388-390` | Complete when: every differentiator, risk, horizon assignment, theme boundary, slice, and ordering constraint is traceable to a verdict | `c001780` | `fb1ec51` | uncovered | — |

### Split, merge, or reorder an existing plan — `SKILL.md:392-417`

Introduced whole by `28b5460` on 2026-08-06, after the last ledger row was written. Every clause is
uncovered, and none of the eleven rows can be read as quantifying over this branch.

| ID | Site | Clause | In | Last | Rows | Anchoring |
|---|---|---|---|---|---|---|
| C-188 | `SKILL.md:394-395` | Reopen only the affected scope | `28b5460` | `28b5460` | uncovered | — |
| C-189 | `SKILL.md:395` | Leave the rest of the plan untouched | `28b5460` | `28b5460` | uncovered | — |
| C-190 | `SKILL.md:395-396` | An edit is not a rewrite; unrelated churn hides what actually moved | `28b5460` | `28b5460` | uncovered | — |
| C-191 | `SKILL.md:398-399` | Justify the edit against the test that owns it: split/merge tests, ordering rules, or a checkpoint whose evidence arrived | `28b5460` | `28b5460` | uncovered | — |
| C-192 | `SKILL.md:399-400` | Size, tidiness, and preference are not justifications | `28b5460` | `28b5460` | uncovered | — |
| C-193 | `SKILL.md:400` | When no test supports the requested edit, say so and stop | `28b5460` | `28b5460` | uncovered | — |
| C-194 | `SKILL.md:402-404` | Conserve the behaviour set: a split distributes and introduces none, a merge yields one outcome, a reorder changes positions only | `28b5460` | `28b5460` | uncovered | — |
| C-195 | `SKILL.md:404-405` | A behaviour that loses its owner moves to `LATER` with a trigger or `OUT-OF-SCOPE` with a rationale, never disappears | `28b5460` | `28b5460` | uncovered | — |
| C-196 | `SKILL.md:407` | Apply steps 3–4 to the affected scope, then republish through step 5, validator included | `28b5460` | `28b5460` | uncovered | — |
| C-197 | `SKILL.md:407-410` | Repair every reference the edit invalidates | `28b5460` | `28b5460` | uncovered | — |
| C-198 | `SKILL.md:410` | A checkpoint whose evidence triggered this edit records the decision it produced | `28b5460` | `28b5460` | uncovered | — |
| C-199 | `SKILL.md:412` | Complete when: every applicable step-5 criterion still holds | `28b5460` | `28b5460` | uncovered | — |
| C-200 | `SKILL.md:412-413` | Complete when: the edit traces to a split test, merge test, ordering rule, or checkpoint | `28b5460` | `28b5460` | uncovered | — |
| C-201 | `SKILL.md:413-414` | Complete when: each resulting slice has one outcome and one learning target and passes the independence tests | `28b5460` | `28b5460` | uncovered | — |
| C-202 | `SKILL.md:414-415` | Complete when: the behaviour set changed only through a recorded horizon move | `28b5460` | `28b5460` | uncovered | — |
| C-203 | `SKILL.md:415` | Complete when: every reference to a slice number resolves to the slice it meant | `28b5460` | `28b5460` | uncovered | — |
| C-204 | `SKILL.md:415-416` | Complete when: slices outside the affected scope are unchanged | `28b5460` | `28b5460` | uncovered | — |
| C-205 | `SKILL.md:416-417` | Complete when: any new departure from breadth before depth is stated once under `Ordering criteria` | `28b5460` | `28b5460` | uncovered | — |

## Row index

All eleven rows, read from the row side. Neither direction is 1:1 — `R-004` covers nine clauses,
`C-019` is covered by two rows.

| Row | `Commit` cell | Body clauses | Restatements | Anchoring | Note |
|---|---|---|---|---|---|
| R-001 | `2c89e7f` | C-126, C-127 (m2) | — | m2 reconstructed; **m1 unresolved** | m1 has no clause: see below |
| R-002 | `d977043` | C-019 (m1), C-017 (m2) | C-023, C-106 (partial), C-150, C-178, C-179 | reconstructed | m1's clause rewritten by `87150d3`; the row still names `d977043` |
| R-003 | `d977043` | C-014, C-015, C-017 | C-023, C-150, C-179 | reconstructed | one disjunct anchored outside `SKILL.md` |
| R-004 | `d977043` | C-111, C-112, C-113, C-115 | C-138, C-139, C-146, C-175, C-177 | reconstructed | m2's clauses predate the row's commit (`c001780`) |
| R-005 | `d977043`, `9aa2586` | C-123 | C-140, C-149 | reconstructed; **`9aa2586` component unresolved** | |
| R-006 | `d977043`, `9aa2586` | C-125 | C-096, C-103, C-141, C-148 | reconstructed; **m1 second half and `9aa2586` component unresolved** | |
| R-007 | `d977043` | C-075, C-094 | — | reconstructed | operative criterion (`Subsystem`) lives in the brief, not in `SKILL.md` |
| R-008 | `9aa2586` | C-033, C-034, C-036 | C-147, C-172 | reconstructed | C-034 rewritten by `eb926bb`; the row still names `9aa2586` |
| R-009 | `a06a5cc` | C-130, C-131 | C-142 | reconstructed | reconstructed from the commit message, which names the observed defect |
| R-010 | `87150d3` | C-018, C-019 | C-106 (partial), C-178 | **declared** | |
| R-011 | `eb926bb` | C-035 | — | **declared** | presupposes C-157, which has no row |

The pattern the plan predicted holds on the whole file, not only on the sample: **the anchor is
intact exactly on the two `ex-ante` rows and drifts exactly on the reconstructed ones.** `R-010` and
`R-011` point at clauses that still carry the wording they were written against. `R-002` and `R-008`
point at commits that no longer own their clause — `87150d3` and `eb926bb` do. `R-005` and `R-006`
carry a second commit in `Commit` whose clause cannot be identified at all.

## Unresolved anchors

Rows with at least one member that does not resolve to a clause of `SKILL.md`. Recorded as failures.
The most similar clause is named as a **candidate** and explicitly not adopted.

- **`R-001`, first member** — *«Il piano colloca l'identità dopo il differenziatore».* `2c89e7f`, the
  row's commit, introduced C-107, C-126, C-127 and C-128; none of them orders identity relative to the
  differentiator. Candidates: C-116 (ordering factor 2, `c001780`) and C-129 (`745192f`). Both predate
  the row's commit and neither states the member. **Unresolved.**
- **`R-005`, `9aa2586` component** — the assertion is about interposition of a foreign theme between a
  named failure and its remedy, which is C-123 (`d977043`). No clause introduced by `9aa2586` states
  it. Candidates: C-071 (never interleave while shared ownership is partial) and C-120 (recovery chain
  before manual escape). **Unresolved.**
- **`R-006`, first member, second half** — *«le slice successive che lo riusano lo dichiarano tale».*
  No clause requires a later slice to declare reuse. The ledger says so itself in *Formulazioni
  riscritte*: the requirement was added to the row after CON-5 *because* `CX` never declared reuse.
  The row demands something the skill does not. **Unresolved.**
- **`R-006`, `9aa2586` component** — candidate C-119. Not stated by either member. **Unresolved.**

## Anchors that resolve outside `SKILL.md`

Distinct failure mode from the above: the member resolves, but to `EVALUATION-BRIEF.md`. These rows
cannot be re-anchored by a skill reformulation, and a `verdetto` on them crosses an authority the
`Misurato su` cell must name.

- **`R-003`, second disjunct** — *«presa dal piano fra le alternative che il brief dichiara
  accettabili»* → brief § `Accepted alternatives`. `SKILL.md` states the opposite at C-016: the plan
  must not pick a side. Added when the row was re-tuned on 2026-08-04.
- **`R-006`, second member's exception** — *«salvo quando valida input controllati che attraversano il
  calcolo di produzione e il brief dello scenario ammette la validazione anticipata»* → brief
  § `Accepted alternatives`, verbatim per the ledger.
- **`R-007`, operative criterion** — *«appartengono a `Subsystem` diversi»* → brief
  § `Material uncertainties`. `SKILL.md` says `one material uncertainty` (C-075, C-094) and never
  mentions subsystems. The row was re-tuned onto the subsystem cut at 22:41 on 2026-08-04, in the same
  minute as the brief's table.

## Totals

| | Clauses |
|---|---|
| Whole file | **205** |
| Covered by at least one row | **40** (20%) |
| — of which body clauses | 20 |
| — of which restatements in gates, anti-patterns, or the unpublished ledger | 20 |
| **Uncovered** | **165** (80%) |

Section breakdown of the uncovered:

| Section | Clauses | Covered | Uncovered |
|---|---|---|---|
| Preamble + Choose the branch | 8 | 0 | 8 |
| § 1 | 15 | 6 | 9 |
| § 2 | 30 | 4 | 26 |
| § 3 | 43 | 3 | 40 |
| ANTI-PATTERNS | 12 | 2 | 10 |
| § 4 | 36 | 15 | 21 |
| § 5 | 37 | 10 | 27 |
| Review an existing plan | 6 | 0 | 6 |
| Split, merge, or reorder | 18 | 0 | 18 |

The 40 covered clauses split evenly between body clauses and restatements, and eighteen of the twenty
restatements are gate members or unpublished-ledger bullets. **The three branches the skill
offers — create, review, split/merge/reorder — are covered asymmetrically to the point of being
incomparable:** `Review` and `Split, merge, or reorder` have 24 clauses and not one row. Every ledger
row was written against a *created* plan, so the two other branches have never made a prediction.

The uncovered clauses are the ones reformulable without breaking a prediction — the list Fase 4
consumes for pruning.

## Verification of the 2026-08-06 sample

The plan records, § Fase 1c, map bullet: perimeter § 1, § 2 and the `Complete when` of § 5;
**37 clauses, 9 covered, 28 uncovered (≈76%)**; the 9 are **4 body clauses plus 5 restatements**; on
those 4 body clauses land **6 rows out of 11**; the § 2 split test (`SKILL.md:80-82`) is uncovered.

Same perimeter, this map:

| | Sample | This map |
|---|---|---|
| Clauses in perimeter | 37 | **56** |
| Covered, restricted to `R-002`, `R-008`, `R-010`, `R-011` | 9 | **11** |
| — body | 4 | **7** |
| — restatements | 5 | **4** |
| Covered by all eleven rows | not stated | 15 |
| Uncovered share | ≈76% | 73% |

**I contradict the sample on the counts and confirm it on everything else.** Explicitly:

- **Contradicted: 37 → 56 clauses, 9 → 11 covered.** The cause is granularity, not disagreement about
  the text. This map splits each gate member into its own entry and splits semicolon-joined
  obligations that different commits introduced (C-034/C-035, C-018/C-019). The sample's 37 is
  reproducible by counting a whole `Proceed when` / `Complete when` gate as one clause, which yields
  the right order of magnitude but cannot produce its own «5 restatements in gates» — the perimeter
  holds only three gates. The two figures cannot both be right; the finer unit is the one Fase 1a
  needs, because an `IMPROVEMENT` entry reformulating a gate member must declare the rows covering
  *that* member.
- **Confirmed: the uncovered share.** 73% against ≈76% — the granularity change moves the ratio by
  three points, not by an order of magnitude.
- **Confirmed: 6 rows out of 11 touch the perimeter.** `R-002`, `R-003`, `R-004`, `R-008`, `R-010`,
  `R-011`. Independent arithmetic, same result.
- **Confirmed: the § 2 split test is uncovered.** C-030, `745192f`, no row — and it is the site the
  ledger names as the diagnosis of CON-5 row C. C-104 (`Theme compression`) is uncovered too, and the
  ledger's diagnosis names both.
- **Confirmed: the anchor holds on `R-010` and `R-011`, drifts on `R-002` and `R-008`.** Verified
  against the diffs: `87150d3` is `+7/-3` on `SKILL.md:50-57` and `eb926bb` is `+4/-2` on
  `SKILL.md:92-96`, exactly as the plan states.
- **Confirmed, with a correction of perimeter:** the plan says four body clauses carry six of eleven
  rows. In this map the six rows touch the perimeter through **seven** body clauses and four
  restatements. The claim that a small number of clauses carries a disproportionate share of the
  ledger survives; the number is 7, not 4.

## Blame divergences

Clauses where `git blame` attributes the line to a commit later than the one that last changed the
clause's **wording**, because a neighbouring edit re-wrapped the paragraph. The `Last` column above
holds the wording commit; this list holds what blame says, so the difference is not silently lost.

| ID | Blame says | Wording last changed by |
|---|---|---|
| C-013 | `d977043` | `745192f` |
| C-016 | `87150d3` | `d977043` |
| C-021, C-022 | `d977043` | `c001780` |
| C-036 | `eb926bb` | `9aa2586` |
| C-048 | `d88328f` | `c001780` |
| C-050 | `fb1ec51` | `c001780` |
| C-065, C-068 | `d977043` | `745192f` |
| C-089 | `745192f` | `c001780` |
| C-095 | `d977043` | `c001780` |
| C-129 | `a06a5cc` | `745192f` |
| C-141 | `a06a5cc` | `d977043` |
| C-169 | `745192f` | `ed35cb7` |
| C-170 | `8c7fe34` | `c001780` |
| C-177 | `fb1ec51` | `c001780` |
| C-180 | `d977043` | `745192f` |

The divergence matters for Fase 1a: a validator that derives the last rewrite from `git blame` alone
would report a clause as re-anchored when only its line wrapping changed, and would re-anchor rows
that nothing touched.
