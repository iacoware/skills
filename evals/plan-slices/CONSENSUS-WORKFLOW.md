# Ciclo di consenso su `plan-slices`

Lo strumento attivo per decidere se una modifica a `skills/plan-slices/SKILL.md` ha peggiorato lo
skill. Documento autoconsistente: si legge in una sessione nuova senza altro contesto.

Il grading system — `GRADING-IMPROVEMENTS-PLAN.md`, `GRADING-EVAL-WORKFLOW.md`,
`grader-rubric.v3.json`, `fixtures/`, `results/calibration-*/` — è **abbandonato dal 2026-08-06**.
Non è un prerequisito di niente qui e non torna. Resta in git; la lapide è in fondo.

## L'obiettivo

Poter modificare `SKILL.md` e accorgersi quando la modifica ha **peggiorato** lo skill. Serve un
**segno con un errore noto**, non un numero: soglie, formula di aggregazione e score calibrato non
sono sul percorso di questa decisione.

L'obiettivo è asimmetrico per costruzione, e la formulazione precedente — *«sapere se la modifica ha
migliorato o peggiorato»* — prometteva più di quanto lo strumento dia. Il ciclo decide su **una
generazione per modello per ciclo**, e la regola di decisione del registro è *«un'affermazione regge
solo se regge su entrambi»*: basta **1 violazione su 2** per falsificare, servono **0 su 2** per
confermare. Il primo lato è solido — un controesempio è un controesempio. Il secondo è assenza di
controesempio su un campione di due.

Che il campione di due non basti non è teoria. Nel ciclo CON-5 `R-002` è violata su `CC` e non su
`CX`; `R-008` è violata su `CX` e non su `CC`. Due generazioni dello stesso ciclo, sulla stessa
regola, esito opposto: è la misura diretta della varianza del generatore, ed è dello stesso ordine di
grandezza dell'effetto che si sta cercando.

Da qui la semantica del registro: lo stato non è `tiene` ma **`non smentita ×k`**, con `k` il numero
di cicli consecutivi in cui la riga non è stata smentita su entrambi i piani. Una riga `×1` e una
`×5` non sono la stessa cosa, e la parola non deve più promettere ciò che il campione non dà. Il
miglioramento si inferisce solo dall'assenza cumulata di smentite, mai da un singolo giro.

La leva economica scelta è il **tempo, non il campione**: rigenerare k volte per lato moltiplica il
costo del ciclo e contraddice la proporzionalità che è la ragione stessa per cui il grading è stato
abbandonato. L'accumulo su cicli successivi dà lo stesso segnale gratis, con il ritardo come prezzo.

## Perché il grading system è abbandonato

Nessun miglioramento allo `SKILL.md` è mai derivato da uno score. Il più sostanzioso — `2c89e7f`,
separazione fra confine di scope e identità — nasce da un umano che ha letto un piano generato,
formulato un sospetto, verificato contro le fonti e scoperto che il difetto vero era un altro: la
giunzione non dichiarata. Nessuno dei 26 criteri della rubric conteneva quella proprietà, perché non
esisteva prima che la lettura la producesse. La lettura umana produce conoscenza nuova; il grading
system misura conoscenza già codificata.

A questo si aggiungono due proprietà che nessuna calibrazione corregge: **non è sostenibile** per il
ritmo di evoluzione di uno skill — 3.477 righe di Python e una matrice di calibrazione da
ricollezionare a ogni cambio di rubric, contro un `SKILL.md` che cambia più volte a settimana — e
**non è preciso** al livello a cui servirebbe, con un agreement inter-grader di 0,56.

Lo strumento decisionale alternativo è l'**intersezione fra due modelli indipendenti sulle modifiche
proposte allo skill**. Su uno `SKILL.md`, dove ogni regola aggiunta è debito permanente che
condiziona ogni generazione futura, un filtro che manca qualcosa costa meno di uno che applica
qualcosa di falso. Ne discende che l'**adjudication è superflua**: risolvere un disaccordo con un
terzo giudizio è più caro e meno sicuro che rimandarlo alla lettura di chi decide.

