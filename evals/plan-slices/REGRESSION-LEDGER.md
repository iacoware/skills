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

- **Prossimo passo — verificare R-002…R-008 su `PLAN-CC-CON-5.md` e `PLAN-CX-CON-5.md`.** I due
  candidati sono stati generati subito dopo `9aa2586` (commit `515e0a3`, 2026-08-04 11:57): sono il
  primo ciclo posteriore a tutte e cinque le modifiche e nessuno dei due è stato valutato. Il
  controllo è offline e non costa chiamate.
  - Un'affermazione regge solo se regge su **entrambi** i piani. I due candidati vengono da modelli
    diversi: una violazione su uno solo smentisce comunque la previsione, perché l'affermazione è
    sullo skill, non sul modello che lo esegue.
  - Conviene partire dai membri leggibili senza le fonti — il secondo membro di R-002 e di R-004,
    l'interposizione di temi in R-005, l'unicità del proprietario in R-006, l'esclusione degli
    `Enabler` in R-008 — e affrontare dopo ciò che richiede il confronto con le fonti: R-003, il
    primo membro di R-004 e R-007.
  - Ogni riga controllata riceve la data in `Ultimo controllo` e lo `Stato` `tiene` o `regredita`.
    Una riga `regredita` resta, con la citazione del punto del piano che l'ha smentita.
  - Se un'affermazione risulta non decidibile sul piano — non falsa, ma non giudicabile da ciò che il
    piano pubblica — è la formulazione a essere sbagliata: si riscrive la riga e si annota il motivo,
    perché è lo stesso difetto già registrato per i miglioramenti confinati nel ragionamento.
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
