# Consensus cycle CON-6 — report

CON-6 ran between 2026-08-06 and 2026-08-07 and is **complete**: generation, structural validation,
`improve`, gate, `review`, `verdetto`, `recidiva`, application. It is the first cycle executed under
`CONSENSUS-WORKFLOW.md` § *Il ciclo* end to end, the first whose verdicts come from a `verdetto`
call rather than offline human reading, and the first instance of `assets/report-template.md`. Every
number below is composition over the artifacts the cycle produced; nothing here cost a call.

It is also the first report that had to **correct its own template**. The corrections are listed
under *Deviations from the procedure*, with what forced each one; they were made in
`assets/report-template.md`, not worked around here.

## Inputs

- **`SKILL.md` at generation:** `28b5460`, 417 lines
- **Candidates:** `recipe-app/results/PLAN-CC-CON-6.md`, `recipe-app/results/PLAN-CX-CON-6.md`
- **Improvement reports:** `PLAN-CC-CON-6.IMPROVEMENT.md`, `PLAN-CX-CON-6.IMPROVEMENT.md`
- **Reviews:** `PLAN-CC-CON-6.REVIEW.md`, `PLAN-CX-CON-6.REVIEW.md`
- **Verdicts:** `PLAN-CC-CON-6.VERDICTS.md`, `PLAN-CX-CON-6.VERDICTS.md`
- **Recidiva:** `CONSENSUS-CON-6.RECIDIVA.md`
- **Models and effort:** generation `claude-opus-5`/`medium` (`CC`) and `gpt-5.6-sol`/`medium` (`CX`);
  `improve`, `review` and `verdict` `claude-opus-5`/`high` (`CC`) and `gpt-5.6-sol`/`high` (`CX`);
  `recidiva` `claude-opus-5`/`high`, on `CC`
- **`Measured on`**, copied verbatim into every ledger row this cycle touches:

```
CON-6 · `CC`+`CX` · brief+plans+sources · gen `claude-opus-5` medium + `gpt-5.6-sol` medium · verdict CON-6 `verdetto`, two instruments — `CC` `claude-opus-5` high, `CX` `gpt-5.6-sol` high
```

All nine artifacts live under `recipe-app/results/`. The seven the cycle's own executions wrote were
committed under `recipe-app/payloads/CON-6/out*/` as they were produced and moved here at step 9 —
see *Deviations from the procedure*, item 7. The payload directories stay where they are: they are
the record of what each execution was allowed to read, not of what it produced.

## Counters

```
SKILL.md                       417 → 421   (+4)
entries applied                  1
  reformulations                 1
  reach-changes                  0
  additions                      0
new ledger rows                  1
    0 intersection · 1 intersection-theme · 0 judgement · 0 pruning
re-anchored rows                 1   (counter reset to ×0)   R-010
absorbed claims                  0
active rows                     17 → 18
entries discarded by the gate    0   (S2b; the discarded S2 attempt is logged apart, 3 on `Clause`)
discarded verdicts               0   (citation does not resolve)
recidiva                         7 pairs over 11 entries
structural validator            OK on both candidates
provider calls                  11   (9 planned; S2 discarded and repeated as S2b)
rows the cycle could not decide  4   (R-002, R-004, R-008, R-009 — the two instruments disagree)
```

### Reading of the counters

The cycle applied **one reformulation and zero additions** out of eleven conforming entries, and the
skill grew by four lines. That is the shape `improve` bidirezionale was built to make reachable, and
this is the first cycle in which the ratchet was actually measured rather than asserted: ten of the
eleven entries are held back by the filter, not by an editorial judgement.

What the numbers accuse is the **filter's yield, not its precision**. One entry in eleven survived
two independent reviews — and even that one survived with the two reviews disagreeing about which
side's wording to apply. The counter to reread next cycle is `active rows 17 → 18`: one row entered,
and it is not a split, so it accuses the addition and nothing else.

Four of seventeen rows got **no verdict at all**, because the two `verdetto` instruments contradict
each other on them. That counter did not exist before this cycle and is the most important thing
CON-6 produced about its own machinery: the design has always specified two `verdetto` executions
and has never said what to do when they disagree.

## What produced the verdicts

The fifth `Measured on` slot names a `verdetto` call for the first time, so this section is not
required by the template. It is written anyway, because the instrument has a property the slot does
not carry: **there are two of them, and they judged the same rows against the same two plans.**

Every ledger row therefore has **four** verdicts, not two: `CC` on candidate A, `CC` on candidate B,
`CX` on candidate A, `CX` on candidate B. The arithmetic the ledger prescribes — *«a claim holds only
if it holds on both plans»* — is about the two **plans**. Nothing in `CONSENSUS-WORKFLOW.md`,
`workflow/LEDGER.md` or `REGRESSION-LEDGER.md` says how to combine two **instruments**.

The rule applied here is the project's own, from `CONSENSUS-WORKFLOW.md` § *Vocabolario*: *«due
modelli discordi mandano il punto alla lettura umana, non a un arbitro»*. So:

