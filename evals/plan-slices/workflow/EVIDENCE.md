# Lo stato dell'evidenza e i limiti

Cosa lo strumento ha davvero misurato finora, e cosa resta fuori dalla sua portata. **Va letto prima
di fidarsi di qualunque affermazione degli altri documenti sulla bontà del filtro.**

È l'unico file di questa directory che ogni ciclo aggiorna: i numeri qui datati sono misure, non
regole.

## Lo stato dell'evidenza

- Le fasi `improve` e `review` sono state eseguite **una volta sola**, nel ciclo CON-4, con prompt poi
  cambiati.
- In quell'unica esecuzione i due `IMPROVEMENT` sono arrivati a **246 righe** (`CC`) contro **10**
  (`CX`), ed entrambi violavano la struttura obbligatoria del prompt — vedi `CONFORMANCE.md`.
  L'intersezione è stata quindi calcolata mappando bullet generici su sezioni operative,
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
  `review`. Ha comunque prodotto due regressioni e due commit dello skill — ma per la ragione qui
  sotto **non è la dimostrazione che il rilevatore gira da solo**. È la dimostrazione che un umano che
  legge due piani generati contro affermazioni appena scritte trova difetti reali: la stessa attività
  a cui `RATIONALE.md` § *Perché il grading system è abbandonato* attribuisce `2c89e7f`.
- Le fasi `verdetto` e `recidiva` a modelli non sono **mai** state eseguite.
- **Il registro è stato popolato a posteriori.** Gli `IMPROVEMENT` e i `REVIEW` di CON-4 sono
  artefatti realmente generati da un workflow; le righe del registro no. `REGRESSION-LEDGER.md` nasce
  il 2026-08-04 alle 21:20 e alle 21:28 il commit `0273a73` — *«backdate the ledger to the CON-4
  review cycle»* — vi scrive `R-002`…`R-008` risalendo a commit già fatti. Nessuna di quelle righe è
  la previsione di chi ha applicato la modifica: sono ricostruzioni, e lo stesso messaggio dichiara il
  criterio con cui sono state scritte — *«each stated over a generated plan rather than over the skill
  text»*.
- **Due righe sole sono previsioni ex-ante:** `R-010` (`865fc56`, 23:12) e `R-011` (`633ddf1`, 23:32),
  scritte nello stesso minuto del commit che verificano — `87150d3` alle 23:11, `eb926bb` alle 23:30.
  Sono anche le due sole la cui clausola è ancora nella forma su cui la riga è nata, e non è una
  coincidenza: è il meccanismo. Entrambe sono tuttora `da verificare`.
- **Quattro righe sono state ritarate sui piani su cui erano misurate.** I verdetti CON-5 entrano alle
  22:02; fra le 22:20 e le 22:41 vengono riscritte `R-002` secondo membro, `R-003`, `R-006` e `R-007`,
  e con loro l'autorità: il conflitto sull'embedding di query entra nel brief alle 22:20 (`b7af297`),
  la tabella `Material uncertainties` alle 22:20 e le sue id alle 22:41 (`249a34e`), lo stesso minuto
  in cui `R-007` è decisa sul criterio di sottosistema. Per quelle quattro righe **CON-5 non è un
  test**: la riga è stata adattata al piano che avrebbe dovuto falsificarla. Lo racconta già
  `recipe-app/results/CONSENSUS-CON-5.REPORT.md` § *Formulazioni riscritte*, senza trarne la
  conseguenza sul contatore.
- **La falsificazione più pulita del corpus è `R-008` su `CX`**: riga scritta alle 21:28, mai
  riscritta, smentita alle 22:02 da tre voci della tabella `Themes`. `R-002` su `CC` regge quasi
  altrettanto, ma il suo primo membro è ancorato ai `Known conflicts` del brief, che quella sera hanno
  ricevuto un conflitto in più.
