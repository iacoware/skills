# Grading di `plan-slices` — Piano di implementazione

## Obiettivo

Implementare le sette slice `NOW` di `GRADING-IMPROVEMENTS.md` senza modificare il contenuto degli
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
  implementati e verificati offline; layout e raccolta shard-safe sono pronti. Mancano soltanto le
  tre run per grader e il checkpoint umano sulla scala dei verdict.
- [ ] **Slice 4 — Un solo addebito:** contratto `primary_criterion` e validazioni principali sono
  implementati; restano fixture/test di accettazione completi dopo il checkpoint della slice 3.
- [ ] **Slice 5 — Adjudication:** richiesta cieca, hash e risoluzione assoluta/paired sono parzialmente
  implementati; restano copertura completa di resume, critical failure paired e test end-to-end.
- [ ] **Slice 6 — Baseline etichettata:** manifest, nuove fixture, ripetizioni e report metriche sono
  implementati; mancano golden test completi, run provider e review umana del report.
- [ ] **Slice 7 — Scoring e rollout:** `scoring.py` espone formula corrente e shadow formula, ma
  selezione calibrata, run completa, `CALIBRATION.v3.json` e confronto before/after non sono fatti.

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
- [ ] Run provider, resume su artefatti reali e checkpoint umano non eseguiti; nessuna autorizzazione
  agli invii è stata concessa in questa sessione.

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
- [ ] Eseguire almeno tre run per grader sulle fixture di confine; richiede autorizzazione esplicita
  perché invoca provider esterni o a pagamento. Non eseguito durante la ripresa.
- [ ] Confrontare accuratezza e ripetibilità sui risultati reali, quindi svolgere il checkpoint umano
  che decide se mantenere i cinque verdict o versionare una scala semplificata; bloccato fino alle
  run autorizzate.
- **Attività offline residue:** nessuna nota per la slice 3. Il join reale resta impossibile finché
  non esistono i 72 artefatti GRADE/SCORE prodotti dalle run autorizzate.
- **Rischio:** finché run e checkpoint restano aperti, la distinzione tra `minor`, `material`,
  `severe` e `absent` è verificata contrattualmente ma non calibrata sul comportamento dei grader;
  la slice 4 non deve avanzare.
- **Rischio operativo:** i candidati storici `PLAN-*-CON-5.md` hanno `Themes.First validation` non
  numerico e falliscono correttamente il preflight v3; usarli richiede una nuova generazione, non la
  modifica degli artefatti immutabili.

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
- [ ] **Prossimo run — 36 chiamate provider:** soltanto dopo il prerequisito, i test e un nuovo
  preflight, ottenere autorizzazione esplicita, raccogliere i grade assoluti con subagent paralleli
  e completare `CALIBRATION-CRITICAL.v3.json`; non avviare slice 4. Preflight e probe provider sono
  stati ripetuti il 2026-08-04 e sono verdi: manca solo l'autorizzazione agli invii.
- [ ] **Smoke test consigliato prima delle 36:** due chiamate singole (una per provider) con
  `SHARD_COUNT=36`, per esercitare lo structured output v3 su provider reali. Gli artefatti prodotti
  fanno parte delle 36 e vengono riusati da `RESUME=1`; il costo aggiuntivo è nullo.
- [ ] **Commit prima degli invii:** slice 0–3 sono interamente non committate. Committare prima del
  run lega i 36 artefatti a una revisione nota e impedisce che una modifica successiva a brief,
  rubric, prompt o fixture invalidi il resume degli artefatti già pagati.
- [x] **Partizionamento obbligatorio:** assegnare a ogni worker un insieme disgiunto di unità
  fixture/provider/run. Prima degli invii, i dry-run degli shard devono avere unione di 36 unità,
  intersezione vuota e target finali unici; un solo coordinatore genera il report dopo il join.
- [x] **Supporto shard:** `SHARD_COUNT`/`SHARD_INDEX` partizionano deterministicamente le sole unità
  provider senza creare report; `calibrate-critical-report` richiede il resume completo, non esegue
  probe o provider e pubblica un unico report atomico.

- **Scope approvato:** raccogliere solo i grade assoluti delle sei fixture `boundary-*` marcate
  `critical_subset: true`, con tre ripetizioni indipendenti per Codex e Claude: 6 × 3 × 2 = 36
  chiamate provider.
- **Scope differito alla slice 6:** le tre fixture non critiche aggiungono 6 chiamate assolute e il
  pair aggiunge 6 chiamate paired; per questo `make calibrate` completo produce 48 chiamate, non 36.
- [x] **Modalità di raccolta implementata:** `make calibrate-critical` filtra il manifest v3
  esistente sul subset critico, esegue solo unità assolute, esclude paired e adjudication e genera
  `CALIBRATION-CRITICAL.v3.json` dai grade grezzi.
- **Riuso:** non creare un manifest alternativo; mantenere hash del manifest, label-set e nomi
  `run-01`…`run-03`. La calibrazione completa potrà riprendere i 36 artefatti solo se versioni,
  input, prompt, CLI, modelli, effort e configurazione restano compatibili con i controlli resume.
- **Separazione dalla slice 5:** un disaccordo materiale non deve fermare la raccolta; richieste e
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
  oppure richiedere una nuova versione della rubric prima di iniziare la slice 4. Le soglie restano
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
- [ ] Eseguire almeno tre run per grader sulle fixture di confine.
- [ ] Confrontare accuratezza sulle label e ripetibilità. Prima della slice 4 decidere se mantenere i
  cinque verdict o semplificare la scala; un cambio incrementa nuovamente la versione rubric.

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

### 5. Adjudication assoluta e paired — parziale

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

### 6. Baseline di calibrazione etichettata — parziale

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

### 7. Formula di scoring calibrata e rollout — non completata

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

Ogni slice forma un commit revertibile. Le slice 3, 5, 6 e 7 terminano con il relativo decision
checkpoint prima di iniziare il contratto successivo. I risultati v3 intermedi restano separati per
versione/configurazione e non diventano baseline canonica finché la slice 7 non è approvata.

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

- Dopo il report delle 36 chiamate, il checkpoint umano mantiene i cinque verdict o richiede una
  scala semplificata e una nuova rubric? La decisione blocca la slice 4 e non è anticipabile senza i
  dati empirici.
