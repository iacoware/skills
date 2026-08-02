# PLAN-CC-CON-4 — Documento di miglioramento

- **Piano analizzato:** [`PLAN-CC-CON-4.md`](PLAN-CC-CON-4.md) (Claude Code).
- **Riferimento semantico:** [`../REFERENCE-PLAN.md`](../REFERENCE-PLAN.md).
- **Piano di confronto:** [`PLAN-CX-CON-4.md`](PLAN-CX-CON-4.md), citato solo come evidenza di comportamento alternativo.
- **Esclusione dichiarata:** problemi e miglioramenti relativi al walking skeleton sono fuori da questo documento.
- **Uso:** analisi. Nessuna modifica allo skill `plan-slices` è stata applicata.

---

## 1. Contraddizione tra fonti asserita in silenzio

**Problema osservato**

- La slice 4 dichiara in `Includes`: «la query viene embeddata a runtime» (`PLAN-CC-CON-4.md:130`), cioè esattamente ciò che `goal.md:110` e `arch-choices.md:33` vietano mentre `concepts.md:153` lo richiede.
- Le `Open questions` (`:366-369`) non nominano la contraddizione: il piano sceglie un lato senza dirlo. È l'anti-pattern `Silent contradiction` già presente nello skill, quindi il divieto esiste ma non viene applicato.
- Il reference la considera l'unica vera contraddizione dello scenario e pretende che venga esposta con le slice bloccate (`REFERENCE-PLAN.md:197`, `:208`), oltre a una `Precondizione` sulla slice di indicizzazione (`:67`).
- `PLAN-CX-CON-4.md` la espone in `Open questions` (`:341`), definisce uno spike time-boxed con domanda, evidenza, criterio d'uscita e trattamento del codice sperimentale (`:337`) e condiziona il contenuto della slice («vettorializza una query secondo la decisione dello spike», `:81`).

**Cambiamento allo skill**

- Nel passo 1, trasformare la riconciliazione in un passo con output obbligatorio: prima di mappare i temi, elencare le coppie di affermazioni in conflitto con riferimento `file:riga` per entrambi i lati. Senza questo elenco il passo non è completo.
- Aggiungere un divieto esplicito e verificabile: nessun bullet `Includes` o `Verification` può asserire uno dei due lati di un conflitto non risolto; la formulazione ammessa è condizionale e rimanda alla decisione (`secondo la decisione dello spike`, `subordinato a …`).
- Rendere obbligatoria una delle due chiusure per ogni conflitto: voce in `Open questions` che nomina le slice bloccate, oppure spike time-boxed prima della prima slice bloccata. Lo skill le offre già come alternative (`SKILL.md:39-42`), ma non chiede la prova che una delle due sia stata scelta.
- Aggiungere il controllo al criterio di completamento del passo 5: «nessuna slice asserisce un lato di un conflitto elencato nello sweep».

**Risultato atteso**

- Le generazioni future producono la contraddizione sull'embedding della query in `Open questions` con le slice 2 e 4 nominate, e la slice di ricerca resta condizionata invece di dichiarare un comportamento vietato dalle fonti.

---

## 2. Decisioni mai prese confuse con decisioni prese

**Problema osservato**

- Il piano intercetta due decisioni aperte su quattro: provider Postgres e modello di embedding (`:368-369`).
- Manca il **modello LLM**, che `arch-choices.md` non fissa e che blocca la slice 7: la slice lo descrive come «LLM cheap a output strutturato» (`:199`) come se fosse deciso, e il checkpoint dopo la 7 (`:363`) presuppone un modello da confermare o sostituire che nessuno ha scelto.
- Il reference attende tutte e quattro le voci e chiede che le decisioni aperte vadano in `Open questions` con la slice bloccata, «mai scelte in silenzio dentro una slice» (`REFERENCE-PLAN.md:210`).

**Cambiamento allo skill**

