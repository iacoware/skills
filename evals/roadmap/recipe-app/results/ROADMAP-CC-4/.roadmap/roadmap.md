# Roadmap — Recipe App

**Goal:** Un ricettario condiviso tra famiglia e amici dove aggiungere una ricetta costa
quasi nulla — un link, un incolla, o due campi a mano — e dove la si ritrova cercando a
parole proprie, anche se è scritta in un'altra lingua, il tutto a un costo di gestione di
pochi centesimi al mese.

**Sources:** `sources/goal.md`, `sources/arch-choices.md`, `sources/tech-choices.md`,
`sources/concepts.md`

**Current state:** Nulla è stato consegnato: repository da aprire, nessun servizio
provisionato, nessuna riga di codice.

## Themes

| Theme | Promise | First validator |
|---|---|---|
| `ricettario` | Scrivo a mano una ricetta che conosco, con le sue foto, e la ritrovo nell'elenco del ricettario. | S3 |
| `import` | Aggiungo una ricetta senza trascriverla: incollo il link, e dove il link non è leggibile incollo il testo della pagina. | `S7` |
| `ricerca` | Cerco a parole mie — "cena leggera", "pomodoro" — e trovo la ricetta anche se è scritta in un'altra lingua. | `S8` |
| `accesso` | Entro con il mio account Google e ritrovo le mie ricette, senza password da inventare né da recuperare. | S9 |
| `condivisione` | Invito con un link chi voglio nel mio ricettario, e da lì in poi lo scriviamo in due o in dieci. | `S10` |

- `ricettario` / `import` — **split.** L'inserimento a mano resta utile e verificabile anche
  se l'estrazione automatica non arrivasse mai.
- `import` / `ricerca` — **split.** L'estrazione si misura sulle ricette che produce, la
  ricerca si misura su ricette qualunque sia la loro origine.
- `ricerca` / `accesso` — **split.** Il recall cross-lingua si misura su un ricettario solo,
  senza che esista un utente autenticato.
- `accesso` / `condivisione` — **split.** Entrare con Google e usare da soli un ricettario è
  valore completo; l'invito è una promessa che si può rimandare o cancellare intera.
- `import` / *candidato `import-testo`* — **merge.** Le fonti dichiarano il copia-incolla il
  fallback del link non leggibile, non una via d'ingresso indipendente.

## NOW

| Id | Title | Theme | Kind | Size | Readiness | Executor | Depends on |
|---|---|---|---|---|---|---|---|
| `S0` | [Repository, CI e account](slices/S0-repository-ci-account.md) | `—` | `enabler` | `small` | `ready` | `mixed` | — |
| `S1` | [Scheletro deployato su Fly con Postgres](slices/S1-scheletro-deployato.md) | `—` | `release` | `medium` | `ready` | `mixed` | S0 |
| `S2` | [Quale modello di embedding regge il cross-lingua](slices/S2-spike-embedding-multilingue.md) | `ricerca` | `spike` | `small` | `ready` | `agent` | — |
| `S3` | [Ricetta a mano, elenco e ricettario corrente](slices/S3-ricetta-a-mano.md) | `ricettario` | `product` | `medium` | `ready` | `agent` | S1 |
| `S4` | [Foto multiple e cover su R2](slices/S4-foto-e-cover.md) | `ricettario` | `product` | `medium` | `ready` | `mixed` | S3 |
| `S5` | [Aggiunta da link con JSON-LD e progress reale](slices/S5-import-da-link.md) | `import` | `product` | `large` | `ready` | `agent` | S4 |
| `S6` | [Fallback LLM quando manca il JSON-LD](slices/S6-fallback-llm.md) | `import` | `product` | `medium` | `ready` | `agent` | S5 |
| `S7` | [Aggiunta da testo incollato](slices/S7-aggiunta-da-testo.md) | `import` | `product` | `small` | `ready` | `agent` | S6 |
| `S8` | [Ricerca semantica nel ricettario corrente](slices/S8-ricerca-semantica.md) | `ricerca` | `product` | `medium` | `ready` | `agent` | S2, S3 |
| `S9` | [Accesso con Google](slices/S9-accesso-con-google.md) | `accesso` | `product` | `medium` | `ready` | `mixed` | S3 |
| `S10` | [Ricettari condivisi per invito](slices/S10-ricettari-condivisi.md) | `condivisione` | `product` | `medium` | `ready` | `agent` | S9 |
| `S11` | [Prima release a famiglia e amici](slices/S11-prima-release.md) | `—` | `release` | `small` | `needs-decision` | `mixed` | — |

