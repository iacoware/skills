# Ciclo di consenso su `plan-slices`

Lo strumento attivo per decidere se una modifica a `skills/plan-slices/SKILL.md` ha peggiorato lo
skill. Questo file è il **punto d'ingresso**: porta la procedura e il vocabolario per intero, e
rimanda a `workflow/` per il dettaglio di ogni meccanismo. Una sessione nuova legge questo, poi solo i
file che la sua fase richiede.

Il grading system — `GRADING-IMPROVEMENTS-PLAN.md`, `GRADING-EVAL-WORKFLOW.md`,
`grader-rubric.v3.json`, `fixtures/`, `results/calibration-*/` — è **abbandonato dal 2026-08-06**.
Non è un prerequisito di niente qui e non torna. Resta in git; la ragione e la lapide sono in
`workflow/RATIONALE.md`.

La lingua del progetto è l'**inglese** dal 2026-08-06: ogni artefatto nuovo nasce in inglese, con due
esclusioni permanenti — `recipe-app/sources/` e gli artefatti storici — e con i **candidati
generati** che la regola non raggiunge affatto, perché la loro lingua la decide lo `SKILL.md` sotto
test. La regola per esteso, con le sue ragioni, sta in `README.md` § *Language*, che è il record. Questi documenti sono un arretrato in
italiano che la Fase 0b converte e che non blocca niente.

## Cosa aprire

| serve | apri |
|---|---|
| eseguire un passo del ciclo | questo file |
| scrivere o correggere un prompt, applicare le voci, attraversare un confine | `workflow/CYCLE.md` |
| il gate del passo 4, la forma delle voci, gli scarti | `workflow/CONFORMANCE.md` + `assets/improvement-template.md` |
| il passo 9, i contatori, cosa il veto legge per primo | `assets/report-template.md` |
| i passi 6 e 7, dormienza, verdetti falsificati | `workflow/LEDGER.md` + `REGRESSION-LEDGER.md` § *How to use* |
| sapere **perché** una decisione è stata presa così | `workflow/RATIONALE.md` |
| sapere **quanto** lo strumento ha già dimostrato, e cosa non copre | `workflow/EVIDENCE.md` |
| il lavoro che resta e in che ordine | `CONSENSUS-WORKFLOW-PLAN.md` § *Rotta* |

## Cosa decide, e con quale errore

Poter modificare `SKILL.md` e accorgersi quando la modifica ha **peggiorato** lo skill. Serve un
**segno con un errore noto**, non un numero: niente soglie, niente formula di aggregazione, niente
score calibrato.

L'obiettivo si regge su **due meccanismi disgiunti, con due prove diverse**:

- **`REGRESSION-LEDGER.md` rileva il peggioramento, ex-post, sulle dimensioni che copre.** È l'unico
  rilevatore in servizio. Copertura misurata: 40 clausole su 205.
- **L'intersezione fra `improve` e `review` previene il peggioramento, ex-ante, su una classe sola:
  le regole false.** È un generatore di proposte con un filtro di precisione sulle proposte. Che il
  filtro sia preciso è **un'ipotesi non ancora verificata**; CON-6 è il suo primo test, e una sua
  falsificazione **non fa cadere l'obiettivo** — fa cadere l'economia con cui si decide cosa applicare.

Lo strumento è **asimmetrico**: con una generazione per modello per ciclo e la regola *«un'affermazione
regge solo se regge su entrambi»*, basta 1 violazione su 2 per falsificare e servono 0 su 2 per
confermare. Il primo lato è solido, il secondo è assenza di controesempio su un campione di due — da
cui lo stato `non smentita ×k` invece di `tiene`, e la leva del **tempo invece del campione**. Il
ragionamento per esteso, con la varianza misurata su CON-5, sta in `workflow/RATIONALE.md` §
*L'obiettivo*.

## Vocabolario

- **Consenso** qui significa **intersezione fra giudizi indipendenti**, mai mediazione né terzo
  giudizio. Due modelli concordi **e ugualmente specifici** sono la ragione più economica per
  applicare una modifica; due modelli discordi mandano il punto alla lettura umana, non a un arbitro.
- **`CON-N`** nei nomi degli artefatti nasce come «con la skill attiva», in opposizione a una
  baseline generata senza skill, prodotta solo alla prima iterazione. Oggi è di fatto il **contatore
  di ciclo**, ed è citato in questa forma da ogni cella `Misurato su` di `REGRESSION-LEDGER.md`. Resta
  così; una eventuale nuova generazione senza skill prenderà un token distinto.
- **Ciclo parziale.** CON-5 non ha artefatti `IMPROVEMENT` né `REVIEW`: si è fermato alla generazione,
  e i suoi verdetti nascono da lettura offline. Il token non si riusa comunque — nove righe del
  registro e due citazioni testuali lo referenziano, e riusarlo le renderebbe ambigue.
- **Fasi** del ciclo: `improve`, `review`, `verdetto`, `recidiva`. `ledger` indica **solo il
  registro**, mai una fase: prima nominava un file, una fase e due lavori diversi.
- **`non smentita ×k`** è lo stato di una riga del registro che k cicli consecutivi non hanno
  falsificato su nessuno dei due piani. Sostituisce `tiene`, che prometteva conferma.
- **Riga dormiente.** Una riga a `non smentita ×3` passa dormiente: verificata 1 ciclo su 3 anziché
  ogni ciclo. Non si cancella e non esce dal registro. Torna attiva immediatamente se `recidiva` la
  risolleva.
