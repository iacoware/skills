# Making the drawing faster

Options for cutting the wall-clock of a `Drawing` session, and secondarily the tokens in the main
context window. Nothing here is implemented. [`ROADMAP-GOAL.md`](./ROADMAP-GOAL.md) stays the
authority on what the tool must not become, and no option below buys time with a new field, a
gradient of detail, or a number nothing can check.

The evidence is `recipe-app/results/ROADMAP-CC-3` and `ROADMAP-CC-2`, profiled from
`TRANSCRIPT.jsonl` rather than read off `METRICS.md` — see *What the metrics say and what they get
wrong* below.

## What the evidence actually says

**One equation explains the whole run: wall-clock = output tokens ÷ ~72 per second.**

CC-3 spent 803s of active time across 16 provider requests, generating 58,147 output tokens — 72
tok/s. CC-2 spent 742s generating 51,594 — 70 tok/s. The rate holds per call on every call large enough for
time-to-first-token not to dominate: 69.5, 71.4, 72.8, 76.4, 80.8 tok/s on the five calls over 70s.

Everything else is noise:

- **Tool execution across the whole of CC-3 is 2 seconds.** Every `cat`, every `sed`, every heredoc
  that writes twelve files, the validator run: two seconds of 803.
- **Input costs no wall-clock.** Cache read grows from 29,572 to 134,291 tokens across the run and
  never shows up in a duration.

So there are exactly two levers: **emit fewer tokens, or emit them in parallel.** Both compress at
the same rate per token, which is what makes them comparable in the tables below.

### Where CC-3's 803 seconds go

`METRICS.md` § *Dove va il tempo* now carries this, computed rather than estimated: each request's
measured seconds divide between its thinking and its work in the same proportion as its tokens, and
the rows add up to the active time.

| Phase | CC-3 | CC-2 |
|---|---|---|
| Thinking | **8m 14s · 61%** | 5m 39s · 46% |
| Writing the documents | **4m 24s · 33%** | 5m 46s · 47% |
| Reading | 23s · 3% | 28s · 4% |
| Validating | 3s · 0% | 3s · 0% |
| Talking to the author | 15s · 2% | 17s · 2% |
| Other | 3s · 0% | 6s · 1% |
| Tool, sub-agent and I/O | **2s · 0%** | 3s · 0% |

The two runs disagree on the split between thinking and writing — 61/33 against 46/47 — and agree on
everything else: the two together are 93–94%, reading is 3–4%, and **everything that is not the model
generating tokens is two seconds.**

### Corrections to the profile in the prompt

- **16 provider calls, not 32.** `METRICS.md` counts assistant *entries*; a single request produces
  one entry per content block. Grouping by `requestId` halves the count.
- **The six slowest calls are 761s of 801 (95%)**, which confirms the shape of the claim. Their
  composition is different from the one in the prompt.
- **No call is pure thinking.** The 275s call (19,014 thinking tokens) is the one that emitted
  `sed -n 1,200p scripts/validate_roadmap.ts`; the 72s call (5,060 thinking) emitted `mkdir -p`. The
  thinking is the map being designed, riding along with whatever cheap tool call the turn happened to
  make. Attributing 275s to reading the validator reads the transcript backwards.
- **The 146s call does not exist in CC-3.** CC-2 has 157s and 179s; CC-3 has 275s, 218s and 72s.
- **All the reading in the run is 23 seconds of 803.** The validator source is 4.6s of it, in two
  calls of 119 output tokens each; the four sources are 5.6s; both references and both templates are
  5.2s. The premise that *before writing a line the session loads ~54k characters* is true and worth
  3% — a main-context token cost, which is the secondary goal, and close to free on the primary one.
- **Cap and floor were already answered before the validator was read.** Call 6 greps
  `cap|floor|WARNING|MAX|MIN_` and `REGISTER_FLOOR = 3` / `REGISTER_CAP = 20` sit at lines 74–75, so
  the grep returned them. The 600 lines read afterwards were reverse-engineering *what the validator
  checks*, which the payload states only in part. That is still a real defect — see **S2** — but it is
  a different one.
