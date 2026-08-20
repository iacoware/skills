# Roadmap skill

Il vocabolario della skill di roadmap — [`ROADMAP-GOAL.md`](./ROADMAP-GOAL.md) e ciò
che ne nasce: l'artefatto vivente che decide *cosa fare dopo*, a monte della catena `to-spec` →
`to-tickets` → `implement`. Copre solo i termini di questo contesto; quelli della catena a valle sono
definiti dalle skill installate.

## Language

**Roadmap**:
L'artefatto vivente che tiene l'ordine di scoperta di un progetto verso un `Goal` dichiarato: temi,
slice `NOW`, speculazioni `LATER`, esclusioni `OUT-OF-SCOPE`. Vive in `.roadmap/`, è una per
progetto e serve un goal alla volta: due goal non corrono mai in parallelo. È uno strumento di sense
making, non di precisione: non porta date, stime, percentuali di completamento.
_Avoid_: plan, delivery plan, piano (`plan` resta solo verbo o attività, mai nome di artefatto,
file o sezione)

**Goal**:
L'esito dichiarato che la roadmap serve, preso dal documento di goal in input o dall'invocazione
della skill, e riscritto in testa a `roadmap.md`. È il metro con cui si chiede, a ogni update, se ciò
che resta in `NOW` arriva da qualche parte. Raggiungerlo svuota `NOW`; dichiararne uno nuovo fa
partire un `Redraw`. Un input che pretende sulla *destinazione* mette in discussione il goal; un
input che pretende sul *percorso* è lavoro, e il goal non si tocca.
_Avoid_: vision, obiettivo, milestone

**Slice**:
Un esito verticale singolo, indipendentemente schedulabile, con un solo learning target. Esiste solo
in `NOW`: ha un id, una riga nel register e un documento in `.roadmap/slices/`. Non è il nome
collettivo delle righe del register: uno spike ha id, riga e documento come una slice, ma non è una
slice.
_Avoid_: ticket, task, story (un ticket di `to-tickets` non va mai chiamato slice in questi
documenti, nonostante `to-tickets` chiami i propri ticket "tracer-bullet vertical slices"); spike

**Spike**:
Un'indagine timeboxed il cui prodotto è conoscenza: ha un learning target e nessun esito verticale,
e perciò non è una slice. Sta nel register con `kind: spike` perché è lavoro che occupa tempo e
sblocca slice successive, e una mappa che lo omette fa fare sense-making su informazione parziale.
Condivide tutto il resto con una slice — id dalla stessa sequenza, `Depends on`, readiness,
executor, documento, close-out in `.roadmap/archive/` — tranne `Audience`, che non si compila. Deve
avere un dipendente: o una slice lo elenca in `Depends on`, o la sua riga dichiara che valida la
fattibilità del goal. Occupa una riga sotto il limite di `NOW` come tutto il resto. A valle non passa
da `to-spec`: `prototype` se la domanda richiede di costruire qualcosa, `wayfinder` se è una scelta
da prendere.
_Avoid_: research slice, investigation slice, non-product work, timebox (non è un campo)

**Register**:
La tabella in `roadmap.md` che tiene il percorso verso il goal: una riga per ogni elemento di `NOW`,
slice o spike, con il titolo della riga e i soli metadati che servono a *confrontare* le righe fra
loro e decidere cosa viene prima — id, titolo, theme, kind, size, readiness, executor, `Depends on`.
Il titolo è un link al documento della riga, e il documento ha un link che riporta qui. La maggior
parte delle righe non è prendibile in mano oggi, ed è voluto: il register risponde a *qual è il
percorso*, non a *cosa posso fare adesso* — a quello risponde `readiness`. Ciò che serve a ragionare
*dentro* una riga sta nel suo documento, a partire dall'`Outcome`, che è la prima riga del documento
e non una colonna. Una riga chiusa esce dal register.
_Avoid_: slice index, index, tabella delle slice, backlog

