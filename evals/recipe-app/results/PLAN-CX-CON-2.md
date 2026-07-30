# Recipe App — Piano di delivery ad alto livello

## Obiettivo e criteri di pianificazione

Portare in uso un ricettario privato condiviso che permetta di acquisire, correggere e
ritrovare ricette, validando presto i due differenziatori:

1. ricerca semantica multilingue;
2. estrazione LLM quando i dati strutturati non sono disponibili.

Fonti: `goal.md`, `concepts.md`, `arch-choices.md`, `tech-choices.md`. Il repository è
greenfield: al momento contiene solo documentazione.

Assunzioni di piano:

- una slice deve stare in un ciclo focalizzato di circa 3–5 giorni per uno sviluppatore;
- ogni slice arriva nell'ambiente rappresentativo ed è attivabile o revertibile da sola;
- l'embedding della query viene calcolato a runtime: è necessario per la ricerca semantica,
  nonostante alcuni documenti limitino gli embedding alla fase di add/edit;
- gli inviti sono link ad alta entropia, riutilizzabili e revocabili dal creator;
- i duplicati sono ammessi, come stabilito in `concepts.md`.

Baseline trasversale per tutte le slice:

- autorizzazione server-side sul ricettario corrente per ogni lettura e mutazione;
- validazione degli input ai boundary, errori attesi tipizzati e messaggi utente specifici;
- log strutturati senza contenuti delle ricette, token o segreti;
- test automatici proporzionati al rischio, migrazioni reversibili e monitoraggio degli
  adapter esterni per latenza, errori e costo;
- UI accessibile, campi obbligatori tramite `required` e soli campi opzionali etichettati.

## Prerequisito non-product — Repository verificabile

**Outcome:** ogni modifica produce un build ripetibile e un esito CI affidabile.

**Perché ora:** nessuna slice può essere verificata o rilasciata con sicurezza senza una
baseline automatizzata.

**Hard dependencies:** nessuna.

**Include:** progetto Next.js/TypeScript/Effect; configurazione coerente di formatting, lint,
typecheck e test; build del container; CI che esegue tutti i quality gate. Nessun provisioning
e nessun deploy.

**Verifica:** clone pulito, installazione deterministica e pipeline verde; un errore introdotto
in lint, tipi o test rende la pipeline rossa.

**Sblocca:** la walking skeleton e ogni slice successiva.

## Slice candidate

### Accesso al primo ricettario

**Outcome:** un utente entra con Google, crea un ricettario privato, lo seleziona e vede la
home vuota nell'ambiente rappresentativo.

**Perché ora:** walking skeleton minima; valida subito runtime, cold start, OAuth, connessione
Postgres e confine di sicurezza multi-tenant.

**Hard dependencies:** Repository verificabile.

**Include:** `User`, `Cookbook`, `Membership`; Auth.js con Google; creazione e selezione del
ricettario corrente; home vuota; Postgres/pgvector provisionato; Docker e Fly.io
scale-to-zero; segreti esterni al repository; estensione CI/CD e primo deploy; health check,
log e gestione degli errori OAuth/DB.

**Verifica:** da browser reale, login, creazione e riapertura del ricettario dopo suspend;
un secondo utente non membro non può leggerlo modificando URL o request; deploy e rollback
completano con successo.

**Sblocca:** verifica reale di tutte le funzioni scoped al ricettario.

### Ricetta trovabile oltre la lingua

**Outcome:** un membro inserisce una ricetta manuale, la vede nella home e la ritrova con una
query semanticamente pertinente in un'altra lingua.

**Perché ora:** è il differenziatore principale e testa l'ipotesi che giustifica il prodotto
rispetto a Mealie.

**Hard dependencies:** Accesso al primo ricettario.

**Include:** modello normalizzato `Recipe`; form condivisibile con gli altri ingressi ma
inizialmente vuoto; salvataggio; elenco; testo indicizzato completo; embedding multilingue;
similarità pgvector limitata al cookbook corrente; stati vuoto/loading/errore; metriche di
qualità, latenza e costo della ricerca. Foto escluse.

**Verifica:** corpus controllato italiano/inglese con query cross-lingua e casi negativi;
ricette di altri cookbook non compaiono; indisponibilità dell'embedder produce un errore
recuperabile senza dati parziali. Accettazione minima della qualità definita prima del test.

**Sblocca:** validazione go/no-go del posizionamento e indice derivato riusabile dagli altri
flussi; correzione post-salvataggio con verifica dell'indice.

### Testo non strutturato trasformato in ricetta

**Outcome:** un membro incolla il testo di una pagina, rivede campi estratti e salva la ricetta
nel proprio ricettario.

**Perché ora:** valida presto il secondo differenziatore e il fallback per paywall e siti
JS-heavy, prima di investire nello scraping esteso.

