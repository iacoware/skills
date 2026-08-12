# Recipe App — Reference plan

Come taglierei io questo prodotto, scritto a mano dalle sole `sources/` e **prima** di aver visto
qualunque piano generato. È il gusto, non la regola: le regole stanno in `../MANUAL-REVIEW.md`, i
fatti sulle fonti in `EVALUATION-BRIEF.md`.

Serve a una cosa sola, che nessun altro artefatto fa: **impedire alla misura di «buono» di derivare
verso l'ultima cosa che un modello ha prodotto.** Per questo è congelato. Si riscrive solo se
cambiano le fonti — mai perché un candidato ha convinto.

**Regola d'uso, una sola: leggi il candidato e formulane il verdetto prima di aprire questo file.**
Poi confronta, e su ogni differenza chiediti chi dei due ha la ragione migliore. Non è un diff da
azzerare: titoli, numerazione, numero di temi, ordine e dettaglio d'esempio possono divergere tutti
senza che nulla sia rotto. Serve a farti notare cosa hai dimenticato, non cosa hai fatto diverso.

Le fonti prevalgono sempre. Dove questo file e `sources/` divergono, il difetto è qui.

**Fuori da ogni payload di generazione.** È la risposta.

Restaurato il 2026-08-11 da `6476f32^`, l'ultima versione prima che `EVALUATION-BRIEF.md` lo
sostituisse per servire un grader cieco. Tolte le sole cicatrici di quell'automazione: le quattro
classi di autorità, le annotazioni `Authority:` per sezione, il blocco
`Machine-readable expectations` che generava `expectations.json`, e il vocabolario da grading —
«oracolo», «penalizzato», «rubric». Nessuna delle 14 slice, dei temi, dei trigger o delle ragioni è
stata toccata.

## Ordering criteria

- Prima il percorso di consegna minimo, poi le convenzioni di dominio e UI su comportamento reale ma minuscolo, poi il rischio esistenziale.
- Lo skeleton prova che l'infrastruttura già decisa è connessa e gira; gli adapter usati da una sola slice restano in quella slice.
- Il differenziatore è la ricerca semantica cross-lingua: va validato prima di qualunque slice di acquisizione, perché senza di esso il prodotto è una riscrittura di Mealie.
- Slice iniziali minuscole finché le convenzioni di delivery, dominio, test e UI richiedono revisione umana frequente; più grandi dopo, solo perché i pattern esistono già nella codebase.
- Confine di scope dalla prima slice che persiste dati, con un resolver unico dello scope corrente; l'identità sostituisce lo scope configurato in quel solo punto, entro la prima slice destinata a utenti reali.
- Acquisizione dal caso più frequente ai fallback, senza aprire adapter nuovi finché il tema non è chiuso.
- LLM solo in fase di add o edit; l'uso dell'embedder sulla query è una contraddizione irrisolta nelle fonti che il piano deve esporre.
- Ogni slice resta nel free tier.

## Themes

| Theme | Desired outcome | First validation |
|---|---|---|
| Ricerca | Descrivo un piatto a parole mie e trovo la ricetta giusta anche se scritta in un'altra lingua | 4. Ricerca semantica cross-lingua |
| Consultazione | Vedo il contenuto del ricettario corrente e apro una ricetta per cucinarla | 5. Lettura della ricetta |
| Scrittura manuale | Salvo e correggo una ricetta a mano, senza passi obbligatori | 7. Inserimento manuale e modifica |
| Import automatico | Aggiungere una ricetta trovata online costa un incollaggio, anche quando il sito non collabora | 8. Import da URL con JSON-LD |
| Foto | Ogni ricetta è riconoscibile a colpo d'occhio senza lavoro manuale | 11. Foto della ricetta |
| Accesso | Entro con il mio account Google e vedo solo il mio ricettario | 6. Accesso Google e ricettario privato |
| Condivisione | Famiglia e amici contribuiscono allo stesso ricettario da pari | 12. Invito e collaborazione paritaria |

## NOW

Ogni campo `Evidenza` illustra come si dimostrerebbe la slice; è un esempio, non il solo modo.

Il `NOW` completo è consegnabile a utenti selezionati. Le slice 0–5 servono sviluppatori e revisori
umani; dalla 6 ogni incremento è utilizzabile da utenti reali. Ogni slice è verticale, verificabile
e revertibile.

### 0. Repository e CI *(Enabler: delivery)*

