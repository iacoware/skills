import { test } from "node:test"
import assert from "node:assert/strict"
import { join } from "node:path"
import { extractLog, extractMap, readMapExtract } from "./extract_map.ts"

const FIXTURE = `# Roadmap — X

**Goal:** g

## Themes

| Theme | Promise | First validator |
|---|---|---|
| \`a\` | Fai A. | \`S1\` |
| \`b\` | Fai B. | \`S2\` |

**Theme boundaries**

- \`a\` / \`b\` — **split.** Il fatto
  che continua.

## NOW

| Id | Title | Theme | Kind | Size | Readiness | Executor | Depends on |
|---|---|---|---|---|---|---|---|
| S1 | [Riga uno](slices/S1-riga-uno.md) | \`a\` | \`product\` | \`small\` | \`ready\` | \`agent\` | — |
| S2 | [Riga due](slices/S2-riga-due.md) | \`b\` | \`spike\` | \`medium\` | \`ready\` | \`agent\` | S1 |

## OUT-OF-SCOPE

- **Cosa esclusa.** Perché sì; il prezzo è
  noto.
`

test("extracts themes with promise and first validator", () => {
  const map = extractMap("R", FIXTURE)

  assert.deepEqual(map.themes, [
    { name: "a", promise: "Fai A.", firstValidator: "S1" },
    { name: "b", promise: "Fai B.", firstValidator: "S2" },
  ])
})

test("extracts a boundary verdict with its fact folded across continuation lines", () => {
  const map = extractMap("R", FIXTURE)

  assert.deepEqual(map.boundaries, [{ pair: ["a", "b"], verdict: "split", fact: "Il fatto che continua." }])
  assert.equal(map.verdictSource, "map")
})

const LOG = `## 2026-09-01 — Drawing

- \`a\` / \`b\` — **split.** Il primo fatto.
  Argument: due righe che
  non contano.
- \`b\` / \`c\` — **split.** Fatto su b e c.

## 2026-09-03 — Revising

- \`a\` / \`b\` — **merge.** Il ripensamento.
`

test("the log folds to the lowest entry per pair and drops the argument from the fact", () => {
  assert.deepEqual(extractLog(LOG), [
    { pair: ["a", "b"], verdict: "merge", fact: "Il ripensamento." },
    { pair: ["b", "c"], verdict: "split", fact: "Fatto su b e c." },
  ])
})

test("sweep entries in the log are left out of the boundary axis, whatever their subject looks like", () => {
  const log = `## 2026-09-04 — Drawing

- \`a\` / \`b\` — **split.** Il fatto.
- \`goal.md\` / \`concepts.md\` — **assumption.** Il lato preso. → \`a, S1\`
- \`goal.md\` § Ricerca / \`arch.md\` § Embedding — **question.** Nessuna sorgente sceglie. → \`a\`
- \`arch.md\` § Estrazione — **spike.** Modello non scelto. → \`S2\`
`

  assert.deepEqual(extractLog(log), [{ pair: ["a", "b"], verdict: "split", fact: "Il fatto." }])
})

test("a log beside the map takes over the verdict axis, and a map that repeats them is flagged", () => {
  const withLog = extractMap("R", "# Roadmap — X\n\n**Goal:** g\n", LOG)
  const duplicated = extractMap("R", FIXTURE, LOG)

  assert.equal(withLog.verdictSource, "log")
  assert.equal(withLog.boundaries.length, 2)
  assert.equal(duplicated.verdictSource, "both")
  assert.deepEqual(duplicated.boundaries, extractLog(LOG))
})

test("extracts NOW rows with linkless title and dependency ids", () => {
  const map = extractMap("R", FIXTURE)

  assert.deepEqual(map.rows, [
    { id: "S1", title: "Riga uno", theme: "a", kind: "product", size: "small", dependsOn: [] },
    { id: "S2", title: "Riga due", theme: "b", kind: "spike", size: "medium", dependsOn: ["S1"] },
  ])
})

test("extracts out-of-scope entries as title without trailing period plus rationale", () => {
  const map = extractMap("R", FIXTURE)

  assert.deepEqual(map.outOfScope, [{ title: "Cosa esclusa", rationale: "Perché sì; il prezzo è noto." }])
})

// Empty against empty counts as agreement downstream, so absence must extract cleanly rather than
// throw: the report is what makes an all-empty axis visible.
test("a map without boundaries or sections extracts as empty axes, not an error", () => {
  const map = extractMap("R", "# Roadmap — X\n\n**Goal:** g\n")

  assert.deepEqual(map, { run: "R", themes: [], boundaries: [], verdictSource: "none", rows: [], outOfScope: [] })
})

test("reads the real ROADMAP-CC-5 map", () => {
  const map = readMapExtract(join(import.meta.dirname, "..", "recipe-app", "results", "ROADMAP-CC-5"))

  assert.equal(map.run, "ROADMAP-CC-5")
  assert.equal(map.themes.length, 6)
  assert.equal(map.boundaries.length, 5)
  assert.equal(map.verdictSource, "map")
  assert.ok(map.boundaries.every((boundary) => boundary.verdict === "split"))
  assert.equal(map.rows.length, 11)
  assert.deepEqual(map.rows.find((row) => row.id === "S4")?.dependsOn, ["S2", "S3"])
  assert.equal(map.outOfScope.length, 5)
  assert.equal(map.outOfScope[0].title, "Ingredienti strutturati in quantità e unità")
})