- **Both instruments agree on both plans** → the verdict stands, and the row's counter moves.
- **The instruments disagree on either plan** → the row takes **no state change**, its counter does
  not move, and it goes to *Points requiring human reading* with both citations. A cycle whose two
  instruments contradict each other has not tested that row.

The consequence, stated so it is not read away: **CON-6 is evidence about thirteen rows, not
seventeen.** For the other four it is evidence that the two instruments read the same published text
differently, which is a fact about the instruments.

## Structural validator

`make validate PLAN=PLAN-CC-CON-6.md` and `PLAN=PLAN-CX-CON-6.md`, step 2. **`OK` on both**, with no
failures. Re-run at step 9 against the same files, unchanged.

Both candidates were generated with the skill explicitly invoked — `/plan-slices` on Claude Code,
`$plan-slices` on Codex — after `3658187` made implicit activation impossible. Two green validator
runs are the observable consequence: the corrected generation prompt held on both sides. The
validator expresses no semantic judgement, so this says the plans have the template's form, nothing
about their quality.

## Entries applied

One entry, the only one both `REVIEW`s classify as shared.

### `A#1` / `B#1` — a slice asserts one side of a behaviour the sources describe incompatibly, and the plan never lists that behaviour among its open entries

- **Origin:** `intersection-theme` — both reviews record `Same remedy: no`. The wording applied is
  **`A`'s**, and the two reviews do not agree on that: `PLAN-CC-CON-6.REVIEW.md` names `A`,
  `PLAN-CX-CON-6.REVIEW.md` names `B`. See *Classification instability* for how the tie was broken
  and for `B`'s wording, which the veto can substitute with one edit.
- **Remedy:** `reformulation` — as declared by the entry. As applied it extends the clause's reach;
  see *Deviations from the procedure*, item 5.
- **Hunk:** `SKILL.md:56-61` § `1 Build the evidence inventory` — replaces the two lines
  `SKILL.md:56-57` at `28b5460`, clause `C-019` of `support/CLAUSE-ROW-MAP.md`
- **Ledger row:** `R-018` — *«Every behaviour that two sources describe incompatibly appears among
  the plan's open entries with the `NOW` slices it blocks, whether or not either source names a
  provider, model, service, or adapter.»*
- **Covering rows declared:** `R-010` — confirmed against `support/clause-row-map.tsv`, where `C-019`
  carries `R-010` with anchoring `declared`. `R-010` is **re-anchored**, not falsified: its claim
  quantifies over a generated plan and the reformulation changed only the clause's text.
- **Discarded reformulation:** `n/a` — the remedy is not an `addition`.

**Why the row is not the entry's own `Binary test`.** The entry's test — *«No `Includes` or
`Verification` bullet asserts in non-conditional form one side of a behaviour that two sources
describe incompatibly, whether or not the plan lists that behaviour among its open entries»* — is
entailed by `R-010`, whose claim already reaches conflicts *«demonstrable by citing two sources in
disagreement»* and never conditions on the behaviour being listed. Writing it as a row would have
put two rows on one clause counting one piece of evidence twice, which is exactly what the two
absorptions of 2026-08-06 closed. `R-018` carries instead the limb of the applied change that no
active row predicted: that the incompatible behaviour is **listed** among the plan's open entries.
`R-002` conditions on a choice already declared open; `R-003` reaches only provider, model, service
and adapter choices, and this entry's defect names none. The reasoning is repeated in
`REGRESSION-LEDGER.md` under the ledger table, where the next cycle will look for it.

## Consequences carried into the ledger

**Re-anchored rows** — automatic: the clause changed wording, the row's claim held its reach.

- `R-010` — new commit `550077f`, counter to `not falsified ×0`, claim unchanged. It read `holds`
  on both plans from both instruments in CON-6, and the reset **discards that measurement on
  purpose**: `×k` counts cycles against a text, and the text changed. The
  boundary is recorded in the row's own `Measured on` cell as well as in the cycle line.

**Absorbed claims** — none. No entry declared `reach-change`, so no `Merged claim` was emitted and
no prediction left the file.

**Splits** — none this cycle.

**Other consequences**

- All 17 pre-existing rows take `Last check: 2026-08-07` and the cycle's `Measured on` line, the four
  undecided ones included: they were checked, and the check did not decide.
- `R-015` moves to `regressed on CC and CX` — the only unanimous falsification of the cycle, and its
  own `Watch for` predicted that this would not be a skill regression. See *Rewritten formulations*.
- `R-001` and `R-016` move to `regressed on CX`, both unanimously and both against `28b5460`.
- `R-006` is held at `not falsified ×1` instead of moving to `×2`: both instruments read `holds` on
  both plans, but `recidiva` pairs `B#5` to it. See *Recidiva*.
- `R-018` is born `ex-ante`, `to verify`, `Commit SKILL.md: 550077f` after the veto, with a `Watch for` cell
  naming the opposite failure — a plan that lists non-conflicts to satisfy the rule.

## Classification instability

