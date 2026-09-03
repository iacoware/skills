# Miglioramenti — dopo `ROADMAP-CC-6`

Sei run letti (`manual-run-1`, `ROADMAP-CC-2` … `ROADMAP-CC-6`) e la storia di `skills/roadmap` fra
gli ancoraggi che i loro `PROMPT.md` dichiarano. Nessun file di `skills/` è stato toccato; qui ci
sono proposte.

## Dove cade ogni run nella storia della skill

| Run | Commit | tree `skills/roadmap` | Come è ancorato |
|---|---|---|---|
| `manual-run-1` | `dcf783d` | `ed75429` | **inferito** — commit che aggiunge la mappa, più l'indizio del layout del template; il suo `PROMPT.md` dichiara l'inferenza e il modo in cui cade |
| `ROADMAP-CC-2` | `666566d` | `eedf170` | ricostruito dal transcript, e concorde con l'inferenza a buon mercato |
| `ROADMAP-CC-3` | `e27d419` | `028f3b4` | dichiarato |
| `ROADMAP-CC-4` | `d805196` | `2f1d0db` | dichiarato |
| `ROADMAP-CC-5` | `37a0976` | `0913e60` | dichiarato |
| `ROADMAP-CC-6` | `fb29812` | `0d47a59` | dichiarato |

Sei tree distinti: nessuna coppia di run ha girato la stessa skill. I commit che ciascun run mette
alla prova, letti tutti:

| Intervallo | Commit su `skills/roadmap` | Che cosa prendono di mira |
|---|---|---|
| `dcf783d..666566d` (→ CC-2) | `18968aa`, `524e180`, `676b580`, `666566d` | ripuntamenti; il tag `goal` per una riga di `Assumptions` a quota mappa (R-015 di `manual-run-1`); le sessioni S2 e S3 del refactoring |
| `666566d..e27d419` (→ CC-3) | `f77bc61`, `e27d419` | R-017; C2 |
| `e27d419..d805196` (→ CC-4) | `2bf0a12`, `ff63c96`, `d805196` | C2 (terzo test) e R-017 *dropped edge*; formato del verdetto di tema; rimozione di `Ordering criteria` |
| `d805196..37a0976` (→ CC-5) | `779bf17`, `79f4a4a`, `7b62754` | R-008/R-009; `Cross-functional concerns`; R-017 in entrambe le direzioni |
| `37a0976..fb29812` (→ CC-6) | `f569dce`, `f25c8d9`, `8eb3a71`, `d8bc79d` | R-017 *dropped edge* ristretto; C2 (soggetto come lookup); C1 (tell del lato preso in un bullet); `Verification` in forma di elenco |

Dove l'ancoraggio di `manual-run-1` è inferito, il confine con `ROADMAP-CC-2` è l'unica cosa che ci
pende, e nessuna attribuzione di questo report ci si regge sopra: i quattro commit di quell'intervallo
non prendono di mira nessuna delle violazioni proposte qui.

## Che cosa ricorre

`ok` verde, `ko` rosso, `·` non registrata.

| Violazione | m-1 | CC-2 | CC-3 | CC-4 | CC-5 | CC-6 | Commit che l'ha presa di mira |
|---|---|---|---|---|---|---|---|
| **C1** / R-015 | ko | ko | ko | ko | ko | ko | `8eb3a71` |
| **C2** / R-015 | ok | ko | ko | ok | ko | ko | `e27d419`, `2bf0a12`, `f25c8d9` |
| **U4** / R-015 | ok | ok | ok | ok | ko | ko | nessuno |
| **R-009** | ok | ko | ko | ko | ok | ko | `779bf17` |
| **R-012** | ok | · | · | ko | ok | ko | nessuno |
| **R-020** | ko | ko | ok | · | ko | ko | nessuno |
| **R-035** | · | ok | ko | ko | ko | ko | nessuno |
| **R-017** | ko | ko | ko | ko | ko | ok | `f77bc61`, `2bf0a12`, `7b62754`, `f569dce` |
| **R-008** | ko | ko | ok | ko | ok | ok | `779bf17` |
| **R-022** | ko | ko | ok | ko | ok | ok | nessuno |
| **H5** | ko | · | · | · | · | ok | nessuno |

Due esclusioni dichiarate prima di cominciare, perché la cura cadrebbe fuori da `skills/roadmap/`:

- **H5** — nessuna clausola della skill obbliga una mappa a enumerare lo stack, e quattro review su
  cinque registrano che nemmeno `reference-roadmap/` nomina React Query. CC-6 la dà verde perché `S0`
  lo nomina testualmente, il che chiude il caso per via del run e non per via della voce. È materia
  del brief: **nominata e scartata**.
- **La sovrapposizione R-021 / R-011** — la riga di repository è `enabler` e fallisce il test
  dell'enabler. Quattro review su sei la segnalano e nessuna la conta rossa: per il preambolo delle
  regole è una clausola che dice due cose che si sovrappongono, non una violazione, e non compete con
  violazioni che sono rosse.

---

## 1. Regressioni

Due.

### 1.1 — R-009: il primo validatore non consegna metà della promessa, in un campo che il tell non guarda

`ok · · ko ok ko` — verde in `manual-run-1` e in `ROADMAP-CC-5`, rossa in CC-2, CC-3, CC-4, CC-6.

