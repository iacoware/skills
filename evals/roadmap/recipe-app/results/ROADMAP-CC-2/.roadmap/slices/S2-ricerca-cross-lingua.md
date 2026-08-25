# S2 — Quanto regge la ricerca cross-lingua

← [Register](../roadmap.md#now)

**Outcome:** Si sa, con numeri misurati su pgvector reale, quale modello di embedding cloud recupera
una ricetta inglese da una query italiana con qualità sufficiente, quanto costa a 10.000 ricette, che
latenza aggiunge all'aggiunta, e se esiste una soglia di distanza che separa un risultato pertinente
da uno che non lo è. Se nessun candidato ci riesce, si sa qui.

**Requested by:** `goal.md` (§ Differenziatore, nota strategica: senza ricerca semantica cross-lingua
si riscrive Mealie) e `arch-choices.md` (§ Embeddings), che chiede un modello "multilingue" senza
sceglierne uno — un aggettivo, non una scelta.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

—

## Includes

- Un corpus di seed di circa cinquanta ricette reali, metà in italiano e metà in inglese, caricate
  direttamente nel Postgres di S1 da uno script: è l'input reale più economico che rende misurabile
  la promessa, e non richiede che l'import esista.
- Un insieme fisso di query scritte come le scriverebbe chi userà l'app — "cena leggera", "pomodoro",
  "qualcosa con le melanzane", più le corrispondenti in inglese — ciascuna con le ricette che ci si
  aspetta di trovare, dichiarate prima di misurare.
- Almeno due modelli candidati fra quelli raggiungibili via API cloud, incluso quello citato dalle
  fonti come esempio, indicizzati sullo stesso corpus con lo stesso testo (`nome + ingredienti +
  preparazione`, più `tag + tempo` dove esistono) e lo stesso indice HNSW.
- La misura del costo per 10.000 ricette e della latenza di una singola chiamata di embedding, la
  sola che l'aggiunta pagherà.

## Verification

Per ciascun modello candidato esiste un numero scritto, non un'impressione: quante delle query
italiane recuperano la ricetta inglese attesa nei primi cinque risultati e quante nelle prime dieci,
e altrettanto nella direzione opposta; quale distanza separa l'ultimo risultato pertinente dal primo
che non lo è, e se quella separazione è abbastanza stabile fra le query da diventare una soglia; il
costo di indicizzare 10.000 ricette; la latenza p95 di una chiamata di embedding. L'esito è una
scelta scritta, con i numeri che la reggono e con la soglia proposta — oppure la constatazione, coi
numeri, che nessun candidato regge, che è un risultato altrettanto valido e che rimette in
discussione il differenziatore.

## Learning target

Un modello di embedding cloud, senza fine-tuning e senza tradurre nulla, recupera una ricetta scritta
in un'altra lingua da una query in italiano con qualità sufficiente a reggere l'unica cosa che
distingue questo prodotto da Mealie — e lo fa a un costo compatibile con "centesimi al mese".

## Excludes

- L'interfaccia di ricerca, la generazione degli embedding dentro il flusso di aggiunta e il
  riempimento dell'indice per le ricette reali: sono di S6, che consuma la scelta fatta qui.
- Il tuning dei parametri dell'indice HNSW: a questa scala non cambia l'esito, e S6 lo rileggerà sul
  corpus vero.
- Del codice scritto per lo spike non sopravvive nulla: restano il corpus di seed, l'insieme di query
  con le attese, i numeri e la scelta.

## Open questions

- —