**Che l'intersezione sia davvero un filtro di precisione è però un'ipotesi non ancora verificata, e
CON-6 è il suo primo test.** Vedi *Lo stato dell'evidenza* qui sotto.

## Lo stato dell'evidenza

Va letto prima di fidarsi di qualunque affermazione di questo documento sulla bontà del filtro.

- Le fasi `improve` e `review` sono state eseguite **una volta sola**, nel ciclo CON-4, con prompt poi
  cambiati.
- In quell'unica esecuzione i due `IMPROVEMENT` sono arrivati a **246 righe** (`CC`) contro **10**
  (`CX`), ed entrambi violavano la struttura obbligatoria del prompt — vedi *Il rischio di
  non-conformità*. L'intersezione è stata quindi calcolata mappando bullet generici su sezioni
  operative, e la formulazione entrata nello `SKILL.md` è quasi sempre quella del lato specifico.
- Sei righe del registro — `R-002`…`R-007` — portano `Origine: intersezione — REVIEW CON-4`. Sono
  state applicate da un filtro con un lato non conforme. Cinque di esse risultano `non smentita`; non
  se ne deduce che il filtro funzioni, solo che quelle regole non sono state smentite.
- Il ciclo CON-5 è **parziale**: generazione più lettura offline del registro, senza `improve` né
  `review`. Ha comunque prodotto due regressioni e due commit dello skill.
- La fase `ledger` a due modelli non è **mai** stata eseguita.

Quindi lo strumento non è «già esistente e da formalizzare»: **CON-6 è la sua prima esecuzione nella
forma documentata.** Il criterio con cui giudicarlo non è che produca tutti gli artefatti previsti,
ma che i due `IMPROVEMENT` abbiano **specificità comparabile**, cioè che l'intersezione sia letterale
e non una mappatura generico → operativo. Se non lo è, la tesi è falsificata al primo giro, e lo si
scopre prima di automatizzare sei chiamate.

## Vocabolario

- **Consenso** qui significa **intersezione fra giudizi indipendenti**, mai mediazione né terzo
  giudizio. Due modelli concordi **e ugualmente specifici** sono la ragione più economica per
  applicare una modifica; due modelli discordi mandano il punto alla lettura umana, non a un arbitro.
- **`CON-N`** nei nomi degli artefatti nasce come «con la skill attiva», in opposizione a una
  baseline generata senza skill, prodotta solo alla prima iterazione. Oggi è di fatto il **contatore
  di ciclo**, ed è citato in questa forma da ogni cella `Misurato su` di `REGRESSION-LEDGER.md`. Resta
  così; una eventuale nuova generazione senza skill prenderà un token distinto.
- **Ciclo parziale.** CON-5 non ha artefatti `IMPROVEMENT` né `REVIEW`: si è fermato alla generazione,
  e i suoi verdetti nascono da lettura offline. Il token non si riusa comunque — nove righe del
  registro e due citazioni testuali lo referenziano, e riusarlo le renderebbe ambigue.
- **Fasi** del ciclo: `improve`, `review`, `ledger`. Il nome `review` indica la sola fase 4 e i suoi
  artefatti, non il workflow.
- **`non smentita ×k`** è lo stato di una riga del registro che k cicli consecutivi non hanno
  falsificato su nessuno dei due piani. Sostituisce `tiene`, che prometteva conferma.
- **Recidiva** è la quota dei difetti sollevati da `improve` che ricadono su un tema coperto da una
  riga `non smentita`. Se è sistematicamente maggiore di zero, il registro sta mentendo su ciò che
  dichiara chiuso.

## Il ciclo