- Distinguere nel passo 1 e nel passo 5 due categorie separate e ugualmente obbligatorie: **contraddizioni tra fonti** e **decisioni mai prese** (provider, modelli, servizi gestiti nominati senza scelta).
- Aggiungere una regola di completezza sulla seconda categoria: ogni adapter, provider o modello esterno che una slice `NOW` invoca deve essere o scelto nelle fonti con citazione, o presente in `Open questions` con la slice che blocca. Un aggettivo qualificante (`cheap`, `multilingue`, `economico`) non è una scelta.
- Aggiungere il controllo al criterio di completamento: «ogni dipendenza esterna invocata in `NOW` ha una fonte che la sceglie o una voce in `Open questions`».

**Risultato atteso**

- Le generazioni future elencano provider Postgres, modello di embedding e modello LLM come decisioni aperte con la rispettiva slice bloccante, senza descrivere come deciso ciò che le fonti lasciano aperto.

---

## 3. Identità consegnata dopo quattro slice di prodotto

**Problema osservato**

- L'accesso Google arriva alla slice 9 (`:237`), dopo form condiviso (5), import JSON-LD (6), fallback LLM (7) e foto (8): quattro slice di prodotto accettate su uno scope configurato.
- La copertura è una riga nei `Cross-functional concerns`: «gli ambienti precedenti alla slice 9 non sono pubblicamente raggiungibili» (`:31`). Nessuna slice dichiara la propria audience, quindi l'`Outcome` di ciascuna parla di «un utente» (`:166`, `:191`, `:215`) mentre l'utente reale non esiste ancora.
- Il reference colloca l'identità alla slice 6, «entro la prima slice destinata a utenti reali», e la dichiara il punto in cui il resolver passa da configurato ad autenticato (`REFERENCE-PLAN.md:88`, `:148`).
- `PLAN-CX-CON-4.md` la porta alla slice 4, subito dopo la validazione del differenziatore, così ogni slice successiva eredita un confine di ownership reale (`:122-141`).
- La regola dello skill esiste ma non è numerabile: «Once the evidence that justified deferring identity exists, deliver identity before further user-facing slices whose acceptance depends on real ownership» (`SKILL.md:243-244`) — «further» non dice quante.

**Cambiamento allo skill**

- Rendere il differimento contabile: l'identità deve arrivare **prima della seconda slice di prodotto che consegna comportamento a un utente finale**; oltre quella soglia il differimento va giustificato una volta sola in `Ordering criteria` con l'evidenza che lo motiva.
- Quando una slice `NOW` precede l'identità, obbligare la dichiarazione della sua audience e del suo ambiente **nella slice**, non solo nei `Cross-functional concerns`: un `Outcome` che dice «un utente» mentre l'identità non esiste va riscritto in termini di sviluppatore o tester.
- Aggiungere il controllo al criterio di completamento del passo 4: «ogni slice `NOW` precedente all'identità nomina un'audience compatibile con lo scope configurato».

**Risultato atteso**

- Le generazioni future collocano l'accesso subito dopo la validazione del differenziatore, oppure dichiarano esplicitamente per ogni slice anteriore che l'audience è di sviluppo — eliminando gli `Outcome` che promettono un utente inesistente.

---

## 4. Via di recupero staccata dal fallimento che recupera

**Problema osservato**

- La slice 6 nomina il paywall tra i fallimenti attesi e ne verifica il messaggio (`:177`, `:182`); la via di fuga — l'import da testo incollato — arriva alla slice 12 (`:295`), sei slice dopo, con foto, accesso, ricettari multipli e inviti in mezzo.
- La slice 12 stessa dichiara di essere il suggerimento offerto «quando l'add da link fallisce per paywall o pagina non leggibile» (`:302`): il piano riconosce il legame e lo posticipa comunque.
- Il reference chiude l'acquisizione in sequenza 8 → 9 → 10 e vieta di aprire adapter nuovi finché il tema non è chiuso (`REFERENCE-PLAN.md:18`, `:151`). `PLAN-CX-CON-4.md` consegna 6 → 7 → 8 nello stesso ordine.
- Causa nello skill: due regole confliggono senza priorità dichiarata. Il passo 3 chiede di «deliver a required correction, retry, or escape path before or with the first behaviour that can create the recoverable state» (`SKILL.md:139-140`); il passo 4 impone breadth-before-depth con eccezioni discorsive (`SKILL.md:232-234`). Il piano ha applicato la seconda e sacrificato la prima, dichiarandolo in `Ordering criteria` (`:12`).