**Attribuzione.** `779bf17` *Catch theme compression where it leaves a trace* la prende di mira, e la
lettura è dal diff prima che dal messaggio: aggiunge a `drawing-the-map.md` § *Themes* il paragrafo
«A promise names only what its first validator delivers. **Where that row excludes a capability the
promise names**, the promise is holding two», e riscrive l'item di `The map holds when` in «no first
validator **excludes** a capability its own theme's promise names». Il messaggio nomina l'istanza di
CC-4 («merged photos into `ricettario` … while the theme's promise says "con le sue foto" and `S3`,
its first validator, excludes them»). Il commit sta in `d805196..37a0976`, quindi il primo run che lo
mette alla prova è CC-5, che la dà verde; CC-6 la riporta rossa.

**Perché il fix precedente ha mancato.** Non è stato cancellato da un refactor: il paragrafo e l'item
sono ancora lì, `drawing-the-map.md:62-64` e `:303-304`. È stato scritto più stretto della classe. Il
fatto portante di CC-6 è che la promessa di `condivisione` — «aggiungiamo **e correggiamo** le stesse
ricette» — ha per primo validatore `S7`, la cui `Verification` ha cinque bullet e nessuno osserva una
correzione. Ma `S7` **non esclude** la correzione: i suoi tre `Excludes` sono elenco/rimozione membri,
inviti per email, gruppi e ruoli. Il tell di `779bf17` è un lookup su `Excludes`, e su questa mappa
`Excludes` è muto — la clausola quindi *non* ci arriva già, e la diagnosi è l'ambito, non la forza.
CC-4 aveva l'esclusione scritta (`S3 Excludes` → «Foto: sono di `S4`») e il fix è stato tarato lì
sopra; CC-2 (il testo incollato è di `S5`) e CC-3 (i passi reali osservati solo dalla `Verification`
di `S5`) sono già due istanze della stessa classe più larga, e le si riconosce dall'osservazione
mancante, non dall'esclusione presente.

**File — `skills/roadmap/references/drawing-the-map.md`**, § *Themes*, righe 62-64. Al posto di:

> **A promise names only what its first validator delivers.** Where that row excludes a capability the
> promise names, the promise is holding two: either the validator is the wrong row, or the capability
> is a theme the table compressed.

si scrive:

> **A promise names only what its first validator delivers, and the row's `Verification` is where that
> is read.** Take the promise clause by clause and name, for each, the bullet of the validator's
> `Verification` that observes it. A clause with no bullet — whether the row excludes the capability,
> points at another row, or simply never mentions it — means the promise is holding two: either the
> validator is the wrong row, or the capability is a theme the table compressed. An `Outcome` that
> asserts the clause is not the observation.

E l'item di `The map holds when` (riga 303-304), al posto di «no first validator excludes a capability
its own theme's promise names»:

> - every theme boundary has a recorded split or merge verdict, and every clause of a theme's promise
>   has a bullet in its first validator's `Verification` that observes it;

L'ultima frase viene da CC-6 e da nessun run prima: l'`Outcome` di `S7` afferma «aggiunge, cerca **e
corregge** le stesse ricette» quando l'edit non esiste ancora, ed è la forma in cui la mappa si è
convinta di avere consegnato.

**Chiude:** R-009 in `ROADMAP-CC-2` (tema `import`, `S4`), `ROADMAP-CC-3` (`import`, `S6`),
`ROADMAP-CC-4` (`ricettario`, `S3`), `ROADMAP-CC-6` (`condivisione`, `S7`).

**Rischia di rompere:** che una promessa si accorci a una sola clausola per far tornare il lookup —
temi più magri e più numerosi, che è il `⚠ opposite` di nessuna regola ma è il costo che
`ROADMAP-GOAL.md` chiama *comprare precisione a spese della frase*. I due sensori sono **R-008**
(«every theme is a product promise in product language … no two independently schedulable value areas
were merged») nella direzione della compressione, e **R-030** più § *The cap is a finding* nell'altra:
sette temi contro sei non spostano il cap, quindici temi sì. Il testo lascia aperte entrambe le uscite
che la clausola già dichiara — cambiare validatore o scorporare il tema — e non ne aggiunge una terza.

**Come si misura:** metà *drawing*, scenario 0 (`REVIEW-WORKFLOW.md` manda lì ogni cambiamento a
`references/drawing-the-map.md`). Serve un run nuovo: la violazione si legge in `.roadmap/`, non nel
transcript, e il validator è cieco su questa regola.

