# S4 — Aggiunta da link con JSON-LD e progress reale

← [Register](../roadmap.md#now)

**Outcome:** Si incolla l'URL di una ricetta e, seguendo una barra che dice a che punto è davvero, la
ricetta compare salvata nel ricettario senza che nessuno abbia ribattuto niente.

**Requested by:** `goal.md` (Aggiunta ricetta — estrazione sincrona con progress sui passi reali,
nessuna review obbligatoria), `concepts.md` (Pipeline di estrazione) e `arch-choices.md` (Estrazione
contenuto — JSON-LD prima).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi prova l'app su staging. Da qui una ricetta trovata su un blog entra nel ricettario in un incolla
e un'attesa, che è il caso che `goal.md` chiama il più frequente.

## Includes

- Un servizio di estrazione dietro `Context.Tag`, con un solo schema di output riusato da ogni
  ingresso; in questa riga l'unica implementazione è il parser JSON-LD.
- Fetch della pagina con l'`HttpClient` di Effect, con timeout e uno `User-Agent` dichiarato.
- Parse del `schema.org/Recipe` in JSON-LD, inclusi i casi in cui sta dentro un `@graph` o in più
  blocchi nella stessa pagina, mappato sui campi di `Recipe`; tempo e tag presi quando ci sono e
  ignorati quando non ci sono.
- `sourceUrl` salvato sulla ricetta e mostrato cliccabile nel dettaglio.
- Progress sincrona sui passi che la pipeline esegue davvero — `Scarico la pagina`, `Leggo la
  ricetta`, `Salvo` — e un errore tipizzato per ciascuno: pagina non raggiungibile, risposta non
  HTML, nessuna ricetta leggibile nella pagina.
- Nessun passo di conferma: finita l'estrazione la ricetta è già salvata e si atterra sul suo
  dettaglio, dove il form di `S3` la corregge.

## Verification

- Su una lista di dieci URL reali di food blog con JSON-LD, dieci ricette entrano nel ricettario con
  titolo, ingredienti e preparazione non vuoti, e nessuna chiamata a pagamento è partita.
- Su un URL senza JSON-LD la barra si ferma al passo `Leggo la ricetta` dicendo che la pagina non
  contiene una ricetta leggibile, non con un errore generico. Il rimedio è `S5`.
- Su un URL dietro paywall o che risponde 403 la barra si ferma al passo `Scarico la pagina`
  nominando quel passo, così l'utente sa che la via d'uscita è incollare il testo. Il rimedio è `S5`.
- Dopo un'estrazione riuscita la ricetta è nel database prima che l'utente tocchi qualcosa: chiudere
  la scheda non la perde.
- La quota di URL coperti dal solo JSON-LD, su quei dieci, è contata e scritta.

## Learning target

Che il JSON-LD copra abbastanza food blog da rendere l'estrazione gratuita nella maggioranza dei
casi — `arch-choices.md` lo dà per hit-rate alto e questa riga è la prima misura — e che
un'estrazione sincrona con progress reale sia un'attesa che una persona sopporta senza un passo di
conferma alla fine.

## Excludes

- Il fallback su LLM e l'ingresso da testo incollato → `S5`, che apre l'adapter LLM e lo possiede da
  solo.
- Il download dell'immagine della pagina e il passo `Salvo la foto` nella barra → `S9`, con il resto
  del tema `foto`.
- L'embedding della ricetta importata → `S6`.
- Un browser headless per i siti che rendono in JavaScript: non è in questa mappa, e la via che le
  sorgenti danno per quei siti è il copia-incolla di `S5`.

## Open questions

- —