1. **Generazione.** Ogni modello produce un piano dalle sole fonti in `recipe-app/sources/`:
   `recipe-app/results/PLAN-CC-CON-N.md` e `recipe-app/results/PLAN-CX-CON-N.md`.
2. **Validazione strutturale.** `make validate PLAN=…` su entrambi. Il validator non esprime giudizi
   semantici.
3. **`improve`.** Ogni modello riceve un payload cieco — `EVALUATION-BRIEF.md`, le fonti e i due
   candidati come `Candidate A`/`Candidate B` — e produce un piano di miglioramento dello skill sui
   difetti osservati in **entrambi** i candidati.
4. **Gate di conformità.** Blocco duro, nessuna chiamata: un `IMPROVEMENT` privo dei campi
   obbligatori si **rigenera** prima di procedere. Vedi *Il rischio di non-conformità*.
5. **`review`.** I due piani di miglioramento vengono confrontati fra loro: cosa è presente in
   entrambi, cosa in uno solo, su cosa sono in disaccordo, e — per ogni voce condivisa — **quale dei
   due lati porta la formulazione operativa**.
6. **`ledger`.** Ogni riga di `REGRESSION-LEDGER.md` viene verificata sui piani appena generati, con
   citazione obbligatoria del punto pubblicato che regge il verdetto.
7. **Contatori.** Il report registra righe di `SKILL.md`, numero di difetti distinti sollevati
   dall'unione dei due `improve`, e recidiva. Non sono uno score: sono il termometro del cricchetto.
8. **Decisione umana.** L'accordo fra i due modelli **su punti di pari specificità** è la ragione più
   economica per applicare: il punto è già stato filtrato. Una voce condivisa in cui solo un lato è
   operativo vale come punto sollevato da un solo modello, e la sua riga di registro nasce `giudizio`,
   non `intersezione`. Un punto sollevato da un solo modello si applica quando l'umano ritrova il
   difetto sul piano generato e lo giudica valido; in quel caso la modifica cita il difetto osservato,
   non il report che l'ha proposta. Ogni modifica applicata aggiunge una riga al registro.

I passi 3, 5 e 6 costano due chiamate ciascuno: sei per ciclo.

Il ciclo nella forma dei passi 1-3, 5 e 8 è esso stesso il risultato di un'evoluzione: i commit dello
skill precedenti al ciclo CON-4 nascono da conversazioni fra umano e agente sui piani generati, senza
confronto fra modelli. La maggior parte della storia dello skill non ha né previsioni scritte né una
traccia recuperabile da git.

### `improve` è bidirezionale

Il prompt chiede, per ogni voce, due campi oltre al rimedio:

- **`Regola esistente che non ha impedito il difetto`** — quale clausola dello `SKILL.md` avrebbe
  dovuto coprirlo e non l'ha fatto, oppure la dichiarazione esplicita che nessuna esiste.
- **`Costo`** — cosa si può togliere o fondere se questa entra.

**Regola dura in fase di decisione:** se il primo campo nomina una clausola esistente, il rimedio di
default è **riformularla**. Una modifica che aggiunge righe non si applica finché la riformulazione
non è stata tentata e scartata con una ragione. Il perché sta in *Il cricchetto*.

### Cecità e simmetria

Dal ciclo CON-6 il payload di `improve` è **cieco e simmetrico**: nessun modello sa quale candidato
ha generato, e ognuno riporta i difetti di entrambi. Fino a CON-5 ogni modello migliorava il piano
che sapeva proprio.

La cecità è **nominale**: un modello può riconoscere il proprio stile anche senza etichetta. È un
limite dichiarato, non mitigato — mitigarlo costerebbe più di quanto il rischio valga.

La mappa `candidate-A`/`candidate-B` → piano → generatore vive in `support/AGENT-PLAN-MAP.md` ed è
esclusa da ogni payload **per costruzione**, perché i payload si compongono da una allowlist
esplicita di file. Il divieto scritto nei prompt serve solo all'esecuzione manuale.

