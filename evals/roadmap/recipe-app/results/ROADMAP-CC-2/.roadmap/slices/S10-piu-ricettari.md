# S10 — Più ricettari e ricettario corrente

← [Register](../roadmap.md#now)

**Outcome:** Si crea un secondo ricettario, si passa dall'uno all'altro, e l'elenco, l'aggiunta e la
ricerca seguono sempre quello corrente, che resta scelto anche alla sessione dopo.

**Requested by:** `goal.md` (§ Condivisione: "un utente può appartenere a più ricettari"; § Home:
"elenco delle ricette del ricettario corrente"; § Ricerca: "scope: solo il ricettario corrente").
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi usa l'app e sta in più di un gruppo — la famiglia e gli amici, o le ricette di casa e quelle da
provare. Dopo questa riga può tenerli separati senza due account.

## Includes

- Creazione di un nuovo ricettario con un nome, che ne fa il creator e ne crea la `Membership`.
- Selettore del ricettario corrente, che elenca quelli di cui si è membri.
- Persistenza della scelta fra le sessioni, così che all'accesso successivo si riapra quello giusto.
- Il risolutore di scope di S7 legge ora la scelta persistita, verificata contro le `Membership`: un
  id di ricettario di cui non si è membri non diventa mai il corrente, per quanto lo si forzi.
- Rinomina del ricettario dalla sua pagina.

## Verification

Si crea un secondo ricettario, vi si aggiunge una ricetta, e l'elenco del primo non la contiene. Si
cerca stando nel secondo: i risultati non comprendono nulla del primo. Si esce e si rientra: il
ricettario corrente è quello che era stato scelto. Forzando l'identificativo di un ricettario di cui
non si è membri — nell'URL o nella richiesta che cambia il corrente — l'app risponde come per un
ricettario inesistente e il corrente non cambia. Un invito accettato in un ricettario lo fa comparire
nel selettore dell'invitato.

## Learning target

Un solo risolutore di scope regge anche quando i ricettari sono più d'uno e il corrente è una scelta
dell'utente invece che una costante — cioè il confine di appartenenza non si allarga in una dozzina
di punti quando smette di essere unico.

## Excludes

- La ricerca su più ricettari insieme: candidato dichiarato fuori MVP; lo scope resta uno solo per
  volta.
- Lo spostamento o la copia di una ricetta da un ricettario all'altro: non chiesto dalle fonti;
  sarà un candidato se servirà.
- Un concetto di gruppo che eviti di ri-invitare le stesse persone in ogni ricettario: candidato, ed
  è esattamente lo svantaggio che questa riga rende visibile.

## Open questions

- —
