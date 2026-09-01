import { mkdirSync, readFileSync, writeFileSync } from "node:fs"
import { join } from "node:path"
import { readMapExtract, type MapExtract } from "./extract_map.ts"

const SUFFIXES = ["B", "C"] as const

export const normalizeRunDir = (dir: string) => dir.replace(/\/+$/, "")

export const satelliteDirsOf = (mainDir: string) =>
  SUFFIXES.map((suffix) => `${normalizeRunDir(mainDir)}${suffix}`)

// L'ancoraggio che `run_cycle.ts` scrive nel PROMPT.md di ogni run headless, riletto: è quel che la
// guardia confronta con l'albero corrente, e quel che rende i satelliti gemelli (stesso modello ed
// effort del principale, qualunque flag riceva il driver).
export type Anchor = {
  tree: string | undefined
  model: string | undefined
  effort: string | undefined
  dirty: boolean
}

export const anchorOf = (promptRecord: string): Anchor => ({
  tree: /\| `skills\/roadmap` \| tree `([0-9a-f]+)`/.exec(promptRecord)?.[1],
  model: /\| Modello \| `([^`]+)` \|/.exec(promptRecord)?.[1],
  effort: /\| Effort \| `([^`]+)` \|/.exec(promptRecord)?.[1],
  dirty: /modifiche non committate/.test(promptRecord),
})

const AXES = ["themes", "rows", "outOfScope"] as const
type Axis = (typeof AXES)[number]
const AXIS_NOUN: Record<Axis, string> = { themes: "tema", rows: "riga", outOfScope: "out-of-scope" }

type Item = { key: string; matchOn: string; record: Record<string, unknown> }

const titleOf = (map: MapExtract, id: string) => map.rows.find((row) => row.id === id)?.title ?? id

// Gli id (S3, primo validator, archi) sono nomi locali al run: nel record che attraversa il confronto
// diventano titoli, che sono l'identità leggibile anche dall'altra parte.
const itemsOf = (map: MapExtract): Record<Axis, Item[]> => ({
  themes: map.themes.map((theme) => ({
    key: theme.name,
    matchOn: theme.name,
    record: { promise: theme.promise, firstValidator: titleOf(map, theme.firstValidator) },
  })),
  rows: map.rows.map((row) => ({
    key: row.id,
    matchOn: row.title,
    record: {
      title: row.title,
      theme: row.theme,
      kind: row.kind,
      size: row.size,
      dependsOn: row.dependsOn.map((id) => titleOf(map, id)),
    },
  })),
  outOfScope: map.outOfScope.map((exclusion) => ({
    key: exclusion.title,
    matchOn: exclusion.title,
    record: { rationale: exclusion.rationale },
  })),
})

type Pairing = { left: Item; right: Item; provenance: "meccanico" | "modello" }
type AxisResult = { aligned: Pairing[]; onlyLeft: Item[]; onlyRight: Item[]; rejected: string[] }

const uniqueByMatch = (items: Item[]) => {
  const counts = new Map<string, number>()
  for (const item of items) counts.set(item.matchOn, (counts.get(item.matchOn) ?? 0) + 1)
  return new Map(items.filter((item) => counts.get(item.matchOn) === 1).map((item) => [item.matchOn, item]))
}

// Il match meccanico accoppia le stringhe identiche; i giudizi del modello entrano solo sul residuo,
// e ogni proposta che nomina una chiave inesistente o già spesa è scartata, non fidata: il vincolo
// «una riga che mappa su due non è allineabile» lo fa rispettare il codice.
export const alignAxis = (
  left: Item[],
  right: Item[],
  proposed: { left: string; right: string }[],
): AxisResult => {
  const leftUnique = uniqueByMatch(left)
  const rightUnique = uniqueByMatch(right)
  const aligned: Pairing[] = []
  const usedLeft = new Set<string>()
  const usedRight = new Set<string>()

  for (const item of left) {
    const twin = leftUnique.has(item.matchOn) ? rightUnique.get(item.matchOn) : undefined
    if (twin === undefined) continue
    aligned.push({ left: item, right: twin, provenance: "meccanico" })
    usedLeft.add(item.key)
    usedRight.add(twin.key)
  }

  const rejected: string[] = []
  const byKeyLeft = new Map(left.map((item) => [item.key, item]))
  const byKeyRight = new Map(right.map((item) => [item.key, item]))
  for (const pair of proposed) {
    const leftItem = byKeyLeft.get(pair.left)
    const rightItem = byKeyRight.get(pair.right)
    if (leftItem === undefined || rightItem === undefined || usedLeft.has(pair.left) || usedRight.has(pair.right)) {
      rejected.push(`\`${pair.left}\` = \`${pair.right}\`: chiave inesistente o già accoppiata`)
      continue
    }
    aligned.push({ left: leftItem, right: rightItem, provenance: "modello" })
    usedLeft.add(pair.left)
    usedRight.add(pair.right)
  }

  return {
    aligned,
    onlyLeft: left.filter((item) => !usedLeft.has(item.key)),
    onlyRight: right.filter((item) => !usedRight.has(item.key)),
    rejected,
  }
}