Il prompt `improve` esclude inoltre dall'analisi ogni problema relativo al **walking skeleton**. È
una restrizione di scope reale del ciclo, non un dettaglio del prompt.

### Confini di strumento

Cicli separati da un confine **non sono confrontabili alla lettera**. La colonna `Misurato su` del
registro esiste per registrarli, e ne porta il ciclo, i piani, gli strumenti, **il modello e
l'effort**. I confini noti:

- **CON-4 → CON-5.** I prompt sono cambiati. Le righe `R-002`…`R-007`, etichettate `intersezione`,
  sono state prodotte con prompt diversi da quelli oggi in `prompts/`.
- **CON-5 → CON-6.** Payload cieco e simmetrico; gate di conformità; `improve` bidirezionale.
- **CON-5 → CON-6, effort.** I due modelli passano da `high` a `medium`. `high` è l'unica
  configurazione mai esercitata contro provider reali.
- **Dopo la fase di modularizzazione e pruning.** Spostare testo dello skill in file caricati
  on-demand cambia ciò che il modello ha in contesto al momento di generare. Non è un refactor neutro:
  è un cambio di strumento al pari degli altri.

## Il rischio di non-conformità

Il documento in precedenza affermava che l'output è markdown libero e che quindi il modo di
fallimento del grading system — risposta sintatticamente valida ma non conforme a un contratto
rigido, sei scarti su diciannove — qui non esiste. **L'affermazione è ritirata: la premessa e la
conclusione sono entrambe false.**

Un contratto c'è: `PROMPTS.md` § *CREATE IMPROVEMENTS* impone titolo, `## Inputs`, una sezione per
miglioramento con otto campi obbligatori e `## Verifica finale`. Nell'unica esecuzione mai fatta:

| | `CC` | `CX` |
|---|---|---|
| Titolo richiesto | no | no |
| `## Inputs` | assente | assente |
| Sezione per miglioramento | sì, 10 | **nessuna**: 8 bullet |
| Otto campi obbligatori | parziale | **zero** |
| `## Verifica finale` | assente | assente |

La disparità 246 contro 10 righe non è differenza di qualità fra modelli: è non-conformità, grave su
un lato. E la differenza con il grading system è a sfavore del ciclo: là la non-conformità produceva
uno **scarto visibile**; qui ha prodotto un artefatto **accettato**, propagato in `review` e da lì in
sei righe di registro etichettate `intersezione`. Il modo di fallimento non è stato eliminato, è
stato reso silenzioso.

Da qui il gate di conformità al passo 4, come **blocco duro**. Un warning su un artefatto che nessuno
ha guardato per due cicli è esattamente ciò che è già successo.

## Il cricchetto

Il ciclo **genera** miglioramenti e non **verifica** miglioramenti. Ogni giro produce una lista
fresca di difetti e non dice mai se la modifica del giro precedente ha funzionato. Il rischio è il
cricchetto: si aggiusta A rompendo B, il ciclo dopo si trova B, si aggiusta B rompendo A, e lo
`SKILL.md` cresce senza convergere.

**Non è un rischio emergente: è la funzione di trasferimento dello strumento.** Un difetto entra in
`improve`, esce come regola nuova, arriva nello `SKILL.md`, diventa riga di registro. Fino al ciclo
CON-6 non esisteva nessun percorso per cui un difetto uscisse come *«questa regola esistente è
formulata male»*. La firma è misurabile:

```
2026-07-30  c001780   247 righe   Add plan-slices skill
2026-07-31  2c89e7f   264
2026-07-31  745192f   312
2026-08-02  d977043   354
2026-08-02  8c7fe34   352   ← unico commit sottrattivo, -7 righe
2026-08-04  9aa2586   382
2026-08-04  eb926bb   389
2026-08-06  28b5460   417 righe
```