**0 of 11 entries** are classified shared by one review and not the other. 2 of 11 — `A#1` and `B#1`,
one pair — are classified shared by **both**. On the measure Phase 7 waits for, this cycle shows
**no instability at all**: the two reviews partition all eleven entries identically, agree on every
`Same remedy` value, and their two `Summary` blocks are identical line for line.

That is one cycle, and the condition Phase 7 declares is two.

### Instability of `Remedy carried by` — a second axis, first observed here

The classification is stable; **the attribution of the remedy is not.** On the single shared entry
both reviews answer `Same remedy: no`, and then name **different sides**:

- `PLAN-CC-CON-6.REVIEW.md` → `A`, because *«its test is decidable against the artefacts a delivery
  plan is generated from»*, while `B`'s test is conditioned on a designated authority document and,
  where none exists, decides nothing.
- `PLAN-CX-CON-6.REVIEW.md` → `B`, because its *«declared-conflict-to-inventory rule gives a finite,
  decidable chain to check in a generated plan»*.

`workflow/CYCLE.md` § *Cosa il workflow applica da sé e cosa no* says an `intersection-theme` entry is
applied *«con la formulazione del lato che la porta»*. It presumes the two reviews name one side.
They did not, and the workflow had no rule to pick.

**The tie was broken on the criterion the `review` prompt itself states** — *«Detail is not a reason;
being decidable on a generated plan is»* — and on one asymmetry the two reviews' arguments do not
share: `B#1`'s rule fires on *«a designated authority»* naming a conflict. In this scenario that is
`EVALUATION-BRIEF.md`, which is eval machinery; `SKILL.md` is a general skill and defines no such
artifact, so `B`'s wording would put a document the skill cannot assume into the skill, and its test
would be vacuously true wherever that document is absent. `A`'s rule fires on the sources, which the
plan is always generated from. `recidiva` independently pairs **both** entries to `R-010`, whose
claim is already in `A`'s shape.

**This is a judgement the workflow is not supposed to make, and the veto owns it.** `B`'s wording,
verbatim, so that substituting it costs one edit:

> Start reconciliation by copying every conflict declared by the designated authority into the
> inventory as a separate item, retaining every cited side and naming the decision it affects. Then
> sweep the sources for additional conflicts and undecided choices. Before cutting slices, account
> for every copied conflict with a selecting source or an open item, and audit each blocked
> `Includes` and `Verification` bullet for conditional wording.

## Points requiring human reading

Nothing here is applied by the workflow.

**Entries the filter does not license** — nine, all unilateral. None breaks the hard rule of
bidirectional `improve`: the one `addition` in the corpus, `B#7`, declares `Clause: none`, so no
discarded reformulation was owed.

- `A#2` — a `Learning / risk` claim states a rate or hit-rate that no `Verification` bullet of the
  same slice measures — **why it is not applied:** shared by neither review — **what to check on the
  plan:** `PLAN-CX-CON-6.md:182` against `:176-178`, and `PLAN-CC-CON-6.md:162` against `:155-158`.
  Manifested by both candidates.
- `A#3` — a `Decision checkpoints` entry names evidence the slice it follows does not produce —
  **why it is not applied:** shared by neither review — **what to check on the plan:**
  `PLAN-CX-CON-6.md:342` against slice 8's `Verification`; `PLAN-CC-CON-6.md:325` against slice 5's.
  Manifested by both candidates.
- `A#4` — a published spike carries no time box and no enabled decision — **why it is not applied:**
  shared by neither review — **what to check on the plan:** `PLAN-CX-CON-6.md:347-349`. `CC`
  publishes no spike, so this is a one-sided defect.
- `B#2` — an open entry's blocked-slice list is over-inclusive in one plan and under-inclusive in the
  other — **why it is not applied:** shared by neither review — **what to check on the plan:**
  `PLAN-CX-CON-6.md:354` against slices 9–11; `PLAN-CC-CON-6.md:333` against slices 5 and 7. This is
  the entry `recidiva` pairs to `R-002`, one of the four rows the instruments could not decide.
- `B#3` — a theme's `First validation` precedes the slice that completes its stated outcome — **why
  it is not applied:** shared by neither review — **what to check on the plan:**
  `PLAN-CC-CON-6.md:20` against slices 5 and 6. Paired to `R-008` by `recidiva`, which is also
  undecided.
- `B#4` — a source-defined correction path arrives after the first behaviour that can require it —
  **why it is not applied:** shared by neither review — **what to check on the plan:**
  `PLAN-CC-CON-6.md:148-166` against `:190-208`.
- `B#5` — a shared adapter is opened early and reopened after intervening themes — **why it is not
  applied:** shared by neither review — **what to check on the plan:** `PLAN-CX-CON-6.md:172` against
  `:256`. Paired to `R-006`, and it contradicts both verdicts on that row: see *Recidiva*.
- `B#6` — identity precedes the differentiator without a hard-dependency exception — **why it is not
  applied:** shared by neither review — **what to check on the plan:** `PLAN-CX-CON-6.md:78`.
  Corroborates the unanimous `R-001` regression.