- **Thinking is 60% of output, not 65%**, and 34,859 tokens rather than 84,869. The qualitative claim
  survives; the number does not.

### The lever the prompt does not name: the map is written at two to three times the density of the reference

`reference-roadmap/` is the oracle this eval judges against, and it is far shorter than what the runs
produce.

| | reference | CC-3 | CC-2 |
|---|---|---|---|
| `roadmap.md` | 8,901 chars | 16,786 (1.9×) | 15,900 (1.8×) |
| rows | 15 | 11 | 12 |
| slice documents, total | 17,502 chars | 29,317 | 38,038 |
| **per row** | **1,167 chars** | **2,665 (2.3×)** | **3,170 (2.7×)** |

Section by section, `roadmap.md` against the reference: Themes 3.1×, Ordering criteria 3.1×,
Assumptions 2.5×, `OUT-OF-SCOPE` 2.5×, Cross-functional concerns 2.2×, `LATER` 1.9×. Inside the slice
documents: `Verification` 3.5× per row, `Includes` 2.9×, `Excludes` 2.3×.

**The one section that did not grow is the register** — the only one that is a table. Every prose
section did.

What that looks like, on the same row in both maps:

> **Reference, `S4` Verification.** Cercando «cena leggera» compaiono ricette che quelle parole non le
> contengono; cercando «pomodoro» compare una ricetta scritta in inglese, senza che nulla sia stato
> tradotto.

> **CC-3, `S4` Verification.** Five clauses: the cross-language demonstration, then measured recall
> against the spike's, then *una ricetta di un altro ricettario non compare mai fra i risultati* —
> which is the scoping invariant that belongs under `Cross-functional concerns` — then a p95 latency
> figure, then re-indexing on edit.

Two of those five restate things the format states once elsewhere. This is the ceremony
`ROADMAP-GOAL.md` refuses, and it is 19,700 characters of it across the map: **≈5,800 output tokens,
≈80 seconds**, before counting the thinking that produced them. It is also a live goal violation —
*visible because the overview fits on one screen*, and 16,786 characters does not.

### One observation on whether the thinking is buying anything

CC-3 wrote its first five slices in a call carrying 9,789 thinking tokens, and its last six in a call
carrying **zero**. `REVIEW.md` finds three of its seven violations in the first batch (`S0`, `S3`,
`S4`) and one in the second (`S6`). That does not prove the thinking is wasted — the 19,014-token
design think preceding both is shared — but nothing in the run supports paying 9,789 tokens for the
second half of the documents either.

---

## Bold options

Ordered by saving over risk.

### B1 — Fan out the row documents to subagents · **accepted**

Once the register, the themes and the edges are fixed, the eleven documents are independent. Main
context fixes the map, dispatches one subagent per row, writes nothing per row itself.

**Files.** `SKILL.md` § *Draw the map* gains a paragraph on delegation and the propagation clause;
the input contract goes into `references/drawing-the-map.md`, next to what already decides the map's
shape. No new payload file — the contract is a list of things main context has already decided, not
new rules.

**Saving.** Of the 4m 24s in *Writing the documents*, 2m 46s is the two calls that wrote the eleven
row documents (12,677 non-thinking output tokens: 5,774 for five rows, 6,903 for six), and a
conservative half of call 12's 9,789 thinking tokens is per-row detail, ≈68s. Total **≈235s**. Fanned out, the critical path is the
slowest single row: ~1,200 output tokens plus its own thinking, call it 2,200 tokens ≈ 30s, plus
dispatch. **Saving 120–200s**, the floor assuming each subagent thinks about its row roughly as much
as the main session did. Main context also stops carrying the documents: ≈8,400 tokens of slice text
and ≈9,800 of per-row thinking never enter it.

**What must be in the contract**, item by item, because each one is a rule that fan-out would
otherwise break:

1. `id`, title, slug, and the five register columns as main context decided them. The subagent may
   not change one.
2. `Outcome`, one line, fixed upstream — the row's identity.
3. `Learning target`, one line, fixed upstream. Identity follows the learning target through a split
   or a merge (`slice-rules.md` § *Identity*), so it cannot be invented downstream.
