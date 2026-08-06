# Ciclo di consenso — piano di implementazione

Piano per separare il ciclo di consenso dal grading system abbandonato e automatizzarlo. Ogni fase è
pensata per una **sessione fredda separata**: dichiara le proprie precondizioni, le attività, come si
verifica e cosa produce. Una fase non presume il contesto conversazionale in cui la precedente è
stata svolta.

Lo strumento e la sua ragione stanno in `CONSENSUS-WORKFLOW.md`; qui c'è solo il lavoro da fare.

## Decisioni già prese

Non si ridiscutono all'inizio di ogni sessione.

- L'obiettivo si regge su **due meccanismi disgiunti**: il registro rileva il peggioramento ex-post
  sulle dimensioni che copre; l'intersezione `improve` + `review` previene ex-ante l'ingresso di
  regole false. Una falsificazione dell'ipotesi sull'intersezione **non fa cadere l'obiettivo**.
- Il ciclo attivo si chiama **consenso**. Le fasi sono **quattro**: `improve`, `review`, `verdetto`,
  `recidiva`. `ledger` indica solo il registro, mai una fase.
- Il grading system è **abbandonato dal 2026-08-06**, non sospeso. Non torna. Il codice resta in git e
  non è mantenuto. **Non si spende tempo a curarne i documenti interni.**
- Dal ciclo CON-6 i payload di `improve` **e di `review`** sono **ciechi e simmetrici**.
- Il ciclo è un **falsificatore, non un confermatore**. Lo stato del registro è `non smentita ×k`.
  Non si aumenta il numero di generazioni per lato: la leva è il tempo, non il campione.
- **`improve` è bidirezionale**, con i campi `Regola esistente che non ha impedito il difetto` e
  `Costo`, e con la regola dura: se una clausola esistente è nominata, il rimedio di default è
  riformularla, e aggiungere righe richiede una ragione scritta.
- **Il contratto di conformità è un template più un validator**, non prosa dentro un prompt: un
  contratto in prosa è ciò che entrambi i lati hanno ignorato in CON-4. La specificità è una **forma**
  che il generico non riempie, non un giudizio con una soglia. **Niente soglie.**
- Una voce non conforme si **scarta e si registra**, con **un solo tentativo**. Il documento non si
  rigenera mai. Un errore di trasporto è un ritentativo della *chiamata*, non del documento. Un lato
  a zero voci conformi non blocca il ciclo.
- **`Origine` ha quattro valori**: `intersezione`, `intersezione-tema`, `giudizio`, `potatura`.
  **I nomi canonici sono inglesi** dal 2026-08-06, perché li scrivono il registro migrato, i prompt e
  il validator: `intersection`, `intersection-theme`, `judgement`, `pruning`. Stessa cosa per
  `Verifica`: `validator` e `reading`. I termini italiani di questo piano e di
  `CONSENSUS-WORKFLOW.md` restano leggibili finché la Fase 0b non li converte, e la mappa fra i due
  insiemi è dichiarata nelle regole d'uso del registro. Prompt e validator non emettono mai gli
  italiani.
- **Una voce che riformula una clausola coperta ri-ancora le righe che la coprono; le supersede solo
  se le subsume.** Due regole, non una, perché **le righe quantificano su un piano generato, non sul
  testo dello skill** — è il criterio con cui il registro è stato scritto (`0273a73`: *«each stated
  over a generated plan rather than over the skill text»*). Ne discende che una riformulazione **non
  falsifica** la riga e non ne rende indecidibile l'affermazione: rompe solo l'attribuzione.
  - **Automatico — ri-ancoraggio.** La riga prende il commit nuovo in `Commit` e `Misurato su`, e il
    contatore va a **`non smentita ×0`**: `×k` conta cicli contro un testo, e il testo è cambiato.
    Nessuna riscrittura dell'affermazione, che resta valida e decidibile.
    **Vale anche per una riga `regredita`**, e a maggior ragione: la smentita era contro un testo che
    non esiste più. La riga va a `×0` e la smentita resta scritta nella cella di stato, con il commit
    contro cui era stata misurata — deciso il 2026-08-06 migrando `R-002` e `R-008`, che erano
    entrambe in questo caso. Perderla azzererebbe il segnale che il registro dichiara portante: *«la
    sequenza di regressioni sullo stesso tema è il segnale che la regola è formulata male»*.
    **Quando la riformulazione tocca un solo membro, `Commit` porta entrambi i commit con il membro
    che ciascuno possiede**: di `R-002` il secondo membro vive ancora su `d977043`.
  - **Umano, nel veto — superamento.** Solo quando l'affermazione nuova **subsume** quella vecchia i
    verdetti smettono di essere indipendenti e tenerle entrambe sovrastima l'evidenza: è il caso
    `R-010` ⊂ `R-002` m1 e `R-011` ⊂ prima clausola di `R-008`. La riga vecchia passa a **`superata
    da R-NNN`**, che **non è una smentita** ed **esce definitivamente** dall'insieme verificato, a
    differenza di una dormiente che torna; la nuova eredita la cella `Da sorvegliare` e le due
    portano `Supersedes` / `Superseded by`. **Sono una colonna sola, `Supersession`**, deciso il
    2026-08-06: la relazione ha due versi e nessuna riga ne porta due nello stesso verso, quindi due
    colonne quasi sempre vuote dicono meno di una. Il file cresce, il costo del `verdetto` no: una
    entra e una esce. La subsunzione fra due affermazioni non si chiede a un modello — il report
    pubblica le **coppie candidate**, decide il veto.
  Le altre due opzioni restano dominate, e la provenienza a posteriori rafforza il verdetto.
  **Riscrivere l'affermazione sul posto** è churn: l'affermazione non è diventata falsa, solo il testo
  sotto è cambiato; e dove va davvero riscritta, `k` andrebbe azzerato comunque, quindi è il
  superamento senza la storia. **Mandare la voce all'elenco umano** dice chi decide, non cosa succede
  alla riga, e lascia indeterminato il campo del template che la domanda doveva sbloccare; misurato su
  `87150d3`, che era già un commit umano deciso a mano, l'esito è esattamente lo stato di oggi —
  `R-002` che punta a `d977043`, testo morto, senza link in avanti.