- `B#7` — downstream consumers invoke an earlier shared capability without declaring reuse — **why it
  is not applied:** shared by neither review — **what to check on the plan:**
  `PLAN-CX-CON-6.md:171`, `PLAN-CC-CON-6.md:151` and `:197`. **This is the entry to read first**: it
  is the only `addition` of the cycle, and the rule it proposes is the one `R-015` predicts and
  `support/CLAUSE-ROW-MAP.md` records as an `unresolved` anchor. `R-015` was falsified unanimously
  this cycle *because the skill never states it*. Applying `B#7` is one of the two moves Fase 4 owes
  on that anchor.

**Rows the cycle could not decide** — four, all from instrument disagreement. Both citations resolve
in every case, so none of these is a discarded verdict; they are two readings of the same text.

- `R-002` on `CC` — `CC` reads `holds` (`Open questions`, entry «Provider Postgres e driver»: it
  *«still names slice 1»*), `CX` reads `falsified` (`PLAN-CC-CON-6.md:330-332`: it names slice 1 then
  *«ogni verifica di connessione successiva»* instead of naming those slices). The disagreement is
  about whether an open entry may name its blocked set partly in prose. `recidiva` sides with `CX`
  via `B#2`.
- `R-004` on both plans — `CC` reads `holds` on both, `CX` reads `falsified` on both, on the same
  behaviour: rejecting a reused invitation token (`PLAN-CX-CON-6.md:279-282`,
  `PLAN-CC-CON-6.md:262-266`). The question is whether a security invariant on a requested capability
  is *«a behaviour the sources do not request»*. The brief is silent on invitation tokens, which is
  why two readings survive.
- `R-008` on `CX` — same evidence, opposite verdict: theme A *«Una persona accede e opera solo nel
  ricettario corrente»* against slice 2's `Outcome` at `PLAN-CX-CON-6.md:95`. `CC` reads the two
  halves as covered, `CX` reads the promise as narrower than the theme.
- `R-009` on `CC` — `CC` reads `falsified` at `PLAN-CC-CON-6.md:229`, slice 8's `Outcome` naming no
  audience before identity at slice 9; `CX` reads `holds` from `PLAN-CC-CON-6.md:8-12`, the
  `Ordering criteria` declaration that all pre-identity evidence is for developers or testers. The
  disagreement is methodological — a per-slice check against a plan-level declaration — and it is
  the one of the four where the two instruments were not looking at the same object.

**Two more points for the veto**

- The wording of the one applied entry: *Classification instability*, above.
- `R-015`'s regression, which Fase 4 owns: *Rewritten formulations*, below.

## Discard log

Step 4, one attempt per entry, no regeneration. **The cycle's own `improve` outputs — S2b — produced
zero discards:** `REPORT-A` 4 conforming of 4, `REPORT-B` 7 of 7. Re-run at step 9 with
`validate_improvement.py --json`, still 4/4 and 7/7, `document_errors` empty.

| Report | Entry | Field | Reason |
|---|---|---|---|
| — | — | — | none |

**The discarded first attempt, counted apart.** The `improve` calls of S2 were discarded whole and
their outputs kept under `recipe-app/payloads/CON-6/discarded/attempt-1/`. They are **not** part of
the counter above, because they measure a defect of the payload the two models read, not the models:

| Report | Entry | Field | Reason |
|---|---|---|---|
| `B` | 1 | `Existing rule that failed to prevent the defect` | ``` `Clause` must name its section as § `section title` ``` |
| `B` | 2 | `Existing rule that failed to prevent the defect` | idem |
| `B` | 3 | `Existing rule that failed to prevent the defect` | idem |

`REPORT-A` was 5 of 5 in that attempt. `CLAUSE-INDEX.md` printed the numbered headings as `## § 1 …`
while `assets/improvement-template.md` asks for `§ ` plus the title as the field's marker, so the
conforming form was a doubled `§`: one side wrote it, the other absorbed the marker into the title
and fell whole. Re-run at step 9 against the corrected tooling, `attempt-1`'s `REPORT-A` is still
5/5 and its `REPORT-B` still 0/3 — the artifacts carry the defect, and the correction was in the
payload, not in them.

**The distribution is the diagnosis.** Both discard sets are concentrated on **one field**, which by
`CONSENSUS-WORKFLOW-PLAN.md` § Fase 2 accuses the template — or, as it turned out twice, the tooling
that renders the template's inputs — and never the model. No discard was spread across fields, so
**the specificity hypothesis takes no `×1` disproof from this cycle**.

### What the gate counts are not evidence of

**`4` against `7` is not clean comparative specificity, and must not be quoted as if it were.**

The gate was corrected **twice inside S2**, and the second correction was decided **at known result**
— knowing which side was falling:

1. `CLAUSE-INDEX.md`, in the payload, printed section headings in a form the template's field marker
   made unconforming. Corrected before S2b, on both sides symmetrically.
2. `LINE_REFERENCE_PATTERN` in the validator accepted one span per `Evidence` cell. `CX` cites sets
   of sites in one cell as its constant convention — 10 of its 10 direct references, against 0 of
   `CC`'s 7 — so `REPORT-B` fell 0 of 7 on a restriction that lived only in the check and never in
   the template. The fix resolves **every** span, which tightens the gate rather than loosening it,
   and the artifacts revalidated unchanged because nothing the models read had changed.

