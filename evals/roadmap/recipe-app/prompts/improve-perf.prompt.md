Lo skill roadmap impiega troppo a disegnare una mappa da zero — quanto esattamente lo dice il METRICS.md di questo run. Voglio proposte di cambiamento coraggiose che riducano il wall-clock e, secondariamente, i token nella main context window. Non implementare nulla in questa sessione: produci opzioni.

## Evidenza da cui partire

Leggi, in quest'ordine:

- @{{RUN_DIR}}/METRICS.md, e il METRICS.md di ogni run precedente sotto evals/roadmap/recipe-app/results/: una misura sola non distingue una tendenza da una giornata storta.
- @{{RUN_DIR}}/TRANSCRIPT.jsonl — profila tu stesso il tempo per chiamata API e cosa lo consuma. METRICS.md è derivato e il transcript è la prova: dove i due sono in disaccordo vince il transcript.
- skills/roadmap/ per intero (SKILL.md, references/, assets/, scripts/)
- design/roadmap/ROADMAP-GOAL.md, che resta l'autorità sull'intento, e CONTEXT.md sul vocabolario

## Cosa voglio

Opzioni di cambiamento allo skill, divise in **coraggiose** (cambiano la forma di come lo skill lavora) e **piccoli miglioramenti** (interventi locali, rischio basso). Ordina dentro ogni gruppo per rapporto risparmio/rischio.

Per ciascuna opzione:

- quali file cambia
- il risparmio atteso, in secondi o token, e su quale riga dell'evidenza lo fondi
- il rischio di qualità, e quale regola di evals/roadmap/EVALUATION-RULES.md o quale voce di recipe-app/EVALUATION-BRIEF.md lo intercetterebbe se si materializzasse
- come si misura dopo: quale metà del REVIEW-WORKFLOW, quante provider call

Due tattiche che voglio siano valutate esplicitamente, accettate o scartate con una ragione:

- **fan-out su subagent**: gli slice document sono indipendenti una volta fissati register, temi e archi. Un subagent per documento, o a gruppi. Cosa deve stare nel contratto di input perché i documenti restino coerenti fra loro (Depends on, Excludes, confini fra temi), e cosa torna in main context — il documento intero o solo la conferma che è stato scritto.
- **subagent che legge e riassume**: le sorgenti, e in generale tutto ciò che serve a decidere ma non a scrivere, potrebbero non entrare mai in main context.

Non limitarti a queste due: se il transcript mostra una terza leva più grossa, quella conta di più.

## Vincoli

- ROADMAP-GOAL.md dice cosa il tool non deve diventare. Nessuna opzione può comprare velocità aggiungendo campi, cerimonia o precisione finta.
- Il payload installato deve restare autosufficiente: gira da ~/.claude/skills/roadmap, senza nulla del repository attorno.
- La sessione parla con l'autore secondo regole precise: un solo blocco di conferma, una sola domanda bloccante, il report a quattro parti in chiusura. Delegare non deve moltiplicare i round trip né spostare una decisione dentro un subagent.
- I run di eval impongono ai subagent gli stessi vincoli di lettura della sessione madre (vedi run.prompt.md accanto a questo). Uno skill che delega deve saper propagare vincoli che non conosce in anticipo: di' come.
- Nessuna provider call in questa sessione. Se un'opzione va verificata con un run, dimmelo e quantifica; AGENTS.md richiede autorizzazione esplicita prima di lanciarlo.

## Output

Scrivi il report in @{{RUN_DIR}}/PERF-SUGGESTIONS.md, in italiano come il resto della directory; è l'unico file che scrivi. Non toccare SKILL.md, references/, assets/, scripts/ né altro sotto evals/. Chiudi con le domande aperte che bloccano la scelta fra le opzioni, se ce ne sono.
