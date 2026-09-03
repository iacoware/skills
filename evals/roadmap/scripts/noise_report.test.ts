import { test } from "node:test"
import assert from "node:assert/strict"
import type { MapExtract, RowRecord } from "./extract_map.ts"
import {
  anchorOf,
  buildReport,
  buildResidual,
  residualCount,
  satelliteDirsOf,
} from "./noise_report.ts"

const mapOf = (run: string, over: Partial<MapExtract> = {}): MapExtract => ({
  run,
  themes: [],
  boundaries: [],
  rows: [],
  outOfScope: [],
  ...over,
})

const rowOf = (over: Partial<RowRecord>): RowRecord => ({
  id: "S1",
  title: "Riga",
  theme: "—",
  kind: "product",
  size: "small",
  dependsOn: [],
  ...over,
})

const theme = (name: string, promise = `promessa di ${name}`) => ({
  name,
  promise,
  firstValidator: "S1",
})

test("satellite directories are siblings with a suffix, trailing slash tolerated", () => {
  assert.deepEqual(satelliteDirsOf("results/ROADMAP-CC-6/"), [
    "results/ROADMAP-CC-6B",
    "results/ROADMAP-CC-6C",
  ])
})

test("anchorOf reads tree, model and effort back out of a PROMPT.md record", () => {
  const anchor = anchorOf(
    "| Modello | `opus` |\n| Effort | `high` |\n| `skills/roadmap` | tree `0913e60`, uguale a HEAD |",
  )

  assert.deepEqual(anchor, { tree: "0913e60", model: "opus", effort: "high", dirty: false })
})

test("anchorOf flags a record that declares uncommitted changes", () => {
  const anchor = anchorOf(
    "| `skills/roadmap` | tree `0913e60` a HEAD, **più modifiche non committate**: `x` |",
  )

  assert.equal(anchor.dirty, true)
})

test("identical twin maps leave no residual", () => {
  const twin = {
    themes: [theme("a")],
    rows: [rowOf({ id: "S1", title: "Riga uno" })],
    outOfScope: [{ title: "Escluso", rationale: "r" }],
  }

  const residual = buildResidual([mapOf("A", twin), mapOf("B", twin), mapOf("C", twin)])

  assert.equal(residualCount(residual), 0)
})

test("the residual holds only what the mechanical match left unpaired", () => {
  const maps = [
    mapOf("A", { themes: [theme("x"), theme("y")] }),
    mapOf("B", { themes: [theme("x"), theme("z")] }),
    mapOf("C", { themes: [theme("x")] }),
  ]

  const residual = buildResidual(maps)

  const ab = residual.pairs[0]
  assert.deepEqual([ab.left, ab.right], ["A", "B"])
  assert.deepEqual(ab.themes.left.map((item) => item.key), ["y"])
  assert.deepEqual(ab.themes.right.map((item) => item.key), ["z"])
})

test("a duplicated title never pairs mechanically: ambiguity goes to the residual", () => {
  const maps = [
    mapOf("A", { rows: [rowOf({ id: "S1", title: "Stessa" }), rowOf({ id: "S2", title: "Stessa" })] }),
    mapOf("B", { rows: [rowOf({ id: "S1", title: "Stessa" })] }),
    mapOf("C", { rows: [] }),
  ]

  const residual = buildResidual(maps)

  assert.deepEqual(residual.pairs[0].rows.left.map((item) => item.key), ["S1", "S2"])
  assert.deepEqual(residual.pairs[0].rows.right.map((item) => item.key), ["S1"])
})

const THREE = (a: Partial<MapExtract>, b: Partial<MapExtract>) => [
  mapOf("A", a),
  mapOf("B", b),
  mapOf("C", b),
]

const NO_ALIGNMENT = { pairs: [] }

// Il report si legge per blocchi: dentro una coppia di run, un asse alla volta. I test asseriscono
// dove asserisce l'occhio — dentro il blocco dell'asse, sotto il suo gruppo.
const axisBlock = (report: string, pair: string, axis: string) => {
  const section = (report.split(`### ${pair}\n`)[1] ?? "").split("\n### ")[0]
  return section.split(/\n(?=\*\*)/).find((block) => block.startsWith(`**${axis}**`)) ?? ""
}

test("a model judgement pairs the residual and carries its provenance into the report", () => {
  const maps = THREE({ themes: [theme("foto")] }, { themes: [theme("immagini")] })
  const alignment = {
    pairs: [{ left: "A", right: "B", themes: [{ left: "foto", right: "immagini" }] }],
  }

  const report = buildReport(maps, alignment)

  assert.match(axisBlock(report, "A ↔ B", "temi"), /Accoppiati:\n- `foto` = `immagini` — modello/)
  assert.match(axisBlock(report, "A ↔ C", "temi"), /Solo A:\n- `foto`/)
})

