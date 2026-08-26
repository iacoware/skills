# Roadmap skill — refactoring plan 2: remove `Ordering criteria`

A work order to delete the `Ordering criteria` section from the map format, in full, and to re-point
everything that reads it. `ROADMAP-GOAL.md` stays the authority on intent, `CONTEXT.md` on
vocabulary. The first refactoring plan was a different job, finished and its file deleted; this one
does not extend it, and the `D` numbers below are local to this document.

This change comes out of [`PERFORMANCE-OPTIONS.md`](./PERFORMANCE-OPTIONS.md) **S1 — bound the prose
in the two templates**, but it is no longer a bound: measurement showed the section is not too long,
it is not read. Disposable once the work is done.

## The problem

Measured on `recipe-app`, reference against `ROADMAP-CC-3`, characters per item:

| Section | ref | CC-3 | × | items |
|---|---|---|---|---|
| `NOW` row | 152 | 156 | 1.03 | 15 → 11 |
| `LATER` | 80 | 75 | 0.94 | 6 → 12 |
| `OUT-OF-SCOPE` | 201 | 252 | 1.25 | 4 → 8 |
| Ordering criteria | 206 | 318 | **1.54** | 4 → **8** |
| Open questions | 252 | 418 | 1.66 | 3 → 2 |
| Cross-functional | 251 | 455 | 1.81 | 5 → 6 |
| Assumptions | 189 | 358 | 1.89 | 6 → 8 |

CC-3's eight criteria, 2,477 characters:

| # | ch | What it holds |
|---|---|---|
| 1 | 247 | *Minimum delivery path* — item 1 of the skill's own list, restated |
| 2 | 358 | *Differentiator first* — item 3 of the skill's list, plus this map's ranking of it |
| 3 | 269 | correction before the correctable state — specific to this map |
| 4 | 294 | required recovery over breadth — a skill rule, but it names a departure |
| 5 | 622 | identity deferred — a departure, specific to this map |
| 6 | 178 | *Breadth before depth* — which `drawing-the-map.md` says is not up for ranking at all |
| 7 | 346 | shared adapter follows its feeders — specific to this map |
| 8 | 163 | *the release closes* — decides nothing |

**946 characters are the map copying the skill back out.** What is left that only this map could know
is two departures, and the payload licenses exactly two: breadth before depth
(`drawing-the-map.md:161-163`) and identity deferred past the second end-user row (`:190-193`). There
is no third.

## The decision

**D1 — the section goes, in full, departures included.** Not shortened, not folded into `Assumptions`,
not replaced. The author's position, and it governs: *if an order can be changed because no hard edge
forbids it, knowing why it was chosen buys nothing. The author has a taste for how work should be
ordered and exercises it where they can.* The register's order is the proposal; `Depends on` is the
only thing that constrains it; a justification changes neither.

**D2 — `drawing-the-map.md` § *Ordering for learning* stays whole.** It is not a description of the
section. It is the ordering rule the model applies while drawing: the ranked criteria, the four things
not up for ranking, where `NOW` ends. Only the clauses that oblige the map to *publish* the reasoning
are cut. The order the model produces must not change.

**D3 — R-012 and R-013 become checks on the outcome, not on the process.** Their subject today is a
sentence in the artifact; with the section gone they would have nothing to read. Rewritten, they read
the register. The reviewer works harder; the map is unaffected. This is the same move
`EVALUATION-RULES.md` already relies on in R-008, where the clause that caught every real failure
across three runs is the outcome clause, not the recorded-verdict one.

**D4 — nothing replaces it.** A `Decisions log` / `Notable decisions` section was considered and
refused: no membership test (`ROADMAP-GOAL.md:23-25` already dropped decision checkpoints by name, and
*anything of that family gets dropped the same way*), and it would hold at most two entries, in a
document whose stated goal is to fit on one screen.

**D5 — the reference roadmap loses the section too.** `reference-roadmap/roadmap.md` is the oracle a
review judges against and it must be a legal map. `REFERENCE-NOTES.md:45` argues for the section and
goes with it.

### What the argument turned on

The claim that removing it damages the map was made twice and failed twice.

- **«The empty `Depends on` cells depend on it.»** False. `drawing-the-map.md:76-78` defines the hard
  edge on its own terms — *a preferred order is not a hard dependency* — and the register template
  repeats the substitution test without naming the section. Line 105 uses `Ordering criteria` as the
  **tell** for spotting a false edge during review, not as the licence for an absent one. No edge
  moves into `Depends on` when the section goes.
- **«Writing the departure is what forces it to be licensed.»** Weak here, though it held for the
  theme verdicts. The verdict obligation forces an *enumeration* — every adjacent pair, including the
  boundary nobody would have noticed, which is exactly where `foto`/`ricettario` failed in three runs
  out of three. The departure obligation is conditional and forces no examination: the departure
  happens under ordering pressure and the sentence follows it. All three runs and the reference defer
  identity to the same place (`S7`, `S6` in the reference), with no variation to attribute to the
  writing.

