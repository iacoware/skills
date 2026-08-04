# Grading di `plan-slices` — Piano di implementazione

## Obiettivo

Implementare le sette slice `NOW` di `GRADING-IMPROVEMENTS.md` senza modificare gli artefatti v2
esistenti. Il risultato è evaluator v3: preflight solo strutturale, grading semanticamente
calibrato, risoluzione auditabile dei disaccordi e scoring scelto su fixture etichettate.

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

### 0. Protezione della baseline e versioning

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

### 1. Preflight esclusivamente strutturale

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

### 2. Brief valutativo e anonimizzazione

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

### 3. Severità e critical failure operativi

**Modifiche**

- Portare la rubric a v3 e codificare per ogni verdict definizione, condizioni operative ed esempi di
  confine non scenario-specifici:
  `pass`; `minor` locale; `material` richiede ristrutturazione; `severe` invalida outcome/release o
  sicurezza; `absent` significa elemento non valutabile perché totalmente mancante.
- Ampliare ogni critical failure con condizioni sufficienti, esclusioni e tipi di citazione
  richiesti. Violare un hard constraint non attiva automaticamente failure o cap.
- Sostituire gli array di stringhe ambigui con `candidate_evidence` e
  `controlling_evidence`; richiedere entrambi per verdict non-pass e critical failure.
- Aggiungere fixture v3 di confine isolate per correzione locale, split/merge/riordino, outcome
  invalidato, safety boundary e assenza totale.
- Lasciare temporaneamente invariata la formula corrente per isolare il cambio semantico.

**Test e checkpoint**

- Schema e validator rifiutano evidenza incompleta, `absent` usato come grave generico e critical
  failure senza condizioni/citazioni.
- Eseguire almeno tre run per grader sulle fixture di confine.
- Confrontare accuratezza sulle label e ripetibilità. Prima della slice 4 decidere se mantenere i
  cinque verdict o semplificare la scala; un cambio incrementa nuovamente la versione rubric.

### 4. Un solo addebito per difetto

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

### 5. Adjudication assoluta e paired

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

### 6. Baseline di calibrazione etichettata

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

### 7. Formula di scoring calibrata e rollout

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
