# Ristrutturare EVALUATION-BRIEF — proposta e ragioni

Esito di una sessione di ragionamento (2026-08-31) su `evals/roadmap/recipe-app/EVALUATION-BRIEF.md`.
Il problema di partenza: il brief confonde a ogni lettura, e l'introduzione non aiuta perché è troppo
lunga e non viene letta. Spiegare di più non è la soluzione; la chiarezza deve venire dalla struttura.

## Diagnosi

**Il brief è organizzato per cinque lettere e quattro sezioni, ma il lettore ha solo tre azioni.**
Le sezioni attuali nominano proprietà della mappa (dove può differire, cosa lascia aperto, cosa sembra
un difetto, cosa contiene); il reviewer arriva con una domanda sola — *cosa faccio con questa voce?* —
e le risposte possibili sono tre, non cinque:

| Azione del reviewer | Lettere | Chi può fallire |
|---|---|---|
| **Spunta** — deve esserci, o è difetto | H | il run |
| **Verifica l'uscita** — deve restare aperto; il difetto è risolverlo in silenzio | C, U | il run (uscita mancante) **e** la review (segnare il lato, che è libero) |
| **Non segnare** — licenza, blocca un rilievo | A, N | solo la review |

I fatti che reggono la diagnosi, stabiliti uno per turno:

- **Regole e brief hanno oggetti diversi.** Una R-xxx è un predicato quantificato sul run, senza
  costanti: viaggia. Il brief lega le costanti di questo scenario su cui quei predicati quantificano:
  resta. Se il brief fosse scritto come elenco di check, predicato e costanti si fonderebbero e un
  secondo scenario dovrebbe riscrivere anche il predicato, che poi drifterebbe rispetto alle regole.
- **Il brief incapsula costanti delle sole `sources/`, mai del reference.** `sources/` → brief (fatti)
  e `sources/` → reference (gusto) sono derivati paralleli; l'unica voce che nomina il reference è N6,
  e lo fa per de-autorizzarlo come target di diff.
- **A e N non trovano violazioni: impediscono di inventarne.** Congelano il giudizio nei punti dove
  ogni review ri-litigherebbe le sources da capo («answered once so that no review re-litigates
  them»). Non si contano nel tally perché la mappa non può fallirle: può sbagliare solo la review,
  segnando ciò che licenziano. Un falso positivo non resta nel REVIEW — fluisce in IMPROVEMENTS e da
  lì in modifiche alla skill per correggere un non-difetto.
- **Le N sono licenze ri-enunciate nel punto della trappola.** N3 dice letteralmente «is A5 plus the
  ranking»; N2→H6, N5→R-010, N6→cap. La duplicazione A↔N è by design.
- **Ogni C/U è una voce composta**: una metà obbligo sul run (l'uscita registrata — consumata da
  R-015, più R-016 via la colonna `Subsystem` delle U e R-022 per i piazzamenti a livello di riga) e
  una metà licenza sulla review (il lato e l'uscita sono liberi). Il brief stesso ha già fattorizzato
  la metà licenza delle U in A compagne: U1↔A1, U2↔A4, U3↔A2+A8, U4↔A9, U5↔A3. Oggi le due metà
  della stessa voce stanno a trenta righe di distanza, ed è una buona parte della confusione.
- **Lato review non esiste nessun consumatore falsificabile.** Se una review segna una differenza che
  A5 licenzia, niente lo rileva se non la rilettura umana.
- **La ground truth dell'autore entra nell'eval solo se derivabile dalle sources.** La sessione che
  disegna vede solo `sources/`; un brief che codificasse una verità che le sources non selezionano
  punirebbe il modello per non aver letto nel pensiero dell'autore. C2 è affilabile (le sources
  selezionano la lettura di costo: «le query sono irrilevanti» falsifica la restatement
  architetturale); C1 no (niente nel testo dice quale source sbaglia). Decisione presa: **si lascia
  tutto com'è** — l'ambiguità di C1 è materiale di test load-bearing, l'esemplare `⚠ failed` di
  R-015. Nota a margine su C1: «deve comunque vettorizzare» non seleziona il lato di arch-choices,
  perché l'embedding avviene al save su ogni percorso (H4) ed è a valle dell'estrazione; la lettura
  probabilmente vera è *schema condiviso, motore saltato*, che concilierebbe le due sources.

## Proposta

Ristrutturare il brief senza toccare né gli id (lettere e numeri sono l'API stabile, citata nei
REVIEW storici) né il contenuto delle voci.

1. **Tre sezioni intitolate con l'azione del reviewer**, in quest'ordine: *Spunta* (le H, la tabella
   di oggi, promossa in cima — è il segnale più forte e oggi è sepolta in fondo), *Verifica l'uscita*
   (C + U), *Non segnare* (A + N fuse in un elenco unico).
2. **Colonna `Licenze` sulla tabella U**, con i puntatori alle A compagne (`A1`, `A4`, `A2 A8`, `A9`,
   `A3`). Puntatori, non testo spostato: il lettore vede la voce intera in una riga, gli id restano
   dove sono. C1 e C2 hanno già la metà licenza inline.
3. **La meta-regola come testata di *Non segnare***: «nessun rilievo resta in piedi contro una voce
   di questa sezione». Così A/N acquistano il consumatore falsificabile che oggi manca, senza
   aggiungere una R: la sezione *è* il check sulla review.
4. **Intro ridotta a ~2 righe** («Fatti su `sources/`, un id stabile per voce; cita l'id, mai la
   parafrasi»). Il resto dell'intro attuale sono regole di workflow — l'autorità sulle sources, cosa
   il brief non decide, gli id mai riusati — e trasloca in `REVIEW-WORKFLOW.md`, che il reviewer sta
   già camminando. Non è spiegare di più: è spostare la spiegazione dove viene già letta.
5. **Il paragrafo sulle tre uscite** in testa all'attuale «What it must leave open» duplica R-015 e
   `drawing-the-map.md`: si riduce a un puntatore a R-015.

### Perché

- Le tre sezioni coincidono con il confine logico del sistema (chi può fallire: run / entrambi /
  review): il lettore che entra in una sezione sa già chi sta giudicando, senza leggere alcuna intro.
- Le stesse tre sezioni coincidono con i bucket del tally (H si contano; C/U contano sotto la regola
  che istanziano; A/N non si contano): la struttura insegna da sola la regola di conteggio.
- È sicuro: verificato che niente cita i *titoli* di sezione del brief — prompt, workflow e review
  citano solo le lettere. I titoli sono liberi di cambiare; gli id non cambiano.

### Alternative scartate

- **Split in più file** (fatti vs licenze): la review legge il brief in un passaggio; la navigazione
  costerebbe più della lunghezza.
- **Spezzare ogni C/U nelle due metà** con id separati: raddoppia gli id per formalizzare una
  distinzione che la colonna `Licenze` e una riga di testata già insegnano.
- **Raggruppare per argomento** (tutte le voci sull'estrazione insieme): ottimizza la lettura
  sequenziale ma rompe la corrispondenza sezione↔azione↔bucket-del-tally.
- **Marcatore di polarità per voce** (`DEVE`/`APERTO`/`LECITO`): con le sezioni giuste è ridondante.
- **Codificare nel brief il lato giusto di C1 lasciando le sources in conflitto**: l'unica mossa
  vietata dal principio della ground truth.
