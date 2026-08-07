# Lo stato dell'evidenza e i limiti

Cosa lo strumento ha davvero misurato finora, e cosa resta fuori dalla sua portata. **Va letto prima
di fidarsi di qualunque affermazione degli altri documenti sulla bontà del filtro.**

È l'unico file di questa directory che ogni ciclo aggiorna: i numeri qui datati sono misure, non
regole. **Con una sola eccezione, ed è deliberata:** la *soglia di abbandono* in fondo è normativa e
sta qui perché è l'unico posto che porta i numeri contro cui si decide. Una soglia scritta altrove
sarebbe una regola senza il suo strumento di misura, che è esattamente come è morto il gate di
ripresa del grading.

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
- Le fasi `verdetto` e `recidiva` a modelli sono state eseguite **una volta sola**, in CON-6, il
  2026-08-07. Prima di quella data non erano mai girate.
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

Quindi lo strumento non era «già esistente e da formalizzare»: **CON-6 è stata la sua prima
esecuzione nella forma documentata**, e vale per il registro quanto per il filtro. Il corpus del
registro è in parte validato — due falsificazioni reali su piani reali; la sua **disciplina** — la
riga scritta dall'umano che applica, nel momento in cui applica — era stata eseguita due volte su
diciassette, ed è tre volte su diciotto da CON-6.

## CON-6, misurato (2026-08-07)

Il primo ciclo completo. Il report è `../recipe-app/results/CONSENSUS-CON-6.REPORT.md`; qui stanno
solo i numeri che dicono quanto lo strumento vale, non cosa ha prodotto.

- **Il criterio dichiarato per giudicare CON-6 — specificità comparabile fra i due `IMPROVEMENT` —
  non è stato misurato.** Il gate è stato corretto **due volte dentro S2**, la seconda **a risultato
  noto**, cioè sapendo quale lato cadeva. Il conteggio `4` contro `7` non è quindi specificità
  comparata e non va citato come tale. Ciò che regge è la forma debole: **entrambi i lati producono
  voci ancorate, localizzabili e conformi**, che è la proprietà che il contratto di conformità
  doveva rendere una forma invece che un giudizio. L'ipotesi sul filtro **non prende né conferma né
  smentita** da questo ciclo.
- **Resa del filtro: 1 voce applicata su 11 conformi.** Misura la resa, non la precisione: delle 10
  scartate non si sa quante fossero regole false e quante regole buone perse. La precisione è
  misurabile solo nel tempo, sull'assenza di regressioni fra le voci applicate.
- **Accordo fra i due strumenti di `verdetto`: 13 righe su 17 (0,76) con tutti e quattro i verdetti
  concordi; 29 verdetti su 34 (0,85) contando per coppia riga-piano.** Il confronto con lo 0,56 di
  inter-grader agreement del grading è **istruttivo ma non alla lettera**: unità diversa, compito
  diverso. Ciò che si confronta è l'ordine di grandezza, ed è lo stesso.
- **4 righe su 17 senza verdetto** — `R-002`, `R-004`, `R-008`, `R-009`. È il ~24% dell'unica
  superficie che il rilevatore guarda, muto per un ciclo. Le quattro discordanze **non sono rumore**:
  cadono tutte su righe la cui formulazione ammette due letture, quindi accusano le righe prima degli
  strumenti. Riscriverle è lavoro dovuto prima di CON-7.
- **Accordo fra i due `REVIEW`: 11 voci su 11 sulla classificazione (1,00), 0 su 1 su `Remedy carried
  by`.** Il filtro ha licenziato *cosa* applicare e non *come*.
- **Costo reale: 5 sessioni supervisionate** — S1, S2, S2b, S3, S4 — e **11 chiamate contro le 9**
  pubblicate. Le chiamate non sono il costo dominante; le sessioni sì.
- **Manutenzione contro resa: 3 correzioni strutturali alla procedura e 4 aggiustamenti di strumento,
  contro 1 modifica allo skill.** È il numero da tenere d'occhio più di ogni altro: un ciclo che
  produce più manutenzione di sé che modifiche al suo bersaglio non è sostenibile per quanto onesti
  siano i suoi contatori. In un primo giro è atteso; se non scende, è la diagnosi.
- **Il cricchetto è stato fermato, per un ciclo.** 1 riformulazione, 0 aggiunte, `SKILL.md` 417 → 421.
  Contro il `+69% in sette giorni e un solo commit sottrattivo` di `RATIONALE.md` § *Il cricchetto*,
  è il primo giro con la firma opposta. Un ciclo non è una tendenza.
- **La prima previsione scritta prima della misura in tutto il corpus è `R-018`**, nata il 2026-08-07
  con la modifica che verifica. Con `R-010` e `R-011` sono tre righe `ex-ante` su diciotto, ed è la
  sola parte del meccanismo che, a CON-7, farà per la prima volta ciò che il file dichiara.

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
  quali criteri, non quanti. CON-6 ha mostrato che il caso non è raro: quattro righe indecise fra i
  due strumenti, e una — `R-006` — dove `recidiva` contraddice entrambi i verdetti.
