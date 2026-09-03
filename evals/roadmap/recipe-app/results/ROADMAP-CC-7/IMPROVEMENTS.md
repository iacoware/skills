# Miglioramenti — dopo `ROADMAP-CC-7`

Letti: i sette `REVIEW.md` sotto `results/`, i `PROMPT.md` per gli ancoraggi, tutti i commit di
`skills/roadmap` fra un ancoraggio e il successivo, `design/roadmap/ROADMAP-GOAL.md` e `CONTEXT.md`,
il preambolo di `EVALUATION-RULES.md`, `skills/roadmap/` per intero e `reference-roadmap/`.
Niente è stato implementato e niente sotto `skills/` è stato toccato: questo file è l'unico scritto.

## Dove cade ogni run nella storia della skill

L'ancoraggio delimita l'intervallo, non seleziona il commit da leggere: dentro ogni intervallo i
commit sono stati letti tutti.

| Run | Ancoraggio | tree `skills/roadmap` | Fonte dell'ancoraggio |
|---|---|---|---|
| `manual-run-1` | `dcf783d` (2026-08-21) | `ed75429` | `PROMPT.md`, che lo dichiara **inferito** |
| `ROADMAP-CC-2` | `666566d` (2026-08-25) | `eedf170` | `PROMPT.md`, ricostruito dal transcript |
| `ROADMAP-CC-3` | `e27d419` (2026-08-25) | `028f3b4` | `PROMPT.md` |
| `ROADMAP-CC-4` | `d805196` (2026-08-26) | `2f1d0db` | `PROMPT.md` |
| `ROADMAP-CC-5` | `37a0976` (2026-08-28) | `0913e60` | `PROMPT.md` |
| `ROADMAP-CC-6`, `-6B`, `-6C` | `fb29812` (2026-09-03) | `0d47a59` | `PROMPT.md` |
| `ROADMAP-CC-7` | `3fc0293` (2026-09-03) | `132d4e7` | `PROMPT.md` |

I due soli ancoraggi non dichiarati dal run sono `manual-run-1` — che dichiara la propria inferenza —
e `ROADMAP-CC-2`, ricostruito dal transcript e concorde col commit che ne aggiunge la mappa
(`bf979c3`). Dove ci fondo qualcosa, sotto, lo dico.
`CC-6B` e `CC-6C` dichiarano lo stesso tree di `CC-6`: stessa skill, nessun fix nuovo alla prova, e
non hanno `REVIEW.md` — non entrano nella tabella. `6f3ba7b` cita però `CC-6B` come sua motivazione.

**I commit dentro ogni intervallo.**

- `dcf783d..666566d` — `18968aa`, `524e180`, `676b580`, `666566d`: il refactoring S1–S3 (SKILL.md
  riscritto come router, regole divise fra `drawing-the-map.md` e `slice-rules.md`, tag `goal` legale
  per una riga di `Assumptions` a quota mappa). È l'unico intervallo che tocca `slice-rules.md`.
- `666566d..e27d419` — `f77bc61` (R-017, *published order*), `e27d419` (C2: due test sulla riga di
  `Assumptions`, sweep dentro un solo documento).
