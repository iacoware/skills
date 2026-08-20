# S6 — Copia-incolla per le pagine che non si lasciano leggere

← [Register](../roadmap.md#now)

**Outcome:** Si incolla il testo di una pagina che il sistema non riesce a leggere e la ricetta entra
nel ricettario per la stessa strada.

**Requested by:** `sources/goal.md` (Visione — copia-incolla come fallback per paywall e siti
JS-heavy), `sources/concepts.md` (Pipeline di estrazione).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi prova l'app sull'ambiente non pubblico e ha appena visto fallire un link: incolla il testo che
vede a schermo e non deve ribattere niente.

## Includes

- Un ingresso di testo che salta il JSON-LD e va sempre all'estrattore di `S5`.
- La stessa pulizia del contenuto e lo stesso schema di output.
- Il rimando al copia-incolla dal messaggio d'errore del path da link, con l'URL già conservato in
  `sourceUrl`.

## Verification

Il testo copiato da una pagina a paywall produce una ricetta di qualità confrontabile con quella che
lo stesso contenuto dà quando è estratto da URL. Dal messaggio d'errore di `S4` si arriva al
copia-incolla senza reincollare l'URL, e la ricetta salvata conserva il link d'origine. Testo che non
è una ricetta fa fallire l'estrazione con un messaggio, non con una ricetta vuota.

## Learning target

Se il testo incollato dall'utente basta all'estrattore quanto l'HTML pulito, cioè se la via d'uscita
è davvero una via d'uscita.

## Excludes

- OCR di una foto e import da file esportati da altre app: restano candidati.
- Un secondo schema di output: qui si riusa quello di `S5` e non se ne apre un altro.

## Open questions

- —
