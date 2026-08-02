# Review of `PLAN-CC-CON-4.IMPROVEMENT.md`

## Inputs

- **Reviewed report:** `PLAN-CC-CON-4.IMPROVEMENT.md`
- **Compared with:** `PLAN-CX-CON-4.IMPROVEMENT.md`

## Improvements also present in the other report

### `Sweep sistematico delle contraddizioni tra fonti con chiusura obbligatoria`

- **In this report:** §1 osserva che la slice 4 asserisce un lato di un conflitto tra fonti («la query viene embeddata a runtime») senza nominarlo in `Open questions`. Propone nel passo 1 un output obbligatorio con le coppie di affermazioni in conflitto e riferimento `file:riga` per entrambi i lati, il divieto per `Includes` e `Verification` di asserire un lato non risolto (ammessa solo la formulazione condizionale), la chiusura obbligatoria via voce in `Open questions` con le slice bloccate oppure spike time-boxed prima della prima slice bloccata, più il controllo di completamento «nessuna slice asserisce un lato di un conflitto elencato nello sweep».
- **In the other report:** bullet 5 chiede «una ricerca sistematica di affermazioni incompatibili … ogni conflitto deve diventare domanda o spike prima delle slice coinvolte»; il bullet 7 aggiunge al validatore il controllo sulle «domande dichiarate ma ignorate dalle slice».
- **Common improvement:** rendere la rilevazione dei conflitti tra fonti un passo sistematico e obbligatorio, e forzare ogni conflitto in una domanda aperta o in uno spike collocato prima delle slice coinvolte.
- **Differences:** questo report è operativo (citazioni `file:riga` per entrambi i lati, divieto esplicito di asserzione dentro `Includes`/`Verification`, formulazione condizionale ammessa, criterio di completamento). L'altro report aggiunge la direzione reciproca qui assente: verificare che le domande dichiarate siano effettivamente referenziate dalle slice.

### `Decisioni mai prese distinte dalle decisioni prese`

- **In this report:** §2 rileva che il modello LLM è trattato come deciso («LLM cheap a output strutturato») pur non essendo fissato dalle fonti, e che le decisioni aperte intercettate sono due su quattro. Propone di separare in passo 1 e passo 5 la categoria «decisioni mai prese» da quella delle contraddizioni, la regola di completezza per cui ogni adapter, provider o modello esterno invocato da una slice `NOW` è scelto nelle fonti con citazione oppure compare in `Open questions` con la slice che blocca, il test discriminante «un aggettivo qualificante non è una scelta», e il relativo controllo di completamento.
- **In the other report:** bullet 5 include le «decisioni ancora placeholder» nella stessa ricerca sistematica dei conflitti, con la stessa chiusura (domanda o spike prima delle slice coinvolte).
- **Common improvement:** i placeholder decisionali vanno rilevati sistematicamente e convertiti in domande esplicite legate alle slice che bloccano.
- **Differences:** qui la categoria è formalmente separata dalle contraddizioni e dotata di un test discriminante e di una regola di copertura su ogni dipendenza esterna in `NOW`; l'altro report la fonde nel medesimo bullet dei conflitti, senza test né copertura.

### `Pipeline o adapter condiviso con un solo proprietario`

- **In this report:** §5 osserva che la slice 8 apre la pipeline media mentre l'acquisizione testuale è ancora aperta, e che la slice 12 non dichiara né owner né esclusione per le foto sul percorso da testo incollato. Propone la regola d'ordine «una slice che apre una pipeline o un adapter condiviso da più percorsi deve seguire tutte le slice `NOW` che le forniscono input, e deve essere l'unica proprietaria di quell'adapter», il nuovo anti-pattern sull'apertura anticipata o duplicata, e l'estensione del controllo di ownership a «ogni combinazione produttore × pipeline condivisa».
- **In the other report:** bullet 6 introduce un ledger interno «fuori dalla slice» contro gli «adapter anticipati»; il bullet 2 la matrice `comportamento → tema → orizzonte → slice proprietaria` che blocca fusioni, duplicazioni e scope leakage; il bullet 7 il controllo automatico sugli «adapter duplicati».
- **Common improvement:** un solo proprietario per adapter o comportamento condiviso, con un meccanismo che blocca aperture anticipate e duplicate.
- **Differences:** qui è presente il vincolo d'ordine (la pipeline segue tutte le slice `NOW` che la alimentano) e la copertura produttore × pipeline; l'altro report propone il meccanismo generico — matrice di tracciabilità, ledger, controllo automatico sui duplicati — senza il vincolo produttori-prima.

### `Ammissione in NOW subordinata a una domanda delle fonti`

