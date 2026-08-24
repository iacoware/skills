# `roadmap` evaluation

One structural validator, one human reading list, and four scenarios. Kept to notice that a change to
`skills/roadmap/SKILL.md` improved one thing while breaking another.

**Audience: a human reviewer, or an agent in a review session** — never a generation session. The
oracle, its notes, the brief and the scenario verdicts are the answer key, which is why they live here
and not beside the skill. So is [`../../design/roadmap/WORKFLOWS.md`](../../design/roadmap/WORKFLOWS.md)
§ 3, which answers the three router scenarios outright.

**No automated grader is planned.** Two were built for `plan-slices` and both are retired;
[`../plan-slices/POST-MORTEM-EVALS.md`](../plan-slices/POST-MORTEM-EVALS.md) says why, and the reasons
apply here harder — this skill lives across sessions, so a map is judged in a state some earlier
session produced.

| Path | Role |
|---|---|
| `../../skills/roadmap/scripts/validate_roadmap.ts` | Structural and referential validator. Deterministic, free, one second. |
| `make validate-roadmap ROADMAP=<dir>` | Runs it from the repository root. `ROADMAP` is the directory holding `roadmap.md`, not a file. |
| `REVIEW-WORKFLOW.md` | The procedure: which half to run, the preconditions, producing a run, reading one. Travels to a new scenario unchanged. |
| `EVALUATION-RULES.md` | What to look for, as numbered checks about the skill. Portable too. |
| `recipe-app/SCENARIOS.md` | The four cards: a drawing from nothing, and three inputs that hold the router. Starting state, prompt, answer, verdict. Answer key. |
| `recipe-app/sources/` | The only input a candidate is drawn from. Copied verbatim from `../plan-slices/recipe-app/sources/`: input, not `plan-slices` output. |
| `recipe-app/EVALUATION-BRIEF.md` | Facts about those sources, with citable ids: where the map may differ, what it must leave open, what only looks like a defect, what it must contain. |
| `recipe-app/reference-roadmap/` | The oracle: one good answer, hand-written from the sources before any candidate existed. Taste, not verifiable. Read last. |
| `recipe-app/REFERENCE-NOTES.md` | The reasons the oracle does not publish. Read with it. |
| `recipe-app/fixtures/` | Frozen starting states, and one minimal mutation of the oracle per validator check. |
| `recipe-app/results/` | What the skill produced, one directory per run with the `PROMPT.md` that produced it. Never an input to a session. |
| `../AGENTS.md` | Authorization rules for provider runs. Binding on every generation call. |

Four jobs, no overlap: a **procedure**, **rules** that hold across scenarios, **facts** about this
scenario's sources, and **worked answers** for it. Add a second scenario and only the last two are
written anew. **Nothing is inherited from `evals/plan-slices/`**: the rule ids and the brief's entry
ids start fresh sequences, so `R-004` there and `R-004` here are unrelated — cite the file with the id
when both are open.

**Why both the oracle and the scenarios.** The brief is the reference map with the answer removed —
everything mechanically checkable kept, everything requiring judgement dropped — and what it drops is
the only defence against the reviewer's sense of *good* drifting toward whatever the model last
produced. But the oracle covers one state, the first drawing, which is the only state anybody can
hand-write honestly; the router cards are how the other branch gets read at all, and they are cheap
because a map already standing proposes before it writes.

## What the net does not cover

Two holes are open on purpose, stated as facts rather than as work so that nobody turns them back into
tasks. What reopens either is a change to `SKILL.md` that real use asked for and that would have
fallen through the hole — never the hole itself.

- **§ 6 has never been asked for.** No prompt has requested a handover and no fixture holds an open
  spike to route; covering it means a fifth card *and* a new frozen state. One session volunteered a
  correct fragment unprompted — R-034.
- **Codex has never run this skill.** `../../skills/roadmap/agents/openai.yaml` and its
  `allow_implicit_invocation: false` are unexercised. The second harness matters when somebody uses
  it, and nobody does yet.

**Know the width of the sample too.** Everything recorded so far is one model family — `claude-opus-5`,
once in its 1M-context variant — one harness, one scenario. A conclusion drawn from it is a conclusion
about the skill *as read by that model on that scenario*.

## Language

English, as the rest of the project since 2026-08-06. Three permanent exclusions: `recipe-app/sources/`,
because converting them is a new scenario rather than a translation; `recipe-app/reference-roadmap/`,
because the skill writes in the author's language; and whatever lands under `recipe-app/results/`,
because it is the record of what was generated. Field, column and state names are English everywhere,
including inside the Italian map, and quotations stay in their original language because they are
evidence.