**The counterfactual is untested and this plan says so.** The section is mandatory in the validator,
so all three runs in `results/` wrote one. Nothing on disk can confirm or deny that removing it leaves
the order unchanged. That is what the run in S4 below is for.

## What changes

### `skills/roadmap`

| File | Line | Change |
|---|---|---|
| `assets/roadmap-template.md` | 48 | delete the section |
| `references/drawing-the-map.md` | 86 | *the sequence belongs to `Ordering criteria`* → *the sequence is order, not dependency* |
| | 100-101 | *what stays unpublished is the reasoning behind the order: `Ordering criteria` states the rules once* → the order's reasoning is unpublished entirely; the register's order carries it, and a reader is free to take a different one wherever no hard edge forbids it |
| | 103-107 | the published-order tell loses its reference to a criterion: an edge a controlled input or a narrower precursor could stand in for, published because someone preferred that sequence |
| | 144-145 | *`Ordering criteria` is a numbered list because the ranking is itself a decision* → the map ranks these criteria for itself, and the register's order is where the ranking shows |
| | 155-156 | *the criterion that loses says so in itself* — delete; it is about written text only |
| | 163 | *and state the departure once in `Ordering criteria`* → the departure has to be one of the four, and the order is what shows it |
| | 192-193 | *justify the remaining deferral once in `Ordering criteria`, naming the evidence* → the rows producing that evidence come before identity in the register |
| | 263-264 | checklist: strike *no edge restates a reason `Ordering criteria` already gives*; the substitution test in the same bullet carries it |
| | 266-267 | checklist: → every departure from breadth is one of the four the skill licenses |
| | 268-269 | checklist: → identity deferred past the second end-user row is preceded by the rows producing its evidence |
| `SKILL.md` | 46 | drop `Ordering criteria` from the list of what to read |
| `scripts/validate_roadmap.ts` | 14, 20 | remove from `ROADMAP_SECTIONS` and `LIST_ONLY_SECTIONS` |
| `scripts/validate_roadmap.test.ts` | 256 | remove the section from the fixture |

`validate_roadmap.shape.test.ts` needs no edit: it derives from the exported `SHAPE`, so template and
validator stay pinned to each other automatically.

### `evals/roadmap`

| File | Line | Change |
|---|---|---|
| `EVALUATION-RULES.md` | 48 | R-003: *`Goal`, themes and `Ordering criteria` untouched* → `Goal` and themes untouched |
| | 94-96 | R-012, rewritten — below |
| | 100-101 | R-013, last sentence rewritten — below |
| | 120 | R-017: strike the clause; rewrite the `⚠ failed` note so published order is spotted by the substitution test |
| `recipe-app/reference-roadmap/roadmap.md` | 67 | delete the section (D5) |
| `recipe-app/REFERENCE-NOTES.md` | 45-47 | delete the paragraph (D5) |
| `recipe-app/fixtures/redrawn/roadmap.md` | 84 | delete the section |
| `recipe-app/fixtures/mid-flight/roadmap.md` | 73 | delete the section |

`recipe-app/results/**` was to be left alone as a historical record. **The author overruled that**:
the three run maps — `ROADMAP-CC-2`, `ROADMAP-CC-3`, `manual-run-1` — lose the section too, so that
every `.roadmap/` on disk is legal under one format and the validator can be pointed at any of them.
What each run wrote survives in git, and in `TRANSCRIPT.jsonl` for the two runs that have one, which
is where the deleted prose is still readable verbatim. `manual-run-1/REVIEW.md` cited the section
twice, and both citations came out because both came out whole: one was a supporting falsification on
an `R-017` finding whose main argument — the controlled input in `S2 Excludes` — stands alone, the
other one item in a list of four on the identity seam. No verdict was reworded, and no other
`REVIEW.md` prose was touched.

### The two rules, rewritten

**R-012, today:** *`Ordering criteria` is a ranked numbered list, and every departure from breadth
before depth is named in the criterion that concedes it rather than left for the reader to notice.*

**R-012, after:** *Once the existential risks are validated the register delivers one thin row per
remaining theme before a second row from one theme, and any departure is one the skill licenses —
another differentiator, a material risk, required recovery, or a materially higher-frequency
behaviour. Read from the rows, never from a statement about them.* `drawing-the-map.md`
*Ordering for learning*.

**R-013, today, last sentence:** *Identity deferred past the second row delivering behaviour to an end
user is justified once in `Ordering criteria`, against named evidence.*

**R-013, after:** *Identity deferred past the second row delivering behaviour to an end user is
preceded in the register by the rows that produce the evidence the deferral rests on.*