- `e27d419..d805196` — `2bf0a12` (terzo test *Its reason survives its citations*; R-017 *dropped
  edge* dopo l'overshoot), `ff63c96` (verdetto di tema ridotto a un paragrafo), `d805196`
  (`Ordering criteria` rimosso dal formato).
- `d805196..37a0976` — `779bf17` (theme compression: *A promise names only what its first validator
  delivers*), `79f4a4a` (cross-functional concerns pubblicati solo dove una riga poteva fare
  altrimenti), `7b62754` (R-017 nelle due direzioni).
- `37a0976..fb29812` — `f569dce` (R-017 *dropped edge* ristretto), `f25c8d9` (C2: il soggetto di una
  citazione è un lookup), `8eb3a71` (C1: tell sul lato preso in un bullet), `d8bc79d`
  (`Verification` in forma di elenco nel template).
- `fb29812..3fc0293` — `6f3ba7b` (lo split test decide, il merge test si chiede solo dove il primo
  cade), `09c37ea` (i verdetti dei temi escono dalla mappa e vanno in `.roadmap/log.md`, scritto
  prima della tabella `Themes`).

## Che cosa ricorre

`ok` verde, `ko` rosso, `·` non registrata.

| Violazione | m-1 | CC-2 | CC-3 | CC-4 | CC-5 | CC-6 | CC-7 | Commit che l'ha presa di mira |
|---|---|---|---|---|---|---|---|---|
| **C1** / R-015 | ko | ko | ko | ko | ko | ko | ko | `8eb3a71` |
| **C2** / R-015 | ok | ko | ko | ok | ko | ko | ok | `e27d419`, `2bf0a12`, `f25c8d9` |
| **U4** / R-015 | ok | ok | ok | ok | ko | ko | ok | nessuno |
| **R-035** | · | ok | ko | ko | ko | ko | ko | nessuno |
| **R-020** | ko | ko | ok | · | ko | ko | ko | nessuno |
| **R-012** | ok | · | · | ko | ok | ko | ok | nessuno |
| **R-022** | ko | ko | ok | ko | ok | ok | ok | nessuno |
| **R-024**, comportamento senza proprietario | ok | ok | ok | ok | ok | ok | ko | nessuno |
| **R-024**, split warning non risolta | ok | ko | ok | ok | ok | ok | · | nessuno |
| **R-009** | ok | ko | ko | ko | ok | ko | ok | `779bf17`, poi `09c37ea` + `6f3ba7b` |
| **R-008** | ko | ko | ok | ko | ok | ok | ok | `779bf17`, `09c37ea` |
| **R-017** | ko | ko | ko | ko | ko | ok | ok | `f77bc61`, `2bf0a12`, `7b62754`, `f569dce` |
| **H5** | ko | · | · | · | · | ok | ok | nessuno |

Le due forme di R-024 stanno su righe separate perché sono clausole diverse della stessa regola: in
`CC-2` è la split warning di `S3` (quattro capacità unite da *e*), in `CC-7` è
*Conserve the behaviour set* — derivazione di tag e tempo, e cancellazione di una ricetta, senza
proprietario. Contarle insieme farebbe sembrare ricorrente una violazione vista una volta.

---

## 1. Regressioni

**Vuota.** Nessuna violazione presa di mira da un commit è tornata rossa dopo essere stata verde.
R-009 e R-008 avevano quella forma fino a `CC-6` — verdi in `CC-5` dopo `779bf17`, rosso R-009 in
`CC-6` — ma `CC-7` li dà verdi entrambi dopo `09c37ea` e `6f3ba7b`, quindi il caso è chiuso e non
riaperto. R-017 è verde per il secondo run consecutivo. C2 torna verde in `CC-7` dopo `f25c8d9`.

---

## 2. Fix che non hanno preso

Uno.

### 2.1 — C1 / R-015: il lato preso in un bullet, e le sorgenti dichiarate concordi

`ko ko ko ko ko ko ko` — sette run su sette, l'unica a punteggio pieno in tutta la storia dell'eval.

**Attribuzione.** `8eb3a71` *Report the side a row takes: bullet-only conflict resolution gets a
tell*. L'id sta nel messaggio del commit, che elenca le cinque istanze allora note e dichiara la
misura («being 5/5, two green runs are needed before calling it closed»). Sta in
`37a0976..fb29812`: i run che lo mettono alla prova sono `CC-6` e `CC-7`, e sono rossi tutti e due.
Nessun run dopo di lui lo dà verde.
Una proposta più forte esiste già — `ROADMAP-CC-6/IMPROVEMENTS.md` § 2.1 — e non è stata applicata:
i due commit di `fb29812..3fc0293` prendono i temi, non lo sweep. Una proposta non è un commit,
quindi la categoria resta questa e l'attribuzione resta a `8eb3a71`.

**L'istanza di `CC-7`.** `slices/S5-estrazione-llm.md:56`, `Excludes`: «L'inserimento manuale a form
vuoto: è già in `S3`, perché le sorgenti lo danno come lo stesso form dell'edit e non come un terzo
motore». Cinque righe di `Assumptions`, due di `Open questions`, nessuna nomina C1; nessuno spike lo
copre.

**Perché il fix precedente ha mancato.** Non l'ambito. Il fatto che `REVIEW.md` dà per portante —
«la lettura è *applicata* in un bullet e non è *riportata* da nessuna parte» — è alla lettera il tell
di `8eb3a71`, e la review lo cita per nome: il testo attuale ci arriva già, quindi la diagnosi è la
forza e non l'ampiezza. La forza le manca dove `8eb3a71` stesso aveva dichiarato il proprio confine:
il tell è condizionato a «one side of **a conflict the sweep found**». Quel fatto non sta sulla
pagina, sta nella memoria della sessione, e uno sweep che non registra la coppia non deve nessuna
uscita. Ogni altro tell che ha preso in questa storia si verifica sull'artefatto e basta — gli
`Excludes` di un primo validatore (`779bf17`), i nomi che una frase citata dà al proprio soggetto
(`f25c8d9`), la riga che sopravvive a essere spostata in un altro progetto (`79f4a4a`). Questo no: un
tell che chiede alla sessione di ricordare non è un lookup. Il difetto è nell'intervento.

`CC-7` aggiunge quello che `CC-6` non aveva: il bullet **dichiara le sorgenti concordi** («le
sorgenti lo danno come…»), mentre `arch-choices.md` § *Estrazione contenuto* punto 3 dice l'opposto.
È la prova diretta che lo sweep non ha mai registrato C1 come conflitto — non che l'abbia registrato
e poi taciuto. `REVIEW.md` marca quel fatto come *corroborazione*: per il **verdetto** la gerarchia è
giusta, perché la violazione sta in piedi comunque; per la **diagnosi del fix mancato** è quel fatto
a reggere, ed è l'unico che distingua le due cause. Su questo punto la review lo sotto-classifica, e
lo dichiaro.

**File — `skills/roadmap/references/drawing-the-map.md`**, § *What the map reports about its input*,
in coda al paragrafo *Taken in a row and nowhere else* (riga 265-271, dopo «it says what was built,
not which side was taken and why»). Non un secondo paragrafo di norma: il modo di far scattare il
tell senza lo sweep.

> The tell does not rest on remembering the sweep. After the first cut, read every `Includes` and
> `Excludes` bullet that says **how** a behaviour works or does not — *it skips the extractor*, *it
> shares the form and not the pipeline* — or that gives its reason as what the sources hold — *the
> sources give it as the same form* — and look that behaviour up in the sources. Where two of them
> describe it differently, the bullet is a side taken and owes its line, whether or not the entry was
> ever on the sweep's list; a bullet reading the sources as agreeing is making the very claim the
> lookup checks. A bullet that only says which row or which horizon a behaviour belongs to owes
> nothing.

E l'item di `The map holds when` (riga 337-338), al posto di «and no side of one was taken only in a
row's `Includes` or `Excludes`»:

> - every conflict and every undecided choice left the sweep by one of the three exits, and every
>   bullet stating how a behaviour works, or reading the sources as agreeing on it, was looked up in
>   the sources before the map was written;

La seconda clausola dell'innesco — il bullet che argomenta da ciò che le sorgenti danno — è nuova
rispetto a `CC-6` § 2.1 ed è tarata sulla riga di `CC-7`, dove il bullet è per metà assegnazione di
proprietà e per metà lettura delle fonti: senza di essa il tell su quella riga è discutibile, con
essa è un lookup. Nessun campo nuovo, nessuna sezione nuova: il costo è un secondo passaggio sulle
fonti, ristretto ai bullet che enunciano un meccanismo o citano le sorgenti, che su queste mappe sono
una manciata.

**Chiude:** C1 / R-015 in `manual-run-1` (`S6 Excludes`), `ROADMAP-CC-2` (`S3 Includes`),
`ROADMAP-CC-3` (`S3 Excludes`), `ROADMAP-CC-4` (`S3 Includes`), `ROADMAP-CC-5` (`S3 Excludes`),
`ROADMAP-CC-6` (`S4 Excludes` + `S8 Includes`), `ROADMAP-CC-7` (`S5 Excludes`).

**Rischia di rompere:** il `⚠ opposite` di **R-015** — una mappa che non prende nessuna lettura e
pubblica tutto come domanda aperta, o che riempie `Assumptions` ogni volta che due fonti si sfiorano.
Se ne accorgerebbero **R-015** stessa, scritta in entrambe le direzioni, il primo dei tre test sulla
riga di `Assumptions` (*Delivery can refute it*, che uccide la riga che ri-afferma una fonte) e, sul
brief, **A1**–**A3**, che dicono dove una fonte seleziona e quindi non c'è niente da riportare. Il
secondo rischio è di costo e non di qualità: un secondo passaggio che non trova niente si vedrebbe in
`METRICS.md` prima che in `REVIEW.md`, e la voce a cui rispondere sarebbe `improve-perf.prompt.md`.

**Come si misura:** metà *drawing*, `REVIEW-WORKFLOW.md` § *Scenario 0*, che è quella indicata per un
cambiamento a `references/drawing-the-map.md`. Serve un run nuovo, e su questa **due**: è a 7/7 e il
primo tentativo è già speso, quindi il `PROMPT.md` del run successivo deve dichiarare che entra in
prova un secondo tentativo sulla stessa violazione.

**Controllo a costo zero, fatto.**
*Contro la riga che l'ha motivato:* prende `CC-7`. `S5 Excludes` dà la propria ragione come ciò che
le sorgenti tengono («le sorgenti lo danno come lo stesso form dell'edit e non come un terzo
motore»), e il lookup su *inserimento manuale* trova `concepts.md` § *Pipeline di estrazione* contro
`arch-choices.md` § *Estrazione contenuto* punto 3, che lo descrivono diversamente: il bullet deve la
sua riga e non ce l'ha. Prende allo stesso modo le sei istanze precedenti, che sono tutte bullet di
meccanismo sullo stesso comportamento.
*Contro `reference-roadmap/`:* letti gli `Includes` e gli `Excludes` di tutte e quindici le righe.
Il tell scatta su **due** bullet e **nessuna riga resta marcata**, perché in entrambi il lookup si
risolve: `S4 Includes` — «L'embedding della query a ogni ricerca» — è un meccanismo su cui
`arch-choices.md` e `goal.md` si contraddicono, e la riga `ricerca-semantica, S4` di `Assumptions`
c'è; `S7 Excludes` — «quello che si scrive nel form si salva così com'è, senza JSON-LD e senza LLM» —
è il meccanismo di C1, e la riga `inserimento-manuale, S7` c'è ed è precisamente quella dovuta. Non
scatta su `S9 Excludes` («La scelta definitiva del modello: si cambia senza toccare la forma di
questa riga»), che è un meccanismo su una scelta indecisa e non su una coppia contraddittoria; né su
`S13 Excludes`, che dà uno scopo e non una lettura delle fonti; né su `S10 Includes` («Lo stesso
motore e lo stesso schema di output di `S9`»), dove le due fonti concordano sul copia-incolla; né sui
bullet di sola appartenenza di `S0`, `S1`, `S2`, `S3`, `S5`, `S6`, `S8`, `S11`, `S12`, `S14`, che
dicono a quale riga o a quale orizzonte un comportamento va e non come funziona.

---

## 3. Mai risolte

Tre, nell'ordine in cui le farei. Il criterio è la ricorrenza.

**Prima, che cosa resta fuori.**

- **H5** — nominata e **scartata**: la cura cadrebbe fuori da `skills/roadmap/`. Nessuna clausola
  della skill obbliga una mappa a enumerare lo stack, e quattro review registrano che nemmeno
  `reference-roadmap/` nomina React Query. È materia del brief. Verde negli ultimi due run per via
  del run, non per via della voce.
- **La sovrapposizione R-021 / R-011** — la riga di repository è `enabler` e per costruzione non ha
  un percorso di produzione end-to-end. Cinque review su sette la segnalano, `CC-7` la mette in una
  sezione sua, e nessuna la conta rossa: per il preambolo delle regole è una clausola che dice due
  cose che si sovrappongono, e non compete con violazioni che sono rosse.
- **R-024, comportamento senza proprietario** — rossa in `CC-7` e in nessun altro run. Due istanze
  dentro lo stesso run (derivazione di tag e tempo buttata in `S6 Excludes`; cancellazione di una
  ricetta verificata da `S8` e `S9` e consegnata da nessuno), con conferma indipendente dal
  riferimento, che le dà una riga intera (`S13`). Resta fuori perché l'unità dell'eval è il run e
  questa ne ha uno: per il preambolo un run registra e due decidono. Torna in lista se `CC-8` la
  ridà rossa, ed è la prima candidata a rientrare.
- **R-008, R-009, R-017, C2** — chiuse da fix e verdi in `CC-7`. Un secondo intervento
  lavorerebbe contro un verde.

### 3.1 — R-035: il messaggio di chiusura si apre sul validator

`· ok ko ko ko ko ko` — cinque run consecutivi, sempre la stessa forma: una riga di stato **prima**
delle quattro parti. «Validatore: `OK`, nessun ERROR né WARNING» (CC-3), «Mappa scritta e validata
(`OK`, nessun warning).» (CC-4, CC-5), «`.roadmap/` scritta e validata» (CC-6), «Mappa scritta.
Validator pulito, nessun `WARNING`.» (CC-7). In tutti e cinque le quattro parti ci sono e
nell'ordine giusto. Nessun commit l'ha mai presa di mira: `09c37ea` tocca quel paragrafo, ma solo per
dire che `log.md` non è fra le quattro. Proposte esistono — `CC-5` § 3.3 e `CC-6` § 3.1 — e non sono
state applicate; una proposta non è un commit, quindi la violazione resta in questa categoria. La
ripropongo perché `CC-7` aggiunge il quinto run e non aggiunge nulla alla diagnosi.

**File — `skills/roadmap/SKILL.md`**, § *5. Close the session*. In deroga al default, e per la
ragione che la skill dichiara da sé: «One checklist per altitude — the row in `slice-rules.md`, the
map in `drawing-the-map.md`, the session here». *Close the session* non ha un file in `references/`,
e la sovrapposizione da sciogliere è fra due clausole della stessa sezione: R-033 vuole che si veda
che il validator ha girato, R-035 vuole quattro parti e nient'altro. `CC-4`, `CC-5`, `CC-6` e `CC-7`
la nominano tutte come sovrapposizione, che il preambolo chiama *a clause saying two things that
overlap*: la cura è disambiguare, non aggiungere.

Al passo del validator, dopo «A `WARNING` is a signal to the author: the cap and the floor are
findings to discuss, not defects to silence.» (riga 195-196):

> A clean run reports nothing. The validator's only output to the author is a `WARNING`, and it goes
> after the four parts with anything else the session owes; that it ran at all is visible in the
> session, not in the message.

E l'apertura del report (riga 198-199), al posto di «**Then report the written map, and nothing
else.** Four things, in this order, read off the files as they now stand:»:

> **Then report the written map, and nothing else.** The `Themes` table is the first thing in the
> message: no preamble, and in particular no line saying the map was written and validated, which
> narrates an operation the author can already see. Four things, in this order, read off the files as
> they now stand:

E l'ultimo item di *The session holds when* (riga 240-241):

> - the session closed on the four-part report — themes, register, open questions, path — with
>   nothing before it and only what it owes after it.

La corroborazione che `CC-7` aggiunge — le due `Open questions` riscritte più corte invece di essere
lette dal file — **non riceve testo nuovo**: «read off the files as they now stand» già ci arriva
alla lettera, quindi lì la diagnosi non è l'ambito e nemmeno la forza, è la stessa apertura narrativa
che porta la sessione a raccontare invece di copiare. Aggiungere una clausola per una cosa che la
frase dice già è come un router ricresce.

**Chiude:** R-035 in `ROADMAP-CC-3`, `ROADMAP-CC-4`, `ROADMAP-CC-5`, `ROADMAP-CC-6`,
`ROADMAP-CC-7`.

**Rischia di rompere:** che una sessione, per non narrare, smetta di riportare un `WARNING` dovuto o
una domanda che ha prodotto — cioè la metà solida del rosso di `CC-3`, dove due domande dovute non
sono mai arrivate all'autore. Se ne accorgerebbero **R-033** («every `WARNING` put to the author
rather than silenced») e **R-035** stessa, che vuole la domanda *dopo* le quattro parti e non al
posto loro. Il secondo rischio è leggere il silenzio sul validator come licenza a non girarlo:
**R-033** legge il transcript e non il messaggio — «What this reads is that it ran and what it did
with the `WARNING`s» — quindi quel sensore resta intatto.

