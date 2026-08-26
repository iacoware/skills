Leggi @{{RUN_DIR}}/REVIEW.md, che è il report di questo run, e poi ogni altro REVIEW.md sotto evals/roadmap/recipe-app/results/, che sono i run precedenti: servono a sapere quali violazioni ricorrono e quali sono comparse una volta sola.

Poi, con quelli in mano: @design/roadmap/ROADMAP-GOAL.md, che resta l'autorità sull'intento, e @design/roadmap/CONTEXT.md sul vocabolario; il preambolo di @evals/roadmap/EVALUATION-RULES.md, fino alla prima regola; e skills/roadmap/ per intero — SKILL.md, references/, assets/, scripts/.

Scegli i tre interventi che pagano di più e presentami solo quelli. Non un catalogo di tutto il migliorabile: tre, quelli che faresti tu per primi, nell'ordine in cui li faresti.

Il criterio è la ricorrenza, non la gravità. Il preambolo delle regole dice che un run registra e due dicono che la clausola non sta facendo il suo lavoro: una violazione che compare in due o più run pesa più di una peggiore vista una volta sola. Una violazione vista una volta sola entra fra i tre solo se dici perché non conviene aspettare il secondo run.

Per ciascuno dei tre:

- quale file cambia, e che cosa ci scrivi al posto di che cosa. Il fix atterra nell'artefatto che lo possiede — una regola applicata male è un difetto di references/, un campo che nessuno riesce a riempire è un difetto del template. Mai in SKILL.md per default: è così che un router ricresce in un monolite.
- quali violazioni chiude, per id (R-xxx, o H/C del brief) e in quali run le hai viste.
- che cosa rischia di rompere, e quale regola di EVALUATION-RULES.md o quale voce di EVALUATION-BRIEF.md se ne accorgerebbe se si materializzasse.
- come si misura dopo: quale metà di @evals/roadmap/REVIEW-WORKFLOW.md, e se serve un run nuovo.

Vincoli:

- ROADMAP-GOAL.md dice che cosa il tool non deve diventare. Nessuna proposta può comprare qualità aggiungendo campi, cerimonia o precisione finta.
- Non toccare i fixture, l'oracolo, EVALUATION-RULES.md, il brief né alcunché sotto evals/: cambiare la rete per far passare uno scenario è ciò che distrugge una eval.
- Non implementare niente in questa sessione e non modificare skills/. Produci proposte.
- Nessuna provider call.

Scrivi il report in @{{RUN_DIR}}/IMPROVEMENTS.md, in italiano come il resto della directory; è l'unico file che scrivi. Se fra le violazioni ricorrenti ce n'è una che hai scartato dai tre, chiudi con una riga che dice quale e perché.
