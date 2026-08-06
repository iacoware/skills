# Registro delle affermazioni verificabili su `plan-slices`

Ogni modifica applicata a `skills/plan-slices/SKILL.md` nasce da un difetto osservato in un piano
generato e implica una previsione: *al prossimo ciclo quel difetto non ricompare*. Questo registro
tiene le previsioni in un posto solo, perché il ciclo di eval le verifichi invece di dimenticarle.

Serve a due cose:

- **Regressioni previste.** A ogni ciclo si rileggono le righe `tiene` e si verifica che l'affermazione
  regga ancora sul piano appena generato.
- **Regressioni non previste.** Se un piano di miglioramento solleva un difetto che una riga di questo
  registro dichiarava chiuso, la riga passa a `regredita`. Non serve un secondo artefatto: è lo stesso
  indice letto al contrario.

## Come si usa

- Una riga per modifica applicata allo `SKILL.md`, aggiunta nello stesso momento della modifica.
- L'affermazione deve essere **binaria e falsificabile** su un piano generato. «Il piano è più chiaro»
  non è un'affermazione; «ogni slice `NOW` cita la frase delle fonti che la richiede» lo è.
- `Origine` si apre con il modo in cui la modifica è stata decisa, e ha **quattro** valori:
  `intersezione` se entrambi i modelli proponevano lo stesso difetto **e lo stesso rimedio**;
  `intersezione-tema` se entrambi vedevano lo stesso difetto ma la formulazione viene da un lato solo;
  `giudizio` se un umano ha ritrovato il difetto sul piano generato e ha applicato un punto sollevato
  da un solo modello o da nessuno; `potatura` se la riga afferma che la rimozione di una clausola non
  fa ricomparire un difetto. I modi sbagliano in modo diverso — il primo manca cose, gli altri possono
  applicarne di false — e distinguerli è l'unico modo per accorgersene a posteriori.
- **Riclassificazione del 2026-08-06.** Le righe `R-002`…`R-008` portavano `intersezione` e sono
  passate a `intersezione-tema`. Lo dicono i `REVIEW` CON-4 stessi, campo `Differences`, ripetuto su
  ogni voce condivisa: *«questo report è operativo […]; l'altro report propone il meccanismo
  generico»*. `PLAN-CX-CON-4.IMPROVEMENT.md` è 8 bullet generici senza nessuno degli otto campi
  richiesti, quindi nessuna di quelle sette righe può avere avuto due formulazioni da intersecare. Le
  due righe falsificate in CON-5 — `R-002` e `R-008` — cadono esattamente dove questa categoria
  prevede: tema visto da due modelli, rimedio scritto da uno solo. Le sette righe sono inoltre state
  prodotte con prompt diversi da quelli oggi in `prompts/`.
- `Verifica` dichiara chi controlla: `validator` se il controllo è o può diventare strutturale in
  `skills/plan-slices/scripts/validate_plan.py`, `lettura` se richiede giudizio umano.
- `Misurato su` dichiara **contro cosa** è stato prodotto il verdetto, nella forma
  `ciclo · piani · strumenti`. Gli strumenti sono `piani` se bastano gli artefatti generati, più
  `fonti`, `brief` e `validator` quando servono. Senza questa colonna un verdetto sembra più solido
  di come è stato ottenuto: la regressione ritirata su R-006 era stata misurata sulle sole fonti,
  ignorando il brief, e la cella non lo diceva.
- `Stato`: `da verificare` finché non c'è un ciclo successivo alla modifica; `tiene` se l'ultimo ciclo
  l'ha confermata; `regredita` se un ciclo l'ha smentita, con la data.
- Una riga `regredita` non si cancella: si aggiunge la riga della correzione e si lasciano entrambe.
  La sequenza di regressioni sullo stesso tema è il segnale che la regola è formulata male, non che
  va riscritta ancora.
- **Il controllo si fa contro l'`EVALUATION-BRIEF.md` dello scenario prima che contro le fonti.** Il
  brief è l'autorità su quali conflitti esistono, quali alternative sono accettate e quali incertezze
  sono materiali; le fonti si aprono solo per verificare una citazione. Il registro sta sopra i
  singoli scenari e le sue righe non conoscono il brief: senza questo passo produce falsi positivi
  contro l'autorità dello scenario.
- **Se una riga contraddice una voce di `Accepted alternatives`, il difetto è nella riga.** Si
  riscrive per ammettere l'alternativa; non si registra una regressione. Stessa cosa se l'affermazione
  non è decidibile da ciò che il piano pubblica, o lo è solo scegliendo fra due letture: in tutti e
  tre i casi si annota il motivo, la data e i piani su cui è emerso, sotto *Formulazioni riscritte*.

## Registro

