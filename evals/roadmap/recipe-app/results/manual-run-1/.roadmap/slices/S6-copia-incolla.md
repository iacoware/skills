# S6 — Copia-incolla: la via d'uscita quando il link non si legge

← [Register](../roadmap.md#now)

**Outcome:** Quando la pagina è dietro paywall o non si lascia leggere, si seleziona il testo, lo si
incolla e si ottiene la stessa ricetta che il link avrebbe dato.

**Requested by:** `sources/goal.md`, il copia-incolla come fallback «quando il link non è leggibile
(paywall, siti JS-heavy)»; `sources/concepts.md`, i due ingressi su un solo motore di estrazione; il
fallimento che `S5` sa produrre e non sa ancora rimediare.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi costruisce e prova l'app, sullo stesso ambiente deployato. Dopo questa riga non resta più a mani
vuote quando un link fallisce: incolla il testo e la ricetta entra lo stesso, senza uscire dall'app e
senza riscriverla.

## Includes

- Un campo per incollare il testo nel flusso di aggiunta.
- La pulizia del testo incollato prima dell'estrazione: spazi, righe di navigazione, ingombro di
  contorno.
- Sempre il percorso del modello, mai il JSON-LD, sullo stesso schema di uscita e sullo stesso
  percorso di salvataggio dell'import da link.
- Il messaggio di fallimento dell'import da link che porta qui in un gesto solo, portandosi dietro
  l'indirizzo che non si è potuto leggere.
- Un tetto dichiarato alla lunghezza del testo accettato, con il rifiuto che lo nomina.

## Verification

Il testo di una pagina dietro paywall, incollato, produce la stessa ricetta che l'import da link
produce dallo stesso contenuto quando la pagina è accessibile: le due si mostrano affiancate. Un
testo incollato che non è una ricetta viene rifiutato con un messaggio, invece di essere salvato come
una ricetta vuota. Un testo oltre il tetto dichiarato viene rifiutato dicendo il tetto. La ricetta
così ottenuta è cercabile insieme alle altre e si corregge con lo stesso form. Dal fallimento
dell'import da link si arriva qui con un gesto, e l'indirizzo che non si è potuto leggere finisce in
`sourceUrl`. Il costo e la p95 dell'estrazione da testo incollato sono riportati accanto a quelli
dell'estrazione da link.

## Learning target

Il copia-incolla chiude davvero il buco che l'import da link lascia aperto: le pagine che il fetch non
prende sono recuperabili dall'utente senza uscire dall'app, e il modello su testo incollato e ripulito
lavora bene quanto su HTML scaricato.

## Excludes

- Nessun OCR, nessun PDF, nessun import da file: non sono nelle fonti.
- Nessun riconoscimento automatico fra indirizzo e testo nello stesso campo: sono due ingressi
  distinti, come le fonti li descrivono.
- Il form di inserimento manuale resta quello della riga a mano, invariato.

## Open questions

—
