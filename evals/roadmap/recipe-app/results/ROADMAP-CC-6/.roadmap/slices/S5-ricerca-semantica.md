# S5 — Ricerca semantica nel ricettario

← [Register](../roadmap.md#now)

**Outcome:** Si scrive "cena leggera" o "pomodoro" nella Home e si ottengono le ricette del
ricettario corrente che ne parlano, comprese quelle scritte in un'altra lingua.
**Requested by:** `goal.md` § Ricerca (MVP: solo semantica) e § Differenziatore; `concepts.md` §
Ricerca (MVP).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi sviluppa e chi prova il prodotto, sull'ambiente non pubblico. Dopo questa riga può ritrovare una
ricetta descrivendola invece di ricordarne il titolo, ed è la prima volta che il differenziatore è
visibile nel prodotto e non in una misura.

## Includes

- Indice HNSW sulla colonna `embedding`, con la definizione uscita da S2.
- Campo di ricerca nella Home e pagina dei risultati.
- Embedding della query al momento della ricerca, con lo stesso modello con cui è indicizzato il
  corpus, e query di similarità su Postgres scopata al ricettario corrente dal resolver di S3.
- Stato vuoto quando nessuna ricetta supera la soglia, distinto dallo stato "il ricettario è vuoto".
- Gestione del fallimento della chiamata di embedding: la ricerca dice che non è riuscita, e
  l'elenco delle ricette resta raggiungibile.

## Verification

- Una ricetta salvata in inglese esce cercando "pomodoro"; una query vaga come "cena leggera" pesca
  ricette il cui testo non contiene quelle parole.
- Una ricetta appartenente a un altro `cookbookId` non compare mai fra i risultati, nemmeno quando è
  la più simile alla query.
- Il tempo dalla pressione di invio al risultato è misurato sull'ambiente di S1 e riportato,
  separando la chiamata di embedding dalla query su Postgres.
- Le query di S2 che il modello scelto sbagliava le sbaglia anche qui, e nella stessa misura: se non
  è così, l'indice o il testo indicizzato non sono quelli misurati.
- Staccando la chiave dell'embedder, la ricerca mostra il proprio errore e la Home continua a
  elencare le ricette.

## Learning target

Se il recall misurato in laboratorio in S2 sopravvive alle ricette vere entrate dalla pipeline di
add, e se una ricerca che paga una chiamata di embedding per query resta abbastanza veloce da essere
il modo normale di ritrovare una ricetta.

## Excludes

- Filtri strutturati su tag e tempo, e ricerca ibrida con full-text: restano candidati, e i campi che
  li abiliteranno S3 li popola già.
- La ricerca che attraversa più ricettari: resta candidata, e questa riga la esclude scopando la
  query a un solo `cookbookId`.
- Ordinamenti, paginazione e sfaccettature dei risultati: nessuna fonte le chiede per l'MVP.

## Open questions

- Nessuna.
