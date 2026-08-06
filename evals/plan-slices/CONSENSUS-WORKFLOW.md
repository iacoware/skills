# Ciclo di consenso su `plan-slices`

Lo strumento attivo per decidere se una modifica a `skills/plan-slices/SKILL.md` ha peggiorato lo
skill. Documento autoconsistente: si legge in una sessione nuova senza altro contesto.

Il grading system — `GRADING-IMPROVEMENTS-PLAN.md`, `GRADING-EVAL-WORKFLOW.md`,
`grader-rubric.v3.json`, `fixtures/`, `results/calibration-*/` — è **abbandonato dal 2026-08-06**.
Non è un prerequisito di niente qui e non torna. Resta in git; la lapide è in fondo.

Dal 2026-08-06 la lingua del progetto è l'**inglese**. Questo documento e il registro sono ancora in
italiano e migrano nelle fasi 0b e 1c; ogni artefatto nuovo nasce in inglese.

## L'obiettivo

Poter modificare `SKILL.md` e accorgersi quando la modifica ha **peggiorato** lo skill. Serve un
**segno con un errore noto**, non un numero: soglie, formula di aggregazione e score calibrato non
sono sul percorso di questa decisione.

L'obiettivo si regge su **due meccanismi disgiunti, con due prove diverse**. Confonderli era
l'errore della stesura precedente, e rendeva irrisolvibili le domande aperte del piano.

- **`REGRESSION-LEDGER.md` rileva il peggioramento, ex-post, sulle dimensioni che copre.** Ogni
  modifica applicata implica una previsione falsificabile; il registro la conserva e il ciclo la
  ricontrolla. È l'unico rilevatore in servizio. Che le sue righe siano falsificabili non è
  un'ipotesi: due lo sono state. Che la copertura sia parziale nemmeno — undici righe contro 417 di
  skill.
- **L'intersezione fra `improve` e `review` previene il peggioramento, ex-ante, su una classe sola:
  le regole false.** Non guarda mai la modifica del giro precedente. È un generatore di proposte con
  un filtro di precisione sulle proposte. Che il filtro sia preciso è **un'ipotesi non ancora
  verificata**, e CON-6 è il suo primo test.

Ne discende la conseguenza che il piano prima negava: **una falsificazione dell'ipotesi non fa cadere
l'obiettivo.** Fa cadere l'economia con cui si decide cosa applicare. Il registro funzionerebbe senza
il filtro; il filtro senza il registro non si accorgerebbe di niente.

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

Lo stesso principio si applica a se stesso: il filtro va tarato per mancare, non per applicare. Da qui
lo scarto per voce con un solo tentativo, la regola dei due lati su `review`, e il fatto che il ciclo
applichi da sé **solo** ciò che il filtro licenzia.

## Lo stato dell'evidenza

Va letto prima di fidarsi di qualunque affermazione di questo documento sulla bontà del filtro.

- Le fasi `improve` e `review` sono state eseguite **una volta sola**, nel ciclo CON-4, con prompt poi
  cambiati.
- In quell'unica esecuzione i due `IMPROVEMENT` sono arrivati a **246 righe** (`CC`) contro **10**
  (`CX`), ed entrambi violavano la struttura obbligatoria del prompt — vedi *Il contratto di
  conformità*. L'intersezione è stata quindi calcolata mappando bullet generici su sezioni operative,
  e la formulazione entrata nello `SKILL.md` è quasi sempre quella del lato specifico.
- **Sette righe del registro** — `R-002`…`R-008` — portano `Origine: intersezione — REVIEW CON-4`.
  La stesura precedente ne contava sei, escludendo `R-008` senza ragione: stessa provenienza, stesso
  `REVIEW`, stesso lato non conforme.
- Di quelle sette, **due sono state falsificate al primo ciclo utile**: `R-002` su `CC` e `R-008` su
  `CX`. Cinque su sette risultano `non smentita ×1`.
