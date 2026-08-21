# S5 — Aggiungi da link: JSON-LD, fallback LLM, avanzamento reale

← [Register](../roadmap.md#now)

**Outcome:** Si incolla l'URL di un blog di cucina e la ricetta è dentro il ricettario in pochi
secondi, senza riscrivere niente e senza confermare niente, con un avanzamento che dice il passo che
sta davvero girando.

**Requested by:** `sources/goal.md`, «Da link» come caso più frequente e la progress bar sui passi
reali; `sources/arch-choices.md`, la cascata JSON-LD prima e LLM in fallback;
`sources/concepts.md`, la pipeline di estrazione.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi costruisce e prova l'app, sullo stesso ambiente deployato. Dopo questa riga può aggiungere una
ricetta trovata in rete incollando un indirizzo, che è il modo in cui le fonti dicono che verranno
aggiunte quasi tutte.

## Includes

- Il fetch della pagina con l'`HttpClient` di Effect, con timeout e un solo tentativo di ripetizione.
- Il motore di estrazione con i suoi due percorsi: JSON-LD `schema.org/Recipe` letto direttamente
  quando c'è, e modello economico con structured output quando manca.
- Un solo schema di uscita per entrambi i percorsi, validato con `Schema` e mai castato.
- `sourceUrl` salvato, `prepTime` e `tags` riempiti best-effort e mai richiesti.
- Il salvataggio immediato senza review, attraverso lo stesso percorso di scrittura della riga a
  mano, così che l'embedding venga derivato senza che questa riga lo riapra.
- L'avanzamento sui passi reali — scarico pagina, leggo ricetta, trovo ingredienti, salvo — dove ogni
  passo ha il suo timeout e il suo messaggio di fallimento.

## Verification

Sull'ambiente deployato, una pagina di blog con JSON-LD diventa una ricetta con titolo, ingredienti e
preparazione senza che venga fatta nessuna chiamata a modello, e il log lo dimostra. Una pagina senza
JSON-LD diventa una ricetta attraverso il modello, e quando l'uscita del modello non rispetta lo
schema viene rifiutata da `Schema` e il fallimento è mostrato invece che salvato. Una pagina dietro
paywall fallisce nominando il passo che è fallito, non con un messaggio generico. L'avanzamento
mostrato corrisponde ai passi realmente eseguiti, nel loro ordine, e non avanza mai a tempo: fermando
il fetch, l'avanzamento si ferma lì. La ricetta è nel ricettario nel momento in cui l'estrazione
finisce, senza nessuna schermata di conferma, ed è immediatamente cercabile con le altre. Su un
campione di venti blog reali si riporta quante volte ha vinto il JSON-LD, quante l'LLM, quante nessuno
dei due, il costo medio per estrazione e la p95 del tempo totale con la macchina fredda.

## Learning target

L'estrazione a due percorsi è abbastanza buona da essere la via d'ingresso più frequente: il JSON-LD
copre gratis il blog comune, e il modello economico copre il resto abbastanza bene che l'utente
corregga di rado invece che sempre.

## Excludes

- Nessun copia-incolla: è la riga successiva, ed è tenuta separata perché fallisce per una causa
  indipendente — ripulire testo arbitrario invece che scaricare una pagina.
- Nessuna foto salvata dalla pagina di origine: la riga delle foto possiede l'object storage da sola
  e aggancia lì questo percorso.
- Nessuna deduplica: i duplicati sono ammessi.
- Nessun import in blocco e nessun import da file di altre app.

## Open questions

—
