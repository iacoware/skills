# S5 — Aggiunta da testo incollato

← [Register](../roadmap.md#now)

**Outcome:** Quando il link non è leggibile, incollo il testo della pagina e ottengo la stessa
ricetta che avrei ottenuto dall'URL.

**Requested by:** `sources/goal.md` § Visione, punto 3 — copia-incolla come fallback per
paywall e siti JS-heavy; rimedio del fallimento dichiarato in `S3`.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi prova l'app sull'ambiente non di produzione: davanti a un link che ha fallito, incolla il
testo e salva la ricetta senza uscire dal flusso di aggiunta.

## Includes

- Un secondo ingresso nel form di add per il testo incollato, che salta il fetch e il JSON-LD
  e va direttamente al motore di `S4`.
- L'errore di un URL non leggibile propone il passaggio all'incolla-testo, con l'URL già
  conservato come `sourceUrl` della ricetta che ne uscirà.
- Progress bar sugli stessi passi reali, meno quelli che non vengono eseguiti.

## Verification

- Il testo copiato da una pagina dietro paywall produce una ricetta salvata, con `sourceUrl`
  valorizzato dall'URL che aveva fallito.
- Un testo incollato che non è una ricetta non salva niente e lo dice.
- La progress bar non mostra il passo di scarico della pagina, che qui non avviene.

## Learning target

Che il fallback dichiarato dalle fonti chiuda davvero il buco lasciato dai link illeggibili —
cioè che l'utente arrivato all'errore ne esca con la ricetta salvata invece che rinunciando.

## Excludes

- OCR, PDF e immagini di pagine: nessuna fonte le chiede.
- Import di file da altre app (Paprika e simili): fuori dalla visione.
- Un motore di estrazione separato: è lo stesso di `S4`, con lo stesso schema.

## Open questions

- —
