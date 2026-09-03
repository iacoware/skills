# S4 — Estrazione LLM quando il JSON-LD manca

← [Register](../roadmap.md#now)

**Outcome:** Un URL senza dati strutturati non fallisce più: il contenuto ripulito va a un LLM
economico che restituisce la ricetta nello stesso schema, e la ricetta entra nel ricettario.

**Requested by:** `sources/arch-choices.md` § Estrazione contenuto — cascata "JSON-LD prima,
LLM in fallback"; rimedio del fallimento dichiarato in `S3`.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi prova l'app sull'ambiente non di produzione: aggiunge da URL di siti che non pubblicano
`schema.org/Recipe` e ottiene comunque la ricetta, dove prima vedeva un errore.

## Includes

- Pulizia del contenuto della pagina prima della chiamata: via navigazione, script e boilerplate,
  con un tetto alla lunghezza del testo inviato.
- Chiamata a un LLM economico con output strutturato, validato con Schema sullo stesso schema
  `Recipe` del ramo JSON-LD — mai un cast. Il modello e il provider sono un solo punto di
  configurazione, deciso dalla domanda aperta qui sotto.
- Il fallback scatta solo quando il JSON-LD manca o non è conforme: una pagina che ce l'ha non
  paga nessuna chiamata.
- Passo dedicato nella progress bar, distinto da quello del parse diretto, e un errore tipizzato
  per output fuori schema e per timeout del modello.
- `prepTime` e `tags` popolati best-effort quando il modello li produce, mai richiesti e mai
  bloccanti.

## Verification

- Un URL di una pagina senza JSON-LD produce una ricetta con nome, ingredienti e preparazione
  fedeli alla pagina, ed è dichiarato su quante pagine del campione di `S3` il risultato regge.
- Un URL con JSON-LD non genera nessuna chiamata al modello, dimostrato dal log delle chiamate.
- Una risposta del modello fuori schema non salva niente e produce il messaggio del suo passo.
- È dichiarato il costo medio per ricetta estratta via modello.
- Il tempo totale dell'aggiunta con fallback resta dentro la singola richiesta sincrona.

## Learning target

Che un modello economico estragga una ricetta usabile da una pagina qualsiasi a frazioni di
cent — se costo, latenza o fedeltà non reggono, la cascata delle fonti non copre i siti che il
JSON-LD lascia fuori e la promessa dell'import da link si restringe.

## Excludes

- Il testo incollato a mano: `S5`, che riusa questo stesso motore.
- Le pagine irraggiungibili — paywall, siti JS-heavy: nessuna pulizia le recupera, il rimedio
  è `S5`.
- La correzione di un'estrazione imprecisa: `S9`.

## Open questions

- Quale modello economico e quale provider: le fonti dicono "cheap, Haiku-class" senza
  sceglierne uno. La decisione fissa costo per ricetta, SDK e forma dell'output strutturato.
