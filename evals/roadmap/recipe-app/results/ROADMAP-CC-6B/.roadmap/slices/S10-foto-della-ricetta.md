# S10 — Foto della ricetta

← [Register](../roadmap.md#now)

**Outcome:** Ogni ricetta ha le sue foto su storage nostro, con una copertina che posso
cambiare, e quelle importate da link arrivano già con l'immagine della pagina.

**Requested by:** `sources/goal.md` § Aggiunta ricetta — foto multiple e cover;
`sources/arch-choices.md` § Object storage foto — R2 e ricarica dell'immagine originale.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

I membri del ricettario: riconoscono un piatto dall'elenco invece che leggendo i nomi, e
aggiungono le foto delle proprie ricette.

## Includes

- Tabella `Photo` con `url` e `isCover`, in migrazione; nel database solo l'URL.
- Adapter verso Cloudflare R2: upload, chiave per ricetta, URL pubblico servito senza egress a
  pagamento.
- Passo "salvo foto" nella pipeline di add: scarico di `og:image` o dell'immagine dello
  `schema.org/Recipe`, ricaricata su R2 — il passo che `S3` aveva escluso dalla progress bar.
- Upload di più foto dal form di `S9`, con limiti di dimensione e tipo, e scelta della
  copertina; la prima foto è la copertina per default.
- Copertina nell'elenco e galleria nella pagina della ricetta; una ricetta senza foto resta
  normale ovunque.
- Il fallimento dello scarico dell'immagine non fa fallire l'aggiunta: la ricetta si salva
  senza foto e il passo lo dice.

## Verification

- Una ricetta aggiunta da un link con `og:image` mostra quell'immagine come copertina, servita
  dal nostro dominio di storage e non dal sito originale.
- Se il sito originale sparisce, la foto resta visibile.
- Caricando tre foto e cambiando copertina, l'elenco mostra quella scelta e la ricetta resta
  con una sola copertina.
- Un link la cui immagine non si scarica produce comunque la ricetta, e la progress bar dice
  che la foto non c'è.
- Un upload troppo grande o di tipo non ammesso viene rifiutato con un messaggio, senza lasciare
  oggetti orfani su R2.

## Learning target

Che tenere le immagini su storage nostro sia il costo giusto per non dipendere dai siti
altrui — e che scaricarle e ricaricarle dentro l'aggiunta sincrona non rovini il tempo che
`S3` ha dimostrato accettabile.

## Excludes

- Ridimensionamento, ritaglio e varianti responsive: nessuna fonte le chiede.
- Cancellazione delle foto orfane quando una ricetta viene modificata: nessuna fonte lo chiede;
  lo spazio a questa scala non è un vincolo.
- OCR sulle foto: fuori dalla visione.

## Open questions

- —