- Le sette righe sono state **riclassificate `intersezione-tema`** il 2026-08-06. Lo dicono i `REVIEW`
  stessi, campo `Differences`, ripetuto su ogni voce condivisa: *«questo report è operativo […];
  l'altro report propone il meccanismo generico»*. Il tema era condiviso, la formulazione veniva da un
  lato solo.
- Le due falsificazioni cadono esattamente dove `intersezione-tema` prevede. Una riga falsificata non
  significa che il difetto identificato fosse falso: significa che **la formulazione scritta non ha
  morso**. La diagnosi di `R-002` è che la clausola dello skill era autocontraddittoria; quella di
  `R-008` riga A è un puntamento sbagliato. In entrambi i casi il tema era giusto — l'avevano visto
  due modelli — e il rimedio era di un lato solo.
- Il ciclo CON-5 è **parziale**: generazione più lettura offline del registro, senza `improve` né
  `review`. Ha comunque prodotto due regressioni e due commit dello skill. È la dimostrazione che il
  rilevatore gira da solo.
- Le fasi `verdetto` e `recidiva` a modelli non sono **mai** state eseguite.

Quindi lo strumento non è «già esistente e da formalizzare»: **CON-6 è la sua prima esecuzione nella
forma documentata.** Il criterio con cui giudicarlo non è che produca tutti gli artefatti previsti, ma
che i due `IMPROVEMENT` abbiano **specificità comparabile**, cioè che l'intersezione sia letterale e
non una mappatura generico → operativo. Il contratto di conformità rende quella proprietà una forma
da riempire invece che un giudizio da emettere.

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
- **Fasi** del ciclo: `improve`, `review`, `verdetto`, `recidiva`. `ledger` indica **solo il
  registro**, mai una fase: prima nominava un file, una fase e due lavori diversi.
- **`non smentita ×k`** è lo stato di una riga del registro che k cicli consecutivi non hanno
  falsificato su nessuno dei due piani. Sostituisce `tiene`, che prometteva conferma.
- **Riga dormiente.** Una riga a `non smentita ×3` passa dormiente: verificata 1 ciclo su 3 anziché
  ogni ciclo. Non si cancella e non esce dal registro. Torna attiva immediatamente se `recidiva` la
  risolleva.
- **Recidiva** è la quota dei difetti sollevati da `improve` che ricadono su un tema coperto da una
  riga del registro. Se è sistematicamente maggiore di zero, il registro sta mentendo su ciò che
  dichiara chiuso. È anche il segnale che risveglia le righe dormienti, cioè ciò che rende sicura la
  dormienza.
- **`Origine`** di una riga: `intersezione` (tema **e** rimedio condivisi), `intersezione-tema` (tema
  condiviso, rimedio da un lato solo), `giudizio` (un lato solo, o umano), `potatura` (rimozione).

## Il ciclo

1. **Generazione.** Ogni modello produce un piano dalle sole fonti in `recipe-app/sources/`:
   `recipe-app/results/PLAN-CC-CON-N.md` e `recipe-app/results/PLAN-CX-CON-N.md`.
2. **Validazione strutturale.** `make validate PLAN=…` su entrambi. Il validator non esprime giudizi
   semantici.
3. **`improve`.** Ogni modello riceve un payload cieco — `EVALUATION-BRIEF.md`, le fonti e i due
   candidati come `Candidate A`/`Candidate B` — e produce un piano di miglioramento dello skill sui
   difetti osservati in **entrambi** i candidati, nella forma di `assets/improvement-template.md`.
4. **Gate di conformità.** `validate_improvement.py`. Una voce priva di un campo obbligatorio, o con
   un riferimento che non si risolve, viene **scartata e registrata**. Nessuna rigenerazione. Vedi
   *Il contratto di conformità*.
5. **`review`.** Payload **cieco e simmetrico**: i due `IMPROVEMENT` come `Report A`/`Report B`,
   nessun «il tuo report». Ogni modello classifica ciascuna voce in condivisa, unica ad A, unica a B,
   contraddittoria; per ogni voce condivisa dichiara se i due lati portano **lo stesso rimedio** o
   solo lo stesso tema.