test("verdicts compare across a model-aligned theme rename", () => {
  const maps = THREE(
    {
      themes: [theme("x"), theme("y")],
      boundaries: [{ pair: ["x", "y"], verdict: "split", fact: "f" }],
    },
    {
      themes: [theme("x"), theme("z")],
      boundaries: [{ pair: ["x", "z"], verdict: "merge", fact: "f" }],
    },
  )
  const alignment = { pairs: [{ left: "A", right: "B", themes: [{ left: "y", right: "z" }] }] }

  const report = buildReport(maps, alignment)

  assert.match(axisBlock(report, "A ↔ B", "verdetti"), /Divergenti:\n- `x \/ y` — split ≠ merge/)
})

test("a boundary over an unaligned theme is not comparable, not a disagreement", () => {
  const maps = THREE(
    { themes: [theme("x"), theme("y")], boundaries: [{ pair: ["x", "y"], verdict: "split", fact: "f" }] },
    { themes: [theme("x")] },
  )

  const report = buildReport(maps, NO_ALIGNMENT)

  assert.match(
    axisBlock(report, "A ↔ B", "verdetti"),
    /Non confrontabili \(un tema della coppia non ha controparte\):\n- `x \/ y` — A/,
  )
})

test("edges agree through the row alignment even when the ids differ", () => {
  const maps = THREE(
    { rows: [rowOf({ id: "S1", title: "Uno" }), rowOf({ id: "S2", title: "Due", dependsOn: ["S1"] })] },
    { rows: [rowOf({ id: "S7", title: "Uno" }), rowOf({ id: "S9", title: "Due", dependsOn: ["S7"] })] },
  )

  const report = buildReport(maps, NO_ALIGNMENT)

  assert.match(axisBlock(report, "A ↔ B", "archi di dipendenza"), /accoppiati 1\n\nAccoppiati:\n- «Due» → «Uno»/)
})

test("an edge whose endpoint has no counterpart is not comparable", () => {
  const maps = THREE(
    { rows: [rowOf({ id: "S1", title: "Uno" }), rowOf({ id: "S2", title: "Solo qui", dependsOn: ["S1"] })] },
    { rows: [rowOf({ id: "S1", title: "Uno" })] },
  )

  const report = buildReport(maps, NO_ALIGNMENT)

  assert.match(
    axisBlock(report, "A ↔ B", "archi di dipendenza"),
    /Non confrontabili \(un estremo non ha controparte\):\n- «Solo qui» → «Uno» — A/,
  )
})

test("field divergence on an aligned row is measured, not an alignment failure", () => {
  const maps = THREE(
    { rows: [rowOf({ id: "S1", title: "Uno", size: "small" })] },
    { rows: [rowOf({ id: "S1", title: "Uno", size: "medium" })] },
  )

  const report = buildReport(maps, NO_ALIGNMENT)

  const righe = axisBlock(report, "A ↔ B", "righe")

  assert.match(righe, /Accoppiati:\n- «Uno» — meccanico/)
  assert.match(righe, /Divergenti:\n- «Uno» — size \(small ≠ medium\)/)
})

test("a proposal naming a spent or unknown key is rejected, not trusted", () => {
  const maps = THREE({ themes: [theme("x")] }, { themes: [theme("x")] })
  const alignment = { pairs: [{ left: "A", right: "B", themes: [{ left: "x", right: "x" }] }] }

  const report = buildReport(maps, alignment)

  assert.match(report, /## Proposte scartate dal validatore/)
  assert.match(report, /`x` = `x`: chiave inesistente o già accoppiata/)
})

test("an all-empty verdict axis is named agreement by absence, visibly", () => {
  const maps = THREE({ themes: [theme("x")] }, { themes: [theme("x")] })

  const report = buildReport(maps, NO_ALIGNMENT)

  assert.match(report, /L'asse verdetti è vuoto su entrambi i run/)
})

test("the synthesis counts each run on its own before any comparison, then the agreement", () => {
  const maps = [
    mapOf("A", { rows: [rowOf({ id: "S1", title: "Uno" })] }),
    mapOf("B", { rows: [rowOf({ id: "S1", title: "Uno" }), rowOf({ id: "S2", title: "Due" })] }),
    mapOf("C", { rows: [rowOf({ id: "S1", title: "Uno" })] }),
  ]

  const report = buildReport(maps, NO_ALIGNMENT)

  assert.match(report, /\| righe \| 1 \| 2 \| 1 \|/)
  assert.match(report, /\| righe \| 1\/2 \| 1\/1 \| 1\/2 \|/)
})
