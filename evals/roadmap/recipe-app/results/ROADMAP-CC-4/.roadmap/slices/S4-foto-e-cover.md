# S4 — Foto multiple e cover su R2

← [Register](../roadmap.md#now)

**Outcome:** Una ricetta porta più foto caricate sul nostro storage, con una cover che si può
cambiare.

**Requested by:** `goal.md` § Aggiunta ricetta ("foto multiple, cover la prima per default");
`arch-choices.md` § Object storage foto.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Sviluppatori e tester sull'ambiente di staging: possono corredare di foto le ricette che
salvano, e `S5` può salvare l'immagine del sito d'origine senza riaprire questa pipeline.

## Includes

- Migrazione `Photo` (`recipeId`, `url`, `isCover`).
- Adapter verso Cloudflare R2 con chiavi solo lato server, incapsulato in un servizio Effect
  che è l'unico punto che carica un file.
- Caricamento di più foto dal form, con limite di tipo e di dimensione e messaggio d'errore
  che non fa perdere la ricetta.
- Prima foto cover per default, cover cambiabile, invariante di una sola cover per ricetta
  imposto nella scrittura.
- Cancellazione di una foto, con ricalcolo della cover se era quella.
- URL serviti dal nostro bucket, mai dal sito d'origine.

## Verification

Caricate tre foto da un telefono, l'elenco mostra la prima come cover. Cambiata la cover,
l'elenco cambia e in banca dati resta una sola cover per quella ricetta. Cancellata la foto
di copertina, un'altra diventa cover e nessuna riga resta senza. Un file di tipo non ammesso
o oltre il limite viene rifiutato con un messaggio che nomina il limite, e la ricetta resta
intatta. L'immagine mostrata è servita dal nostro bucket, verificabile dall'URL.

## Learning target

Che il caricamento verso R2 dentro la richiesta Next regga foto vere da telefono, e che
l'invariante della cover si tenga avendo un solo punto di scrittura.

## Excludes

- Scaricare l'immagine dal sito d'origine: è di `S5`, che consuma questa pipeline senza
  riaprirne la proprietà.
- Ridimensionamento e ottimizzazione: candidato.
- Le foto non entrano nel testo indicizzato: la ricerca di `S8` non le tocca.

## Open questions

- —
