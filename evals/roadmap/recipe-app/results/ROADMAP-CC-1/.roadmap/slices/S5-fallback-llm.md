# S5 — Fallback LLM quando il JSON-LD manca

← [Register](../roadmap.md#now)

**Outcome:** Quando il JSON-LD non c'è, la pagina pulita passa a un modello economico con output
strutturato e la ricetta si salva lo stesso.

**Requested by:** `sources/arch-choices.md` (Estrazione contenuto — fallback LLM),
`sources/concepts.md` (Pipeline di estrazione), `sources/tech-choices.md` (Schema per validare
l'output dell'estrazione LLM).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi prova l'app sull'ambiente non pubblico: incolla il link di un sito che non espone structured
data e ottiene lo stesso risultato di prima, senza sapere che dietro è cambiato il motore.

## Includes

- La porta `RecipeExtractor` come `Context.Tag`, con l'adapter del modello dietro un `Layer`.
- Lo stesso schema di output del path JSON-LD, validato con `Schema`.
- Il passo aggiunto all'avanzamento, distinto da quello del JSON-LD.
- Log di ogni chiamata con il costo stimato, e un timeout oltre il quale il passo fallisce e lo dice.
- La riga è scritta per non anticipare la scelta del modello: nessun vendor compare nell'interfaccia,
  e l'adapter è sostituibile senza toccare la pipeline.

## Verification

Su un elenco dichiarato di pagine prive di structured data la ricetta si salva con titolo,
ingredienti e preparazione leggibili, e il risultato è confrontabile con quello che la stessa pagina
darebbe via JSON-LD dove entrambi esistono. Un output fuori schema fa fallire l'estrazione con un
messaggio, mai un salvataggio di campi inventati. Il costo medio per ricetta è dichiarato e sta nelle
frazioni di cent che le sorgenti mettono a budget. Il JSON-LD viene sempre tentato per primo: un
contatore lo dimostra.

## Learning target

Se un modello di quella fascia di prezzo estrae abbastanza bene da giustificare l'assenza di una
review obbligatoria.

## Excludes

- Testo incollato dall'utente: è di `S6`, che riusa questo stesso motore.
- Il modello e il provider non sono scelti qui: la riga non ne dipende e non ne anticipa nessuno.

## Open questions

- Quale modello e quale provider, dentro la fascia di prezzo che le sorgenti indicano. Le sorgenti
  danno una classe, non una scelta, e la scelta è dell'autore.
