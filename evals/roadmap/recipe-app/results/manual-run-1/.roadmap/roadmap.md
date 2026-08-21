# Roadmap — Recipe App

**Goal:** Un ricettario condiviso in cui le ricette entrano quasi da sole — da link, da testo
incollato o a mano — e si ritrovano descrivendole a parole proprie anche quando sono scritte in
un'altra lingua, a centesimi al mese.

**Sources:** `sources/goal.md`, `sources/concepts.md`, `sources/arch-choices.md`,
`sources/tech-choices.md`.

**Current state:** Niente è stato consegnato. Questo è il primo disegno: non esiste repository, non
esiste ambiente, non esiste codice. Le scelte di infrastruttura e di stack sono prese sulla carta e
nessuna è ancora stata messa alla prova.

## Themes

| Theme | Promise | First validator |
|---|---|---|
| `ricettario` | Le ricette stanno in un posto solo: le scrivi come ti vengono, le rileggi, le correggi quando serve. | `S3` |
| `ricerca` | Trovi una ricetta descrivendola a parole tue, anche se è scritta in un'altra lingua. | `S4` |
| `import` | Aggiungi una ricetta senza riscriverla: incolli il link e la ricetta è dentro. | `S5` |
| `identità` | Entri con Google e quello che salvi è tuo; chi non è entrato non vede niente. | `S7` |
| `condivisione` | Apri il ricettario a chi vuoi con un link, e dentro siete tutti pari. | `S8` |

## NOW