const PAIR_INDICES = [
  [0, 1],
  [0, 2],
  [1, 2],
] as const

const stripped = (item: Item) => ({ key: item.key, ...item.record })

type ResidualAxis = { left: ReturnType<typeof stripped>[]; right: ReturnType<typeof stripped>[] }
type ResidualPair = { left: string; right: string } & Record<Axis, ResidualAxis>
export type Residual = { main: string; pairs: ResidualPair[] }

export const buildResidual = (maps: MapExtract[]): Residual => ({
  main: maps[0].run,
  pairs: PAIR_INDICES.map(([l, r]) => {
    const leftItems = itemsOf(maps[l])
    const rightItems = itemsOf(maps[r])
    const axes = Object.fromEntries(
      AXES.map((axis) => {
        const result = alignAxis(leftItems[axis], rightItems[axis], [])
        return [axis, { left: result.onlyLeft.map(stripped), right: result.onlyRight.map(stripped) }]
      }),
    ) as Record<Axis, ResidualAxis>
    return { left: maps[l].run, right: maps[r].run, ...axes }
  }),
})

export const residualCount = (residual: Residual) =>
  residual.pairs.reduce(
    (total, pair) => total + AXES.reduce((n, axis) => n + pair[axis].left.length + pair[axis].right.length, 0),
    0,
  )

const isRecord = (value: unknown): value is Record<string, unknown> =>
  typeof value === "object" && value !== null && !Array.isArray(value)

const proposedFor = (alignment: unknown, left: string, right: string, axis: Axis) => {
  const pairs = isRecord(alignment) && Array.isArray(alignment.pairs) ? alignment.pairs : []
  const found = pairs.find(
    (pair) => isRecord(pair) && pair.left === left && pair.right === right,
  ) as Record<string, unknown> | undefined
  const list = found?.[axis]
  if (!Array.isArray(list)) return []
  return list
    .filter((pair): pair is Record<string, unknown> => isRecord(pair))
    .filter((pair) => typeof pair.left === "string" && typeof pair.right === "string")
    .map((pair) => ({ left: pair.left as string, right: pair.right as string }))
}

type VerdictOutcome = {
  agree: number
  disagree: string[]
  onlyLeft: string[]
  onlyRight: string[]
  blind: string[]
  leftTotal: number
  rightTotal: number
}

const canonPair = (a: string, b: string) => [a, b].sort().join(" / ")

