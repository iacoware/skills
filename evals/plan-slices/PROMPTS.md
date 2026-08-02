## GENERATE PLAN

Leggi i documenti markdown in @evals/plan-slices/recipe-app/sources/ partendo da @evals/plan-slices/recipe-app/sources/goal.md e crea una pianificazione di alto livello in slice e scrivila nel documento @evals/plan-slices/recipe-app/results/PLAN-CC-CON-XX.md

---

## CREATE IMPROVEMENTS

Leggi e applica lo skill `$plan-slices` in modalità Review.

Obiettivo: confrontare i piani dell’eval `recipe-app` e produrre un solo documento di miglioramento relativo al piano generato dal tuo stesso agente.

## Vincoli assoluti

- Non modificare `$plan-slices`, validator, test, reference o piani.
- Crea esclusivamente il documento `*.IMPROVEMENT.md` richiesto.
- Non creare né modificare il documento dell’altro agente.
- Ignora i file `*.IMPROVEMENT.md` nella selezione dei piani.
- Confronta i suffissi numericamente, non lessicograficamente e non per data.
- Escludi completamente dall’analisi e dal documento qualsiasi problema o miglioramento relativo al walking skeleton.
- Il main agent è l’unico autorizzato a scrivere file.
- I sub-agent devono solamente leggere e restituire report.
- Non usare assunzioni non supportate: distingui fatti osservati e inferenze.
- Non elogiare o penalizzare un piano in generale: riporta differenze verificabili.

## Identità del piano da migliorare

- Se sei Codex, il tuo prefisso è `PLAN-CX-CON-`.
- Se sei Claude Code, il tuo prefisso è `PLAN-CC-CON-`.

## Workflow obbligatorio

### 1. Valutazione delegata

Crea un sub-agent dedicato esclusivamente alla valutazione.

Se l’infrastruttura lo consente, crealo senza ereditare la conversazione principale
(`fork_turns="none"` o equivalente). Forniscigli direttamente queste istruzioni e i percorsi
necessari.

Il sub-agent deve:

1. Leggere `evals/plan-slices/recipe-app/REFERENCE-PLAN.md`.
2. Cercare in `evals/plan-slices/recipe-app/results/`:
    - `PLAN-CX-CON-<numero>.md`;
    - `PLAN-CC-CON-<numero>.md`.
3. Escludere `*.IMPROVEMENT.md`.
4. Selezionare per ciascun prefisso il suffisso numerico massimo.
5. Leggere i due piani selezionati.
6. Confrontarli con il reference, usando i criteri di review di `$plan-slices`:
    - individuazione e confini dei temi;
    - outcome e primo validatore dei temi;
    - suddivisione, coesione e verticalità delle slice;
    - ordine delle slice e validazione anticipata dei rischi;
    - contenuto, verifica, learning target e outcome delle slice;
    - assegnazione a `NOW`, `LATER` e `OUT-OF-SCOPE`;
    - contraddizioni, assunzioni e domande aperte.
7. Non analizzare né menzionare il walking skeleton.
8. Non modificare alcun file.

Il report deve essere conciso ma contenere:

- percorsi esatti dei due piani selezionati e relativi suffissi;
- identità del piano appartenente al main agent;
- per ogni difetto rilevante del piano del main agent:
    - evidenza precisa nel piano;
    - aspettativa ricavata dal reference;
    - confronto con il piano dell’altro agente, indicando se evita, condivide o manifesta diversamente il problema;
    - criterio o anti-pattern di `$plan-slices` coinvolto;
    - conseguenza sulla qualità del piano;
- contraddizioni e domande aperte che cambiano concretamente scope, ordine o verificabilità;
- eventuali punti nei quali il reference e l’altro piano non forniscono evidenza sufficiente.

Non proporre ancora modifiche allo skill.

### 2. Progettazione degli improvement delegata

Attendi il completamento del primo sub-agent. Crea quindi un secondo sub-agent, distinto e senza
ereditare la conversazione principale, se supportato.

Passagli:

- integralmente il report del primo sub-agent;
- l’identità del main agent;
- il percorso di `$plan-slices`;
- il vincolo di non modificare file.

Il secondo sub-agent deve leggere:

- `$plan-slices/SKILL.md`;
- il template richiamato dallo skill;
- il validator e i relativi test;
- le aspettative o rubriche semantiche pertinenti all’eval, se presenti.

Deve trasformare esclusivamente i difetti supportati dal report in miglioramenti generalizzabili,
evitando regole specifiche della sola recipe app.

