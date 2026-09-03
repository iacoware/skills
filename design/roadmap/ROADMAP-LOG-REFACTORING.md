# Refactoring — introduzione del roadmap-log

Cattura la discussione del 2026-09-01, rivista il 2026-09-03 contro lo stato del repo. Sostituisce
la voce «roadmap-decisions» di `TODO.md`.

## Problema

La sezione `Theme boundaries` di `roadmap.md` serve al modello più che all'umano: è l'atto di
scriverla che contrasta la theme compression (osservato: senza, le decisioni peggiorano). Per
l'umano è materiale da appendice — contesta guardando la tabella Themes, non le boundary.

Spostarla in fondo al documento non basta: ordine di scrittura = ordine del documento, quindi in
fondo verrebbe scritta a massimo costo affondato (NOW, validators, OUT-OF-SCOPE già committati) e
degraderebbe da strumento di decisione a razionalizzazione a posteriori.

## Decisione

Un file separato accanto alla mappa — `.roadmap/log.md` — ad uso esclusivo del modello.
`roadmap.md` resta il documento per l'umano e perde la sezione `Theme boundaries`; il log riceve i
verdetti, scritti **prima** della tabella Themes. Nessuna copia dei verdetti resta nella mappa: due
copie della stessa decisione sono drift garantito.

Chi legge la mappa contesta dalla tabella Themes (tema mancante, compressione); se qualcosa non
torna, il log è lì da aprire. Non si perde contestabilità.

Il log non entra mai nel report di chiusura (le quattro parti di R-035) e il validator non lo legge:
è un file in più in `.roadmap/`, che il validator ignora già oggi (legge solo `roadmap.md`,
`slices/`, `archive/`), e giudicarne il contenuto sarebbe il validator che grada il giudizio, che
`ROADMAP-GOAL.md` vieta.

## Le quattro regole

Senza queste, il log introduce problemi nuovi invece di risolverne:

1. **Ordine imposto.** La skill dice esplicitamente: verdetti nel log, poi la tabella Themes, poi il
   resto della mappa. Se il modello scrive la mappa e poi verbalizza, si torna alla
   razionalizzazione — peggio di oggi, perché nemmeno adiacente.
2. **Autorità.** La mappa vince, il log è memoria, non contratto. Append-only con data: ogni
   operazione che tocca i temi appende (anche i ripensamenti — non si riscrive un verdetto, se ne
   appende uno nuovo che lo supera).
3. **Disciplina di dimensione.** Formato stretto per entry: coppia, verdetto `split`/`merge`, il
   fatto che ha deciso; argomento oltre al fatto ammesso (nel log ha senso, nella mappa no) ma con
   tetto per entry. Il log viene riletto a ogni operazione: cresce nel contesto.
4. **Rilettura garantita.** Le sessioni sulle operazioni (porta *Operations on the map*) leggono il
   log all'ingresso. Oggi i verdetti viaggiano dentro `roadmap.md` che viene letto comunque; questa
   garanzia gratuita va sostituita con un obbligo scritto, o i verdetti evaporano in silenzio.

## Formato

Spec inline in `drawing-the-map.md` (tre campi, non vale un asset). Un H2 per sessione, con data e
porta; sotto, un bullet per decisione nel formato che il bullet di `Theme boundaries` ha già oggi —
così `BOUNDARY_PATTERN` di `extract_map.ts` si riusa tal quale:

```markdown
## 2026-09-03 — Drawing

- `cattura` / `ricerca` — **split.** La ricerca si rinvia intera senza invalidare l'evidenza della
  cattura.
  Argomento: [facoltativo, al massimo due righe].
```

Regole di lettura e scrittura:

- **Append in coda, sempre.** Una sessione apre il proprio H2 e scrive sotto; non tocca gli H2
  precedenti. Su una coppia già decisa si appende un bullet nuovo: il fold è «per coppia vince
  l'entry più in basso».
- **La coppia è ordinata come nella tabella Themes** (temi adiacenti), che è quel che rende
  meccanico il fold e l'estrazione.
