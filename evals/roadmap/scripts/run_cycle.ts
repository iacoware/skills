import { spawn, spawnSync } from "node:child_process"
import { randomUUID } from "node:crypto"
import { copyFileSync, existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs"
import { homedir } from "node:os"
import { join } from "node:path"
import { createInterface } from "node:readline/promises"
import { parseArgs } from "node:util"
import { render } from "./render_prompt.ts"
import { anchorOf, normalizeRunDir, prepareNoise, reportNoise, satelliteDirsOf } from "./noise_report.ts"

const SCENARIO = "evals/roadmap/recipe-app"
const RESULTS = `${SCENARIO}/results`
const PROMPTS = `${SCENARIO}/prompts`
const FAMILY = "ROADMAP-CC"

const STEPS = {
  run: { prompt: "run.prompt.md", writes: ".roadmap/roadmap.md", label: "disegno della mappa" },
  review: { prompt: "review.prompt.md", writes: "REVIEW.md", label: "review del run" },
  improve: { prompt: "improve.prompt.md", writes: "IMPROVEMENTS.md", label: "proposte di miglioramento" },
  noise: { prompt: "noise.prompt.md", writes: "noise/alignment.json", label: "allineamento del residuo" },
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

type Planned = {
  step: Step
  runDir: string
  model: string
  effort: string
  sessionId: string
  satelliteOf?: string
  tag?: string
}

const plan = (step: Step, runDir: string, model: string, effort: string): Planned => ({
  step,
  runDir,
  model,
  effort,
  sessionId: randomUUID(),
})

// Chi lancia autorizza una volta sola, davanti all'elenco completo dei passi: tornare a chiedere a
// metà ciclo non aggiungerebbe una decisione, perché la decisione su quelle sessioni è già presa qui.
const authorize = async (planned: Planned[], assumed: boolean) => {
  const count = planned.length === 1 ? "1 sessione" : `${planned.length} sessioni`
  console.log(`\n── autorizzazione: ${count} ──`)
  for (const { step, runDir, model, effort, sessionId } of planned)
    console.log(
      [
        "",
        STEPS[step].label,
        `run       ${runDir}`,
        `modello   ${model}    effort ${effort}`,
        `sessione  ${sessionId}`,
        `scrive    ${runDir}/${STEPS[step].writes}`,
      ].join("\n"),
    )

  console.log(
    [
      "",
      "Una sessione per passo, ognuna a contesto vuoto. Quante richieste al provider faccia non è noto",
      "in anticipo: ROADMAP-CC-3 ne ha fatte 16. `evals/AGENTS.md` vuole questa autorizzazione",
      "esplicita, ed è l'unica che il ciclo chiede: i passi seguenti partono senza chiedere ancora.",
      "",
    ].join("\n"),
  )

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

const send = (prompt: string, sessionId: string, model: string, effort: string, tag = "") =>
  new Promise<void>((resolve) => {
    const started = Date.now()
    const prefix = tag === "" ? "" : `[${tag}] `
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
        if (progress !== undefined && progress !== "" && progress !== last)
          console.log(prefix === "" ? progress : progress.replace(/^/gm, prefix))
        if (progress !== undefined && progress !== "") last = progress
      }
    })

    child.on("error", (error) => fail(`claude non è partito: ${error.message}`))
    child.on("close", (code) => {
      const elapsed = Math.round((Date.now() - started) / 1000)
      console.log(`\n${prefix}Sessione chiusa dopo ${Math.floor(elapsed / 60)}m ${elapsed % 60}s (exit ${code}).`)
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

const git = (...args: string[]) => spawnSync("git", args, { encoding: "utf8" }).stdout.trim()

// L'ancoraggio del run alla skill che ha girato. Senza, il ciclo di miglioramento deve dedurlo dalla
// data del commit che aggiunge il run, e un run committato dopo una modifica a `skills/roadmap`
// sposta il confine: un fix mai messo alla prova si legge come un fix che non ha preso.
const skillVersion = () => {
  const uncommitted = git("status", "--porcelain", "--", "skills/roadmap")
    .split("\n")
    .map((line) => line.slice(3).trim())
    .filter((path) => path !== "")

  return {
    commit: git("log", "-1", "--format=%h %s"),
    tree: git("rev-parse", "--short", "HEAD:skills/roadmap"),
    uncommitted,
  }
}

const skillRow = ({ tree, uncommitted }: ReturnType<typeof skillVersion>) =>
  uncommitted.length === 0
    ? `tree \`${tree}\`, uguale a HEAD`
    : `tree \`${tree}\` a HEAD, **più modifiche non committate**: ${uncommitted.map((path) => `\`${path}\``).join(", ")}`

type Recorded = {
  runDir: string
  sessionId: string
  model: string
  effort: string
  prompt: string
  skill: ReturnType<typeof skillVersion>
  satelliteOf?: string
}

const satelliteParagraph = (mainDir: string) => `
Satellite di \`${mainDir.split("/").pop()}\` per il prezzamento del rumore
([\`design/roadmap/EVAL-NOISE.md\`](../../../../../design/roadmap/EVAL-NOISE.md)): stesso commit,
stesso prompt, stesso modello ed effort del principale, lanciato da \`make eval-noise\`. È un run di
prima classe minus review, generation-only: non riceve mai \`REVIEW.md\` né \`IMPROVEMENTS.md\` — e
i suoi confronti stanno nel \`NOISE.md\` del principale.
`

const promptRecord = ({ runDir, sessionId, model, effort, prompt, skill, satelliteOf }: Recorded) => `# Prompt — ${runDir.split("/").pop()}

Run headless: nessuna persona ha guidato la sessione in interattivo, ed è la departure che
[\`../README.md\`](../README.md) obbliga a registrare qui. Il testo è
[\`../../prompts/run.prompt.md\`](../../prompts/run.prompt.md) con \`{{RUN_DIR}}\` risolto, e non
differisce in altro dalla card 0 di [\`../../SCENARIOS.md\`](../../SCENARIOS.md).
${satelliteOf === undefined ? "" : satelliteParagraph(satelliteOf)}

Quel che questa forma non mette alla prova è il path di invocazione interattivo. Nello scenario 0
non c'è niente da confermare e niente da rispondere — il prompt risponde da sé all'unica domanda
dovuta, quella su che cosa è stato consegnato — quindi la perdita è piccola, ma non è zero.

| | |
|---|---|
| Harness | \`claude -p\` |
| Modello | \`${model}\` |
| Effort | \`${effort}\` |
| Session id | \`${sessionId}\` |
| Commit | \`${skill.commit}\` |
| \`skills/roadmap\` | ${skillRow(skill)} |

Le ultime due righe sono l'ancoraggio, e la skill che ha girato è quella che dichiarano: la sessione
legge la copia installata, e il ciclo si ferma prima di inviare se quella copia e l'albero di lavoro
divergono. Il commit è il punto della storia — è da lì che il ciclo di miglioramento delimita
l'intervallo dei fix che questo run ha messo alla prova, \`git log <commit del run precedente>..<questo>
-- skills/roadmap\`, e dentro l'intervallo si leggono tutti i commit. Il tree è l'identità del
contenuto: due run che ne dichiarano uno uguale hanno girato la stessa skill, per quanti commit ci
siano stati in mezzo.

Il prompt, alla lettera:

~~~
${prompt}
~~~
`

const runStep = async ({ step, runDir, model, effort, sessionId, satelliteOf, tag }: Planned) => {
  const prompt = render(readFileSync(`${PROMPTS}/${STEPS[step].prompt}`, "utf8"), { RUN_DIR: runDir })

  console.log(`\n── ${STEPS[step].label}${tag === undefined ? "" : ` [${tag}]`} ──`)

  if (step === "run") {
    mkdirSync(runDir, { recursive: true })
    writeFileSync(
      `${runDir}/PROMPT.md`,
      promptRecord({ runDir, sessionId, model, effort, prompt, skill: skillVersion(), satelliteOf }),
    )
  }

  // Terza guardia, della stessa specie delle altre due: improve legge il report di questo run prima
  // di ogni altro, e senza quello spenderebbe una chiamata su un run che nessuno ha giudicato.
  if (step === "improve" && !existsSync(`${runDir}/REVIEW.md`))
    fail(`${runDir}/REVIEW.md non c'è: improve parte dal report di questo run, e il ciclo si ferma qui.`)

  await send(prompt, sessionId, model, effort, tag)

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

// Il prezzamento del rumore (design/roadmap/EVAL-NOISE.md): genera i satelliti mancanti del run
// principale — gemelli: stesso commit, stesso prompt, modello ed effort presi dal suo PROMPT.md e
// non dai flag — poi estrazione e match meccanico, la sessione di allineamento sul residuo, e
// l'aritmetica che scrive NOISE.md.
const runNoise = async (mainDir: string, model: string, effort: string, yes: boolean) => {
  if (!existsSync(`${mainDir}/.roadmap/roadmap.md`))
    fail(`${mainDir}/.roadmap/roadmap.md non c'è: il principale non ha una mappa da confrontare.`)
  if (!existsSync(`${mainDir}/PROMPT.md`))
    fail(`${mainDir}/PROMPT.md non c'è: senza ancoraggio i satelliti non possono dirsi gemelli.`)

  const anchor = anchorOf(readFileSync(`${mainDir}/PROMPT.md`, "utf8"))
  if (anchor.tree === undefined || anchor.model === undefined || anchor.effort === undefined)
    fail(`${mainDir}/PROMPT.md: ancoraggio illeggibile (tree, modello o effort mancano dalla tabella).`)

  // La guardia sulla versione: satelliti su una skill diversa misurerebbero versione + rumore
  // insieme, che è il vizio che questo metro elimina.
  const current = skillVersion()
  if (anchor.dirty)
    fail(`${mainDir}/PROMPT.md dichiara modifiche non committate: il tree non identifica la skill che ha girato.`)
  if (current.uncommitted.length > 0)
    fail(`skills/roadmap ha modifiche non committate: il tree corrente non identifica la skill che girerebbe.`)
  if (current.tree !== anchor.tree)
    fail(
      `skills/roadmap è al tree \`${current.tree}\`, il principale ha girato su \`${anchor.tree}\`:\n` +
        `satelliti su una skill diversa misurerebbero versione + rumore insieme. Nessuna sessione parte.`,
    )

  const satellites = satelliteDirsOf(mainDir)
    .filter((dir) => !existsSync(`${dir}/.roadmap/roadmap.md`))
    .map((dir) => ({
      ...plan("run", dir, anchor.model!, anchor.effort!),
      satelliteOf: mainDir,
      tag: dir.slice(-1),
    }))
  const alignment = plan("noise", mainDir, model, effort)

  console.log(
    "\nI satelliti già completi non si rigenerano; la sessione di allineamento parte solo se il match" +
      "\nmeccanico lascia un residuo.",
  )
  await authorize([...satellites, alignment], yes)

  await Promise.all(satellites.map(runStep))

  const residual = prepareNoise(mainDir)
  console.log(`\nresiduo dopo il match meccanico: ${residual} record -> ${mainDir}/noise/residual.json`)
  if (residual === 0) {
    console.log("Residuo vuoto: la sessione di allineamento non parte.")
    writeFileSync(`${mainDir}/noise/alignment.json`, `${JSON.stringify({ pairs: [] }, null, 2)}\n`)
  } else {
    await runStep(alignment)
  }

  reportNoise(mainDir)
  console.log(`noise -> ${mainDir}/NOISE.md`)
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

  if (values.step === "noise")
    return runNoise(normalizeRunDir(needsRun("noise")), reviewModel, reviewEffort, yes)

  const planned = ((): Planned[] => {
    switch (values.step) {
      case "run":
        return [plan("run", nextRunDir(), model, effort)]
      case "review":
        return [plan("review", needsRun("review"), reviewModel, reviewEffort)]
      case "improve":
        return [plan("improve", needsRun("improve"), reviewModel, reviewEffort)]
      case "cycle": {
        const runDir = nextRunDir()
        return [
          plan("run", runDir, model, effort),
          plan("review", runDir, reviewModel, reviewEffort),
          plan("improve", runDir, reviewModel, reviewEffort),
        ]
      }
      default:
        return fail(`--step sconosciuto: ${values.step}. Sono run, review, improve, noise, cycle.`)
    }
  })()

  await authorize(planned, yes)

  for (const step of planned) await runStep(step)

  if (values.step === "cycle")
    console.log(
      `\nCiclo finito su ${planned[0]!.runDir}: mappa, review e proposte.` +
        `\nRestano a mano le due letture che il ciclo non fa: improve-perf.prompt.md sul costo del run,` +
        `\ne i tre interventi da leggere prima di toccare skills/roadmap.`,
    )
}

await main()
