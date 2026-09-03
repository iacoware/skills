# S11 — Il ricettario in mano a famiglia e amici

← [Register](../roadmap.md#now)

**Outcome:** L'app esce dallo staging: dominio pubblico, credenziali, database e storage di
produzione, e i primi inviti partono davvero.

**Requested by:** `goal.md` § Visione; `arch-choices.md` §§ Hosting, Riepilogo costi.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Famiglia e amici, sull'app di produzione: creano il loro ricettario, si invitano a vicenda e ci
mettono dentro le ricette che usano.

## Includes

- App Fly di produzione con `suspend` e scale-to-zero, dominio e TLS.
- Database Neon di produzione con le migrazioni applicate dal deploy, e bucket R2 di produzione.
- Client OAuth Google portato da modalità test a produzione, con consent screen e domini
  autorizzati.
- Segreti di produzione separati da quelli di staging.
- Log degli errori consultabili da chi manda avanti l'app.
- Backup del database verificato con un restore di prova.
- Una nota operativa che dice quando passare a macchina sempre-calda e come: `min_machines_running`
  in `fly.toml`, ~$3/mese, reversibile.

## Verification

- Un invitato che non ha mai visto l'app arriva dal link, entra con Google, aggiunge una ricetta da
  link e la ritrova cercandola — tutto sul dominio pubblico.
- Dopo un giorno di silenzio la prima richiesta risponde, e il tempo di risveglio è misurato e
  confrontato con quello di `S1`.
- Un restore del backup su un database vuoto rimette in piedi ricette, foto referenziate e
  membership.
- Il conto del primo mese è letto sulle fatture di Fly, Neon, R2 e dei due provider di modelli, e
  confrontato con il target di centesimi al mese.
- Un errore in produzione si ritrova nei log con abbastanza contesto da sapere quale passo è
  fallito.

## Learning target

Se l'insieme scelto per il costo — Fly a consumo con `suspend`, Neon e R2 in free tier, modelli
chiamati solo in aggiunta e in edit — regge utenti veri a centesimi al mese, e se il cold start del
primo utente è il fastidio minore che `arch-choices.md` prevede.

## Excludes

- Monitoraggio e alerting oltre ai log: candidato in `LATER`.
- IaC versionata: candidato in `LATER`, per l'MVP bastano `fly.toml` e la CLI.
- Ricettari pubblici tematici: candidato in `LATER`.

## Open questions

- Il dominio pubblico su cui esce l'app e chi riceve i primi inviti non stanno in nessuna fonte:
  sono decisioni dell'autore, e senza di esse questa riga non parte.