**Controllo a costo zero, fatto.**
*Contro la riga che l'ha motivato:* il testo prende CC-6 — la promessa di `condivisione` ha due
clausole, «aggiungiamo» ha il primo bullet di `S7` («diventa membro, vede le ricette già presenti e ne
aggiunge una»), «correggiamo» non ha nessuno dei cinque. Prende anche CC-4 (nessun bullet di `S3`
nomina una foto), CC-3 (la terza clausola di `import` è osservata solo da `S5`) e CC-2 (il testo
incollato è di `S5`).
*Contro `reference-roadmap/`:* letti tutti e sette i primi validatori. `ricerca-semantica`/`S4` — «la
ricetta esce, in qualunque lingua sia scritta» contro «cercando «cena leggera» compaiono ricette che
quelle parole non le contengono; cercando «pomodoro» compare una ricetta scritta in inglese»: due
clausole, due osservazioni. `consultazione`/`S5` — «si sfogliano e si leggono» contro «dall'elenco …
si apre la ricetta e la si legge per intero». `inserimento-manuale`/`S7` — «la scrivi tu, e la correggi
quando vuoi» contro «si scrive una ricetta a mano, la si ritrova …, **la si modifica** e la ricerca
segue la modifica»: è il gemello strutturale esatto del rosso di CC-6, e il riferimento lo osserva.
`import-automatico`/`S8`, `foto`/`S11`, `condivisione`/`S12` — una clausola ciascuno, osservata.
`autenticazione`/`S6` è la più stretta: la promessa è «si entra senza password e senza aspettare
un'email» e la `Verification` osserva «entrando con un account Google si torna esattamente dove si
era» — entrare con Google *è* l'osservazione del modo, e non conto due clausole dove la seconda è
l'avverbio della prima. Nessuna riga marcata; quella è la riga da tenere d'occhio se il testo si
irrigidisse. Il riferimento è pre-`d8bc79d` e le sue `Verification` sono in prosa: ho letto le loro
frasi come le osservazioni che il formato di oggi vuole in elenco.

### 1.2 — C2 / R-015: la ragione della riga sulla ricerca riassegna il soggetto della frase che cita

`ok ko ko ok ko ko` — verde in `manual-run-1` e in `ROADMAP-CC-4`, rossa nelle altre quattro.

**Attribuzione.** Tre commit la prendono di mira, tutti e tre con l'id nel messaggio: `e27d419` *fix
violazione C2 di ROADMAP-CC-2* (i due test su una riga di `Assumptions`), `2bf0a12` *Ripara i due fix
della sessione precedente* («C2, residuo … Aggiunto il terzo test: la ragione deve reggere le proprie
citazioni»), `f25c8d9` *Make reading a citation's subject a lookup, not a judgement*. Il verde di CC-4
cade nell'intervallo aperto da `2bf0a12`, ed è quel commit a spiegarlo: la riga `ricerca, S8` di CC-4
legge il divieto come vincolo di costo e cita «le query sono irrilevanti», che è la lettura che il
terzo test manda a cercare. CC-5 e CC-6 riportano la forma di CC-3.

Nota sulla classificazione: presa da sola, `f25c8d9` è un fix che non ha preso — un solo run dopo, e
rosso. La storia intera però soddisfa la definizione di regressione (un commit identificabile,
`2bf0a12`, un run verde dopo, e poi il ritorno), e le due categorie sono disgiunte: la registro qui, e
la diagnosi qui sotto copre anche il secondo tentativo.

**Perché il fix precedente ha mancato.** Il fatto portante di CC-6 è che la riga scrive «La mappa legge
il divieto come un divieto di ri-embeddare **il corpus** a ogni ricerca, non come un divieto di
embeddare la query», mentre la frase citata — `arch-choices.md:33`, «Usato solo in fase di add e
all'edit, mai a runtime **sulle query di ricerca**» — ha per soggetto le query. Il testo attuale ci
arriva già, alla lettera: `f25c8d9` ha scritto «a reading that leaves the sentence standing and gives
it a different subject — the ban is about *that* mechanism, not this one — is a misreading however the
rest of the sources read», e la review lo cita come la clausola che scatta. Quindi la diagnosi **non è
l'ambito, è la forza**: la clausola dichiara di essere un lookup e poi non dice su che cosa si guarda.
Un modello che deve decidere se «corpus» sia «un soggetto diverso» da «query» sta ancora facendo un
giudizio. Il tell meccanico che manca è quello sulle parole. (Il rilievo che la riga cita solo
`arch-choices.md` mentre `goal.md:110-111` dichiara lo stesso divieto è marcato dalla review come
*corroborazione*, ed è corretto così: quel fatto è già coperto da «Where two sources state a constraint
together, splitting them needs a source that splits them», che `2bf0a12` aveva scritto e che qui non
è il difetto.)

**File — `skills/roadmap/references/drawing-the-map.md`**, § *What the map reports about its input*,
terzo test su una riga di `Assumptions`, dentro il periodo che comincia con «The section names the
subject of what it states». Dopo «is a misreading however the rest of the sources read» si inserisce:

> The lookup is on the words: the noun the reading makes the sentence about has to be a noun the
> sentence uses. Where the reading's subject is a term the quoted sentence never names — the ban is
> about the corpus, where the sentence says *the search queries* — the reading has replaced the
> sentence instead of reading it, and the line either takes the sentence as it stands or says which of
> two sources it is choosing against.

E l'item di `The map holds when` (righe 318-320) chiude sullo stesso lookup, al posto di «or gives one
a subject its section does not name»:

> - delivery can refute every `Assumptions` line, every reading about how something works lands in a
>   bullet of the row it is traced to, and no reading is contradicted by the lines it cites or makes a
>   sentence about a noun that sentence does not use;

Nessun campo nuovo, nessuna sezione nuova: cambia una frase dentro un test che già esiste.

