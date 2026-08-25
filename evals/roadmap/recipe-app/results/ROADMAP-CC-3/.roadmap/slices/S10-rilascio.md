# S10 — Rilascio a famiglia e amici

← [Register](../roadmap.md#now)

**Outcome:** L'applicazione coerente gira in produzione sul suo indirizzo, e le prime persone reali
la usano dal loro telefono senza che nessuno stia a guardarle.

**Requested by:** Il registro punta a utenti finali reali, e questa è la riga più piccola che ce li
porta. L'operatività da mettere in piedi è quella dichiarata in `sources/arch-choices.md` § Hosting
e § Riepilogo costi.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Famiglia e amici, sul loro telefono e sul loro computer, senza nessuno accanto che spieghi.

## Includes

- Applicazione Fly e database Neon di produzione, separati da staging, con i loro segreti.
- Dominio e certificato.
- Client OAuth di Google configurato per il dominio di produzione, con la schermata di consenso
  portata fuori dallo stato di test, così che possano entrare persone che non sono in una lista di
  tester.
- Migrazioni eseguite in produzione dal deploy, come in staging.
- Lettura del costo reale del primo periodo, messo accanto al target dichiarato.
- Un modo scritto di ripristinare il database, provato almeno una volta.

## Verification

Una persona che non ha mai visto il progetto entra con il proprio account Google dal dominio di
produzione, accetta un invito, aggiunge una ricetta incollando un link e la ritrova cercando a
parole sue, tutto dal telefono e senza aiuto. Il costo del primo periodo è misurato e messo accanto
al target di pochi centesimi al mese. Un ripristino del database da backup è stato eseguito almeno
una volta su staging e la procedura è scritta.

## Learning target

Che l'insieme regga fuori dalle nostre mani: che il risveglio della macchina dopo l'inattività, il
consenso OAuth aperto al pubblico e il costo reale non riservino sorprese quando a usare l'app sono
persone che non sanno niente di com'è fatta.

## Excludes

- Ogni capacità nuova: questa riga porta in produzione ciò che esiste e non aggiunge niente.
- Monitoraggio elaborato, quote e limiti d'uso, che nessuna sorgente chiede.
- Infrastruttura come codice versionata, esclusa esplicitamente in `OUT-OF-SCOPE`.

## Open questions

- Chi possiede gli account di produzione — Fly, Neon, R2, Google Cloud — e su quale dominio va
  pubblicata l'applicazione? Nessuna sorgente lo dice, e finché l'autore non lo indica la riga non
  può partire.
