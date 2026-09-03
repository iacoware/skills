# S5 — Estrazione LLM: fallback senza JSON-LD e testo incollato

← [Register](../roadmap.md#now)

**Outcome:** Le pagine che il JSON-LD non copre entrano lo stesso: da sole quando la pagina si
scarica, incollandone il testo quando non si scarica.

**Requested by:** `arch-choices.md` (Estrazione contenuto — fallback LLM e copia-incolla che riusano
lo stesso motore) e `goal.md`, che dà il copia-incolla come fallback dichiarato per paywall e siti
JS-heavy.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi prova l'app su staging. Da qui nessun sito lo lascia a mani vuote: al più gli chiede di incollare
il testo.

## Includes

- Una seconda implementazione dell'estrattore aperto da `S4`: pulizia dell'HTML in testo e una
  chiamata a un modello cheap con output strutturato, decodificata con lo stesso `Schema` di `S4` e
  mai castata.
- Innesto automatico nella cascata: JSON-LD assente o non valido significa LLM, senza che l'utente
  scelga niente e senza che la barra cambi passo.
- Un secondo ingresso nella home: si incolla il testo di una pagina, si saltano fetch e JSON-LD e si
  va sempre su LLM, con la stessa barra meno il passo `Scarico la pagina`.
- Errori tipizzati distinti per il percorso LLM — risposta che non valida contro lo schema, timeout,
  quota esaurita — ognuno con il proprio messaggio, separato da "non ho trovato una ricetta".
- Il costo di ogni chiamata scritto nei log applicativi, così che il conto si possa leggere dopo
  invece di scoprirlo a fine mese.

## Verification

- Su cinque URL reali di blog senza JSON-LD, fra cui uno scelto perché è del tipo su cui
  `arch-choices.md` dice che Mealie fallisce, cinque ricette entrano con titolo, ingredienti e
  preparazione riconoscibili, e la barra non ha mai chiesto niente all'utente.
- Incollando il testo della pagina dietro paywall che ha fatto fermare `S4` al passo `Scarico la
  pagina`, la ricetta entra: il fallback che le sorgenti dichiarano chiude davvero quel buco.
- Quando il modello restituisce qualcosa che non valida contro lo schema non viene salvato niente, e
  il messaggio dice che la lettura non è riuscita, non che la pagina non contiene una ricetta.
- Il costo medio per ricetta è misurato su quelle dieci estrazioni ed è scritto: `arch-choices.md`
  promette frazioni di cent, e qui la promessa si conferma o cade.
- Su un URL con JSON-LD valido il conteggio delle chiamate a pagamento è zero: la cascata non
  scavalca il percorso gratuito.

## Learning target

Che un modello cheap con output strutturato validato estragga una ricetta usabile sia da HTML
ripulito sia da testo incollato a mano, a frazioni di cent per ricetta e abbastanza bene da reggere
la scelta di non mettere nessun passo di correzione prima del salvataggio.

## Excludes

- L'inserimento manuale a form vuoto: è già in `S3`, perché le sorgenti lo danno come lo stesso form
  dell'edit e non come un terzo motore.
- Un browser headless per i siti JS-heavy: le sorgenti risolvono quel caso col copia-incolla, che è
  qui.
- La foto della pagina scaricata o incollata → `S9`.
- L'embedding della ricetta estratta → `S6`.

## Open questions

- Quale modello e quale provider per l'estrazione. `arch-choices.md` dice "modello cheap,
  Haiku-class, con output strutturato validato": è una classe, non una scelta. La decisione fissa il
  meccanismo di output strutturato su cui questa riga costruisce la decodifica e il costo per ricetta
  che deve misurare.
