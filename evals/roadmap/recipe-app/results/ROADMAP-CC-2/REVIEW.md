# Review — ROADMAP-CC-2

Mappa: `.roadmap/` (12 righe, `S0`–`S11`, 6 temi). Transcript presente (`TRANSCRIPT.jsonl`, 150
righe): le regole di sessione sono giudicabili, non inconclusive.

Ordine seguito: validator → `EVALUATION-BRIEF.md` → `EVALUATION-RULES.md` (saltate *Revising an
existing map*, R-006, R-018) → `reference-roadmap/` con `REFERENCE-NOTES.md`. Nessun punteggio.
Nessun file toccato oltre a questo.

## Validator

`make validate-roadmap ROADMAP=evals/roadmap/recipe-app/results/ROADMAP-CC-2/.roadmap` → `OK`.
Nessun `ERROR`, nessun `WARNING`. La mappa resta un reperto: nulla è stato corretto.

## Violazioni

### Il brief

| Id | Dove | Cosa la falsifica |
|---|---|---|
| **H5** | Assente da tutta `.roadmap/` | React Query / TanStack Query non è nominato in nessuna riga, in nessun `Includes`, in nessun `Cross-functional concern`. Lo stack di H5 è completo su tutto il resto (Google OAuth `S7`, Postgres+pgvector `S1`, R2 `S8`, embedding cloud multilingue `S2`/`S6`, Next.js su Fly `S0`/`S1`, Effect `S3`, Drizzle `S3`/`S7`). *Nota: anche `reference-roadmap/` non lo nomina — vedi «Sul brief e sull'oracolo».* |
| **C1** | Nessuna riga di `Assumptions`, nessuna di `Open questions`, nessuno spike | Il lato di `concepts.md` è preso e mai dichiarato. `S3` consegna un form che non attraversa l'estrattore; `S5:12` cita `concepts.md` «§ Pipeline di estrazione: due ingressi, un solo motore» come `Requested by`, e i due ingressi sono URL e testo incollato — l'inserimento manuale è fuori dal motore. `arch-choices.md` § Estrazione contenuto («stesso motore e schema» anche per l'input manuale) non compare da nessuna parte. Grep su `Assumptions` per *estraz\|motore\|manuale\|schema*: zero occorrenze. |
| **C2** | `roadmap.md` § Assumptions, ultima riga (`ricerca`, `S2`, `S6`) + `S6-ricerca-semantica.md` | L'uscita formale c'è, ma la lettura non è nessuna delle tre risoluzioni che il brief elenca (chiamata per query, cache, precomputazione): è la ri-affermazione del vincolo — «Gli embedding si generano solo in aggiunta e in modifica, mai sulla query di ricerca». Poi `S6` consegna ricerca per similarità senza che nessun bullet di `Includes` dica come la query diventa un vettore, e la sua `Verification` certifica che «nessuna chiamata all'API di embedding parte durante una ricerca». La mappa pubblica la domanda e scrive la riga come se l'avesse risposta. |

Le voci A e N non producono violazioni: A1 (`S1` `needs-decision` + `Open questions` di riga), A2/A3
(`S2` e `S5` scelgono classe e non provider), A4 (`suspend` in `S1`, macchina calda in `LATER`),
A5/N3 (corpus di seed in `S2`, licenziato dal criterio 2), A6 (copertina dentro `S8`), A7 (nessun
passo di review), A8 (`S2` spike), A9 (`S4` misura la quota JSON-LD come learning target), A10 (fuso
in `S3`), A11 (criterio 5), N1 (riga di `Assumptions` sul costo), N2, N5, N6 — tutte a posto.
U1 → `S1`; U2 → riga di `Assumptions` sul costo + misura in `S1`, riletta in `S11`; U3 → `S2`;
U4 → `S4`; U5 → `S5`. Nessuna uncertainty resta senza uscita.

### Le regole

| Id | Dove | Cosa la falsifica |
|---|---|---|
| **R-008** | `roadmap.md` § Themes / § Assumptions | Verdetti di confine registrati per tre coppie soltanto (`ricette`/`import`, `accesso`/`condivisione`, `condivisione` vs. più ricettari). Il confine `foto`/`ricette` non ha verdetto e l'argomento di merge è reale: le foto si caricano dal form di `S3` e appartengono alla `Recipe` (`S8-foto-della-ricetta.md` § Includes, terzo bullet). |
| **R-009** | `roadmap.md` § Themes, riga `import` → `S4` | La promessa ha due metà — «Incolli il link di un blog … ; **quando il link non si lascia leggere, incolli il testo e finisce uguale**» — e il first validator ne consegna una. Il testo incollato è di `S5` (`S4` § Excludes, primo bullet, lo esclude esplicitamente). È la forma che la regola dichiara ⚠ failed. |
| **R-013** | `roadmap.md` § Assumptions | La clausola chiede che `Assumptions` registri cosa le righe prima del seam possono ignorare. Non c'è: il fatto sta in § Cross-functional concerns → Authorization («Fino a S6 il risolutore legge un id dalla configurazione») e in `S3` § Excludes, mai in `Assumptions`. Il resto di R-013 regge (seam in `S3`, risolutore unico nominato, rinvio dell'identità giustificato una volta nel criterio 5 contro l'evidenza nominata). |
| **R-015** | vedi C1 e C2 sopra | Due entry del brief non escono per una delle tre uscite: C1 per nessuna, C2 per una che non risolve. |
| **R-017 (a)** | `roadmap.md` § NOW, colonne `Depends on` di `S1`, `S2`, `S3` | Repository e scheletro sono pubblicati come archi: `S1`→`S0`, `S2`→`S1`, `S3`→`S1`. `drawing-the-map.md` § Hard dependencies: «What every row depends on is not published». |
| **R-017 (b)** | `roadmap.md` § NOW, `S6`, `S7`, `S8`, `S10` | Archi che sono ordine e non durezza. `S6`→`S5`: la ricerca semantica è verificabile sulle ricette di `S3`/`S4` e sul corpus di seed di `S2` — il fallback LLM non è un precursore insostituibile. `S7`→`S6`: l'accesso Google non ha bisogno della ricerca. `S8`→`S5`: la foto da link viene da `og:image`/JSON-LD, cioè da `S4`, non dall'LLM. `S10`→`S9`: più ricettari servono la `Membership` di `S7`, non l'invito. |
| **R-020 (a)** | `S3`, `S4`, `S7`, `S8`, `S11` § Learning target | Learning target doppi, due affermazioni indipendentemente confutabili unite da *e*. `S3`: il modello povero basta **e** il seam regge senza autenticazione. `S4`: quota JSON-LD **e** latenza dell'estrazione sincrona. `S7`: il seam regge alla sostituzione **e** Google da solo basta a far entrare una persona vera. `S8`: un solo adapter serve due alimentatori **e** il ricaricamento sta nel piano gratuito. `S11`: il percorso completo regge **e** costa quanto le assunzioni dicono. «One vertical outcome, one learning target. Both singular.» |
| **R-020 (b)** | `S8` § Learning target vs. § Verification | «costa abbastanza poco, in tempo di aggiunta e in spazio, da stare nel piano gratuito» non ha nessuna osservazione: la `Verification` conta foto, copertine, 404 e file orfani, e non misura né tempo né spazio né costo. «Checking that data exists does not demonstrate its quality, latency or cost.» |
| **R-020 (c)** | `S7` § Learning target vs. § Verification | «basta a far entrare una persona reale dal suo telefono» è verificato con due account Google in mano a chi sviluppa; nessun telefono e nessuna persona reale compaiono nella `Verification`. La mappa stessa dice altrove che il primo pubblico non-sviluppatore è `S11`. |
| **R-020 (d)** | `S9` § Learning target vs. § Verification | «nessuno chiede la sola lettura, e la parità completa fra membri non produce il danno» non è confutabile dalla consegna di `S9`: la `Verification` è tutta meccanica (token manomesso, token scaduto, doppia accettazione, scope A/B/C). |
| **R-022** | `S0-repository-e-pipeline-verde.md` § Includes, quarto bullet, con `readiness: ready` | Il bullet asserisce l'apertura dell'account presso il «provider LLM ed embedding» mentre `S5` § Open questions dichiara non scelti «quale modello e quale **provider**», e `S2` deve ancora scegliere il modello di embedding. L'`Excludes` di `S0` prova a separare provider da modello («il modello lo scelgono S5 e S2»), ma `S5` mette in questione anche il provider. Bullet che asserisce un lato di una decisione che nessuno ha preso; la `Verification` di `S0` («Ogni account della lista è aperto») non è eseguibile finché la scelta non c'è. |
| **R-024** | `S3-ricetta-a-mano.md` | Split warning non risolto e senza coesione nominata: quattro capacità distinte unite da *e* già nel titolo (elenco, lettura, scrittura, correzione) e due rischi materiali indipendenti (povertà del modello di ricetta, tenuta del seam di scope). `slice-rules.md` licenzia *create-and-edit* nella stessa riga, non l'aggiunta di elenco e lettura. Il resto di R-024 regge: ogni pipeline condivisa ha un proprietario dichiarato (embedding `S6`, storage `S8`, schema di estrazione `S4`/`S5`, risolutore di scope `S3`→`S7`→`S10`). |

## Verdi

- **R-002** — `S0`–`S11` per incremento, greenfield, nessun id riciclato (verificato anche dal validator).
- **R-007** — l'unica misura pura (U3) è coniata come spike `S2` e non lasciata dentro la riga che blocca. La regola è ⚠ failed altrove; qui il routing fa quello che il reading trova.
- **R-010** — `S0`, `S1`, `S11` portano `theme: —`.
- **R-011** — due righe distinte; `S1` raggiunge Postgres in TCP col driver reale, applica una migration non di dominio col runner in pipeline, abilita pgvector, e non porta entità di dominio, autenticazione né tenancy. Né *oversized* né *hollow*.
- **R-012** — lista numerata e ranked; le deviazioni da ampiezza-prima-di-profondità sono nominate dentro i criteri 3, 5 e 7 che le concedono.
- **R-014** — ogni riga prima dell'identità nomina il proprio pubblico («chi sviluppa e chi prova l'app sull'ambiente non pubblico»); nessun `Outcome` promette un utente che non può esistere; `S2` lascia `Audience` vuoto.
- **R-016** — l'unico `enabler` è `S0` e non risolve nessuna uncertainty.
- **R-019** — `S2`: `kind: spike`, `Audience` vuoto, dipendente (`S6` lo nomina), nessun timebox.
- **R-021** — `S0` è il prerequisito di repository che la skill prescrive, account e segreti compresi; non è enabler camouflage per quella clausola. (Il problema di `S0` è R-022, non R-021.)
- **R-023** — nessuna delle failure nominate: niente layer slices, niente fake verticality (il corpus di seed è A5), niente deferred safety (lo scope entra con `S3`, la sostituzione al seam è esplicitamente esclusa dalla failure), niente atomization, niente horizon dumping.
- **R-025** — le righe di `LATER` non portano id, colonne né documento, e ciascuna è ciò che non serve *questo* goal.
- **R-026** — tutte e sei le voci di `OUT-OF-SCOPE` sono scritte come licenza con il prezzo: *poiché X, l'implementazione può fare a meno di Y; il prezzo è Z*. È la parte meglio riuscita della mappa.
- **R-032** — nessun `.roadmap/` in piedi: la mappa è scesa subito, nessuna conferma chiesta, nessuna domanda fra un file e l'altro. Transcript: `mkdir` a #98, `roadmap.md` a #106, slice a #110–#130, zero domande.
- **R-033** — validator girato dopo la scrittura (#138): 5 `ERROR` (quattro dai backtick dentro due celle `Depends on`, il quinto — «S2: a spike needs a dependent» — conseguenza della cella `S6` illeggibile). Corretti con una sed e ri-validato a `OK` (#142–#143). Nessun `WARNING`, quindi niente da portare all'autore; la riga finale che dice «validatore verde, nessun warning» è vera.
- **R-035** — chiusura sulle quattro parti nell'ordine giusto e nient'altro: tabella `Themes`, register `NOW`, `Open questions`, percorso a `roadmap.md`. Nessun riassunto dei documenti, nessuna narrazione delle operazioni.

## Inconclusive o vacue

- **R-001** — greenfield: non c'è nulla di consegnato da chiedere. La sessione ha letto le fonti, controllato il project root (#61) e caricato entrambe le reference e entrambi i template prima di disegnare. Non c'è niente da segnare.
- **R-003, R-004, R-005** — nessun input contro un goal registrato: prima mappa contro un goal dichiarato nelle fonti.
- **R-034** — nessun handover chiesto né tentato; la sessione si chiude sul report.
- Saltate su richiesta: sezione *Revising an existing map* (R-027–R-031), R-006, R-018.

**Limite del transcript.** I blocchi `thinking` della sessione sono presenti ma redatti: `thinking: ""`
con la sola firma, su tutte le occorrenze. Non c'è passo di sanificazione che li tolga — `Makefile:27`
copia la sessione di Claude Code così com'è — quindi il ragionamento non è registrato all'origine.
Restano leggibili tutti gli **atti** (tool call, domande poste, ordine delle scritture, messaggio di
chiusura), che è ciò di cui R-001, R-032, R-033, R-034 e R-035 hanno bisogno: nessuna di quelle cinque
resta appesa. Quello che non si può leggere è l'intenzione, e conta per una domanda sola — su **C1**,
se lo sweep dei conflitti sia stato fatto e la riga poi non scritta, oppure non sia mai partito. Sono
due difetti diversi e il fix atterra in file diversi. Da questo reperto non si distinguono, e la
distinzione non cambia il verdetto sulla mappa: la riga manca comunque.

## Contro `reference-roadmap/`

Non è un target di diff. Su ogni differenza, quale delle due ha la ragione migliore.

**Dove il riferimento ha la ragione migliore.**

- **C2.** Il riferimento risolve nominando il meccanismo — «la query si embedda a ogni ricerca», leggendo il vincolo come di costo, «dove `arch-choices.md` lo mette anche lui». Il candidato afferma il vincolo e lascia `S6` senza meccanismo. Il riferimento è drawable, il candidato no.
- **C1.** Stessa lettura in entrambi (il form manuale non attraversa l'estrattore), ma il riferimento la scrive come riga di `Assumptions` con la ragione (`concepts.md` § inserimento-manuale, `S7`), il candidato non la scrive affatto. `REFERENCE-NOTES.md`: «one resolving silently is worse than one resolving wrongly and saying so».
- **`Depends on`.** Il riferimento non pubblica prerequisiti (`S1`, `S2`, `S6`, `S8` hanno `—`) e lo motiva. Il candidato li pubblica. Conferma R-017 (a).
- **Cosa le righe prima del seam possono ignorare.** Il riferimento ce l'ha come riga di `Assumptions` (`condivisione`, `S12`), il candidato lo lascia in `Cross-functional concerns`. Conferma R-013 e dimostra che il campo è riempibile.
- **`inserimento-manuale`.** Il riferimento fonde scrittura e correzione in `S7` e tiene elenco e lettura in un tema e in una riga a parte (`consultazione`, `S5`), con verdetto scritto. Il candidato le impila tutte e quattro in `S3` senza verdetto. Conferma R-024.

**Dove il candidato ha una ragione almeno pari, o migliore.**

- **Il differenziatore consegnato dopo gli alimentatori.** Il riferimento consegna indicizzazione e ricerca a `S3`/`S4`, prima che si possa aggiungere una ricetta. Il candidato misura sul seed a `S2` e consegna la ricerca a `S6`, dopo tutti e tre i percorsi di aggiunta, e lo motiva nel criterio 6 («chi apre una pipeline condivisa viene dopo tutti quelli che la alimentano, e la possiede da solo») — che è la clausola *A row that opens a pipeline or adapter shared by several paths follows every `NOW` row that feeds it*. Entrambe le ragioni sono dichiarate e ranked: è una scelta di forma, non un difetto. Il costo che il candidato paga è che la promessa esistenziale si consegna quinta; il costo che il riferimento paga è un `enabler` che indicizza prima che esista un percorso reale che produca ricette.
- **Accesso su URL pubblico.** Il candidato apre una `Open questions` che il riferimento non ha — chi può entrare quando l'app è pubblica, e chi paga le chiamate LLM di chi entra. È una domanda che cambia la forma della mappa (una riga in più prima del rilascio) ed è ben posta.
- **`OUT-OF-SCOPE`.** Il candidato ne ha sei contro quattro, tutte scritte come licenza, incluse «review obbligatoria» e «vector DB dedicato» che il riferimento non registra.
- **Spostamento di una ricetta fra ricettari.** Il riferimento lo tiene come `Open questions` di mappa; il candidato lo esclude esplicitamente in `S10` § Excludes. L'esclusione dichiarata è un'uscita legittima e più economica: non cambia la forma della mappa.
- **Fallimento totale dell'estrazione.** Il riferimento lo tiene aperto («si salva una ricetta parziale o non si salva niente»); il candidato decide — niente riga a metà — e lo dichiara come invariante in `Cross-functional concerns` → Operability e lo verifica in `S4` e `S5`. Non è nel brief, quindi non è C-anything; la decisione dichiarata regge.
- **Conteggio.** 12 righe contro 15, 6 temi contro 7. N6 licenzia entrambi.

**Differenze che non sono di nessuno dei due.**

- Il riferimento separa indicizzazione (`S3`, `enabler`) da ricerca (`S4`, `product`) e nota che un enabler non può validare una promessa; il candidato tiene tutto in `S6` `product`, che valida la promessa direttamente. Nessuna delle due viola R-009.
- Il riferimento ha `S13` (tag e tempo derivati) come riga a sé; il candidato li popola dentro `S4` e `S5` come best-effort e lo dice negli `Excludes` di `S6`. Coesione contro visibilità: nessuna delle due sbaglia.
- Nessuno dei due porta gli elementi «deliberatamente assenti» di `REFERENCE-NOTES.md`: niente tag di tema nei titoli, niente colonne ripetute nei documenti, niente date, stime o percentuali.

## Sul brief e sull'oracolo

Non è una violazione del candidato, ma va detto perché il report lo espone: **H5 elenca React Query,
e né il candidato né `reference-roadmap/` lo nominano.** O il vincolo è vero e il riferimento
congelato lo manca — nel qual caso il difetto sta nell'oracolo — o H5 chiede più di quanto una mappa
debba portare, e il difetto sta nel brief. Non si decide qui: la decisione su cosa cambiare viene
dopo il report, e in questa sessione né il brief né il riferimento né la mappa sono stati toccati.

Da tenere per un secondo run — che è anche l'unico modo di sciogliere la domanda su C1 lasciata
aperta qui sopra, perché un run solo non dà verdetto: **R-009** (`import` con la
promessa a due metà) e **R-015** su **C1** sono esattamente le due forme che `EVALUATION-RULES.md`
segna già ⚠ failed. Se cadono di nuovo, la domanda smette di essere se il modello ha avuto una
brutta giornata.
