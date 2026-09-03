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

## Accordo per asse

### ROADMAP-CC-6 ↔ ROADMAP-CC-6B

| Asse | Accoppiati | mecc/mod | Divergenti | Solo ROADMAP-CC-6 | Solo ROADMAP-CC-6B | Non confrontabili |
| --- | --- | --- | --- | --- | --- | --- |
| temi | 5 | 1/4 | — | 1 | 1 | — |
| verdetti | 1 | — | 0 | 3 | 2 | 4 |
| righe | 11 | 1/10 | 4 | 0 | 1 | — |
| archi | 7 | — | — | 1 | 4 | 1 |
| out-of-scope | 4 | 1/3 | — | 0 | 1 | — |

Accoppiamenti e casi:

- tema `foto` — meccanico
- tema `cattura` = `aggiunta-da-link` — modello
- tema `ricerca` = `ricerca-semantica` — modello
- tema `condivisione` = `ricettari-condivisi` — modello
- tema `correzione` = `scrittura-e-correzione` — modello
- tema `accesso` — non allineabile (solo ROADMAP-CC-6)
- tema `aggiunta-da-testo` — non allineabile (solo ROADMAP-CC-6B)
- riga «Repository, CI e credenziali» — meccanico; diverge su size (small ≠ medium)
- riga «Scheletro deployato su Fly con Postgres» = «Walking skeleton: Next.js su Fly con Postgres e migrazioni» — modello
- riga «Recall cross-lingua degli embedding multilingue» = «Spike: la ricerca cross-lingua regge su ricette vere?» — modello; diverge su theme (ricerca ≠ goal), size (medium ≠ small)
- riga «Aggiungi da link con JSON-LD, elenco e dettaglio» = «Aggiunta da link con JSON-LD e elenco del ricettario» — modello
- riga «Estrazione LLM per pagine senza structured data» = «Estrazione LLM quando il JSON-LD manca» — modello
- riga «Ricerca semantica nel ricettario» = «Ricerca semantica cross-lingua nel ricettario» — modello
- riga «Accesso con Google e ricettario proprio» = «Accesso con Google e scope autenticato» — modello; diverge su theme (accesso ≠ ricettari-condivisi)
- riga «Invito condivisibile a un ricettario» = «Invito via link e ricettari condivisi» — modello; diverge su size (small ≠ medium)
- riga «Modifica di una ricetta e inserimento a mano» = «Scrittura a mano e correzione» — modello
- riga «Foto multiple e copertina» = «Foto della ricetta» — modello
- riga «Rilascio a famiglia e amici» = «Messa in mano a famiglia e amici» — modello
- riga «Aggiunta da testo incollato» — non allineabile (solo ROADMAP-CC-6B)
- out-of-scope «Ingredienti strutturati in quantità e unità» — meccanico
- out-of-scope «La review obbligatoria prima del salvataggio» = «Review obbligatoria dell'estratto» — modello
- out-of-scope «La deduplica delle ricette» = «Deduplica delle ricette» — modello
- out-of-scope «Invio di email e notifiche» = «Qualunque provider di posta» — modello
- out-of-scope «Ruoli e permessi granulari» — non allineabile (solo ROADMAP-CC-6B)
- verdetto `cattura / ricerca` — solo ROADMAP-CC-6
- verdetto `cattura / correzione` — solo ROADMAP-CC-6
- verdetto `cattura / foto` — solo ROADMAP-CC-6
- verdetto `ricerca-semantica / ricettari-condivisi` — solo ROADMAP-CC-6B
- verdetto `ricettari-condivisi / scrittura-e-correzione` — solo ROADMAP-CC-6B
- verdetto `ricerca / accesso` (tema senza allineamento, ROADMAP-CC-6)
- verdetto `accesso / condivisione` (tema senza allineamento, ROADMAP-CC-6)
- verdetto `aggiunta-da-link / aggiunta-da-testo` (tema senza allineamento, ROADMAP-CC-6B)
- verdetto `aggiunta-da-testo / ricerca-semantica` (tema senza allineamento, ROADMAP-CC-6B)
- archi concordi: 7
- arco «Aggiungi da link con JSON-LD, elenco e dettaglio» → «Recall cross-lingua degli embedding multilingue» — solo ROADMAP-CC-6
- arco «Ricerca semantica cross-lingua nel ricettario» → «Spike: la ricerca cross-lingua regge su ricette vere?» — solo ROADMAP-CC-6B
- arco «Scrittura a mano e correzione» → «Ricerca semantica cross-lingua nel ricettario» — solo ROADMAP-CC-6B
- arco «Foto della ricetta» → «Scrittura a mano e correzione» — solo ROADMAP-CC-6B
- arco «Messa in mano a famiglia e amici» → «Foto della ricetta» — solo ROADMAP-CC-6B
- arco «Aggiunta da testo incollato» → «Estrazione LLM quando il JSON-LD manca» (estremo senza allineamento, ROADMAP-CC-6B)

