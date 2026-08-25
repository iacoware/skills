# S8 — Foto della ricetta con copertina

← [Register](../roadmap.md#now)

**Outcome:** Una ricetta ha le sue foto, con una copertina scelta da chi la guarda; le foto caricate
a mano e quelle prese dalla pagina di origine finiscono entrambe sul nostro object storage, quindi
non si rompono quando il sito di partenza cambia.

**Requested by:** `goal.md` (§ Aggiunta ricetta: foto multiple, cover la prima per default,
cambiabile; § Aggiunta ricetta: passo "Salvo foto" nell'avanzamento) e `arch-choices.md` (§ Object
storage foto — Cloudflare R2, ricaricamento per evitare hotlinking).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi usa l'app. Dopo questa riga il ricettario si guarda oltre che leggersi, e una ricetta importata
da un blog porta con sé la sua foto invece di restare un muro di testo.

## Includes

- Bucket Cloudflare R2 e adapter di storage, posseduto da questa riga e da nessun'altra: è il punto
  unico da cui passano tutti i caricamenti, sia manuali sia automatici.
- Schema e migration per `Photo` (id, `recipeId`, url, `isCover`), con l'invariante di una sola
  copertina per ricetta.
- Caricamento di più foto dal form di S3, con limiti espliciti di numero e dimensione e validazione
  del tipo di file.
- Copertina: la prima foto per default, cambiabile con un'azione dalla pagina della ricetta.
- Nel percorso di aggiunta da link, scaricamento dell'immagine indicata da `og:image` o dal JSON-LD e
  suo ricaricamento su R2, con il passo "Salvo foto" che compare ora nell'avanzamento perché ora è un
  passo vero.
- Un download di foto fallito non blocca il salvataggio della ricetta e non lascia file orfani sullo
  storage.

## Verification

Si caricano tre foto su una ricetta: compaiono tutte, la prima è la copertina, si sceglie la terza
come copertina e dopo un ricaricamento è ancora la terza — e ce n'è sempre e solo una. Si importa un
link che espone `og:image`: la foto compare sulla ricetta e il suo URL è quello del nostro storage e
non quello del sito di origine, verificato ispezionando l'URL. Si importa un link la cui immagine
risponde 404: la ricetta si salva ugualmente, l'avanzamento nomina il passo fallito e non resta
nessun file parziale su R2. Si tenta il caricamento di un file che non è un'immagine e di uno oltre
il limite: entrambi rifiutati con un messaggio, senza scrivere nulla. Si cancella una ricetta: le sue
foto non restano sullo storage.

## Learning target

Un solo adapter di storage serve onestamente due alimentatori con profili di fallimento diversi —
l'utente che carica e la pipeline che scarica da un sito che non controlliamo — senza che nessuno dei
due debba riaprirne la proprietà; e il ricaricamento su storage proprio costa abbastanza poco, in
tempo di aggiunta e in spazio, da stare nel piano gratuito.

## Excludes

- Ridimensionamento, ritaglio, generazione di miniature e CDN dedicata: non chiesti dalle fonti; se
  la dimensione delle foto diventasse un costo, sarà un candidato con un numero a sostenerlo.
- L'indicizzazione delle foto nella ricerca: il testo indicizzato è quello dichiarato in S6 e non
  include immagini.
- Le foto come ingresso di estrazione (OCR): candidato dichiarato fuori MVP.

## Open questions

- —