| ID | Commit `SKILL.md` | Origine | Affermazione verificabile | Verifica | Ultimo controllo | Misurato su | Stato |
|---|---|---|---|---|---|---|---|
| R-001 | `2c89e7f` | `giudizio` — `NOTES.md` § *Confine di scope vs identità* | Il piano colloca l'identità dopo il differenziatore **e** dichiara in `Cross-functional concerns` la giunzione unica da cui si risolve lo scope corrente. | lettura, automatizzabile in parte | 2026-08-04 | CON-5 · `CC`+`CX` · brief+piani | tiene |
| R-002 | `d977043` | `intersezione-tema` — `REVIEW` CON-4 § *Sweep sistematico delle contraddizioni* ≡ *Explicit handling of source contradictions* | Nessuna bullet `Includes` o `Verification` afferma in forma non condizionale un lato di un conflitto fra le fonti — quelli elencati in `Known conflicts` del brief, più quelli dimostrabili citando due fonti in disaccordo — e ogni scelta che il piano dichiara aperta nomina le slice `NOW` che blocca, in qualunque sezione la dichiari. | lettura per il primo membro; il secondo è automatizzabile sulla sezione delle scelte aperte, qualunque sia il suo titolo (ogni voce cita almeno un numero di slice `NOW` esistente) | 2026-08-04 | CON-5 · `CC`+`CX` · brief+fonti | regredita su `CC` |
| R-003 | `d977043` | `intersezione-tema` — `REVIEW` CON-4 § *Decisioni mai prese distinte dalle decisioni prese* ≡ *Explicit handling of undecided choices* | Nessuna slice `NOW` dipende da una scelta esterna — provider, modello, servizio o adapter — che non sia presa da una fonte citabile, o presa dal piano fra le alternative che il brief dichiara accettabili, o dichiarata aperta con la slice che blocca, in qualunque sezione la dichiari; un aggettivo qualificante — `cheap`, `multilingual`, `managed` — non conta come scelta. | lettura: l'inventario delle dipendenze esterne richiede il confronto con le fonti e con le `Accepted alternatives` del brief | 2026-08-04 | CON-5 · `CC`+`CX` · brief+fonti | tiene |
| R-004 | `d977043` | `intersezione-tema` — `REVIEW` CON-4 § *Ammissione in NOW subordinata a una domanda delle fonti* ≡ *Trace scope and horizon ownership* | Nessuna slice `NOW` consegna un comportamento che le fonti non richiedono; ogni voce `LATER` dichiara un `Promotion trigger` e ogni voce `OUT-OF-SCOPE` una razionale di esclusione. | lettura per il primo membro — lo skill colloca la tracciatura nel ragionamento, non nel piano; il secondo è automatizzabile sulla struttura del template | 2026-08-04 | CON-5 · `CC`+`CX` · brief+fonti | tiene |
| R-005 | `d977043`, `9aa2586` | `intersezione-tema` — `REVIEW` CON-4 § *Continuità del tema* ≡ *Keep a theme and its recovery path contiguous* | Se una slice `NOW` nomina un modo di fallimento nella propria `Verification` e un'altra slice `NOW` ne è il rimedio, nessuna slice di un tema diverso è collocata fra le due. | lettura per l'accoppiamento fallimento→rimedio; l'interposizione di temi è automatizzabile sull'annotazione `*(Theme: X)*` delle slice | 2026-08-04 | CON-5 · `CC`+`CX` · piani | tiene |
| R-006 | `d977043`, `9aa2586` | `intersezione-tema` — `REVIEW` CON-4 § *Pipeline o adapter condiviso con un solo proprietario* ≡ *Open shared pipelines and adapters once, after their producers* | Una pipeline o un adapter condiviso da più percorsi è aperto negli `Includes` di una sola slice `NOW`; le slice successive che lo riusano lo dichiarano tale. Quella slice segue ogni slice `NOW` che le fornisce input, salvo quando valida input controllati che attraversano il calcolo di produzione e il brief dello scenario ammette la validazione anticipata. | lettura per l'identificazione dei produttori; l'unicità del proprietario è automatizzabile in parte (stesso adapter nominato negli `Includes` di due slice) | 2026-08-04 | CON-5 · `CC`+`CX` · brief+piani | tiene |
| R-007 | `d977043` | `intersezione-tema` — `REVIEW` CON-4 § *Audit esplicito di split* ≡ *Split capabilities and enablers with independent risks* | Nessuna slice `Enabler` valida incertezze su più di un sottosistema: la sua `Verification` non può fallire per cause che, in `Material uncertainties` del brief, appartengono a `Subsystem` diversi. Più voci dello stesso sottosistema sono una incertezza sola, anche quando la risposta invalida la scelta verificata. | lettura: il verdetto di split per coppia vive nel ledger non pubblicato, sul piano resta osservabile solo l'esito; l'elenco delle incertezze, dei sottosistemi e delle decisioni che cambiano lo pubblica il brief | 2026-08-04 | CON-5 · `CC`+`CX` · brief+piani | tiene |
| R-008 | `9aa2586` | `intersezione-tema` — `REVIEW` CON-4 § *Use repeatable, decision-changing verification*, parte «each theme has a first validation» | La `First validation` di ogni tema punta a una slice `NOW` non annotata `Enabler`, il cui `Outcome` copre l'intero desired outcome del tema; l'eccezione vale solo se il desired outcome del tema è dichiaratamente per uno sviluppatore. | validator per l'esistenza del riferimento e, da R-011, per l'esclusione degli `Enabler`; lettura per la copertura dell'outcome | 2026-08-04 | CON-5 · `CC`+`CX` · brief+piani | regredita su `CX` |
| R-009 | `a06a5cc` | `giudizio` — messaggio di commit di `a06a5cc`, difetto osservato su un piano graduato | Nessun `Outcome` di una slice `NOW` che precede l'identità promette un utente reale: ogni slice che precede l'identità e consegna un comportamento nomina il proprio pubblico, sviluppatore o tester sull'ambiente non pubblico dichiarato. Se le slice `NOW` che consegnano comportamento a un utente finale prima dell'identità sono più di due, `Ordering criteria` giustifica una volta il differimento residuo nominando l'evidenza che lo richiede. | lettura: il pubblico si legge dagli `Outcome` e la giustificazione dagli `Ordering criteria`, ma decidere se una slice consegna a un utente finale richiede giudizio | 2026-08-04 | CON-5 · `CC`+`CX` · piani | tiene |
| R-010 | `87150d3` | `giudizio` — correzione di R-002, primo membro, regredita su `CC` in CON-5 | Una scelta che il piano non risolve citando una fonte che seleziona resta aperta anche quando il piano la dichiara in `Open questions` o le assegna una spike: nessuna bullet `Includes` o `Verification` di una slice che quella scelta blocca ne asserisce un lato. | lettura: riconoscere quali slice una scelta aperta blocca richiede il confronto fra la dichiarazione e le bullet | — | — | da verificare |
| R-011 | `eb926bb` | `giudizio` — correzione di R-008, clausola `Enabler`, regredita su `CX` in CON-5 | Nessuna riga della tabella `Themes` la cui `First validation` risolve a una slice annotata `*(Enabler: …)*` omette il marcatore `*(Developer outcome)*` nella cella `Desired outcome`. | validator: il controllo incrocia due fatti già pubblicati, il numero di slice risolto dalla cella e il tag del titolo di quella slice | — | — | da verificare |

