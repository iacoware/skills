# S4 — Ricerca semantica cross-lingua nel ricettario

← [Register](../roadmap.md#now)

**Outcome:** Si cerca una ricetta descrivendola a parole proprie e il ricettario corrente restituisce
quelle che c'entrano, anche quando sono scritte in un'altra lingua.

**Requested by:** `sources/goal.md`, «Ricerca (MVP: solo semantica)» e il differenziatore;
`sources/concepts.md`, la query di similarità scoped al ricettario; il modello scelto da `S2`.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi costruisce e prova l'app, sullo stesso ambiente deployato e sullo stesso ricettario configurato.
Dopo questa riga può scrivere cosa gli va di mangiare, con parole sue e nella sua lingua, e ottenere
le ricette che c'entrano invece di scorrere l'elenco.

## Includes

- L'embedding di una ricetta derivato al salvataggio e ri-derivato a ogni modifica, da
  `nome + ingredienti + preparazione`, più `tags` e `prepTime` quando ci sono.
- Il modello scelto dallo spike, chiamato solo in scrittura.
- La colonna vettoriale sulla tabella `Recipe` vera, con il suo indice HNSW, e il riempimento a
  posteriori delle ricette già scritte.
- Il campo di ricerca e la lista dei risultati sulla home, con la query embeddata al momento della
  ricerca e la similarità filtrata sul ricettario corrente, attraverso lo stesso risolutore.
- Il corpus e l'insieme di query dello spike tenuti come test di regressione.

## Verification

Sull'ambiente deployato una query in italiano recupera una ricetta scritta in inglese, e il test di
regressione sul corpus dello spike tiene il recall che lo spike aveva registrato — se scende, è la
misura del prodotto a smentire quella del laboratorio. Una ricetta modificata cambia subito posizione
nei risultati: l'embedding è derivato e non stantio. Una ricetta di un altro ricettario non compare
mai. Una query che non incontra niente lo dice, invece di mostrare tutto. Se la chiamata di embedding
fallisce, la ricetta resta salvata e visibile nell'elenco, segnalata come non ancora cercabile, e una
modifica successiva la rimette in ordine. La p95 della richiesta di ricerca sull'ambiente deployato è
riportata, e il costo per query è riportato accanto.

## Learning target

Il differenziatore tiene nel prodotto e non solo nello spike: un embedding derivato al salvataggio e
una query embeddata al momento della ricerca fanno trovare a una persona una ricetta che non sa
nominare, attraverso le lingue, senza che venga mai digitata una parola chiave.

## Excludes

- Nessun filtro strutturato per tag o tempo e nessuna ricerca ibrida: sono candidati, e i campi si
  popolano già così che diventino abilitabili senza migrazione.
- Nessuna ricerca su più ricettari: è candidata, e lo scope resta quello corrente.
- Nessun riordino manuale dei risultati e nessuna paginazione oltre quella che le centinaia di
  ricette per ricettario richiedono.

## Open questions

—
