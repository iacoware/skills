# Roadmap — Recipe App

**Goal:** Un ricettario condiviso tra famiglia e amici in cui aggiungere una ricetta costa
quasi nulla (incolli un link) e ritrovarla funziona anche a distanza di lingua: cerchi
"pomodoro" e trova la ricetta scritta in inglese. Tutto entro un budget di centesimi al mese.

**Sources:** `sources/goal.md`, `sources/concepts.md`, `sources/arch-choices.md`,
`sources/tech-choices.md`.

**Current state:** Niente di consegnato: primo disegno, repository ancora da creare.

## Themes

| Theme | Promise | First validator |
|---|---|---|
| `aggiunta-da-link` | Incollo l'URL di una ricetta e la ritrovo nel ricettario senza compilare niente, guardando i passi reali dell'estrazione mentre avviene. | `S3` |
| `aggiunta-da-testo` | Quando il link non è leggibile — paywall, sito JS-heavy — incollo il testo della pagina e la ricetta entra lo stesso. | `S5` |
| `ricerca-semantica` | Cerco "cena leggera" o "pomodoro" e trovo le ricette pertinenti del ricettario corrente, anche quelle scritte in un'altra lingua. | `S6` |
| `ricettari-condivisi` | Entro col mio account Google e invito famiglia e amici con un link: dentro un ricettario tutti leggono e modificano le stesse ricette, e ognuno può stare in più ricettari. | `S8` |
| `scrittura-e-correzione` | Scrivo una ricetta a mano, e correggo qualunque ricetta salvata, nello stesso form. | `S9` |
| `foto` | Ogni ricetta ha le sue foto con una copertina che scelgo io, e quelle importate da link arrivano già con l'immagine della pagina. | `S10` |

**Theme boundaries**

- `aggiunta-da-link` / `aggiunta-da-testo` — **split.** Il testo incollato è il fallback
  dichiarato per i link illeggibili: cancellarlo lascia intatta la prova dell'import da URL, e
  viceversa.
- `aggiunta-da-testo` / `ricerca-semantica` — **split.** La ricerca si misura su ricette già
  presenti, comunque siano entrate.
- `ricerca-semantica` / `ricettari-condivisi` — **split.** La ricerca si dimostra dentro un
  ricettario solo, la condivisione si dimostra con due membri e nessuna query.
- `ricettari-condivisi` interno (accesso / invito) — **merge.** Il login da solo non produce
  riscontro utile e l'invito non esiste senza identità: una promessa sola, validata da `S8`,
  con `S7` come prima metà.
- `ricettari-condivisi` / `scrittura-e-correzione` — **split.** Correggere una ricetta si
  dimostra da soli, senza nessun altro membro.
- `scrittura-e-correzione` / `foto` — **split.** Le foto si rinviano in blocco senza togliere
  niente al form: nessuna prova del form dipende da esse.

## NOW

| Id | Title | Theme | Kind | Size | Readiness | Executor | Depends on |
|---|---|---|---|---|---|---|---|
| S0 | [Repository, CI e credenziali](slices/S0-repository-ci-credenziali.md) | `—` | `enabler` | `medium` | `ready` | `mixed` | — |
| S1 | [Spike: la ricerca cross-lingua regge su ricette vere?](slices/S1-spike-ricerca-cross-lingua.md) | `goal` | `spike` | `small` | `ready` | `agent` | — |
| S2 | [Walking skeleton: Next.js su Fly con Postgres e migrazioni](slices/S2-walking-skeleton.md) | `—` | `release` | `medium` | `ready` | `mixed` | — |
| S3 | [Aggiunta da link con JSON-LD e elenco del ricettario](slices/S3-aggiunta-da-link-json-ld.md) | `aggiunta-da-link` | `product` | `large` | `ready` | `agent` | — |
| S4 | [Estrazione LLM quando il JSON-LD manca](slices/S4-estrazione-llm-fallback.md) | `aggiunta-da-link` | `product` | `medium` | `needs-decision` | `agent` | S3 |
| S5 | [Aggiunta da testo incollato](slices/S5-aggiunta-da-testo-incollato.md) | `aggiunta-da-testo` | `product` | `small` | `ready` | `agent` | S4 |
| S6 | [Ricerca semantica cross-lingua nel ricettario](slices/S6-ricerca-semantica.md) | `ricerca-semantica` | `product` | `medium` | `ready` | `agent` | S1, S3 |
| S7 | [Accesso con Google e scope autenticato](slices/S7-accesso-google.md) | `ricettari-condivisi` | `product` | `medium` | `ready` | `mixed` | S3 |
| S8 | [Invito via link e ricettari condivisi](slices/S8-invito-e-ricettario-condiviso.md) | `ricettari-condivisi` | `product` | `medium` | `needs-decision` | `agent` | S7 |
| S9 | [Scrittura a mano e correzione](slices/S9-scrittura-e-correzione.md) | `scrittura-e-correzione` | `product` | `medium` | `ready` | `agent` | S3, S6 |
| S10 | [Foto della ricetta](slices/S10-foto-della-ricetta.md) | `foto` | `product` | `medium` | `ready` | `agent` | S3, S9 |
| S11 | [Messa in mano a famiglia e amici](slices/S11-messa-in-produzione.md) | `—` | `release` | `small` | `ready` | `mixed` | S8, S10 |

## LATER

- Filtri strutturati per tag e tempo sulla ricerca, sui campi già popolati best-effort in
  fase di aggiunta.
