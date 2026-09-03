# Roadmap — Recipe App

**Goal:** Un'app dove famiglia e amici tengono le ricette in ricettari condivisi, le aggiungono
incollando un link con attrito quasi nullo, e le ritrovano con una ricerca semantica che funziona
anche fra lingue diverse — il tutto a centesimi al mese.

**Sources:** `sources/goal.md`, `sources/concepts.md`, `sources/arch-choices.md`,
`sources/tech-choices.md`.

**Current state:** Niente è stato consegnato. È la prima stesura e sta soltanto sui quattro
documenti di `sources/`: nessuna riga di codice, nessun conto aperto, nessuna decisione verificata
sul campo.

## Themes

| Theme | Promise | First validator |
|---|---|---|
| `ricettario` | Scrivo una ricetta a mano nel mio ricettario, la ritrovo nell'elenco, la rileggo e la correggo quando voglio. | `S3` |
| `import` | Incollo il link di una ricetta e il sistema la scarica, la legge e la salva da solo, dicendomi a che punto è davvero. | `S4` |
| `ricerca` | Cerco "cena leggera" o "pomodoro" e trovo la ricetta giusta del mio ricettario, anche se è scritta in un'altra lingua. | `S6` |
| `identita` | Entro con il mio account Google e ritrovo le mie ricette, che nessun altro vede. | `S7` |
| `condivisione` | Mando un link a chi voglio e da lì dentro il ricettario siamo pari: leggiamo ed editiamo tutto in due. | `S8` |
| `foto` | Le mie ricette hanno le loro foto con una copertina scelta da me, e quando importo da un link la foto arriva da sola. | `S9` |

## NOW

| Id | Title | Theme | Kind | Size | Readiness | Executor | Depends on |
|---|---|---|---|---|---|---|---|
| S0 | [Repository, CI e conti da spendere](slices/S0-repository-ci-conti.md) | `—` | `enabler` | `small` | `needs-decision` | `mixed` | — |
| S1 | [Scheletro camminante: container su Fly, Postgres e migrazioni](slices/S1-scheletro-camminante.md) | `—` | `release` | `medium` | `ready` | `mixed` | — |
| S2 | [Spike: quanto regge la ricerca cross-lingua](slices/S2-spike-ricerca-cross-lingua.md) | `ricerca` | `spike` | `medium` | `ready` | `agent` | — |
| S3 | [Il ricettario a mano: elenco, dettaglio, form](slices/S3-ricettario-a-mano.md) | `ricettario` | `product` | `medium` | `ready` | `agent` | — |
| S4 | [Aggiunta da link con JSON-LD e progress reale](slices/S4-aggiunta-da-link.md) | `import` | `product` | `medium` | `ready` | `agent` | S3 |
| S5 | [Estrazione LLM: fallback senza JSON-LD e testo incollato](slices/S5-estrazione-llm.md) | `import` | `product` | `medium` | `needs-decision` | `agent` | S4 |
| S6 | [Ricerca semantica cross-lingua nel ricettario](slices/S6-ricerca-semantica.md) | `ricerca` | `product` | `medium` | `ready` | `agent` | S2, S3 |
| S7 | [Login Google e il ricettario di chi entra](slices/S7-login-google.md) | `identita` | `product` | `medium` | `ready` | `mixed` | S3 |
| S8 | [Invito al ricettario e membri pari](slices/S8-invito-e-membri.md) | `condivisione` | `product` | `medium` | `ready` | `agent` | S7 |
| S9 | [Foto della ricetta, a mano e dal link](slices/S9-foto-ricetta.md) | `foto` | `product` | `medium` | `ready` | `mixed` | S4 |
| S10 | [In mano a famiglia e amici](slices/S10-in-mano-a-famiglia-e-amici.md) | `—` | `release` | `small` | `ready` | `mixed` | S8 |

## LATER

- Filtri strutturati su tag e tempo, e ricerca ibrida che mette insieme semantica e full-text.
- Ricerca che attraversa più ricettari insieme invece del solo ricettario corrente.
- Ricettari pubblici tematici (vegano, giapponese), come `Cookbook.visibility = public`.
- Un concetto di gruppo sopra i ricettari, se ri-invitare le stesse persone a ogni ricettario
  diventasse fastidioso.
- Ruoli e permessi granulari dentro un ricettario, se "tutti pari" si rivelasse troppo.
- Macchina Fly sempre calda (`min_machines_running = 1`, ~$3/mese), se il risveglio del primo utente
  della giornata desse fastidio.
- Passkeys come secondo metodo di accesso, quando il recupero dell'account e il supporto in Auth.js
  saranno meno acerbi.

## OUT-OF-SCOPE

- **Ingredienti strutturati in quantità e unità.** Perché non li modelliamo, il salvataggio non ha
  parsing né validazione di unità, il form è tre campi di testo libero e l'estrazione non deve
  indovinare numeri: il prezzo è che lista della spesa e scaling delle porzioni restano impossibili
  finché qualcuno non riscrive il modello e migra le ricette già dentro.
- **Il passo di review nel flusso di aggiunta.** Perché non esiste, l'estrazione si salva senza
  conferma e non c'è nessun form intermedio, nessuna bozza e nessuno stato "in attesa" da
  mantenere: il prezzo è che un'estrazione sbagliata entra nel ricettario e ci resta finché qualcuno
  non la corregge.
- **La deduplica delle ricette.** Perché i duplicati sono ammessi, l'aggiunta non fa nessun controllo
  di esistenza, non ha una chiave naturale da definire e non chiede mai conferma: il prezzo è che due
  membri che linkano la stessa pagina si ritrovano due ricette identiche nello stesso ricettario.
