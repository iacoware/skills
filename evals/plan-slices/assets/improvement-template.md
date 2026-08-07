# Improvement report — cycle CON-[N]

## Inputs

- **Candidate A:** `CANDIDATE-A.md`
- **Candidate B:** `CANDIDATE-B.md`

[The two candidates are labelled A and B and nothing else. Neither is yours. They reach the payload
under these names because their real ones carry the generator's alias.]

## Entries

### 1. [The defect, stated in one line]

---

**Evidence — candidate A**

- `CANDIDATE-A.md:[NN]` — [what the cited text shows]

**Evidence — candidate B**

- `not manifested` — [what candidate B does instead, at the place the defect would appear]

[Each cell holds either a locatable reference — `CANDIDATE-A.md:NN`, `CANDIDATE-B.md:NN-MM`, or
`slice N Includes` naming a slice and one of its fields — or the literal `not manifested` followed by
what that candidate does instead. A defect no candidate manifests is not a defect this cycle
observed. A defect shown at several places may name them all in one cell —
`CANDIDATE-A.md:NN-MM,PP-QQ` — and every span is resolved: more sites is a stronger claim, and each
one is checked.]

**Existing rule that failed to prevent the defect**

- **Clause:** `SKILL.md:[NN]-[MM]` § `[section title]` — «[the clause, quoted]»
- **Covering rows:** `R-[NNN]`[, `R-[NNN]`]

[`Clause: none` when the skill states nothing on the point; then `Covering rows: none` too. When a
clause is named, `Covering rows` lists every ledger row that covers it, or `uncovered` when no row
does. Those rows are what the cycle re-anchors or what this entry must absorb; declaring `uncovered`
for a clause the ledger covers discards the entry.]

**Remedy**

- `reformulation` | `reach-change` | `addition`

[`reformulation` — the named clause changes wording and keeps its reach; the covering rows are
re-anchored. `reach-change` — the rule's reach is extended, restricted, or corrected; `Merged claim`
states the single row that replaces the covering rows. `addition` — the skill gains a rule it did
not have, and a new ledger row with it.]

[**How many rows a reformulation adds is decided at application, against the `Binary test` below,
and it is not always zero.** Where the test is already entailed by a covering row's claim, no row is
added: two rows on one clause count one piece of evidence twice. Where the change carries a limb no
active row predicts, that limb becomes a row. The gate cannot check this — it is structural, and it
cannot tell a reformulation from a reach extension by reading the text either. The report does, in
*Entries applied*. If the change extends the rule's reach, the honest value here is `reach-change`
and a `Merged claim` is owed.]

**Change to the skill**

- **Section:** `[section title]`
- **Change:** [the normative modification, in the wording it would take in `SKILL.md`]

**Merged claim**

- [The one claim that replaces every covering row declared above, in the grammar of `Binary test`.]

[Required when `Remedy` is `reach-change`, forbidden otherwise. Merge only when the merged claim
stays decidable on a generated plan in one reading; where it would blur, keep the rows apart and
propose a reformulation instead.]

**Reformulation attempted and discarded, and why**

- **Reformulation attempted:** [the rewriting of the named clause that was actually written]
- **Discarded because:** [what that rewriting fails to cover, stated over a generated plan]

[Required when `Remedy` is `addition` **and** a clause is named, forbidden otherwise. The default
remedy for a named clause is to reformulate it; adding rules next to it needs a written reason.
**«The clause is covered by a ledger row» is not an admissible reason.** Covered clauses are the few
already accused — twenty body clauses out of 205 carry the whole ledger — which makes them the
likeliest candidates for reformulation, not the exempt ones.]

**Binary test**

- [One claim a generated plan can falsify on its own, in the grammar of the ledger's rows: `No NOW
  slice …`, `Every LATER entry …`, `The plan …`, `If …`. It states what a plan does, not what it
  should do, and it names what it quantifies over.]

**Cost**

- [What is removed or merged if this rule enters. `none` plus the reason when nothing is.]

[Repeat one numbered H3 section per entry. An entry that fails the contract is discarded on its own;
the rest of the document stands, and the document is never regenerated.]
