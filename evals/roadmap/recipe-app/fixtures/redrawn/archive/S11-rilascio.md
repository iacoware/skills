# S11 — Rilascio a famiglia e amici

← [Register](../roadmap.md#now)

**Outcome:** Famiglia e amici usano l'app su un indirizzo stabile, con la spesa sotto controllo e
senza sorprese al primo accesso.

**Requested by:** `sources/goal.md` (Visione, Principi guida — budget bassissimo),
`sources/arch-choices.md` (Hosting — cold start e costo, Riepilogo costi).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Famiglia e amici: aprono un link, entrano con Google e usano il ricettario senza che nessuno debba
spiegargli niente.

## Includes

- Dominio e certificato su Fly, con i redirect OAuth di produzione.
- Consent screen Google configurato per utenti reali.
- La scelta fra `suspend` con scale-to-zero e macchina sempre calda, presa sulla latenza misurata in
  `S1` e su quella osservata dai primi utenti.
- Backup e point-in-time recovery su Neon, verificati con un restore di prova.
- Tetto di spesa impostato presso il provider di embedding e quello del modello di fallback.

## Verification

Una persona invitata che non ha mai visto l'app arriva dal link a una ricetta cercata in meno di un
minuto, senza istruzioni. Il primo accesso dopo ore di silenzio sta entro la soglia scelta, e la
soglia è scritta. Un restore di prova riporta il database a uno stato precedente e l'app riparte. Il
tetto di spesa è un limite imposto dal provider, non un buon proposito: superarlo blocca le chiamate
invece di produrre una fattura.

## Learning target

Se il costo reale a traffico di famiglia sta dove le sorgenti lo mettono, o se il target di
centesimi al mese era ottimismo.

## Excludes

- Monitoring e alerting oltre i log già previsti dai concerns: non richiesti dalle sorgenti.
- IaC versionata: resta candidata, qui bastano `fly.toml` e la CLI.
- Onboarding guidato, email di benvenuto, pagine pubbliche: esclusi, non c'è provider email.

## Open questions

- Si parte con `suspend` e scale-to-zero a centesimi al mese, o con la macchina sempre calda a
  ~$3/mese? Le sorgenti consigliano la prima e lasciano la seconda come flag reversibile, ma non
  scelgono.
