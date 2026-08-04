# Grading di `plan-slices` — Piano di implementazione

## Obiettivo

Implementare le otto slice `NOW` di `GRADING-IMPROVEMENTS.md` senza modificare il contenuto degli
artefatti storici. Gli artefatti v1 e v2 sono archiviati rispettivamente sotto
`calibration-legacy/raw/` e `calibration-v2/raw/`. Il risultato è evaluator v3: preflight solo
strutturale, grading semanticamente calibrato, risoluzione auditabile dei disaccordi e scoring
scelto su fixture etichettate.

## Stato implementazione — 2026-08-04

- [x] **Slice 0 — Protezione baseline e versioning:** contratti/versioni v3, naming centralizzato,
  ripetizioni, metadata con manifest/label-set, resume hash-bound e protezione overwrite.
- [x] **Slice 1 — Preflight strutturale:** expectations eliminate; validator solo strutturale con
  `Themes.First validation` numerico; Make e preflight aggiornati; test di parafrasi inclusi.
- [x] **Slice 2 — Brief e anonimizzazione:** brief attivo, prompt assoluto/paired neutrali,
  alias validati, mapping confinato ai metadata, hash di brief/fonti/prompt/mapping registrati.
- [ ] **Slice 3 — Severità e critical failure:** rubric/grade contract e fixture di confine sono
  implementati e verificati offline; layout e raccolta shard-safe sono pronti. La raccolta provider è
  stata avviata e si è fermata a 15 unità valide su 36: 6 unità sono fallite perché i grader hanno
  violato il grade contract e 15 non sono state eseguite per fail-fast. Il checkpoint umano sulla
  scala dei verdict resta aperto e ora dipende anche da una decisione su contratto e budget.
- [ ] **Slice 4 — Un solo addebito:** contratto `primary_criterion` e validazioni principali sono
  implementati; restano fixture e test di accettazione. È la prossima slice perché congela lo schema
  grade prima di qualunque run pagata.
- [ ] **Slice 5 — Strumento relativo validato:** nuova, non iniziata. Scollegare paired da assoluto,
  eseguire a ordine invertito, comporre altre coppie dalle fixture esistenti e misurare il falso
  cambiamento sui criteri invarianti.
- [ ] **Slice 6 — Adjudication:** richiesta cieca, hash e risoluzione assoluta/paired sono parzialmente
  implementati; restano copertura completa di resume, critical failure paired e test end-to-end.
- [ ] **Slice 7 — Calibrazione assoluta etichettata:** manifest, nuove fixture, ripetizioni e report
  metriche sono implementati; mancano golden test completi, run provider e review umana del report.
  Assorbe le attività empiriche residue della slice 3.
- [ ] **Slice 8 — Scoring e rollout:** `scoring.py` espone formula corrente e shadow formula, ma
  selezione calibrata, run completa, `CALIBRATION.v3.json` e confronto before/after non sono fatti.

### Riordino del 2026-08-04

Le slice `NOW` sono state riordinate in `GRADING-IMPROVEMENTS.md` dopo la prima raccolta reale. La
misura relativa diventa Theme D con primo validatore alla slice 5; la misura assoluta diventa Theme E
e scende alla slice 7. Motivo: la domanda che l'evaluator serve è un before/after, e con agreement
inter-grader 0.56 sui verdetti assoluti la differenza fra due score è meno affidabile del confronto
diretto. La ex slice 4 resta al suo posto perché congela lo schema grade prima delle run pagate,
regola ora esplicita in `Ordering criteria`. Le attività empiriche della slice 3 — tre run per grader,
accuratezza e ripetibilità — passano alla slice 7; alla slice 3 restano contratto, fixture e test
offline, che sono completi.

### Verifiche completate

- [x] `make test` rieseguito il 2026-08-04: 34 test offline passano.
- [x] Le sei fixture v3 di confine passano il validator strutturale.
- [x] Il manifest v3 passa la validazione con denominatori zero resi come `null`.
- [x] Dry-run `grade` e `compare` su fixture v3 valide e `calibrate` completati senza provider o
  scritture; i candidati storici `PLAN-*-CON-5.md` non passano il validator v3.
- [x] Dry-run `calibrate-critical` completato senza provider o scritture: 36 chiamate assolute,
  zero paired e zero adjudication; report diagnostico separato dalla calibrazione completa.
- [x] Quattro dry-run shard: 9 chiamate e 18 target ciascuno, unione 36/72, intersezione zero,
  nessun report condiviso e tutti i target macchina sotto `calibration-v3/raw/`.
- [x] Smoke test su provider reali: `boundary-absent` run-01 per Claude e per Codex completati e poi
  ripresi con `RESUME=1` senza nuove chiamate. Lo structured output v3, incluso `pattern` su
  `candidate`, è accettato da entrambi i provider: il rischio schema residuo è chiuso.
- [x] Resume su artefatti reali verificato: 15 unità riprese senza chiamate; `calibrate-critical-report`
  rifiuta il join con `report-only requires every provider artifact to resume successfully` e non
  scrive nulla in `results/calibration-v3/`.
