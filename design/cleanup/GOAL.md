# Obiettivi del /cleanup skill

I modelli tendono ad accumulare documentazione, regole e anche codice senza mai eliminare l'esistente, se non su richiesta esplicita.

In questo modo i documenti markdown accumulano sempre più prosa: diventano nel tempo illeggibili per l'umano e confondono l'agente, riportando affermazioni ambigue e non amalgamate con il resto, creando rumore e diluendo l'attenzione del modello.

## Perché l'agente accumula

L'accumulo non è pigrizia, è il risultato di incentivi asimmetrici:

- **Il costo è differito e non lo paga chi scrive.** L'attenzione diluita ricade su una sessione futura, non su quella che ha risolto il problema; nessun ciclo di feedback si chiude su chi ha aggiunto la riga, quindi il file appare gratis ogni volta che si decide di allungarlo.
- **Aggiungere sembra diligenza, togliere sembra rischio.** In teoria le due azioni sono simmetriche, all'atto pratico no: per cancellare bisogna dimostrare che _nessuno_ ne ha bisogno, per aggiungere basta che _qualcuno_ potrebbe averne bisogno.
- **Il momento in cui si scrive è il peggiore possibile.** A fine ticket la comprensione appena acquisita sembra preziosa in proporzione a quanto è costata ottenerla, non a quanto servirà dopo: mezz'ora di indagine diventa un paragrafo caricato per sempre.
- **«Documenta quello che abbiamo imparato» non ha criterio di completamento.** Ha un pavimento e nessun soffitto: un'istruzione così ha un solo esito possibile nel tempo, la sedimentazione.
- **Si scrive per giustificare, non per istruire.** La prosa che argomenta le decisioni di design è un registro che convince chi legge e gonfia il conto; una checklist direbbe le stesse cose in un terzo dello spazio.

## Rimedi strutturali

La buona volontà del modello non basta: è esattamente ciò che produce l'accumulo. Servono due vincoli strutturali:

- **Il gesto di default deve cambiare bersaglio.** Il posto dove scrivere il perché è il file che si sta modificando: il codice porta il proprio perché addosso e non può andare stale. CLAUDE.md prende solo ciò che non ha un altro file dove stare.
- **Serve un soffitto dichiarato.** Un numero, scritto in CLAUDE.md stesso: superato quello, aggiungere una riga obbliga a toglierne un'altra. Senza soffitto il file torna a gonfiarsi in pochi mesi.

## Documenti e artefatti da sistemare

- CLAUDE.md, AGENTS.md (in genere symlinkati in una direzione o nell'altra)
- README.md
- docs/\*.md
- Commenti nel codice
- Codice non usato
- Semplificazioni nel codice

## Come deve comportarsi

Nessuna modifica deve essere fatta in questa fase. Presentare un report in cui mostra in modo chiaro un elenco di artefatti (documenti/codice):

- Nome del doc.
- Obiettivo del doc
- Elenco di modifiche e cancellazioni numerate in modo che l'utente possa usare il numero come riferimento per accettare/rifiutare:
    - Cosa suggerisce di togliere
    - Perché suggerisce di togliere