- Ricerca ibrida semantica + full-text, se la sola semantica manca i titoli esatti.
- Ricettari pubblici tematici, come `Cookbook.visibility = public`.
- Ricerca che spazia su tutti i ricettari di cui sono membro.
- Un concetto di gruppo sopra i ricettari, se ri-invitare per ognuno diventasse fastidioso.
- Macchina Fly sempre calda (~$3/mese, un flag in `fly.toml`) se il cold start desse fastidio.

## OUT-OF-SCOPE

- **Ingredienti strutturati in quantità e unità.** Poiché gli ingredienti restano testo
  libero, l'implementazione può fare a meno di parser, tabelle di unità e normalizzazione, e
  il form di add non ha nessun campo obbligatorio. Il prezzo: lista della spesa e scaling
  porzioni restano impossibili finché non si migrano i dati esistenti.
- **Ruoli e permessi granulari.** Poiché dentro un ricettario tutti i membri sono pari, un
  solo controllo — sei membro? — governa lettura e scrittura, e non serve nessun modello di
  ruolo. Il prezzo: qualunque membro può riscrivere o cancellare le ricette degli altri, e
  nessuno può risalire a chi l'ha fatto.
- **Deduplica delle ricette.** Poiché i duplicati sono consentiti, il salvataggio non fa
  nessun controllo di unicità né merge. Il prezzo: due membri che linkano la stessa pagina
  si ritrovano due ricette identiche nel ricettario.
- **Qualunque provider di posta.** Poiché non si manda nessuna email, spariscono invio,
  password, hashing, reset e template. Il prezzo: identità e recupero account dipendono
  interamente da Google, e chi non ha un account Google resta fuori dall'app.
- **Review obbligatoria dell'estratto.** Poiché non c'è nessun passo di conferma prima del
  salvataggio, il flusso di add non ha stato intermedio da persistere né bozze da riprendere.
  Il prezzo: un'estrazione sbagliata entra nel ricettario, e la si scopre solo leggendola.

## Assumptions

- `S2` — Provider Postgres: `arch-choices.md` lascia aperto "Neon o Supabase", `tech-choices.md`
  nomina Neon nella scelta del driver. Prendiamo **Neon**, e la lettura cade se il free tier
  non dà pgvector con HNSW o non regge le connessioni di una macchina che si sospende.
- `S2` — Driver: le fonti elencano `postgres.js` e `node-postgres` senza sceglierne uno.
  Prendiamo **`postgres.js`** con poche connessioni; cade se la ripresa da `suspend` lascia
  connessioni morte che il primo utente paga.
- `S3, S6, S7` — Seam di identità: fino a `S7` le ricette vivono in un unico ricettario
  configurato, risolto da un solo `currentCookbook`. Le righe prima di `S7` possono ignorare
  chi è l'utente e quanti ricettari esistono. La lettura cade se `S7` deve toccare qualcosa
  oltre a quel resolver — query, schema o UI.
- `S6, ricerca-semantica` — `goal.md` vieta LLM ed embedding "a runtime sulle query di
  ricerca", ma `concepts.md` scrive `similarity(embedding, embedding(query))` e
  `arch-choices.md` stima il costo delle query dicendolo irrilevante. Leggiamo il divieto come
  riferito ai **documenti**: la query dell'utente viene embeddata a ogni ricerca. Cade se la
  chiamata esterna per query sfonda la latenza accettabile della ricerca.
- `S3, aggiunta-da-link` — Il progresso "sui passi reali" viaggia come risposta in streaming
  di una singola richiesta sincrona; le fonti chiedono estrazione sincrona con progresso vero e
  citano lo streaming come vantaggio del container, ma non nominano il meccanismo. Cade se il
  proxy di Fly bufferizza la risposta o tronca la richiesta prima della fine dell'estrazione.
- `goal, S2, S11` — Costo: `goal.md` dice "tutto entro free tier → ~$0/mese",
  `arch-choices.md` dice che Fly non ha più un free tier vero e stima centesimi/mese con
  `suspend`. Prendiamo la seconda lettura, più specifica: il target è centesimi/mese, non $0
  letterali. Cade con la prima bolletta.

## Open questions

- `goal, S1, ricerca-semantica` — Se `S1` dicesse che nessun embedder economico regge la
  cross-lingua su ricette vere, cade il differenziatore che `goal.md` chiama "il nord": si
  ripiega su ricerca ibrida — oggi fuori scope — o si rimette in discussione il posizionamento
  rispetto a Mealie? La risposta cambia se `ricerca-semantica` resta un tema.

## Cross-functional concerns

- **Autorizzazione.** Ogni lettura e scrittura di ricette passa da un solo resolver dello
  scope corrente: configurato fino a `S7`, ricavato da sessione e membership dopo. Nessuna
  query prende il `cookbookId` da un input del client, in nessuna riga.
- **Validazione ed errori.** Ogni passo della pipeline di add ha un errore tipizzato suo, e
  quell'errore è il messaggio che la progress bar mostra: pagina non raggiungibile, contenuto
  non leggibile, output del modello fuori schema. Un passo che fallisce non può degradare in
  un messaggio generico, perché il fallimento preciso è la funzionalità.
- **Costo.** LLM ed embedding dei documenti si pagano solo in add e in edit, mai su una
  lettura: nessuna riga può introdurre una chiamata a pagamento che si ripete a ogni apertura
  o a ogni elenco di ricette.
- **Integrità dei dati.** `Recipe.embedding` è un indice derivato, mai dato canonico:
  rigenerabile da `nome + ingredienti + preparazione` più `tag + tempo` quando ci sono, e la
  sua assenza o obsolescenza non blocca né la lettura né il salvataggio della ricetta.
- **Sicurezza.** Il link di invito è l'unica credenziale che concede una membership: token
  non indovinabile, e chi lo apre entra solo dopo essersi autenticato.
