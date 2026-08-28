# Miglioramenti — dopo `ROADMAP-CC-5`

Proposte, non implementazioni — **con una eccezione**: il fix di § 2.1 è stato applicato a
`skills/roadmap/references/drawing-the-map.md` in una sessione successiva, perché toglieva un falso
positivo invece di aggiungere una regola. Tutto il resto resta proposta.

Il § 1.1 è stato **riscritto** in una sessione successiva: la prima stesura pesava male i due fatti
che il `REVIEW.md` porta contro la riga e ne ricavava una diagnosi sbagliata. Le guardie che
l'avrebbero presa stanno ora in `prompts/review.prompt.md` e `prompts/improve.prompt.md` — sotto
`evals/` è l'unica cosa toccata oltre a questo file, e alza l'asticella di prova invece di allentare
la rete.

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

`ko` rosso, `ok` verde con la prova nel `REVIEW.md`, `·` non registrata dal run, `(ko)` rosso
registrato dal run ma **non valido** — la regola spara a vuoto, e la cella non conta come ricorrenza.

| Violazione | m-1 | CC-2 | CC-3 | CC-4 | CC-5 | Commit che l'ha presa di mira |
|---|:--:|:--:|:--:|:--:|:--:|---|
| **R-015 / C1** — il lato preso solo in un bullet di riga | ko | ko | ko | ko | ko | nessuno |
| **H5** — React Query assente | ko | ko | ko | ko | ko | nessuno (né l'oracolo lo nomina) |
| **R-015 / C2** — la ragione non regge le citazioni | ok | ko | ko | ok | ko | `e27d419`, `2bf0a12` |
| **R-017 dropped edge** | · | · | ko | ko | (ko) | `2bf0a12`, `7b62754` |
| **R-020** — claim del `Learning target` senza osservazione | ko | ko | · | · | ko | nessuno |
| **R-035** — chiusura oltre le quattro parti | · | ok | ko | ko | ko | nessuno |
| **R-022** — `Includes` che decide ciò che è indeciso | ko | ko | · | ko | ok | nessuno |
| **R-008** — theme compression | ko | ko | · | ko | ok | `ff63c96`, `779bf17` |
| **R-009** — first validator che copre metà promessa | ok | ko | ko | ko | ok | `779bf17` |
| **R-017 published order** | ko | ko | ok | ko | ok | `f77bc61`, `7b62754` |
| **R-017 false edge** (arco sostituibile) | ko | ko | ok | ok | ok | `f77bc61` |
| **R-012** — ampiezza prima di profondità, e ranking | ok | ok | · | ko | ok | nessuno |
| **R-013** — `Assumptions` non registra cosa ignorare | ok | ko | · | ok | ok | nessuno |

Il `(ko)` di `CC-5` è l'unico della tabella: la clausola che lo produce marca come violazione tre
righe del `reference-roadmap`, quindi *dropped edge* resta a **due** rossi su tre run osservati e non
a tre. I rossi di `CC-3` e `CC-4` restano genuini, e sono di due forme diverse fra loro. Vedi § 2.1.

**Fix dimostrati da questo run, e vanno registrati come tali:** `779bf17` (R-008 e R-009 verdi in
`CC-5` dopo tre run rossi di fila su R-009 — la clausola aggiunta è un lookup posizionale, «no first
validator excludes a capability its own theme's promise names», e ha preso al primo run); `7b62754` su
entrambe le forme che lo motivavano — *published order* (`CC-5`: «nessuna cella nomina `S0` o `S1`»)
e la *dropped edge* di `CC-4`, la riga `release` senza prova propria (`CC-5`: `S10` pubblica i suoi
tre archi e il review le dà ragione contro il riferimento), con l'avvertenza che la seconda clausola
colpisce anche righe corrette (§ 2.1); `f77bc61` per la metà *false edge*, verde da tre run; `524e180` per la tracciatura
delle righe di `Assumptions`, mai più rossa dopo `manual-run-1`. Di `79f4a4a` non si può dire niente: nessuna regola di
`EVALUATION-RULES.md` legge l'*ambient restatement*, quindi il suo effetto non è misurato — e la cura,
se serve, cade fuori da `skills/roadmap/`.

## 1. Regressioni

Una sola.

### 1.1 — `R-015` / `C2`: la riga di `Assumptions` sulla ricerca riassegna il soggetto della frase che cita

**Storia.** `e27d419` — *fix violazione C2 di ROADMAP-CC-2* — prende di mira la voce: **id del brief
nel messaggio del commit**. Aggiunge i primi due test («Delivery can refute it», «It lands in a row»),
e `CC-3` mostra che la voce resta rossa per un terzo modo di fallire. `2bf0a12` — **id del brief nel
messaggio**, che apre con «C2, residuo» — aggiunge il terzo test, *Its reason survives its citations*.
Sta in `e27d419..d805196`, quindi è la skill che `ROADMAP-CC-4` ha girato, e `CC-4` la dà **verde**:
la riga `ricerca, S8` legge il divieto come vincolo di costo, che è la lettura che le fonti
sostengono. `ROADMAP-CC-5` la ridà rossa, nella forma esatta di `CC-3`.

**Il fatto portante.** Il `REVIEW.md` di `CC-5` porta due fatti contro la riga `ricerca, S4` e li
lascia allo stesso livello. Li peso qui, e il primo regge da solo.

La riga scrive: «La mappa legge il divieto **come riferito all'LLM e alla ri-indicizzazione del
corpus**». La frase che cita — «Usato solo in fase di add e all'edit, mai a runtime sulle query di
ricerca» — sta dentro `arch-choices.md` § *Embeddings*, e il soggetto di quella sezione è il modello
di embedding. La lettura lascia la frase in piedi e le cambia il soggetto: è una lettura sbagliata,
non un'assunzione, e il divieto parla proprio dell'embedding della query.

Il secondo fatto — `goal.md` § *Vincoli e scala* ripete il divieto nominando LLM ed embedding
insieme, e la riga non lo cita — è **corroborazione** e non regge niente da solo: le due fonti dicono
la stessa cosa, quindi la fonte non citata non aggiunge forza a una smentita che la fonte citata già
porta per intero. La prima stesura di questo § costruiva su questo secondo fatto, e da lì ricavava
una diagnosi di ambito mancante che non esiste.

**Perché il fix precedente ha mancato: giusto, e senza forza.** La clausola non è stata cancellata da
nessun refactor — sta intatta in `references/drawing-the-map.md:257-262` — e **copre già il fatto
portante**: «Read each cited line inside the section that holds it: a reading the cited text will not
bear is a misreading». Manda perfino nel posto esatto, dentro la sezione che tiene la frase. Quel che
non dice è che cosa farci una volta arrivati: la sezione **nomina il soggetto** dell'enunciato, e
quello è un dato da leggere, non un giudizio da formulare. Senza dirlo, la clausola resta una
rilettura a mano, e infatti la riga di `CC-5` la sfiora — cita «poche righe sopra conta il costo
delle query», che è la lettura buona — senza farne il fondamento. Non serve una regola più larga:
serve un tell meccanico dentro quella che c'è.

**Il fix.** File: `skills/roadmap/references/drawing-the-map.md`, § *What the map reports about its
input*, terzo test (righe 257-262). Due frasi dopo la prima; il resto del test non si tocca:

> The section names the subject of what it states, and that is a lookup, not a judgement: a reading
> that leaves the sentence standing and gives it a different subject — the ban is about *that*
> mechanism, not this one — is a misreading however the rest of the sources read. Where sources
> genuinely conflict, the line chooses between them and says which it took; it does not make the
> conflict go away by re-describing what one of them is about.

E l'item di `The map holds when` (righe 306-307) chiude sul lookup:

> - delivery can refute every `Assumptions` line, every reading about how something works lands in a
>   bullet of the row it is traced to, and no reading is contradicted by the lines it cites **or gives
>   one a subject its section does not name**;

**Chiude:** `R-015` / `C2` in `ROADMAP-CC-3` e `ROADMAP-CC-5`; la forma di `ROADMAP-CC-2` resta
chiusa dai due test precedenti, che non si toccano.

**Il controllo a costo zero.** Prima direzione, prende le righe che deve prendere:

- `CC-5`, `ricerca, S4` — lettura «riferito all'LLM e alla ri-indicizzazione del corpus», citazione
  sotto `## Embeddings`. Soggetti diversi: presa.
- `CC-3`, `S4, ricerca` — «si legge il divieto come riferito all'estrazione LLM, non all'embedding
  della query», stessa citazione. Presa.

Seconda direzione, non marca nessuna delle sei righe `Assumptions` di `reference-roadmap/`:

- `ricerca-semantica, S4` — è questa stessa voce, risolta bene: tiene il soggetto («mai embedding a
  runtime»), dichiara che i sorgenti si contraddicono, sceglie la lettura economica. Non presa, ed è
  la riga che il fix deve lasciar passare.
- `inserimento-manuale, S7` — la più vicina al confine: restringe il referente di «lo stesso motore e
  schema» sulla forza del diagramma di `concepts.md`. Restringe l'oggetto di una frase, non ne cambia
  il soggetto, che resta il copia-incolla. Non presa — ed è lei a fissare quanto stretto deve essere
  il tell.
- `S1` (Neon e Supabase intercambiabili), `import-automatico, S9` (copertura del JSON-LD), `S3` + `S4`
  (corpus di seed), `condivisione, S12` (un solo ricettario implicito fino a `S12`) — nessuna prende
  una lettura sul soggetto di un enunciato citato: niente da marcare.

**Rischia di rompere:** il `⚠ opposite` di R-015 — una mappa che, non riuscendo a far reggere nessuna
lettura, pubblica la voce come domanda aperta. Rischio nuovo e specifico di questo testo: che una
restrizione legittima del referente di una frase venga letta come riassegnazione di soggetto e
spedita in `Open questions`. Il caso limite ce l'abbiamo già scritto — `inserimento-manuale, S7` del
riferimento — ed è il controllo da rifare a ogni ritocco della formula. Se ne accorgerebbero **R-015
`⚠ opposite`** e la clausola «Exposing is not resolving», che vieta di pubblicare come indecisa una
voce che una fonte seleziona; sul brief, **A1**–**A3** dicono dove una fonte seleziona e **C2** quale
risoluzione è ammessa.

**Come si misura:** metà *drawing*, scenario 0 (`make eval-cycle`); il file è
`references/drawing-the-map.md`, che quella metà copre per intero. Serve un run nuovo. Il validator
qui non vede niente e un `OK` verde non è evidenza su questa regola.

## 2. Fix che colpisce anche dove non deve

Uno solo, ed è il contrario di quel che il run sembrava dire.

### 2.1 — `R-017` *dropped edge*: la clausola di `7b62754` marca tre righe del riferimento

**Storia.** `2bf0a12` la prende di mira per primo — **id della regola nel messaggio del commit**
(«R-017, overshoot»), con il caso di `CC-3` — e produce il test sintattico su `Includes` (tabella,
migrazione, resolver, adapter). `ROADMAP-CC-4` resta rosso in un'altra forma: `S11`, riga `release`
con `—`, la cui `Verification` è fatta *tutta* di capacità che `S10`, `S5` e `S8` consegnano.
`7b62754` — *Fix R-017 both ways: no edge to a prerequisite, and read `Verification`* — implementa
quella diagnosi estendendo la lettura a `Verification`, ed è in `d805196..37a0976`, quindi è la skill
che `ROADMAP-CC-5` ha girato. `CC-5` risulta rosso una terza volta: `roadmap.md` *NOW*, riga `S5`,
`Depends on: S3`, mentre l'ultima frase della sua `Verification` — «Le ricette salvate qui compaiono
nella ricerca di `S4`» — nomina una capacità che `S4` consegna.

**Quel rosso non regge, e il riferimento lo dimostra.** `S5` salva «verso la stessa forma di `Recipe`
che `S3` persiste»; l'hook di embedding che `S4` installa sta su quel percorso di scrittura, quindi
`S5` lo eredita senza costruirci sopra niente. La frase è un controllo di non-bypass, non l'esercizio
di una capacità che serve alla riga per esistere. Il `reference-roadmap` fa la stessa cosa in tre
righe, e in nessuna pubblica l'arco verso la ricerca:

| Riga del riferimento | `Depends on` | Frase di `Verification` |
|---|---|---|
| `S7` scrittura a mano | `S3` | «la si ritrova **cercandola** a parole proprie … e la **ricerca** segue la modifica» |
| `S8` import da URL | `S3` | «la ricetta si salva senza altri passaggi **e la si trova cercandola**» |
| `S10` copia-incolla | `S9` | «la ricetta si salva, **e la si trova cercandola**» |

`S4` (ricerca) precede tutte e tre nel registro del riferimento, e `S8` è l'analogo diretto di `S5`:
stessa riga, stesso tema, stessa frase. La clausola aggiunta da `7b62754` — «Read the dependent's
`Verification` as well as its `Includes`. Where the evidence that a row is done exercises a capability
another `NOW` row delivers … the row does not carry `—`» — marca quindi come violazione tre righe
della chiave di risposta. È il criterio del preambolo di `EVALUATION-RULES.md` per una regola che
sbaglia, non per una mappa che sbaglia.

**`7b62754` ha preso, e ha colpito troppo.** Le tre istanze rosse sono di tre forme, non di una:

- `CC-3` — `S4` con `Depends on: S2` mentre il suo `Includes` costruisce sulla tabella `recipe`,
  sulla migrazione e sul resolver `currentCookbook` che `S3` consegna. **Genuina**, ed è la forma che
  il test sintattico di `2bf0a12` chiude; `CC-3` la precede.
- `CC-4` — `S11`, riga `release` con `—` e nessuna prova propria. **Genuina**, ed è la forma che
  `7b62754` chiude: in `CC-5` `S10` pubblica i suoi tre archi e il review le dà ragione contro il
  riferimento.
- `CC-5` — `S5`, prova locale più una frase a valle. **Falso positivo**, per il confronto qui sopra.

**Perché colpisce troppo.** Il testo chiede se la `Verification` *nomina* una capacità altrui. La domanda che
separa `S11` da `S5` è un'altra: se la riga **può essere costruita** prima che quella capacità esista.
`S11` non ha prova propria — tolte le capacità altrui non resta niente da osservare, e la riga non
esiste. `S5` ha una prova locale e una clausola che guarda a valle: spostata `S4` dopo `S5`, quella
clausola si sposta o cade e non si rompe nient'altro. È esattamente la differenza fra dipendenza e
ordine per cui il campo `Depends on` esiste, e pubblicarla direbbe il falso — che l'import non si può
costruire prima della ricerca.

**Il fix — applicato.** Il binario «publish the edge, or cut the
sentence» obbligherebbe il riferimento a pubblicare tre archi falsi o a cancellare tre frasi di prova
legittime: va scartato. Serve invece restringere la clausola di `7b62754`. File:
`skills/roadmap/references/drawing-the-map.md`, § *Hard dependencies*, il paragrafo alle righe 98-103.
Al posto del testo attuale:

> Read the dependent's `Verification` as well as its `Includes`, and ask of it the same question:
> could this row be built before that capability exists? Where the evidence that a row is done is
> *made of* capabilities other `NOW` rows deliver — a `kind: release` row has no proof of its own —
> nothing controlled stands in, and the row publishes the row its evidence enters through, not one
> edge per capability the evidence touches. Where a row's proof stands on its own and one clause
> reaches downstream to observe that what the row produces arrives somewhere else, that clause is
> order: a reorder moves it or drops it and breaks nothing, and publishing the edge would claim the
> row cannot be built first, which is false.

E l'item di `The map holds when` (righe 290-293) torna a nominare la prova, non la menzione:

> - every published `Depends on` survives the substitution test — no controlled input and no narrower
>   real precursor already in `NOW` can stand in — and no row that builds on a table, resolver or
>   adapter another `NOW` row delivers, **or whose evidence is made of capabilities other `NOW` rows
>   deliver**, carries `—`;

**Chiude:** il falso positivo di `ROADMAP-CC-5`, e lascia in piedi i due test che prendono le istanze
genuine — quello su `Includes` di `2bf0a12` per `CC-3`, e la prima frase per `S11` di `CC-4`. Del
primo va detto che resta *presunto*: nessun run dopo `2bf0a12` ha riprodotto quella forma, quindi non
è mai stato osservato verde.

**Rischia di rompere:** che una riga di rilascio scritta con una singola frase di prova apparentemente
locale si sottragga alla clausola. Se ne accorgerebbe **R-017 `⚠ failed`** nella metà *dropped edge*,
e il controllo a basso costo è sintattico: nessuna riga `kind: release` porta `—` **tranne lo
scheletro**, che è il rilascio che non ha ancora niente a monte. Il secondo rischio
è di leggere «that clause is order» come licenza a scrivere `Verification` che sconfinano ovunque: lo
prende **R-023** (*fake verticality*), perché una prova che vive a valle non è la prova di questa
riga.

**Come si misura:** metà *drawing*, scenario 0, e serve un run nuovo per sapere se la clausola
ristretta continua a prendere le due forme genuine. Il controllo che il fix stesso prescrive è però a
costo zero, ed è stato fatto al momento di applicarlo: riletta contro `reference-roadmap/`, la
clausola nuova non marca nessuna delle sue quindici righe. Le quattro righe con `—` (`S0`, `S1`, `S2`,
`S6`) hanno prova propria; `S7`, `S8` e `S10` cadono ora sotto «that clause is order»; `S14`, riga
`release` la cui prova è fatta di capacità altrui, pubblica il suo arco (`S12`) ed è presa
correttamente. È il test che `7b62754` non aveva fatto.

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