**Cambiamento allo skill**

- Dichiarare la precedenza: la regola sulla via di recupero **vince** su breadth-before-depth, e l'eccezione «required recovery» del passo 4 va resa operativa con un test verificabile — se una slice nomina un modo di fallimento nella propria `Verification` e un'altra slice `NOW` ne è il rimedio, il rimedio precede l'inizio di un nuovo tema.
- Rendere esplicito il caso simmetrico: un rimedio che le fonti dichiarano fallback di un percorso già consegnato non è «depth» opzionale, è chiusura di quel percorso.
- Aggiungere il controllo al criterio di completamento del passo 4: «ogni fallimento nominato in una `Verification` ha il proprio rimedio consegnato prima della prima slice di un tema diverso».

**Risultato atteso**

- Le generazioni future collocano il copia-incolla immediatamente dopo il fallback LLM, chiudendo il tema di acquisizione prima di aprire foto o condivisione.

---

## 5. Pipeline condivisa aperta prima dei suoi produttori

**Problema osservato**

- La slice 8 apre la pipeline media e include già il download dell'immagine durante l'add da link (`:225`), ma l'acquisizione testuale non è chiusa: il copia-incolla arriva alla 12.
- La pipeline viene quindi progettata contro un insieme incompleto di produttori, e la slice 12 non dice nulla su cosa accada alle foto nel percorso da testo incollato: nessun owner esplicito, nessuna esclusione.
- Il reference colloca le foto alla slice 11, dopo la chiusura dell'acquisizione, «input diversi su una sola pipeline media, aperta una volta sola» (`REFERENCE-PLAN.md:123`, `:152`).
- Nota a credito del piano: le foto stanno **in una sola slice**, che è il comportamento corretto; l'errore è la posizione, non la coesione. `PLAN-CX-CON-4.md` sbaglia in modo speculare, spezzando la pipeline tra la slice 6 e la 10.

**Cambiamento allo skill**

- Aggiungere una regola d'ordine esplicita: una slice che apre una pipeline o un adapter condiviso da più percorsi deve seguire tutte le slice `NOW` che le forniscono input, e deve essere l'unica proprietaria di quell'adapter.
- Aggiungere l'anti-pattern corrispondente — apertura anticipata o duplicata di una pipeline condivisa — accanto agli anti-pattern esistenti sull'accumulo di infrastruttura.
- Estendere il controllo esistente «ogni comportamento in scope ha un owner o un'esclusione esplicita» ai percorsi: ogni combinazione produttore × pipeline condivisa ha un owner o un'esclusione.

**Risultato atteso**

- Le generazioni future collocano le foto dopo l'ultima slice di acquisizione e dichiarano in una sola slice come ciascun percorso di ingresso alimenta la pipeline media.

---

## 6. Slice in `NOW` senza domanda nelle fonti

**Problema osservato**

- La slice 10 «Ricettari e ricettario corrente» introduce in `NOW` la creazione di nuovi ricettari e il selettore (`:257-273`).
- Le fonti dichiarano che un utente **può appartenere** a più ricettari (`goal.md:92`, `concepts.md:10`), non che debba poterne creare dall'interfaccia nell'MVP. Il reference mette la creazione esplicita in `LATER` con trigger (`REFERENCE-PLAN.md:161`) e la esclude dalla slice di accesso (`:87`).
- Effetto: una slice `NOW` in più, con la sua superficie di UI e i suoi test, prima del rilascio agli utenti pilota.
- Causa nello skill: l'anti-pattern `Horizon dumping` copre «speculative ideas in `NOW`» (`SKILL.md:207-208`) ma non chiede alcuna traccia positiva verso le fonti, quindi una capability plausibile entra senza attrito.