- [ ] Matrice 36/36 e checkpoint umano non completati. 21 delle 36 chiamate autorizzate sono state
  consumate; 15 restano autorizzate ma non bastano a chiudere le 21 unità mancanti.

### Slice 3 — attività residue e rischi

- **Verifica offline più recente — 2026-08-04:** `make test` conferma 34 test passanti (3 validator
  e 31 evaluator); le sei fixture `boundary-*` passano singolarmente il validator strutturale.
  Lo schema ora vieta evidenza controllante vuota per difetti e critical failure; il validator
  continua a richiederla dinamicamente per ogni criterio non-pass. I test coprono layout, staging,
  shard, resume completo e pubblicazione offline del report. `make calibrate-critical DRY_RUN=1`
  conferma la matrice 36/0/0 e non crea artefatti. Nessun artefatto provider v3 è disponibile per
  confrontare accuratezza o ripetibilità.
- **Riverifica pre-run — 2026-08-04:** ripetuti i quattro dry-run shard (9 unità ciascuno, unione 36,
  intersezione vuota, nessun report negli shard); `make calibrate-critical-report` senza artefatti
  fallisce con `report-only requires every provider artifact to resume successfully` e non crea
  `results/calibration-v3/`, che resta inesistente: nessun rischio di overwrite. `probe_provider`
  verificato manualmente: `codex-cli 0.146.0` con `codex login status` OK e `claude 2.1.221` con
  `claude auth status` `loggedIn: true` anche dentro la sandbox; il falso negativo precedente non si
  riproduce. I flag CLI usati (`codex exec --ephemeral/--output-schema/...`,
  `claude --safe-mode/--json-schema/--effort/...`) esistono nelle versioni installate e
  `provider_command` è invariato rispetto a v2, che ha prodotto run reali.
- **Rischio schema residuo:** rispetto a v2 lo schema assoluto v3 introduce `pattern` su `candidate`
  (`^candidate-[A-Z]$`); `const`, `minItems`, `maxItems` e `minLength` erano già usati in v2 con
  entrambi i provider. È l'unico costrutto mai esercitato contro un provider reale: se rifiutato
  dallo structured output, fallirebbero tutte le chiamate. Mitigazione senza sprechi: autorizzare
  prima due sole unità (`SHARD_COUNT=36 SHARD_INDEX=1` claude, `SHARD_INDEX=4` codex), validarne gli
  artefatti e poi eseguire il resto con `RESUME=1`, che riusa i due grade già scritti.
- **Nota metadata:** senza `SKILL_COMMITS` i comandi registrano `--candidate-skill-commit unknown`.
  È corretto per le fixture `boundary-*`, scritte a mano e non generate dalla skill.
- [x] Copertura offline per evidenza incompleta, uso improprio di `absent` e critical failure senza
  condizioni, esclusioni o citazioni.
- [x] Validazione strutturale delle sei fixture di confine e suite offline completa.
- [ ] Eseguire almeno tre run per grader sulle fixture di confine. Parzialmente eseguito il
  2026-08-04 con autorizzazione esplicita a 36 chiamate: nessuna fixture ha tre run complete per
  entrambi i grader e due fixture non hanno alcun dato.
- [ ] Confrontare accuratezza e ripetibilità sui risultati reali, quindi svolgere il checkpoint umano
  che decide se mantenere i cinque verdict o versionare una scala semplificata. Le metriche parziali
  esistono ma non sono utilizzabili per il checkpoint: campione incompleto e distorto dagli scarti.

### Slice 3 — esito della raccolta provider del 2026-08-04

- **Consumo autorizzazione:** 21 chiamate su 36. Due smoke test più 19 chiamate negli shard, di cui
  13 hanno prodotto artefatti validi e 6 sono state rifiutate dopo la risposta del provider. Restano
  15 chiamate autorizzate contro 21 unità mancanti: la matrice non è chiudibile nell'autorizzazione
  corrente nemmeno se ogni chiamata residua andasse a buon fine.
- **Partizionamento:** sei shard `SHARD_COUNT=6`, unione 36, intersezione vuota, 72 target unici tutti
  sotto `calibration-v3/raw/`, nessun report negli shard. Il partizionamento ha funzionato: nessuna
  collisione, nessun overwrite, nessuno staging orfano. `CALIBRATION-CRITICAL.v3.json` non è stato
  generato e `results/calibration-v3/` contiene solo `raw/`.
- **Artefatti validi:** 15 unità, 30 file. `boundary-pass` 2 Claude + 3 Codex; `boundary-local`
  2 Claude + 3 Codex; `boundary-restructure` 1 Claude + 2 Codex; `boundary-absent` 1 Claude + 1 Codex.
  `boundary-severe` e `boundary-safety` hanno zero unità.
- **Failure di contratto, non di trasporto:** i sei scarti sono grade sintatticamente validi che
  violano il grade contract v3. Tre modalità distinte:
  `absent is only valid for a totally missing element` (2 volte, entrambe Claude: `severity: absent`
  con `element_absent: false`); `non-pass requires a defect` (1 volta, Claude: criterio non-pass con
  `defect_ids` vuoto); `may be charged only to its primary criterion` (3 volte, tutte Codex: un
  criterio cita un difetto il cui `primary_criterion` è un altro criterio).
