# Noise — ROADMAP-CC-6

Generato da `make eval-noise RUN=<dir del principale>`: mai scritto a mano, rigenerabile. A
differenza di `METRICS.md` non è derivato puro: la colonna di provenienza distingue gli
accoppiamenti meccanici da quelli giudicati dalla sessione di allineamento
(`../../prompts/noise.prompt.md` su `noise/residual.json`, giudizi in `noise/alignment.json`),
e rilanciando possono cambiare al più quei giudizi. Il disegno è
`design/roadmap/EVAL-NOISE.md`.

Run gemelli: `ROADMAP-CC-6`, `ROADMAP-CC-6B`, `ROADMAP-CC-6C` — stessa skill (tree `0d47a59`), stesso prompt, stesso modello ed effort.

Misura l'accordo tra run a versione ferma, non la qualità contro le regole: i casi non
allineabili non sono errori dello strumento, sono la misura.

## Sintesi

Quanto ha prodotto ciascun run — conteggi grezzi, nessun confronto:

| Asse | ROADMAP-CC-6 | ROADMAP-CC-6B | ROADMAP-CC-6C |
| --- | --- | --- | --- |
| temi | 6 | 6 | 5 |
| verdetti | 6 | 5 | 5 |
| righe | 11 | 12 | 12 |
| archi di dipendenza | 8 | 12 | 9 |
| out-of-scope | 4 | 5 | 6 |

Accordo per coppia, `accoppiati / confrontabili`: il denominatore esclude i non confrontabili,
e per i verdetti conta come mancato accordo anche una divergenza sul verdetto stesso.

| Asse | ROADMAP-CC-6 ↔ ROADMAP-CC-6B | ROADMAP-CC-6 ↔ ROADMAP-CC-6C | ROADMAP-CC-6B ↔ ROADMAP-CC-6C |
| --- | --- | --- | --- |
| temi | 5/7 | 5/6 | 4/7 |
| verdetti | 1/6 | 4/5 | 0/4 |
| righe | 11/12 | 11/12 | 12/12 |
| righe — campi concordi | 7/11 | 6/11 | 7/12 |
| archi di dipendenza | 7/12 | 8/8 | 8/13 |
| out-of-scope | 4/5 | 4/6 | 5/6 |

## Come leggere

Ogni coppia di run ha una tabella e, sotto, un blocco per asse nello stesso ordine. Il numero di
bullet di ogni gruppo elencato è esattamente la cella corrispondente in tabella.

- **Accoppiati** — oggetti riconosciuti come lo stesso oggetto nei due run. In `«A» = «B»` la
  sinistra è il primo run della coppia, la destra il secondo; un solo nome significa stringa
  identica. `mecc/mod` divide gli accoppiamenti fra stringa identica e giudizio del modello, ed è
  `—` su verdetti e archi di dipendenza perché quei due assi non passano mai dal modello: si
  confrontano traducendo i nomi già allineati su temi e righe.
- **Divergenti** — sottoinsieme degli accoppiati, non una categoria a sé: stesso oggetto, campo
  diverso (`theme`, `kind`, `size` per le righe; il verdetto per i verdetti). Il gruppo elencato
  ripete quegli accoppiamenti con il delta dei campi.
- **Solo X** — presente in X, senza controparte nell'altro run.
- **Archi di dipendenza** — le voci di `Depends on` della tabella NOW, una per coppia. In
  `«A» → «B»` la punta va al prerequisito: «A» dipende da «B».
- **Non confrontabili** — oggetti derivati che non arrivano al confronto perché un loro estremo
  non è allineato: un verdetto su una coppia di temi di cui uno non ha controparte, un arco di
  dipendenza che tocca una riga senza controparte. Non è disaccordo, è cecità del confronto.

## Accordo per asse

### ROADMAP-CC-6 ↔ ROADMAP-CC-6B

| Asse | Accoppiati | mecc/mod | Divergenti | Solo ROADMAP-CC-6 | Solo ROADMAP-CC-6B | Non confrontabili |
| --- | --- | --- | --- | --- | --- | --- |
| temi | 5 | 1/4 | — | 1 | 1 | — |
| verdetti | 1 | — | 0 | 3 | 2 | 4 |
| righe | 11 | 1/10 | 4 | 0 | 1 | — |
| archi di dipendenza | 7 | — | — | 1 | 4 | 1 |
| out-of-scope | 4 | 1/3 | — | 0 | 1 | — |