- Il ciclo nella forma dei passi 1-3, 5 e 8 è esso stesso il risultato di un'evoluzione: i commit dello
  skill precedenti al ciclo CON-4 nascono da conversazioni fra umano e agente sui piani generati, senza
  confronto fra modelli. La maggior parte della storia dello skill non ha né previsioni scritte né una
  traccia recuperabile da git.

Quindi lo strumento non è «già esistente e da formalizzare»: **CON-6 è la sua prima esecuzione nella
forma documentata**, e vale per il registro quanto per il filtro. Il corpus del registro è in parte
validato — due falsificazioni reali su piani reali; la sua **disciplina** — la riga scritta dall'umano
che applica, nel momento in cui applica — è stata eseguita due volte su diciassette. Il criterio con
cui giudicare CON-6 non è che produca tutti gli artefatti previsti, ma
che i due `IMPROVEMENT` abbiano **specificità comparabile**, cioè che l'intersezione sia letterale e
non una mappatura generico → operativo. Il contratto di conformità rende quella proprietà una forma
da riempire invece che un giudizio da emettere.

## Limiti che restano

- **La copertura è minoranza, e ora è un numero.** `support/CLAUSE-ROW-MAP.md` conta **205 clausole
  normative** in `SKILL.md` a `28b5460`: **40 coperte da almeno una riga (20%)**, di cui **20 sono
  restatement** in gate, anti-pattern o ledger non pubblicato — quindi le clausole di corpo coperte
  sono **20 su 205**. **165 scoperte (80%).** Il peggioramento è rilevabile **solo sulla superficie
  coperta**; su tutto il resto è invisibile, e non esiste un secondo strumento che la guardi.
- **Un solo scenario.** Tutto gira su `recipe-app`. Limite accettato, non risolto — ma la ragione
  scritta prima era sbagliata: un secondo scenario **non «raddoppia il costo di ogni ciclo»**. Richiede
  un secondo `EVALUATION-BRIEF.md`, che è lavoro umano sostanziale e non replicabile, più la
  riderivazione delle righe che ne dipendono. Quattordici righe su diciassette portano il brief in
  `Misurato su` — `Known conflicts`, `Accepted alternatives`, `Authority`, `Hard constraints`,
  `Material uncertainties` — e non sono decidibili senza. La ragione vecchia faceva sembrare la
  decisione più facile da invertire di quanto sia.
- **Il salto dal difetto alla regola non è controllato.** Ogni difetto osservato è scenario-bound; ogni
  regola scritta nello `SKILL.md` non lo è. La generalizzazione avviene dentro `improve`, senza
  artefatto e senza rilettura. È lì che nasce l'overfitting, non nel fatto che lo scenario sia uno.
- **Varianza di generazione.** `n = 1` per lato, nessuna ripetizione prevista in nessuna fase. Un
  before/after singolo confonde l'effetto della modifica con la variabilità di una generazione, e il
  disaccordo fra i due lati su `R-002` e `R-008` mostra che la varianza è già visibile a questa scala.
  È il limite da cui discende la semantica `non smentita ×k`.
- **`non smentita` non è conferma.** Otto righe su diciassette hanno questo stato a `×1`, e sono
  proprio quelle che autorizzerebbero a smettere di guardare una regola.
- **La falsificazione è solida, la diagnosi no.** Un controesempio su un piano falsifica la riga senza
  ambiguità. Ma dedurne *quale* clausola correggere è dove la varianza rientra: `R-010` nasce da una
  violazione su un solo modello, e la sua stessa nota lo dichiara — *«è il modo tipico in cui
  `giudizio` applica una regola falsa»*.
- **Cecità nominale.** Vedi `CYCLE.md` § *Cecità e simmetria*. Il contratto di conformità la
  indebolisce.
- **«Peggiorato» non è definito quando i segnali sono discordi.** La decisione resta umana e guarda
  quali criteri, non quanti.