## LATER

- Filtri di ricerca strutturati per tag e tempo, sui campi che le estrazioni popolano già.
- Ricerca ibrida: semantica più full-text sullo stesso indice.
- Ricerca che attraversa tutti i ricettari di cui si è membri.
- Ricettari pubblici tematici, come `visibility=public` sul ricettario esistente.
- Un concetto di gruppo sopra i ricettari, se ri-invitare per ognuno diventasse fastidioso.
- Macchina Fly sempre calda (~$3/mese) se il cold start dopo il silenzio desse fastidio.
- Ridimensionamento e ottimizzazione delle foto caricate.
- Passkeys come secondo modo di entrare.

## OUT-OF-SCOPE

- **Ingredienti strutturati in quantità e unità.** Perché nessuno li parsa, il salvataggio
  accetta qualunque testo e nessun flusso può bloccarsi su una riga che non capisce; il
  prezzo è che lista della spesa e scaling delle porzioni restano impossibili.
- **Ruoli e permessi granulari.** Perché dentro un ricettario tutti i membri sono pari,
  l'autorizzazione è un unico controllo di appartenenza e non c'è matrice da mantenere; il
  prezzo è che nessuno può essere limitato alla sola lettura.
- **Review obbligatoria dell'estratto.** Perché si salva subito, l'aggiunta non ha bozze,
  stati intermedi né code da riprendere; il prezzo è che ricette imperfette entrano nel
  ricettario e vanno corrette dopo, in modifica.
- **Deduplica delle ricette.** Perché i duplicati sono ammessi, il salvataggio non confronta
  niente con niente; il prezzo è lo stesso link salvato due volte da due membri.
- **Provider email.** Perché non si manda una sola email, non esistono password, reset,
  verifica indirizzo né notifiche; il prezzo è che l'invito viaggia fuori dall'app come link
  copiato e che serve un account Google per entrare.
- **Lavoro asincrono: code, worker, job.** Perché l'estrazione è sincrona dentro la
  richiesta, non c'è infrastruttura da tenere accesa e il container resta stateless con
  scale-to-zero pulito; il prezzo è che l'utente aspetta e che un'estrazione lenta occupa una
  richiesta.
- **Vector database dedicato.** Perché i vettori stanno in Postgres, c'è un solo datastore da
  provisionare, migrare e salvare; il prezzo è che oltre l'ordine di grandezza previsto
  (≤10k ricette) la ricerca andrebbe ripensata.

## Assumptions

- `goal, S1` — Le fonti si contraddicono sul costo: `goal.md` promette free tier e ~$0/mese,
  `arch-choices.md` dice che Fly non ha più un free tier vero. Si prende la lettura di
  `arch-choices.md`: si parte con `suspend` + scale-to-zero, il ~$0 è un'approssimazione di
  "pochi centesimi". Delivery la rifiuta se il costo misurato del primo mese esce dai
  centesimi.
- `ricerca, S8` — `goal.md` dice che LLM ed embedding servono "solo in fase di add, mai a
  runtime sulle query", ma la query di `concepts.md` contiene `embedding(query)`, che è per
  forza a runtime. Si legge il vincolo come "nessuna estrazione a runtime", coerente con
  `arch-choices.md` che dice le query "irrilevanti" per costo. Delivery la rifiuta se costo o
  latenza dell'embedding di query risultano percepibili.