4. `Depends on` **in both directions**: the ids this row depends on and the ids that depend on it,
   each with its one-line outcome. Without the reverse edge the subagent cannot write `Excludes`
   honestly.
5. The whole register as id + title + one-line outcome. This is what lets `Excludes` name *where* a
   behaviour went, which is the conservation clause of `slice-rules.md` § *Splitting and merging*.
6. `Cross-functional concerns` verbatim, with the instruction that a row restates none of it — and
   main context naming which row is the first to cross each trust boundary or perform each external
   side effect, since that row and only that row verifies it.
7. The `Assumptions` and map-level `Open questions` lines traced to this id, so that the reading lands
   in a bullet (`drawing-the-map.md`, the *it lands in a row* test).
8. Where the row sits relative to the identity seam: which resolver owns scope at this point in the
   order, and whether the row precedes or follows authenticated identity.
9. `Requested by`, as main context traced it.
10. Two payload paths and no others: `assets/slice-template.md` and `references/slice-rules.md`. Never
    `drawing-the-map.md` — a subagent decides nothing about the map's shape.

**What comes back: the path written, and a `—`-or-lines block of what the subagent could not settle.
Not the document.** Three reasons. The four-part report is read off `roadmap.md` and the register,
never off the row documents (`SKILL.md` § *Close the session*). The validator, which runs after
writing, is precisely the thing that checks the documents cohere with the register. And returning
eleven documents spends the ≈8,400 tokens the fan-out just saved, to re-read what the validator reads
better. The accepted cost: a judgement defect inside one document is invisible in main context — which
is already true today of the six slices written with no thinking, and is what the eval exists for.

**Round trips are unchanged.** Subagents never address the author. Anything a subagent cannot settle
comes back as a line, and main context routes it into that row's `Open questions` with
`needs-decision` or `needs-info` — an exit the format already has. No new field, no extra
confirmation, no decision moved into a subagent: everything a subagent could decide was decided
upstream and handed to it.

**Propagating constraints the skill has never seen.** Three clauses, and the third is the load-bearing
one:

- every instruction the session received restricting what may be read, written, searched or run is
  copied **verbatim** into every delegated prompt, above the contract. The skill does not paraphrase
  and does not judge which restriction is relevant;
- the delegated prompt names every file the subagent may open, by path, and states that it may not
  search, list or glob;
- **a closed input set is what covers a restriction the skill never saw.** A subagent that can open
  only two named payload files and its own contract cannot reach `reference-roadmap/` whether or not
  the eval's prohibition was forwarded.