- **Il prompt enuncia già le tre regole** (`grade_plan.py`, blocco `Rules`). Gli scarti sono
  non-conformità dei grader, non istruzioni mancanti. Resta però un'ambiguità reale sulla terza:
  il prompt dice di addebitare il difetto a un solo `primary_criterion`, mentre il validator vieta
  anche la semplice citazione da un altro criterio. Le tre regole sono vincoli cross-field che lo
  structured output schema non può esprimere, quindi vengono intercettate solo a valle della chiamata.
- **Amplificazione fail-fast:** un solo grade rifiutato interrompe l'intero shard. Sei scarti hanno
  bloccato 15 unità mai tentate; lo shard 3 ha perso 5 unità su 6 per un rifiuto alla prima. È la
  causa principale della bassa resa, non il tasso di rifiuto in sé (6 su 19, circa 32%).

### Slice 3 — metriche parziali, non valide per il checkpoint

Calcolate con `calibration_report.build_report` sulle 15 unità disponibili e scritte solo in
scratchpad; non pubblicate come `CALIBRATION-CRITICAL.v3.json`.

| Metrica | Valore | Numeratore/Denominatore |
|---|---|---|
| Accuratezza vs label, complessiva | 0.5949 | 232/390 |
| Accuratezza Claude | 0.4744 | 74/156 |
| Accuratezza Codex | 0.6752 | 158/234 |
| Intra-grader esatto | 0.7308 | 171/234 |
| Intra-grader entro un livello | 0.8590 | 201/234 |
| Inter-grader esatto | 0.5615 | 219/390 |
| Inter-grader entro un livello | 0.7974 | 311/390 |
| Critical failure precision | 0.3077 | 4/13 |
| Critical failure recall | 1.0000 | 4/4 |
| Primary criterion corretto | 0.1186 | 21/177 |
| Paired direction | null | 0/0, fuori scope |

- **Perché non sono utilizzabili:** il campione copre 4 fixture su 6 ed è sbilanciato fra provider
  (6 unità Claude contro 9 Codex); mancano del tutto `boundary-severe` e `boundary-safety`, cioè
  proprio i confini alti della scala che il checkpoint deve giudicare. Soprattutto, gli scarti non
  sono casuali: le risposte che violavano il contratto sono state eliminate, quindi le metriche
  descrivono il sottoinsieme conforme e sovrastimano la disciplina dei grader.
- **Segnali comunque annotabili, da confermare su matrice completa:** precision dei critical failure
  bassa con recall pieno indica sovra-attivazione; l'accuratezza del `primary_criterion` sotto 0.12
  è coerente con i tre scarti Codex sulla regola dell'addebito unico e riguarda direttamente la
  slice 4; `theme_independent_value`, `uncertainty_conflicts` e `slice_single_owner` sono i criteri
  con accordo peggiore.
- **Attività offline residue:** nessuna nota per la slice 3. Il join reale resta impossibile finché
  non esistono i 72 artefatti GRADE/SCORE prodotti dalle run autorizzate.
- **Rischio:** finché run e checkpoint restano aperti, la distinzione tra `minor`, `material`,
  `severe` e `absent` è verificata contrattualmente ma non calibrata sul comportamento dei grader;
  le run pagate non devono partire prima che lo schema grade sia congelato.
- **Rischio — costo delle non-conformità:** ogni grade rifiutato è una chiamata già pagata che non
  produce artefatto. Con l'attuale rigidità del contratto e il fail-fast, completare la matrice costa
  più delle 36 chiamate preventivate. Qualunque rilassamento del contratto o modifica di prompt o
  rubric cambia gli hash e invalida il resume delle 15 unità già raccolte, che andrebbero ripagate.
- **Rischio — invalidazione retroattiva:** le 15 unità valide sono legate a brief, fonti, rubric,
  prompt, modelli, effort e versioni CLI correnti. Vanno considerate consumate finché non si decide
  se il contratto resta invariato.
- **Rischio operativo:** i candidati storici `PLAN-*-CON-5.md` hanno `Themes.First validation` non
  numerico e falliscono correttamente il preflight v3; usarli richiede una nuova generazione, non la
  modifica degli artefatti immutabili.

### Slice 3 — remediation proposta

Proposte, non attività autorizzate: nessuna è decisa e nessuna va eseguita prima delle risposte in
`Open questions`. Sono scritte in prosa proprio per non confonderle con il lavoro approvato.

**Conservare gli output rifiutati.** `run_grader` valida prima di scrivere, quindi il grade non
conforme non raggiunge mai il file e l'orchestrator ripulisce lo staging vuoto: delle sei risposte
pagate resta solo la riga di errore. Salvarle sotto `raw/rejected/`, fuori dal set di resume e dal
join del report, costa nulla e conserva evidenza già pagata. Capire *come* i grader violano il
contratto è materiale della slice 3, non rumore operativo.

