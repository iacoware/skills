import { readFileSync } from "node:fs"
import { basename, join } from "node:path"

export type ThemeRecord = { name: string; promise: string; firstValidator: string }
export type BoundaryRecord = { pair: [string, string]; verdict: string; fact: string }
export type RowRecord = {
  id: string
  title: string
  theme: string
  kind: string
  size: string
  dependsOn: string[]
}
export type ExclusionRecord = { title: string; rationale: string }

export type MapExtract = {
  run: string
  themes: ThemeRecord[]
  boundaries: BoundaryRecord[]
  rows: RowRecord[]
  outOfScope: ExclusionRecord[]
}

const H2_PATTERN = /^## (?!#)(.+?)[ \t]*$/gm
const SEPARATOR_CELL_PATTERN = /^:?-+:?$/
const LINK_PATTERN = /^\[(.+)\]\((.+)\)$/
const BOUNDARY_PATTERN = /^`(.+?)`\s*\/\s*`(.+?)`\s*[—–-]+\s*\*\*(.+?)[.:]?\*\*\s*(.*)$/
const EXCLUSION_PATTERN = /^\*\*(.+?)[.:]?\*\*\s*(.*)$/
const NONE = "—"

const bare = (cell: string) => {
  const match = /^`(.+)`$/.exec(cell.trim())
  return match ? match[1] : cell.trim()
}

const sectionOf = (text: string, name: string) => {
  const matches = [...text.matchAll(H2_PATTERN)]
  const index = matches.findIndex((match) => match[1].trim() === name)
  if (index === -1) return ""
  const start = matches[index].index + matches[index][0].length
  const next = matches[index + 1]
  return text.slice(start, next ? next.index : text.length)
}

const tableRows = (body: string) =>
  body
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line.startsWith("|") && line.endsWith("|"))
    .slice(1)
    .map((line) => line.slice(1, -1).split("|").map((cell) => cell.trim()))
    .filter((cells) => !cells.every((cell) => SEPARATOR_CELL_PATTERN.test(cell)))

const bullets = (body: string) => {
  const items: string[] = []
  for (const line of body.split("\n")) {
    if (/^- \S/.test(line)) items.push(line.slice(2).trim())
    else if (/^\s{2,}\S/.test(line) && items.length > 0) items[items.length - 1] += ` ${line.trim()}`
  }
  return items
}

const parseIds = (cell: string) => {
  const value = cell.trim()
  return value === NONE || value === "" ? [] : value.split(",").map(bare)
}

// The parse never fails on a missing or malformed section: an axis that is absent extracts as empty,
// and empty against empty is agreement the report makes visible rather than an error here.
export const extractMap = (run: string, roadmap: string): MapExtract => {
  const themesBody = sectionOf(roadmap, "Themes")

  const themes = tableRows(themesBody).map((cells) => ({
    name: bare(cells[0] ?? ""),
    promise: cells[1] ?? "",
    firstValidator: bare(cells[2] ?? ""),
  }))

  const boundaries = bullets(themesBody)
    .map((item) => BOUNDARY_PATTERN.exec(item))
    .filter((match) => match !== null)
    .map((match) => ({
      pair: [match[1], match[2]] as [string, string],
      verdict: match[3].trim().toLowerCase(),
      fact: match[4].trim(),
    }))

  const rows = tableRows(sectionOf(roadmap, "NOW")).map((cells) => {
    const titleCell = cells[1] ?? ""
    const link = LINK_PATTERN.exec(titleCell)
    return {
      id: bare(cells[0] ?? ""),
      title: link ? link[1].trim() : titleCell,
      theme: bare(cells[2] ?? ""),
      kind: bare(cells[3] ?? ""),
      size: bare(cells[4] ?? ""),
      dependsOn: parseIds(cells[7] ?? ""),
    }
  })

  const outOfScope = bullets(sectionOf(roadmap, "OUT-OF-SCOPE"))
    .map((item) => EXCLUSION_PATTERN.exec(item))
    .filter((match) => match !== null)
    .map((match) => ({ title: match[1].trim(), rationale: match[2].trim() }))

  return { run, themes, boundaries, rows, outOfScope }
}

export const readMapExtract = (runDir: string): MapExtract => {
  const dir = runDir.replace(/\/+$/, "")
  return extractMap(basename(dir), readFileSync(join(dir, ".roadmap", "roadmap.md"), "utf8"))
}

if (process.argv[1]?.endsWith("extract_map.ts")) {
  const dir = process.argv[2]
  if (dir === undefined) {
    console.error("uso: extract_map.ts <run directory>")
    process.exit(2)
  }
  console.log(JSON.stringify(readMapExtract(dir), null, 2))
}
