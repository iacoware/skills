# P6 — Repository wiring

**Depends on** P3 and P5. **Produces** the ways anybody else reaches the skill.

Read [`../PLAN.md`](../PLAN.md) first.

## Reads

`Makefile`, `README.md`, [`../../../CONTEXT-MAP.md`](../../../CONTEXT-MAP.md).

## Produces

- `make test` running both suites — `python3 -m unittest` for `plan-slices`, `node --test` for
  `roadmap`;
- `make validate-roadmap ROADMAP=<dir>`, the directory defaulting to `.roadmap`;
- the `README.md` row for the skill, with its explicit invocation, next to the `plan-slices` one;
- the `CONTEXT-MAP.md` update, pointing at the skill folder as well as at the design set.

## Work

Additive only. `plan-slices` keeps its target, its validator and its tests working: it is deprecated
in P8, not removed, and a `make test` that stops running its suite has broken the yardstick the first
roadmaps are read against.

`node --test` takes a positional argument as a file or a glob, never as a directory to search: given
one it tries to load the directory as a module and dies with `MODULE_NOT_FOUND`. Only the argument-less
form recurses, from the working directory, and it does discover `.test.ts` — from the repository root
it runs the 40 tests. So the target either drops the path or names the file, and naming it —
`node --test skills/roadmap/scripts/validate_roadmap.test.ts` — is what keeps the suite from silently
growing whatever `.test.ts` lands in the repository later.

## Done when

- both suites run from one command, and both are green;
- `make validate-roadmap` runs the validator on the oracle and on a project's `.roadmap/` alike;
- `README.md` and `CONTEXT-MAP.md` name the skill and resolve to files that exist.