- **Una voce vale `intersezione` o `intersezione-tema` solo se entrambi i `REVIEW` la classificano
  condivisa.** Classificazione unilaterale → `giudizio`, e nessuna applicazione automatica.
- **Il workflow applica al working tree e non committa mai.** Applica solo ciò che il filtro
  licenzia. Una voce = un hunk di `SKILL.md` + una riga di registro, stesso id, riga con
  `Commit: (pending)`. Il veto umano legge i **contatori in testa al report**, poi `git diff`.
- **`recidiva` è una chiamata sola**, modello fisso `claude-opus-5`, e produce l'**elenco delle
  coppie** `voce improve → riga | nessuna`, non uno scalare. Controargomento ed eventi di inversione
  sono in `CONSENSUS-WORKFLOW.md` § *Perché `recidiva` è una sola chiamata*.
- **Dormienza a `non smentita ×3`**, verifica 1 ciclo su 3, risveglio immediato da `recidiva`.
  Sostituisce il pensionamento, che era rinviato senza trigger osservabile.
- I prompt escono da `PROMPTS.md` e diventano l'unica sorgente sotto `prompts/`; `PROMPTS.md` resta
  scratchpad umano senza valore normativo.
- `support/AGENT-PLAN-MAP.md` tiene la mappa alias → piano → generatore ed è escluso da ogni payload.
- `CON-N` resta il contatore di ciclo negli artefatti; non si rinominano artefatti storici. **CON-5
  non si riusa.** Il prossimo ciclo è **CON-6**.
- **Modelli ed effort: `gpt-5.6-sol` e `claude-opus-5`, entrambi a `high` in CON-6.** `medium` è un
  confine di strumento isolato in **CON-7**: cambiarlo in CON-6 confonderebbe la variabile testata —
  la specificità degli `IMPROVEMENT` — con una scelta di costo indipendente.
- **La revisione di `EVALUATION-BRIEF.md` sta dopo CON-6**, per la stessa ragione: è l'autorità contro
  cui si decidono sette righe su undici.
- **L'inglese è la lingua del progetto dal 2026-08-06.** Le fonti in `recipe-app/sources/` e gli
  artefatti storici — `PLAN-*`, `IMPROVEMENT`, `REVIEW`, report — **non si convertono mai**.
- Un confine di strumento **si attraversa una volta sola, deliberatamente, e si registra.**
- La decisione su cosa applicare allo `SKILL.md` resta umana in ogni fase, in forma di veto.
- **Le 15 unità di calibrazione già pagate non vanno conservate.** I 30 file sono tracciati in git.

## Fase 0a — L'inglese è la lingua del progetto

**Precondizioni:** nessuna. **Chiamate provider:** zero. **Va per prima.**

Solo la decisione e la regola. La conversione dei documenti esistenti è Fase 0b e non blocca niente;
separarle è ciò che evita di scrivere in italiano tutto ciò che nasce dalla Fase 0 in poi.

- [ ] Dichiarare in `CONSENSUS-WORKFLOW.md` e in `evals/plan-slices/README.md` che **ogni artefatto
  nuovo nasce in inglese**: prompt, template, validator, report, righe di registro, commit.
- [ ] Dichiarare le **due esclusioni permanenti**, con la ragione:
  - `recipe-app/sources/` — convertirle è un **nuovo scenario**, non una traduzione. Invaliderebbe i
    cinque piani, le righe misurate su di essi e le citazioni del brief, che puntano a titoli di
    sezione italiani (`sources/goal.md`, "Vincoli e scala").
  - `PLAN-*`, `*.IMPROVEMENT.md`, `*.REVIEW.md` e i report già prodotti — sono il record di ciò che è
    stato generato. Tradurli è falsificarlo.
- [ ] Registrare che `EVALUATION-BRIEF.md` è già in inglese e che i titoli di sezione italiani che
  contiene sono **puntatori alle fonti**, non prosa da tradurre. `SKILL.md` è già in inglese.

**Verifica:** la regola e le due esclusioni sono scritte in entrambi i documenti.

## Fase 0 — Separazione dei due strumenti

**Precondizioni:** Fase 0a. **Chiamate provider:** zero.

L'ambizione di questa fase è stata **ridotta** il 2026-08-06: la versione precedente prescriveva di
riscrivere internamente `GRADING-IMPROVEMENTS-PLAN.md` (52 KB). Con il grading abbandonato quella è
manutenzione di un documento morto e non si fa.

- [x] Rinominare `EVAL-WORKFLOW.md` in `GRADING-EVAL-WORKFLOW.md` e seguire i riferimenti — commit
  `570e929`.
- [x] Creare `CONSENSUS-WORKFLOW.md` estraendo dal `Riesame del 2026-08-04` obiettivo, diagnosi,
  ciclo, buco e registro, gate e limiti.
- [x] Riscrivere `CONSENSUS-WORKFLOW.md` sull'esito della sessione di grilling del 2026-08-06:
  obiettivo asimmetrico, stato dell'evidenza, rischio di non-conformità, cricchetto misurato,
  confini di strumento, lapide del grading.