### Regressioni rilevate — ciclo CON-5 (2026-08-04)

Controllo offline su `recipe-app/results/PLAN-CC-CON-5.md` e `PLAN-CX-CON-5.md`, generati dopo
`9aa2586`. Un'affermazione regge solo se regge su entrambi: le righe qui sotto sono smentite da uno
solo dei due, e tanto basta.

- **R-002, primo membro — `PLAN-CC-CON-5.md`, slice 4, `Includes`.** «Query embeddata e confrontata
  in una sola interrogazione Postgres, con scope al ricettario risolto» afferma in forma non
  condizionale il lato `concepts.md` di una contraddizione con le fonti — `goal.md` § *Vincoli e
  scala* e `arch-choices.md` § *Embeddings* vietano l'embedding «a runtime sulle query di ricerca»,
  `concepts.md` § *Ricerca (MVP)* definisce la ricerca come `similarity(Recipe.embedding,
  embedding(query))`. Il piano riconosce la contraddizione altrove — `Learning / risk` della stessa
  slice e voce `Open questions` che ne blocca l'accettazione — ma la bullet `Includes` resta
  assertiva. Il piano `CX` non viola il membro: slice 2 e 3 dicono «query generata secondo la
  decisione presa/della spike».
- **R-002, primo membro — `PLAN-CC-CON-5.md`, slice 2, `Includes`.** Seconda violazione della stessa
  riga, sul secondo conflitto dichiarato dal brief. «Form condiviso creazione ed edit: titolo,
  ingredienti e preparazione come testo libero, nessun parsing di quantità e unità» asserisce il
  percorso manuale mentre `EVALUATION-BRIEF.md` § *Known conflicts* impone di «defer to a resolved
  interpretation **before asserting the manual path**»: `concepts.md` § *Pipeline di estrazione* fa
  saltare l'estrazione all'input manuale, `arch-choices.md` § *Estrazione contenuto* gliela fa
  riusare. Il piano risolve il conflitto di soppiatto, scegliendo il lato `concepts.md` in una voce
  `LATER` («Derivazione di tag e tempo per le ricette inserite a mano»). `CX` fa quanto richiesto:
  slice 5 «trattamento di tag e tempo conforme alla decisione del lavoro non-prodotto», con la voce
  corrispondente in `Non-product work`.
- **R-008 — `PLAN-CX-CON-5.md`, tabella `Themes`.** Tre voci smentiscono la riga, su entrambi i
  membri. Riga A: la `First validation` è «2. Indicizzazione multilingue osservabile», slice
  annotata `*(Enabler: ricerca semantica)*`, mentre il desired outcome del tema — «Trovare nel
  ricettario corrente ricette pertinenti anche tra lingue diverse» — non è dichiarato per uno
  sviluppatore, quindi l'eccezione non si applica. Riga D: desired outcome «cover controllabile»
  contro l'`Outcome` della slice 9, «una cover stabile senza hotlink fragile» — la scelta della cover
  arriva solo alla slice 11. Riga C: desired outcome «da input manuale, URL o testo» contro
  l'`Outcome` della slice 5, che copre il solo inserimento manuale. Il piano `CC` regge su tutte e
  sei le righe.

### Formulazioni riscritte — ciclo CON-5 (2026-08-04)

