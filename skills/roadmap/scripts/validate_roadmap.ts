import { existsSync, readFileSync, readdirSync, realpathSync } from "node:fs"
import { join } from "node:path"

const ROADMAP_FILE = "roadmap.md"
const SLICES_DIRECTORY = "slices"
const ARCHIVE_DIRECTORY = "archive"

const ROADMAP_FIELDS = ["Goal", "Sources", "Current state"]
const ROADMAP_SECTIONS = [
  "Themes",
  "NOW",
  "LATER",
  "OUT-OF-SCOPE",
  "Ordering criteria",
  "Assumptions",
  "Open questions",
  "Cross-functional concerns",
]
const LIST_ONLY_SECTIONS = [
  "Ordering criteria",
  "Assumptions",
  "Open questions",
  "Cross-functional concerns",
  "LATER",
  "OUT-OF-SCOPE",
]
const HORIZONS_WITHOUT_IDS = ["LATER", "OUT-OF-SCOPE"]
const REGISTER_COLUMNS = [
  "Id",
  "Title",
  "Theme",
  "Kind",
  "Size",
  "Readiness",
  "Executor",
  "Depends on",
]
const THEME_COLUMNS = ["Theme", "Promise", "First validator"]

const SLICE_FIELDS = ["Outcome", "Requested by", "Spec", "Tickets", "ADRs"]
const SLICE_SECTIONS = [
  "Audience",
  "Includes",
  "Verification",
  "Learning target",
  "Excludes",
  "Open questions",
]

const KINDS = ["product", "enabler", "release", "spike"]
const SIZES = ["small", "medium", "large"]
const READINESSES = ["ready", "needs-decision", "needs-info"]
const EXECUTORS = ["agent", "human", "mixed"]

// The templates are what a session reads and these constants are what the validator enforces: the
// same shape stated twice, in two files nothing else connects. validate_roadmap.shape.test.ts is
// that connection.
export const SHAPE = {
  roadmapFields: ROADMAP_FIELDS,
  roadmapSections: ROADMAP_SECTIONS,
  registerColumns: REGISTER_COLUMNS,
  themeColumns: THEME_COLUMNS,
  sliceFields: SLICE_FIELDS,
  sliceSections: SLICE_SECTIONS,
  kinds: KINDS,
  sizes: SIZES,
  readinesses: READINESSES,
  executors: EXECUTORS,
}

const SPIKE = "spike"
const NONE = "—"
const GOAL_THEME = "goal"
const REGISTER_FLOOR = 3
const REGISTER_CAP = 20