- [x] Seconda riscrittura, grilling del 2026-08-06: separazione delle due tesi, quattro fasi,
  contratto template + validator, `intersezione-tema`, dormienza, `review` cieco, applica-e-veta.
- [ ] **Banner in testa a `GRADING-IMPROVEMENTS-PLAN.md`, `GRADING-IMPROVEMENTS.md` e
  `GRADING-EVAL-WORKFLOW.md`:** «Abbandonato il 2026-08-06. Documento non mantenuto, conservato per
  la storia. Lo strumento attivo è `CONSENSUS-WORKFLOW.md`.» Nient'altro: **il corpo di quei
  documenti non si tocca**.
- [ ] Creare `evals/plan-slices/README.md` **in inglese** come punto d'ingresso della directory, con
  **due** gruppi di artefatti:
  - **attivo** — `CONSENSUS-WORKFLOW.md`, `CONSENSUS-WORKFLOW-PLAN.md`, `prompts/`, `assets/`,
    `support/`, `REGRESSION-LEDGER.md`, `NOTES.md`, `recipe-app/sources/`,
    `recipe-app/EVALUATION-BRIEF.md`, `recipe-app/results/PLAN-*` e i report di ciclo,
    `validate_plan.py` che vive nella skill, `evals/AGENTS.md`, il target `validate`;
  - **archiviato** — `GRADING-*.md`, `grader-rubric*.json`, `fixtures/`, `results/calibration-*/`,
    gli script di grading e i target `grade`/`compare`/`calibrate*`.

**Verifica:** `grep -rn "EVAL-WORKFLOW"` non trova riferimenti al vecchio nome; i tre documenti di
grading aprono con il banner; nessun file di codice è stato toccato, quindi `make test` resta quello
di prima.

**Output:** un commit per il banner, uno per il README.

## Fase 0b — Conversione dei documenti umani

**Precondizioni:** Fase 0a. **Chiamate provider:** zero. **Nessuna fase dipende da questa.**

Documenti che nessun modello legge durante un ciclo. La conversione è lavoro bruto senza rischio e
senza dipendenze: può stare per ultima, o essere fatta a pezzi, o slittare indefinitamente.

- [ ] `CONSENSUS-WORKFLOW.md`, `CONSENSUS-WORKFLOW-PLAN.md`, `NOTES.md`, `PROMPTS.md`.
- [ ] Non toccare i documenti di grading: sono archivio.
- [ ] Riparare `CONSENSUS-WORKFLOW.md:128`, che rimanda a *Formulazioni riscritte* del registro: la
  sezione è in `recipe-app/results/CONSENSUS-CON-5.REPORT.md` dalla Fase 1c.

**Verifica:** i documenti convertiti non citano artefatti con nomi diversi da quelli reali; le
citazioni testuali dagli artefatti storici restano **in italiano fra virgolette**, perché sono prove.

## Fase 1a — Contratto: template e validator degli `IMPROVEMENT`

**Precondizioni:** Fase 0a, **più la mappa clausola → riga prodotta in Fase 1c**. **Chiamate
provider:** zero.

La domanda che bloccava questa fase — cosa succede alla riga quando una voce riformula la clausola
che la copre — è decisa: vedi *Decisioni già prese*, ri-ancoraggio automatico e superamento su
subsunzione.

La dipendenza dalla mappa nasce dalla decisione stessa. Il validator controlla che le righe coprenti
dichiarate da una voce **coincidano con la mappa**, e senza mappa quel controllo non distingue una
voce che dichiara `uncovered` per ignoranza da una che lo dichiara con ragione — cioè esattamente il
caso che la regola dura esiste per intercettare. È l'unico pezzo di 1c che serve a 1a: traduzione,
split della narrativa e migrazione semantica del registro non entrano.

È il pezzo che decide tutti gli altri, ed è l'unico che è codice. Replica l'architettura che nello
skill ha retto cinque cicli: `assets/plan-template.md` + `scripts/validate_plan.py`.

- [ ] Creare `assets/improvement-template.md` **in inglese**, con i campi obbligatori per voce:
  - `Evidence — candidate A` e `Evidence — candidate B`, **due celle separate**: un riferimento
    localizzabile (`PLAN-…-CON-N.md:NN`, oppure `slice N` più il nome del campo) oppure la
    dichiarazione esplicita che quel candidato non manifesta il difetto;
  - `Existing rule that failed to prevent the defect` — clausola di `SKILL.md` con la sua sezione,
    **più le righe di registro che la coprono, oppure `uncovered`**, oppure `none` se nessuna
    clausola è nominata. Le righe dichiarate sono ciò che il workflow **ri-ancora** quando la voce
    riformula, ed è l'unico modo per rendere meccanicamente rilevabile un caso che oggi è invisibile:
    `R-002` porta `Commit: d977043` mentre la sua clausola è stata riscritta da `87150d3`, senza
    nessun link in avanti;
  - `Change to the skill` — sezione precisa e modifica normativa concreta;
  - `Reformulation attempted and discarded, and why` — obbligatorio quando il campo precedente nomina
    una clausola **e** la voce aggiunge righe. **«La clausola è coperta da una riga del registro» non
    è una ragione ammissibile**, ed è il vincolo che tiene in piedi la regola dura: le clausole
    coperte sono le poche già accusate — quattro clausole di corpo portano sei righe su undici — cioè
    le candidate più probabili alla riformulazione. Ammettere la copertura come esenzione le
    renderebbe permanentemente non riformulabili e restituirebbe il cricchetto intatto;
  - `Binary test` — nella grammatica delle righe del registro, decidibile su un piano generato;
  - `Cost` — cosa si toglie o si fonde se questa entra.
