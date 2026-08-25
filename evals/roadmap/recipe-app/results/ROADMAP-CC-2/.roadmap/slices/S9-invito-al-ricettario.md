# S9 — Invito al ricettario e membri alla pari

← [Register](../roadmap.md#now)

**Outcome:** Chi ha creato un ricettario genera un link, lo manda a chi vuole, e da quel momento chi
lo apre legge, aggiunge, corregge e cerca dentro lo stesso ricettario, alla pari.

**Requested by:** `goal.md` (§ Condivisione: creator che invita tramite link/codice, membri pari) e
`concepts.md` (§ Modello di condivisione: cookbook-centrico; § Entità principali: `Invitation`).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Le famiglie e i gruppi di amici a cui l'app è destinata. È la riga che trasforma un archivio
personale nella cosa che il prodotto promette di essere.

## Includes

- Schema e migration per `Invitation` (`cookbookId`, token, scadenza opzionale), con token generato
  da un generatore crittografico.
- Generazione del link di invito dalla pagina del ricettario, da parte del creator.
- Accettazione: chi apre il link da autenticato ottiene una `Membership` e finisce dentro il
  ricettario; chi lo apre da non autenticato passa dall'entrata con Google e poi vi finisce comunque.
- Elenco dei membri del ricettario, così che si veda chi c'è dentro.
- Un token già consumato, scaduto o inesistente non crea nulla e lo dice, senza rivelare quale
  ricettario c'era dietro.
- Nessun ruolo: l'unica domanda di autorizzazione resta l'esistenza della `Membership`.

## Verification

Un utente A crea una ricetta e genera il link di invito; un utente B, con un altro account Google,
apre il link e vede l'elenco di A. B aggiunge una ricetta da link e A la vede; B corregge una ricetta
di A e A vede la correzione; B cerca e i risultati comprendono le ricette di entrambi, perché lo
scope è il ricettario e non l'utente. Un utente C, che non ha aperto nessun invito, non vede nulla:
né dall'elenco, né dalla ricerca, né dall'URL diretto di una ricetta. Un token manomesso di un
carattere non crea alcuna `Membership`. Un token scaduto viene rifiutato con un messaggio che non
nomina il ricettario. Aprendo due volte lo stesso link, B non ottiene due `Membership`.

## Learning target

La condivisione aggregata attorno al ricettario, senza ruoli e senza permessi, basta davvero al modo
in cui una famiglia usa un ricettario: nessuno chiede la sola lettura, e la parità completa fra
membri non produce il danno che i permessi granulari servirebbero a prevenire.

## Excludes

- La creazione di ricettari ulteriori e il passaggio dall'uno all'altro: sono di S10.
- Ricettari pubblici tematici (`visibility=public`): candidato dichiarato fuori MVP, abilitabile poi
  senza migrazione perché il campo esiste già da S3.
- Un concetto di gruppo sopra i ricettari, per non ri-invitare le stesse persone in ognuno:
  candidato, con lo svantaggio accettato esplicitamente dalle fonti.
- Revoca di una `Membership` e rimozione di un membro: non chieste dalle fonti; se servissero,
  saranno un candidato.

## Open questions

- —
