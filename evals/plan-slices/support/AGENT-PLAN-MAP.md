# Agent → plan map

Which generator produced each artifact under `recipe-app/results/`, and — from CON-6 on — under which
alias each artifact enters a payload. Produced for Fase 1b-ii.

**Excluded from every payload**, like the rest of `support/`. The exclusion is by construction: a
payload is composed from an explicit allowlist and this file is not on it. The prohibition written
into the prompts covers manual execution only.

## Why the file exists

Two consumers, and they want different things from it.

- **The ledger.** `REGRESSION-LEDGER.md` § *`Measured on`* has a `gen` slot — *model and effort per
  side* — and its cells are filled from here. Without it a verdict does not say what produced the
  plan it was measured on.
- **Blindness.** From CON-6 `improve` and `review` receive the artifacts renamed. This is the only
  place that maps the alias back to the side, and it is why it must never travel with them.

## What a generator is here

Four facts, and they are not interchangeable:

- **harness** — the CLI and session the generation prompt was run in. `CC` and `CX` name **this and
  nothing else**;
- **mode** — interactive session or headless call. It is a tool boundary in its own right: Fase 6
  crosses it when `PHASE=generate` replaces the interactive sessions;
- **model**;
- **effort**.

The `Measured on` grammar splits them: the harness rides in the `plans` slot as `CC`+`CX`, model and
effort in `gen`. A cell reading `CC`+`CX` therefore says nothing about the model, which is the
confusion this file was created to end.

## Aliases, and why there are two assignments per cycle

Two independent assignments, decided when the payload is composed and written here **before** the
call:

| Assignment | Artifacts | Used by |
|---|---|---|
| `CANDIDATE-A` / `CANDIDATE-B` | the two generated plans | `improve`, `verdict` |
| `REPORT-A` / `REPORT-B` | the two conforming `IMPROVEMENT`s | `review`, `recidiva` |

**The two must not coincide.** If the side holding `CANDIDATE-A` also holds `REPORT-A`, then anyone
who breaks blindness in one phase breaks it in the other for free, and the two phases stop failing
independently. Blindness is nominal anyway — a model can recognise its own prose — so the point is
not to make it airtight but to keep one leak from being two.

The assignment is a decision, never a derivation: it is not read off the file name, not fixed by
alphabetical order of the alias, and not carried over from the previous cycle.

**CON-1…CON-5 have no aliases.** Those payloads carried the real file names, and each model knew
which plan and which report were its own — the state of affairs `workflow/CYCLE.md` § *Cecità e
simmetria* records as the CON-5 → CON-6 boundary.

## The map

`Attribution` is how the harness was decided. The fourteen CON-1…CON-5 rows are `reconstructed`; the
evidence is below, and their model and effort are `unrecorded`, once, for the reason stated in its
own section. The CON-6 rows are `declared`: written before the calls, which is the whole point of the
column — with one cell corrected afterwards, `effort corrected`, and the correction is described
below rather than hidden in the cell. Writing a cell before the call makes it checkable, not true.

