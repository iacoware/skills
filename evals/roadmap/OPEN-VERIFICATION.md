# Open verification

What the net has not caught yet. P8 ran the skill five times on 2026-08-20 and closed its ticket;
this is the work those runs left open, written so a session that was not there can execute it.

Read [`REVIEW-WORKFLOW.md`](REVIEW-WORKFLOW.md) and [`EVALUATION-RULES.md`](EVALUATION-RULES.md)
first — this file gives the tasks, those two give the procedure and the checks. You are the
**reviewer**: everything in this repository is open to you, including the oracle and the brief. What
must stay blind is the session you drive, and § *Before any session* of the workflow says how.

Ordered by what they buy per provider call. Item 1 is the one to do first.

## The intent

**The eval exists to notice that a change to `SKILL.md` improved one thing and broke another.** It is
not here to prove the skill is good, and it produces no score. A skill made of prose has no compiler:
the only thing standing between a clause that got sharpened and a clause that quietly stopped firing
is somebody running it and reading what came out.

That is why the items below are worth provider calls at all. Each one is a place where the net
currently has a hole, and a hole in the net is not neutral — it is a change nobody will notice.

Two of them, 1 and 2, are about the skill's reading. Two, 3 and 4, are about whether the skill loads
and stays inert until invoked. Both kinds matter and they fail differently: a bad reading produces a
map you have to argue with, a bad invocation produces a roadmap redrawn because an agent thought it
was being helpful.

**Item 1 has a narrower intent than the rest.** It is not asking *is the skill right about spikes*. It
is asking one question with two answers: **did the skill stop distinguishing a spike from an enabler,
or did one session have a bad day?** Nothing you do below is worth anything if you lose hold of that
distinction, because the two call for opposite responses — one is a clause to sharpen, the other is a
clause to leave alone.

## How to draw a conclusion

The rules that govern this are in `EVALUATION-RULES.md`; what follows is how to apply them when a run
is in front of you and it is tempting to conclude too much.

**One run is a question. Two runs that agree are a verdict.** This is the whole epistemics and
everything else follows from it. A single red check tells you a session did something once. It does
not tell you the skill causes it, because the generator is not deterministic and never will be.

**A red check is not permission to edit the skill.** Before touching a clause, ask which of these
three you are looking at:

1. *The skill states the clause and the session ignored it.* One run: record and stop. Two runs:
   the clause is not doing its job, and the fix goes where the clause lives.
2. *The skill no longer states the clause the check names.* **Then the defect is in the check.**
   Rewrite it or delete it. The rules describe the skill; they do not govern it, and a check that
   outlives its clause turns into a rule nobody voted for.
3. *The clause is stated but says two things that overlap.* This is item 1's suspect. It reads like
   a model failure and is a writing failure. It needs two runs before it is anything at all.

**Never change the skill to make a scenario pass.** This is the failure mode that quietly destroys an
eval: the reviewer's sense of *good* drifts toward whatever the model last produced, and the net ends
up shaped like the thing it was supposed to catch. The same holds for the fixtures and for the
oracle. A fixture moves when the state it stands for moves. The oracle is rewritten when the sources
change, never because a candidate argued well.

**Half the evidence is not in the files.** The skill is a conversation that ends in one proposed
block, so what the session asked, what it declined to write, and what it put to the author are
evidence exactly as much as what it wrote. Several checks have no artifact at all. If you only read
the diff, you are reading the smaller half.

**A conclusion may be *inconclusive*, and saying so is a result.** A run that half-does the thing is
not a red check and not a green one. Record what it did and what it did not, cite the rule id, and
leave the mark off. Forcing an ambiguous run into a verdict is how a rule acquires a failure record
it did not earn — and the next reviewer will act on that record without re-reading the run.

**Know the width of your sample.** Everything below is one model, one harness, one scenario,
`recipe-app`. A conclusion about the skill drawn from it is a conclusion about the skill *as read by
that model on that scenario*. That is still worth having; it is just not the same sentence.