- **Esito:** ogni push produce un verdetto automatico di build, lint, typecheck e test.
- **Evidenza:** CI verde su un PR di prova; un errore di tipo e un test rotto introdotti ad arte la fanno fallire.
- **Fuori dalla slice:** provisioning, deploy, entità di dominio.
- **Perché qui:** stabilisce la cadenza di revisione prima che esista codice da rivedere.

### 1. Walking skeleton in ambiente dev *(Enabler: delivery)*

- **Esito:** uno sviluppatore verifica che runtime, database e pipeline di migrazione siano connessi e funzionanti nell'app deployata.
- **Evidenza:** un commit costruisce l'immagine e la distribuisce; la pipeline applica una migrazione non di dominio; la route diagnostica esegue una query reale sul database attraverso il driver scelto e risponde dopo deploy e dopo risveglio da `suspend`; cold start misurato come baseline, riconnessione al database inclusa.
- **Fuori dalla slice:** entità e CRUD di dominio, autenticazione, tenancy, object storage, provider di embedding, promozione in produzione.
- **Perché qui:** prova che l'infrastruttura decisa è connessa e in esecuzione sul path più sottile possibile, prima che un fallimento di connessione si confonda con uno di dominio.

### 2. Contesto del ricettario corrente *(Enabler: domain conventions)*

- **Esito:** uno sviluppatore crea il ricettario configurato tramite il percorso di produzione e ne apre la shell vuota.
- **Evidenza:** un input controllato crea e persiste il ricettario; la shell lo legge tramite il resolver unico dello scope; un id fuori scope risponde 404; i dati sopravvivono a un redeploy.
- **Fuori dalla slice:** creazione tramite UI, ricette, ricerca, identità.
- **Perché qui:** prima persistenza di dominio e prima revisione di dominio, scope, ORM, UI e test su un comportamento minimo; l'infrastruttura Postgres è già provata dalla slice 1 e questa slice non è una dipendenza della ricerca.

### 3. Pipeline di indicizzazione su fixture *(Enabler: ricerca semantica)*

- **Esito:** uno sviluppatore carica ricette fixture multilingue e ottiene da riga di comando un ranking per similarità prodotto dalla pipeline reale.
- **Evidenza:** il seed attraversa validazione, embedding cloud, persistenza e indice HNSW reali, senza vettori precalcolati; una frase in linguaggio naturale restituisce top-k con score, scoped al ricettario; costo token e latenza registrati.
- **Fuori dalla slice:** UI, acquisizione da fonti esterne.
- **Perché qui:** l'input più economico capace di validare il motore rischioso, senza attendere le slice di aggiunta.
- **Precondizione:** la contraddizione sull'embedding della query deve essere risolta prima di implementare e verificare il ranking.

### 4. Ricerca semantica cross-lingua *(Theme: Ricerca)*

- **Esito:** chi usa l'app descrive un piatto a parole proprie e ottiene le ricette pertinenti del ricettario corrente, anche se scritte in un'altra lingua.
- **Evidenza:** da browser, `pomodoro` e `cena leggera` trovano fixture inglesi; le ricette di un altro ricettario non compaiono mai; nessuna chiamata LLM nei log di ricerca; latenza percepita misurata.
- **Fuori dalla slice:** filtri strutturati, ricerca ibrida, dettaglio ricetta.
- **Perché qui:** rischio esistenziale, validato appena la pipeline lo rende osservabile.

### 5. Lettura della ricetta *(Theme: Consultazione)*

- **Esito:** si vede l'elenco delle ricette del ricettario e se ne apre una per cucinarla.
- **Evidenza:** un risultato di ricerca apre il dettaglio corrispondente; ingredienti e preparazione sono resi come testo a righe; l'id di una ricetta di un altro ricettario risponde 404.
- **Fuori dalla slice:** modifica, foto.
- **Perché qui:** completa il tema Consultazione sul contenuto reale e serve ogni tema successivo, restando minuscola.

### 6. Accesso Google e ricettario privato *(Theme: Accesso)*

- **Esito:** al primo accesso un utente crea automaticamente il proprio ricettario privato e lo vede al posto dello scope configurato.
- **Evidenza:** l'utente A non vede né cerca le ricette di B; l'accesso anonimo alle rotte di prodotto reindirizza al login; un secondo accesso non crea un secondo ricettario.
- **Fuori dalla slice:** inviti, ruoli, ricettari multipli, creazione esplicita di altri ricettari.
- **Perché qui:** è il punto in cui il resolver di scope passa da configurato ad autenticato, prima che il prodotto arrivi a utenti reali; da qui in poi ogni slice è consegnabile.