**Cambiamento allo skill**

- Chiedere al passo 4 una traccia esplicita: ogni slice `NOW` cita la frase delle fonti che ne richiede il comportamento. Una capability soltanto compatibile con il modello dati, ma mai richiesta, va in `LATER` con trigger.
- Rendere questo il test di default per gli orizzonti: `NOW` richiede una richiesta esplicita; `LATER` richiede un trigger; `OUT-OF-SCOPE` richiede un'esclusione dichiarata.
- Aggiungere il controllo al criterio di completamento: «ogni slice `NOW` ha una citazione di fonte che la richiede».

**Risultato atteso**

- Le generazioni future collocano la creazione di ricettari aggiuntivi in `LATER` con il trigger dell'attrito osservato, riducendo `NOW` al perimetro dichiarato dalle fonti.

---

## 7. Enabler di dominio minuscolo assente, enabler rischioso sovraccarico

**Problema osservato**

- La slice 2 concentra schema `Cookbook` e `Recipe`, indice HNSW, resolver di scope, servizio di embedding, corpus bilingue reale e comando diagnostico (`:78-103`): è la slice più grande del piano proprio dove le convenzioni di dominio, ORM, test e scope vengono riviste per la prima volta.
- Conseguenza: il rischio esistenziale (qualità del ranking cross-lingua) e il primo rischio di dominio (persistenza, scope, 404 fuori scope) vengono validati insieme, quindi un fallimento non è attribuibile.
- Il reference separa una slice minuscola di dominio — persistenza, resolver unico, shell del ricettario vuoto, id fuori scope 404 — prima dell'indicizzazione (`REFERENCE-PLAN.md:54-59`, `:144`).
- `PLAN-CX-CON-4.md` commette lo stesso accorpamento: è un difetto sistematico dello skill, non del singolo piano.
- Causa nello skill: la calibrazione delle dimensioni dice di tenere strette le prime slice (`SKILL.md:163-165`) ma non impedisce a un enabler di cumulare più incertezze materiali, mentre i test sull'enabler chiedono che ne risolva «one material uncertainty» (`SKILL.md:148`) senza controllo a valle.

**Cambiamento allo skill**

- Rendere verificabile il limite già dichiarato: un enabler che tocca più di una incertezza materiale va diviso, e la prima slice che persiste dati stabilisce persistenza e resolver di scope su un comportamento minimo **prima** di qualunque enabler di motore.
- Aggiungere il criterio di attribuzione: se una sola slice può fallire per due cause indipendenti che cambiano decisioni diverse, va divisa.
- Aggiungere il controllo al criterio di completamento del passo 3: «nessun enabler valida più di una incertezza materiale».

**Risultato atteso**

- Le generazioni future producono una slice di dominio minuscola (ricettario corrente, resolver, fuori scope 404) prima della pipeline di embedding, e un enabler di ricerca che porta solo il rischio del ranking.

---

## 8. Slice di rilascio incompleta rispetto ai vincoli dichiarati

**Problema osservato**

- La slice 13 copre ambiente di produzione, segreti, credenziali OAuth, migrazioni, scale-to-zero, e misura cold start e costo (`:313-330`).
- Mancano due elementi che le fonti rendono obbligatori: **backup con prova di ripristino** — unico datastore, nessuna replica (`concepts.md:163`) — e **tetto di spesa con allarme** su LLM ed embedding, con il costo target dichiarato in `goal.md:42`.
- Il reference li richiede entrambi nella slice di rilascio (`REFERENCE-PLAN.md:135`). `PLAN-CX-CON-4.md` copre almeno limiti di consumo e dashboard su errori, latenza, costi e capacità dei free tier (`:287`).
- Causa nello skill: la prescrizione sulla release chiede «only source-backed operational readiness» (`SKILL.md:248`), formula che limita gli eccessi ma non chiede la copertura dei vincoli dichiarati nelle fonti.

