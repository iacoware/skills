# Miglioramenti — dopo `ROADMAP-CC-4`

Proposte, non implementazioni. Niente sotto `skills/` è stato toccato in questa sessione, e niente
sotto `evals/`.

## Dove cade ogni run nella storia della skill

| Run | Ancoraggio | `skills/roadmap` tree | Fonte |
|---|---|---|---|
| `manual-run-1` | `dcf783d` | `ed75429` | **inferito** — commit che aggiunge `results/manual-run-1/.roadmap`; il run non dichiara nulla |
| `ROADMAP-CC-2` | `666566d` | `eedf170` | dichiarato in `PROMPT.md` (ricostruito dal transcript) |
| `ROADMAP-CC-3` | `e27d419` | `028f3b4` | dichiarato in `PROMPT.md` (ricostruito dal transcript) |
| `ROADMAP-CC-4` | `d805196` | `2f1d0db` | dichiarato in `PROMPT.md` (ricostruito dal transcript) |

Quattro tree distinti: nessuna coppia di run mette alla prova la stessa skill. I commit dentro ogni
intervallo, tutti letti:

- `dcf783d..666566d` — `18968aa`, `524e180`, `676b580`, `666566d`. Il grosso è il refactoring S2/S3
  (`SKILL.md` diventa router a due porte, `drawing-the-map.md` si carica sulla sola `Drawing`);
  `524e180` legalizza il tag `goal` su una riga di `Assumptions`.
- `666566d..e27d419` — `f77bc61` (*Fix violation of R-17*), `e27d419` (C2: due test su una riga di
  `Assumptions`, e lo sweep dei conflitti anche dentro un singolo documento).
- `e27d419..d805196` — `2bf0a12` (ripara i due fix precedenti: terzo test sulle citazioni, e
  **dropped edge** come specchio di *published order*), `ff63c96` (verdetto di tema a una riga, con
  slot nel template), `d805196` (rimozione di `Ordering criteria` dal formato).
- `d805196..HEAD` — `779bf17` (*Catch theme compression where it leaves a trace*), `79f4a4a`
  (concern pubblicato solo dove una riga poteva fare altrimenti).

**Ancoraggio inferito solo per `manual-run-1`.** Il confine `dcf783d` è la data del commit che ne
aggiunge la mappa, non la versione che ha girato: se la skill fosse cambiata fra il run e il commit,
l'intervallo `dcf783d..666566d` conterrebbe un commit di troppo o uno di meno. Dove sotto ci fondo
qualcosa, è detto.

**I due commit dopo `d805196` non sono messi alla prova da nessun run.** `PROMPT.md` di CC-4 lo
dichiara già per `779bf17`. Vale anche per `79f4a4a`. Contarli come fix che non hanno preso sarebbe
leggere un fix mai testato.

## Che cosa ricorre

`ko` rosso, `ok` verde con la prova nel `REVIEW.md`, `·` non registrata dal run.