**temi** — accoppiati 5 (meccanici 1, dal modello 4) · solo ROADMAP-CC-6: 1 · solo ROADMAP-CC-6B: 1

Accoppiati:
- `foto` — meccanico
- `cattura` = `aggiunta-da-link` — modello
- `ricerca` = `ricerca-semantica` — modello
- `condivisione` = `ricettari-condivisi` — modello
- `correzione` = `scrittura-e-correzione` — modello

Solo ROADMAP-CC-6:
- `accesso`

Solo ROADMAP-CC-6B:
- `aggiunta-da-testo`

**verdetti** — accoppiati 1 · solo ROADMAP-CC-6: 3 · solo ROADMAP-CC-6B: 2 · non confrontabili 4

Accoppiati:
- `correzione / foto` — split

Solo ROADMAP-CC-6:
- `cattura / ricerca`
- `cattura / correzione`
- `cattura / foto`

Solo ROADMAP-CC-6B:
- `ricerca-semantica / ricettari-condivisi`
- `ricettari-condivisi / scrittura-e-correzione`

Non confrontabili (un tema della coppia non ha controparte):
- `ricerca / accesso` — ROADMAP-CC-6
- `accesso / condivisione` — ROADMAP-CC-6
- `aggiunta-da-link / aggiunta-da-testo` — ROADMAP-CC-6B
- `aggiunta-da-testo / ricerca-semantica` — ROADMAP-CC-6B

**righe** — accoppiati 11 (meccanici 1, dal modello 10) · divergenti sui campi 4 · solo ROADMAP-CC-6B: 1

Accoppiati:
- «Repository, CI e credenziali» — meccanico
- «Scheletro deployato su Fly con Postgres» = «Walking skeleton: Next.js su Fly con Postgres e migrazioni» — modello
- «Recall cross-lingua degli embedding multilingue» = «Spike: la ricerca cross-lingua regge su ricette vere?» — modello
- «Aggiungi da link con JSON-LD, elenco e dettaglio» = «Aggiunta da link con JSON-LD e elenco del ricettario» — modello
- «Estrazione LLM per pagine senza structured data» = «Estrazione LLM quando il JSON-LD manca» — modello
- «Ricerca semantica nel ricettario» = «Ricerca semantica cross-lingua nel ricettario» — modello
- «Accesso con Google e ricettario proprio» = «Accesso con Google e scope autenticato» — modello
- «Invito condivisibile a un ricettario» = «Invito via link e ricettari condivisi» — modello
- «Modifica di una ricetta e inserimento a mano» = «Scrittura a mano e correzione» — modello
- «Foto multiple e copertina» = «Foto della ricetta» — modello
- «Rilascio a famiglia e amici» = «Messa in mano a famiglia e amici» — modello

Divergenti:
- «Repository, CI e credenziali» — size (small ≠ medium)
- «Recall cross-lingua degli embedding multilingue» — theme (ricerca ≠ goal), size (medium ≠ small)
- «Accesso con Google e ricettario proprio» — theme (accesso ≠ ricettari-condivisi)
- «Invito condivisibile a un ricettario» — size (small ≠ medium)

Solo ROADMAP-CC-6B:
- «Aggiunta da testo incollato»

**archi di dipendenza** — accoppiati 7 · solo ROADMAP-CC-6: 1 · solo ROADMAP-CC-6B: 4 · non confrontabili 1

Accoppiati:
- «Estrazione LLM per pagine senza structured data» → «Aggiungi da link con JSON-LD, elenco e dettaglio»
- «Ricerca semantica nel ricettario» → «Aggiungi da link con JSON-LD, elenco e dettaglio»
- «Accesso con Google e ricettario proprio» → «Aggiungi da link con JSON-LD, elenco e dettaglio»
- «Invito condivisibile a un ricettario» → «Accesso con Google e ricettario proprio»
- «Modifica di una ricetta e inserimento a mano» → «Aggiungi da link con JSON-LD, elenco e dettaglio»
- «Foto multiple e copertina» → «Aggiungi da link con JSON-LD, elenco e dettaglio»
- «Rilascio a famiglia e amici» → «Invito condivisibile a un ricettario»

