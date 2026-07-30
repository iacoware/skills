# Recipe App — Piano di delivery

Piano di alto livello derivato da
[`goal.md`](../goal.md), [`concepts.md`](../concepts.md),
[`arch-choices.md`](../arch-choices.md) e [`tech-choices.md`](../tech-choices.md);
il repository contiene al momento solo la documentazione.

## Principi di pianificazione

- Validare presto il vero differenziatore: ricerca semantica multilingue cross-lingua.
- Usare fixture controllate per testare la ricerca prima dei flussi completi di acquisizione.
- Validare il modello normalizzato e la review con l'input manuale prima delle integrazioni
  esterne.
- Consegnare JSON-LD e fallback LLM separatamente per misurarne affidabilità e costo.
- Mantenere ogni incremento entro il ricettario corrente, con costi compatibili con il target
  di circa $0/mese.

## Temi

| Tema | Risultato desiderato |
|---|---|
| A. Ritrovare | L'utente ritrova nel ricettario corrente ricette pertinenti anche quando query e ricetta sono in lingue diverse. |
| B. Acquisire e curare | L'utente salva ricette corrette da input manuale, URL o testo e ne mantiene contenuti e foto. |
| C. Condividere | Più utenti collaborano come pari nello stesso ricettario senza esporre dati di altri ricettari. |

## Baseline trasversale

Ogni slice applica autorizzazione server-side per membership e ricettario corrente, validazione
Schema agli ingressi non fidati, errori applicativi tipizzati, messaggi utili senza dati sensibili,
logging dei passi e dei fallimenti, UI accessibile e test automatici. Le operazioni esterne hanno
timeout e fallimenti espliciti; progress e stato mostrano solo passi reali. Dati e vettori restano
in Postgres, foto in R2; i duplicati sono ammessi. Ogni rilascio mantiene build Docker ripetibile,
migrazioni versionate, rollback applicativo e compatibilità con scale-to-zero.

## 0. Base repository e CI

**Outcome:** Il team dispone di una base ripetibile che segnala regressioni prima del merge.

**Includes:** Next.js App Router e TypeScript; Effect 3, Drizzle, Vitest e convenzioni di progetto;
configurazione locale; schema iniziale; build Docker; CI con lint, typecheck, test e build, senza
provisioning né deploy.

**Verification:** Una checkout pulita installa, esegue migrazioni su un database di test e supera
lint, typecheck, test e build Docker in CI; un errore intenzionale rende la pipeline rossa.

## 1. Ricettario privato deployato *(Tema: C)*

**Outcome:** Un utente accede con Google, crea un ricettario privato e ne vede l'elenco ricette
vuoto nell'ambiente rappresentativo.

**Includes:** Auth.js con Google OAuth; User, Cookbook e Membership; creazione e selezione del
ricettario corrente; home vuota; provisioning Neon/Supabase e Fly.io; migrazioni, secret e
pipeline di deploy minimi.

**Verification:** Da browser, un nuovo utente completa OAuth, crea un ricettario, ricarica la home
e lo ritrova vuoto; un utente non membro non può leggerlo. CI distribuisce la stessa immagine
verificata su Fly.io e uno smoke test passa dopo un risveglio da suspend.

## 2. Ricerca semantica cross-lingua *(Tema: A)*

**Outcome:** L'utente cerca nella propria lingua e trova ricette pertinenti scritte in un'altra
lingua, limitatamente al ricettario corrente.

**Includes:** Recipe ed embedding derivato; adapter cloud multilingue; pgvector e query di
similarità; campo ricerca nella home; corpus bilingue controllato caricato come fixture.

**Verification:** Su un corpus rappresentativo e versionato, query italiane come “pomodoro”
portano ricette inglesi pertinenti entro la soglia di ranking concordata; ricette semanticamente
estranee e appartenenti a un altro ricettario non compaiono. Si registrano qualità, latenza e costo
per query per decidere se la proposta distintiva è sostenibile.

## 3. Inserimento manuale con review *(Tema: B)*

**Outcome:** L'utente compila, rivede e salva una ricetta manuale che compare nel ricettario
corrente ed è ricercabile.

