# S8 — Foto della ricetta con copertina

← [Register](../roadmap.md#now)

**Outcome:** Una ricetta porta più foto con una copertina che si sceglie, e l'aggiunta da link
salva la foto della pagina sul nostro storage invece di puntare a quello altrui.

**Requested by:** `goal.md` § Aggiunta ricetta (foto multiple, cover); `arch-choices.md` § Object
storage foto; il passo "Salvo foto" che `S3` ha escluso.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi legge e chi aggiunge ricette nel ricettario: l'elenco smette di essere una lista di titoli.

## Includes

- Bucket Cloudflare R2 e credenziali, con adapter di storage dietro un `Context.Tag`: questa riga
  lo possiede e le altre lo consumano.
- Tabella `Photo` con `recipeId`, `url` e `isCover`, e l'invariante di una sola copertina per
  ricetta, tenuta nel database e non nel client.
- Upload di più foto dal form di edit, scelta della copertina, rimozione di una foto — e se era la
  copertina, la successiva prende il suo posto.
- Copertina mostrata in elenco e in dettaglio.
- Nel flusso di aggiunta da link: download di `og:image` o dell'immagine dello `schema.org/Recipe`
  e ricarica su R2, con il passo "Salvo foto" che compare in coda alla progress.
- Il fallimento del download non fa fallire l'aggiunta: la ricetta resta salvata senza foto e la
  progress lo dice.

## Verification

- Una ricetta con tre foto mostra la prima come copertina; cambiando copertina l'elenco segue.
- Non esistono due `Photo` con `isCover` per la stessa ricetta, nemmeno forzando due cambi
  concorrenti.
- Una ricetta importata da link mostra un'immagine servita dal nostro storage e non dal sito di
  origine, e resta visibile dopo che l'originale è stato rimosso.
- Un `og:image` irraggiungibile lascia la ricetta salvata senza foto, con il passo segnato come non
  riuscito.
- Una foto caricata da un membro è visibile agli altri membri del ricettario e a nessun altro.
- Il traffico in uscita da R2 misurato dopo una sessione di lettura conferma l'egress a zero costo.

## Learning target

Se R2 con zero egress regge le foto del ricettario senza costo e senza CDN davanti, e se il
download della copertina all'import può fallire senza portarsi dietro l'aggiunta.

## Excludes

- Ridimensionamento e ottimizzazione delle immagini, e raccolta delle foto orfane sullo storage:
  candidati in `LATER`.
- OCR da foto di un libro: candidato in `LATER`.
- Foto come input dell'estrazione: fuori, gli ingressi sono link, testo e form.

## Open questions

- —