const H1_PATTERN = /^# (?!#)(.+?)[ \t]*$/m
const H2_PATTERN = /^## (?!#)(.+?)[ \t]*$/gm
const FIELD_PATTERN = /^\*\*([^*:]+):\*\*[ \t]*(.*)$/gm
const LIST_ITEM_PATTERN = /^\s*(?:[-+*]|\d+\.)\s+\S/
const CONTINUATION_PATTERN = /^\s{2,}\S/
const SEPARATOR_CELL_PATTERN = /^:?-+:?$/
const ID_PATTERN = /^S(?:0|[1-9]\d*)$/
const ID_ANYWHERE_PATTERN = /(?<![\w-])S\d+(?![\w-])/
const SLICE_FILENAME_PATTERN = /^(S(?:0|[1-9]\d*))-[^\s/]+\.md$/
const SLICE_TITLE_PATTERN = /^(S\S*)\s+—\s+(.+?)[ \t]*$/
const LINK_PATTERN = /^\[(.+)\]\((.+)\)$/
const REGISTER_BACKLINK_PATTERN = /\]\(\.\.\/roadmap\.md#now\)/

type Diagnostic = { level: "error" | "warning"; message: string }

type Section = { name: string; body: string }

type Field = { name: string; value: string }

type Table = { header: string[]; rows: string[][] }

type Row = {
  id: string
  title: string
  link: string
  theme: string
  kind: string
  size: string
  readiness: string
  executor: string
  dependsOn: string[]
}

type SliceDocument = { filename: string; text: string }

type RoadmapDirectory = {
  roadmap: string
  slices: SliceDocument[]
  archive: string[]
}

const error = (message: string): Diagnostic => ({ level: "error", message })
const warning = (message: string): Diagnostic => ({ level: "warning", message })

const bare = (cell: string) => {
  const match = /^`(.+)`$/.exec(cell.trim())
  return match ? match[1] : cell.trim()
}

const preambleOf = (text: string) => {
  const firstSection = /^## /m.exec(text)
  return firstSection ? text.slice(0, firstSection.index) : text
}

const parseFields = (text: string): Field[] =>
  [...text.matchAll(FIELD_PATTERN)].map((match) => ({
    name: match[1].trim(),
    value: match[2].trim(),
  }))

const parseSections = (text: string): Section[] => {
  const matches = [...text.matchAll(H2_PATTERN)]
  return matches.map((match, index) => {
    const start = match.index + match[0].length
    const next = matches[index + 1]
    return {
      name: match[1].trim(),
      body: text.slice(start, next ? next.index : text.length),
    }
  })
}

const sectionNamed = (sections: Section[], name: string) =>
  sections.find((section) => section.name === name)

const parseTable = (body: string): Table => {
  const lines = body
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line.startsWith("|") && line.endsWith("|"))
    .map((line) => line.slice(1, -1).split("|").map((cell) => cell.trim()))
  return {
    header: lines.length > 0 ? lines[0] : [],
    rows: lines
      .slice(1)
      .filter((cells) => !cells.every((cell) => SEPARATOR_CELL_PATTERN.test(cell))),
  }
}

const parseIdList = (cell: string) => {
  const value = cell.trim()
  return value === NONE || value === "" ? [] : value.split(",").map(bare)
}

const parseRow = (cells: string[]): Row => {
  const titleCell = cells[1] ?? ""
  const link = LINK_PATTERN.exec(titleCell)
  return {
    id: bare(cells[0] ?? ""),
    title: link ? link[1].trim() : titleCell,
    link: link ? link[2].trim() : "",
    theme: bare(cells[2] ?? ""),
    kind: bare(cells[3] ?? ""),
    size: bare(cells[4] ?? ""),
    readiness: bare(cells[5] ?? ""),
    executor: bare(cells[6] ?? ""),
    dependsOn: parseIdList(cells[7] ?? ""),
  }
}

const missingNames = (expected: string[], present: string[]) =>
  expected.filter((name) => !present.includes(name))

const unknownNames = (expected: string[], present: string[]) =>
  present.filter((name) => !expected.includes(name))

const isOutOfOrder = (expected: string[], present: string[]) => {
  const ranks = present
    .filter((name) => expected.includes(name))
    .map((name) => expected.indexOf(name))
  return ranks.some((rank, index) => index > 0 && rank <= ranks[index - 1])
}

const listOnlyDiagnostics = (section: Section) => {
  const diagnostics: Diagnostic[] = []
  let inFence = false
  section.body.split("\n").forEach((line, index) => {
    const stripped = line.trim()
    if (stripped === "") return
    if (stripped.startsWith("```")) {
      inFence = !inFence
      return
    }
    if (inFence || LIST_ITEM_PATTERN.test(line) || CONTINUATION_PATTERN.test(line)) return
    diagnostics.push(
      error(
        `${section.name}: line ${index + 1} is prose; the section holds list items and their continuations only`,
      ),
    )
  })
  return diagnostics
}

const columnDiagnostics = (label: string, expected: string[], header: string[]) =>
  header.join(" | ") === expected.join(" | ")
    ? []
    : [error(`${label}: expected the columns ${expected.join(", ")}, in that order`)]

