# Il ciclo — regole di dettaglio

Le regole che governano i passi del ciclo oltre alla loro sequenza. La sequenza, la tabella delle
esecuzioni e il vocabolario stanno in `../CONSENSUS-WORKFLOW.md`; i numeri di passo citati qui sono
quelli.

Lo legge chi scrive i prompt (Fase 1b-i), chi esegue il ciclo a mano (Fase 2) e chi scrive
l'orchestratore (Fase 5).

## Cosa il workflow applica da sé e cosa no

Il passo 8 è automatico solo dove il filtro è portante. Tre insiemi disgiunti:

- **Condivisa da entrambi i `REVIEW`, stesso rimedio** → applicata, `Origine: intersezione`.
- **Condivisa da entrambi i `REVIEW`, rimedi diversi** → applicata con la formulazione del lato che
  la porta, `Origine: intersezione-tema`. Due lettori indipendenti che vedono rotta la stessa area
  sono evidenza reale; che concordino anche sulla cura è un evento separato e più raro.
- **Condivisa da un `REVIEW` solo, o unica a un lato** → **non applicata**. Va nell'elenco dei punti
  che richiedono lettura umana. Si applica quando l'umano ritrova il difetto sul piano generato e lo
  giudica valido; in quel caso la riga nasce `giudizio` e la modifica cita il difetto osservato, non
  il report che l'ha proposta.

La regola dura di `improve` bidirezionale è meccanica allo stesso passo: se il campo `Regola esistente
che non ha impedito il difetto` nomina una clausola e la voce aggiunge righe **senza** la ragione
scritta per cui la riformulazione è stata scartata, la voce **non si applica da sé** e passa
all'elenco umano.

## `improve` è bidirezionale

Il template chiede, per ogni voce, due campi oltre al rimedio:

- **`Regola esistente che non ha impedito il difetto`** — quale clausola dello `SKILL.md` avrebbe
  dovuto coprirlo e non l'ha fatto, oppure la dichiarazione esplicita che nessuna esiste.
- **`Costo`** — cosa si può togliere o fondere se questa entra.

**Regola dura:** se il primo campo nomina una clausola esistente, il rimedio di default è
**riformularla**. Una modifica che aggiunge righe non si applica finché la riformulazione non è stata
tentata e scartata con una ragione. Il perché sta in `RATIONALE.md` § *Il cricchetto*.

La regola è applicabile solo se esiste la **mappa clausola → riga di registro**. Davanti a «la
clausola X non ha impedito il difetto» servono tre risposte che il registro da solo non dà, perché
traccia i commit e non le clausole, e ci sono state diciotto riscritture: X esiste ancora nella forma
che una riga afferma? X ha una riga, e quindi riformularla ne rompe la previsione? Se non ha nessuna
riga, il rimedio nasce scoperto. Senza la mappa il default resta quello che è sempre stato — aggiungere
una regola nuova — e il meccanismo costruito per fermare il cricchetto lo alimenta.

## Cecità e simmetria

Dal ciclo CON-6 i payload di `improve` **e di `review`** sono **ciechi e simmetrici**: nessun modello
sa quale candidato ha generato né quale `IMPROVEMENT` ha scritto. Fino a CON-5 ogni modello migliorava
il piano che sapeva proprio, e recensiva il proprio report contro quello dell'altro — cioè la fase che
assegna l'etichetta di precisione sapeva di chi era ogni punto.

La cecità è **nominale**: un modello può riconoscere il proprio stile anche senza etichetta. È un
limite dichiarato, non mitigato — mitigarlo costerebbe più di quanto il rischio valga. Il contratto di
conformità la indebolisce ulteriormente, chiedendo riferimenti localizzati ai candidati.

Le due mappe — `CANDIDATE-A`/`CANDIDATE-B` → piano e `REPORT-A`/`REPORT-B` → `IMPROVEMENT`, che non
devono coincidere — vivono in `support/AGENT-PLAN-MAP.md` insieme al generatore di ogni artefatto, e
sono escluse da ogni payload **per costruzione**, perché i payload si compongono da una allowlist
esplicita di file. Il divieto scritto nei prompt serve solo all'esecuzione manuale.

Il prompt `improve` esclude inoltre dall'analisi ogni problema relativo al **walking skeleton**. È
una restrizione di scope reale del ciclo, non un dettaglio del prompt.

## Confini di strumento

Cicli separati da un confine **non sono confrontabili alla lettera**. La colonna `Misurato su` del
registro esiste per registrarli, e ne porta il ciclo, i piani, gli strumenti, **il modello e
l'effort**. I confini noti:

- **CON-4 → CON-5.** I prompt sono cambiati. Le righe `R-002`…`R-008`, oggi `intersezione-tema`, sono
  state prodotte con prompt diversi da quelli in `prompts/`.
- **CON-5 → CON-6.** Payload cieco e simmetrico su `improve` **e** `review`; contratto di conformità
  con template e validator; `improve` bidirezionale; registro tradotto in inglese e migrato alla
  semantica `non smentita ×k` con la narrativa di ciclo estratta.
- **CON-6 → CON-7, effort.** I due modelli passano da `high` a `medium`. `high` è l'unica
  configurazione mai esercitata contro provider reali, e resta ferma in CON-6: cambiarla nello stesso
  ciclo che deve testare la specificità degli `IMPROVEMENT` avrebbe confuso la variabile testata con
  una scelta di costo indipendente.
- **CON-6 → CON-7, brief.** La revisione di `EVALUATION-BRIEF.md` sta dopo CON-6 per la stessa
  ragione: è l'autorità contro cui si decidono quattordici righe su diciassette.
- **Dopo la fase di modularizzazione e pruning.** Spostare testo dello skill in file caricati
  on-demand cambia ciò che il modello ha in contesto al momento di generare. Non è un refactor neutro:
  è un cambio di strumento al pari degli altri.

Principio che governa la lista: **un confine si attraversa una volta sola, deliberatamente, e si
registra.** Non si sgocciola. È la ragione per cui traduzione, split e migrazione del registro stanno
tutti in una fase sola, e per cui effort e brief stanno tutti e due dopo CON-6.

La modularizzazione di **questi documenti** non è un confine: nessuno di essi entra in un payload, che
si compone da allowlist — brief, fonti, candidati.
