# S3 — Ricetta a mano, elenco e ricettario corrente

← [Register](../roadmap.md#now)

**Outcome:** Si crea, si corregge e si rilegge una ricetta scritta a mano, e l'elenco mostra
solo le ricette del ricettario corrente.

**Requested by:** `goal.md` §§ Home, Aggiunta ricetta; `concepts.md` § Entità principali, che
definisce `Recipe` e `Cookbook`.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Sviluppatori e tester sull'ambiente di staging, non pubblico: possono salvare ricette che
conoscono e correggerle, e da qui in poi ogni riga ha ricette vere su cui appoggiarsi.

## Includes

- Migrazioni per `Cookbook` e `Recipe` (`name`, `ingredients`, `steps`, `prepTime`
  opzionale, `tags`, `sourceUrl` opzionale, `cookbookId`), con un ricettario seed creato
  dalla migrazione.
- Un unico risolutore del ricettario corrente, letto da configurazione, attraverso cui
  passano tutte le letture e le scritture di ricette: è il seam che `S9` sostituirà.
- Servizio di accesso alle ricette come porta `Context.Tag` con adapter Drizzle in `Layer`.
- Un solo form per creazione e correzione: titolo, ingredienti e preparazione come testo
  libero su più righe, nessun parsing, nessun campo obbligatorio oltre il titolo, nessun
  passo prima del salvataggio.
- Elenco delle ricette del ricettario corrente, con apertura in lettura e in modifica.
- Colonne `tags` e `prepTime` create qui ma mai chieste all'utente: restano vuote finché
  un'estrazione non le popola.

## Verification

Una ricetta salvata con ingredienti su più righe e caratteri accentati ricompare identica
nell'elenco, in lettura e nel form di modifica, dopo che la macchina Fly si è riaddormentata
e risvegliata. Una ricetta scritta in un secondo ricettario non compare nell'elenco mentre il
risolutore punta al primo. Un test dimostra che nessuna query di ricette viene eseguita senza
il vincolo di ricettario, cioè che non esiste un accesso che scavalchi il risolutore. Salvare
con i soli campi obbligatori riesce.

## Learning target

Che la normalizzazione minima regga l'intero giro creazione-correzione-lettura senza chiedere
niente all'utente, e che un solo risolutore basti a tenere ogni accesso dentro un ricettario
prima ancora che esista un'identità.

## Excludes

- Foto: sono di `S4`.
- Embedding e ricerca: sono di `S8`, che possiede la pipeline alimentata da questa riga.
- Autenticazione e ricettari multipli scelti dall'utente: sono di `S9` e `S10`.
- Popolamento di `tags` e `prepTime`: appartiene alle estrazioni, `S5`, `S6` e `S7`.

## Open questions

- —
