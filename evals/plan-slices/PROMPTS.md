# Scratchpad — one prompt awaiting its successor

**This file governs nothing.** The normative prompts of the consensus cycle are the four files under
`prompts/` — `improve.prompt.md`, `review.prompt.md`, `verdict.prompt.md`, `recidiva.prompt.md` —
and only those are run.

What is left here is **generation**, which has no successor yet: Phase 6 moves it under `prompts/`
and this file goes away with it.

`## CREATE IMPROVEMENTS` and `## CREATE REVIEW 2`, the CON-1…CON-5 ancestors of `improve` and
`review`, were **removed on 2026-08-07**, when the four prompts replaced them. Nothing normative was
lost: they named a deleted reference plan, told each agent which plan was its own, and stated their
contract in prose — the three things the rewrite exists to undo. The text as sent in CON-4 is
`472233d:evals/plan-slices/PROMPTS.md`, byte-identical to what was deleted, and that commit is what
the documents citing it now point at. This file is not the record of anything: it had already been
pruned once, in `be3daac`, hours after the CON-4 artifacts landed.

## GENERATE PLAN

Rewritten for CON-6. The CON-1…CON-5 text is `472233d:evals/plan-slices/PROMPTS.md`; what changed and
why is `workflow/CYCLE.md` § *Confini di strumento*, CON-5 → CON-6 generation. Run it once per side,
in a fresh interactive session, changing only the output path — `PLAN-CC-CON-N.md` on Claude Code,
`PLAN-CX-CON-N.md` on Codex.

The skill is **invoked explicitly**, and that is the whole reason this prompt was rewritten: since
`3658187` neither harness activates it on its own.

**Claude Code**, one message:

```
/plan-slices Read the markdown documents in @evals/plan-slices/recipe-app/sources/, starting from @evals/plan-slices/recipe-app/sources/goal.md, and produce a high-level delivery plan cut into slices. Write it to evals/plan-slices/recipe-app/results/PLAN-CC-CON-6.md. Read nothing else in this repository, in this session or in any session you delegate to: the sources are the only input, and the existing plans under results/ are off limits.
```

**Codex**, one message:

```
$plan-slices Read the markdown documents in evals/plan-slices/recipe-app/sources/, starting from evals/plan-slices/recipe-app/sources/goal.md, and produce a high-level delivery plan cut into slices. Write it to evals/plan-slices/recipe-app/results/PLAN-CX-CON-6.md. Read nothing else in this repository, in this session or in any session you delegate to: the sources are the only input, and the existing plans under results/ are off limits.
```

The two differ in the `@` prefixes, which are Claude Code's file-reference syntax and have no Codex
equivalent. That asymmetry is inherited from CON-1…CON-5, not introduced here.

Model and effort are set in the session, not in the prompt, and are written into
`support/AGENT-PLAN-MAP.md` before the call: `claude-opus-5` · `high` and `gpt-5.6-sol` · `high`.
