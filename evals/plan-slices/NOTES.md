# Note dagli eval

Osservazioni emerse eseguendo gli eval delle skill, con le modifiche che ne sono derivate e cosa
resta da verificare. Ogni nota è autoconsistente: non serve il contesto della sessione in cui è nata.

## plan-slices — Confine di scope vs identità nell'ordinamento delle slice

**Contesto.** Eval `evals/plan-slices/recipe-app`: pianificazione di una recipe app greenfield
(Next.js, Postgres+pgvector, Auth.js + Google OAuth, condivisione cookbook-centrica). Il
differenziatore dichiarato è la ricerca semantica cross-lingua; senza di essa il prodotto è una
riscrittura di Mealie. Piano prodotto: `results/PLAN-CC-CON-2.md`.

**Osservazione.** Il piano colloca l'autenticazione alla slice 5, dopo il walking skeleton (1),
l'enabler di indicizzazione su fixture (2), la ricerca semantica (3) e l'elenco/lettura ricetta (4).
Sospetto iniziale: una funzionalità così di base rinviata rischia un rilavoro intenso, e
anticiparla subito dopo il walking skeleton sarebbe costato poco.

**Conclusione: l'ordine è giustificato, ma solo a una condizione.** La distinzione che conta non è
"auth presto vs tardi", è **confine di scope vs identità**:

- Il **confine** (`Cookbook`, `Recipe.cookbookId`, ogni query filtrata, 404 fuori scope) esiste già
  dalla slice 2, cioè dalla prima slice che persiste dati.
- L'**identità** (chi sei, e da dove viene il `cookbookId` corrente) è l'unica cosa rinviata.

Il rilavoro intenso che ci si aspetta dall'auth tardiva nasce dal rinvio del **confine**: query
scritte senza filtro, tabelle senza colonna di tenancy, UI senza il concetto di spazio corrente. Il
retrofit tocca allora ogni query e rischia di dimenticarne una, cioè un buco di sicurezza. Se invece
il confine c'è già, cambia solo **da dove si legge lo scope corrente**, non chi filtra.

**Condizione da rendere esplicita.** Il rilavoro resta limitato solo se le slice pre-auth risolvono
lo scope corrente in **un unico punto** (es. `currentCookbookId()`: prima legge la configurazione,
dalla slice di auth legge la sessione). Se l'id viene ricavato in più handler, il rilavoro diventa
reale. Il piano generato non dichiarava questa giunzione: è il difetto vero, non l'ordine.

**Asimmetria dei costi** che regge la scelta:

| | Auth anticipata | Auth dopo il differenziatore |
|---|---|---|
| Ritardo sul verdetto del differenziatore | ~1 slice | nessuno |
| Rilavoro se il differenziatore regge | nessuno | risolutore di scope + protezione rotte |
| Costo se il differenziatore non regge | auth costruita per un prodotto che cambia | nulla di sprecato |
| Attrito nelle verifiche intermedie | login a ogni sessione di test | verifiche da script/browser diretti |

Il punto decisivo: **l'auth non ha rischio tecnico** (Auth.js + Google su Next.js è percorso
battuto, esito noto), la ricerca semantica cross-lingua sì. Anticipare lavoro certo davanti a lavoro
incerto è esattamente ciò che l'ordinamento risk-first evita. Vale anche che la migrazione che
introduce `User`/`Membership`/`creatorId` arriva quando il DB ha solo fixture e la produzione non
esiste ancora: il momento più economico possibile.

**Variante considerata e non applicata.** Spostare la slice di auth prima di elenco/lettura
(`0,1,2,3,5,4,…`): dopo la 3 il verdetto sul differenziatore c'è già, quindi non ritarda nulla di
importante, e l'unica slice mai costruita senza sessione resta la ricerca. Hedge a costo quasi nullo
se si vuole ridurre la superficie pre-identità. Non applicata al piano perché il piano è un artefatto
di test, non un deliverable.

**Modifiche alla skill.**

- Passo 4, nuova regola di ordinamento: *"Separate a boundary from the identity behind it. Ship the
  tenancy, ownership, or scope boundary with the first slice that persists data, and let a single
  named resolver own the current scope; then a later slice can replace a configured scope with an
  authenticated one at one seam. State that seam under `Cross-functional concerns`. Never defer the
  boundary itself, and never defer identity when no such seam exists."*
- `ANTI-PATTERNS` → `Deferred safety`, clausola di disambiguazione: sostituire uno scope configurato
  con uno autenticato a una giunzione dichiarata non è deferred safety; pubblicare slice con letture
  non scoped sì. Senza questa clausola l'anti-pattern spingeva verso l'auth anticipata anche quando
  non serve.

**Da verificare al prossimo eval.** Se la skill riproduce l'auth dopo il differenziatore **e**
dichiara la giunzione in `Cross-functional concerns`, la regola funziona. Se riproduce l'ordine ma
omette la giunzione, la prosa non basta e serve un controllo strutturale nel validatore (es. sezione
o campo obbligatorio quando una slice di identità segue la prima slice che persiste dati).
