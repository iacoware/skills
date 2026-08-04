# Note dagli eval

Osservazioni emerse eseguendo gli eval delle skill, con le modifiche che ne sono derivate e cosa
resta da verificare. Ogni nota è autoconsistente: non serve il contesto della sessione in cui è nata.

## Evaluator — Ritentare finché la risposta è valida contamina una baseline di calibrazione

**Contesto.** Raccolta di calibrazione dell'evaluator `plan-slices` v3: sei fixture di confine, tre
ripetizioni indipendenti per due grader, 36 chiamate provider, sei shard paralleli disgiunti. Lo
scopo era misurare quanto i grader sono accurati rispetto a label umane e quanto sono ripetibili,
per decidere se la scala dei verdict a cinque livelli regge. Il grade contract valida ogni risposta
e scarta quelle non conformi.

**Osservazione.** Sei risposte su diciannove sono state rifiutate non per errori di trasporto ma per
violazione del contratto: uso di `absent` come gravità generica, criterio non-pass senza difetti,
difetto citato da un criterio diverso dal proprio `primary_criterion`. Le regole erano già enunciate
nel prompt. Il riflesso naturale è ritentare l'unità fallita finché produce un artefatto valido.

**Il riflesso è sbagliato, e non per il costo.** Ritentare finché la risposta è conforme è un filtro
di qualità silenzioso: le unità su cui un grader tende a sbagliare vengono ricampionate finché
obbedisce, quelle facili passano al primo colpo. La baseline che ne risulta misura i grader *quando
si comportano bene*. Per un eval funzionale sarebbe accettabile; per una **baseline di calibrazione**
è autodistruttivo, perché le grandezze che deve stimare — accuratezza, ripetibilità, correttezza
dell'attribuzione — sono esattamente quelle che il filtro distorce. Nel campione parziale
l'accuratezza del criterio primario risultava 0.119, ed era già misurata sul solo sottoinsieme
conforme: il numero vero è peggiore, non migliore.

**Conseguenza di metodo: la conformità al contratto è una metrica, non uno scarto operativo.** Va
contata e riportata per provider e per modo di fallimento, accanto ad accuratezza e agreement. Se il
tasso resta basso anche dopo aver chiarito il prompt, il risultato non è "i grader sbagliano", è "il
contratto chiede più di quanto i grader sappiano produrre" — che è un'informazione diretta sul
contratto, e nel caso specifico un argomento concreto per semplificare la scala dei verdict.

**Due difetti operativi che questo ha rivelato.**

- **L'output rifiutato veniva distrutto.** Il leaf command validava prima di scrivere, quindi il
  grade non conforme non raggiungeva mai il file e lo staging veniva ripulito. Di sei risposte pagate
  restavano sei righe di errore. Una risposta rifiutata è evidenza già acquistata: va messa in
  quarantena fuori dal set di resume, non cancellata.
- **Il fail-fast amplificava una violazione locale in perdita di copertura.** Un solo grade rifiutato
  interrompeva l'intero shard: sei scarti hanno bloccato quindici unità mai tentate, e uno shard ne
  ha perse cinque su sei per un rifiuto alla prima unità. Il fail-fast serve per la causa condivisa
  — schema rifiutato, autenticazione rotta, configurazione errata — dove proseguire brucerebbe tutto.
  Non serve per una non-conformità della singola risposta, che non dice nulla sull'unità successiva.
  La forma giusta è un circuit breaker: prosegui, aborta dopo N fallimenti consecutivi.

**Generalizzazione.** Quando un contratto rigido filtra l'output di un modello non deterministico,
decidere *prima* se il filtro è parte della misura o parte della raccolta. Se è parte della misura,
ritentare falsifica il risultato e il tasso di scarto va pubblicato. Se è parte della raccolta,
ritentare è legittimo ma va dichiarato, perché chi legge la baseline deve sapere quante risposte sono
state guardate per ottenerne una.

**Da verificare.** Se una riformulazione meccanica delle regole nel prompt — espresse sui campi che
il modello compila, non sui concetti — alza sensibilmente il tasso di conformità, il problema era la
formulazione. Se non lo alza, era la richiesta, e il contratto va semplificato prima di spendere una
matrice completa.

## plan-slices — Confine di scope vs identità nell'ordinamento delle slice

**Contesto.** Eval `evals/plan-slices/recipe-app`: pianificazione di una recipe app greenfield
(Next.js, Postgres+pgvector, Auth.js + Google OAuth, condivisione cookbook-centrica). Il
differenziatore dichiarato è la ricerca semantica cross-lingua; senza di essa il prodotto è una
riscrittura di Mealie. Piano prodotto: `results/PLAN-CC-CON-2.md`.

