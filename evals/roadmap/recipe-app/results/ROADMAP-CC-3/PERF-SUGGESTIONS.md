# Come rendere più veloce il disegno

Letto da questo run e da `ROADMAP-CC-2`, con i numeri di [`METRICS.md`](METRICS.md) accanto. In
italiano come il resto della directory; l'analisi completa, con i rischi di qualità riga per riga e
le opzioni scartate, sta in [`design/roadmap/PERFORMANCE-OPTIONS.md`](../../../../../design/roadmap/PERFORMANCE-OPTIONS.md).

Niente qui è stato implementato, e nessuna di queste misure è stata verificata con un run.

## Il fatto da cui discende tutto

**La sessione è lenta solo perché scrive tanto.**

Il modello produce circa 72 token al secondo, e il tempo totale è esattamente i token diviso 72.
Tutto il resto non conta:

- eseguire comandi — ogni `cat`, ogni `sed`, l'heredoc che scrive dodici file, il validator:
  **due secondi** su 13 minuti (`METRICS.md`, riga *Tool, sub-agent e I/O*);
- leggere — sorgenti, references, template, sorgente del validator: **23 secondi su 803**;
- l'input in generale non costa wall-clock: la cache read cresce da 29.572 a 134.291 token e non
  compare mai in una durata.

Quindi ci sono **solo due modi** per andare più veloci: scrivere di meno, oppure scrivere più cose in
parallelo. Non esiste un terzo modo.

Dove va il tempo, da `METRICS.md`:

| Fase | CC-3 | CC-2 |
|---|---|---|
| Thinking | **8m 14s · 61%** | 5m 39s · 46% |
| Scrittura dei documenti | **4m 24s · 33%** | 5m 46s · 47% |
| Tutto il resto | 46s · 6% | 57s · 7% |

## 1. Far scrivere meno prosa

L'intervento migliore: il più semplice, il più sicuro, il più efficace.

La mappa esce lunga il doppio o il triplo del reference — `roadmap.md` 16.786 caratteri contro 8.901,
e 2.665 caratteri per riga contro 1.167. Non è più contenuto: è la stessa cosa detta più lunga, e
spesso ripetuta. La `Verification` di `S4` ha cinque frasi, e due ripetono cose che stanno già scritte
altrove nella mappa — lo scoping, che appartiene a `Cross-functional concerns`, e la latenza, che
appartiene a `S2`.

Il motivo è che i template dicono a cosa serve ogni sezione e non quanto deve essere lunga, e l'unico
metro che la sessione ha è la prosa densa dello skill stesso. Che imita.

Si dice la forma, non la misura: *`Verification` è una scena sola che qualcuno può guardare*. Mai un
numero di caratteri — sarebbe un budget di token, e `ROADMAP-GOAL.md` lo vieta.

**Guadagno atteso: circa 80 secondi**, più il pensiero che serviva a produrli. E la mappa torna a
stare su uno schermo, che è quello che `ROADMAP-GOAL.md` chiede e che oggi non succede.

**Cosa cambia:** i due template, e una riga in `references/drawing-the-map.md` per le sezioni di
mappa.

**Rischio:** tagliare troppo e perdere evidenza. Lo intercetta R-020 — ogni affermazione del
`Learning target` deve avere un'osservazione in `Verification` — che è la regola da tenere d'occhio,
perché la pressione a tagliare cade esattamente lì.

## 2. Far scrivere gli 11 documenti in parallelo

Una volta decisi temi, register e dipendenze, i documenti non si parlano più fra loro: si possono
scrivere tutti insieme invece che uno dopo l'altro. Oggi sono circa 4 minuti in fila; in parallelo
diventa il tempo del più lento, meno di un minuto.

**Guadagno atteso: 2-3 minuti.** In più i documenti non entrano mai nella finestra principale, che è
l'obiettivo secondario.

**La condizione:** ogni subagent riceve tutto quello che è già stato deciso — non solo la sua riga, ma
l'elenco delle altre righe con il loro esito in una frase, le dipendenze in entrambe le direzioni, e
le regole comuni. Altrimenti due documenti si contendono lo stesso pezzo di lavoro, oppure uno scrive
una dipendenza che non esiste. Torna indietro solo *il file è scritto*, mai il documento.

