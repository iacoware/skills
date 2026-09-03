# Prompt — ROADMAP-CC-6C

Run headless: nessuna persona ha guidato la sessione in interattivo, ed è la departure che
[`../README.md`](../README.md) obbliga a registrare qui. Il testo è
[`../../prompts/run.prompt.md`](../../prompts/run.prompt.md) con `{{RUN_DIR}}` risolto, e non
differisce in altro dalla card 0 di [`../../SCENARIOS.md`](../../SCENARIOS.md).

Satellite di `ROADMAP-CC-6` per il prezzamento del rumore
([`design/roadmap/EVAL-NOISE.md`](../../../../../design/roadmap/EVAL-NOISE.md)): stesso commit,
stesso prompt, stesso modello ed effort del principale, lanciato da `make eval-noise`. È un run di
prima classe minus review, generation-only: non riceve mai `REVIEW.md` né `IMPROVEMENTS.md` — e
i suoi confronti stanno nel `NOISE.md` del principale.


Quel che questa forma non mette alla prova è il path di invocazione interattivo. Nello scenario 0
non c'è niente da confermare e niente da rispondere — il prompt risponde da sé all'unica domanda
dovuta, quella su che cosa è stato consegnato — quindi la perdita è piccola, ma non è zero.

| | |
|---|---|
| Harness | `claude -p` |
| Modello | `opus` |
| Effort | `high` |
| Session id | `a92fa0fb-508b-4f20-9dce-c9913a43abbb` |
| Commit | `fb29812 Implement eval-noise: satellite twin runs and the per-axis agreement report` |
| `skills/roadmap` | tree `0d47a59`, uguale a HEAD |

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

Tratta ./evals/roadmap/recipe-app/results/ROADMAP-CC-6C/ come project root; crea la directory prima.

Vincoli di lettura di questa sessione, sopra a quello che dice la skill — valgono anche per qualunque sub-agent a cui deleghi:

- Gli unici file del repository che puoi leggere sono i documenti sotto evals/roadmap/recipe-app/sources/ e i file che scrivi tu stesso.
- Tutto il resto di evals/ è off limits in lettura: puoi solo scriverci dentro. In particolare non cercare, non elencare e non aprire nulla che si chiami reference-roadmap, fixtures, EVALUATION-*, REVIEW-WORKFLOW, REFERENCE-NOTES, SCENARIOS, PROMPT.md, REVIEW.md, IMPROVEMENTS.md, README.md, AGENTS.md o altri results/ di run precedenti.
- Off limits anche design/, skills/, CONTEXT-MAP.md e AGENTS.md alla radice del repo.
- Non eseguire find, ls -R, grep, glob o qualunque ricerca che spazi su quelle directory. Se un tuo comando restituisse per sbaglio contenuto proibito, ignoralo e non usarlo.

~~~