### 7. Inserimento manuale e modifica *(Theme: Scrittura manuale)*

- **Esito:** un membro salva una ricetta che conosce e corregge in seguito qualsiasi ricetta del ricettario.
- **Evidenza:** stessa form vuota in creazione e precompilata in modifica; il salvataggio non richiede campi oltre al nome; una ricetta creata a mano è trovabile con una query che non ne ripete le parole; una modifica cambia il ranking, a conferma della reindicizzazione.
- **Fuori dalla slice:** parsing di quantità e unità, foto, review obbligatoria.
- **Perché qui:** stabilisce la form condivisa e il percorso salva + reindicizza che tutte le slice di import riusano come superficie di correzione.

### 8. Import da URL con JSON-LD *(Theme: Import automatico)*

- **Esito:** un membro incolla l'URL di un food blog e ottiene la ricetta salvata senza review.
- **Evidenza:** URL con JSON-LD salvato con `sourceUrl` valorizzato e zero chiamate LLM; paywall e JSON-LD assente producono un messaggio specifico sul passo fallito e nessuna ricetta creata; hit-rate del JSON-LD sul campione reale registrato.
- **Fuori dalla slice:** LLM, foto, testo incollato.
- **Perché qui:** caso di acquisizione più frequente e percorso gratuito, prima di qualunque costo variabile.

### 9. Fallback LLM per URL non strutturati *(Theme: Import automatico)*

- **Esito:** anche le pagine senza dati strutturati producono una ricetta salvata, senza intervento dell'utente.
- **Evidenza:** su un campione annotato la ricetta salvata contiene ingredienti e preparazione corretti; output non conforme allo schema non produce salvataggi parziali; le metriche distinguono parse diretto e fallback pagato; costo medio per estrazione confrontato con la soglia.
- **Fuori dalla slice:** nuovo flusso di add — il fallback si innesta nel passo `Leggo ricetta` esistente.
- **Perché qui:** secondo differenziatore, subito dopo il percorso gratuito che ne delimita l'uso.

### 10. Import da testo incollato *(Theme: Import automatico)*

- **Esito:** quando il link non è leggibile, un membro incolla il testo della pagina e ottiene la stessa ricetta salvata.
- **Evidenza:** testo da pagina con paywall salvato e trovabile, senza chiamate HTTP alla fonte; un testo che non è una ricetta produce un errore preciso senza salvataggio; progresso ridotto ai passi realmente eseguiti.
- **Fuori dalla slice:** OCR, import da file.
- **Perché qui:** chiude il tema acquisizione riusando motore e schema della 9, senza aprire adapter nuovi.

### 11. Foto della ricetta *(Theme: Foto)*

- **Esito:** le ricette importate arrivano già con la foto e un membro può aggiungerne altre a mano.
- **Evidenza:** l'immagine di `schema.org/Recipe` o `og:image` è scaricata e riservita dal proprio storage, mai in hotlink; l'upload manuale accetta più foto; la prima è cover; un file oltre limite o un download fallito non blocca il salvataggio della ricetta; le foto restano servibili dopo un redeploy.
- **Fuori dalla slice:** scelta manuale della cover, scelta di quali foto tenere durante l'import.
- **Perché qui:** input diversi su una sola pipeline media, aperta una volta sola quando l'acquisizione testuale è chiusa.

### 12. Invito e collaborazione paritaria *(Theme: Condivisione)*

- **Esito:** il creator condivide un link e chi lo apre entra nel ricettario come membro pari.
- **Evidenza:** B accetta l'invito di A, legge e modifica le ricette di A, e A vede le modifiche; accettazione idempotente per lo stesso membro; token scaduto o revocato non crea `Membership`; con più ricettari, elenco e ricerca seguono quello selezionato.
- **Fuori dalla slice:** ruoli, permessi granulari, creazione di ricettari aggiuntivi dall'interfaccia.
- **Perché qui:** ultimo tema, unico che richiede identità già presente.

### 13. Rilascio agli utenti pilota *(Release: delivery)*

- **Esito:** famiglia e amici usano l'app in produzione, entro il budget dichiarato.
- **Evidenza:** due utenti reali completano in produzione import, ricerca, modifica e condivisione; costo del primo mese misurato contro il target di centesimi; backup con prova di ripristino; tetto di spesa e allarme su LLM ed embedding.
- **Fuori dalla slice:** nuove capability di prodotto.
- **Perché qui:** senza questa slice `NOW` non raggiunge mai gli utenti dichiarati e il vincolo di costo non viene mai misurato sul campo.

