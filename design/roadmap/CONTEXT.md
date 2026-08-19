# Roadmap skill

Il vocabolario della skill di roadmap — [`ROADMAP-GOAL.md`](./ROADMAP-GOAL.md) e ciò
che ne nasce: l'artefatto vivente che decide *cosa fare dopo*, a monte della catena `to-spec` →
`to-tickets` → `implement`. Copre solo i termini di questo contesto; quelli della catena a valle sono
definiti dalle skill installate.

## Language

**Roadmap**:
L'artefatto vivente che tiene l'ordine di scoperta di un progetto: temi, slice `NOW`, speculazioni
`LATER`, esclusioni `OUT-OF-SCOPE`. Vive in `.roadmap/`, è uno per progetto, e non viene mai
riscritto da zero.
_Avoid_: plan, delivery plan, piano (`plan` resta solo verbo o attività, mai nome di artefatto,
file o sezione)

**Slice**:
Un esito verticale singolo, indipendentemente schedulabile, con un solo learning target. Esiste solo
in `NOW`: ha un id, una riga nel register e un documento in `.roadmap/slices/`.
_Avoid_: ticket, task, story (un ticket di `to-tickets` non va mai chiamato slice in questi
documenti, nonostante `to-tickets` chiami i propri ticket "tracer-bullet vertical slices")

**Register**:
La tabella in `roadmap.md` che è la coda del lavoro aperto: una riga per slice `NOW`, con i soli
metadati che servono a *confrontare* le slice fra loro e decidere cosa viene prima — id, theme,
kind, size, readiness, executor, `Depends on`, esito in una riga. Ciò che serve a ragionare *dentro*
una slice sta nel suo documento. Una slice chiusa esce dal register.
_Avoid_: slice index, index, tabella delle slice

**Id**:
L'identità stabile di una slice (`S0`, `S1`, …), assegnata alla promozione da `LATER` a `NOW` per
incremento monotòno. Sopravvive a riordini e inserimenti, non viene mai riciclata, e non esprime
posizione: l'ordine di consegna lo porta l'ordine del register.
_Avoid_: numero di slice, indice, posizione

**NOW**:
L'orizzonte del lavoro su cui è importante concentrarsi adesso. Solo le slice `NOW` hanno id,
register e documento.

**LATER**:
L'orizzonte della speculazione: tutto ciò su cui non è importante concentrarsi adesso. È uno
strumento di focus, non un backlog. Da lì una candidate può morire o essere promossa.

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

**Learning target**:
Ciò che la slice deve insegnare: uno solo, obbligatorio, ed è l'invariante che regge lo split test.
Il rischio non è un campo a sé — se è materiale è il learning target.
_Avoid_: Learning / risk

**Horizon**:
Nome collettivo in prosa dei tre orizzonti `NOW`, `LATER`, `OUT-OF-SCOPE`. Mai un campo, mai una
colonna, mai un'intestazione.
