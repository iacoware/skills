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
- `Stato`: `da verificare` finché non c'è un ciclo successivo alla modifica; `tiene` se l'ultimo ciclo
  l'ha confermata; `regredita` se un ciclo l'ha smentita, con la data.
- Una riga `regredita` non si cancella: si aggiunge la riga della correzione e si lasciano entrambe.
  La sequenza di regressioni sullo stesso tema è il segnale che la regola è formulata male, non che
  va riscritta ancora.

## Registro

| ID | Commit `SKILL.md` | Origine | Affermazione verificabile | Verifica | Ultimo controllo | Stato |
|---|---|---|---|---|---|---|
| R-001 | `2c89e7f` | `giudizio` — `NOTES.md` § *Confine di scope vs identità* | Il piano colloca l'identità dopo il differenziatore **e** dichiara in `Cross-functional concerns` la giunzione unica da cui si risolve lo scope corrente. | lettura, automatizzabile in parte | — | da verificare |
| R-002 | `d977043` | `intersezione` — `REVIEW` CON-4 § *Sweep sistematico delle contraddizioni* ≡ *Explicit handling of source contradictions* | Nessuna bullet `Includes` o `Verification` afferma in forma non condizionale un lato di una contraddizione fra le fonti, e ogni voce di `Open questions` nomina le slice `NOW` che blocca. | lettura per il primo membro; il secondo è automatizzabile (ogni voce di `Open questions` cita almeno un numero di slice `NOW` esistente) | 2026-08-04 | regredita su `CC` |
| R-003 | `d977043` | `intersezione` — `REVIEW` CON-4 § *Decisioni mai prese distinte dalle decisioni prese* ≡ *Explicit handling of undecided choices* | Ogni provider, modello, servizio o adapter esterno nominato da una slice `NOW` è selezionato da una fonte citabile oppure compare in `Open questions` con la slice che blocca; un aggettivo qualificante — `cheap`, `multilingual`, `managed` — non conta come scelta. | lettura: l'inventario delle dipendenze esterne richiede il confronto con le fonti | 2026-08-04 | tiene |
| R-004 | `d977043` | `intersezione` — `REVIEW` CON-4 § *Ammissione in NOW subordinata a una domanda delle fonti* ≡ *Trace scope and horizon ownership* | Nessuna slice `NOW` consegna un comportamento che le fonti non richiedono; ogni voce `LATER` dichiara un `Promotion trigger` e ogni voce `OUT-OF-SCOPE` una razionale di esclusione. | lettura per il primo membro — lo skill colloca la tracciatura nel ragionamento, non nel piano; il secondo è automatizzabile sulla struttura del template | 2026-08-04 | tiene |
| R-005 | `d977043`, `9aa2586` | `intersezione` — `REVIEW` CON-4 § *Continuità del tema* ≡ *Keep a theme and its recovery path contiguous* | Se una slice `NOW` nomina un modo di fallimento nella propria `Verification` e un'altra slice `NOW` ne è il rimedio, nessuna slice di un tema diverso è collocata fra le due. | lettura per l'accoppiamento fallimento→rimedio; l'interposizione di temi è automatizzabile sull'annotazione `*(Theme: X)*` delle slice | 2026-08-04 | tiene |
| R-006 | `d977043`, `9aa2586` | `intersezione` — `REVIEW` CON-4 § *Pipeline o adapter condiviso con un solo proprietario* ≡ *Open shared pipelines and adapters once, after their producers* | Una pipeline o un adapter condiviso da più percorsi compare negli `Includes` di una sola slice `NOW`, e quella slice segue ogni slice `NOW` che le fornisce input. | lettura per l'identificazione dei produttori; l'unicità del proprietario è automatizzabile in parte (stesso adapter nominato negli `Includes` di due slice) | 2026-08-04 | regredita su `CX` |
| R-007 | `d977043` | `intersezione` — `REVIEW` CON-4 § *Audit esplicito di split* ≡ *Split capabilities and enablers with independent risks* | Nessuna slice `Enabler` valida più di una incertezza materiale: la sua `Verification` non può fallire per due cause indipendenti che cambierebbero decisioni diverse. | lettura: il verdetto di split per coppia vive nel ledger non pubblicato, sul piano resta osservabile solo l'esito | 2026-08-04 (tentato) | da verificare — non decidibile |
| R-008 | `9aa2586` | `intersezione` — `REVIEW` CON-4 § *Use repeatable, decision-changing verification*, parte «each theme has a first validation» | La `First validation` di ogni tema punta a una slice `NOW` non annotata `Enabler`, il cui `Outcome` copre l'intero desired outcome del tema; l'eccezione vale solo se il desired outcome del tema è dichiaratamente per uno sviluppatore. | validator per l'esistenza del riferimento; automatizzabile l'esclusione degli `Enabler`; lettura per la copertura dell'outcome | 2026-08-04 | regredita su `CX` |

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
- **R-006 — `PLAN-CX-CON-5.md`, slice 2 `Includes` contro slice 5–8.** La pipeline di embedding
  sulle scritture apre alla slice 2 («Ricette normalizzate controllate attraversano il percorso reale
  di embedding … e persistenza pgvector») e riappare negli `Includes` della slice 5 («Embedding
  rigenerato su creazione e modifica»), della 6 («seguito dall'embedding») e della 7 («Stesso
  salvataggio immediato, embedding»). Il secondo membro cade in modo indipendente
  dall'interpretazione di «proprietario»: le slice che forniscono ricette all'indice — 5 manuale, 6
  URL, 7 incolla, 8 fallback — seguono tutte la slice che apre la pipeline, che quindi non segue i
  propri produttori. Il piano `CC` ha la forma prevista: produttore alla slice 2, pipeline alla
  slice 3.
