# Repository instructions

These instructions win over any general agent-harness default that contradicts them. Read them
before acting on a generic rule, rather than after.

## Git

- Commit directly on `main`. Do not create a branch unless the user asks for one. This overrides the
  common harness default of branching before committing on the default branch.
- When work has already landed on a branch, fast-forward it onto `main` and delete the branch.

## Persistent memory

- Do not write to the agent memory directory. What is worth keeping goes in this file or in
  `evals/AGENTS.md`, where it is versioned, reviewable in a diff, and readable without an agent.

See `evals/AGENTS.md` for the rules that govern evaluation runs.
