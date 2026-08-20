# Open verification

What the net has not caught yet. P8 ran the skill five times on 2026-08-20 and closed its ticket;
this is the work those runs left open, written so a session that was not there can execute it. The
second run of router scenario 3 has since been done — it is recorded on R-007 and in
`recipe-app/results/ROUTER-3-CC-2/`, and what it left open is item 1 below.

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

**Item 1 has a narrower intent than the rest.** Two runs have now failed R-007 and the question is no
longer *whether* — it is **where**. Both sessions found the unknown; neither turned it into a spike,
and they failed to by different routes. So item 1 is not *is the skill right about spikes* and no
longer *did one session have a bad day*: it is **which clause stops working, the one that reads the
input or the one that turns the reading into a row**. Lose hold of that and you will sharpen a clause
that is already firing.

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

## 1. R-007 — the third run of router scenario 3

**Cost: one run.** **Buys: the location of a defect whose existence is no longer in question.**

### What happened the first two times

Same fixture, same prompt, two runs, two failures, and they do not look alike.

`ROUTER-3-CC-1` did the split and got the column wrong: it took the unknown out of `S13`, minted it
as `S17` — a row whose `Verification` is nothing but declared numbers and whose `Learning target` is
knowledge — and wrote `kind: enabler` on it, with an `Audience` naming the people building the thing.

`ROUTER-3-CC-2` minted nothing at all. It read the input as work, correctly, then widened `S13` to
carry the corpus: the seed bullet rewritten to thousands of recipes across dozens of uncurated
cookbooks, two observations appended to `Verification`, the `Learning target` rewritten to cover
recall at scale *and* first-page usability, the executor moved to `mixed`. It even argued, in the
block, that the two risks are one row — cohesion reasoning applied to material the map cannot know
yet.

**The overlap hypothesis is dead.** Run two did not mint an enabler, so nothing in
`references/slice-rules.md`'s enabler definition has earned a rewrite, and the temptation to sharpen
it should be treated as the thing that survived a falsification attempt and lost.

### The hypothesis to falsify

What the two runs share is not the mistake, it is the half that worked. Both sessions **found** the
unknown and named it as an unknown — run one in its own row, run two in the middle of its own
proposal. Neither carried that finding into the `Kind` column or into the decision to split.

The suspicion is that **the reading fires and the routing does not**: the spike test in
`references/slice-rules.md` tells a session how to recognise a spike, and § 2 of `SKILL.md` tells it
that the reading needs no question — but neither says *the recognised unknown leaves the row it was
found in*. Run two's cohesion argument is what a session does when nothing stops it.

**Do not act on the suspicion before the third run.** A hypothesis that explains two failures is
exactly the kind that survives on the strength of its own tidiness.

### Setup

```bash
mkdir -p evals/roadmap/recipe-app/results/ROUTER-3-CC-3/.roadmap
cp -R evals/roadmap/recipe-app/fixtures/redrawn/. evals/roadmap/recipe-app/results/ROUTER-3-CC-3/.roadmap/
make validate-roadmap ROADMAP=evals/roadmap/recipe-app/results/ROUTER-3-CC-3/.roadmap
```

The same fixture again, and nothing about the skill changed in between. A third run against an edited
skill answers a different question and cannot be composed with the first two.

### The prompt

Take `results/ROUTER-3-CC-2/PROMPT.md` verbatim and change `ROUTER-3-CC-2` to `ROUTER-3-CC-3`
throughout. Change nothing else. Both previous runs were driven through a general-purpose sub-agent
with an empty context; drive it any other way and you are not running it again.

### The answers to give

- **When it asks what was delivered:** *Nothing since the redraw.* Nothing more, whatever else it
  attached to the question — both runs so far attached something.
- **Then confirm once**, and run `make validate-roadmap` on the run directory.

### What to read, in this order

1. Does the unknown end up in a row of its own, or inside `S13`?
2. If it has its own row, what is in the `Kind` column?
3. Did the session say anywhere that it recognised an unknown? That sentence is the evidence for the
   hypothesis above, and it is in the transcript rather than in the files.

### What each outcome means

| Run three | Verdict | What to do |
|---|---|---|
| `kind: spike`, empty `Audience`, `S13` depends on it | One correct in three, on a scenario built to be unambiguous | The clause is weak rather than absent. Record it and stop: a coin-flip is not a location |
| No new row; `S13` widened again | The routing is where it fails | Two of three by the same route, and the fix lands in `references/slice-rules.md`, *The spike test* — what the recognised unknown obliges, not how to recognise it. Never in `SKILL.md` § 2, which is doing its half |
| A new row with a wrong `Kind` again | The column is where it fails, and the overlap comes back into play | Then and only then reopen the enabler boundary in `references/slice-rules.md` |

Whatever you write, re-run the scenario a fourth time against it. A rule change with no run behind it
is a guess, and this rule has now cost three.

## 2. R-034 has never been asked for

**Cost: one run, on top of an existing state.** **Buys: the only deliberate reading of § 6 there will
have been.**

No prompt has ever asked for a row to be handed over. One session has since volunteered a fragment:
`ROUTER-3-CC-2` closed by saying no row was pickable — `S13`, `S14` and `S15` all `ready` but all
depending on an undelivered `S12` — and then derived, unasked, `ready` + `mixed` → `ready-for-human`
with `/grill-with-docs` before `/to-spec`. Both halves correct. That is one row, one kind, one
executor pair, arrived at by accident, and it leaves the rest of the paragraph — the routing of a
spike, the `/to-spec` exception for an already-clarified slice, the refusal to hand over anything not
`ready` — still unread.

This is the largest hole in the net, and no scenario in `REVIEW-WORKFLOW.md` covers it. Closing it
means **writing a fourth scenario**, not just running one. It needs to hold at least:

- a `ready` + `agent` row and a `ready` + `human` row, so the label is derived twice and differently;
- one row that is `needs-decision`, which must not be handed over at all;
- one spike, which must go to `/prototype` or `/wayfinder` and never to `/to-spec`;
- a slice with no recorded clarification, which owes `/grill-with-docs` rather than `/to-spec`.

`fixtures/mid-flight/` already carries `ready` rows of both executors and a `needs-decision` row, so
three of the four are covered. **The fourth is not: no fixture holds an open spike** — `S2` is a
spike and it is in `archive/`, and `redrawn/` has none either. Either the scenario runs on a state
frozen from a run that minted one, the way `redrawn/` itself was made, or it says out loud that the
spike half of § 6 stays unread. What is new is the author's opening sentence — something like *give
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
