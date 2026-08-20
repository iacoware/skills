import { test } from "node:test"
import assert from "node:assert/strict"
import { mkdirSync, mkdtempSync, readFileSync, readdirSync, writeFileSync } from "node:fs"
import { tmpdir } from "node:os"
import { basename, join } from "node:path"
import { main, readRoadmapDirectory, validateRoadmap } from "./validate_roadmap.ts"

const SCENARIO = join(import.meta.dirname, "..", "..", "..", "evals", "roadmap", "recipe-app")
const ORACLE = join(SCENARIO, "reference-roadmap")
const FIXTURES = join(SCENARIO, "fixtures", "validator")

const S2_ROW =
  "| `S2` | [Spike: quale embedding regge la ricerca cross-lingua](slices/S2-spike-embedding-cross-lingua.md) | `ricerca-semantica` | `spike` | `small` | `needs-info` | `agent` | — |"
const S3_ROW =
  "| `S3` | [Indicizzazione semantica delle ricette](slices/S3-indicizzazione-semantica.md) | `ricerca-semantica` | `enabler` | `medium` | `ready` | `agent` | `S2` |"

const errorsOf = (contents: ReturnType<typeof readRoadmapDirectory>) =>
  validateRoadmap(contents)
    .filter((diagnostic) => diagnostic.level === "error")
    .map((diagnostic) => diagnostic.message)

const warningsOf = (contents: ReturnType<typeof readRoadmapDirectory>) =>
  validateRoadmap(contents)
    .filter((diagnostic) => diagnostic.level === "warning")
    .map((diagnostic) => diagnostic.message)

const replaceOnce = (text: string, find: string, replace: string, where: string) => {
  const at = text.indexOf(find)
  assert.notEqual(at, -1, `${where}: '${find.slice(0, 40)}…' no longer matches the oracle`)
  assert.equal(text.indexOf(find, at + 1), -1, `${where}: '${find.slice(0, 40)}…' matches twice`)
  return text.slice(0, at) + replace + text.slice(at + find.length)
}

const edit = (find: string, replace: string, file = "roadmap.md") =>
  ({ in: file, find, replace })

const mutate = (mutation: {
  edits?: { in: string; find: string; replace: string }[]
  remove?: string[]
  add?: Record<string, string>
}) => {
  const contents = readRoadmapDirectory(ORACLE)
  let roadmap = contents.roadmap
  let slices = contents.slices.map((slice) => ({ ...slice }))
  const archive = [...contents.archive]
  for (const change of mutation.edits ?? []) {
    if (change.in === "roadmap.md") {
      roadmap = replaceOnce(roadmap, change.find, change.replace, change.in)
      continue
    }
    const slice = slices.find((candidate) => candidate.filename === basename(change.in))
    assert.ok(slice, `${change.in} is not a document of the oracle`)
    slice.text = replaceOnce(slice.text, change.find, change.replace, change.in)
  }
  for (const path of mutation.remove ?? []) {
    slices = slices.filter((slice) => slice.filename !== basename(path))
  }
  for (const [path, text] of Object.entries(mutation.add ?? {})) {
    if (path.startsWith("archive/")) archive.push(basename(path))
    else slices.push({ filename: basename(path), text })
  }
  return { roadmap, slices, archive }
}

test("the oracle passes every check and raises no warning", () => {
  assert.deepEqual(validateRoadmap(readRoadmapDirectory(ORACLE)), [])
})

for (const filename of readdirSync(FIXTURES).filter((name) => name.endsWith(".json")).sort()) {
  const fixture = JSON.parse(readFileSync(join(FIXTURES, filename), "utf8"))

  test(`the validator catches ${fixture.check}`, () => {
    const errors = errorsOf(mutate(fixture))

    assert.notEqual(errors.length, 0, `${filename} left the oracle green`)
    for (const message of errors) assert.ok(message.includes(fixture.expect), message)
  })
}

test("a spike may leave out the Audience section altogether", () => {
  const contents = mutate({
    edits: [edit("## Audience\n\n—\n\n", "", "slices/S2-spike-embedding-cross-lingua.md")],
  })

  assert.deepEqual(errorsOf(contents), [])
})

