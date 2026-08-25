# Roadmap — Recipe App

**Goal:** Un ricettario condiviso tra famiglia e amici in cui aggiungere una ricetta da link costa un
incollaggio e nient'altro, e in cui si ritrova quello che si cerca a senso e in qualunque lingua sia
scritta la ricetta — tenuto in piedi a pochi centesimi al mese.

**Sources:** `sources/goal.md`, `sources/concepts.md`, `sources/arch-choices.md`,
`sources/tech-choices.md`.

**Current state:** Nulla è stato consegnato. Il progetto è greenfield: non c'è repository, non ci
sono account aperti, non c'è nulla in produzione. Le decisioni di stack e infrastruttura sono prese
e documentate nelle fonti; questa mappa è il primo disegno del percorso che le mette in opera.

## Themes

| Theme | Promise | First validator |
|---|---|---|
| `ricette` | Scrivi una ricetta a mano e la correggi quando vuoi: titolo, ingredienti e preparazione come testo libero, senza campi obbligatori oltre a quelli. | `S3` |
| `import` | Incolli il link di un blog e la ricetta è nel ricettario senza compilare nulla; quando il link non si lascia leggere, incolli il testo e finisce uguale. | `S4` |
| `ricerca` | Cerchi "cena leggera" o "pomodoro" e trovi la ricetta anche se è scritta in inglese, senza aver mai messo un tag. | `S6` |
| `foto` | Ogni ricetta ha le sue foto, con una copertina scelta da te, e quelle prese da un link non si rompono nel tempo. | `S8` |
| `accesso` | Entri con Google, senza password da inventare né da recuperare, e ritrovi il tuo ricettario. | `S7` |
| `condivisione` | Mandi un link a chi vuoi e da quel momento legge ed edita il tuo stesso ricettario, alla pari con te. | `S9` |

## NOW

