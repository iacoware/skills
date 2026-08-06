# Ciclo di consenso — piano di implementazione

Piano per separare il ciclo di consenso dal grading system abbandonato e automatizzarlo. Ogni fase è
pensata per una **sessione fredda separata**: dichiara le proprie precondizioni, le attività, come si
verifica e cosa produce. Una fase non presume il contesto conversazionale in cui la precedente è
stata svolta.

Lo strumento e la sua ragione stanno in `CONSENSUS-WORKFLOW.md`; qui c'è solo il lavoro da fare.

Le fasi chiuse sono uscite da questo file il 2026-08-06 e stanno in `CONSENSUS-WORKFLOW-PLAN-CLOSED.md`
con la loro cronaca. Non serve aprirlo per lavorare: ciò che le fasi aperte usano è ripetuto dove
serve.

## Rotta

Cosa aprire, per fase. Una sessione legge questa tabella, le *Decisioni già prese* e la propria fase.

| Fase | Stato | Oltre a questo file, apri |
|---|---|---|
| 0a, 0, 0c, 1a | **chiuse** — `f659c8b`, `f659c8b`, `88a4e9b`, `278edfd` | `CONSENSUS-WORKFLOW-PLAN-CLOSED.md`, solo per sapere *perché* |
| 0d — split dei documenti | **chiusa** — 2026-08-06 | come sopra |
| 0b — conversione | aperta, senza dipendenze | i documenti da convertire |
| **1b-i — prompt** | **aperta, prossima** | `assets/improvement-template.md`, `PROMPTS.md`, `CONSENSUS-WORKFLOW.md` § *Il ciclo*, `workflow/CYCLE.md` |
| **1b-ii — mappa generatori** | **aperta, indipendente da 1b-i** | `recipe-app/results/PLAN-*`, `git log`, `REGRESSION-LEDGER.md` § *`Measured on`* |
| 1c — report template | aperta, resta un deliverable | `recipe-app/results/CONSENSUS-CON-5.REPORT.md`, `assets/improvement-template.md` |
| 2 — CON-6 | aperta, **9 chiamate, autorizzazione** | `prompts/`, `../AGENTS.md`, `support/AGENT-PLAN-MAP.md` |
| 2b, 4 | aperte, dopo CON-6 | `recipe-app/EVALUATION-BRIEF.md` (2b); `support/CLAUSE-ROW-MAP.md` (4) |
| 3, 5, 6, 7 | aperte, codice | `scripts/`, `Makefile` |

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
  che il generico non riempie, non un giudizio con una soglia. **Niente soglie.** Una voce non
  conforme si **scarta e si registra**, con **un solo tentativo**, e un lato a zero voci conformi non
  blocca il ciclo. Forma, scarto, codice di uscita e cosa il gate *non* misura stanno in
  `workflow/CONFORMANCE.md` e in `assets/improvement-template.md`; qui non si duplicano.
- **`Origine` ha quattro valori**: `intersezione`, `intersezione-tema`, `giudizio`, `potatura`.
  **I nomi canonici sono inglesi** dal 2026-08-06, perché li scrivono il registro migrato, i prompt e
  il validator: `intersection`, `intersection-theme`, `judgement`, `pruning`. Stessa cosa per
  `Verifica`: `validator` e `reading`. I termini italiani di questo piano, di
  `CONSENSUS-WORKFLOW.md` e di `workflow/` restano leggibili finché la Fase 0b non li converte, e la
  mappa fra i due
  insiemi è dichiarata nelle regole d'uso del registro. Prompt e validator non emettono mai gli
  italiani.
- **Una voce che tocca una clausola coperta o ri-ancora la riga, o la assorbe** — due regole, non
  una, perché **le righe quantificano su un piano generato, non sul testo dello skill**. Ne discende
  che una riformulazione **non falsifica** la riga: rompe l'attribuzione. Testo che cambia a portata
  invariata → ri-ancoraggio, automatico; portata che cambia → assorbimento, e un'affermazione **esce**
  dal registro. Regole, vincoli e cronaca degli assorbimenti già fatti vivono in
  `REGRESSION-LEDGER.md` § *Re-anchoring and absorption* e nelle celle `Absorbs`; qui non si
  duplicano. Ciò che va saputo senza aprirle: **una riga = una affermazione** è regola di scrittura
  dal 2026-08-06, l'assorbimento è **la sola mossa che toglie una previsione**, e il ciclo che ne
  emette uno lo mette in cima a ciò che il veto rilegge.