| Violazione | m-1 | CC-2 | CC-3 | CC-4 | Commit che l'ha presa di mira |
|---|:--:|:--:|:--:|:--:|---|
| **R-015 / C1** — il lato preso solo in un bullet di riga | ko | ko | ko | ko | nessuno |
| **H5** — React Query assente | ko | ko | ko | ko | nessuno (e nemmeno l'oracolo lo nomina) |
| **R-009** — first validator che copre metà promessa | ok | ko | ko | ko | `779bf17`, **non testato** |
| **R-008** — theme compression | ko | ko | · | ko | `ff63c96` (metà verdetti), `779bf17` **non testato** |
| **R-022** — `Includes` che decide ciò che è indeciso | ko | ko | · | ko | nessuno |
| **R-017 published order** | ko | ko | ok | ko | `f77bc61` |
| **R-017 false edge** (arco sostituibile) | ko | ko | ok | ok | `f77bc61` — **fix dimostrato** |
| **R-017 dropped edge** | · | · | ko | ko | `2bf0a12` |
| **R-020** — learning target doppio / claim non osservato | ko | ko | · | · | nessuno |
| **R-012** — ampiezza prima di profondità, e ranking | ok | ok | · | ko | nessuno (ma `d805196` toglie ciò che reggeva i verdi) |
| **R-035** — chiusura oltre le quattro parti | · | ok | ko | ko | nessuno |

Su `R-008`: `ff63c96` ha preso di mira la metà «ogni confine porta un verdetto» e quella metà **ha
preso** — CC-4 scrive cinque righe di verdetto, una per ogni confine disegnato. Quello che resta
rosso è la compressione stessa, che nessun commit prima di `d805196` tocca. Attribuzione letta dal
diff: il messaggio di `ff63c96` parla di perf, ma il diff sostituisce «Run both tests explicitly, and
record the verdict» con «on every boundary between adjacent themes» più lo slot nel template.

## 1. Regressioni

Una sola.

### 1.1 — `R-017`, *published order*: `S1 → S0` e `S3 → S1` tornano pubblicati

**Storia.** `f77bc61` — *Fix violation of R-17* — la prende di mira: **id nel messaggio del commit**.
Sta in `666566d..e27d419`, quindi nella skill che `ROADMAP-CC-3` ha girato, e CC-3 la dà verde con la
prova («due archi pubblicati, `S4 → S2` e `S8 → S7`, entrambi duri»; il cartellino R-017 di
`EVALUATION-RULES.md` registra *Fixed*). `ROADMAP-CC-4` la ridà rossa: `roadmap.md:40` (`S1 → S0`) e
`:42` (`S3 → S1`) pubblicano «dopo il repository» e «dopo lo scheletro» — esattamente ciò che
`drawing-the-map.md:97` vieta, e la clausola è ancora lì, intatta.

**Perché il fix precedente ha mancato: cancellato da due refactor, ciascuno per una ragione buona.**
`f77bc61` poggiava su quattro appoggi. Due sono stati tolti dopo:

- `2bf0a12` toglie dal template la spinta di default — «on most maps most rows carry `—`» — perché
  aveva causato l'overshoot opposto. Quella riga è ciò che una sessione legge *mentre riempie la
  colonna*, ed è stata sostituita da «Both directions are failures», che nomina il rischio senza dare
  un default. (Attribuzione: **letta dal diff**; il messaggio nomina R-017, ma per il fallimento
  opposto.)
- `d805196` riscrive il *tell* di **Published order**, da «the reason for the edge is already written
  in `Ordering criteria`» a «the substitution test itself», e lascia cadere dalla checklist «no edge
  restates a reason `Ordering criteria` already gives». Il test di sostituzione **non copre** il
  prerequisito universale: niente può sostituire lo scheletro, quindi `S3 → S1` lo passa. Il tell
  concreto è stato scambiato con uno che non vede questo caso. (Attribuzione: **letta dal diff**.)

C'è un terzo effetto, e lo do come inferenza e non come dato: la regola sintattica che `2bf0a12`
aggiunge — «Where the dependent's `Includes` builds on a table, a migration, a resolver or an adapter
that another `NOW` row delivers … the edge is hard and stays published» — è leggibile come una
*licenza* proprio per l'arco allo scheletro, che consegna il runner delle migrazioni e la connessione
al datastore. Se quella lettura è quella che CC-4 ha fatto, le due clausole si contraddicono a due
paragrafi di distanza.

**Il fix.** File: `skills/roadmap/references/drawing-the-map.md`, § *Hard dependencies*, righe 92–94.
Al paragrafo sintattico si aggiunge l'eccezione che gli manca:

> … no fixture supplies it without bypassing the production path: the edge is hard and stays
> published — **except where the deliverer is one of the two prerequisites.** The repository row and
> the skeleton are what every row depends on; their edges carry no information and are never
> published, however hard they are.

E `The map holds when` guadagna il lookup che il tell perduto faceva:

> - no `Depends on` cell names the repository row or the skeleton;

**Chiude:** `R-017 (published order)` in `manual-run-1`, `ROADMAP-CC-2`, `ROADMAP-CC-4`.

**Rischia di rompere:** riapre *dropped edge* nell'unico punto in cui l'arco allo scheletro sarebbe
portante — una riga che senza lo scheletro non è verificabile e che un riordino potrebbe spostare
davanti. Per costruzione non succede: lo scheletro è secondo nel register e nessuna riga di prodotto
può precederlo, ed è precisamente il motivo per cui la clausola esiste. Se ne accorgerebbe **R-017
`⚠ opposite`** e l'item di checklist che sopravvive («no row that builds on a table, resolver or
adapter another `NOW` row delivers carries `—`»). Il validator qui non vede niente: controlla che gli
id risolvano e non chiudano cicli, non se un arco vada pubblicato — e questo va detto, perché un
`OK` verde non è evidenza su questa regola.

