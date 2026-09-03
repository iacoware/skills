# Roadmap — Recipe App

**Goal:** Un ricettario condiviso tra famiglia e amici in cui una ricetta si aggiunge incollando un
link (o incollandone il testo, o scrivendola a mano) e si ritrova cercandola a parole, anche quando è
scritta in un'altra lingua — tenuto entro pochi centesimi al mese.

**Sources:** `sources/goal.md`, `sources/arch-choices.md`, `sources/tech-choices.md`,
`sources/concepts.md`.

**Current state:** Niente è stato consegnato. Il progetto è greenfield: non esiste repository, non
esistono account sui servizi, non esiste codice. Le scelte di infrastruttura e di stack sono già
prese nelle fonti e questa mappa le dà per decise.

## Themes

| Theme | Promise | First validator |
|---|---|---|
| `cattura` | Incollo il link di una ricetta, l'app la salva da sola mostrandomi a che punto è, e la ritrovo in elenco. | `S3` |
| `ricerca` | Cerco "cena leggera" o "pomodoro" e trovo le ricette del ricettario che ne parlano, anche quando sono scritte in un'altra lingua. | `S5` |
| `accesso` | Entro con il mio account Google e trovo il mio ricettario, senza password e senza email. | `S6` |
| `condivisione` | Mando un link a mia sorella e da quel momento aggiungiamo e correggiamo le stesse ricette. | `S7` |
| `correzione` | Correggo una ricetta estratta male, o ne scrivo una a mano che non sta su nessun sito, con lo stesso form. | `S8` |
| `foto` | Vedo le ricette con le loro foto e scelgo quale fa da copertina. | `S9` |

**Theme boundaries**

- `cattura` / `ricerca` — **split.** Un ricettario di poche decine di ricette si sfoglia: la ricerca
  si può rimandare senza invalidare la prova che l'aggiunta funziona.
- `cattura` / `correzione` — **split.** Il flusso di add non ha review e salva anche un'estrazione
  sbagliata, quindi la correzione si cancella intera senza toccare l'aggiunta.
- `cattura` / `foto` — **split.** Il download dell'immagine è un passo in più nella stessa pipeline,
  ma un ricettario senza immagini resta pienamente usabile.
- `ricerca` / `accesso` — **split.** La qualità della ricerca si misura su un ricettario configurato,
  prima che esista un'identità.
- `accesso` / `condivisione` — **split.** Un utente solo col proprio ricettario è già usabile senza
  inviti.
- `correzione` / `foto` — **split.** Il form di modifica e la galleria si cancellano l'uno senza
  l'altra.

## NOW

| Id | Title | Theme | Kind | Size | Readiness | Executor | Depends on |
|---|---|---|---|---|---|---|---|
| `S0` | [Repository, CI e credenziali](slices/S0-repository-ci-credenziali.md) | `—` | `enabler` | `small` | `ready` | `mixed` | — |
| `S1` | [Scheletro deployato su Fly con Postgres](slices/S1-scheletro-fly-postgres.md) | `—` | `release` | `medium` | `needs-decision` | `mixed` | — |
| `S2` | [Recall cross-lingua degli embedding multilingue](slices/S2-recall-cross-lingua.md) | `ricerca` | `spike` | `medium` | `ready` | `agent` | — |
| `S3` | [Aggiungi da link con JSON-LD, elenco e dettaglio](slices/S3-add-da-link-jsonld.md) | `cattura` | `product` | `large` | `ready` | `agent` | `S2` |
| `S4` | [Estrazione LLM per pagine senza structured data](slices/S4-estrazione-llm.md) | `cattura` | `product` | `medium` | `needs-decision` | `agent` | `S3` |
| `S5` | [Ricerca semantica nel ricettario](slices/S5-ricerca-semantica.md) | `ricerca` | `product` | `medium` | `ready` | `agent` | `S3` |
| `S6` | [Accesso con Google e ricettario proprio](slices/S6-accesso-google.md) | `accesso` | `product` | `medium` | `ready` | `mixed` | `S3` |
| `S7` | [Invito condivisibile a un ricettario](slices/S7-invito-ricettario.md) | `condivisione` | `product` | `small` | `ready` | `agent` | `S6` |
| `S8` | [Modifica di una ricetta e inserimento a mano](slices/S8-modifica-e-inserimento-manuale.md) | `correzione` | `product` | `medium` | `ready` | `agent` | `S3` |
| `S9` | [Foto multiple e copertina](slices/S9-foto-e-copertina.md) | `foto` | `product` | `medium` | `ready` | `agent` | `S3` |
| `S10` | [Rilascio a famiglia e amici](slices/S10-rilascio.md) | `—` | `release` | `small` | `ready` | `mixed` | `S7` |