- [ ] Creare `scripts/consensus/validate_improvement.py` con i controlli:
  - presenza di ogni campo obbligatorio per voce;
  - **i riferimenti si risolvono**: il file esiste e il numero di riga è nel range. Intercetta le
    citazioni allucinate, che è un rischio reale in un artefatto che nessuno rilegge riga per riga;
  - **le righe dichiarate coprenti si risolvono** in `REGRESSION-LEDGER.md` e coincidono con la mappa
    clausola → riga della Fase 1c; una clausola che la mappa dichiara coperta e la voce dichiara
    `uncovered` è uno scarto;
  - `Binary test` presente e non vuoto, con una grammatica minima.
- [ ] **Dare alla mappa il formato che il validator consuma: dati separati dalla prosa.** La Fase 1c
  consegna `support/CLAUSE-ROW-MAP.md`, 205 clausole in tabelle markdown più un centinaio di righe di
  prosa. Il validator non deve parsare markdown: estrarre i record — id, sede, commit d'introduzione,
  commit dell'ultima riscrittura, righe coprenti, ancoraggio — in un file tabellare sotto `support/`,
  e lasciare nel `.md` regola di conteggio, ancoraggi irrisolti, ancoraggi che risolvono sul brief,
  verifica del campione e divergenze di blame, che nessuno script legge. Il taglio è **dati contro
  prosa, non per sezione di `SKILL.md`**: le due interrogazioni sono «quali righe coprono questa
  clausola» e «quali clausole sono scoperte», e nessuna delle due è per sezione. Da fare qui e non in
  1c, perché il formato lo detta il consumatore e il consumatore è questo validator.
  - **Sede e commit sono rigenerabili da git**, quindi li emette lo script invece di fidarsi delle
    celle scritte a mano. Il commit dell'ultima riscrittura è quello che ha cambiato il **testo** della
    clausola, **non `git blame` della riga**: le 16 divergenze in fondo alla mappa sono righe
    rimandate a capo da una modifica vicina, e un ri-ancoraggio dedotto dal blame azzererebbe `×k` su
    righe che nessuno ha toccato.
  - **L'ancoraggio non è rigenerabile** e si mantiene a mano: per nove righe su undici è un'inferenza,
    e i quattro `unresolved` sono fallimenti registrati, non celle da riempire.
  - **Riparare i tre riferimenti che la migrazione del registro ha reso stali**, già che il file si
    riapre qui: `CLAUSE-ROW-MAP.md:302` e `:381` puntano a *Difetti degli artefatti mai registrati* e
    *Formulazioni riscritte*, che ora vivono in `CONSENSUS-CON-5.REPORT.md`; `:210` punta a *Da
    popolare*, ora *To populate*. La Fase 1c non poteva toccarli senza attraversare due volte lo
    stesso confine.
- [ ] Implementare lo **scarto per voce**: la voce cade, il documento resta, ogni scarto esce con il
  campo mancante e il motivo in forma leggibile dal report. **Nessuna rigenerazione.**
- [ ] Test del validator su artefatti reali: `PLAN-CC-CON-4.IMPROVEMENT.md` deve produrre voci
  parzialmente conformi, `PLAN-CX-CON-4.IMPROVEMENT.md` deve produrre **zero** voci conformi. Sono la
  fixture negativa che il progetto già possiede.

**Verifica:** `make test` verde; il validator sui due artefatti di CON-4 dà l'asimmetria attesa; il
residuo dichiarato è che il validator verifica **che** il riferimento esista, non che **sostenga**
l'affermazione — stessa spaccatura `validator`/`lettura` delle righe del registro.

## Fase 1b — I quattro prompt

**Precondizioni:** Fase 1a. **Chiamate provider:** zero.

I prompt **citano** il template, non lo duplicano.

- [ ] `prompts/improve.prompt.md`: payload cieco simmetrico, un solo documento per valutatore
  sull'unione dei difetti dei due candidati, divieto esplicito di leggere `support/`, i due campi
  bidirezionali, l'esclusione del walking skeleton dichiarata come restrizione di scope del ciclo,
  `EVALUATION-BRIEF.md` al posto di `REFERENCE-PLAN.md` eliminato da `6476f32`.
- [ ] `prompts/review.prompt.md`: payload **cieco e simmetrico** — i due `IMPROVEMENT` come
  `Report A`/`Report B`, mai «il tuo report». Sezioni simmetriche: condivisa, unica ad A, unica a B,
  contraddittoria. Per ogni voce condivisa, il campo che dichiara se i due lati portano **lo stesso
  rimedio** o solo lo stesso tema — è il dato che separa `intersezione` da `intersezione-tema`.
- [ ] `prompts/verdict.prompt.md`: per ogni riga attiva, verdetto più **citazione obbligatoria** del
  punto pubblicato (piano, slice, sezione). Nessun verdetto senza citazione; una citazione che non si
  risolve è uno scarto. La cella `Da sorvegliare` della riga entra nel prompt come istruzione
  aggiuntiva per quella riga.
- [ ] `prompts/recidiva.prompt.md`: una sola chiamata, input i due `IMPROVEMENT` più **tutte** le
  righe, dormienti incluse. Output l'elenco delle coppie `voce → riga | nessuna`. Nessuno scalare.
- [ ] Aggiungere in testa a `PROMPTS.md` la nota che è uno scratchpad umano e che la sorgente
  normativa è `prompts/`.
