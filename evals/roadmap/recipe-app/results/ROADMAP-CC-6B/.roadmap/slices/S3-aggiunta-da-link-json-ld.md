# S3 — Aggiunta da link con JSON-LD e elenco del ricettario

← [Register](../roadmap.md#now)

**Outcome:** Incollo l'URL di una ricetta, guardo i passi reali dell'estrazione scorrere, e la
ricetta compare nell'elenco del ricettario senza che io abbia compilato niente.

**Requested by:** `sources/goal.md` § Cosa fa (MVP) — Home e Aggiunta ricetta;
`sources/concepts.md` § Pipeline di estrazione, ramo JSON-LD.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi sviluppa e chi prova l'app sull'ambiente non di produzione di `S2`: aggiunge ricette vere
da URL veri e le rilegge, in un unico ricettario configurato. Gli utenti finali arrivano con
`S7`.

## Includes

- Tabelle `Cookbook` e `Recipe` con la loro migrazione: `name`, `ingredients`, `steps`,
  `prepTime?`, `tags`, `sourceUrl?`, tutti testo libero o nulli.
- Un solo resolver `currentCookbook`, che qui restituisce il ricettario configurato: ogni
  lettura e scrittura di ricetta passa da lì, nessuna prende il `cookbookId` dal client.
- Fetch della pagina con l'HttpClient di Effect, timeout e limite di dimensione; parse del
  JSON-LD `schema.org/Recipe` e mappatura sui campi `Recipe`, validata con Schema.
- Una risposta in streaming che emette i passi realmente eseguiti — scarico pagina, leggo
  ricetta, salvo — e li mostra nella UI di add.
- Un errore tipizzato per passo, che diventa il messaggio visto: pagina non raggiungibile,
  risposta non HTML, JSON-LD assente o non conforme.
- Salvataggio immediato senza nessuna conferma, elenco delle ricette del ricettario e pagina
  di lettura di una ricetta.

## Verification

- Da un URL di food blog con JSON-LD, la ricetta compare nell'elenco con nome, ingredienti e
  preparazione leggibili, e l'utente non ha compilato nessun campo.
- Durante l'aggiunta i passi appaiono uno dopo l'altro mentre accadono, e l'ultimo appare
  quando la ricetta è già scritta a database — non prima.
- Un URL dietro paywall e un URL senza JSON-LD falliscono ognuno con il proprio messaggio, che
  nomina il passo caduto; il ricettario resta come prima, senza ricette a metà.
- Su un campione di URL reali è dichiarato quanti avevano JSON-LD utilizzabile.
- Nessuna query di lettura o scrittura delle ricette compila il `cookbookId` da un parametro
  di richiesta.
- La stessa pagina aggiunta due volte produce due ricette, senza errore.

## Learning target

Che una ricetta entri nel ricettario dal solo URL dentro una singola richiesta sincrona, con la
progress bar che mostra i passi veri e un fallimento che dice quale passo è caduto — la
promessa di attrito minimo sta o cade sul fatto che questo entri nei tempi di una richiesta.

## Excludes

- L'estrazione quando il JSON-LD manca: è `S4`, il rimedio del fallimento che questa riga
  dichiara.
- Il passo "Salvo foto" della progress bar e qualunque immagine: `S10` lo aggiunge alla
  pipeline che questa riga apre.
- Embedding e ricerca: `S6`. Qui le ricette si trovano solo scorrendo l'elenco.
- Login, ricettari multipli e membership: `S7` e `S8` sostituiscono il resolver, non le query.
- Modifica di una ricetta salvata: `S9`.

## Open questions

- —
