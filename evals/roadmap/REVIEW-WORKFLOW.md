# Review workflow

How to run one review of `skills/roadmap/SKILL.md`, to notice that a change to it broke something it
used to get right. What to look for is in [`EVALUATION-RULES.md`](EVALUATION-RULES.md); what to run it
on is a card in [`recipe-app/SCENARIOS.md`](recipe-app/SCENARIOS.md), and the text each card sends is
a file in [`recipe-app/prompts/`](recipe-app/prompts/). This document is the procedure and travels to
a new scenario unchanged.

## Which run answers your change

A change rarely needs both halves.

- **A drawing — scenario 0**, a map from nothing. Half an hour. Run it after a change to *Establish
  the situation*, *Draw the map* or *Close the session*, to `references/drawing-the-map.md` or to
  either template. **Automated end to end.**
- **The router — scenarios 1, 2 and 3**, a map already standing, one card per way the router can
  misread an input. Ten minutes each. Run them after a change to *Choose the door*, *Operations on the
  map* or `references/slice-rules.md`, where the router and the five operations live. **Driven by
  hand**, because each has a turn only a person can answer.

`references/slice-rules.md` is read on every session, so a change to it shows in both halves and the
router is the cheaper place to see it. Run either after a change you believe is substantive, not after
every commit: one run is a question, the same run twice with the same answer is a verdict. What the
net does not cover is in [`README.md`](README.md).

## Scenario 0, in order

```bash
make eval-cycle          # install, then the drawing and its review: two sessions, empty context each
```

**The cycle installs the skill itself** — `make add`, before it asks to send anything — and stops if
`~/.claude/skills/roadmap` still differs from `skills/roadmap` afterwards. That symlink points at a
copy of the skill and not at this repository, and it is what the agent reads: a run that skipped the
step would review the version before your change, and nothing in its report would say so. The
by-hand path installs nothing for you, so the router scenarios still start here:

```bash
make add                 # install the skill under review, then restart the session
diff -r skills/roadmap ~/.claude/skills/roadmap --exclude=.claude && echo "installed copy matches"
```

`make eval-cycle` asks once, listing both sessions, and sends nothing until you answer — the review
does not come back to ask a second time: [`../AGENTS.md`](../AGENTS.md) binds, and approval of a plan
is never approval to send. It works in `recipe-app/results/ROADMAP-CC-<N>`, `<N>` being the next free
number, and writes there in this order:

| File | Written by | What it is |
|---|---|---|
| `PROMPT.md` | the driver, before sending | harness, model, effort, session id, and the prompt word for word |
| `.roadmap/` | the drawing session | the map — the artifact under judgement |
| `TRANSCRIPT.jsonl` | the driver, by session id | the session as the harness recorded it |
| `METRICS.md` | `run_metrics.ts` | time, tokens, calls, tools. Derived: where it and the transcript disagree, the transcript wins |
| `REVIEW.md` | the review session | one line per violation, with rule and brief ids. **This is the output** |

`make eval-run` and `make eval-review RUN=<dir>` are each half, for when one of them has to be redone.
The validator is not a step of its own: `review.prompt.md` has the review session run it first thing,
and report a red rather than repair it.

**Then read `REVIEW.md`.** *Reading a run: a drawing*, below, is the discipline that prompt
implements, and so is what you read the report against.

**Two further prompts start from the same run and are not sent by the cycle.** `render_prompt.ts`
prints the text to paste into a fresh session; each writes one file beside `REVIEW.md`:

```bash
node evals/roadmap/scripts/render_prompt.ts evals/roadmap/recipe-app/prompts/improve.prompt.md RUN_DIR=<dir>
node evals/roadmap/scripts/render_prompt.ts evals/roadmap/recipe-app/prompts/improve-perf.prompt.md RUN_DIR=<dir>
```

The first picks the three changes to the skill that pay most, ranked by which violations recur across
runs, and writes `IMPROVEMENTS.md`. The second reads the metrics and the transcript for what the run
cost, and writes `PERF-SUGGESTIONS.md`.

### What driving it this way costs

**Two guards stop the cycle rather than spend the review call**: a transcript holding no
`Skill(roadmap)` call means the run exercised the model and not the skill, and a session that wrote no
`roadmap.md` did not finish.

**What licenses it is particular to scenario 0.** A router run has to be answered — step 3 below — and
on this card there is nothing to answer: the prompt already says the project is greenfield and that
the directory is to be created, which is the one question *Establish the situation* obliges the
session to ask. `ROADMAP-CC-3` bears it out, with one user turn in the whole run and R-001 green.

**What it does not put to the test** is the interactive invocation path, and a headless run is not the
same run as an interactive one: same prompt text, different harness. Read one against `ROADMAP-CC-3`
as well as against the oracle, at least until a run has shown the behaviour did not move.

## The router scenarios, by hand

`make add` first, and the diff above to check it took: nothing below installs the skill for you.

1. **Copy the card's starting state** into a fresh `recipe-app/results/ROUTER-<n>-CC-<N>`, with the
   command the card gives. Never point a session at `reference-roadmap/` or at `fixtures/`: both are
   frozen and a session writes.