**Chiude:** C2 / R-015 in `ROADMAP-CC-3` («si legge il divieto come riferito all'estrazione LLM»),
`ROADMAP-CC-5` («riferito all'LLM e alla ri-indicizzazione del corpus»), `ROADMAP-CC-6` («divieto di
ri-embeddare il corpus»). Non chiude la forma di CC-2 (la riga che ri-afferma il vincolo invece di
risolverlo), che `e27d419` ha già chiusa e che nessun run dopo di lui ripropone.

**Rischia di rompere:** il `⚠ opposite` di **R-015** — una mappa che, non potendo riformulare, non
prende più nessuna lettura e pubblica tutto in `Open questions`. Il testo lascia esplicitamente la
seconda uscita («says which of two sources it is choosing against»), che è la strada del riferimento;
se ne accorgerebbero R-015 stessa, scritta in entrambe le direzioni, e sul brief **A1** e **A3**, che
dicono dove una fonte seleziona e quindi non c'è niente da riportare. Il secondo rischio è che una
riga si riduca a citare senza leggere: lo prenderebbe il primo dei tre test, *Delivery can refute it*
(«a line restating what a source already says … either it quotes the source, and goes»), che è
esattamente il rosso di CC-2 e resta in vigore.

**Come si misura:** metà *drawing*, scenario 0. Serve un run nuovo; il validator è cieco su questa
regola, quindi un `OK` non è evidenza.

**Controllo a costo zero, fatto.**
*Contro la riga che l'ha motivato:* prende CC-6 — «corpus» non compare in «mai a runtime sulle query
di ricerca», e il lookup fallisce sulla parola. Prende CC-5 e CC-3 allo stesso modo («LLM» e
«ri-indicizzazione» non sono nomi di quella frase).
*Contro `reference-roadmap/`:* lette tutte e sei le righe di `Assumptions`. `ricerca-semantica, S4` —
classifica il vincolo («di costo, non di architettura») e dichiara che le fonti si contraddicono e che
la mappa sceglie: non riassegna nessun soggetto, e i nomi che usa — query, runtime — sono quelli della
frase. `inserimento-manuale, S7` — «"stesso schema" vale per la forma della `Recipe` che si salva, non
per un motore che quel percorso non tocca»: restringe il referente di due nomi che la frase citata usa
entrambi («riusano lo stesso motore e schema»), e resta dentro. È la riga di taratura che il messaggio
di `f25c8d9` già nominava, e la formulazione sulle parole la lascia libera dove una formulazione sul
«significato» l'avrebbe presa. `S1` (Neon/Supabase), `import-automatico, S9` (copertura del JSON-LD),
`S3, S4` (corpus di semina), `condivisione, S12` (un solo ricettario implicito) non leggono il soggetto
di nessuna frase. Nessuna riga marcata.

---

## 2. Fix che non hanno preso

Uno.

### 2.1 — C1 / R-015: il lato preso in un bullet e riportato da nessuna parte

`ko ko ko ko ko ko` — sei run su sei, l'unica a punteggio pieno.

**Attribuzione.** `8eb3a71` *Report the side a row takes: bullet-only conflict resolution gets a tell*.
L'id sta nel messaggio, che elenca le cinque istanze allora note. Sta in `37a0976..fb29812`: CC-6 è il
solo run che lo mette alla prova, e lo dà rosso — il lato è preso in `S4 Excludes` («L'inserimento a
mano: è di S8 … perché condivide con essa il form **e non la pipeline**») più `S8 Includes`, e nessuna
riga di `Assumptions`, nessuna di `Open questions`, nessuno spike nomina C1.

**Perché il fix precedente ha mancato.** Non l'ambito: il paragrafo *Taken in a row and nowhere else*
descrive l'istanza di CC-6 alla lettera, e la review lo cita per nome. Copre anche la scappatoia che
il candidato usa, perché il bullet di CC-6 si giustifica proprio con la condivisione del form («A
neighbouring row that shares the schema, the pipeline or the form is not the report either»). La
clausola quindi ci arriva già, e la diagnosi è la forza. Ma la forza le manca per una ragione precisa
e che il commit stesso aveva dichiarato come suo confine noto: **«a sweep that never records the
conflict escapes the tell»**. Il tell è condizionato a «one side of a conflict **the sweep found**» —
un fatto che non sta sulla pagina, sta nella memoria della sessione. Ogni altro tell che ha preso in
questa storia si verifica sull'artefatto e basta: gli `Excludes` di un primo validatore (`779bf17`),
i nomi di una frase citata (`f25c8d9`), la riga che sopravvive a essere spostata in un altro progetto
(`79f4a4a`). Questo no. Il difetto non è nel piano, è nell'intervento: un tell che chiede alla
sessione di ricordare non è un lookup.

**File — `skills/roadmap/references/drawing-the-map.md`**, § *What the map reports about its input*.
In coda al paragrafo *Taken in a row and nowhere else* (dopo «it says what was built, not which side
was taken and why») si aggiunge il modo di farlo scattare senza lo sweep:

> The tell does not rest on remembering the sweep. After the first cut, read every `Includes` and
> `Excludes` bullet that says **how** a behaviour works or does not — *it skips the extractor*, *it
> shares the form and not the pipeline*, *what is typed is saved as typed* — and look that behaviour up
> in the sources. Where two of them describe it differently, the bullet is a side taken, and it owes
> its line whether or not the entry was ever on the sweep's list. A bullet that only says which row a
> behaviour belongs to owes nothing.

E l'item di `The map holds when` (righe 315-316), al posto di «and no side of one was taken only in a
row's `Includes` or `Excludes`»:

> - every conflict and every undecided choice left the sweep by one of the three exits, and every
>   bullet stating how a behaviour works was looked up in the sources before the map was written;

Il costo è un secondo passaggio sulle fonti, ed è lavoro di sessione, non un campo della mappa: una
mappa che non ha niente da riportare non cresce di una riga. Il passaggio è ristretto ai bullet che
enunciano un meccanismo, che su queste mappe sono una manciata; l'ultima frase della citazione lo dice
per escludere i bullet di sola proprietà, che sono la maggioranza.

**Chiude:** C1 / R-015 in `manual-run-1` (`S6 Excludes`), `ROADMAP-CC-2` (`S3 Includes`),
`ROADMAP-CC-3` (`S3 Excludes`), `ROADMAP-CC-4` (`S3 Includes`), `ROADMAP-CC-5` (`S3 Excludes`),
`ROADMAP-CC-6` (`S4 Excludes` + `S8 Includes`).

**Rischia di rompere:** ancora il `⚠ opposite` di **R-015** — riportare una lettura ogni volta che due
fonti si sfiorano, e riempire `Assumptions` di righe che la consegna non può confutare. Il sensore è
il primo dei tre test, *Delivery can refute it*, che uccide la riga che ri-afferma una fonte; e sul
brief **A1**–**A3**, che dicono dove una fonte seleziona. Il secondo rischio è di costo, non di
qualità: se il secondo passaggio allungasse la sessione senza trovare niente, si vedrebbe in
`METRICS.md` prima che in `REVIEW.md`, e la voce a cui rispondere sarebbe `improve-perf.prompt.md`,
non una regola.

**Come si misura:** metà *drawing*, scenario 0. Serve un run nuovo, e su questa ne servono **due**: è
a 6/6, e il preambolo delle regole dice che un run registra e due decidono. Il `PROMPT.md` del run
successivo deve dichiarare che entra in prova un secondo tentativo sulla stessa violazione, perché il
primo è già stato speso.

**Controllo a costo zero, fatto.**
*Contro la riga che l'ha motivato:* prende CC-6 — `S4 Excludes` dice **come** funziona l'inserimento a
mano («condivide con essa il form e non la pipeline»), e il lookup su «inserimento manuale» trova
`concepts.md` § *Pipeline di estrazione* riga 126 contro `arch-choices.md` § *Estrazione contenuto*
punto 3, che lo descrivono diversamente: il bullet deve la sua riga, e non ce l'ha. Prende allo stesso
modo le cinque istanze precedenti, che sono tutte bullet di meccanismo sullo stesso comportamento.
*Contro `reference-roadmap/`:* letti gli `Includes` e gli `Excludes` di tutte e quindici le righe. Il
tell scatta su una sola, `S7 Excludes` — «Il motore di estrazione: quello che si scrive nel form si
salva così com'è, senza JSON-LD e senza LLM» — che è un bullet di meccanismo su un comportamento che
le fonti descrivono in due modi; **e lì il lookup si risolve**, perché la riga `inserimento-manuale,
S7` di `Assumptions` c'è ed è precisamente quella dovuta. È il comportamento voluto: il tell scatta e
non marca. Non scatta su `S9 Excludes` («La scelta definitiva del modello: si cambia senza toccare la
forma di questa riga»), che è un meccanismo su cui nessuna coppia di fonti si contraddice — è la
scelta indecisa U5, un'altra categoria dello sweep; né su `S13 Excludes`, `S0 Excludes`,
`S1 Excludes`, `S3 Excludes`, `S6 Excludes`, `S11 Excludes`, `S12 Excludes`, che dicono a quale riga o
a quale orizzonte un comportamento appartiene e non come funziona. Nessuna riga del riferimento
marcata.

---

## 3. Mai risolte

Tre, nell'ordine in cui le farei. Il criterio è la ricorrenza.

### 3.1 — R-035: il messaggio di chiusura si apre sul validator

`· ok ko ko ko ko` — quattro run consecutivi, sempre nella stessa forma: una riga di stato **prima**
delle quattro parti. «Validatore: `OK`, nessun ERROR né WARNING» (CC-3), «Mappa scritta e validata
(`OK`, nessun warning).» (CC-4, CC-5), «`.roadmap/` scritta e validata (`OK`, nessun warning).»
(CC-6). In tutti e quattro le quattro parti ci sono e nell'ordine giusto, e in CC-5 e CC-6 quel che
va dopo sta dopo: quel che ricorre è solo l'apertura. Nessun commit l'ha mai presa di mira. Una
proposta esiste — `ROADMAP-CC-5/IMPROVEMENTS.md` § 3.3 — e non è stata applicata; una proposta non è
un commit, quindi la violazione resta in questa categoria. La riscrivo qui perché CC-6 aggiunge il
quarto run e non aggiunge nulla alla diagnosi.

**File — `skills/roadmap/SKILL.md`**, § *5. Close the session*. In deroga al default, e per la ragione
che la skill dichiara da sé: «One checklist per altitude — the row in `slice-rules.md`, the map in
`drawing-the-map.md`, the session here». *Close the session* non ha un file in `references/`, e la
sovrapposizione da sciogliere è fra due clausole della stessa sezione — R-033 vuole che si veda che il
validator ha girato, R-035 vuole quattro parti e nient'altro. CC-4, CC-5 e CC-6 la nominano tutte e
tre come sovrapposizione, che il preambolo delle regole chiama *a clause saying two things that
overlap*: la cura è disambiguare, non aggiungere.

Al passo del validator, dopo «A `WARNING` is a signal to the author: the cap and the floor are findings
to discuss, not defects to silence.», si aggiunge dove finisce il suo esito:

> A clean run reports nothing. The validator's only output to the author is a `WARNING`, and it goes
> after the four parts with anything else the session owes; that it ran at all is visible in the
> session, not in the message.

E l'apertura del report, al posto di «**Then report the written map, and nothing else.** Four things,
in this order, read off the files as they now stand:»:

> **Then report the written map, and nothing else.** The `Themes` table is the first thing in the
> message: no preamble, and in particular no line saying the map was written and validated, which
> narrates an operation the author can already see. Four things, in this order, read off the files as
> they now stand:

E l'ultimo item di *The session holds when*:

> - the session closed on the four-part report — themes, register, open questions, path — with nothing
>   before it and only what it owes after it.

**Chiude:** R-035 in `ROADMAP-CC-3`, `ROADMAP-CC-4`, `ROADMAP-CC-5`, `ROADMAP-CC-6`.

**Rischia di rompere:** che una sessione, per non narrare, smetta di riportare un `WARNING` dovuto o
una domanda che ha prodotto — cioè la metà solida del rosso di CC-3, dove due domande dovute non sono
mai arrivate all'autore. Se ne accorgerebbero **R-033** («every `WARNING` put to the author rather
than silenced») e **R-035** stessa, che vuole la domanda *dopo* le quattro parti e non al posto loro.
Il secondo rischio è leggere il silenzio sul validator come licenza a non girarlo: R-033 legge il
transcript e non il messaggio — «What this reads is that it ran and what it did with the `WARNING`s» —
quindi quel sensore resta intatto.

