# REDRAW-CC-1 — what was sent

**Date:** 2026-08-20 · **Model:** claude-opus-5 · **Effort:** session default
**Harness:** Claude Code, driven through a general-purpose sub-agent with an empty context. See
[`../README.md`](../README.md) for what that changes and what it costs.

**Starting state:** `fixtures/mid-flight/`

```bash
mkdir -p evals/roadmap/recipe-app/results/REDRAW-CC-1/.roadmap
cp -R evals/roadmap/recipe-app/fixtures/mid-flight/. evals/roadmap/recipe-app/results/REDRAW-CC-1/.roadmap/
```

**This run is not one of the three router scenarios.** It exists because `fixtures/redrawn/` cannot
be derived from the first drawing — a redraw is another map — and `design/roadmap/PLAN.md` rules out
hand-writing it. Its output was frozen as that fixture, unedited. It is also the only run in this
directory that exercises the redraw rules, R-018.

## Turn 1 — the prompt

> You are running the `roadmap` skill explicitly, as if the user had typed `/roadmap`. Do this first,
> before anything else:
>
> Try to invoke it with the Skill tool: skill name `roadmap`. If that tool call fails or the skill is
> not available to you, instead read `~/.claude/skills/roadmap/SKILL.md` and follow it as your
> operating instructions, loading its `references/` and `assets/` files exactly as it tells you to.
> That installed copy is the skill payload.
>
> Then, the request:
>
> Treat evals/roadmap/recipe-app/results/REDRAW-CC-1/ as the project root; the roadmap is in its
> .roadmap/, and the documents it names as sources are in evals/roadmap/recipe-app/sources/. **Where
> this thing is going has changed, and I have decided it: it is not a private cookbook for family and
> friends any more. I want public thematic cookbooks that anybody can find and read without an
> account, and I want search to work across the whole public corpus, not inside one cookbook.
> Discovery is the product now; the private cookbook stays as a mode, not as the point.** Read
> nothing else in this repository, in this session or in any session you delegate to: everything else
> under evals/ and under design/ is off limits.
>
> Hard constraints on this session, on top of whatever the skill says:
>
> - The only repository files you may read are `evals/roadmap/recipe-app/results/REDRAW-CC-1/.roadmap/`
>   and its contents, and the four documents under `evals/roadmap/recipe-app/sources/`. Everything
>   else under `evals/` and under `design/` is off limits — in particular do not look for, list, or
>   open anything named `reference-roadmap`, `fixtures`, `EVALUATION-*`, `REVIEW-WORKFLOW`, or
>   anything under `design/`. Do not run `find`, `ls -R`, `grep` or any search that would range over
>   those directories. Reading the skill payload under `~/.claude/skills/roadmap/` is expected and
>   allowed.
> - Do not delegate to sub-agents.
> - **The goal change is a decision already taken, not a question. Do not ask me whether the
>   destination has moved; it has. Anything else the skill tells you to ask, ask.**
> - Nothing is written until the author has confirmed one block of changes. Honour that literally. If
>   the skill tells you to ask the author something, STOP and return the question as your final
>   answer without writing anything — I will answer, and you continue. When you reach a proposed
>   block of changes, STOP and return it without writing any file; I will confirm, and only then do
>   you write and run the validator.
>
> Your final answer for this turn is whatever the skill has you put to the author at the point you
> stop — a question, or the proposed block. Nothing else.

The bolded line about the goal being settled is specific to this run: the router's job is to decide
whether an input moves the destination, and here the destination was named as already moved so that
the redraw branch could be reached at all. That makes this run useless as evidence about § 2 routing,
and it is the reason it is not one of the three scenarios.

The session asked what had been delivered, as § 1 requires.

## Turn 2 — the answer given

> All eight are done — `S4` through `S11`. None of them produced a decision that clears the ADR bar.

Chosen to put every row into `archive/`, so the frozen fixture has the shape scenario 3 needs: a
finished map behind it, and a high-water mark the next id counts from.

## Turn 3 — the answer given

> Confermo.
