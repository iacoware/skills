# Open verification

What the net does not catch, and how to conclude from a run that it did or did not.

**This file carried four things to go and do, and on 2026-08-21 it was cut to two.** Closing a hole
kept opening the next one while the skill had still never been used on a real project, and the net
exists to protect something real use has not yet appraised. The two that survive finish work already
started; the two that went are recorded below as holes, so that nobody re-derives them as tasks.

Read [`REVIEW-WORKFLOW.md`](REVIEW-WORKFLOW.md) and [`EVALUATION-RULES.md`](EVALUATION-RULES.md)
first — those give the procedure and the checks, this gives the epistemics. You are the
**reviewer**: everything in this repository is open to you, including the oracle and the brief. What
must stay blind is the session you drive, and § *Before any session* of the workflow says how.

## The intent

**The eval exists to notice that a change to `SKILL.md` improved one thing and broke another.** It is
not here to prove the skill is good, and it produces no score. A skill made of prose has no compiler:
the only thing standing between a clause that got sharpened and a clause that quietly stopped firing
is somebody running it and reading what came out.

That is also why a hole in the net is not neutral: it is a change nobody will notice. Knowing where
the holes are is what keeps a green run from meaning more than it does.

**Two holes were left open on purpose on 2026-08-21**, and are stated here as facts rather than as
work, so that a reviewer knows the width of what a green run means and does not turn them back into
tasks:

- **§ 6 has never been asked for.** No prompt has requested a handover, and no fixture holds an open
  spike to route — covering it means a fourth scenario *and* a new frozen state. One session
  volunteered a correct fragment; see R-034. Left open because real use exercises handover the first
  time an author asks for a row to pick up.
- **Codex has never run this skill.** `agents/openai.yaml`, its `default_prompt`, and
  `allow_implicit_invocation: false` are unexercised. Left open because the second harness matters
  when somebody uses it, and nobody does yet.

What reopens either is a change to `SKILL.md` that real use asked for and that would have fallen
through the hole — never the hole itself. A net is worth extending when there is something it would
have caught.

**The two items below are different: they finish work already begun**, and both are cheap. Item 1 is
one run and is bounded — it records and stops. Item 2 costs nothing but a person.

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
3. *The clause is stated but says two things that overlap.* It reads like a model failure and is a
   writing failure. It needs two runs before it is anything at all.

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

**Know the width of your sample.** Everything recorded so far is one model, one harness, one
scenario, `recipe-app`. A conclusion about the skill drawn from it is a conclusion about the skill *as read by
that model on that scenario*. That is still worth having; it is just not the same sentence.

## Before any run

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

Those commands are idempotent: the directory may already be sitting there, prepared and green, and
re-running them changes nothing. The installed copy was reinstalled and verified identical on
2026-08-21 — check it again anyway, § *Before any run* says how.

The same fixture again, and nothing a session reads changed in between: the payload moved once on
2026-08-21, and only in `scripts/` (an exported constant and its tests). `SKILL.md`, `references/`
and `assets/` are byte-identical to what runs one and two saw. A third run against an edited skill
answers a different question and cannot be composed with the first two.

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

**This run is bounded: record the verdict and stop.** Whatever the table says, do not change the
skill on the strength of it and do not run a fourth time. The reading rows above name where a fix
would land if one is ever written; what licenses writing it is real use hitting the same wall, not
this scenario's record. R-007 has already cost two runs and it is not the skill's most expensive
open question — that a real project has never used the skill is.

## 2. The real invocation path is still unverified

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
- **In this file**, by deleting the item you closed, and without adding one. An open list that only
  grows stops being read — this one was cut from four to two once already.

And the rule that governs all of it: **a defect lands in the phase that owns it**, never in
`SKILL.md` by default. A rule applied badly is P4. A field nobody can fill is P2. The map of phases is
[`../../design/roadmap/PLAN.md`](../../design/roadmap/PLAN.md).