**+69% in sette giorni, 18 commit, un solo commit che toglie qualcosa.** `R-010` e `R-011` sono
entrambe correzioni di righe precedenti (`R-002`, `R-008`) ed **entrambe sono entrate come regole
aggiuntive**, non come riformulazioni delle regole che avevano fallito — perché nessun'altra forma
era disponibile.

Il principio mancante era già scritto, nel posto sbagliato. `REGRESSION-LEDGER.md`: *«La sequenza di
regressioni sullo stesso tema è il segnale che la regola è formulata male, non che va riscritta
ancora.»* Il registro sapeva che un difetto ricorrente accusa una regola esistente; il prompt che
genera i rimedi non lo sapeva, e non aveva modo di dirlo.

Tre rimedi, tutti a costo zero di chiamate:

- **`improve` bidirezionale con regola dura**, sopra.
- **Righe di registro sottrattive.** Una riga può nascere `Origine: potatura`, con l'affermazione
  «la rimozione di X non fa ricomparire il difetto Y». Prima il registro poteva registrare solo
  crescita, quindi anche la sua storia era cieca al fenomeno.
- **Contatori e recidiva**, passo 7. Se la recidiva è sistematicamente maggiore di zero, il registro
  sta dichiarando chiuso ciò che non lo è. Se è zero mentre lo `SKILL.md` continua a crescere, il
  ciclo trova cose genuinamente nuove — legittimo, ma prima o poi va chiesto se quella crescita sia
  sostenibile.

## Il registro

La chiusura proporzionata al buco è `REGRESSION-LEDGER.md`. Ogni modifica allo `SKILL.md` derivata da
un `REVIEW` implica una previsione falsificabile — *«al prossimo ciclo questo difetto non
ricompare»* — e il registro la rende obbligatoria: una riga per modifica applicata, con id, commit
dello skill, origine, affermazione verificabile, modo di verifica, ultimo controllo, artefatti e
strumenti su cui è stato prodotto il verdetto, ed esito.

Lo stesso registro copre anche le regressioni **non previste**, senza un secondo artefatto: se il
piano di miglioramento del ciclo N solleva un difetto che il ciclo N-2 aveva chiuso, quella è una
regressione, ed è output che già si paga e che altrimenti si butta via. Serve solo l'indice per
riconoscerla quando ricompare.

**La falsificabilità sta nella formulazione della riga, non nell'automazione.** Automatizzare la fase
`ledger` non rende falsificabile ciò che non lo era: serve a garantire che il controllo **avvenga**
ogni ciclo e che ogni verdetto citi il punto del piano che lo regge. Delle undici righe attuali solo
R-011, e metà di R-008, sono decidibili dal validator strutturale — il controllo esiste già in
`skills/plan-slices/scripts/validate_plan.py`. Le altre richiedono il confronto con il brief, cioè un
giudizio: la fase `ledger` lo chiede a due modelli indipendenti e applica lo stesso filtro di
consenso delle altre fasi.

## Quando una valutazione segnala un peggioramento

Se il confronto dice `better` su tre criteri e `worse` su uno, la mossa giusta è l'indagine
qualitativa: chiedere all'agente quale criterio è peggiorato e quale regola dello `SKILL.md` può
averlo causato. Vincolo obbligatorio: l'agente produrrà sempre una spiegazione plausibile, anche in
assenza di nesso. Vale solo se nomina una clausola specifica e genera una previsione falsificabile —
*«togli o riformula questa clausola e il criterio risale»* — verificata rigenerando. Senza il passo di
falsificazione è un racconto ben scritto.

## Cosa il ciclo eredita dal grading system

Costruito, pagato e riusato subito: il validator strutturale `validate_plan.py`;
`recipe-app/EVALUATION-BRIEF.md`, che sostituisce il confronto con un piano ideale — confrontare con
un piano ideale misura la somiglianza a quel piano, non la qualità; l'anonimizzazione dei candidati;
la tassonomia dei sette assi di lettura, che coincide con quella della rubric v3; l'hashing di
prompt, fonti e brief con artefatti immutabili, che tiene i cicli confrontabili; la disciplina di
`NOTES.md`. Non serve la scala a cinque verdetti, non serve lo score.