**Sostituire il fail-fast con un circuit breaker.** Il fail-fast va conservato per il caso sistemico
— schema rifiutato, autenticazione rotta, configurazione errata — dove proseguire brucerebbe ogni
unità dello shard. Non serve invece per una non-conformità della singola risposta, che non dice nulla
sull'unità successiva. Regola proposta: proseguire dopo una violazione di contratto, abortire lo
shard dopo due o tre fallimenti consecutivi. Sarebbe bastato a recuperare gran parte delle 15 unità
mai tentate.

**Non rilassare il contratto, correggere il prompt.** La regola dell'addebito unico è portante: se un
criterio potesse citare un difetto di un altro, quel difetto influenzerebbe due verdict, cioè il
doppio addebito che la v3 esiste per vietare, e la slice 4 perderebbe il proprio invariante.
Degradarla ad avvertimento non è raccomandato. Il problema è che il prompt descrive le regole in
termini di concetti mentre il validator le applica ai campi; riformularle meccanicamente:
`defect_ids` di un criterio può contenere solo difetti il cui `primary_criterion` è quel criterio;
`severity: absent` se e solo se `element_absent: true`; ogni criterio non-pass elenca almeno un
`defect_id`. Sono vincoli cross-field che lo structured output schema non può esprimere, quindi il
prompt resta l'unico punto di controllo prima della spesa.

**Perché non completare la matrice con il prompt attuale.** Ritentare le unità fallite finché la
risposta è conforme è un filtro di qualità silenzioso: le fixture su cui un grader tende a violare
verrebbero ricampionate finché non obbedisce, e la baseline misurerebbe i grader quando si comportano
bene. È lo stesso difetto che rende inutilizzabili le metriche parziali di oggi, esteso a tutte e 36
le unità, e colpisce proprio accuratezza, ripetibilità e correttezza del `primary_criterion`. Il tasso
di conformità al contratto va trattato come metrica di prima classe, non come scarto operativo.

**Sequenza proposta.** Primo, applicare quarantena, circuit breaker e prompt: sono modifiche offline a
costo zero. Secondo, uno smoke da due chiamate sul prompt corretto, mirato ai due modi di fallimento
osservati — Claude su `boundary-restructure` per l'uso improprio di `absent`, Codex su
`boundary-severe` per la citazione incrociata. Terzo, decidere il budget in base a quell'esito e non
prima. Lo smoke è il test decisivo più economico disponibile: se la non-conformità persiste anche con
il prompt corretto, il problema non è la formulazione ma la richiesta, e diventa un argomento
concreto per la scala semplificata al checkpoint.

**Ordini di grandezza.** Con la resa osservata di 13 unità valide su 19 chiamate, completare le 21
unità mancanti con il prompt attuale costa circa 31 chiamate; ricollezionare tutte e 36 con il prompt
corretto ne costa circa 40 se la resa sale attorno al 90%. La differenza di costo è modesta rispetto
alla differenza di qualità della baseline.

**Vincolo operativo se il prompt cambia.** Le 15 unità valide vanno archiviate sotto un prefisso
pilota prima di rilanciare. Con gli hash cambiati il resume le rifiuta e senza resume `check_targets`
si rifiuta di sovrascrivere: in entrambi i casi il preflight aborta. Non vanno cancellate: hanno
comprato il dato di conformità, circa il 68%, con modi di fallimento distinti per provider.

### Slice 3 — checkpoint esterno residuo

- [x] **Prerequisito — riorganizzare artefatti e script:** collocare i file macchina v3, inclusi
  `*.GRADE.json`, `*.SCORE.json`, metadata e staging, sotto una directory dedicata come
  `recipe-app/results/calibration-v3/raw/`. Lasciare nella directory principale solo report e
  artefatti destinati alla lettura umana; conservare immutato il contenuto degli artefatti storici.
- [x] **Aggiornamento script:** centralizzare il nuovo layout nei path builder e adeguare orchestrator,
  artifact store, resume, discovery del report, Makefile, documentazione e test. Conservare naming
  versionato, scrittura atomica, hash, protezione overwrite e riuso futuro dei 36 grade.
- [x] **Verifica offline del layout:** testare target unici, staging confinato, resume e report sui
  nuovi path; verificare che nessun artefatto macchina v3 venga scritto direttamente in `results/`.
- [x] **Archivio storico:** spostati senza modificarne il contenuto 4 artefatti v2 in
  `calibration-v2/raw/` e 16 artefatti v1 in `calibration-legacy/raw/`; piani e artefatti umani
  restano direttamente in `results/`.
- [ ] **Run 36 chiamate provider:** avviato il 2026-08-04 con autorizzazione esplicita e subagent
  paralleli su shard disgiunti; interrotto a 15 unità valide. `CALIBRATION-CRITICAL.v3.json` non
  esiste. Nessuna slice successiva avviata.
- [x] **Smoke test prima delle 36:** eseguito con `SHARD_COUNT=36`, indici 1 e 4. Entrambi i provider
  hanno accettato lo structured output v3 e gli artefatti sono stati riusati da `RESUME=1` a costo
  nullo.
- [x] **Commit prima degli invii:** slice 0–3 sono committate; l'albero era pulito all'avvio del run,
  quindi i 15 artefatti sono legati a una revisione nota.