const roadmapStructureDiagnostics = (text: string, sections: Section[]) => {
  const diagnostics: Diagnostic[] = []
  if (!H1_PATTERN.test(text)) diagnostics.push(error(`${ROADMAP_FILE}: missing the title`))

  const fields = parseFields(preambleOf(text))
  const names = fields.map((field) => field.name)
  for (const missing of missingNames(ROADMAP_FIELDS, names)) {
    diagnostics.push(error(`${ROADMAP_FILE}: missing the '${missing}' field`))
  }
  if (isOutOfOrder(ROADMAP_FIELDS, names)) {
    diagnostics.push(
      error(`${ROADMAP_FILE}: the fields must read ${ROADMAP_FIELDS.join(", ")}, in that order`),
    )
  }
  for (const field of fields) {
    if (ROADMAP_FIELDS.includes(field.name) && field.value === "") {
      diagnostics.push(error(`${ROADMAP_FILE}: the '${field.name}' field is empty`))
    }
  }

  const sectionNames = sections.map((section) => section.name)
  for (const missing of missingNames(ROADMAP_SECTIONS, sectionNames)) {
    diagnostics.push(error(`${ROADMAP_FILE}: missing the '${missing}' section`))
  }
  for (const unknown of unknownNames(ROADMAP_SECTIONS, sectionNames)) {
    diagnostics.push(error(`${ROADMAP_FILE}: '${unknown}' is not a section of the roadmap`))
  }
  if (isOutOfOrder(ROADMAP_SECTIONS, sectionNames)) {
    diagnostics.push(
      error(`${ROADMAP_FILE}: the sections must read ${ROADMAP_SECTIONS.join(", ")}, in that order`),
    )
  }
  for (const name of LIST_ONLY_SECTIONS) {
    const section = sectionNamed(sections, name)
    if (section) diagnostics.push(...listOnlyDiagnostics(section))
  }
  return diagnostics
}

const themeTableDiagnostics = (sections: Section[], rows: Row[]) => {
  const section = sectionNamed(sections, "Themes")
  if (!section) return []

  const table = parseTable(section.body)
  const diagnostics = columnDiagnostics("Themes", THEME_COLUMNS, table.header)
  const ids = new Set(rows.map((row) => row.id))
  for (const cells of table.rows) {
    const theme = bare(cells[0] ?? "")
    const validator = bare(cells[2] ?? "")
    if (!ids.has(validator)) {
      diagnostics.push(
        error(`Themes: the first validator of '${theme}' is '${validator}', which is not a row`),
      )
    }
  }
  return diagnostics
}

const themeSlugs = (sections: Section[]) => {
  const section = sectionNamed(sections, "Themes")
  return new Set(section ? parseTable(section.body).rows.map((cells) => bare(cells[0] ?? "")) : [])
}

const registerDiagnostics = (table: Table, rows: Row[]) => {
  const diagnostics = columnDiagnostics("NOW", REGISTER_COLUMNS, table.header)
  for (const cells of table.rows) {
    if (cells.length !== REGISTER_COLUMNS.length) {
      diagnostics.push(
        error(
          `NOW: the row '${bare(cells[0] ?? "")}' carries ${cells.length} cells where the register has ${REGISTER_COLUMNS.length}`,
        ),
      )
    }
  }
  const seen = new Set<string>()
  for (const row of rows) {
    if (!ID_PATTERN.test(row.id)) {
      diagnostics.push(error(`NOW: '${row.id}' is not an id of the form S<number>`))
      continue
    }
    if (seen.has(row.id)) diagnostics.push(error(`NOW: the id '${row.id}' is carried by two rows`))
    seen.add(row.id)
  }
  return diagnostics
}

