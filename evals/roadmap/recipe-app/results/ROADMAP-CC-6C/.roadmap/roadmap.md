# Roadmap — Recipe App

**Goal:** Un ricettario condiviso tra famiglia e amici in cui aggiungere una ricetta costa quasi
nulla — incolli un link, o incolli il testo, o la scrivi a mano — e in cui la si ritrova con una
ricerca semantica che funziona anche fra lingue diverse, tenendo il conto a centesimi al mese.

**Sources:** `sources/goal.md`, `sources/concepts.md`, `sources/arch-choices.md`,
`sources/tech-choices.md`.

**Current state:** Niente è stato consegnato. È il primo disegno: non esiste ancora un repository,
e `archive/` è vuoto.

## Themes

| Theme | Promise | First validator |
|---|---|---|
| `aggiunta-ricette` | Incolli il link di una ricetta e la ritrovi salvata nel ricettario, senza confermare niente; quello che l'estrazione ha sbagliato lo correggi dopo. | `S3` |
| `ricerca-semantica` | Cerchi a parole tue e trovi le ricette del ricettario corrente, anche quando sono scritte in un'altra lingua. | `S5` |
| `identita` | Entri con il tuo account Google e vedi solo i ricettari di cui fai parte. | `S6` |
| `condivisione` | Mandi un link a chi vuoi e da quel momento legge ed edita le stesse ricette, alla pari con te. | `S7` |
| `foto` | Ogni ricetta porta le sue foto, con una copertina che scegli tu. | `S8` |

**Theme boundaries**

- `aggiunta-ricette` / `ricerca-semantica` — **split.** La ricerca si rinvia intera e l'aggiunta
  resta verificabile dall'elenco e dal dettaglio.
- `aggiunta-ricette` / `foto` — **split.** L'import salva la ricetta anche quando la foto non
  arriva, e la galleria con la copertina è valore che si programma da sé.
- `ricerca-semantica` / `identita` — **split.** La qualità cross-lingua si misura su un ricettario
  configurato, senza sapere chi è l'utente.
- `identita` / `condivisione` — **split.** Login e scope per ricettario reggono l'app monoutente e
  si validano senza che esista un invito.
- `condivisione` / `foto` — **split.** Nessuna delle due tocca l'invariante dell'altra: le foto si
  cancellano intere senza toccare l'evidenza dell'invito.

## NOW

| Id | Title | Theme | Kind | Size | Readiness | Executor | Depends on |
|---|---|---|---|---|---|---|---|
| `S0` | [Repository, CI e account dei servizi](slices/S0-repository-ci-account.md) | `—` | `enabler` | `small` | `ready` | `mixed` | — |
| `S1` | [Scheletro deployato su Fly con Postgres](slices/S1-scheletro-deployato.md) | `—` | `release` | `medium` | `ready` | `mixed` | — |
| `S2` | [Quale embedder regge la ricerca cross-lingua](slices/S2-embedder-cross-lingua.md) | `goal` | `spike` | `small` | `ready` | `mixed` | — |
| `S3` | [Aggiungi una ricetta da link e correggila dopo](slices/S3-aggiungi-da-link.md) | `aggiunta-ricette` | `product` | `large` | `ready` | `agent` | `S2` |
| `S4` | [Fallback LLM quando la pagina non ha JSON-LD](slices/S4-fallback-llm.md) | `aggiunta-ricette` | `product` | `medium` | `ready` | `agent` | `S3` |
| `S5` | [Ricerca semantica cross-lingua nel ricettario](slices/S5-ricerca-semantica.md) | `ricerca-semantica` | `product` | `medium` | `ready` | `agent` | `S3` |
| `S6` | [Accedi con Google e vedi i tuoi ricettari](slices/S6-accedi-con-google.md) | `identita` | `product` | `large` | `ready` | `mixed` | `S3` |
| `S7` | [Invita nel ricettario con un link](slices/S7-invito-ricettario.md) | `condivisione` | `product` | `medium` | `ready` | `agent` | `S6` |
| `S8` | [Foto della ricetta con copertina](slices/S8-foto-ricetta.md) | `foto` | `product` | `medium` | `ready` | `mixed` | `S3` |
| `S9` | [Aggiungi una ricetta incollando il testo](slices/S9-copia-incolla.md) | `aggiunta-ricette` | `product` | `small` | `ready` | `agent` | `S4` |
| `S10` | [Scrivi una ricetta a mano](slices/S10-inserimento-manuale.md) | `aggiunta-ricette` | `product` | `small` | `ready` | `agent` | `S3` |
| `S11` | [Il ricettario in mano a famiglia e amici](slices/S11-rilascio.md) | `—` | `release` | `medium` | `needs-decision` | `mixed` | `S7` |

