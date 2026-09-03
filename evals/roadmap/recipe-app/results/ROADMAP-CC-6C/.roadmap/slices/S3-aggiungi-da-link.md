# S3 — Aggiungi una ricetta da link e correggila dopo

← [Register](../roadmap.md#now)

**Outcome:** Incolli l'URL di una ricetta, la vedi salvata nel ricettario corrente senza confermare
niente, e quello che l'estrazione ha sbagliato lo correggi con l'edit.

**Requested by:** `goal.md` §§ Home, Aggiunta ricetta; `concepts.md` §§ Recipe, Pipeline di
estrazione.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Gli sviluppatori e un tester sull'ambiente di staging di `S1`. È la prima riga che salva dati, e
gira su un ricettario configurato: non esiste ancora nessun login, quindi non esiste ancora
nessun utente finale.

## Includes

- Tabelle `Cookbook` (minima) e `Recipe` con `cookbookId`, `name`, `ingredients`, `steps`,
  `prepTime?`, `tags`, `sourceUrl?` ed `embedding`, e la loro migrazione Drizzle.
- Il resolver `currentCookbook`, unico punto che risolve lo scope, configurato su un ricettario
  seed: ogni lettura e ogni scrittura passa di lì.
- Form "aggiungi da link"; fetch della pagina con l'`HttpClient` di Effect; pulizia del contenuto;
  parse del JSON-LD `schema.org/Recipe` decodificato con `Schema`, mai castato.
- Scrittura dell'embedding nella stessa transazione del salvataggio, con il modello che `S2` ha
  scelto e con la dimensione di vettore che ha misurato.
- Progress sui passi che accadono davvero — `Scarico pagina → Leggo la ricetta → Salvo` — che si
  ferma sul passo fallito con un messaggio che lo nomina: fetch fallito, timeout, risposta non
  HTML, pagina senza JSON-LD.
- Elenco delle ricette del ricettario corrente e pagina di dettaglio.
- Form di edit con titolo, ingredienti e preparazione come testo libero, che rigenera l'embedding
  al salvataggio: è il percorso di correzione dichiarato, e arriva con la prima riga che può
  produrre una ricetta sbagliata.

## Verification

- Un URL di food blog con JSON-LD produce una ricetta salvata, visibile in elenco e in dettaglio,
  con nome, ingredienti e preparazione presi dalla pagina, e `sourceUrl` valorizzato.
- Fra estrazione e salvataggio non c'è nessun passo: la ricetta è in elenco senza che il tester
  confermi o corregga niente.
- La progress mostra i passi nell'ordine in cui accadono; su una pagina senza JSON-LD si ferma
  dicendo che nella pagina non c'è una ricetta leggibile, non con un errore generico.
- Un fetch in timeout o che risponde 403 non lascia niente sul database.
- Subito dopo il salvataggio la riga `Recipe` ha un embedding non nullo; dopo un edit del titolo
  l'embedding è cambiato.
- Con il resolver puntato su un secondo ricettario, l'elenco e il dettaglio non vedono la ricetta.
- Il costo dell'embedding per ricetta salvata è misurato e scritto.

## Learning target

Se la cascata "scarico, leggo il JSON-LD, salvo" produce ricette utilizzabili dai blog reali senza
chiedere niente all'utente, e se il salvataggio senza review regge una volta che la correzione è
disponibile subito dopo.

## Excludes

- Fallback LLM quando il JSON-LD manca: è di `S4`, e chiude il buco che questa riga apre.
- Copia-incolla del testo: è di `S9`. Inserimento a mano: è di `S10`.
- Foto e il passo "Salvo foto" nella progress: sono di `S8`, che possiede lo storage.
- Ricerca: è di `S5`. Login e ricettari reali: sono di `S6`.
- Cancellare una ricetta: candidato in `LATER`, nessuna fonte lo chiede.

## Open questions

- —