**Includes:** Form condiviso inizialmente vuoto; nome, ingredienti, preparazione, tempo e tag;
validazione; persistenza normalizzata; generazione dell'embedding al salvataggio; elenco ricette e
dettaglio minimo.

**Verification:** Un membro salva una ricetta valida, la ritrova dopo il reload e tramite ricerca;
input invalido non produce dati parziali, mentre un non membro non può salvarla nel ricettario.

## 4. Import URL con JSON-LD *(Tema: B)*

**Outcome:** L'utente incolla un URL supportato, segue l'avanzamento reale e rivede una ricetta
estratta senza chiamare il fallback LLM.

**Includes:** Fetch HTTP; pulizia HTML; rilevamento e parsing di `schema.org/Recipe`; mapping al
modello normalizzato; `sourceUrl`; form di review condiviso; avanzamento sincrono e fallimenti
precisi per download, lettura e ingredienti.

**Verification:** Pagine controllate con JSON-LD valido producono una review correggibile e poi una
ricetta ricercabile; la telemetria dimostra zero chiamate LLM. Timeout, URL non sicuri, markup
invalido e pagina irraggiungibile restituiscono il passo fallito senza salvataggi parziali.

## 5. Fallback LLM da URL *(Tema: B)*

**Outcome:** L'utente ottiene una ricetta rivedibile anche da una pagina leggibile priva di
`schema.org/Recipe`.

**Includes:** Adapter per modello economico; prompt e output strutturato; decodifica Schema;
attivazione solo dopo l'assenza di JSON-LD; stessi progress, review e persistenza del percorso
primario.

**Verification:** Un campione versionato di pagine senza JSON-LD produce campi utili entro le
soglie concordate di accuratezza e costo; output malformato, contenuto non pertinente e failure del
provider generano errori precisi e nessuna ricetta corrotta.

## 6. Estrazione da testo incollato *(Tema: B)*

**Outcome:** L'utente aggira paywall o pagine non leggibili incollando il testo e ottenendo la
stessa review normalizzata.

**Why now:** Riusa l'adapter LLM già misurato, ma resta un ingresso indipendente e può essere
riordinato dopo il relativo checkpoint.

**Includes:** Input testo; pulizia; estrazione strutturata LLM; review condivisa; salvataggio ed
embedding, senza fetch né tentativo JSON-LD.

**Verification:** Testo copiato da una pagina non accessibile produce una ricetta correggibile e
ricercabile; testo vuoto, non culinario o output invalido falliscono chiaramente senza scritture
parziali.

## 7. Correzione dopo il salvataggio *(Tema: B)*

**Outcome:** Un membro corregge una ricetta esistente e la ricerca riflette subito il contenuto
aggiornato.

**Includes:** Riutilizzo del form di review; update atomico dei dati normalizzati; rigenerazione
dell'embedding quando cambia il testo indicizzato; gestione esplicita dei fallimenti del provider.

**Verification:** Modificando ingredienti o preparazione cambiano dettaglio e risultati semantici
dopo il reload; un errore di embedding non lascia testo e vettore incoerenti; un estraneo riceve
accesso negato.

## 8. Invito e accesso al ricettario *(Tema: C)*

**Outcome:** Un utente autenticato apre un link/codice condivisibile e diventa membro del
ricettario invitante senza perdere gli altri ricettari.

**Includes:** Invitation con token non prevedibile; creazione del link da parte del creator;
accettazione autenticata idempotente; membership N:N; selezione del ricettario raggiunto e
isolamento degli altri.

**Verification:** Un secondo account accetta l'invito, vede il ricettario dopo un nuovo login e può
passare fra i propri ricettari; token alterato o riferito a un ricettario non accessibile non
concede membership.

## 9. Modifica paritaria condivisa *(Tema: C)*

**Outcome:** Ogni membro modifica le ricette condivise con gli stessi poteri degli altri membri.

**Why now:** Una ricetta già modificabile rende verificabile il modello di collaborazione senza
introdurre ruoli o permessi granulari.

**Includes:** Autorizzazione uniforme basata su Membership per lettura e modifica; aggiornamento
visibile agli altri membri; `creatorId` senza ruolo applicativo aggiuntivo.

