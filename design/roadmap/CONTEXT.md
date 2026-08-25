# Roadmap skill

Il vocabolario della skill di roadmap: l'artefatto vivente che decide *cosa fare dopo*, a monte della
catena `to-spec` → `to-tickets` → `implement`. Copre solo i termini di questo contesto; quelli della
catena a valle sono definiti dalle skill installate. Il razionale sta in
[`ROADMAP-GOAL.md`](./ROADMAP-GOAL.md), le regole in [`skills/roadmap`](../../skills/roadmap).

## Language

**Roadmap**:
L'artefatto vivente che tiene l'ordine di scoperta di un progetto verso un `Goal` dichiarato: temi,
slice `NOW`, speculazioni `LATER`, esclusioni `OUT-OF-SCOPE`. Vive in `.roadmap/`, è una per progetto
e serve un goal alla volta. È uno strumento di sense making, non di precisione: niente date, stime,
percentuali di completamento.
_Avoid_: plan, delivery plan, piano (`plan` resta solo verbo o attività, mai nome di artefatto, file
o sezione)

**Goal**:
L'esito dichiarato che la roadmap serve, riscritto in testa a `roadmap.md`. È il metro con cui si
chiede, a ogni sessione, se ciò che resta in `NOW` arriva da qualche parte. Un input che pretende
sulla *destinazione* mette in discussione il goal; un input che pretende sul *percorso* è lavoro.
_Avoid_: vision, obiettivo, milestone

**Slice**:
Un esito verticale singolo, indipendentemente schedulabile, con un solo learning target. Esiste solo
in `NOW`: ha un id, una riga nel register e un documento in `.roadmap/slices/`. Non è il nome
collettivo delle righe del register.
_Avoid_: ticket, task, story (un ticket di `to-tickets` non va mai chiamato slice in questi
documenti, nonostante `to-tickets` chiami i propri ticket "tracer-bullet vertical slices"); spike

**Spike**:
Un'indagine il cui prodotto è conoscenza: ha un learning target e nessun esito verticale, e perciò
non è una slice. Sta nel register con `kind: spike`, deve avere un dipendente e occupa una riga sotto
il limite di `NOW`. Condivide tutto con una slice tranne `Audience`, che resta vuota.
_Avoid_: research slice, investigation slice, non-product work, timebox (non è un campo)

**Register**:
La tabella in `roadmap.md` che tiene il percorso verso il goal: una riga per ogni elemento di `NOW`,
slice o spike, con il titolo e i soli metadati che servono a confrontare le righe fra loro — id,
titolo, theme, kind, size, readiness, executor, `Depends on`. Il titolo è un link al documento della
riga, e il documento ha un link che riporta qui. Risponde a *qual è il percorso*, non a *cosa posso
fare adesso*: a quello risponde `readiness`. Una riga chiusa esce dal register.
_Avoid_: slice index, index, tabella delle slice, backlog

**Id**:
L'identità stabile di una riga del register (`S0`, `S1`, …), assegnata alla promotion per incremento
monotòno. La sequenza è una sola: `kind` dice cosa è la riga, l'id no. Non viene mai riciclata e non
esprime posizione: l'ordine di consegna lo porta l'ordine del register.
_Avoid_: numero di slice, indice, posizione

**NOW**:
L'orizzonte di ciò che serve per arrivare al `Goal`. Solo ciò che sta in `NOW` ha id, riga nel
register e documento. È limitato — da tre o quattro righe a venti, quindici il numero a cui puntare —
e il limite vincola la granularità, non il conteggio.

**LATER**:
L'orizzonte di ciò che non serve per *questo* goal: speculazione, o materiale per il goal successivo.
È uno strumento di focus, non un backlog.

**Candidate**:
Una voce di `LATER`: una riga in `roadmap.md`, senza id e senza documento.
_Avoid_: entry, item, idea, candidate capability, LATER slice

**OUT-OF-SCOPE**:
L'esclusione dichiarata: i problemi che la soluzione non risolve, scritti come licenza per i
trade-off che l'implementazione prende proprio perché quei problemi restano fuori. Nessun id, mai
implementata.
_Avoid_: wontfix (è il ruolo di `triage` per una richiesta esterna rifiutata), `.out-of-scope/` (è la
knowledge base di `triage`); la sezione `Out of Scope` di una spec è il confine di quella spec,
ereditato dalle esclusioni della slice

**Assumptions**:
La prima delle due sezioni di `roadmap.md` che riferiscono sull'input: cosa la skill ha preso per
vero *per poter* disegnare la mappa, ogni riga tracciata al tema o all'id che tocca. Chiede di essere
corretta, e di solito muore alla close-out.
_Avoid_: Assumptions and gaps, assunzioni implicite

