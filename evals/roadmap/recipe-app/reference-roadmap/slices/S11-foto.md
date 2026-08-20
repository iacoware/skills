# S11 — Foto della ricetta

← [Register](../roadmap.md#now)

**Outcome:** Una ricetta mostra le proprie foto, e la prima è la copertina.

**Requested by:** `sources/goal.md` § Aggiunta ricetta, `sources/arch-choices.md` § Object storage
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi sfoglia l'elenco e riconosce una ricetta dalla foto prima che dal nome.

## Includes

- Il caricamento di più foto su object storage, con nel database il solo URL.
- Il download dell'immagine trovata durante l'import e la sua ricarica sul proprio storage.
- La prima foto come copertina, in elenco e in lettura.

## Verification

Una ricetta importata da un link mostra la propria foto anche quando il sito d'origine la sposta o
ne blocca il collegamento diretto.

## Learning target

Che tenere le foto fuori dal database, con dentro il solo URL, basti a non avere volumi e a non
rompere la macchina che si spegne.

## Excludes

- La scelta manuale della copertina.
- Decidere quali foto tenere quando l'import ne trova molte.
- Ritaglio, ridimensionamento e ottimizzazione.

## Open questions

—
