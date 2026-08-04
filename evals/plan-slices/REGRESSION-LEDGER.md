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
- `Origine` si apre con il modo in cui la modifica è stata decisa: `intersezione` se i due modelli
  proponevano lo stesso miglioramento, `giudizio` se un umano ha ritrovato il difetto sul piano
  generato e ha applicato un punto sollevato da un solo modello o da nessuno. I due modi sbagliano
  in modo diverso — il primo manca cose, il secondo può applicarne di false — e distinguerli è
  l'unico modo per accorgersene a posteriori.
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
| R-002 | `d977043` | `intersezione` — `REVIEW` CON-4 § *Sweep sistematico delle contraddizioni* ≡ *Explicit handling of source contradictions* | Nessuna bullet `Includes` o `Verification` afferma in forma non condizionale un lato di un conflitto fra le fonti — quelli elencati in `Known conflicts` del brief, più quelli dimostrabili citando due fonti in disaccordo — e ogni scelta che il piano dichiara aperta nomina le slice `NOW` che blocca, in qualunque sezione la dichiari. | lettura per il primo membro; il secondo è automatizzabile sulla sezione delle scelte aperte, qualunque sia il suo titolo (ogni voce cita almeno un numero di slice `NOW` esistente) | 2026-08-04 | CON-5 · `CC`+`CX` · brief+fonti | regredita su `CC` |
| R-003 | `d977043` | `intersezione` — `REVIEW` CON-4 § *Decisioni mai prese distinte dalle decisioni prese* ≡ *Explicit handling of undecided choices* | Nessuna slice `NOW` dipende da una scelta esterna — provider, modello, servizio o adapter — che non sia presa da una fonte citabile, o presa dal piano fra le alternative che il brief dichiara accettabili, o dichiarata aperta con la slice che blocca, in qualunque sezione la dichiari; un aggettivo qualificante — `cheap`, `multilingual`, `managed` — non conta come scelta. | lettura: l'inventario delle dipendenze esterne richiede il confronto con le fonti e con le `Accepted alternatives` del brief | 2026-08-04 | CON-5 · `CC`+`CX` · brief+fonti | tiene |
| R-004 | `d977043` | `intersezione` — `REVIEW` CON-4 § *Ammissione in NOW subordinata a una domanda delle fonti* ≡ *Trace scope and horizon ownership* | Nessuna slice `NOW` consegna un comportamento che le fonti non richiedono; ogni voce `LATER` dichiara un `Promotion trigger` e ogni voce `OUT-OF-SCOPE` una razionale di esclusione. | lettura per il primo membro — lo skill colloca la tracciatura nel ragionamento, non nel piano; il secondo è automatizzabile sulla struttura del template | 2026-08-04 | CON-5 · `CC`+`CX` · fonti | tiene |
| R-005 | `d977043`, `9aa2586` | `intersezione` — `REVIEW` CON-4 § *Continuità del tema* ≡ *Keep a theme and its recovery path contiguous* | Se una slice `NOW` nomina un modo di fallimento nella propria `Verification` e un'altra slice `NOW` ne è il rimedio, nessuna slice di un tema diverso è collocata fra le due. | lettura per l'accoppiamento fallimento→rimedio; l'interposizione di temi è automatizzabile sull'annotazione `*(Theme: X)*` delle slice | 2026-08-04 | CON-5 · `CC`+`CX` · piani | tiene |
| R-006 | `d977043`, `9aa2586` | `intersezione` — `REVIEW` CON-4 § *Pipeline o adapter condiviso con un solo proprietario* ≡ *Open shared pipelines and adapters once, after their producers* | Una pipeline o un adapter condiviso da più percorsi è aperto negli `Includes` di una sola slice `NOW`; le slice successive che lo riusano lo dichiarano tale. Quella slice segue ogni slice `NOW` che le fornisce input, salvo quando valida input controllati che attraversano il calcolo di produzione e il brief dello scenario ammette la validazione anticipata. | lettura per l'identificazione dei produttori; l'unicità del proprietario è automatizzabile in parte (stesso adapter nominato negli `Includes` di due slice) | 2026-08-04 | CON-5 · `CC`+`CX` · brief+piani | tiene |
| R-007 | `d977043` | `intersezione` — `REVIEW` CON-4 § *Audit esplicito di split* ≡ *Split capabilities and enablers with independent risks* | Nessuna slice `Enabler` valida incertezze su più di un sottosistema: la sua `Verification` non può fallire per cause che, in `Material uncertainties` del brief, appartengono a `Subsystem` diversi. Più voci dello stesso sottosistema sono una incertezza sola, anche quando la risposta invalida la scelta verificata. | lettura: il verdetto di split per coppia vive nel ledger non pubblicato, sul piano resta osservabile solo l'esito; l'elenco delle incertezze, dei sottosistemi e delle decisioni che cambiano lo pubblica il brief | 2026-08-04 | CON-5 · `CC`+`CX` · brief+piani | tiene |
| R-008 | `9aa2586` | `intersezione` — `REVIEW` CON-4 § *Use repeatable, decision-changing verification*, parte «each theme has a first validation» | La `First validation` di ogni tema punta a una slice `NOW` non annotata `Enabler`, il cui `Outcome` copre l'intero desired outcome del tema; l'eccezione vale solo se il desired outcome del tema è dichiaratamente per uno sviluppatore. | validator per l'esistenza del riferimento; automatizzabile l'esclusione degli `Enabler`; lettura per la copertura dell'outcome | 2026-08-04 | CON-5 · `CC`+`CX` · piani | regredita su `CX` |

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

- **Correzioni per R-002 e R-008.** Il registro prescrive che a una riga `regredita` segua la riga
  della correzione, e che nessuna delle due si cancelli. Le due righe restano scoperte finché una
  modifica dello `SKILL.md` non le riapre: la sessione CON-5 misurava, non correggeva.
- **Modifiche dei cinque commit senza riga di registro.** `d88328f` (walking skeleton non cavo),
  `b0d6dc5` (limitazione alle roadmap ad alto livello) e `a06a5cc` (soglia al differimento
  dell'identità) non sono ricostruibili dall'intersezione dei due `REVIEW`: il primo non compare in
  nessuna delle due sezioni `also present`, `a06a5cc` corrisponde a un miglioramento presente in un
  solo report, `b0d6dc5` non ha una corrispondenza verificata. Sono modifiche entrate per giudizio
  su un difetto osservato — `a06a5cc` cita il proprio nel messaggio di commit — e la loro previsione
  va ricostruita da lì, non dai `REVIEW`.
- **Modifiche precedenti a `d88328f`.** Nascono da conversazioni fra umano e agente sui piani
  generati, precedenti al confronto fra modelli: non esiste un artefatto da cui ricostruire una
  previsione. Si registrano solo se un ciclo futuro ne solleva una regressione.
