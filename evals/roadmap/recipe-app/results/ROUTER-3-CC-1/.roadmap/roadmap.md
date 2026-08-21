# Roadmap — Recipe App

**Goal:** Ricettari tematici pubblici che chiunque trova e legge senza account, e una ricerca che
attraversa tutto il corpus pubblico invece di un solo ricettario. La scoperta è il prodotto; il
ricettario privato resta una modalità.

**Sources:** `sources/goal.md`, `sources/concepts.md`, `sources/arch-choices.md`,
`sources/tech-choices.md`, e la nuova meta dichiarata dall'autore.

**Current state:** Consegnate `S0`–`S11`: repository e CI, scheletro su Fly con Neon, lo spike
sull'embedder, il ricettario corrente, la cattura da link con JSON-LD, il fallback LLM e il
copia-incolla, la ricerca semantica dentro il ricettario, l'accesso Google, i ricettari condivisi,
le foto su R2 e il rilascio a famiglia e amici. L'app privata è intera e non viene riaperta: questa
mappa la apre al pubblico. I due prerequisiti greenfield non si ridisegnano — stanno in `archive/` —
e il contatore degli id riparte da dove l'hanno lasciato. Dal ridisegno non è stata consegnata
nessuna riga. L'autore ha dichiarato la forma del corpus su cui la ricerca deve funzionare —
migliaia di ricette, ricettari che nessuno ha curato insieme — e il corpus è uscito da una riga di
`Includes` di `S13` per diventare `S17`.

## Themes

| Theme | Promise | First validator |
|---|---|---|
| `pubblico` | Rendi pubblico un ricettario tematico e chiunque, senza account, lo apre e lo legge — e puoi tornare indietro. | `S12` |
| `scoperta` | Cerchi con parole tue e trovi ricette in tutti i ricettari pubblici, anche scritte in un'altra lingua, senza account. | `S13` |
| `trovabilita` | Una ricetta pubblica si trova da fuori: un motore di ricerca la indicizza, e il link incollato mostra di cosa parla. | `S14` |

## NOW

| Id | Title | Theme | Kind | Size | Readiness | Executor | Depends on |
|---|---|---|---|---|---|---|---|
| S12 | [Ricettario pubblico, leggibile senza account](slices/S12-ricettario-pubblico.md) | pubblico | product | medium | needs-decision | agent | — |
| S17 | [Corpus di partenza: migliaia di ricette da ricettari non coordinati](slices/S17-corpus-di-partenza.md) | scoperta | enabler | medium | needs-decision | mixed | — |
| S13 | [Ricerca su tutto il corpus pubblico](slices/S13-ricerca-corpus-pubblico.md) | scoperta | product | medium | ready | agent | S12, S17 |
| S14 | [Pagine pubbliche indicizzabili e condivisibili](slices/S14-pagine-trovabili.md) | trovabilita | product | small | ready | mixed | S12 |
| S15 | [Vetrina dei ricettari pubblici](slices/S15-vetrina-pubblica.md) | scoperta | product | small | ready | agent | S12 |
| S16 | [Rilascio pubblico](slices/S16-rilascio-pubblico.md) | — | release | medium | needs-decision | mixed | S13 |

## LATER

- Filtri strutturati per tag e tempo, e ricerca ibrida semantica più full-text: più attraenti su un
  corpus grande di quanto fossero dentro un ricettario, non necessarie per arrivarci.
- Ricerca che attraversa tutti i ricettari di cui si è membri: è un'altra cosa dalla ricerca sul
  corpus pubblico, e nessuna delle due porta l'altra.
- Un concetto di gruppo sopra i ricettari, se ri-invitare in ognuno diventasse fastidioso.
- Ruoli e permessi dentro un ricettario, oltre al solo `creatorId`.
- Passkeys come secondo metodo d'accesso, quando il recupero da dispositivo perso sarà risolto.
- Import da file esportati da altre app di ricette.
- Un quarto ingresso di estrazione: la foto di una pagina di libro, via OCR.
- Deduplica di due ricette linkate dallo stesso URL: in un corpus non coordinato è il caso normale, e
  la promuove il numero dichiarato sui primi dieci risultati della ricerca pubblica, non il gusto.
- IaC versionata al posto di `fly.toml` e CLI, se l'ambiente smettesse di essere ricostruibile a
  mano.
- Coda di moderazione e segnalazione del contenuto pubblico, sopra la sola via d'uscita che è
  togliere dal pubblico.
- Salvare nel proprio ricettario una ricetta trovata in pubblico.
- Profilo pubblico di chi pubblica, e classificazione automatica dei temi.

## OUT-OF-SCOPE

- **Ingredienti strutturati in quantità e unità.** Poiché la normalizzazione fine è dichiarata non
  necessaria — la ricerca è semantica e chi legge interpreta il testo — nessuna riga paga il costo di
  un parser né di un modello di ingrediente. Il prezzo è che lista della spesa e scaling delle
  porzioni restano preclusi, e che introdurli dopo costerà una migrazione dei dati esistenti.
