# Grading di `plan-slices` — Piano di miglioramento

- **Sources:** `GRADING-EVAL-WORKFLOW.md`, `grader-rubric.json`, evaluator v2, fixture e
  artefatti `recipe-app/results/PLAN-CC-CON-5.*.v2.*`; run critica v3 del 2026-08-04 e
  `NOTES.md`.
- **Current state:** il preflight orchestrato esegue già solo la validazione strutturale; brief,
  severità operative e contratto dei difetti sono in v3. La prima raccolta assoluta reale si è
  fermata a 15 unità su 36 e misura agreement inter-grader 0.56 esatto e 0.80 entro un livello.
- **Evidence:** sullo stesso candidato Codex produce `43,75` e Claude `70,00`. Sul subset critico v3
  i grader concordano sul livello esatto poco più di una volta su due, ma quasi sempre entro un
  livello: il disaccordo è sulla risoluzione della scala, non sul giudizio.
- **Decisione:** eliminare interamente expectations, regex semantiche, lint semantico, Plan IR ed
  estrazione semantica; mantenere soltanto validazione strutturale e grading.
- **Audience:** sviluppatori dello skill e dell'evaluator; il risultato `NOW` è uno strumento di
  misura per decisioni interne, non una release rivolta a utenti finali.

## Ordering criteria

- Semplificare prima il confine di validazione, così nessuna calibrazione incorpora segnali regex.
- Stabilire autorità, severità e ownership dei difetti prima di misurare il comportamento dei grader.
- Validare lo strumento relativo prima di completare la calibrazione assoluta: la decisione che
  l'evaluator serve è un before/after, e la differenza fra due verdetti assoluti rumorosi è meno
  affidabile di un confronto diretto fra i due candidati nella stessa chiamata.
- Ogni modifica al contratto capace di invalidare artefatti già raccolti precede le run che li
  raccolgono; le run pagate non si ripetono per un cambio di schema evitabile.
- Scegliere la formula di aggregazione solo dopo fixture etichettate e run ripetute.
- Versionare ogni modifica capace di cambiare verdict, direzione, score o interpretazione degli
  artefatti.

## Themes

| Theme | Desired outcome | First validation |
|---|---|---|
| A. Confine di validazione | Solo difetti di formato bloccano il candidato prima del grading | 1. Preflight esclusivamente strutturale |
| B. Giudizio semantico stabile | Grader diversi applicano la stessa autorità e soglie operative | 2. Brief valutativo senza piano ideale |
| C. Risoluzione dei disaccordi | Ogni divergenza materiale produce un risultato risolto e auditabile | 6. Adjudication dei disaccordi |
| D. Misura relativa affidabile | Una modifica alla skill risulta migliore o peggiore con un errore misurato | 5. Strumento relativo validato |
| E. Misura assoluta calibrata | Score e soglie sono scelti contro casi etichettati, non per intuizione | 7. Calibrazione assoluta etichettata |

## Cross-functional concerns

- **Authority:** le fonti di prodotto controllano i fatti; il brief interpreta solo vincoli,
  alternative e conflitti già rintracciabili nelle fonti.
- **Validation and errors:** il validator blocca esclusivamente forma e riferimenti strutturali; il
  grader possiede ogni giudizio scenario-specifico e qualitativo.
- **Reproducibility:** prompt, fonti, brief, rubric, candidati, modello, effort e configurazione sono
  identificati e hashati in ogni artefatto.
- **Auditability:** ogni verdict, direzione e critical failure cita candidato ed evidenza
  controllante; score e cap sono sempre derivati in codice.
- **Data integrity and recovery:** output immutabili, scrittura atomica e resume accettano soltanto
  artefatti completi con schema, configurazione e hash coincidenti; una risposta rifiutata dal
  contratto è conservata in quarantena, non scartata.
- **Cost of measurement:** ogni chiamata provider è autorizzata esplicitamente e contata; il tasso di
  conformità al contratto è una metrica pubblicata, non uno scarto operativo.

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
- Lo schema rifiuta evidenza incompleta, `absent` usato come grave generico e critical failure senza
  condizioni o citazioni.
- Le regole del prompt sono enunciate sui campi che il modello compila, non sui soli concetti.

**Outcome**

- Le etichette di verdict descrivono conseguenze operative confrontabili, non sensibilità del grader.

### 4. Un solo addebito per difetto *(Theme: B)*

---

**Includes**

- Sostituire `primary_axis` con un `primary_criterion` esplicito per ogni root defect.
- Nella prima versione, vietare effetti secondari: un difetto può ridurre un solo criterio.
- Richiedere conseguenza concreta ed evidenza specifica per ogni difetto.
- Mantenere separati difetti distinti anche quando derivano dalla stessa area del piano.
- Chiudere ogni modifica allo schema grade prima delle run che ne raccolgono gli artefatti.

**Verification**

- Backup e spend guardrails mancanti non abbassano automaticamente contenuto e orizzonti insieme.
- Merge consultazione/scrittura non produce tre penalità per la stessa conseguenza.
- Il contratto rifiuta difetti senza criterio primario, non referenziati o addebitati più volte.

**Learning / risk**

- Il vincolo può sottorappresentare conseguenze realmente indipendenti; verranno reintrodotte solo
  dopo fixture che ne dimostrino la necessità e la ripetibilità.

**Outcome**

- Lo score riflette difetti distinti invece del numero di rubriche alle quali un grader li collega.

### 5. Strumento relativo validato *(Theme: D)*

---

**Includes**

