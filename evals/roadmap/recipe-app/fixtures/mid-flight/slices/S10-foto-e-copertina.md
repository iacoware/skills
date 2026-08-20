# S10 — Foto multiple e copertina su object storage

← [Register](../roadmap.md#now)

**Outcome:** Una ricetta si illustra con più foto su object storage, la prima è la copertina, la
copertina si cambia, e l'aggiunta da link porta a casa da sé l'immagine della pagina.

**Requested by:** `sources/goal.md` (Aggiunta ricetta — foto multiple, cover),
`sources/arch-choices.md` (Object storage foto — Cloudflare R2), `sources/concepts.md` (Photo).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

I membri di un ricettario: caricano le foto dei loro piatti e scelgono quale si vede in elenco.

## Includes

- Bucket R2 e adapter di storage: è l'unico proprietario di questo confine, e nessun'altra riga lo
  riapre.
- Upload di più foto dalla scheda ricetta, con l'URL salvato in `Photo` e il file mai nel database.
- Invariante di una sola cover per ricetta: la prima caricata per default, cambiabile.
- Download dell'immagine indicata da `og:image` o dallo `schema.org/Recipe` e ricarica su storage
  proprio, con il passo "Salvo foto" aggiunto qui all'avanzamento di `S4`.
- Copertina mostrata in elenco.

## Verification

Tre foto caricate compaiono nell'ordine di caricamento, la prima è copertina, e cambiando copertina
l'elenco cambia subito; in nessun momento una ricetta ha due cover. Una ricetta aggiunta da un link
con `og:image` mostra quell'immagine servita dal nostro dominio e non dal sito d'origine, e continua
a mostrarla se il sito d'origine la toglie. Se il download dell'immagine fallisce, la ricetta si
salva comunque e l'avanzamento dice quale passo è saltato. Cancellare una foto non lascia mai un URL
rotto nel database.

## Learning target

Se un solo confine di storage regge sia l'upload dal browser sia il fetch lato server, che
falliscono in modi diversi e che nessuna riga successiva dovrà riaprire.

## Excludes

- Editing delle immagini, gallerie, ridimensionamenti serviti a più risoluzioni: restano candidati.
- OCR di una foto come quarto ingresso di estrazione: resta candidato.
- Pulizia degli oggetti orfani su R2: tollerata per scelta, dichiarata fra i concerns.

## Open questions

- —