6. **`verdetto`.** Ogni riga attiva del registro viene verificata sui piani appena generati, con
   citazione obbligatoria del punto pubblicato che regge il verdetto. Un verdetto la cui citazione non
   si risolve viene scartato e registrato. Le righe dormienti entrano 1 ciclo su 3.
7. **`recidiva`.** Una sola chiamata, modello fisso. Produce l'elenco delle coppie `voce improve →
   riga di registro | nessuna`, su **tutte** le righe, dormienti incluse. Non un numero: l'elenco.
8. **Applicazione.** Il workflow applica al working tree **solo ciò che il filtro licenzia** — le
   voci classificate condivise da **entrambi** i `REVIEW`. Una voce = **un hunk di `SKILL.md` + una
   riga di registro**, stesso id. Le righe nascono con `Commit SKILL.md: (pending)`. **Il workflow
   non committa mai.**
9. **Report.** `recipe-app/results/CONSENSUS-CON-N.REPORT.md`, con i contatori **in testa**.
10. **Veto umano.** Si leggono i contatori, poi `git diff`. Si rifiuta il batch, o una voce per id.
    Ciò che sopravvive lo committa l'umano.

Esecuzioni per ciclo:

| fase | esecuzioni |
|---|---|
| generazione | 2 |
| `improve` | 2 |
| `review` | 2 |
| `verdetto` | 2 |
| `recidiva` | 1 |
| **totale** | **9**, di cui 7 dopo la generazione |

Qualifica obbligatoria dell'unità: in **Fase 2** un'esecuzione è una sessione agentica che può
delegare internamente; in **Fase 5** ogni delega è una chiamata contata dal dry-run, ed è quel numero
che `evals/AGENTS.md` chiede di autorizzare. Dire «sei chiamate a ciclo» senza qualificare l'unità era
falso in entrambi i regimi: i prompt di `PROMPTS.md` delegano già a due sub-agent ciascuno.

Il ciclo nella forma dei passi 1-3, 5 e 8 è esso stesso il risultato di un'evoluzione: i commit dello
skill precedenti al ciclo CON-4 nascono da conversazioni fra umano e agente sui piani generati, senza
confronto fra modelli. La maggior parte della storia dello skill non ha né previsioni scritte né una
traccia recuperabile da git.

### Cosa il workflow applica da sé e cosa no

Il passo 8 è automatico solo dove il filtro è portante. Tre insiemi disgiunti:

- **Condivisa da entrambi i `REVIEW`, stesso rimedio** → applicata, `Origine: intersezione`.
- **Condivisa da entrambi i `REVIEW`, rimedi diversi** → applicata con la formulazione del lato che
  la porta, `Origine: intersezione-tema`. Due lettori indipendenti che vedono rotta la stessa area
  sono evidenza reale; che concordino anche sulla cura è un evento separato e più raro.
- **Condivisa da un `REVIEW` solo, o unica a un lato** → **non applicata**. Va nell'elenco dei punti
  che richiedono lettura umana. Si applica quando l'umano ritrova il difetto sul piano generato e lo
  giudica valido; in quel caso la riga nasce `giudizio` e la modifica cita il difetto osservato, non
  il report che l'ha proposta.

La regola dura di `improve` bidirezionale è meccanica allo stesso passo: se il campo `Regola esistente
che non ha impedito il difetto` nomina una clausola e la voce aggiunge righe **senza** la ragione
scritta per cui la riformulazione è stata scartata, la voce **non si applica da sé** e passa
all'elenco umano.

### `improve` è bidirezionale

Il template chiede, per ogni voce, due campi oltre al rimedio:

- **`Regola esistente che non ha impedito il difetto`** — quale clausola dello `SKILL.md` avrebbe
  dovuto coprirlo e non l'ha fatto, oppure la dichiarazione esplicita che nessuna esiste.
- **`Costo`** — cosa si può togliere o fondere se questa entra.

**Regola dura:** se il primo campo nomina una clausola esistente, il rimedio di default è
**riformularla**. Una modifica che aggiunge righe non si applica finché la riformulazione non è stata
tentata e scartata con una ragione. Il perché sta in *Il cricchetto*.

La regola è applicabile solo se esiste la **mappa clausola → riga di registro**. Davanti a «la
clausola X non ha impedito il difetto» servono tre risposte che il registro da solo non dà, perché
traccia i commit e non le clausole, e ci sono state diciotto riscritture: X esiste ancora nella forma
che una riga afferma? X ha una riga, e quindi riformularla ne rompe la previsione? Se non ha nessuna
riga, il rimedio nasce scoperto. Senza la mappa il default resta quello che è sempre stato — aggiungere
una regola nuova — e il meccanismo costruito per fermare il cricchetto lo alimenta.

### Cecità e simmetria

Dal ciclo CON-6 i payload di `improve` **e di `review`** sono **ciechi e simmetrici**: nessun modello
sa quale candidato ha generato né quale `IMPROVEMENT` ha scritto. Fino a CON-5 ogni modello migliorava
il piano che sapeva proprio, e recensiva il proprio report contro quello dell'altro — cioè la fase che
assegna l'etichetta di precisione sapeva di chi era ogni punto.

La cecità è **nominale**: un modello può riconoscere il proprio stile anche senza etichetta. È un
limite dichiarato, non mitigato — mitigarlo costerebbe più di quanto il rischio valga. Il contratto di
conformità la indebolisce ulteriormente, chiedendo riferimenti localizzati ai candidati.

La mappa `candidate-A`/`candidate-B` → piano → generatore vive in `support/AGENT-PLAN-MAP.md` ed è
esclusa da ogni payload **per costruzione**, perché i payload si compongono da una allowlist
esplicita di file. Il divieto scritto nei prompt serve solo all'esecuzione manuale.

Il prompt `improve` esclude inoltre dall'analisi ogni problema relativo al **walking skeleton**. È
una restrizione di scope reale del ciclo, non un dettaglio del prompt.

### Confini di strumento

Cicli separati da un confine **non sono confrontabili alla lettera**. La colonna `Misurato su` del
registro esiste per registrarli, e ne porta il ciclo, i piani, gli strumenti, **il modello e
l'effort**. I confini noti:

- **CON-4 → CON-5.** I prompt sono cambiati. Le righe `R-002`…`R-008`, oggi `intersezione-tema`, sono
  state prodotte con prompt diversi da quelli in `prompts/`.
- **CON-5 → CON-6.** Payload cieco e simmetrico su `improve` **e** `review`; contratto di conformità
  con template e validator; `improve` bidirezionale; registro tradotto in inglese e migrato alla
  semantica `non smentita ×k` con la narrativa di ciclo estratta.
- **CON-6 → CON-7, effort.** I due modelli passano da `high` a `medium`. `high` è l'unica
  configurazione mai esercitata contro provider reali, e resta ferma in CON-6: cambiarla nello stesso
  ciclo che deve testare la specificità degli `IMPROVEMENT` avrebbe confuso la variabile testata con
  una scelta di costo indipendente.
- **CON-6 → CON-7, brief.** La revisione di `EVALUATION-BRIEF.md` sta dopo CON-6 per la stessa
  ragione: è l'autorità contro cui si decidono sette righe su undici.
- **Dopo la fase di modularizzazione e pruning.** Spostare testo dello skill in file caricati
  on-demand cambia ciò che il modello ha in contesto al momento di generare. Non è un refactor neutro:
  è un cambio di strumento al pari degli altri.

Principio che governa la lista: **un confine si attraversa una volta sola, deliberatamente, e si
registra.** Non si sgocciola. È la ragione per cui traduzione, split e migrazione del registro stanno
tutti in una fase sola, e per cui effort e brief stanno tutti e due dopo CON-6.

## Il contratto di conformità

Il documento in precedenza affermava che l'output è markdown libero e che quindi il modo di
fallimento del grading system — risposta sintatticamente valida ma non conforme a un contratto
rigido, sei scarti su diciannove — qui non esiste. **L'affermazione è ritirata: la premessa e la
conclusione sono entrambe false.**

Un contratto c'era già, descritto in prosa in `PROMPTS.md` § *CREATE IMPROVEMENTS*: titolo,
`## Inputs`, una sezione per miglioramento con otto campi obbligatori e `## Verifica finale`.
Nell'unica esecuzione mai fatta:

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
sette righe di registro. Il modo di fallimento non è stato eliminato, è stato reso silenzioso.