const verdictsOf = (leftMap: MapExtract, rightMap: MapExtract, themePairs: Pairing[]): VerdictOutcome => {
  const nameMap = new Map(themePairs.map((pair) => [pair.left.key, pair.right.key]))
  const alignedRight = new Set(themePairs.map((pair) => pair.right.key))
  const remaining = new Map(
    rightMap.boundaries.map((boundary) => [canonPair(boundary.pair[0], boundary.pair[1]), boundary]),
  )

  let agree = 0
  const disagree: string[] = []
  const onlyLeft: string[] = []
  const blind: string[] = []

  for (const boundary of leftMap.boundaries) {
    const mapped = boundary.pair.map((name) => nameMap.get(name))
    const label = `\`${boundary.pair.join(" / ")}\``
    if (mapped[0] === undefined || mapped[1] === undefined) {
      blind.push(`${label} (tema senza allineamento, ${leftMap.run})`)
      continue
    }
    const twin = remaining.get(canonPair(mapped[0], mapped[1]))
    if (twin === undefined) {
      onlyLeft.push(label)
      continue
    }
    remaining.delete(canonPair(mapped[0], mapped[1]))
    if (twin.verdict === boundary.verdict) agree += 1
    else disagree.push(`${label}: ${boundary.verdict} ≠ ${twin.verdict}`)
  }

  const onlyRight: string[] = []
  for (const boundary of remaining.values()) {
    const label = `\`${boundary.pair.join(" / ")}\``
    if (boundary.pair.some((name) => !alignedRight.has(name)))
      blind.push(`${label} (tema senza allineamento, ${rightMap.run})`)
    else onlyRight.push(label)
  }

  return {
    agree,
    disagree,
    onlyLeft,
    onlyRight,
    blind,
    leftTotal: leftMap.boundaries.length,
    rightTotal: rightMap.boundaries.length,
  }
}

type EdgeOutcome = { agree: number; onlyLeft: string[]; onlyRight: string[]; blind: string[] }

const edgesOf = (map: MapExtract) =>
  map.rows.flatMap((row) => row.dependsOn.map((dependency) => [row.id, dependency] as const))

const edgeLabel = (map: MapExtract, [from, to]: readonly [string, string]) =>
  `«${titleOf(map, from)}» → «${titleOf(map, to)}»`

const edgeOutcomeOf = (leftMap: MapExtract, rightMap: MapExtract, rowPairs: Pairing[]): EdgeOutcome => {
  const idMap = new Map(rowPairs.map((pair) => [pair.left.key, pair.right.key]))
  const alignedRight = new Set(rowPairs.map((pair) => pair.right.key))
  const remaining = new Set(edgesOf(rightMap).map(([from, to]) => `${from}->${to}`))

  let agree = 0
  const onlyLeft: string[] = []
  const blind: string[] = []
  for (const edge of edgesOf(leftMap)) {
    const from = idMap.get(edge[0])
    const to = idMap.get(edge[1])
    if (from === undefined || to === undefined) {
      blind.push(`${edgeLabel(leftMap, edge)} (estremo senza allineamento, ${leftMap.run})`)
    } else if (remaining.delete(`${from}->${to}`)) {
      agree += 1
    } else {
      onlyLeft.push(edgeLabel(leftMap, edge))
    }
  }

  const onlyRight: string[] = []
  for (const key of remaining) {
    const edge = key.split("->") as unknown as readonly [string, string]
    if (alignedRight.has(edge[0]) && alignedRight.has(edge[1])) onlyRight.push(edgeLabel(rightMap, edge))
    else blind.push(`${edgeLabel(rightMap, edge)} (estremo senza allineamento, ${rightMap.run})`)
  }

  return { agree, onlyLeft, onlyRight, blind }
}

const ROW_FIELDS = ["theme", "kind", "size"] as const

const rowDivergences = (pairing: Pairing, themeMap: Map<string, string>) =>
  ROW_FIELDS.filter((field) => {
    const left = String(pairing.left.record[field])
    const right = String(pairing.right.record[field])
    // Il tema è un nome locale al run: prima di confrontarlo passa per l'allineamento dei temi.
    const mapped = field === "theme" ? (themeMap.get(left) ?? left) : left
    return mapped !== right
  }).map(
    (field) => `${field} (${String(pairing.left.record[field])} ≠ ${String(pairing.right.record[field])})`,
  )

const itemLabel = (axis: Axis, item: Item) =>
  axis === "themes" ? `\`${item.key}\`` : axis === "rows" ? `«${item.matchOn}»` : `«${item.key}»`

const provenanceSplit = (result: AxisResult) => {
  const mechanical = result.aligned.filter((pair) => pair.provenance === "meccanico").length
  return `${mechanical}/${result.aligned.length - mechanical}`
}

const pairingLine = (axis: Axis, pairing: Pairing, note = "") => {
  const same = pairing.left.matchOn === pairing.right.matchOn && pairing.left.key === pairing.right.key
  const identity = same
    ? itemLabel(axis, pairing.left)
    : `${itemLabel(axis, pairing.left)} = ${itemLabel(axis, pairing.right)}`
  return `- ${AXIS_NOUN[axis]} ${identity} — ${pairing.provenance}${note}`
}