- Scollegare le unità paired dai grade assoluti nell'orchestrator; il prompt di confronto riceve già
  soltanto rubric, fonti, brief e i due candidati.
- Eseguire ogni coppia anche a ordine invertito e registrare l'inversione nei metadata.
- Comporre altre coppie etichettate dalle fixture di confine esistenti, con direzioni attese e
  criteri invarianti.
- Misurare tasso di falso cambiamento sui criteri invarianti, stabilità fra i due ordini e agreement
  inter-grader sulla direzione.
- Conservare le risposte rifiutate dal contratto e pubblicare il tasso di conformità per provider.

**Verification**

- I criteri etichettati invarianti risultano `same` in entrambi gli ordini e ogni deviazione è contata.
- Invertire l'ordine non cambia la direzione riportata sui criteri con direzione attesa.
- Il report distingue direzione corretta, falso cambiamento e disaccordo fra grader.
- Nessuna unità paired richiede artefatti assoluti per essere eseguita.

**Learning / risk**

- Se il tasso di falso cambiamento resta alto, il problema è la rubric a 26 criteri, non la scala dei
  verdict, e la calibrazione assoluta non lo correggerebbe.
- Il contratto paired pretende direzione, confidence ed evidenza per ogni criterio: il rischio di
  non-conformità è almeno pari a quello assoluto.

**Outcome**

- Una modifica alla skill è giudicabile migliore o peggiore con un errore misurato, senza passare
  dalla differenza fra due score assoluti.

### 6. Adjudication dei disaccordi *(Theme: C)*

---

**Includes**

- Attivare adjudication tra grade assoluti dello stesso candidato e tra confronti paired discordanti.
- Mostrare all'adjudicator soltanto criteri discordanti, evidenze concorrenti e parti controllanti
  delle fonti e del brief, con grader anonimizzati.
- Usare inizialmente revisione umana e registrare verdict, direzione, critical failure, motivazione
  ed evidenza.
- Produrre `RESOLVED.GRADE.json` e ricalcolare `RESOLVED.SCORE.json` esclusivamente in codice.
- Risolvere i disaccordi paired sulla direzione senza mediare score o direzioni.

**Verification**

- Il caso `PLAN-CC-CON-5` termina con un solo grade risolto, non con una richiesta `pending`.
- Resume e hash invalidano una risoluzione quando cambia uno degli input esaminati.
- Nessun criterio concorde viene rivalutato o alterato dall'adjudication.

**Outcome**

- Una divergenza materiale produce un risultato autorevole e riproducibile per la decisione successiva.

### 7. Calibrazione assoluta etichettata *(Theme: E)*

---

**Includes**

- Espandere fixture immutabili per omissioni operative, conflitti pre-decisi, alternative accettate,
  learning senza osservazione, ownership e conseguenze duplicate.
- Far assegnare a revisori umani verdict ammessi, difetto primario e critical failure attesi.
- Eseguire almeno tre run per grader sul subset critico con evaluator e input identici.
- Misurare accuratezza contro etichette, ripetibilità intra-grader, agreement inter-grader e
  precisione e recall dei critical failure.
- Mantenere le soglie non bloccanti finché dimensione e copertura del campione non sono sufficienti.

**Verification**

- Il report distingue agreement da correttezza rispetto alle etichette umane.
- Ogni metrica espone numeratore, denominatore, distribuzione per criterio e versione evaluator.
- Run ripetute non reinterpretano `absent` come sinonimo generico di `severe`.

**Learning / risk**

- Ritentare un'unità rifiutata finché è conforme filtra proprio i casi che il grader sbaglia e
  falsifica le metriche che questa slice deve produrre.

**Outcome**

- Le modifiche al grader sono valutabili contro una baseline esplicita, non contro convergenza casuale.

### 8. Formula di scoring calibrata *(Theme: E)*

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
- **Rubric ridotta ai criteri discriminanti**
  - **Promotion trigger:** la slice 5 mostra falso cambiamento concentrato su un sottoinsieme stabile
    di criteri, oppure criteri che nessun grader distingue mai.
  - **Expected value:** ridurre rumore e costo per chiamata senza perdere potere diagnostico.
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

- **After slice 4:** contratto grade congelato → autorizzare le run pagate, sapendo che una modifica
  successiva allo schema le invaliderebbe.
- **After slice 5:** falso cambiamento sui criteri invarianti e stabilità fra ordini → decidere se lo
  strumento relativo basta per giudicare le modifiche alla skill e con quale profondità serve ancora
  la calibrazione assoluta.
- **After slice 6:** costo e qualità delle risoluzioni umane → definire soglia e casi candidati per un
  adjudicator automatico in `LATER`.
- **After slice 7:** ripetibilità e accuratezza sulle fixture di severità → confermare la scala a
  cinque livelli o versionare una rubric semplificata.
- **After slice 8:** baseline completa → autorizzare nuovi confronti tra versioni dello skill.

## Open questions

- La scala a cinque verdict resta o viene semplificata? La risposta cambia rubric, contratto e
  metriche; blocca la slice 7 e il rollout della slice 8, non le slice 4 e 5.
- Quante chiamate provider sono autorizzate oltre le 36 iniziali, di cui 21 già consumate? Blocca
  ogni run delle slice 5 e 7.
- Il grade contract resta invariato o la citazione di un difetto da un criterio diverso dal proprio
  `primary_criterion` smette di essere un errore fatale? Blocca la chiusura della slice 4 e, per
  effetto delle versioni, le run delle slice 5 e 7.