**Come si misura:** metà *drawing*, scenario 0. Serve un run nuovo. Va scritto insieme al fix 2.1,
perché i due si spingono in direzioni opposte.

## 2. Fix che non hanno preso

Uno solo.

### 2.1 — `R-017`, *dropped edge*: `S11` porta `—` e la sua `Verification` chiama tre righe

**Storia.** `2bf0a12` — *Ripara i due fix della sessione precedente* — la prende di mira: **id nel
messaggio del commit**, con il caso preciso di CC-3 («`S4` costruisce sulle tabelle e sul resolver che
`S3` consegna, e porta `—`»). Sta in `e27d419..d805196`, quindi nella skill di `ROADMAP-CC-4`, che è
l'unico run dopo di lui. Ed è rosso: `roadmap.md:50`, `S11` porta `Depends on —` mentre la sua
`Verification` — «una persona non tecnica invitata entra dal dominio pubblico, aggiunge una ricetta da
link e la ritrova cercandola a parole sue» — richiede `S10`, `S5` e `S8`.

**Perché il fix precedente ha mancato: diagnosi costruita sull'unica istanza che aveva.** Il test che
`2bf0a12` scrive è sintattico su nomi di *impianto* — table, migration, resolver, adapter — e si legge
dentro l'`Includes` del dipendente. Il dropped edge di CC-4 sta a un'altra altitudine e in un altro
campo: `S11` è la riga di rilascio, e ciò senza cui non è verificabile sono *capacità* (un invito
accettato, una ricetta aggiunta dal percorso che la aggiunge, una ricerca che risponde), non tabelle;
e stanno in `Verification`, non in `Includes`. Il lookup non restituisce niente e il `—` regge. La
diagnosi dell'istanza era giusta; la regola che ne è uscita è più stretta della classe di fallimento.

**Il fix.** Stesso file e stessa sezione del 1.1 — `drawing-the-map.md` § *Hard dependencies* — in
coda allo stesso paragrafo:

> Read the dependent's `Verification` as well as its `Includes`. Where the evidence that a row is
> done exercises a capability another `NOW` row delivers, no controlled input stands in: putting the
> capability there by hand is the fixture that bypasses the production path. A `kind: release` row is
> where this bites hardest, because its whole evidence is other rows' capabilities exercised end to
> end.

E l'item di checklist si estende:

> - … and no row whose `Verification` exercises a capability another `NOW` row delivers carries `—`.

**Chiude:** `R-017 (dropped edge)` in `ROADMAP-CC-3` e `ROADMAP-CC-4`.

**Rischia di rompere:** *published order* di nuovo, ed è la stessa oscillazione che ha prodotto
questa coppia. Una riga di rilascio può finire per nominare mezza mappa, che è il rumore da cui la
regola era partita («fifteen edges that all say *after the skeleton* bury the four that carry
information»). Se ne accorgerebbe **R-017 `⚠ opposite`** nella direzione opposta, e il lookup del 1.1
— nessuna cella nomina i due prerequisiti — che taglia via i candidati più numerosi. Le due proposte
vanno scritte e misurate insieme: separate, riproducono il ciclo `f77bc61` → `2bf0a12`.

