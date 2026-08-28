# Roadmap — Recipe App

**Goal:** Un ricettario condiviso tra famiglia e amici in cui aggiungere una ricetta costa quasi
niente — si incolla un link e si compila da sola — e in cui si ritrova quello che si cerca per
significato e non per parola, anche attraverso le lingue: cerchi "pomodoro" e trovi la ricetta
scritta in inglese. Tutto entro pochi centesimi al mese.

**Sources:** `sources/goal.md`, `sources/concepts.md`, `sources/arch-choices.md`,
`sources/tech-choices.md`.

**Current state:** Primo disegno. Non è stato consegnato niente: nessun repository, nessun account,
nessun deploy.

## Themes

| Theme | Promise | First validator |
|---|---|---|
| `ricettario` | Vedi l'elenco delle ricette del ricettario corrente, ne scrivi una a mano e la correggi quando vuoi. | `S3` |
| `estrazione` | Incolli l'URL di una ricetta e si compila da sola, mostrando i passi che sta davvero facendo, e si salva senza doverla rivedere prima. | `S5` |
| `foto` | Ogni ricetta porta le sue foto, con una copertina che all'inizio è la prima e poi la scegli tu. | `S7` |
| `ricerca` | Cerchi "cena leggera" nel ricettario corrente e trovi anche le ricette scritte in un'altra lingua. | `S4` |
| `identita` | Entri con il tuo account Google e vedi soltanto i ricettari di cui fai parte. | `S8` |
| `condivisione` | Mandi un link a un familiare e da lì in poi leggete e scrivete le stesse ricette, da pari. | `S9` |

**Theme boundaries**

- `ricettario` / `estrazione` — **split.** Cancellata l'estrazione, l'evidenza del ricettario resta
  intatta: si verifica su ricette scritte a mano.
- `estrazione` / `foto` — **split.** Le foto hanno un adapter e un invariante propri (una sola
  copertina) e due produttori distinti, mentre l'estrazione si verifica su ricette senza immagini.
- `foto` / `ricerca` — **split.** La ricerca indicizza `nome + ingredienti + preparazione` e non
  legge le foto: nessuna delle due tocca l'evidenza dell'altra.
- `ricerca` / `identita` — **split.** La ricerca si misura su un ricettario configurato, prima che
  esista un utente autenticato.
- `identita` / `condivisione` — **split.** L'accesso con Google resta utile con un solo membro;
  l'invito si cancella senza invalidarlo.

## NOW

| Id | Title | Theme | Kind | Size | Readiness | Executor | Depends on |
|---|---|---|---|---|---|---|---|
| S0 | [Repository, CI e account](slices/S0-repository-ci-e-account.md) | `—` | `enabler` | `small` | `needs-decision` | `mixed` | — |
| S1 | [Scheletro deployato su Fly](slices/S1-scheletro-deployato-su-fly.md) | `—` | `release` | `medium` | `ready` | `mixed` | — |
| S2 | [Spike: recall cross-lingua degli embedding](slices/S2-spike-recall-cross-lingua.md) | `ricerca` | `spike` | `small` | `ready` | `agent` | — |
| S3 | [Ricetta a mano nel ricettario](slices/S3-ricetta-a-mano-nel-ricettario.md) | `ricettario` | `product` | `medium` | `ready` | `agent` | — |
| S4 | [Ricerca semantica cross-lingua](slices/S4-ricerca-semantica-cross-lingua.md) | `ricerca` | `product` | `medium` | `ready` | `agent` | S2, S3 |
| S5 | [Aggiunta da link con progresso reale](slices/S5-aggiunta-da-link-con-progresso-reale.md) | `estrazione` | `product` | `large` | `ready` | `agent` | S3 |
| S6 | [Fallback LLM e copia-incolla](slices/S6-fallback-llm-e-copia-incolla.md) | `estrazione` | `product` | `medium` | `ready` | `agent` | S5 |
| S7 | [Foto della ricetta](slices/S7-foto-della-ricetta.md) | `foto` | `product` | `medium` | `ready` | `mixed` | S3, S5 |
| S8 | [Accesso con Google e ricettari propri](slices/S8-accesso-con-google-e-ricettari-propri.md) | `identita` | `product` | `large` | `ready` | `mixed` | S3, S4 |
| S9 | [Invito al ricettario](slices/S9-invito-al-ricettario.md) | `condivisione` | `product` | `medium` | `ready` | `agent` | S8 |
| S10 | [Rilascio a famiglia e amici](slices/S10-rilascio-a-famiglia-e-amici.md) | `—` | `release` | `small` | `ready` | `mixed` | S6, S7, S9 |