Righe che il ciclo non ha potuto decidere, che ha deciso solo scegliendo fra due letture, o che
contraddicevano l'`EVALUATION-BRIEF.md` dello scenario. In tutti i casi il difetto è nella riga: qui
resta il motivo, perché la riscrittura non si perda nella storia del file.

- **R-006 — contraddiceva il brief, riscritta, verdetto `tiene`.** Il ciclo aveva registrato una
  regressione su `PLAN-CX-CON-5.md`: la pipeline di embedding sulle scritture apre alla slice 2
  («Ricette normalizzate controllate attraversano il percorso reale di embedding … e persistenza
  pgvector») e i suoi produttori — 5 manuale, 6 URL, 7 incolla, 8 fallback — la seguono tutti, quindi
  la slice che la apre non segue i propri produttori. Ma `EVALUATION-BRIEF.md` § *Accepted
  alternatives* ammette esattamente questo: «Controlled inputs may validate extraction, embeddings,
  or search before their final user entry point when they traverse the production computation». Il
  secondo membro è stato emendato con quella deroga. Resta osservato, senza valore di regressione,
  che `CX` nomina l'embedding negli `Includes` di quattro slice (2, 5, 6, 7) senza mai dichiarare
  quali siano riuso: è la ragione per cui il primo membro ora chiede la dichiarazione esplicita.
- **R-007 — riscritta sul criterio dichiarato, verdetto `tiene`.** Nella formulazione originale il
  membro chiedeva quali *decisioni* cambierebbero al fallimento della `Verification` di un `Enabler`,
  e il piano pubblica la mappa decisione↔slice solo dove c'è un `Decision checkpoint`: per gli
  `Enabler` di consegna non ce n'è nessuno — `CC` apre i checkpoint alla slice 3, `CX` alla slice 2 —
  cioè proprio dove serviva. Il ciclo l'ha quindi lasciata non decisa.
  Il criterio è stato poi dichiarato: R-007 esiste per impedire che una slice metta troppa carne al
  fuoco, dove la soglia è che ogni slice resti implementabile in una sessione fredda separata, senza
  context rot. Da lì discende che il taglio non è per decisione ma per **sottosistema**: verificare
  che l'infrastruttura di consegna scelta soddisfi resta una incertezza sola anche quando la risposta
  la invalida e costringe a cambiare bersaglio; sarebbero due se la stessa slice validasse anche il
  motore semantico. La riga e la tabella `Material uncertainties` del brief sono state riscritte su
  questo taglio.
  Verdetto sui sei `Enabler`: `CC` 0 e `CX` 0 non toccano incertezze materiali; `CC` 1 e `CX` 1
  stanno interamente in *Delivery infrastructure* — la seconda bullet di `Verification` di `CX` 1
  («Arresto, risveglio da `suspend`, nuova connessione e redeploy preservano il round trip») unisce
  U1 e U2, stesso sottosistema; `CC` 3 e `CX` 2 stanno interamente in *Semantic engine*, e il
  controllo di scope in `CX` 2 non conta, perché è un hard constraint del brief e un suo fallimento è
  un bug, non un cambio di decisione. Nessuno dei due piani viola la riga.
- **R-002, secondo membro — riscritta, era vera a vuoto.** Il membro quantificava sulle voci di
  `Open questions`, sezione che `CX` non ha: le sue scelte non prese stanno in `Non-product work`,
  ognuna con la slice che blocca («prima della slice 1», «prima della slice 2»…). Così com'era, un
  piano lo soddisfaceva omettendo la sezione. Ora il membro quantifica sulle scelte dichiarate
  aperte, qualunque sia il titolo della sezione che le ospita. Il primo membro è stato agganciato ai
  `Known conflicts` del brief, che nel frattempo ha ricevuto il conflitto sull'embedding di query:
  prima il conflitto andava ricostruito dalle fonti a ogni ciclo.
- **R-003 — riscritta, puniva chi decide.** La disgiunzione ammetteva solo «selezionato da una fonte
  citabile oppure in `Open questions`», ma `EVALUATION-BRIEF.md` § *Accepted alternatives* consente
  al piano di scegliere da sé Neon o Supabase, l'embedder multilingue e il modello di estrazione: un
  piano che sceglie sarebbe stato bocciato. Il vincolo che conta è che nessuna scelta esterna entri
  in `NOW` senza essere né presa né dichiarata aperta, e la riga ora dice quello. Sui due candidati
  il verdetto non cambia — entrambi dichiarano tutte le scelte esterne aperte con la slice che
  bloccano, `CC` in `Open questions` e `CX` in `Non-product work` — ma prima reggeva solo scegliendo
  la lettura sostanziale contro quella letterale.

### Chiusura del ciclo CON-5 — righe rimaste (2026-08-04)

Righe che il primo passaggio del ciclo non aveva toccato, o che aveva misurato con lo strumento
sbagliato. Stessi due piani, stesso criterio: un'affermazione regge solo se regge su entrambi.