- [ ] Creare `support/AGENT-PLAN-MAP.md` con le righe di CON-1…CON-5 e il formato per i cicli futuri.
- [ ] **Riempire lo slot `gen` di `Misurato su` nelle undici righe del registro** dai dati della
  mappa. Oggi portano tutte `gen unrecorded`: modello ed effort di CON-1…CON-5 non esistono in nessun
  artefatto, e `CC`/`CX` nominano l'harness, non il modello. Se la mappa non riesce a ricostruirli, le
  celle restano `unrecorded` e lo si dichiara una volta invece di lasciarlo sembrare una svista.

**Verifica:** nessun prompt nomina `REFERENCE-PLAN.md`, `support/`, i path o i nomi dei generatori;
`review` non contiene la parola «tuo»; i nomi degli artefatti citati coincidono con quelli della
struttura del report.

**Rischio:** i prompt riscritti non sono mai stati eseguiti. È esattamente ciò che la Fase 2 misura.

## Fase 1c — Registro, mappa e report

**Precondizioni:** Fase 0a. **Precede Fase 1a**, che ne consuma la mappa clausola → riga; indipendente
da 1b. **Chiamate provider:** zero.

La fase porta **tre deliverable separabili**, e solo il primo blocca 1a:

- **la mappa clausola → riga**, artefatto nuovo che non tocca il testo del registro. I riferimenti
  `R-NNN` sono stabili attraverso la traduzione, quindi può essere prodotta prima e da sola —
  **fatta** il 2026-08-06, `support/CLAUSE-ROW-MAP.md`, 205 clausole;
- **il registro**: estrazione della narrativa, traduzione, migrazione semantica e riclassificazione —
  **fatto** il 2026-08-06, insieme a `recipe-app/results/CONSENSUS-CON-5.REPORT.md`;
- **la struttura del report di ciclo**, in fondo a questa fase. **Ancora aperta.** Il report CON-5
  non la definisce e non la segue: CON-5 è un ciclo parziale, quindi i contatori che non hanno un
  valore portano `n/a — partial cycle` invece di uno zero che si leggerebbe come misura.

Un solo attraversamento del confine sul registro: traduzione, split e migrazione semantica nella
stessa passata. Due passate su testo come la formulazione di `R-002` — già riscritta tre volte — sono
più pericolose di una, perché la seconda ha meno contesto della prima.

- [x] **Estrarre la narrativa di ciclo** dal registro: il 62% del file, riletto dal `verdetto` a ogni
  ciclo senza servire. Va in `recipe-app/results/CONSENSUS-CON-5.REPORT.md`, creato retroattivamente
  come contenitore. Righe **73–310** della versione italiana a `f99449c`; la stima 63–301 di questo
  piano era di una revisione precedente del registro. **Non si traduce**: è il record di ciò che
  CON-5 ha deciso, scritto in italiano il 2026-08-04, e tradurre un record lo falsifica. Solo la
  cornice del report nasce in inglese, e lo dichiara.
- [x] **Eccezione obbligatoria:** le note *«Da cercare al prossimo ciclo, oltre alla riga»* di `R-010`
  e `R-011` non sono narrativa, sono istruzioni per il verdetto successivo. Diventano una cella
  **`Da sorvegliare`** della riga.
- [x] **Tradurre** il registro in inglese.
- [x] **Migrare la semantica**: `tiene` → `non smentita ×k`; stato `dormiente` a `×3`; **stato
  `superata da R-NNN`**, che non conta come smentita e toglie la riga dall'insieme verificato in via
  definitiva; colonna `Misurato su` estesa a modello ed effort; `Origine: potatura`; cella `Da
  sorvegliare`; celle **`Supersedes` / `Superseded by`**; cella `Commit` che ammette `(pending)`.
  - **`Misurato su` ha cinque slot, non quattro**, deciso il 2026-08-06:
    `ciclo · piani · strumenti · gen <modello e effort per lato> · verdict <strumento>`. Il quinto
    serve perché i verdetti CON-5 vengono da **lettura umana offline**, non da una chiamata: senza lo
    slot quel fatto sparisce al primo ciclo automatizzato, ed è esattamente il tipo di cosa che la
    colonna esiste per non far sparire. Fase 5 lo emette.
  - **`to verify` e `non smentita ×0` restano due stati distinti.** Il primo dice che nessun ciclo ha
    girato contro la riga — `R-010`, `R-011`; il secondo che dei cicli hanno girato e nessuno conta
    come test, per provenienza o per ri-ancoraggio. Al `verdetto` la differenza cambia cosa si sta
    guardando.
- [x] **Nessuna riga parte da `×1`.** La versione precedente di questa fase prescriveva `×1 misurate
  sul solo CON-5`; è sbagliato, perché il registro è stato popolato **a posteriori** — vedi
  `CONSENSUS-WORKFLOW.md` § *Lo stato dell'evidenza*. Serve una cella **`Provenienza`** con tre
  valori, e il `k` iniziale discende da quella:
  - **`ex-ante`** — riga scritta nello stesso minuto del commit che verifica: `R-010`, `R-011`.
    Previsioni vere, entrambe ancora `da verificare`, quindi **`×0`**.
  - **`ricostruita`** — riga scritta a ritroso su un commit già fatto, ma non toccata durante la
    misura: `R-001`, `R-004`, `R-005`, `R-008`, `R-009` e il primo membro di `R-002`. CON-5 è un test
    valido, quindi **`×1`**.
  - **`ricostruita e ritarata`** — riga riscritta fra le 22:20 e le 22:41 del 2026-08-04, cioè dopo
    che i verdetti CON-5 delle 22:02 avevano mostrato cosa dicevano i piani: `R-002` secondo membro,
    `R-003`, `R-006`, `R-007`. Per queste CON-5 **non è un test** — la riga è stata adattata al piano
    che avrebbe dovuto falsificarla, e per `R-007` anche il brief, nello stesso minuto. Partono da
    **`×0`**: il primo test vero è CON-6.