**Come si misura:** metà *drawing*, scenario 0, che `REVIEW-WORKFLOW.md` indica per ogni cambiamento
a *Close the session*. Serve un run nuovo, e il rilievo si legge in `TRANSCRIPT.jsonl`, non in
`.roadmap/`.

**Controllo a costo zero.**
*Contro la riga che l'ha motivato:* prende `CC-7`, transcript idx 114 — «Mappa scritta. Validator
pulito, nessun `WARNING`.» sta prima della tabella `Themes`, non c'era nessuna `WARNING`, e la riga
cade sia sotto «A clean run reports nothing» sia sotto «no line saying the map was written and
validated». Prende allo stesso modo `CC-3`, `CC-4`, `CC-5` e `CC-6`.
*Contro `reference-roadmap/`:* **niente da controllare, e mi fermo alla prima metà.** La proposta
cade ad altitudine di sessione e il riferimento è una mappa, non un transcript: non ha un messaggio
di chiusura da marcare. Non sostituisce il run nuovo, che resta l'unica misura.

### 3.2 — R-020: il secondo claim del `Learning target` che nessuna osservazione raggiunge

`ko ko ok · ko ko ko` — rossa in `manual-run-1` (`S3`, `S5`), `ROADMAP-CC-2` (cinque righe),
`ROADMAP-CC-5` (`S5`, `S7`, `S9`), `ROADMAP-CC-6` (`S9`), `ROADMAP-CC-7` (`S4`); discussa e non
contata in `CC-3` e `CC-4`. Nessun commit l'ha mai presa di mira: `slice-rules.md` non è più stato
toccato dopo `676b580`, e `d8bc79d` cambia il *template* mettendo la `Verification` in forma di
elenco — presupposto di questa proposta, non suo sostituto.