- **R-001 — `tiene` su entrambi.** Primo membro: il brief dichiara che il differenziatore è la
  ricerca semantica multilingue e che `NOW` deve validarla; `CC` la valida agli slice 3 e 4 e
  consegna l'identità allo slice 5, `CX` agli slice 2 e 3 con l'identità allo slice 4. Il secondo
  differenziatore che `CX` dichiara negli `Ordering criteria` — l'estrazione fallback, slice 7 e 8 —
  non sposta il verdetto: l'autorità sul differenziatore è il brief, non il piano. Secondo membro:
  `CC` § *Authorization* dichiara «l'unico risolutore `currentCookbook` … diventa derivato dalla
  sessione allo slice 5, che è il seam unico del passaggio»; `CX` dichiara «un solo
  `CurrentCookbookResolver`; lo scope configurato delle slice 2–3 è sostituito da sessione e
  membership nella slice 4». In entrambi la giunzione è unica e nominata con la slice che la
  attraversa.
- **R-004 — rimisurata sul brief, il verdetto `tiene` non cambia.** Il primo passaggio l'aveva
  misurata sulle sole fonti, lo stesso difetto che aveva prodotto la regressione ritirata su R-006.
  Riletto su `Authority` e `Hard constraints`, il primo membro regge: ogni slice `NOW` dei due piani
  ricade in una sezione che il brief dichiara autorevole — ricerca semantica scoped, pipeline di
  estrazione JSON-LD-poi-fallback, salvataggio senza review con l'edit come recupero, Google OAuth,
  foto su object storage con cover cambiabile, condivisione per invito fra pari. Il perimetro delle
  esclusioni è quello di `Fuori scope MVP`: ricettari pubblici, filtri strutturati, ricerca
  cross-ricettario, gruppi e ruoli granulari non compaiono in `NOW` in nessuno dei due — `CX` slice 4
  nomina `visibility=private`, che è la conferma del default, non l'apertura del caso pubblico.
  Sulle fonti si è aperto solo `goal.md` § *Fuori scope MVP*, per verificare il perimetro citato dal
  brief, e le righe su foto multiple e cover cambiabile. Il secondo membro è strutturale e regge:
  sette voci `LATER` in `CC` e otto in `CX`, tutte con `Promotion trigger`; nove voci `OUT-OF-SCOPE`
  in `CC` e cinque in `CX`, tutte con razionale.
- **R-009 — riga nuova, ricostruita da `a06a5cc`, `tiene` su entrambi.** Il commit non ha riga di
  registro e non è ricostruibile dai `REVIEW`: il miglioramento compare in un solo report. Il difetto
  osservato sta nel suo messaggio — «one graded plan accepted four product slices on a scope no user
  owned, each Outcome promising a user who did not exist yet» — e la previsione è ricostruita da lì.
  La formulazione sceglie il criterio dell'`Outcome` che promette un utente inesistente, non la
  lettura letterale «ogni slice dichiara un pubblico»: quest'ultima boccerebbe un `Enabler` il cui
  `Outcome` non promette nessun utente — `CC` slice 1 — che è esattamente il caso che il difetto
  osservato non riguarda. La soglia resta il secondo membro, condizionale, come nel commit: fa
  scattare una giustificazione, non un tetto al differimento.
  Verdetto: nelle slice che precedono l'identità nessun `Outcome` promette un utente reale. `CC`
  (identità alla slice 5) dichiara sviluppatori alle slice 0, 2 e 3, «chi prova l'app sull'ambiente
  non pubblico» alla 4; `CX` (identità alla slice 4) dichiara sviluppatori alle slice 0, 1 e 2 e «un
  tester» alla 3, con l'`Includes` che limita il pubblico ai tester autorizzati. Le slice `NOW` che
  consegnano a un utente finale prima dell'identità sono quindi zero in entrambi e la soglia non
  scatta; `CC` giustifica comunque il differimento negli `Ordering criteria` («nessuna behaviour
  rivolta a utenti reali precede lo slice 5»).

### Correzioni applicate dopo il ciclo CON-5 (2026-08-04)

- **R-010, correzione di R-002 — `87150d3`.** La regola violata esisteva già, nel corpo del passo 1 e
  nel `Complete when`. Non è stata riscritta per aggiungere un divieto: era autocontraddittoria. Lo
  stesso periodo usava `close` per l'atto di dichiarare («*Close* every material entry either with an
  `Open questions` item … or with a spike») e per l'atto di decidere («*Until it closes*, no
  `Includes` or `Verification` bullet may assert a side»). `CC` ha fatto letteralmente la prima —
  voce `Open questions` sul conflitto dell'embedding di query, con la slice bloccata — e ne ha
  dedotto il diritto di asserire nella slice 4. La correzione separa *esporre* da *risolvere*: solo
  una fonte che seleziona risolve, mentre una domanda pubblicata e una spike pianificata lasciano
  aperta la voce, perché al momento in cui il piano è scritto nessuna delle due ha prodotto la
  risposta. Entrambe le sedi restano ammesse, come richiede R-003: cambia solo cosa autorizzano a
  scrivere nelle slice bloccate.
  **Da cercare al prossimo ciclo, oltre alla riga.** La correzione nasce da una violazione su un solo
  modello: `CX` non violava nessuno dei due membri di R-002 e usava già la formulazione condizionale.
  È il modo tipico in cui `giudizio` applica una regola falsa. Il fallimento da sorvegliare non è il
  ritorno dell'assertivo ma il suo opposto: piani che rinviano tutto alla decisione pendente e non
  pubblicano più niente di verificabile. Se compare, il difetto è in R-010, non nei piani.

