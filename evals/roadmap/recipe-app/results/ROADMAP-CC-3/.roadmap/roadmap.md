# Roadmap — Recipe App

**Goal:** Un ricettario condiviso tra famiglia e amici dove aggiungere una ricetta costa quasi
nulla — incolli un link, incolli il testo, o la scrivi — e dove la si ritrova cercando in
linguaggio naturale anche quando è scritta in un'altra lingua, a un costo di esercizio di pochi
centesimi al mese.

**Sources:** `sources/goal.md`, `sources/arch-choices.md`, `sources/tech-choices.md`,
`sources/concepts.md`.

**Current state:** Nulla è stato consegnato. Il progetto è greenfield: non esiste repository, non
esiste ambiente, non esiste codice. Le scelte di stack e di infrastruttura sono però già prese e
documentate, quindi la mappa le tratta come decise e non le rimette in discussione.

## Themes

| Theme | Promise | First validator |
|---|---|---|
| `ricettario` | Scrivo una ricetta a mano, la ritrovo nell'elenco del ricettario e la correggo quando voglio. | `S3` |
| `ricerca` | Cerco a parole mie e trovo la ricetta giusta dentro il ricettario corrente, anche quando è scritta in un'altra lingua. | `S4` |
| `import` | Aggiungo una ricetta senza scriverla: incollo il link, o incollo il testo della pagina quando il link non si legge, e vedo i passi reali dell'estrazione. | `S6` |
| `identita` | Entro con il mio account Google e vedo i ricettari di cui sono membro, passando dall'uno all'altro. | `S7` |
| `condivisione` | Invito familiari e amici in un ricettario con un link; dentro siamo tutti pari e lavoriamo sulle stesse ricette. | `S8` |
| `foto` | Ogni ricetta porta le sue foto — quella presa dal link e quelle che carico io — con una copertina che scelgo. | `S9` |

Verdetti sui confini fra temi:

- `ricettario` / `import` — **split.** L'inserimento a mano con la sua correzione produce evidenza
  utile da solo e resta in piedi se l'import viene cancellato; l'import non regge senza un posto
  dove atterrare, ma il test chiede che *almeno uno* dei due sia cancellabile. Form condiviso e
  stessa entità `Recipe` non sono ragione per fonderli.
- `import` interno (link, testo incollato) — **merge.** Stessa interazione, stesso motore di
  estrazione, stesso schema di output, stesso bersaglio di apprendimento; il testo incollato è
  dichiarato *fallback* del link e da solo non chiude nulla. Un tema, due righe.
- `ricerca` / tutto il resto — **split.** È il differenziatore dichiarato: può essere cancellata
  lasciando in piedi un ricettario condiviso (saremmo Mealie), e ogni altro tema resta valido se
  cade.
- `identita` / `condivisione` — **split.** L'invito è cancellabile lasciando intatta l'evidenza
  dell'accesso Google e dei ricettari personali; il contrario non vale, e tanto basta.
- `foto` / `ricettario` — **split.** Le foto sono rimandabili in blocco senza invalidare né
  l'inserimento né la ricerca, che indicizza solo testo. Condividere l'entità `Recipe` non è una
  ragione per fonderle.

## NOW

| Id | Title | Theme | Kind | Size | Readiness | Executor | Depends on |
|---|---|---|---|---|---|---|---|
| `S0` | [Repository e CI verde](slices/S0-repository-e-ci.md) | `—` | `enabler` | `small` | `ready` | `mixed` | — |
| `S1` | [Scheletro deployato su Fly con Postgres e migrazioni](slices/S1-scheletro-deployato.md) | `—` | `release` | `medium` | `ready` | `mixed` | — |
| `S2` | [Quale embedder regge la ricerca cross-lingua](slices/S2-spike-embedder-multilingue.md) | `ricerca` | `spike` | `medium` | `ready` | `agent` | — |
| `S3` | [Ricettario con ricette scritte a mano](slices/S3-ricette-a-mano.md) | `ricettario` | `product` | `medium` | `ready` | `agent` | — |
| `S4` | [Ricerca semantica cross-lingua nel ricettario](slices/S4-ricerca-semantica.md) | `ricerca` | `product` | `medium` | `ready` | `agent` | `S2` |
| `S5` | [Aggiungi da link con estrazione JSON-LD e progresso reale](slices/S5-add-da-link.md) | `import` | `product` | `large` | `ready` | `agent` | — |
| `S6` | [Estrazione LLM per link senza JSON-LD e testo incollato](slices/S6-estrazione-llm.md) | `import` | `product` | `medium` | `ready` | `agent` | — |
| `S7` | [Accesso Google e ricettari reali](slices/S7-accesso-google.md) | `identita` | `product` | `large` | `ready` | `mixed` | — |
| `S8` | [Invito a un ricettario con link condivisibile](slices/S8-invito-ricettario.md) | `condivisione` | `product` | `medium` | `needs-decision` | `agent` | `S7` |
| `S9` | [Foto della ricetta con copertina](slices/S9-foto-ricetta.md) | `foto` | `product` | `medium` | `ready` | `mixed` | — |
| `S10` | [Rilascio a famiglia e amici](slices/S10-rilascio.md) | `—` | `release` | `small` | `needs-info` | `mixed` | — |