- [ ] **Decisione umana necessaria prima di riprendere:** servono tre risposte, nessuna delle quali è
  presa in questa sessione. Primo, se autorizzare le chiamate aggiuntive oltre le 36 necessarie a
  chiudere 21 unità con margine per le non-conformità. Secondo, se il grade contract deve restare
  invariato, rendere la citazione incrociata dei difetti un avvertimento anziché un errore, o
  chiarire il prompt; ogni modifica a prompt o rubric ripaga le 15 unità già raccolte. Terzo, se
  sostituire il fail-fast per shard con un proseguimento che marca la singola unità come fallita,
  così che una non-conformità non blocchi le unità indipendenti restanti.
- [x] **Partizionamento obbligatorio:** assegnare a ogni worker un insieme disgiunto di unità
  fixture/provider/run. Prima degli invii, i dry-run degli shard devono avere unione di 36 unità,
  intersezione vuota e target finali unici; un solo coordinatore genera il report dopo il join.
- [x] **Supporto shard:** `SHARD_COUNT`/`SHARD_INDEX` partizionano deterministicamente le sole unità
  provider senza creare report; `calibrate-critical-report` richiede il resume completo, non esegue
  probe o provider e pubblica un unico report atomico.

- **Scope approvato:** raccogliere solo i grade assoluti delle sei fixture `boundary-*` marcate
  `critical_subset: true`, con tre ripetizioni indipendenti per Codex e Claude: 6 × 3 × 2 = 36
  chiamate provider.
- **Scope differito alla slice 7:** le tre fixture non critiche aggiungono 6 chiamate assolute e il
  pair aggiunge 6 chiamate paired; per questo `make calibrate` completo produce 48 chiamate, non 36.
- [x] **Modalità di raccolta implementata:** `make calibrate-critical` filtra il manifest v3
  esistente sul subset critico, esegue solo unità assolute, esclude paired e adjudication e genera
  `CALIBRATION-CRITICAL.v3.json` dai grade grezzi.
- **Riuso:** non creare un manifest alternativo; mantenere hash del manifest, label-set e nomi
  `run-01`…`run-03`. La calibrazione completa potrà riprendere i 36 artefatti solo se versioni,
  input, prompt, CLI, modelli, effort e configurazione restano compatibili con i controlli resume.
- **Separazione dalla slice 6:** un disaccordo materiale non deve fermare la raccolta; richieste e
  resolution di adjudication saranno prodotte solo dopo che la matrice grezza è completa.
- [x] **Preflight obbligatorio:** il dry-run completo mostra esattamente 36 chiamate provider, zero
  paired e zero adjudication; quattro shard mostrano 9 chiamate ciascuno, unione completa e nessuna
  collisione; target, input e configurazione usano i default previsti.
- **Autorizzazione:** l'approvazione di questa strategia non autorizza ancora gli invii. Nella nuova
  sessione richiedere consenso esplicito dopo il dry-run perché le chiamate usano servizi esterni e
  possono consumare quota o generare costi.
- **Configurazione prevista:** usare i default correnti (`gpt-5.6-sol`/`high`,
  `claude-opus-5`/`high`, timeout 900 secondi), senza variarli nella matrice; registrare versioni CLI
  e tutti gli hash già previsti dai metadata.
- **Evidenza da consegnare:** accuratezza rispetto alle label per criterio/provider, agreement
  intra-grader sulle tre ripetizioni, agreement inter-grader sul prodotto delle run, precision/recall
  dei critical failure e distribuzione completa dei verdict per fixture.
- **Checkpoint umano:** esaminare report e disaccordi grezzi; confermare la scala a cinque verdict
  oppure richiedere una nuova versione della rubric al checkpoint della slice 7. Le soglie restano
  diagnostiche e non vanno inventate dopo aver visto i risultati.
- **Autenticazione Claude:** il 2026-08-04 `claude auth status` ha restituito `loggedIn: false` nella
  sandbox dell'agente e `loggedIn: true` fuori sandbox. È un falso negativo dovuto all'isolamento
  delle credenziali; ripetere il solo probe fuori sandbox prima di dichiarare il provider non
  autenticato, senza esporre dettagli dell'account.

## Decisioni di progetto

- `recipe-app/EVALUATION-BRIEF.md` sostituisce `REFERENCE-PLAN.md`; il reference v2 resta nella
  storia Git, non nell'evaluator attivo.
- Rubric, schema grade, scoring e manifest hanno versioni esplicite e indipendenti. Gli artefatti
  nuovi usano `.v3.`; i `*.v2.*` restano immutabili e non vengono ricalcolati o ripresi da v3.
- Prompt e output usano alias neutrali (`candidate-A`, `grader-1`); path, provider e mapping restano
  solo nei metadata non mostrati al grader o al revisore cieco.
- Le evidenze diventano strutturate: localizzazioni nel candidato ed evidenze controllanti da
  fonte/brief sono campi distinti e non vuoti.
- Un difetto appartiene a un solo `primary_criterion`. Effetti secondari non esistono in v3.
- I disaccordi limitati a `pass` ↔ `minor` non attivano adjudication; sono materiali solo quelli in
  cui almeno un verdict è `material`, `severe` o `absent`, oppure differisce un critical failure.