## Before any of them

**Authorization is required and is not implied by this document.** [`../AGENTS.md`](../AGENTS.md)
binds: report the exact external-call count and get explicit approval before sending a single
provider request. Approval of a plan is not approval to send.

**Check the installed copy is the one you mean to review.** `make add` copies the payload into
`~/.agents/skills/`, and `~/.claude/skills/roadmap` is a symlink to it. Verify before running:

```bash
diff -r skills/roadmap ~/.claude/skills/roadmap --exclude=.claude && echo "installed copy matches"
```

If `make add` fails on `~/.npm` permissions, it is the sandbox — rerun it outside.

## 1. R-007 — the second run of router scenario 3

**Cost: one run.** **Buys: a verdict instead of a question**, on the only check that went red with a
named suspect behind it.

### What happened the first time

The session read the input correctly and found the unknown. It took that unknown out of `S13`, which
could not carry it, and minted it as a new row — then wrote `kind: enabler` on it. Read
`recipe-app/results/ROUTER-3-CC-1/.roadmap/slices/S17-corpus-di-partenza.md`: its
`Verification` is nothing but declared numbers, its `Learning target` is knowledge, and its
`Audience` names the people building the thing. Those are a spike's properties. Only the column
disagreed.

### The hypothesis to falsify

`references/slice-rules.md` defines `enabler` as a row that, among other things, *resolves one
material uncertainty* and *may include the smallest diagnostic consumer needed to observe its
uncertainty*. The spike test in the same file keys on the honest `Verification` stating a
measurement. A row that resolves one material uncertainty and verifies by measurement satisfies the
opening of both. The suspicion is that the overlap is what pulled the column. **Do not act on the
suspicion before the second run** — if run two mints a spike, there is nothing to fix and the
overlap is doing no harm.

### Setup

```bash
mkdir -p evals/roadmap/recipe-app/results/ROUTER-3-CC-2/.roadmap
cp -R evals/roadmap/recipe-app/fixtures/redrawn/. evals/roadmap/recipe-app/results/ROUTER-3-CC-2/.roadmap/
make validate-roadmap ROADMAP=evals/roadmap/recipe-app/results/ROUTER-3-CC-2/.roadmap
```

The fixture must be the same one. A second run on a different starting state answers a different
question.

### The prompt

Take `results/ROUTER-3-CC-1/PROMPT.md` verbatim and change `ROUTER-3-CC-1` to `ROUTER-3-CC-2`
throughout. Change nothing else — not the author's opening sentence, not the read restriction, not
the hard constraints. **If you drive it any other way than the first run was driven, you are not
running it again**, you are running something else, and the two results do not compose.

Record the new `PROMPT.md` as the workflow requires, including the model and effort the session
actually reports.

### The answers to give

- **When it asks what was delivered:** *Nothing since the redraw.* Nothing more, whatever else it
  attached to the question.
- **Then confirm once**, and run `make validate-roadmap` on the run directory.

### What to read, in this order

1. Does the session mint a new row for the unknown at all, or does it widen `S13`?
2. If it mints one, what is in the `Kind` column?
3. Is the row's `Verification` a measurement, and is its `Audience` empty or filled?

### What each outcome means

| Run two | Verdict | What to do |
|---|---|---|
| `kind: spike`, empty `Audience`, `S13` depends on it | R-007 went red once and green once | Note both on the R-007 record. No change to the skill. One bad day, not a defect |
| `kind: enabler` again, on a row with a spike's verification | R-007 is a verdict | The defect is in **P4**, `references/slice-rules.md`. Sharpen the boundary so a row cannot satisfy the opening of both — see below |
| No new row; `S13` widened to carry the corpus | A different failure | This is the failure scenario 3 names in its own text. Record it against R-007 and say which of the two it was |