2. **Send the card's prompt.** Render it with that directory and paste the output into a fresh
   session — nothing sends it for you:

   ```bash
   node evals/roadmap/scripts/render_prompt.ts evals/roadmap/recipe-app/prompts/router-1.prompt.md RUN_DIR=<dir>
   ```

   The skill is invoked explicitly, as `/roadmap`: the frontmatter sets `disable-model-invocation:
   true`, and dropping the prefix reviews the model instead of the skill. Model and effort are set in
   the session and never in the prompt, and this run's `PROMPT.md` records what the session said rather
   than what you intended.

3. **Answer what it asks and nothing else.** *Establish the situation* obliges the session to ask what
   was delivered — the only place it is asked — and a tracker cannot answer it; each card says what to
   answer. Answering more turns the run into a collaboration you cannot read.
4. **Confirm nothing that redraws the map.** A map already standing proposes a block first, and a
   redraw you let it write teaches nothing the proposal did not already say.
5. **Capture the transcript**: `make capture-run RUN=<dir>` from a second terminal, the moment the
   session closes on its four-part report and before anything else is typed into it. It copies the
   newest `.jsonl` under `~/.claude/projects/<this repository>/`, so one fresh session per run and no
   `/clear` before capturing; where you typed on anyway, a line in `PROMPT.md` says where the run ends.
   **The session never captures itself**: an instruction to produce a summary of what it believes it
   did would spend R-035 — the session closed on the four parts *and nothing else* — in every run
   after it.
6. **`make validate-roadmap ROADMAP=<dir>/.roadmap`** from the repository root — structural,
   deterministic, free, and `ROADMAP` is the directory holding `roadmap.md`, not a file. A red is a
   finding and not a repair: nothing in the run directory is edited to make it pass. Record it against
   R-033 and read on. A red that is the harness's rather than the session's — the wrong path, a copy
   that did not complete — means the run is broken instead of failed, and it is produced again.
7. **Write `REVIEW.md`** by walking *Reading a run: a router scenario*, below.

A router run keeps a `PROMPT.md` always, since its prompt is the thing under test and a paraphrase is
a different run. What else a run directory keeps, and why, is in
[`recipe-app/results/README.md`](recipe-app/results/README.md).

## The transcript, in either reading

**What a session may read** is `sources/` and its own copy of `.roadmap/`; the prompt says so. Off
limits in particular: `reference-roadmap/` and `REFERENCE-NOTES.md`, `EVALUATION-RULES.md`,
`EVALUATION-BRIEF.md` and `recipe-app/SCENARIOS.md`, which are the answer keys — the cards carry the
router verdicts outright — the whole of `design/roadmap/`, and any earlier run's `REVIEW.md` or
`IMPROVEMENTS.md`.

`TRANSCRIPT.jsonl` holds the half of the evidence that is not in `.roadmap/` — what the session asked,
what it declined to write, what it put to the author — and is the only place that read restriction can
be checked, since a search ranging over `evals/` shows there and nowhere else. Read it **alongside**
whichever reading below applies, never instead of one: without it every such rule is *inconclusive*,
and the report says that rather than green. It is the harness's log and not prose — filter it to the
`user` and `assistant` turns and their tool calls.

## Reading a run: a drawing

1. **Against `recipe-app/EVALUATION-BRIEF.md`**, opening `sources/` only to verify a citation. **The
   brief is the authority**, not the sources: it decides which conflicts exist, which alternatives are
   accepted, which uncertainties are material. Cite its ids instead of paraphrasing. Read the register
   and the slice documents together — a row whose document contradicts it is a defect the register
   alone cannot show, and half the rules are about a field the table does not carry.
2. **Walk [`EVALUATION-RULES.md`](EVALUATION-RULES.md)**, keeping the brief's uncertainty table open
   for R-016. On a first drawing skip *Revising an existing map*, R-006 and R-018. The four-part
   report the session closes on is evidence too.
3. **Only now** open `recipe-app/reference-roadmap/` and `recipe-app/REFERENCE-NOTES.md`. Forming your
   verdict first is what keeps the reference a memory aid instead of a diff target — the order is the
   whole discipline, and what you are hunting is what you forgot, not what you did differently.

How binding the reference is:

- Where reference and `sources/` diverge, the defect is in the reference.
- **Ids, titles, slugs, theme count, row count and register order may all differ.** On each
  difference, ask which of the two has the better reason; `REFERENCE-NOTES.md` holds the reference's.
- Each `Verification` shows one way a row could be demonstrated, not the only one. The same holds for
  `Cross-functional concerns`, whose five headings are owed but not their content.
- A source may support a `LATER` or `OUT-OF-SCOPE` classification other than the reference's, and the
  brief says where.
- The reference takes one exit out of the sweep for each conflict and each undecided choice. Another
  exit is a different choice and not a defect; **no** exit is R-015.

## Reading a run: a router scenario

Read the proposed block against the card's verdict, and cite what actually failed rather than the
verdict as a whole — a session can get the altitude right and the operation wrong, which is a finding
against one rule and not against the card. On scenario 2 the correct session ends in a question and
there is nothing to confirm: record the question and stop.