- **R-011, correzione di R-008 limitata alla clausola `Enabler` — `eb926bb`.** Anche qui la regola
  violata esisteva già: il § 2 la porta da `9aa2586`, e `PLAN-CX-CON-5.md` è stato generato dopo
  quel commit e l'ha violata lo stesso. Un secondo divieto testuale sarebbe la mossa già fallita.
  La modifica non aggiunge un vincolo: rende **dichiarabile** l'eccezione già ammessa. Il tema che
  la invoca appende `*(Developer outcome)*` alla cella `Desired outcome`, e il validator confronta
  quel marcatore con il tag del titolo della slice che la cella risolve. Il gate smette di chiedere
  a chi scrive un'affermazione e mette a confronto due fatti che il piano pubblica già.
  Verificato sugli artefatti esistenti: il controllo scatta su `CX` CON-5 riga A e su `CC` CON-3
  riga B — stesso difetto, altro modello, ciclo precedente a `9aa2586` — e non produce falsi
  positivi su `CC` CON-2, CON-4 e CON-5, che restano `OK`. La correzione non nasce quindi da una
  sola osservazione su un solo modello, che era la ragione per cui era stata rimandata.
  **Da cercare al prossimo ciclo, oltre alla riga.** Il marcatore è dichiarativo: un piano può
  apporlo a un desired outcome che per uno sviluppatore non è. Il validator non lo può sapere, e
  quel residuo resta `lettura` dentro R-008. Il fallimento da sorvegliare è il marcatore apposto
  per far passare il controllo, non la sua assenza.

### Diagnosi decise dopo il ciclo CON-5 (2026-08-04)

Le tre voci della tabella `Themes` di `PLAN-CX-CON-5.md` che hanno fatto regredire R-008 non hanno
la stessa causa, e questo era il nodo che bloccava la correzione. Misurato su CON-5 · `CX` ·
brief+piani, con controllo incrociato su CON-2, CON-3 e CON-4 di entrambi i modelli.

- **Riga A — puntamento sbagliato, corretta da R-011.** Il tema è tagliato bene e la slice che
  copre l'intero desired outcome esiste già: la 3, `*(Theme: A)*`, `Outcome` «Un tester può
  valutare il principale differenziatore nel prodotto reale distribuito». La cella punta una slice
  troppo presto, alla 2, il cui `Outcome` nomina esplicitamente gli sviluppatori mentre il desired
  outcome del tema — «Trovare nel ricettario corrente ricette pertinenti anche tra lingue diverse»
  — no. L'`Accepted alternative` del brief sugli input controlli («may validate extraction,
  embeddings, or search before their final user entry point») autorizza l'**ordine**, cioè che
  l'`Enabler` preceda il validatore, cosa che R-008 già ammette al primo periodo; non dice nulla su
  quale slice la cella `First validation` debba nominare. Nessuna contraddizione con il brief:
  il difetto è nel piano.
- **Riga C — `Theme compression`, non primo validatore parziale.** Il tema C tiene le slice 5
  (manuale), 6 (URL/JSON-LD), 7 (incolla/LLM) e 8 (fallback LLM automatico).
  *Test di split, applicato:* ciascuna può essere cancellata, differita o riordinata senza
  invalidare l'evidenza delle altre. L'evidenza della 6 è l'hit-rate JSON-LD sui blog reali (U4 del
  brief), quella della 7 è accuratezza e costo del modello cheap a output strutturato (U5), quella
  della 5 è che il modello testuale minimo riduce l'attrito — nessuna delle tre ha bisogno delle
  altre. Il piano lo dichiara da sé: tre `Learning / risk` distinti e due voci di `Non-product work`
  separate, «Arricchimento manuale, prima della slice 5» e «Selezione LLM estrazione, prima della
  slice 7». I cinque criteri del § 2 separano su quattro: lavoro dell'utente (scrivere una ricetta
  che si conosce vs salvarne una trovata online), frequenza d'uso (gli `Ordering criteria` dello
  stesso piano dicono che l'import da URL è il «caso più frequente»), rischio primario (attrito vs
  U4 vs U5), adapter e profilo operativo (form condiviso vs fetch server-side con SSRF e parser
  JSON-LD vs provider LLM con timeout e costo per chiamata).
  *Test di merge, applicato:* fallisce. Ciò che le quattro slice condividono è il salvataggio
  immediato, il form di edit e la rigenerazione dell'embedding — cioè «a shared entity, form,
  pipeline, or implementation», che il § 2 nomina esplicitamente come ragione **non** sufficiente
  per unire valore schedulabile in modo indipendente.
  *Controprova strutturale:* se il tema fosse legittimo, l'unica slice che copre «manuale, URL o
  testo» sarebbe la 8, l'ultima del tema. Un tema il cui desired outcome è validabile solo dalla
  propria ultima slice non ha un primo validatore per costruzione: è compresso, non mal puntato.
  *Controprova fra generazioni:* `CX` CON-3 taglia le stesse capacità in tre temi (C manuale, D
  importazione web, E estrazione resiliente) e CON-4 in due (C manutenzione, D acquisizione da
  fonti esterne); `CC` CON-5 in due (A cattura manuale, B import automatico). CON-5 di `CX`
  comprime rispetto ai propri cicli precedenti e rispetto all'altro modello.
  *Sede:* il test di split del § 2, che vieta già esattamente questo e non va riscritto. **R-008
  resta scoperta sulla riga C**: la correzione non è sua. Nessuna modifica applicata — un vincolo
  aggiunto a R-008 sulla copertura enumerativa avrebbe scritto una regola contro il difetto
  sbagliato, che è la ragione per cui la proposta era stata rimandata.