- [x] **Ri-ancorare retroattivamente le due righe che hanno subito una riformulazione.** `87150d3` ha
  riscritto in loco la clausola di `R-002` (`SKILL.md:50-57`, `+7/-3`) ed `eb926bb` quella di `R-008`
  (`SKILL.md:92-96`, `+4/-2`). Le due righe prendono il commit nuovo in `Commit` e `Misurato su`; le
  affermazioni **non si toccano**, perché quantificano sul piano e restano decidibili. Attenzione al
  perimetro: di `R-002` la riformulazione tocca il **solo primo membro**, mentre il secondo vive su
  `SKILL.md:51`, intatta da `d977043` — righe e clausole non sono 1:1 in nessuno dei due versi.
  Il **superamento** delle due coppie (`R-010` ⊂ `R-002` m1, `R-011` ⊂ prima clausola di `R-008`) è
  una decisione umana e va posta come tale, non applicata in migrazione: `R-002` m2 sopravvive
  comunque al superamento di m1, quindi `R-002` non può uscire intera.
- [x] **Annotare la sovrapposizione dei verdetti.** `R-010` è un sottocaso di `R-002` m1 e `R-011`
  della prima clausola di `R-008`: i loro verdetti non sono indipendenti, e contarli come due
  osservazioni sovrastima l'evidenza. `R-008` lo dice già in prosa nella cella `Verifica`.
- [x] **Riclassificare `R-002`…`R-008` da `intersezione` a `intersezione-tema`** e annotare che sono
  state prodotte con prompt diversi da quelli di `prompts/` e con un lato non conforme.
- [x] **Mappa clausola → riga di registro**, con le clausole scoperte marcate come tali. Spostata qui
  da Fase 4 il 2026-08-06: senza la mappa il campo `Regola esistente che non ha impedito il difetto`
  non ha contropartita al momento di decidere, e il default resta aggiungere una regola nuova — cioè
  il cricchetto sopravvive al meccanismo costruito per fermarlo. La mappa produce anche l'elenco delle
  clausole **senza riga**, che sono quelle riformulabili senza rompere una previsione.
  Campione già misurato il 2026-08-06 su `R-002`, `R-008`, `R-010` e `R-011`, perimetro § 1, § 2 e il
  `Complete when` di § 5, unità contata «frase o bullet che impone un obbligo, un divieto o un permesso
  condizionato»: **37 clausole, 9 coperte, 28 scoperte (≈76%)**. Le 9 coperte sono in realtà **4
  clausole di corpo** più 5 loro restatement nei gate, e su quelle 4 atterrano **6 righe su 11**. Fra
  le scoperte c'è il **test di split del § 2** (`SKILL.md:80-82`), che il registro nomina come sede
  della diagnosi della riga C di CON-5 senza avergli mai dato una riga. La mappa completa parte da qui.
  **Ogni voce della mappa dichiara come l'ancoraggio è stato ottenuto**, `dichiarato` o `ricostruito`.
  Per nove righe su undici la clausola non è mai stata registrata: la riga è nata su un commit, non su
  un testo, e l'ancoraggio lo sta inferendo la mappa. Nel campione l'ancoraggio regge intatto
  esattamente sulle due righe `ex-ante` — `R-010`, `R-011` — e va alla deriva esattamente sulle due
  ricostruite, `R-002` e `R-008`. Un ancoraggio `ricostruito` può anche **non risolversi**: la mappa
  registra il fallimento invece di scegliere la clausola più somigliante.
- [ ] **Struttura di `recipe-app/results/CONSENSUS-CON-N.REPORT.md`** — unico deliverable residuo
  di questa fase — con i **contatori in testa**:

  ```
  SKILL.md   417 → 451   (+34)
  voci applicate         5
    riformulazioni       0
    aggiunte             5   ← ognuna con la ragione della riformulazione scartata
  righe di registro nuove 5   (2 intersezione, 1 intersezione-tema, 2 giudizio)
  righe ri-ancorate       0   (contatore riportato a ×0)
  coppie candidate al superamento 0
  righe attive           11 → 16
  voci scartate dal gate  3   (per campo mancante)
  verdetti scartati       0   (citazione non risolta)
  recidiva                2 coppie su 9 voci
  ```

  `righe attive N → M` è per il registro ciò che `0 riformulazioni su 5 aggiunte` è per lo skill: il
  contatore che morde sull'accumulo invece che sul merito. Una riformulazione ri-ancora e non aggiunge
  nulla; un superamento lascia il numero invariato — una entra e una esce — quindi una crescita di
  `righe attive` accusa sempre e solo le aggiunte. `coppie candidate al superamento` è ciò che il veto
  deve guardare: sono le sovrapposizioni fra affermazioni, cioè i verdetti che smetterebbero di essere
  indipendenti.

  Poi: esito del validator strutturale; voci applicate con id, hunk e origine; **voci classificate
  condivise da un solo `REVIEW`** — la misura di instabilità che sblocca la Fase 7 e che oggi nessuno
  produce; elenco dei punti che richiedono lettura umana; log degli scarti; coppie di recidiva;
  verdetti con le loro citazioni.

**Verifica:** il registro contiene solo tabella, regole d'uso e backlog vivo; nessuna riga di
narrativa di ciclo; ogni riga ha `Misurato su` in tutti e cinque gli slot, con `unrecorded` dove il
dato non esiste e mai una cella muta; la mappa copre tutte e undici le righe e dichiara quante
clausole di `SKILL.md` restano scoperte.

