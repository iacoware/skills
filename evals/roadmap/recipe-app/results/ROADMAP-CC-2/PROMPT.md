# Run `ROADMAP-CC-2`

A drawing from an empty directory, against `skills/roadmap/SKILL.md` as rewritten by sessions S1–S4
of `design/roadmap/REFACTORING-PLAN.md`. Reconstructed from `TRANSCRIPT.jsonl`, which is what the
session received, rather than from the card in [`../../PROMPTS.md`](../../PROMPTS.md).

## Model and harness

`claude-opus-5`, Claude Code CLI, one interactive session driven by a person — no sub-agent, and no
turn in `TRANSCRIPT.jsonl` carries `isSidechain: true`. 37 assistant turns.

Effort: high

## The version of the skill that ran

Commit `666566d` — *Execute session S3 of the refactoring plan* — and `skills/roadmap` at tree
`eedf170`.

**Reconstructed, not recorded**: this run predates the anchor `run_cycle.ts` now writes before
sending, so it is read back out of `TRANSCRIPT.jsonl`, where the files the session `cat`-ed survive
in full. `references/drawing-the-map.md` and `assets/roadmap-template.md` match two candidate
versions, `676b580` and `666566d`, which differ in `SKILL.md` alone — and `SKILL.md` is loaded by
the harness, so no `cat` of it is in the transcript. What separates them is what the session quoted
back:
76 of the 76 lines proper to `666566d` appear in the transcript, against 1 of the 78 proper to
`676b580`. No commit touched `skills/roadmap` between that version and `bf979c3`, the commit that
added this run, so here the anchor and the cheap inference agree.

## The exact text sent

Sent as the first and only human turn.

```
Leggi evals/roadmap/recipe-app/sources/goal.md e usa /roadmap per disegnare la strada che raggiunge l'obiettivo che dichiara.

Tratta evals/roadmap/recipe-app/results/ROADMAP-CC-2/ come project root; crea la directory prima.

Vincoli di lettura di questa sessione, sopra a quello che dice la skill — valgono anche per qualunque sub-agent a cui deleghi:

Gli unici file del repository che puoi leggere sono i documenti sotto evals/roadmap/recipe-app/sources/ e i file che scrivi tu stesso.
Tutto il resto di evals/ è off limits in lettura: puoi solo scriverci dentro. In particolare non cercare, non elencare e non aprire nulla che si chiami reference-roadmap, fixtures, EVALUATION-*, REVIEW-WORKFLOW, REFERENCE-NOTES, SCENARIOS, PROMPT.md, REVIEW.md, README.md, AGENTS.md o altri results/ di run precedenti.
Off limits anche design/, skills/, CONTEXT-MAP.md e AGENTS.md alla radice del repo.
Non eseguire find, ls -R, grep, glob o qualunque ricerca che spazi su quelle directory. Se un tuo comando restituisse per sbaglio contenuto proibito, ignoralo e non usarlo.
```

It carries the read restriction of [`../../REVIEW-WORKFLOW.md`](../../REVIEW-WORKFLOW.md)
_Producing a run_ step 2, and is not the wording of any card in `SCENARIOS.md`: the card was adapted
to a project root under `results/` and to a session that may delegate.

## Answers given back

**None.** After the prompt above no human turn carries content: the session asked nothing and was
answered nothing, and it closed without a second stop. Step 3 of _Producing a run_ — answer what it
asks and nothing else — had nothing to answer, which is itself evidence and belongs to the reading,
not to a defect recorded here.

## Where the run ends

At the four-part report, which is the last assistant turn in `TRANSCRIPT.jsonl`. Nothing was typed
into the session after it, so the capture needs no line saying where to stop reading.
