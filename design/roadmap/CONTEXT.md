# Roadmap skill

Il vocabolario della skill di roadmap — [`ROADMAP-GOAL.md`](./ROADMAP-GOAL.md) e ciò
che ne nasce: l'artefatto vivente che decide *cosa fare dopo*, a monte della catena `to-spec` →
`to-tickets` → `implement`. Copre solo i termini di questo contesto; quelli della catena a valle sono
definiti dalle skill installate.

## Language

**Roadmap**:
L'artefatto vivente che tiene l'ordine di scoperta di un progetto verso un `Goal` dichiarato: temi,
slice `NOW`, speculazioni `LATER`, esclusioni `OUT-OF-SCOPE`. Vive in `.roadmap/`, è uno per
progetto, e non viene mai riscritto da zero. È uno strumento di sense making, non di precisione: non
porta date, stime, percentuali di completamento.
_Avoid_: plan, delivery plan, piano (`plan` resta solo verbo o attività, mai nome di artefatto,
file o sezione)

**Goal**:
L'esito dichiarato che la roadmap serve, preso dal documento di goal in input o dall'invocazione
della skill, e riscritto in testa a `roadmap.md`. È il metro con cui si chiede, a ogni update, se ciò
che resta in `NOW` arriva da qualche parte. Raggiungerlo svuota `NOW`; dichiararne uno nuovo è un
evento di `roadmap-create` sullo stesso `.roadmap/`, non di update.
_Avoid_: vision, obiettivo, milestone

**Slice**:
Un esito verticale singolo, indipendentemente schedulabile, con un solo learning target. Esiste solo
in `NOW`: ha un id, una riga nel register e un documento in `.roadmap/slices/`.
_Avoid_: ticket, task, story (un ticket di `to-tickets` non va mai chiamato slice in questi
documenti, nonostante `to-tickets` chiami i propri ticket "tracer-bullet vertical slices")

**Register**:
La tabella in `roadmap.md` che tiene il percorso verso il goal: una riga per slice `NOW`, con i soli
metadati che servono a *confrontare* le slice fra loro e decidere cosa viene prima — id, theme,
kind, size, readiness, executor, `Depends on`, esito in una riga. La maggior parte delle righe non è
prendibile in mano oggi, ed è voluto: il register risponde a *qual è il percorso*, non a *cosa posso
fare adesso* — a quello risponde `readiness`. Ciò che serve a ragionare *dentro* una slice sta nel
suo documento. Una slice chiusa esce dal register.
_Avoid_: slice index, index, tabella delle slice, backlog

**Id**:
L'identità stabile di una slice (`S0`, `S1`, …), assegnata alla promozione da `LATER` a `NOW` per
incremento monotòno. Sopravvive a riordini e inserimenti, non viene mai riciclata, e non esprime
posizione: l'ordine di consegna lo porta l'ordine del register.
_Avoid_: numero di slice, indice, posizione

**NOW**:
L'orizzonte di ciò che serve per arrivare al `Goal`: le slice che, prese tutte, ci portano. Solo le
slice `NOW` hanno id, riga nel register e documento. È limitato — da tre o quattro slice a venti,
quindici il numero a cui puntare — e il limite vincola la granularità, non il conteggio: un problema
più grande non compra più righe, compra slice più ciccione. Non c'è gradiente di dettaglio al suo
interno: il documento di `S12` è sottile quanto quello di `S1`, e la minore confidenza si manifesta
in `Open decisions` e `readiness`, non in un campo.

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

**Assumptions and gaps**:
La sezione di `roadmap.md` che riferisce sull'input: cosa la skill ha dovuto assumere per disegnare
la mappa (*assumed*) e cosa non è riuscita a risolvere (*unresolved*), ogni riga tracciata al tema o
all'id che tocca. Serve all'autore come seconda verifica sulla completezza della visione. Ci finisce
solo ciò che mette in dubbio la *forma* della mappa; ciò che blocca una singola slice sta nelle sue
`Open decisions`, con `readiness: needs-decision`. Non è una coda di lavoro: una voce muore quando
riceve risposta.
_Avoid_: Open questions, open issues

**Requested by**:
Il riferimento in entrata del documento di slice: cosa ha prodotto la slice — un documento sorgente,
oppure, per il lavoro ammesso più tardi, la slice consegnata che l'ha resa visibile. Non si chiama
`Sources` perché quel nome è già preso a livello di roadmap.

**Kind**:
Colonna del register che dice cosa è una slice: `product`, `enabler`, `release`. Sostituisce i tag
`(Theme: …)`, `(Enabler: …)`, `(Release: delivery)` nel titolo.

**Size**:
Colonna del register con un segnale grossolano di dimensione, il cui unico effetto è instradare la
slice a valle: `large` passa da `to-tickets`, altrimenti si va diritti a `to-spec`. Non è un budget
di token.

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
metà ne riceve uno nuovo.
_Avoid_: split/merge/reorder come nomi di operazioni distinte

**Retirement**:
L'operazione con cui una slice esce da `NOW` senza essere stata consegnata: muore, o retrocede a
candidate in `LATER`. L'id è speso e non torna disponibile; il documento non va in
`.roadmap/archive/` — che significa *consegnato* — ma viene cancellato, perché git è l'archivio di
ciò che non è mai successo.
_Avoid_: demotion (è il caso particolare, non il nome dell'operazione), wontfix

**Learning target**:
Ciò che la slice deve insegnare: uno solo, obbligatorio, ed è l'invariante che regge lo split test.
Il rischio non è un campo a sé — se è materiale è il learning target.
_Avoid_: Learning / risk

**Horizon**:
Nome collettivo in prosa dei tre orizzonti `NOW`, `LATER`, `OUT-OF-SCOPE`. Mai un campo, mai una
colonna, mai un'intestazione.
