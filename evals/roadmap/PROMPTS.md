```
Questo è uno scratchpad per l'umano. Non scriverci.
```

---

## Generazione di una roadmap per recipe-app

Leggi evals/roadmap/recipe-app/sources/goal.md e usa /roadmap per disegnare la strada che raggiunge
l'obiettivo che dichiara.

Tratta evals/roadmap/recipe-app/results/ROADMAP-CC-<N>/ come project root; crea la directory prima.

Vincoli di lettura di questa sessione, sopra a quello che dice la skill — valgono anche
per qualunque sub-agent a cui deleghi:

- Gli unici file del repository che puoi leggere sono i documenti sotto
  evals/roadmap/recipe-app/sources/ e i file che scrivi tu stesso.
- Tutto il resto di evals/ è off limits in lettura: puoi solo scriverci dentro.
  In particolare non cercare, non elencare e non aprire nulla che si
  chiami reference-roadmap, fixtures, EVALUATION-\*, REVIEW-WORKFLOW, REFERENCE-NOTES,
  SCENARIOS, PROMPT.md, REVIEW.md, README.md, AGENTS.md o altri results/ di run
  precedenti.
- Off limits anche design/, skills/, CONTEXT-MAP.md e AGENTS.md alla radice del repo.
- Non eseguire find, ls -R, grep, glob o qualunque ricerca che spazi su quelle
  directory. Se un tuo comando restituisse per sbaglio contenuto proibito, ignoralo e
  non usarlo.

**Dopo la chiusura — non fa parte del prompt, e non si chiede alla sessione.** Appena la sessione ha
dato il report finale, da un secondo terminale e prima di digitare altro lì dentro:

```
make capture-transcript RUN=evals/roadmap/recipe-app/results/ROADMAP-CC-<N>
```

Una sessione fresca per run, e cattura prima di `/clear`, che apre un file nuovo.

---

## Valutazione di un piano generato per recipe-app

Rivedi la mappa in @evals/roadmap/recipe-app/results/ROADMAP-CC-<N>/.roadmap/ e scrivi il report
in @evals/roadmap/recipe-app/results/ROADMAP-CC-<N>/REVIEW.md.

Prima gira `make validate-roadmap ROADMAP=evals/roadmap/recipe-app/results/ROADMAP-CC-<N>/.roadmap`
dalla radice del repo. Se segnala ERROR, riportalo nel report e continua: la mappa è un reperto e non
va corretta.

Poi, in quest'ordine, che non va invertito:

1. @evals/roadmap/recipe-app/EVALUATION-BRIEF.md con la mappa in mano. Il brief è l'autorità sui
   sources: apri @evals/roadmap/recipe-app/sources/ solo per verificare una citazione. Le voci A e N
   licenziano differenze e non sono violazioni; lo sono le H mancanti e le C risolte in silenzio.
2. @evals/roadmap/EVALUATION-RULES.md, regola per regola. Questo è un primo disegno: salta la sezione
   "Revising an existing map", R-006 e R-018. Leggi il register e i documenti in slices/ insieme.
3. Solo alla fine @evals/roadmap/recipe-app/reference-roadmap/ con REFERENCE-NOTES.md, per trovare
   quello che ti sei dimenticato. Non è un target di diff: id, titoli, numero di temi e di righe
   possono differire; su ogni differenza chiedi quale delle due ha la ragione migliore.

Se la directory del run contiene un TRANSCRIPT.jsonl, leggilo: è lì che sta la metà delle prove che la
mappa non porta — cosa ha chiesto, cosa ha proposto, se ha girato il validator, come ha chiuso. Se non
c'è, quelle regole sono _inconclusive_, non rosse, e il report lo dice.

Report: una riga per violazione, con l'id (R-xxx, o H/C del brief), dove sta nella mappa, e cosa la
falsifica. Nessun punteggio. In questa sessione non modificare SKILL.md, i fixture, l'oracolo né la
mappa valutata: l'unico file che scrivi è REVIEW.md, e la decisione su cosa cambiare viene dopo il
report.

---

## Rifattorizza lo skill

Leggi @skills/roadmap/SKILL.md. Vorrei renderlo il più lean possibile rimuovendo contenuto superficiale e duplicazioni.
La ristrutturazione deve rendere efficace per un LLM usare lo skill, non renderlo chiaro per un umano.

Proponimi delle opzioni di ristrutturazione suddividendole in due opzioni: coraggiose e di piccoli miglioramenti.

Tieni sempre in mente l'intento dello skill dichiarato in ROADMAP-GOAL.md.

---