- **`support/CLAUSE-ROW-MAP.md` è un costo ricorrente proporzionale al ritmo di cambiamento dello
  skill,** cioè la stessa forma di costo che ha ucciso il grading. 577 righe, 205 clausole ancorate
  **per numero di riga**: l'hunk di 4 righe applicato in CON-6 ha già sfalsato ogni sito dopo
  `SKILL.md:57` e cambiato il testo di `C-019`. `extract_clause_map.py` rigenera il `.tsv`, non la
  mappa. È l'unico tapis roulant del ciclo, ed è dichiarato qui perché nessun altro documento lo
  chiama con questo nome.
- **Il peso non è sceso, si è spostato dal codice alla prosa.** ~2.100 righe di procedura più ~950 di
  dati mantenuti, contro uno `SKILL.md` di 421 righe: un rapporto di circa 7 a 1. Il grading pesava
  3.477 righe di Python; il ciclo ne pesa 1.395, ma la differenza è finita nei documenti. La
  distinzione che tiene in piedi la scelta è il **tipo** di costo — la prosa si scrive una volta, la
  matrice di calibrazione si ricollezionava a ogni cambio — e vale finché il numero sopra non cresce.

## Soglia di abbandono

**Questa sezione è normativa.** È l'unica del file, e la ragione per cui esiste è simmetrica a un
errore già commesso: il grading system è morto portando un **gate di ripresa irraggiungibile per
costruzione** — `RATIONALE.md` § *Perché il grading system è abbandonato*. Il ciclo di consenso
aveva il difetto speculare, e cioè **nessuna soglia di abbandono affatto**: nessun numero che, se
raggiunto, dica di fermarsi. Uno strumento senza condizione di uscita non si valuta, si difende.

Le tre condizioni qui sotto sono **decidibili dai contatori che il report già pubblica**, senza
misure nuove e senza chiamate. È il requisito che il gate del grading non aveva, ed è il solo modo
per cui una soglia possa scattare davvero.

**Scattano insieme, non a maggioranza: basta una.** Sono valutate alla chiusura di **CON-8**, cioè
dopo due cicli oltre quello che ha prodotto i numeri di partenza.

1. **Manutenzione contro resa.** Il rapporto cumulato su CON-6…CON-8 fra *correzioni strutturali alla
   procedura* — sezione *Deviations from the procedure* del report — e *voci applicate allo skill* —
   contatore `entries applied` — **non è sceso sotto 1**. Valore di partenza a CON-6: **3 a 1**.
2. **Superficie muta del rilevatore.** Le *righe che il ciclo non ha potuto decidere* — contatore
   `rows the cycle could not decide` — restano **≥ 3** a CON-8, **dopo** che le quattro formulazioni
   ambigue di CON-6 sono state riscritte. La riscrittura è lavoro dovuto prima di CON-7: se non viene
   fatta, la condizione si valuta come se fosse scattata, perché una soglia aggirabile non
   rimandando il lavoro non è una soglia. Valore di partenza a CON-6: **4 su 17**.
3. **Il meccanismo non ha mai fatto il suo mestiere.** Nessuna delle righe `ex-ante` — `R-010`,
   `R-011`, `R-018`, e quelle che nasceranno con lo stesso `Provenance` — ha raggiunto
   `non smentita ×2` a CON-8. Sono le sole righe la cui previsione è stata scritta **prima** della
   misura; se dopo tre cicli nessuna accumula, il ciclo non sta verificando modifiche, sta
   collezionando difetti. Valore di partenza a CON-6: **0 su 3**.

**Cosa si fa se una scatta, deciso ora e non allora.** Non si calibra meglio, che è la risposta con
cui il grading ha comprato tre settimane. Si confronta il ciclo con l'**alternativa più economica che
ha storicamente prodotto miglioramenti**: un umano che legge un piano generato — `2c89e7f`, e i due
commit di CON-5 — cioè **una sessione contro cinque**. Di ciò che il ciclo aggiunge sopra quella
baseline si tiene solo la parte che si è pagata da sé, e la candidata è una sola: la **previsione
falsificabile attaccata alla modifica**, che è ciò che la lettura umana non dà e l'unica ragione per
cui il registro esiste. `improve`, `review`, il gate di conformità e la `recidiva` sono la parte che
in quello scenario si smonta, e con loro il tapis roulant di `support/CLAUSE-ROW-MAP.md`.

**Il validator strutturale e `EVALUATION-BRIEF.md` sopravvivono a qualunque esito.** Sono già
sopravvissuti al grading — `RATIONALE.md` § *Cosa il ciclo eredita* — e non dipendono da nessuno dei
due meccanismi.

**Nessuna delle tre condizioni riguarda l'ipotesi sul filtro.** Una sua falsificazione non fa cadere
l'obiettivo, e non deve poter far cadere lo strumento: queste soglie misurano se lo strumento **si
paga**, che è una domanda diversa e finora mai posta per scritto.