Solo ROADMAP-CC-6:
- «Aggiungi da link con JSON-LD, elenco e dettaglio» → «Recall cross-lingua degli embedding multilingue»

Solo ROADMAP-CC-6B:
- «Ricerca semantica cross-lingua nel ricettario» → «Spike: la ricerca cross-lingua regge su ricette vere?»
- «Scrittura a mano e correzione» → «Ricerca semantica cross-lingua nel ricettario»
- «Foto della ricetta» → «Scrittura a mano e correzione»
- «Messa in mano a famiglia e amici» → «Foto della ricetta»

Non confrontabili (un estremo non ha controparte):
- «Aggiunta da testo incollato» → «Estrazione LLM quando il JSON-LD manca» — ROADMAP-CC-6B

**out-of-scope** — accoppiati 4 (meccanici 1, dal modello 3) · solo ROADMAP-CC-6B: 1

Accoppiati:
- «Ingredienti strutturati in quantità e unità» — meccanico
- «La review obbligatoria prima del salvataggio» = «Review obbligatoria dell'estratto» — modello
- «La deduplica delle ricette» = «Deduplica delle ricette» — modello
- «Invio di email e notifiche» = «Qualunque provider di posta» — modello

Solo ROADMAP-CC-6B:
- «Ruoli e permessi granulari»

### ROADMAP-CC-6 ↔ ROADMAP-CC-6C

| Asse | Accoppiati | mecc/mod | Divergenti | Solo ROADMAP-CC-6 | Solo ROADMAP-CC-6C | Non confrontabili |
| --- | --- | --- | --- | --- | --- | --- |
| temi | 5 | 2/3 | — | 1 | 0 | — |
| verdetti | 4 | — | 0 | 0 | 1 | 2 |
| righe | 11 | 1/10 | 5 | 0 | 1 | — |
| archi di dipendenza | 8 | — | — | 0 | 0 | 1 |
| out-of-scope | 4 | 1/3 | — | 0 | 2 | — |

**temi** — accoppiati 5 (meccanici 2, dal modello 3) · solo ROADMAP-CC-6: 1

Accoppiati:
- `condivisione` — meccanico
- `foto` — meccanico
- `cattura` = `aggiunta-ricette` — modello
- `ricerca` = `ricerca-semantica` — modello
- `accesso` = `identita` — modello

Solo ROADMAP-CC-6:
- `correzione`

**verdetti** — accoppiati 4 · solo ROADMAP-CC-6C: 1 · non confrontabili 2

Accoppiati:
- `cattura / ricerca` — split
- `cattura / foto` — split
- `ricerca / accesso` — split
- `accesso / condivisione` — split

Solo ROADMAP-CC-6C:
- `condivisione / foto`

Non confrontabili (un tema della coppia non ha controparte):
- `cattura / correzione` — ROADMAP-CC-6
- `correzione / foto` — ROADMAP-CC-6

**righe** — accoppiati 11 (meccanici 1, dal modello 10) · divergenti sui campi 5 · solo ROADMAP-CC-6C: 1

Accoppiati:
- «Scheletro deployato su Fly con Postgres» — meccanico
- «Repository, CI e credenziali» = «Repository, CI e account dei servizi» — modello
- «Recall cross-lingua degli embedding multilingue» = «Quale embedder regge la ricerca cross-lingua» — modello
- «Aggiungi da link con JSON-LD, elenco e dettaglio» = «Aggiungi una ricetta da link e correggila dopo» — modello
- «Estrazione LLM per pagine senza structured data» = «Fallback LLM quando la pagina non ha JSON-LD» — modello
- «Ricerca semantica nel ricettario» = «Ricerca semantica cross-lingua nel ricettario» — modello
- «Accesso con Google e ricettario proprio» = «Accedi con Google e vedi i tuoi ricettari» — modello
- «Invito condivisibile a un ricettario» = «Invita nel ricettario con un link» — modello
- «Modifica di una ricetta e inserimento a mano» = «Scrivi una ricetta a mano» — modello
- «Foto multiple e copertina» = «Foto della ricetta con copertina» — modello
- «Rilascio a famiglia e amici» = «Il ricettario in mano a famiglia e amici» — modello

