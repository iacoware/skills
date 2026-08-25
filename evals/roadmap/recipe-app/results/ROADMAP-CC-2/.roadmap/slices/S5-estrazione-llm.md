# S5 — Estrazione LLM: link illeggibili e testo incollato

← [Register](../roadmap.md#now)

**Outcome:** Quando la pagina non espone `schema.org/Recipe`, l'estrazione ripiega da sola su un LLM
con output strutturato validato; e quando la pagina non si lascia nemmeno scaricare — paywall, sito
che monta tutto in JavaScript — si incolla il testo e finisce nello stesso motore e nello stesso
modello di ricetta.

**Requested by:** `arch-choices.md` (§ Estrazione contenuto, passi 2 e 3), `goal.md` (§ Visione,
modo 3: copia-incolla come fallback quando il link non è leggibile) e `concepts.md` (§ Pipeline di
estrazione: due ingressi, un solo motore).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi sviluppa e chi prova l'app sull'ambiente non pubblico. Dopo questa riga nessun sito è più un
vicolo cieco: o il link basta, o l'incollaggio del testo lo sostituisce, e in entrambi i casi non si
compila un form.

## Includes

- Pulizia del contenuto — HTML scaricato o testo incollato — in testo leggibile, riusata da entrambi
  gli ingressi.
- Adapter LLM con output strutturato, decodificato con `Schema` nello stesso modello di ricetta di
  S4: un output che non valida è un errore nominato e non una ricetta salvata a metà. Timeout,
  numero massimo di tentativi e limite alla dimensione dell'input espliciti.
- Ripiego automatico nel percorso da URL: quando il JSON-LD manca, si passa all'LLM senza chiedere
  nulla e l'avanzamento lo dice, nominando il passo.
- Un ingresso per il testo incollato nella home, che salta il JSON-LD e va sempre all'LLM.
- `tags` e `prepTime` chiesti all'LLM come best-effort: se non li produce, la ricetta si salva
  ugualmente.
- Salvataggio immediato senza review, come in S4.

## Verification

Su una lista dichiarata di URL privi di JSON-LD — presa dagli scarti misurati in S4 — l'aggiunta
produce una ricetta salvata, e per ciascuna si registra se titolo, ingredienti e preparazione sono
usabili senza correzione, giudicati da una persona che ha davanti la pagina: il conteggio è il
risultato. Incollando il testo di una pagina dietro paywall si ottiene lo stesso esito con lo stesso
modello di ricetta. Con un URL che espone il JSON-LD, il contatore delle chiamate del provider LLM
non si muove: il fallback è un fallback. Forzando l'LLM a restituire un oggetto che non rispetta lo
schema, il flusso si ferma con un messaggio che nomina il passo e non resta nessuna ricetta né
nessuna riga parziale. Il costo per ricetta estratta è misurato e scritto.

## Learning target

Un modello economico con output strutturato, su testo ripulito, produce una ricetta buona abbastanza
da essere salvata senza review — cioè il costo di un'estrazione imperfetta corretta dopo è davvero
minore di quello di un form da confermare a ogni aggiunta, come le fonti assumono.

## Excludes

- La foto presa dalla pagina: è di S8.
- L'embedding della ricetta: è di S6.
- OCR e foto di pagine di libro come quarto ingresso: è un candidato, non è chiesto dall'MVP.
- Qualunque confronto con le ricette già presenti: i duplicati sono consentiti per scelta dichiarata.

## Open questions

- **Quale modello e quale provider per l'estrazione.** `arch-choices.md` dice "modello cheap,
  Haiku-class, con output strutturato validato": è un aggettivo e una classe, non una scelta. Va
  scelto qui, con il criterio del costo per ricetta e della quota di estrazioni usabili senza
  correzione, misurati sulla stessa lista di URL della verifica.