## Fase 2 — Ciclo CON-6 manuale

**Precondizioni:** Fasi 1a, 1b, 1c. **Chiamate provider:** **9** — 2 generazione, 2 `improve`,
2 `review`, 2 `verdetto`, 1 `recidiva`. Effort **`high`**. Richiede **autorizzazione esplicita** dopo
il dry-run e il conteggio, per `evals/AGENTS.md`.

I piani CON-5 **non si riusano**: sono delle 11:57 del 2026-08-04, mentre `87150d3` è delle 23:11 e
`eb926bb` delle 23:30. Precedono entrambi i commit, quindi non possono verificare `R-010` e `R-011`.

- [ ] Generare i due candidati con lo `SKILL.md` corrente e registrarli in
  `support/AGENT-PLAN-MAP.md`.
- [ ] `make validate` su entrambi.
- [ ] Eseguire `improve`, il gate, `review`, `verdetto` e `recidiva` a mano, copiando i prompt da
  `prompts/`.
- [ ] Scrivere `CONSENSUS-CON-6.REPORT.md` nella struttura di Fase 1c, contatori in testa.
- [ ] Applicare le sole voci che il filtro licenzia, una riga di registro per voce, `Commit:
  (pending)`. **Non committare dal workflow.** Leggere i contatori, poi `git diff`, poi decidere.
- [ ] Correggere `prompts/`, `assets/` e `CONSENSUS-WORKFLOW.md` dove la procedura non ha retto.

**Verifica — due criteri distinti, ed è il secondo quello che conta:**

1. *Completamento.* Il ciclo si chiude producendo tutti gli artefatti previsti senza intervento non
   documentato. Ogni scostamento è annotato.
2. *Validità della tesi.* I due `IMPROVEMENT` hanno **specificità comparabile**, misurata in modo
   descrittivo: quante voci sopravvivono al gate per lato. Nessuna soglia — un ciclo non emette un
   verdetto su un'ipotesi, coerentemente con `non smentita ×k`.

**Cosa si fa in ciascuno dei tre esiti — deciso prima di eseguire:**

- **Un lato a ~0 voci operative.** Decide il log degli scarti. Scarti concentrati **tutti sullo stesso
  campo** → il template è scritto male, si corregge quel campo e si ripete. Scarti **sparsi** → il
  modello non sa fare il lavoro, l'ipotesi prende una smentita `×1`, la Fase 5 non parte e si decide a
  CON-7.
- **Entrambi operativi, voci condivise con lo stesso rimedio.** `Origine: intersezione`, applicazione
  automatica.
- **Entrambi operativi, stesso tema e rimedi diversi.** `Origine: intersezione-tema`: il tema porta
  l'evidenza d'intersezione, la formulazione viene dal lato che la fornisce ed è decisa dall'umano.
  Non è una ritirata: è la classificazione per voce di ciò che è già successo in CON-4, e mantiene
  `review` portante — è la fase che separa questo esito dal precedente.

**Fuori dal tavolo per CON-6:** cambiare uno dei due modelli. È un confine di strumento e renderebbe
il ciclo non interpretabile, per la stessa ragione per cui l'effort resta a `high`.

**Output:** il ciclo eseguito, la procedura corretta, e il primo dato sulla tesi. È il gate delle
Fasi 2b, 4 e 5.

## Fase 2b — Revisione del brief

**Precondizioni:** Fase 2. **Chiamate provider:** zero; si verifica su CON-7.

Dopo CON-6, mai prima: `EVALUATION-BRIEF.md` è l'autorità contro cui si decidono sette righe su
undici, e toccarlo prima del ciclo che verifica per la prima volta `R-010` e `R-011` aggiungerebbe un
confine al verdetto.

- [ ] Verificare duplicazioni. Il file è 51 righe e già asciutto; il candidato reale non è ridondanza
  di token ma una **separazione di responsabilità sporca**: `Known conflicts`, secondo bullet,
  riscrive quasi verbatim la regola di `R-002` (*«no `Includes` or `Verification` bullet may assert
  either side»*), cioè mette una regola di scrittura del piano dentro il documento che descrive lo
  scenario. Il brief dovrebbe dichiarare il conflitto, non come si scrive il piano.
- [ ] Modularizzare solo se la lettura lo giustifica; non inseguire token che non ci sono.
- [ ] Registrare il confine in `Misurato su` per tutte le righe che citano il brief.

**Verifica:** CON-7. Le righe che citano il brief non cambiano verdetto per effetto della revisione;
se cambiano, il brief ha cambiato significato e la revisione va rifatta.

## Fase 3 — Riorganizzazione del codice

**Precondizioni:** Fase 0; indipendente dalla Fase 2, che non tocca codice. **Chiamate provider:**
zero.

L'ambizione di questa fase è stata **ridotta** il 2026-08-06: `scripts/runtime/` esisteva per ospitare
il codice *condiviso fra i due strumenti*. Con un solo strumento in servizio non c'è niente da
condividere.

- [ ] Spostare in `scripts/consensus/` **solo** ciò che il ciclo userà davvero: invocazione provider,
  hashing, scrittura atomica e resume, estratti da `grader_runtime.py` e `orchestrator_artifacts.py`.
  `validate_improvement.py` ci vive già dalla Fase 1a.
- [ ] Lasciare il resto del grading dov'è, come archivio, con i suoi test e i suoi target.
- [ ] Aggiornare import, test, `Makefile` e documentazione di ciò che è stato spostato.

