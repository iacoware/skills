# Reference plan — note

**Parcheggio temporaneo.** Questo file esiste perché `REFERENCE-PLAN.md` è diventato un esemplare
conforme al template dello skill e non può più ospitare materiale che il template non prevede. Dove
ciascuna sezione vada davvero — `../MANUAL-REVIEW.md`, `EVALUATION-BRIEF.md`, o qui — è una
decisione ancora da prendere. Finché resta aperta, niente va perso.

## Regole d'uso del reference plan

Duplicano il punto 5 del loop in `../MANUAL-REVIEW.md`; se restano lì, qui si cancellano.

- Scritto a mano dalle sole `sources/` e prima di aver visto qualunque piano generato. È il gusto,
  non la regola: le regole stanno in `../MANUAL-REVIEW.md`, i fatti sulle fonti in
  `EVALUATION-BRIEF.md`.
- Serve a una cosa sola, che nessun altro artefatto fa: impedire alla misura di «buono» di derivare
  verso l'ultima cosa che un modello ha prodotto. Per questo è congelato. Si riscrive solo se
  cambiano le fonti — mai perché un candidato ha convinto.
- Leggi il candidato e formulane il verdetto prima di aprire il reference. Poi confronta, e su ogni
  differenza chiediti chi dei due ha la ragione migliore. Non è un diff da azzerare: titoli,
  numerazione, numero di temi, ordine e dettaglio d'esempio possono divergere tutti senza che nulla
  sia rotto. Serve a farti notare cosa hai dimenticato, non cosa hai fatto diverso.
- Le fonti prevalgono sempre. Dove il reference e `sources/` divergono, il difetto è nel reference.
- Ogni bullet di `Verification` illustra come si dimostrerebbe la slice: è un esempio, non il solo
  modo.
- Le sei voci di `Cross-functional concerns` sono dovute; la formulazione e il dettaglio operativo
  sono un modo di dirle, non l'unico.
- I `Decision checkpoints` sono consigliati, non una precedenza esatta.
- `LATER` e `OUT-OF-SCOPE`: una fonte può sostenere una classificazione diversa da questa.

## Vincoli che il reference tratta come non negoziabili

Quattro sono anche in `EVALUATION-BRIEF.md` § `Hard constraints`; gli altri quattro — idempotenza,
salvataggi parziali e SSRF, backup e tetti di spesa, separazione CI/skeleton — stanno solo qui.

- Repository/CI e walking skeleton sono separati; lo skeleton usa deploy, database reale e migration
  runner con operazioni non di dominio, senza CRUD, autenticazione o tenancy.
- La pipeline reale di indicizzazione precede il validatore di ricerca; la ricerca semantica
  cross-lingua precede l'acquisizione perché è il rischio esistenziale dichiarato.
- Il confine di scope si applica dalla prima persistenza tramite un resolver unico; l'identità lo
  sostituisce allo stesso seam prima della prima audience reale.
- Il primo accesso autenticato crea il primo ricettario in modo idempotente.
- L'import URL prova prima JSON-LD; l'LLM è recovery automatico dello stesso flusso; il testo
  incollato è il successivo escape manuale.
- Output non validi, timeout o fallimenti esterni non producono salvataggi parziali; URL remoti
  applicano protezione SSRF.
- `NOW` raggiunge utenti selezionati in produzione, con backup ripristinabile e limiti/allarmi di
  spesa per LLM ed embedding.
- La contraddizione sull'embedding della query e le scelte provider/modello restano esplicite e
  bloccano le slice indicate finché non risolte.

## Ordinamento e decomposizione preferiti

- Un enabler di dominio minuscolo valida persistenza, resolver di scope, shell, UI e test prima
  dell'indicizzazione.
- La pipeline di indicizzazione è immediatamente adiacente alla ricerca.
- Una form condivisa di inserimento e modifica precede il primo import.
- Le foto arrivano dopo l'acquisizione testuale e hanno un solo owner della pipeline media e della
  cover.