La forma che ricorre è una sola: un `Learning target` con due clausole unite da *e* o *o*, la prima
osservata e la seconda no. `CC-7` `S4` — «Che il JSON-LD copra abbastanza food blog … **e** che
un'estrazione sincrona con progress reale sia un'attesa che una persona sopporta senza un passo di
conferma alla fine», e nessuno dei cinque bullet di `Verification` osserva un'attesa o mette davanti
una persona. `CC-6` `S9`, `CC-5` `S7`, `CC-2` `S8`, `manual-run-1` `S3`: identiche.

Il fatto portante di `CC-7` — una clausola sull'attesa sopportabile senza osservazione — è coperto
alla lettera dalla parola *usability* della clausola attuale, quindi **la diagnosi è la forza e non
l'ambito**, e la cura è un tell meccanico, non una regola più larga.

**File — `skills/roadmap/references/slice-rules.md`**, § *Verification maps to the learning target*.
Subito dopo «Checking that data exists does not demonstrate its quality, usability, latency or cost.»
(riga 28-30):

> **A `Learning target` joined by *and* or *or* makes two claims, and the one that goes unobserved is
> the second.** Name, for each, the `Verification` bullet that could come out against it — one bullet
> may answer both — unless the row's `Includes` make the second true by construction. A second claim
> no bullet reaches has two honest exits, and neither is a longer `Verification`: cut it and let the
> row learn one thing, or move it to the row whose evidence already settles it, which is usually the
> row that set the figure it is measured against.