**Un contratto descritto in prosa dentro un prompt è ciò che entrambi i lati hanno ignorato.** Il
rimedio non è ripetere la prosa: è la stessa architettura che lo skill usa già e che funziona —
`assets/plan-template.md` dà la forma, `scripts/validate_plan.py` la controlla, e le righe del registro
si dividono in `validator` e `lettura` lungo quella cucitura. `CC` rispetta il template dei piani da
cinque cicli.

Quindi: **`assets/improvement-template.md` + `scripts/consensus/validate_improvement.py`.**

### La specificità è una forma, non un giudizio

Un gate che conta i campi non si accorge del difetto di CON-4. Otto sezioni con otto campi ciascuna,
tutte scritte come *«rendere obbligatorio un audit interno split/merge per ogni coppia di
capability»*, lo passerebbero. La genericità sta nel contenuto dei campi.

Il template la esclude **per forma**:

1. **`Evidenza — candidato A`** e **`Evidenza — candidato B`** sono due celle separate. O contengono
   un riferimento localizzabile — `PLAN-…-CON-N.md:NN`, oppure `slice N` più il nome del campo — o la
   dichiarazione esplicita che quel candidato non manifesta il difetto. Un bullet generico non riempie
   due celle di evidenza.
2. **`Regola esistente che non ha impedito il difetto`** nomina una clausola di `SKILL.md` con la sua
   sezione, oppure dichiara `nessuna`.
