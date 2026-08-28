# Prompt — ROADMAP-CC-5

Run headless: nessuna persona ha guidato la sessione in interattivo, ed è la departure che
[`../README.md`](../README.md) obbliga a registrare qui. Il testo è
[`../../prompts/run.prompt.md`](../../prompts/run.prompt.md) con `{{RUN_DIR}}` risolto, e non
differisce in altro dalla card 0 di [`../../SCENARIOS.md`](../../SCENARIOS.md).

Quel che questa forma non mette alla prova è il path di invocazione interattivo. Nello scenario 0
non c'è niente da confermare e niente da rispondere — il prompt risponde da sé all'unica domanda
dovuta, quella su che cosa è stato consegnato — quindi la perdita è piccola, ma non è zero.

| | |
|---|---|
| Harness | `claude -p` |
| Modello | `opus` |
| Effort | `high` |
| Session id | `feac66af-a33a-46f5-9211-0db3da0a7c50` |
| Commit | `37a0976 Update TODO` |
| `skills/roadmap` | tree `0913e60`, uguale a HEAD |

Le ultime due righe sono l'ancoraggio, e la skill che ha girato è quella che dichiarano: la sessione
legge la copia installata, e il ciclo si ferma prima di inviare se quella copia e l'albero di lavoro
divergono. Il commit è il punto della storia — è da lì che il ciclo di miglioramento delimita
l'intervallo dei fix che questo run ha messo alla prova, `git log <commit del run precedente>..<questo>
-- skills/roadmap`, e dentro l'intervallo si leggono tutti i commit. Il tree è l'identità del
contenuto: due run che ne dichiarano uno uguale hanno girato la stessa skill, per quanti commit ci
siano stati in mezzo.

Il prompt, alla lettera:

~~~
Leggi evals/roadmap/recipe-app/sources/goal.md e usa /roadmap per disegnare la strada che raggiunge l'obiettivo che dichiara.

Tratta evals/roadmap/recipe-app/results/ROADMAP-CC-5/ come project root; crea la directory prima.

Vincoli di lettura di questa sessione, sopra a quello che dice la skill — valgono anche per qualunque sub-agent a cui deleghi:

- Gli unici file del repository che puoi leggere sono i documenti sotto evals/roadmap/recipe-app/sources/ e i file che scrivi tu stesso.
- Tutto il resto di evals/ è off limits in lettura: puoi solo scriverci dentro. In particolare non cercare, non elencare e non aprire nulla che si chiami reference-roadmap, fixtures, EVALUATION-*, REVIEW-WORKFLOW, REFERENCE-NOTES, SCENARIOS, PROMPT.md, REVIEW.md, IMPROVEMENTS.md, README.md, AGENTS.md o altri results/ di run precedenti.
- Off limits anche design/, skills/, CONTEXT-MAP.md e AGENTS.md alla radice del repo.
- Non eseguire find, ls -R, grep, glob o qualunque ricerca che spazi su quelle directory. Se un tuo comando restituisse per sbaglio contenuto proibito, ignoralo e non usarlo.

~~~