**Id**:
L'identità stabile di una riga del register (`S0`, `S1`, …), assegnata alla promozione da `LATER` a
`NOW` per incremento monotòno. La sequenza è una sola: `kind` dice cosa è la riga, l'id no.
Sopravvive a riordini e inserimenti, non viene mai riciclata, e non esprime posizione: l'ordine di
consegna lo porta l'ordine del register.
_Avoid_: numero di slice, indice, posizione

**NOW**:
L'orizzonte di ciò che serve per arrivare al `Goal`: le slice che, prese tutte, ci portano, più gli
spike che servono a scoprire come. Solo ciò che sta in `NOW` ha id, riga nel register e documento. È
limitato — da tre o quattro slice a venti, quindici il numero a cui puntare — e il limite vincola la
granularità, non il conteggio: un problema
più grande non compra più righe, compra slice più ciccione. Non c'è gradiente di dettaglio al suo
interno: il documento di `S12` è sottile quanto quello di `S1`, e la minore confidenza si manifesta
in `Open questions` e `readiness`, non in un campo.

**LATER**:
L'orizzonte di ciò che non serve per *questo* goal: speculazione, o materiale per il goal
successivo. È uno strumento di focus, non un backlog. Da lì una candidate può morire o essere
promossa — e la promotion è il momento in cui si riconosce che qualcosa creduto laterale è invece
sul percorso.

**Candidate**:
Una voce di `LATER`: una riga in `roadmap.md`, senza id e senza documento. La promotion la
trasforma in slice, assegnandole id, riga nel register e documento.
_Avoid_: entry, item, idea, candidate capability, LATER slice

**OUT-OF-SCOPE**:
L'esclusione dichiarata: i problemi che la soluzione non risolve. Serve a giustificare i trade-off
che l'implementazione prende proprio perché quei problemi restano fuori. Nessun id, mai
implementata.
_Avoid_: wontfix (è il ruolo di `triage` per una richiesta esterna rifiutata), `.out-of-scope/` (è
la knowledge base di `triage`); la sezione `Out of Scope` di una spec è il confine di quella spec,
ereditato dalle esclusioni della slice

**Assumptions**:
La prima delle due sezioni di `roadmap.md` che riferiscono sull'input: cosa la skill ha preso per
vero *per poter* disegnare la mappa, ogni riga tracciata al tema o all'id che tocca. Chiede di essere
corretta, e di solito muore alla close-out, quando la consegna la conferma o la smentisce. Viene
prima di `Open questions`: un'assunzione presa in silenzio fa più danno di una domanda lasciata
visibilmente aperta. Insieme a `Open questions` dà all'autore una seconda lettura sulla completezza
della visione.
_Avoid_: Assumptions and gaps, assunzioni implicite

**Outcome**:
La prima riga del documento di slice: una frase che dice cosa la riga consegna. Sta lì e non nel
register perché il register nomina la riga con il titolo — quindici frasi incolonnate renderebbero
illeggibili le colonne accanto. Su uno spike dice quale conoscenza produce.
_Avoid_: esito in una riga come colonna del register, Outcome come sezione in fondo al documento

**Open questions**:
Ciò che è rimasto senza risposta, allo stesso nome a due altitudini: la seconda sezione di
`roadmap.md`, e il campo del documento di slice. Chiede una risposta e muore quando la riceve. A
deciderne l'altitudine è solo ciò che blocca — se mette in dubbio la *forma* della mappa sta in
`roadmap.md`, tracciata al tema o all'id che tocca; se blocca una sola slice sta su quella slice, e
si vede nel register come `readiness: needs-decision` oppure `needs-info`. Il nome è uno perché con
due si instraderebbe a sensazione invece che per scope, e perché il campo di slice tiene entrambi gli
stati: ciò che una slice aspetta da qualcun altro è una domanda, non una decisione di qualcuno. Non è
una coda di lavoro e non assegna id.
_Avoid_: Open decisions, unresolved, gaps, open issues, backlog di domande

**Requested by**:
Il riferimento in entrata del documento di slice: cosa ha prodotto la slice — un documento sorgente,
oppure, per il lavoro ammesso più tardi, la slice consegnata che l'ha resa visibile. Non si chiama
`Sources` perché quel nome è già preso a livello di roadmap.