| Cycle | Artifact | Role | Harness | Mode | Model · effort | Alias | Attribution |
|---|---|---|---|---|---|---|---|
| CON-1 | `PLAN-CC-CON-1.md` | candidate | `CC` — Claude Code CLI | interactive session | unrecorded | — | reconstructed |
| CON-1 | `PLAN-CX-CON-1.md` | candidate | `CX` — Codex CLI | interactive session | unrecorded | — | reconstructed |
| CON-2 | `PLAN-CC-CON-2.md` | candidate | `CC` — Claude Code CLI | interactive session | unrecorded | — | reconstructed |
| CON-2 | `PLAN-CX-CON-2.md` | candidate | `CX` — Codex CLI | interactive session | unrecorded | — | reconstructed |
| CON-3 | `PLAN-CC-CON-3.md` | candidate | `CC` — Claude Code CLI | interactive session | unrecorded | — | reconstructed |
| CON-3 | `PLAN-CX-CON-3.md` | candidate | `CX` — Codex CLI | interactive session | unrecorded | — | reconstructed |
| CON-4 | `PLAN-CC-CON-4.md` | candidate | `CC` — Claude Code CLI | interactive session | unrecorded | — | reconstructed |
| CON-4 | `PLAN-CX-CON-4.md` | candidate | `CX` — Codex CLI | interactive session | unrecorded | — | reconstructed |
| CON-4 | `PLAN-CC-CON-4.IMPROVEMENT.md` | `improve` output | `CC` — Claude Code CLI | interactive session | unrecorded | — | reconstructed |
| CON-4 | `PLAN-CX-CON-4.IMPROVEMENT.md` | `improve` output | `CX` — Codex CLI | interactive session | unrecorded | — | reconstructed |
| CON-4 | `PLAN-CC-CON-4.REVIEW.md` | `review` output | `CC` — Claude Code CLI | interactive session | unrecorded | — | reconstructed |
| CON-4 | `PLAN-CX-CON-4.REVIEW.md` | `review` output | `CX` — Codex CLI | interactive session | unrecorded | — | reconstructed |
| CON-5 | `PLAN-CC-CON-5.md` | candidate | `CC` — Claude Code CLI | interactive session | unrecorded | — | reconstructed |
| CON-5 | `PLAN-CX-CON-5.md` | candidate | `CX` — Codex CLI | interactive session | unrecorded | — | reconstructed |
| CON-6 | `PLAN-CC-CON-6.md` | candidate | `CC` — Claude Code CLI | interactive session | `claude-opus-5` · `medium` | `CANDIDATE-B` | declared · effort corrected |
| CON-6 | `PLAN-CX-CON-6.md` | candidate | `CX` — Codex CLI | interactive session | `gpt-5.6-sol` · `medium` | `CANDIDATE-A` | declared · effort corrected |
| CON-6 | `PLAN-CC-CON-6.IMPROVEMENT.md` | `improve` output | `CC` — Claude Code CLI | interactive session | `claude-opus-5` · `high` | `REPORT-A` | declared |
| CON-6 | `PLAN-CX-CON-6.IMPROVEMENT.md` | `improve` output | `CX` — Codex CLI | interactive session | `gpt-5.6-sol` · `high` | `REPORT-B` | declared |
| CON-6 | `PLAN-CC-CON-6.REVIEW.md` | `review` output | `CC` — Claude Code CLI | interactive session | `claude-opus-5` · `high` | — | declared |
| CON-6 | `PLAN-CX-CON-6.REVIEW.md` | `review` output | `CX` — Codex CLI | interactive session | `gpt-5.6-sol` · `high` | — | declared |
| CON-6 | `PLAN-CC-CON-6.VERDICTS.md` | `verdict` output | `CC` — Claude Code CLI | interactive session | `claude-opus-5` · `high` | — | declared |
| CON-6 | `PLAN-CX-CON-6.VERDICTS.md` | `verdict` output | `CX` — Codex CLI | interactive session | `gpt-5.6-sol` · `high` | — | declared |

CON-5 is a partial cycle: it stopped at generation, so it has no `IMPROVEMENT` and no `REVIEW`, and
its verdicts come from offline human reading.

### CON-6: decided at S3, before the five calls

- **Three payload directories, disjoint, one per phase.**
  `recipe-app/payloads/CON-6/review/` holds `REPORT-A.md` and `REPORT-B.md` and nothing else;
  `verdict/` holds `CANDIDATE-A.md`, `CANDIDATE-B.md`, `EVALUATION-BRIEF.md`, `sources/` and
  `LEDGER-ROWS.md`; `recidiva/` holds the two reports and `ROWS.md`. Each is exactly the allowlist
  of its prompt, as `improve/` was at S2. The candidates, the brief and the four sources in
  `verdict/` are byte-identical to the copies `improve/` carried, which are themselves identical to
  the repository originals: checked with `diff`, not assumed.
- **Both alias assignments stand from S1 and are not re-decided.** `CANDIDATE-A` is `CX`'s plan,
  `CANDIDATE-B` is `CC`'s; `REPORT-A` is `CC`'s `IMPROVEMENT`, `REPORT-B` is `CX`'s. Both
  `IMPROVEMENT`s came out of S2b fully conforming — 4 of 4 and 7 of 7, revalidated unchanged — so
  the two reports enter `review` and `recidiva` **whole**: no entry was stripped, and the ids the
  two phases pair on are the reports' own numbering, `A#1`…`A#4` and `B#1`…`B#7`.
- **The two projections carry claims and nothing else.** `LEDGER-ROWS.md` is `id · claim · watch
  for`, `ROWS.md` is `id · claim`; all 17 claims were extracted from `REGRESSION-LEDGER.md` and
  compared cell by cell against both files — verbatim on every row. No state, no counter, no origin,
  no provenance travels with them. **All 17 rows are active and none is dormant**, so the 1-cycle-in-3
  rule does not bite here and both files carry the same 17 ids.
