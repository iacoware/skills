# Miglioramenti — dopo `ROADMAP-CC-5`

Proposte, non implementazioni. Niente sotto `skills/` è stato toccato in questa sessione, e niente
sotto `evals/` oltre a questo file. Git è stato solo letto.

## Dove cade ogni run nella storia della skill

| Run | Ancoraggio | `skills/roadmap` tree | Fonte dell'ancoraggio |
|---|---|---|---|
| `manual-run-1` | `dcf783d` | `ed75429` | **inferito** — commit che aggiunge `results/manual-run-1/.roadmap` |
| `ROADMAP-CC-2` | `666566d` | `eedf170` | dichiarato in `PROMPT.md` (ricostruito dal transcript) |
| `ROADMAP-CC-3` | `e27d419` | `028f3b4` | dichiarato in `PROMPT.md` (ricostruito dal transcript) |
| `ROADMAP-CC-4` | `d805196` | `2f1d0db` | dichiarato in `PROMPT.md` (ricostruito dal transcript) |
| `ROADMAP-CC-5` | `37a0976` | `0913e60` | dichiarato in `PROMPT.md`, **scritto prima dell'invio** |

Cinque tree distinti: nessuna coppia di run mette alla prova la stessa skill, e ogni intervallo porta
almeno un cambiamento reale. I commit dentro ciascun intervallo, tutti letti:

- `dcf783d..666566d` — `18968aa` (ripuntamenti), `524e180` (tag `goal` legale su una riga di
  `Assumptions`), `676b580` + `666566d` (refactoring S2/S3: `SKILL.md` diventa router a due porte,
  `drawing-the-map.md` si carica sulla sola `Drawing`).
- `666566d..e27d419` — `f77bc61` (*Fix violation of R-17*: test di sostituzione e *published order*),
  `e27d419` (C2: i primi due test su una riga di `Assumptions`, e lo sweep dei conflitti anche dentro
  un singolo documento).
- `e27d419..d805196` — `2bf0a12` (terzo test, *Its reason survives its citations*; **dropped edge**
  come specchio di *published order*), `ff63c96` (verdetto di tema a una riga, con slot nel template),
  `d805196` (rimozione di `Ordering criteria` dal formato).
- `d805196..37a0976` — `779bf17` (*Catch theme compression where it leaves a trace*: «A promise names
  only what its first validator delivers»), `79f4a4a` (concern pubblicato solo dove una riga poteva
  fare altrimenti), `7b62754` (*Fix R-017 both ways*, che implementa le proposte 1.1 e 2.1 di
  `ROADMAP-CC-4/IMPROVEMENTS.md`).

**Ancoraggio inferito solo per `manual-run-1`**, ed è il confine `dcf783d`: è la data del commit che
ne aggiunge la mappa, non la versione che ha girato. Sotto non ci fondo nessuna delle voci delle prime
due categorie.

**Le tre proposte «mai risolte» del ciclo precedente non sono state implementate** — nessun commit di
`d805196..37a0976` tocca § *What the map reports about its input*, § `readiness` di `slice-rules.md`
né § *Ordering for learning*. Quel che segue non le ricicla alla lettera: le riscrive dove `CC-5` dà
evidenza nuova, e ne scarta una.

## Che cosa ricorre

`ko` rosso, `ok` verde con la prova nel `REVIEW.md`, `·` non registrata dal run.

