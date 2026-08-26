# S11 — Prima release a famiglia e amici

← [Register](../roadmap.md#now)

**Outcome:** L'app è raggiungibile su un dominio proprio dalle persone invitate, con le
protezioni operative minime che il piano dei costi presuppone.

**Requested by:** `goal.md` § Visione (app condivisa tra familiari e amici) e § Principi
guida (budget bassissimo); `arch-choices.md` § Hosting e § Riepilogo costi.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Le persone invitate, non tecniche: usano l'app dal loro telefono senza sapere che cos'è Fly.

## Includes

- Dominio e TLS sull'app Fly, segreti di produzione separati da quelli di staging.
- Verifica del ripristino: un restore di prova dal piano Neon che riporta indietro un dato
  cancellato.
- Log ed avviso minimo sugli errori di estrazione, con il passo che li ha causati.
- Tetto di spesa impostato dove il fornitore lo permette, sulle API a pagamento.
- Pagina di errore, e un runbook breve: deploy, rollback, rotazione delle chiavi.

## Verification

Una persona non tecnica invitata entra dal dominio pubblico, aggiunge una ricetta da link e la
ritrova cercandola a parole sue. Un restore di prova riporta un dato cancellato, con il tempo
impiegato annotato. Un'estrazione fallita compare nel log con il passo che l'ha causata e fa
scattare l'avviso. Il costo del primo mese, misurato a consuntivo su Fly, Neon, R2 e API, è
confrontato con i centesimi assunti dal riepilogo costi; se non ci sta, la scelta della
macchina sempre calda è presa consapevolmente e scritta.

## Learning target

Che l'insieme regga con utenti veri al costo dichiarato, risveglio dopo il silenzio incluso.

## Excludes

- Registrazione aperta a chiunque: candidato, qui si entra solo su invito.
- Scalabilità oltre la cerchia prevista: fuori dall'ordine di grandezza dichiarato.
- Infrastruttura come codice versionata: le fonti la rimandano, per l'MVP bastano `fly.toml`
  e la CLI.

## Open questions

- Nessuna fonte dice a chi si apre la prima release — la sola famiglia o tutti gli invitati
  degli invitati — né su quale dominio, e la risposta decide se il tetto di spesa e l'avviso
  vadano accesi prima o possano aspettare.
