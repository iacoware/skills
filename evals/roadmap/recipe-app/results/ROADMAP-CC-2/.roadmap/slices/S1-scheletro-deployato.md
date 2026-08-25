# S1 — Scheletro deployato su Fly con Postgres e pgvector

← [Register](../roadmap.md#now)

**Outcome:** Un URL raggiungibile su Fly serve l'app dal container, parla con il Postgres gestito
attraverso il driver reale, applica le migration dal runner nella pipeline e sa scrivere e rileggere
un vettore con pgvector.

**Requested by:** Prerequisito dello scheletro deployato per il lavoro greenfield; infrastruttura da
`arch-choices.md` (§ Datastore, § Hosting).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi sviluppa. Dopo questa riga può consegnare una riga di dominio sapendo che, se qualcosa non
risale, non è per il deploy, per la connessione al database, per le migration o per l'estensione
vettoriale.

## Includes

- Provisioning dell'app Fly con `fly.toml`: container Docker, `auto_stop` in modalità `suspend`,
  scale-to-zero, nessun volume.
- Database Postgres gestito sul provider scelto, raggiunto in TCP dal driver standard, con la
  configurazione di pool che il contenitore che si sospende richiede.
- Runner di migration eseguito dalla pipeline di deploy, che applica una migration non di dominio:
  una tabella di servizio e `CREATE EXTENSION vector`, con un indice HNSW su una colonna vettoriale
  di quella tabella.
- Un endpoint di salute non di dominio che scrive una riga con un vettore, la rilegge con
  l'operatore di distanza e riporta l'esito.
- Deploy dalla pipeline di S0, non dalla macchina di chi sviluppa.

## Verification

L'URL pubblico dell'app risponde e l'endpoint di salute riporta l'esito reale del round-trip: la riga
è stata scritta sul Postgres gestito e riletta con l'operatore di distanza, con il valore atteso. La
migration risulta applicata dal runner in pipeline e non a mano, e rieseguire il deploy non la
riapplica. Dopo dieci minuti di inattività la prima richiesta risponde, e il tempo di risveglio è
misurato e scritto: è il numero contro cui si rileggerà l'esperienza di aggiunta sincrona. Un deploy
con una stringa di connessione errata fallisce in modo visibile invece di servire una pagina che
finge.

## Learning target

Le tre decisioni infrastrutturali prese sulla carta reggono insieme: container Fly che si sospende,
Postgres gestito raggiunto in TCP con un pool che sopravvive alla sospensione, e pgvector abilitabile
via migration sul piano gratuito del provider. Se una delle tre non regge, si scopre qui, dove il
fallimento può essere di una sola di esse.

## Excludes

- Qualunque entità di dominio, CRUD, autenticazione e nozione di ricettario: sono di S3 e S7.
- Object storage, provider LLM e provider di embedding: ciascuno ha una sola riga che lo usa e sarà
  quella a validarlo (S8, S5, S6).
- Il dominio di produzione e le credenziali di produzione: sono di S11. Questo ambiente è non
  pubblico e serve a chi sviluppa e a chi prova.

## Open questions

- **Neon o Supabase.** `arch-choices.md` li nomina entrambi senza sceglierne uno. Entrambi offrono
  pgvector sul piano gratuito e nessuno dei due cambia la forma della mappa; la scelta si prende qui,
  perché è qui che si apre il progetto e si misura il comportamento della connessione contro la
  sospensione della macchina.
- **`postgres.js` o `node-postgres`.** `tech-choices.md` li nomina entrambi. Si sceglie qui, con il
  criterio del comportamento del pool alla riapertura dopo lo scale-to-zero, che è l'unica differenza
  che conta a questa scala.