**Hard dependencies:** Accesso al primo ricettario.

**Include:** pulizia del testo; porta di estrazione e adapter LLM economico; structured output
decodificato con Schema; progress reale sui passi applicabili; form di review riusato; limiti
di dimensione, timeout e retry controllati; nessun salvataggio prima della conferma; telemetria
di esito e costo senza registrare il testo.

**Verifica:** set rappresentativo di testi rumorosi, incompleti e multilingue; accuratezza dei
campi confrontata con golden cases; output invalido o timeout non crea ricette e consente
retry/correzione manuale.

**Sblocca:** fallback riusabile dall'import URL.

### Ricetta correggibile con indice coerente

**Outcome:** un membro corregge una ricetta già salvata e i risultati di ricerca riflettono
subito e soltanto il nuovo contenuto.

**Perché ora:** completa la promessa di review post-salvataggio e valida l'invariante più
delicato tra dato canonico ed embedding derivato prima di aprire l'edit ad altri membri.

**Hard dependencies:** Ricetta trovabile oltre la lingua. Senza una ricetta realmente salvata,
indicizzata e ricercabile non è possibile osservare la transizione dal vecchio al nuovo indice;
una sola fixture non verifica il comportamento end-to-end.

**Include:** riapertura del form comune; update autorizzato dei campi normalizzati;
rigenerazione dell'embedding; consistenza atomica o stato esplicito e recuperabile se il provider
fallisce; concorrenza ottimistica per evitare sovrascritture silenziose; audit tecnico senza
registrare il contenuto.

**Verifica:** dopo la correzione, una query pertinente al vecchio testo non trova più la ricetta
e una pertinente al nuovo testo sì; provider indisponibile e due edit concorrenti non producono
una ricetta con embedding obsoleto né perdita silenziosa di dati.

**Sblocca:** verifica dell'editing paritario nel ricettario condiviso.

### Ricettario condiviso tra pari

**Outcome:** il creator condivide un link; un secondo utente entra nel ricettario e può vedere
e modificare le ricette come gli altri membri.

**Perché ora:** copre il secondo asse di valore del prodotto e verifica presto che il modello
cookbook-centrico sia comprensibile e sicuro.

**Hard dependencies:** Ricetta correggibile con indice coerente. Senza una mutazione di ricetta
già disponibile non è possibile dimostrare che membri diversi possano davvero “editare tutto”;
la sola membership o una fixture verifica soltanto la lettura.

**Include:** `Invitation`; emissione e revoca del link da parte del creator; join autenticato
e idempotente; membership N:N; switch tra più ricettari; riuso dell'edit esistente da parte di
ogni membro; protezione da token enumerabili, accessi cross-cookbook e race sul join. Nessun
ruolo granulare.

**Verifica:** due account reali condividono e modificano la stessa ricetta; lo stesso utente
può passare tra due cookbook senza contaminazione di dati o ricerca; link revocato, token
invalido e non membro sono rifiutati; dopo un edit la ricerca usa solo il nuovo contenuto.

**Sblocca:** uso familiare reale e feedback sul costo di reinvito per più ricettari.

### Import da URL con fallback trasparente

**Outcome:** un membro incolla un URL, segue l'avanzamento reale, corregge l'estratto e salva
la ricetta; l'app usa JSON-LD oppure passa automaticamente al fallback LLM.

**Perché ora:** è il percorso di acquisizione più frequente; arriva dopo aver provato
separatamente il rischio LLM e il form comune.

**Hard dependencies:** Accesso al primo ricettario.

**Include:** fetch sicuro con difese SSRF, redirect/size/time limit; parsing
`schema.org/Recipe`; fallback sull'adapter di estrazione; eventi reali
`Scarico pagina → Leggo ricetta → Trovo ingredienti`; `sourceUrl`; review prima del
salvataggio; messaggi distinti per URL invalido, sito irraggiungibile, paywall, contenuto non
riconoscibile e provider indisponibile. La persistenza delle foto resta esclusa.

**Verifica:** matrice di siti con JSON-LD, senza JSON-LD, redirect, JS-heavy/paywall e failure;
si osserva il ramo realmente eseguito, il fallback avviene solo quando previsto e nessun
fallimento lascia ricette parziali. Test SSRF coprono indirizzi locali e metadata endpoint.

**Sblocca:** percorso principale di acquisizione e sorgenti immagine per la galleria.

### Foto multiple e cover durevole

**Outcome:** un membro associa più foto a una ricetta, sceglie la cover e continua a vederle
anche se la sorgente originale sparisce.

**Perché ora:** completa la qualità del ricettario dopo aver validato ricerca, acquisizione e
condivisione; isola il rischio storage dal rischio di estrazione.

**Hard dependencies:** Accesso al primo ricettario.