3. **`Test binario`** è scritto nella grammatica delle righe del registro — `Nessuna slice NOW…`,
   `Ogni voce LATER…` — cioè decidibile su un piano generato.

Il punto 3 elimina una cucitura mai dichiarata: oggi qualcuno traduce prosa in affermazione
falsificabile, a mano, al momento di applicare. Con il template la riga la scrive il modello che ha
trovato il difetto, e l'umano accetta o rifiuta.

**Non servono soglie.** Misurare la specificità con una quota e una soglia era ragionamento
confermazionista dentro un documento costruito su `non smentita ×k`. Senza soglia il criterio è
descrittivo: quante voci sopravvivono al gate per lato. `CX` a 0 e `CC` a 9 falsifica l'ipotesi senza
che nessuno si sia impegnato su un numero arbitrario; 7 e 9 non conferma niente — è un ciclo `×1`.

### Cosa fa il gate quando una voce non è conforme

**Scarto per voce, un solo tentativo.** La voce cade, il resto del documento resta. Ogni scarto è
registrato nel report con il campo mancante e il motivo.

Perché un tentativo e non due: una voce scartata non è persa. `improve` rigenera una lista fresca ogni
ciclo, quindi il difetto ricompare al giro dopo a costo marginale zero, mentre la rigenerazione paga
subito, può non convergere, e mette nel record un artefatto ottenuto con più tentativi degli altri.
Vale la regola generale — *«un filtro che manca qualcosa costa meno di uno che applica qualcosa di
falso»*.

Due precisazioni che tengono pulito il dato:

- **Un errore di trasporto o una risposta vuota non è un tentativo di conformità.** Si ritenta la
  *chiamata*. Si rigenera il *documento* mai. Sono due contatori diversi e solo il secondo dice
  qualcosa sull'ipotesi.
- **Un lato che produce zero voci conformi non blocca il ciclo.** `review` gira lo stesso, con l'esito
  ovvio: nessuna intersezione possibile, quindi nessuna applicazione automatica. «`CX` ha prodotto 0
  voci conformi in CON-6» è un dato del ciclo, non un guasto da riparare; se era transitorio, CON-7 lo
  mostra.

Il log degli scarti è anche la diagnosi quando un lato collassa: scarti concentrati **tutti sullo
stesso campo** accusano il template, e si corregge quel campo. Scarti **sparsi** accusano il modello,
e l'ipotesi prende una smentita `×1`.

