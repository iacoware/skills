# `roadmap` evaluation

One structural validator, one human reading list, and three scenarios that hold the router. Kept to
notice that a change to `skills/roadmap/SKILL.md` improved one thing while breaking another.

No automated grader is planned. Two were built for `plan-slices` and both are retired; the reasons
are in [`../plan-slices/POST-MORTEM-EVALS.md`](../plan-slices/POST-MORTEM-EVALS.md), and they were
about coupling a measurement to the behaviour of a non-deterministic generator rather than about
that skill in particular. They apply here unchanged, and they apply harder: this skill lives across
sessions, so a plan judged once is replaced by a map judged in a state some earlier session produced.

**Audience: a human reviewer, or an agent in a review session.** Never a generation session — the
oracle, its rationale, the brief and the router scenarios' verdicts are the answer key, which is why
they live here and not beside the skill, where an agent exploring the directory could pick them up. The design set is off limits to
a generation session too, for a sharper reason:
[`../../design/roadmap/WORKFLOWS.md`](../../design/roadmap/WORKFLOWS.md) § 3 is the answer key to the
three router scenarios, verdicts and all.

## What is live

| Path | Role |
|---|---|
| `../../skills/roadmap/scripts/validate_roadmap.ts` | Structural and referential validator. Deterministic, free, one second. |
| `make validate-roadmap ROADMAP=<dir>` | Runs it, from the repository root. `ROADMAP` is the directory holding `roadmap.md`, not a file. |
| `REVIEW-WORKFLOW.md` | How to review one fresh drawing: the preconditions every session runs under, the generation prompt, and the five steps. |
| `recipe-app/ROUTER-SCENARIOS.md` | The other half of the net: three cases that hold the router, each with its starting state, its prompt and its verdict. Answer key — off limits to a generation session. |
| `EVALUATION-RULES.md` | What to look for, as numbered checks. Rules about the skill, portable to any scenario. |
| `OPEN-VERIFICATION.md` | What the net does not cover, and how to draw a conclusion from a run. The intent, the epistemics, and the one check still owed. |
| `recipe-app/sources/` | The only inputs a candidate roadmap is drawn from. Copied verbatim from `../plan-slices/recipe-app/sources/`: they are input, not `plan-slices` output. |
| `recipe-app/EVALUATION-BRIEF.md` | Facts about those sources: where the map may differ, what it must leave open, what only looks like a defect, what it must contain. Verifiable, no taste, entries with citable ids. Read at step 3. |
| `recipe-app/reference-roadmap/` | One good answer, hand-written from the sources before any candidate existed: the map as it stands the first time it is drawn. Taste, not verifiable. Read at step 5, never earlier. |
| `recipe-app/REFERENCE-ROADMAP-RATIONALE.md` | Why each row is a row and sits where it sits — what the published map deliberately does not carry. |
| `recipe-app/fixtures/validator/` | One minimal mutation of the oracle per validator check. Read by `validate_roadmap.test.ts`, not by a reviewer. |
| `recipe-app/fixtures/mid-flight/`, `recipe-app/fixtures/redrawn/` | The starting states of router scenarios 1 and 3. Cut out of a real run and frozen. |
| `recipe-app/fixtures/README.md` | What each of the three fixture directories is, who reads it, and which run it came from. |
| `recipe-app/results/` | What the skill produced, one directory per run, each with the `PROMPT.md` that produced it. Never an input to a session. |
| `../AGENTS.md` | Authorization rules for provider runs. Binding for every generation call below. |

Four jobs, no overlap: a **procedure**, **rules** that hold across scenarios, **facts** about this
scenario's sources, and **worked answers** for this scenario — the oracle with its rationale for the
drawing branch, `ROUTER-SCENARIOS.md` for the other. Add a second scenario and the rules travel
unchanged, the drawing procedure travels with a directory substituted, and everything under the
scenario's own directory is written anew.

**Nothing is inherited from `evals/plan-slices/`.** The rule ids here start a fresh sequence and the
brief's entry ids are its own: `R-004` in `EVALUATION-RULES.md` and `R-004` in the `plan-slices` list
are unrelated, and so are `A1`, `C1`, `H1`. The retired ledger those ids came from was about a plan
document, and no row of it was about this format. Cite an id with its file when both are open.

**Why the brief is not enough on its own.** It is the reference map with the answer removed:
everything mechanically checkable kept, everything requiring judgement dropped. What it drops is the
only artifact carrying the author's own judgement about how this product should be cut — and the only
defence against the failure mode of pure manual review, the reviewer's sense of *good* drifting
toward whatever the model last produced. A frozen reference costs nothing per run and does not drift.

**Why the scenarios are not enough either.** A drawn map and a re-trued map fail in different ways.
The oracle covers one state, the first drawing, and it is the only state that can be hand-written
honestly; everything after it is a state some earlier session produced. The scenarios are how the
other branch gets read at all, and they are cheap: each starts from a map already standing, the
branch that proposes before it writes, so a wrong turn costs a proposal and not a record.

## Language

English, as the rest of the project since 2026-08-06. Three exclusions, all permanent:
`recipe-app/sources/`, because converting them is a new scenario rather than a translation;
`recipe-app/reference-roadmap/`, because the skill writes in the author's language and the sources
are Italian; and whatever lands under `recipe-app/results/`, because it is the record of what was
generated. Field names, column names and state values are English everywhere, including inside the
Italian map, because they are format rather than prose. Quotations stay in their original language
inside quotation marks, wherever they appear, because they are evidence.