**Come si misura:** metà *drawing*, scenario 0. Serve un run nuovo. Il cartellino R-017 di
`EVALUATION-RULES.md` dice ancora che lo specchio *dropped edge* non è mai stato dimostrato: CC-4
dimostra che non lo è, e chi tiene il cartellino ne prenda nota — non è materia di questo report,
perché il fix atterra fuori da `skills/roadmap/`.
## 3. Mai risolte

Tre proposte. Il criterio di scelta è la ricorrenza.

**Prima, che cosa resta fuori.**

- **H5** (4/4) si scarta: la cura cade fuori da `skills/roadmap/`. Nessuna clausola della skill
  obbliga una mappa a enumerare lo stack, e CC-2 e CC-4 registrano entrambe che nemmeno
  `reference-roadmap/` nomina React Query. Per il preambolo di `EVALUATION-RULES.md` il difetto è nel
  check, e il check non è materia di questo report.
- **R-009** (3/4) e **R-008** (3/4) si scartano: `779bf17` li prende di mira alla lettera — «no first
  validator excludes a capability its own theme's promise names» sostituisce la norma nella checklist
  — ed è dopo la versione che CC-4 ha girato. Proporre un secondo intervento su una clausola mai
  eseguita sarebbe un tiro alla cieca. Il prossimo run di scenario 0 li misura, non un'altra riga.
- **R-035** (2 run) si scarta per valore: la metà di CC-4 è dichiarata discutibile dal review stesso
  (sovrapposizione con R-033), e la metà solida di CC-3 — due domande dovute che non arrivano
  all'autore — è un difetto del messaggio di chiusura, non della mappa.

### 3.1 — `R-015` / `C1`: il conflitto risolto dentro una riga e riportato da nessuna parte

**File:** `skills/roadmap/references/drawing-the-map.md`, § *What the map reports about its input*.

Oggi la sezione dice che ogni entry «leaves by one of three exits, and no other» (riga 215) e poi
passa ai tre test su una riga di `Assumptions` già scritta. La norma c'è; il tracciato no. In tutti e
quattro i run il lato di C1 è stato preso in un bullet — `S6 § Excludes` (m-1), `S3 § Includes` (CC-2,
CC-4), `S3 § Excludes` (CC-3) — e nessuna riga è stata scritta.

**Che cosa si aggiunge**, subito dopo il terzo exit (riga 227), sulla forma che ha funzionato in
`779bf17`: una lettura che diventa un lookup.

> **Taken in a row and nowhere else** is the failure to watch for, and its tell is mechanical: a
> bullet of `Includes` or `Excludes` picks one side of a conflict the sweep found, and no line of
> `Assumptions`, no line of `Open questions` and no spike names that entry. The bullet is where the
> reading is *applied*, never where it is *reported*; a reader who finds only the bullet cannot tell
> a decision from an oversight.

E l'item di `The map holds when` (riga 287) diventa:

> - every conflict and every undecided choice left the sweep by one of the three exits, and no side
>   of one was taken only in a row's `Includes` or `Excludes`;

Nessun campo nuovo, nessuna sezione nuova: la mappa non cresce di una riga se non aveva niente da
riportare.

**Chiude:** `C1` / `R-015` in `manual-run-1`, `ROADMAP-CC-2`, `ROADMAP-CC-3`, `ROADMAP-CC-4`.

