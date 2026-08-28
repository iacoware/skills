# S1 — Scheletro deployato su Fly

← [Register](../roadmap.md#now)

**Outcome:** Un'app Next.js deployata su Fly in ambiente di staging risponde a una richiesta
leggendo e scrivendo su Postgres attraverso il driver reale, dopo che il runner ha applicato una
migrazione.

**Requested by:** Prerequisito dello scheletro della skill; la configurazione viene da
`arch-choices.md` (*Hosting*) e da `tech-choices.md` (*Persistenza / ORM*).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi sviluppa: da qui in poi ogni riga si deploya invece di girare solo in locale, e il rischio di
driver, connessione e migrazione è già stato pagato fuori da una riga di dominio.

## Includes

- Dockerfile e `fly.toml` per un'app Fly di staging, con `auto_stop` in modalità `suspend` e
  scale-to-zero, container stateless senza volumi.
- CD dalla CI: un push verde deploya.
- Runner di migrazione Drizzle eseguito al deploy, con una prima migrazione non di dominio che crea
  l'estensione `vector` e una tabella di sonda con una colonna scalare e una colonna `vector`.
- Un endpoint non di dominio che a ogni chiamata scrive una riga nella tabella di sonda, la rilegge
  e calcola una distanza vettoriale fra due valori costanti, tutto attraverso il driver Postgres
  standard su TCP.
- Misura del tempo della prima richiesta dopo un periodo di inattività, registrata nel repository.

## Verification

Un push verde produce un deploy senza intervento manuale. Chiamato l'endpoint, la risposta contiene
il valore appena scritto e riletto da Postgres e il risultato dell'operatore di distanza: una
risposta statica non passa. Il log del deploy mostra la migrazione applicata, e un secondo deploy
non la riapplica. Dopo un'attesa sufficiente a far sospendere la macchina, la prima richiesta ha
successo e il suo tempo è misurato e scritto, non stimato: se non fosse sotto il secondo che le
fonti promettono, il numero lo dice.

## Learning target

Se `suspend` più scale-to-zero e un driver Postgres standard su TCP reggono il ciclo
sospensione-risveglio senza connessioni morte, e quanto costa davvero la prima richiesta dopo il
silenzio — perché è l'unica cosa che può obbligare a tenere la macchina calda, e quella è una voce
di costo.

## Excludes

- Nessuna entità di dominio, nessun CRUD, nessuna autenticazione, nessuno scope: la prima entità
  arriva con S3.
- Nessun adapter esterno che una riga sola userà: R2 è di S7, l'LLM di S6, l'embedder di S4.
- Nessun ambiente di produzione: è di S10.

## Open questions

- —
