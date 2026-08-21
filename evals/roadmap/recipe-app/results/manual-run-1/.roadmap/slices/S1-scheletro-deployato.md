# S1 — Scheletro deployato: Fly, Postgres, migrazioni

← [Register](../roadmap.md#now)

**Outcome:** Un container Next.js deployato su Fly raggiunge Postgres attraverso il driver reale su
TCP, il runner di migrazioni ha applicato una migrazione non di dominio, e il cold start dopo lo
scale-to-zero è un numero misurato invece che una speranza.

**Requested by:** `references/drawing-the-map.md`, il prerequisito dello scheletro; le decisioni di
hosting, datastore e indice vettoriale di `sources/arch-choices.md`.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi costruisce l'app. Dopo questa riga ha un ambiente non di produzione a cui spedire lavoro, e sa se
l'infrastruttura decisa sulla carta sta in piedi — prima che una qualunque riga di dominio possa
fallire per colpa sua.

## Includes

- `Dockerfile` per Next.js in modalità standalone, e `fly.toml` con `auto_stop` in `suspend` e
  `min_machines_running` a zero.
- Database Neon collegato, raggiunto dal container con il driver Postgres standard su TCP — nessun
  driver serverless.
- Runner di migrazioni Drizzle agganciato al passo di release del deploy.
- Una sola migrazione non di dominio: una tabella `heartbeat`, l'estensione `vector` abilitata e una
  tabella `probe` con una colonna vettoriale e il suo indice HNSW.
- Una rotta `/health` che scrive una riga in `heartbeat`, la rilegge attraverso Drizzle e la
  restituisce.
- La misura del primo tempo di risposta dopo che la macchina si è sospesa, e dopo che si è fermata
  del tutto.

## Verification

L'URL deployata risponde con la riga che ha appena scritto e riletto su Neon: il percorso attraversa
il driver reale, non una risposta statica. Il log del deploy mostra la migrazione applicata, e un
secondo deploy la mostra idempotente. `CREATE EXTENSION vector` e la creazione dell'indice HNSW
riescono sul provider scelto, e un fallimento qui è la confutazione dell'assunzione su Neon. Il primo
tempo di risposta dopo `suspend` è riportato e confrontato con il sub-secondo che le fonti
promettono; il primo tempo dopo l'arresto completo è riportato accanto. Il bundle deployato non
contiene nessun segreto. Il costo di questo deploy in esercizio per una settimana è letto sul conto
reale e riportato.

## Learning target

L'infrastruttura decisa — container Fly con `suspend` e scale-to-zero, Neon su TCP con driver
standard, migrazioni Drizzle al release, pgvector con indice HNSW — è collegata e funziona insieme, e
il suo cold start è un fastidio e non un limite architetturale.

## Excludes

- Nessuna entità di dominio, nessun CRUD, nessuna autenticazione, nessuna tenancy: farebbero uno
  scheletro sovradimensionato, e ognuna di quelle cose si valida da sola più avanti.
- Nessun object storage: l'adapter è aperto e posseduto dalla riga delle foto, che è l'unica a
  scriverci e arriva dopo tutte quelle che la alimentano.
- Nessuna chiamata a modelli: embedding ed estrazione arrivano con le righe che li usano.

## Open questions

—
