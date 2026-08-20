# P7 — The evaluation harness

**Depends on** P1 for the oracle, P5 for the invocation, P6 for the targets it cites. **Produces**
the net that notices a change to `SKILL.md` improving one thing and breaking another.

Read [`../PLAN.md`](../PLAN.md) first.

## Reads

- `evals/plan-slices/` in full — `README.md`, `REVIEW-WORKFLOW.md`, `EVALUATION-RULES.md`,
  `recipe-app/EVALUATION-BRIEF.md`, and `POST-MORTEM-EVALS.md` for what was retired and why;
- [`../PLAN-INPUTS.md`](../PLAN-INPUTS.md) § *Evals* and § *Reviewing the skill itself*;
- [`../WORKFLOWS.md`](../WORKFLOWS.md), which the scenarios are derived from.

## Produces

- `evals/roadmap/README.md`, `REVIEW-WORKFLOW.md`, `EVALUATION-RULES.md`;
- `evals/roadmap/recipe-app/EVALUATION-BRIEF.md`.

## Work

The four jobs stay separate exactly as they are for `plan-slices`: a procedure, rules that hold
across scenarios, facts about this scenario's sources, one worked answer with its reasoning — the
last two being P1's oracle and rationale. Rule ids start a fresh sequence; nothing is inherited,
because nothing in the retired ledger was about this format.

Three scenarios hold the router, each stating its starting state, the author's opening sentence, and
the verdict a correct session reaches:

1. **sounds like a change of destination, is work** — cross-cookbook search is a candidate already in
   `LATER`; the session promotes it and the goal is untouched;
2. **sounds like work, is a change of destination** — a `visibility=public` flag costs an afternoon
   and moves the product to the open web; the skill asks which claim holds instead of admitting a
   slice;
3. **sounds like a slice, is a spike** — search on the public corpus, where the honest verification
   is a measurement; a spike is minted and the waiting slice gains it in `Depends on`.

Scenarios 1 and 3 need a map that is not the initial one. Their starting states are **not**
hand-written: P8 cuts them out of a real run and freezes them under
`evals/roadmap/recipe-app/fixtures/`. Write the scenarios here against that promise, and leave the
fixture paths dangling until P8 fills them.

## Done when

- the five steps of the workflow are runnable by someone who has not read this plan;
- the generation prompts exist for Claude Code and Codex, with the explicit-invocation prefix and the
  instruction to read nothing else in the repository;
- the brief states what the roadmap must leave open, where it may legitimately differ, and what only
  looks like a defect;
- every rule names the clause of `SKILL.md` it guards, and a rule guarding a clause the skill no
  longer states is a defect in the rule.