- **Un redraw azzera il log.** I temi si ridisegnano da zero (`drawing-the-map.md`, *What carries*)
  e i verdetti su temi morti sono peso morto riletto a ogni operazione; coerente con «no history of
  superseded goals is kept — git has the rest». Il nuovo log parte con il solo H2 del redraw.
- **Tetto per entry**: fatto in una riga, argomento in due. È l'unica disciplina di dimensione che
  serve finché il log tiene un solo tipo di decisione; se ne entrano altri (sotto), il tetto va
  ripensato per tipo.

Il formato è agnostico rispetto al tipo di decisione — H2 per sessione, bullet «soggetto — verdetto
— fatto» — di proposito: un secondo tipo entra come bullet con un soggetto diverso, non come
formato nuovo.

## Modifiche

Lato skill:

- `skills/roadmap/assets/roadmap-template.md` — rimuovere il blocco `Theme boundaries` (righe
  19–24).
- `skills/roadmap/references/drawing-the-map.md:51` — «Record each verdict under the `Theme
  boundaries` label» diventa: verdetti registrati nel log, prima di scrivere la tabella Themes
  (regole 1 e 3), più la spec del formato qui sopra. Il paragrafo sulla precedenza dello split test
  (`6f3ba7b`, righe 47–49) resta dov'è: decide il verdetto, non dove va scritto.
- `skills/roadmap/SKILL.md` — il layout `.roadmap/` (riga 14) nomina il log; le letture d'ingresso
  di una sessione (righe 43–48) lo includono (regola 4); *Operations on the map* dice che
  un'operazione che tocca i temi (reshaping: split/merge; admission in un tema nuovo) appende
  (regola 2); *Close the session* dice che il log non è fra le quattro parti del report.
- `skills/roadmap/scripts/validate_roadmap.ts` — **nessuna modifica**: ignora i file che non conosce,
  e deve continuare a farlo.

Lato eval (nello stesso cambio, o il reviewer non trova i verdetti):

