## 2026-08-20 — Drawing

- `cattura` / `ricerca` — **split.** La ricerca si rinvia intera senza invalidare l'evidenza della
  cattura: una ricetta incollata è salvata anche se nessuno la cerca.
- `ricerca` / `accesso` — **split.** L'accesso si rinvia intero senza invalidare l'evidenza della
  ricerca: si cerca nel ricettario corrente anche con un solo ricettario e nessun account.
- `accesso` / `condivisione` — **split.** La condivisione si rinvia intera senza invalidare
  l'evidenza dell'accesso: entrare col proprio account e trovare il proprio ricettario è validato
  anche senza inviti.
  Argument: il merge test suonerebbe — l'accesso da solo dà poco feedback — ma lo split tiene, e lo
  split decide.
- `condivisione` / `foto` — **split.** Le foto si rinviano intere senza toccare inviti e passaggio
  fra ricettari.
