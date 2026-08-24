# Results

What the skill actually produced, one directory per run. Never read by a generation session, and
never the input to one: a session gets a copy.

**Every run keeps its own `PROMPT.md`**: the exact text sent, every answer given back, and the model
and harness it ran on. Half the evidence about this skill is in what a session asked and what it
declined to write, and none of that survives in the map alone.

**And its own `TRANSCRIPT.jsonl`**, which is where that half actually lives: the session as the
harness recorded it, copied out by whoever drove the run and never written by the session itself.
[`../../REVIEW-WORKFLOW.md`](../../REVIEW-WORKFLOW.md), *Producing a run* step 5, says when and how.
A run without one is half a net — R-001, R-003 to R-005 and R-031 to R-035 have nothing to read
against it, and a review says *inconclusive* there rather than green.

A run that has been reviewed keeps the report beside the map it judges, as `REVIEW.md`. It cites rule
ids, brief ids and the oracle, so it is answer key: a generation session pointed at a run directory
may not read it, and no run directory that holds one is reused for generation.

| Run | Branch exercised | Starting state | Outcome | Net |
|---|---|---|---|---|
| `manual-run-1` | Drawing | empty project | 11 rows, `S0`–`S10`, validator green | half — no transcript |

`manual-run-1` is the one run driven by a person in an interactive session rather than through a
sub-agent, and the only one without its own `PROMPT.md`: what was sent is in
[`../../PROMPTS.md`](../../PROMPTS.md). It has no transcript either — it predates the obligation — so
the nine rules that read the session are inconclusive against it, and its `REVIEW.md` says so.

## A run driven by a sub-agent

[`../../REVIEW-WORKFLOW.md`](../../REVIEW-WORKFLOW.md) is written for a human typing `/roadmap` into an
interactive session. A sub-agent needs three additions to the card's prompt, and the `PROMPT.md` has
to carry the full text so the difference is readable: how to reach a skill it cannot type, do not
delegate, and stop at the proposal.

What that costs is the invocation path — anything depending on how the harness loads the skill goes
untested. What it does not touch is the reading the session does or the block it proposes, which is
what the rules are about. The transcript to capture is the driver's: the sub-agent's turns are in it,
marked `isSidechain: true`.