- `evals/roadmap/EVALUATION-RULES.md` R-008 — «every boundary carries a recorded split or merge
  verdict»: il verdetto ora sta in `log.md`; la regola dice dove guardare, e che il fold vale (una
  coppia con due entry è decisa dall'ultima).
- `evals/roadmap/recipe-app/EVALUATION-BRIEF.md` A10 — «what is owed is the recorded verdict»:
  idem.
- Regole nuove, una per rischio della sezione *Verifica*: log scritto prima della tabella Themes
  (transcript: l'ordine dei `Write`); nessun verdetto duplicato in `roadmap.md`; log riletto
  all'ingresso in un run di revisione (transcript: un `Read` di `log.md` prima del blocco
  proposto). Vanno sotto *Draw the map* le prime due, sotto *Revising an existing map* la terza.
- `evals/roadmap/scripts/extract_map.ts` (più una riga di inventario in `noise_report.ts`) —
  `readMapExtract` legge solo `roadmap.md`: deve leggere anche `log.md` quando c'è. L'asse «verdetti» diventa un fold del giornale (per coppia vince
  l'entry più in basso) e riconosce il formato per run, perché proprio CC-7 vs baseline confronta
  una mappa vecchio formato con una nuova: sezione in `roadmap.md` → vecchio; `log.md` presente →
  nuovo; entrambi → nuovo, e il report lo segnala come duplicato. Il ragionamento sta in
  `EVAL-NOISE.md`, «Dipendenza dal roadmap-log»; tutto l'adattamento sta nell'estrattore,
  `noise.prompt.md` non si tocca. Senza, l'asse non fallisce: si svuota, e il report lo dichiara
  solo come «accordo per assenza».
- `evals/roadmap/recipe-app/fixtures/mid-flight/` — **oggi non ha verdetti da nessuna parte**
  (nessuna sezione `Theme boundaries`: congelato il 2026-08-20 con `aaa3080`, sei giorni prima
  che il verdetto di tema entrasse nel template con `ff63c96` e `779bf17`). Lo scenario di
  revisione al passo 4 presuppone «mappa + log esistenti»: serve un `log.md` nel fixture con i
  quattro verdetti fra i cinque temi (`cattura/ricerca`, `ricerca/accesso`,
  `accesso/condivisione`, `condivisione/foto`), datato col congelamento. È un fixture che si muove
  perché lo stato che rappresenta si muove, il caso che `fixtures/README.md` ammette; i verdetti
  sono scritti a mano dove il resto del fixture è «entirely the run's» — il run d'origine precede
  il verdetto di tema, nessun transcript li porta — e il README lo dice. Stesso vuoto in `redrawn/` e in `reference-roadmap/`: il primo si
  aggiorna solo se lo scenario 3 torna eseguibile; l'oracolo non ha bisogno del log, perché R-008
  giudica la presenza e la lettura dei verdetti del run, non un diff contro l'oracolo.
- `evals/roadmap/recipe-app/SCENARIOS.md` scenario 1 — aggiungere il check (b): la sessione ha letto
  `log.md` all'ingresso, e il verdetto `ricerca`/`condivisione` è sopravvissuto intatto o è stato
  superato da un'entry nuova; nell'elenco regole della carta entra la regola nuova sulla rilettura.

## Verifica

Rischi da coprire, e dove si leggono:

- (a) log sciatto — un file «che nessun umano legge» invita sciatteria: transcript + log del run.
- (b) log non riletto in revisione — l'unico rischio che l'eval attuale non vede, perché i run CC
  esercitano solo Drawing e il tally esclude R-027–R-031: serve uno scenario di revisione.
- (c) mappa scritta prima del log: transcript.

Sequenza, con lo stato al 2026-09-03:

1. **CC-6 su HEAD prima di toccare la skill — fatto** (`209c83a`: run su `fb29812`, tree
   `0d47a59`, gemelli 6B/6C, `NOISE.md`). I 4 commit non testati (`f569dce`…`d8bc79d`) sono ora
   attribuibili: R-017 è passata da rossa a verde, R-015 resta rossa (C1 in 6 run su 6).
   **Il prezzo del rumore è noto, e sull'asse verdetti è alto**: accordo 1/6, 4/5, 0/4 fra i tre
   gemelli, contro 11/12, 11/12, 12/12 sulle righe. Non è sciatteria sui verdetti: l'asse dipende
   dall'insieme e dall'ordine dei temi (5–6 temi, accoppiati 5/7, 5/6, 4/7), e un tema in più o in
   altra posizione cambia le adiacenze. Conseguenza per CC-7: l'asse verdetti di `NOISE.md` non
   distingue il cambio log dal dado, e non va usato per giudicarlo.
2. **Il cambio log atterra da solo — fatto il 2026-09-03.** L'intervallo non è pulito: `6f3ba7b`
   (precedenza dello split test, stessa sezione *Themes* di `drawing-the-map.md`) è atterrato dopo
   CC-6 senza run e viaggia in CC-7 senza dichiarazione a parte. Le due modifiche si distinguono nel
   contenuto: la precedenza dello split si vede in un `merge` dove lo split tiene (il caso CC-6B), il
   log in presenza, posizione e ordine dei `Write`. Se R-008 o R-009 peggiorano, il revert è di
   entrambi.
3. **CC-7 (Drawing).** Giudicato sui check mirati — R-008 (presenza e fold dei verdetti nel log),
   R-009, numero di temi contro 6/6/5, transcript per (a) e (c) — **non sul pass rate aggregato**:
   con n=1 per versione, un delta di ±3 regole sull'aggregato non è leggibile, e ora si sa anche
   perché (righe divergenti sui campi 4–5 su 11 a versione ferma).
4. **Scenario di revisione prima di dichiarare il cambio promosso.** Lo scenario 1 di
   `SCENARIOS.md` è quello giusto: mai girato, fixture `mid-flight` col log aggiunto sopra, la
   promozione tocca `ricerca` e sfiora `condivisione`. Lo scenario 2 chiede e si ferma senza
   scrivere; il 3 è marcato *do not run*. Copre (b).

Reversibilità: il cambio è testo (template + skill + due voci eval + un fixture); se CC-7 puzza,
revert e si è perso un ciclo di eval.

## Fuori da questo documento

Il prezzamento del rumore run-su-run è un tema a parte e il suo ragionamento sta in
`EVAL-NOISE.md` (satelliti CC-6B/6C sulla stessa versione, `make eval-noise`); qui conta solo che
il giudizio su CC-7 non si appoggi all'aggregato, e ora nemmeno all'asse verdetti.

## Altri decision-log: candidati

Il perimetro del primo colpo resta stretto — solo verdetti di boundary — per la ragione del
documento originale: partire stretto è reversibile. Ma la domanda «quali altre decisioni del modello
migliorano se scritte prima della mappa» ha risposte con evidenza, e il formato sopra è fatto per
riceverle un tipo alla volta, ciascuno col suo run. Il criterio di ammissione è lo stesso dei
verdetti: una decisione che la skill già impone, che oggi resta nel ragionamento e che i run
mostrano presa male o non presa. In ordine di evidenza:

1. **Le uscite dello sweep** (`drawing-the-map.md`, *What the map reports about its input*). Per
   ogni conflitto e ogni scelta non decisa: sorgente, lato preso, uscita (`Assumptions` / `Open
   questions` / spike). **R-015 è rossa in 6 run su 6** per C1, e `8eb3a71` che la prendeva di mira
   non ha attecchito; il tell «taken in a row and nowhere else» è oggi verificabile solo rifacendo
   lo sweep. Stesso meccanismo dei verdetti: lo sweep «is what has to be thought before the section
   is written», e niente obbliga a pensarlo. Scritto nel log prima di `Assumptions`, lo sweep
   avviene, e il lato preso in un bullet senza riga nella mappa diventa un diff (entry nel log senza
   uscita). Costo: 5–10 entry per disegno. Candidato più forte.
2. **Il test di sostituzione sugli archi** (*Hard dependencies*): per coppia candidata, `edge` /
   `order`, e lo stand-in nominato oppure il deliverable che nessun fixture fornisce. R-017 rossa in
   5 run su 6 con quattro commit a bersaglio, verde solo su CC-6; secondo asse più rumoroso
   (7/12, 8/8, 8/13). È la decisione che reshaping e reorder rileggono per costruzione: un riordino
   è esattamente ciò che l'arco protegge. Costo: il più alto — le coppie sono molte; il perimetro va
   ristretto a quelle su cui la regola pone la domanda (dipendente il cui `Includes` o
   `Verification` tocca ciò che un'altra riga `NOW` consegna).
3. **Ranking dichiarato e deroghe** (*Ordering for learning*): la riga «the map declares its own
   ranking» non ha oggi nessun posto dove il ranking sia detto, e ogni deroga a breadth-before-depth
   deve essere una delle quattro. R-012 rossa in 2 run su 4 registrati, nessun commit a bersaglio.
   `Ordering criteria` fu rimosso dalla mappa perché cerimonia per l'umano; il log è dove quella
   voce del `TODO.md` stava andando. Costo: una riga per il ranking, una per deroga. Attenzione:
   R-012 «read from the rows, never from a statement about them» resta vero — il log serve alla
   decisione, non al reviewer.
4. **Lo sweep cross-funzionale**: cinque dimensioni, una riga ciascuna, «nulla» o la concern
   pubblicata. «The absence is information», ma un'assenza è indistinguibile da uno sweep non
   fatto. R-022 rossa in 3 run su 6, verde negli ultimi due. Costo quasi zero; evidenza debole.
5. **La rilettura di `LATER` e delle righe aperte in un redraw** (*What carries*): ogni candidato
   riceve un verdetto — promosso, tenuto, ucciso — e oggi gli uccisi spariscono senza traccia.
   Nessuno scenario lo esercita (il fixture `redrawn/` è l'output di un redraw, non il suo test).
   Ultimo per evidenza.

Cosa **non** entra: il verdetto slice/spike all'admission (lo porta `kind`), la domanda di coverage
(R-031 vive nel transcript ed è «usually one line»), le retirement (git). Tutte «field nobody
re-reads».

Vincolo che cresce con ogni tipo ammesso: la regola 3. Il log è riletto a ogni operazione; a due
tipi si sta sotto le venti entry, al terzo serve un tetto complessivo o un fold anche in scrittura
(una sessione riscrive le entry superate della propria sezione, mai delle altre).