**Nessun round trip in più con l'autore:** i subagent non gli parlano mai. Quello che un subagent non
riesce a decidere torna come una riga di testo, e la sessione la mette nelle `Open questions` di
quella riga — un'uscita che il formato ha già.

**Cosa cambia:** un paragrafo in `SKILL.md` e il contratto di input in
`references/drawing-the-map.md`.

**Rischio:** la coerenza fra righe. Lo intercettano R-024 (un solo proprietario per comportamento),
R-017 (archi duri mancanti o di troppo), R-009 (il first validator copre la promessa *intera*) e,
nel brief, H3 — la cascata di estrazione divisa su tre righe che devono concordare sull'ordine.

## 3. Provare a farla pensare meno

Il pensiero è **8 minuti su 13, il 61%**. È il numero più grosso, e l'unico che il transcript non
sa scomporre.

C'è un indizio che vale la pena seguire: la sessione ha scritto i primi 5 documenti con quasi 10.000
token di ragionamento e gli ultimi 6 con **zero**, e `REVIEW.md` non trova gli ultimi 6 peggiori dei
primi 5 — tre delle sette violazioni stanno nel primo gruppo, una nel secondo. Non è una prova, ma
non c'è niente che giustifichi quei 10.000 token.

Il modo più economico per scoprirlo **non è cambiare lo skill**: è fare un run con l'effort più basso
e lo skill identico. Costa due chiamate e dice se quegli 8 minuti stanno comprando qualcosa.
`REVIEW-WORKFLOW.md` fissa modello ed effort nella sessione, quindi è una variabile dell'eval e non
del payload — e cambiarla sposta la linea di base contro cui ogni run precedente è stato misurato.

## Cosa non fare

**Non far leggere le sorgenti a un subagent che riassume.** Sembra un risparmio e non lo è: leggere
tutte e quattro le sorgenti costa **6 secondi**. E `REVIEW.md` mostra che questa mappa ha già perso
React Query (H5) e ha già sbagliato una citazione (R-015 sulla riga `S4, ricerca`) *avendo le sorgenti
intere sotto gli occhi*. Un riassunto peggiora esattamente quei due errori per guadagnare sei secondi.

**Non ridurre la documentazione caricata all'inizio per andare più veloci.** Tutta la lettura del run
sono 23 secondi su 803. È un costo di contesto, non di tempo: vale la pena farlo per i token, mai per
i secondi.

**Non rimandare i documenti delle righe lontane, e non farli più magri.** `ROADMAP-GOAL.md` rifiuta il
gradiente di dettaglio dentro `NOW` per nome: quello che cambia fra vicino e lontano è la fiducia, e
la fiducia ha già `Open questions` e `readiness`.

## Cosa costa verificarlo

Una modifica per volta: cambiarne due insieme compra una misura che non attribuisce niente.

| | run | review | chiamate |
|---|---|---|---|
| Prosa più corta, per farsi una domanda | 1 | 1 | **2** |
| Prosa più corta, per avere un verdetto | 2 | 2 | **4** |
| Subagent in parallelo, per farsi una domanda | 1 | 1 | **2** |
| Subagent in parallelo, per avere un verdetto | 2 | 2 | **4** |
| Effort più basso, per farsi una domanda | 1 | 1 | **2** |

Gratis, e da fare comunque: `wc -c` della mappa nuova contro CC-2 e CC-3, `make validate-roadmap`, e
la riga *Tool, sub-agent e I/O* delle METRICS — oggi due secondi, ed è lì che si vedrà se il parallelo
sta davvero lavorando.

`AGENTS.md` richiede il conteggio esatto e l'autorizzazione esplicita prima di mandare una sola
richiesta al provider.

## In sintesi

Prendendo 1 e 2: **da 13 minuti a circa 9**. Sotto i 9 ci si arriva solo intervenendo sul pensiero,
cioè il punto 3.