**Cambiamento allo skill**

- Aggiungere il verso mancante: la slice `(Release: delivery)` deve coprire **ogni vincolo operativo dichiarato nelle fonti** — durabilità dei dati quando esiste un solo datastore, tetto di spesa e allarme quando il costo è un vincolo di prodotto, ripristino quando esiste stato non ricostruibile.
- Chiedere che ogni voce di questa copertura citi la fonte del vincolo, così la release resta ancorata e non diventa una checklist generica.
- Aggiungere il controllo al criterio di completamento: «ogni vincolo operativo dichiarato nelle fonti ha una voce nella slice di rilascio o un'esclusione esplicita».

**Risultato atteso**

- Le generazioni future includono backup con prova di ripristino e tetto di spesa con allarme nella slice di rilascio, misurati contro il target di costo dichiarato.

---

## 9. Verification forte sui casi felici, debole sui modi di fallimento ripetibili

**Problema osservato**

- Le verifiche del piano sono concrete e falsificabili — `"pomodoro"` che risale ricette inglesi, `"cena leggera"`, latenza post-cold-start, costo confrontato col target (`:92-94`, `:136-138`) — ed è il punto di forza rispetto a `PLAN-CX-CON-4.md`, che resta astratto.
- Restano però scoperti modi di fallimento che le fonti rendono attesi: idempotenza dell'accettazione di un invito (`:286-289` verifica solo token manomesso o scaduto), retry che non duplicano ricetta o oggetti dopo un salvataggio parziale, oggetti orfani su R2 quando l'upload fallisce a metà (`:230` verifica solo che la ricetta si salvi).
- Il reference chiede accettazione idempotente e integrità dei dati come esiti verificati (`REFERENCE-PLAN.md:128`, `:184`); `PLAN-CX-CON-4.md` li copre (`:181`, `:248`, `:272`).
- Secondo scoperto: la qualità del ranking cross-lingua — il rischio esistenziale — è verificata con query ad hoc invece che con un set di valutazione versionato. `PLAN-CX-CON-4.md` introduce un set bilingue con query di intento, ingredienti e casi negativi (`:84-86`), che rende il checkpoint dopo la slice 2 ripetibile invece che aneddotico.
- Causa nello skill: la prescrizione «name relevant abuse, timeout, invalid-output, and partial-failure modes» (`SKILL.md:171-172`) elenca categorie ma non include ripetizione, idempotenza e residui, e nulla distingue una prova di esistenza da una misura di qualità ripetibile.

**Cambiamento allo skill**

- Estendere l'elenco dei modi da nominare con **ripetizione della stessa operazione, idempotenza e residui** per ogni slice che scrive tramite un adapter esterno o crea appartenenze.
- Rafforzare la regola esistente «checking that data exists does not demonstrate its quality» (`SKILL.md:175-176`): quando un `Learning / risk` afferma qualità, pertinenza o accuratezza, la `Verification` deve nominare un **set di valutazione versionato** con casi positivi e negativi, non esempi scelti a mano.
- Mantenere esplicito il requisito complementare, già rispettato dal piano: almeno un letterale concreto (query, URL, input di fallimento) per ogni slice rischiosa.

**Risultato atteso**

- Le generazioni future conservano le verifiche concrete già prodotte e aggiungono set di valutazione versionati per i claim di qualità, oltre a idempotenza e pulizia dei residui dove esiste un effetto esterno ripetibile.

---

## 10. Orizzonti compattati e voci fuori posto

**Problema osservato**