Lo scarto registrato è il rimedio al degrado silenzioso, che è il difetto storico: un warning su un
artefatto che nessuno ha guardato per due cicli è esattamente ciò che è già successo.

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

Quattro rimedi, tutti a costo zero di chiamate:

- **`improve` bidirezionale con regola dura**, sopra, resa applicabile dalla mappa clausola → riga.
- **Righe di registro sottrattive.** Una riga può nascere `Origine: potatura`, con l'affermazione
  «la rimozione di X non fa ricomparire il difetto Y». Prima il registro poteva registrare solo
  crescita, quindi anche la sua storia era cieca al fenomeno.
- **Contatori in testa al report.** Il passaggio da *«leggo i report e scrivo io la modifica»* a
  *«leggo il diff e pongo il veto»* è più sostenibile, ma inverte il default: autorare-prima ha per
  default l'inazione, vetare-dopo ha per default l'accettazione. E la patologia misurata è l'accumulo.
  Un veto è debole contro un diff di otto righe di regola plausibile — diciotto volte in una settimana
  e sei di nuovo a +69%. I contatori in testa lo rendono forte perché mordono sull'accumulo invece che
  sul merito: `0 riformulazioni su 5 aggiunte` è già il verdetto, e non richiede di leggere le regole.
- **Recidiva**, passo 7. Se è sistematicamente maggiore di zero, il registro sta dichiarando chiuso ciò
  che non lo è. Se è zero mentre lo `SKILL.md` continua a crescere, il ciclo trova cose genuinamente
  nuove — legittimo, ma prima o poi va chiesto se quella crescita sia sostenibile.

## Il registro

La chiusura proporzionata al buco è `REGRESSION-LEDGER.md`. Ogni modifica allo `SKILL.md` implica una
previsione falsificabile — *«al prossimo ciclo questo difetto non ricompare»* — e il registro la rende
obbligatoria: una riga per modifica applicata, con id, commit dello skill, origine, affermazione
verificabile, modo di verifica, ultimo controllo, artefatti e strumenti su cui è stato prodotto il
verdetto, cosa sorvegliare oltre all'affermazione, ed esito.

Lo stesso registro copre anche le regressioni **non previste**, senza un secondo artefatto: se il
piano di miglioramento del ciclo N solleva un difetto che il ciclo N-2 aveva chiuso, quella è una
regressione. È la fase `recidiva` a produrre quell'accoppiamento; prima era dichiarata nel registro e
non la faceva nessuno.

**La falsificabilità sta nella formulazione della riga, non nell'automazione.** Automatizzare il
`verdetto` non rende falsificabile ciò che non lo era: serve a garantire che il controllo **avvenga**
ogni ciclo e che ogni verdetto citi il punto del piano che lo regge. Delle undici righe attuali solo
R-011, e metà di R-008, sono decidibili dal validator strutturale — il controllo esiste già in
`skills/plan-slices/scripts/validate_plan.py`. Le altre richiedono il confronto con il brief, cioè un
giudizio.

### Dormienza

Il costo del `verdetto` cresceva in modo monotono, e il trigger dichiarato per affrontarlo era la
recidiva — che misura un'altra grandezza: se il registro mente, non quanto costa leggerlo. Ennesima
porta con nessuno alla maniglia.

Il modo di fallimento non è il costo in token: è la **diluizione**. Un modello a cui dai quaranta
righe restituisce quaranta verdetti comunque, con meno attenzione per riga, e degrada in silenzio.

- **La diluizione diventa osservabile** con la stessa regola dello scarto: un verdetto la cui citazione
  non si risolve — file, sezione o numero di slice inesistente — viene scartato e registrato. Il tasso
  di scarto è il termometro.
- **Dormienza invece di pensionamento.** Una riga a `non smentita ×3` passa dormiente e si verifica 1
  ciclo su 3. Non si cancella niente.
- **La `recidiva` rende sicura la dormienza.** Una riga dormiente risollevata da `improve` torna attiva
  immediatamente. Senza recidiva la dormienza sarebbe cieca.