If the verdict is the third row of that table, the fix is not obvious and must not be improvised. The
enabler and the spike genuinely overlap in the world, and the rule that separates them is *does
anything survive the row that somebody else consumes*. Whatever you write, it lands in
`references/slice-rules.md` and nowhere else — never in `SKILL.md` because that is where it showed
up. Then re-run this scenario a third time; a rule change with no run behind it is a guess.

## 2. R-034 has no evidence at all

**Cost: one run, on top of an existing state.** **Buys: the only reading of § 6 there has ever been.**

No session has reached § 6. The five runs of P8 produced 18 rows with `readiness: ready` between
them, and not one prompt asked for a row to be handed over, so that whole paragraph — the derived
`triage` label, the routing by kind, the refusal to send a spike to `/to-spec` — has never been read
by anything.

This is the largest hole in the net, and no scenario in `REVIEW-WORKFLOW.md` covers it. Closing it
means **writing a fourth scenario**, not just running one. It needs to hold at least:

- a `ready` + `agent` row and a `ready` + `human` row, so the label is derived twice and differently;
- one row that is `needs-decision`, which must not be handed over at all;
- one spike, which must go to `/prototype` or `/wayfinder` and never to `/to-spec`;
- a slice with no recorded clarification, which owes `/grill-with-docs` rather than `/to-spec`.

`fixtures/mid-flight/` already carries `ready` rows of both executors and a `needs-decision` row, so
the state may not need to be new. What is new is the author's opening sentence — something like *give
me the next thing I can actually pick up* — and the verdict it is read against.

Write the scenario into `REVIEW-WORKFLOW.md` beside the other three before running it. A scenario
invented after the result is not a scenario.

## 3. Codex has never run this skill

**Cost: one run per half you care about.** **Buys: evidence that the second harness works at all.**

Every run so far was Claude Code. `skills/roadmap/agents/openai.yaml` sets
`allow_implicit_invocation: false` and carries a `display_name`, a `short_description` and a
`default_prompt` that nothing has ever exercised. `REVIEW-WORKFLOW.md` already holds the `$roadmap`
prompts; the directories are `ROADMAP-CX-<N>` and `ROUTER-<n>-CX-<N>`.

Two things are worth knowing and only one is about the skill's reading:

- that the payload loads and the skill runs to a proposal on Codex at all;
- that it does **not** activate on its own — which is what `allow_implicit_invocation: false` is for,
  and which is tested by a session that never types the `$` prefix and must then come out without the
  skill.

The second is cheaper and catches the failure that matters more: a roadmap redrawn because an agent
thought it was being helpful.

## 4. The real invocation path is still unverified

**Cost: nothing, if a person does it once.**

The P8 runs were driven through sub-agents, which cannot type `/roadmap`; they were told to call the
skill by name and to fall back to reading `~/.claude/skills/roadmap/SKILL.md`. That is written up in
`recipe-app/results/README.md`. It leaves one thing untested: that a real author typing `/roadmap`
into an interactive session gets the payload loaded, with `disable-model-invocation: true` set.

Nothing needs to be recorded for this beyond a line saying it was done. One interactive session, any
prompt, stopped as soon as the skill is clearly loaded.

## Recording what you find

A run that changes nothing still changed the record. Put the result where the next reviewer will hit
it:

- **On the rule**, in `EVALUATION-RULES.md`, as a `⚠ Has failed` mark carrying the run and the date,
  or as a second date on a mark that is already there. A check that went green on the second run
  keeps its mark and gains the green — the history is the point.
- **In the run directory**, as `PROMPT.md`. Non-negotiable, and the workflow says so.
- **In this file**, by deleting the item you closed. An open list that only grows stops being read.

And the rule that governs all of it: **a defect lands in the phase that owns it**, never in
`SKILL.md` by default. A rule applied badly is P4. A field nobody can fill is P2. The map of phases is
[`../../design/roadmap/PLAN.md`](../../design/roadmap/PLAN.md).