## Vincoli che questo piano tratta come non negoziabili

Quattro sono anche in `EVALUATION-BRIEF.md` § `Hard constraints`; gli altri quattro — idempotenza,
salvataggi parziali e SSRF, backup e tetti di spesa, separazione CI/skeleton — stanno solo qui.

- Repository/CI e walking skeleton sono separati; lo skeleton usa deploy, database reale e migration runner con operazioni non di dominio, senza CRUD, autenticazione o tenancy.
- La pipeline reale di indicizzazione precede il validatore di ricerca; la ricerca semantica cross-lingua precede l'acquisizione perché è il rischio esistenziale dichiarato.
- Il confine di scope si applica dalla prima persistenza tramite un resolver unico; l'identità lo sostituisce allo stesso seam prima della prima audience reale.
- Il primo accesso autenticato crea il primo ricettario in modo idempotente.
- L'import URL prova prima JSON-LD; l'LLM è recovery automatico dello stesso flusso; il testo incollato è il successivo escape manuale.
- Output non validi, timeout o fallimenti esterni non producono salvataggi parziali; URL remoti applicano protezione SSRF.
- `NOW` raggiunge utenti selezionati in produzione, con backup ripristinabile e limiti/allarmi di spesa per LLM ed embedding.
- La contraddizione sull'embedding della query e le scelte provider/modello restano esplicite e bloccano le slice indicate finché non risolte.

## Preferred ordering and decomposition

- Un enabler di dominio minuscolo valida persistenza, resolver di scope, shell, UI e test prima dell'indicizzazione.
- La pipeline di indicizzazione è immediatamente adiacente alla ricerca.
- Una form condivisa di inserimento e modifica precede il primo import.
- Le foto arrivano dopo l'acquisizione testuale e hanno un solo owner della pipeline media e della cover.
- L'invito è l'ultimo tema di prodotto.

## LATER

Una fonte può sostenere una classificazione diversa da questa.

- **Scelta manuale della cover** — *Trigger:* utenti pilota che segnalano la prima foto come rappresentazione sbagliata. *Valore:* rifinitura di un default già spedito.
- **Scelta di quali foto tenere durante l'import** — *Trigger:* import che portano immagini irrilevanti in modo sistematico. *Valore:* qualità della galleria senza reintrodurre una review obbligatoria.
- **Filtri strutturati (tag, tempo) e ricerca ibrida semantica + full-text** — *Trigger:* query reali che la sola semantica sbaglia sistematicamente, tipo "senza glutine" o "meno di 30 minuti". *Valore:* `tags` e `prepTime` sono già popolati, quindi attivabili senza migrazione.
- **Ricerca cross-ricettario** — *Trigger:* utenti con più ricettari che cercano ripetutamente nello scope sbagliato. *Valore:* elimina il cambio di contesto manuale.
- **Creazione di ricettari aggiuntivi dall'interfaccia** — *Trigger:* un gruppo chiede di separare i contenuti oltre al ricettario creato al primo accesso. *Valore:* il modello N:N esiste già.
- **Ricettari pubblici tematici** — *Trigger:* richiesta di condividere fuori dal gruppo invitato. *Valore:* `visibility=public` è già modellato.
- **Concetto di gruppo sopra i ricettari** — *Trigger:* ri-invitare gli stessi membri a ogni nuovo ricettario diventa attrito segnalato. *Valore:* additivo sopra `Membership`.
- **Macchina Fly sempre calda** — *Trigger:* cold start percepito come fastidioso dagli utenti pilota. *Valore:* un flag reversibile in `fly.toml` al costo noto di ~$3/mese.
- **Passkeys** — *Trigger:* la dipendenza da Google limita l'adozione e il recupero account in Auth.js matura. *Valore:* accesso senza password senza provider email.

## OUT-OF-SCOPE

Esclusioni esplicite delle fonti, non lavoro obbligatorio lasciato incompleto.

- **Ingredienti strutturati (quantità e unità)** — trade-off accettato in `goal.md`: la ricerca è semantica e chi legge interpreta il testo.
- **Lista della spesa e scaling delle porzioni** — dipendono dagli ingredienti strutturati.
- **Review obbligatoria prima del salvataggio** — bloccare l'utente a ogni aggiunta è il costo che il prodotto elimina; la correzione resta disponibile come edit.
- **Deduplica delle ricette** — duplicati consentiti per scelta esplicita in `concepts.md`.
- **Ruoli e permessi granulari** — nell'MVP basta `creatorId` e tutti i membri sono pari.
- **Email + password e magic link** — richiedono comunque un provider email.
- **Vector DB dedicato** — a ≤10k ricette pgvector con HNSW è già istantaneo.
- **IaC versionata (SST, Terraform)** e **hosting su Vercel o Cloudflare Workers** — scartati in `arch-choices.md` per costo e complessità.

