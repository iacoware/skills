# ROUTER-3-CC-3 — what was sent

**Date:** 2026-08-21 · **Model:** claude-opus-5[1m] · **Effort:** session default
**Harness:** Claude Code, driven through a general-purpose sub-agent with an empty context. See
[`../README.md`](../README.md) for what that changes and what it costs.

**The model id is not the one the first two runs carry.** `ROUTER-3-CC-1` and `ROUTER-3-CC-2` are
recorded as `claude-opus-5`; this session says `claude-opus-5[1m]`, the same model with the 1M
context window. Written down rather than smoothed over: everything else — fixture, prompt, answers,
sub-agent driving — is identical, and this is the one axis on which the three runs are not the same
run.

**Starting state:** `fixtures/redrawn/` — the same state `ROUTER-3-CC-1` and `ROUTER-3-CC-2` ran on.

```bash
mkdir -p evals/roadmap/recipe-app/results/ROUTER-3-CC-3/.roadmap
cp -R evals/roadmap/recipe-app/fixtures/redrawn/. evals/roadmap/recipe-app/results/ROUTER-3-CC-3/.roadmap/
```

The directory was verified byte-identical to the fixture and validator-green before the prompt was
sent, and `skills/roadmap/` was verified byte-identical to `~/.claude/skills/roadmap/`.

This is `ROUTER-3-CC-2`'s prompt verbatim with `ROUTER-3-CC-2` changed to `ROUTER-3-CC-3` throughout
and nothing else touched — the third run [`../../../OPEN-VERIFICATION.md`](../../../OPEN-VERIFICATION.md)
asked for, to locate a defect two runs had already established.

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
> Treat evals/roadmap/recipe-app/results/ROUTER-3-CC-3/ as the project root; the roadmap is in its .roadmap/,
> and the documents it names as sources are in evals/roadmap/recipe-app/sources/. **Search has to work on the public corpus — thousands of recipes across cookbooks nobody curated together.** Read
> nothing else in this repository, in this session or in any session you delegate to: everything else
> under evals/ and under design/ is off limits.
>
> Hard constraints on this session, on top of whatever the skill says:
>
> - The only repository files you may read are `evals/roadmap/recipe-app/results/ROUTER-3-CC-3/.roadmap/` and
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

The session asked what had been delivered, and attached a second question to it — whether *cookbooks
nobody curated together* settles the map's open question about who has the right to publish, laying
out two readings and what each would change. Only the first was answered, as in `ROUTER-3-CC-1` and
`ROUTER-3-CC-2`; see the note on R-005 in `../../EVALUATION-RULES.md`. This is the fifth run in a row
to attach one.

## Turn 2 — the answer given

> Nothing since the redraw.

## Turn 3 — the answer given

> Confermo.

## What came back

**A new row, minted `kind: enabler`.** The session read the input as work, kept the goal untouched,
declined to settle the publishing-rights question, and split the corpus out of `S13` into a new row
`S17` — *Corpus pubblico alla scala dichiarata* — `kind: enabler`, `needs-decision`, `mixed`,
`Depends on: S12`, with `S13` gaining `S17` in its own `Depends on`. It also rewrote `S13`'s first
`Includes` bullet to consume that corpus, moved its `Learning target` from *scale* to
*heterogeneity*, rewrote its `Verification` around a second query list written by looking at the
corpus, killed the duplicates line in `Assumptions` — its condition, *finché il corpus è piccolo*,
being what the input contradicts — narrowed the scale assumption, and extended both `Open questions`
without answering either.

`S17` is a spike everywhere except the column: its `Learning target` is knowledge — *se un corpus
della scala dichiarata si può costruire con il motore consegnato e dentro il budget dichiarato* —
and its `Verification` is nothing but declared numbers. Its `Audience` is filled, and names the
people building the thing.

**Where it differs from `ROUTER-3-CC-1`**, which also split and also wrote `enabler`: the row is not
the same row. `CC-1`'s `S17` builds a test-bench corpus so that `S13`'s measurement means something;
`CC-3`'s `S17` builds the production corpus, unattended and costed. In both, what stayed inside
`S13` is the measurement the scenario says is the unknown — recall and latency for a shared index at
that volume. No run so far has minted the spike the scenario describes.

The session volunteered one push-back before confirmation: that the skill's ordering guidance calls a
seed corpus *"una riga di `Includes`"*, and that it was contradicting that default deliberately. It
offered to fold `S17` back into `S13` if the author disagreed. Nothing was answered beyond
`Confermo.`

`make validate-roadmap` on this directory is green, from the repository root and from the session's
own run at § 5. The session reported no `WARNING` and put the six-row count against the cap
explicitly. The verdict this run produces is on R-007 in `../../EVALUATION-RULES.md`.