**Verification:** Invitato e creator modificano la stessa ricetta in sessioni separate e vedono
l'ultimo stato persistito; un utente esterno non legge né modifica ricetta, embedding o foto.

## 10. Foto sorgente durevole *(Tema: B)*

**Outcome:** La foto principale trovata durante un import URL resta disponibile senza dipendere
dal sito sorgente.

**Includes:** Rilevamento della foto da JSON-LD/metadata; download controllato; upload su
Cloudflare R2; Photo e cover iniziale; passo reale “Salvo foto”; limiti di tipo e dimensione.

**Verification:** Dopo l'import e la rimozione della risorsa sorgente, la cover continua a essere
servita da R2; file non valido o upload fallito non crea riferimenti rotti e indica il passo
fallito.

## 11. Galleria foto e scelta cover *(Tema: B)*

**Outcome:** L'utente associa più foto a una ricetta e sceglie quale mostrare come cover.

**Includes:** Upload multiplo controllato; elenco foto; selezione atomica di una sola cover;
visualizzazione coerente in elenco e dettaglio.

**Verification:** Un membro aggiunge più foto, cambia cover e ritrova la scelta dopo il reload;
database e UI non espongono mai più di una cover, upload parzialmente falliti sono segnalati e un
estraneo non può caricare o cambiare foto.

## Grafo delle dipendenze forti

```text
Base repository e CI
└── Ricettario privato deployato
    ├── Ricerca semantica cross-lingua
    ├── Inserimento manuale con review
    ├── Import URL con JSON-LD
    │   ├── Fallback LLM da URL
    │   └── Foto sorgente durevole
    ├── Estrazione da testo incollato
    ├── Correzione dopo il salvataggio
    ├── Invito e accesso al ricettario
    ├── Modifica paritaria condivisa
    └── Galleria foto e scelta cover
```

## Ordine raccomandato e vincoli deboli

La ricerca precede l'acquisizione completa perché fixture controllate bastano a validare il
differenziatore. L'inserimento manuale precede gli import per stabilizzare modello e review a costo
basso. Correzione, inviti e modifica paritaria seguono i due rischi distintivi per completare presto
un percorso collaborativo reale. Il testo incollato preferisce il fallback URL già misurato, ma può
essere anticipato. R2 e gestione foto arrivano dopo i flussi core perché non ne determinano la
validità e possono essere riordinate indipendentemente.

## Checkpoint decisionali

- **Dopo Ricerca semantica cross-lingua:** qualità sul corpus bilingue, latenza e costo → confermare
  il differenziatore oppure cambiare modello, indicizzazione, soglie o priorità del prodotto.
- **Dopo Fallback LLM da URL:** accuratezza, failure rate e costo sul campione senza JSON-LD →
  cambiare provider/prompt, limitare i siti supportati o anticipare il copia-incolla.
- **Dopo Modifica paritaria condivisa:** test con utenti reali su invito, isolamento e assenza di
  ruoli → mantenere il modello cookbook-centrico oppure fermare le estensioni e rivedere membership
  e autorizzazione.

## Fuori scope

- Ricettari pubblici tematici: evoluzione successiva tramite `visibility=public`.
- Filtri per tag/tempo, full-text e ricerca ibrida: il MVP valida solo la semantica.
- Gruppi o team sopra i ricettari: da introdurre solo se i reinviti risultano onerosi.
- Ricerca cross-ricettario e ruoli/permessi granulari: contrari allo scope e alla semplicità MVP.
- Password, magic link e passkey: Google OAuth è la decisione MVP.
- Deduplicazione delle ricette, vector DB dedicato e IaC multi-cloud: complessità senza valore alla
  scala prevista.

## Domande aperte

- La ricerca richiede l'embedding della query al runtime, come indicato in `concepts.md`, ma
  `goal.md` e `arch-choices.md` dichiarano che embedding/LLM sono usati solo in add/edit e mai sulle
  query: quale vincolo prevale? Senza embedding runtime di una query arbitraria serve un diverso
  disegno della ricerca semantica.
