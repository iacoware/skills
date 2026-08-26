import { readFileSync } from "node:fs"

const PLACEHOLDER = /\{\{([A-Z_]+)\}\}/g

export const render = (template: string, values: Record<string, string>) => {
  const rendered = template.replace(PLACEHOLDER, (whole, key: string) => values[key] ?? whole)
  const left = [...rendered.matchAll(PLACEHOLDER)].map((match) => match[0])
  if (left.length > 0) throw new Error(`placeholder senza valore: ${[...new Set(left)].join(", ")}`)
  return rendered
}

const main = () => {
  const [templatePath, ...pairs] = process.argv.slice(2)
  if (templatePath === undefined) {
    console.error("uso: render_prompt.ts <template> CHIAVE=valore ...")
    process.exit(1)
  }

  const values = Object.fromEntries(
    pairs.map((pair) => {
      const at = pair.indexOf("=")
      if (at < 1) throw new Error(`argomento non è CHIAVE=valore: ${pair}`)
      return [pair.slice(0, at), pair.slice(at + 1)]
    }),
  )

  process.stdout.write(render(readFileSync(templatePath, "utf8"), values))
}

if (process.argv[1]?.endsWith("render_prompt.ts")) main()
