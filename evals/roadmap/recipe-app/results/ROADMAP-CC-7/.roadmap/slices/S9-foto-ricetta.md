# S9 — Foto della ricetta, a mano e dal link

← [Register](../roadmap.md#now)

**Outcome:** Una ricetta ha le sue foto con una copertina scelta, e quando arriva da un link la foto
della pagina è già lì senza che nessuno l'abbia caricata.

**Requested by:** `goal.md` (Aggiunta ricetta — foto multiple, cover che è la prima per default e
cambiabile), `arch-choices.md` (Object storage foto — Cloudflare R2 e la ricarica per evitare
l'hotlinking) e `concepts.md` (`Photo`).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Famiglia e amici. Da qui il ricettario si sfoglia guardandolo invece di leggerlo.

## Includes

- Adapter di object storage dietro `Context.Tag`, con implementazione R2: upload, URL pubblico,
  cancellazione. È l'unico punto del codice che parla con R2.
- Tabella `Photo` con ricetta, URL e copertina, e l'invariante di una sola copertina per ricetta
  garantita in scrittura e non dall'interfaccia.
- Upload di più foto dal form di `S3`, con la prima che diventa copertina per default e un comando
  per cambiarla.
- Nel percorso da link: download dell'immagine indicata dal `schema.org/Recipe` o dall'`og:image`,
  ricarica su R2 e salvataggio come copertina. È qui che compare il passo `Salvo la foto` nella barra
  di `S4`, e non prima, perché prima non c'era niente da salvare.
- Miniatura della copertina nell'elenco e nei risultati di ricerca.
- Il fallimento della foto non fa fallire l'aggiunta: la ricetta si salva lo stesso e la barra lo
  dice.

## Verification

- Importando da un URL con `og:image`, la ricetta ha una copertina servita dal nostro storage e non
  dal sito d'origine: togliendo l'immagine dal sito originale, la nostra resta.
- Caricando tre foto su una ricetta la prima è copertina; cambiando copertina, esattamente una foto
  risulta di copertina e le altre no, anche facendo due cambi in parallelo sulla stessa ricetta.
- Se il download dell'immagine fallisce o l'immagine non esiste, la ricetta entra comunque nel
  ricettario senza copertina, e la barra dice che la foto non è stata salvata invece di far fallire
  l'aggiunta.
- Cancellando una ricetta, i suoi oggetti su R2 non restano orfani.
- Il consumo del bucket dopo cento ricette importate è misurato e confrontato con i 10GB del piano
  gratuito, per sapere a che scala il piano finisce.

## Learning target

Che ricaricare le immagini sul proprio storage invece di linkarle risolva davvero l'hotlinking che si
rompe, restando dentro il piano gratuito alla scala prevista — e che la copertina si possa tenere
unica senza un modello più ricco di quello che le sorgenti concedono.

## Excludes

- Il ridimensionamento e le miniature generate lato server: le foto si servono come sono e la
  miniatura è resa dal layout. Nessuna sorgente chiede una pipeline di immagini.
- L'OCR della foto di una pagina di libro: non è in questa mappa.
- L'immagine come segnale di ricerca: `goal.md` indicizza solo testo, tag e tempo.

## Open questions

- —