- **Una voce vale `intersezione` o `intersezione-tema` solo se entrambi i `REVIEW` la classificano
  condivisa.** Classificazione unilaterale → `giudizio`, e nessuna applicazione automatica.
- **Il workflow applica al working tree e non committa mai.** Applica solo ciò che il filtro
  licenzia. Una voce = un hunk di `SKILL.md` + una riga di registro, stesso id, riga con
  `Commit: (pending)`. Il veto umano legge i **contatori in testa al report**, poi `git diff`.
- **`recidiva` è una chiamata sola**, modello fisso `claude-opus-5`, e produce l'**elenco delle
  coppie** `voce improve → riga | nessuna`, non uno scalare. Controargomento ed eventi di inversione
  sono in `workflow/LEDGER.md` § *Perché `recidiva` è una sola chiamata*.
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
  cui si decidono quattordici righe su diciassette.
- **L'inglese è la lingua del progetto dal 2026-08-06.** Le fonti in `recipe-app/sources/` e gli
  artefatti storici — `PLAN-*`, `IMPROVEMENT`, `REVIEW`, report — **non si convertono mai**.
- Un confine di strumento **si attraversa una volta sola, deliberatamente, e si registra.**
- La decisione su cosa applicare allo `SKILL.md` resta umana in ogni fase, in forma di veto.
- **Le 15 unità di calibrazione già pagate non vanno conservate.** I 30 file sono tracciati in git.

## Fase 0b — Conversione dei documenti umani

**Precondizioni:** Fase 0a. **Chiamate provider:** zero. **Nessuna fase dipende da questa.**

Documenti che nessun modello legge durante un ciclo. La conversione è lavoro bruto senza rischio e
senza dipendenze: può stare per ultima, o essere fatta a pezzi, o slittare indefinitamente.

- [ ] `CONSENSUS-WORKFLOW.md`, i cinque file di `workflow/`, `CONSENSUS-WORKFLOW-PLAN.md`,
  `CONSENSUS-WORKFLOW-PLAN-CLOSED.md`, `NOTES.md`, `PROMPTS.md`. Dopo la Fase 0d sono unità
  indipendenti: si converte un file per volta, senza attraversare tutto il documento.
- [ ] Non toccare i documenti di grading: sono archivio.

**Verifica:** i documenti convertiti non citano artefatti con nomi diversi da quelli reali; le
citazioni testuali dagli artefatti storici restano **in italiano fra virgolette**, perché sono prove.

## Fase 1b — I quattro prompt e la mappa dei generatori

**Splittata in due sessioni il 2026-08-06**, prima di iniziarla. Non è una divisione per volume: i
due blocchi hanno contesti disgiunti. Scrivere i prompt chiede il template, `CONSENSUS-WORKFLOW.md` e
il `PROMPTS.md` legacy; ricostruire chi ha generato i piani CON-1…CON-5 chiede diciotto artefatti e
la storia di git, che non dicono niente su come si scrive un prompt. **Le due sotto-fasi non
dipendono l'una dall'altra** e possono andare in qualsiasi ordine; entrambe sono precondizione della
Fase 2.

### Fase 1b-i — I quattro prompt

**Precondizioni:** Fase 1a. **Chiamate provider:** zero.

I prompt **citano** il template, non lo duplicano.

I quattro stanno in una sessione sola e non si separano ulteriormente: la simmetria cieca è un
invariante **fra** `improve` e `review` — stesse sezioni, `Report A`/`Report B`, mai «il tuo
report» — e scriverli in sessioni diverse è il modo tipico di farli divergere. `verdetto` e
`recidiva` sono più corti e condividono la lettura del registro. Se il budget di una sessione non
regge, il taglio è dopo `improve`, `review` e la nota a `PROMPTS.md`: sono i due prompt che il ciclo
usa per primi, e `verdetto` e `recidiva` restano lavoro dichiarato invece che lavoro a metà.

