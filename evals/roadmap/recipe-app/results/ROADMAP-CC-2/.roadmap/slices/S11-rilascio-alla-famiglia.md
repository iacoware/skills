# S11 — Rilascio alla famiglia

← [Register](../roadmap.md#now)

**Outcome:** L'app è su un indirizzo stabile, con credenziali e segreti di produzione, e i primi
membri veri della famiglia entrano dal proprio telefono, aggiungono ricette e le ritrovano cercando —
senza che nessuno debba avere accesso a una console.

**Requested by:** Riga di rilascio che chiude il percorso: `goal.md` (§ Visione: app condivisa fra
familiari e amici) e `arch-choices.md` (§ Hosting, § Riepilogo costi).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

I membri della famiglia e gli amici a cui l'app è destinata, sui loro dispositivi reali. È la prima
volta che il pubblico non è né chi sviluppa né chi prova.

## Includes

- Applicazione Fly di produzione, separata dall'ambiente di prova, con dominio e certificato, e
  `auto_stop` in modalità `suspend` con scale-to-zero come deciso.
- Credenziali OAuth Google di produzione con l'URL di callback del dominio reale, e tutti i segreti
  di produzione nei secret di Fly.
- Database e bucket di produzione, distinti da quelli di prova, con le migration applicate dalla
  pipeline.
- Verifica dei backup del database: che siano attivi sul provider, e che un ripristino su un database
  vuoto ricostruisca davvero i dati.
- Un runbook di una pagina: come si deploya, come si ripristina un backup, dove si guardano gli
  errori, quali contatori dicono quanto si sta spendendo.
- L'ingresso dei primi utenti reali, con almeno un invito accettato.

## Verification

Un membro della famiglia, dal proprio telefono e senza istruzioni scritte da noi, apre il dominio,
entra con Google, apre l'invito ricevuto, aggiunge una ricetta incollando il link di un blog e la
ritrova cercandola con una parola in una lingua diversa da quella della ricetta. La prima richiesta
dopo un'ora di silenzio risponde, e il tempo che ci mette è misurato sul dominio di produzione e
confrontato con quello registrato in S1. Il ripristino di un backup è stato eseguito davvero su un
database vuoto e ha ricostruito ricette, ricettari e appartenenze. La spesa del primo periodo di uso
reale è letta dai contatori dei provider e confrontata con il target di centesimi al mese dichiarato
nelle assunzioni.

## Learning target

Il percorso completo — entrare, essere invitati, aggiungere da link, ritrovare cercando — regge in
mano a persone che non l'hanno costruito, sui loro dispositivi, e costa quanto le assunzioni dicono
che costi. Se il conto reale smentisce il target, si scopre qui, dove è ancora una riga in `fly.toml`
e non una riscrittura.

## Excludes

- Qualunque capacità nuova: quello che non è entrato entro S10 è un candidato, non un allargamento di
  questa riga.
- Monitoraggio, alerting e analytics oltre a quanto serve per leggere errori e spesa: nessuna fonte
  li chiede, e per un'app di famiglia sarebbero infrastruttura per accumulo.
- La macchina sempre calda: candidato, da valutare con il numero misurato qui e non prima.

## Open questions

- —