**Include:** `Photo`; Cloudflare R2; copia delle immagini importate senza hotlinking; gestione
galleria e scelta cover; vincolo di una sola cover; validazione MIME/dimensione, nomi object
non prevedibili, cleanup compensativo e rimozione autorizzata; progress reale `Salvo foto`.

**Verifica:** più immagini importate restano disponibili con origine rimossa; cambio cover
atomico anche con due richieste concorrenti; file non ammesso e guasto R2 hanno esito
esplicito e non lasciano riferimenti DB o object orfani.

**Sblocca:** esperienza MVP completa.

## Grafo delle hard dependency

```text
Repository verificabile
└── Accesso al primo ricettario
    ├── Ricetta trovabile oltre la lingua
    │   └── Ricetta correggibile con indice coerente
    │       └── Ricettario condiviso tra pari
    ├── Testo non strutturato trasformato in ricetta
    ├── Import da URL con fallback trasparente
    └── Foto multiple e cover durevole
```

Non ci sono altre hard dependency: dati controllati o una capacità più stretta permettono di
verificare ciascun outcome senza forzare l'ordine raccomandato.

## Ordine raccomandato e vincoli deboli

1. Repository verificabile.
2. Accesso al primo ricettario.
3. Ricetta trovabile oltre la lingua.
4. Testo non strutturato trasformato in ricetta.
5. Ricetta correggibile con indice coerente.
6. Ricettario condiviso tra pari.
7. Import da URL con fallback trasparente.
8. Foto multiple e cover durevole.

Soft dependency:

- l'import URL segue preferibilmente l'estrazione da testo, così riusa un fallback già
  misurato;
- le foto seguono preferibilmente l'import URL, che fornisce sorgenti realistiche;
- la correzione segue preferibilmente il test LLM, così un eventuale stop strategico evita
  ulteriore investimento nel workflow.

Priority preference:

- ricerca cross-lingua prima di ogni funzione commodity, perché decide il posizionamento;
- fallback LLM subito dopo, perché è il secondo differenziatore e concentra costo e
  incertezza;
- correzione e condivisione prima di approfondire il flusso URL, per coprire presto tutti i
  temi core;
- foto per ultime, perché non cambiano il go/no-go del prodotto.

## Checkpoint decisionali

- **Dopo Ricetta trovabile oltre la lingua:** misurare rilevanza cross-lingua, latenza e
  costo. Se la qualità non supera la soglia concordata, fermare le slice non iniziate e
  valutare modello, composizione del testo o ricerca ibrida; non costruire un clone commodity.
- **Dopo Testo non strutturato trasformato in ricetta:** confrontare accuratezza, correzioni
  utente e costo per ricetta. Se insufficienti, restringere i contenuti supportati o cambiare
  provider prima dell'import URL.
- **Dopo Ricettario condiviso tra pari:** verificare comprensione di invito, cookbook corrente
  e reinvito. Solo evidenza di attrito rilevante giustifica anticipare un futuro concetto di
  gruppo.
- **Dopo Import da URL con fallback trasparente:** misurare copertura JSON-LD, frequenza del
  fallback e failure per categoria; adattare solo i parser che aumentano materialmente la
  copertura.
- **Dopo Foto multiple e cover durevole:** verificare consumo R2, orphan rate e limiti file
  prima di estendere upload o trasformazioni.

## Esclusioni MVP

- cookbook pubblici: valore futuro, nessuna necessità per validare il ricettario privato;
- filtri strutturati, full-text e ricerca ibrida: profondità prematura prima della misura
  semantica;
- ricerca cross-cookbook: contraddice lo scope deciso del cookbook corrente;
- gruppi/team e ruoli granulari: complessità non giustificata dal modello tra pari;
- email/password, magic link e passkey: Google OAuth è una decisione già presa;
- deduplica: i duplicati sono esplicitamente consentiti;
- vector database separato, IaC generalista e hosting sempre caldo: costo e complessità non
  giustificati alla scala prevista.

## Open questions

- Scegliere provider Postgres tra Neon e Supabase e modelli/provider effettivi per embedding
  ed estrazione: le fonti indicano alternative o esempi, non decisioni definitive.
- Confermare l'embedding della query a runtime e correggere i documenti che dichiarano
  “embedding solo in fase di add/edit”; senza questo non è implementabile la ricerca semantica
  su testo libero.
- Definire corpus e soglie go/no-go per rilevanza cross-lingua e accuratezza dell'estrazione;
  senza soglie i primi due checkpoint non producono una decisione verificabile.
- Le foto MVP provengono solo dalle pagine importate oppure è richiesto anche upload manuale
  per ricette inserite a mano/copia-incolla? La risposta cambia UI, sicurezza e verifica della
  slice foto.
