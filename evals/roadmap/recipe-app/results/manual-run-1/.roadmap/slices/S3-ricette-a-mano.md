# S3 — Ricette a mano nel ricettario: crea, elenca, leggi, correggi

← [Register](../roadmap.md#now)

**Outcome:** Una ricetta scritta a mano viene salvata in un ricettario, compare nell'elenco, si
rilegge e si corregge — e ogni lettura e scrittura passa da un solo punto che possiede il ricettario
corrente.

**Requested by:** `sources/goal.md`, «Home» e «Aggiunta ricetta»; `sources/concepts.md`, le entità
`Cookbook` e `Recipe` e il principio di normalizzazione minima; `references/drawing-the-map.md`, il
seam dell'identità.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi costruisce e prova l'app, sull'ambiente deployato non di produzione. Non esiste ancora il login:
l'app gira su un solo ricettario configurato. Dopo questa riga può scrivere una ricetta vera,
ritrovarla nell'elenco, rileggerla e correggerla senza toccare il database a mano.

## Includes

- Tabelle `Cookbook` e `Recipe` con la loro migrazione: `name`, `ingredients`, `steps` come testo
  libero, `sourceUrl`, `prepTime` e `tags` presenti e vuoti, `embedding` presente e nullo.
- Un risolutore nominato del ricettario corrente, unico punto da cui passa ogni query su `Recipe`;
  qui restituisce il ricettario configurato.
- Un solo form condiviso da creazione e modifica, con i campi vuoti quando si crea: titolo,
  ingredienti e preparazione come testo libero, nessun parsing di quantità e unità, i campi
  facoltativi marcati «(optional)» e nessun asterisco.
- L'elenco delle ricette del ricettario corrente e la pagina di dettaglio.
- Nessun passo di conferma: si salva e si è dentro.

## Verification

Una ricetta scritta sull'ambiente deployato compare nell'elenco e si rilegge identica, a capo
compresi. Modificarla cambia lei e nient'altro. Una ricetta inserita nel database dentro un secondo
ricettario è assente dall'elenco ed è irraggiungibile anche conoscendo la sua URL: il filtro di scope
è esercitato, non assunto. Il form rifiuta un titolo vuoto dicendo perché, e accetta ingredienti e
preparazione vuoti senza protestare, perché niente è obbligatorio oltre il nome. Un test fallisce se
una query su `Recipe` scritta nel codice aggira il risolutore. `prepTime`, `tags` ed `embedding`
restano nulli e non bloccano nessuna operazione.

## Learning target

Il minimo che le fonti dichiarano sufficiente — titolo, ingredienti e preparazione come testo libero,
dentro un ricettario risolto da un solo punto nominato — regge una ricetta vera dall'inserimento alla
correzione, e quel punto può reggere lo scope da subito così che l'autenticazione più avanti lo
sostituisca in un posto solo.

## Excludes

- Nessun embedding e nessuna ricerca: la riga di ricerca possiede la pipeline di embedding da sola e
  riempie a posteriori quello che questa riga ha scritto.
- Nessuna foto: l'object storage è aperto e posseduto dalla riga delle foto, che segue tutte le righe
  che lo alimentano.
- Nessun login, nessun invito, nessuna appartenenza: arrivano alle righe dell'identità e della
  condivisione, e sostituiscono il ricettario configurato in questo stesso punto.
- `prepTime` e `tags` esistono ma restano vuoti: è l'import a riempirli, best-effort.

## Open questions

—
