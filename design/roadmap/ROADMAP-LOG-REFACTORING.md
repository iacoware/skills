# Refactoring — introduzione del roadmap-log

Cattura la discussione del 2026-09-01. Sostituisce la voce «roadmap-decisions» di `TODO.md`.

## Problema

La sezione `Theme boundaries` di `roadmap.md` serve al modello più che all'umano: è l'atto di
scriverla che contrasta la theme compression (osservato: senza, le decisioni peggiorano). Per
l'umano è materiale da appendice — contesta guardando la tabella Themes, non le boundary.

Spostarla in fondo al documento non basta: ordine di scrittura = ordine del documento, quindi in
fondo verrebbe scritta a massimo costo affondato (NOW, validators, OUT-OF-SCOPE già committati) e
degraderebbe da strumento di decisione a razionalizzazione a posteriori.

## Decisione

Un file separato accanto alla mappa — proposta: `.roadmap/log.md` — ad uso esclusivo del modello.
`roadmap.md` resta il documento per l'umano e perde la sezione `Theme boundaries`; il log riceve i
verdetti, scritti **prima** della tabella Themes. Nessuna copia dei verdetti resta nella mappa: due
copie della stessa decisione sono drift garantito.

Chi legge la mappa contesta dalla tabella Themes (tema mancante, compressione); se qualcosa non
torna, il log è lì da aprire. Non si perde contestabilità.

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

## Modifiche

Lato skill:

- `skills/roadmap/assets/roadmap-template.md` — rimuovere la sezione `Theme boundaries` (righe
  19–24).
- Template o spec del log — formato entry, data, append-only. Da decidere se asset separato in
  `assets/` o spec inline in `drawing-the-map.md` (propendo per l'inline: il formato è tre campi).
- `skills/roadmap/references/drawing-the-map.md:47` — «Record each verdict under the `Theme
  boundaries` label» diventa: verdetti registrati nel log, prima di scrivere la tabella Themes
  (regole 1 e 3).
- `skills/roadmap/SKILL.md` — il layout `.roadmap/` (riga ~14) nomina il log; le letture d'ingresso
  di una sessione (riga ~45) e la porta Operations lo includono (regole 2 e 4).

Lato eval (nello stesso cambio, o il reviewer non trova i verdetti):

- `evals/roadmap/EVALUATION-RULES.md` R-008 — «every boundary carries a recorded split or merge
  verdict»: il verdetto ora sta nel log; la regola dice dove guardare.
- `evals/roadmap/recipe-app/EVALUATION-BRIEF.md` A10 — «what is owed is the recorded verdict»:
  idem.
- Candidate regole nuove (o estensioni): log scritto prima della tabella Themes (si legge dal
  transcript); log riletto in un run di revisione; nessun verdetto duplicato nella mappa.
- `evals/roadmap/scripts/extract_map.ts` — l'asse «verdetti» di `eval-noise` oggi legge la sezione
  `Theme boundaries`: col log l'estrazione diventa un fold del giornale append-only (per coppia
  vince l'entry più recente) e riconosce il formato per run, perché proprio CC-7 vs baseline
  confronta una mappa vecchio formato con una nuova. Il ragionamento sta in `EVAL-NOISE.md`,
  «Dipendenza dal roadmap-log»; tutto l'adattamento sta nell'estrattore, `noise.prompt.md` non si
  tocca. Senza, l'asse non fallisce: si svuota, e il report lo dichiara solo come «accordo per
  assenza».

## Verifica

Rischi da coprire, e dove si leggono:

- (a) log sciatto — un file «che nessun umano legge» invita sciatteria: transcript + log del run.
- (b) log non riletto in revisione — l'unico rischio che l'eval attuale non vede, perché i run CC
  esercitano solo Drawing e il tally esclude R-027–R-031: serve uno scenario di revisione.
- (c) mappa scritta prima del log: transcript.

Sequenza:

1. **CC-6 su HEAD attuale, prima di toccare la skill.** Da CC-5 (tree `0913e60`) sono atterrati 4
   commit non testati (`f569dce`…`d8bc79d`); impacchettarli col cambio log renderebbe un'eventuale
   regressione non attribuibile.
2. **Il cambio log atterra da solo**, tutte le modifiche sopra in un intervallo pulito.
3. **CC-7 (Drawing).** Giudicato sui check mirati — R-008 e compressione temi, transcript per (a) e
   (c) — **non sul pass rate aggregato**: con n=1 per versione e varianza ignota, un delta di ±3
   regole sull'aggregato non è leggibile.
4. **Scenario di revisione prima di dichiarare il cambio promosso.** Gli scenari 1–3 di
   `SCENARIOS.md` esistono e non sono mai girati: fixture = mappa + log esistenti, operazione che
   tenta un verdetto registrato; check = l'ha riletto, il verdetto è sopravvissuto o è stato
   superato con un'entry nuova. Copre (b).

Reversibilità: il cambio è testo (template + skill + due voci eval); se CC-7 puzza, revert e si è
perso un ciclo di eval.

## Fuori da questo documento

Il prezzamento del rumore run-su-run è un tema a parte e il suo ragionamento sta in
`EVAL-NOISE.md` (satelliti CC-6B/6C sulla stessa versione, `make eval-noise`); qui conta solo che
il giudizio su CC-7 non si appoggi all'aggregato finché quel prezzo non è noto.

## Open questions

- Perimetro del log al primo colpo: solo verdetti di boundary, o tutte le decisioni del modello
  (il vecchio appunto «roadmap-decisions» in `TODO.md` immaginava anche gli Ordering criteria, poi
  rimossi dal formato)? Partire stretto è reversibile; partire largo cambia formato, regole eval e
  costo di rilettura.
- Nome e posizione del file: `.roadmap/log.md` è la proposta, non una decisione.
