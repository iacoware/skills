# Roadmap log

## 2026-09-03 — Drawing

- `ricettario` / `import` — **split.** L'import si cancella intero e il ricettario regge lo stesso:
  `goal.md` dà l'inserimento a mano come modo autonomo di aggiungere una ricetta, non come ripiego
  dell'import.
  Argument: l'evidenza del ricettario è "scrivo una ricetta, la ritrovo, la correggo", e non nomina
  da dove il testo arriva.
- `import` / `ricerca` — **split.** La ricerca semantica si rinvia intera senza invalidare l'evidenza
  dell'import: una ricetta importata è salvata, elencata e leggibile senza che nessun embedding
  esista.
  Argument: condividono la tabella `Recipe` e nient'altro, e una tabella condivisa non è una ragione
  per fondere valore schedulabile separatamente.
- `ricerca` / `identita` — **split.** La ricerca è verificabile su un ricettario a proprietario
  configurato, prima che esista un login; e il login regge su un ricettario che si scorre soltanto.
- `identita` / `condivisione` — **split.** La condivisione si cancella intera e il login regge:
  resta un'app monoutente con `creatorId` come unico ruolo, che è esattamente ciò che `concepts.md`
  descrive prima che arrivi una `Membership` di qualcun altro.
- `condivisione` / `foto` — **split.** Le foto si rinviano intere senza invalidare l'evidenza della
  condivisione: due membri che editano la stessa ricetta di testo la dimostrano per intero.