So the `7` of `REPORT-B` was read under a rule made explicit **after** those entries were written,
and the `4` of `REPORT-A` was not affected by either correction. What the cycle supports is the weak
claim: **both sides produce entries that are anchored, localizable and conforming.** It does not
support any statement about *how much* more specific one side is than the other, and the two numbers
are not comparable as a ratio. Nothing about the specificity hypothesis is decided by them.

A third figure belongs here for the same reason: **eleven provider calls were spent, not nine.**

**Discarded verdicts** — **none**. All 68 verdicts (17 rows × 2 candidates × 2 instruments) carry a
citation, and every citation resolves against the plan it judges: line references land inside the
section they claim, `slice N Field` references name a slice the plan has and a field it carries,
and section-and-entry references quote text present verbatim. Checked one by one at step 9.

| Row | Candidate | Citation as written | Why it does not resolve |
|---|---|---|---|
| — | — | — | none |

The discard rate is the thermometer of dilution; at seventeen rows per execution it reads zero.

## Verdicts

Four verdicts per row, never aggregated: two instruments × two candidates. `CC` is `claude-opus-5`,
`CX` is `gpt-5.6-sol`, both at `high`. `Resulting state` applies the rule declared in *What produced
the verdicts*. All 17 rows are active; **zero are dormant**, so the 1-cycle-in-3 rule does not bite.

| Row | Candidate A (`CC` / `CX`) | Candidate B (`CC` / `CX`) | Resulting state | Watch for |
|---|---|---|---|---|
| `R-001` | `falsified` / `falsified` | `holds` / `holds` | **regressed on `CX`** (2026-08-07) | no note on this row |
| `R-002` | `holds` / `holds` | `holds` / **`falsified`** | undecided — instruments disagree; `not falsified ×0` held | no note on this row |
| `R-003` | `holds` / `holds` | `holds` / `holds` | `not falsified ×1` | no note on this row |
| `R-004` | `holds` / **`falsified`** | `holds` / **`falsified`** | undecided — instruments disagree; `not falsified ×1` held | no note on this row |
| `R-005` | `holds` / `holds` | `holds` / `holds` | `not falsified ×2` | no note on this row |
| `R-006` | `holds` / `holds` | `holds` / `holds` | `not falsified ×1` held — `recidiva` contradicts | no note on this row |
| `R-007` | `holds` / `holds` | `holds` / `holds` | `not falsified ×2` | no note on this row |
| `R-008` | `holds` / **`falsified`** | `holds` / `holds` | undecided — instruments disagree; `regressed` (CON-5) held | no note on this row |
| `R-009` | `holds` / `holds` | **`falsified`** / `holds` | undecided — instruments disagree; `not falsified ×1` held | no note on this row |
| `R-010` | `holds` / `holds` | `holds` / `holds` | `not falsified ×0` — re-anchored, see below | `not observed` (both) — the over-deferral failure did not appear; both plans keep the observable result asserted while deferring the mechanism |
| `R-011` | `holds` / `holds` | `holds` / `holds` | `not falsified ×1` | `not observed` (both) — no `*(Developer outcome)*` marker in either `Themes` table, so the escape hatch was not used |
| `R-012` | `holds` / `holds` | `holds` / `holds` | `not falsified ×2` | no note on this row |
| `R-013` | `holds` / `holds` | `holds` / `holds` | `not falsified ×2` | no note on this row |
| `R-014` | `holds` / `holds` | `holds` / `holds` | `not falsified ×2` | no note on this row |
| `R-015` | `falsified` / `falsified` | `falsified` / `falsified` | **regressed on `CC` and `CX`** (2026-08-07) | no note on this row |
| `R-016` | `falsified` / `falsified` | `holds` / `holds` | **regressed on `CX`** (2026-08-07) | both instruments report the early-opening exception exercised for the embedding pipeline, resolving to the brief's `Accepted alternatives` and not to `SKILL.md` |
| `R-017` | `holds` / `holds` | `holds` / `holds` | `not falsified ×2` | no note on this row |

Candidate A is `PLAN-CX-CON-6.md`, candidate B is `PLAN-CC-CON-6.md` — the mapping lives in
`support/AGENT-PLAN-MAP.md` and is restated here only because the cycle is over and the report cites
real artifacts.

**`R-010` was re-measured by the application itself.** Both instruments read `holds` on both plans
against `28b5460`, and then this cycle's applied entry reformulated the very clause the row is
anchored to. Per `REGRESSION-LEDGER.md` § *Re-anchoring and absorption* the counter restarts at `×0`
against `550077f`: the CON-6 measurement was real and is deliberately discarded, because it
measured a text that no longer exists. The verdict is trustworthy; it is simply
no longer about the text the row now declares.

**The four undecided rows are not `row-defect`.** No instrument returned `row-defect` on any row
this cycle. All four disagreements are two readings of a decidable claim, which is a different
failure from a claim that cannot be decided — and it is the failure the two-instrument design
produces and never named.

## Regressions detected

