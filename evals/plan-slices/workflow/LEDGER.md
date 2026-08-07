# Il registro

Il meccanismo di `REGRESSION-LEDGER.md`: cosa registra, perché la dormienza, perché `recidiva` è una
chiamata sola, cosa fare quando un verdetto falsifica una riga. Le **regole d'uso** — formato delle
celle, ri-ancoraggio, assorbimento, split — stanno nel registro stesso, § *How to use*, e qui non si
duplicano.

Lo legge chi esegue i passi 6 e 7 del ciclo (Fase 2) e chi li automatizza (Fase 5).

## Cosa il registro registra

La chiusura proporzionata al buco è `REGRESSION-LEDGER.md`. Ogni modifica allo `SKILL.md` implica una
previsione falsificabile — *«al prossimo ciclo questo difetto non ricompare»* — e il registro la rende
obbligatoria: una riga per modifica applicata, con id, commit dello skill, origine, affermazione
verificabile, modo di verifica, ultimo controllo, artefatti e strumenti su cui è stato prodotto il
verdetto, cosa sorvegliare oltre all'affermazione, ed esito.

**L'obbligo è dichiarato, non ancora esercitato.** Quindici righe su diciassette sono ricostruzioni
scritte a ritroso su commit già fatti; vedi `EVIDENCE.md`. La conseguenza operativa è che le
affermazioni **quantificano su un piano generato, non sul testo dello skill** — è il criterio con cui
sono state scritte, e ha due effetti opposti. Buono: riformulare una clausola **non falsifica** la
riga che la copre, perché la riga non afferma niente sul testo della clausola. Cattivo: l'unico
ancoraggio al testo sotto processo è la cella `Commit`, quindi una riformulazione lascia la riga a
misurare un testo diverso da quello che dichiara, in silenzio. È esattamente ciò che è successo a
`R-002` e a `R-008`, e la ragione per cui una clausola riformulata **ri-ancora** le righe che la
coprono e ne azzera il contatore `×k`.

Quando invece cambia la **portata** della regola — estesa, ristretta o corretta — la riga non si
ri-ancora: **una riga sola afferma tutto** e l'affermazione che sostituisce esce dal file. È
l'**assorbimento**, scritto da `improve` ed editato nel veto, con le regressioni assorbite conservate
in una cella invece che in una riga. Regole e vincoli stanno in `REGRESSION-LEDGER.md` §
*Re-anchoring and absorption*; applicato per la prima volta a mano il 2026-08-06 su `R-002` m1 →
`R-010` e sulla clausola `Enabler` di `R-008` → `R-011`, che erano ancorate alla stessa clausola e
contavano due volte la stessa evidenza.

**Una riga = una affermazione**, ed è la regola di scrittura di ogni riga dal 2026-08-06, non solo un
vincolo dell'assorbimento. Una riga che ne porta due non può portare un contatore: smentita su un
membro, `×k` resterebbe scritto per gli altri, e disaggregare dopo un ciclo vuol dire ricostruire
previsioni a posteriori. Le quattro righe scritte prima della regola — `R-001`, `R-004`, `R-006`,
`R-009` — sono state splittate lo stesso giorno, una riga per affermazione, con il primo membro che
conserva l'id e gli altri che ne prendono di nuovi in coda; ogni figlio eredita il contatore del
padre. **Da undici a diciassette righe senza una previsione in più:** la superficie coperta non si
muove di una clausola, e un report non deve leggere `righe attive 11 → 17` come sei regole nuove
entrate nello skill. Lo split è la mossa inversa dell'assorbimento e sta nella stessa colonna,
`Absorbs`.

Lo stesso registro copre anche le regressioni **non previste**, senza un secondo artefatto: se il
piano di miglioramento del ciclo N solleva un difetto che il ciclo N-2 aveva chiuso, quella è una
regressione. È la fase `recidiva` a produrre quell'accoppiamento; prima era dichiarata nel registro e
non la faceva nessuno.

**La falsificabilità sta nella formulazione della riga, non nell'automazione.** Automatizzare il
`verdetto` non rende falsificabile ciò che non lo era: serve a garantire che il controllo **avvenga**
ogni ciclo e che ogni verdetto citi il punto del piano che lo regge. Delle diciassette righe attuali
solo R-011, e metà di R-008, sono decidibili dal validator strutturale con un controllo che esiste già in
`skills/plan-slices/scripts/validate_plan.py`. R-013 e R-014 sono automatizzabili sulla struttura del
template ma il controllo non è scritto: il validator verifica solo che le sezioni `LATER` e
`OUT-OF-SCOPE` portino una lista. Le altre richiedono il confronto con il brief, cioè un giudizio.

## Dormienza

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

## Due strumenti di `verdetto`, e cosa fare quando discordano

Il passo 6 ha **due esecuzioni**, una per lato, e ciascuna giudica **entrambi** i piani: ogni riga
porta quindi **quattro** verdetti, non due. L'aritmetica che il registro dichiara — *«un'affermazione
regge solo se regge su entrambi»* — parla dei due **piani** e non ha mai detto niente sui due
**strumenti**. Il buco è emerso a CON-6, il primo ciclo i cui verdetti nascono da una chiamata: su
quattro righe su diciassette i due strumenti si sono contraddetti sullo stesso testo pubblicato.

La regola è quella che il progetto ha già, `../CONSENSUS-WORKFLOW.md` § *Vocabolario*: *«due modelli
discordi mandano il punto alla lettura umana, non a un arbitro»*. Applicata al verdetto:

- **strumenti concordi sui due piani** → il verdetto vale, e si applica l'aritmetica sui piani;
- **strumenti discordi su uno dei due piani** → la riga **non cambia stato**, il contatore **non si
  muove**, e la riga va nell'elenco umano con entrambe le citazioni.

Un ciclo i cui due strumenti si contraddicono su una riga **non l'ha testata**, e il report lo
pubblica come contatore: `rows the cycle could not decide`. Non è un `row-defect`: quello dice che
l'affermazione è scritta male, questo dice che due lettori decidibilmente in disaccordo hanno letto
lo stesso testo in due modi. Confonderli sposterebbe sulla riga la colpa dello strumento.

Stesso trattamento, per la stessa ragione, quando è la `recidiva` a contraddire i due verdetti: la
riga non avanza il contatore e va al veto. Non si decide a maggioranza — vedi la sezione seguente.

## Perché `recidiva` è una sola chiamata

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

## Cosa il registro non contiene

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