## LATER

- Filtri di ricerca strutturati su tag e tempo, sui campi che l'estrazione popola già da subito.
- Ricerca ibrida: semantica più full-text, per i casi in cui si cerca un nome esatto.
- Ricerca che attraversa tutti i ricettari di cui sono membro.
- Ricettari pubblici tematici, come `visibility=public` sul ricettario esistente.
- Un concetto di gruppo sopra i ricettari, se ri-invitare le stesse persone diventasse fastidioso.
- Ruoli e permessi dentro un ricettario, oltre al solo `creatorId`.
- Cancellare una ricetta, e uscire da un ricettario.
- Revocare un invito e vedere gli inviti ancora attivi.
- Import da file esportati da altri ricettari, come Paprika o Mealie.
- Macchina Fly sempre calda, se il risveglio della prima richiesta desse davvero fastidio.
- Ridimensionamento e compressione delle foto caricate dal telefono.
- Passkeys accanto a Google, quando il recupero account sarà risolvibile.

## OUT-OF-SCOPE

- **Ingredienti strutturati in quantità e unità.** Poiché gli ingredienti restano testo libero,
  nessuna riga deve scrivere un parser, una tabella di unità o una normalizzazione: il prezzo è
  che lista della spesa e scaling delle porzioni restano preclusi finché l'esclusione regge.
- **Lista della spesa e scaling delle porzioni.** Poiché sono dichiarate irrisolte, il modello
  dati può fermarsi a `Recipe` senza entità ingrediente né step: il prezzo è non competere sulla
  collaborazione in cucina che altre app coprono.
- **Review obbligatoria prima del salvataggio.** Poiché non esiste, il flusso di aggiunta può
  salvare un'estrazione imperfetta e restare a un passo solo: il prezzo è che il ricettario
  contiene ricette sbagliate finché qualcuno non le corregge, e obbliga la correzione a esistere
  prima della prima riga che può produrne una.
- **Dedup delle ricette.** Poiché i duplicati sono consentiti, nessuna riga deve calcolare
  identità di contenuto né gestire fusioni: il prezzo è che lo stesso link salvato da due membri
  produce due ricette identiche.
- **Provider email.** Poiché non si invia posta, l'autenticazione può fare a meno di password,
  reset e magic link: il prezzo è la dipendenza da Google e l'esclusione di chi non ha un account
  Google.
- **Permessi granulari dentro un ricettario.** Poiché tutti i membri sono pari, nessuna riga deve
  modellare ruoli o liste di controllo: il prezzo è che un membro può riscrivere o rovinare il
  lavoro degli altri senza alcun freno.
- **Vector DB dedicato.** Poiché la scala dichiarata si ferma a diecimila ricette, dati e vettori
  stanno in un solo Postgres e nessuna riga deve gestire un secondo datastore: il prezzo è che
  oltre quella scala la scelta va rifatta da capo.
- **Infrastruttura come codice versionata.** Poiché l'infrastruttura resta un file di
  configurazione più la CLI del provider, nessuna riga deve mantenere moduli Terraform o simili:
  il prezzo è che ricreare l'ambiente da zero è manuale e documentato a mano.

## Assumptions

- `S1, goal` — Il datastore è **Neon**: `arch-choices.md` lascia aperto «Neon o Supabase», ma
  `tech-choices.md` nomina Neon quando decide il driver, e si prende quella lettura. La
  connessione è `postgres.js` su TCP diretto, senza pooler serverless, perché su Fly gira Node
  completo. Delivery la smentisce se il piano gratuito impone il pooler o chiude le connessioni
  sotto scale-to-zero.
- `S1, goal` — Il target di costo si legge come **pochi centesimi al mese**, non come zero
  stretto: `goal.md` riassume «tutto entro free tier» ma `arch-choices.md` dice nello stesso
  documento che Fly un free tier vero non ce l'ha più. Si parte con `suspend` più scale-to-zero,
  che è la strategia consigliata dalle sorgenti. La prima bolletta dopo lo scheletro la conferma
  o la smentisce.
- `S1` — pgvector è disponibile e abilitabile sul piano scelto, e lo scheletro lo dimostra
  eseguendo `CREATE EXTENSION vector` in una migrazione non di dominio, prima che qualunque riga
  di prodotto ci si appoggi.
- `S4, ricerca` — La query di ricerca **viene embeddata a runtime**, una chiamata per ricerca.
  `goal.md` e `arch-choices.md` dicono «mai a runtime sulle query», ma `concepts.md` definisce la
  ricerca come `similarity(Recipe.embedding, embedding(query))` e `arch-choices.md` aggiunge che
  «le query sono irrilevanti» sul costo: si legge il divieto come riferito all'estrazione LLM,
  non all'embedding della query. Cade se la latenza di quella chiamata domina la ricerca.
