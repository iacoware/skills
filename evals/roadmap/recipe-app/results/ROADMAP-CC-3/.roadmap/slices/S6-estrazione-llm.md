# S6 — Estrazione LLM per link senza JSON-LD e testo incollato

← [Register](../roadmap.md#now)

**Outcome:** Quando la pagina non ha dati strutturati, e quando il link non si legge affatto e si
incolla il testo a mano, la ricetta viene comunque estratta e salvata dallo stesso motore.

**Requested by:** `sources/goal.md` § Visione, punto 3, che dichiara il copia-incolla il fallback
per paywall e siti JS-heavy; `sources/arch-choices.md` § Estrazione contenuto, secondo e terzo
gradino della cascata; `sources/concepts.md` § Pipeline di estrazione, che pretende un solo motore
per due ingressi.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi sviluppa e chi collauda, sull'ambiente di staging non pubblico. Dopo questa riga nessun sito
resta fuori: se il link non si legge, si incolla il testo.

## Includes

- Porta `Context.Tag` per l'estrattore LLM e layer adapter che la implementa, così che il modello
  sia sostituibile senza toccare la pipeline.
- Pulizia del contenuto prima della chiamata, uguale per i due ingressi.
- Output strutturato validato con `Schema`, mai un cast, con errore tipizzato quando non valida;
  timeout e un numero finito di ritentativi.
- Il gradino mancante della cascata sul percorso da link: quando il JSON-LD non c'è, si chiama
  l'LLM invece di fallire.
- Area «incolla il testo» nella home, che salta il JSON-LD e va sempre all'LLM.
- Derivazione best-effort di tempo e tag anche da questo ramo, e gli stessi passi di progresso
  reale del percorso da link.
- Costo e latenza di ogni chiamata a pagamento in log strutturato.

## Verification

Una pagina senza JSON-LD che prima si fermava con «nessuna ricetta strutturata trovata» ora produce
una ricetta salvata. Lo stesso contenuto incollato come testo produce una ricetta equivalente. Su
un campione dichiarato di pagine sono registrate la quota di output che non supera la validazione
`Schema` e il costo medio per ricetta, e si confronta con le frazioni di cent che le sorgenti danno
per scontate. Un output non valido non salva nulla di parziale e l'utente legge quale passo è
fallito. Una ricetta estratta male si corregge con il form che esiste già, senza passaggi in più.

## Learning target

Che un modello di classe Haiku con output validato produca ricette utilizzabili sia da HTML
ripulito sia da testo incollato abbastanza spesso da rendere accettabile il salvataggio senza
review — e a quale costo per ricetta, che è l'unica voce variabile del budget dichiarato.

## Excludes

- OCR e import da foto o PDF: nessuna sorgente li chiede, e il copia-incolla è il fallback
  dichiarato.
- Ogni review obbligatoria prima del salvataggio.
- Le foto, che restano alla riga che apre l'object storage.

## Open questions

- —