**Osservazione.** Il piano colloca l'autenticazione alla slice 5, dopo il walking skeleton (1),
l'enabler di indicizzazione su fixture (2), la ricerca semantica (3) e l'elenco/lettura ricetta (4).
Sospetto iniziale: una funzionalità così di base rinviata rischia un rilavoro intenso, e
anticiparla subito dopo il walking skeleton sarebbe costato poco.

**Conclusione: l'ordine è giustificato, ma solo a una condizione.** La distinzione che conta non è
"auth presto vs tardi", è **confine di scope vs identità**:

- Il **confine** (`Cookbook`, `Recipe.cookbookId`, ogni query filtrata, 404 fuori scope) esiste già
  dalla slice 2, cioè dalla prima slice che persiste dati.
- L'**identità** (chi sei, e da dove viene il `cookbookId` corrente) è l'unica cosa rinviata.

Il rilavoro intenso che ci si aspetta dall'auth tardiva nasce dal rinvio del **confine**: query
scritte senza filtro, tabelle senza colonna di tenancy, UI senza il concetto di spazio corrente. Il
retrofit tocca allora ogni query e rischia di dimenticarne una, cioè un buco di sicurezza. Se invece
il confine c'è già, cambia solo **da dove si legge lo scope corrente**, non chi filtra.

**Condizione da rendere esplicita.** Il rilavoro resta limitato solo se le slice pre-auth risolvono
lo scope corrente in **un unico punto** (es. `currentCookbookId()`: prima legge la configurazione,
dalla slice di auth legge la sessione). Se l'id viene ricavato in più handler, il rilavoro diventa
reale. Il piano generato non dichiarava questa giunzione: è il difetto vero, non l'ordine.

**Asimmetria dei costi** che regge la scelta:

| | Auth anticipata | Auth dopo il differenziatore |
|---|---|---|
| Ritardo sul verdetto del differenziatore | ~1 slice | nessuno |
| Rilavoro se il differenziatore regge | nessuno | risolutore di scope + protezione rotte |
| Costo se il differenziatore non regge | auth costruita per un prodotto che cambia | nulla di sprecato |
| Attrito nelle verifiche intermedie | login a ogni sessione di test | verifiche da script/browser diretti |

Il punto decisivo: **l'auth non ha rischio tecnico** (Auth.js + Google su Next.js è percorso
battuto, esito noto), la ricerca semantica cross-lingua sì. Anticipare lavoro certo davanti a lavoro
incerto è esattamente ciò che l'ordinamento risk-first evita. Vale anche che la migrazione che
introduce `User`/`Membership`/`creatorId` arriva quando il DB ha solo fixture e la produzione non
esiste ancora: il momento più economico possibile.

**Variante considerata e non applicata.** Spostare la slice di auth prima di elenco/lettura
(`0,1,2,3,5,4,…`): dopo la 3 il verdetto sul differenziatore c'è già, quindi non ritarda nulla di
importante, e l'unica slice mai costruita senza sessione resta la ricerca. Hedge a costo quasi nullo
se si vuole ridurre la superficie pre-identità. Non applicata al piano perché il piano è un artefatto
di test, non un deliverable.

**Modifiche alla skill.**

- Passo 4, nuova regola di ordinamento: *"Separate a boundary from the identity behind it. Ship the
  tenancy, ownership, or scope boundary with the first slice that persists data, and let a single
  named resolver own the current scope; then a later slice can replace a configured scope with an
  authenticated one at one seam. State that seam under `Cross-functional concerns`. Never defer the
  boundary itself, and never defer identity when no such seam exists."*
- `ANTI-PATTERNS` → `Deferred safety`, clausola di disambiguazione: sostituire uno scope configurato
  con uno autenticato a una giunzione dichiarata non è deferred safety; pubblicare slice con letture
  non scoped sì. Senza questa clausola l'anti-pattern spingeva verso l'auth anticipata anche quando
  non serve.

**Da verificare al prossimo eval.** Se la skill riproduce l'auth dopo il differenziatore **e**
dichiara la giunzione in `Cross-functional concerns`, la regola funziona. Se riproduce l'ordine ma
omette la giunzione, la prosa non basta e serve un controllo strutturale nel validatore (es. sezione
o campo obbligatorio quando una slice di identità segue la prima slice che persiste dati).
