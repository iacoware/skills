# Prezzamento del rumore — `eval-noise`

Cattura la discussione del 2026-09-01. Compagno di `ROADMAP-LOG-REFACTORING.md`: il suo passo 1
(CC-6 prima del cambio log) è il lancio su cui questo metro si tara la prima volta.

## Problema

Ogni run CC ha girato su una versione diversa della skill: i delta tra run (68% CC-4 → 87% CC-5)
vengono letti come effetto dei fix, ma la varianza run-su-run a versione **ferma** non è mai stata
misurata — n=1 per versione. Senza quel prezzo, un futuro confronto (es. CC-7 col roadmap-log
contro la baseline) non distingue regressione da dado.

CC-2..5 non sono una stima del rumore ma un tetto: parte della loro divergenza è effetto dei fix
(la sparizione del tema `foto` in CC-4 è pre-`779bf17`). Servono run gemelli: stesso commit, stesso
`run.prompt.md`, stesso modello ed effort.

## Decisione

Tre run sulla stessa HEAD — un principale più due satelliti — e un comparatore di mappe che produce
una **tabella di accordo per asse**, non «una varianza»: con n=3 la domanda a cui si risponde è
binaria (praticamente deterministico vs balla), e tre run danno il caso «due concordano, uno
diverge», che con due è indistinguibile da «balla sempre».

Il comparatore non è usa-e-getta: è lo stesso strumento con cui si confronterà CC-7 contro la
baseline sugli stessi assi. Il prezzamento è solo il suo primo uso.

## La pipeline

1. **Lancio** — A, B, C in parallelo (~13 min wall-clock, costo generazione CC-5 come riferimento).
2. **Estrazione deterministica** — parse delle tabelle di ogni mappa in JSON normalizzato: temi,
   verdetti di boundary, righe NOW col record completo (titolo, tema, kind, size, archi di
   dipendenza), OUT-OF-SCOPE.
3. **Match meccanico** — stringhe identiche e record coincidenti sui campi strutturati si accoppiano
   senza modello. Sui run gemelli fa più lavoro di quanto CC-2..5 suggeriscano (`ricerca` e
   `condivisione` sono identici perfino cross-versione), ma non è il pilastro: il disegno regge
   anche a match esatto zero.
4. **Allineamento via modello sul residuo** — domande binarie sul record intero, non solo sul
   titolo; output vincolato: coppia allineata, oppure «non allineabile». I casi che non si
   allineano — un tema senza controparte, una riga che mappa su due — **non sono errore dello
   strumento: sono la misura** (compression, granularità che balla).
5. **Aritmetica** — tabella di accordo per asse (temi, verdetti, righe, archi di dipendenza,
   out-of-scope), ogni accoppiamento con la colonna di provenienza: meccanico / giudicato dal
   modello / non allineabile.
6. **Resa** — sopra le tre coppie, una sintesi: inventario per run (quanto ha prodotto ciascuno,
   prima di ogni confronto) e accordo per coppia come `accoppiati / confrontabili`. Sotto ogni
   tabella, un blocco per asse nello stesso ordine, con i gruppi elencati uno a uno — accoppiati,
   divergenti, solo-X, non confrontabili — e l'invariante che il numero di bullet di un gruppo è la
   sua cella in tabella. Nessun giudizio nella sintesi: solo aritmetica, la lettura la fa chi legge.

Perché l'estrazione invece del confronto whole-doc: copertura garantita per costruzione (ogni riga
entra perché ce la mette il codice, il modello non può saltarla); separazione tra giudizio e misura
(il modello fornisce corrispondenze puntuali ispezionabili, i numeri li fa il codice); forma del
compito (micro-domanda binaria = affidabile, diff esaustivo di tre documenti = no); riproducibilità
(rilanciando cambiano al più i pochi verdetti di allineamento, visibili uno a uno e stabilizzabili
a maggioranza). **Non è una review-lite**: misura accordo tra run, non qualità contro le regole —
se giudicasse chi ha ragione, ricontaminerebbe varianza del generatore e del giudice.

## Infrastruttura

Tutti pezzi nuovi in slot esistenti, nessuna infrastruttura nuova:

