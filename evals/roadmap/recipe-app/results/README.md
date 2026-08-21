# Results

What the skill actually produced, one directory per run. Never read by a generation session, and
never the input to one: a session gets a copy.

Three runs keep only their `PROMPT.md`. `ROADMAP-CC-1` and `REDRAW-CC-1` wrote what
`../fixtures/mid-flight/` and `../fixtures/redrawn/` now hold, and `ROUTER-2-CC-1` wrote nothing at
all, so its tree was a byte copy of `../reference-roadmap/`. Keeping a second copy of any of the
three said nothing the first one did not; git holds them if the deletion ever needs undoing.

| Run | Branch exercised | Starting state | Outcome |
|---|---|---|---|
| `manual-run-1` | Drawing | empty project | 11 rows, `S0`–`S10`, validator green |
| `ROADMAP-CC-1` | Drawing | empty project | 12 rows, `S0`–`S11`, validator green — tree kept as `../fixtures/mid-flight/` |
| `ROUTER-1-CC-1` | Re-truing — promotion | `fixtures/mid-flight/` | promoted into `S12`, no redraw, no question |
| `ROUTER-2-CC-1` | Router — question | `reference-roadmap/` copied | ended in a question, wrote nothing — no tree to keep |
| `REDRAW-CC-1` | Redraw | `fixtures/mid-flight/` | `S0`–`S11` archived, `S12`–`S16` drawn — tree kept as `../fixtures/redrawn/` |
| `ROUTER-3-CC-1` | Re-truing — spike | `fixtures/redrawn/` | minted `S17`, `kind: enabler` — diverges, see R-007 |
| `ROUTER-3-CC-2` | Re-truing — spike, second run | `fixtures/redrawn/` | minted nothing, widened `S13` — diverges again and differently, see R-007 |
| `ROUTER-3-CC-3` | Re-truing — spike, third run | `fixtures/redrawn/` | minted `S17`, `kind: enabler` — run one's failure again, see R-007 |

`manual-run-1` is the one run driven by a person in an interactive session rather than through a
sub-agent, and the only one without its own `PROMPT.md`: what was sent is in
[`../../PROMPTS.md`](../../PROMPTS.md).

`REDRAW-CC-1` is the run `fixtures/redrawn/` was frozen from; it is not one of the three router
scenarios. `ROUTER-2-CC-1` wrote nothing because the correct session for that scenario writes
nothing — that the oracle was left unchanged *is* the result. `ROUTER-3-CC-2` and `ROUTER-3-CC-3` are
`ROUTER-3-CC-1` run again on the same fixture with the same prompt, which is the only thing that
makes the three comparable — and `ROUTER-3-CC-3` ran on `claude-opus-5[1m]` rather than
`claude-opus-5`, which its `PROMPT.md` records. Scenario 3 is not run a fourth time; R-007 says why.

Every run keeps its own `PROMPT.md`: the exact text sent, every answer given back, and the model and
harness it ran on. Half the evidence about this skill is in what a session asked and what it declined
to write, and none of that survives in the map alone.

## These runs were driven by a sub-agent, not by a person

[`../../REVIEW-WORKFLOW.md`](../../REVIEW-WORKFLOW.md) is written for a human typing `/roadmap` into
an interactive session. The runs of 2026-08-20 were driven differently, and each `PROMPT.md` carries
the full text so the difference is readable rather than assumed. What was added, in every run:

- **how to reach the skill.** A sub-agent cannot type `/roadmap`, and the skill sets
  `disable-model-invocation: true`, so the prompt tells it to call the skill by name and to fall back
  to reading `~/.claude/skills/roadmap/SKILL.md` as its instructions. The installed copy was verified
  byte-identical to `skills/roadmap/` first.
- **do not delegate.** The workflow's read restriction has to survive one level down.
- **stop at the proposal.** An interactive session stops for confirmation on its own; a sub-agent
  runs to completion, so it was told explicitly to return the block and write nothing until answered.

What this costs: the invocation path is not the one a real author uses, so anything that depends on
how the harness loads the skill is untested here. What it does not touch is the reading the session
does or the block it proposes, which is what the rules are about.

The prompts themselves — the request, the read restriction, and the author's opening sentence — are
the workflow's, unchanged.
