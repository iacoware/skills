# S3 — Ricetta a mano: elenco, scrittura, correzione

← [Register](../roadmap.md#now)

**Outcome:** Sull'ambiente non pubblico si scrive una ricetta a mano, la si vede nell'elenco, la si
riapre e la si corregge; tutto quello che si legge e si scrive è già confinato a un ricettario da un
unico risolutore di scope.

**Requested by:** `goal.md` (§ Aggiunta ricetta: "stesso form per edit e inserimento manuale";
§ Home: elenco) e `concepts.md` (§ Entità principali: `Recipe`, `Cookbook`).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi sviluppa e chi prova l'app sull'ambiente non pubblico di S1. Dopo questa riga può mettere dentro
una ricetta che conosce e ritrovarla, e soprattutto può correggere una ricetta sbagliata — che è la
condizione per cui S4 può permettersi di salvare senza review.

## Includes

- Schema Drizzle e migration per `Cookbook` (id, nome, `visibility` con il solo valore privato) e
  `Recipe` (id, `cookbookId`, nome, ingredienti, preparazione, `prepTime` e `tags` opzionali,
  `sourceUrl` opzionale), con gli ingredienti e la preparazione come testo libero.
- Un risolutore unico del ricettario corrente, che in questa riga legge l'id da una variabile
  d'ambiente: è il seam che S7 sostituirà in quel solo punto. Nessuna query di dominio riceve
  `cookbookId` da fuori.
- Elenco delle ricette del ricettario corrente, e pagina di lettura di una ricetta.
- Un solo form, usato per creare a mano (campi vuoti) e per correggere (campi pieni): nessun campo
  marcato con l'asterisco, gli opzionali marcati "optional", `required` nativo dove serve.
- La logica applicativa in Effect secondo le convenzioni di progetto: porta come `Context.Tag`,
  adapter come `Layer`, errori attesi come `Data.TaggedError`, payload del form decodificati con
  `Schema`.

## Verification

Sull'URL di S1 si crea una ricetta col form vuoto, la si trova nell'elenco, la si apre, la si
modifica e dopo un ricaricamento la modifica è persistita. Un salvataggio con il titolo vuoto viene
rifiutato con un messaggio, non con un errore generico, e non lascia righe. Cambiando l'id di
ricettario configurato e riavviando, l'elenco è vuoto e l'URL di una ricetta dell'altro ricettario
risponde come per una ricetta inesistente: lo scope non è un filtro dell'interfaccia, è nella query.
Il diff mostra che nessuna query di dominio costruisce `cookbookId` da sé.

## Learning target

Il modello di ricetta deliberatamente povero — titolo, ingredienti e preparazione come testo libero,
niente ingrediente strutturato, niente step — basta per scrivere e ritrovare una ricetta vera; e il
seam di scope regge senza autenticazione, cioè quando S7 sostituirà lo scope configurato con quello
della sessione non ci sarà dominio da riscrivere.

## Excludes

- Autenticazione, utenti, `Membership` e creazione di ricettari: sono di S7 e S9. Qui il ricettario è
  uno solo, configurato, e il pubblico dichiarato è chi sviluppa e chi prova.
- Le foto: sono di S8, che possiede l'object storage dopo tutti i percorsi che lo alimentano.
- L'embedding e la ricerca: sono di S6, che possiede la generazione per tutti e tre i percorsi di
  aggiunta. Fino ad allora le ricette esistono senza indice, e S6 le riempirà.

## Open questions

- —
