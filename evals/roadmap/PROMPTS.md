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

## Migliorare le performance

Lo skill roadmap impiega 13-14 minuti per disegnare una mappa da zero. Voglio proposte di
cambiamento coraggiose che riducano il wall-clock e, secondariamente, i token nella main
context window. Non implementare nulla in questa sessione: produci opzioni.

## Evidenza da cui partire

Leggi, in quest'ordine:

- evals/roadmap/recipe-app/results/ROADMAP-CC-3/METRICS.md e ROADMAP-CC-2/METRICS.md
- evals/roadmap/recipe-app/results/ROADMAP-CC-3/TRANSCRIPT.jsonl — profila tu stesso il
  tempo per chiamata API e cosa lo consuma. Non fidarti del mio profilo qui sotto: verificalo.
- skills/roadmap/ per intero (SKILL.md, references/, assets/, scripts/)
- design/roadmap/ROADMAP-GOAL.md, che resta l'autorità sull'intento, e CONTEXT.md sul vocabolario

Il mio profilo di CC-3, da confermare o smentire: 743s su 803s di tempo attivo stanno in 6
chiamate API su 32. Due sono thinking puro (275s e 146s), tre sono heredoc Bash che generano
roadmap.md e gli 11 documenti in slices/ (94s, 85s, 72s), una è thinking (71s). Il thinking è
il 65% dell'output. Prima di scrivere una riga la sessione carica in main context
slice-rules.md (~13k char), drawing-the-map.md (~16k), i due template (~5k) e ~20k di
validate_roadmap.ts letto in tre pezzi — quest'ultimo per dedurre cap e floor, che nessun
documento le dice.

## Cosa voglio

Opzioni di cambiamento allo skill, divise in **coraggiose** (cambiano la forma di come lo
skill lavora) e **piccoli miglioramenti** (interventi locali, rischio basso). Ordina dentro
ogni gruppo per rapporto risparmio/rischio.

Per ciascuna opzione:

- quali file cambia
- il risparmio atteso, in secondi o token, e su quale riga dell'evidenza lo fondi
- il rischio di qualità, e quale regola di evals/roadmap/EVALUATION-RULES.md o quale voce di
  recipe-app/EVALUATION-BRIEF.md lo intercetterebbe se si materializzasse
- come si misura dopo: quale metà del REVIEW-WORKFLOW, quante provider call

Due tattiche che voglio siano valutate esplicitamente, accettate o scartate con una ragione:

- **fan-out su subagent**: gli 11 slice document sono indipendenti una volta fissati register,
  temi e archi. Un subagent per documento, o a gruppi. Cosa deve stare nel contratto di input
  perché i documenti restino coerenti fra loro (Depends on, Excludes, confini fra temi), e cosa
  torna in main context — il documento intero o solo la conferma che è stato scritto.
- **subagent che legge e riassume**: le sorgenti, e in generale tutto ciò che serve a decidere
  ma non a scrivere, potrebbero non entrare mai in main context.
  Non limitarti a queste due: se il transcript mostra una terza leva più grossa, quella conta di più.

## Vincoli

- ROADMAP-GOAL.md dice cosa il tool non deve diventare. Nessuna opzione può comprare velocità
  aggiungendo campi, cerimonia o precisione finta.
- Il payload installato deve restare autosufficiente: gira da ~/.claude/skills/roadmap, senza
  nulla del repository attorno.
- La sessione parla con l'autore secondo regole precise: un solo blocco di conferma, una sola
  domanda bloccante, il report a quattro parti in chiusura. Delegare non deve moltiplicare i
  round trip né spostare una decisione dentro un subagent.
- I run di eval impongono ai subagent gli stessi vincoli di lettura della sessione madre (vedi
  il prompt in evals/roadmap/PROMPTS.md). Uno skill che delega deve saper propagare vincoli che
  non conosce in anticipo: di' come.
- Nessuna provider call in questa sessione. Se un'opzione va verificata con un run, dimmelo e
  quantifica; AGENTS.md richiede autorizzazione esplicita prima di lanciarlo.

## Output

Un documento in design/roadmap/PERFORMANCE-OPTIONS.md, in inglese come il resto di design/.
Non toccare SKILL.md, references/, assets/, scripts/ né alcunché sotto evals/.
Chiudi con le domande aperte che bloccano la scelta fra le opzioni, se ce ne sono.

---

## Riflettere su PERFORMANCE-OPTIONS

Leggi @design/roadmap/PERFORMANCE-OPTIONS.md e @evals/roadmap/recipe-app/results/ROADMAP-CC-3/PERF-SUGGESTIONS.md . Vorrei discutere del suggerimento S1 "Scrivere meno prosa". Sono d'accordo sul mettere in campo questo fix. Se prendo la roadmap di CC-3, la tabella dei Themes di Now, di Later e out-of-scope vanno bene, mentre le altre sezioni come ordering criteria, assumptions, cross functional concerns sono molto lunghe, lì forse si può ridurre qualcosa. Non mi è chiaro come poterlo fare però.

Sei d'accordo con il mio assesment? Mi suggerisci una strategia per attuare la riduzione?
