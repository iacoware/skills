# Ciclo di consenso su `plan-slices`

Lo strumento attivo per decidere se una modifica a `skills/plan-slices/SKILL.md` ha migliorato o
peggiorato lo skill. Documento autoconsistente: si legge in una sessione nuova senza altro contesto.

Il grading system — `GRADING-IMPROVEMENTS-PLAN.md`, `GRADING-EVAL-WORKFLOW.md`,
`grader-rubric.v3.json`, `fixtures/`, `results/calibration-*/` — è **sospeso** dietro il gate
descritto in fondo. Non è cancellato e non è un prerequisito di niente qui.

## L'obiettivo

Poter modificare `SKILL.md` e sapere se la modifica ha migliorato o peggiorato lo skill. Serve un
**segno con un errore noto**, non un numero: soglie, formula di aggregazione e score calibrato non
sono sul percorso di questa decisione.

## Perché non il grading system

Nessun miglioramento allo `SKILL.md` è finora derivato da uno score. Il più sostanzioso — `2c89e7f`,
separazione fra confine di scope e identità — nasce da un umano che ha letto un piano generato,
formulato un sospetto, verificato contro le fonti e scoperto che il difetto vero era un altro: la
giunzione non dichiarata. Nessuno dei 26 criteri della rubric conteneva quella proprietà, perché non
esisteva prima che la lettura la producesse. La lettura umana produce conoscenza nuova; il grading
system misura conoscenza già codificata.

Lo strumento decisionale c'era già, ed è l'**intersezione fra due modelli indipendenti sulle
modifiche proposte allo skill**. È un filtro di precisione, e il suo modo di sbagliare è mancare
qualcosa, non applicare qualcosa di falso. Su uno `SKILL.md`, dove ogni regola aggiunta è debito
permanente che condiziona ogni generazione futura, la precisione è la proprietà giusta da
massimizzare. Ne discendono due conseguenze:

- l'agreement inter-grader 0,56 misurato dal grading system è **irrilevante** per questo filtro: un
  disaccordo non corrompe l'output. Applicare comunque un punto discorde resta una decisione umana
  che costa una lettura in più e va pagata con un difetto citato, non con il numero;
- l'**adjudication è superflua**: risolvere un disaccordo con un terzo giudizio è più caro e meno
  sicuro che rimandarlo alla lettura di chi decide.

Il grading system sostituisce un filtro i cui errori sono visibili leggendo con una misura i cui
errori vanno stimati — e stimarli costa più dello strumento. I numeri della sproporzione e le
condizioni per riprenderlo stanno in `GRADING-IMPROVEMENTS-PLAN.md`.

## Vocabolario

- **Consenso** qui significa **intersezione fra giudizi indipendenti**, mai mediazione né terzo
  giudizio. Due modelli concordi sono la ragione più economica per applicare una modifica; due
  modelli discordi mandano il punto alla lettura umana, non a un arbitro.
- **`CON-N`** nei nomi degli artefatti nasce come «con la skill attiva», in opposizione a una
  baseline generata senza skill, prodotta solo alla prima iterazione. Oggi è di fatto il **contatore
  di ciclo**, ed è citato in questa forma da ogni cella `Misurato su` di `REGRESSION-LEDGER.md`. Resta
  così; una eventuale nuova generazione senza skill prenderà un token distinto.
- **Fasi** del ciclo: `improve`, `review`, `ledger`. Il nome `review` indica la sola fase 4 e i suoi
  artefatti, non il workflow.

## Il ciclo

1. **Generazione.** Ogni modello produce un piano dalle sole fonti in `recipe-app/sources/`:
   `results/PLAN-CC-CON-N.md` e `results/PLAN-CX-CON-N.md`.
2. **Validazione strutturale.** `make validate PLAN=…` su entrambi. Il validator non esprime giudizi
   semantici.
3. **`improve`.** Ogni modello riceve un payload cieco — `EVALUATION-BRIEF.md`, le fonti e i due
   candidati come `Candidate A`/`Candidate B` — e produce un piano di miglioramento dello skill sui
   difetti osservati in **entrambi** i candidati.
4. **`review`.** I due piani di miglioramento vengono confrontati fra loro: cosa è presente in
   entrambi, cosa in uno solo, su cosa sono in disaccordo.
5. **`ledger`.** Ogni riga di `REGRESSION-LEDGER.md` viene verificata sui piani appena generati, con
   citazione obbligatoria del punto pubblicato che regge il verdetto.