The rest of R-013 — the seam under `Cross-functional concerns`, the `Assumptions` line recording what
rows before the seam may ignore — is untouched, and is where the identity decision now lives alone
instead of half here and half in a criterion. `drawing-the-map.md:184` and the deleted `:192` were
splitting one subject across two sections; CC-3 wrote its opening sentence twice, near verbatim, once
in each.

## What must not change

- the order the model produces. D2 exists for this, and S4 measures it;
- § *Ordering for learning* as a drawing rule, in full;
- `Assumptions`, `Open questions`, `Cross-functional concerns`, and the register — this plan touches
  none of them;
- the seven sections that remain, in their current relative order.

## Sessions

| # | Files | Done when |
|---|---|---|
| S1 ✅ | `references/drawing-the-map.md`, `SKILL.md:46`, `assets/roadmap-template.md` | the payload no longer names the section anywhere, and § *Ordering for learning* still carries every ordering rule it carried before |
| S2 ✅ | `scripts/validate_roadmap.ts`, `scripts/validate_roadmap.test.ts` | `make test` green, and a map carrying `## Ordering criteria` now fails the section check |
| S3 ✅ | `EVALUATION-RULES.md`, `reference-roadmap/roadmap.md`, `REFERENCE-NOTES.md`, both fixtures | `make validate-roadmap` clean against each fixture and against the reference; no rule cites an anchor that moved |
| S4 | none — it runs, it does not edit | one drawing run on `recipe-app`, scenario 0, plus its review |

S1 to S3 spend no provider call. **S4 costs two sessions** — one run, one review — and `AGENTS.md`
requires the exact count and explicit approval before either is sent.

## Done when

- `Ordering criteria` survives in no map and in no review on disk, and in prose only where it is
  history: `PERFORMANCE-OPTIONS.md`'s measurements, the two `TRANSCRIPT.jsonl` files, this plan, and
  the one validator test that pins its rejection;
- the drawn register's order matches `ROADMAP-CC-3`'s on the two things the deleted rules governed:
  identity is not earlier than the rows producing the evidence for its deferral, and the one departure
  from breadth is still a licensed one;
- R-012 and R-013 return a verdict readable from the register alone, with no section to quote;
- `make test` and `make validate-roadmap` are clean, and the shape test still pins the template to the
  validator;
- `roadmap.md` for `recipe-app` is ~2,571 characters shorter than CC-3's **was**, and no other section
  grew to absorb it. CC-3's file no longer carries the section, so the baseline is this number and the
  per-section table above, not a diff against the file.

## Not in this plan

Left open from the same S1 discussion, each still measured and unspent:

- **`Assumptions`** — 668 characters, 23% of the section, are a refutation clause (*«cade se…»*) the
  reference never writes. `drawing-the-map.md:235` states *delivery can refute it* as a test the
  drawer runs, not as a sentence the line carries.
- **`Cross-functional concerns`** — every CC-3 bullet is three sentences, every reference bullet one or
  two, and the extra one enumerates the rows a rule touches inside the one section that exists in
  order to name none. ~1,200 characters. Cutting a whole bullet is the one move that *raises* the
  total: `ROADMAP-GOAL.md:93` says the section exists so the eleven slice documents do not each
  restate it.
- **The slice documents** — ~16,400 characters at reference density, across `Verification` (3.5× per
  row), `Includes` (2.9×) and `Excludes` (2.3×). The largest remaining item in S1 by a wide margin.

Already done and committed: the theme-boundary verdict is bounded to one line per boundary with a home
in the template (`ff63c96`), worth ~650 characters.

## What S1 to S3 changed beyond the tables above

Three edits the tables did not foresee, each forced by the deletion:

- `drawing-the-map.md:29` and `EVALUATION-RULES.md` R-018 both listed *the ordering criteria*, in
  lowercase, among what a redraw draws from nothing. Both lost the item; neither table caught them
  because neither spells the section in title case.
- `fixtures/validator/missing-section.json` removed the `## Assumptions` heading to prove the section
  check fires. With `Ordering criteria` gone, `Assumptions`' bullets fall into `OUT-OF-SCOPE`, which
  forbids ids, and the fixture raised a second error the test refuses. It now removes
  `## Open questions` instead, whose bullets fall into `Assumptions`, where ids are legal.
- One test was added, not just edited: a map still carrying `## Ordering criteria` is rejected as a
  section the roadmap does not have. That is the answer to the open question below, pinned.

## Answered

- **Deprecated or deleted, for a map already on disk?** Deleted. The validator rejects the section
  with the message it already has for an unknown one, and `SKILL.md` § *Operations on the map* gains
  one paragraph telling a `Revising` session to delete it with the rest of the block. No tolerance
  branch, so nothing to remove later.

## Open questions

- **S4 has not run.** It costs two provider calls — one drawing run on `recipe-app` scenario 0, one
  review — and `AGENTS.md` requires explicit approval before either is sent. Until it does, the
  counterfactual this plan rests on stays untested: nothing on disk shows whether the order survives
  the section's removal.