- L'invito è l'ultimo tema di prodotto.
- Il `NOW` completo è consegnabile a utenti selezionati: le slice 0–5 servono sviluppatori e
  revisori umani, dalla 6 ogni incremento è utilizzabile da utenti reali.

## Perché ogni slice sta dove sta

`SKILL.md` § 5 vieta di pubblicare rationale d'ordine per slice, quindi queste righe sono uscite dal
piano. L'ordine delle slice e `Ordering criteria` le sostituiscono; restano qui perché sono il
ragionamento che il confronto con un candidato mette alla prova.

| Slice | Perché lì |
|---|---|
| 0. Repository e CI | Stabilisce la cadenza di revisione prima che esista codice da rivedere. |
| 1. Walking skeleton | Prova che l'infrastruttura decisa è connessa sul path più sottile possibile, prima che un fallimento di connessione si confonda con uno di dominio. |
| 2. Contesto del ricettario | Prima persistenza e prima revisione di dominio, scope, ORM, UI e test su un comportamento minimo; Postgres è già provato dalla 1 e questa slice non è una dipendenza della ricerca. |
| 3. Pipeline di indicizzazione | L'input più economico capace di validare il motore rischioso, senza attendere le slice di aggiunta. |
| 4. Ricerca semantica | Rischio esistenziale, validato appena la pipeline lo rende osservabile. |
| 5. Lettura della ricetta | Completa il tema Consultazione sul contenuto reale e serve ogni tema successivo, restando minuscola. |
| 6. Accesso Google | Il resolver di scope passa da configurato ad autenticato prima che il prodotto arrivi a utenti reali; da qui ogni slice è consegnabile. |
| 7. Inserimento manuale | Stabilisce la form condivisa e il percorso salva + reindicizza che tutte le slice di import riusano come superficie di correzione. |
| 8. Import da URL | Caso di acquisizione più frequente e percorso gratuito, prima di qualunque costo variabile. |
| 9. Fallback LLM | Secondo differenziatore, subito dopo il percorso gratuito che ne delimita l'uso. |
| 10. Testo incollato | Chiude il tema Import automatico riusando motore e schema della 9, senza aprire adapter nuovi. |
| 11. Foto | Input diversi su una sola pipeline media, aperta una volta sola quando l'acquisizione testuale è chiusa. |
| 12. Invito | Ultimo tema, unico che richiede identità già presente. |
| 13. Rilascio | Senza questa slice `NOW` non raggiunge mai gli utenti dichiarati e il vincolo di costo non viene mai misurato sul campo. |

## Tensioni note con le fonti

Ambiguità o incompletezze delle fonti, dove scelte diverse sono legittime quanto quelle del
reference a patto che conservino le condizioni indicate. Il reference non risolve le decisioni
elencate in `Open questions`; sulle altre tensioni, un piano che sceglie diversamente si giudica
sulla motivazione.

- **Cover cambiabile:** `goal.md:74` la dichiara, il reference la mette in `LATER` come rifinitura di
  un default già spedito. Un piano che la tiene in `NOW` non è in errore se la mantiene dentro la
  slice 11.
- **Scelta delle foto durante l'import:** interazione a tempo di add, in tensione con "nessun passo
  obbligatorio prima del salvataggio" (`concepts.md:144`). Il reference la rinvia.
- **Embedding della query a runtime:** il reference non sceglie un'interpretazione; un piano corretto
  espone la contraddizione, le slice bloccate e non afferma contemporaneamente entrambe le
  condizioni.
- **Promozione in produzione:** il reference applica la prescrizione dello skill e usa
  `(Release: delivery)`; ometterla o riclassificarla in silenzio è un errore.
- **Provider aperti:** Postgres (Neon o Supabase), modello di embedding e modello LLM restano
  decisioni non prese nelle fonti. Vanno in `Open questions` con la slice che bloccano, mai scelte
  in silenzio dentro una slice.
