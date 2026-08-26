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

// One provider request reaches the transcript as one assistant entry per content block — a thinking
// block, a text block, a tool call — and every one of them repeats the request's `usage`. Summing per
// entry counts the same tokens two or three times, so the request is the unit here and `requestId` is
// what groups it. Older entries that carry none stand alone under their own uuid.
const requestKey = (entry: unknown) => stringAt(entry, "requestId") ?? `uuid:${stringAt(entry, "uuid")}`

const WRITES = /(^|[^0-9&>])>>?[^&]|\btee\b|\bsed\b[^|;&]*\s-i\b|\b(mv|cp|rm|install)\b/
// Running the validator, not reading it: the session opens `validate_roadmap.ts` with `sed` and
// `grep` too, and that is reading the payload like any other file.
const VALIDATES = /(^|[\s&|;])node\b[^|;&]*validate_roadmap/
const READS = /\b(cat|sed|head|tail|less|more|grep|rg|find|ls|wc|diff|awk|jq|file|stat|tree)\b/
const WRITE_TOOLS = new Set(["Write", "Edit", "MultiEdit", "NotebookEdit"])
const READ_TOOLS = new Set(["Read", "Grep", "Glob", "NotebookRead", "WebFetch", "WebSearch"])

const PHASES = [
  ["thinking", "Thinking"],
  ["writing", "Scrittura dei documenti"],
  ["reading", "Lettura"],
  ["validating", "Validazione"],
  ["talking", "Parola all'autore"],
  ["other", "Altro"],
] as const

type Phase = (typeof PHASES)[number][0]

// What the request did, at its strongest: a turn that wrote a file was producing the map even when it
// also listed a directory. `talking` is the turn that called no tool at all — the questions the
// session asks and the four-part report it closes on.
const phaseOf = (calls: { name: string; command: string }[]): Exclude<Phase, "thinking"> => {
  if (calls.length === 0) return "talking"
  if (calls.some(({ name, command }) => WRITE_TOOLS.has(name) || WRITES.test(command))) return "writing"
  if (calls.some(({ command }) => VALIDATES.test(command))) return "validating"
  if (calls.some(({ name, command }) => READ_TOOLS.has(name) || READS.test(command))) return "reading"
  return "other"
}

type Totals = Record<string, number>

type Request = {
  side: "main" | "sidechain"
  entries: unknown[]
  tokens: Totals
  phase: Exclude<Phase, "thinking">
}

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
  phases: Record<Phase, number>
  overhead: number
}

const emptyTotals = (): Totals => ({
  thinking: 0,
  ...Object.fromEntries(TOKEN_FIELDS.map(([key]) => [key, 0])),
})

