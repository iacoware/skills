# S9 — Foto multiple e copertina

← [Register](../roadmap.md#now)

**Outcome:** Aggiungendo una ricetta da link, l'immagine della pagina finisce sul nostro storage e
diventa la copertina; da una ricetta si caricano altre foto e si sceglie quale fa da copertina.
**Requested by:** `goal.md` § Aggiunta ricetta ("foto multiple per ricetta; la cover è la prima foto
per default, cambiabile") e il passo "Salvo foto" della barra di avanzamento; `arch-choices.md` §
Object storage foto; `concepts.md` § Photo.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi usa il ricettario. Dopo questa riga sfoglia un elenco di piatti invece di un elenco di titoli.

## Includes

- Tabella `Photo` con `recipeId`, `url` e `isCover`, e l'invariante di una sola copertina per ricetta.
- Adapter Cloudflare R2 per il caricamento e l'esposizione dei file, con i segreti di S0: è l'unica
  riga che lo possiede.
- Passo "salvo foto" innestato in coda alla pipeline di add di S3, con il proprio segmento nella barra
  di avanzamento: scarica `og:image` o l'immagine dello `schema.org/Recipe` e la ricarica su R2, con
  limiti su schema, dimensione e timeout, senza seguire redirect verso indirizzi interni.
- Caricamento manuale di una o più foto da una ricetta, e scelta della copertina.
- Copertina nell'elenco e galleria nel dettaglio, con il segnaposto per le ricette senza foto.

## Verification

- Aggiungendo da link una ricetta con `og:image`, la foto compare in elenco come copertina e il file
  è servito dal nostro storage, non dal sito d'origine.
- Se l'immagine d'origine non è scaricabile, la ricetta si salva comunque: la barra segna il passo
  foto come non riuscito e l'elenco mostra il segnaposto.
- Caricando due foto da una ricetta senza copertina, la prima diventa copertina; scegliendo la
  seconda, l'elenco cambia e la prima smette di essere copertina.
- Le foto di una ricetta di un altro ricettario non sono elencabili da chi non ne è membro.
- Un file troppo grande o di tipo non previsto viene rifiutato con un messaggio, senza lasciare un
  oggetto orfano su R2.

## Learning target

Se rimpiazzare l'hotlinking scaricando e ricaricando l'immagine regge sui siti veri — dove
`og:image` manca, reindirizza o è protetta — e se lo fa dentro il tempo della pipeline sincrona di
S3.

## Excludes

- Ritaglio, ridimensionamento e varianti responsive delle immagini: nessuna fonte li chiede.
- OCR sulle foto: fuori, l'MVP legge testo, non immagini.
- Cancellazione di una foto già caricata: nessuna fonte la chiede.

## Open questions

- Nessuna.
