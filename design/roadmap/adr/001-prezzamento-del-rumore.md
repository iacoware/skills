# ADR 001 — Prezzamento del rumore con run gemelli e comparatore per asse

Data: 2026-09-01. Stato: accettata, implementata (`make eval-noise`, `extract_map.ts`,
`noise_report.ts`, `noise.prompt.md`). Regola operativa dei satelliti in
[`evals/roadmap/recipe-app/results/README.md`](../../../evals/roadmap/recipe-app/results/README.md).

## Contesto

Ogni run CC girava su una versione diversa della skill: i delta tra run (68% CC-4 → 87% CC-5)
venivano letti come effetto dei fix, ma la varianza run-su-run a versione **ferma** non era mai
stata misurata — n=1 per versione. Senza quel prezzo un confronto futuro non distingue regressione
da dado. CC-2..5 non sono una stima del rumore ma un tetto: parte della loro divergenza è effetto
dei fix.

## Decisione

Run gemelli — stesso commit, stesso prompt, stesso modello ed effort — e un comparatore che produce
una **tabella di accordo per asse** (temi, verdetti di boundary, righe NOW, archi di dipendenza,
out-of-scope), con la provenienza di ogni accoppiamento: meccanico, giudicato dal modello, non
allineabile.

## Razionale

**Tre run, non due.** Con n=3 la domanda è binaria (praticamente deterministico vs balla), e tre run
danno il caso «due concordano, uno diverge», che con due è indistinguibile da «balla sempre».

**Estrazione + micro-domande, non diff whole-doc.** Copertura garantita per costruzione: ogni riga
entra perché ce la mette il codice, il modello non può saltarla. Separazione tra giudizio e misura:
il modello fornisce corrispondenze puntuali ispezionabili, i numeri li fa il codice. Forma del
compito: una domanda binaria su un record intero è affidabile, il diff esaustivo di tre documenti
no. Riproducibilità: rilanciando cambiano al più i pochi verdetti di allineamento, visibili uno a
uno. I casi che non si allineano non sono errore dello strumento: **sono la misura**.

**Non è una review-lite.** Misura accordo tra run, non qualità contro le regole: se giudicasse chi
ha ragione, ricontaminerebbe varianza del generatore e del giudice.

**Satelliti come sibling `-B`/`-C`, non sottocartella.** La numerazione `^ROADMAP-CC-(\d+)$` non li
vede e non si sposta; una sottocartella romperebbe «one directory per run» e le assunzioni di
`run-metrics`/`capture-run`. Sono run di prima classe minus review: kit completo, mai `REVIEW.md`.

**Guardia sulla versione.** Satelliti su un tree di `skills/roadmap` diverso dal principale
misurerebbero versione + rumore insieme: il vizio che il metro elimina.

**Ortogonale a `eval-cycle`.** Il prezzamento costa due run ed è occasionale: si fa quando cambia
qualcosa di strutturale o per ritarare il metro, non a ogni ciclo.

## Conseguenze

Il JSON normalizzato dell'estrattore è l'interfaccia stabile: il passaggio dei verdetti da
`roadmap.md` a `.roadmap/log.md` è stato assorbito tutto lì (fold append-only del giornale, doppio
formato nello stesso confronto, colonna `verdictSource`) senza toccare il prompt di allineamento.
Un cambio di formato che arrivasse fino al prompt vorrebbe dire che il taglio a due stadi è
sbagliato.