**Quality risk, and what would catch it.** Cross-row coherence is the whole of it.
**R-024** — one owner per behaviour, and a split that introduces no outcome — is the rule whose
failure mode is two subagents claiming the same behaviour, and it would show first. **R-017** on both
halves: a missing hard edge (already ⚠ opposite on CC-3, where `S4` carries `—` while building on
`S3`'s tables and resolver) and a published edge that restates a criterion. **R-009**, whose subject
is whether a first validator covers the *complete* promise — a property of a row that only the map can
see. **R-023**, whose named failures (atomization, deferred safety) are cross-row shapes. From the
brief: **H3**, the extraction cascade split across three rows that must agree on its order; **H2**,
scoping, which every row must respect; **H4**.

**How it is measured.** The drawing half, scenario 0 (`REVIEW-WORKFLOW.md` § *Which half to run*).
One provider call for the run, one for the review session. Two runs and two reviews for a verdict.
`make validate-roadmap` afterwards is free and is where a broken reference shows.

### B2 — Write `roadmap.md` inside the fan-out window · **accepted, conditional on B1**

`roadmap.md` costs 95s in CC-3 and 95s in CC-2, and it does not depend on the row documents — only
the reverse. If subagents run in the background, main context emits the `roadmap.md` heredoc while
they work and the 95s disappears into the parallel window.

**Files.** One sentence in `SKILL.md` § *Draw the map*, ordering the dispatch before the write.

**Saving.** Up to **95s**, absorbed rather than removed.

**Risk.** Not quality — it changes nothing about the content. It is a **portability** risk: the
payload must run from `~/.claude/skills/roadmap` with nothing around it, and background subagents are
a harness capability the skill cannot assume. Stated as a preference — *dispatch first, then write* —
it degrades to a plain ordering on a harness that blocks, and costs nothing there.

**Measured** by the same run as B1; it is not separable from it and does not need its own.

### B3 — Give the drawing an explicit order of operations · **accepted, unpriced**

The 8m 14s of thinking is the largest number in the run and the one the transcript cannot break
down. `drawing-the-map.md` is 17,488 characters of argumentative prose — themes, cap, dependencies,
prerequisites, ordering, seam, sweep, checklist — that fixes the order of exactly one thing (*sweep
the sources before the map is drawn*) and leaves the session to derive the rest. A single 19,014-token
think is what deriving it looks like.

**Files.** `references/drawing-the-map.md` only. Explicitly **not** `SKILL.md`: `EVALUATION-RULES.md`
is direct that a rule applied badly is a defect in `references/` and that landing fixes in `SKILL.md`
by default is how a router grows back into a monolith.

**Saving.** Unpriced, and the document should not pretend otherwise. If an explicit order cuts the
design think by a quarter, that is ≈8,700 tokens ≈ **123s**; it could equally cut nothing. This is the
option that most needs a run, and the only honest way to price it is to run it.

**Risk, and it is the highest here.** An order that fixes the sequence can suppress the traversal
between themes and rows that the split and merge verdicts need — **R-008**, which owes a recorded
verdict on every boundary. A procedure that keeps the steps and loses the reasons costs **R-012**
(every departure from breadth named in the criterion that concedes it) and **R-015** (three exits, and
the *its reason survives its citations* test that CC-3 already failed on the `S4, ricerca` line).
`ROADMAP-GOAL.md` also names the direction of travel to avoid: a checklist is one revision away from
a field nobody re-reads.

**Measured** on the drawing half. One run, one review; two of each for a verdict. Because its effect
is on thinking rather than on artifacts, `METRICS.md` alone reads it — but only once the token
double-count below is fixed.

### B4 — A subagent that reads and summarises the sources · **rejected**

**On wall-clock it buys nine seconds.** Calls 1 and 2 read all four source documents in 3.3s + 5.7s.
That settles it against the primary goal.

On the secondary goal it buys ≈5,800 main-context tokens, and pays for them in the place the eval is
most sensitive. `Assumptions` lines must survive the *its reason survives its citations* test, which
requires the cited lines in context at the moment the line is written — and CC-3 failed exactly that
test with the full sources in context. **H5** was missed the same way: React Query is named in
`sources/tech-choices.md` § *Data fetching client* and in `goal.md`, and no document in the map
mentions it. A summariser makes both failure modes more likely, not less.

The narrower form — a subagent returning the conflict and undecided-choice inventory with verbatim
quotations and line references on both sides — is the only version that would not degrade R-015, and
it saves nothing, because it is the quotations that cost the tokens. Rejected on both goals.

### B5 — Defer the row documents to handover · **rejected**

Writing the register on the `Drawing` door and each document only when the row is picked up removes
the entire 243s of per-row work. It also breaks the format: the validator errors on a row that does
not resolve to a document, the register cannot carry `Learning target` (which is the invariant the
split test runs on), and `ROADMAP-GOAL.md` states that a single row must be expandable, promotable and
closeable without touching anything else.

The weaker variant — thinner documents for the far half of `NOW` — is refused by name in
`ROADMAP-GOAL.md` § *No gradient of detail inside `NOW`*: what differs between near and far is
confidence, and confidence already has `Open questions` and `readiness: needs-decision`.

### B6 — Split the drawing across two author turns · **rejected**

Confirming the register before the documents are written would let the author stop a wrong map before
243s is spent on it. It adds a round trip, and the session's contract with the author is one
confirmation block and one blocking question. It is also the wrong shape for this door: a first map
writes unasked precisely because there is nothing on disk to lose, and it argues with its own first
cut in the same session (`SKILL.md` § *Draw the map*). **R-032** reads this directly.

---

## Small improvements

Ordered by saving over risk. **S1 has the best ratio in this document, bold options included.** A
reader taking exactly one change should take it.

### S1 — Bound the prose in the two templates

The templates say what each section is for and nothing about how much of it there should be. The
payload is the only thing the session has to calibrate against, and the payload is written in dense
argumentative prose — so the output comes back at 2–3× the reference's density, uniformly, in every
prose section and no table.

**Files.** `assets/slice-template.md` and `assets/roadmap-template.md`; one clause in
`references/drawing-the-map.md` for the map-level sections.

**Saving.** 19,700 characters ≈ 5,800 output tokens ≈ **80s**, floor 60s, plus the thinking that
produced them, which is unpriced. Founded on the reference/CC-3 table above: `Verification` 3.5× per
row, `Includes` 2.9×, Themes and Ordering criteria 3.1× each.

**How the bound is stated matters more than the number.** `ROADMAP-GOAL.md` forbids a token budget,
so a character count is the wrong instrument. A form rule is not: `Verification` is *one scene
somebody can watch*, the way the reference's `S4` is one sentence with two observations in it;
`Includes` is *the minimum, one bullet per thing that has to exist*; `Excludes` names a destination
per bullet and no argument. That is a bound on shape, which is what the rest of the payload already
does everywhere else.

**Risk.** A bound that cuts too deep drops evidence. **R-020** — every material claim in
`Learning target` has an observation in `Verification` — is the rule that would catch it, and it is
the one to watch, since the shortening pressure lands exactly there. **R-026** likewise, for
`OUT-OF-SCOPE` entries compressed from a licence back into a line saying what will not be done.
Against those: CC-3's `S4 Verification` currently *fails* by over-writing, restating the H2 scoping
invariant that `Cross-functional concerns` owns and the latency figure that `S2` owns — so on this
row the bound and the rules pull the same way.

**Measured** on the drawing half. One run, one review; the artifact sizes are then a free
before/after (`wc -c` against CC-2 and CC-3, which are on disk).

### S2 — Publish the cap, the floor and what the validator checks

`drawing-the-map.md` says `NOW` is capped and has a floor without saying what either is; `SKILL.md`
lists four of the validator's checks out of roughly twenty. CC-3 grepped for the numbers, got them,
and then read 600 lines of `validate_roadmap.ts` anyway to learn what else would come back red.

**Files.** `references/drawing-the-map.md` § *The cap is a finding, not a budget* takes the two
numbers; `SKILL.md` § *Run the validator* takes a one-line-per-check list.
`scripts/validate_roadmap.ts` exports them; `scripts/validate_roadmap.shape.test.ts` pins the document
to the export — **the mechanism already exists**, since that test already pins both templates to
`SHAPE`.

**Saving.** ≈10s of wall-clock and ≈6,000 main-context tokens, plus one avoided fix-up round (call 15,
5.1s). Small, and near-free.

**Risk.** Drift between the document and the code, which the shape test removes. No rule is exposed:
this publishes what the payload already enforces. It also closes a real gap in self-sufficiency — the
payload currently expects a session to read a TypeScript file to find out what its own validator wants.

**Measured** by `node --test skills/roadmap/scripts/` — **no provider call**. Whether it changes
session behaviour needs the drawing half like everything else, but it can be shipped on the free test
alone.

### S3 — Read the payload in one call

CC-3 reads the two references in one call and the two templates in the next; CC-2 spreads the same
material across four. One command for both references and both templates saves a request.

**Files.** One sentence in `SKILL.md`, near the two-references paragraph.

**Saving.** 3–6s, no token change. Listed because it is free, not because it matters.

**Risk.** None identified. **Measured** incidentally by any run.

---

## The dial the skill does not own

**Reasoning effort is the single largest number on the critical path and it is not a skill change.**
34,859 thinking tokens, 8m 14s, 61% of CC-3. `REVIEW-WORKFLOW.md` fixes model and effort in the
session and requires that what the session actually said be written down, so it is an eval variable
rather than a payload one. It belongs in this document because the brief asks for the biggest lever
the transcript shows, and this is it.

The cheapest experiment available is **one run at a lower effort with the payload unchanged**: one
provider call for the run, one for the review, and it prices the 8m 14s that B3 can only guess at. The
cost of taking it is that it moves the baseline every previous run was measured against.

There is a payload-side version of the same lever, and it is B3's real mechanism: **the payload's own
prose density is a thinking budget the skill sets implicitly.** 48,700 characters of argumentative
prose across `SKILL.md` and the two references is the register the session reproduces — in its
thinking, and then in the map, which comes back at three times the reference's density in exactly the
sections the payload argues hardest. B3 and S1 are the same thesis at two altitudes: *the tool writes
the way its own documents are written.*

---

## The metrics this was read off

`run_metrics.ts` used to sum `message.usage` **per assistant entry**, and one provider request
produces one entry per content block — so every token figure and the call count in every `METRICS.md`
was inflated by roughly 2×. It now groups by `requestId`, and CC-2 and CC-3 have been regenerated.

| | before | now |
|---|---|---|
| API calls | 32 | **16** |
| output | 130,487 | **58,147** |
| ↳ thinking | 84,869 | **34,859** |
| thinking share | 65% | **60%** |
| cache read | 2,563,287 | **1,332,316** |

The wall-clock rows were computed from timestamps and were already right; only the per-call average
inherited the bad denominator.

`METRICS.md` also carries the phase table now, so the breakdown this document argues from is
regenerable rather than hand-profiled. Two things about how it is computed are worth knowing before
an after-measurement is read against a before:

- **The phase of a request is the strongest thing it did**, in the order writes a file → runs the
  validator → reads → called no tool at all. A turn that wrote a document while also listing a
  directory was producing the map. Reading `validate_roadmap.ts` with `sed` counts as reading, not as
  validating — only invoking it is validating.
- **A sub-agent's requests never enter the phases.** They run beside the driver, so adding their
  seconds would count the same wall-clock twice. What a sub-agent costs the session is the tool wait,
  which lands in *Tool, sub-agent e I/O* — which is why that row, two seconds today, is the one to
  read after B1.

## Provider calls, if the options are taken

Nothing was sent in this session. `AGENTS.md` requires the exact count and explicit approval before
any of this runs.

| | runs | reviews | total sessions |
|---|---|---|---|
| S1 alone, to a question | 1 | 1 | **2** |
| S1, to a verdict | 2 | 2 | **4** |
| B1 + B2 together, to a question | 1 | 1 | **2** |
| B1 + B2, to a verdict | 2 | 2 | **4** |
| B3, to a verdict | 2 | 2 | **4** |
| Effort dial, to a question | 1 | 1 | **2** |

Free, and worth doing first: the `run_metrics.ts` grouping fix, the `SHAPE` test for S2,
`make validate-roadmap` on every run.

**Recommended order.** S1 first and alone, because it shrinks what B1 has to parallelise and would
otherwise confound it. Then B1 with B2. B3 last, and only if the first two leave a target unmet.
Changing two at once buys one measurement that attributes nothing.

**Realistic target, taken in that order:** 803s → **520–580s** on S1 + B1 + B2, a 28–35% cut, with
B3 or the effort dial as the only route below 500s. Main context peak falls from ≈134k tokens by
≈24k on S1 + B1 + S2, before counting what the thinking reduction takes with it.

## Open questions

- **How is S1's bound stated so it does not become a token budget?** The reference is the evidence for
  what is enough, and the payload cannot cite it — `reference-roadmap/` lives under `evals/` and a
  session may not read it. A form rule (*one scene somebody can watch*) is the version that does not
  violate `ROADMAP-GOAL.md`; a count with a stated reason is the version that is measurable. This
  blocks S1's wording, not S1.
- **Does the target harness guarantee subagents, and background subagents?** B1 needs the first and B2
  the second, and the payload must run from `~/.claude/skills/roadmap` with nothing around it. A
  degradation clause — *where the session cannot delegate, write them in one pass* — solves it, at the
  cost of a payload that describes two ways of working. `ROADMAP-GOAL.md` refused a two-branch split
  once already for a different reason; whether this one is the same shape is a judgement worth taking
  before B1 is written.
- **Is a lower reasoning effort admissible as an eval variable?** It is the largest lever and the
  cheapest to price, and taking it re-bases every past run.