- **Naming** — satelliti come sibling con suffisso: `ROADMAP-CC-6B`, `ROADMAP-CC-6C`.
  `nextRunDir()` numera con `^ROADMAP-CC-(\d+)$` (`run_cycle.ts:53`): i suffissi non matchano,
  la numerazione non si sposta, zero modifiche. Scartata la sottocartella `CC-6/noise/`: rompe
  «one directory per run» e le assunzioni di `run-metrics`/`capture-run`.
- **I satelliti sono run di prima classe minus review** — kit completo (`PROMPT.md`,
  `TRANSCRIPT.jsonl`, `METRICS.md`); il loro `PROMPT.md` dichiara «satellite di CC-N,
  generation-only, non riceve mai `REVIEW.md`». `results/README.md` va aggiornato con questa
  regola (ha già l'inversa: un run con review non si riusa per generazione) e con le righe dei
  satelliti nella tabella dei run.
- **`NOISE.md` nella cartella del run principale** — stessa convenzione di `METRICS.md`: generato,
  mai scritto a mano, rigenerabile. Con una differenza dichiarata nell'header: non è derivato puro,
  contiene i giudizi di allineamento del modello — da qui la colonna di provenienza.
- **`make eval-noise RUN=<dir del principale>`** — genera i satelliti *mancanti*, poi l'analisi.
  Produce due run, non tre: il principale esiste già dal ciclo normale. Rilanciabile: se B e C ci
  sono, rigenera solo `NOISE.md` (utile ritoccando estrattore o prompt di allineamento).
- **Guardia sulla versione** — prima di generare satelliti, confronta il tree `skills/roadmap`
  registrato nel `PROMPT.md` del principale con quello corrente; se divergono, rifiuta. Satelliti
  su una skill diversa misurerebbero versione + rumore insieme: il vizio che il metro elimina.
- **Slot** — `prompts/noise.prompt.md` accanto a `run.prompt.md` (sessione headless guidata da
  `run_cycle.ts`, che già sa farlo); estrattore in `scripts/` accanto a `run_metrics.ts`, testato
  come gli altri (`test-evals`).

## Composizione con il ciclo

Ortogonale a `eval-cycle`, non un suo passo: il prezzamento è occasionale (costa 2 run), si fa
quando cambia qualcosa di strutturale o per ritarare il metro.

```
make eval-run              # → ROADMAP-CC-6
make eval-noise RUN=evals/roadmap/recipe-app/results/ROADMAP-CC-6   # → 6B, 6C, NOISE.md
make eval-review RUN=...   # review del solo principale
```

`eval-noise` e `eval-review` sono indipendenti (i satelliti non toccano il principale): ordine
libero, anche in parallelo. L'eventuale zucchero `eval-cycle NOISE=1` si aggiunge dopo, se serve.

Doppio uso del primo lancio: A/B/C **sono** CC-6 — review completa sul solo principale (che testa i
4 commit pendenti da CC-5), satelliti come materiale di prezzamento. Un lancio serve ciclo e
taratura insieme.

## Dipendenza dal roadmap-log

Il primo prezzamento avviene prima del cambio log (passo 1 dell'altro documento): l'estrattore
legge i verdetti dalla sezione `Theme boundaries` di `roadmap.md`. Quando il log atterra,
l'adattamento sta **tutto nello script di estrazione**, più una riga di inventario nel report che
dichiara la fonte dei verdetti — `noise.prompt.md` resta intatto: riceve
record dal JSON normalizzato e non sa da quale file i verdetti arrivino. Il JSON è l'interfaccia
stabile; un cambio di formato dei documenti che arrivasse fino al prompt vorrebbe dire che il
taglio a due stadi è sbagliato.

L'aggiornamento dell'estrattore non è «leggi un file diverso», e ha due sottigliezze:

1. **Il log è append-only**: l'estrazione dei verdetti è un fold del giornale — per ogni coppia di
   temi vince l'entry più recente — non un grep di sezione.
2. **Doppio formato nello stesso confronto**: proprio CC-7 vs baseline — il confronto per cui il
   metro nasce — ha la baseline coi verdetti in `roadmap.md` e CC-7 in `.roadmap/log.md`.
   L'estrattore riconosce il formato per run (la sezione c'è? il log c'è?) e normalizza entrambi
   nello stesso JSON; da lì in giù nulla si accorge del cambio.

Senza questo adattamento, l'asse «verdetti» non fallisce: esce vuoto, e vuoto = vuoto conta come
accordo — si svuota in silenzio proprio sul confronto per cui il metro è stato costruito.
