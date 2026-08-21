# Open verification

What the net does not catch, and how to conclude from a run that it did or did not.

**This file carried four things to go and do, was cut to two on 2026-08-21, and is down to one.**
Closing a hole kept opening the next one while the skill had still never been used on a real project,
and the net exists to protect something real use has not yet appraised. The two that went in the cut
are recorded below as holes, so that nobody re-derives them as tasks; the third closed the same day —
R-007's third run of router scenario 3, whose verdict now lives on R-007 in `EVALUATION-RULES.md` and
whose record says not to run a fourth.

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

**The item below is different: it finishes work already begun**, and it costs nothing but a person.

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

**Half the evidence is not in the files.** What the session asked, what it declined to write, and
what it put to the author are evidence exactly as much as what it wrote. Several checks have no artifact at all. If you only read
the diff, you are reading the smaller half.

**A conclusion may be *inconclusive*, and saying so is a result.** A run that half-does the thing is
not a red check and not a green one. Record what it did and what it did not, cite the rule id, and
leave the mark off. Forcing an ambiguous run into a verdict is how a rule acquires a failure record
it did not earn — and the next reviewer will act on that record without re-reading the run.

**Know the width of your sample.** Everything recorded so far is one model family — `claude-opus-5`,
and once its 1M-context variant — one harness, one scenario, `recipe-app`. A conclusion about the
skill drawn from it is a conclusion about the skill *as read by that model on that scenario*. That is
still worth having; it is just not the same sentence.

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

## The real invocation path is still unverified

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
  grows stops being read — this one went from four to two to one in a single day.

And the rule that governs all of it: **a defect lands in the phase that owns it**, never in
`SKILL.md` by default. A rule applied badly is P4. A field nobody can fill is P2. The map of phases is
[`../../design/roadmap/PLAN.md`](../../design/roadmap/PLAN.md).
