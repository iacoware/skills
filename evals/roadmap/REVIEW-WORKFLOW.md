# Review workflow

How to run one review of `skills/roadmap/SKILL.md`, to notice that a change to it broke something it
used to get right. What to look for is in [`EVALUATION-RULES.md`](EVALUATION-RULES.md); what to run it
on is a card in [`recipe-app/SCENARIOS.md`](recipe-app/SCENARIOS.md) — scenario 0 is a map drawn from
nothing, scenarios 1–3 are a map already standing. This document is the procedure and travels to a new
scenario unchanged.

## Which half to run

A change rarely needs both.

- **A drawing — scenario 0.** Half an hour, one provider call. Run it after a change to *Establish
  the situation*, *Draw the map* or *Close the session*, to `references/drawing-the-map.md` or to
  either template.
- **The router — scenarios 1, 2, 3.** Ten minutes and one provider call each. Run them after a change
  to *Choose the door*, *Operations on the map* or `references/slice-rules.md`, where the router and
  the five operations live.

`references/slice-rules.md` is read on every session, so a change to it shows in both halves and the
router is the cheaper place to see it. *Hand over a ready row* shows in whichever half you run, and
only if the session gets as far as handing a row over.

Run either after a change you believe is substantive, not after every commit. One run is a question;
the same run twice with the same answer is a verdict. What the net does not cover, and how narrow the
sample is, is in [`README.md`](README.md).

## Before any session

**Authorization is required and is not implied by this document.** [`../AGENTS.md`](../AGENTS.md)
binds: report the exact external-call count and get explicit approval before sending a single provider
request. Approval of a plan is not approval to send.

**Install the skill you mean to review.** `make add` copies the payload into `~/.agents/skills/` and
the agent reads the copy; skip it and you are reviewing the version before your change. Restart the
session afterwards, and check the copy is the one you expect:

```bash
diff -r skills/roadmap ~/.claude/skills/roadmap --exclude=.claude && echo "installed copy matches"
```

`~/.claude/skills/roadmap` is a symlink to that copy. If `make add` fails on `~/.npm` permissions, it
is the sandbox — rerun it outside.

**The skill is invoked explicitly**, as `/roadmap`: the frontmatter sets `disable-model-invocation:
true`, and dropping the prefix means reviewing the model instead of the skill.

**Model and effort are set in the session, never in the prompt.** Check what the session actually says
before sending, and write down what it said rather than what you intended.

**Every run gets its own directory** under `recipe-app/results/`, and the session is pointed at that
directory as if it were the project. Never point a session at `reference-roadmap/` or at `fixtures/`:
both are frozen and a session writes.

**Every run directory keeps a `PROMPT.md`** with the exact text sent, every answer given back, and the
model and harness it ran on — written from what the session received, not from the card. A run driven
another way is still evidence, but only if the adaptation is readable.

**And it keeps the session itself**, as `TRANSCRIPT.jsonl`. Half the rules have no artifact in
`.roadmap/` — what the session asked, what it declined to write, what it put to the author — and
against a run without one they are inconclusive by construction rather than green. Step 5 below says
when and how; a run that skips it is half a net, and says so.

**What a session may read** is `sources/` and its own copy of `.roadmap/`; the prompt says so.
Off limits in particular: `reference-roadmap/` and `REFERENCE-NOTES.md`, `EVALUATION-RULES.md`,
`EVALUATION-BRIEF.md` and `recipe-app/SCENARIOS.md`, which are the answer keys — the cards carry the
router verdicts outright — and the whole of `design/roadmap/`, which argues the reasoning behind
them.

## Producing a run

1. **Copy the card's starting state** into this run's directory, with the command the card gives.
   Scenario 0 starts from an empty directory.
2. **Send the card's prompt**, with this run's directory substituted. What it carries beyond the
   request is the read restriction: the sources as the only input, no search ranging over the rest of
   the repository, and the same restriction on anything the session delegates to.
3. **Answer what it asks and nothing else.** *Establish the situation* obliges the session to ask
   what was delivered — the only place it is asked — and a tracker cannot answer it; each card says
   what to answer. Answering more turns the run into a collaboration you cannot read.
4. **Confirm only where the card says so.** A first drawing writes unasked — there is no `.roadmap/`
   to lose — and argues with its own first cut in the same session. A map already standing proposes a
   block first: never confirm a proposal that redraws the map, since a redraw you let it write teaches
   nothing the proposal did not already say.
5. **Capture the transcript** — `make capture-transcript RUN=<the run directory>` from a second
   terminal, the moment the session closes on its four-part report and before anything else is typed
   into it. The target copies the newest `.jsonl` under `~/.claude/projects/<this repository>/`, which
   the harness writes as the session runs, so the copy is the run as it stood at the report. **The
   session never captures itself**: asked to, it would write a summary of what it believes it did, and
   an instruction to produce one would spend R-035 — which reads that the session closed on the four
   parts *and nothing else* — in every run after it. Two habits keep the file honest: **one fresh
   session per run**, since `/clear` opens a new file and capturing before it is not optional; and,
   where you carried on typing before remembering, a line in `PROMPT.md` saying where the run ends.
   A sub-agent-driven run captures the driver's session, which carries the sub-agent's turns marked
   `isSidechain: true`. A harness with no such file leaves `/export` inside the session, after the
   report: it costs one turn, spent where there is nothing left to read.
6. **`make validate-roadmap ROADMAP=<the run directory>/.roadmap`** from the repository root —
   structural, deterministic, free. `ROADMAP` is the directory holding `roadmap.md`, not a file. If it
   is red, stop and fix before reading. The session runs the validator itself at *Close the session*
   and its run is not this one: it resolves `.roadmap` against the run directory rather than the
   repository root, so a session that does not change directory first gets nothing — an artifact of
   this layout, not a defect. R-033 reads that it ran at all and what it did with the `WARNING`s.

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