const valueDiagnostics = (rows: Row[], themes: Set<string>) => {
  const diagnostics: Diagnostic[] = []
  const legal = [
    { column: "Kind", values: KINDS, of: (row: Row) => row.kind },
    { column: "Size", values: SIZES, of: (row: Row) => row.size },
    { column: "Readiness", values: READINESSES, of: (row: Row) => row.readiness },
    { column: "Executor", values: EXECUTORS, of: (row: Row) => row.executor },
  ]
  for (const row of rows) {
    for (const { column, values, of } of legal) {
      if (!values.includes(of(row))) {
        diagnostics.push(
          error(`${row.id}: '${of(row)}' is not a legal ${column}; expected ${values.join(", ")}`),
        )
      }
    }
    if (row.theme === GOAL_THEME && row.kind !== SPIKE) {
      diagnostics.push(
        error(`${row.id}: only a spike may claim the theme '${GOAL_THEME}', which declares that it validates the goal's feasibility`),
      )
    } else if (row.theme !== NONE && row.theme !== GOAL_THEME && !themes.has(row.theme)) {
      diagnostics.push(error(`${row.id}: the theme '${row.theme}' is not in the theme table`))
    }
  }
  return diagnostics
}

const cycleThrough = (rows: Row[]) => {
  const edges = new Map(rows.map((row) => [row.id, row.dependsOn]))
  const settled = new Set<string>()
  const walked: string[] = []
  const walk = (id: string): string[] | null => {
    if (settled.has(id)) return null
    const revisited = walked.indexOf(id)
    if (revisited !== -1) return [...walked.slice(revisited), id]
    walked.push(id)
    for (const next of edges.get(id) ?? []) {
      if (!edges.has(next)) continue
      const cycle = walk(next)
      if (cycle) return cycle
    }
    walked.pop()
    settled.add(id)
    return null
  }
  for (const row of rows) {
    const cycle = walk(row.id)
    if (cycle) return cycle
  }
  return null
}

const dependencyDiagnostics = (rows: Row[]) => {
  const diagnostics: Diagnostic[] = []
  const ids = new Set(rows.map((row) => row.id))
  for (const row of rows) {
    for (const dependency of row.dependsOn) {
      if (!ids.has(dependency)) {
        diagnostics.push(
          error(`${row.id}: 'Depends on' names '${dependency}', which is not a row of this register`),
        )
      }
    }
  }
  const cycle = cycleThrough(rows)
  if (cycle) {
    diagnostics.push(error(`NOW: 'Depends on' closes a cycle through ${cycle.join(" → ")}`))
  }
  return diagnostics
}

const sliceDocumentDiagnostics = (row: Row, document: SliceDocument) => {
  const label = `${SLICES_DIRECTORY}/${document.filename}`
  const diagnostics: Diagnostic[] = []

  const filename = SLICE_FILENAME_PATTERN.exec(document.filename)
  if (!filename) {
    diagnostics.push(error(`${label}: the filename must read S<id>-<slug>.md`))
  } else if (filename[1] !== row.id) {
    diagnostics.push(error(`${label}: the filename carries the id '${filename[1]}' and the register row '${row.id}'`))
  }

  const heading = H1_PATTERN.exec(document.text)
  const title = heading ? SLICE_TITLE_PATTERN.exec(heading[1]) : null
  if (!title) {
    diagnostics.push(error(`${label}: the title must read '# S<id> — <title>'`))
  } else {
    if (title[1] !== row.id) {
      diagnostics.push(error(`${label}: the title carries the id '${title[1]}' and the register row '${row.id}'`))
    }
    if (title[2] !== row.title) {
      diagnostics.push(error(`${label}: the title reads '${title[2]}' and the register row '${row.title}'`))
    }
  }

  if (!REGISTER_BACKLINK_PATTERN.test(document.text)) {
    diagnostics.push(error(`${label}: missing the link back to the register`))
  }

  const fields = parseFields(preambleOf(document.text))
  const fieldNames = fields.map((field) => field.name)
  for (const missing of missingNames(SLICE_FIELDS, fieldNames)) {
    diagnostics.push(error(`${label}: missing the '${missing}' field`))
  }
  if (isOutOfOrder(SLICE_FIELDS, fieldNames)) {
    diagnostics.push(error(`${label}: the fields must read ${SLICE_FIELDS.join(", ")}, in that order`))
  }
  for (const field of fields) {
    if (SLICE_FIELDS.includes(field.name) && field.value === "") {
      diagnostics.push(error(`${label}: the '${field.name}' field is empty`))
    }
  }

  const sections = parseSections(document.text)
  const sectionNames = sections.map((section) => section.name)
  const expected = SLICE_SECTIONS.filter(
    (name) => name !== "Audience" || row.kind !== SPIKE || sectionNames.includes("Audience"),
  )
  for (const missing of missingNames(expected, sectionNames)) {
    diagnostics.push(error(`${label}: missing the '${missing}' section`))
  }
  for (const unknown of unknownNames(SLICE_SECTIONS, sectionNames)) {
    diagnostics.push(error(`${label}: '${unknown}' is not a section of a slice document`))
  }
  if (isOutOfOrder(SLICE_SECTIONS, sectionNames)) {
    diagnostics.push(error(`${label}: the sections must read ${SLICE_SECTIONS.join(", ")}, in that order`))
  }
  for (const section of sections) {
    if (!SLICE_SECTIONS.includes(section.name)) continue
    const content = section.body.trim()
    if (content === "") {
      diagnostics.push(error(`${label}: the '${section.name}' section is empty`))
    } else if (section.name === "Audience" && content === NONE && row.kind !== SPIKE) {
      diagnostics.push(error(`${label}: only a spike may leave 'Audience' unfilled`))
    }
  }
  return diagnostics
}