- **Review obbligatoria prima del salvataggio.** Poiché bloccare l'utente su un form a ogni aggiunta
  è dichiarato inaccettabile, l'aggiunta può salvare estrazioni imperfette. Il prezzo era un
  ricettario con qualche errore dentro casa; adesso è che un'estrazione imperfetta può diventare
  leggibile da chiunque, e l'unico argine è che pubblicare resta un atto deliberato e reversibile.
- **Provider email.** Poiché non si invia nessuna email, spariscono password, hashing e flusso di
  reset, e chi legge non ha bisogno di niente. Il prezzo è la dipendenza da Google per chi scrive,
  un invito che l'invitante consegna a mano, e nessun canale per raggiungere un lettore o per
  ricevere da lui una segnalazione.
- **Vector DB dedicato.** Poiché la scala dichiarata resta quella delle sorgenti, i vettori stanno in
  Postgres con pgvector e si interrogano in transazione con i dati. Il prezzo è che oltre quella
  scala la ricerca va ripensata e non soltanto scalata, e adesso quel conto lo presenta la scoperta,
  che è il prodotto.
- **Permessi per azione dentro un ricettario.** Poiché tutti i membri sono pari, nessuna riga porta
  controlli oltre alla membership, e la lettura pubblica è una visibilità del ricettario, non un
  ruolo. Il prezzo è che non si invita nessuno in sola lettura, e che non si pubblica una singola
  ricetta senza pubblicare il ricettario che la contiene.
- **Deduplica delle ricette.** Poiché i duplicati sono dichiarati consentiti, nessuna riga paga una
  chiave di unicità né un confronto di similarità in scrittura. Il prezzo è cresciuto: lo stesso link
  pubblicato in due ricettari pubblici esce due volte nei risultati, e i risultati sono il prodotto.
- **Contributi da chi legge senza account.** Poiché leggere non costa un account, non c'è nessuno a
  cui attaccare un commento, un voto o una correzione. Il prezzo è che la scoperta non ha nessun
  segnale sociale con cui ordinare, e deve reggersi sulla sola somiglianza semantica.

## Ordering criteria

1. **La piattaforma c'è già.** Nessun prerequisito da ridisegnare: repository, scheletro, datastore,
   storage e identità sono consegnati, quindi la prima riga di questa mappa è già una promessa e non
   un enabler.
2. **Il confine di visibilità prima di tutto ciò che lo sfrutta.** Il rischio esistenziale di questa
   mappa non è il recall, è la fuga: una ricetta privata letta da un anonimo non si recupera dopo.
   `S12` possiede quel confine da solo, e ogni riga che segue lo consuma senza riaprirlo.
3. **Il differenziatore, che ora si misura su un corpus e non su un ricettario.** Perde una volta
   sola, contro il n. 2: la ricerca su tutto il pubblico non è misurabile finché il pubblico non
   esiste, e nessun input controllato può sostituirlo senza aggirare proprio l'autorizzazione in
   prova.
4. **Il corpus prima della misura sul corpus.** Un banco di prova che costa una riga di `Includes`
   sta dentro la riga che lo usa; questo costa migliaia di estrazioni, un conto una tantum e
   un'esposizione, e soprattutto potrebbe spiegare da solo un recall deludente. `S17` lo costruisce e
   `S13` lo misura, così un numero brutto dice quale delle due decisioni riaprire. Non è una deroga
   alla breadth: un enabler precede il suo validatore e non valida nessun tema.
5. **Il rimedio nasce con lo stato che lo rende necessario.** Togliere dal pubblico non è una riga
   successiva né un'aggiunta operativa: sta dentro `S12`, la riga che sa pubblicare.
6. **Un solo proprietario per confine condiviso.** `S14` aggiunge metadati alla pagina pubblica e non
   riapre mai l'autorizzazione stabilita da `S12`; `S13` applica la visibilità dentro la query e non
   ne inventa una seconda.
7. **Un esito sottile da ogni tema prima del secondo sullo stesso tema.** `S12`, `S13` e `S14`
   aprono i tre temi, e solo dopo `S15` torna sulla scoperta. Questa mappa non deroga.
8. **Dove finisce `NOW`.** Con la riga di rilascio più piccola che regge traffico anonimo e crawler a
   un costo dichiarato: `S16`.

## Assumptions

- `pubblico` — Pubblico è il **ricettario**, non la singola ricetta: `Cookbook.visibility`, che `S8`
  ha già portato con il solo valore privato. Tematico significa che chi pubblica lo dichiara nel nome
  e in una descrizione; il sistema non classifica niente da sé.
- `S12` — Nessuna riga consegnata va riscritta: la lettura pubblica si aggiunge come seconda autorità
  accanto alla membership dentro il punto che già risolve lo scope, e la modalità privata resta
  letteralmente il codice di prima. Se questa lettura cade, `S12` è molto più grande di come è
  dimensionata qui.
- `trovabilita` — "Chiunque li trova" si legge come includere l'arrivo da un motore di ricerca
  esterno, non soltanto la ricerca dentro l'app. È l'unica cosa che giustifica il tema: se la lettura
  è sbagliata, `S14` cade e il tema con lei.