- **Riga D — copertura parziale, causa diversa dalla C.** Qui il tema regge: le slice 9 e 11
  condividono l'adapter R2 e l'unico invariante pubblicato in `Cross-functional concerns` («una sola
  foto è cover»), e la 11 non produce evidenza utile senza la 9. Il test di merge passa su
  interazione e invariante, quindi non c'è compressione. Il difetto è la copertura: desired outcome
  «Conservare foto affidabili con una cover controllabile» contro l'`Outcome` della slice 9, «una
  cover stabile senza hotlink fragile», che copre il solo termine dell'affidabilità; la scelta della
  cover arriva alla 11. La lettura alternativa — «controllabile» come «controllata dal sistema,
  non in hotlink» — è esclusa dal vocabolario del piano stesso: la slice 11 chiama quell'atto
  «controllarne l'immagine principale». Decidibile da ciò che il piano pubblica, quindi la riga non
  va in *Formulazioni riscritte*. La terza clausola di R-008 vieta già il caso; nessuna modifica
  applicata, e la verifica resta `lettura` perché il confronto termine per termine si fa su una
  cella scritta nella lingua dell'utente.

### Difetti degli artefatti mai registrati (2026-08-04)

Difetti reali degli artefatti generati che nessun ciclo aveva annotato. Non sono regressioni: non
c'è una riga di registro che li dichiarasse chiusi. Gli artefatti non sono stati modificati.

- **`CX` CON-2, CON-3 e CON-4 — 17 celle `First validation` non risolvibili.** `validate_plan.py`
  fallisce con `must start with a NOW slice number` su 4 righe in CON-2, 7 in CON-3 e 6 in CON-4:
  ogni cella porta il solo titolo della slice e nessun numero, mentre il template chiede
  `[NOW slice number]`. Il riferimento va quindi ricostruito accoppiando titoli a mano, che è
  esattamente il lavoro che la colonna esiste per evitare, e nessuna delle affermazioni di R-008 è
  decidibile da quelle celle senza quel passaggio. `CC` supera il controllo su tutti e tre i cicli
  e `CX` CON-5 è il primo piano `CX` che pubblica il numero. Misurato su CON-2..CON-4 · `CX` ·
  validator.
  Il difetto non è attribuibile a una riga esistente: R-008 nasce con `9aa2586`, dopo quei tre
  cicli, e la tolleranza del validator alla cella che porta anche il titolo è di `c10111d`, più
  recente ancora. Resta un dato sulla direzione del formato, non una previsione smentita.

## Miglioramenti concordi non arrivati nello skill

Estratti dalle sezioni `Improvements also present in the other report` dei due `REVIEW` CON-4 e
verificati contro il diff di `d88328f`, `b0d6dc5`, `d977043`, `a06a5cc` e `9aa2586`. Restano qui
finché non sono applicati o esplicitamente scartati con una ragione.

### Mai applicati

- **Controlli semantici nel validatore.** Entrambi i report chiedevano che le regole diventassero
  controllabili da uno strumento: il report `CX` al bullet 7 propone di estendere il validatore con
  controlli semantici configurabili — temi interrotti, adapter duplicati, domande dichiarate ma
  ignorate dalle slice — e il report `CC` riconosce le due sedi come compatibili. È stata applicata
  solo la sede testuale: `d977043` aggiunge i controlli ai `Proceed when` e al `Complete when`, cioè
  a gate che valuta chi scrive il piano. `validate_plan.py` non è toccato da nessuno dei cinque
  commit e resta strutturale: sezioni, campi delle slice, ordine, tabella dei temi. I tre controlli
  proposti sono esattamente quelli che oggi rendono `lettura` le righe R-002, R-005 e R-006.
- **Set di valutazione versionati per i claim di qualità.** Il `REVIEW` `CX` classifica come comune
  *Use repeatable, decision-changing verification* e vi aggancia la richiesta del report `CC` di
  «set di valutazione versionati con casi positivi e negativi» per ogni claim di qualità, rilevanza
  o accuratezza. Nello `SKILL.md` non esiste alcuna occorrenza: dei due membri del tema è stato
  recepito solo il primo validatore di tema (R-008). Senza questa regola, una slice può verificare
  che un motore semantico risponda, non che risponda bene.

### Recepiti nel ragionamento, quindi non osservabili su un piano