## Cross-functional concerns attesi

Le sette preoccupazioni sono dovute; la formulazione e il dettaglio operativo qui sotto sono un modo
di dirle, non l'unico.

- **Scope:** un resolver unico possiede il ricettario corrente; ogni lettura e scrittura è filtrata su di esso e un id fuori scope risponde 404. La slice 6 sostituisce lo scope configurato con la membership autenticata in quell'unico punto.
- **Validazione ed errori:** ogni input non fidato (HTML remoto, JSON-LD, output LLM, payload di form) decodificato con `Schema`, mai asserito; nessun salvataggio parziale quando la decodifica fallisce.
- **Operabilità:** timeout e retry espliciti sugli adapter esterni; log strutturato per passo con esito, durata e token; il progresso mostrato all'utente riflette i passi reali e nomina il passo fallito.
- **Sicurezza:** URL forniti dall'utente protetti da SSRF con host e schemi consentiti; upload limitati per tipo e dimensione; chiavi e segreti solo a runtime; token di invito ad alta entropia.
- **Integrità dei dati:** una sola cover per ricetta; embedding rigenerato a ogni modifica indicizzata; duplicati consentiti deliberatamente.
- **Costo:** ogni slice resta nel free tier; LLM e embedding delle ricette operano solo in add o edit; il costo dell'embedding della query resta subordinato alla decisione aperta.
- **Accessibilità:** flussi da tastiera, stato e progresso annunciati, campi opzionali marcati `(optional)` e nessun asterisco sui campi obbligatori.

## Decision checkpoints attesi

Consigliati, non una precedenza esatta.

- **Dopo la 4:** qualità del ranking cross-lingua, latenza e costo → cambiare modello di embedding, oppure rimettere in discussione la proposta di valore.
- **Dopo la 8:** hit-rate del JSON-LD sui siti realmente usati → restringere o anticipare il fallback LLM.
- **Dopo la 9:** costo medio per estrazione → cambiare modello o limitare il fallback ai casi espliciti.
- **Dopo la 13:** cold start e costo misurati sugli utenti pilota → promuovere la macchina sempre calda o restare su scale-to-zero.

## Open questions attese

Le fonti non decidono questi punti; una slice bloccata non può affermare silenziosamente una scelta.

- **Embedding della query a runtime:** `goal.md:110` e `arch-choices.md:33` lo vietano, mentre `concepts.md:153` richiede `embedding(query)`; blocca implementazione e verifica delle slice 3 e 4.
- **Provider Postgres:** Neon o Supabase; blocca lo skeleton della slice 1, perché determina driver, modalità di connessione e limiti del free tier.
- **Modello di embedding:** deve essere multilingue; blocca la pipeline della slice 3.
- **Modello LLM:** deve supportare output strutturato entro il budget; blocca il fallback della slice 9.

## Tensioni note con le fonti

Ambiguità o incompletezze delle fonti, dove le scelte qui sotto sono legittime quanto le mie a patto
che conservino le condizioni indicate. Questo piano non risolve le decisioni elencate in
`Open questions attese`; sulle altre tensioni, un piano che sceglie diversamente si giudica sulla
motivazione.

- **Cover cambiabile:** `goal.md:74` la dichiara, questo piano la mette in `LATER` come rifinitura di un default già spedito. Un piano che la tiene in `NOW` non è in errore se la mantiene dentro la slice 11.
- **Scelta delle foto durante l'import:** interazione a tempo di add, in tensione con "nessun passo obbligatorio prima del salvataggio" (`concepts.md:144`). Questo piano la rinvia.
- **Embedding della query a runtime:** questo piano non sceglie un'interpretazione; un piano corretto espone la contraddizione, le slice bloccate e non afferma contemporaneamente entrambe le condizioni.
- **Promozione in produzione:** questo piano applica la prescrizione dello skill e usa `(Release: delivery)`; ometterla o riclassificarla in silenzio è un errore.
- **Provider aperti:** Postgres (Neon o Supabase), modello di embedding e modello LLM restano decisioni non prese nelle fonti. Vanno in `Open questions` con la slice che bloccano, mai scelte in silenzio dentro una slice.