- `S0, S1` — Nessuna fonte sceglie tra Neon e Supabase: si prende Neon, per pgvector sul
  piano gratuito e connessione TCP diretta. Delivery la rifiuta se i limiti di connessione o
  l'indice HNSW non reggono; il cambio resta dietro Drizzle.
- `import, S6` — Nessuna fonte sceglie il modello di estrazione oltre a dirlo "Haiku-class":
  si prende Claude Haiku 4.5 con structured output validato da Schema. Delivery la rifiuta se
  la qualità misurata su pagine reali non produce estratti accettabili senza review.
- `import, S5` — Le fonti chiedono estrazione sincrona con progress sui passi reali senza
  dire come: si assume streaming dal server al client dentro la stessa richiesta di add,
  nessuna coda. Delivery la rifiuta se i timeout di piattaforma o proxy tagliano la richiesta
  prima della fine.
- `goal, S3, S9` — L'identità arriva dopo le righe che validano il differenziatore: fino a
  `S9` tutto gira su un unico proprietario implicito e su un ricettario seed scelto da un
  risolutore configurato, su ambiente non pubblico. Delivery la rifiuta se a `S9` la
  sostituzione dello scope tocca più del risolutore.
- `accesso, S9` — Nessuna fonte descrive il primo accesso: si assume che l'utente ottenga
  automaticamente un ricettario personale, senza passi da compiere. Delivery la rifiuta se
  serve un passo esplicito di creazione perché l'utente non capisce dove si trova.

## Open questions

- `goal` — Nessuna fonte fissa un tetto di spesa per LLM ed embedding né dice cosa succede
  quando lo si supera. Se serve una quota per utente o per ricettario, la mappa guadagna una
  riga e il flusso di aggiunta cambia forma.
- `condivisione, S10` — Nessuna fonte dice se un invito è revocabile o se un membro può
  uscire da un ricettario. La risposta decide se `condivisione` ha una riga in più o una
  licenza in OUT-OF-SCOPE.
- `ricerca, S2, S8` — Se `S2` mostrasse che nessun modello a costo trascurabile regge il
  cross-lingua sulle ricette, cade il differenziatore dichiarato e la mappa va ridisegnata
  attorno a una ricerca ibrida, oggi rimandata.

## Cross-functional concerns

- **Authorization.** Ogni lettura e ogni scrittura di ricette e foto passa da un unico
  risolutore del ricettario corrente: configurato fino a `S9`, derivato da sessione e
  appartenenza da `S9` in poi. Nessun ruolo: essere membro significa leggere e scrivere tutto.
- **Validation and errors.** Errori come `Data.TaggedError`, gestiti con `catchTag` solo ai
  boundary; l'output dell'LLM e ogni risposta esterna sono validati con `Schema`, mai
  castati; ogni fallimento dell'estrazione nomina il passo reale in cui è avvenuto.
- **Operability.** Timeout su fetch pagina, chiamata LLM ed embedding; log strutturato per
  passo di estrazione con costo della chiamata; scale-to-zero con `suspend`, con la prima
  richiesta dopo il silenzio accettata come lenta e misurata; nessun processo in background
  da sorvegliare.
- **Accessibility and security.** Nessun asterisco sui campi obbligatori, gli opzionali
  marcati "(optional)"; URL incollati trattati come ostili (niente indirizzi privati,
  redirect controllati, dimensione massima); upload limitati per tipo e dimensione; segreti
  solo lato server.
- **Data integrity and recovery.** L'embedding è indice derivato e si rigenera da
  nome, ingredienti e preparazione più tag e tempo se presenti; il fallimento di embedding o
  di upload non fa perdere la ricetta, che resta salvata e ritentabile; una sola cover per
  ricetta; duplicati ammessi per scelta.
- **Cost.** Le chiamate a pagamento avvengono in aggiunta e in modifica; l'unica in lettura è
  l'embedding della query, ed è misurata. Ogni riga che ne introduce una registra a log il
  costo per chiamata.
