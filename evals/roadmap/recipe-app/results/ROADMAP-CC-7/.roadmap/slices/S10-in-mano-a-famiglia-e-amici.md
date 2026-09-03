# S10 — In mano a famiglia e amici

← [Register](../roadmap.md#now)

**Outcome:** L'app gira su un dominio proprio con i propri conti di produzione, e le prime persone
reali ci entrano con il loro account Google e ci mettono ricette che poi cucineranno.

**Requested by:** `goal.md` (Visione e Cosa fa — MVP: un ricettario condiviso fra famiglia e amici) e
`arch-choices.md` (Hosting e Riepilogo costi).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Famiglia e amici, sull'app vera. È la prima volta che le ricette che ci finiscono dentro sono quelle
di qualcuno, e non quelle di un test.

## Includes

- App Fly di produzione con database, bucket e chiavi separati da staging, con `suspend` e
  `min_machines_running = 0`, come raccomanda `arch-choices.md`.
- Dominio e certificato, e il redirect OAuth di produzione registrato sul client Google.
- Schermata di consenso Google configurata per utenti esterni, con abilitati gli account di chi
  proverà l'app.
- Backup del database attivo sul piano scelto, e una prova di ripristino su un database
  usa-e-getta.
- Un posto dove leggere errori e spesa: log applicativi consultabili, e la bolletta di Fly, del
  provider di embedding e di quello LLM sotto gli occhi.

## Verification

- Almeno tre persone che non hanno scritto il codice entrano con il proprio Google, una crea un
  ricettario e invita le altre, e insieme ci mettono almeno venti ricette vere — la maggior parte
  incollando un link.
- Almeno una di quelle ricette viene ritrovata con la ricerca semantica da qualcuno che non l'aveva
  aggiunta.
- Il primo accesso della giornata, a macchina sospesa, è cronometrato da una persona reale e il
  numero è scritto; se dà fastidio, la macchina sempre calda è la riga che `LATER` tiene pronta ed è
  un flag.
- La bolletta del primo mese è letta e confrontata con i centesimi al mese che `arch-choices.md`
  promette, LLM ed embedding compresi.
- Un ripristino dal backup su un database vuoto rimette in piedi ricette, ricettari, membership e
  riferimenti alle foto.

## Learning target

Che l'insieme regga fuori dal laboratorio: che le persone aggiungano ricette senza che nessuno
spieghi loro come si fa, che la ricerca semantica sia il motivo per cui tornano invece di una
curiosità mostrata una volta, e che il conto a fine mese sia quello che le sorgenti promettono.

## Excludes

- La macchina Fly sempre calda → `LATER`: è un flag in `fly.toml`, reversibile, e la si accende solo
  se il risveglio dà davvero fastidio.
- Ricettari pubblici, filtri di ricerca, gruppi sopra i ricettari → `LATER`.
- Ogni monitoraggio oltre ai log e alla bolletta: a questa scala il canale di allerta sono le persone
  che la usano.
- Un onboarding, una landing page o qualunque acquisizione: l'app arriva a chi riceve un link.

## Open questions

- —