## LATER

- Filtri di ricerca strutturati per tag e tempo, e ricerca ibrida semantica + full-text: i campi si
  popolano da subito, quindi si abilitano senza migrazione.
- Ricerca che attraversa tutti i ricettari di cui l'utente è membro.
- Ricettari pubblici tematici, come `visibility = public` sul ricettario esistente.
- Un concetto di gruppo sopra i ricettari, se ri-invitare le stesse persone in ognuno diventasse
  fastidioso.
- Ruoli dentro il ricettario, se la parità fra membri si rivelasse insufficiente.
- Revoca di una membership e rimozione di un membro dal ricettario.
- Cancellare una ricetta o un ricettario: nessuna fonte lo chiede, oggi la correzione è l'edit.
- Import da file di altre app (Paprika, Mealie) e da PDF; OCR da foto di un libro.
- Passkeys come secondo modo di entrare, quando il recupero account sarà risolto.
- Ridimensionamento e ottimizzazione delle immagini, e raccolta delle foto orfane sullo storage.
- IaC versionata al posto di `fly.toml` + CLI, se l'infrastruttura crescesse.

## OUT-OF-SCOPE

- **Ingredienti strutturati in quantità e unità.** Poiché resta irrisolto, l'implementazione può
  salvare ingredienti e preparazione come testo libero, senza parser né modello di ingrediente e
  senza form che chieda righe strutturate: il prezzo è che lista della spesa e scaling porzioni
  restano preclusi finché il modello non cambia.
- **Deduplica delle ricette.** Poiché due membri possono linkare la stessa pagina nello stesso
  ricettario, l'implementazione può salvare senza confronto, senza chiave naturale e senza merge:
  il prezzo sono duplicati visibili in elenco e in ricerca.
- **Invio di email.** Poiché nessun messaggio esce dall'app, l'implementazione può fare a meno di
  provider SMTP, template, code di invio e flusso di reset password: il prezzo è che entrare
  richiede un account Google e che l'invito viaggia solo come link che il creator gira a mano.
- **Review obbligatoria prima del salvataggio.** Poiché l'estratto si salva sempre,
  l'implementazione può fare a meno di uno stato bozza, di una coda di conferme e di due percorsi
  di lettura: il prezzo è che ricette imperfette entrano subito in elenco e in ricerca finché
  qualcuno non le corregge.
- **Un secondo datastore.** Poiché dati e vettori stanno nello stesso Postgres, l'implementazione
  può fare a meno di sincronizzazione, di transazioni distribuite e di un indice da ricostruire: il
  prezzo è che la ricerca resta vincolata a quello che pgvector sa fare.
- **Permessi granulari dentro un ricettario.** Poiché ogni membro è pari, l'implementazione può
  fare a meno di un campo ruolo, di una matrice di permessi e di controlli oltre la membership: il
  prezzo è che chiunque entri dal link può anche modificare e cancellare quello che hanno scritto
  gli altri.

## Assumptions

- `goal` — "~$0/mese" è letto come pochi centesimi al mese, non come free tier: `goal.md` mette
  Fly.io fra i servizi entro free tier, `arch-choices.md` dice che Fly un free tier vero non ce
  l'ha più. Presa la seconda, che è la più recente e la più specifica: si parte con `suspend` +
  scale-to-zero e il cold start del primo utente è accettato; la macchina sempre-calda a ~$3/mese
  è il ripiego, un flag reversibile.
- `S1` — Il provider Postgres è Neon. `arch-choices.md` lascia aperto "Neon o Supabase";
  `tech-choices.md` nomina Neon quando descrive la connessione TCP col driver standard, ed è
  l'unica delle due a scegliere. Presa Neon con `postgres.js`: delivery la smentisce se il free
  tier o il numero di connessioni sotto scale-to-zero non reggono.