Per ogni miglioramento deve restituire:

- `Problema osservato`: problema nel piano del main agent;
- `Evidenza dal reference`;
- `Confronto con l’altro piano`;
- `Cambiamento allo skill`: sezione precisa e modifica normativa concreta;
- `Testing strutturale`: cambiamenti al validator o ai suoi test, solo se il requisito è
  verificabile sintatticamente;
- `Testing semantico`: aspettativa, fixture o criterio di valutazione necessario per verificare
  giudizi di contenuto;
- `Risultato atteso`: comportamento osservabile nelle future generazioni;
- `Rischio di regressione o overfitting`, se presente.

Non forzare controlli semantici nel validator strutturale. Se un miglioramento non richiede uno dei
due tipi di test, indicare `Non applicabile` con una breve motivazione.

### 3. Scrittura affidata al main agent

Dopo avere ricevuto il secondo report, il main agent deve:

1. Verificare che ogni improvement sia supportato dal report di valutazione.
2. Rimuovere duplicazioni, proposte non generalizzabili e affermazioni non dimostrate.
3. Individuare il proprio piano selezionato:
    - Codex: `PLAN-CX-CON-<numero>.md`;
    - Claude Code: `PLAN-CC-CON-<numero>.md`.
4. Creare un solo file nella stessa directory, inserendo `.IMPROVEMENT` prima di `.md`.
5. Non modificare nessun altro file.

Usa questa struttura:

# Improvement analysis for `<nome piano>`

## Inputs

- Reference: `<percorso>`
- Own plan: `<percorso>`
- Other plan: `<percorso>`
- Selection: highest numeric suffix, excluding `*.IMPROVEMENT.md`

## Improvements

### 1. `<titolo sintetico>`

- **Problema osservato:** ...
- **Evidenza dal reference:** ...
- **Confronto con l’altro piano:** ...
- **Cambiamento concreto a `plan-slices`:** ...
- **Testing strutturale:** ...
- **Testing semantico:** ...
- **Risultato atteso:** ...
- **Rischi:** ...

Ripeti la sezione per ogni miglioramento supportato.

## Verifica finale

Prima di concludere, verifica e comunica:

- quale suffisso numerico è stato selezionato per ciascun agente;
- percorso del documento creato;
- che esista un solo nuovo documento `*.IMPROVEMENT.md`;
- che nessun piano, skill, validator, test o documento dell’altro agente sia stato modificato;
- che il documento non contenga argomenti esclusi.

Punto essenziale: il secondo sub-agent riceve il report strutturato, non l’intera cronologia. Inoltre separa test strutturali e semantici, evitando di
trasformare giudizi architetturali in controlli sintattici fragili.

---

## CREATE REVIEW 2

AGENTE_CORRENTE: `<Codex | Claude Code>`

Nella directory `evals/plan-slices/recipe-app/results/`, individua per
ciascun agente il documento
IMPROVEMENT con il suffisso numerico più alto:

- Codex: `PLAN-CX-CON-<numero>.IMPROVEMENT.md`
- Claude Code: `PLAN-CC-CON-<numero>.IMPROVEMENT.md`

Confronta i suffissi come numeri interi, non lessicograficamente e non per
data di modifica.

Se `AGENTE_CORRENTE` non è stato valorizzato esplicitamente con `Codex`
oppure `Claude Code`, fermati
e chiedi di specificarlo.

## Input e responsabilità

Il main agent deve leggere entrambi gli IMPROVEMENT selezionati:

1. l’IMPROVEMENT Codex con il suffisso numerico più alto;
2. l’IMPROVEMENT Claude Code con il suffisso numerico più alto.

Non leggere:

- reference;
- piani originali;
- documenti REVIEW esistenti;
- altri file non necessari al confronto.

Delega inoltre il confronto a un sub-agent dedicato, preferibilmente senza
passargli la conversazione
principale.

Il sub-agent deve:

- leggere entrambi gli IMPROVEMENT selezionati;
- confrontarli semanticamente secondo le regole seguenti;
- restituire al main agent un riepilogo strutturato nelle quattro categorie
  richieste;
- evidenziare eventuali casi dubbi di classificazione;
- non creare, modificare o eliminare file.

Il main agent deve verificare il riepilogo del sub-agent rispetto ai due
IMPROVEMENT e scrivere il
solo REVIEW appartenente ad `AGENTE_CORRENTE`.

## Vincoli del confronto

Considera gli improvement già verificati:

- non rivalutare la correttezza degli improvement;
- consulta `$plan-slices/SKILL.md` soltanto se necessario per chiarire
  terminologia o contraddizioni;
- escludi completamente qualsiasi miglioramento relativo al walking
  skeleton;
- non menzionare nel REVIEW gli elementi esclusi relativi al walking
  skeleton.

Confronta gli improvement per significato, non per formulazione.

Individua:

1. miglioramenti presenti in entrambi i report;
2. miglioramenti presenti solo nel report Codex;
3. miglioramenti presenti solo nel report Claude Code;
4. miglioramenti in contraddizione.

Applica queste regole di classificazione:

- assegna ogni miglioramento normalizzato a una sola categoria;
- una formulazione diversa non costituisce automaticamente un miglioramento
  unilaterale;
- un maggiore livello di dettaglio non costituisce automaticamente un
  miglioramento unilaterale;
- differenze compatibili nell’implementazione non costituiscono
  automaticamente una contraddizione;
- se entrambi i report identificano lo stesso problema e propongono
  soluzioni sostanzialmente
  compatibili, classificalo come condiviso e descrivi le differenze;
- se entrambi identificano lo stesso problema ma propongono soluzioni
  incompatibili, classificalo
  esclusivamente come contraddizione;
- non duplicare lo stesso miglioramento in più sezioni;
- calcola i conteggi finali sugli improvement normalizzati, non sul numero
  di frasi o bullet originali.

## Output dell’esecuzione

Produci esattamente un documento REVIEW, determinato da `AGENTE_CORRENTE`:

- se `AGENTE_CORRENTE` è `Codex`, crea esclusivamente
  `PLAN-CX-CON-<numero-Codex>.REVIEW.md`;
- se `AGENTE_CORRENTE` è `Claude Code`, crea esclusivamente
  `PLAN-CC-CON-<numero-Claude-Code>.REVIEW.md`.

Il suffisso del REVIEW deve coincidere con quello dell’IMPROVEMENT
dell’agente corrente.

La prospettiva del documento dipende da `AGENTE_CORRENTE`:

- il REVIEW Codex valuta l’IMPROVEMENT Codex rispetto all’IMPROVEMENT
  Claude Code;
- il REVIEW Claude Code valuta l’IMPROVEMENT Claude Code rispetto
  all’IMPROVEMENT Codex.

Non creare, leggere, modificare, sovrascrivere o validare il REVIEW
dell’altro agente.

## Struttura obbligatoria del REVIEW

Usa esattamente questa struttura:

# Review of `<documento IMPROVEMENT dell’agente corrente>`

## Inputs

- **Reviewed report:** `<IMPROVEMENT dell’agente corrente>`
- **Compared with:** `<IMPROVEMENT dell’altro agente>`

## Improvements also present in the other report

### `<miglioramento normalizzato>`

- **In this report:** ...
- **In the other report:** ...
- **Common improvement:** ...
- **Differences:** ...

## Improvements unique to this report

### `<miglioramento>`

- **Improvement:** ...
- **Difference from the other report:** ...

## Improvements present only in the other report

### `<miglioramento>`

- **Other report:** ...
- **Missing from this report:** ...

## Contradictory improvements

### `<area del conflitto>`

- **This report:** ...
- **Other report:** ...
- **Conflict:** ...
- **Suggested resolution:** ...

## Summary

- **Shared:** `<numero>`
- **Unique to this report:** `<numero>`
- **Only in the other report:** `<numero>`
- **Contradictions:** `<numero>`

Per ogni sezione priva di elementi, scrivi esclusivamente:

- None identified.

Non aggiungere sezioni ulteriori.

## Verifica finale

Prima di terminare, verifica che:

- siano stati letti entrambi gli IMPROVEMENT selezionati;
- i suffissi massimi siano stati determinati numericamente;
- sia stato creato o aggiornato esattamente un REVIEW;
- il REVIEW prodotto appartenga ad `AGENTE_CORRENTE`;
- il suo suffisso coincida con quello dell’IMPROVEMENT dell’agente
  corrente;
- il REVIEW dell’altro agente non sia stato letto né modificato;
- ogni miglioramento compaia in una sola categoria;
- gli elementi relativi al walking skeleton siano completamente assenti;
- i conteggi nel `Summary` corrispondano agli elementi delle rispettive
  sezioni;
- nessun IMPROVEMENT, skill o altro file sia stato modificato.

La presenza di REVIEW preesistenti, compreso quello dell’altro agente, non
costituisce errore e non
autorizza a leggerli, modificarli o eliminarli.
