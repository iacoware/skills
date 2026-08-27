# Prompt — ROADMAP-CC-3

**Questo file è ricostruito da `TRANSCRIPT.jsonl`, non scritto prima dell'invio.** Il run è di
prima che `run_cycle.ts` guidasse il ciclo, e non aveva lasciato il `PROMPT.md` che
[`../README.md`](../README.md) obbliga a tenere. Ogni riga qui sotto è un dato che il transcript
prova; quello che il transcript non registra non compare.

| | |
|---|---|
| Harness | Claude Code CLI (`entrypoint: cli`, versione `2.1.241`) |
| Modello | `claude-opus-5` |
| Effort | `high` |
| Session id | `10ff2305-b95a-4abb-8145-6bf50e8d9aae` |
| Commit | `e27d419` — *fix violazione C2 di ROADMAP-CC-2* |
| `skills/roadmap` | tree `028f3b4` |

Nessuna riga del transcript porta `isSidechain: true`: la sessione non ha delegato a sub-agent.

**Le ultime due righe sono ricostruite come il resto.** La sessione ha letto i file della skill con
`cat`, e il transcript ne conserva il testo integrale: confrontato con ogni versione storica di
`skills/roadmap`, `references/drawing-the-map.md` combacia per intero con una versione sola, quella
di `e27d419`. Fra quella e `e287aee`, il commit che aggiunge il run, nessun commit tocca la skill:
qui l'ancoraggio e l'inferenza dalla data darebbero la stessa risposta.

Il prompt, alla lettera — primo e unico turno d'autore con contenuto:

~~~
Leggi evals/roadmap/recipe-app/sources/goal.md e usa /roadmap per disegnare la strada che raggiunge l'obiettivo che dichiara.

Tratta evals/roadmap/recipe-app/results/ROADMAP-CC-3/ come project root; crea la directory prima.

Vincoli di lettura di questa sessione, sopra a quello che dice la skill — valgono anche per qualunque sub-agent a cui deleghi:

- Gli unici file del repository che puoi leggere sono i documenti sotto evals/roadmap/recipe-app/sources/ e i file che scrivi tu stesso.
- Tutto il resto di evals/ è off limits in lettura: puoi solo scriverci dentro. In particolare non cercare, non elencare e non aprire nulla che si chiami reference-roadmap, fixtures, EVALUATION-*, REVIEW-WORKFLOW, REFERENCE-NOTES, SCENARIOS, PROMPT.md, REVIEW.md, README.md, AGENTS.md o altri results/ di run precedenti.
- Off limits anche design/, skills/, CONTEXT-MAP.md e AGENTS.md alla radice del repo.
- Non eseguire find, ls -R, grep, glob o qualunque ricerca che spazi su quelle directory. Se un tuo comando restituisse per sbaglio contenuto proibito, ignoralo e non usarlo.
~~~

Porta il vincolo di lettura di [`../../REVIEW-WORKFLOW.md`](../../REVIEW-WORKFLOW.md) *Producing a
run* passo 2, e non è la formulazione di nessuna card di `SCENARIOS.md`: la card è stata adattata
a un project root sotto `results/` e a una sessione che può delegare.
