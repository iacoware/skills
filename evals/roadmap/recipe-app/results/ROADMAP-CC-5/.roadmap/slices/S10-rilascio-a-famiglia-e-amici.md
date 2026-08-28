# S10 — Rilascio a famiglia e amici

← [Register](../roadmap.md#now)

**Outcome:** L'app gira in produzione e le persone a cui è destinata la usano dai loro telefoni, con
il conto del primo mese sotto gli occhi.

**Requested by:** `goal.md` (*Visione*, *Principi guida — Budget bassissimo*) e `arch-choices.md`
(*Hosting*, *Riepilogo costi*).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

I familiari e gli amici a cui l'app è destinata: la usano sul loro telefono, sul loro account, senza
che nessuno debba far girare niente per loro.

## Includes

- App Fly di produzione con `suspend` e scale-to-zero, database Postgres e bucket R2 separati da
  quelli di staging, segreti di produzione e redirect URI Google di produzione.
- Migrazioni applicate al deploy anche in produzione, con la stessa pipeline di staging.
- Spesa di LLM ed embedding osservabile: quanto è stato speso nel mese si legge senza aprire la
  console del fornitore.
- Il primo ricettario vero creato e condiviso con persone reali.

## Verification

Un familiare, dal proprio telefono e con il proprio account Google, apre il link d'invito, entra nel
ricettario, aggiunge una ricetta da un link di un blog, ne aggiunge una incollando il testo di una
pagina che il link non copre, ci mette una foto, e trova la ricetta scritta in inglese cercando in
italiano — tutto sull'URL di produzione e senza assistenza. La prima richiesta dopo una notte di
silenzio è misurata e il numero è dichiarato accanto al sub-secondo che le fonti promettono. Il conto
effettivo del primo mese — Fly, database, R2, LLM, embedding — è dichiarato voce per voce accanto ai
centesimi al mese che le fonti prevedono.

## Learning target

Se l'insieme costa davvero centesimi al mese quando lo usano persone vere, e se il risveglio dopo il
silenzio reale è tollerabile per una famiglia o costringe alla macchina sempre calda, che è la voce
di costo che le fonti mettono a circa tre dollari al mese.

## Excludes

- Nessuna macchina sempre calda: è un flag reversibile in `fly.toml` ed è in `LATER`, da accendere
  solo se la misura di questa riga lo impone.
- Nessuna IaC versionata: le fonti scelgono `fly.toml` più CLI per l'MVP.
- Nessun tetto di spesa per ricettario o per utente: è la domanda aperta della mappa, e se la
  risposta lo richiede diventa una riga sua.

## Open questions

- —