6. **Decisione umana.** Si decide cosa applicare allo `SKILL.md`. L'accordo fra i due modelli è la
   ragione più economica per applicare: il punto è già stato filtrato e non serve altra evidenza. Un
   punto sollevato da un solo modello si applica quando l'umano ritrova il difetto sul piano generato
   e lo giudica valido; in quel caso la modifica cita il difetto osservato, non il report che l'ha
   proposta. Ogni modifica applicata aggiunge una riga al registro.

I passi 3, 4 e 5 costano due chiamate ciascuno: sei per ciclo. L'output è markdown libero, quindi il
modo di fallimento che ha fermato la raccolta del grading system — risposta sintatticamente valida
ma non conforme a un contratto rigido, sei scarti su diciannove — qui non esiste.

Il ciclo nella forma dei passi 1-4 e 6 è esso stesso il risultato di un'evoluzione: i commit dello
skill precedenti al ciclo CON-4 nascono da conversazioni fra umano e agente sui piani generati, senza
confronto fra modelli. La maggior parte della storia dello skill non ha né previsioni scritte né una
traccia recuperabile da git.

### Cecità e simmetria

Dal ciclo CON-6 il payload di `improve` è **cieco e simmetrico**: nessun modello sa quale candidato
ha generato, e ognuno riporta i difetti di entrambi. Fino a CON-5 ogni modello migliorava il piano
che sapeva proprio. È un cambio di strumento, e i cicli attraverso questo confine non sono
confrontabili alla lettera: la colonna `Misurato su` del registro esiste per registrarlo.

La mappa `candidate-A`/`candidate-B` → piano → generatore vive in `support/AGENT-PLAN-MAP.md` ed è
esclusa da ogni payload **per costruzione**, perché i payload si compongono da una allowlist
esplicita di file. Il divieto scritto nei prompt serve solo all'esecuzione manuale.

## Il buco, ed è uno solo

Il ciclo **genera** miglioramenti e non **verifica** miglioramenti. Ogni giro produce una lista
fresca di difetti e non dice mai se la modifica del giro precedente ha funzionato. Il rischio è il
cricchetto: si aggiusta A rompendo B, il ciclo dopo si trova B, si aggiusta B rompendo A, e lo
`SKILL.md` cresce senza convergere. Il grading system è stato costruito per chiudere questo buco ed è
sproporzionato al buco.

La chiusura proporzionata è `REGRESSION-LEDGER.md`. Ogni modifica allo `SKILL.md` derivata da un
`REVIEW` implica una previsione falsificabile — *«al prossimo ciclo questo difetto non ricompare»* —
e il registro la rende obbligatoria: una riga per modifica applicata, con id, commit dello skill,
origine, affermazione verificabile, modo di verifica, ultimo controllo, artefatti su cui è stato
prodotto il verdetto ed esito.

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
  sospeso. Zero chiamate.
- **Fase 1 — procedura eseguibile.** Questo documento diventa eseguibile passo per passo; i prompt di
  `improve` e `review` escono da `PROMPTS.md`, che resta scratchpad umano, e diventano l'unica
  sorgente sotto `prompts/`; `scripts/runtime/` raccoglie invocazione provider, hash, scrittura
  atomica e resume, condivisi fra i due strumenti. Zero chiamate.
- **Fase 2 — CON-6 manuale.** Il ciclo si esegue nella forma cieca simmetrica con i prompt corretti,
  per far emergere dove la procedura documentata non corrisponde agli artefatti. Automatizzare prima
  significherebbe automatizzare una procedura non verificata.
- **Fase 3 — orchestratore.** `make consensus N=… PHASE=improve|review|ledger|report`, con dry-run,
  `CONFIRM_SEND`, resume e hash sul runtime condiviso. Sei chiamate a ciclo.
- **Fase 4 — generazione.** Anche il passo 1 passa dall'orchestratore.

## Gate verso il grading system

Il grading system si riprende **solo** se il ciclo, eseguito in questa forma, lascia sfuggire una
regressione reale: cioè se si scopre in ritardo un peggioramento che il registro non aveva
intercettato. Quella è l'evidenza che serve un rilevatore che guarda dove l'umano non sta guardando.
L'ipotesi che una regressione *possa* sfuggire non è evidenza. I test da eseguire in quel caso, il
budget residuo e la stop rule sono in `GRADING-IMPROVEMENTS-PLAN.md`.

## Limiti che restano

Tutto gira su un solo scenario, `recipe-app`: uno skill può migliorare su un dominio e peggiorare su
un altro. E «peggiorato» non è definito quando i segnali sono discordi: la decisione resta umana e
guarda quali criteri, non quanti.
