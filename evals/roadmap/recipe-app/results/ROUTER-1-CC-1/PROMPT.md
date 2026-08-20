# ROUTER-1-CC-1 — what was sent

**Date:** 2026-08-20 · **Model:** claude-opus-5 · **Effort:** session default
**Harness:** Claude Code, driven through a general-purpose sub-agent with an empty context. See
[`../README.md`](../README.md) for what that changes and what it costs.

**Starting state:** `fixtures/mid-flight/`

```bash
mkdir -p evals/roadmap/recipe-app/results/ROUTER-1-CC-1/.roadmap
cp -R evals/roadmap/recipe-app/fixtures/mid-flight/. evals/roadmap/recipe-app/results/ROUTER-1-CC-1/.roadmap/
```

## Turn 1 — the prompt

> You are running the `roadmap` skill explicitly, as if the user had typed `/roadmap`. Do this
> first, before anything else:
>
> Try to invoke it with the Skill tool: skill name `roadmap`. If that tool call fails or the skill
> is not available to you, instead read `~/.claude/skills/roadmap/SKILL.md` and follow it as your
> operating instructions, loading its `references/` and `assets/` files exactly as it tells you
> to. That installed copy is the skill payload.
>
> Then, the request:
>
> Treat evals/roadmap/recipe-app/results/ROUTER-1-CC-1/ as the project root; the roadmap is in its .roadmap/,
> and the documents it names as sources are in evals/roadmap/recipe-app/sources/. **Search has to work across every cookbook I belong to, not just the current one.** Read
> nothing else in this repository, in this session or in any session you delegate to: everything else
> under evals/ and under design/ is off limits.
>
> Hard constraints on this session, on top of whatever the skill says:
>
> - The only repository files you may read are `evals/roadmap/recipe-app/results/ROUTER-1-CC-1/.roadmap/` and
>   its contents, and the four documents under `evals/roadmap/recipe-app/sources/`. Everything else
>   under `evals/` and under `design/` is off limits — in particular do not look for, list, or
>   open anything named `reference-roadmap`, `fixtures`, `EVALUATION-*`, `REVIEW-WORKFLOW`, or
>   anything under `design/`. Do not run `find`, `ls -R`, `grep` or any search that would range
>   over those directories. Reading the skill payload under `~/.claude/skills/roadmap/` is expected
>   and allowed.
> - Do not delegate to sub-agents.
> - Nothing is written until the author has confirmed one block of changes. Honour that literally. If
>   the skill tells you to ask the author something, STOP and return the question as your final
>   answer without writing anything — I will answer, and you continue. When you reach a proposed
>   block of changes, STOP and return it without writing any file; I will confirm, and only then do
>   you write and run the validator.
>
> Your final answer for this turn is whatever the skill has you put to the author at the point you
> stop — a question, or the proposed block. Nothing else.

The session asked what had been delivered, as § 1 requires.

## Turn 2 — the answer given

> Nothing since the last session.

The scenario prescribes this answer, and nothing more. The session then returned the block.

## Turn 3 — the answer given

> Confermo.
