# `roadmap` evaluation

One structural validator, one human reading list, and four scenarios. Kept to notice that a change to
`skills/roadmap/SKILL.md` improved one thing while breaking another.

**Audience: a human reviewer, or an agent in a review session** — never a generation session. The
oracle, its notes, the brief and the scenario verdicts are the answer key, which is why they live here
and not beside the skill.

| Path | Role |
|---|---|
| `../../skills/roadmap/scripts/validate_roadmap.ts` | Structural and referential validator. Deterministic, free, one second. |
| `make validate-roadmap ROADMAP=<dir>` | Runs it from the repository root. `ROADMAP` is the directory holding `roadmap.md`, not a file. |
| `REVIEW-WORKFLOW.md` | The procedure: which half to run, the preconditions, producing a run, reading one. Travels to a new scenario unchanged. |
| `EVALUATION-RULES.md` | What to look for, as numbered checks about the skill. Portable too. |
| `recipe-app/SCENARIOS.md` | The four cards: a drawing from nothing, and three inputs that hold the router. Starting state, prompt, answer, verdict. Answer key. |
| `recipe-app/sources/` | The only input a candidate is drawn from. |
| `recipe-app/EVALUATION-BRIEF.md` | Facts about those sources, with citable ids: where the map may differ, what it must leave open, what only looks like a defect, what it must contain. |
| `recipe-app/reference-roadmap/` | The oracle: one good answer, hand-written from the sources before any candidate existed. Taste, not verifiable. Read last. |
| `recipe-app/REFERENCE-NOTES.md` | The reasons the oracle does not publish. Read with it. |
| `recipe-app/fixtures/` | Frozen starting states, and one minimal mutation of the oracle per validator check. |
| `recipe-app/results/` | What the skill produced, one directory per run, written by the run itself with the `PROMPT.md` that produced it. Never an input to a session. |
| `../AGENTS.md` | Authorization rules for provider runs. Binding on every generation call. |

Add a second scenario and only the last two jobs are written anew: a **procedure** and **rules** hold
across scenarios, **facts** about the sources and **worked answers** do not.

## What the net does not cover

Two holes are open on purpose. What reopens either is a change to `SKILL.md` that real use asked for
and that would have fallen through the hole — never the hole itself.

- **§ 6 has never been asked for.** No prompt has requested a handover and no fixture holds an open
  spike to route; covering it means a fifth card *and* a new frozen state.
- **Codex has never run this skill.** `../../skills/roadmap/agents/openai.yaml` and its
  `allow_implicit_invocation: false` are unexercised. The second harness matters when somebody uses
  it, and nobody does yet.

**Know the width of the sample too.** Everything recorded so far is one model family — `claude-opus-5`,
once in its 1M-context variant — one harness, one scenario. A conclusion drawn from it is a conclusion
about the skill *as read by that model on that scenario*.

## Language

English, with three permanent exclusions, all Italian: `recipe-app/sources/`, because converting them
is a new scenario and not a translation; `recipe-app/reference-roadmap/`, because the skill writes in
the author's language; and `recipe-app/results/`, because it is the record of what was generated.
Field, column and state names are English everywhere, and quotations stay in their original language,
being evidence.
