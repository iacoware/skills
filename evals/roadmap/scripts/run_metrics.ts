import { readFileSync, writeFileSync } from "node:fs"
import { basename, join } from "node:path"

const TOKEN_FIELDS = [
  ["input_tokens", "input non-cache"],
  ["cache_creation_input_tokens", "cache creation"],
  ["cache_read_input_tokens", "cache read"],
  ["output_tokens", "output"],
] as const

const isRecord = (value: unknown): value is Record<string, unknown> =>
  typeof value === "object" && value !== null && !Array.isArray(value)

const at = (value: unknown, ...path: string[]): unknown =>
  path.reduce<unknown>((node, key) => (isRecord(node) ? node[key] : undefined), value)

const stringAt = (value: unknown, ...path: string[]) => {
  const found = at(value, ...path)
  return typeof found === "string" ? found : undefined
}

const numberAt = (value: unknown, ...path: string[]) => {
  const found = at(value, ...path)
  return typeof found === "number" ? found : 0
}

const arrayAt = (value: unknown, ...path: string[]) => {
  const found = at(value, ...path)
  return Array.isArray(found) ? found : []
}

const textOf = (message: unknown): string => {
  const content = at(message, "content")
  if (typeof content === "string") return content
  return arrayAt(message, "content")
    .map((block) => (stringAt(block, "type") === "text" ? (stringAt(block, "text") ?? "") : ""))
    .join("")
}

const holdsToolResult = (message: unknown) =>
  arrayAt(message, "content").some((block) => stringAt(block, "type") === "tool_result")

// A local command (`/clear`, `/compact`) reaches the transcript as a user entry but never reaches the
// model: counting one as a prompt would put the run's start before the request that produced the map.
const isLocalCommand = (text: string) => text.trimStart().startsWith("<command-name>")

// A sub-agent's turn arrives as a user entry too, and it is the driver working rather than waiting.
const isPrompt = (entry: unknown) =>
  stringAt(entry, "type") === "user" &&
  at(entry, "isMeta") !== true &&
  at(entry, "isSidechain") !== true &&
  !holdsToolResult(at(entry, "message")) &&
  textOf(at(entry, "message")).trim() !== "" &&
  !isLocalCommand(textOf(at(entry, "message")))

const toolLabel = (block: unknown) => {
  const name = stringAt(block, "name") ?? "?"
  const target =
    name === "Skill"
      ? stringAt(block, "input", "skill")
      : name === "Task"
        ? stringAt(block, "input", "subagent_type")
        : undefined
  return target ? `${name} (${target})` : name
}

const duration = (milliseconds: number) => {
  const total = Math.round(milliseconds / 1000)
  const minutes = Math.floor(total / 60)
  const seconds = total % 60
  return minutes === 0 ? `${seconds}s` : `${minutes}m ${String(seconds).padStart(2, "0")}s`
}

const thousands = (value: number) => value.toLocaleString("en-US").replace(/,/g, ".")

const share = (part: number, whole: number) =>
  whole === 0 ? "—" : `${Math.round((part / whole) * 100)}%`

type Totals = Record<string, number>

type Metrics = {
  run: string
  lines: number
  session: { from: string; to: string }
  span: number
  active: number
  idle: number
  prompts: number
  calls: { main: number; sidechain: number }
  slowest: number
  models: string[]
  tokens: { main: Totals; sidechain: Totals }
  tools: Map<string, number>
}

const collect = (run: string, lines: string[]): Metrics => {
  const entries = lines.map((line) => JSON.parse(line) as unknown)
  const stamped = entries
    .filter((entry) => stringAt(entry, "timestamp") !== undefined)
    .sort((left, right) => (stringAt(left, "timestamp")! < stringAt(right, "timestamp")! ? -1 : 1))
  if (stamped.length === 0) throw new Error(`${run}: no timestamped entry`)

  const millis = (entry: unknown) => Date.parse(stringAt(entry, "timestamp")!)
  const firstPrompt = stamped.find(isPrompt)
  const from = firstPrompt ?? stamped[0]
  const to = stamped[stamped.length - 1]

  let idle = 0
  let slowest = 0
  for (const [index, entry] of stamped.entries()) {
    // Whatever happened before the request that started the run is not the run.
    if (index === 0 || millis(entry) <= millis(from)) continue
    const gap = millis(entry) - millis(stamped[index - 1])
    // Waiting for the person to type is not the skill being slow, so it leaves the active time.
    if (isPrompt(entry)) idle += gap
    else slowest = Math.max(slowest, gap)
  }

  const empty = (): Totals => ({ thinking: 0, ...Object.fromEntries(TOKEN_FIELDS.map(([key]) => [key, 0])) })
  const tokens = { main: empty(), sidechain: empty() }
  const calls = { main: 0, sidechain: 0 }
  const models = new Set<string>()
  const tools = new Map<string, number>()

  for (const entry of entries) {
    const side = at(entry, "isSidechain") === true ? "sidechain" : "main"
    if (stringAt(entry, "type") === "assistant" && isRecord(at(entry, "message"))) {
      const message = at(entry, "message")
      calls[side] += 1
      const model = stringAt(message, "model")
      if (model) models.add(model)
      for (const [key] of TOKEN_FIELDS) tokens[side][key] += numberAt(message, "usage", key)
      tokens[side].thinking += numberAt(message, "usage", "output_tokens_details", "thinking_tokens")
    }
    for (const block of arrayAt(at(entry, "message"), "content")) {
      if (stringAt(block, "type") !== "tool_use") continue
      const label = toolLabel(block)
      tools.set(label, (tools.get(label) ?? 0) + 1)
    }
  }

  const span = millis(to) - millis(from)
  return {
    run,
    lines: lines.length,
    session: { from: stringAt(stamped[0], "timestamp")!, to: stringAt(to, "timestamp")! },
    span,
    active: span - idle,
    idle,
    prompts: entries.filter(isPrompt).length,
    calls,
    slowest,
    models: [...models],
    tokens,
    tools,
  }
}