## LATER

- Filtri di ricerca strutturati su tag e tempo di preparazione, sui campi che l'MVP popola già.
- Ricerca ibrida: similarità semantica combinata con full-text sul testo della ricetta.
- Ricerca che attraversa tutti i ricettari di cui l'utente è membro.
- Ricettari pubblici tematici, con `visibility` a `public`.
- Un concetto di gruppo sopra i ricettari, che eviti di ri-invitare gli stessi membri ogni volta.
- Ruoli e permessi dentro un ricettario, se "tutti pari" diventasse scomodo.
- Passkeys come secondo metodo di accesso accanto a Google.
- Macchina Fly sempre calda, se la latenza del primo utente dopo il silenzio desse fastidio.

## OUT-OF-SCOPE

- **Ingredienti strutturati in quantità e unità.** Perché resta irrisolto, `ingredients` può essere
  una colonna di testo libero, nessuna riga deve scrivere un parser di unità né un modello di
  ingrediente, e l'estrazione può fallire su una quantità senza fallire sulla ricetta. Il prezzo è
  che lista della spesa e scaling delle porzioni restano impossibili finché quel modello non esiste.
- **La review obbligatoria prima del salvataggio.** Perché resta irrisolta, il flusso di add non ha
  stato intermedio da persistere né schermata di conferma, e la pipeline può scrivere direttamente
  sulla tabella finale. Il prezzo è che in elenco compaiono ricette estratte male finché qualcuno
  non le corregge.
- **La deduplica delle ricette.** Perché resta irrisolta, l'aggiunta non deve mai confrontare una
  ricetta con quelle già presenti e non serve una nozione di identità della ricetta oltre alla sua
  riga. Il prezzo è che la stessa ricetta linkata da due membri dello stesso ricettario compare due
  volte.
- **Invio di email e notifiche.** Perché resta irrisolto, nessuna riga porta un provider email, un
  template, una coda di invio o un flusso di reset — ed è questo che rende Google OAuth sufficiente
  come unico metodo di accesso. Il prezzo è che un invito viaggia solo come link copiato a mano su
  un canale che non è l'app, e che nulla avvisa i membri di quello che succede nel ricettario.

## Assumptions

- `goal, S1, S10` — Le fonti si contraddicono sull'hosting: `goal.md` dichiara "tutto entro free
  tier … target ~$0/mese", `arch-choices.md` dice che Fly "non ha più un free tier vero". La mappa
  prende la lettura di `arch-choices.md`, che è la sezione che analizza il fornitore: il bersaglio è
  *pochi centesimi al mese* con `suspend` e scale-to-zero, non zero, e diventa ~$3/mese il giorno in
  cui si tiene la macchina calda. S10 legge la spesa reale e la confronta con questa cifra.
- `ricerca, S5` — `arch-choices.md` dice che gli embedding non si usano "mai a runtime sulle query di
  ricerca", ma poche righe sopra ne prezza il costo ("le query sono irrilevanti"). La mappa legge il
  divieto come un divieto di ri-embeddare il corpus a ogni ricerca, non come un divieto di embeddare
  la query: senza il vettore della query non esiste ricerca semantica. S5 fa una chiamata di
  embedding per ricerca, e nessuna riga ne fa una per ricetta mostrata.
