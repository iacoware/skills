# Making the drawing faster

Options for bringing a `Drawing` session under **five minutes of active time**, and secondarily for
cutting the tokens in the main context window. Nothing here is implemented.
[`ROADMAP-GOAL.md`](./ROADMAP-GOAL.md) stays the authority on what the tool must not become, and no
option below buys time with a new field, a gradient of detail, or a number nothing can check.

This version supersedes the one read off `ROADMAP-CC-3`. The evidence is now
`recipe-app/results/ROADMAP-CC-5`, `ROADMAP-CC-6` and its two satellites `ROADMAP-CC-6B` and
`ROADMAP-CC-6C` — three runs of the same `skills/roadmap` tree, same prompt, `opus` at effort `high`
— profiled per provider request from `TRANSCRIPT.jsonl`. `METRICS.md` carries the phase totals; the
per-request profile below is what the totals hide.

## What the evidence says now

**The equation from the CC-3 report still holds: wall-clock = output tokens ÷ ~72 per second.** 71,
73, 72 and 74 tok/s on the four runs. Tool execution is 2–4 seconds per run, cache reads cost no
wall-clock, and nothing but the model generating tokens takes time.

What the per-request profile adds is *where* those tokens are emitted:

| Run | active | design think — **one request** | writing, serial | reading | close |
|---|---|---|---|---|---|
| CC-5 | 13m 20s | 458s · 32k thinking tokens (two requests: 296s + 162s) | 267s | 30s | 37s |
| CC-6 | 10m 02s | 257s · 18.4k | 295s | 27s | 21s |
| CC-6B | 11m 02s | 319s · 22.8k | 282s | 27s | 30s |
| CC-6C | 12m 27s | 482s · 33.5k | 217s | 21s | 24s |

*Writing* is `roadmap.md` (57–63s in every run) plus the row documents, written in four to six
heredocs of 35–60s each, one after the other. *Close* is validator, one fix-up, and the four-part
report.

Three things the CC-3 report could not see:

1. **The design think is a single provider request and it is 43–65% of the run.** After the payload
   and the sources are in context, the session emits one request carrying 18k–33k thinking tokens and
   a trivial tool call (`grep` on the validator, `mkdir -p`), then writes everything. No later request
   thinks more than 3k tokens. Whatever the drawing derives — themes, verdicts, rows, edges, order,
   the seam — it derives here, in one unbounded pass, before a line is written.
2. **At a fixed skill version that one request varies twofold**: 257s, 319s, 482s on the three
   satellites. Active time varies 602–747s with it. A single run is a ±25% measurement of anything
   that touches the think, which is why the measurement plan below uses the twins.
3. **The writing is ~250s and entirely serial**, and the two options that would parallelise it —
   B1 and B2 of the previous report, marked *accepted* — were never implemented. No run has a
   sub-agent in it.

### What changed since the CC-3 report, and what did not

`roadmap.md` shrank: 16,786 characters on CC-3 to 10,157–11,683 on the CC-6 twins, against a
reference of 8,055 — from 1.9× to 1.3×. `Ordering criteria` was removed from the format, the theme
verdict became a one-line paragraph. **The row documents did not shrink**: 28,129–30,582 characters
for 11–12 rows, 2,344–2,777 per row, against 1,167 in the reference — still 2.0–2.4×, unchanged from
CC-3's 2.3×. The bullet-form `Verification` (`d8bc79d`) did not cut the per-row size on its own.

S2 — publish the cap, the floor and the validator's checks — was not done, and every run still pays
for it in the same place: the session reads 200–480 lines of `validate_roadmap.ts` (CC-6C `cat`s the
whole 20,897 characters) **immediately before** the design think. That is ≈5,500 tokens of TypeScript
in context at the moment the session decides how much there is to reason about. Its wall-clock cost is
ten seconds; what it does to the think is unmeasured.

## The arithmetic of the target

Five minutes is 300s. What the profile leaves room for, taking CC-6 (the best twin) as *today*:

| Phase | today | needed | how |
|---|---|---|---|
| Reading | 21–30s | ~10s | one request for the payload, one for the sources |
| Design think | 257–482s | **≤120s** | P1, or the effort dial |
| Writing window | 217–295s | **≤70s** | P2: critical path is the slowest single row |
| Close | 21–37s | ~25s | unchanged |
| **Total** | **602–747s** | **~225s** | |