E l'item di `A row holds when` (riga 204), al posto di «every material claim in `Learning target` has
an observation in `Verification`»:

> - every material claim in `Learning target` has an observation in `Verification`, and where two are
>   joined by *and* or *or* the second names the bullet that could come out against it or was cut;

L'uscita economica è **tagliare la clausola**, non gonfiare la `Verification` in un piano di misura:
è la lettura che `ROADMAP-GOAL.md` impone («whatever buys precision at the cost of that sentence is a
non-goal»), ed è quella che il paragrafo mette per prima.

**Chiude:** R-020 in `manual-run-1`, `ROADMAP-CC-2`, `ROADMAP-CC-5`, `ROADMAP-CC-6`,
`ROADMAP-CC-7`.

**Rischia di rompere:** è la proposta più vicina al confine di `ROADMAP-GOAL.md`. Due modi di
sbagliare: righe che diventano piani di misura, e ogni incertezza che si trasforma in uno spike. Se
ne accorgerebbero **R-007 `⚠ opposite`** («every uncertain row turning into a spike. Uncertainty is
the learning target of an ordinary row») e, sul brief, **A9** con **U4**, che licenziano
esplicitamente la misura dentro una riga ordinaria: se dopo il fix U4 uscisse per uno spike, il fix
ha spinto troppo. Il terzo sensore è **R-030** con § *The cap is a finding*, perché claim tagliati
sono righe più strette e quindi più numerose.