**Come si misura:** metà *drawing*, scenario 0, che `REVIEW-WORKFLOW.md` indica per ogni cambiamento a
*Close the session*. Serve un run nuovo, e il rilievo si legge in `TRANSCRIPT.jsonl`, non in
`.roadmap/`.

**Controllo a costo zero.** *Contro la riga che l'ha motivato:* il testo prende il turno 95 di CC-6 —
la riga «`.roadmap/` scritta e validata (`OK`, nessun warning).» sta prima della tabella `Themes` e
non c'era nessuna `WARNING`, quindi cade sotto «A clean run reports nothing» e sotto «no line saying
the map was written and validated». Prende allo stesso modo CC-3, CC-4 e CC-5.
*Contro `reference-roadmap/`:* **niente da controllare, e mi fermo alla prima metà.** La proposta cade
ad altitudine di sessione, e il riferimento è una mappa, non un transcript: non ha un messaggio di
chiusura da marcare. Non sostituisce il run nuovo, che resta l'unica misura.

### 3.2 — R-020: la clausola del `Learning target` non ha un lookup, e il claim che nessuno osserva è sempre il secondo

`ko ko ok · ko ko` — rossa in `manual-run-1` (`S3`, `S5`), `ROADMAP-CC-2` (cinque righe),
`ROADMAP-CC-5` (`S5`, `S7`, `S9`), `ROADMAP-CC-6` (`S9`); discussa e non contata in CC-3 e CC-4.
Nessun commit l'ha mai presa di mira. `d8bc79d` tocca la `Verification` ma non la regola: mette la
sezione in forma di elenco, il che è il presupposto della proposta qui sotto e non il suo sostituto.