- **Recidiva** è la quota dei difetti sollevati da `improve` che ricadono su un tema coperto da una
  riga del registro. Se è sistematicamente maggiore di zero, il registro sta mentendo su ciò che
  dichiara chiuso. È anche il segnale che risveglia le righe dormienti, cioè ciò che rende sicura la
  dormienza.
- **`Origine`** di una riga: `intersezione` (tema **e** rimedio condivisi), `intersezione-tema` (tema
  condiviso, rimedio da un lato solo), `giudizio` (un lato solo, o umano), `potatura` (rimozione).

## Il ciclo

1. **Generazione.** Ogni modello produce un piano dalle sole fonti in `recipe-app/sources/`:
   `recipe-app/results/PLAN-CC-CON-N.md` e `recipe-app/results/PLAN-CX-CON-N.md`.
2. **Validazione strutturale.** `make validate PLAN=…` su entrambi. Il validator non esprime giudizi
   semantici.
3. **`improve`.** Ogni modello riceve un payload cieco — `SKILL.md`, `EVALUATION-BRIEF.md`, le fonti,
   i due candidati **rinominati** `CANDIDATE-A.md`/`CANDIDATE-B.md`, l'indice delle clausole e le
   affermazioni del registro — e produce un piano di miglioramento dello skill sui difetti osservati
   in **entrambi** i candidati, nella forma di `assets/improvement-template.md`. Le ultime due voci
   sono ciò che il contratto chiede per `Covering rows` e `Merged claim`, e la loro conseguenza sulla
   `recidiva` è dichiarata in `prompts/improve.prompt.md`.
4. **Gate di conformità.** `validate_improvement.py`. Una voce priva di un campo obbligatorio, o con
   un riferimento che non si risolve, viene **scartata e registrata**. Nessuna rigenerazione. Vedi
   `workflow/CONFORMANCE.md`.
5. **`review`.** Payload **cieco e simmetrico**: i due `IMPROVEMENT` come `Report A`/`Report B`,
   nessun «il tuo report». Ogni modello classifica ciascuna voce in condivisa, unica ad A, unica a B,
   contraddittoria; per ogni voce condivisa dichiara se i due lati portano **lo stesso rimedio** o
   solo lo stesso tema.
6. **`verdetto`.** Ogni riga attiva del registro viene verificata sui piani appena generati, con
   citazione obbligatoria del punto pubblicato che regge il verdetto. Un verdetto la cui citazione non
   si risolve viene scartato e registrato. Le righe dormienti entrano 1 ciclo su 3. **Le esecuzioni
   sono due e ciascuna giudica entrambi i piani**, quindi ogni riga porta quattro verdetti: strumenti
   concordi, il verdetto vale; strumenti discordi su un piano, la riga non cambia stato e va alla
   lettura umana — `workflow/LEDGER.md` § *Due strumenti di `verdetto`*.
7. **`recidiva`.** Una sola chiamata, modello fisso. Produce l'elenco delle coppie `voce improve →
   riga di registro | nessuna`, su **tutte** le righe, dormienti incluse. Non un numero: l'elenco.
8. **Applicazione.** Il workflow applica al working tree **solo ciò che il filtro licenzia** — le
   voci classificate condivise da **entrambi** i `REVIEW`. Una voce = **un hunk di `SKILL.md`** più
   ciò che il registro deve registrare: una riga nuova quando la modifica porta una previsione che
   nessuna riga attiva fa, il solo ri-ancoraggio delle righe coperte quando non la porta. Le righe
   nuove nascono con `Commit SKILL.md: (pending)`. **Il workflow non committa mai.** Cosa è
   automatico e cosa no: `workflow/CYCLE.md`.
9. **Report.** `recipe-app/results/CONSENSUS-CON-N.REPORT.md`, nella forma di
   `assets/report-template.md`, con i contatori **in testa**. È composizione degli artefatti del
   ciclo: nessuna chiamata. Gli artefatti prodotti dalle esecuzioni si spostano qui a questo passo,
   con i nomi veri; le directory di payload restano dove sono.
10. **Veto umano.** Si leggono i contatori, poi `git diff`. Si rifiuta il batch, o una voce per id.
    Ciò che sopravvive lo committa l'umano.

Esecuzioni per ciclo:

| fase | esecuzioni |
|---|---|
| generazione | 2 |
| `improve` | 2 |
| `review` | 2 |
| `verdetto` | 2 |
| `recidiva` | 1 |
| **totale** | **9**, di cui 7 dopo la generazione |

Qualifica obbligatoria dell'unità: in **Fase 2** un'esecuzione è una sessione agentica che può
delegare internamente; in **Fase 5** ogni delega è una chiamata contata dal dry-run, ed è quel numero
che `evals/AGENTS.md` chiede di autorizzare. Dire «sei chiamate a ciclo» senza qualificare l'unità era
falso in entrambi i regimi: i prompt di CON-1…CON-5 — `472233d:PROMPTS.md`, rimossi dal working tree
il 2026-08-07 — delegavano a due sub-agent ciascuno.

I quattro prompt sotto `prompts/` **non prescrivono nessuna delega**: quante ne fa un'esecuzione lo
decide l'harness. Il vincolo che vale in entrambi i regimi è uno solo ed è scritto nei prompt — una
sessione delegata legge la stessa allowlist e niente altro. Il conteggio della tabella è quindi in
esecuzioni; la Fase 5 lo riporta in chiamate.