### ROADMAP-CC-6 ↔ ROADMAP-CC-6C

| Asse | Accoppiati | mecc/mod | Divergenti | Solo ROADMAP-CC-6 | Solo ROADMAP-CC-6C | Non confrontabili |
| --- | --- | --- | --- | --- | --- | --- |
| temi | 5 | 2/3 | — | 1 | 0 | — |
| verdetti | 4 | — | 0 | 0 | 1 | 2 |
| righe | 11 | 1/10 | 5 | 0 | 1 | — |
| archi | 8 | — | — | 0 | 0 | 1 |
| out-of-scope | 4 | 1/3 | — | 0 | 2 | — |

Accoppiamenti e casi:

- tema `condivisione` — meccanico
- tema `foto` — meccanico
- tema `cattura` = `aggiunta-ricette` — modello
- tema `ricerca` = `ricerca-semantica` — modello
- tema `accesso` = `identita` — modello
- tema `correzione` — non allineabile (solo ROADMAP-CC-6)
- riga «Scheletro deployato su Fly con Postgres» — meccanico
- riga «Repository, CI e credenziali» = «Repository, CI e account dei servizi» — modello
- riga «Recall cross-lingua degli embedding multilingue» = «Quale embedder regge la ricerca cross-lingua» — modello; diverge su theme (ricerca ≠ goal), size (medium ≠ small)
- riga «Aggiungi da link con JSON-LD, elenco e dettaglio» = «Aggiungi una ricetta da link e correggila dopo» — modello
- riga «Estrazione LLM per pagine senza structured data» = «Fallback LLM quando la pagina non ha JSON-LD» — modello
- riga «Ricerca semantica nel ricettario» = «Ricerca semantica cross-lingua nel ricettario» — modello
- riga «Accesso con Google e ricettario proprio» = «Accedi con Google e vedi i tuoi ricettari» — modello; diverge su size (medium ≠ large)
- riga «Invito condivisibile a un ricettario» = «Invita nel ricettario con un link» — modello; diverge su size (small ≠ medium)
- riga «Modifica di una ricetta e inserimento a mano» = «Scrivi una ricetta a mano» — modello; diverge su theme (correzione ≠ aggiunta-ricette), size (medium ≠ small)
- riga «Foto multiple e copertina» = «Foto della ricetta con copertina» — modello
- riga «Rilascio a famiglia e amici» = «Il ricettario in mano a famiglia e amici» — modello; diverge su size (small ≠ medium)
- riga «Aggiungi una ricetta incollando il testo» — non allineabile (solo ROADMAP-CC-6C)
- out-of-scope «Ingredienti strutturati in quantità e unità» — meccanico
- out-of-scope «La review obbligatoria prima del salvataggio» = «Review obbligatoria prima del salvataggio» — modello
- out-of-scope «La deduplica delle ricette» = «Deduplica delle ricette» — modello
- out-of-scope «Invio di email e notifiche» = «Invio di email» — modello
- out-of-scope «Un secondo datastore» — non allineabile (solo ROADMAP-CC-6C)
- out-of-scope «Permessi granulari dentro un ricettario» — non allineabile (solo ROADMAP-CC-6C)
- verdetto `condivisione / foto` — solo ROADMAP-CC-6C
- verdetto `cattura / correzione` (tema senza allineamento, ROADMAP-CC-6)
- verdetto `correzione / foto` (tema senza allineamento, ROADMAP-CC-6)
- archi concordi: 8
- arco «Aggiungi una ricetta incollando il testo» → «Fallback LLM quando la pagina non ha JSON-LD» (estremo senza allineamento, ROADMAP-CC-6C)

### ROADMAP-CC-6B ↔ ROADMAP-CC-6C

| Asse | Accoppiati | mecc/mod | Divergenti | Solo ROADMAP-CC-6B | Solo ROADMAP-CC-6C | Non confrontabili |
| --- | --- | --- | --- | --- | --- | --- |
| temi | 4 | 2/2 | — | 2 | 1 | — |
| verdetti | 0 | — | 0 | 1 | 3 | 6 |
| righe | 12 | 1/11 | 5 | 0 | 0 | — |
| archi | 8 | — | — | 4 | 1 | 0 |
| out-of-scope | 5 | 2/3 | — | 0 | 1 | — |

