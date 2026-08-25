# S4 — Aggiunta da link con JSON-LD e avanzamento reale

← [Register](../roadmap.md#now)

**Outcome:** Si incolla l'URL di una pagina di ricetta, si vede l'avanzamento sui passi realmente
eseguiti, e la ricetta è nel ricettario senza aver compilato nulla e senza aver confermato nulla —
gratis, quando la pagina espone `schema.org/Recipe`.

**Requested by:** `goal.md` (§ Cosa fa (MVP) → Aggiunta ricetta: estrazione sincrona con progress bar
sui passi reali, nessuna review obbligatoria) e `arch-choices.md` (§ Estrazione contenuto, passo 1) e
`concepts.md` (§ Pipeline di estrazione).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi sviluppa e chi prova l'app sull'ambiente non pubblico. Dopo questa riga può aggiungere una
ricetta incollando un link, invece di ricopiarla a mano dal blog.

## Includes

- Un campo per l'URL nella home e il flusso di aggiunta che ne segue.
- Scaricamento della pagina con l'`HttpClient` di Effect: timeout esplicito, redirect seguiti,
  user-agent onesto, errore distinguibile per pagina irraggiungibile, risposta non HTML, o corpo
  troppo grande.
- Estrazione del JSON-LD `schema.org/Recipe` e decodifica con `Schema` in un modello di ricetta, mai
  con un cast: nome, ingredienti e preparazione riportati a testo libero, `prepTime` e `tags`
  riempiti quando la pagina li dà e lasciati vuoti quando non li dà.
- `sourceUrl` salvato sulla ricetta.
- Avanzamento sui passi realmente eseguiti, trasmesso al client mentre accadono: quando un passo
  fallisce, il messaggio nomina quel passo e dice cosa si può fare — che, per una pagina illeggibile,
  è il percorso che S5 apre.
- Salvataggio immediato senza passo di review, e apertura della ricetta salvata, da cui il form di
  S3 è a un click per correggere.

## Verification

Su una lista dichiarata di una quindicina di URL reali dei siti che questa famiglia usa davvero, si
conta e si scrive quante pagine producono una ricetta salvata con il solo JSON-LD, e per quante il
JSON-LD manca. Su un URL che lo espone, la ricetta salvata ha titolo, ingredienti e preparazione
riconoscibili rispetto alla pagina, e `sourceUrl` valorizzato. L'avanzamento mostra i passi mentre
accadono e non dopo, e i passi mostrati corrispondono a quelli eseguiti (verificabile confrontandoli
con il log della richiesta). Su un URL protetto da paywall e su un URL inesistente il flusso si ferma
sul passo giusto con un messaggio che lo nomina, e non resta nessuna ricetta a metà nel database.
Aprendo la ricetta salvata e correggendola col form di S3, la correzione persiste. Nessuna chiamata a
pagamento è partita: il contatore del provider non si muove.

## Learning target

Il JSON-LD `schema.org/Recipe` copre una quota dei siti che questa famiglia usa davvero abbastanza
alta da rendere la maggior parte delle aggiunte gratuite — e l'estrazione sincrona con avanzamento
reale sta dentro un tempo che non fa sembrare l'app rotta, compreso il caso in cui la macchina Fly si
stava risvegliando.

## Excludes

- Il fallback su LLM per le pagine senza JSON-LD e l'ingresso da testo incollato: sono di S5, che è
  il recupero dichiarato del fallimento di questa riga e la segue immediatamente.
- Il download della foto dalla pagina: è di S8, che possiede l'object storage. Fino ad allora
  l'avanzamento non ha il passo "Salvo foto", perché i passi mostrati sono solo quelli veri.
- L'embedding della ricetta salvata: è di S6, che lo genera per tutti e tre i percorsi di aggiunta e
  riempie a ritroso quelle già salvate.

## Open questions

- —