- Il workflow umano usa file JSON immutabili: richiesta cieca, resolution compilata dal revisore,
  grade/score risolti derivati in codice. Nessuna UI interattiva è necessaria.
- `grading_contract.py` conserva rubric e contratti grade/paired, che co-evolvono. Estrarre
  `scoring.py` e `adjudication_contract.py`: formula e adjudication hanno lifecycle e test distinti;
  provider runtime e artifact store restano invariati salvo i nuovi contratti.

## Contratti v3

| Contratto | Cambiamento principale |
|---|---|
| Rubric | Definizioni operative dei verdict; trigger, esclusioni, cap e citazioni richieste per ogni critical failure |
| Grade | Alias candidato; evidenza strutturata; `primary_criterion`; un solo criterio per difetto |
| Score | `rubric_version`, `scoring_version`, strategia, componenti e cap interamente derivati |
| Adjudication | Tipo `absolute`/`paired`, input hashati, soli elementi discordanti, resolution umana validata |
| Manifest | Fixture v3 autocontenute, label umane, ripetizioni, subset critico, paired e criteri invariati |
| Metadata | Hash di fonti, brief, rubric, prompt, candidati, configurazione, modello, effort, CLI e mapping alias |

## Sequenza di implementazione

### 0. Protezione della baseline e versioning — completata

**Modifiche**

- Aggiungere costanti/versioni v3 e impedire combinazioni tra rubric, schema, scoring e manifest
  incompatibili.
- Centralizzare la costruzione dei nomi artefatto; includere versione e, per calibrazione,
  `run-01`, `run-02`, ….
- Conservare lettura e verifica dei v2 solo nei test storici necessari; ogni comando attivo produce
  esclusivamente v3.
- Registrare nei metadata anche hash del manifest e label-set quando presenti.

**Test**

- Rifiuto di resume tra versioni o con qualunque hash/configurazione differente.
- Nessun overwrite dei v2; nomi distinti per ripetizioni dello stesso provider.
- Scrittura atomica e cleanup degli staging su failure invariati.

### 1. Preflight esclusivamente strutturale — completata

**Modifiche**

- Eliminare `recipe-app/expectations.json`, `scripts/derive_expectations.py`, relativo test, target
  Make, `--expectations`, JSON block del reference e documentazione operativa associata.
- Rimuovere da `skills/plan-slices/scripts/validate_plan.py` tutte le regole scenario-specifiche,
  regex e helper delle expectations.
- Conservare sezioni, ordine, tabelle, numerazione, tag, campi, liste e release finale.
- Rendere strutturale il riferimento `Themes.First validation`: deve indicare un numero di slice
  NOW esistente; non confrontare titolo o contenuto.
- Semplificare `make validate` a una sola invocazione del validator; l'orchestrator continua a
  eseguire lo stesso controllo nel preflight.

**Test**

- Eliminare i test expectations; aggiungere test per riferimento numerico valido, mancante e fuori
  range.
- Aggiungere due piani equivalenti con sinonimi/parafrasi: stesso esito strutturale.
- Test orchestrator: invalido si ferma prima del provider; valido crea sempre unità di grading.
- Verifica repository: nessun modulo, CLI, fixture attiva, Make target o documento operativo usa
  expectations.

### 2. Brief valutativo e anonimizzazione — completata

**Modifiche**

- Creare `recipe-app/EVALUATION-BRIEF.md` con sole sezioni:
  `Authority`, `Hard constraints`, `Accepted alternatives`, `Known conflicts`. Ogni voce cita file e
  sezione della fonte; nessun titolo/ordine/numero ideale o example evidence.
- Eliminare `REFERENCE-PLAN.md` dall'evaluator attivo e rinominare ovunque `reference` in `brief`:
  Makefile, CLI, prompt, metadata, artifact validation, test e documentazione.
- Passare al prompt il contenuto con intestazioni neutre (`Source 1`, `Evaluation brief`,
  `Candidate A`), mai path o nome del generatore.
- Far restituire al modello l'alias, poi validarlo; salvare alias→path e provider solo nei metadata.
- Aggiornare prompt assoluto e paired alle nuove classi di autorità.

**Test**

- Snapshot prompt senza `PLAN-CX`, `PLAN-CC`, `codex`, `claude`, path locali o decomposizione ideale.
- Mutando alias/path non cambia il payload semantico inviato.
- Piano con decomposizione alternativa source-supported non riceve vincoli di exact matching.
- Metadata e resume rilevano variazioni di brief, fonti, mapping e prompt.

### 3. Severità e critical failure operativi — parziale, checkpoint aperto

**Modifiche**

- [x] Portare la rubric a v3 e codificare per ogni verdict definizione, condizioni operative ed esempi di
  confine non scenario-specifici:
  `pass`; `minor` locale; `material` richiede ristrutturazione; `severe` invalida outcome/release o
  sicurezza; `absent` significa elemento non valutabile perché totalmente mancante.
- [x] Ampliare ogni critical failure con condizioni sufficienti, esclusioni e tipi di citazione
  richiesti. Violare un hard constraint non attiva automaticamente failure o cap.
- [x] Sostituire gli array di stringhe ambigui con `candidate_evidence` e
  `controlling_evidence`; richiedere entrambi per verdict non-pass e critical failure.
