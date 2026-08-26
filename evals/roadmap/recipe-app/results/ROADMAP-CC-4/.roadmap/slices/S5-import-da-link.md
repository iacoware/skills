# S5 — Aggiunta da link con JSON-LD e progress reale

← [Register](../roadmap.md#now)

**Outcome:** Incollato l'indirizzo di una pagina, la ricetta viene scaricata, letta dal
`schema.org/Recipe` e salvata subito, con i passi reali sotto gli occhi e un errore preciso
quando uno di essi non riesce.

**Requested by:** `goal.md` § Aggiunta ricetta (estrazione sincrona, progress sui passi
reali, nessuna review); `arch-choices.md` § Estrazione contenuto, primo gradino della
cascata; `concepts.md` § Pipeline di estrazione.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Sviluppatori e tester sull'ambiente di staging: possono aggiungere una ricetta incollando un
link invece di trascriverla, che è il caso che le fonti dichiarano più frequente.

## Includes

- Fetch della pagina con `HttpClient` di Effect: timeout, dimensione massima, redirect
  controllati, rifiuto degli indirizzi privati.
- Parsing del `JSON-LD schema.org/Recipe`: nome, ingredienti, preparazione, tag e tempo dove
  ci sono, immagine.
- Download dell'immagine dichiarata dalla pagina e ricarico sul nostro bucket attraverso la
  pipeline di `S4`, così che il link al sito d'origine non venga mai usato.
- Progresso trasmesso al client durante la stessa richiesta, sui passi realmente eseguiti:
  scarico pagina, leggo ricetta, trovo ingredienti, salvo foto.
- Errori tipizzati per passo, con messaggio che dice cosa è successo dove: pagina non
  raggiungibile, risposta non leggibile, nessuna ricetta nella pagina.
- Salvataggio senza review, con `sourceUrl` valorizzato, e atterraggio sulla ricetta aperta
  in modifica.

## Verification

Su tre food blog reali che espongono JSON-LD, la ricetta entra con nome, ingredienti e
preparazione riconoscibili e con la cover servita dal nostro bucket. Su una pagina senza
JSON-LD il flusso si ferma al passo "leggo ricetta" con un messaggio che dice esattamente
quello, e nessuna ricetta parziale resta salvata. Interrotta la rete verso il sito, il
messaggio nomina il passo "scarico pagina" e la banca dati resta pulita. Il progresso mostrato
corrisponde ai passi eseguiti: un passo lento resta acceso finché non termina, e nessun passo
si accende prima di essere iniziato. Il costo di questo percorso è zero chiamate a pagamento,
verificabile dal log.

## Learning target

Che un'estrazione sincrona con progresso reale stia dentro una sola richiesta su Fly senza
essere tagliata, e quanto spesso il solo JSON-LD basti sui siti che useremo davvero.

## Excludes

- Estrazione quando il JSON-LD manca: è di `S6`, che innesta il secondo ramo nella cascata
  aperta qui.
- Incollare il testo di una pagina: è di `S7`.
- Code, worker e riprese asincrone: fuori scope dichiarato.

## Open questions

- —
