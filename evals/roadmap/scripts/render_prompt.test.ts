import { test } from "node:test"
import assert from "node:assert/strict"
import { readFileSync, readdirSync } from "node:fs"
import { join } from "node:path"
import { render } from "./render_prompt.ts"

const PROMPTS = join(import.meta.dirname, "..", "recipe-app", "prompts")

test("resolves every occurrence of a placeholder", () => {
  const rendered = render("{{RUN_DIR}}/.roadmap and {{RUN_DIR}}/REVIEW.md", { RUN_DIR: "results/X" })

  assert.equal(rendered, "results/X/.roadmap and results/X/REVIEW.md")
})

test("refuses to render a prompt whose placeholder has no value", () => {
  assert.throws(() => render("write to {{RUN_DIR}}", {}), /RUN_DIR/)
})

test("names every unresolved placeholder once, not once per occurrence", () => {
  assert.throws(() => render("{{A}} {{A}} {{B}}", {}), /\{\{A\}\}, \{\{B\}\}/)
})

test("leaves text that is not a placeholder alone", () => {
  assert.equal(render("{ {RUN_DIR} } and {{lowercase}}", {}), "{ {RUN_DIR} } and {{lowercase}}")
})

// The cycle passes exactly one value, so a prompt naming anything else renders nowhere and the
// failure would only show at send time, with a session already authorized.
test("each shipped prompt is rendered by RUN_DIR alone", () => {
  const prompts = readdirSync(PROMPTS).filter((name) => name.endsWith(".prompt.md"))

  assert.ok(prompts.length > 0)
  for (const name of prompts) {
    const template = readFileSync(join(PROMPTS, name), "utf8")

    assert.doesNotThrow(() => render(template, { RUN_DIR: "results/X" }), name)
  }
})

test("the drawing prompt still carries the read restriction it is sent for", () => {
  const rendered = render(readFileSync(join(PROMPTS, "run.prompt.md"), "utf8"), {
    RUN_DIR: "evals/roadmap/recipe-app/results/ROADMAP-CC-9",
  })

  assert.match(rendered, /\/roadmap/)
  assert.match(rendered, /evals\/roadmap\/recipe-app\/results\/ROADMAP-CC-9\/ come project root/)
  assert.match(rendered, /Vincoli di lettura/)
  assert.match(rendered, /reference-roadmap, fixtures, EVALUATION-\*/)
})

// The three router cards send the same frame around one different sentence. Three files repeating
// that frame is how the drawing prompt came to exist in two versions, so the repetition is asserted
// rather than trusted.
const OPENS = "sources/. "
const CLOSES = " Read nothing else"

const frameOf = (text: string) => {
  const opens = text.indexOf(OPENS) + OPENS.length
  const closes = text.indexOf(CLOSES)

  assert.ok(opens > OPENS.length - 1 && closes > opens, "prompt does not carry the router frame")
  return { before: text.slice(0, opens), after: text.slice(closes), sentence: text.slice(opens, closes) }
}

test("the router prompts differ only in the sentence the router reads", () => {
  const frames = [1, 2, 3].map((card) =>
    frameOf(readFileSync(join(PROMPTS, `router-${card}.prompt.md`), "utf8")),
  )

  for (const frame of frames.slice(1)) {
    assert.equal(frame.before, frames[0].before)
    assert.equal(frame.after, frames[0].after)
  }
  assert.equal(new Set(frames.map((frame) => frame.sentence)).size, 3)
})