- **Il provider email.** Perché non ne esiste uno, non ci sono password, reset, notifiche né inviti
  spediti: l'invito è un link che chi invita inoltra da sé, e l'identità è tutta delegata a Google —
  il prezzo è che chi perde l'accesso al proprio account Google perde l'accesso all'app, e che non
  c'è nessun modo di avvisare qualcuno di qualcosa.

## Assumptions

- `goal`, `S1`, `S10` — **Il target di costo si legge come "centesimi al mese", non come free tier
  stretto.** `goal.md` riassume l'hosting dentro il free tier; `arch-choices.md`, che è la sezione
  che decide l'hosting, dice che Fly non ha più un free tier vero ed è a consumo dal 2024. Presa la
  lettura di `arch-choices.md`: si parte con `suspend` + scale-to-zero e si accetta una bolletta di
  centesimi.
- `ricerca`, `S6` — **La ricerca embedda la query a runtime, una chiamata per ricerca.** `goal.md` e
  `arch-choices.md` dicono che embedding e LLM non girano mai a runtime sulle query, ma la query di
  `concepts.md` è `similarity(Recipe.embedding, embedding(query))`, che senza il vettore della query
  non esiste; e `arch-choices.md`, poche righe sotto il divieto, conta comunque il costo delle query
  e lo chiama irrilevante. Presa la lettura per cui il divieto è sul costo e sulla latenza, non sul
  meccanismo.
- `import`, `S4` — **I passi della barra sono quelli che la pipeline esegue davvero, non i quattro di
  `goal.md` alla lettera.** `goal.md` elenca `Scarico pagina → Leggo ricetta → Trovo ingredienti →
  Salvo foto` ma vincola una cosa sola: che i passi siano reali e non finti. La pipeline di
  `concepts.md` non ha un passo che "trova gli ingredienti" — l'estrazione è un colpo solo, JSON-LD o
  LLM — e la foto arriva con il tema `foto`. La barra mostra i passi che ci sono.
- `ricettario`, `identita`, `S3`, `S7` — **Prima del login lo scope del ricettario è configurato, non
  autenticato, e il seam è uno solo.** Nessuna sorgente dice da dove esca il ricettario "corrente"
  prima che ci sia un utente. Le righe che precedono il login girano su un unico proprietario
  implicito e non vanno riscritte quando arriva quello vero: passano tutte da un solo resolver, di
  cui il login sostituisce il layer e nient'altro.
- `identita`, `S7` — **Il primo login crea da sé il ricettario personale di chi entra.** Le sorgenti
  danno `Cookbook.creatorId` e la membership N:N ma non dicono da dove nasca il primo ricettario;
  senza, l'home non ha uno scope e il primo salvataggio ha un passo di setup davanti, contro il
  principio dell'attrito minimo.

## Open questions

- `goal`, `S5`, `S8` — L'estrazione LLM si paga a ricetta e non ha tetto per utente, mentre l'invito
  è un link che chiunque può inoltrare a chiunque. Nessuna sorgente dice se serva un limite di
  aggiunte per utente o per ricettario. Se serve, è una riga che oggi la mappa non ha.
- `condivisione`, `S8` — Nessuna sorgente dice se un membro possa uscire da un ricettario o esserne
  rimosso, né che fine facciano le sue ricette e il ricettario se il creator se ne va. Se la risposta
  è che si può, è una riga che oggi la mappa non ha; se è che non si può, è un'esclusione da
  scrivere.

## Cross-functional concerns

- **Autorizzazione.** Ogni lettura e ogni scrittura di ricette passa da un unico resolver del
  ricettario corrente: nessuna query di dominio prende `cookbookId` da input dell'utente. Il resolver
  nasce configurato e diventa autenticato senza che le query cambino, e l'unica domanda di
  autorizzazione che il sistema si pone è se esista una `Membership`.
- **Validazione ed errori.** Non c'è un passo di review, quindi l'unico controllo su un'estrazione è
  quello automatico: ciò che non valida contro lo schema non viene salvato, e il messaggio nomina il
  passo della pipeline in cui è successo — `Scarico la pagina` è un'altra cosa da `Leggo la ricetta`,
  e l'utente deve poterle distinguere per sapere se il rimedio è incollare il testo.
- **Operabilità.** La macchina parte spenta: `auto_stop = suspend`, `min_machines_running = 0`. Ogni
  riga che dichiara una latenza la misura sul primo colpo dopo il silenzio, mai a macchina calda.
- **Sicurezza.** Il token d'invito è una credenziale al portatore ed è l'unica cosa che separa un
  estraneo dal ricettario: generato con entropia crittografica, non enumerabile, revocabile dal
  ricettario, e mai scritto nei log né in un URL che l'app registra.
- **Integrità e recupero del dato.** L'`embedding` è indice derivato e non dato canonico: si rigenera
  da `nome + ingredienti + preparazione`, più `tag` e `tempo` quando ci sono, a ogni salvataggio e a
  ogni modifica. Una ricetta senza embedding, o con uno vecchio, resta visibile, apribile e
  correggibile: esce solo dai risultati di ricerca finché non è rigenerato.
- **Costo.** LLM ed embedding si pagano solo in scrittura, una volta per ricetta. Nessuna riga può
  introdurre una chiamata a pagamento su un percorso di lettura, e la sola eccezione ammessa è
  l'embedding della query di ricerca — che è dichiarata in `Assumptions` e misurata in `S6`.