**Come si misura:** `slice-rules.md` è letto in ogni sessione, quindi il cambiamento tocca entrambe
le metà di `REVIEW-WORKFLOW.md`; la violazione però si osserva su una mappa disegnata, quindi la
misura è **scenario 0** e i router 1-3 sono il controllo a basso costo che le righe non si siano
assottigliate. Serve un run nuovo.

**Controllo a costo zero, fatto.**
*Contro la riga che l'ha motivato:* prende `CC-7`. Il `Learning target` di `S4` ha due clausole unite
da «e»; la prima ha il bullet «La quota di URL coperti dal solo JSON-LD, su quei dieci, è contata e
scritta», la seconda non ha nessuno dei cinque e gli `Includes` non la rendono vera per costruzione.
L'uscita è tagliarla o spostarla su `S10`, che le persone vere ce l'ha. Prende allo stesso modo
`CC-6` `S9`, `CC-5` `S7`, `CC-2` `S8` e `manual-run-1` `S5`.
*Contro `reference-roadmap/`:* accoppiati clausola e osservazione su tutte e quindici le righe.
**Nessuna riga marcata.** Le cinque che ho guardato da vicino, perché sono il margine: **`S0`** —
«Quanto della catena gratuita si accende davvero senza carta di credito, **e** dove invece serve»,
dove lo stesso bullet («un checkout pulito parte in locale con i soli segreti documentati») può
uscire in entrambe le direzioni, ed è il caso che la clausola ammette con «one bullet may answer
both»; **`S6`** — «tolga davvero dall'MVP email, password e flusso di reset, **e** non li sposti da
un'altra parte», raggiunta da «entrando con un account Google si torna esattamente dove si era»;
**`S8`** — «senza chiamare nessun modello a pagamento», che gli `Includes` rendono vera per
costruzione (nessun modello ci compare) e che la carve-out esclude; **`S11`** — «basti a non avere
volumi **e** a non rompere la macchina che si spegne», dove la seconda metà segue dalla prima e gli
`Includes` la fissano («con nel database il solo URL»); **`S12`** — «**e** che nessuna delle righe
già consegnate debba essere ripensata», raggiunta dal bullet dei due account che esercita le righe
precedenti attraverso l'appartenenza. `S1`, `S3`, `S4`, `S5`, `S7`, `S9`, `S13`, `S14` portano un
claim solo, e `S2` due claim con due cifre riportate.
*Confine noto, e lo dichiaro:* l'innesco è testuale su *and* / *or*, quindi non scatta su una
clausola subordinata — `S10` del riferimento («restando dentro il budget di centesimi per ricetta»,
senza osservazione di costo). Allargarlo al claim singolo marcherebbe `S10` e `S9` del riferimento, e
una clausola che condanna la chiave di risposta è un difetto della clausola. Il tell è più stretto
della regola per costruzione, e prende la forma che ricorre.

