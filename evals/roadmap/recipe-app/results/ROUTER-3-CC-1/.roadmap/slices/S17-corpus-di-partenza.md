# S17 — Corpus di partenza: migliaia di ricette da ricettari non coordinati

← [Register](../roadmap.md#now)

**Outcome:** Esistono davvero migliaia di ricette in decine di ricettari tematici pronti alla
pubblicazione, catturate con la pipeline consegnata da fonti che nessuno ha messo d'accordo, con il
costo una tantum e il rumore dell'estrazione dichiarati.

**Requested by:** L'input dell'autore (la ricerca deve funzionare su un corpus pubblico di migliaia
di ricette, in ricettari che nessuno ha curato insieme). Nasce dallo scorporo di `S13`, che portava
il corpus in una riga di `Includes`.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi lavora al progetto: ha un banco di prova che non abbiamo reso ordinato senza accorgercene, e sa
quanto costa costruirlo prima di spendere quel costo.

## Includes

- Migliaia di ricette — l'ordine di grandezza dichiarato dall'autore, sotto il ≤10k delle sorgenti —
  distribuite in decine di ricettari tematici, non in tre.
- Fonti che nessuno ha messo d'accordo: domini diversi, temi che si sovrappongono, italiano e inglese
  mescolati, e nessuna scelta fatta per rendere il corpus coerente.
- La pipeline consegnata usata così com'è — JSON-LD quando c'è, fallback LLM quando manca, embedding
  a ogni salvataggio — perché il corpus deve avere la qualità di estrazione che ha il prodotto,
  difetti compresi.
- Il conto una tantum dichiarato prima di spenderlo: chiamate LLM, embedding, e volume delle foto
  contro il free tier di R2.
- I ricettari restano privati: questa riga costruisce il corpus, non decide di pubblicarlo.

## Verification

Il numero di ricette e di ricettari è dichiarato, e con esso la forma del corpus: quante ricette per
ricettario, quanti temi si sovrappongono, la proporzione fra le due lingue, quante ricette vengono
dallo stesso dominio d'origine e quante volte lo stesso URL è stato catturato in ricettari diversi.
La quota di estrazioni passate da JSON-LD e quella passata dall'LLM è dichiarata, con un campione
letto a mano che dice quante ricette sono sbagliate o vuote: è il rumore su cui `S13` misurerà. Il
costo una tantum è dichiarato voce per voce contro il preventivo delle sorgenti, e il volume su R2
contro il suo free tier, dicendo quale voce lo sfonda se lo sfonda. Nessun ricettario di questa riga
è pubblico.

## Learning target

Se un corpus della forma che l'autore descrive — migliaia di ricette in ricettari che nessuno ha
coordinato — si può mettere insieme con la pipeline consegnata, a che costo e con quanto rumore
dentro.

## Excludes

- La misura della ricerca su questo corpus: è di `S13`, la riga a cui il corpus serve.
- La pubblicazione dei ricettari e ciò che la pagina pubblica può mostrare: è di `S12`.
- La deduplica: esclusa dalla mappa; qui i duplicati si contano, non si tolgono.
- Qualunque correzione alla pipeline di cattura: estrazioni peggiori del previsto sono un risultato
  di questa riga, non un suo lavoro.

## Open questions

- Se il materiale estratto da pagine altrui possa essere ripubblicato. Costruire migliaia di ricette
  estratte ha senso solo se possono diventare pubbliche: è la domanda aperta a livello di mappa, e
  finché non ha risposta il valore di questa riga resta sospeso.
- Chi pubblica questi ricettari: se li pubblichiamo noi, il primo editore del corpus siamo noi.
