# S6 — Fallback LLM quando manca il JSON-LD

← [Register](../roadmap.md#now)

**Outcome:** Quando la pagina non espone dati strutturati, la ricetta viene estratta lo stesso
da un modello cheap con output validato, senza che l'utente debba fare nulla di diverso.

**Requested by:** `arch-choices.md` § Estrazione contenuto, secondo gradino della cascata;
`goal.md` § Differenziatore, che dichiara l'estrazione LLM il rimedio ai siti senza dati
strutturati.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Sviluppatori e tester sull'ambiente di staging: il link che prima si fermava con "nessuna
ricetta nella pagina" ora produce una ricetta salvata.

## Includes

- Pulizia dell'HTML in testo leggibile, come ingresso del modello.
- Chiamata al modello di estrazione (Claude Haiku 4.5, assunzione della mappa) con output
  strutturato, timeout e un solo ritentativo.
- Validazione dell'uscita con `Schema`, mai un cast: un'uscita che non passa è un errore, non
  una ricetta.
- Innesto come secondo ramo della cascata di `S5`: stessi passi di progresso, stessa
  tassonomia di errori, stesso salvataggio senza review.
- `tags` e `prepTime` derivati best-effort e mai chiesti: la loro assenza non blocca niente.
- Costo di ogni chiamata registrato a log.

## Verification

Su tre pagine reali prive di JSON-LD, di cui una pesantemente JavaScript, la ricetta si salva
con nome, ingredienti e preparazione riconoscibili. Un'uscita del modello che non rispetta lo
schema produce un errore al passo "leggo ricetta" e nessuna ricetta corrotta in banca dati. Il
costo medio misurato su dieci estrazioni sta nelle frazioni di cent che il piano assume, letto
dal log. Le pagine con JSON-LD continuano a non chiamare il modello, verificabile dal log
delle stesse tre pagine di `S5`.

## Learning target

Se un modello cheap con uscita validata produca estratti che un utente accetta senza
correggerli, e a quale costo reale per ricetta.

## Excludes

- Ingresso da testo incollato: è di `S7`, che riusa questo motore.
- OCR da foto e import da file esportati da altre app: candidati.
- Review obbligatoria dell'estratto: fuori scope dichiarato, la correzione resta in modifica.

## Open questions

- —