## Stato dell'automazione

- **Fase 0 — separazione.** Documenti e artefatti dei due strumenti distinti; grading marcato come
  abbandonato. Zero chiamate.
- **Fase 1 — procedura eseguibile.** Questo documento diventa eseguibile passo per passo; i prompt di
  `improve`, `review` e `ledger` escono da `PROMPTS.md`, che resta scratchpad umano, e diventano
  l'unica sorgente sotto `prompts/`; il gate di conformità è specificato qui. Zero chiamate.
- **Fase 2 — CON-6 manuale.** Il ciclo si esegue nella forma cieca simmetrica con i prompt corretti,
  per far emergere dove la procedura documentata non corrisponde agli artefatti — e per testare
  l'ipotesi di *Lo stato dell'evidenza*. Sei chiamate.
- **Fase 3 — riorganizzazione del codice.** Zero chiamate.
- **Fase 4 — modularizzazione e pruning dello skill.** Zero chiamate; si verifica su CON-7.
- **Fase 5 — orchestratore.** `make consensus N=… PHASE=improve|review|ledger|report`, con dry-run,
  `CONFIRM_SEND`, resume e hash. Sei chiamate a ciclo.
- **Fase 6 — generazione.** Anche il passo 1 passa dall'orchestratore.

## Lapide del grading system

Abbandonato il **2026-08-06**. Non sospeso, non dietro un gate: non torna.

Le due ragioni sono in *Perché il grading system è abbandonato* — non sostenibile per il ritmo di
evoluzione di uno skill, e non preciso al livello a cui servirebbe. Il codice e i documenti restano
in git e sono recuperabili dalla storia; non sono mantenuti.

Il gate di ripresa che questo documento portava fino al 2026-08-06 era anche **irraggiungibile per
costruzione**: prevedeva la ripresa solo se il ciclo avesse lasciato sfuggire una regressione reale,
scoperta in ritardo — ma l'unico rilevatore in servizio è il ciclo stesso, e la classe di regressioni
per cui il grading era stato costruito è proprio quella su dimensioni che nessuna riga del registro
copre. Nessuno strumento la guardava, quindi non poteva mai far scattare il gate. La **recidiva**
sopravvive a quel gate, con scopo diverso: non è una porta di rientro al grading, è il segnale di
convergenza del ciclo di consenso.

## Limiti che restano

- **Un solo scenario.** Tutto gira su `recipe-app`: uno skill può migliorare su un dominio e
  peggiorare su un altro. Limite accettato, non risolto: un secondo scenario raddoppia il costo di
  ogni ciclo.
- **Varianza di generazione.** `n = 1` per lato, nessuna ripetizione prevista in nessuna fase. Un
  before/after singolo confonde l'effetto della modifica con la variabilità di una generazione, e il
  disaccordo fra i due lati su `R-002` e `R-008` mostra che la varianza è già visibile a questa scala.
  È il limite da cui discende la semantica `non smentita ×k`.
- **`non smentita` non è conferma.** Sette righe su undici hanno questo stato, e sono proprio quelle
  che autorizzerebbero a smettere di guardare una regola.
- **Cecità nominale.** Vedi *Cecità e simmetria*.
- **Il registro non pensiona righe.** Ogni ciclo rilegge tutte le righe `non smentita`, e le righe
  crescono di una per modifica applicata; la fase di pruning ne aggiungerà. Il costo della fase
  `ledger` cresce in modo monotono. Rinviato il 2026-08-06 come non urgente; il contatore di recidiva
  lo renderà visibile quando morde.
- **«Peggiorato» non è definito quando i segnali sono discordi.** La decisione resta umana e guarda
  quali criteri, non quanti.