- **R-008 — `PLAN-CX-CON-5.md`, tabella `Themes`.** Tre voci smentiscono la riga, su entrambi i
  membri. Riga A: la `First validation` è «2. Indicizzazione multilingue osservabile», slice
  annotata `*(Enabler: ricerca semantica)*`, mentre il desired outcome del tema — «Trovare nel
  ricettario corrente ricette pertinenti anche tra lingue diverse» — non è dichiarato per uno
  sviluppatore, quindi l'eccezione non si applica. Riga D: desired outcome «cover controllabile»
  contro l'`Outcome` della slice 9, «una cover stabile senza hotlink fragile» — la scelta della cover
  arriva solo alla slice 11. Riga C: desired outcome «da input manuale, URL o testo» contro
  l'`Outcome` della slice 5, che copre il solo inserimento manuale. Il piano `CC` regge su tutte e
  sei le righe.

### Formulazioni da riscrivere — emerse nel ciclo CON-5

Righe che il ciclo non ha potuto decidere, o che ha deciso solo scegliendo fra due letture. Restano
al loro posto: il difetto è nella formulazione, non nel piano, e riscriverle senza un secondo caso
significherebbe adattarle a questi due candidati.

- **R-007 — non decidibile, resta `da verificare`.** Il secondo membro chiede quali *decisioni*
  cambierebbero se la `Verification` di un `Enabler` fallisse, ma il piano pubblica la mappa
  decisione↔slice solo dove esiste un `Decision checkpoint`. Per gli `Enabler` di consegna non ne
  esiste nessuno — `CC` apre i checkpoint alla slice 3, `CX` alla slice 2 — e sono proprio quelli
  dove il dubbio si pone: la seconda bullet di `Verification` della slice 1 di `CX` («Arresto,
  risveglio da `suspend`, nuova connessione e redeploy preservano il round trip») può fallire per il
  modo di sospensione Fly o per il pooling del provider Postgres, che sono decisioni distinte —
  `LATER` § *Fly sempre caldo* e `Non-product work` § *Selezione Postgres*. Attribuire il
  fallimento all'una o all'altra richiede di ricostruire la mappa, non di leggerla: il verdetto
  sarebbe inventato. Sugli `Enabler` semantici — `CC` slice 3, `CX` slice 2 — la riga regge, perché
  lì il checkpoint pubblica la decisione.
- **R-002, secondo membro — non falsificabile su un piano senza `Open questions`.** `CX` non ha
  quella sezione: le scelte non prese stanno in `Non-product work`, ognuna con la slice che blocca
  («prima della slice 1», «prima della slice 2»…). Il membro risulta quindi vero a vuoto, e un piano
  può soddisfarlo omettendo la sezione. Il verdetto della riga viene dal primo membro.
- **R-003 — decisa sulla sostanza, non sulla lettera.** La disgiunzione nomina `Open questions` come
  unica sede alternativa a una fonte citabile. Su `CX` provider Postgres, percorso di embedding e
  modello di estrazione sono dichiarati non decisi in `Non-product work`, con la slice che
  bloccano: stessa informazione, sezione diversa. La riga è `tiene` perché nessuna slice `NOW` di
  nessuno dei due piani nomina una dipendenza esterna né scelta da una fonte né dichiarata aperta;
  letta alla lettera sarebbe `regredita` su `CX` per il solo nome della sezione.

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

- **R-001, mai controllata.** Nasce da `2c89e7f`, precedente ai cinque commit, e il ciclo CON-5 non
  l'ha inclusa. Va verificata sugli stessi due piani, con lo stesso criterio: regge solo se regge su
  entrambi.
- **Correzioni per R-002, R-006 e R-008.** Il registro prescrive che a una riga `regredita` segua la
  riga della correzione, e che nessuna delle due si cancelli. Le tre righe restano scoperte finché
  una modifica dello `SKILL.md` non le riapre: la sessione CON-5 misurava, non correggeva.
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