test("a spike claiming the goal theme stands with no row waiting on it", () => {
  const contents = mutate({
    edits: [
      edit(S2_ROW, S2_ROW.replace("`ricerca-semantica`", "`goal`")),
      edit(S3_ROW, S3_ROW.replace("| `S2` |", "| — |")),
    ],
  })

  assert.deepEqual(errorsOf(contents), [])
})

test("only a spike may claim the goal theme", () => {
  const contents = mutate({ edits: [edit(S3_ROW, S3_ROW.replace("`ricerca-semantica`", "`goal`"))] })

  assert.deepEqual(errorsOf(contents), [
    "S3: only a spike may claim the theme 'goal', which declares that it validates the goal's feasibility",
  ])
})

test("a row naming a theme the theme table does not carry", () => {
  const contents = mutate({ edits: [edit(S3_ROW, S3_ROW.replace("`ricerca-semantica`", "`sapori`"))] })

  assert.deepEqual(errorsOf(contents), ["S3: the theme 'sapori' is not in the theme table"])
})

for (const { column, cell, illegal, legal } of [
  { column: "Kind", cell: "`enabler`", illegal: "`epic`", legal: "product, enabler, release, spike" },
  { column: "Size", cell: "`medium`", illegal: "`enorme`", legal: "small, medium, large" },
  { column: "Readiness", cell: "`ready`", illegal: "`bloccata`", legal: "ready, needs-decision, needs-info" },
  { column: "Executor", cell: "`agent`", illegal: "`robot`", legal: "agent, human, mixed" },
]) {
  test(`a ${column} outside its legal values`, () => {
    const contents = mutate({ edits: [edit(S3_ROW, S3_ROW.replace(cell, illegal))] })

    assert.deepEqual(errorsOf(contents), [
      `S3: '${illegal.replaceAll("`", "")}' is not a legal ${column}; expected ${legal}`,
    ])
  })
}

test("a section roadmap.md has no business carrying", () => {
  const contents = mutate({ edits: [edit("## LATER\n", "## Backlog\n\n- Una voce.\n\n## LATER\n")] })

  assert.deepEqual(errorsOf(contents), ["roadmap.md: 'Backlog' is not a section of the roadmap"])
})

test("two register rows carrying the same id", () => {
  const contents = mutate({ edits: [edit(S3_ROW, `${S3_ROW}\n${S3_ROW}`)] })

  assert.ok(errorsOf(contents).includes("NOW: the id 'S3' is carried by two rows"))
})

test("an id that is not of the form S<number>", () => {
  const contents = mutate({ edits: [edit(S3_ROW, S3_ROW.replace("| `S3` |", "| `S03` |"))] })

  assert.ok(errorsOf(contents).includes("NOW: 'S03' is not an id of the form S<number>"))
})

test("a field of roadmap.md left empty", () => {
  const contents = mutate({
    edits: [
      edit(
        "**Sources:** `sources/goal.md`, `sources/concepts.md`, `sources/arch-choices.md`,\n`sources/tech-choices.md`.",
        "**Sources:**",
      ),
    ],
  })

  assert.deepEqual(errorsOf(contents), ["roadmap.md: the 'Sources' field is empty"])
})

const document = (id: number) => `# S${id} — Riga ${id}

← [Register](../roadmap.md#now)

**Outcome:** Quello che la riga consegna.

**Requested by:** \`sources/goal.md\`
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi usa il prodotto, e cosa sa fare dopo.

## Includes

- Il minimo perché l'outcome tenga.

## Verification

Si vede da fuori che la riga è finita.

## Learning target

Quello che la riga è lì per scoprire.

## Excludes

- Quello che un lettore si aspetterebbe e non trova.

## Open questions

—
`

