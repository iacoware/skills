```
Questo è uno scratchpad per l'umano. Non scriverci.
```

---

I prompt del ciclo — il disegno, la sua review, e le due letture di quella review, sulla qualità e
sul costo — non stanno più qui. Sono quattro file in
[`recipe-app/prompts/`](recipe-app/prompts/), uno per sessione, e li manda
[`scripts/run_cycle.ts`](scripts/run_cycle.ts): là il file *è* il prompt alla lettera, e una copia in
questo scratchpad tornerebbe a divergere come è già successo.

Quel che resta qui sotto sono prompt one-off, tenuti per poterli rileggere.

---

## Rifattorizza lo skill

Leggi @skills/roadmap/SKILL.md. Vorrei renderlo il più lean possibile rimuovendo contenuto superficiale e duplicazioni.
La ristrutturazione deve rendere efficace per un LLM usare lo skill, non renderlo chiaro per un umano.

Proponimi delle opzioni di ristrutturazione suddividendole in due opzioni: coraggiose e di piccoli miglioramenti.

Tieni sempre in mente l'intento dello skill dichiarato in ROADMAP-GOAL.md.

---

## Riflettere su PERFORMANCE-OPTIONS

Leggi @design/roadmap/PERFORMANCE-OPTIONS.md e @evals/roadmap/recipe-app/results/ROADMAP-CC-3/PERF-SUGGESTIONS.md . Vorrei discutere del suggerimento S1 "Scrivere meno prosa". Sono d'accordo sul mettere in campo questo fix. Se prendo la roadmap di CC-3, la tabella dei Themes di Now, di Later e out-of-scope vanno bene, mentre le altre sezioni come ordering criteria, assumptions, cross functional concerns sono molto lunghe, lì forse si può ridurre qualcosa. Non mi è chiaro come poterlo fare però.

Sei d'accordo con il mio assesment? Mi suggerisci una strategia per attuare la riduzione?
