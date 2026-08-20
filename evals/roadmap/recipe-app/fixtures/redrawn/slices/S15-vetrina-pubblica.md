# S15 — Vetrina dei ricettari pubblici

← [Register](../roadmap.md#now)

**Outcome:** Chi arriva senza account vede quali ricettari pubblici ci sono, di che tema parlano, e
ne apre uno.

**Requested by:** La nuova meta dichiarata dall'autore (la scoperta è il prodotto, e l'unità
pubblicata è il ricettario tematico), `sources/concepts.md` (Cookbook come unità di condivisione).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chiunque, senza account: entra dalla porta principale senza avere una query in testa e senza conoscere
nessun link, e trova un ricettario tematico da sfogliare.

## Includes

- L'elenco dei ricettari pubblici, con nome, descrizione e copertina, e quante ricette contengono.
- Un ordine dichiarato e stabile per l'elenco.
- Il passaggio dalla vetrina al ricettario e dalla ricetta al ricettario che la contiene.
- Il conteggio, nei log già previsti, della porta da cui entra ogni sessione anonima: vetrina,
  ricerca o link esterno.

## Verification

Un anonimo che apre la radice del sito vede i ricettari pubblici e nessuno di quelli privati, ne apre
uno e ne legge una ricetta senza mai incontrare un login. Un ricettario tolto dal pubblico sparisce
dall'elenco alla richiesta successiva. I log dicono, su una settimana, da quale delle tre porte sono
entrate le sessioni anonime, e la proporzione è scritta.

## Learning target

Se nel corpus si entra dal ricettario o dalla ricetta — cioè se la vetrina è una porta che la gente
usa, o se la scoperta è tutta ricerca e link arrivati da fuori.

## Excludes

- Classificazione automatica dei temi, profili di chi pubblica, ordinamenti per popolarità: restano
  candidati; qui l'ordine è dichiarato e non si finge un segnale che non abbiamo.
- La ricerca: è di `S13`, e questa riga non ne apre una seconda.

## Open questions

- —