- [x] Aggiungere fixture v3 di confine isolate per correzione locale, split/merge/riordino, outcome
  invalidato, safety boundary e assenza totale.
- [x] Lasciare temporaneamente invariata la formula corrente per isolare il cambio semantico.

**Test e checkpoint**

- [x] Schema e validator rifiutano evidenza incompleta, `absent` usato come grave generico e critical
  failure senza condizioni/citazioni.
- [ ] Eseguire almeno tre run per grader sulle fixture di confine. Parziale: 15 unità su 36, nessuna
  fixture con copertura completa, `boundary-severe` e `boundary-safety` senza dati.
- [ ] Confrontare accuratezza sulle label e ripetibilità. Al checkpoint della slice 7 decidere se mantenere i
  cinque verdict o semplificare la scala; un cambio incrementa nuovamente la versione rubric. Le
  metriche parziali sono registrate ma non sufficienti a decidere.

### 4. Un solo addebito per difetto — parziale

**Modifiche**

- Sostituire `primary_axis` e `criterion_ids` con `primary_criterion`.
- Aggiungere a ogni difetto `consequence`, `severity`, evidenza candidato ed evidenza controllante.
- Ogni difetto è referenziato da esattamente un criterio; ogni criterio non-pass ha almeno un
  difetto; il verdict del criterio coincide con la severità peggiore dei propri difetti.
- Derivare l'axis dal criterio; eliminare logica e prompt degli effetti secondari.
- Tenere separati difetti con conseguenze indipendenti, anche nella stessa area del piano.

**Test**

- Rifiuto di difetti senza criterio, dangling, non referenziati, duplicati o addebitati a più
  criteri.
- Backup/spend guardrail mancanti incidono su un solo criterio per root defect.
- Un merge consultazione/scrittura non può abbassare tre criteri tramite lo stesso defect id.
- Due difetti realmente distinti sullo stesso criterio restano validi e il peggiore determina il
  verdict.

### 5. Strumento relativo validato — non iniziata

**Modifiche**

- Rimuovere da `_paired_prerequisites` la dipendenza delle unità paired dagli artefatti assoluti
  risolti; `render_comparison_prompt` riceve già solo rubric, fonti, brief e i due candidati, quindi
  il legame è di provenienza e non semantico. Conservare la registrazione della provenienza dove
  esiste davvero.
- Aggiungere l'esecuzione a ordine invertito come unità distinta, con nome artefatto e metadata che
  registrano quale candidato occupava la posizione A.
- Comporre nuove coppie nel manifest dalle fixture `boundary-*` esistenti, come già fa
  `learning-evidence-improvement`, etichettando direzioni attese e `invariant_criteria`.
- Estendere `calibration_report.py` con tasso di falso cambiamento sui criteri invarianti, stabilità
  fra i due ordini e agreement inter-grader sulla direzione, ciascuno con numeratore e denominatore.
- Applicare qui la remediation della slice 3: quarantena delle risposte rifiutate, circuit breaker al
  posto del fail-fast e regole del prompt enunciate sui campi.

**Test e checkpoint**

- Golden test delle nuove metriche con classi assenti, ordini sbilanciati e provider sbilanciati.
- Un'unità paired si esegue e riprende senza alcun artefatto assoluto presente.
- L'inversione dell'ordine produce un target distinto e non collide con l'ordine diretto.
- Checkpoint: falso cambiamento e stabilità fra ordini decidono se lo strumento relativo basta per
  giudicare le modifiche alla skill e con quale profondità serve ancora la calibrazione assoluta.

### 6. Adjudication assoluta e paired — parziale

**Modifiche**

- Aggiungere un'unità di adjudication assoluta dopo i due grade di ogni candidato e prima del paired.
- Definire trigger deterministici per criteri materialmente discordanti e critical failure
  discordanti; non usare differenze di score, perché sono derivate e dipendono dalla formula.
- Generare due artefatti atomici:
  - richiesta cieca con alias, soli criteri/failure discordanti, evidenze concorrenti e hash input;
  - metadata separati con mapping alias→provider/path, non consegnati al revisore.
- Estendere `adjudicate.py` con comandi `request` e `resolve`. `resolve` accetta una resolution umana,
  impedisce modifiche ai criteri concordi e produce `<candidate>.v3.RESOLVED.GRADE.json` e
  `.RESOLVED.SCORE.json`.
- Per criteri concordi, preservare il verdict e unire deterministicamente le osservazioni aliasate;
  per quelli discordanti, accettare solo verdict, difetti, motivazione ed evidenza della resolution.
- Applicare lo stesso contratto al paired: direction risolta, mai media di score/direzioni.
- Se non esiste disaccordo materiale, derivare automaticamente gli artefatti resolved. Se esiste,
  il comando termina `pending-review`; dopo la resolution, `RESUME=1` valida gli hash e prosegue.

**Test**

- `PLAN-CC-CON-5`: richiesta assoluta limitata ai criteri discordanti; fixture di resolution produce
  un solo grade e score risolti.