- **What was dropped from the `Watch for` cells, and why.** Four rows carry a note; the projection is
  not a copy. `R-011` enters whole. `R-010` enters as the instruction only — *«a plan that defers
  everything to a pending decision»* — without the sentence that names a harness and retells the
  row's own history: a payload that names `CX` breaks the blindness of a phase whose candidates are
  aliased. `R-016` enters without its pointer to `support/CLAUSE-ROW-MAP.md`, which is excluded from
  every payload by construction; what remains is where the exception is decided, and the brief is in
  the payload. `R-015` does not enter at all: its note is about the row's provenance and the Fase 4
  decision it forces, it names a harness, and it is not an instruction about a generated plan. This
  is an editorial decision on what a projection is, taken before the calls and recorded because it
  changes what two of the five executions read.
- **Output directories are separate per phase and per side, and empty.**
  `out-review/CC`, `out-review/CX`, `out-verdict/CC`, `out-verdict/CX`, `out-recidiva`. The S2b
  lesson applied forward: the two `IMPROVEMENT`s stay in `out/` and no execution of this session
  writes there, so no run has another run's artifact — or the previous phase's, under its real
  name — one `ls` away. As at S2, each rendered prompt names its own side in its output path: the
  side already knows which harness it is, and the path says nothing about which report or which
  candidate is whose.
- **`recidiva` has no row in the table above and one is not added.** It is a single call with no
  side; the model is fixed at `claude-opus-5` and declared in `REGRESSION-LEDGER.md` § *`Measured
  on`*. The facts that belong here are the two the ledger cell does not carry: it runs on `CC` —
  Claude Code CLI, interactive session — at effort `high`.
- **Effort is `high` on all five calls**, verified in session before sending, per side
  `claude-opus-5` for `CC` and `gpt-5.6-sol` for `CX`. The generation stays `medium` and is what the
  `gen` slot of every cell this cycle writes must say.
- **One prompt defect was corrected before the calls, at unknown result.**
  `prompts/recidiva.prompt.md` forbade any count anywhere while its own output structure requires
  three — the two report sizes and the number of rows considered. The prohibition now names what it
  is for: the pairings. Unlike the two corrections of S2, this one was decided without knowing what
  either side would produce.

### CON-6: decided at S2, before the two `improve` calls

- **The payload is a directory, not a list of repository paths.**
  `recipe-app/payloads/CON-6/improve/` holds exactly the allowlist of `prompts/improve.prompt.md`
  and nothing else: the two candidates under their aliases, `SKILL.md` at `28b5460`, the brief, the
  sources, the template, and the two projections. For a manual execution the allowlist is written,
  not imposed, and a directory is the closest a written one gets to being imposed.
- **`CLAUSE-INDEX.md` and `LEDGER-CLAIMS.md` are projections, and both were checked before the
  calls.** Every one of the 200 site cells was fed to `validate_improvement.py` as an entry would
  state it: all 200 are accepted with the rows the index prints. The index was also compared, site
  by site, against the Markdown of `support/CLAUSE-ROW-MAP.md` rather than against the `.tsv` both
  it and the gate derive from. Two defects found by that check are recorded in
  `../CONSENSUS-WORKFLOW-PLAN.md` § Fase 2, S2; both were in the tooling, neither in the map.
- **Effort is `high` on both `improve` calls**, and it is the cell S1 got wrong by not checking. It
  is verified in the session, before sending, not declared and assumed. Confirmed in session for the
  first attempt, and it is the configuration the repeat runs at: a repeated S2 repeats at the same
  configuration, so the two rows above hold for both attempts and are not re-declared.
- **The first attempt was discarded, and the fault was the index, not either model.** The gate read
  `REPORT-A` 5 conforming of 5 and `REPORT-B` 0 of 3, all three discards on the same field with the
  same message. `CLAUSE-INDEX.md` printed the numbered headings as `## § 1 …`, while the template
  asks for `§ ` + the title as the marker of that field, so the conforming form was a doubled `§`.
  One side wrote it, the other absorbed the marker into the title and was discarded whole. The three
  `REPORT-B` entries name site, section and quotation correctly; restoring the separator alone makes
  all three conform. The index now prints those headings without the `§` and states the rule for the
  field; `_comparable` strips `§` either way, so both forms are accepted and no cell of the map or of
  the `.tsv` changed. The discarded outputs are kept under
  `../recipe-app/payloads/CON-6/discarded/attempt-1/` — outside `out/`, the one directory the two
  executions write to, so that the repeat does not run with the previous attempt one `ls` away — as
  the evidence for that reading. This is
  the third tooling defect found at S2, and like the first two it would have discarded correct
  entries. The corrected index was re-checked the same way before the repeat: all 200 site cells,
  plus each span alone of the two cells that print two, were fed to the gate in the form the index
  now induces — `§ ` + the title as printed — and all 204 are accepted, on the rule field and on
  `Section` alike.