Divergenti:
- «Recall cross-lingua degli embedding multilingue» — theme (ricerca ≠ goal), size (medium ≠ small)
- «Accesso con Google e ricettario proprio» — size (medium ≠ large)
- «Invito condivisibile a un ricettario» — size (small ≠ medium)
- «Modifica di una ricetta e inserimento a mano» — theme (correzione ≠ aggiunta-ricette), size (medium ≠ small)
- «Rilascio a famiglia e amici» — size (small ≠ medium)

Solo ROADMAP-CC-6C:
- «Aggiungi una ricetta incollando il testo»

**archi di dipendenza** — accoppiati 8 · non confrontabili 1

Accoppiati:
- «Aggiungi da link con JSON-LD, elenco e dettaglio» → «Recall cross-lingua degli embedding multilingue»
- «Estrazione LLM per pagine senza structured data» → «Aggiungi da link con JSON-LD, elenco e dettaglio»
- «Ricerca semantica nel ricettario» → «Aggiungi da link con JSON-LD, elenco e dettaglio»
- «Accesso con Google e ricettario proprio» → «Aggiungi da link con JSON-LD, elenco e dettaglio»
- «Invito condivisibile a un ricettario» → «Accesso con Google e ricettario proprio»
- «Modifica di una ricetta e inserimento a mano» → «Aggiungi da link con JSON-LD, elenco e dettaglio»
- «Foto multiple e copertina» → «Aggiungi da link con JSON-LD, elenco e dettaglio»
- «Rilascio a famiglia e amici» → «Invito condivisibile a un ricettario»

Non confrontabili (un estremo non ha controparte):
- «Aggiungi una ricetta incollando il testo» → «Fallback LLM quando la pagina non ha JSON-LD» — ROADMAP-CC-6C

**out-of-scope** — accoppiati 4 (meccanici 1, dal modello 3) · solo ROADMAP-CC-6C: 2

Accoppiati:
- «Ingredienti strutturati in quantità e unità» — meccanico
- «La review obbligatoria prima del salvataggio» = «Review obbligatoria prima del salvataggio» — modello
- «La deduplica delle ricette» = «Deduplica delle ricette» — modello
- «Invio di email e notifiche» = «Invio di email» — modello

Solo ROADMAP-CC-6C:
- «Un secondo datastore»
- «Permessi granulari dentro un ricettario»

### ROADMAP-CC-6B ↔ ROADMAP-CC-6C

| Asse | Accoppiati | mecc/mod | Divergenti | Solo ROADMAP-CC-6B | Solo ROADMAP-CC-6C | Non confrontabili |
| --- | --- | --- | --- | --- | --- | --- |
| temi | 4 | 2/2 | — | 2 | 1 | — |
| verdetti | 0 | — | 0 | 1 | 3 | 6 |
| righe | 12 | 1/11 | 5 | 0 | 0 | — |
| archi di dipendenza | 8 | — | — | 4 | 1 | 0 |
| out-of-scope | 5 | 2/3 | — | 0 | 1 | — |

**temi** — accoppiati 4 (meccanici 2, dal modello 2) · solo ROADMAP-CC-6B: 2 · solo ROADMAP-CC-6C: 1

Accoppiati:
- `ricerca-semantica` — meccanico
- `foto` — meccanico
- `aggiunta-da-link` = `aggiunta-ricette` — modello
- `ricettari-condivisi` = `condivisione` — modello

Solo ROADMAP-CC-6B:
- `aggiunta-da-testo`
- `scrittura-e-correzione`

Solo ROADMAP-CC-6C:
- `identita`

**verdetti** — accoppiati 0 · solo ROADMAP-CC-6B: 1 · solo ROADMAP-CC-6C: 3 · non confrontabili 6

Solo ROADMAP-CC-6B:
- `ricerca-semantica / ricettari-condivisi`

Solo ROADMAP-CC-6C:
- `aggiunta-ricette / ricerca-semantica`
- `aggiunta-ricette / foto`
- `condivisione / foto`

Non confrontabili (un tema della coppia non ha controparte):
- `aggiunta-da-link / aggiunta-da-testo` — ROADMAP-CC-6B
- `aggiunta-da-testo / ricerca-semantica` — ROADMAP-CC-6B
- `ricettari-condivisi / scrittura-e-correzione` — ROADMAP-CC-6B
- `scrittura-e-correzione / foto` — ROADMAP-CC-6B
- `ricerca-semantica / identita` — ROADMAP-CC-6C
- `identita / condivisione` — ROADMAP-CC-6C