const collectRequests = (stamped: unknown[]): Request[] => {
  const byKey = new Map<string, Request>()
  const order: Request[] = []

  for (const entry of stamped) {
    if (stringAt(entry, "type") !== "assistant" || !isRecord(at(entry, "message"))) continue
    const key = requestKey(entry)
    const existing = byKey.get(key)
    if (existing) {
      existing.entries.push(entry)
      continue
    }
    const message = at(entry, "message")
    const tokens = emptyTotals()
    for (const [field] of TOKEN_FIELDS) tokens[field] = numberAt(message, "usage", field)
    tokens.thinking = numberAt(message, "usage", "output_tokens_details", "thinking_tokens")
    const request: Request = {
      side: at(entry, "isSidechain") === true ? "sidechain" : "main",
      entries: [entry],
      tokens,
      phase: "other",
    }
    byKey.set(key, request)
    order.push(request)
  }

  for (const request of order) {
    const calls = request.entries
      .flatMap((entry) => arrayAt(at(entry, "message"), "content"))
      .filter((block) => stringAt(block, "type") === "tool_use")
      .map((block) => ({
        name: stringAt(block, "name") ?? "",
        command: stringAt(block, "input", "command") ?? "",
      }))
    request.phase = phaseOf(calls)
  }

  return order
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
  for (const [index, entry] of stamped.entries()) {
    // Whatever happened before the request that started the run is not the run.
    if (index === 0 || millis(entry) <= millis(from)) continue
    // Waiting for the person to type is not the skill being slow, so it leaves the active time.
    if (isPrompt(entry)) idle += millis(entry) - millis(stamped[index - 1])
  }

  const requests = collectRequests(stamped)

  // A sub-agent runs beside the session rather than after it, so its requests overlap the driver's
  // wall-clock and adding them to the phases would count the same seconds twice. The phases are the
  // main chain; what a sub-agent costs the driver is the tool wait, which lands in the overhead row.
  const mainChain = stamped.filter((entry) => at(entry, "isSidechain") !== true)
  const position = new Map(mainChain.map((entry, index) => [entry, index]))

  const phases: Record<Phase, number> = {
    thinking: 0,
    writing: 0,
    reading: 0,
    validating: 0,
    talking: 0,
    other: 0,
  }
  let measured = 0
  let slowest = 0

  for (const request of requests) {
    if (request.side !== "main") continue
    const index = position.get(request.entries[0])
    if (index === undefined || index === 0) continue
    const start = Math.max(millis(mainChain[index - 1]), millis(from))
    const elapsed = millis(request.entries[request.entries.length - 1]) - start
    if (elapsed <= 0) continue

    measured += elapsed
    slowest = Math.max(slowest, elapsed)

    // Wall-clock is output tokens over a rate this session holds within a few per cent on every
    // request long enough to swamp the time to first token, so a request's seconds divide between its
    // thinking and its work exactly as its tokens do. Measured seconds are what is split: the phases
    // then add up to what the clock says, with no modelled rate and no residual to explain.
    const output = request.tokens.output_tokens
    const thought = output === 0 ? 0 : (elapsed * request.tokens.thinking) / output
    phases.thinking += thought
    phases[request.phase] += elapsed - thought
  }

  const empty = emptyTotals()
  const tokens = { main: { ...empty }, sidechain: { ...empty } }
  const calls = { main: 0, sidechain: 0 }
  const models = new Set<string>()
  const tools = new Map<string, number>()

  for (const request of requests) {
    calls[request.side] += 1
    const model = stringAt(at(request.entries[0], "message"), "model")
    if (model) models.add(model)
    for (const key of Object.keys(empty)) tokens[request.side][key] += request.tokens[key]
  }

  for (const entry of entries) {
    for (const block of arrayAt(at(entry, "message"), "content")) {
      if (stringAt(block, "type") !== "tool_use") continue
      const label = toolLabel(block)
      tools.set(label, (tools.get(label) ?? 0) + 1)
    }
  }

  const span = millis(to) - millis(from)
  const active = span - idle
  return {
    run,
    lines: lines.length,
    session: { from: stringAt(stamped[0], "timestamp")!, to: stringAt(to, "timestamp")! },
    span,
    active,
    idle,
    prompts: entries.filter(isPrompt).length,
    calls,
    slowest,
    models: [...models],
    tokens,
    tools,
    phases,
    overhead: active - measured,
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
  const rate = metrics.active === 0 ? 0 : Math.round(main.output_tokens / (metrics.active / 1000))

  return [
    `# Metrics — ${metrics.run}`,
    "",
    "Generato da `make run-metrics RUN=<dir>` leggendo `TRANSCRIPT.jsonl`. Nessun numero scritto a",
    "mano: rigenerabile finché il transcript resta.",
    "",
    `**Transcript:** ${metrics.lines} righe · **Modello:** ${metrics.models.map((model) => `\`${model}\``).join(", ") || "—"} · **Sessione:** ${metrics.session.from} → ${metrics.session.to}`,
    "",
    "L'unità è la **richiesta al provider**, non la riga di transcript: una richiesta arriva come una",
    "entry per blocco di contenuto — thinking, testo, chiamata di tool — e ognuna ripete lo stesso",
    "`usage`. Il raggruppamento è per `requestId`.",
    "",
    "## Tempo",
    "",
    "| | |",
    "|---|---|",
    `| Dal primo prompt all'ultimo evento | ${duration(metrics.span)} |`,
    `| Di cui attesa dell'utente | ${duration(metrics.idle)} |`,
    `| **Tempo attivo** | **${duration(metrics.active)}** |`,
    `| Richiesta più lenta | ${duration(metrics.slowest)} |`,
    `| Media per richiesta | ${totalCalls === 0 ? "—" : duration(metrics.active / totalCalls)} |`,
    "",
    "## Dove va il tempo",
    "",
    "Il tempo di ogni richiesta è ripartito fra il pensiero e il lavoro che ha prodotto, in proporzione",
    "ai token emessi; la fase di una richiesta è la cosa più forte che ha fatto, e `Parola all'autore` è",
    "il turno che non ha chiamato nessun tool. Le righe sommano al tempo attivo. Le richieste di un",
    "sub-agent corrono accanto alla sessione e non entrano nelle fasi: quel che costano al driver è",
    "l'attesa del tool, che sta nell'ultima riga.",
    "",
    "| Fase | Tempo | Quota |",
    "|---|---|---|",
    ...PHASES.map(
      ([key, label]) =>
        `| ${label} | ${duration(metrics.phases[key])} | ${share(metrics.phases[key], metrics.active)} |`,
    ),
    `| Tool, sub-agent e I/O | ${duration(metrics.overhead)} | ${share(metrics.overhead, metrics.active)} |`,
    "",
    `Token di output al secondo, sul main: **${rate}**.`,
    "",
    "## Token",
    "",
    `| ${columns.join(" | ")} |`,
    `|${columns.map(() => "---").join("|")}|`,
    ...TOKEN_FIELDS.map(([key, label]) => tokenRow(label, key)),
    tokenRow("↳ di cui thinking", "thinking"),
    "",
    `Thinking sull'output: **${share(totalThinking, totalOutput)}**. Cache read per richiesta: **${totalCalls === 0 ? "—" : thousands(Math.round(totalRead / totalCalls))}**.`,
    "",
    "## Turni",
    "",
    "| | |",
    "|---|---|",
    `| Prompt dell'utente | ${metrics.prompts} |`,
    `| Richieste al provider | ${withSidechain ? `${totalCalls} (${metrics.calls.main} main, ${metrics.calls.sidechain} sub-agent)` : totalCalls} |`,
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