La forma che ricorre è la più semplice delle due metà della regola: un `Learning target` con due
clausole, la prima osservata e la seconda no. CC-6 `S9` — «se rimpiazzare l'hotlinking … regge sui
siti veri **e se lo fa dentro il tempo della pipeline sincrona di S3**», e nessuno dei cinque bullet
osserva un tempo. CC-5 `S7` — «o se in pratica la allunga oltre il budget di richiesta», senza
osservazione. CC-2 `S8` — «costa abbastanza poco, in tempo di aggiunta e in spazio, da stare nel piano
gratuito», con una `Verification` che conta foto e file orfani. `manual-run-1` `S3` — il secondo claim
osservato nella `Verification` di un'altra riga. Su CC-6 la stessa mancanza costa due volte: **U4**
esce dalla sweep per la strada che A9 licenzia — la misura dentro una riga ordinaria — e la misura non
c'è, che è il rosso R-015 su U4 e insieme il rosso R-020.

**File — `skills/roadmap/references/slice-rules.md`**, § *Verification maps to the learning target*.
La clausola oggi è una norma senza tracciato: «Every material claim in `Learning target` maps to an
observation in `Verification`, stated so that delivery can refute it. Checking that data exists does
not demonstrate its quality, usability, latency or cost.» Il fatto portante di CC-6 — una clausola
sulla latenza senza osservazione — è coperto alla lettera dalla parola *latency*, quindi la diagnosi è
la forza e la cura è un tell meccanico, non una regola più larga. Subito dopo quella frase:

> **Pair them off before the row is done.** Read the `Learning target` as the claims it makes — two
> joined by *and* or *or* are two claims — and name, for each, the `Verification` bullet that could
> come out against it. A claim with no bullet has two honest exits and neither is a longer
> `Verification`: cut the claim and let the row learn one thing, or move it to the row whose evidence
> already settles it, which is usually the row that set the figure the claim is measured against.