- `S3, S4, S5` — Fino a S6 il ricettario corrente è un cookbook seminato che il resolver dello scope
  restituisce da configurazione: queste righe girano sull'ambiente non pubblico, con un solo
  proprietario implicito, e possono ignorare che esistano più utenti. L'assunto è che non vadano
  riscritte quando arriva l'identità — cambia solo cosa restituisce il resolver.
- `accesso, S6` — Nessuna fonte dice come nasce il primo ricettario di un utente. La mappa assume che
  al primo accesso Google se ne crei automaticamente uno di cui l'utente è creator, senza schermata
  di creazione: è la lettura coerente con "attrito minimo" e con il fatto che nessuna fonte descrive
  un flusso di creazione.
- `S6, S10` — La mappa assume che l'app Google OAuth resti in modalità testing, dove i tester
  autorizzati bastano per famiglia e amici, e che quindi l'MVP non debba passare dalla verifica
  dell'app da parte di Google. Se il limite o la verifica mordono, S10 cresce di un passo che oggi
  non ha.
- `cattura, S3, S4` — `goal.md` chiede un'estrazione **sincrona** con progress sui passi reali, e
  `arch-choices.md` mette l'app su macchine che si sospendono. La mappa assume che una singola
  estrazione (fetch, parse o chiamata LLM, embedding, scrittura) stia dentro il tempo di una
  richiesta HTTP, e quindi che nessuna riga debba introdurre coda, job o worker. S3 misura quel tempo
  ed è la riga che può rifiutare l'assunto.

## Open questions

- `goal, condivisione` — Un utente può stare in più ricettari e la Home mostra "il ricettario
  corrente", ma nessuna fonte dice come si sceglie. Se serve uno switcher esplicito o una schermata
  di scelta post-login, è una riga che questa mappa non ha; se il corrente è semplicemente l'ultimo
  usato, non lo è.

## Cross-functional concerns

- **Authorization.** Ogni lettura e ogni scrittura di `Recipe` e `Photo` passa da un solo resolver
  del ricettario corrente: fino a S6 restituisce il cookbook configurato, da S6 quello del membro
  autenticato. Nessuna riga interroga `Recipe` senza un `cookbookId`, e l'unica domanda di
  autorizzazione che l'MVP pone è "sei membro di questo ricettario?".
- **Validation and errors.** Un'estrazione parziale si salva comunque: nessuna riga può introdurre
  una conferma o una review prima del salvataggio, e un campo che l'estrazione non ha trovato resta
  vuoto invece di bloccare la ricetta. Ogni passo della pipeline di add nomina il proprio fallimento
  all'utente — "paywall", "pagina non leggibile", "non ho trovato una ricetta in questa pagina" —
  mai un errore generico.
- **Cost.** LLM ed embedding si spendono solo in scrittura (aggiunta e modifica) e sull'embedding
  della singola query di ricerca. Nessuna riga può introdurre una chiamata a pagamento per ricetta
  mostrata, per riga di elenco o per apertura della Home.
- **Operability.** Ogni riga resta compatibile con `suspend` e scale-to-zero: nessun processo
  long-running, nessuno stato in memoria che debba sopravvivere fra due richieste, nessun volume
  montato. Le foto stanno su R2, i dati su Postgres, e il contenitore è sacrificabile.
- **Data integrity and recovery.** `embedding` è indice derivato, non dato canonico: ogni riga che
  scrive `name`, `ingredients`, `steps`, `tags` o `prepTime` lo rigenera insieme a quella scrittura,
  e un embedding mancante o vecchio degrada la ricerca senza mai perdere la ricetta.
- **Accessibility and security.** S3 e S9 scaricano dal server URL che l'utente ha incollato: la riga
  che apre ciascun fetch — la pagina in S3, l'immagine in S9 — limita schema, dimensione e timeout, e
  non segue redirect verso indirizzi interni.
