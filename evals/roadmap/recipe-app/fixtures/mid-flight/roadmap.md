# Roadmap — Recipe App

**Goal:** Mettere in mano a famiglia e amici un ricettario condiviso in cui salvare una ricetta
costa un incolla, e ritrovarla costa una frase nella propria lingua — anche quando la ricetta è
scritta in un'altra.

**Sources:** `sources/goal.md`, `sources/concepts.md`, `sources/arch-choices.md`,
`sources/tech-choices.md`.

**Current state:** Consegnate `S0`–`S3`: repository e CI, scheletro su Fly con Neon, lo spike
sull'embedder, e il ricettario corrente con il form condiviso. Il tema `ricettario` è validato per
intero e ha lasciato la tabella. `NOW` tiene le otto righe che restano.

## Themes

| Theme | Promise | First validator |
|---|---|---|
| `cattura` | Incolli il link di una ricetta e te la ritrovi salvata senza compilare niente; quando la pagina non si lascia leggere hai una via d'uscita che non ti fa ribattere tutto. | `S4` |
| `ricerca` | Cerchi con parole tue dentro il ricettario corrente e trovi la ricetta anche se è scritta in un'altra lingua. | `S7` |
| `accesso` | Entri con il tuo account Google e il ricettario che usi è il tuo: nessuna password, nessuna email. | `S8` |
| `condivisione` | Inviti famiglia e amici in un ricettario con un link: chi entra legge e modifica tutto come te, e tu passi da un ricettario all'altro. | `S9` |
| `foto` | Ogni ricetta si illustra con più foto; la prima è la copertina, e la copertina si cambia. | `S10` |

## NOW

