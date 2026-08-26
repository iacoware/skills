# Review — recipe-app, manual-run-1

Mappa valutata: `.roadmap/` di questo run, letta come reperto e non corretta. Ordine di lettura:
validator, `EVALUATION-BRIEF.md`, `EVALUATION-RULES.md`, `reference-roadmap/` per ultimo.
Saltate per istruzione: la sezione *Re-truing an existing map* (R-027 … R-030), R-006, R-018.
Nessun punteggio.

## Validator

`make validate-roadmap ROADMAP=evals/roadmap/recipe-app/results/manual-run-1/.roadmap/` →
`OK`. Nessun `ERROR`, nessun `WARNING`.

## Il transcript non esiste

Di questo run non è stato conservato il transcript. Le regole che leggono la sessione — cosa ha
chiesto, cosa ha proposto, se ha girato il validator, come ha chiuso — sono **inconclusive, non
rosse**: R-001, R-003, R-004, R-005, R-031, R-032, R-033, R-034, R-035. Di R-002 l'artefatto copre
la metà leggibile (`S0`…`S10` contigui, `archive/` inesistente, nessun id riciclato); che il mint sia
stato high-water mark + 1 lo direbbe solo la sessione.

## Brief — violazioni

- **H5** — `React Query` non compare in nessun punto della mappa: `S0 Includes` elenca lo stack
  installato come «Next.js con App Router e TypeScript, Effect, Drizzle e Vitest», e nessuna riga di
  prodotto lo nomina dopo. Falsificato da `sources/tech-choices.md:34-36` («**@tanstack/react-query**
  per il data fetching dai client component») e da `sources/goal.md:100`, che lo elenca fra le scelte
  di stack. È l'unico elemento di H5 assente: Google OAuth (`S7`), Postgres+pgvector (`S1`), R2
  (`S9`), embedding multilingue cloud (`S2`/`S4`), Next.js su Fly (`S1`), Effect e Drizzle (`S0`)
  ci sono tutti.
- **C1** — il lato è preso in silenzio. `S3 Includes` consegna «un solo form condiviso da creazione e
  modifica» senza mai passare dall'estrattore, e `S6 Excludes` lo asserisce esplicitamente («Il form
  di inserimento manuale resta quello della riga a mano, invariato»): è la lettura di
  `concepts.md`, «Pipeline di estrazione». `sources/arch-choices.md`, «Estrazione contenuto» punto 3,
  dice l'opposto («Copia-incolla / manuale: saltano il JSON-LD, **riusano lo stesso motore e
  schema**»). In `Assumptions` non c'è nessuna linea per questo conflitto, in `Open questions`
  nemmeno, e nessuno spike lo precede. Prendere il lato è concesso; prenderlo qui non lascia traccia.