Base di partenza asimmetrica, e va saputo prima di stimare: `improve` e `review` esistono in
`PROMPTS.md` come `## CREATE IMPROVEMENTS` e `## CREATE REVIEW 2` e si riscrivono — inglese, cecità,
simmetria; `verdetto` e `recidiva` **non esistono** e nascono da zero.

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
  normativa è `prompts/`. Va in questa sessione e nello stesso commit del primo prompt estratto:
  finché non c'è, `prompts/` e `PROMPTS.md` sono due sorgenti senza gerarchia dichiarata.

**Verifica:** nessun prompt nomina `REFERENCE-PLAN.md`, `support/`, i path o i nomi dei generatori;
`review` non contiene la parola «tuo»; i nomi degli artefatti citati coincidono con quelli della
struttura del report.

**Rischio:** i prompt riscritti non sono mai stati eseguiti. È esattamente ciò che la Fase 2 misura.

### Fase 1b-ii — Mappa dei generatori e slot `gen`

**Precondizioni:** nessuna; indipendente dalla 1b-i. **Chiamate provider:** zero.

I due deliverable sono in ordine, non in parallelo: la mappa è la fonte da cui si riempiono le celle.

- [ ] Creare `support/AGENT-PLAN-MAP.md` con le righe di CON-1…CON-5 e il formato per i cicli futuri.
- [ ] **Riempire lo slot `gen` di `Misurato su` in tutte le righe del registro** dai dati della
  mappa — sono diciassette dopo lo split della Fase 0c. Oggi portano tutte `gen unrecorded`: modello
  ed effort di CON-1…CON-5 non esistono in nessun artefatto, e `CC`/`CX` nominano l'harness, non il
  modello. Se la mappa non riesce a ricostruirli, le celle restano `unrecorded` e lo si dichiara una
  volta invece di lasciarlo sembrare una svista.

**Verifica:** ogni riga del registro porta uno slot `gen` risolto o `unrecorded` con la ragione
dichiarata una volta sola; la mappa nomina un generatore per ogni `PLAN-*` sotto
`recipe-app/results/`; il file resta escluso da ogni payload.

## Fase 1c — Registro, mappa e report

**Precondizioni:** Fase 0a. Indipendente da 1a e da 1b-i/1b-ii: la mappa che 1a consuma è già
consegnata.
**Chiamate provider:** zero.

**Due deliverable su tre sono fatti** il 2026-08-06, in un solo attraversamento del confine:

- **la mappa clausola → riga** — `support/CLAUSE-ROW-MAP.md`: 205 clausole normative, 40 coperte
  (20%), di cui 20 restatement, 165 scoperte. Dichiara per ogni voce come l'ancoraggio è stato
  ottenuto — `declared`, `reconstructed`, `unresolved` — più regola di conteggio, divergenze di blame
  e verifica del campione. Quattro ancoraggi restano `unresolved` e li decide la Fase 4;
- **il registro** — estrazione della narrativa in `recipe-app/results/CONSENSUS-CON-5.REPORT.md`,
  traduzione, migrazione semantica, riclassificazione a `intersection-theme`, ri-ancoraggio di
  `R-002` e `R-008`, e i due assorbimenti del 2026-08-06. Le regole d'uso del registro sono il
  record: non si riassumono qui.

Resta il terzo.

