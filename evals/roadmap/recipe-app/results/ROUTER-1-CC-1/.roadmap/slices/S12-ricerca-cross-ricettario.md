# S12 — Ricerca su tutti i ricettari di cui si è membri

← [Register](../roadmap.md#now)

**Outcome:** Una frase cercata trova la ricetta in qualunque ricettario di cui si è membri, non solo
in quello corrente.

**Requested by:** L'autore, in sessione: la ricerca deve attraversare tutti i ricettari di cui si è
membri. Supera `sources/goal.md` (Ricerca — "Scope: solo il ricettario corrente"; Fuori scope MVP —
"Ricerca cross-ricettario") e promuove il candidato che stava in `LATER`.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi sta in più di un ricettario: cerca una volta sola e non deve ricordare in quale ricettario aveva
salvato la ricetta.

## Includes

- Un resolver esplicito dell'insieme leggibile — le membership dell'utente autenticato — accanto a
  `CurrentCookbook`, che resta il proprietario dello scope di scrittura e dell'elenco.
- La query di similarità filtrata su quell'insieme in un'unica interrogazione, non una per
  ricettario.
- Ogni risultato dice a quale ricettario appartiene: due ricettari possono contenere lo stesso
  titolo.
- Quale dei due comportamenti della domanda aperta qui sotto valga: la riga li regge entrambi e non
  ne sceglie nessuno.

## Verification

Un membro di due ricettari cerca una frase e trova ricette di entrambi, ognuna con il ricettario che
la contiene; per chi è membro di uno solo la ricerca non cambia. Una ricetta di un ricettario di cui
non si è membri non esce mai, nemmeno conoscendone l'id, e il filtro sta nella query, non nella UI.
Revocata una membership come la revoca `S9`, le ricette di quel ricettario spariscono dai risultati
alla ricerca successiva. Le query di prova di `S2` trovano ancora le stesse ricette che trovavano in
`S7`, ora in mezzo a quelle degli altri ricettari. La latenza p95 della ricerca sull'unione è
dichiarata, e il costo resta quello di una sola chiamata di embedding sulla query.

## Learning target

Se il ranking puramente semantico regge quando il corpus è l'unione di più ricettari, o se
mescolarli rende i risultati inutilizzabili senza i filtri che oggi sono candidati.

## Excludes

- Filtri per tag e tempo e ricerca ibrida: restano candidati, e questa riga è ciò che dirà se
  servono prima di quanto la mappa credeva.
- Ricettari pubblici tematici: restano candidati, qui si legge solo dove si è membri.
- Elenco e scrittura non cambiano scope: restano al ricettario corrente di `CurrentCookbook`.

## Open questions

- La ricerca è sempre su tutte le membership, o resta possibile restringerla al ricettario corrente?
  Le sorgenti dicevano solo il ricettario corrente e l'istruzione dice non solo quello: quale delle
  due letture vale decide se questa riga porta anche un modo di restringere lo scope.
