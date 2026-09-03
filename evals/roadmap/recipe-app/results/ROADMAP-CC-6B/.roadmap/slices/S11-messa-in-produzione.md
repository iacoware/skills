# S11 — Messa in mano a famiglia e amici

← [Register](../roadmap.md#now)

**Outcome:** L'app è raggiungibile a un indirizzo stabile, con l'accesso Google in modalità
produzione, e le persone vere la usano dai loro telefoni.

**Requested by:** Chiusura di `NOW` sull'ambiente d'uso dichiarato (`drawing-the-map.md`);
operatività da `sources/arch-choices.md` § Hosting e § Riepilogo costi.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Famiglia e amici: aprono un indirizzo dal telefono, entrano con Google e usano il ricettario
senza che nessuno debba avviare niente.

## Includes

- Ambiente di produzione su Fly con dominio e TLS, `auto_stop` in modalità `suspend` e
  scale-to-zero come raccomandato dalle fonti.
- Client OAuth Google in modalità produzione, con i redirect URI del dominio definitivo.
- Database di produzione separato da quello di prova, con le migrazioni applicate dal deploy e
  i backup del provider verificati con un ripristino di prova.
- Bucket R2 di produzione e segreti di produzione separati.
- Le pagine sono usabili da telefono, che è come verranno aperte.

## Verification

- Da un telefono, su rete mobile, una persona che non ha mai visto l'app entra con Google,
  apre un invito, aggiunge una ricetta da link e la ritrova cercandola.
- La prima richiesta dopo ore di silenzio va a buon fine, e il tempo che ci mette è dichiarato
  e giudicato accettabile o no — è la soglia che decide se serve la macchina sempre calda.
- Un ripristino del backup su un database vuoto restituisce le ricette.
- Dopo una settimana d'uso è dichiarata la spesa reale di Fly, del database, di R2 e delle
  chiamate ai modelli.

## Learning target

Che il conto delle fonti tenga davanti a utenti veri: centesimi al mese con `suspend` e
scale-to-zero, e un cold start che nessuno segnala. Se una delle due cade, cade con un numero
che dice quale.

## Excludes

- Macchina sempre calda a ~$3/mese: candidato, un flag reversibile, da accendere solo se questa
  riga dimostra che serve.
- Monitoraggio e alerting oltre i log di Fly: nessuna fonte li chiede a questa scala.
- IaC versionata: le fonti la dichiarano over-engineering per l'MVP, bastano `fly.toml` e CLI.

## Open questions

- —