const render = (metrics: Metrics) => {
  const { main, sidechain } = metrics.tokens
  const withSidechain = metrics.calls.sidechain > 0
  const columns = withSidechain ? ["Voce", "Main", "Sub-agent", "Totale"] : ["Voce", "Totale"]
  const tokenRow = (label: string, key: string) => {
    const total = main[key] + sidechain[key]
    return withSidechain
      ? `| ${label} | ${thousands(main[key])} | ${thousands(sidechain[key])} | ${thousands(total)} |`
      : `| ${label} | ${thousands(total)} |`
  }
  const totalCalls = metrics.calls.main + metrics.calls.sidechain
  const totalOutput = main.output_tokens + sidechain.output_tokens
  const totalThinking = main.thinking + sidechain.thinking
  const totalRead = main.cache_read_input_tokens + sidechain.cache_read_input_tokens

  return [
    `# Metrics — ${metrics.run}`,
    "",
    "Generato da `make run-metrics RUN=<dir>` leggendo `TRANSCRIPT.jsonl`. Nessun numero scritto a",
    "mano: rigenerabile finché il transcript resta.",
    "",
    `**Transcript:** ${metrics.lines} righe · **Modello:** ${metrics.models.map((model) => `\`${model}\``).join(", ") || "—"} · **Sessione:** ${metrics.session.from} → ${metrics.session.to}`,
    "",
    "## Tempo",
    "",
    "| | |",
    "|---|---|",
    `| Dal primo prompt all'ultimo evento | ${duration(metrics.span)} |`,
    `| Di cui attesa dell'utente | ${duration(metrics.idle)} |`,
    `| **Tempo attivo** | **${duration(metrics.active)}** |`,
    `| Chiamata più lenta | ${duration(metrics.slowest)} |`,
    `| Media per chiamata | ${totalCalls === 0 ? "—" : duration(metrics.active / totalCalls)} |`,
    "",
    "## Token",
    "",
    `| ${columns.join(" | ")} |`,
    `|${columns.map(() => "---").join("|")}|`,
    ...TOKEN_FIELDS.map(([key, label]) => tokenRow(label, key)),
    tokenRow("↳ di cui thinking", "thinking"),
    "",
    `Thinking sull'output: **${share(totalThinking, totalOutput)}**. Cache read per chiamata: **${totalCalls === 0 ? "—" : thousands(Math.round(totalRead / totalCalls))}**.`,
    "",
    "## Turni",
    "",
    "| | |",
    "|---|---|",
    `| Prompt dell'utente | ${metrics.prompts} |`,
    `| Chiamate API | ${withSidechain ? `${totalCalls} (${metrics.calls.main} main, ${metrics.calls.sidechain} sub-agent)` : totalCalls} |`,
    "",
    "## Tool",
    "",
    "| Tool | Chiamate |",
    "|---|---|",
    ...[...metrics.tools]
      .sort((left, right) => right[1] - left[1] || left[0].localeCompare(right[0]))
      .map(([label, count]) => `| \`${label}\` | ${count} |`),
    ...(metrics.tools.size === 0 ? ["| — | 0 |"] : []),
    "",
  ].join("\n")
}

export const main = (argv: string[]): number => {
  const directory = argv[0]
  if (directory === undefined) {
    console.error("usage: run_metrics.ts <run directory>")
    return 2
  }
  const transcript = join(directory, "TRANSCRIPT.jsonl")
  try {
    const lines = readFileSync(transcript, "utf8").split("\n").filter((line) => line.trim() !== "")
    const output = join(directory, "METRICS.md")
    writeFileSync(output, render(collect(basename(directory), lines)))
    console.log(`metrics -> ${output}`)
    return 0
  } catch (cause) {
    console.error(`ERROR: ${cause instanceof Error ? cause.message : String(cause)}`)
    return 1
  }
}

process.exitCode = main(process.argv.slice(2))