**Verifica:** `make test` verde; nessun artefatto sotto `recipe-app/results/` modificato.

## Fase 4 — Modularizzazione e pruning dello skill

**Precondizioni:** Fase 2, e la mappa prodotta in Fase 1c. **Chiamate provider:** zero per la fase; la
verifica costa un ciclo (CON-7).

Va **dopo CON-6**, non prima. Potare prima significa scegliere cosa togliere in base a quanto una
clausola sembra ridondante leggendola, che è esattamente il tipo di giudizio che il ciclo esiste per
non fare. E anticipare la sola modularizzazione «tanto è neutra» è falso: sposta ciò che il modello ha
in contesto al momento di generare.

Stato di partenza: `SKILL.md` monolitico a **417 righe**, con tre rami d'ingresso — `Choose the
branch`, `Review an existing plan`, `Split, merge, or reorder an existing plan` — che caricano tutte e
417 comunque. La disclosure progressiva esiste già, ma solo per `assets/plan-template.md` e
`scripts/validate_plan.py`.

- [ ] Aggiornare la mappa clausola → riga prodotta in Fase 1c con ciò che CON-6 ha cambiato.
- [ ] Modularizzare per ramo d'ingresso, così che un ramo non caricato non occupi contesto.
- [ ] Potare e fondere. **Ogni rimozione è coperta o scoperta:** coperta → la riga di registro
  esistente si riscrive e la previsione resta; scoperta → nasce una riga `Origine: potatura` con
  l'affermazione «la rimozione di X non fa ricomparire il difetto Y». Nessuna rimozione senza una
  delle due.
- [ ] **Decidere i quattro ancoraggi `unresolved`** che la mappa registra come fallimenti: `R-001` m1,
  la componente `9aa2586` di `R-005`, la seconda metà di `R-006` m1 e la componente `9aa2586` di
  `R-006`. Per ciascuno una sola delle due mosse: lo skill acquista la clausola che la riga
  presuppone, oppure la riga si riscrive per smettere di pretendere ciò che lo skill non dice. È
  lavoro di questa fase perché è la stessa decisione della potatura letta al contrario — lì si toglie
  testo coperto da una riga, qui c'è una riga che copre testo inesistente. Il caso netto è `R-006` m1:
  il requisito è stato aggiunto alla riga dopo CON-5 **perché** `CX` non dichiarava il riuso, quindi
  un verdetto contro quel membro sembra una regressione dello skill senza esserlo.
- [ ] Registrare il confine di strumento in `Misurato su` per tutte le righe attive.

**Verifica:** **CON-7**. La fase non si chiude quando lo `SKILL.md` è più corto: si chiude quando
CON-7 non ha smentito le righe di potatura, e nessuna riga attiva ha un ancoraggio `unresolved`.

## Fase 5 — Orchestratore del ciclo

**Precondizioni:** Fasi 2 e 3. **Chiamate provider:** 7 per ciclo dopo la generazione, dietro dry-run
e `CONFIRM_SEND`.

- [ ] `scripts/consensus/` con il comando che rende i prompt da `prompts/`, compone i payload ciechi
  da una allowlist esplicita, invoca i provider e scrive gli artefatti.
- [ ] Target `make consensus N=… PHASE=improve|review|verdict|recidiva|report`, con `DRY_RUN`,
  `RESUME`, `CONFIRM_SEND` e registrazione degli hash, del modello e dell'effort.
- [ ] **Il gate di conformità è `validate_improvement.py`**, invocato dalla fase: le voci non conformi
  cadono e finiscono nel log degli scarti, `review` parte comunque.
- [ ] **L'applicazione è codice:** una voce licenziata dal filtro produce un hunk di `SKILL.md` e una
  riga di registro con lo stesso id e `Commit: (pending)`. **Nessun commit.** Un target
  `make consensus-reject ID=…` toglie una voce sola, hunk e riga insieme.
- [ ] Il join `report` è deterministico: nessuna chiamata, solo composizione degli artefatti prodotti.
  I contatori sono composizione; la **recidiva no** — è la fase 7, ed è per questo che esiste come
  fase invece che come calcolo del report.
- [ ] Test che nessun path sotto `support/` compaia in un prompt renderizzato.
- [ ] Test che il dry-run mostri esattamente le esecuzioni attese per fase e i target attesi.

**Verifica:** dry-run di tutte le fasi; un ciclo completo eseguito e ripreso con `RESUME=1` senza
nuove chiamate; confronto degli artefatti con quelli prodotti a mano nella Fase 2.

## Fase 6 — Generazione automatizzata

**Precondizioni:** Fase 5. **Chiamate provider:** 2 in più per ciclo.

- [ ] `PHASE=generate` produce i due candidati dalle sole fonti, con hash e resume, e aggiorna
  `support/AGENT-PLAN-MAP.md`.
- [ ] Annotare nel registro che lo strumento di generazione è cambiato: i piani CON-1…CON-N-1 nascono
  da sessioni interattive, non da chiamate headless. È un confine di strumento.

## Fase 7 — Intersezione deterministica, opzionale

**Precondizioni:** almeno due cicli completi in Fase 5. **Da decidere dopo, non ora.**

Far produrre alla fase `review` un output strutturato minimo — id, titolo, categoria, lato che porta
il rimedio — così che l'intersezione la calcoli il codice invece del modello.

La condizione di sblocco è ora **osservabile**: il report di Fase 1c pubblica le voci classificate
condivise da un solo `REVIEW`. Prima la fase diceva «si valuta se due cicli mostrano che la
classificazione è instabile», ma niente misurava quell'instabilità, quindi la condizione non poteva
verificarsi.
