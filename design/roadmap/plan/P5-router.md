# P5 — The router

**Depends on** P2, P3, P4. **Produces** the skill itself.

Read [`../PLAN.md`](../PLAN.md) first.

## Reads

- everything P2, P3 and P4 produced;
- [`../ROADMAP-GOAL.md`](../ROADMAP-GOAL.md) § *The skill* and § *The integration boundary*;
- [`../WORKFLOWS.md`](../WORKFLOWS.md) § 3, which holds the three inputs the router gets wrong;
- `skills/plan-slices/SKILL.md` and `skills/plan-slices/agents/openai.yaml`, for the frontmatter and
  the explicit-invocation settings.

## Produces

- `skills/roadmap/SKILL.md`;
- `skills/roadmap/agents/openai.yaml`.

## Work

`SKILL.md` establishes the situation — whether `.roadmap/` exists, what goal is recorded, what has
been delivered since — then takes one of two branches, decided by whether the input makes a claim
about the destination or about the path, with work as the default and by a wide margin.

Drawing loads `references/drawing-the-map.md` and does not end when the files are written: the first
round of revision happens in the same session, because a first map is a proposal to argue with.
Re-truing runs the five operations — close-out, promotion, admission, revision, retirement — ordered
close-out first, since everything else is decided against a register already trued up.

Both branches end the same way: re-ask the coverage question, propose one block of changes, ask for
confirmation once, run the validator.

`disable-model-invocation: true` in the frontmatter, `allow_implicit_invocation: false` in
`agents/openai.yaml`. A roadmap redrawn because an agent thought it was being helpful is the failure
those settings exist to prevent.

## Done when

- no subcommand and no verb the author has to type appears anywhere;
- the unreconcilable case is a question with a short answer — state the recorded goal, state what the
  input looks like, ask which holds — never an inference;
- close-out states the three questions of absorption, and states that three noes write nothing;
- handover suggests the clarifying conversation, `/grill-with-docs` or `/wayfinder` for a slice,
  `/prototype` or `/wayfinder` for a spike, never `/to-spec` directly, and degrades cleanly when
  `docs/agents/issue-tracker.md` is absent;
- the `triage` labels are derived at handover and never stored;
- it is shorter than `skills/plan-slices/SKILL.md`, since the rules now live beside it;
- `make add-skill SKILL=roadmap` installs it and the installed copy still resolves its references,
  assets and script.