Le altre voci sono a posto: **C2** esce dalla porta giusta (`Assumptions` `S4`, che nomina la
lettura di costo e il perché); **U1**/**U2** vanno su `S1`, **U3** sullo spike `S2`, **U4** è
consegnata come misura dentro `S5` (licenziata da **A9**), **U5** è un'assunzione dichiarata su `S5`
(**A3**). **A6** licenzia la copertina in `NOW`, **A10** la fusione crea/modifica, **A11** la
posizione dell'identità, **N1**…**N6** non producono findings.

## Regole — violazioni

- **R-015** — stessa violazione di **C1**: il conflitto sull'inserimento manuale non esce da nessuna
  delle tre porte; il lato viene preso in un `Excludes` (`S6`) senza una linea da nessuna parte. È
  esattamente la forma che la carta della regola marca `⚠ failed`.
- **R-015** — `Assumptions`, seconda linea `S1`: «Le fonti nominano il driver come "postgres.js /
  node-postgres" senza sceglierne uno. La mappa **ne prende uno** e lascia che lo scheletro lo
  confuti». L'assunzione non nomina la lettura presa, quindi `S1` non può confutarla: la regola chiede
  «an `Assumptions` line **naming the reading taken** and why». `S1 Includes` dice «il driver Postgres
  standard su TCP — nessun driver serverless», che restringe ma non sceglie.
- **R-015** — `Assumptions`, la linea sul costo è taggata `—`. La regola chiede che «every line traces
  to a theme or an id» e `assets/roadmap-template.md` prescrive `[theme or id]`; `—` non è nessuno dei
  due. (Il contenuto è **N1** e non è un difetto: lo è la tracciatura.)
- **R-008** — theme compression sulle foto. `S9` è taggata `theme: ricettario`, la cui `Promise` è
  «Le ricette stanno in un posto solo: le scrivi come ti vengono, le rileggi, le correggi quando
  serve» — non promette niente sulle foto, che `S9 Outcome` invece consegna. Le foto sono
  cancellabili intere senza invalidare l'evidenza di `ricettario` (split test), e nessun verdetto di
  split o merge è registrato per quel confine: l'unico verdetto in mappa è quello su
  `identità`/`condivisione` in `Assumptions`. Il reference tiene `foto` come tema a sé.
- **R-017** — `S4 Depends on: S2, S3` — l'edge su `S3` non è hard. `S2 Excludes` dichiara che «del
  codice dello spike non sopravvive niente tranne il corpus e l'insieme di query, che diventano la
  fixture di regressione che la riga di ricerca riusa»: è precisamente il controlled input che, per
  la regola, impedisce a un predecessore di essere hard.
- **R-017** — sono pubblicate le dipendenze che ogni riga ha: `S1 ← S0`, `S2 ← S1`, `S3 ← S1`. La
  regola dice che «what every row depends on — the repository, the skeleton — is not published», e
  `drawing-the-map.md` *Hard dependencies* spiega perché. Nel reference `S1`, `S2`, `S6` e `S8`
  portano `—`.
- **R-020** — `S3 Learning target` non è singolare: «il minimo … regge una ricetta vera
  dall'inserimento alla correzione, **e** quel punto può reggere lo scope da subito così che
  l'autenticazione più avanti lo sostituisca in un posto solo». Il secondo claim non ha osservazione
  in `S3 Verification` (che esercita il filtro di scope, non il costo della sostituzione): è
  osservato in `S7 Verification` («Si riporta quanti file sono stati toccati per commutare il
  risolutore»), ed è alla lettera il `Learning target` di `S7`.
- **R-020** — `S5 Learning target` afferma che «il modello economico copre il resto abbastanza bene
  che **l'utente corregga di rado invece che sempre**». `S5 Verification` riporta quante volte vince
  il JSON-LD, quante l'LLM, il costo medio e la p95: nessuna osservazione del tasso di correzione, e
  nessun'altra riga lo misura. Il claim non è refutabile dalla consegna.
- **R-022** — `S1` è `ready` e `Includes` pubblica un lato: «Database Neon collegato». Le fonti
  lasciano il provider indeciso (`arch-choices.md`, «Datastore»: Neon o Supabase), la mappa lo
  risolve con una linea di `Assumptions` a livello mappa invece che sulla riga. Il brief **A1** dice
  dove appartiene: «It blocks the skeleton alone, so it belongs on that row as `needs-decision`
  rather than at map altitude», e `REFERENCE-NOTES.md` lo ribadisce; il reference porta `S1`
  `needs-decision`. La regola aggiunge che `Includes` e `Verification` devono deferire alla decisione
  pendente — qui `Verification` lo fa a metà («un fallimento qui è la confutazione dell'assunzione su
  Neon»), `Includes` no.

Verificate e verdi sull'artefatto: **R-002**, **R-007** (`S2` è lo spike che la misura chiedeva, e la
misura di `S5` è quella che **A9** licenzia dentro la riga), **R-009**, **R-010**, **R-011**,
**R-012**, **R-013**, **R-014**, **R-016**, **R-019**, **R-021**, **R-023**, **R-024**, **R-025**,
**R-026**.

## Reference — differenze che non sono violazioni

Letto per ultimo, non come target di diff. Su ogni differenza, quale delle due ha la ragione migliore:

- **Il differenziatore su dati seed.** Il reference consegna indicizzazione e ricerca (`S3`/`S4`)
  prima che qualcuno possa aggiungere una ricetta; la candidata mette `S3` a mano davanti a `S4`. Il
  reference ha la ragione migliore, ed è la ragione già registrata sopra come **R-017**: il corpus
  che la candidata conserva le sarebbe bastato.
- **Sette temi contro cinque, quindici righe contro undici.** Sul conteggio **N6** licenzia; l'unico
  confine che regge una critica è quello delle foto, sopra come **R-008**. `consultazione` fuso in
  `ricettario` è difendibile — elenco e lettura non producono feedback utile senza la scrittura.
- **L'identità.** Il reference la mette presto (`S6`) e fa dipendere la scrittura da lei; la
  candidata la rinvia a `S7` e istituisce il seam in `S3`. **A11** licenzia entrambe, e la ragione
  della candidata è migliore per la mappa che ha disegnato: `drawing-the-map.md` *The identity seam*
  prescrive esattamente quel seam, la candidata lo consegna con la prima riga che persiste dati, lo
  dichiara in `Cross-functional concerns` e ne verifica il costo in `S7`.
- **Import in due righe.** Il reference separa `S8` JSON-LD da `S9` fallback LLM per due learning
  target distinti; la candidata li fonde in `S5`. Il reference ha la ragione migliore, e la
  conseguenza è già registrata sopra come **R-020** (il learning target fuso porta un claim che
  nessuna verifica raccoglie).
- **Indicizzazione separata dalla ricerca.** Il reference splitta perché un `enabler` non può
  validare un tema; la candidata non ha quel vincolo, non usando un enabler lì. Pari.
- **Tag e tempo derivati.** Riga a sé nel reference (`S13`), riempimento best-effort dentro `S5`
  nella candidata. Pari: `concepts.md` § Recipe dice che «si popolano da JSON-LD o LLM», cioè solo
  sui percorsi che attraversano l'estrazione, ed è quello che la candidata fa.
- **`404` e mai `403`.** Il reference lo mette sotto `Cross-functional concerns`; la candidata dice
  solo «irraggiungibile anche conoscendo la sua URL» (`S3`) e «rifiutata» (`S8`). Il reference ha la
  ragione leggermente migliore — è una regola condivisa e verificabile — ma nessuna regola né il
  brief la esigono.
- **Due open questions contro tre.** Il reference pubblica «cosa succede quando l'estrazione fallisce
  del tutto» e «una ricetta si può spostare fra ricettari». La candidata decide la prima in `S5` («il
  fallimento è mostrato invece che salvato») e le dà un rimedio consegnato subito dopo con `S6`; la
  seconda non la solleva. Nessuna delle due è nel brief fra le incertezze materiali, e il brief è
  l'autorità: non sono violazioni, e sulla prima la ragione migliore è della candidata, che al posto
  della domanda consegna il recupero.

## Note sul checklist (non sono findings sulla mappa)

Tre punti dove il primo disegno delle regole non regge il peso, emersi mentre le applicavo:

- **R-021 contro il prerequisito del repository.** `S0` è `enabler` e non esercita «a real end-to-end
  production path»: per costruzione non può, dato che `drawing-the-map.md` gli vieta provisioning e
  deploy. Nessuno dei quattro `kind` calza la riga del repository, e candidata e reference la
  etichettano entrambe `enabler`. Questa è una clausola che dice due cose che si sovrappongono, non
  un fallimento del modello.
- **Nessuna regola guarda le quattro cose non-rankable.** «The cheapest real input that can validate a
  risky engine is the right one» è fra le clausole che `drawing-the-map.md` dichiara fuori dal
  ranking, ma R-012 controlla solo che una deroga sia *nominata*, non che sia *ammissibile*: qui la
  violazione è entrata di rimbalzo via R-017, e con un ordinamento diverso sarebbe passata.
- **I verdetti di split/merge fra righe non hanno lettore.** `slice-rules.md` chiede di leggere le
  righe adiacenti contro i due test «and record the verdict for each pair»; R-008 legge quei verdetti
  solo per i *temi*, e R-024 legge la conservazione del comportamento, non il verdetto. In questa
  mappa nessuna coppia di righe porta un verdetto registrato e nessuna regola lo rileva.