Three rows, all against `28b5460`. A regressed row is not deleted; the correction row is added and
both are kept.

- **`R-001`, on `CX`** — `PLAN-CX-CON-6.md:78`: slice 2 is *«Accesso al primo ricettario privato»*
  with `Includes` *«Login e sessione con Auth.js v5 e Google OAuth»*, while the differentiator the
  brief declares — multilingual semantic search — is validated at slices 3 and 4. Identity precedes
  the differentiator. Unanimous on both instruments. `PLAN-CC-CON-6.md` holds, placing identity at
  slice 9 and declaring the ordering under `Ordering criteria`. `improve` raised the same defect
  independently as `B#6`, and `recidiva` paired it to this row: the ledger, the verdicts and the
  improvement reports agree.
- **`R-016`, on `CX`** — `PLAN-CX-CON-6.md:194`: slice 7 opens the LLM extraction adapter, but the
  paste path that feeds it arrives at slice 8 (`:218`). The opener does not follow every `NOW` slice
  that feeds it, and the exception does not apply: slice 7 validates real pages, not controlled
  inputs. Unanimous. `PLAN-CC-CON-6.md` holds, opening the extractor at slice 6 after both feeders.
- **`R-015`, on `CC` and `CX`** — the only row falsified on **both** plans by **both** instruments.
  `PLAN-CX-CON-6.md:171` and `PLAN-CC-CON-6.md:151` both consume the embedding pipeline opened at
  slice 3 with no reuse declaration. It is a real defect of both artifacts — and it is **not** a
  regression of the skill. See *Rewritten formulations*.

## Rewritten formulations

- **`R-015` — the row predicts a rule `SKILL.md` does not state; falsified unanimously, and the
  falsification is not a skill regression.** Its own `Watch for` cell said so before the cycle ran:
  the reuse requirement was added to the parent row after CON-5 *because* `CX` never declared reuse,
  and `support/CLAUSE-ROW-MAP.md` records the anchor as `unresolved` — no clause of the skill
  requires it. A row that predicts what the skill never says cannot be falsified by a plan that
  follows the skill.
  **The row is not rewritten by this cycle, deliberately.** It is not one of the three cases
  `REGRESSION-LEDGER.md` § *Authority and rewritten formulations* covers: the claim is decidable, it
  needs no choice between two readings, and it contradicts nothing in `Accepted alternatives`. The
  defect is the **missing clause**, and Fase 4 already owns that decision — *«lo skill acquista la
  clausola che la riga presuppone, oppure la riga si riscrive per smettere di pretendere ciò che lo
  skill non dice»*. CON-6 supplies what Fase 4 was waiting for: the anchor is now falsified on both
  plans by both instruments, and `B#7` proposes the exact clause, with its own binary test, as the
  cycle's only `addition`. The row stays `regressed` until Fase 4 chooses.
  The `Watch for` note that predicted this **did not enter the `verdetto` payload** — S3 withheld it
  because it names a harness and would have broken blindness. The four verdicts were therefore
  produced without it, which is why they read the row straight and got it right.

## Diagnoses decided

Two of the three regressions produce a diagnosis; one does not, and saying so is the point.

- **`R-001` on `CX` — diagnosis, seat named, no rule added.** The clause is `SKILL.md:261-268`
  § `4 Assign horizons and order for learning`, the ordering list whose second item is *«differentiating
  value and existential business risk»* — identity is none of the six. `B#6` locates the same seat
  and proposes reading the list as **precedence after hard dependencies**, with an exception stated
  once under `Ordering criteria` when identity really is a hard dependency. Falsifiable prediction:
  *«make the list a precedence and require the exception to be declared, and a plan does not put
  identity before the differentiator's first validator without saying why»*. **No rule is added by
  this cycle**: `B#6` is unilateral, the seat is a clause that arguably already forbids the case, and
  a second textual prohibition next to a list that was not read as a list is the move
  `workflow/LEDGER.md` names as the one that has already failed.
- **`R-016` on `CX` — no diagnosis, and this is not an omission.** The defect is an ordering error on
  a clause that states the rule exactly (`SKILL.md:284-286`, *«a slice that opens a pipeline or
  adapter shared by several paths follows every `NOW` slice that feeds it, and owns it alone»*), and
  the plan violates it while `PLAN-CC-CON-6.md` follows it and even restates it in its own
  `Ordering criteria`. A diagnosis whose seat is a clause that already forbids the case ends here
  with **no rule added**.
- **`R-015` — the diagnosis is the missing clause itself**, and it belongs to Fase 4. See above.

## Corrections applied after the cycle

**None.** No change was made to `SKILL.md` outside the automatic application of `A#1`/`B#1`. The
three regressions produced no correction: `R-001`'s and `R-016`'s seats are clauses that already
state the rule, and `R-015`'s correction is a Fase 4 decision on an `unresolved` anchor.

`SKILL.md` therefore differs from `28b5460` by exactly one hunk, `+6/-2`, committed as `550077f`.

## Recidiva