const registerOf = (ids: number[]) => `# Roadmap — Prova

**Goal:** un goal dichiarato, in una riga.

**Sources:** \`sources/goal.md\`.

**Current state:** niente di consegnato.

## Ordering criteria

1. **Percorso minimo di consegna prima.** Finché non si consegna, non si impara niente.

## Themes

| Theme | Promise | First validator |
|---|---|---|
| \`tema\` | Si può fare la cosa promessa | \`S${ids[0]}\` |

## Assumptions

- \`tema\` — qualcosa preso per vero per poter disegnare la mappa.

## Open questions

- \`tema\` — qualcosa rimasto senza risposta.

## Cross-functional concerns

- **Authorization.** Regola condivisa.
- **Validation and errors.** Regola condivisa.
- **Operability.** Regola condivisa.
- **Accessibility and security.** Regola condivisa.
- **Data integrity and recovery.** Regola condivisa.

## NOW

| Id | Title | Theme | Kind | Size | Readiness | Executor | Depends on |
|---|---|---|---|---|---|---|---|
${ids
  .map(
    (id) =>
      `| \`S${id}\` | [Riga ${id}](slices/S${id}-riga.md) | \`tema\` | \`product\` | \`small\` | \`ready\` | \`agent\` | — |`,
  )
  .join("\n")}

## LATER

- Una candidate, e niente di più.

## OUT-OF-SCOPE

- **Un problema dichiarato irrisolto.** La licenza che dà.
`

const registerWith = (count: number) => {
  const ids = Array.from({ length: count }, (_, index) => index)
  return {
    roadmap: registerOf(ids),
    slices: ids.map((id) => ({ filename: `S${id}-riga.md`, text: document(id) })),
    archive: [],
  }
}

test("a register inside the cap and above the floor says nothing", () => {
  assert.deepEqual(validateRoadmap(registerWith(5)), [])
})

test("a register past the cap warns and does not fail", () => {
  const contents = registerWith(21)

  assert.deepEqual(errorsOf(contents), [])
  assert.deepEqual(warningsOf(contents), [
    "NOW: 21 rows are past the cap of 20; a bigger problem buys fatter slices, not more rows",
  ])
})

test("a register below the floor warns and does not fail", () => {
  const contents = registerWith(2)

  assert.deepEqual(errorsOf(contents), [])
  assert.deepEqual(warningsOf(contents), [
    "NOW: 2 rows are below the floor of 3; a map this small does not repay its cost",
  ])
})

const captured = (run: () => number) => {
  const lines: string[] = []
  const { log, error } = console
  console.log = (line: string) => lines.push(line)
  console.error = (line: string) => lines.push(line)
  try {
    return { code: run(), lines }
  } finally {
    console.log = log
    console.error = error
  }
}

const writtenAt = (directory: string, contents: ReturnType<typeof registerWith>) => {
  mkdirSync(join(directory, "slices"), { recursive: true })
  writeFileSync(join(directory, "roadmap.md"), contents.roadmap)
  for (const slice of contents.slices) {
    writeFileSync(join(directory, "slices", slice.filename), slice.text)
  }
  return directory
}

test("the command exits zero on a roadmap that only warns", () => {
  const directory = writtenAt(mkdtempSync(join(tmpdir(), "roadmap-")), registerWith(2))

  const { code, lines } = captured(() => main([directory]))

  assert.equal(code, 0)
  assert.ok(lines.some((line) => line.startsWith("WARNING: ")))
})

test("the command reads .roadmap when no directory is given", () => {
  const root = mkdtempSync(join(tmpdir(), "roadmap-"))
  writtenAt(join(root, ".roadmap"), registerWith(5))
  const previous = process.cwd()

  process.chdir(root)
  try {
    assert.equal(captured(() => main([])).code, 0)
  } finally {
    process.chdir(previous)
  }
})

test("the command exits one on a roadmap that fails a check", () => {
  const contents = registerWith(5)
  const directory = writtenAt(mkdtempSync(join(tmpdir(), "roadmap-")), {
    ...contents,
    slices: contents.slices.slice(1),
  })

  const { code, lines } = captured(() => main([directory]))

  assert.equal(code, 1)
  assert.ok(lines.some((line) => line.startsWith("ERROR: ")))
})

test("the command exits two when there is no roadmap to read", () => {
  const { code } = captured(() => main([join(tmpdir(), "nessuna-roadmap-qui")]))

  assert.equal(code, 2)
})