## LATER

- Indice HNSW su `Recipe.embedding`, se le ricette per ricettario superassero le centinaia previste.
- Filtri strutturati per tag e tempo, e ricerca ibrida semantica più full-text: i campi si popolano
  da subito, quindi si abilitano senza migrazione.
- Ricettari pubblici tematici, come `Cookbook.visibility = public`.
- Un concetto di gruppo sopra i ricettari, se ri-invitare gli stessi membri in ognuno diventasse
  fastidioso.
- Ricerca su più ricettari insieme.
- Macchina Fly sempre calda (`min_machines_running = 1`), se il risveglio misurato desse fastidio.
- Passkeys come secondo metodo di accesso.
- Ridimensionamento e thumbnail delle foto.
- Import da foto o PDF con OCR, se ribattere una ricetta di carta diventasse frequente.
- IaC versionata al posto di `fly.toml` più CLI.

## OUT-OF-SCOPE

- **Ingredienti strutturati in quantità e unità.** Perché la ricetta resta testo libero,
  l'implementazione può fare a meno di un parser di ingredienti, di un modello di step e di ogni
  campo obbligatorio prima del salvataggio; il prezzo è che lista della spesa e scaling delle
  porzioni restano preclusi per sempre, non rimandati.
- **Deduplica delle ricette.** Perché due membri possono linkare la stessa ricetta senza che il
  sistema se ne accorga, l'aggiunta non paga né confronto né chiave di unicità e resta un solo
  INSERT; il prezzo è che lo stesso piatto può comparire più volte nello stesso ricettario.
- **Ruoli e permessi granulari.** Perché dentro un ricettario tutti i membri sono pari, ogni
  controllo di autorizzazione si riduce a "esiste una `Membership`" e nessuna schermata ha varianti
  per ruolo; il prezzo è che non si può invitare qualcuno in sola lettura.
- **Revisione obbligatoria prima del salvataggio.** Perché l'estratto si salva comunque, il flusso
  di aggiunta non ha stato intermedio, bozze, né form da superare, e l'edit è l'unica correzione;
  il prezzo è che ricette imperfette entrano nel ricettario e si sistemano dopo.
- **Accesso senza Google.** Perché l'identità è solo Google OAuth, l'app non ha password, hashing,
  invio email né flusso di reset, e non paga alcun provider email; il prezzo è la dipendenza da
  Google e l'esclusione di chi non ha un account Google.

## Assumptions

- `goal, S1, S10` — `goal.md` dice "tutto entro free tier … target ~$0/mese" ma `arch-choices.md`
  dice che Fly "non ha più un free tier vero". La mappa legge il secondo, che è il documento che
  decide l'hosting, e prende la sua raccomandazione: `suspend` più scale-to-zero, target centesimi
  al mese e non zero. S1 misura il risveglio, S10 dichiara la bolletta vera.
- `ricerca, S4` — `arch-choices.md` dice che gli embedding sono usati "mai a runtime sulle query di
  ricerca", ma poche righe sopra conta il costo delle query e `concepts.md` scrive
  `embedding(query)`. La mappa legge il divieto come riferito all'LLM e alla ri-indicizzazione del
  corpus: la query viene embeddata a ogni ricerca e la sua latenza sta dentro la richiesta. S4 la
  misura.
- `ricerca, S4` — `arch-choices.md` dice che "a questi numeri lo scan vettoriale è già in pochi ms"
  e che HNSW serve a 100k+: alla scala dichiarata (centinaia di ricette per ricettario) la mappa
  prende lo scan esatto filtrato per `cookbookId` e rimanda l'indice, che sotto un filtro stretto
  rischia di perdere recall. Il p95 misurato da S4 può smentirla.
- `estrazione, S5` — i quattro passi che `goal.md` elenca per la progress bar non corrispondono agli
  stadi della pipeline di `concepts.md`: "Trovo ingredienti" non è uno stadio, l'estrazione produce
  la ricetta intera in un colpo. La mappa tiene il vincolo ("passi reali, non fake") e non l'elenco:
  la barra riporta gli stadi in cui il server è davvero entrato.
