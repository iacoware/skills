# `improve` — prompt for step 3 of the consensus cycle

Normative source for the `improve` phase. `PROMPTS.md` is a scratchpad and does not govern anything.
The cycle is `CONSENSUS-WORKFLOW.md` § *Il ciclo*; the detail rules are `workflow/CYCLE.md`; the
conformity gate that reads what this prompt produces is `workflow/CONFORMANCE.md`.

**Everything below the rule is the prompt. Everything above it is not sent.**

**Slots the runner fills:** `{{cycle}}` — the cycle number, e.g. `6`; `{{output}}` — the path the
document is written to.

**Payload, as an allowlist.** The runner composes it from these files and nothing else, under the
names the prompt uses:

| name in the payload | source |
|---|---|
| `SKILL.md` | `skills/plan-slices/SKILL.md`, at the commit the two candidates were generated with |
| `CANDIDATE-A.md`, `CANDIDATE-B.md` | the two generated plans, **renamed**; the real names carry the generator alias |
| `EVALUATION-BRIEF.md` | `recipe-app/EVALUATION-BRIEF.md` |
| `sources/` | `recipe-app/sources/` |
| `CLAUSE-INDEX.md` | the clause → row map, projected to `site · section · covering rows`, no claim text |
| `LEDGER-CLAIMS.md` | the active ledger rows, projected to `id · claim` |
| `assets/improvement-template.md` | verbatim |

Two of those need a reason. **`CLAUSE-INDEX.md`** exists because the contract asks each entry for a
clause site, its section title and its covering rows, and all three are decided by the map, not by
reading `SKILL.md`: without the index every entry that names a clause is discarded on a field the
model cannot get right. **`LEDGER-CLAIMS.md`** exists because `Merged claim` must replace the
covering rows, which cannot be written without reading them; without it `reach-change` is
unreachable and absorption — the only move that removes a prediction — silently stops happening.
The consequence is declared, not hidden: the agents that write these documents have seen the
ledger's claims, so `recidiva` measures pairings raised **despite** the claim being visible. That
makes a pairing stronger evidence and a zero weaker evidence than it would otherwise be.

---

You are improving `plan-slices`, a skill that instructs an agent to turn a set of sources into a
delivery plan cut into slices. Its full text is `SKILL.md`.

Two delivery plans were generated from the same sources, by two different agents, under that exact
text. They are `CANDIDATE-A.md` and `CANDIDATE-B.md`. **Neither of them is yours**: do not try to
work out who generated which, do not write as though one were yours, and do not name a model, an
agent or a harness anywhere in the document.

Produce **one** document, proposing changes to `SKILL.md` that come from the defects observed in the
two candidates — the union of them, not one candidate's list.

## What you may read

`SKILL.md`, `CANDIDATE-A.md`, `CANDIDATE-B.md`, `EVALUATION-BRIEF.md`, the files under `sources/`,
`CLAUSE-INDEX.md`, `LEDGER-CLAIMS.md`, `assets/improvement-template.md`.

Nothing else, in this session or in any session you delegate to. Do not search the repository for
context you were not given.

`EVALUATION-BRIEF.md` is the authority for this scenario: it declares which conflicts exist, which
alternatives are acceptable, and which uncertainties are material. The sources are opened only to
check a citation. A defect that consists of a candidate choosing an alternative the brief accepts is
not a defect.

## What counts as a defect

- **Observed, and locatable.** Every entry rests on what a candidate publishes, cited at the line,
  slice or field where it appears. Distinguish what you read from what you infer, and say which.
- **Manifested by at least one candidate.** A defect neither candidate shows is not a defect this
  cycle observed, however plausible.
- **Generalizable.** The rule you propose is a rule about delivery plans, not about recipe apps,
  cookbooks, embeddings or this scenario's stack. A rule that reads as a fix for this scenario is
  overfitting and will be rejected.
- **Not about the walking skeleton.** Defects concerning the walking skeleton slice — its content,
  its placement, whether it should exist — are outside the scope of this cycle. This is a
  restriction decided in advance, not an oversight. Raise none, and mention none.

Do not rank the two candidates and do not praise or condemn either overall. The subject is the
skill, not the plans; the plans are evidence.

## The form

`assets/improvement-template.md` is the contract. Fill exactly the fields it declares, in the order
it declares them, with the headings it uses. Do not add fields, do not drop fields, do not restate
the template's own explanatory notes in the document.

Four points where the contract needs something you have to look up rather than write:

- **`Clause` and `Covering rows`** come from `CLAUSE-INDEX.md`. Cite the site exactly as the index
  states it, name the section exactly as the index names it — the preamble's section is `Preamble`,
  which is not a heading in `SKILL.md` — and list that clause's covering rows exactly, or state
  `uncovered` when the index gives it none. Guessing either is a discarded entry. The `Section` of
  `Change to the skill` is one of the same section names, including for an entry that names no
  clause.
- **`Merged claim`**, required only for `reach-change`, replaces the covering rows you declared.
  Read them in `LEDGER-CLAIMS.md` and write the one claim that says everything they said. If the
  merged claim would be broader and vaguer than the rows it replaces, do not merge: propose a
  `reformulation` instead.
- **`Binary test`** is one claim, in the grammar of the ledger's rows — `No NOW slice …`, `Every
  LATER entry …`, `The plan …`, `If …`. It states what a plan does, not what it should do, it names
  what it quantifies over, and it can be decided on a generated plan without judgement words.
- **`Remedy`, and the rule that governs it.** When the entry names an existing clause, the default
  remedy is `reformulation`. Choosing `addition` next to a named clause requires the reformulation
  you actually attempted, written out, and what it fails to cover, stated over a generated plan.
  *«The clause is covered by a ledger row»* is not an admissible reason — covered clauses are the
  few already accused, which makes them the likeliest to need rewriting, not the exempt ones.

## One attempt

Each entry is validated on its own. An entry that fails the contract is **discarded and logged**;
the rest of the document stands, and the document is never regenerated. There is no second attempt
and no partial credit.

So: fewer entries that resolve beat more entries that do not. An entry you cannot ground in a cited
point of a candidate is an entry to drop, not to soften.

## Output

Write exactly one file, at `{{output}}`, titled `# Improvement report — cycle CON-{{cycle}}`.

Create, modify or delete nothing else — not the skill, not the candidates, not the sources, not the
brief, not any file under the repository. The document is the whole of the work.

Before finishing, check that: every entry has both evidence cells filled with a resolving reference
or with `not manifested` plus what that candidate does instead; every `Clause`, section title and
covering-row list matches `CLAUSE-INDEX.md`; no entry concerns the walking skeleton; no candidate is
described as yours; and no model, agent or harness is named.
