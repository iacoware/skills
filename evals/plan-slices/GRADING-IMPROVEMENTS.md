# Grading di `plan-slices` — Piano di miglioramento

- **Sources:** `EVAL-WORKFLOW.md`, `grader-rubric.json`, evaluator v2, fixture e
  artefatti `recipe-app/results/PLAN-CC-CON-5.*.v2.*`.
- **Current state:** il preflight orchestrato esegue già solo la validazione strutturale; il grading
  semantico è criterion-level e lo scoring è deterministico, ma reference, severità, aggregazione e
  adjudication lasciano ancora ampia variabilità interpretativa.
- **Evidence:** sullo stesso candidato Codex produce `43,75` e Claude `70,00`; il validator delle
  expectations segnala otto errori, dei quali sei sono mismatch lessicali e due omissioni reali.
- **Decisione:** eliminare interamente expectations, regex semantiche, lint semantico, Plan IR ed
  estrazione semantica; mantenere soltanto validazione strutturale e grading.
- **Audience:** sviluppatori dello skill e dell'evaluator; il risultato `NOW` è una baseline
  calibrata per decisioni interne, non una release rivolta a utenti finali.

## Ordering criteria

- Semplificare prima il confine di validazione, così nessuna calibrazione incorpora segnali regex.
- Stabilire autorità, severità e ownership dei difetti prima di confrontare nuovamente i grader.
- Risolvere il grading assoluto prima di usare gli score per giudicare regressioni paired.
- Scegliere la formula di aggregazione solo dopo fixture etichettate e run ripetute.
- Versionare ogni modifica capace di cambiare verdict, score o interpretazione degli artefatti.

## Themes

| Theme | Desired outcome | First validation |
|---|---|---|
| A. Confine di validazione | Solo difetti di formato bloccano il candidato prima del grading | 1. Preflight esclusivamente strutturale |
| B. Giudizio semantico stabile | Grader diversi applicano la stessa autorità e soglie operative | 2. Brief valutativo senza piano ideale |
| C. Risoluzione dei disaccordi | Ogni divergenza materiale produce un grade risolto e auditabile | 5. Adjudication del grading assoluto |
| D. Misura calibrata | Score e direzione paired sono scelti contro casi etichettati, non per intuizione | 6. Baseline di calibrazione etichettata |

## Cross-functional concerns

- **Authority:** le fonti di prodotto controllano i fatti; il brief interpreta solo vincoli,
  alternative e conflitti già rintracciabili nelle fonti.
- **Validation and errors:** il validator blocca esclusivamente forma e riferimenti strutturali; il
  grader possiede ogni giudizio scenario-specifico e qualitativo.
- **Reproducibility:** prompt, fonti, brief, rubric, candidati, modello, effort e configurazione sono
  identificati e hashati in ogni artefatto.
- **Auditability:** ogni verdict e critical failure cita candidato ed evidenza controllante; score e
  cap sono sempre derivati in codice.
- **Data integrity and recovery:** output immutabili, scrittura atomica e resume accettano soltanto
  artefatti completi con schema, configurazione e hash coincidenti.

## NOW

### 1. Preflight esclusivamente strutturale *(Theme: A)*

---

**Includes**

- Rimuovere `expectations.json`, blocchi machine-readable nei reference e relativi generatori.
- Rimuovere `--expectations`, regole regex, target Make e documentazione del lint semantico.
- Conservare nel validator solo sezioni, ordine, tabelle, numerazione, tag, campi e liste richieste.
- Eliminare test delle expectations; mantenere o riclassificare solo controlli scenario-agnostici di
  forma e riferimenti espliciti.

**Verification**

- Suite offline senza moduli, fixture, CLI o documentazione delle expectations.
- Parafrasi e sinonimi non cambiano l'esito strutturale dello stesso piano.
- Un piano strutturalmente invalido si ferma; uno valido raggiunge sempre il grading.

**Learning / risk**

- Le omissioni scenario-specifiche non hanno più un fallback deterministico e devono essere coperte
  esplicitamente dalle fixture del grader.

**Outcome**

- Il preflight ha un confine semplice: formato deterministico, contenuto affidato al grading.

### 2. Brief valutativo senza piano ideale *(Theme: B)*

---

**Includes**