- **The repeat cleared the clause field and hit a fourth defect, this one in the validator.**
  `REPORT-A` 4 of 4; `REPORT-B` 0 of 7, every discard on the two `Evidence` cells, because `CX`
  cites sets of sites in one cell — `CANDIDATE-A.md:149-153,351-355` — and the reference pattern
  took one span. It is that side's constant convention, not an edge case: 10 of its 10 direct
  references carry several spans, against 0 of `CC`'s 7. The template lists *examples* of a
  locatable reference and never says one per cell, and the gate read only the first bullet anyway,
  so two sites in two bullets already passed with the second unread. `_reference_errors` now takes
  the list and resolves **every** span, which tightens the check rather than loosening it; the
  artifacts were revalidated unchanged — 4 of 4 and 7 of 7 — since nothing the models read had
  changed. `assets/improvement-template.md` states the form from now on, but **only at the source**:
  the copy inside this payload stays as it was, because it is the evidence of what the two sides
  actually read. The correction was decided knowing which side was falling, and that is recorded
  here rather than smoothed over.

### CON-6: decided at S1, and what the two calls actually did

- **`SKILL.md` is `28b5460`**, the working tree clean at that commit. The installed copy under
  `~/.agents/skills/plan-slices/` is byte-identical to it, checked with `diff -r`; the candidates are
  therefore generated against the committed text and not against a stale install.
- **`REPORT-A` is `CC`, `REPORT-B` is `CX`** — decided here, at S1, with the candidate assignment, so
  that the two do not coincide: `CC` holds `CANDIDATE-B` and `REPORT-A`. The two `IMPROVEMENT` rows
  join the table at S2, before the `improve` calls; the assignment they will carry is this one and is
  not re-decided there.
- **Both sides are invoked explicitly**: `/plan-slices` on Claude Code, `$plan-slices` on Codex. Since
  `3658187` the skill carries `disable-model-invocation: true` and `allow_implicit_invocation: false`,
  so the CON-1…CON-5 generation prompt would have produced plans generated **without the skill**. The
  boundary is recorded in `../workflow/CYCLE.md` § *Confini di strumento*.
- **Effort was `medium`, not the `high` declared here before the calls.** Both sides, symmetrically;
  the two cells were corrected when S1 closed, and the plans were **not** regenerated. Two reasons
  and one consequence. The thesis CON-6 tests is comparative — how many entries per side survive the
  conformance gate — so a symmetric shift does not touch it, and the four cycle phases stay at
  `high`, which is where that variable lives. And there is no `high` generation baseline to be
  comparable with: CON-1…CON-5 read `unrecorded`, so regenerating would have bought a comparability
  that does not exist. The error is asymmetric in the skill's favour: a candidate generated at lower
  effort is a harder condition, so a `not falsified` verdict measured on these plans is stronger, not
  weaker — only a `regressed` verdict is ambiguous, and that ambiguity is carried by the `gen` slot
  of the row that records it. The consequence is in `../workflow/CYCLE.md` § *Confini di strumento*:
  the CON-6 → CON-7 effort boundary is not what it said it was.
- **The plans are in Italian**, as CON-1…CON-5 were, and the prediction this section previously
  carried — *«the first cycle in which they are in English»* — was **wrong**. `SKILL.md:335` says
  *«write content in the user's language»*, and the two harnesses resolved that to Italian on both
  sides; the sources under `recipe-app/sources/` are Italian too, and nothing here separates the two
  causes, which happen to agree. What is English is the **structure** — section names, field names,
  order — because it comes from the template, which is exactly what that same line prescribes. So
  the plans conform to the skill, `../README.md` § *Language* does not reach them, and the boundary
  predicted at CON-5 → CON-6 **was not crossed**: one fewer, not one more.

### How the harness was reconstructed

No document declares the `CC` / `CX` expansion. Four pieces of evidence give it, and they agree:

- `GRADING-IMPROVEMENTS-PLAN.md:551` lists `PLAN-CX`, `PLAN-CC`, `codex`, `claude` in one
  de-identification rule — the two aliases and the two provider names side by side, and only two
  providers ever appear in this project;
- `PROMPTS.md` § `GENERATE PLAN`, the only surviving generation prompt, writes to
  `…/results/PLAN-CC-CON-XX.md` and addresses its inputs with `@`-prefixed paths, which is Claude
  Code's interactive file-reference syntax. It pins `CC` to Claude Code, and the pairing does the
  rest;
- the grading artifacts name their two providers `claude` and `codex` (`grader.provider`), so those
  are the two CLIs installed and used for this scenario;
- `PLAN-CX-CON-4.REVIEW.md` is in English while `PLAN-CC-CON-4.REVIEW.md` is in Italian, and the
  ledger's own characterisation of the two CON-4 `IMPROVEMENT`s — one operational with `file:line`
  citations, the other eight generic bullets — matches the CC / CX split consistently across the
  cycle. Weak on its own, corroborating next to the rest.

**The `IMPROVEMENT` and `REVIEW` sides** follow from `workflow/CYCLE.md` § *Cecità e simmetria*: up to
CON-5 each model improved the plan it knew as its own and reviewed its own report against the other's.
`PLAN-CC-CON-4.REVIEW.md` declares `Reviewed report: PLAN-CC-CON-4.IMPROVEMENT.md`, so both `CC`
artifacts are `CC`'s.

**The mode** follows from the shape of the generation prompt — an `@`-reference chat message, not a
headless invocation — and is the fact Fase 6 of `CONSENSUS-WORKFLOW-PLAN.md` already commits to
recording as a boundary: *«i piani CON-1…CON-N-1 nascono da sessioni interattive, non da chiamate
headless»*.

## Model and effort: unrecorded, declared once

**Which model and which effort generated `CC` and `CX` in CON-1…CON-5 cannot be reconstructed.** All
fourteen cells read `unrecorded`, and so do the seventeen `gen` slots in `REGRESSION-LEDGER.md`. This
is the declaration the ledger points at; it is not repeated per row and it is not a lapse in filling
the table.

Where it was looked for, and what was found:

- **The artifacts themselves.** No plan, `IMPROVEMENT` or `REVIEW` names a model, an agent or a
  harness. The CON-6 prompts forbid it; the prompts of CON-1…CON-5 simply never asked for it.
- **`PROMPTS.md` § `GENERATE PLAN`.** The only surviving generation prompt. It names an output path
  and says nothing about configuration.
- **Every grading artifact under `recipe-app/results/calibration-*`.** These record
  `grader.provider`, `grader.requested_model`, `grader.effort` and `grader.cli_version` — for the
  **grader**. The v1 artifacts record `"model": "cli-default"`, which names the CLI default at run
  time and is not resolvable backwards. No field names the candidate's generator: the candidate
  appears as a path, without so much as a hash.
- **The commit messages** of the five commits that carry the plans.
- **`GRADING-IMPROVEMENTS-PLAN.md`.** It records `gpt-5.6-sol`/`high` and `claude-opus-5`/`high`, and
  the CLI versions `codex-cli 0.146.0`, `claude 2.1.221`, `2.1.220 (Claude Code)`. All of it belongs
  to grading runs of 2026-08-03 and 2026-08-04. None of it belongs to a generation.

**The inference is refused.** Copying the grading defaults into these cells would put a plausible
number in the one column that exists to state how a verdict was actually obtained — the failure mode
the column was added to prevent. `unrecorded` is the true value.

The practical consequence: CON-1…CON-5 and CON-6 are separated by a boundary that cannot be
described, on top of the boundaries `workflow/CYCLE.md` lists. A CON-6 verdict that differs from a
CON-5 one cannot be attributed to the skill rather than to a model change, because there is no way to
know whether the model changed. From CON-6 the cell is filled before the call, not after.

## When each artifact was generated

Commit dates bound the generation from above; where an artifact is referenced by something dated
earlier, the earlier date is the real bound. Times are local, as `git log` reports them.