const documentDiagnostics = (rows: Row[], slices: SliceDocument[]) => {
  const diagnostics: Diagnostic[] = []
  const byFilename = new Map(slices.map((slice) => [slice.filename, slice]))
  const claimed = new Set<string>()
  for (const row of rows) {
    const target = row.link.startsWith(`${SLICES_DIRECTORY}/`)
      ? row.link.slice(SLICES_DIRECTORY.length + 1)
      : null
    if (target === null) {
      diagnostics.push(error(`${row.id}: the title must link to ${SLICES_DIRECTORY}/S<id>-<slug>.md`))
      continue
    }
    const document = byFilename.get(target)
    if (!document) {
      diagnostics.push(error(`${row.id}: the title links to '${row.link}', which is not there`))
      continue
    }
    claimed.add(target)
    diagnostics.push(...sliceDocumentDiagnostics(row, document))
  }
  for (const slice of slices) {
    if (!claimed.has(slice.filename)) {
      diagnostics.push(
        error(`${SLICES_DIRECTORY}/${slice.filename}: no register row links to this document`),
      )
    }
  }
  return diagnostics
}

const idDiagnostics = (slices: SliceDocument[], archive: string[]) => {
  const diagnostics: Diagnostic[] = []
  const minted = new Map<string, string>()
  const filenames = [
    ...slices.map((slice) => ({ directory: SLICES_DIRECTORY, filename: slice.filename })),
    ...archive.map((filename) => ({ directory: ARCHIVE_DIRECTORY, filename })),
  ]
  for (const { directory, filename } of filenames) {
    const match = SLICE_FILENAME_PATTERN.exec(filename)
    if (!match) {
      diagnostics.push(error(`${directory}/${filename}: the filename must read S<id>-<slug>.md`))
      continue
    }
    const owner = minted.get(match[1])
    if (owner) {
      diagnostics.push(
        error(`${directory}/${filename}: the id '${match[1]}' is already spent by ${owner}; ids are never recycled`),
      )
      continue
    }
    minted.set(match[1], `${directory}/${filename}`)
  }
  return diagnostics
}

const horizonDiagnostics = (sections: Section[]) => {
  const diagnostics: Diagnostic[] = []
  for (const name of HORIZONS_WITHOUT_IDS) {
    const section = sectionNamed(sections, name)
    if (!section) continue
    section.body.split("\n").forEach((line, index) => {
      const found = ID_ANYWHERE_PATTERN.exec(line)
      if (found) {
        diagnostics.push(
          error(`${name}: line ${index + 1} carries the id '${found[0]}'; only a row of the register has one`),
        )
      }
    })
  }
  return diagnostics
}

