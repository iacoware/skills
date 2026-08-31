Rivedi la mappa in @{{RUN_DIR}}/.roadmap/ e scrivi il report in @{{RUN_DIR}}/REVIEW.md.

Prima gira `make validate-roadmap ROADMAP={{RUN_DIR}}/.roadmap` dalla radice del repo. Se segnala ERROR, riportalo nel report e continua: la mappa è un reperto e non va corretta.

Poi, in quest'ordine, che non va invertito:

1. @evals/roadmap/recipe-app/EVALUATION-BRIEF.md con la mappa in mano. Il brief è l'autorità sui sources: apri @evals/roadmap/recipe-app/sources/ solo per verificare una citazione. Le voci A e N licenziano differenze e non sono violazioni; lo sono le H mancanti e le C risolte in silenzio.
2. @evals/roadmap/EVALUATION-RULES.md, regola per regola. Questo è un primo disegno: salta la sezione "Revising an existing map", R-006 e R-018. Leggi il register e i documenti in slices/ insieme.
3. Solo alla fine @evals/roadmap/recipe-app/reference-roadmap/ con REFERENCE-NOTES.md, per trovare quello che ti sei dimenticato. Non è un target di diff: id, titoli, numero di temi e di righe possono differire; su ogni differenza chiedi quale delle due ha la ragione migliore.

Se la directory del run contiene un TRANSCRIPT.jsonl, leggilo: è lì che sta la metà delle prove che la mappa non porta — cosa ha chiesto, cosa ha proposto, se ha girato il validator, come ha chiuso. Se non c'è, quelle regole sono _inconclusive_, non rosse, e il report lo dice.

Report: una riga per violazione, con l'id (R-xxx, o H/C del brief), dove sta nella mappa, e cosa la falsifica. **Dove più fatti convergono sulla stessa riga, uno solo regge il verdetto**: nominalo, e marca gli altri come corroborazione. Una catena di fatti allo stesso livello lascia a chi legge la scelta di quale usare, e chi legge sceglierà quello che gli serve. Nessun verdetto aggregato sulla mappa. In questa sessione non modificare SKILL.md, i fixture, l'oracolo né la mappa valutata: l'unico file che scrivi è REVIEW.md, e la decisione su cosa cambiare viene dopo il report.

Chiudi il report con la sezione `## Tally` che il preambolo di @evals/roadmap/EVALUATION-RULES.md definisce: quattro liste di id — verdi, rossi, inconclusive, non applicabili o saltati — sui check che questa carta ammette, cioè le regole più le righe H del brief. Un check è rosso se almeno un rilievo gli sta contro, per quanti convergano; un rilievo C o U conta una volta sola, sotto la regola che istanzia; le voci A e N licenziano differenze e non si contano. In fondo il pass rate, verdi/(verdi+rossi), e il commit del repo che fissa il rule set (`git rev-parse HEAD`). Il tally è una linea di tendenza fra run della stessa carta sullo stesso rule set, non un verdetto sulla mappa: il giudizio resta per check, su due run.