| Id | Title | Theme | Kind | Size | Readiness | Executor | Depends on |
|---|---|---|---|---|---|---|---|
| `S0` | [Repository, CI, account e segreti](slices/S0-repository-ci-account-segreti.md) | `—` | `enabler` | `small` | `ready` | `mixed` | — |
| `S1` | [Scheletro deployato: Fly, Postgres, migrazioni](slices/S1-scheletro-deployato.md) | `—` | `release` | `medium` | `ready` | `mixed` | `S0` |
| `S2` | [Spike: recupero cross-lingua misurato su corpus reale](slices/S2-spike-recupero-cross-lingua.md) | `ricerca` | `spike` | `medium` | `ready` | `agent` | `S1` |
| `S3` | [Ricette a mano nel ricettario: crea, elenca, leggi, correggi](slices/S3-ricette-a-mano.md) | `ricettario` | `product` | `medium` | `ready` | `agent` | `S1` |
| `S4` | [Ricerca semantica cross-lingua nel ricettario](slices/S4-ricerca-semantica.md) | `ricerca` | `product` | `medium` | `ready` | `agent` | `S2`, `S3` |
| `S5` | [Aggiungi da link: JSON-LD, fallback LLM, avanzamento reale](slices/S5-aggiungi-da-link.md) | `import` | `product` | `large` | `ready` | `agent` | `S3` |
| `S6` | [Copia-incolla: la via d'uscita quando il link non si legge](slices/S6-copia-incolla.md) | `import` | `product` | `medium` | `ready` | `agent` | `S5` |
| `S7` | [Entri con Google: il ricettario è tuo](slices/S7-entri-con-google.md) | `identità` | `product` | `medium` | `needs-decision` | `mixed` | `S3` |
| `S8` | [Inviti con un link: membri pari nello stesso ricettario](slices/S8-inviti-con-un-link.md) | `condivisione` | `product` | `medium` | `needs-decision` | `agent` | `S7` |
| `S9` | [Foto delle ricette: più di una, con la copertina](slices/S9-foto-delle-ricette.md) | `ricettario` | `product` | `medium` | `ready` | `agent` | `S5` |
| `S10` | [In mano a famiglia e amici](slices/S10-in-mano-a-famiglia-e-amici.md) | `—` | `release` | `small` | `ready` | `mixed` | `S8`, `S9` |

## LATER

- Filtri strutturati per tag e tempo, e ricerca ibrida semantica + full-text: i campi si popolano già
  in automatico dalla prima estrazione, quindi mancherebbe solo l'interfaccia.
- Ricerca su tutti i ricettari a cui si appartiene, non solo su quello corrente.
- Ricettari pubblici tematici, con `visibility=public` sul ricettario che esiste già.
- Un concetto di gruppo sopra i ricettari, se ri-invitare le stesse persone in ogni ricettario
  diventasse fastidioso.
- Togliere un membro da un ricettario, o uscirne di propria iniziativa.
- Passkeys accanto a Google, quando il recupero del dispositivo perso avrà una risposta.
- Macchina Fly sempre calda a circa tre dollari al mese, se il cold start desse fastidio.
- Ridimensionamento delle foto e miniature, se il peso delle pagine o il free tier dell'object
  storage lo chiedessero.

## OUT-OF-SCOPE

- **Ingredienti strutturati, con quantità e unità.** Poiché gli ingredienti restano testo libero,
  l'implementazione può fare a meno di un parser, di un modello di unità di misura e di un'entità
  ingrediente; il prezzo è che lista della spesa e scaling delle porzioni restano impossibili senza
  tornare sul modello dati.
- **Review obbligatoria prima del salvataggio.** Poiché non si rivede niente prima di salvare, il
  flusso di aggiunta può fare a meno di uno stato di bozza, di un'approvazione e di una schermata di
  conferma; il prezzo è che un'estrazione imperfetta resta visibile nel ricettario finché qualcuno
  non la corregge.
- **Deduplica delle ricette.** Poiché i duplicati sono ammessi, l'aggiunta può fare a meno di un
  indice di URL canonici, di un confronto di similarità in scrittura e di un'interfaccia di merge; il
  prezzo è che la stessa ricetta può comparire due volte nello stesso ricettario.
- **Ruoli e permessi granulari.** Poiché dentro un ricettario tutti sono pari, l'autorizzazione è un
  solo controllo di appartenenza in un solo punto; il prezzo è che chiunque sia membro può modificare
  e cancellare anche ciò che non ha aggiunto.
- **Provider email.** Poiché non esiste nessun canale email, l'app può fare a meno di reset password,
  magic link e inviti spediti per posta; il prezzo è che serve un account Google e che l'invito
  viaggia come link che chi invita consegna a mano.
- **Traduzione dei contenuti.** Poiché la ricerca attraversa le lingue con gli embedding, le ricette
  restano nella lingua in cui sono scritte e non c'è nessuna pipeline di traduzione; il prezzo è che
  si cerca in italiano ma si cucina leggendo l'inglese.
- **Vector database dedicato.** Poiché dati e vettori stanno nello stesso Postgres, non c'è un
  secondo datastore da tenere in sincrono né un secondo conto da pagare, e filtro esatto e similarità
  stanno in una query sola; il prezzo è che il tetto di scala è quello di pgvector su un'istanza free
  tier, e superarlo vorrebbe dire cambiare infrastruttura.

## Ordering criteria

1. **Prima si consegna, poi si impara.** Il repository con la CI e lo scheletro deployato vengono
   prima di qualunque promessa, e sono due righe distinte: una CI verde non dice niente
   sull'argomento hosting, e aprire account è lavoro umano con un modo di fallire diverso da un
   deploy che non si alza.
2. **Il differenziatore prima di tutto il resto.** La ricerca semantica cross-lingua è l'unica cosa
   che separa questo prodotto da Mealie: se non regge, il progetto è una riscrittura. Si misura su un
   corpus reale appena l'infrastruttura esiste, prima che quattro promesse ci si appoggino sopra, e
   poi si consegna come prodotto. Questo criterio cede una volta sola, a favore del criterio 3: il
   ricettario a mano viene prima della ricerca, perché senza righe da cercare la ricerca non è
   consegnabile.
3. **Le convenzioni nascono nella prima riga che ne ha bisogno.** Nessuna riga di sole convenzioni:
   la forma di `Recipe`, il form condiviso fra creazione e modifica, il seam del ricettario corrente
   e le convenzioni di test nascono dentro la prima riga che li usa davvero.
4. **L'incertezza costosa prima della frequenza, e la frequenza prima del resto.** L'estrazione da
   link è insieme il rischio tecnico maggiore (hit-rate del JSON-LD, qualità dell'LLM, latenza
   sincrona) e il modo più frequente di aggiungere: viene subito dopo il differenziatore.
   L'autenticazione, che è lavoro senza incertezza, cede il posto — vedi il criterio 6.
5. **Il recupero richiesto batte l'ampiezza.** Le fonti dichiarano il copia-incolla la via d'uscita
   di quando il link non si legge: chiude il percorso che la riga precedente apre, quindi passa
   davanti all'apertura di un'altra promessa.
6. **Ampiezza prima di profondità, con un rinvio dichiarato.** Una riga sottile per ogni promessa
   prima di una seconda riga sulla stessa promessa. L'identità è rinviata oltre la seconda riga che
   consegna comportamento, e questa è la giustificazione: le due incertezze vere — recupero
   cross-lingua ed estrazione — si validano entrambe su un unico ricettario configurato, e nessuna
   delle loro verifiche cambia quando lo scope passa da configurato ad autenticato. Il seam che rende
   il rinvio non distruttivo è consegnato da `S3`, la prima riga che persiste dati; le righe che lo
   precedono nominano come pubblico chi costruisce e prova l'app, mai un utente che non può esistere.
7. **Chi apre un adapter condiviso viene dopo chi lo alimenta.** Le foto aprono l'object storage e lo
   posseggono da sole: stanno dopo l'inserimento a mano e dopo l'import da link, che sono le due
   strade che ci scrivono dentro. È l'altra deroga all'ampiezza, e vale solo per questo.
8. **La release chiude.** L'ultima riga mette il rilascio coerente in mano a famiglia e amici, con la
   sola prontezza operativa che le fonti chiedono e niente altro.

## Assumptions

- `S1` — Le fonti nominano «Neon o Supabase» senza sceglierne uno. La mappa legge **Neon**, perché
  `tech-choices.md` descrive la connessione Drizzle come TCP verso Neon. Reversibile: entrambi
  offrono pgvector, e lo scheletro è la riga che lo confuterebbe.
- `S1` — Le fonti nominano il driver come «postgres.js / node-postgres» senza sceglierne uno. La
  mappa ne prende uno e lascia che lo scheletro lo confuti: modo di connessione, pooling e
  interazione con il cold start sono esattamente ciò che quella riga misura.
- `S1` — Fly gira con `suspend` + scale-to-zero, come raccomandano le fonti. La macchina sempre calda
  è un flag reversibile in `fly.toml` e resta una candidata.
- `—` — `goal.md` dice «tutto entro free tier, target ~$0/mese»; `arch-choices.md` dice che Fly non
  ha più un free tier vero. La mappa legge il target come **centesimi al mese**, non come zero: il
  vincolo resta mordente, ma nessuna riga è costretta a fingere che l'hosting sia gratis.
- `S4` — `goal.md` dice che LLM ed embedding si usano «solo in fase di add, mai a runtime sulle query
  di ricerca», mentre `concepts.md` calcola `embedding(query)` al momento della ricerca. La mappa
  legge il vincolo come **di costo e non di chiamata**: la query si embedda a runtime con una sola
  chiamata da frazioni di cent, e niente altro sul percorso di ricerca chiama un modello.
- `S5` — Il modello di estrazione è nominato per classe («cheap, Haiku-class») e non scelto. La mappa
  lo legge come **qualunque modello economico con structured output**, perché la riga valida l'uscita
  contro `Schema` e non contro il modello: cambiarlo è configurazione, non forma.
- `identità`, `condivisione` — Le fonti trattano la condivisione come un blocco unico. La mappa la
  legge come **due promesse separate**: entrare ed essere proprietario è valore completo e
  cancellabile da solo — un ricettario personale privato è già un prodotto — mentre invitare è ciò
  che si aggiunge sopra. Se l'autore le considera una cosa sola, le due righe si fondono e l'ordine
  non cambia.
- `S3` — Le fonti descrivono il ricettario corrente ma non dicono come si sceglie prima che esista il
  login. La mappa assume che le righe precedenti all'identità girino su **un unico ricettario
  configurato**, risolto da un solo punto nominato, e che non vadano riscritte quando lo scope
  autenticato lo sostituisce lì.

## Open questions

- `ricerca` — Se lo spike misura che nessun modello multilingue entro budget recupera cross-lingua a
  un livello che una persona chiamerebbe funzionante, cade il differenziatore e con esso la ragione
  dichiarata per non usare Mealie. Si ripiega su una ricerca ibrida keyword + semantica — oggi
  candidata — accettando di somigliare alle alternative, o si cambia obiettivo? La risposta ridisegna
  una promessa intera e non è della mappa.
- `import` — Le fonti chiedono un'estrazione **sincrona** con progress sui passi reali, ma non dicono
  oltre quale attesa smette di essere accettabile; il fallback LLM sommato al cold start di Fly può
  arrivare a decine di secondi. Se il tetto è basso, l'aggiunta diventa asincrona e le due righe
  dell'import si ridisegnano.

## Cross-functional concerns

- **Authorization.** Ogni lettura e scrittura di ricette e foto passa da un unico risolutore nominato
  del ricettario corrente, e nessuna query tocca le ricette senza il filtro su quel ricettario. Prima
  dell'identità il risolutore restituisce un ricettario configurato; dopo lo risolve dalla membership
  dell'utente autenticato — stesso punto, sostituzione unica. Verificato la prima volta dalla riga
  che persiste i primi dati, e di nuovo dalle due righe che attraversano il confine di identità.
- **Validation and errors.** Gli errori attesi sono `Data.TaggedError`, gestiti con `catchTag` solo
  dove si recuperano o si traducono in uscita di boundary. Ogni dato che arriva da fuori — HTML,
  JSON-LD, uscita dell'LLM, risposte delle API — si decodifica con `Schema` e non si castra mai. Un
  fallimento dice quale passo è fallito, mai «qualcosa è andato storto».
- **Operability.** L'estrazione è sincrona e ha un timeout per passo; il progress mostra il passo
  realmente in corso e non avanza mai a tempo. Log strutturati con un identificativo di richiesta, e
  il costo di ogni chiamata a modello loggato in fase di add. Il cold start dopo scale-to-zero è
  misurato dallo scheletro e ri-misurato alla release.
- **Accessibility and security.** I campi obbligatori non si marcano con l'asterisco: si marcano
  «(optional)» quelli facoltativi, si usa `required` nativo e lo stato è esposto alle tecnologie
  assistive. I segreti restano lato server e non entrano mai nel bundle client; gli oggetti su object
  storage hanno chiavi non indovinabili e il bucket non è elencabile.
- **Data integrity and recovery.** L'embedding è indice derivato e mai dato canonico: si rigenera a
  ogni modifica, e se la generazione fallisce la ricetta resta salvata e visibile, segnalata come non
  ancora cercabile e recuperabile con una modifica. Una sola copertina per ricetta è invariante,
  anche quando la copertina viene cancellata. Un upload fallito non lascia mai una ricetta mezza
  salvata né un oggetto orfano che nessuno sa di avere.
- **Cost.** Le fonti fanno del costo un vincolo che più righe devono rispettare: chiamate a modelli
  solo in aggiunta e in modifica, indice HNSW su Postgres invece di un vector database dedicato, Fly
  con `suspend` e scale-to-zero, object storage senza egress. Nessuna riga introduce un costo fisso
  mensile senza dichiararlo nella propria verifica.