- **In this report:** §6 rileva che la slice 10 porta in `NOW` la creazione di ricettari, che le fonti non richiedono. Propone che ogni slice `NOW` citi la frase delle fonti che ne richiede il comportamento, il test di default sugli orizzonti (`NOW` richiede una richiesta esplicita, `LATER` un trigger, `OUT-OF-SCOPE` un'esclusione dichiarata) e il controllo «ogni slice `NOW` ha una citazione di fonte che la richiede».
- **In the other report:** bullet 6 chiede il ledger che impedisce «funzionalità `LATER` introdotte in `NOW`»; il bullet 2 include l'orizzonte nella matrice di tracciabilità che blocca lo scope leakage.
- **Common improvement:** un filtro meccanico che impedisce a capability non richieste o rinviabili di entrare in `NOW`.
- **Differences:** qui il filtro è positivo (citazione di fonte obbligatoria per ogni slice `NOW`) e codifica il criterio di ammissione dei tre orizzonti; l'altro report lavora in negativo, intercettando la fuga di scope senza richiedere alcuna citazione.

### `Continuità del tema: nessun tema riaperto dopo temi indipendenti`

- **In this report:** §4 osserva che la slice 6 nomina il fallimento da paywall mentre la via di fuga (import da testo incollato) arriva alla slice 12, sei slice dopo, con temi estranei in mezzo, e che la slice 12 stessa dichiara il legame. Propone di dichiarare la precedenza della regola sulla via di recupero su breadth-before-depth, il test operativo «se una slice nomina un modo di fallimento nella propria `Verification` e un'altra slice `NOW` ne è il rimedio, il rimedio precede l'inizio di un nuovo tema», e il relativo controllo di completamento.
- **In the other report:** bullet 3 chiede che «un tema non deve essere riaperto dopo temi indipendenti senza motivazione»; il bullet 7 aggiunge al validatore il controllo sui «temi interrotti».
- **Common improvement:** vietare l'interposizione di temi estranei tra l'apertura e la chiusura di un tema, e renderlo verificabile.
- **Differences:** qui la regola è derivata dall'accoppiamento fallimento/rimedio e risolve esplicitamente il conflitto di priorità tra due regole già presenti nello skill; l'altro report enuncia la continuità del tema in forma generica, con la clausola di scampo «senza motivazione», e ne propone l'automazione.

### `Audit esplicito di split quando una slice porta preoccupazioni indipendenti`

- **In this report:** §7 rileva che la slice 2 accorpa schema, indice HNSW, resolver di scope, servizio di embedding, corpus bilingue e comando diagnostico, rendendo non attribuibile un eventuale fallimento. Propone che un enabler che tocca più di una incertezza materiale vada diviso, che la prima slice che persiste dati stabilisca persistenza e resolver prima di qualunque enabler di motore, il criterio di attribuzione «se una sola slice può fallire per due cause indipendenti che cambiano decisioni diverse, va divisa», e il controllo «nessun enabler valida più di una incertezza materiale».
- **In the other report:** bullet 1 rende obbligatorio «un audit interno split/merge per ogni coppia di capability, registrando quali possono essere rinviate indipendentemente».
- **Common improvement:** forzare una decisione di split/merge esplicita e registrata invece dell'accorpamento implicito, usando l'indipendenza come criterio.
- **Differences:** qui il criterio è l'attribuzione del rischio (una sola incertezza materiale per enabler, cause di fallimento indipendenti); nell'altro report è la rinviabilità indipendente, valutata a coppie su tutte le capability. I due test sono compatibili e complementari.

### `Regole rese meccanicamente verificabili`

- **In this report:** la diagnosi ricorrente è che le regole esistenti non sono controllabili — «la regola dello skill esiste ma non è numerabile … "further" non dice quante», «lo skill le offre già come alternative … ma non chiede la prova che una delle due sia stata scelta». Il rimedio è sistematico: ogni sezione chiude aggiungendo un controllo al criterio di completamento del passo corrispondente, cioè un gate per l'autore del piano.
- **In the other report:** bullet 7 chiede di estendere il validatore con controlli semantici configurabili, cioè un gate strumentale esterno al testo dello skill.
- **Common improvement:** la guida esistente fallisce perché nulla ne verifica l'applicazione; servono regole esplicite e controllabili.
- **Differences:** qui i controlli vivono nei criteri di completamento dei passi dello skill e sono rivolti a chi scrive il piano; nell'altro report vivono in un validatore configurabile e sono rivolti allo strumento. Le due sedi sono compatibili e possono condividere lo stesso insieme di regole.

## Improvements unique to this report

### `Soglia contabile per il differimento dell'identità e audience dichiarata per slice`

- **Improvement:** §3 rileva che l'accesso Google arriva alla slice 9, dopo quattro slice di prodotto accettate su uno scope configurato, coperte solo da una riga nei `Cross-functional concerns`, mentre ogni `Outcome` parla di «un utente» che non esiste ancora. Propone che l'identità arrivi prima della seconda slice di prodotto che consegna comportamento a un utente finale, con differimento ulteriore giustificato una sola volta in `Ordering criteria`, che ogni slice `NOW` anteriore all'identità dichiari audience e ambiente dentro la slice riscrivendo «un utente» in termini di sviluppatore o tester, e il controllo di completamento corrispondente al passo 4.
- **Difference from the other report:** l'altro report non tratta né la collocazione dell'identità né l'audience delle slice; i suoi audit di ordinamento riguardano continuità dei temi e adiacenza enabler/validatore, non la soglia oltre la quale un ambiente configurato smette di reggere l'accettazione.

### `Copertura nella slice di rilascio di ogni vincolo operativo dichiarato nelle fonti`

- **Improvement:** §8 rileva che la slice 13 copre ambiente, segreti, credenziali OAuth, migrazioni, scale-to-zero, cold start e costo, ma omette backup con prova di ripristino (unico datastore, nessuna replica) e tetto di spesa con allarme su LLM ed embedding rispetto al costo target dichiarato. Propone che la slice `(Release: delivery)` copra ogni vincolo operativo dichiarato nelle fonti — durabilità, tetto di spesa con allarme, ripristino di stato non ricostruibile — con citazione della fonte per ogni voce, e il controllo «ogni vincolo operativo dichiarato nelle fonti ha una voce nella slice di rilascio o un'esclusione esplicita».
- **Difference from the other report:** l'altro report non contiene alcun elemento su rilascio, prontezza operativa o vincoli non funzionali dichiarati dalle fonti.

### `Verification su ripetizione, idempotenza e residui, e set di valutazione versionati per i claim di qualità`

- **Improvement:** §9 identifica come scoperti l'idempotenza dell'accettazione di un invito, i retry che duplicano ricetta o oggetti dopo un salvataggio parziale, gli oggetti orfani su upload interrotto, e il fatto che il rischio esistenziale sul ranking cross-lingua sia verificato con query ad hoc. Propone di estendere l'elenco dei modi da nominare con ripetizione, idempotenza e residui per ogni slice che scrive tramite un adapter esterno o crea appartenenze, di richiedere un set di valutazione versionato con casi positivi e negativi quando un `Learning / risk` afferma qualità, pertinenza o accuratezza, e di mantenere almeno un letterale concreto per ogni slice rischiosa.
- **Difference from the other report:** l'altro report non propone regole sul contenuto delle `Verification`. La sua unica indicazione adiacente — ridurre il dettaglio implementativo pubblicato — privilegia esplicitamente «evidenza capace di cambiare una decisione», quindi punta al dettaglio prescrittivo negli `Includes` e non entra in conflitto con la concretezza richiesta qui nelle verifiche.

### `Una voce per bullet negli orizzonti e test di separazione LATER / OUT-OF-SCOPE`

- **Improvement:** §10 rileva che `OUT-OF-SCOPE` accorpa quattro esclusioni eterogenee in un solo bullet con una motivazione unica, e che vi finisce la ricerca cross-ricettario, che meriterebbe `LATER` con trigger. Propone una voce per bullet in `LATER` e `OUT-OF-SCOPE`, ciascuna con motivazione o trigger propri, il test di separazione bidirezionale (una voce con trigger plausibile appartiene a `LATER`; una voce `OUT-OF-SCOPE` che contiene un trigger è mal classificata) e il controllo di completamento corrispondente.
- **Difference from the other report:** l'altro report tocca gli orizzonti solo come tracciabilità e prevenzione dello scope leakage, senza mai affrontare la granularità delle voci né il confine tra rinvio condizionato ed esclusione definitiva.

## Improvements present only in the other report

### `Adiacenza tra enabler e suo validatore`

- **Other report:** bullet 3 chiede un «audit di adiacenza: enabler e validatore devono restare vicini».
- **Missing from this report:** nessuna sezione impone un vincolo di prossimità tra la slice che introduce un enabler e la slice che ne valida il valore; §7 riguarda la divisione di un enabler sovraccarico, non la distanza tra i due.

### `Distinzione esplicita tra primo enabler tecnico e prima validazione di prodotto per tema`

- **Other report:** bullet 4 chiede di rendere esplicita la distinzione per ciascun tema, rafforzata dal controllo di validatore «first validation inesistente» (bullet 7).
- **Missing from this report:** la proprietà è citata solo tra i punti di forza da non perdere («temi tracciati al numero della slice che li valida per primo»), senza diventare un cambiamento allo skill né un controllo.

### `Riduzione del dettaglio implementativo pubblicato`

- **Other report:** bullet 8 chiede di privilegiare outcome, rischio, confini ed evidenza capace di cambiare una decisione, riducendo il dettaglio implementativo nel piano pubblicato.
- **Missing from this report:** nessuna sezione affronta il volume di dettaglio implementativo del piano emesso; le prescrizioni qui riguardano cosa deve essere presente, mai cosa vada tolto.

## Contradictory improvements

- None identified.

## Summary

- **Shared:** 7
- **Unique to this report:** 4
- **Only in the other report:** 3
- **Contradictions:** 0
