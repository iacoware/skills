# Fixtures

Frozen input. Nothing here is a result, and no session is ever pointed at this directory: a session
writes, and everything under `fixtures/` has to stay exactly as it is or the thing it feeds stops
meaning anything. Both consumers copy before they read.

Three subdirectories, two different jobs.

| Path | What it is | Who reads it |
|---|---|---|
| `validator/` | 20 JSON files. Each is one minimal mutation of the reference roadmap, plus the error it must produce. **Not roadmaps** — patches. | `skills/roadmap/scripts/validate_roadmap.test.ts`, which applies each one to the oracle in memory |
| `mid-flight/` | A complete `.roadmap/` directory: the first drawing with `S0`–`S3` closed out into `archive/`, plus the `log.md` the format acquired later. | Router scenario 1 of [`../SCENARIOS.md`](../SCENARIOS.md) |
| `redrawn/` | A complete `.roadmap/` directory: the map redrawn against the public-cookbooks goal, `S0`–`S11` archived. | Router scenario 3 |

`validator/` has [its own README](validator/README.md) explaining the patch format.

## Where the two roadmaps came from

Neither is hand-written, and that is deliberate. The oracle in `../reference-roadmap/` covers one
state, the first drawing, because it is the only state anybody can write honestly from the sources
alone. Every state after it is a state some earlier session produced,
so these two were taken out of real runs:

- **`mid-flight/`** is a first drawing with a close-out applied by hand: four documents moved to
  `archive/`, their register rows removed, the theme they validated whole dropped from the table, the
  dependencies they satisfied unpublished, and the two assumptions delivery answered killed. The
  content is entirely the run's, with one exception: **`log.md` is hand-written.** The run that drew
  this map predates the theme verdict, so no transcript carries one to recover; the four entries
  are the split verdicts the five themes in the table imply, dated with the freeze, and the
  `accesso` / `condivisione` argument is the case that gave the split test its precedence. A
  scenario reading R-038 against this fixture judges whether the session read and appended to the
  log, never whether it agreed with these verdicts.
- **`redrawn/`** is the whole of what one redraw session wrote, unedited. A redraw is another map and
  cannot be derived from the first drawing, so it took its own session.

## Changing one

A fixture moves when the state it stands for moves — never to make a scenario pass. If the
high-water mark changes, the ids in the scenario text are what get corrected, and
`../SCENARIOS.md` says so at the head of the scenarios.

`validator/` fixtures are anchored to the oracle by exact `find` strings: change
`../reference-roadmap/roadmap.md` and run `make test-roadmap`, which fails on the fixture itself
rather than passing for the wrong reason.

The two complete states are anchored differently, because nothing derives them: `make test-roadmap`
runs the validator over every directory here that holds a `roadmap.md`, so a change to the shape the
validator enforces names them instead of leaving them to be found by the next session that copies
one. The check discovers the directories rather than listing them — a scenario that needs a new
frozen state is covered by adding it.