- Un criterio concorde modificato dalla resolution viene rifiutato.
- Resolution stale dopo modifica di grade, brief, rubric o fonti viene rifiutata.
- Nessun provider/mapping compare nella richiesta cieca.
- Resume copre: agreement automatico, pending umano, resolution completa e paired successivo.

### 7. Calibrazione assoluta etichettata — parziale

**Modifiche**

- Creare manifest e fixture v3 nuove; non modificare le fixture già usate. Le nuove fixture sono
  autocontenute: niente `preserve reference` o dipendenze implicite da un piano ideale non inviato.
- Coprire almeno: omissioni operative, conflitti pre-decisi, alternative accettate, learning senza
  osservazione, ownership condivisa, conseguenze duplicate e confini di severità.
- Etichettare ogni fixture con verdict ammessi per criterio, primary criterion ammessi per il difetto
  isolato, critical failure attese/assenti e provenance della review umana.
- Etichettare ogni pair con direzioni attese e criteri invariati.
- Aggiungere `runs` per fixture/pair e almeno tre ripetizioni per provider sul subset critico; il
  manifest materializza unità e nomi distinti.
- Ampliare `calibration_report.py` con:
  accuratezza vs label; intra-grader; inter-grader; precision/recall critical failure; primary
  criterion; paired direction; stabilità dei criteri invariati. Ogni metrica espone numeratore,
  denominatore, distribuzione per criterio/provider e versioni complete.
- Mantenere `thresholds_enforced: false`; campioni mancanti producono `null` con denominatore zero.

**Test e checkpoint**

- Validazione manifest: id/path unici, label complete, run positive, fixture strutturalmente valide.
- Metriche golden includono successi, errori, classi assenti, più run e provider sbilanciati.
- Intra-grader usa coppie dello stesso provider; inter-grader usa il prodotto delle run, senza pairing
  arbitrario per indice.
- Review umana di label e report prima di scegliere lo scoring.

### 8. Formula di scoring calibrata e rollout — non completata

**Modifiche**

- Estrarre funzioni pure in `scoring.py`. Calcolare in shadow mode almeno:
  axis worst-criterion ponderato attuale, media dei criteri per asse e sole varianti motivate dalle
  fixture.
- Applicare gli stessi critical-failure cap a ogni strategia candidata.
- Nel report confrontare direzione/rank attesi, separazione forti-critici, spread e discontinuità;
  documentare i casi che distinguono le formule.
- Al checkpoint scegliere una sola strategia, registrarla con `scoring_version`, e rendere il campo
  obbligatorio in rubric, score, resume e report.
- Rieseguire matrice assoluta e paired completa; pubblicare `CALIBRATION.v3.json` e confronto
  before/after. Non riscrivere score storici.
- Aggiornare `EVAL-WORKFLOW.md`, `recipe-app/README.md`, Makefile e help con brief, v3,
  ripetizioni, pending review, resolve e interpretazione dei resolved.

**Test finali**

- Golden test di ogni formula, rounding, pesi e cap.
- `make test` completamente offline.
- Dry-run di `grade`, `compare` e `calibrate`: file inviati, alias, versioni e output corretti.
- Run completa con provider autorizzati; resume senza nuove chiamate; modifica di un input invalida
  solo gli artefatti dipendenti.
- Audit manuale: nessun giudizio semantico nel validator, nessun score/direction scelto dal modello,
  nessuna identità del generatore nei payload ciechi.

## Strategia di consegna

Ogni slice forma un commit revertibile. Le slice 5, 6, 7 e 8 terminano con il relativo decision
checkpoint prima di iniziare il contratto successivo. I risultati v3 intermedi restano separati per
versione/configurazione e non diventano baseline canonica finché la slice 8 non è approvata.

## Rischi

- Il brief può essere troppo povero o prescrittivo: review umana e fixture di alternative accettate
  ne controllano entrambi gli estremi.
- L'adjudication umana aumenta latenza: il trigger esclude divergenze solo locali e il payload mostra
  esclusivamente il disaccordo.
- Tre run moltiplicano costo e durata: limitarle al subset critico finché la baseline non giustifica
  copertura più ampia.
- Fixture isolate semplificano il matching del difetto primario ma possono non rappresentare piani
  realistici; affiancare almeno due candidati completi senza usarli per inferire regole nuove.

## Open questions

- Il checkpoint umano mantiene i cinque verdict o richiede una scala semplificata e una nuova rubric?
  La decisione blocca la slice 7 e resta non anticipabile: la matrice è ferma a 15 unità su 36 e i
  due confini alti della scala non hanno alcun dato.
- Si autorizzano chiamate provider oltre le 36 iniziali? Ne servono almeno 21 per le unità mancanti,
  più un margine per le non-conformità, e ne restano 15 autorizzate.
- Il grade contract resta invariato o la citazione di un difetto da un criterio diverso dal suo
  `primary_criterion` smette di essere un errore fatale? Ogni modifica a contratto, prompt o rubric
  invalida il resume delle 15 unità già pagate.
- Il fail-fast per shard resta, o una singola unità non conforme viene marcata fallita lasciando
  proseguire le unità indipendenti dello stesso shard? Ora è collocata nella slice 5, che è la prima
  a spendere chiamate dopo il riordino.
