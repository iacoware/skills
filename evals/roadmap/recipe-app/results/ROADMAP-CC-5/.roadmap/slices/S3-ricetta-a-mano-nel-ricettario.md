# S3 — Ricetta a mano nel ricettario

← [Register](../roadmap.md#now)

**Outcome:** Su staging si scrive una ricetta a mano nel ricettario corrente, la si vede
nell'elenco, la si riapre e la si corregge con lo stesso form.

**Requested by:** `goal.md` (*Cosa fa (MVP) — Home*, *Aggiunta ricetta*) e `concepts.md`
(*Entità principali — Cookbook, Recipe*, *Modello di condivisione*).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi sviluppa e chi prova l'app sull'ambiente di staging non pubblico: non esiste ancora accesso, e
il ricettario corrente è quello configurato. Dopo questa riga possono tenere ricette vere dentro
l'app invece che altrove.

## Includes

- Schema Drizzle e migrazione per `Cookbook` (con `creatorId` nullo finché non esistono utenti) e
  `Recipe` (`name`, `ingredients`, `steps`, `prepTime` opzionale, `tags`, `sourceUrl` opzionale),
  con `Recipe.cookbookId` non nullo e vincolo di chiave esterna.
- Un unico resolver `CurrentCookbook`, definito come `Context.Tag`, che possiede lo scope; in questa
  riga il suo `Layer` lo risolve da configurazione a un ricettario seminato dalla migrazione. È il
  punto che S8 sostituirà.
- Ogni lettura e ogni scrittura di `Recipe` passa dallo scope: nessuna query senza `cookbookId`.
- Home con l'elenco delle ricette del ricettario corrente e l'ingresso "aggiungi a mano".
- Un solo form, usato sia per scrivere una ricetta nuova sia per correggerne una esistente:
  ingredienti e preparazione come testo libero, nessun parsing di quantità e unità, solo il titolo
  obbligatorio, i campi facoltativi marcati come tali.
- Salvataggio riuscito con tutto vuoto tranne il titolo.

## Verification

Una ricetta scritta a mano compare nell'elenco e riaperta mostra lo stesso testo, righe di
ingredienti comprese. Una ricetta salvata con il solo titolo si salva e si riapre. Cambiando in
configurazione il ricettario corrente, l'elenco e la lettura di una singola ricetta non restituiscono
nulla del primo ricettario, e la ricetta del primo non è raggiungibile neanche chiedendola per id.
Un inserimento di `Recipe` senza `cookbookId` viene rifiutato dal database. Una ricerca nel codice
non trova query su `Recipe` che non passino dal resolver.

## Learning target

Se un solo resolver può possedere ogni lettura e ogni scrittura di ricetta fin dalla prima riga che
persiste dati, in modo che S8 possa scambiare il ricettario configurato con quello dell'utente
autenticato cambiando un adapter e nessun punto di query.

## Excludes

- Nessuna foto: sono di S7.
- Nessuna estrazione da link o da testo: sono di S5 e S6.
- Nessuna ricerca: è di S4; l'elenco è in ordine di inserimento.
- Nessun accesso, nessun utente, nessuna creazione di ricettari dall'interfaccia: sono di S8.
- `prepTime` e `tags` esistono come colonne ma restano vuoti: nessuna fonte li chiede all'utente, e
  chi li deriva sono S5 e S6.

## Open questions

- —