| Violazione | m-1 | CC-2 | CC-3 | CC-4 | CC-5 | Commit che l'ha presa di mira |
|---|:--:|:--:|:--:|:--:|:--:|---|
| **R-015 / C1** — il lato preso solo in un bullet di riga | ko | ko | ko | ko | ko | nessuno |
| **H5** — React Query assente | ko | ko | ko | ko | ko | nessuno (né l'oracolo lo nomina) |
| **R-015 / C2** — la ragione non regge le citazioni | ok | ko | ko | ok | ko | `e27d419`, `2bf0a12` |
| **R-017 dropped edge** | · | · | ko | ko | ko | `2bf0a12`, `7b62754` |
| **R-020** — claim del `Learning target` senza osservazione | ko | ko | · | · | ko | nessuno |
| **R-035** — chiusura oltre le quattro parti | · | ok | ko | ko | ko | nessuno |
| **R-022** — `Includes` che decide ciò che è indeciso | ko | ko | · | ko | ok | nessuno |
| **R-008** — theme compression | ko | ko | · | ko | ok | `ff63c96`, `779bf17` |
| **R-009** — first validator che copre metà promessa | ok | ko | ko | ko | ok | `779bf17` |
| **R-017 published order** | ko | ko | ok | ko | ok | `f77bc61`, `7b62754` |
| **R-017 false edge** (arco sostituibile) | ko | ko | ok | ok | ok | `f77bc61` |
| **R-012** — ampiezza prima di profondità, e ranking | ok | ok | · | ko | ok | nessuno |
| **R-013** — `Assumptions` non registra cosa ignorare | ok | ko | · | ok | ok | nessuno |

**Fix dimostrati da questo run, e vanno registrati come tali:** `779bf17` (R-008 e R-009 verdi in
`CC-5` dopo tre run rossi di fila su R-009 — la clausola aggiunta è un lookup posizionale, «no first
validator excludes a capability its own theme's promise names», e ha preso al primo run); `7b62754`
per la metà *published order* (`CC-5`: «nessuna cella nomina `S0` o `S1`»); `f77bc61` per la metà
*false edge*, verde da tre run; `524e180` per la tracciatura delle righe di `Assumptions`, mai più
rossa dopo `manual-run-1`. Di `79f4a4a` non si può dire niente: nessuna regola di
`EVALUATION-RULES.md` legge l'*ambient restatement*, quindi il suo effetto non è misurato — e la cura,
se serve, cade fuori da `skills/roadmap/`.

## 1. Regressioni

Una sola.

### 1.1 — `R-015` / `C2`: la ragione della riga di `Assumptions` sulla ricerca torna smentita dalle sue fonti

**Storia.** `e27d419` — *fix violazione C2 di ROADMAP-CC-2* — prende di mira la voce: **id del brief
nel messaggio del commit**. Aggiunge i primi due test («Delivery can refute it», «It lands in a row»),
e `CC-3` mostra che la voce resta rossa per un terzo modo di fallire. `2bf0a12` — *Ripara i due fix
della sessione precedente*, il cui messaggio apre con «C2, residuo»: **id del brief nel messaggio** —
aggiunge il terzo test, *Its reason survives its citations*, con dentro la frase scritta per il caso di
`CC-3`: «Where two sources state a constraint together, splitting them needs a source that splits
them». Sta in `e27d419..d805196`, quindi è la skill che `ROADMAP-CC-4` ha girato, e `CC-4` la dà
**verde**: la riga `ricerca, S8` legge il divieto come vincolo di costo, che è la lettura che il brief
non falsifica. `ROADMAP-CC-5` la ridà rossa, nella forma esatta di `CC-3`: la riga `ricerca, S4` legge
il divieto «come riferito all'LLM e alla ri-indicizzazione del corpus», cita `arch-choices.md`
§ *Embeddings* — dove il soggetto sono gli embedding — e **non cita** `goal.md` § *Vincoli e scala*,
che ripete lo stesso divieto nominando i due insieme.

**Perché il fix precedente ha mancato: giusto, ma con l'ambito sbagliato.** La clausola non è stata
cancellata da nessun refactor — sta intatta in `references/drawing-the-map.md:251-256`, e la checklist
porta il suo item («no reading is contradicted by the lines it cites», riga 301). Il difetto è che il
test è scritto **sulle citazioni che la riga già porta**: «Read each cited line inside the section that
holds it». Una riga che non cita la fonte che la refuterebbe passa il test in silenzio, ed è
esattamente ciò che `CC-5` ha fatto. La diagnosi di `2bf0a12` veniva da `CC-3`, dove la lettura
sbagliata stava *dentro* il testo citato; la classe di fallimento include anche la scelta della
citazione, e lì il test non arriva. Vale la pena notare che la clausola aveva persino anticipato
l'esito — «the one the sources support is usually a few lines from the quote already taken» — e `CC-5`
la sfiora («poche righe sopra conta il costo delle query») senza farne il fondamento: la regola è
giusta e non ha forza, perché resta una lettura da fare dopo, senza nessun tell meccanico.

**Il fix.** File: `skills/roadmap/references/drawing-the-map.md`, § *What the map reports about its
input*, terzo test (righe 251-256). Al posto del testo attuale:

> - **Its reason survives its citations, and the citations are all of them.** Read each cited line
>   inside the section that holds it: a reading the cited text will not bear is a misreading, not an
>   assumption, and delivery cannot refute what the sources already refuted. Before the line is
>   written, look for every other place the sources state the same constraint — the tell is
>   mechanical: the constraint's own words, searched across the sources rather than inside the
>   document the reading came from. A line that cites one statement and takes a reading another
>   refuses has chosen its evidence, and a source the line does not cite refutes it just as well.
>   Where two sources state a constraint together, splitting them needs a source that splits them.
>   When the text will not bear the reading, either the entry is still open or another reading is
>   available — and the one the sources support is usually a few lines from the quote already taken.

E l'item di `The map holds when` (righe 300-301) chiude sul punto in cui la regola perde:

> - delivery can refute every `Assumptions` line, every reading about how something works lands in a
>   bullet of the row it is traced to, and no reading is contradicted by the lines it cites **or by
>   another statement of the same constraint the line leaves uncited**;

**Chiude:** `R-015` / `C2` in `ROADMAP-CC-3` e `ROADMAP-CC-5`; la forma di `ROADMAP-CC-2` resta chiusa
dai due test precedenti, che non si toccano.

**Rischia di rompere:** il `⚠ opposite` di R-015 — una mappa che, non riuscendo a far reggere nessuna
lettura, pubblica la voce come domanda aperta. Il testo lo argina con «either the entry is still open
or another reading is available», ma la spinta esiste. Se ne accorgerebbe **R-015 `⚠ opposite`»** e la
clausola «Exposing is not resolving», che vieta di pubblicare come indecisa una voce che una fonte
seleziona; sul brief, le voci **A1**–**A3** dicono dove una fonte seleziona e quindi l'uscita per
`Open questions` sarebbe sbagliata, e **C2** dice quale risoluzione è ammessa. Rischio secondario:
righe di `Assumptions` che diventano rassegne di citazioni — lo prenderebbe il primo test, «A line
restating what a source already says is true by construction», e il vincolo di
`ROADMAP-GOAL.md` contro il campo che nessuno rilegge.

**Come si misura:** metà *drawing*, scenario 0 (`make eval-cycle`); il file è
`references/drawing-the-map.md`, che quella metà copre per intero. Serve un run nuovo. Il validator qui
non vede niente e un `OK` verde non è evidenza su questa regola.

## 2. Fix che non hanno preso

Uno solo.

### 2.1 — `R-017` *dropped edge*: `S5` porta `Depends on: S3` e la sua `Verification` esercita `S4`

**Storia.** `2bf0a12` la prende di mira per primo — **id della regola nel messaggio del commit**
(«R-017, overshoot»), con il caso di `CC-3` — e produce il test sintattico su `Includes` (tabella,
migrazione, resolver, adapter). `ROADMAP-CC-4` resta rosso, e il ciclo precedente diagnostica il
motivo: il fallimento di `CC-4` stava in `Verification` e non in `Includes`. `7b62754` — *Fix R-017
both ways: no edge to a prerequisite, and read `Verification`* — implementa quella diagnosi:
**id della regola nel messaggio**, ed è in `d805196..37a0976`, quindi è la skill che `ROADMAP-CC-5` ha
girato. È il solo run dopo di lui, ed è di nuovo rosso: `roadmap.md` *NOW*, riga `S5`,
`Depends on: S3`, mentre l'ultima frase della sua `Verification` — «Le ricette salvate qui compaiono
nella ricerca di `S4`» — esercita una capacità che `S4` consegna. Nessun run dopo `2bf0a12` ha mai
dato verde questa metà della regola.

**Perché il fix precedente ha mancato: la deroga scritta nello stesso respiro se lo mangia.** Il
paragrafo di `7b62754` (`drawing-the-map.md:98-103`) dice la cosa giusta nella prima frase e poi la
limita: «What it publishes is the row its evidence enters through, not one edge per capability the
evidence touches», con l'esempio della riga `kind: release`. La deroga è stata scritta per l'istanza
che aveva — `S11` di `CC-4`, riga di rilascio la cui prova è *tutta* fatta di capacità altrui — e su
quella metà **ha preso**: `S10` di `CC-5` pubblica i suoi tre archi e il review le dà ragione contro
il riferimento. Applicata a una riga la cui prova è locale tranne una frase, la stessa deroga si legge
come licenza a scartare la frase periferica, che è precisamente quel che `S5` fa. La diagnosi era
giusta sul campo (`Verification` e non `Includes`) e sbagliata sulla forma del fallimento: il test
distingue per *quanto pesa* la prova che sconfina, e il fallimento non ha peso, ha una frase.

**Il fix.** Stesso file e stessa sezione, `drawing-the-map.md` § *Hard dependencies*, in coda al
paragrafo delle righe 98-103, sostituendo l'ultima frase con un binario invece che con una misura di
centralità:

> A sentence of `Verification` that names what another `NOW` row delivers is either an edge or is not
> evidence: publish the edge, or cut the sentence. A row whose proof leans on a capability it does not
> name is the reorder that breaks with nobody noticing, and a proof nobody would miss was decoration.
> What a row publishes is the row its evidence enters through, never one edge per capability the
> evidence touches — that bounds **how many** edges a row carries, never **whether** it carries one: a
> `kind: release` row, whose whole evidence is other rows' capabilities exercised end to end, names the
> row its evidence enters through; an ordinary row that reaches out in a single clause names that row
> or drops the clause.

**Chiude:** `R-017` *dropped edge* in `ROADMAP-CC-3`, `ROADMAP-CC-4` e `ROADMAP-CC-5`. Copre anche la
lettura contraria che `CC-5` registra — l'asserzione di `S5` è marginale e si potrebbe togliere: il
binario dice che togliere è l'altra uscita legittima, e chiude comunque il buco.

**Rischia di rompere:** *published order*, che è l'oscillazione da cui questa coppia nasce — una
`Verification` scritta larga fa nascere archi che il test di sostituzione non chiedeva. Se ne
accorgerebbe **R-017 `⚠ opposite`** nella direzione opposta (pubblicare tre archi di troppo costa meno
di un arco caduto, quindi il rischio è accettato e non nullo), e il lookup di `7b62754` che resta —
«no `Depends on` cell names the repository row or the skeleton» — taglia i candidati più numerosi. Il
secondo rischio è che una sessione tagli le frasi di `Verification` invece di pubblicare gli archi,
impoverendo la prova: lo prenderebbe **R-020**, perché una `Verification` accorciata lascia scoperto un
claim del `Learning target`, e **R-023** (*fake verticality*) dove il taglio sostituisce il percorso
reale.

**Come si misura:** metà *drawing*, scenario 0. Serve un run nuovo, ed è lo stesso della proposta 1.1:
i due file toccati sono lo stesso, e le due regole non interferiscono.

## 3. Mai risolte

Tre proposte, nell'ordine in cui le farei. Il criterio è la ricorrenza.

**Prima, che cosa resta fuori.**

- **H5** (5/5) si scarta perché la cura cade fuori da `skills/roadmap/`: nessuna clausola della skill
  obbliga una mappa a enumerare lo stack, e quattro review su cinque registrano che nemmeno
  `reference-roadmap/` nomina React Query. `CC-5` aggiunge il sospetto giusto — il difetto potrebbe
  stare nella granularità di H5. È materia del brief, non di questo report.
- **La sovrapposizione `R-021` / `R-011`** — la riga di repository è `enabler` e fallisce il test
  dell'enabler — è segnalata da quattro review su cinque, e la sua cura *cadrebbe* dentro
  `slice-rules.md` § *The columns* → `kind`. Non entra fra le tre perché nessun run la conta rossa:
  per il preambolo di `EVALUATION-RULES.md` è una clausola che dice due cose che si sovrappongono, e
  non compete con tre violazioni che sono rosse.
- **`R-008` e `R-009`** escono dalla lista: `779bf17` li ha chiusi e `CC-5` lo dimostra. Un secondo
  intervento sarebbe lavoro contro un verde.
- **`R-012`** resta con un solo run rosso (`CC-4`, subito dopo la rimozione di `Ordering criteria`) e
  `CC-5` verde con la deroga unica leggibile dalla riga. Il debito che `d805196` si era lasciato dietro
  è pagato: un run ha mostrato che l'ordine regge senza la sezione.

### 3.1 — `R-015` / `C1`: il conflitto risolto dentro una riga e riportato da nessuna parte

**Cinque run su cinque, ed è l'unica a punteggio pieno.** Il lato di C1 è stato preso in `S6 Excludes`
(m-1), `S3 Includes` (CC-2, CC-4), `S3 Excludes` (CC-3, CC-5), e nessuna riga di `Assumptions`, nessuna
di `Open questions` e nessuno spike lo dice mai.

**File:** `skills/roadmap/references/drawing-the-map.md`, § *What the map reports about its input*,
subito dopo il terzo exit (riga 236) e prima di «Exposing is not resolving».

La norma c'è — «Every entry then leaves by one of three exits, and no other» — e non ha tracciato. Si
aggiunge quello, nella forma che `779bf17` ha appena dimostrato: una lettura che diventa un lookup.

> **Taken in a row and nowhere else** is the failure to watch for, and its tell is mechanical: a bullet
> of `Includes` or `Excludes` picks one side of a conflict the sweep found, and no line of
> `Assumptions`, no line of `Open questions` and no spike names that entry. The bullet is where the
> reading is *applied*, never where it is *reported*, and a reader who finds only the bullet cannot
> tell a decision from an oversight. A neighbouring row that shares the schema, the pipeline or the
> form is not the report either: it says what was built, not which side was taken and why.

E l'item di `The map holds when` (riga 298) passa da una lettura a un lookup:

> - every conflict and every undecided choice left the sweep by one of the three exits, and no side of
>   one was taken only in a row's `Includes` or `Excludes`;

Nessun campo nuovo e nessuna sezione nuova: una mappa che non aveva niente da riportare non cresce di
una riga. La seconda frase è nuova rispetto alla proposta del ciclo precedente, e viene da `CC-5`, dove
la conciliazione parziale (`S6` che condivide lo `Schema` con `S5`) è stata presa per la riga dovuta.

**Chiude:** `C1` / `R-015` in `manual-run-1`, `ROADMAP-CC-2`, `ROADMAP-CC-3`, `ROADMAP-CC-4`,
`ROADMAP-CC-5`.

**Rischia di rompere:** il `⚠ opposite` di R-015 — una mappa che non prende nessuna lettura e pubblica
tutto come domanda aperta. Il testo spinge a *riportare* la lettura, non a smettere di prenderla, ma
una sessione può leggerlo come «nel dubbio, `Open questions`». Se ne accorgerebbe **R-015** stessa, che
è scritta in entrambe le direzioni, e sul brief le voci **A1**–**A3**, che dicono dove una fonte
seleziona e quindi non c'è niente da riportare.

**Come si misura:** metà *drawing*, scenario 0. Serve un run nuovo, e su questa ne servono davvero
**due**: è l'unica a 5/5, e un run solo è una domanda.

### 3.2 — `R-020`: il claim che la consegna non può smentire perché la prova è scelta per confermarlo

**File:** `skills/roadmap/references/slice-rules.md`, § *Verification maps to the learning target*
(righe 26-30).

Rossa in `manual-run-1` (`S3`, `S5`), in `ROADMAP-CC-2` (cinque righe) e in `ROADMAP-CC-5` (`S5`, `S7`,
`S9`), discussa e non contata in `CC-3` e `CC-4`. Nessun commit l'ha mai presa di mira.

Il ciclo precedente l'aveva scartata perché il *singolare* di R-020 si pesta i piedi con l'obbligo di
R-013. Le tre istanze di `CC-5` sono di un'altra metà della regola, e quella sovrapposizione non le
tocca: l'osservazione **c'è** ed è scelta in modo da non poter uscire diversamente. `S5` afferma «se il
solo JSON-LD copre abbastanza pagine reali» e verifica su «tre URL veri **che espongono JSON-LD**»;
`S9` afferma che la parità fra membri «regge all'uso vero» e verifica su due account Google di prova;
`S7` afferma un rischio sul budget di richiesta e non lo osserva affatto. È la metà misurabile della
regola, ed è quella che ricorre.

La clausola oggi si ferma a «Checking that data exists does not demonstrate its quality, usability,
latency or cost». Si aggiunge, subito dopo:

> **A claim about how often, how many or how well is refutable only when the evidence could have come
> out the other way.** Where the `Verification` picks its input by the property the claim is about —
> pages known to carry the data, accounts the team owns, a corpus assembled around the answer — it can
> confirm and never refute, and the row has proved its pipeline instead of its claim. Name the input
> the claim would fail on, or narrow the `Learning target` to what this row's evidence can actually
> settle and let the claim travel to the row that runs on real input.

E l'item di `A row holds when` (riga 204):

> - every material claim in `Learning target` has an observation in `Verification`, and no observation
>   runs on input selected by the property the claim measures;

**Chiude:** `R-020` in `manual-run-1`, `ROADMAP-CC-2`, `ROADMAP-CC-5`. In `CC-3` e `CC-4` la stessa
forma è registrata come discussione e non come rosso, quindi non la conto.

**Rischia di rompere:** è la proposta che sta più vicina al confine di `ROADMAP-GOAL.md`, e va letta
per come è scritta — l'uscita economica è **restringere il claim**, non gonfiare la `Verification` in
un disegno sperimentale. I due modi in cui potrebbe comprare precisione finta: righe che diventano
piani di misura, e ogni incertezza che si trasforma in uno spike. Se ne accorgerebbero **R-007
`⚠ opposite`** («every uncertain row turning into a spike. Uncertainty is the learning target of an
ordinary row») e, sul brief, **A9** con **U4**, che licenziano esplicitamente una misura dentro una
riga ordinaria: se dopo il fix U4 uscisse per uno spike, il fix ha spinto troppo. Il cap
(**R-030**, e § *The cap is a finding*) è il terzo sensore, perché righe più strette sono righe più
numerose.

**Come si misura:** `slice-rules.md` è letto in ogni sessione, quindi il cambiamento tocca entrambe le
metà di `REVIEW-WORKFLOW.md`; la violazione però si osserva solo su una mappa disegnata, quindi la
misura è scenario 0 e i router 1-3 sono il controllo a basso costo che le righe non si siano
assottigliate. Serve un run nuovo.

### 3.3 — `R-035`: il messaggio di chiusura si apre sul validator

**File:** `skills/roadmap/SKILL.md`, § *5. Close the session* (righe 172-195) e l'ultimo item di
*The session holds when* (righe 223-224).

Rossa in `ROADMAP-CC-3`, `ROADMAP-CC-4` e `ROADMAP-CC-5`, tre run consecutivi, sempre nella stessa
forma: una riga di stato del validator **prima** delle quattro parti — «Validatore: `OK`, nessun ERROR
né WARNING» (CC-3), «Mappa scritta e validata (`OK`, nessun warning).» (CC-4 e CC-5). Nessun commit
l'ha mai presa di mira. In tutti e tre i run le quattro parti ci sono e nell'ordine, e in `CC-5` la
domanda dovuta sta correttamente dopo: quel che ricorre è solo l'apertura.

**Perché atterra in `SKILL.md`, in deroga al default.** *Close the session* non ha un file in
`references/`: il passo del validator e il report a quattro parti sono due clausole della stessa
sezione, e la skill dichiara da sé che la sessione è l'altitudine che `SKILL.md` possiede («One
checklist per altitude … the session here»). La sovrapposizione è fra R-033 — si deve vedere che il
validator ha girato — e R-035 — quattro parti e nient'altro; `CC-4` la nomina come tale. È il caso che
il preambolo di `EVALUATION-RULES.md` chiama *a clause saying two things that overlap*, e la cura è
disambiguare, non aggiungere.

Al passo del validator (dopo riga 183) si aggiunge dove finisce il suo esito:

> A clean run reports nothing: the validator's only output to the author is a `WARNING`, and it goes
> after the four parts with anything else the session owes. That it ran at all is visible in the
> session, not in the message.

E l'apertura del report (riga 185) diventa esplicita su cosa viene per primo:

> **Then report the written map, and nothing else.** The `Themes` table is the first thing in the
> message — no preamble, and in particular no line saying the map was written and validated, which is
> the narration of an operation and is what the author can already see. Four things, in this order,
> read off the files as they now stand:

L'item di *The session holds when* (righe 223-224):

> - the session closed on the four-part report — themes, register, open questions, path — with nothing
>   before it and only what it owes after it.

**Chiude:** `R-035` in `ROADMAP-CC-3`, `ROADMAP-CC-4`, `ROADMAP-CC-5`.

**Rischia di rompere:** che una sessione, per non narrare, smetta di riportare un `WARNING` dovuto o
una domanda che ha prodotto — cioè la metà solida del rosso di `CC-3`, dove due domande dovute non sono
mai arrivate all'autore. Se ne accorgerebbero **R-033** («every `WARNING` put to the author rather than
silenced») e **R-035** stessa, che vuole la domanda dopo le quattro parti e non al posto loro. Il
secondo rischio è di leggere il silenzio sul validator come licenza a non girarlo: R-033 legge il
transcript e non il messaggio — «What this reads is that it ran and what it did with the `WARNING`s» —
quindi il sensore resta intatto.

**Come si misura:** metà *drawing*, scenario 0, che `REVIEW-WORKFLOW.md` indica per un cambiamento a
*Close the session*. Serve un run nuovo, e il rilievo si legge nel `TRANSCRIPT.jsonl`, non in
`.roadmap/`.

---

**Scartata dalle tre, pur essendo ricorrente:** `R-022` — `Includes` che decide un lato di ciò che la
riga dichiara indeciso — rossa in `manual-run-1`, `ROADMAP-CC-2` e `ROADMAP-CC-4`, ma **verde in
`ROADMAP-CC-5`**, dove `S0` è `needs-decision` e sia `Includes` sia `Verification` dicono «il provider
scelto». Nessun commit spiega quel verde, quindi è varianza e la violazione resta *mai risolta*; ma la
proposta scritta il ciclo scorso è tarata su una forma che il run più recente non riproduce, e
scriverne una seconda al buio costa più di quel che compra. Torna in lista al primo run che la ridà
rossa.
