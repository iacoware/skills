# Consensus cycle CON-5 — report

**Created retroactively on 2026-08-06**, in Fase 1c, as the container for the CON-5 cycle narrative
that until then lived inside `REGRESSION-LEDGER.md`. CON-5 ran on 2026-08-04 and produced no report:
this file is where its narrative now lives, not a reconstruction of a report that once existed.

**CON-5 was a partial cycle.** Generation plus offline reading of the ledger, with no `improve`, no
`review`, no `verdetto` call and no `recidiva`. The counters below therefore have a defined value
only where the partial cycle produced one; the rest is marked `n/a — partial cycle` rather than
filled with a zero that would read as a measurement.

**Language.** This frame is in English, per the project rule of 2026-08-06. The narrative below is
**not translated**: it is the record of what CON-5 decided, written in Italian on 2026-08-04, and
translating a record falsifies it. It is reproduced verbatim from `REGRESSION-LEDGER.md` at `f99449c`,
lines 73–310, with two changes and only two:

1. heading levels promoted from `###` to `##`, this file having no enclosing section;
2. the two paragraphs *«Da cercare al prossimo ciclo, oltre alla riga»* of `R-010` and `R-011`
   removed. They are not narrative — they are instructions for the next `verdetto` — and they moved
   into the `Watch for` cell of their own ledger row. A marker is left where each stood.

## Counters

```
SKILL.md                        383 → 389   (+6)
entries applied                   2
  reformulations                  2   ← 87150d3 and eb926bb both rewrite in place
  additions                       0
new ledger rows                   2   (0 intersection, 0 intersection-theme, 2 judgement)
re-anchored rows                  0   at the time; 2 retroactively on 2026-08-06
absorbed claims                   0   at the time; 2 retroactively on 2026-08-06
active rows                       9 → 11
entries rejected by the gate    n/a — partial cycle, no conformity gate existed
rejected verdicts               n/a — partial cycle, verdicts came from offline human reading
recidiva                        n/a — partial cycle, never run
structural validator            n/a — not run on the two candidates as part of the cycle
```

Reading of the counters, for the record: the cycle applied **two reformulations and zero
additions**, which is the shape `improve` bidirezionale was later built to make reachable from
inside the workflow. The skill still grew by 6 lines — a reformulation is not free — and the ledger
grew by 2 rows on 9. `workflow/RATIONALE.md` § *Il cricchetto* draws the consequence: what entered as
an addition was the ledger row, not the rule.

Line counts verified against git: `87150d3^` 383, `87150d3` 387 (`+7/-3`), `eb926bb` 389 (`+4/-2`).

## What produced the verdicts

Offline human reading of the two generated plans — `recipe-app/results/PLAN-CC-CON-5.md` and
`PLAN-CX-CON-5.md`, both generated after `9aa2586` — against ledger claims written the same day.
Model and effort of the two generations were never recorded; `Measured on` in the ledger says so.

This is the reason CON-5 is not evidence that the detector runs on its own: it is evidence that a
human reading two generated plans against freshly written claims finds real defects.

## Consequences carried into the ledger

- `R-010` and `R-011` were written in the same minute as the commits they verify — the only two
  `ex-ante` rows in the corpus.
- The two `Da cercare al prossimo ciclo` notes became the `Watch for` cells of `R-010` and `R-011`.
- The CON-5 corrections rewrote in place the clauses `R-002` and `R-008` were measuring, and the two
  rows kept pointing at the old commits. Re-anchored to `87150d3` and `eb926bb` on 2026-08-06, then
  **absorbed** the same day: the corrections and the rows they corrected had landed on the same
  clause, so `R-010` took over `R-002`'s first member and `R-011` took over `R-008`'s `Enabler`
  clause and its exception. The overlap CON-5 created — two rows predicting one thing — is closed.
  The uncorrected members stayed as their own rows: `R-002`'s open-choices requirement, and `R-008`'s
  outcome coverage carrying rows C and D of this cycle's regression.

---

## Regressioni rilevate — ciclo CON-5 (2026-08-04)

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

## Formulazioni riscritte — ciclo CON-5 (2026-08-04)

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

## Chiusura del ciclo CON-5 — righe rimaste (2026-08-04)

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

## Correzioni applicate dopo il ciclo CON-5 (2026-08-04)

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
  *(The note «Da cercare al prossimo ciclo, oltre alla riga» that stood here is not narrative: it is
  an instruction for the next `verdetto`, and it moved into the `Watch for` cell of `R-010` in
  `REGRESSION-LEDGER.md` on 2026-08-06.)*

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
  *(The note «Da cercare al prossimo ciclo, oltre alla riga» that stood here is not narrative: it is
  an instruction for the next `verdetto`, and it moved into the `Watch for` cell of `R-011` in
  `REGRESSION-LEDGER.md` on 2026-08-06.)*

## Diagnosi decise dopo il ciclo CON-5 (2026-08-04)

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

## Difetti degli artefatti mai registrati (2026-08-04)

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