- [ ] **`evals/plan-slices/assets/report-template.md`**, in inglese: la struttura di
  `recipe-app/results/CONSENSUS-CON-N.REPORT.md`. Sta in `assets/` accanto a
  `improvement-template.md`, non dentro `CONSENSUS-WORKFLOW.md`, perché il join `report` della Fase 5
  lo rende come rende gli altri template. **Contatori in testa:**

  ```
  SKILL.md   417 → 451   (+34)
  voci applicate         5
    riformulazioni       0
    aggiunte             5   ← ognuna con la ragione della riformulazione scartata
  righe di registro nuove 5   (2 intersezione, 1 intersezione-tema, 2 giudizio)
  righe ri-ancorate       0   (contatore riportato a ×0)
  affermazioni assorbite  0
  righe attive           17 → 22
  voci scartate dal gate  3   (per campo mancante)
  verdetti scartati       0   (citazione non risolta)
  recidiva                2 coppie su 9 voci
  ```

  `righe attive N → M` è per il registro ciò che `0 riformulazioni su 5 aggiunte` è per lo skill: il
  contatore che morde sull'accumulo invece che sul merito. Ri-ancoraggio e assorbimento non aggiungono
  righe — l'assorbimento anzi ne toglie una se il membro assorbito era tutta la riga — quindi una
  crescita di `righe attive` accusa sempre e solo le aggiunte. `affermazioni assorbite` è ciò che il
  veto deve leggere per primo: è l'unico contatore che dice che una previsione è **uscita** dal file,
  e ogni assorbimento va riletto perché la fusione può aver allargato ciò che la riga afferma.

  Poi: esito del validator strutturale; voci applicate con id, hunk e origine; **voci classificate
  condivise da un solo `REVIEW`** — la misura di instabilità che sblocca la Fase 7 e che oggi nessuno
  produce; elenco dei punti che richiedono lettura umana; log degli scarti; coppie di recidiva;
  verdetti con le loro citazioni.

  Il report CON-5 è già un'istanza parziale della struttura, non un modello: è un ciclo parziale,
  quindi i contatori senza valore portano `n/a — partial cycle` invece di uno zero che si leggerebbe
  come misura. Il template dichiara quella convenzione.

**Verifica:** il template rende ogni contatore derivabile dagli artefatti del ciclo senza una
chiamata, e il report CON-5 riscritto nella sua forma non perde nessuno dei dati che porta oggi.

## Fase 2 — Ciclo CON-6 manuale

**Precondizioni:** Fasi 0c, 1a, 1b-i, 1b-ii, 1c. `0c` è esplicita e non solo transitiva: un ciclo eseguito su
righe multi-affermazione produce verdetti che lo split dovrebbe poi disaggregare a posteriori.
**Chiamate provider:** **9** — 2 generazione, 2 `improve`,
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
- [ ] Correggere `prompts/`, `assets/`, `CONSENSUS-WORKFLOW.md` e `workflow/` dove la procedura non
  ha retto.

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
diciassette — sono le righe che lo portano in `Misurato su` — e toccarlo prima del ciclo che verifica
per la prima volta `R-010` e `R-011` aggiungerebbe un
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
- [ ] **Decidere i quattro ancoraggi `unresolved`** che la mappa registra come fallimenti. Dopo la
  Fase 0c due sono **righe intere** e si nominano per id — `R-001` e `R-015` — e due sono componenti
  `9aa2586` delle celle `Commit` di `R-005` e `R-006`, commit di cui nessuna affermazione rivendica
  una clausola. Per ciascuno una sola delle due mosse: lo skill acquista la clausola che la riga
  presuppone, oppure la riga si riscrive per smettere di pretendere ciò che lo skill non dice — per i
  due commit, la terza è toglierli dalla cella. È lavoro di questa fase perché è la stessa decisione
  della potatura letta al contrario — lì si toglie testo coperto da una riga, qui c'è una riga che
  copre testo inesistente. Il caso netto è `R-015`: il requisito è stato aggiunto a `R-006` dopo CON-5
  **perché** `CX` non dichiarava il riuso, quindi un verdetto contro quella riga sembra una
  regressione dello skill senza esserlo.
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
- [ ] **Ri-ancoraggio e assorbimento sono codice, con confini diversi.** Una voce che riformula
  ri-ancora da sé le righe che dichiara coprenti: commit nuovo, `×0`, nessuna riscrittura. Una voce
  con `Merged claim` **non si applica da sé**: emette la riga fusa, l'`Absorbs` con le regressioni
  assorbite, e il diff che toglie le affermazioni sostituite — e passa all'elenco umano, perché è
  l'unica mossa del ciclo che fa **uscire** una previsione dal registro.
- [ ] **Emettere `Misurato su` in tutti e cinque gli slot**, quinto incluso: `verdict <strumento>`.
  Esiste perché i verdetti CON-5 vengono da lettura umana offline, e senza lo slot quel fatto sparisce
  al primo ciclo automatizzato — cioè esattamente ciò che la colonna esiste per non far sparire.
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
