# Results

What the skill actually produced, one directory per run. Never read by a generation session, and
never the input to one: a session gets a copy.

**A run keeps its own `PROMPT.md` only where the prompt is what is under test** — the three router
cards, whose sentence is the input the router reads, and where a paraphrase is a different run.
Elsewhere the card in [`../../PROMPTS.md`](../../PROMPTS.md) *is* the prompt, and copying a constant
into every directory buys nothing: the text the session received and every answer given back are in
`TRANSCRIPT.jsonl` verbatim, which is where the rules read them anyway.

**Write one anyway where the run departs from the card**, since the transcript shows the departure
without explaining it: a model or harness other than the card assumes, a sub-agent driving instead of
a person, or a point where the run ends before the file does.

**Every run keeps its own `TRANSCRIPT.jsonl`**: the session as the harness recorded it, copied out by
whoever drove the run and never written by the session itself. Half the evidence about this skill is
not in the map — what the session was sent, what it asked back, what it declined to write — and this
is the file that holds it.
[`../../REVIEW-WORKFLOW.md`](../../REVIEW-WORKFLOW.md), *Producing a run* step 5, says when and how.
A run without one is half a net — R-001, R-003 to R-005 and R-031 to R-035 have nothing to read
against it, and a review says *inconclusive* there rather than green.

**And its own `METRICS.md`**, which is the one thing the transcript holds but does not show: active
time, tokens by category, API calls, tools. It is never written by hand — `make run-metrics
RUN=<dir>` regenerates it — so it is derived and not evidence: where the two disagree the transcript
wins. It serves the work on speed and token cost, not the judgement: no rule in
`EVALUATION-RULES.md` reads it.

A run that has been reviewed keeps the report beside the map it judges, as `REVIEW.md`. It cites rule
ids, brief ids and the oracle, so it is answer key: a generation session pointed at a run directory
may not read it, and no run directory that holds one is reused for generation.

| Run | Branch exercised | Starting state | Outcome | Net |
|---|---|---|---|---|
| `manual-run-1` | Drawing | empty project | 11 rows, `S0`–`S10`, validator green | half — no transcript |

`manual-run-1` is the one run driven by a person in an interactive session rather than through a
sub-agent, and what was sent is the drawing card in [`../../PROMPTS.md`](../../PROMPTS.md). It has no
transcript either — it predates the obligation — so
the nine rules that read the session are inconclusive against it, and its `REVIEW.md` says so.

## A run driven by a sub-agent

[`../../REVIEW-WORKFLOW.md`](../../REVIEW-WORKFLOW.md) is written for a human typing `/roadmap` into an
interactive session. A sub-agent needs three additions to the card's prompt — how to reach a skill it
cannot type, do not delegate, and stop at the proposal — and that is a departure, so such a run keeps
a `PROMPT.md` carrying the full text whichever card it runs.

What that costs is the invocation path — anything depending on how the harness loads the skill goes
untested. What it does not touch is the reading the session does or the block it proposes, which is
what the rules are about. The transcript to capture is the driver's: the sub-agent's turns are in it,
marked `isSidechain: true`.