E l'item di `A row holds when`, al posto di «every material claim in `Learning target` has an
observation in `Verification`»:

> - every claim in `Learning target` names the `Verification` bullet that could come out against it,
>   and a claim no bullet can reach was cut rather than carried;

L'uscita economica è **tagliare la clausola**, non gonfiare la `Verification` in un piano di misura:
è la lettura che `ROADMAP-GOAL.md` impone, ed è quella che il paragrafo mette per prima.

**Chiude:** R-020 in `manual-run-1`, `ROADMAP-CC-2`, `ROADMAP-CC-5`, `ROADMAP-CC-6`; e la metà di
U4 / R-015 di CC-6 che dipende dalla misura mancante.

**Rischia di rompere:** è la proposta più vicina al confine di `ROADMAP-GOAL.md`. Due modi di
sbagliare: righe che diventano piani di misura, e ogni incertezza che si trasforma in uno spike. Se ne
accorgerebbero **R-007 `⚠ opposite`** («every uncertain row turning into a spike. Uncertainty is the
learning target of an ordinary row») e, sul brief, **A9** con **U4**, che licenziano esplicitamente la
misura dentro una riga ordinaria: se dopo il fix U4 uscisse per uno spike, il fix ha spinto troppo. Il
terzo sensore è **R-030** più § *The cap is a finding*, perché claim tagliati significano righe più
strette e quindi più numerose.

**Come si misura:** `slice-rules.md` è letto in ogni sessione, quindi il cambiamento tocca entrambe le
metà di `REVIEW-WORKFLOW.md`; la violazione però si osserva su una mappa disegnata, quindi la misura è
scenario 0 e i router 1-3 sono il controllo a basso costo che le righe non si siano assottigliate.
Serve un run nuovo.

**Controllo a costo zero, fatto.**
*Contro la riga che l'ha motivato:* prende CC-6 — il `Learning target` di `S9` ha due clausole unite da
«e», la prima ha i bullet sull'`og:image` scaricata e ricaricata, la seconda («dentro il tempo della
pipeline sincrona di S3») non ne ha nessuno dei cinque; l'uscita è tagliarla, e il tempo lo misura già
`S3` («Il tempo … è misurato su una decina di siti reali»). Prende CC-5 `S7`, CC-2 `S8` e
`manual-run-1` `S5` allo stesso modo.
*Contro `reference-roadmap/`:* accoppiati clausola e osservazione su tutte e quindici le righe, leggendo
le `Verification` in prosa del riferimento (pre-`d8bc79d`) come le osservazioni che oggi starebbero in
elenco. Nessuna marcata. Le due più strette, e le nomino perché sono il margine: **`S0`** — «Quanto
della catena gratuita si accende davvero senza carta di credito, e dove invece serve», contro «un
checkout pulito parte in locale con i soli segreti documentati e nessun passaggio a voce»: la seconda
metà non è un claim indipendente ma il negativo della prima, e un account che chiedesse la carta
lascerebbe un segreto non documentato — l'osservazione può uscire dall'altra parte, quindi si accoppia;
**`S8`** — «abbastanza per una ricetta leggibile, **senza chiamare nessun modello a pagamento**»,
contro «la ricetta si salva senza altri passaggi»: la seconda clausola è garantita dalla costruzione
della riga, i cui `Includes` non contengono nessun modello, e il bullet la osserva. `S2` accoppia due
claim a due figure riportate («quante delle ricette attese compaiono … e quanto costa indicizzare»);
`S1`, `S3`, `S4`, `S5`, `S6`, `S7`, `S9`, `S10`, `S11`, `S12`, `S13`, `S14` portano un claim solo, e
ciascuno la sua osservazione. Ho scartato le formulazioni che pretendevano una *cifra* per ogni claim
su tempo o costo: marcavano `S8` e `S10` del riferimento, e una clausola che condanna la chiave di
risposta è un difetto della clausola.

### 3.3 — R-012: il recupero dovuto arriva sei posizioni dopo lo stato che lo richiede

`ok · · ko ok ko` — rossa in `ROADMAP-CC-4` e in `ROADMAP-CC-6`, verde in `manual-run-1` e in CC-5,
*inconclusive* in CC-2 e CC-3 (i due report precedono la riscrittura della regola e leggono la vecchia
lista di `Ordering criteria`). Nessun commit l'ha mai presa di mira: `d805196` ha tolto la sezione che
la argomentava e ha riscritto la clausola di conseguenza, ma non è un fix di una violazione. Il verde
di CC-5 nessun commit lo spiega — i tre di quell'intervallo prendono R-008/R-009, i concern e R-017 —
quindi è varianza, e la violazione resta qui.

CC-6: `S8` (tema `correzione`) sta in posizione 9, dopo che `S5` apre `ricerca`, `S6` apre `accesso` e
`S7` apre `condivisione`. `goal.md:70-71` fa dell'edit il recupero dichiarato del salvataggio senza
review, e lo stato recuperabile — una ricetta estratta male e salvata — nasce con `S3`, in posizione 4.