- `S3`, `aggiunta-ricette` — I quattro passi di progress dichiarati in `goal.md`
  (`Scarico pagina → Leggo ricetta → Trovo ingredienti → Salvo foto`) non corrispondono alla
  pipeline di `concepts.md`, dove una sola estrazione produce titolo, ingredienti e preparazione
  insieme, e le foto arrivano dopo il salvataggio. Presa la pipeline: la progress mostra i passi
  che accadono davvero, "Trovo ingredienti" sparisce dentro "Leggo la ricetta" e "Salvo foto"
  compare quando `S8` lo aggiunge.
- `S3`, `S6`, `identita` — Le righe prima di `S6` girano su un ricettario configurato e su un
  proprietario implicito. Il resolver `currentCookbook` è il solo punto che cambia quando arriva
  l'identità, e nessuna di quelle righe va riscritta: `S6` lo smentisce se sostituire lo scope
  configurato con quello autenticato tocca più di quel punto.
- `S4`, `aggiunta-ricette` — Il modello di estrazione è `claude-haiku-4-5` con output strutturato.
  `arch-choices.md` dice "modello cheap, Haiku-class" senza sceglierne uno: presa la classe alla
  lettera. La misura di qualità e di costo per ricetta in `S4` la smentisce.
- `S5`, `ricerca-semantica` — La query viene embeddata a runtime. `goal.md` e `arch-choices.md`
  dicono che gli embedding servono "solo in fase di add, mai a runtime sulle query", ma
  `concepts.md` calcola `similarity(Recipe.embedding, embedding(query))` e il riepilogo costi dello
  stesso `arch-choices.md` dice che "le query sono irrilevanti", il che concede che esistano. Letto
  come divieto di chiamate LLM e di ri-embedding del corpus a runtime, non della singola chiamata
  da pochi token sulla query. `S5` la smentisce se quella chiamata pesa sulla latenza percepita.

## Open questions

- `goal`, `ricerca-semantica`, `S2` — Qual è la soglia di recall cross-lingua sotto la quale il
  differenziatore non esiste? `S2` produce i numeri, ma il numero accettabile lo possiede l'autore,
  e una risposta negativa non sposta una riga: cancella il differenziatore e la mappa va ridisegnata
  attorno a un ricettario condiviso con ricerca ordinaria.
- `goal`, `aggiunta-ricette` — Nessuna fonte nomina la cancellazione di una ricetta o di un
  ricettario. L'MVP esce senza? Se no manca una riga in `NOW`, e oggi il candidato in `LATER` è
  l'unico posto in cui quel comportamento esiste.

## Cross-functional concerns

- **Authorization.** Ogni lettura e ogni scrittura di ricette e foto passa da un solo resolver,
  `currentCookbook`: configurato su un ricettario seed da `S3`, autenticato da `S6`. Nessuna riga
  interroga le tabelle fuori da quello scope, e nessuna introduce un controllo più fine della
  membership.
- **Validation and errors.** L'estrazione è una cascata di passi nominati, e ogni fallimento si
  riporta col passo che l'ha causato — pagina non scaricata, ricetta non trovata nella pagina,
  output del modello non conforme — mai come errore generico e mai come ricetta parziale salvata.
- **Operability.** Lo scale-to-zero con `suspend` è la configurazione di default, quindi nessuna
  riga può introdurre stato in-process, volumi o lavoro in background che debba sopravvivere alla
  richiesta: l'estrazione resta sincrona e il container resta stateless.
- **Data integrity and recovery.** L'`embedding` è indice derivato, non dato canonico: ogni riga
  che scrive `name`, `ingredients`, `steps`, `tags` o `prepTime` lo rigenera nella stessa
  transazione. Una ricetta senza embedding è un bug, non uno stato del sistema.
- **Cost.** Nessuna riga introduce un servizio a canone, e LLM ed embedding si chiamano solo in
  aggiunta, in edit e sulla query di ricerca. Ogni riga che chiama un servizio a pagamento misura
  nella sua `Verification` quanto costa per ricetta o per richiesta.