**Kind**:
Colonna del register che dice cosa è una riga: `product`, `enabler`, `release` sono slice, `spike`
no. Sostituisce i tag `(Theme: …)`, `(Enabler: …)`, `(Release: delivery)` nel titolo.

**Size**:
Colonna del register con un segnale grossolano di dimensione, il cui unico effetto è instradare la
slice a valle: `large` passa da `to-tickets`, altrimenti si va diritti a `to-spec`. Non è un budget
di token, e su uno spike non decide nulla: lì instrada `kind`.

**Theme**:
Una promessa di prodotto rinviabile o cancellabile per intero, con un esito desiderato in linguaggio
di prodotto e una prima slice `NOW` che lo valida.

**Readiness**:
Colonna del register che dice se una slice si può prendere in mano: `ready`, `needs-decision` (una
scelta che l'autore possiede e non ha preso), `needs-info` (si aspetta qualcun altro). Non nomina
mai un attore: le etichette di `triage` si derivano all'handover combinandola con `executor`.
_Avoid_: usare direttamente `ready-for-agent` / `ready-for-human` come stato di slice

**Executor**:
Colonna del register che dice chi può eseguire la slice: `agent`, `human`, `mixed`. Esiste separata
da `readiness` perché quasi ogni slice infrastrutturale è `mixed`.

**Promotion**:
L'operazione che trasforma una candidate in slice: le assegna id, riga nel register e documento.

**Close-out**:
L'operazione che chiude una slice consegnata: la toglie dal register, sposta il documento in
`.roadmap/archive/` e assorbe l'evidenza prodotta nelle decisioni successive.
_Avoid_: reconcile, absorb (restano verbi nella definizione, mai nomi dell'operazione)

**Admission**:
L'operazione con cui lavoro nuovo entra in roadmap, come candidate in `LATER` o come slice in `NOW`.
Se porterebbe `NOW` oltre il limite, obbliga a fondere o a rimandare: la lista non cresce.

**Revision**:
L'operazione che rimaneggia slice esistenti senza aggiungerne né chiuderne: split, merge,
riscrittura, riordino. Lo split conserva l'id sulla metà che eredita il learning target; l'altra
metà ne riceve uno nuovo. Il merge segue la stessa regola all'incontrario: la riga che resta tiene
l'id del learning target che sopravvive, e l'altro id è speso.
_Avoid_: split/merge/reorder come nomi di operazioni distinte

**Retirement**:
L'operazione con cui una slice esce da `NOW` senza essere stata consegnata: muore, o retrocede a
candidate in `LATER`. L'id è speso e non torna disponibile; il documento non va in
`.roadmap/archive/` — che significa *consegnato* — ma viene cancellato, perché git è l'archivio di
ciò che non è mai successo.
_Avoid_: demotion (è il caso particolare, non il nome dell'operazione), wontfix

**Redraw**:
Il ridisegno della mappa quando viene dichiarato un goal nuovo. Si rifanno da zero `Goal`, temi,
register, criteri di ordinamento, `Assumptions` e `Open questions`; sopravvivono
`.roadmap/archive/`, il massimo id raggiunto, `OUT-OF-SCOPE` e `Cross-functional concerns` — e
un'esclusione che il goal nuovo contraddice si toglie in modo esplicito. Né `LATER` né le slice
ancora aperte passano in automatico: ogni candidate si rilegge una per una contro il goal nuovo, ogni
slice aperta si rigiustifica tenendo l'id oppure va in retirement. Non è un'operazione fra le cinque:
è il ramo di disegno che riparte con più input.
_Avoid_: reset, ricreazione, nuova roadmap

**Learning target**:
Ciò che la slice deve insegnare: uno solo, obbligatorio, ed è l'invariante che regge lo split test.
Il rischio non è un campo a sé — se è materiale è il learning target.
_Avoid_: Learning / risk

**Horizon**:
Nome collettivo in prosa dei tre orizzonti `NOW`, `LATER`, `OUT-OF-SCOPE`. Mai un campo, mai una
colonna, mai un'intestazione.