- Sostituire il reference completo con un brief conciso collegato alle fonti.
- Includere solo hard constraint, accepted alternative, conflitti noti e classificazione
  dell'autorità; escludere decomposizione preferita, titoli, ordine ideale ed example evidence.
- Scrivere il brief per revisione umana, senza schema machine-readable o estrazione automatica.
- Presentare candidati e provider al grader con alias neutrali; conservare il mapping nei metadata.

**Verification**

- Una decomposizione alternativa supportata dalle fonti non è penalizzata per mancato matching.
- Un hard constraint violato resta rilevabile con citazioni dal brief e dalla fonte controllante.
- Prompt snapshot privo di nomi che rivelano generatore o piano ideale.

**Learning / risk**

- Un brief troppo prescrittivo ricrea l'ancoraggio del reference; uno troppo povero aumenta la
  ricostruzione interpretativa richiesta a ogni grader.

**Outcome**

- Entrambi i grader ricevono la stessa evidenza necessaria senza essere ancorati a una soluzione.

### 3. Severità e critical failure operativi *(Theme: B)*

---

**Includes**

- Definire `pass` come criterio soddisfatto con evidenza pertinente.
- Definire `minor` come correzione locale senza cambiare outcome, ordine, confini o orizzonte.
- Definire `material` come split, merge, riordino, cambio di scope/horizon o nuova evidenza capace di
  cambiare una decisione; `severe` come outcome o release invalidati o confine di sicurezza violato.
- Riservare `absent` all'assenza totale dell'elemento necessario per valutare il criterio, non a un
  difetto semplicemente grave.
- Dare a ogni critical failure condizioni di attivazione sufficienti, esclusioni e citazioni
  richieste; un hard constraint non implica automaticamente `severe` o un cap.

**Verification**

- Fixture di confine distinguono correzione locale, ristrutturazione e invalidazione della release.
- Entrambi i grader attivano lo stesso critical failure sui casi netti e nessuno sulle alternative
  accettate.
- Run ripetute non reinterpretano `absent` come sinonimo generico di `severe`.

**Outcome**

- Le etichette di verdict descrivono conseguenze operative confrontabili, non sensibilità del grader.

### 4. Un solo addebito per difetto *(Theme: B)*

---

**Includes**

- Sostituire `primary_axis` con un `primary_criterion` esplicito per ogni root defect.
- Nella prima versione, vietare effetti secondari: un difetto può ridurre un solo criterio.
- Richiedere conseguenza concreta ed evidenza specifica per ogni difetto.
- Mantenere separati difetti distinti anche quando derivano dalla stessa area del piano.

**Verification**

- Backup e spend guardrails mancanti non abbassano automaticamente contenuto e orizzonti insieme.
- Merge consultazione/scrittura non produce tre penalità per la stessa conseguenza.
- Il contratto rifiuta difetti senza criterio primario, non referenziati o addebitati più volte.

**Learning / risk**

- Il vincolo può sottorappresentare conseguenze realmente indipendenti; verranno reintrodotte solo
  dopo fixture che ne dimostrino la necessità e la ripetibilità.

**Outcome**

- Lo score riflette difetti distinti invece del numero di rubriche alle quali un grader li collega.

### 5. Adjudication del grading assoluto *(Theme: C)*

---

**Includes**

- Attivare adjudication anche tra grade assoluti dello stesso candidato, non solo dopo confronti paired.
- Mostrare all'adjudicator soltanto criteri discordanti, evidenze concorrenti e parti controllanti
  delle fonti e del brief, con grader anonimizzati.
- Usare inizialmente revisione umana e registrare verdict, critical failure, motivazione ed evidenza.
- Produrre `RESOLVED.GRADE.json` e ricalcolare `RESOLVED.SCORE.json` esclusivamente in codice.
- Applicare lo stesso workflow ai disaccordi paired senza mediare score o direzioni.

**Verification**

- Il caso `PLAN-CC-CON-5` termina con un solo grade risolto, non con una richiesta `pending`.
- Resume e hash invalidano una risoluzione quando cambia uno degli input esaminati.
- Nessun criterio concorde viene rivalutato o alterato dall'adjudication.

**Outcome**

- Una divergenza materiale produce un risultato autorevole e riproducibile per la decisione successiva.

### 6. Baseline di calibrazione etichettata *(Theme: D)*

