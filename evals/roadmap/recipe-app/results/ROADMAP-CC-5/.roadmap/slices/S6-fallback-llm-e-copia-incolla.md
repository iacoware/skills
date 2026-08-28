# S6 — Fallback LLM e copia-incolla

← [Register](../roadmap.md#now)

**Outcome:** Le pagine che il JSON-LD non copre si aggiungono lo stesso — l'URL passa per l'LLM, e
quando neanche la pagina è leggibile si incolla il suo testo e si ottiene la stessa ricetta.

**Requested by:** `goal.md` (*Visione — Copia-incolla*, *Differenziatore*) e `arch-choices.md`
(*Estrazione contenuto — Fallback LLM*), sullo stesso motore che `concepts.md` descrive in
*Pipeline di estrazione*.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi prova l'app su staging: il vicolo cieco che S5 lascia sui siti senza dati strutturati e dietro
paywall si chiude, e non resta nessuna pagina da cui la ricetta vada ribattuta.

## Includes

- Una porta Effect `Extractor` con due adapter, JSON-LD e LLM, e un solo `Schema` di output
  condiviso: quello che S5 già persiste.
- Adapter LLM su un modello cheap con structured output, la cui risposta è validata con `Schema` e
  mai castata; una risposta che non soddisfa lo schema viene ritentata una volta e poi fallisce
  nominando lo stadio di lettura, senza salvare una ricetta parziale.
- Il percorso da URL cade sull'LLM quando il JSON-LD manca, e il progresso dice quale dei due
  adapter ha girato.
- Ingresso "incolla il testo" in Home: salta il JSON-LD, va sempre sull'LLM, e riusa lo stesso
  motore, lo stesso schema e lo stesso salvataggio del percorso da URL.
- Timeout e tetto di spesa per estrazione, e il modello dietro la porta perché resti sostituibile.
- `prepTime` e `tags` derivati dall'LLM quando li ricava, best-effort, mai chiesti a chi aggiunge.

## Verification

Una pagina JS-heavy senza JSON-LD, aggiunta per URL, produce una ricetta che una persona rilegge come
corretta. Il testo di una pagina dietro paywall, incollato, produce lo stesso risultato. Una risposta
del modello che viola lo schema — forzata in test — fa fallire l'aggiunta con il messaggio dello
stadio di lettura e non lascia niente nel database. Il costo in token per estrazione è misurato su
almeno cinque pagine reali e dichiarato accanto alle "frazioni di cent" che le fonti assumono: se è
di un ordine di grandezza diverso, il numero lo dice. Entrambi gli ingressi salvano attraversando lo
stesso codice che S5 ha scritto, verificato dal fatto che una modifica al salvataggio si vede da
tutti e tre gli ingressi.

## Learning target

Se un modello cheap con output strutturato validato trasforma il testo ripulito di una pagina
qualsiasi in una ricetta abbastanza buona da salvare senza revisione, e se lo fa al costo che le
fonti danno per scontato.

## Excludes

- Nessun OCR e nessun import da foto o PDF: l'ingresso resta testuale, e l'OCR è in `LATER`.
- Nessun passo di revisione prima del salvataggio: `OUT-OF-SCOPE`.
- Nessuna foto: è di S7.
- Nessun tetto di spesa per ricettario o per utente: è la domanda aperta della mappa, non una
  decisione presa qui.

## Open questions

- —
