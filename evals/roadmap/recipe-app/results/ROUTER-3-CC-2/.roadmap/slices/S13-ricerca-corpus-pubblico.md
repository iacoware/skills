# S13 — Ricerca su tutto il corpus pubblico

← [Register](../roadmap.md#now)

**Outcome:** Una ricerca fatta senza account attraversa le ricette di tutti i ricettari pubblici e
ogni risultato dice da quale ricettario viene; dentro un ricettario privato la ricerca resta quella
consegnata.

**Requested by:** La nuova meta dichiarata dall'autore (la ricerca funziona su tutto il corpus
pubblico, non dentro un ricettario), `sources/goal.md` (Differenziatore — ricerca semantica
cross-lingua), `sources/arch-choices.md` (Datastore, Embeddings). Lo spike archiviato ne ha lasciato
il corpus di prova e le query attese.

**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chiunque, senza account: scrive "pomodoro" o "cena leggera" e si ritrova ricette che stanno in
ricettari di cui non è membro, che non ha mai aperto e che non sapeva esistessero.

## Includes

- Un seed che sia davvero un corpus e non un banco di prova: migliaia di ricette in decine di
  ricettari tematici diversi, catturati con la pipeline già consegnata da siti diversi, in più lingue,
  per tutti e tre gli ingressi (JSON-LD, fallback LLM, copia-incolla). Nessuna mano editoriale sopra
  l'insieme: i ricettari non stanno insieme perché qualcuno li ha scelti, e la loro qualità è
  disomogenea come sarà quella vera. Un corpus curato da noi misurerebbe una cosa che in pubblico non
  esisterà.
- Il filtro di visibilità applicato dentro la query vettoriale, non dopo, con l'indice HNSW già in
  piedi.
- Risultati che nominano il ricettario d'origine e ci portano dentro.
- L'embedding della sola stringa cercata a ogni query, come nella ricerca consegnata; il corpus non
  viene mai ri-embeddato.
- Un limite di frequenza sulle ricerche anonime, che nasce qui perché è qui che qualcuno senza
  account fa partire per la prima volta una chiamata a pagamento.
- La ricerca dentro un ricettario privato invariata, e l'una non vede mai l'altra.

## Verification

Una query in italiano trova una ricetta scritta in inglese che sta in un ricettario pubblico di cui
chi cerca non è membro. Nessun risultato viene mai da un ricettario privato, nemmeno dai propri,
nemmeno cambiando la query, nemmeno da loggati. Il recall@10 sulle query di prova dello spike è
dichiarato sul corpus pubblico e messo accanto a quello misurato dentro il singolo ricettario: la
riga dice se il cross-lingua ha tenuto o quanto ha perso, e su quali query. La latenza p95 della
query di similarità è dichiarata con il filtro di visibilità applicato, sul corpus del seed. Una
raffica di ricerche anonime viene limitata e lo dice, e il costo di embedding per finestra è
dichiarato. Sulle stesse query di prova la riga dichiara che cosa contiene la prima pagina: quanti
risultati sono la stessa ricetta arrivata da due ricettari diversi, quanti vengono tutti dallo stesso
ricettario, quanti sono fuori tema. È l'unica misura che dice se la somiglianza semantica da sola
basta a ordinare un corpus che nessuno ha curato insieme, adesso che i duplicati non sono più un
dettaglio di casa e che la mappa non ammette nessun altro segnale. Il costo una tantum della cattura
del seed è dichiarato accanto al preventivo delle sorgenti: sono le migliaia di estrazioni più care
che il progetto farà in una volta sola.

## Learning target

Se la scoperta regge su un corpus che nessuno ha curato insieme — il recall cross-lingua misurato
dentro un solo ricettario quando le ricette in gara sono migliaia e non centinaia, e la prima pagina
quando quelle migliaia arrivano da decine di ricettari fatti da persone diverse, con qualità
disomogenea e duplicati ammessi.

## Excludes

- Filtri per tag e tempo e ricerca ibrida: restano candidati, e i campi si popolano già da soli.
- La ricerca che attraversa i ricettari privati di cui si è membri: resta candidata, ed è un'altra
  cosa da questa.
- La deduplica dei risultati: esclusa dalla mappa, con il prezzo scritto.
- La vetrina dei ricettari: è di `S15`.

## Open questions

- —