Non sono voci di registro perché nessuna affermazione su un piano generato può falsificarle: lo
skill richiede l'output e poi ne vieta la pubblicazione. Il miglioramento è applicato, la sua
verificabilità no.

- **Citazione della fonte per ogni slice `NOW`.** Chiesta da entrambi i report — «ogni slice `NOW`
  cita la frase delle fonti che ne richiede il comportamento» / «require every `NOW` slice to cite a
  source that requests it». `d977043` introduce il test di ammissione ma prescrive `Trace each NOW
  slice to the requesting statement in reasoning, not in the published plan`.
- **Riferimenti a entrambi i lati di ogni conflitto e verdetto di split per ogni coppia adiacente.**
  `d977043` chiede lo sweep con un riferimento per lato e il verdetto per coppia; `9aa2586` colloca
  entrambi nel ledger e chiude con `Keep the ledger in reasoning, not the published plan`.

Questa è una scelta di progetto — il piano pubblicato resta una roadmap, non un registro di audit —
ma ha un costo misurabile: tre dei sei miglioramenti comuni recepiti producono, sul piano, solo una
conseguenza indiretta. Se il ledger fosse un artefatto separato e versionato accanto al piano, R-003,
R-004 e R-007 diventerebbero controllabili senza toccare il template.

## Da popolare

- **Correzione per R-008, parziale.** R-002 è coperta da R-010; R-008 è coperta da R-011 sulla sola
  clausola `Enabler`, cioè sulla riga A della regressione. Restano scoperte la riga C — la cui sede
  è il test di split del § 2, non R-008 — e la riga D, che R-008 vieta già e che nessuno strumento
  può decidere al posto di una lettura. Le tre diagnosi stanno in *Diagnosi decise dopo il ciclo
  CON-5*.
- **Correzioni rimandate in attesa di un secondo ciclo.** Tre proposte nate dalle stesse due
  regressioni sono state scritte e non applicate, perché ognuna estende un perimetro o aggiunge un
  vincolo sulla base di una sola osservazione, su un solo modello. Il registro esiste per distinguere
  questo caso: sono candidate `giudizio`, e un secondo ciclo le rende `intersezione` di fatto o le
  scarta. Il pattern comune a R-002 e R-008 non è che manchino regole — quelle violate esistevano
  entrambe — ma che i gate chiedono affermazioni invece di confronti: aggiungere altri divieti
  testuali ha una probabilità non piccola di non mordere, come i due già presenti.
  - **Scelta di un lato per collocazione in un altro horizon.** Il divieto di R-010 copre `Includes` e
    `Verification`. `CC` ha scelto il lato `concepts.md` del conflitto manuale/estrazione mettendo la
    derivazione di tag e tempo per le ricette manuali in una voce `LATER`, sede fuori perimetro.
    L'estensione — collocare in `LATER` o `OUT-OF-SCOPE` un comportamento che solo un lato del
    conflitto richiede è sceglierlo — va applicata insieme all'allineamento dell'anti-pattern
    *Silent contradiction*, che oggi nomina solo la slice non condizionale. **Sblocca:** la stessa
    scelta per collocazione osservata su una generazione diversa da `CC`.
  - **`First validation` che punta a un `Enabler`, controllata dal validator. — Applicata, R-011
    (2026-08-04).** Sbloccata dalla prima delle due vie che la voce indicava: il marcatore esplicito
    `*(Developer outcome)*` nel template. La condizione «una sola osservazione su un solo modello»
    è caduta con `CC` CON-3 riga B, che porta lo stesso difetto.
  - **Copertura del desired outcome, confronto termine per termine. — Non applicata, diagnosi decisa
    (2026-08-04).** La diagnosi alternativa che la voce chiedeva di decidere è quella giusta sulla
    riga C: `Theme compression`, sede il test di split del § 2, che già la vieta. Sulla riga D invece
    la diagnosi enumerativa regge, ed è già coperta dalla terza clausola di R-008. Le due righe hanno
    cause diverse, quindi una sola regola nuova accanto a R-008 avrebbe mancato entrambe. Nessuna
    regola aggiunta. **Sblocca una regola nuova:** una copertura parziale osservata su un tema che
    supera il test di split, cioè non riducibile a compressione, su una generazione diversa da `CX`
    CON-5.
- **Modifiche dei cinque commit senza riga di registro.** `d88328f` (walking skeleton non cavo) e
  `b0d6dc5` (limitazione alle roadmap ad alto livello) non sono ricostruibili dall'intersezione dei
  due `REVIEW`: il primo non compare in nessuna delle due sezioni `also present`, il secondo non ha
  una corrispondenza verificata. Sono modifiche entrate per giudizio su un difetto osservato e la
  loro previsione va ricostruita da lì, non dai `REVIEW`. `a06a5cc` (soglia al differimento
  dell'identità) era nella stessa condizione ed è ora R-009, ricostruita dal proprio messaggio di
  commit, che nomina il difetto osservato.
- **Modifiche precedenti a `d88328f`.** Nascono da conversazioni fra umano e agente sui piani
  generati, precedenti al confronto fra modelli: non esiste un artefatto da cui ricostruire una
  previsione. Si registrano solo se un ciclo futuro ne solleva una regressione.