**righe** — accoppiati 12 (meccanici 1, dal modello 11) · divergenti sui campi 5

Accoppiati:
- «Ricerca semantica cross-lingua nel ricettario» = «Ricerca semantica cross-lingua nel ricettario» — meccanico
- «Repository, CI e credenziali» = «Repository, CI e account dei servizi» — modello
- «Spike: la ricerca cross-lingua regge su ricette vere?» = «Quale embedder regge la ricerca cross-lingua» — modello
- «Walking skeleton: Next.js su Fly con Postgres e migrazioni» = «Scheletro deployato su Fly con Postgres» — modello
- «Aggiunta da link con JSON-LD e elenco del ricettario» = «Aggiungi una ricetta da link e correggila dopo» — modello
- «Estrazione LLM quando il JSON-LD manca» = «Fallback LLM quando la pagina non ha JSON-LD» — modello
- «Aggiunta da testo incollato» = «Aggiungi una ricetta incollando il testo» — modello
- «Accesso con Google e scope autenticato» = «Accedi con Google e vedi i tuoi ricettari» — modello
- «Invito via link e ricettari condivisi» = «Invita nel ricettario con un link» — modello
- «Scrittura a mano e correzione» = «Scrivi una ricetta a mano» — modello
- «Foto della ricetta» = «Foto della ricetta con copertina» — modello
- «Messa in mano a famiglia e amici» = «Il ricettario in mano a famiglia e amici» — modello

Divergenti:
- «Repository, CI e credenziali» — size (medium ≠ small)
- «Aggiunta da testo incollato» — theme (aggiunta-da-testo ≠ aggiunta-ricette)
- «Accesso con Google e scope autenticato» — theme (ricettari-condivisi ≠ identita), size (medium ≠ large)
- «Scrittura a mano e correzione» — theme (scrittura-e-correzione ≠ aggiunta-ricette), size (medium ≠ small)
- «Messa in mano a famiglia e amici» — size (small ≠ medium)

**archi di dipendenza** — accoppiati 8 · solo ROADMAP-CC-6B: 4 · solo ROADMAP-CC-6C: 1

Accoppiati:
- «Estrazione LLM quando il JSON-LD manca» → «Aggiunta da link con JSON-LD e elenco del ricettario»
- «Aggiunta da testo incollato» → «Estrazione LLM quando il JSON-LD manca»
- «Ricerca semantica cross-lingua nel ricettario» → «Aggiunta da link con JSON-LD e elenco del ricettario»
- «Accesso con Google e scope autenticato» → «Aggiunta da link con JSON-LD e elenco del ricettario»
- «Invito via link e ricettari condivisi» → «Accesso con Google e scope autenticato»
- «Scrittura a mano e correzione» → «Aggiunta da link con JSON-LD e elenco del ricettario»
- «Foto della ricetta» → «Aggiunta da link con JSON-LD e elenco del ricettario»
- «Messa in mano a famiglia e amici» → «Invito via link e ricettari condivisi»

Solo ROADMAP-CC-6B:
- «Ricerca semantica cross-lingua nel ricettario» → «Spike: la ricerca cross-lingua regge su ricette vere?»
- «Scrittura a mano e correzione» → «Ricerca semantica cross-lingua nel ricettario»
- «Foto della ricetta» → «Scrittura a mano e correzione»
- «Messa in mano a famiglia e amici» → «Foto della ricetta»

Solo ROADMAP-CC-6C:
- «Aggiungi una ricetta da link e correggila dopo» → «Quale embedder regge la ricerca cross-lingua»

**out-of-scope** — accoppiati 5 (meccanici 2, dal modello 3) · solo ROADMAP-CC-6C: 1

Accoppiati:
- «Ingredienti strutturati in quantità e unità» — meccanico
- «Deduplica delle ricette» — meccanico
- «Ruoli e permessi granulari» = «Permessi granulari dentro un ricettario» — modello
- «Qualunque provider di posta» = «Invio di email» — modello
- «Review obbligatoria dell'estratto» = «Review obbligatoria prima del salvataggio» — modello

Solo ROADMAP-CC-6C:
- «Un secondo datastore»