### Perché `recidiva` è una sola chiamata

Il filtro di consenso esiste dove un disaccordo cambia cosa entra nello skill. La recidiva non fa
entrare niente: è un termometro, e un termometro non ha bisogno di consenso — ha bisogno di essere **lo
stesso strumento ogni volta**. Due valori discordi da riconciliare a mano aggiungono una terza
decisione umana per ciclo sul contatore meno importante dei tre. E applicare la regola *«regge solo se
regge su entrambi»* alla recidiva massimizzerebbe i falsi positivi proprio dove servono meno.

Modello fisso: `claude-opus-5`, dichiarato in `Misurato su`. Cambiarlo è un confine di strumento.

**Controargomento registrato.** Se la recidiva diventa il segnale che sblocca una decisione, vuole il
filtro e le due chiamate. L'inversione si valuta a uno di questi due eventi:

1. Un valore di recidiva viene citato come ragione di una modifica applicata allo `SKILL.md`, o di un
   cambio di stato di una riga che **riduce** la verifica — pensionamento, chiusura, messa in
   dormienza. Non vale per il **risveglio**, che la aumenta: l'asimmetria è benigna, un falso positivo
   costa una riga verificata in più.
2. Il matching risulta instabile fra cicli: stessa voce, stessa riga, verdetto diverso senza che gli
   artefatti siano cambiati.

L'evento 2 è osservabile solo perché l'output di `recidiva` è l'**elenco delle coppie**, non uno
scalare. Un numero nudo nasconde esattamente l'instabilità che autorizzerebbe l'inversione.

### Cosa il registro non contiene

La narrativa di ciclo — regressioni rilevate, formulazioni riscritte, diagnosi decise — vive nel report
del suo ciclo, non nel registro. Erano 239 righe su 386, il 62%, rilette dal `verdetto` a ogni ciclo
senza servire a niente.

Unica eccezione, obbligatoria: le note *«Da cercare al prossimo ciclo, oltre alla riga»* non sono
narrativa, sono **istruzioni per il verdetto successivo** — *«il fallimento da sorvegliare non è il
ritorno dell'assertivo ma il suo opposto»*, *«il marcatore apposto per far passare il controllo, non la
sua assenza»*. Stanno **nella riga**, cella `Da sorvegliare`. Sono l'unico posto dove il registro dice
cosa cercare oltre all'affermazione.

## Quando il `verdetto` falsifica una riga

La mossa giusta è l'indagine qualitativa: chiedere quale regola dello `SKILL.md` ha lasciato passare il
difetto. Vincolo obbligatorio: l'agente produrrà sempre una spiegazione plausibile, anche in assenza di
nesso. Vale solo se nomina una clausola specifica e genera una previsione falsificabile — *«togli o
riformula questa clausola e il difetto non ricompare»* — verificata rigenerando. Senza il passo di
falsificazione è un racconto ben scritto.

È la disciplina con cui sono state prodotte le diagnosi di `R-010` e `R-011`, e per cui su tre righe
regredite di CON-5 due hanno prodotto una correzione e una no: la riga C è stata diagnosticata come
`Theme compression`, sede il test di split del § 2, e **nessuna regola è stata aggiunta**.

L'innesco è il verdetto, non un punteggio. La formulazione precedente partiva da *«se il confronto dice
`better` su tre criteri e `worse` su uno»*, vocabolario del grading: nel ciclo di consenso non esiste
nessun confronto che emetta `better`/`worse`.

## Cosa il ciclo eredita dal grading system

Costruito, pagato e riusato subito: il validator strutturale `validate_plan.py`;
`recipe-app/EVALUATION-BRIEF.md`, che sostituisce il confronto con un piano ideale — confrontare con
un piano ideale misura la somiglianza a quel piano, non la qualità; l'anonimizzazione dei candidati;
la tassonomia dei sette assi di lettura, che coincide con quella della rubric v3; l'hashing di
prompt, fonti e brief con artefatti immutabili, che tiene i cicli confrontabili; la disciplina di
`NOTES.md`. Non serve la scala a cinque verdetti, non serve lo score.

