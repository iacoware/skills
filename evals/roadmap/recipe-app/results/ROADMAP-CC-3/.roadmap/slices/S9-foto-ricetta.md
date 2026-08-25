# S9 — Foto della ricetta con copertina

← [Register](../roadmap.md#now)

**Outcome:** Una ricetta porta più foto — quella presa dalla pagina importata e quelle caricate a
mano — e la prima è la copertina, cambiabile.

**Requested by:** `sources/goal.md` § Aggiunta ricetta, che chiede foto multiple e una copertina
per default modificabile; `sources/concepts.md` § Photo; `sources/arch-choices.md` § Object storage
foto, che sceglie R2 e impone di ricaricare l'immagine invece di puntare al sito d'origine.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi aggiunge e chi legge le ricette. Dopo questa riga l'elenco si guarda invece di leggersi, e una
ricetta importata porta con sé la sua immagine anche quando il sito d'origine la cambia o la
toglie.

## Includes

- Bucket R2 e adapter di storage dietro una porta `Context.Tag`.
- Tabella `photo` con URL e indicazione di copertina; una sola copertina per ricetta, come
  invariante applicativa.
- Upload multiplo dalla pagina della ricetta, con un limite dichiarato di numero e di peso per
  file.
- Copertina implicita alla prima foto caricata, e cambiabile.
- Un passo in più nel progresso dell'import: l'immagine indicata dalla pagina viene scaricata e
  ricaricata sul nostro storage, e il fallimento di questo passo non blocca il salvataggio della
  ricetta.

## Verification

Si caricano più foto e compaiono tutte; cambiando copertina, l'elenco mostra subito la nuova.
Importando da un link con immagine, la foto compare e il suo URL punta al nostro storage e non al
sito d'origine. Simulando un fallimento dell'upload, la ricetta esiste comunque, l'utente vede che
la foto manca, e nel database non resta nessun riferimento a un file che non c'è. Lo spazio
occupato alla scala dichiarata viene stimato e messo accanto al piano gratuito.

## Learning target

Che tenere le foto fuori dal database e referenziarle per URL regga i fallimenti parziali senza mai
lasciare il database a promettere un'immagine che non esiste — che è l'unico modo in cui questo
disaccoppiamento può fare male.

## Excludes

- Ridimensionamento e compressione delle immagini: candidati in `LATER`, e il limite dichiarato
  sull'upload è ciò che tiene finché non servono.
- OCR e lettura di ricette dalle foto, mai chiesti dalle sorgenti.
- Gallerie, riordino delle foto e ritaglio.

## Open questions

- —