- `S6, import` — Il modello di estrazione è di classe Haiku con output strutturato validato da
  `Schema`, dietro una porta `Context.Tag` sostituibile: le sorgenti dicono «modello cheap,
  Haiku-class» senza sceglierne uno. La misura del tasso di fallimento della validazione durante
  la consegna la conferma o la smentisce.
- `S5, import` — Il progresso reale viaggia in **streaming HTTP** dal server verso il client: le
  sorgenti pretendono passi reali e non finti, ma non dicono con quale trasporto. Cade se il
  buffering della piattaforma impedisce lo streaming, e in quel caso la riga ripiega su polling
  di uno stato lato server, senza cambiare il resto della mappa.
- `S3, S7, goal` — Le righe che precedono l'accesso Google girano su un **ricettario seed
  configurato** dietro il resolver `currentCookbook`, con proprietario unico implicito e su
  ambiente non pubblico. Si assume che sostituire lo scope configurato con quello autenticato
  tocchi il solo resolver. Cade se l'identità deve rimettere mano alle query di dominio scritte
  prima di lei.
- `S7, identita` — Al primo accesso di un utente senza ricettari se ne crea uno di default con
  lui come `creator`: nessuna sorgente descrive l'onboarding, ma senza un ricettario corrente né
  elenco né ricerca hanno uno scope. Cade se l'autore vuole invece che il primo accesso porti a
  una schermata di scelta.

## Open questions

- `goal, ricerca` — Se la misura sull'embedder dicesse che nessun modello multilingue di
  commodity regge il cross-lingua alla qualità attesa, cade il differenziatore dichiarato, e le
  sorgenti stesse ammettono che senza di esso staremmo riscrivendo Mealie. Che cosa diventa
  allora il goal: ricerca ibrida, traduzione del testo in fase di aggiunta, o si accetta la
  parità con le alternative esistenti? Nessuna sorgente lo dice, e la risposta ridisegna la
  mappa, non una riga.
- `goal` — Non c'è politica dichiarata di backup e ripristino per l'unico datastore, né una
  risposta a cosa succede se il piano gratuito viene superato o se il progetto viene sospeso per
  inattività. Dati e indice vettoriale stanno tutti lì. La risposta può aggiungere una riga di
  operabilità al registro, quindi vive qui e non su una riga sola.

## Cross-functional concerns

- **Autorizzazione.** Ogni lettura e scrittura di ricette e foto passa dal resolver
  `currentCookbook`, che è l'unico posto dove si decide lo scope: nessuna query di dominio prende
  un identificativo di ricettario da input dell'utente non verificato. Dentro un ricettario i
  membri sono pari e non esiste controllo più fine dell'appartenenza. Il confine si verifica la
  prima volta sulla riga che persiste la prima ricetta, con scope configurato, e una seconda
  volta sulla riga dell'identità, con scope autenticato, allo stesso punto di sutura.
- **Validazione ed errori.** Gli errori attesi sono `Data.TaggedError` e si gestiscono ai
  boundary con `catchTag`; nessun errore nudo finisce nel canale d'errore. Ogni dato che arriva
  da fuori — HTML scaricato, output dell'LLM, risposta di un'API — si **decodifica** con `Schema`
  e non si asserisce mai con un cast. Un fallimento nella derivazione best-effort di tag, tempo o
  foto non blocca mai il salvataggio della ricetta.
- **Operabilità.** Ogni chiamata esterna — scaricare la pagina, l'LLM, gli embeddings, l'object
  storage — ha timeout esplicito e un numero finito di retry, e quando fallisce l'utente legge
  quale passo è fallito e non un errore generico. Ogni riga che spende soldi registra costo e
  latenza dei passi a pagamento in log strutturato. Il risveglio della macchina dopo inattività è
  atteso e non è un errore.
- **Accessibilità e sicurezza.** I campi obbligatori non si marcano con l'asterisco, gli
  opzionali si marcano «(optional)», e lo stato obbligatorio arriva alle tecnologie assistive
  dall'attributo nativo. I segreti — credenziali OAuth, chiavi LLM ed embeddings, chiavi
  dell'object storage — vivono solo come secret della piattaforma e mai nel repository. Un URL
  incollato è input non fidato: si scarica con timeout, con limite di dimensione della risposta e
  senza seguire redirect verso indirizzi di rete interna.
- **Integrità dei dati e recupero.** `Recipe` è la sola fonte di verità; l'embedding è un
  **indice derivato**, rigenerato a ogni modifica e ricostruibile da zero, e la sua assenza
  degrada la ricerca senza perdere dati. I duplicati sono ammessi per scelta: nessuna riga
  introduce dedup. Le foto stanno sull'object storage e il database tiene solo l'URL, quindi un
  upload fallito lascia la ricetta salvata e la foto mancante, mai il contrario.
- **Costo.** LLM ed embeddings si chiamano solo quando si aggiunge o si corregge una ricetta,
  mai nel percorso di lettura, e la sola eccezione dichiarata è l'embedding della query di
  ricerca. Nessuna riga introduce un servizio a canone fisso, e ogni riga che apre un servizio
  dichiara su quale piano gira e quanto ci si aspetta che costi alla scala prevista.
