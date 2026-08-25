# Review — ROADMAP-CC-3

Mappa: `.roadmap/` — 11 righe, 6 temi, greenfield, un solo turno d'autore.
Letti in quest'ordine: validator, `EVALUATION-BRIEF.md` con la mappa in mano, `EVALUATION-RULES.md`
regola per regola (saltate *Revising an existing map*, R-006, R-018), `TRANSCRIPT.jsonl` (125 righe),
e per ultima `reference-roadmap/` con `REFERENCE-NOTES.md`.

Il transcript c'è: le regole di sessione sono giudicabili, non *inconclusive*.

## Validator

```
make validate-roadmap ROADMAP=evals/roadmap/recipe-app/results/ROADMAP-CC-3/.roadmap
OK
```

Nessun `ERROR`, nessun `WARNING`. Il registro sta fra floor 3 e cap 20.

## Violazioni

| Id | Dove | Che cosa la falsifica |
|---|---|---|
| **C1** (e **R-015**) | `S3` § Excludes, primo punto: «Ogni estrazione da link o da testo incollato: sono i temi dell'import» | Il conflitto è risolto lì e da nessun'altra parte: nessuna riga di `Assumptions`, nessuna `Open questions`, nessuno spike. `arch-choices.md:43` dice «Copia-incolla / **manuale**: saltano il JSON-LD, riusano lo stesso motore e schema»; la mappa prende la lettura di `concepts.md:123` («salta l'estrazione») dentro un `Excludes`. È esattamente la forma che R-015 marca ⚠ failed — «the side gets taken in an `Excludes` bullet with no line anywhere» — e il reference, che prende la stessa lettura, la dichiara in `Assumptions` (`inserimento-manuale, S7`). |
| **H5** | Nessun documento della mappa | React Query manca. `grep -ri "react query\|react-query\|tanstack" .roadmap/` non restituisce nulla; `S0` § Includes elenca Next.js, TypeScript, Effect, Drizzle, vitest, Prettier e si ferma lì. `tech-choices.md:34-36` gli dedica una sezione («Data fetching client — TanStack React Query») e `goal.md:100` lo nomina fra le scelte di stack. Ogni altra voce di H5 è presente. |
| **R-015** | `Assumptions`, riga `S4, ricerca` | L'uscita è quella giusta e la lettura è ammessa da C2, ma il *perché* è smentito dalle sue stesse citazioni. La riga dice «si legge il divieto come riferito all'estrazione LLM, non all'embedding della query»: `arch-choices.md:33` sta dentro `## Embeddings` e il suo soggetto è il modello di embedding, e `goal.md:110-111` scrive «LLM/embedding usati **solo in fase di add** … mai a runtime sulle query di ricerca», nominando i due insieme. Il divieto parla proprio dell'embedding della query. La ragione buona — quella che il reference usa — è che è un vincolo di costo e non di architettura, e la mappa ce l'ha in mano (cita «le query sono irrilevanti») ma non la usa. |
| **R-009** | `Themes`, riga `import`, first validator `S6` | La promessa ha tre clausole («incollo il link, o incollo il testo …, **e vedo i passi reali dell'estrazione**») e `S6` non ne osserva la terza: la sua `Verification` verifica pagina-senza-JSON-LD → ricetta salvata, testo incollato → ricetta equivalente, quota di output non validi, costo. I passi reali compaiono solo nell'`Includes` di `S6` e sono osservati solo dalla `Verification` di `S5` («i passi avanzano in momenti diversi: la barra segue il lavoro e non un timer»). È la forma che R-009 marca ⚠ failed: o una clausola era di troppo, o il validator è la riga sbagliata. |
| **R-017** | `NOW`, `S4`, `Depends on` = `S2` | Manca l'arco duro `S4 → S3`. `S4` § Includes aggiunge la colonna `embedding` in migrazione sulla tabella `recipe`, fa backfill «per le ricette già salvate» e filtra la query di similarità «dal resolver `currentCookbook`»: tabelle e resolver li consegna `S3`, e nessun input controllato li sostituisce. Nessun criterio di ordinamento dà quella ragione — il criterio 2 argomenta il contrario, che «la ricerca apre prima di import, identità, condivisione e foto» — quindi qui il `—` non è la deroga che R-017 licenzia, è l'arco che un riordino romperebbe senza che nessuno se ne accorga (⚠ opposite). |
| **R-035** | Messaggio di chiusura (transcript, ultimo turno assistant) | Due scarti. Prima delle quattro parti c'è una riga di narrazione dell'operazione — «Validatore: `OK`, nessun ERROR né WARNING» — e il validator non aveva niente di dovuto da riportare. Dopo le quattro parti non c'è nulla, ma la sessione aveva prodotto due domande che non ha risposto e che non arrivano all'autore: `S8` è `needs-decision` (link aperto o vincolato all'indirizzo) e `S10` è `needs-info` (chi possiede gli account di produzione, su quale dominio). Vivono nei documenti delle righe e restano lì. |
| **R-015** (minore) | `Assumptions`, riga `S1, goal` (Neon) | Sovra-scopata. Il brief A1 dice che la scelta del provider «blocks the skeleton alone», e `drawing-the-map.md` ammette il tag `goal` solo «where what it touches is the whole map and no theme or row owns it». La riga accanto (`S1, goal`, il target di costo) il tag `goal` se lo merita; questa no. La scelta di Neon in sé non è una violazione: la mappa cita `tech-choices.md:43`, che nomina Neon decidendo il driver, e una sorgente che seleziona risolve la voce. |

## Non violazioni, ma da discutere

- **R-020, `S5`.** Due bersagli d'apprendimento in una riga: «che l'estrazione sincrona con progresso reale sia sostenibile» e «quanto spesso il solo JSON-LD basti». Falliscono per cause indipendenti che cambiano decisioni diverse — lo streaming ripiega su polling (lo dice l'assunzione `S5, import`), l'hit-rate sposta l'LLM prima o dopo — che è la split warning di `slice-rules.md`. A9 licenzia la *misura* dell'hit-rate su una riga ordinaria, non il bersaglio doppio. È l'unica riga `large` di prodotto della mappa.
- **R-021, `S0`.** `kind: enabler` non passa il test dell'enabler alla lettera: non attraversa nessun percorso di produzione end-to-end, e lo dichiara («Ogni provisioning e ogni deploy: appartengono allo scheletro»). Ma `drawing-the-map.md` § *The two prerequisites* impone proprio quella riga con «no provisioning, no deploy», e nessuno dei quattro `kind` le calza. Due clausole della skill che si contraddicono, non un difetto del run: per il preambolo delle regole il fix, se c'è, sta in `references/`, non qui.
- **R-013, criterio 5.** L'evidenza nominata («finché la misura sull'embedder e la ricerca sul corpus reale non hanno dimostrato il cross-lingua») è esaurita a `S4`, e `S5` e `S6` consegnano comportamento prima di `S7`. La clausola della skill però vieta solo le righe successive «whose acceptance depends on real ownership or membership», e l'estrazione non ci dipende; A11 licenzia il piazzamento. Resta che il criterio 5 si chiude con «l'identità è la prima riga dopo l'import» senza dire perché l'import stia dentro la deroga.

## Verde, e vale la pena registrarlo

- **R-007** (⚠ failed 3/3 su scenario 3). Qui non fallisce. L'unica misura senza esito consegnabile — U3, il cross-lingua — è coniata come spike `S2`, con dipendente `S4`. La misura di U4 sta dentro `S5` come bersaglio di una riga ordinaria, che è la seconda uscita che A9 ammette esplicitamente.
- **R-017, metà «false edge».** Due archi pubblicati, `S4 → S2` e `S8 → S7`, entrambi duri. I quattro archi che i criteri 3, 4 e 7 già motivano — `S5 → S3`, `S6 → S5`, `S9 → S5` — sono correttamente `—`, che è precisamente il *published order* che `drawing-the-map.md` chiede di non pubblicare. Su questo la mappa è più stretta del reference, che pubblica `S9 → S8`, `S10 → S9` e `S11 → S8` nonostante il suo criterio 4 ne dia già la ragione.
- **R-026.** Tutte e otto le voci di `OUT-OF-SCOPE` sono scritte come licenza, con la forma «poiché X, nessuna riga deve Y: il prezzo è Z». Nessun cimitero.
- **R-025.** Le dodici righe di `LATER` non hanno id, colonne né documento, e nessuna è comportamento obbligatorio parcheggiato: cancellazione ricetta, revoca invito, ridimensionamento foto e import da Paprika/Mealie non sono chiesti da nessuna sorgente (`grep -i "cancell\|elimin\|revoc\|compress" sources/` non trova nulla di pertinente).
- **R-033.** Il validator è girato dopo la scrittura, ha dato un `ERROR` (`'Depends on' names '—'`, il carattere dentro backtick), è stato corretto con un `sed` sul solo registro e rigirato fino a `OK`. Nessun `WARNING` da mettere all'autore.
- **R-032.** Nessuna `.roadmap/` in piedi: la mappa è stata scritta subito e senza chiedere conferma, in tre scritture (registro, `S0`–`S4`, `S5`–`S10`), non un file alla volta con una domanda in mezzo.
- **R-001, R-002.** L'input dichiarava greenfield e diceva di creare la directory, quindi la domanda su cosa fosse stato consegnato era già risposta; il check di filesystem è stato piegato dentro il `mkdir -p … && ls -a`, che ha restituito la directory vuota. Ids da `S0` a `S10`, minted da niente, nessuno riciclato.
- **Brief.** H1 (`S4`), H2 (resolver in `S3`, filtro in `S4`, membri pari in `S8`), H3 (`S5` → `S6` → form di `S3`), H4 (`S5`/`S6` salvano senza review, `S4` rigenera l'embedding a ogni correzione), H6 (tutte e cinque in `LATER`, i ruoli anche in `OUT-OF-SCOPE`), H7 (`S1`), H8 (`S10`) sono tutte coperte. C2 esce per la porta giusta (la ragione è il difetto, non l'uscita). U1 e U2 su `S1`, U3 sullo spike `S2`, U4 su `S5`, U5 su `S6`: nessuna uncertainty resta senza collocazione, e nessun enabler ne risolve due di sottosistemi diversi (R-016 — l'unico enabler è `S0`, che non ne tocca nessuna). Nessuna voce A o N è violata: A5/N3 coprono la ricerca su corpus seed, A6 la copertina in `NOW`, A7 la scelta delle foto rimandata, A8/A9 le uscite di U3 e U4, A11 l'identità dopo l'import, N2 i ricettari pubblici in `LATER`, N5 i tre `theme: —`, N6 le 11 righe contro le 15 del reference.

## Vacue o non giudicabili in questo run

R-003, R-004, R-005 (nessun input da riconciliare: un solo turno d'autore, greenfield);
R-027, R-028, R-029, R-030, R-031 (nessuna mappa in piedi, e la coverage question è vacua su
`Drawing`); R-034 (nessun handover chiesto e nessuno offerto);
R-006 e R-018 saltate su richiesta.

## Contro il reference — differenze, non difetti

Ordinate dalla più discutibile alla meno.

1. **`consultazione` come tema a sé.** Il reference gli dà un tema e un first validator (`S5`, elenco e lettura sul corpus seed); il candidato lo fonde dentro `ricettario` («Scrivo … la ritrovo nell'elenco … e la correggo»). Il candidato non registra un verdetto su questo confine perché il tema non lo disegna. La ragione del reference è che sfogliare è cancellabile lasciando in piedi la scrittura, e la sua evidenza regge da sola su dati seed. La ragione del candidato è implicita: senza lettura non si verifica la scrittura. La prima è argomentata, la seconda no — punto al reference, ma non è un difetto di regola.
2. **Autorizzazione: 404 o rifiuto esplicito.** Reference: «un id fuori dallo scope del chiamante risponde 404 e mai 403 — l'esistenza di una ricetta altrui non si rivela». Candidato, `S7` § Verification: «riceve un rifiuto esplicito, non una pagina vuota che si può scambiare per "non ci sono ricette"». Il candidato risolve un problema di UX creandone uno di leak: il rifiuto esplicito conferma che la ricetta esiste. Nessuna sorgente decide, ma la ragione del reference è più forte.
3. **Indicizzazione separata dalla ricerca.** Il reference le splitta (`S3` enabler, `S4` product) per far esistere l'indice contro dati veri prima che ci sia una casella di ricerca da discutere. Il candidato fa una riga sola. Entrambe stanno in piedi; il candidato evita un enabler che dovrebbe passare il test dell'enabler, il reference guadagna un gradino di apprendimento in più.
4. **Provider Postgres.** Reference: `S1` `needs-decision`, il provider «blocks `S1` alone». Candidato: `S1` `ready` più una riga di `Assumptions` che cita `tech-choices.md:43`, dove Neon è nominato decidendo il driver. `drawing-the-map.md` dice che «only a source that selects resolves an entry»: se quella riga seleziona, il candidato ha la ragione migliore e il reference sta pubblicando come indecisa una scelta fatta. Resta lo scopo `goal` di troppo, già segnato sopra.
5. **`Depends on`.** Il candidato ne pubblica 2 su 11 righe, il reference 9 su 15. Sui quattro archi che i criteri già motivano il candidato è nel giusto (vedi *Verde*); su `S4 → S3` il reference è nel giusto e il candidato no.
6. **Due `Open questions` che il reference ha e il candidato no.** Che cosa succede se l'estrazione fallisce del tutto — il candidato la risponde in `S6` § Verification («Un output non valido non salva nulla di parziale»), che è una risposta e non un silenzio. Se una ricetta si possa spostare fra ricettari — nessuna sorgente lo chiede, quindi non è comportamento in scope e R-024 non lo reclama. Nessuna delle due è una violazione.
7. **`LATER`: 12 righe contro 6.** Nessuna delle sei in più è comportamento obbligatorio parcheggiato. Differenza di ampiezza, non di regola.