- `estrazione, S6` — "modello cheap, Haiku-class" è una classe, non un modello. La mappa la prende
  come tale e tiene l'estrattore dietro una porta Effect con output validato da `Schema`, così il
  modello resta sostituibile; S6 misura il costo per estrazione contro le "frazioni di cent" che le
  fonti assumono.
- `ricettario, identita, S3, S8` — nessuna fonte dice come si sceglie il "ricettario corrente" su
  cui poggiano elenco e ricerca. La mappa lo fa possedere da un solo resolver: in S3 risolve da
  configurazione a un ricettario seminato, in S8 all'appartenenza dell'utente autenticato. Le righe
  da S3 a S7 girano quindi su un proprietario unico implicito, su staging non pubblico, e la mappa
  assume che nessuna di esse debba essere riscritta quando arriva l'identità: S8 lo verifica
  guardando se i punti di query sono rimasti intatti.
- `foto, estrazione, S5, S7` — `goal.md` mette `Salvo foto` tra i passi dell'aggiunta da link, ma lo
  storage foto ha un adapter e un invariante propri e due produttori che lo alimentano. La mappa dà
  a S7 la proprietà intera di quello storage e gli fa aggiungere quello stadio al flusso che S5
  consegna, quindi S5 salva ricette senza immagini. Se i tester leggessero come inaccettabili le
  ricette che S5 salva, l'ordine è sbagliato.

## Open questions

- `goal, ricerca, S2, S4` — nessuna fonte dice cosa succede se la recall cross-lingua misurata non
  regge la promessa. Le fonti stesse avvertono che senza quella ricerca "staremmo riscrivendo
  Mealie": se il numero di S2 fosse deludente, o entra una riga di ripiego che oggi la mappa non ha
  (la ricerca ibrida, che l'MVP rimanda) o si cambia obiettivo. La risposta decide quale.
- `goal, condivisione, S9, S10` — le fonti fissano il costo assumendo che ad aggiungere ricette sia
  chi possiede il ricettario, ma da S9 in poi chiunque abbia il link può farlo, e nessuna fonte dice
  se serve un tetto per ricettario o per utente. Se serve, è una riga che la mappa non ha.

## Cross-functional concerns

- **Authorization.** Un solo resolver, `CurrentCookbook`, possiede lo scope: ogni lettura e ogni
  scrittura di `Recipe` e `Photo` ci passa, da S3 in poi, e nessuna query lo aggira. S8 sostituisce
  l'adapter dietro quel resolver senza toccare i punti di query, e una richiesta per un ricettario
  di cui non si è membri viene rifiutata, non svuotata.
- **Validation and errors.** L'estrazione non si fida di nulla che arrivi da fuori: JSON-LD e output
  LLM sono decodificati con `Schema` e mai castati, ogni fallimento è un `Data.TaggedError` e la
  barra di progresso lo nomina per stadio. Un errore che il flusso non sa nominare non salva una
  ricetta parziale.
- **Accessibility and security.** L'URL da aggiungere arriva dall'utente e viene scaricato dal
  nostro server: S5 lo tratta come ingresso ostile — solo schema `http(s)`, nessun indirizzo di rete
  privata, tetto alla dimensione del corpo e al numero di redirect. Lo stesso vale per l'immagine di
  copertina che S7 scarica.
- **Cost.** Il costo è un vincolo che le fonti impongono a più righe, quindi ogni chiamata a un
  servizio a pagamento — estrazione LLM, embedding, download immagine — dichiara timeout e tetto per
  richiesta, e la riga che la introduce misura la spesa reale invece di ripetere la stima delle
  fonti.
- **Data integrity and recovery.** L'`embedding` è indice derivato, non dato canonico: si rigenera a
  ogni scrittura di `Recipe` e il suo fallimento non impedisce il salvataggio. Sullo stesso
  principio la foto è un effetto opzionale dell'aggiunta: se lo storage non risponde, la ricetta si
  salva comunque e lo stadio si dichiara fallito.
- **Operability.** Le migrazioni Drizzle girano al deploy e non a mano: S1 lo stabilisce con una
  migrazione non di dominio, e ogni riga successiva ci appoggia il proprio schema. È la condizione
  perché scale-to-zero resti pulito, dato che il container è stateless.
