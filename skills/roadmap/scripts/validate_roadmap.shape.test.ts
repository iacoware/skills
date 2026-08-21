import { test } from "node:test"
import assert from "node:assert/strict"
import { readFileSync } from "node:fs"
import { join } from "node:path"
import { SHAPE } from "./validate_roadmap.ts"

const ASSETS = join(import.meta.dirname, "..", "assets")
const roadmapTemplate = readFileSync(join(ASSETS, "roadmap-template.md"), "utf8")
const sliceTemplate = readFileSync(join(ASSETS, "slice-template.md"), "utf8")

const headings = (template: string) =>
  [...template.matchAll(/^## (?!#)(.+?)[ \t]*$/gm)].map(([, name]) => name)

const fields = (template: string) =>
  [...template.matchAll(/^\*\*([^*:]+):\*\*/gm)].map(([, name]) => name)

const tableHeader = (template: string, heading: string) => {
  const section = template.split(new RegExp(`^## ${heading}$`, "m"))[1]
  assert.ok(section, `the template no longer has a '${heading}' section`)

  const header = section.split("\n").find((line) => line.startsWith("|"))
  assert.ok(header, `'${heading}' no longer holds a table`)

  return header
    .split("|")
    .slice(1, -1)
    .map((cell) => cell.trim())
}

const vocabulary = (column: string) => {
  const sentence = roadmapTemplate.match(new RegExp("`" + column + "` is ([^;.]+)"))
  assert.ok(sentence, `the register template no longer says what \`${column}\` may hold`)

  return [...sentence[1].matchAll(/`([^`]+)`/g)].map(([, value]) => value)
}

test("the roadmap template declares the sections the validator enforces, in order", () => {
  assert.deepEqual(headings(roadmapTemplate), SHAPE.roadmapSections)
})

test("the roadmap template declares the fields the validator enforces", () => {
  assert.deepEqual(fields(roadmapTemplate), SHAPE.roadmapFields)
})

test("the register template declares the columns the validator enforces", () => {
  assert.deepEqual(tableHeader(roadmapTemplate, "NOW"), SHAPE.registerColumns)
})

test("the themes template declares the columns the validator enforces", () => {
  assert.deepEqual(tableHeader(roadmapTemplate, "Themes"), SHAPE.themeColumns)
})

test("the slice template declares the sections the validator enforces, in order", () => {
  assert.deepEqual(headings(sliceTemplate), SHAPE.sliceSections)
})

test("the slice template declares the fields the validator enforces", () => {
  assert.deepEqual(fields(sliceTemplate), SHAPE.sliceFields)
})

const ENUMERATED_COLUMNS = [
  ["Kind", SHAPE.kinds],
  ["Size", SHAPE.sizes],
  ["Readiness", SHAPE.readinesses],
  ["Executor", SHAPE.executors],
] as const

for (const [column, values] of ENUMERATED_COLUMNS) {
  test(`the register template declares what \`${column}\` may hold`, () => {
    assert.deepEqual(vocabulary(column), values)
  })
}
