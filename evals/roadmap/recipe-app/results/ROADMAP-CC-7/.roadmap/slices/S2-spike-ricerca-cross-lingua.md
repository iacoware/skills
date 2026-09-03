# S2 — Spike: quanto regge la ricerca cross-lingua

← [Register](../roadmap.md#now)

**Outcome:** Un numero su cui decidere: quale modello di embedding multilingue, e con che recall,
trova una ricetta scritta in inglese quando la query è in italiano.

**Requested by:** `goal.md` (Differenziatore e la nota strategica che chiama la ricerca cross-lingua
"il vero elemento distintivo") e `arch-choices.md` (Embeddings), che vincola il modello a essere
multilingue e ne nomina uno solo come esempio, senza sceglierlo.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

—

## Includes

- Un corpus seme di una sessantina di ricette reali raccolte a mano da blog: circa trenta in
  italiano, venticinque in inglese, cinque in francese o spagnolo, salvate come file di testo con
  nome, ingredienti e preparazione.
- Una tabella usa-e-getta sul Postgres di staging con il testo e il vettore di ogni ricetta,
  interrogata sia in scan pieno sia con indice HNSW.
- Almeno due candidati dichiarati multilingue a confronto, fra cui quello che `arch-choices.md`
  nomina come esempio, sullo stesso corpus e con le stesse query.
- Una ventina di query in italiano scritte prima di vedere qualunque risultato: metà per ingrediente
  ("pomodoro", "ceci"), metà per intenzione ("cena leggera", "dolce senza forno"), ognuna con le
  ricette che dovrebbero uscire marcate a mano.
- La misura del costo reale: token spesi per indicizzare il corpus e per una singola query.

## Verification

- Per ogni candidato è scritto il recall@10 delle query italiane che devono trovare ricette in
  inglese, tenuto separato dal recall delle query che devono trovare ricette italiane: è la
  differenza fra i due numeri a dire se il cross-lingua funziona o se sta solo funzionando la lingua
  di partenza.
- È scritto di quanto cala il recall passando dallo scan pieno all'indice HNSW sul corpus seme, con i
  parametri usati.
- È scritta la latenza p95 di una ricerca completa — embedding della query più `select` — misurata
  contro il Postgres di staging, e il costo in dollari per indicizzare diecimila ricette.
- La raccomandazione è una frase che nomina un modello e dice se il recall cross-lingua basta a
  reggere il differenziatore, o se `goal.md` va riletto perché senza quello staremmo riscrivendo
  Mealie.

## Learning target

Che un embedding multilingue commerciale trovi ricette scritte in un'altra lingua abbastanza bene da
giustificare il progetto — è l'unica promessa che `goal.md` dichiara esistenziale — e quale dei
candidati lo faccia meglio a parità di costo.

## Excludes

- Il codice: la tabella usa-e-getta si droppa e lo script resta fuori dal build. Sopravvivono solo il
  corpus seme, che `S6` riusa per i propri test, e la raccomandazione scritta.
- Qualunque interfaccia: qui non c'è schermo, solo numeri.
- La ricerca ibrida e i filtri strutturati → `LATER`: qui si misura la sola semantica, perché è la
  sola che l'MVP promette.
- La derivazione di tag e tempo: il corpus seme porta solo il testo, così il numero misura
  l'embedding e non l'arricchimento.

## Open questions

- —
