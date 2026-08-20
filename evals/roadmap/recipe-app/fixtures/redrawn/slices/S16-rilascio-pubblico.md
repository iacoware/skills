# S16 — Rilascio pubblico

← [Register](../roadmap.md#now)

**Outcome:** Il corpus pubblico sta davanti a traffico anonimo e a crawler a un costo dichiarato, con
un tetto che blocca invece di fatturare.

**Requested by:** La nuova meta dichiarata dall'autore (chiunque, senza account),
`sources/arch-choices.md` (Hosting — cold start, scale-to-zero e costo; Riepilogo costi),
`sources/goal.md` (Principi guida — budget bassissimo). La riga di rilascio archiviata aveva scelto
la posizione di hosting per famiglia e amici.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chiunque arrivi, incluso chi arriva per primo dopo ore di silenzio e non ha nessun motivo di
aspettare; e chi paga il conto a fine mese.

## Includes

- La posizione di hosting rivista per il pubblico: `suspend` con scale-to-zero contro macchina sempre
  calda, decisa sulla latenza osservata sul traffico anonimo e non su quella di famiglia.
- Cache delle pagine pubbliche anonime, coerente con la propagazione dichiarata quando una visibilità
  cambia.
- Tetti di spesa aggiornati presso il provider di embedding, dimensionati sulle ricerche che ora può
  innescare chiunque.
- Il costo osservato su una settimana di traffico reale e di crawler, messo accanto al preventivo
  delle sorgenti.

## Verification

Il primo accesso anonimo dopo un periodo di silenzio sta entro la soglia scelta, e la soglia è
scritta. Una pagina pubblica servita dalla cache non tocca il database, e una visibilità tolta si
propaga entro la finestra dichiarata nei concerns. Superare il tetto di spesa blocca le chiamate
invece di produrre una fattura: è un limite imposto dal provider, non un buon proposito. Il costo
della settimana osservata è dichiarato voce per voce contro il preventivo, e la riga dice quale voce
lo sfonda se lo sfonda.

## Learning target

Se il preventivo delle sorgenti — centesimi al mese — sopravvive al pubblico, o se la scoperta ha un
prezzo che il progetto non aveva messo a bilancio.

## Excludes

- Monitoring e alerting oltre i log già previsti dai concerns: non richiesti.
- Coda di moderazione e flusso di segnalazione: restano candidati; la via d'uscita è togliere dal
  pubblico, e la possiede `S12`.
- IaC versionata: resta candidata, qui bastano `fly.toml` e la CLI.

## Open questions

- Si resta su `suspend` con scale-to-zero, o si passa alla macchina sempre calda? La scelta era già
  stata fatta per famiglia e amici, e il pubblico la riapre: adesso il primo accesso dopo il silenzio
  non è di un parente che aspetta, è di uno sconosciuto o di un crawler.