One execution, `claude-opus-5` at `high`, on `CC`. **7 pairs over 11 entries.** Every entry of both
reports appears exactly once, as a pair or under the entries with no row; the two report sizes and
the row count in its `Inputs` block match the artifacts.

| Entry | Row | Why the defect falsifies the claim | Other rows considered |
|---|---|---|---|
| `A#1` | `R-010` | an `Includes` bullet asserts one side of a conflict the brief lists under `Known conflicts`, with no deferring wording and no open entry | `R-003` — names no external component; `R-002` — the behaviour is never declared open |
| `B#1` | `R-010` | slice wording specifies one interpretation of an authority-declared conflict with no selecting source cited | `R-002` — the conflict is never declared open; `R-003` — restricted to external component choices |
| `B#2` | `R-002` | a choice **is** declared open and its published blocked list omits `NOW` slices the answer blocks | `R-003` — implicated, but the fault is in what the declaration names |
| `B#3` | `R-008` | a `First validation` points at a slice that treats as an error a case the unqualified desired outcome promises | `R-011` — the pointer does resolve to a product slice |
| `B#5` | `R-006` | a shared adapter's opening work is split across the `Includes` of separate `NOW` slices | `R-016` — a split cannot be repaired by placement; `R-015` — the second slice reopens rather than reuses |
| `B#6` | `R-001` | identity is delivered in an earlier slice than the differentiator's enabler and product validation | `R-017` — antecedent never arises; `R-009` — almost nothing precedes identity |
| `B#7` | `R-015` | `NOW` slices consume a pipeline an earlier slice opened with no reuse declaration in their `Includes` | `R-006` — the pipeline is opened once; `R-016` — the opener's position is not examined |

**Entries with no row:** `A#2` — an unmeasured `Learning / risk` rate; `A#3` — a `Decision
checkpoints` entry whose evidence the preceding slice does not produce; `A#4` — a spike with neither
a time box nor an enabled decision; `B#4` — a source-defined correction path arriving after the
first behaviour that creates the state.

**Rows woken up:** none. There are no dormant rows.

**Four of the seven pairs corroborate a verdict; one contradicts both.** `B#6`→`R-001` and
`B#7`→`R-015` land on rows the verdicts falsified unanimously, and `A#1`/`B#1`→`R-010` land on the
row the applied entry re-anchors. `B#2`→`R-002` and `B#3`→`R-008` land on two of the four rows the
instruments could not decide, and side with `CX` in both.

**`B#5` → `R-006` is the one to reread.** Both `verdetto` instruments read `R-006` as `holds` on
both plans, and `PLAN-CC-CON-6.VERDICTS.md` addresses this exact point explicitly — *«the R2 photo
path is first opened in slice 6 `Includes` and extended, not re-opened, by slice 10»* — while
`recidiva` reads the same two slices of `PLAN-CX-CON-6.md` (`:172` and `:256`) as a split opening.
The row is therefore **held at `not falsified ×1` and not advanced to `×2`**: a cycle in which the
detector's own two mechanisms contradict each other has not confirmed the row. This is not resolved
by majority — `workflow/LEDGER.md` is explicit that `recidiva` is a thermometer and that applying
*«regge solo se regge su entrambi»* to it would maximise false positives. It goes to the veto.

A pairing is evidence, not an oversight: both reports were written with `LEDGER-CLAIMS.md` in front
of them, so a pair is a defect raised **despite** the claim being visible. Seven of eleven entries
land on a row the ledger declares live — the ratio is high enough to be the finding of this section
in its own right, on a ledger that covers 40 clauses out of 205.

## Artifact defects with no row

Real defects of the generated plans that no ledger row had recorded. They are **not** regressions,
and the artifacts are not modified.

- **Unmeasured `Learning / risk` claims, both plans.** `PLAN-CX-CON-6.md:182` promises *«hit-rate,
  durata e affidabilità»* and `PLAN-CC-CON-6.md:162` *«l'hit-rate reale del JSON-LD»*, while both
  slices' `Verification` blocks hold one success case and a list of handled failures. Measured on the
  plans alone. Not attributable to an existing row: no row quantifies over `Learning / risk`.
- **Checkpoints without producing evidence, both plans.** `PLAN-CX-CON-6.md:342` and
  `PLAN-CC-CON-6.md:325` name coverage and hit-rate evidence their preceding slices do not state.
  Measured on the plans alone; no row quantifies over `Decision checkpoints`.
- **Spikes with no time box, `CX` only.** All three `Non-product work` entries at
  `PLAN-CX-CON-6.md:347-349` state an activity and an exit and no time box; `:348` states no enabled
  decision. `CC` publishes no spike. Measured on the plan alone; no row quantifies over spike fields.
- **Correction path after its producer, `CC` only.** Slice 5 saves extracted content without review
  and edit arrives at slice 7. Measured on the plan and the brief, whose *«edit is the recovery
  path»* constraint the ordering does not contradict outright — which is why this is an observation
  and not a regression.

These four are exactly `recidiva`'s *entries with no row*, arrived at independently: the phase that
pairs entries to rows and the phase that reads the plans agree on what the ledger does not cover.

## Deviations from the procedure

