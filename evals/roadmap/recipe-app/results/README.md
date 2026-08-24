# Results

What the skill actually produced, one directory per run. Never read by a generation session, and
never the input to one: a session gets a copy.

**Every run keeps its own `PROMPT.md`**: the exact text sent, every answer given back, and the model
and harness it ran on. Half the evidence about this skill is in what a session asked and what it
declined to write, and none of that survives in the map alone.

| Run | Branch exercised | Starting state | Outcome |
|---|---|---|---|
| `manual-run-1` | Drawing | empty project | 11 rows, `S0`–`S10`, validator green |

`manual-run-1` is the one run driven by a person in an interactive session rather than through a
sub-agent, and the only one without its own `PROMPT.md`: what was sent is in
[`../../PROMPTS.md`](../../PROMPTS.md).

## A run driven by a sub-agent

[`../../REVIEW-WORKFLOW.md`](../../REVIEW-WORKFLOW.md) is written for a human typing `/roadmap` into an
interactive session. A sub-agent needs three additions to the card's prompt, and the `PROMPT.md` has
to carry the full text so the difference is readable: how to reach a skill it cannot type, do not
delegate, and stop at the proposal.

What that costs is the invocation path — anything depending on how the harness loads the skill goes
untested. What it does not touch is the reading the session does or the block it proposes, which is
what the rules are about.