Two conclusions the table forces. **P2 is the sure saving and it is not enough**: with the writing
fanned out and nothing else changed, CC-6 lands at ≈400s and CC-6C at ≈590s. **The think decides the
target**: at its best observed value (257s) it alone is 86% of the budget, so under five minutes needs
the think to lose at least half, and the only two things that act on it are the payload (P1) and the
effort setting (P3).

---

## The three options

### P1 — Draw by writing: the register is the first file written, not the last thing thought

**Mechanism.** Today the session derives the whole map in its head and then writes it. Thinking is
unbounded; the register is twelve rows, ≈1,500 output tokens. The change fixes an explicit order of
operations in `drawing-the-map.md` whose first step after the source sweep is *write the draft
`roadmap.md`* — `Goal`, themes with their one-line verdicts, the register, the edges — and runs the
rest of the reference as a **revision pass on the written draft**: the split and merge tests on each
boundary, the two prerequisites, the order for learning, the seam, `Assumptions` and `Open questions`
traced to rows. `SKILL.md` § *Draw the map* already says a first map is a draft to argue with, in the
same session; P1 applies that sentence to the moment the map is born instead of after it is complete.
The thinking is not forbidden — it is given a written object to argue against, twelve lines long,
instead of a blank page and 48,000 characters of rules.

This is B3 of the previous report with its missing first step. B3 asked for an order and could not say
what the order bought; the profile now says the whole cost sits in one pre-writing request, so the
order that matters is the one that moves the first write forward.

**Includes S2.** The cap, the floor and one line per validator check go into the payload —
`drawing-the-map.md` § *The cap is a finding, not a budget* takes the two numbers, `SKILL.md` § *Run
the validator* takes the list — exported from `validate_roadmap.ts` and pinned by
`validate_roadmap.shape.test.ts`, which already pins both templates to `SHAPE`. Nothing then needs to
open the validator before thinking. Free to ship: `node --test skills/roadmap/scripts/` and no
provider call.

**Files.** `references/drawing-the-map.md` — the order and the two numbers. `SKILL.md` § *Draw the
map* — one sentence: the draft goes down before the argument, and § *Run the validator* — the check
list. `scripts/validate_roadmap.ts` and its shape test. Not `SKILL.md` for the order itself:
`EVALUATION-RULES.md` is direct that a rule applied badly is a defect in `references/`.

**Saving.** Not priceable from the transcript, and this document should not pretend otherwise. The
target is a think of **≤120s (≈8,500 tokens)** from 257–482s. If the order cuts the think by half on
the best twin, that is ≈130s; on the worst, ≈240s. It could cut nothing: a model at effort `high` may
think 20k tokens before emitting a draft whatever the reference says. This is the option that most
needs a run.

**Risk — the highest here.** An order that fixes the sequence can suppress the traversal between
themes and rows that the split and merge verdicts need: **R-008**, which owes a recorded verdict on
every boundary. A draft written before the sweep lands its assumptions loses **R-012** (every
departure from breadth named in the criterion that concedes it) and **R-015** (three exits, and the
*its reason survives its citations* test). `ROADMAP-GOAL.md` names the direction to avoid: a
checklist is one revision away from a field nobody re-reads. What contains the risk is that the
revision pass keeps every rule and every reason; what changes is only whether the draft exists when
they are applied.

**Measured** on the drawing half, scenario 0, **with the satellites**: one main run and two twins
(`make eval-noise`), one review. Three timing points, because a ±25% measurement cannot read a change
of this shape on its own. The `NOISE.md` agreement table says whether the draft-first map holds its
themes and verdicts across twins as well as the current one does.

### P2 — Fan out the row documents to sub-agents; write `roadmap.md` inside the window

B1 and B2 of the previous report, accepted then and still not implemented. Restated here in full
because the contract is the specification.

**Mechanism.** Once the register, the themes and the edges are fixed, the eleven documents are
independent. Main context fixes the map, dispatches one sub-agent per row **in the background**, then
emits the `roadmap.md` heredoc while they run — `roadmap.md` (57–63s in every run) does not depend on
the documents, only the reverse — and writes nothing per row itself. The validator that runs after
writing is what checks that the documents cohere with the register.

**Saving — the sure one.** Writing goes from 217–295s serial to the critical path of the slowest
single row: ≈700 output tokens of document plus the sub-agent's own reading of two payload files and
its own thinking, **call it 60–70s** with dispatch. **150–220s** on the four runs. Main context also
stops carrying ≈8,500 tokens of slice text.