---

**Includes**

- Espandere fixture immutabili per omissioni operative, conflitti pre-decisi, alternative accettate,
  learning senza osservazione, ownership e conseguenze duplicate.
- Far assegnare a revisori umani verdict ammessi, difetto primario e critical failure attesi.
- Eseguire almeno tre run per grader sul subset critico con evaluator e input identici.
- Misurare accuratezza contro etichette, ripetibilità intra-grader, agreement inter-grader, precisione
  e recall dei critical failure e direzione paired.
- Mantenere le soglie non bloccanti finché dimensione e copertura del campione non sono sufficienti.

**Verification**

- Il report distingue agreement da correttezza rispetto alle etichette umane.
- Ogni metrica espone numeratore, denominatore, distribuzione per criterio e versione evaluator.
- Le fixture paired verificano anche criteri invariati, evitando miglioramenti ottenuti spostando il
  difetto altrove.

**Outcome**

- Le modifiche al grader sono valutabili contro una baseline esplicita, non contro convergenza casuale.

### 7. Formula di scoring calibrata *(Theme: D)*

---

**Includes**

- Confrontare `worst criterion wins`, media dei criteri e sole varianti motivate dalle fixture.
- Conservare i critical-failure cap per proprietà realmente non compensabili.
- Selezionare la formula che preserva direzione attesa, separa casi forti e critici e riduce
  discontinuità non giustificate.
- Versionare rubric, formula e artefatti; non ricalibrare retroattivamente risultati storici.
- Rieseguire la matrice assoluta e paired completa e pubblicare la nuova baseline.

**Verification**

- Test deterministici ricalcolano esattamente score, pesi e cap da ogni grade valido.
- Report before/after mostra score spread, rank delle fixture, critical failure e direzione paired.
- La formula scelta è documentata con casi in cui differisce dalle alternative scartate.

**Learning / risk**

- La media riduce la sensibilità a un singolo verdict ma può compensare difetti importanti; il worst
  criterion evita la compensazione ma amplifica una sola divergenza.

**Outcome**

- Lo score aggrega verdict calibrati senza introdurre una sensibilità maggiore del giudizio sottostante.

## LATER

- **Adjudicator automatico indipendente**
  - **Promotion trigger:** il workflow umano produce un campione sufficiente e un modello raggiunge
    precisione e recall concordate sui casi adjudicati.
  - **Expected value:** ridurre costo e latenza delle risoluzioni non critiche mantenendo auditabilità.
- **Effetti secondari dei difetti**
  - **Promotion trigger:** fixture etichettate mostrano conseguenze indipendenti perse dal solo
    `primary_criterion` e agreement stabile sulla loro attribuzione.
  - **Expected value:** rappresentare impatti multipli reali senza reintrodurre doppio addebito.
- **Scenari di dominio aggiuntivi**
  - **Promotion trigger:** la baseline `recipe-app` è stabile e nuovi domini rivelano rischi di
    overfitting della rubric o del brief.
  - **Expected value:** misurare generalizzazione dell'evaluator oltre il caso iniziale.

## OUT-OF-SCOPE

- **Plan IR e Markdown renderer** — complessità non giustificata per un artefatto destinato a umani.
- **Expectations tipizzate, regex o lint semantico** — duplicano il grader con affidabilità inferiore.
- **Estrattore semantico Markdown → fatti** — reintroduce un grader implicito senza risolvere il
  giudizio sul contenuto.
- **Hard compliance come fase separata** — hard constraint e critical failure restano verdict del
  grading, con score cap deterministico.
- **Miglioramenti dello skill generatore** — vanno valutati con l'evaluator stabilizzato, non mescolati
  alla sua ricalibrazione.

## Decision checkpoints

- **After slice 3:** ripetibilità sulle fixture di severità → confermare la scala a cinque livelli o
  semplificarla prima di cambiare il contratto dei difetti.
- **After slice 5:** costo e qualità delle risoluzioni umane → definire soglia e casi candidati per un
  adjudicator automatico in `LATER`.
- **After slice 6:** metriche etichettate → scegliere la formula di scoring e soglie di affidabilità,
  senza ottimizzare per la sola concordanza tra modelli.
- **After slice 7:** baseline completa → autorizzare nuovi confronti tra versioni dello skill.