Va aggiunta l'architettura template + validator, ereditata dallo skill invece che dal grading: è la
sola parte del sistema che ha retto cinque cicli senza degradare.

## Stato dell'automazione

- **Fase 0a — inglese.** La decisione e la regola che ogni artefatto nuovo nasce in inglese. Zero
  chiamate.
- **Fase 0 — separazione.** Documenti e artefatti dei due strumenti distinti; grading marcato come
  abbandonato. Zero chiamate.
- **Fase 0b — conversione dei documenti umani.** Nessuna dipendenza; può slittare indefinitamente.
- **Fase 1a — contratto.** Template e validator degli `IMPROVEMENT`. Zero chiamate.
- **Fase 1b — prompt.** I quattro prompt sotto `prompts/`, che citano il template invece di duplicarlo.
- **Fase 1c — registro e mappa.** Traduzione, split della narrativa, migrazione semantica,
  riclassificazione, mappa clausola → riga, struttura del report.
- **Fase 2 — CON-6 manuale.** Nove esecuzioni, effort `high`.
- **Fase 2b — revisione del brief.** Dopo CON-6. Zero chiamate.
- **Fase 3 — riorganizzazione del codice.** Zero chiamate.
- **Fase 4 — modularizzazione e pruning dello skill.** Zero chiamate; si verifica su CON-7.
- **Fase 5 — orchestratore.** `make consensus N=… PHASE=improve|review|verdict|recidiva|report`, con
  dry-run, `CONFIRM_SEND`, resume e hash.
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

- **La copertura è minoranza.** Undici righe di registro contro 417 righe di `SKILL.md`. Il
  peggioramento è rilevabile **solo sulla superficie coperta**; su tutto il resto è invisibile, e non
  esiste un secondo strumento che la guardi. La mappa clausola → riga della Fase 1c è ciò che rende
  questa frase un numero invece di un'impressione.
- **Un solo scenario.** Tutto gira su `recipe-app`. Limite accettato, non risolto — ma la ragione
  scritta prima era sbagliata: un secondo scenario **non «raddoppia il costo di ogni ciclo»**. Richiede
  un secondo `EVALUATION-BRIEF.md`, che è lavoro umano sostanziale e non replicabile, più la
  riderivazione delle righe che ne dipendono. Sette righe su undici citano il brief — `Known
  conflicts`, `Accepted alternatives`, `Authority`, `Hard constraints`, `Material uncertainties` — e
  non sono decidibili senza. La ragione vecchia faceva sembrare la decisione più facile da invertire di
  quanto sia.
- **Il salto dal difetto alla regola non è controllato.** Ogni difetto osservato è scenario-bound; ogni
  regola scritta nello `SKILL.md` non lo è. La generalizzazione avviene dentro `improve`, senza
  artefatto e senza rilettura. È lì che nasce l'overfitting, non nel fatto che lo scenario sia uno.
- **Varianza di generazione.** `n = 1` per lato, nessuna ripetizione prevista in nessuna fase. Un
  before/after singolo confonde l'effetto della modifica con la variabilità di una generazione, e il
  disaccordo fra i due lati su `R-002` e `R-008` mostra che la varianza è già visibile a questa scala.
  È il limite da cui discende la semantica `non smentita ×k`.
- **`non smentita` non è conferma.** Cinque righe su undici hanno questo stato a `×1`, e sono proprio
  quelle che autorizzerebbero a smettere di guardare una regola.
- **La falsificazione è solida, la diagnosi no.** Un controesempio su un piano falsifica la riga senza
  ambiguità. Ma dedurne *quale* clausola correggere è dove la varianza rientra: `R-010` nasce da una
  violazione su un solo modello, e la sua stessa nota lo dichiara — *«è il modo tipico in cui
  `giudizio` applica una regola falsa»*.
- **Cecità nominale.** Vedi *Cecità e simmetria*. Il contratto di conformità la indebolisce.
- **«Peggiorato» non è definito quando i segnali sono discordi.** La decisione resta umana e guarda
  quali criteri, non quanti.