**A knob inside it.** The Agent tool takes `model`; the sub-agents can run on `sonnet`, which emits
faster and thinks less, and the row document is the one artifact in the map whose form is fully fixed
upstream. Stated as a preference, not a requirement, and unmeasured: it is a second variable, so it
runs as a separate twin set if the first fan-out lands over 70s on the critical path.

**Where S1 goes.** The per-row density that did not move (2.0–2.4× the reference) is bounded here,
in the contract, as a rule of form and never a count: `Verification` is *one scene somebody can
watch*, `Includes` *the minimum, one bullet per thing that has to exist*, `Excludes` *a destination
per bullet and no argument*. A sub-agent with one row and a form rule has nothing to over-write with.
**R-020** (every material claim in `Learning target` has an observation in `Verification`) is the
rule that catches a bound cutting too deep.

**What must be in the contract**, item by item, because each one is a rule that fan-out would
otherwise break:

1. `id`, title, slug, and the five register columns as main context decided them. The sub-agent may
   not change one.
2. `Outcome`, one line, fixed upstream — the row's identity.
3. `Learning target`, one line, fixed upstream. Identity follows the learning target through a split
   or a merge (`slice-rules.md` § *Identity*), so it cannot be invented downstream.
4. `Depends on` **in both directions**: the ids this row depends on and the ids that depend on it,
   each with its one-line outcome. Without the reverse edge the sub-agent cannot write `Excludes`
   honestly.
5. The whole register as id + title + one-line outcome. This is what lets `Excludes` name *where* a
   behaviour went — the conservation clause of `slice-rules.md` § *Splitting and merging*.
6. `Cross-functional concerns` verbatim, with the instruction that a row restates none of it — and
   main context naming which row is the first to cross each trust boundary or perform each external
   side effect, since that row and only that row verifies it.
7. The `Assumptions` and map-level `Open questions` lines traced to this id, so that the reading lands
   in a bullet (`drawing-the-map.md`, the *it lands in a row* test).
8. Where the row sits relative to the identity seam: which resolver owns scope at this point in the
   order, and whether the row precedes or follows authenticated identity.
9. `Requested by`, as main context traced it.
10. The form rule for each section, from *Where S1 goes* above.
11. Two payload paths and no others: `assets/slice-template.md` and `references/slice-rules.md`.
    Never `drawing-the-map.md` — a sub-agent decides nothing about the map's shape.

**What comes back: the path written, and a `—`-or-lines block of what the sub-agent could not
settle. Not the document.** The four-part report is read off `roadmap.md` and the register, never off
the row documents; the validator checks coherence better than a re-read would; and returning eleven
documents spends the tokens the fan-out just saved. Anything a sub-agent cannot settle comes back as a
line and main context routes it into that row's `Open questions` with `needs-decision` or
`needs-info` — an exit the format already has. **Round trips are unchanged**: sub-agents never
address the author, and no decision moves into one, because everything a sub-agent could decide was
decided upstream and handed to it.

**Propagating constraints the skill has never seen.** Three clauses, and the third is the
load-bearing one:

- every instruction the session received restricting what may be read, written, searched or run is
  copied **verbatim** into every delegated prompt, above the contract. The skill does not paraphrase
  and does not judge which restriction is relevant;
- the delegated prompt names every file the sub-agent may open, by path, and states that it may not
  search, list or glob;
- **a closed input set is what covers a restriction the skill never saw.** A sub-agent that can open
  only two named payload files and its own contract cannot reach `reference-roadmap/` whether or not
  the eval's prohibition was forwarded.

**Degradation.** The payload must run from `~/.claude/skills/roadmap` with nothing around it, and
background sub-agents are a harness capability the skill cannot assume. One clause — *where the
session cannot delegate, write the documents in one pass, in register order* — and *dispatch first,
then write `roadmap.md`* stated as a preference, which degrades to a plain ordering on a harness that
blocks and costs nothing there. `ROADMAP-GOAL.md` refused a two-branch split once for a different
reason; this is not a second way of working but the same work with or without parallelism, and the
clause is one sentence.

**Files.** `SKILL.md` § *Draw the map* — delegation, the propagation clauses, the degradation clause,
dispatch-before-write. `references/drawing-the-map.md` — the input contract, next to what already
decides the map's shape. `assets/slice-template.md` — the form rule per section, since the sub-agent
reads the template and not the contract's prose. No new payload file.

