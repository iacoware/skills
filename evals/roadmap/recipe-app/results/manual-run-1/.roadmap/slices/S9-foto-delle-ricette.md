# S9 — Foto delle ricette: più di una, con la copertina

← [Register](../roadmap.md#now)

**Outcome:** Una ricetta ha le sue foto — caricate dal dispositivo o prese dalla pagina da cui è
stata importata — servite dal nostro object storage, con una copertina sola che si può cambiare.

**Requested by:** `sources/goal.md`, «Foto multiple per ricetta; la cover è la prima foto per
default, cambiabile»; `sources/arch-choices.md`, Cloudflare R2 e il ricaricare l'immagine per evitare
hotlinking; `sources/concepts.md`, l'entità `Photo`.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

I membri di un ricettario. Dopo questa riga la ricetta si riconosce dall'elenco perché ha la sua
foto, e chi la guarda decide quale foto la rappresenta.

## Includes

- Il bucket su Cloudflare R2 e l'adapter di upload, aperti e posseduti qui da soli: nessuna riga
  precedente ci scrive e nessuna successiva ne riapre la proprietà.
- Il caricamento di una o più foto dal dispositivo, dal form della ricetta.
- Il recupero dell'immagine della pagina di origine — `og:image` o `schema.org/Recipe` — al momento
  dell'import, ricaricata su R2 invece che linkata, agganciata al percorso di import già consegnato.
- La tabella `Photo` con `url` e `isCover`, e l'invariante della copertina: una sola per ricetta, la
  prima per default, cambiabile.
- La copertina mostrata nell'elenco, e la cancellazione di una foto compresa quella di copertina.
- Un tetto dichiarato a dimensione e formato dei file accettati.

## Verification

Una ricetta con tre foto mostra la prima come copertina nell'elenco, e promuovere la terza cambia
quello che l'elenco mostra. Una ricetta importata da un blog con `og:image` porta quell'immagine
servita da R2 e non dal sito di origine: l'indirizzo originale non compare da nessuna parte nella
pagina, e spegnere l'accesso al sito di origine non rompe l'immagine. Un upload fallito lascia la
ricetta salvata e senza quella foto, con un messaggio, e non lascia mai una ricetta a metà né un
oggetto orfano su R2. Cancellare la copertina ne promuove un'altra, e cancellare l'ultima foto lascia
la ricetta senza copertina e non con una copertina che punta al vuoto. Un file che non è
un'immagine, o che supera il tetto dichiarato, è rifiutato dicendo perché. Le chiavi degli oggetti non
sono indovinabili e il bucket non è elencabile. Lo spazio occupato dopo cento ricette con foto è
riportato contro il free tier.

## Learning target

Le foto passate da un unico adapter — caricate da una persona e recuperate da una pagina — tengono
l'invariante della copertina e non costano niente, e l'app non dipende mai da un'immagine ospitata da
qualcun altro.

## Excludes

- Nessun ridimensionamento e nessuna miniatura: sono candidati, da fare se il peso delle pagine o il
  free tier lo chiederanno.
- Nessun OCR da foto, nessuna estrazione di ricette da un'immagine.
- Nessuna galleria oltre la ricetta, nessun riordino delle foto oltre la scelta della copertina.

## Open questions

—
