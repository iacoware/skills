# S4 — Fallback LLM quando la pagina non ha JSON-LD

← [Register](../roadmap.md#now)

**Outcome:** Le pagine senza structured data smettono di fallire: un modello cheap ne estrae la
ricetta con output validato, e sappiamo quanto costa e quanto è affidabile.

**Requested by:** `arch-choices.md` § Estrazione contenuto, che dichiara la cascata JSON-LD →
LLM; è il rimedio del fallimento che `S3` mette in `Verification`.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Gli sviluppatori e un tester sullo staging: aggiungendo il link di un sito senza JSON-LD ottengono
comunque una ricetta salvata invece di un errore.

## Includes

- Adapter LLM dietro un `Context.Tag` con layer separato, su `claude-haiku-4-5` con output
  strutturato.
- Prompt che riceve il contenuto già ripulito da `S3` e restituisce nome, ingredienti,
  preparazione, tag e tempo.
- Output decodificato con `Schema` e mai castato: quello che non passa non viene salvato.
- Innesto nella cascata subito dopo il tentativo JSON-LD, dentro il passo di progress "Leggo la
  ricetta", che dice quale delle due strade ha preso.
- Errori tipizzati per output non conforme, timeout e rate limit, con `catchTag` al boundary.
- Token e costo registrati per ogni chiamata.

## Verification

- Su almeno 10 pagine reali senza JSON-LD si può dire quante producono una ricetta salvabile senza
  correzioni strutturali, e quali campi mancano nelle altre.
- Un output che non passa lo `Schema` produce un errore che nomina il passo, e non lascia sul
  database nessuna ricetta parziale.
- Una pagina con JSON-LD non chiama l'LLM: il costo registrato per quell'aggiunta è zero.
- Il costo medio per ricetta estratta con LLM è misurato e confrontato con "frazioni di cent" di
  `arch-choices.md`.
- Un timeout del modello lascia l'utente con un messaggio che gli propone di riprovare, non con una
  progress ferma.

## Learning target

Se un modello Haiku-class con output strutturato estrae ricette utilizzabili dal testo di una
pagina qualunque a frazioni di cent, e se con quella qualità il salvataggio senza review resta una
scelta difendibile.

## Excludes

- Copia-incolla del testo: è di `S9`, e riusa questo motore così com'è.
- OCR e import da PDF: candidati in `LATER`.
- Traduzione della ricetta: esclusa, la ricerca è cross-lingua senza tradurre.

## Open questions

- —
