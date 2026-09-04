# Results

What the skill actually produced, one directory per run. Never read by a generation session, and
never the input to one: a session gets a copy.

**A run driven headless keeps a `PROMPT.md`, always.** `make eval-run` writes it before sending:
harness, model, effort, session id, the prompt word for word, and the version of the skill that ran —
the commit, and the `skills/roadmap` tree at it. Those last two are what let the improvement cycle
place a run in the history of the skill instead of inferring it from when the run happened to be
committed: what it needs is the boundary between two runs, since every commit inside the interval is
a fix that the later run put to the test. The prompt is no longer a constant
— it is [`../prompts/run.prompt.md`](../prompts/run.prompt.md), a file under version control that the
improvement cycle may change between one run and the next — so a directory that did not carry its own
copy would leave nothing saying which version it was sent.

**A run driven by hand keeps one where the prompt is what is under test** — the three router cards,
whose sentence is the input the router reads, and where a paraphrase is a different run — **or where
the run departs from the card**, since the transcript shows the departure without explaining it: a
model or harness other than the card assumes, a sub-agent driving instead of a person, or a point
where the run ends before the file does.

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

**A satellite run is a first-class run minus review.** `make eval-noise RUN=<main run>` launches the
missing twins of a run — same commit, same prompt, same model and effort, read back out of the main
run's `PROMPT.md` — as sibling directories suffixed `B` and `C` (`ROADMAP-CC-6B`), each with the
full kit: `PROMPT.md`, which declares the satellite, `TRANSCRIPT.jsonl`, `METRICS.md`. A satellite
is generation-only and never receives a `REVIEW.md` — the inverse of the rule below, by which a run
that holds one is never reused for generation — and what it exists for lands beside the main run's
map as `NOISE.md`: generated, never hand-written, regenerable, but unlike `METRICS.md` not purely
derived — it carries the model's alignment judgements, each marked by provenance.
The rationale is
[`design/roadmap/adr/001-prezzamento-del-rumore.md`](../../../../design/roadmap/adr/001-prezzamento-del-rumore.md).

A run that has been reviewed keeps the report beside the map it judges, as `REVIEW.md`, and the
proposals the cycle drew from it as `IMPROVEMENTS.md` beside that. Both cite rule ids, brief
ids and the oracle, so both are answer key: a generation session pointed at a run directory may not
read either, and no run directory that holds one is reused for generation. `IMPROVEMENTS.md` is
anchored to its run but reads every other run's `REVIEW.md` too, and the history of `skills/roadmap`
between the commits that added each run — what one report cannot show is which violations recur, and
what no report shows at all is which of them a change to the skill had already taken aim at: a
violation that goes green and comes back is a regression, one that never goes green is a fix that did
not take, and neither is legible from the reports alone.

The three `ROADMAP-CC-*` runs predate that record, and each one's `PROMPT.md` now carries the anchor
read back out of its own transcript: the sessions `cat`-ed the skill's files, so the text they ran on
survives in full and matches exactly one historical version. Each says so, and says how. On
`ROADMAP-CC-4` the reconstruction and the cheap inference disagree — `779bf17` lands between the
skill that ran and the commit that added the run — which is the whole reason the record is now taken
before sending rather than deduced afterwards. `manual-run-1` keeps no transcript, so for that one
there is nothing to read the skill back out of. What it keeps instead is a partial `PROMPT.md`, the
anchor and nothing else, since nothing else survives: the cheap inference, the one piece of evidence
that goes past it — the map as committed matches exactly one template version — what would falsify
it, and what hangs on it. It stays an inference and says so, and what the file removes is the work of
redoing it every cycle, not the doubt.

| Run | Branch exercised | Starting state | Outcome | Net |
|---|---|---|---|---|
| `manual-run-1` | Drawing | empty project | 11 rows, `S0`–`S10`, validator green | half — no transcript |

`manual-run-1` is the one run driven by a person in an interactive session rather than through a
sub-agent, and what was sent is the drawing prompt, which lived in `../../PROMPTS.md` then and is
[`../prompts/run.prompt.md`](../prompts/run.prompt.md) now. It has no
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