**Il difetto è che la stessa norma sta in due posti con due inneschi diversi.**
`drawing-the-map.md` § *Ordering for learning* la innesca su un fatto scritto: «**When a row names a
failure mode in its `Verification`** and another `NOW` row is its remedy, the remedy comes before a
different theme opens». `slice-rules.md` § *Splitting and merging a row* la innesca sullo stato:
«Deliver a required correction, retry or escape path **before or with the first behaviour that can
create the recoverable state**». Su CC-6 il secondo innesco scatta e il primo no: la `Verification` di
`S3` nomina un fallimento — «Su una pagina senza JSON-LD l'aggiunta fallisce … è il fallimento che S4
rimedia» — e quello è il rimedio di `S4`, licenziato e consegnato subito dopo; il salvataggio di
un'estrazione *sbagliata* non è nominato da nessun bullet di `S3`, quindi la clausola dell'ordine non
ci arriva. La review lo registra come corroborazione; è il fatto che regge il verdetto, e sotto quel
nome ci sta il difetto.

**File — `skills/roadmap/references/drawing-the-map.md`**, § *Ordering for learning*, il secondo dei
quattro punti non soggetti a ranking. Al posto di «When a row names a failure mode in its
`Verification` and another `NOW` row is its remedy, the remedy comes before a different theme opens»:

> - **Required recovery outranks breadth.** The remedy comes before a different theme opens, and there
>   are two ways a row asks for one: it names a failure mode in its `Verification` and another `NOW`
>   row is that remedy, or it is the first behaviour that can create a state the sources declare
>   recoverable — a save with no review step, an import that may be wrong — and the correction is a
>   different row. A remedy the sources declare a fallback of a delivered path closes that path; it is
>   not optional depth. Where the sources define a recovery chain, the primary interaction gains its
>   required automatic recovery before a separate manual escape is drawn.

La seconda metà è la stessa frase che `slice-rules.md` già porta, letta all'altitudine dell'ordine
invece che a quella dello split: nessuna norma nuova, un innesco allineato.

**Chiude:** R-012 in `ROADMAP-CC-6` (`S8` nona, contro `S3` quarta). **Non** chiude il rilievo di
`ROADMAP-CC-4`, che è di un'altra metà della regola — `S4` seconda riga di `ricettario` in posizione 5
senza nessuna delle quattro licenze, e la ricerca esistenziale nona — e che nessun run dopo di lui
ripropone: CC-5 e CC-6 portano il differenziatore rispettivamente in posizione 5 e 6, con lo spike
davanti. Quella metà la lascio in osservazione.

**Rischia di rompere:** che ogni riga che scrive qualcosa si porti dietro la sua correzione, e la
breadth non apra più — cioè il rovescio esatto della clausola, righe più grasse e temi che restano
chiusi. Se ne accorgerebbe **R-012** stessa nella sua prima metà («deliver one thin row per remaining
theme before a second row from one theme»), che è scritta in quella direzione; e **R-024**
(«a merge yields one outcome and one learning target»), se la correzione venisse fusa dentro la riga
che crea lo stato invece di precederla. Il freno è nel testo: *before or with*, dove «with» è la
fusione e resta ammessa, e l'innesco chiede che siano le fonti a dichiarare lo stato recuperabile —
non basta che una riga scriva.

**Come si misura:** metà *drawing*, scenario 0. Serve un run nuovo: si legge dall'ordine del registro,
e il validator non guarda l'ordine.

**Controllo a costo zero, fatto.**
*Contro la riga che l'ha motivato:* prende CC-6 — `goal.md:70-71` dichiara lo stato recuperabile
(«Nessuna review obbligatoria: l'estratto si salva subito. La correzione è sempre disponibile dopo»),
`S3` è la prima riga che lo crea, `S8` è un'altra riga, e fra le due `ricerca`, `accesso` e
`condivisione` aprono. La mappa lo dice due volte da sé, nel `Learning target` di `S4` e nell'`Audience`
di `S8`.
*Contro `reference-roadmap/`:* letto l'ordine intero. La clausola allargata **non marca nessuna riga**,
e il riferimento è l'istanza positiva: la prima riga che crea una ricetta d'utente è `S7`
*Scrittura e correzione a mano*, che **è** la correzione — «before or with» nella sua forma «with» — e
`S8` (import da URL) la segue. Il riferimento ne dà la ragione nel `Learning target` di `S7` («è la
condizione che rende accettabile salvare subito un'estrazione imperfetta»), che è la stessa frase che
CC-6 scrive nell'`Audience` di `S8` e poi contraddice con l'ordine. Le altre catene di recupero del
riferimento reggono col vecchio innesco e non hanno bisogno del nuovo: `S9` è il rimedio del fallimento
che `S8` nomina nella propria `Verification` e lo segue immediatamente; `S10` segue `S9`. `S3`, `S4`,
`S5`, `S6` non creano stato recuperabile — il corpus di semina di `S3` è dato di prova, non scrittura
d'utente — quindi l'innesco nuovo non ci scatta sopra. Nessuna riga marcata.

---

**Scartata dalle tre, pur essendo ricorrente:** **R-022** — `Includes` che decide un lato di ciò che la
riga dichiara indeciso — rossa in `manual-run-1`, `ROADMAP-CC-2` e `ROADMAP-CC-4`, ma verde negli
ultimi due run consecutivi (CC-5 `S0` e CC-6 `S1`/`S4`, dove `Includes` dice «il fornitore scelto» e
«il modello LLM scelto»): due verdi di fila sono il ratchet del preambolo, e una proposta scritta oggi
lavorerebbe contro di essi.
