# S3 — Ricettario con ricette scritte a mano

← [Register](../roadmap.md#now)

**Outcome:** Una ricetta si scrive a mano in un form, si salva nel ricettario corrente, compare
nell'elenco e si riapre con lo stesso form per correggerla.

**Requested by:** `sources/goal.md` § Home per l'elenco e § Aggiunta ricetta, che chiede lo stesso
form per inserimento manuale e per la correzione; `sources/concepts.md` § Recipe per i campi e
§ Modello di condivisione per lo scope.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi sviluppa e chi collauda, sull'ambiente di staging non pubblico: l'identità non esiste ancora,
quindi non c'è un utente finale da promettere. Dopo questa riga possono creare, leggere e
correggere ricette vere su un database vero.

## Includes

- Tabelle `cookbook` e `recipe` con la loro migrazione, e un ricettario seed creato da migrazione.
- Il resolver `currentCookbook`: l'unico posto della base di codice che decide di quale ricettario
  si stia parlando. Per ora restituisce l'identificativo configurato. Ogni lettura e ogni scrittura
  di dominio passa da lì e nessuna query riceve un ricettario da fuori.
- Form unico per creare e per correggere: titolo, ingredienti e preparazione come testo libero,
  nessun parsing di quantità e unità. Nessun campo marcato con l'asterisco, gli opzionali marcati
  «(optional)», lo stato obbligatorio esposto dall'attributo nativo.
- Elenco delle ricette del ricettario corrente, con l'ingresso alla singola ricetta.
- Logica in Effect con errori `Data.TaggedError` gestiti al boundary.

## Verification

Si crea una ricetta a mano, compare nell'elenco, si riapre, si modifica e la modifica sopravvive a
un nuovo deploy. Una ricetta scritta in un ricettario diverso da quello corrente non compare
nell'elenco e non si apre nemmeno andandoci diritti per URL; la prova gira contro il database
reale, non contro un doppio. Il form dichiara i campi obbligatori senza asterisco e uno screen
reader legge lo stato obbligatorio.

## Learning target

Che il confine di scope stia davvero tutto dentro un solo resolver — che ogni percorso di lettura e
di scrittura possa passare da lì senza che nessuna query di dominio sappia niente di ricettari —
così che più avanti l'identità autenticata sostituisca quel solo punto e non riscriva nulla di
quello che è stato costruito prima.

## Excludes

- Ogni estrazione da link o da testo incollato: sono i temi dell'import, e arrivano dopo perché la
  correzione deve esistere prima della prima riga che può produrre una ricetta sbagliata.
- La derivazione di tag e tempo di preparazione: le sorgenti vietano di chiederli all'utente, e
  nascono solo dall'estrazione. Qui i campi non esistono nel form.
- Le foto, che aprono l'object storage e hanno una riga loro.
- L'autenticazione: il ricettario corrente è configurato, non scelto da chi entra.
- La cancellazione di una ricetta, che nessuna sorgente chiede: resta una candidata in `LATER`.

## Open questions

- —