Ten, and none silent.

1. **Eleven provider calls instead of nine.** The two `improve` calls of S2 were discarded at the
   gate for a payload defect and repeated as S2b, with its own authorization. The count belongs in
   the record because `CONSENSUS-WORKFLOW.md` publishes nine per cycle as the price of the tool.
2. **Generation ran at `medium`, not the `high` declared before the calls.** Both sides,
   symmetrically. Sanated by correcting the two `support/AGENT-PLAN-MAP.md` cells and splitting the
   effort decision into two variables, not by regenerating. The consequence carried forward: a
   `falsified` verdict measured on these plans is ambiguous between skill and effort and must be read
   with the `gen` slot; a `not falsified` one is not, because lower effort is a harder condition.
3. **Four tooling corrections inside one cycle**, three at S2 and one at S3. Two were decided at
   known result — the `Evidence` reference pattern, and the `CLAUSE-INDEX.md` heading form. Their
   consequence for the counters is *What the gate counts are not evidence of*.
4. **The `verdetto` phase has two instruments and no combination rule.** The gap is structural, not
   an execution error: `CONSENSUS-WORKFLOW.md` has always specified two executions and no document
   says what a disagreement produces. Resolved here by `CONSENSUS-WORKFLOW.md` § *Vocabolario*, and
   the rule is now written into `workflow/LEDGER.md` and `prompts/verdict.prompt.md` so the next
   cycle does not re-derive it.
5. **The applied entry declares `reformulation` while its `Change` extends the clause's reach.** By
   `assets/improvement-template.md`'s own taxonomy that is a `reach-change`, which would have
   required a `Merged claim` the entry does not carry. The gate is structural and cannot tell the
   two apart from the text. Applied as declared — hunk plus re-anchoring of `R-010` — **plus** one
   new row for the limb no active row predicted, because the alternative is a rule entering
   `SKILL.md` with nothing able to falsify it. `assets/improvement-template.md` and
   `workflow/CYCLE.md` now state this case; the choice is the veto's to reverse.
6. **The two `REVIEW`s name different sides in `Remedy carried by`.** `workflow/CYCLE.md` presumed
   they would agree. Tie broken on the `review` prompt's own criterion, with `B`'s wording published
   verbatim above so the veto can substitute it. `workflow/CYCLE.md` now names the case.
7. **The seven cycle artifacts moved to `recipe-app/results/`.** They were **already tracked and
   committed** under `recipe-app/payloads/CON-6/out*/` — `7fcfb7d`, `12cead3`, `f7de09c`, `338f3e6` —
   contrary to the assumption that they were untracked, so this step is a rename, not a first
   commit. The convention is CON-4's and the map already names them this way. The reason is not
   tidiness: a payload directory is composed from an allowlist, and leaving a cycle's outputs inside
   that tree means the next composition has to exclude them **by name** instead of by construction.
   The payload directories themselves stay: they are the record of what each execution could read.
8. **`assets/report-template.md` corrected in ten places** while writing its first instance, per the
   standing rule that a template failure is fixed in the template, not worked around in the report:
   the four-verdict `Verdicts` table with its citation policy and its `row-defect` distinction; the
   *What produced the verdicts* section made mandatory for a two-instrument `verdetto`; the second
   axis under *Classification instability*; the new *What the gate counts are not evidence of*
   section; the discarded-attempt table under *Discard log*; the two new counters and their
   derivations; the note that `entries applied` does not bound `new ledger rows`; the `Remedy` and
   `Ledger row` fields of *Entries applied*, with the paragraph on which row a reformulation is owed;
   the *Recidiva* rule for a pair that contradicts a verdict; and the artifact location under
   *Inputs*. Four sibling documents took the consequences: `assets/improvement-template.md`,
   `workflow/CYCLE.md`, `workflow/LEDGER.md`, `prompts/verdict.prompt.md`, plus steps 6, 8 and 9 of
   `CONSENSUS-WORKFLOW.md` § *Il ciclo*.
9. **Two `Watch for` cells entered the `verdetto` payload as a projection, not a copy.** `R-010`
   without the sentence naming a harness, `R-016` without its pointer to `support/`, `R-015` not at
   all. Decided at S3 at unknown result and recorded there. It changed what two of the five
   executions read, and in `R-015`'s case it is why the verdict was reached straight.
10. **No commit was made by the application step**, and the veto was exercised afterwards.
    `SKILL.md` and `REGRESSION-LEDGER.md` were left modified in the working tree with `R-018` and
    the re-anchored `R-010` both carrying `Commit SKILL.md: (pending)`; the artifacts and this
    report were committed separately as the cycle's record, which is a different commit from the one
    the workflow does not make. The human veto then accepted the batch on 2026-08-07: `SKILL.md` is
    `550077f`, and the two `(pending)` cells were resolved to it before the ledger was committed —
    the order the `Commit SKILL.md` rule requires, since the id does not exist until the veto.
    **The tie-break on the wording was accepted with the batch**, so `A`'s formulation is what the
    skill now carries; `B`'s stays published above, and reversing it is a normal change from here on,
    not a veto.
