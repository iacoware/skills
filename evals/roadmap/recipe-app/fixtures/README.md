# Fixtures

Frozen input. Nothing here is a result, and no session is ever pointed at this directory: a session
writes, and everything under `fixtures/` has to stay exactly as it is or the thing it feeds stops
meaning anything. Both consumers copy before they read.

Three subdirectories, two different jobs.

| Path | What it is | Who reads it |
|---|---|---|
| `validator/` | 20 JSON files. Each is one minimal mutation of the reference roadmap, plus the error it must produce. **Not roadmaps** — patches. | `skills/roadmap/scripts/validate_roadmap.test.ts`, which applies each one to the oracle in memory |
| `mid-flight/` | A complete `.roadmap/` directory: the first drawing with `S0`–`S3` closed out into `archive/`. | Router scenario 1 of [`../../REVIEW-WORKFLOW.md`](../../REVIEW-WORKFLOW.md) |
| `redrawn/` | A complete `.roadmap/` directory: the map redrawn against the public-cookbooks goal, `S0`–`S11` archived. | Router scenario 3 |

`validator/` has [its own README](validator/README.md) explaining the patch format.

## Where the two roadmaps came from

Neither is hand-written, and that is deliberate — see the premise in
[`../../../../design/roadmap/PLAN.md`](../../../../design/roadmap/PLAN.md). The oracle in
`../reference-roadmap/` covers one state, the first drawing, because it is the only state anybody can
write honestly from the sources alone. Every state after it is a state some earlier session produced,
so these two were taken out of real runs:

- **`mid-flight/`** is what `ROADMAP-CC-1` wrote, with a close-out applied by hand: four documents
  moved to `archive/`, their register rows removed, the theme they validated whole dropped from the
  table, the dependencies they satisfied unpublished, and the two assumptions delivery answered
  killed. The content is entirely the run's.
- **`redrawn/`** is the whole of what `REDRAW-CC-1` wrote, unedited. A redraw is another map and
  cannot be derived from the first drawing, so it took its own session.

Neither run keeps its own copy under `../results/`: the fixture *is* that copy, and a second one
would be the same tree twice. `../results/README.md` keeps the row, and `PROMPT.md` the prompt.

## Changing one

A fixture moves when the state it stands for moves — never to make a scenario pass. If the
high-water mark changes, the ids in the scenario text are what get corrected, and
`REVIEW-WORKFLOW.md` says so at the head of the scenarios.

`validator/` fixtures are anchored to the oracle by exact `find` strings: change
`../reference-roadmap/roadmap.md` and run `make test-roadmap`, which fails on the fixture itself
rather than passing for the wrong reason.

The two complete states are anchored differently, because nothing derives them: `make test-roadmap`
runs the validator over every directory here that holds a `roadmap.md`, so a change to the shape the
validator enforces names them instead of leaving them to be found by the next session that copies
one. The check discovers the directories rather than listing them — a scenario that needs a new
frozen state is covered by adding it.
