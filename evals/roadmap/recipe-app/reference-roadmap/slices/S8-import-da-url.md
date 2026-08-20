# S8 — Import da URL con JSON-LD

← [Register](../roadmap.md#now)

**Outcome:** Si incolla il link di un food blog e la ricetta si salva da sola.

**Requested by:** `sources/goal.md` § Visione, § Aggiunta ricetta,
`sources/arch-choices.md` § Estrazione contenuto
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi incolla il link di un food blog — il modo più frequente di aggiungere una ricetta, e quello per
cui l'app viene aperta.

## Includes

- Il campo per l'URL e il fetch della pagina.
- La lettura del JSON-LD `schema.org/Recipe` e il salvataggio della ricetta con `sourceUrl`.
- La barra di avanzamento sui passi reali, con un messaggio preciso quando un passo fallisce.

## Verification

Incollando l'URL di un blog con dati strutturati la ricetta si salva senza altri passaggi e la si
trova cercandola; su una pagina che non si riesce a scaricare il messaggio dice quale passo è
fallito e perché.

## Learning target

Che il JSON-LD dei siti che usiamo davvero contenga abbastanza per una ricetta leggibile, senza
chiamare nessun modello a pagamento.

## Excludes

- Il fallback quando il JSON-LD manca, che è `S9`.
- Il copia-incolla, che è `S10`.
- Le foto trovate nella pagina, che sono `S11`.

## Open questions

—