**Rischia di rompere:** il `⚠ opposite` di R-015 — una mappa che non prende nessuna lettura e
pubblica tutto come domanda aperta. Il testo spinge a *riportare* la lettura, non a smettere di
prenderla, ma una sessione può leggerlo come «nel dubbio, `Open questions`». Se ne accorgerebbe
R-015 stessa, che è già scritta in entrambe le direzioni («Exposing is not resolving» da un lato,
il `⚠ opposite` dall'altro), e le voci `A1`–`A3` del brief, che dicono dove una fonte *seleziona* e
quindi l'entry è risolta.

**Come si misura:** metà *drawing*, scenario 0 (`make eval-cycle`) — il file è
`references/drawing-the-map.md`. Serve un run nuovo. Un run è una domanda: due run che tengono sono
il verdetto, e su questa violazione ne servono davvero due, perché è l'unica a 4/4.

### 3.2 — `R-022`: `Includes` decide ciò che la riga dichiara indeciso

**File:** `skills/roadmap/references/slice-rules.md`, § *The columns* → `readiness`, righe 168–170.

La clausola c'è ed è netta («publishing it unconditionally is **silent contradiction**»). È fallita in
tre run, in due forme:

- `manual-run-1` (`S1` `ready`, `Includes` «Database Neon collegato») e `ROADMAP-CC-2` (`S0` `ready`,
  `Includes` apre l'account del provider LLM che `S5` dichiara non scelto): readiness sbagliata *e*
  bullet che decide;
- `ROADMAP-CC-4` (`S11` `needs-decision`, la sua `Open questions` dice che la risposta decide se
  tetto di spesa e avviso vadano accesi prima, e `Includes` li mette dentro entrambi): readiness
  **giusta** e bullet che decide lo stesso.

La seconda forma dice dove la regola si perde: viene applicata alla colonna e mai ri-letta contro il
documento. Il tracciato sta dentro la riga stessa.

**Che cosa si scrive al posto della frase attuale:**

> A row whose decision the sources leave open is `needs-decision`, and its `Includes` and
> `Verification` are worded to defer to the pending decision rather than picking a side — publishing
> it unconditionally is **silent contradiction**. The tell is inside the row and is a lookup, not a
> reading: take every noun the row's own `Open questions` leaves open — a provider, a model, a
> threshold, a capability that may or may not ship — and read `Includes` for it. Where it stands
> there unconditioned, the row has decided what it declares undecided. `needs-decision` in the
> register does not license the bullet: the readiness says the choice is open, the bullet says it is
> closed, and the reader believes the bullet.

**Chiude:** `R-022` in `manual-run-1`, `ROADMAP-CC-2`, `ROADMAP-CC-4`. In `ROADMAP-CC-3` non è
registrata — né rossa né verde — quindi non è un verde da cui inferire qualcosa.

**Rischia di rompere:** righe che si coprono le spalle — un `Includes` scritto così vago che non ci
si costruisce niente, cioè «a row that stops at one layer is not thin, it is unfinished»
(`slice-rules.md` § *What makes a slice*). Se ne accorgerebbe **R-020**, perché un `Includes` che
non impegna nulla lascia il `Learning target` senza osservazione in `Verification`; e **R-023**, che
guarda le righe che si fermano prima. Sul brief, `A1` è il caso di riferimento: la scelta del
provider blocca `S1` da sola, e la riga deve restare costruibile appena la scelta arriva.

**Come si misura:** `slice-rules.md` è letto in ogni sessione, quindi il cambiamento si vede in
entrambe le metà. La violazione però si osserva solo su una mappa disegnata: la misura è scenario 0,
e gli scenari router 1–3 sono il controllo a basso costo che la forma vaga non sia comparsa. Serve un
run nuovo.

### 3.3 — `R-012`: l'ordine, dopo che è stata tolta la sezione che lo argomentava

**Vista in un run solo, ed è il motivo per cui va fatta ora e non dopo il secondo.** `d805196` toglie
`Ordering criteria` e il suo stesso messaggio chiude con: «S4 of the plan — one drawing run and its
review, to show the order holds without the section — has not run». `ROADMAP-CC-4` **è** quel run, ed
è rosso due volte sulla stessa regola: `S4` (seconda riga di `ricettario`) sta in quinta posizione,
prima della prima riga di `ricerca`, `accesso` e `condivisione`, senza che nessuna delle quattro
licenze sia leggibile dalla riga; e `S8`, la ricerca semantica che la mappa stessa dichiara
esistenziale, è nona. I verdi precedenti non sono confrontabili: `manual-run-1` e CC-2 li avevano
*grazie* alla sezione — CC-2 in particolare è verde perché «le deviazioni sono nominate dentro i
criteri 3, 5 e 7 che le concedono», criteri che non esistono più. Aspettare il secondo run non compra
informazione nuova: compra la conferma di un'ipotesi già falsificata da chi l'ha formulata.

**File:** `skills/roadmap/references/drawing-the-map.md`, § *Ordering for learning*. Due edit, nessuna
sezione e nessun campo nuovo — la sezione rimossa non torna.

**(a)** Alla non-negoziabile **Breadth before depth** (righe 161–164) si aggiunge il tracciato, in
coda al testo attuale:

> The trace it leaves is positional and needs no argument to find: a theme's **second** row standing
> before another theme's **first**. Read the register once in order; for each such pair, name which
> of the four licenses it, reading the licence off the row's own `Learning target` rather than off an
> intention. A pair no licence covers is the reorder to make before the map goes down.

E l'item di `The map holds when` (riga 284) passa da una lettura a un lookup:

> - no theme's second row stands before another theme's first unless one of the four licences reads
>   off that row's `Learning target`;

**(b)** Alla terza non-negoziabile — «A row that opens a pipeline or adapter shared by several paths
follows every `NOW` row that feeds it» (righe 170–171) — si aggiunge il vincolo che le manca, ed è la
diagnosi che il review di CC-4 fa su `S8`:

> Where that constraint pushes the differentiator or the existential risk behind the themes that lean
> on it, it is the shape of the candidate row that is pushing, not the constraint: the pipeline and
> the promise it serves are two rows, and *the cheapest real input that can validate a risky engine*
> pays for the split. A non-negotiable that fires only because of how a row was cut is a finding
> about the cut.

**Chiude:** entrambe le voci `R-012` di `ROADMAP-CC-4`.

**Rischia di rompere:** un riordino meccanico che scavalca le altre tre non-negoziabili — tipicamente
*required recovery outranks breadth*, che in CC-4 licenzia correttamente `S6` e `S7` prima di aprire
un altro tema. Se ne accorgerebbe **R-012** stessa, che elenca il recupero dovuto fra le quattro
licenze, e `drawing-the-map.md` § *Required recovery outranks breadth*. Un riordino che rompesse un
arco duro non pubblicato lo prenderebbe **R-017 `⚠ opposite`**. Sul brief: `H1` (la ricerca in `NOW`)
e `A5`/`N3` (il corpus seed come input reale più economico) sono le voci che direbbero se lo split
del punto (b) è stato comprato con lavoro che nessuna fonte chiede.

**Come si misura:** metà *drawing*, scenario 0. Serve un run nuovo, ed è lo stesso run che chiude il
debito che `d805196` si è lasciato dietro.


---

**Scartata dalle tre, pur essendo ricorrente:** `R-020` — learning target doppio, e claim del
`Learning target` senza osservazione in `Verification` — rossa in `manual-run-1` (`S3`, `S5`) e in
`ROADMAP-CC-2` (`S3`, `S4`, `S7`, `S8`, `S9`, `S11`), e vista nella stessa forma in `ROADMAP-CC-3`
(`S5`) e in `ROADMAP-CC-4` (`S3`) ma non contata in nessuno dei due. È l'unica dove non riesco a
separare il difetto della skill dal giudizio del revisore, e CC-4 dice perché: il singolare di R-020
e l'obbligo di R-013 — il seam di scope viaggia con la prima riga che persiste — si pestano i piedi
sulla stessa riga, che è una sovrapposizione di clausole e non un fallimento del modello. Finché
quella non è sciolta, un fix su R-020 non è misurabile.
