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
make eval-cycle          # install, then the drawing, its review and the proposals: three sessions, empty context each
```

`make eval-cycle` asks once, listing all three sessions, and sends nothing until you answer — no
later step comes back to ask again: [`../AGENTS.md`](../AGENTS.md) binds, and approval of a plan
is never approval to send. It works in `recipe-app/results/ROADMAP-CC-<N>`, `<N>` being the next free
number, and writes there in this order:

| File | Written by | What it is |
|---|---|---|
| `PROMPT.md` | the driver, before sending | harness, model, effort, session id, the prompt word for word, and the commit and `skills/roadmap` tree the run ran on |
| `.roadmap/` | the drawing session | the map — the artifact under judgement |
| `TRANSCRIPT.jsonl` | the driver, by session id | the session as the harness recorded it |
| `METRICS.md` | `run_metrics.ts` | time, tokens, calls, tools. Derived: where it and the transcript disagree, the transcript wins |
| `REVIEW.md` | the review session | one line per violation, with rule and brief ids. **This is the output** |
| `IMPROVEMENTS.md` | the improvement session | what to change in the skill, in three categories |

`make eval-run`, `make eval-review RUN=<dir>` and `make eval-improve RUN=<dir>` are each one step, for
when one of them has to be redone — or to run the proposals again over an older run after a change to
`improve.prompt.md`.
The validator is not a step of its own: `review.prompt.md` has the review session run it first thing,
and report a red rather than repair it.

**Then read `REVIEW.md`.** The discipline it was written under is `review.prompt.md`, word for word
— the brief first, the rules, the reference last, the tally to close — and that is what you read the
report against.

**The third session is the proposals.** It reads every run's `REVIEW.md` and the git history of
`skills/roadmap` between them, and writes `IMPROVEMENTS.md`: every regression and every fix that did
not take, plus the three otherwise recurring violations that pay most to close. It proposes and
implements nothing — reading the three before touching `skills/roadmap` is yours.

**One prompt is still not sent by the cycle**: `improve-perf.prompt.md`, which reads the metrics and
the transcript for what the run cost and writes `PERF-SUGGESTIONS.md`. `render_prompt.ts` prints the
text to paste into a fresh session:

```bash
node evals/roadmap/scripts/render_prompt.ts evals/roadmap/recipe-app/prompts/improve-perf.prompt.md RUN_DIR=<dir>
```

## The router scenarios, by hand

`make add` first — nothing below installs the skill for you.

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
7. **Write `REVIEW.md`**: read the proposed block against the card's verdict, and cite what actually
   failed rather than the verdict as a whole — a session can get the altitude right and the operation
   wrong, which is a finding against one rule and not against the card. Close on the tally the head
   of [`EVALUATION-RULES.md`](EVALUATION-RULES.md) defines, over the card's rule list.

A router run keeps a `PROMPT.md` always, since its prompt is the thing under test and a paraphrase is
a different run. What else a run directory keeps, and why, is in
[`recipe-app/results/README.md`](recipe-app/results/README.md).