const summaryRow = (cells: (string | number)[]) => `| ${cells.join(" | ")} |`

export const buildReport = (maps: MapExtract[], alignment: unknown, anchor?: Anchor): string => {
  const sections: string[] = []
  const rejected: string[] = []

  for (const [l, r] of PAIR_INDICES) {
    const leftMap = maps[l]
    const rightMap = maps[r]
    const leftItems = itemsOf(leftMap)
    const rightItems = itemsOf(rightMap)

    const results = Object.fromEntries(
      AXES.map((axis) => [
        axis,
        alignAxis(leftItems[axis], rightItems[axis], proposedFor(alignment, leftMap.run, rightMap.run, axis)),
      ]),
    ) as Record<Axis, AxisResult>
    for (const axis of AXES)
      rejected.push(
        ...results[axis].rejected.map((line) => `${leftMap.run} ↔ ${rightMap.run}, ${AXIS_NOUN[axis]}: ${line}`),
      )

    const verdicts = verdictsOf(leftMap, rightMap, results.themes.aligned)
    const edges = edgeOutcomeOf(leftMap, rightMap, results.rows.aligned)
    const themeMap = new Map(results.themes.aligned.map((pair) => [pair.left.key, pair.right.key]))
    const divergentRows = results.rows.aligned
      .map((pairing) => ({ pairing, fields: rowDivergences(pairing, themeMap) }))
      .filter(({ fields }) => fields.length > 0)

    const lines: string[] = []
    for (const axis of AXES) {
      for (const pairing of results[axis].aligned) {
        const fields = axis === "rows" ? rowDivergences(pairing, themeMap) : []
        lines.push(pairingLine(axis, pairing, fields.length > 0 ? `; diverge su ${fields.join(", ")}` : ""))
      }
      for (const item of results[axis].onlyLeft)
        lines.push(`- ${AXIS_NOUN[axis]} ${itemLabel(axis, item)} — non allineabile (solo ${leftMap.run})`)
      for (const item of results[axis].onlyRight)
        lines.push(`- ${AXIS_NOUN[axis]} ${itemLabel(axis, item)} — non allineabile (solo ${rightMap.run})`)
    }
    lines.push(...verdicts.disagree.map((line) => `- verdetto ${line}`))
    lines.push(...verdicts.onlyLeft.map((line) => `- verdetto ${line} — solo ${leftMap.run}`))
    lines.push(...verdicts.onlyRight.map((line) => `- verdetto ${line} — solo ${rightMap.run}`))
    lines.push(...verdicts.blind.map((line) => `- verdetto ${line}`))
    if (edges.agree > 0) lines.push(`- archi concordi: ${edges.agree}`)
    lines.push(...edges.onlyLeft.map((line) => `- arco ${line} — solo ${leftMap.run}`))
    lines.push(...edges.onlyRight.map((line) => `- arco ${line} — solo ${rightMap.run}`))
    lines.push(...edges.blind.map((line) => `- arco ${line}`))

    const emptyVerdicts = verdicts.leftTotal === 0 && verdicts.rightTotal === 0

    sections.push(
      [
        `### ${leftMap.run} ↔ ${rightMap.run}`,
        "",
        summaryRow(["Asse", "Accoppiati", "mecc/mod", "Divergenti", `Solo ${leftMap.run}`, `Solo ${rightMap.run}`, "Non confrontabili"]),
        summaryRow(Array(7).fill("---")),
        summaryRow([
          "temi",
          results.themes.aligned.length,
          provenanceSplit(results.themes),
          "—",
          results.themes.onlyLeft.length,
          results.themes.onlyRight.length,
          "—",
        ]),
        summaryRow([
          "verdetti",
          verdicts.agree + verdicts.disagree.length,
          "—",
          verdicts.disagree.length,
          verdicts.onlyLeft.length,
          verdicts.onlyRight.length,
          verdicts.blind.length,
        ]),
        summaryRow([
          "righe",
          results.rows.aligned.length,
          provenanceSplit(results.rows),
          divergentRows.length,
          results.rows.onlyLeft.length,
          results.rows.onlyRight.length,
          "—",
        ]),
        summaryRow([
          "archi",
          edges.agree,
          "—",
          "—",
          edges.onlyLeft.length,
          edges.onlyRight.length,
          edges.blind.length,
        ]),
        summaryRow([
          "out-of-scope",
          results.outOfScope.aligned.length,
          provenanceSplit(results.outOfScope),
          "—",
          results.outOfScope.onlyLeft.length,
          results.outOfScope.onlyRight.length,
          "—",
        ]),
        ...(emptyVerdicts
          ? [
              "",
              "L'asse verdetti è vuoto su entrambi i run: accordo per assenza. Se la skill registra i",
              "verdetti altrove, è l'estrattore a non leggerli, non i run a concordare.",
            ]
          : []),
        "",
        "Accoppiamenti e casi:",
        "",
        ...lines,
      ].join("\n"),
    )
  }

  return [
    `# Noise — ${maps[0].run}`,
    "",
    "Generato da `make eval-noise RUN=<dir del principale>`: mai scritto a mano, rigenerabile. A",
    "differenza di `METRICS.md` non è derivato puro: la colonna di provenienza distingue gli",
    "accoppiamenti meccanici da quelli giudicati dalla sessione di allineamento",
    "(`../../prompts/noise.prompt.md` su `noise/residual.json`, giudizi in `noise/alignment.json`),",
    "e rilanciando possono cambiare al più quei giudizi. Il disegno è",
    "`design/roadmap/EVAL-NOISE.md`.",
    "",
    `Run gemelli: ${maps.map((map) => `\`${map.run}\``).join(", ")} — stessa skill` +
      (anchor?.tree !== undefined ? ` (tree \`${anchor.tree}\`)` : "") +
      ", stesso prompt, stesso modello ed effort.",
    "",
    "Misura l'accordo tra run a versione ferma, non la qualità contro le regole: i casi non",
    "allineabili non sono errori dello strumento, sono la misura.",
    "",
    "## Accordo per asse",
    "",
    sections.join("\n\n"),
    ...(rejected.length > 0
      ? ["", "## Proposte scartate dal validatore", "", ...rejected.map((line) => `- ${line}`)]
      : []),
    "",
  ].join("\n")
}

