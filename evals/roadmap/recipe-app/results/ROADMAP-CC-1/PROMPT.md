# ROADMAP-CC-1 — what was sent

**Date:** 2026-08-20 · **Model:** claude-opus-5 · **Effort:** session default
**Harness:** Claude Code, driven through a general-purpose sub-agent with an empty context. See
[`../README.md`](../README.md) for what that changes and what it costs.

## Turn 1 — the prompt

> You are running the `roadmap` skill explicitly, as if the user had typed `/roadmap`. Do this first,
> before anything else:
>
> Try to invoke it with the Skill tool: skill name `roadmap`. If that tool call fails or the skill is
> not available to you, instead read `~/.claude/skills/roadmap/SKILL.md` and follow it as your
> operating instructions, loading its `references/` and `assets/` files exactly as it tells you to.
> That installed copy is the skill payload; it is byte-identical to the one in this repository.
>
> Then, the request:
>
> Read the markdown documents in evals/roadmap/recipe-app/sources/, starting from
> evals/roadmap/recipe-app/sources/goal.md, and draw the roadmap that reaches the goal they state.
> Treat evals/roadmap/recipe-app/results/ROADMAP-CC-1/ as the project root: write the map to
> evals/roadmap/recipe-app/results/ROADMAP-CC-1/.roadmap/. Read nothing else in this repository, in
> this session or in any session you delegate to: the sources are the only input, and everything else
> under evals/ and under design/ is off limits.
>
> Hard constraints on this session, on top of whatever the skill says:
>
> - The only repository files you may read are the four documents under
>   `evals/roadmap/recipe-app/sources/` and, later, the files you yourself write under
>   `evals/roadmap/recipe-app/results/ROADMAP-CC-1/`. Everything else under `evals/` and under
>   `design/` is off limits — in particular do not look for, list, or open anything named
>   `reference-roadmap`, `EVALUATION-*`, `REVIEW-WORKFLOW`, or anything under `design/`. Do not run
>   `find`, `ls -R`, `grep` or any search that would range over those directories. Reading the skill
>   payload under `~/.claude/skills/roadmap/` is expected and allowed.
> - Do not delegate to sub-agents.
> - The skill says nothing is written until the author has confirmed one block of changes. Honour
>   that literally: work through the skill's steps, argue with your own first cut as § 3 requires,
>   and then STOP and return your proposed block of changes as your final answer WITHOUT writing any
>   file yet. Your final answer is what the author reads before confirming. I will reply with the
>   confirmation, and only then do you write the files and run the validator as § 5 says.
>
> Your final answer for this turn should be: the proposed block of changes, in full, exactly as the
> skill's § 5 asks you to present it, plus anything the skill told you to ask the author. Nothing
> else.

The session returned the full block and five questions.

## Turn 2 — the answer given

> Confermo.

Nothing else was answered. § 1 of the workflow says the questions are evidence, and answering them
turns the run into a collaboration that cannot be read.