### 3.3 — R-012: il recupero dovuto arriva dopo che un altro tema ha aperto

`ok · · ko ok ko ok` — rossa in `ROADMAP-CC-4` e `ROADMAP-CC-6`, verde in `manual-run-1`, `CC-5` e
`CC-7`, *inconclusive* in `CC-2` e `CC-3` (quei report precedono la riscrittura della regola e
leggono la vecchia lista di `Ordering criteria`). Nessun commit l'ha mai presa di mira: `d805196` ha
tolto la sezione che la argomentava e ha riscritto la clausola di conseguenza, ma non è il fix di una
violazione. Nessun commit spiega né il verde di `CC-5` né quello di `CC-7` — i due commit di
`fb29812..3fc0293` prendono i temi — quindi sono varianza fra generazioni e la violazione resta qui.
Entra terza, e non `R-024`, per il criterio dichiarato: due run contro uno.

`CC-6`: `S8` (tema `correzione`) in posizione 9, dopo che `ricerca`, `accesso` e `condivisione` hanno
aperto, mentre lo stato recuperabile nasce con `S3` in posizione 4 e `goal.md:70-71` dichiara l'edit
il recupero del salvataggio senza review.

**Il difetto è che la stessa norma sta in due posti con due inneschi diversi.**
`drawing-the-map.md` § *Ordering for learning* la innesca su un fatto scritto — «**When a row names a
failure mode in its `Verification`** and another `NOW` row is its remedy» — mentre `slice-rules.md`
§ *Splitting and merging a row* la innesca sullo stato: «Deliver a required correction, retry or
escape path **before or with the first behaviour that can create the recoverable state**». Su `CC-6`
il secondo innesco scatta e il primo no, perché nessun bullet di `S3` nomina il salvataggio di
un'estrazione sbagliata come fallimento. Non è ambito mancante: la norma c'è due volte. È l'innesco
ad altitudine d'ordine che non arriva al fatto.

**File — `skills/roadmap/references/drawing-the-map.md`**, § *Ordering for learning*, il secondo dei
quattro punti non soggetti a ranking (righe 201-205). Al posto di «When a row names a failure mode in
its `Verification` and another `NOW` row is its remedy, the remedy comes before a different theme
opens»:

> - **Required recovery outranks breadth.** The remedy comes before a different theme opens, and
>   there are two ways a row asks for one: it names a failure mode in its `Verification` and another
>   `NOW` row is that remedy, or it is the first behaviour that can create a state the sources
>   declare recoverable — a save with no review step, an import that may be wrong — and the
>   correction is a different row. A remedy the sources declare a fallback of a delivered path closes
>   that path; it is not optional depth. Where the sources define a recovery chain, the primary
>   interaction gains its required automatic recovery before a separate manual escape is drawn.

La seconda metà è la frase che `slice-rules.md` già porta, letta all'altitudine dell'ordine invece
che a quella dello split: nessuna norma nuova, un innesco allineato.

**Chiude:** R-012 in `ROADMAP-CC-6` (`S8` nona contro `S3` quarta). **Non** chiude il rilievo di
`ROADMAP-CC-4`, che è l'altra metà della regola — il differenziatore in nona posizione e `S4` seconda
riga del suo tema senza nessuna delle quattro licenze — e che nessun run dopo di lui ripropone.
`CC-7` registra quella metà come tensione fra due clausole non-rankable (*the cheapest real input*
contro *a row that opens a pipeline follows every feeder*) e dà la ragione a nessuna delle due: se
torna rossa, quella è materia della stessa forma di disambiguazione che `6f3ba7b` ha appena
dimostrato sui due test di tema, e non di questa proposta.

**Rischia di rompere:** che ogni riga che scrive qualcosa si porti dietro la sua correzione e la
breadth non apra più — il rovescio esatto della clausola: righe più grasse e temi che restano chiusi.
Se ne accorgerebbe **R-012** stessa nella sua prima metà («deliver one thin row per remaining theme
before a second row from one theme»), e **R-024** («a merge yields one outcome and one learning
target») se la correzione venisse fusa dentro la riga che crea lo stato invece di precederla. Il
freno è nel testo: *before or with*, dove «with» è la fusione e resta ammessa, e l'innesco chiede che
siano **le sorgenti** a dichiarare lo stato recuperabile — non basta che una riga scriva.

**Come si misura:** metà *drawing*, scenario 0. Serve un run nuovo: si legge dall'ordine del
registro, e il validator non guarda l'ordine.

**Controllo a costo zero, fatto.**
*Contro la riga che l'ha motivato:* prende `CC-6`. `goal.md:70-71` dichiara lo stato recuperabile
(«Nessuna review obbligatoria: l'estratto si salva subito. La correzione è sempre disponibile
dopo»), `S3` è la prima riga che lo crea, `S8` è un'altra riga, e fra le due aprono tre temi.
Non marca `CC-7`, che è verde e resta verde: lì il form condiviso di creazione e modifica è `S3`,
posizione 4, e la prima riga che crea uno stato recuperabile è `S4`, che la segue — la forma «with»
della clausola.
*Contro `reference-roadmap/`:* letto l'ordine intero. **Nessuna riga marcata**, e il riferimento è
l'istanza positiva: la prima riga che crea una ricetta d'utente è `S7` *Scrittura e correzione a
mano*, che **è** la correzione, e `S8` (import da URL) la segue. `S3` semina un corpus di prova e non
scrittura d'utente, quindi l'innesco nuovo non ci scatta; `S4`, `S5`, `S6` non creano stato
recuperabile; `S9` è il rimedio del fallimento che `S8` nomina nella propria `Verification` e lo
segue immediatamente, catena che regge già col vecchio innesco; `S10` segue `S9`.

---

**Scartata dalle tre, pur essendo ricorrente:** **R-022** — un bullet di `Includes` che decide un
lato di ciò che la riga dichiara indeciso — rossa in `manual-run-1`, `ROADMAP-CC-2` e
`ROADMAP-CC-4`, ma verde negli ultimi **tre** run consecutivi (`CC-5` `S0`, `CC-6` `S1`/`S4`, `CC-7`
`S0`/`S5`, dove `Includes` e `Verification` dicono «il provider scelto» e «un modello cheap con
output strutturato»). Il ratchet del preambolo è a due run verdi: scriverne una proposta oggi
lavorerebbe contro tre, e su una forma che i run recenti non riproducono più. Torna in lista al primo
run che la ridà rossa.
