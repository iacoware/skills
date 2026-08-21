# S17 — Corpus pubblico alla scala dichiarata

← [Register](../roadmap.md#now)

**Outcome:** Migliaia di ricette stanno in ricettari pubblici veri, catturate senza che nessuno stia
a guardare, e il conto di averle catturate è dichiarato voce per voce.

**Requested by:** La scala dichiarata dall'autore (migliaia di ricette, in ricettari che nessuno ha
messo insieme), `sources/arch-choices.md` (Estrazione contenuto — costo del fallback; Riepilogo
costi). Split da `S13`, che portava il seed in una riga di `Includes` scritta quando il corpus era
piccolo.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi sviluppa: ha finalmente un corpus su cui la misura di `S13` significa qualcosa, invece di tre
ricettari che non mettono in gara niente.

## Includes

- Un'esecuzione non presidiata del motore di estrazione già consegnato: nessun avanzamento sincrono,
  nessuno che guarda, e una ripresa che riparte da dove si era fermata.
- I ricettari pubblici in cui il corpus atterra, dichiarati uno per uno con la loro provenienza.
- Il conto: quante ricette sono passate dal JSON-LD gratis e quante dal fallback a pagamento, e il
  totale contro il preventivo delle sorgenti.
- Il rifiuto di una pagina che non dà una ricetta leggibile, contato e non nascosto: il corpus con
  dentro quello che ci è finito è il corpus su cui `S13` misurerà.

## Verification

Al termine il numero di ricette pubbliche è dichiarato e sta nell'ordine di grandezza dichiarato
dall'autore. La corsa viene interrotta a metà e ripresa: non duplica ciò che aveva già salvato e non
ripaga il fallback su quelle ricette. Il costo è dichiarato voce per voce — chiamate LLM, embedding,
traffico — contro il preventivo di `arch-choices.md`, e la riga dice se lo sfonda e su quale voce.
La distribuzione delle ricette per ricettario d'origine e per lingua è dichiarata: se il corpus è per
il 90% in una lingua sola, `S13` misura una cosa diversa da quella che promette. Quante estrazioni
sono state rifiutate e quante sono passate con campi vuoti è un numero scritto, non un'impressione.

## Learning target

Se un corpus della scala dichiarata si può costruire con il motore consegnato e dentro il budget
dichiarato, o se la scoperta costa il suo corpus prima ancora di costare le sue ricerche.

## Excludes

- La misura del recall e la ricerca: sono di `S13`, che consuma questo corpus e non lo costruisce.
- La curatela e la moderazione di cosa merita starci: restano fuori; questa riga dichiara la
  provenienza, non la giudica.
- Un ingresso di importazione per gli utenti: non richiesto, e questa corsa non è un prodotto.
- La deduplica: esclusa dalla mappa, e qui il prezzo si vede per la prima volta.

## Open questions

- Da dove vengono le migliaia di ricette e in quali ricettari pubblici atterrano: le raccogliamo noi
  da fonti che scegliamo noi, o si aspetta che le pubblichino persone vere? Se le raccogliamo noi, il
  corpus l'abbiamo messo insieme noi — che è esattamente la condizione che l'input dice di non
  volere. La scelta è dell'autore e blocca questa riga.
- Vale anche qui la domanda aperta di mappa sulla ripubblicazione: catturare migliaia di pagine
  altrui dentro ricettari pubblici è la stessa domanda di `S12`, a una scala che la rende difficile
  da ignorare.