**Open questions**:
Ciò che è rimasto senza risposta, allo stesso nome a due altitudini: la seconda sezione di
`roadmap.md`, e il campo del documento di slice. A deciderne l'altitudine è solo ciò che blocca — la
*forma* della mappa, oppure una sola riga, e allora si vede nel register come `readiness`. Chiede una
risposta e muore quando la riceve. Non è una coda di lavoro e non assegna id.
_Avoid_: Open decisions, unresolved, gaps, open issues, backlog di domande

**Outcome**:
La prima riga del documento di slice: una frase che dice cosa la riga consegna. Su uno spike dice
quale conoscenza produce.
_Avoid_: esito in una riga come colonna del register, Outcome come sezione in fondo al documento

**Requested by**:
Il riferimento in entrata del documento di slice: cosa ha prodotto la slice — un documento sorgente,
oppure, per il lavoro ammesso più tardi, la slice consegnata che l'ha resa visibile. Non si chiama
`Sources` perché quel nome è già preso a livello di roadmap.

**Theme**:
Una promessa di prodotto rinviabile o cancellabile per intero, con un esito desiderato in linguaggio
di prodotto e una prima slice `NOW` che lo valida.

**Kind**:
Colonna del register che dice cosa è una riga: `product`, `enabler`, `release` sono slice, `spike`
no.

**Size**:
Colonna del register con un segnale grossolano di dimensione, il cui unico effetto è instradare la
riga a valle: `large` passa da `to-tickets`, altrimenti si va diritti a `to-spec`. Non è un budget di
token, e su uno spike non decide nulla.

**Readiness**:
Colonna del register che dice se una riga si può prendere in mano: `ready`, `needs-decision` (una
scelta che l'autore possiede e non ha preso), `needs-info` (si aspetta qualcun altro). Non nomina mai
un attore: le etichette di `triage` si derivano all'handover combinandola con `executor`.
_Avoid_: usare direttamente `ready-for-agent` / `ready-for-human` come stato di riga

**Executor**:
Colonna del register che dice chi può eseguire la riga: `agent`, `human`, `mixed`.

**Learning target**:
Ciò che la riga deve insegnare: uno solo, obbligatorio, ed è l'invariante che regge lo split test. Il
rischio non è un campo a sé — se è materiale è il learning target.
_Avoid_: Learning / risk

**Promotion**:
L'operazione che trasforma una candidate in riga del register: le assegna id, riga e documento.

**Close-out**:
L'operazione che chiude una riga consegnata: la toglie dal register, sposta il documento in
`.roadmap/archive/` e assorbe l'evidenza prodotta nelle decisioni successive.
_Avoid_: reconcile, absorb (restano verbi nella definizione, mai nomi dell'operazione)

**Admission**:
L'operazione con cui lavoro nuovo entra in roadmap, come candidate in `LATER` o come riga in `NOW`.
Se porterebbe `NOW` oltre il limite, obbliga a fondere o a rimandare: la lista non cresce.

**Reshaping**:
L'operazione che rimaneggia righe esistenti senza aggiungerne né chiuderne: split, merge, riscrittura,
riordino. L'id resta al learning target sia nello split sia nel merge.
_Avoid_: split/merge/reorder come nomi di operazioni distinte; revision (è il ramo un'altitudine
sopra)

**Retirement**:
L'operazione con cui una riga esce da `NOW` senza essere stata consegnata: muore, o retrocede a
candidate in `LATER`. L'id è speso; il documento viene cancellato, non archiviato.
_Avoid_: demotion (è il caso particolare, non il nome dell'operazione), wontfix

**Drawing**:
La porta che decide la forma della mappa intera: si prende quando nessuna mappa regge un goal
dichiarato, oppure quando l'input contraddice il `Goal` registrato. È la sola che carica
`references/drawing-the-map.md`, e vale tanto al primo disegno quanto al redraw.
_Avoid_: create, creation, primo disegno come nome del ramo (il redraw è la stessa porta)

**Revising**:
La porta di default, quella di quasi tutte le sessioni: il goal regge, e ciò che va fatto sulla mappa
si deriva dalla situazione come una o più delle cinque operazioni. Cambia forma e appartenenza —
chiude righe, assegna id, cancella documenti — quindi non è un controllo.
_Avoid_: update (è la divisione in due skill che questo progetto ha rifiutato), maintenance,
manutenzione

**Redraw**:
Il ridisegno della mappa quando viene dichiarato un goal nuovo. Non è un'operazione fra le cinque: è
il ramo di disegno che riparte con più input — l'archivio, il massimo id raggiunto, le esclusioni, i
concern, le candidate e le righe ancora aperte.
_Avoid_: reset, ricreazione, nuova roadmap; porta (nomina un caso, mai un ramo: il ramo è `Drawing`)

**Horizon**:
Nome collettivo in prosa dei tre orizzonti `NOW`, `LATER`, `OUT-OF-SCOPE`. Mai un campo, mai una
colonna, mai un'intestazione.