- `OUT-OF-SCOPE` accorpa quattro esclusioni eterogenee in un solo bullet con una motivazione unica: «Ruoli e permessi granulari, ricerca cross-ricettario, vector DB dedicato, IaC versionata» (`:356`). Ogni voce perde la propria motivazione, che è il solo contenuto utile di quella sezione.
- Dentro quell'accorpamento finisce **ricerca cross-ricettario**, che il reference tiene in `LATER` con trigger e valore attesi (`REFERENCE-PLAN.md:160`): un'esclusione definitiva al posto di un rinvio condizionato.
- Causa nello skill: il passo 5 impone brevità e liste (`SKILL.md:266-282`) senza vincolare la granularità delle voci di orizzonte, e la distinzione `LATER` / `OUT-OF-SCOPE` non ha un test operativo.

**Cambiamento allo skill**

- Imporre **una voce per bullet** in `LATER` e `OUT-OF-SCOPE`, ciascuna con la propria motivazione o il proprio trigger.
- Aggiungere il test di separazione: se una voce ha un trigger plausibile che ne cambierebbe la priorità, appartiene a `LATER`; `OUT-OF-SCOPE` è riservato a ciò che una decisione dichiarata nelle fonti esclude. Il test vale anche in senso inverso: una voce `OUT-OF-SCOPE` che contiene un trigger è mal classificata.
- Aggiungere il controllo al criterio di completamento: «nessun bullet di orizzonte contiene più di una voce; nessuna voce `OUT-OF-SCOPE` contiene un trigger».

**Risultato atteso**

- Le generazioni future producono orizzonti leggibili voce per voce, con la ricerca cross-ricettario in `LATER` e le esclusioni definitive motivate una a una.

---

## Riepilogo dei cambiamenti proposti allo skill

| # | Area | Cambiamento | Difetto che elimina |
|---|---|---|---|
| 1 | Passo 1 | Sweep delle contraddizioni con `file:riga`, divieto di asserire un lato, chiusura obbligatoria | Slice 4 asserisce l'embedding a runtime |
| 2 | Passo 1 e 5 | Categoria separata per le decisioni mai prese; ogni dipendenza esterna scelta o aperta | Modello LLM trattato come deciso |
| 3 | Passo 4 | Soglia numerabile per il differimento dell'identità e audience dichiarata per slice | Identità alla slice 9 dopo quattro slice di prodotto |
| 4 | Passi 3 e 4 | Precedenza della via di recupero su breadth-before-depth | Copia-incolla alla slice 12 |
| 5 | Passo 4 | Pipeline condivisa aperta una volta sola, dopo i suoi produttori | Foto alla slice 8, acquisizione ancora aperta |
| 6 | Passo 4 | Ogni slice `NOW` cita la fonte che la richiede | Creazione di ricettari in `NOW` |
| 7 | Passo 3 | Un enabler valida una sola incertezza materiale | Slice 2 sovraccarica |
| 8 | Passo 4 | Release copre ogni vincolo operativo dichiarato nelle fonti | Backup e tetto di spesa assenti |
| 9 | Passo 3 | Ripetizione, idempotenza e residui; set di valutazione versionato per i claim di qualità | Invito e upload verificati solo sul caso felice |
| 10 | Passo 5 | Una voce per bullet negli orizzonti; test `LATER` / `OUT-OF-SCOPE` | Esclusioni accorpate, ricerca cross-ricettario declassata |

## Punti di forza da non perdere

Cambiamenti allo skill che indebolissero questi comportamenti sarebbero una regressione rispetto a `PLAN-CC-CON-4.md`.

- Temi in corrispondenza 1:1 con il reference, ciascuno tracciato al numero della slice che lo valida per primo.
- Consultazione come tema autonomo, con una slice che consegna davvero la lettura della ricetta.
- Foto in una sola slice, con un solo proprietario dell'invariante di cover.
- Verifiche con letterali concreti e misure di latenza e costo confrontate con un target dichiarato.
- Un claim per bullet e nessuna ripetizione dei `Cross-functional concerns` dentro le slice.
