# S4 — Estrazione LLM per pagine senza structured data

← [Register](../roadmap.md#now)

**Outcome:** Quando la pagina linkata non ha JSON-LD, l'aggiunta non fallisce più: passa da sola
all'estrazione LLM; e quando la pagina non è nemmeno leggibile, si incolla il testo e si ottiene la
stessa ricetta.
**Requested by:** `arch-choices.md` § Estrazione contenuto (cascata JSON-LD → LLM); `goal.md` §
Visione, punto 3 (copia-incolla come fallback per paywall e siti JS-heavy); rimedio del fallimento
verificato in S3.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi sviluppa e chi prova il prodotto, sull'ambiente non pubblico. Dopo questa riga può salvare
ricette da siti che non pubblicano structured data, che sono quelli su cui Mealie si arrende.

## Includes

- Adapter verso il modello LLM scelto, con output strutturato validato da `Schema` — mai un cast — e
  timeout e retry decorati con `pipe`.
- Innesto sul ramo mancante della cascata di S3: JSON-LD assente, la pipeline prosegue sull'LLM come
  passo successivo della stessa barra di avanzamento.
- Pulizia del contenuto della pagina prima di darlo al modello, per non spendere token sul menu di
  navigazione.
- Secondo ingresso: un campo dove incollare il testo, che salta fetch e JSON-LD ed entra nella
  pipeline al passo di pulizia, riusando lo stesso motore e lo stesso schema di output.
- Errore tipizzato e messaggio proprio quando il modello risponde qualcosa che lo schema rifiuta, o
  quando risponde che nel testo non c'è una ricetta.

## Verification

- Un URL di una pagina senza JSON-LD, che in S3 falliva, produce una ricetta salvata con nome,
  ingredienti e preparazione riconoscibili; su una decina di pagine di questo tipo è scritto quante
  sono uscite corrette, quante parziali e quante sbagliate.
- Il testo di una pagina dietro paywall, incollato, produce la stessa ricetta che l'utente vede a
  schermo.
- Su un URL con JSON-LD valido nessuna chiamata al modello viene fatta: la cascata si ferma prima, e
  lo si vede dal conteggio delle chiamate.
- Quando il modello risponde fuori schema, la ricetta non viene salvata a metà e l'utente riceve un
  messaggio che dice che l'estrazione non è riuscita, non un errore di validazione.
- Il costo per ricetta estratta via LLM è misurato su quella decina di pagine ed è scritto, per il
  confronto con le "frazioni di cent" che `arch-choices.md` mette a bilancio.

## Learning target

Se un modello economico con output validato produce da HTML sporco ricette abbastanza buone da essere
salvate senza review, che è la scommessa su cui poggia il "nessun passo obbligatorio prima del
salvataggio".

## Excludes

- L'inserimento a mano: è di S8, insieme alla modifica, perché condivide con essa il form e non la
  pipeline.
- Le foto estratte dalla pagina: sono di S9.
- OCR e import da PDF o da foto: non sono chiesti da nessuna fonte.

## Open questions

- Quale modello, di quale fornitore? `arch-choices.md` chiede "un modello cheap, Haiku-class, con
  output strutturato validato" e non ne sceglie uno. La scelta cambia l'adapter e il costo per
  ricetta, non la forma della pipeline.