- `scoperta` — L'ordine di grandezza non è più un'assunzione: l'autore dichiara migliaia di ricette,
  sotto il ≤10k delle sorgenti. Resta assunto che pgvector con HNSW regga quel volume con il filtro
  di visibilità dentro la query, e `S13` è la riga che lo può smentire; l'esclusione del vector DB
  dedicato sta in piedi su questo.
- `scoperta`, `S17` — Si assume di riuscire a costruire un corpus davvero non coordinato invece di
  uno che, scegliendolo noi, risulta ordinato. Se ci riesce solo ordinato, la misura di `S13` si
  autoassolve e il suo learning target non è raggiunto.
- `scoperta` — I duplicati restano consentiti, ma non sono più un caso di bordo: in un corpus che
  nessuno ha coordinato lo stesso piatto catturato da fonti popolari è la norma, non l'eccezione. Si
  assume che i risultati restino utili lo stesso; `S13` conta quanta parte dei primi dieci se ne va,
  ed è quel numero a decidere della candidata deduplica.

## Open questions

- `pubblico`, `trovabilita` — Ripubblicazione del materiale estratto. La riga delle foto scarica
  l'immagine indicata dalla pagina d'origine e la riserve dal nostro dominio: dentro un ricettario di
  famiglia era una cache privata, in pubblico è ripubblicazione di materiale altrui, e lo stesso vale
  per il testo estratto. La pagina pubblica mostra solo le foto caricate dagli utenti, o anche quella
  estratta? Nessuna sorgente parla di licenze perché nessuna sorgente prevedeva il pubblico. La
  risposta cambia cosa mostrano `S12` e `S14`, e quanto vale il tema `trovabilita`: un'anteprima
  senza immagine è un'anteprima povera. Adesso la stessa domanda decide anche se `S17` si fa:
  costruire migliaia di ricette estratte ha senso solo se possono diventare pubbliche.
- `goal` — Chi ha il diritto di pubblicare. Qualunque membro rende pubblico un ricettario, o la
  pubblicazione passa da qualcuno? Se la scoperta è il prodotto, la qualità del corpus è il prodotto,
  e la risposta decide se esiste una riga di curatela che questa mappa oggi non ha. `S17` la rende
  concreta: se il corpus di partenza lo pubblichiamo noi, il primo editore del corpus siamo noi.

## Cross-functional concerns

- **Authorization.** L'invariante precedente — ogni lettura e ogni scrittura scoped al ricettario
  corrente — è sollevata per le sole letture, e in chiaro. Da qui le autorità sono due: la membership
  (privato, invariata) e `visibility=public` (lettura anonima). Un solo punto nominato risolve
  l'autorità di lettura, e ogni scrittura resta membership, sempre. Il prezzo del sollevamento: il
  seam nato in `S3` e chiuso in `S8` smette di essere l'unica strada, e ogni percorso di lettura va
  verificato due volte, da membro e da anonimo, perché un errore qui non è un difetto, è una fuga.
- **Validation and errors.** Errori tipizzati con `Data.TaggedError`, gestiti ai boundary con
  `catchTag`. L'output dell'LLM e le risposte HTTP si validano con `Schema`, mai castati. Nessun
  campo obbligatorio oltre al titolo; ingredienti e preparazione restano testo libero.
- **Operability.** Ogni chiamata a pagamento viene loggata con il costo stimato. La ricerca anonima è
  una chiamata a pagamento innescata da chi non ha un account: è limitata per frequenza, e il limite
  è verificato dalla prima riga che la espone. Il traffico dei crawler è traffico e si misura come
  tale. Un passo fallito dice quale e perché, mai un errore generico.
- **Accessibility and security.** Nei form i campi obbligatori non portano l'asterisco e gli
  opzionali sono marcati "optional". Segreti solo in Fly secrets. Il token d'invito è imprevedibile e
  revocabile. Una pagina pubblica non espone mai un dato personale di un membro, l'email per prima.
- **Data integrity and recovery.** `Recipe.embedding` è indice derivato, mai dato canonico: se la sua
  generazione fallisce la ricetta si salva comunque e resta invisibile alla sola ricerca. Una sola
  cover per ricetta. Duplicati consentiti per scelta. Togliere dal pubblico è immediato e si propaga
  a cache, sitemap e risultati di ricerca entro una finestra dichiarata.
- **Cost.** LLM ed embedding girano in fase di add e di edit, mai sul corpus a runtime; l'unica
  chiamata a runtime è l'embedding della stringa cercata. Fra il corpus e la fattura stanno un limite
  di frequenza e un tetto imposto dal provider. Nessuna riga porta dentro un servizio che esca dal
  free tier senza dirlo qui. Il costo una tantum di costruire il corpus è di `S17`, dichiarato prima
  di spenderlo, e il volume delle foto è misurato contro il free tier di R2, che a migliaia di
  ricette è la voce che può saltare per prima.
