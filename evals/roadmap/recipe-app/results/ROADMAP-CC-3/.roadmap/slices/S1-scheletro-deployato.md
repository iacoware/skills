# S1 — Scheletro deployato su Fly con Postgres e migrazioni

← [Register](../roadmap.md#now)

**Outcome:** La più piccola applicazione deployata che dimostra che il container su Fly, il
database Postgres e il runner di migrazioni sono davvero collegati e vivi in un ambiente di
staging.

**Requested by:** Prerequisito dello scheletro richiesto dal metodo. L'infrastruttura da provare è
quella già decisa in `sources/arch-choices.md` § Datastore e § Hosting.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi lavorerà sulle righe di prodotto. Dopo questa riga possono dare per acquisito che una modifica
raggiunge un ambiente vero, che il database risponde e che una migrazione viene applicata, e non
devono più scoprirlo dentro una riga di dominio.

## Includes

- Dockerfile per Next.js e configurazione Fly con `auto_stop` in modalità `suspend` e
  scale-to-zero, che è la strategia consigliata dalle sorgenti.
- Applicazione Fly di staging, con deploy eseguito dalla CI di S0.
- Progetto Neon di staging, raggiunto da Drizzle con driver standard su TCP diretto, senza pooler
  serverless.
- Runner di migrazioni eseguito al deploy, con due migrazioni non di dominio: l'abilitazione
  dell'estensione `vector` e una tabella tecnica con una riga dentro.
- Un endpoint che a ogni richiesta legge quella riga dal database e riporta l'esito
  dell'estensione `vector`.

## Verification

L'URL di staging risponde e il corpo contiene il valore letto dal database in quella richiesta e la
conferma che l'estensione `vector` è installata: la risposta non può essere statica. Una terza
migrazione aggiunta al repository risulta applicata dopo il deploy successivo, senza intervento
manuale. Dopo un periodo di inattività sufficiente a far sospendere la macchina, la prima richiesta
risponde comunque, e il tempo di risveglio misurato viene scritto. Il costo del periodo di prova è
letto sulla fattura e messo accanto al target di pochi centesimi al mese.

## Learning target

Che la combinazione decisa regga davvero: container su Fly con `suspend` e scale-to-zero, Postgres
raggiunto su TCP diretto senza pooler, migrazioni applicate dal deploy, pgvector disponibile sul
piano gratuito scelto. E quanto costa, in secondi di risveglio e in denaro.

## Excludes

- Ogni entità di dominio, ogni CRUD, ogni autenticazione e ogni nozione di ricettario: lo scheletro
  resta non di dominio apposta, perché un fallimento qui deve dire quale decisione infrastrutturale
  rivedere.
- L'object storage delle foto: lo usa una sola riga più avanti, ed è quella a doverlo validare.
- L'ambiente di produzione, che è la riga di rilascio.

## Open questions

- —