| Id | Title | Theme | Kind | Size | Readiness | Executor | Depends on |
|---|---|---|---|---|---|---|---|
| `S0` | [Repository e pipeline verde](slices/S0-repository-e-pipeline-verde.md) | — | `enabler` | `small` | `ready` | `mixed` | — |
| `S1` | [Scheletro deployato su Fly con Postgres e pgvector](slices/S1-scheletro-deployato.md) | — | `release` | `medium` | `needs-decision` | `mixed` | `S0` |
| `S2` | [Quanto regge la ricerca cross-lingua](slices/S2-ricerca-cross-lingua.md) | `ricerca` | `spike` | `small` | `ready` | `mixed` | `S1` |
| `S3` | [Ricetta a mano: elenco, scrittura, correzione](slices/S3-ricetta-a-mano.md) | `ricette` | `product` | `medium` | `ready` | `agent` | `S1` |
| `S4` | [Aggiunta da link con JSON-LD e avanzamento reale](slices/S4-aggiunta-da-link.md) | `import` | `product` | `medium` | `ready` | `agent` | `S3` |
| `S5` | [Estrazione LLM: link illeggibili e testo incollato](slices/S5-estrazione-llm.md) | `import` | `product` | `medium` | `needs-decision` | `agent` | `S4` |
| `S6` | [Ricerca semantica nel ricettario corrente](slices/S6-ricerca-semantica.md) | `ricerca` | `product` | `medium` | `needs-decision` | `agent` | `S2`, `S5` |
| `S7` | [Accesso con Google e ricettario dell'utente](slices/S7-accesso-con-google.md) | `accesso` | `product` | `medium` | `ready` | `mixed` | `S6` |
| `S8` | [Foto della ricetta con copertina](slices/S8-foto-della-ricetta.md) | `foto` | `product` | `medium` | `ready` | `agent` | `S5` |
| `S9` | [Invito al ricettario e membri alla pari](slices/S9-invito-al-ricettario.md) | `condivisione` | `product` | `medium` | `ready` | `agent` | `S7` |
| `S10` | [Più ricettari e ricettario corrente](slices/S10-piu-ricettari.md) | `condivisione` | `product` | `small` | `ready` | `agent` | `S9` |
| `S11` | [Rilascio alla famiglia](slices/S11-rilascio-alla-famiglia.md) | — | `release` | `small` | `ready` | `mixed` | `S8`, `S10` |

## LATER

- Filtri strutturati di ricerca su tag e tempo, sui campi che l'MVP popola già in automatico.
- Ricerca ibrida: semantica più full-text, per quando si cerca un titolo esatto.
- Ricerca su tutti i ricettari a cui si appartiene, non solo su quello corrente.
- Ricettari pubblici tematici (vegano, giapponese) come `Cookbook` con `visibility=public`.
- Un concetto di gruppo sopra i ricettari, se ri-invitare le stesse persone in ognuno diventasse
  fastidioso.
- Import da file esportati da altre app (Paprika, Mealie, Tandoor).
- Macchina Fly sempre calda (`min_machines_running=1`, ~$3/mese), se il risveglio dopo l'inattività
  desse fastidio all'uso reale.
- Segnalazione dei duplicati in fase di aggiunta, senza impedirli.
- Passkeys accanto a Google, quando il supporto di Auth.js sarà maturo.
- OCR di una foto di pagina di libro come quarto ingresso dell'estrazione.

## OUT-OF-SCOPE

- **Ingredienti strutturati in quantità e unità.** Poiché gli ingredienti restano testo libero,
  l'implementazione può salvarli come una stringa e non avere parser, unità, conversioni né
  vocabolario di ingredienti; il prezzo è che lista della spesa e scaling delle porzioni restano
  impossibili finché qualcuno non riparsa tutte le ricette già salvate.
- **Ruoli e permessi granulari.** Poiché dentro un ricettario tutti sono pari, ogni autorizzazione si
  decide con una sola domanda — *esiste una `Membership` fra questo utente e questo ricettario?* — e
  non serve né un campo `role` né una matrice di permessi; il prezzo è che non si può invitare
  qualcuno in sola lettura e che chiunque entri può cancellare tutto.
- **Deduplicazione delle ricette.** Poiché i duplicati sono consentiti, l'aggiunta non deve
  confrontare, normalizzare né chiedere conferma prima di salvare, e i due percorsi di estrazione
  restano indipendenti; il prezzo è un ricettario che può contenere la stessa ricetta due volte con
  titoli diversi.
- **Review obbligatoria prima del salvataggio.** Poiché non c'è, il flusso di aggiunta non ha stati
  intermedi, bozze da riprendere né ricette a metà da ripulire; il prezzo è che un'estrazione
  sbagliata entra nel ricettario e nell'indice semantico finché qualcuno non la corregge.
- **Qualunque provider di posta.** Poiché non ce n'è uno, niente password da resettare, niente
  conferma dell'indirizzo, niente notifiche e niente costo ricorrente; il prezzo è che l'accesso
  dipende interamente da Google e chi non ha un account Google resta fuori.
- **Vector DB dedicato.** Poiché i vettori stanno nello stesso Postgres dei dati, filtro esatto e
  similarità si fanno in una query e in una transazione sola, e non c'è una seconda infrastruttura da
  tenere in sincrono; il prezzo è che oltre l'ordine di grandezza previsto (~10k ricette) la ricerca
  andrà rimisurata prima di crescere ancora.

## Ordering criteria

1. **Prima si consegna, poi si impara.** Finché non esiste un percorso deployato, nessuna misura vale
   niente: S0 e S1 precedono qualunque promessa, e sono due righe perché una CI verde non dice nulla
   sull'ipotesi di hosting e aprire account non fallisce come fallisce un deploy che non risale.
2. **Il differenziatore e il rischio esistenziale, appena c'è dove misurarli.** Senza ricerca semantica
   cross-lingua il prodotto è una riscrittura di Mealie: S2 la misura subito dopo lo scheletro, sul
   corpus più economico che la renda misurabile — ricette italiane e inglesi caricate direttamente nel
   database — invece di aspettare che l'import le produca. Perde solo contro il criterio 1.
3. **Il recupero richiesto batte l'ampiezza.** S5 è il fallback che le fonti dichiarano per il
   fallimento di S4 (paywall, siti JS-heavy, JSON-LD assente): chiude quel percorso prima che si apra
   un altro tema. È l'unica ragione per cui `import` prende due righe di fila, ed è anche la ragione
   per cui S3 precede S4: la correzione dopo l'estrazione è il recupero dichiarato dell'aggiunta
   automatica, e va consegnata prima della prima riga che può produrre una ricetta da correggere.
4. **Le convenzioni nascono nella prima riga che ne ha bisogno.** Non c'è nessuna riga di sola
   impalcatura: il modello di dominio nasce in S3, lo schema di estrazione in S4, l'adapter LLM in S5,
   quello degli embedding in S6, quello di R2 in S8, ognuno dentro la riga che per prima lo usa
   davvero.
5. **L'identità si rinvia solo finché l'evidenza lo richiede.** S3–S6 hanno per pubblico l'autore e chi
   prova l'app sull'ambiente non pubblico su Fly, e girano su uno scope configurato: l'evidenza che
   giustifica il rinvio è la qualità della ricerca cross-lingua, che l'autenticazione non rende né più
   né meno vera. Appena S6 la produce, S7 arriva prima di qualunque altra riga rivolta a utenti veri.
   Perde contro i criteri 2 e 3, e vince su tutto il resto.
6. **Chi apre una pipeline condivisa viene dopo tutti quelli che la alimentano, e la possiede da
   solo.** S6 possiede la generazione degli embedding per tutti e tre i percorsi di aggiunta (S3, S4,
   S5); S8 possiede l'object storage sia per l'upload manuale sia per il download della foto da un
   link. Nessuna delle due riesce prima dei propri alimentatori senza lasciare un contratto
   provvisorio da riaprire.
7. **Ampiezza prima di profondità.** Dopo S6 arriva una riga sottile per ciascun tema rimasto —
   `accesso` in S7, `foto` in S8, `condivisione` in S9 — prima di una seconda riga sullo stesso tema
   (S10). Le uniche deviazioni sono quelle concesse ai criteri 3 e 5.
8. **Il rilascio chiude.** S11 mette il prodotto coerente in mano alla famiglia e non aggiunge
   capacità: quello che non è entrato entro S10 diventa un candidato, non un allargamento di S11.

## Assumptions

- `goal`, `S1`, `S11` — Il target di costo è **pochi centesimi al mese**, non zero. `goal.md` dice
  "tutto entro free tier → ~$0/mese" e cita Fly fra i free tier; `arch-choices.md` dice esplicitamente
  che Fly non ha più un free tier vero. Prendiamo la lettura di `arch-choices.md`, che è la più
  specifica e la più recente: DB, storage ed embedding stanno a $0, l'hosting costa centesimi con
  `suspend` più scale-to-zero, e la macchina sempre calda a ~$3/mese resta un flag reversibile in
  `fly.toml`, in `LATER`.
- `accesso`, `condivisione`, `S7`, `S10` — Il primo ricettario di un utente viene **creato
  automaticamente al primo accesso** e il "ricettario corrente" è l'ultimo scelto, ricordato fra le
  sessioni. Le fonti parlano di "elenco delle ricette del ricettario corrente" e di appartenenza a più
  ricettari senza mai dire da dove esce il primo né come si cambia; questa lettura evita un passo di
  onboarding obbligatorio, coerente con "nessun passo obbligatorio prima del salvataggio".
- `condivisione`, `S9` — **L'invito lo genera il creator.** `goal.md` dice insieme "ogni ricettario ha
  un creator che invita gli altri" e "dentro un ricettario tutti i membri sono pari"; leggiamo la
  parità come riferita a ricette e foto — leggere ed editare tutto — e non alla generazione degli
  inviti, che resta l'unica cosa che `Cookbook.creatorId` distingue.
- `ricette`, `import` — `ricette` e `import` sono **due temi** e non uno: l'aggiunta automatica può
  essere cancellata o rinviata per intero lasciando intatta l'evidenza della scrittura a mano, e la
  scrittura a mano è per di più il percorso di correzione da cui l'import dipende. Un form condiviso
  non è una ragione per fonderli.
- `accesso`, `condivisione` — `accesso` e `condivisione` sono **due temi** e non uno: si può stare a
  lungo su un ricettario personale con l'accesso Google e nessun invito, e l'evidenza dell'accesso
  resta valida. Il contrario non vale, ma basta una direzione perché siano due promesse schedulabili
  separatamente.
- `condivisione`, `S10` — I **più ricettari sono dentro `condivisione`**, non un tema a sé. Condividono
  con l'invito l'unico invariante che conta — ogni lettura e scrittura passa dal ricettario corrente e
  dalla `Membership` — e per una famiglia che ne ha uno solo la possibilità di crearne un secondo non
  produce feedback utile finché non c'è nessun altro dentro.
- `ricerca`, `S2`, `S6` — Gli embedding si generano **solo in aggiunta e in modifica**, mai sulla query
  di ricerca. È il vincolo di costo di `arch-choices.md`; una query che chiamasse l'API rimetterebbe in
  discussione l'intera voce di costo e va trattata come una regressione, non come un dettaglio.

## Open questions

- `goal`, `accesso`, `S7`, `S11` — **A chi si apre l'accesso quando l'app è su un URL pubblico?**
  Nessuna fonte lo dice. Con Google OAuth aperto, chiunque abbia un account Google può entrare,
  crearsi un ricettario e spendere le nostre chiamate LLM ed embedding; con una allow-list di indirizzi
  serve una riga che la gestisca, e la mappa oggi non ce l'ha. La risposta decide se S7 e S11 restano
  come sono o se nasce una riga in più prima del rilascio.
- `goal`, `import`, `ricerca` — **Quante ricette entrano davvero e con che ritmo?** Le fonti danno il
  tetto (≤10k totali, centinaia per ricettario) ma non la frequenza reale di aggiunta. Se il ritmo
  fosse di poche ricette al mese, la barra di avanzamento sui passi reali di S4 e l'ottimizzazione
  dell'indice HNSW di S6 sono lavoro speso su un percorso che si attraversa raramente, e l'ordine fra
  `import` e `foto` andrebbe riletto.

## Cross-functional concerns

- **Authorization.** Ogni lettura e scrittura di `Recipe`, `Photo` e `Invitation` passa da un unico
  risolutore di scope — il ricettario corrente — che è l'unica fonte di `cookbookId`: nessuna query di
  dominio lo prende da input dell'utente. Fino a S6 il risolutore legge un id dalla configurazione
  dell'ambiente; S7 lo sostituisce con quello derivato da sessione e `Membership`, in quel solo punto.
  Una risorsa fuori dallo scope corrente non esiste per chi la chiede: si risponde come per una
  risorsa inesistente, senza rivelarne l'esistenza.
- **Validation and errors.** Tutto ciò che arriva dall'esterno — HTML scaricato, output dell'LLM, body
  delle API, payload dei form — si decodifica con `Schema` e non si castra mai. Gli errori attesi sono
  `Data.TaggedError` e restano tipizzati fino al boundary, dove `catchTag` li traduce in un messaggio
  che dice quale passo è fallito e cosa può fare l'utente. Un output LLM che non valida è un errore
  nominato, non una ricetta salvata a metà.
- **Operability.** Ogni chiamata esterna — fetch della pagina, LLM, embedding, object storage — ha un
  timeout esplicito, un numero massimo di tentativi e un errore distinguibile dagli altri. La barra di
  avanzamento dell'aggiunta riporta i passi realmente eseguiti e nomina quello fallito; non ci sono
  passi finti. Un'aggiunta fallita non lascia righe orfane nel database né file orfani nello storage.
  Il primo accesso dopo un periodo di inattività paga il risveglio della macchina Fly: è atteso, e il
  tempo va misurato in S1 e riletto in S11.
- **Accessibility and security.** I campi obbligatori non si marcano con l'asterisco: si marcano gli
  opzionali con "optional" e si usa l'attributo `required` nativo. Stati di caricamento e avanzamento
  sono annunciati alle tecnologie assistive, non solo disegnati. Chiavi API, credenziali OAuth e
  credenziali dell'object storage stanno nei secret di Fly e nell'ambiente locale, mai nel repository
  né nel bundle client. Il token di invito è generato con un generatore crittografico e non è
  indovinabile.
- **Data integrity and recovery.** `embedding`, `tags` e `prepTime` sono derivati e mai canonici: la
  loro assenza non impedisce di salvare, leggere o correggere una ricetta, e la loro rigenerazione
  fallita lascia la ricetta valida e ritentabile, non persa. Le foto vivono sull'object storage e il
  database ne tiene solo l'URL: un URL rotto degrada la ricetta, non la invalida. Ogni migration è
  applicata dal runner nella pipeline, mai a mano su un database vivo.
- **Cost.** LLM ed embedding si chiamano solo in aggiunta e in modifica, una tantum per ricetta, e mai
  su una query di ricerca o sul rendering di una pagina. Ogni riga che introduce una chiamata a
  pagamento dice nella propria verifica quante volte viene chiamata e quando non lo è.
