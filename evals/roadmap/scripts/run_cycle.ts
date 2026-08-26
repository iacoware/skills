import { spawn, spawnSync } from "node:child_process"
import { randomUUID } from "node:crypto"
import { copyFileSync, existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs"
import { homedir } from "node:os"
import { join } from "node:path"
import { createInterface } from "node:readline/promises"
import { parseArgs } from "node:util"
import { render } from "./render_prompt.ts"

const SCENARIO = "evals/roadmap/recipe-app"
const RESULTS = `${SCENARIO}/results`
const PROMPTS = `${SCENARIO}/prompts`
const FAMILY = "ROADMAP-CC"

const STEPS = {
  run: { prompt: "run.prompt.md", writes: ".roadmap/roadmap.md", label: "disegno della mappa" },
  review: { prompt: "review.prompt.md", writes: "REVIEW.md", label: "review del run" },
  improve: { prompt: "improve.prompt.md", writes: "IMPROVEMENTS.md", label: "proposte di miglioramento" },
} as const

type Step = keyof typeof STEPS

const fail = (message: string): never => {
  console.error(`\n${message}`)
  process.exit(1)
}

// La sessione legge `~/.claude/skills/roadmap`, che è una copia e non un link al repo: senza
// reinstallare, il ciclo giudicherebbe la versione precedente alla modifica sotto esame. È l'unico
// passo che il driver non può lasciare a chi lo lancia, perché dimenticarlo non si vede nel report.
const install = () => {
  console.log("── installo la skill sotto esame ──")
  const installed = spawnSync("make", ["add"], { stdio: "inherit" })
  if (installed.error !== undefined) fail(`make add non è partito: ${installed.error.message}`)
  if (installed.status !== 0) fail(`make add è uscito con ${installed.status}: il ciclo si ferma qui.`)

  const copy = join(homedir(), ".claude", "skills", "roadmap")
  const compared = spawnSync("diff", ["-r", "skills/roadmap", copy, "--exclude=.claude"], {
    stdio: "inherit",
  })
  if (compared.status !== 0)
    fail(
      `${copy} non corrisponde a skills/roadmap: l'installazione non ha preso la versione in\n` +
        `sviluppo, e il ciclo si ferma qui.`,
    )

  console.log(`skill installata: ${copy} corrisponde a skills/roadmap.`)
}

const nextRunDir = () => {
  const taken = readdirSync(RESULTS, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => new RegExp(`^${FAMILY}-(\\d+)$`).exec(entry.name)?.[1])
    .filter((found) => found !== undefined)
    .map(Number)
  return `${RESULTS}/${FAMILY}-${Math.max(0, ...taken) + 1}`
}

// The harness names the transcript after the session id, so choosing the id ourselves is what makes
// the file findable: no newest-file race, and no window in which a `/clear` opens a different one.
const transcriptOf = (sessionId: string) =>
  join(homedir(), ".claude", "projects", process.cwd().replaceAll("/", "-"), `${sessionId}.jsonl`)

const claudeArgs = (prompt: string, sessionId: string, model: string, effort: string) => [
  "-p",
  prompt,
  "--model",
  model,
  "--effort",
  effort,
  "--session-id",
  sessionId,
  "--permission-mode",
  "bypassPermissions",
  "--output-format",
  "stream-json",
  "--verbose",
]

const authorize = async (plan: string, assumed: boolean) => {
  console.log(plan)
  if (assumed) return console.log("Autorizzato da riga di comando (--yes).\n")

  const ask = createInterface({ input: process.stdin, output: process.stdout })
  const answer = await ask.question("Mando? [s/N] ")
  ask.close()
  if (!/^s(i|ì)?$/i.test(answer.trim())) fail("Annullato: nessuna richiesta mandata.")
  console.log()
}

const progressOf = (event: unknown) => {
  if (typeof event !== "object" || event === null) return undefined
  const record = event as Record<string, unknown>
  if (record.type === "result") return undefined

  const message = record.message as { content?: unknown } | undefined
  if (!Array.isArray(message?.content)) return undefined

  return message.content
    .map((block: Record<string, unknown>) =>
      block.type === "tool_use"
        ? `→ ${block.name}${block.name === "Skill" ? ` (${(block.input as Record<string, unknown>)?.skill})` : ""}`
        : block.type === "thinking"
          ? "· pensa"
          : block.type === "text"
            ? "· scrive"
            : undefined,
    )
    .filter((line) => line !== undefined)
    .join("\n")
}

const send = (prompt: string, sessionId: string, model: string, effort: string) =>
  new Promise<void>((resolve) => {
    const started = Date.now()
    const child = spawn("claude", claudeArgs(prompt, sessionId, model, effort), {
      stdio: ["ignore", "pipe", "inherit"],
    })

    let buffered = ""
    let last = ""
    child.stdout.setEncoding("utf8")
    child.stdout.on("data", (chunk: string) => {
      buffered += chunk
      const lines = buffered.split("\n")
      buffered = lines.pop() ?? ""
      for (const line of lines) {
        if (line.trim() === "") continue
        let progress: string | undefined
        try {
          progress = progressOf(JSON.parse(line))
        } catch {
          continue
        }
        // Thinking and prose arrive block by block; repeating the same line for each is noise.
        if (progress !== undefined && progress !== "" && progress !== last) console.log(progress)
        if (progress !== undefined && progress !== "") last = progress
      }
    })

    child.on("error", (error) => fail(`claude non è partito: ${error.message}`))
    child.on("close", (code) => {
      const elapsed = Math.round((Date.now() - started) / 1000)
      console.log(`\nSessione chiusa dopo ${Math.floor(elapsed / 60)}m ${elapsed % 60}s (exit ${code}).`)
      if (code !== 0) fail(`La sessione è uscita con ${code}: il ciclo si ferma qui.`)
      resolve()
    })
  })

const capture = (runDir: string, sessionId: string) => {
  const source = transcriptOf(sessionId)
  if (!existsSync(source)) fail(`Transcript non trovato: ${source}\nIl run è girato ma non è catturato.`)

  copyFileSync(source, `${runDir}/TRANSCRIPT.jsonl`)
  console.log(`transcript -> ${runDir}/TRANSCRIPT.jsonl`)
}

// A prose mention of `/roadmap` is not proof the skill loaded, and a session that answered out of its
// own head tested the model instead of the skill. Reviewing that run would spend a call on nothing.
const invokedTheSkill = (runDir: string) =>
  readFileSync(`${runDir}/TRANSCRIPT.jsonl`, "utf8")
    .split("\n")
    .filter((line) => line.trim() !== "")
    .some((line) => {
      try {
        const content = (JSON.parse(line) as { message?: { content?: unknown } }).message?.content
        return (
          Array.isArray(content) &&
          content.some(
            (block: Record<string, unknown>) =>
              block.type === "tool_use" &&
              block.name === "Skill" &&
              String((block.input as Record<string, unknown>)?.skill).includes("roadmap"),
          )
        )
      } catch {
        return false
      }
    })

const promptRecord = (runDir: string, sessionId: string, model: string, effort: string, prompt: string) => `# Prompt — ${runDir.split("/").pop()}

Run headless: nessuna persona ha guidato la sessione in interattivo, ed è la departure che
[\`../README.md\`](../README.md) obbliga a registrare qui. Il testo è
[\`../../prompts/run.prompt.md\`](../../prompts/run.prompt.md) con \`{{RUN_DIR}}\` risolto, e non
differisce in altro dalla card 0 di [\`../../SCENARIOS.md\`](../../SCENARIOS.md).

Quel che questa forma non mette alla prova è il path di invocazione interattivo. Nello scenario 0
non c'è niente da confermare e niente da rispondere — il prompt risponde da sé all'unica domanda
dovuta, quella su che cosa è stato consegnato — quindi la perdita è piccola, ma non è zero.

| | |
|---|---|
| Harness | \`claude -p\` |
| Modello | \`${model}\` |
| Effort | \`${effort}\` |
| Session id | \`${sessionId}\` |

Il prompt, alla lettera:

~~~
${prompt}
~~~
`

const runStep = async (step: Step, runDir: string, model: string, effort: string, yes: boolean) => {
  const sessionId = randomUUID()
  const prompt = render(readFileSync(`${PROMPTS}/${STEPS[step].prompt}`, "utf8"), { RUN_DIR: runDir })

  await authorize(
    [
      `\n── ${STEPS[step].label} ──`,
      `run       ${runDir}`,
      `modello   ${model}    effort ${effort}`,
      `sessione  ${sessionId}`,
      `scrive    ${runDir}/${STEPS[step].writes}`,
      "",
      "Una sessione, a contesto vuoto. Quante richieste al provider faccia non è noto in anticipo:",
      "ROADMAP-CC-3 ne ha fatte 16. `evals/AGENTS.md` vuole questa autorizzazione esplicita.",
      "",
    ].join("\n"),
    yes,
  )

  if (step === "run") {
    mkdirSync(runDir, { recursive: true })
    writeFileSync(`${runDir}/PROMPT.md`, promptRecord(runDir, sessionId, model, effort, prompt))
  }

  await send(prompt, sessionId, model, effort)

  if (step === "run") {
    capture(runDir, sessionId)
    spawn("node", ["evals/roadmap/scripts/run_metrics.ts", runDir], { stdio: "inherit" })
  }

  if (!existsSync(`${runDir}/${STEPS[step].writes}`))
    fail(`La sessione non ha scritto ${runDir}/${STEPS[step].writes}: il ciclo si ferma qui.`)

  if (step === "run" && !invokedTheSkill(runDir))
    fail(
      `Nel transcript non c'è nessuna chiamata a Skill(roadmap): questo run ha messo alla prova il\n` +
        `modello, non la skill. Il ciclo si ferma qui e la review non parte.`,
    )

  console.log(`${runDir}/${STEPS[step].writes} scritto.`)
}

const main = async () => {
  const { values } = parseArgs({
    options: {
      step: { type: "string", default: "cycle" },
      run: { type: "string" },
      model: { type: "string", default: "opus" },
      effort: { type: "string", default: "high" },
      "review-model": { type: "string" },
      "review-effort": { type: "string" },
      yes: { type: "boolean", default: false },
    },
  })

  if (!existsSync(SCENARIO)) fail(`Da lanciare dalla radice del repo: ${SCENARIO} non esiste da qui.`)

  install()

  const model = values.model as string
  const effort = values.effort as string
  const reviewModel = (values["review-model"] as string | undefined) ?? model
  const reviewEffort = (values["review-effort"] as string | undefined) ?? effort
  const yes = values.yes as boolean

  const needsRun = (step: string) => {
    const given = values.run as string | undefined
    if (given === undefined) fail(`--run è obbligatorio per ${step}.`)
    if (!existsSync(given!)) fail(`${given}: non è una directory di run.`)
    return given!
  }

  switch (values.step) {
    case "run":
      return runStep("run", nextRunDir(), model, effort, yes)
    case "review":
      return runStep("review", needsRun("review"), reviewModel, reviewEffort, yes)
    case "improve":
      return runStep("improve", needsRun("improve"), reviewModel, reviewEffort, yes)
    case "cycle": {
      const runDir = nextRunDir()
      await runStep("run", runDir, model, effort, yes)
      await runStep("review", runDir, reviewModel, reviewEffort, yes)
      console.log(`\nCiclo finito su ${runDir}. improve resta da lanciare a mano.`)
      return
    }
    default:
      return fail(`--step sconosciuto: ${values.step}. Sono run, review, improve, cycle.`)
  }
}

await main()