Accoppiamenti e casi:

- tema `ricerca-semantica` — meccanico
- tema `foto` — meccanico
- tema `aggiunta-da-link` = `aggiunta-ricette` — modello
- tema `ricettari-condivisi` = `condivisione` — modello
- tema `aggiunta-da-testo` — non allineabile (solo ROADMAP-CC-6B)
- tema `scrittura-e-correzione` — non allineabile (solo ROADMAP-CC-6B)
- tema `identita` — non allineabile (solo ROADMAP-CC-6C)
- riga «Ricerca semantica cross-lingua nel ricettario» = «Ricerca semantica cross-lingua nel ricettario» — meccanico
- riga «Repository, CI e credenziali» = «Repository, CI e account dei servizi» — modello; diverge su size (medium ≠ small)
- riga «Spike: la ricerca cross-lingua regge su ricette vere?» = «Quale embedder regge la ricerca cross-lingua» — modello
- riga «Walking skeleton: Next.js su Fly con Postgres e migrazioni» = «Scheletro deployato su Fly con Postgres» — modello
- riga «Aggiunta da link con JSON-LD e elenco del ricettario» = «Aggiungi una ricetta da link e correggila dopo» — modello
- riga «Estrazione LLM quando il JSON-LD manca» = «Fallback LLM quando la pagina non ha JSON-LD» — modello
- riga «Aggiunta da testo incollato» = «Aggiungi una ricetta incollando il testo» — modello; diverge su theme (aggiunta-da-testo ≠ aggiunta-ricette)
- riga «Accesso con Google e scope autenticato» = «Accedi con Google e vedi i tuoi ricettari» — modello; diverge su theme (ricettari-condivisi ≠ identita), size (medium ≠ large)
- riga «Invito via link e ricettari condivisi» = «Invita nel ricettario con un link» — modello
- riga «Scrittura a mano e correzione» = «Scrivi una ricetta a mano» — modello; diverge su theme (scrittura-e-correzione ≠ aggiunta-ricette), size (medium ≠ small)
- riga «Foto della ricetta» = «Foto della ricetta con copertina» — modello
- riga «Messa in mano a famiglia e amici» = «Il ricettario in mano a famiglia e amici» — modello; diverge su size (small ≠ medium)
- out-of-scope «Ingredienti strutturati in quantità e unità» — meccanico
- out-of-scope «Deduplica delle ricette» — meccanico
- out-of-scope «Ruoli e permessi granulari» = «Permessi granulari dentro un ricettario» — modello
- out-of-scope «Qualunque provider di posta» = «Invio di email» — modello
- out-of-scope «Review obbligatoria dell'estratto» = «Review obbligatoria prima del salvataggio» — modello
- out-of-scope «Un secondo datastore» — non allineabile (solo ROADMAP-CC-6C)
- verdetto `ricerca-semantica / ricettari-condivisi` — solo ROADMAP-CC-6B
- verdetto `aggiunta-ricette / ricerca-semantica` — solo ROADMAP-CC-6C
- verdetto `aggiunta-ricette / foto` — solo ROADMAP-CC-6C
- verdetto `condivisione / foto` — solo ROADMAP-CC-6C
- verdetto `aggiunta-da-link / aggiunta-da-testo` (tema senza allineamento, ROADMAP-CC-6B)
- verdetto `aggiunta-da-testo / ricerca-semantica` (tema senza allineamento, ROADMAP-CC-6B)
- verdetto `ricettari-condivisi / scrittura-e-correzione` (tema senza allineamento, ROADMAP-CC-6B)
- verdetto `scrittura-e-correzione / foto` (tema senza allineamento, ROADMAP-CC-6B)
- verdetto `ricerca-semantica / identita` (tema senza allineamento, ROADMAP-CC-6C)
- verdetto `identita / condivisione` (tema senza allineamento, ROADMAP-CC-6C)
- archi concordi: 8
- arco «Ricerca semantica cross-lingua nel ricettario» → «Spike: la ricerca cross-lingua regge su ricette vere?» — solo ROADMAP-CC-6B
- arco «Scrittura a mano e correzione» → «Ricerca semantica cross-lingua nel ricettario» — solo ROADMAP-CC-6B
- arco «Foto della ricetta» → «Scrittura a mano e correzione» — solo ROADMAP-CC-6B
- arco «Messa in mano a famiglia e amici» → «Foto della ricetta» — solo ROADMAP-CC-6B
- arco «Aggiungi una ricetta da link e correggila dopo» → «Quale embedder regge la ricerca cross-lingua» — solo ROADMAP-CC-6C