**Quality risk.** Cross-row coherence is the whole of it. **R-024** — one owner per behaviour — is
the rule whose failure mode is two sub-agents claiming the same behaviour, and it would show first.
**R-017** on both halves: a missing hard edge and a published edge that restates a criterion.
**R-009**, whether a first validator covers the *complete* promise — a property only the map can see.
**R-023**, whose named failures (atomization, deferred safety) are cross-row shapes. From the brief:
**H3**, the extraction cascade split across rows that must agree on its order; **H2**, scoping,
which every row must respect; **H4**.

**Measured** on the drawing half, scenario 0, main run plus twins and one review — the same kit as
P1, and run **before** P1 so that the two savings are attributed separately. `METRICS.md`'s *Tool,
sub-agent e I/O* row, 2–4s today, is where the fan-out's cost lands, and its sub-agent columns appear
on the first run that has one.

### P3 — The effort dial: not a skill change, and the only lever that reaches the target on its own

**What it is.** `REVIEW-WORKFLOW.md` fixes model and effort in the session; every run in the evidence
is `opus` at `high`. At `high` the design think never came in under 18,400 tokens in any run profiled (CC-3 to CC-6C). If P1
does not take at least half off it, **under five minutes is not reachable from the payload at this
effort** — and that is a fact about the target, not about the skill, and belongs in this document so
that nobody spends three more payload revisions looking for it in the references.

**What it costs to know.** One main run at `medium` with the payload unchanged, its two twins, one
review — four sessions. It prices the think directly, which P1 can only attempt to move. It also
re-bases every previous run: a `medium` baseline is a different baseline, and the eval-noise
comparator is what makes the two comparable on the axes that matter.

**Risk.** The same rules as P1 — R-008, R-012, R-015 — because the thinking that a lower effort
removes is the thinking the verdicts and the citations come from. The twins say whether the map holds
its shape at the lower effort; the review says whether it holds its reasons.

**Where it lives.** The eval's `PROMPT.md` records effort; `run_cycle.ts` takes it as a parameter.
For an author using the skill outside the eval, it is a session setting and the payload has nothing to
say about it — which is exactly why the honest form of this option is a paragraph in this document,
not a line in `SKILL.md`.

---

## What this document drops from the previous version

- **B4, a summarising sub-agent for the sources — still rejected.** Reading is 21–30s of the run,
  and the *its reason survives its citations* test needs the cited lines in context when the line is
  written.
- **B5, deferring the row documents to handover — still rejected.** It breaks the format: the
  validator errors on a row with no document, and `Learning target` cannot live in the register.
- **B6, splitting the drawing across two author turns — still rejected.** One confirmation block, one
  blocking question, and a first map writes unasked because there is nothing to lose.
- **S3, reading the payload in one call** — folded into P1's order as the reading step. 3–6s.
- **S1** — folded into P2's contract; **S2** — folded into P1. Neither was done as a standalone
  change, and on the twins the standalone version of S1 that was done (`Verification` in bullet form)
  moved nothing.

## Recommended order, and the provider calls it costs

`AGENTS.md` requires the exact count and explicit approval before any of this runs. Nothing was sent
in this session.

| Step | what | sessions | reads |
|---|---|---|---|
| 0 | S2's export and shape test | 0 | `node --test`, free |
| 1 | **P2**, main + twins + review | 4 | writing window ≤70s; `NOISE.md` agreement against CC-6's |
| 2 | **P1**, main + twins + review | 4 | design think ≤120s; R-008/R-012/R-015 in the review |
| 3 | **P3** at `medium`, only if step 2 leaves the think over 120s | 4 | the think, priced; a new baseline |

P2 first because it is the sure saving, it does not touch the think, and it shrinks what P1 has to
be read against. P1 second and measured with twins, because a ±25% measurement reads nothing on its
own. P3 only if the payload cannot get there — and if it comes to that, this document should say so
in its next version rather than propose a P4.

**Realistic outcome, taken in that order.** After P2: 400–590s. After P1, if it delivers half:
**270–350s**. Under 300s on every twin needs either P1 to deliver more than half, or P3.

## Open questions

- **Does `claude -p` run sub-agents in the background?** P2's window needs it; the first run of step
  1 answers it, and the degradation clause covers a *no* at the cost of B2's 60s.
- **How is P1's order stated so that it fixes when the draft is written and nothing about what the
  argument may conclude?** The risk to R-008 is the order suppressing a verdict, not the order
  existing. The wording blocks P1, not its measurement.
- **Is a `medium` baseline admissible?** It re-bases every run since CC-2. Only worth deciding if
  step 2 fails.
