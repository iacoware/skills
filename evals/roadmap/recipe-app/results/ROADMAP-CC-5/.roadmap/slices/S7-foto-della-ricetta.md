# S7 — Foto della ricetta

← [Register](../roadmap.md#now)

**Outcome:** Una ricetta porta più foto con una copertina scelta, e l'aggiunta da link si prende da
sola l'immagine della pagina senza rimanere appesa a quel sito.

**Requested by:** `goal.md` (*Aggiunta ricetta — Foto multiple*, *Attrito minimo in aggiunta*),
`concepts.md` (*Entità principali — Photo*) e `arch-choices.md` (*Object storage foto*).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi prova l'app su staging: l'elenco smette di essere una lista di titoli e le ricette si
riconoscono a colpo d'occhio.

## Includes

- Una porta Effect `PhotoStore` con l'adapter Cloudflare R2, e le credenziali che S0 ha aperto.
- Tabella `Photo` (`recipeId`, `url`, `isCover`) e migrazione, con l'invariante di una sola
  copertina per ricetta garantito nel percorso di scrittura e non solo nell'interfaccia.
- Caricamento di una o più foto dalla schermata della ricetta, con validazione di tipo e dimensione
  e rifiuto motivato di ciò che non è un'immagine; rimozione di una foto, che è la correzione di un
  caricamento sbagliato.
- La prima foto diventa copertina per default, e la copertina è cambiabile; l'elenco in Home mostra
  la copertina.
- Sul percorso da link, l'immagine indicata da `og:image` o dal JSON-LD viene scaricata e ricaricata
  su R2 — mai linkata a caldo dal sito d'origine — e diventa lo stadio "salvo foto" del progresso
  che S5 ha costruito, con gli stessi tetti su dimensione e redirect che S5 applica alla pagina.
- Lo stadio della foto è un effetto opzionale: se fallisce, la ricetta resta salvata e lo stadio si
  dichiara fallito.

## Verification

Una ricetta porta più foto, la prima compare come copertina nell'elenco, e sceglierne un'altra
cambia quello che l'elenco mostra. Un'aggiunta da link salva un'immagine il cui URL sta sul nostro
dominio R2 e non su quello del sito d'origine, e l'immagine si vede ancora dopo che il riferimento
originale è stato reso irraggiungibile. Con R2 reso irraggiungibile, l'aggiunta da link salva
comunque la ricetta e mostra lo stadio della foto come fallito con un messaggio suo. Un file che non
è un'immagine viene rifiutato con un messaggio. Rimossa la copertina, un'altra foto la sostituisce e
la ricetta non resta senza.

## Learning target

Se lo stadio della foto può fallire senza trascinarsi dietro l'aggiunta — cioè se un effetto verso
uno storage esterno resta davvero opzionale dentro un'estrazione sincrona, o se in pratica la
allunga oltre il budget di richiesta.

## Excludes

- Nessun ridimensionamento e nessuna thumbnail: `LATER`.
- Nessun OCR sulle foto: `LATER`.
- Nessuna galleria o riordino delle foto oltre alla scelta della copertina: le fonti chiedono solo
  quella.

## Open questions

- —