| Id | Title | Theme | Kind | Size | Readiness | Executor | Depends on |
|---|---|---|---|---|---|---|---|
| S4 | [Aggiunta da link con JSON-LD e avanzamento reale](slices/S4-aggiunta-da-link.md) | cattura | product | medium | ready | agent | — |
| S5 | [Fallback LLM quando il JSON-LD manca](slices/S5-fallback-llm.md) | cattura | product | medium | needs-decision | mixed | S4 |
| S6 | [Copia-incolla per le pagine che non si lasciano leggere](slices/S6-copia-incolla.md) | cattura | product | small | ready | agent | S5 |
| S7 | [Ricerca semantica cross-lingua nel ricettario corrente](slices/S7-ricerca-semantica.md) | ricerca | product | medium | needs-decision | agent | — |
| S8 | [Accesso con Google e ricettario dell'utente](slices/S8-accesso-google.md) | accesso | product | medium | needs-decision | mixed | — |
| S9 | [Ricettari condivisi: invito via link e più ricettari](slices/S9-ricettari-condivisi.md) | condivisione | product | large | ready | agent | S8 |
| S10 | [Foto multiple e copertina su object storage](slices/S10-foto-e-copertina.md) | foto | product | medium | ready | mixed | S4 |
| S11 | [Rilascio a famiglia e amici](slices/S11-rilascio.md) | — | release | small | needs-decision | mixed | S9 |

## LATER

- Filtri strutturati per tag e tempo, e ricerca ibrida semantica più full-text.
- Ricettari pubblici tematici, come Cookbook con `visibility=public`.
- Ricerca che attraversa tutti i ricettari di cui si è membri.
- Un concetto di gruppo sopra i ricettari, se ri-invitare in ognuno diventasse fastidioso.
- Ruoli e permessi dentro un ricettario, oltre al solo `creatorId`.
- Passkeys come secondo metodo d'accesso, quando il recupero da dispositivo perso sarà risolto.
- Import da file esportati da altre app di ricette.
- Un quarto ingresso di estrazione: la foto di una pagina di libro, via OCR.
- Deduplica di due ricette linkate dallo stesso URL nello stesso ricettario.
- IaC versionata al posto di `fly.toml` e CLI, se l'ambiente smettesse di essere ricostruibile a mano.

## OUT-OF-SCOPE

- **Ingredienti strutturati in quantità e unità.** Poiché la normalizzazione fine è dichiarata non
  necessaria — la ricerca è semantica e chi legge interpreta il testo — nessuna riga paga il costo
  di un parser né di un modello di ingrediente. Il prezzo è che lista della spesa e scaling delle
  porzioni restano preclusi, e che introdurli dopo costerà una migrazione dei dati esistenti.
- **Review obbligatoria prima del salvataggio.** Poiché bloccare l'utente su un form a ogni aggiunta
  è dichiarato inaccettabile, l'aggiunta può salvare estrazioni imperfette. Il prezzo è che un
  ricettario contiene errori finché qualcuno non li corregge, e che la correzione deve perciò essere
  sempre a un clic — motivo per cui il form condiviso non è rimandabile.
- **Provider email nell'MVP.** Poiché non si invia nessuna email, spariscono password, hashing e
  flusso di reset. Il prezzo è la dipendenza da Google, l'esclusione di chi non ha un account
  Google, e un invito che l'invitante deve consegnare a mano perché nessuno lo spedisce per lui.
- **Vector DB dedicato.** Poiché la scala dichiarata è ≤10k ricette e centinaia per ricettario, i
  vettori stanno in Postgres con pgvector e si interrogano in transazione con i dati. Il prezzo è
  che oltre quella scala la ricerca va ripensata, non soltanto scalata.
- **Permessi per azione dentro un ricettario.** Poiché tutti i membri sono pari, nessuna riga porta
  controlli oltre alla membership. Il prezzo è che non si può invitare qualcuno in sola lettura, e
  che chiunque entri può cancellare quello che hanno scritto gli altri.
- **Deduplica delle ricette.** Poiché i duplicati sono dichiarati consentiti, nessuna riga paga una
  chiave di unicità né un confronto di similarità in scrittura. Il prezzo è che lo stesso link
  aggiunto da due membri produce due ricette, e che la ricerca le restituirà entrambe.

## Ordering criteria

1. **Il percorso minimo di consegna.** Repository e scheletro prima di ogni promessa, e separati:
   una CI verde non dice niente sull'ipotesi di hosting, e aprire account è lavoro umano con un modo
   di fallire diverso da un deploy che non si alza.
2. **Il rischio esistenziale e il differenziatore.** La ricerca semantica cross-lingua è il motivo
   per cui questo progetto non è Mealie: si misura per prima, su `S2`, su un corpus di prova, senza
   aspettare che esista un prodotto. Questo criterio perde una volta sola, contro il n. 5: la *riga*
   di ricerca `S7` segue tutti i produttori che alimentano gli embedding. Lo spike è ciò che compra
   l'anticipo che la riga non può prendersi.
3. **La correzione prima dello stato correggibile.** L'aggiunta non ha review: la prima riga che può
   salvare una ricetta imperfetta deve già saperla correggere. Per questo il form condiviso `S3`
   arriva prima dell'aggiunta da link `S4`, benché il link sia il caso più frequente — la frequenza
   (n. 6) perde qui.
4. **La catena di recupero dichiarata dalle sorgenti, prima che si apra un altro tema.** Le sorgenti
   dichiarano il fallback LLM il recupero automatico del path da link e il copia-incolla la sua via
   d'uscita manuale: `S5` e `S6` chiudono quel path prima che un altro tema si apra. È l'unica
   deroga a *breadth before depth* di questa mappa, e sta qui.
5. **Un solo proprietario per ogni pipeline condivisa.** La riga che apre una pipeline segue tutte
   le righe che la alimentano: `S7` segue le tre righe di cattura e il form, `S10` segue le righe
   che producono ricette e un `og:image`.
6. **La frequenza d'uso, e un esito sottile da ogni tema che resta.** Dopo i rischi esistenziali, un
   esito da ogni promessa prima di una seconda riga sulla stessa. Perde contro il n. 3 e il n. 4.
7. **L'identità appena l'evidenza lo consente.** `S8` è rimandata oltre la seconda riga d'uso perché
   l'evidenza che ancora manca — il tasso di successo della cascata di estrazione e il recall
   cross-lingua — si raccoglie su un unico proprietario implicito, e Auth.js non ne aggiunge un
   grammo. Appena `S7` ha misurato, l'accesso arriva: prima di `S9` che ne dipende, e prima di `S10`
   che non ne dipende.
8. **Dove finisce `NOW`.** Con la riga più piccola che mette il rilascio coerente in mano a famiglia
   e amici, `S11`, con la sola prontezza operativa che le sorgenti chiedono.

## Assumptions

- `S7` — "embedding mai a runtime sulle query di ricerca" e `similarity(embedding, embedding(query))`
  si contraddicono apertamente. Si legge che il **corpus** non viene mai ri-embeddato a query time,
  mentre la **stringa cercata** viene embeddata a ogni ricerca: una chiamata corta che le stesse
  sorgenti dichiarano irrilevante come costo. Se la lettura fosse sbagliata, la ricerca semantica
  come descritta non è implementabile.
- `S3`, `accesso` — Le righe da `S3` a `S7` girano su un unico proprietario implicito:
  `CurrentCookbook` restituisce un ricettario configurato, l'ambiente Fly non viene pubblicizzato, e
  `S8` sostituisce il resolver in quell'unico punto. Nessuna riga precedente va riscritta.
- `S5` — "output strutturato validato" si legge come `Schema` di Effect sul JSON del modello, con
  l'estrazione che fallisce e lo dice invece di salvare campi inventati.
- `S10` — Le sorgenti chiedono `og:image`/`schema.org` ricaricata su storage proprio, ma non dicono
  quante immagini una pagina possa dare: si legge **una sola** immagine di copertina per estrazione,
  e tutte le altre foto arrivano dall'utente.

## Open questions

- `ricerca`, `goal` — Se `S2` dicesse che nessun embedder multilingue dentro il budget regge il
  cross-lingua, il differenziatore cade e il progetto starebbe riscrivendo Mealie. Cosa si fa
  allora: si tira dentro la ricerca ibrida (oggi candidata), o si cambia meta? Questa risposta
  ridisegna la mappa, non una riga.
- `cattura` — Le sorgenti non dicono cosa succede quando l'estrazione riesce a metà: titolo sì,
  ingredienti no. Si salva comunque e si corregge dopo, o si dirotta sul copia-incolla? La risposta
  decide se `S6` è una via d'uscita o il ramo normale della cattura.
- `foto`, `cattura` — Le sorgenti mettono "Salvo foto" fra i passi dell'avanzamento dell'aggiunta da
  link, ma quella stessa foto è l'unica riga di un altro tema. Se la copertina automatica fosse
  parte del minimo dell'aggiunta, `S10` si scioglierebbe dentro `S4` e il tema `foto` sparirebbe.

## Cross-functional concerns

- **Authorization.** Ogni lettura e ogni scrittura sono scoped al ricettario corrente, risolto da un
  unico `CurrentCookbook`: è il seam dell'identità di questa mappa. Nasce in `S3` restituendo un
  ricettario configurato, e `S8` lo sostituisce con quello del membro autenticato in quel solo
  punto. Da `S9` la membership è l'unico controllo: nessun ruolo, `creatorId` a parte.
- **Validation and errors.** Errori tipizzati con `Data.TaggedError`, gestiti ai boundary con
  `catchTag`. L'output dell'LLM e le risposte HTTP si validano con `Schema`, mai castati. Nessun
  campo obbligatorio oltre al titolo; ingredienti e preparazione restano testo libero.
- **Operability.** L'estrazione è sincrona con timeout per passo, e l'avanzamento mostra solo i passi
  che la riga esegue davvero. Un passo fallito dice quale e perché — paywall, pagina irraggiungibile,
  JSON-LD assente, output fuori schema — mai un errore generico. Ogni chiamata a pagamento (LLM,
  embedding) viene loggata con il costo stimato.
- **Accessibility and security.** Nei form i campi obbligatori non portano l'asterisco e gli
  opzionali sono marcati "optional"; obbligatorietà esposta anche alle tecnologie assistive. Segreti
  solo in Fly secrets, mai nel repository. Il token d'invito è imprevedibile e revocabile. Nessun
  contenuto remoto servito per hotlink.
- **Data integrity and recovery.** `Recipe.embedding` è indice derivato, mai dato canonico: si
  rigenera a ogni salvataggio, e se la sua generazione fallisce la ricetta si salva comunque e resta
  invisibile alla sola ricerca. Una sola cover per ricetta. Duplicati consentiti per scelta.
  Cancellare una foto può lasciare un oggetto orfano su R2, mai un URL rotto nel DB.
- **Cost.** LLM ed embedding girano solo in fase di add e di edit, mai sul corpus a runtime. Il
  JSON-LD viene sempre tentato prima dell'LLM. Nessuna riga porta dentro un servizio che esca dal
  free tier senza dirlo qui.