export const prepareNoise = (mainDir: string) => {
  const main = normalizeRunDir(mainDir)
  const maps = [main, ...satelliteDirsOf(main)].map(readMapExtract)
  const residual = buildResidual(maps)
  mkdirSync(join(main, "noise"), { recursive: true })
  writeFileSync(join(main, "noise", "residual.json"), `${JSON.stringify(residual, null, 2)}\n`)
  return residualCount(residual)
}

export const reportNoise = (mainDir: string) => {
  const main = normalizeRunDir(mainDir)
  const maps = [main, ...satelliteDirsOf(main)].map(readMapExtract)
  const alignment = JSON.parse(readFileSync(join(main, "noise", "alignment.json"), "utf8")) as unknown
  const anchor = ((): Anchor | undefined => {
    try {
      return anchorOf(readFileSync(join(main, "PROMPT.md"), "utf8"))
    } catch {
      return undefined
    }
  })()
  writeFileSync(join(main, "NOISE.md"), buildReport(maps, alignment, anchor))
}

export const main = (argv: string[]): number => {
  const [mode, dir] = argv
  if (dir === undefined || (mode !== "--prepare" && mode !== "--report")) {
    console.error("uso: noise_report.ts --prepare|--report <run directory del principale>")
    return 2
  }
  try {
    if (mode === "--prepare") {
      const count = prepareNoise(dir)
      console.log(`residuo: ${count} record -> ${normalizeRunDir(dir)}/noise/residual.json`)
    } else {
      reportNoise(dir)
      console.log(`noise -> ${normalizeRunDir(dir)}/NOISE.md`)
    }
    return 0
  } catch (cause) {
    console.error(`ERROR: ${cause instanceof Error ? cause.message : String(cause)}`)
    return 1
  }
}

if (process.argv[1]?.endsWith("noise_report.ts")) {
  process.exitCode = main(process.argv.slice(2))
}