| Cycle | Bound | Evidence |
|---|---|---|
| CON-1 | by 2026-07-30 13:24 | `f336e63` adds both, as `PLAN-CC-CON.md` and `PLAN-CX-CON.md` |
| CON-2 | `CC` by 2026-07-31 14:58, `CX` by 2026-07-31 17:08 | `e5c166c`; `c925d86`, which adds the `CX` blob under the name `PLAN-CX-CON-4.md` |
| CON-3 | by 2026-08-01 16:12 | `1e466f4` — both blobs first appear there |
| CON-4 | by 2026-08-01 16:12 | `1e466f4` — both blobs first appear there |
| CON-4 `IMPROVEMENT`, `REVIEW` | by 2026-08-02 15:37 | `472233d` adds all four |
| CON-5 | **by 2026-08-02 17:03** | `f00d75d` commits `calibration-legacy/raw/PLAN-{CC,CX}-CON-5.{claude,codex}.v1.SCORE.json`, which grade both plans. The plans themselves were committed only at `515e0a3`, 2026-08-04 11:57 |

Two caveats on the CON-5 row, both load-bearing:

- **The bound is on existence, not on the committed text.** The v1 metadata records no candidate
  hash, so nothing proves the text graded on 2026-08-02 is byte-identical to the text committed on
  2026-08-04. The v2 artifacts stamp `2026-08-03T13:56:32Z` (codex) and `2026-08-03T21:07:41Z`
  (claude) on `PLAN-CC-CON-5.md` and carry no candidate hash either.
- **It strengthens the Fase 2 argument rather than weakening it.** `CONSENSUS-WORKFLOW-PLAN.md`
  refuses to reuse the CON-5 plans because they predate `87150d3` (2026-08-04 23:11) and `eb926bb`
  (2026-08-04 23:30) and so cannot test `R-010` and `R-011`. That file dates them to 11:57 on
  2026-08-04, which is when they were **committed**; they existed at least a day and a half earlier,
  so the gap is wider than stated.

## The `1e466f4` renumbering — why `CON-N` is the cycle

`1e466f4` (2026-08-01 16:12, message *renaming*) did more than rename, and reading it as a rename
misdates half this table. Matching blob hashes across it:

| Before | After |
|---|---|
| `PLAN-CC-CON.md` | `PLAN-CC-CON-1.md` — unchanged |
| `PLAN-CC-CON-2.md` | unchanged |
| — | `PLAN-CC-CON-3.md`, `PLAN-CC-CON-4.md` — new blobs |
| `PLAN-CX-CON.md` | `PLAN-CX-CON-1.md` — unchanged |
| `PLAN-CX-CON-4.md` | `PLAN-CX-CON-2.md` — same blob, renumbered |
| — | `PLAN-CX-CON-3.md`, `PLAN-CX-CON-4.md` — new blobs |
| `PLAN-CX-CON-2.md`, `PLAN-CX-CON-3.md` | deleted |
| `PLAN-CC-SENZA.md`, `PLAN-CX-SENZA.md` | deleted |

`CX` had run three times before the plan format was restructured; `CC` had run once. The commit drops
the two unpaired pre-restructure `CX` runs and renumbers the rest so that **`CON-N` means the cycle,
not the side's run ordinal**. Two consequences worth holding on to:

- `PLAN-CX-CON-2.md` was generated on 2026-07-31 under a different name. Its git history read without
  the blob match dates it to 2026-08-01, an hour and a half of a whole cycle off.
- Two `CX` generations exist in history and in no cycle. They carry no ledger row and no verdict, and
  they are not evidence about anything the cycle measures.

## Format for a new cycle

Add the rows **before** the calls, not after the report. Per cycle, eight rows at most: two
candidates, two `IMPROVEMENT`s, two `REVIEW`s, two `VERDICTS`. Each row carries harness, mode,
model, effort, alias, and the attribution — which for a cycle recorded ahead of time is `declared`,
the value CON-1…CON-5 could not have.

**The two `VERDICTS` rows joined the format at CON-6**, which is the first cycle whose verdicts come
from a `verdetto` call instead of offline human reading. Their alias column is `—`: those artifacts
enter no payload, so they have nothing to be blind about, and the column would record a mapping that
does not exist. What their rows carry that nothing else does is the fifth `Measured on` slot,
`verdict <instrument>`, which without them would name a call whose model and effort are recorded
nowhere. The same holds for the two `REVIEW` rows.

Both alias assignments are decided at payload composition and written here first. A row whose alias
column is filled after the call has recorded nothing: the point of the column is that the mapping
existed before anyone could have inferred it.

The `recidiva` call has no row here. It is one call on a fixed model, declared in
`REGRESSION-LEDGER.md` § *`Measured on`* rather than mapped to a side, because it has no side.