const spikeDiagnostics = (rows: Row[]) => {
  const awaited = new Set(rows.flatMap((row) => row.dependsOn))
  return rows
    .filter((row) => row.kind === SPIKE && row.theme !== GOAL_THEME && !awaited.has(row.id))
    .map((row) =>
      error(
        `${row.id}: a spike needs a dependent — either a row names it in 'Depends on', or it claims the theme '${GOAL_THEME}'`,
      ),
    )
}

const countDiagnostics = (rows: Row[]) => {
  if (rows.length > REGISTER_CAP) {
    return [
      warning(
        `NOW: ${rows.length} rows are past the cap of ${REGISTER_CAP}; a bigger problem buys fatter slices, not more rows`,
      ),
    ]
  }
  if (rows.length < REGISTER_FLOOR) {
    return [
      warning(
        `NOW: ${rows.length} rows are below the floor of ${REGISTER_FLOOR}; a map this small does not repay its cost`,
      ),
    ]
  }
  return []
}

export const validateRoadmap = (contents: RoadmapDirectory): Diagnostic[] => {
  const sections = parseSections(contents.roadmap)
  const now = sectionNamed(sections, "NOW")
  const register = now ? parseTable(now.body) : { header: [], rows: [] }
  const rows = register.rows.map(parseRow)

  return [
    ...roadmapStructureDiagnostics(contents.roadmap, sections),
    ...themeTableDiagnostics(sections, rows),
    ...(now ? registerDiagnostics(register, rows) : []),
    ...valueDiagnostics(rows, themeSlugs(sections)),
    ...dependencyDiagnostics(rows),
    ...documentDiagnostics(rows, contents.slices),
    ...idDiagnostics(contents.slices, contents.archive),
    ...horizonDiagnostics(sections),
    ...spikeDiagnostics(rows),
    ...countDiagnostics(rows),
  ]
}

const markdownIn = (directory: string) =>
  existsSync(directory)
    ? readdirSync(directory)
        .filter((filename) => filename.endsWith(".md"))
        .sort()
    : []

export const readRoadmapDirectory = (directory: string): RoadmapDirectory => {
  const roadmap = join(directory, ROADMAP_FILE)
  if (!existsSync(roadmap)) throw new Error(`${roadmap} is not there`)
  const slices = join(directory, SLICES_DIRECTORY)
  return {
    roadmap: readFileSync(roadmap, "utf8"),
    slices: markdownIn(slices).map((filename) => ({
      filename,
      text: readFileSync(join(slices, filename), "utf8"),
    })),
    archive: markdownIn(join(directory, ARCHIVE_DIRECTORY)),
  }
}

export const main = (argv: string[]): number => {
  const directory = argv[0] ?? ".roadmap"
  let contents: RoadmapDirectory
  try {
    contents = readRoadmapDirectory(directory)
  } catch (cause) {
    console.error(`ERROR: ${cause instanceof Error ? cause.message : String(cause)}`)
    return 2
  }
  const diagnostics = validateRoadmap(contents)
  for (const diagnostic of diagnostics) {
    console.error(`${diagnostic.level.toUpperCase()}: ${diagnostic.message}`)
  }
  if (diagnostics.some((diagnostic) => diagnostic.level === "error")) return 1
  console.log(`OK: ${directory}`)
  return 0
}

// An installed skill is reached through a symlink, and process.argv[1] keeps the link path while
// import.meta.filename holds the target: comparing them unresolved makes the command exit 0 in
// silence on exactly the invocation SKILL.md prescribes.
const invokedAsCommand = () => {
  const entry = process.argv[1]
  if (entry === undefined) return false
  try {
    return realpathSync(entry) === import.meta.filename
  } catch {
    return false
  }
}

if (invokedAsCommand()) {
  process.exitCode = main(process.argv.slice(2))
}
