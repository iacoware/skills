# S10 — Rilascio a famiglia e amici

← [Register](../roadmap.md#now)

**Outcome:** L'app gira in produzione con il proprio database, il proprio bucket e le credenziali
Google di produzione, e le prime persone reali ci entrano dal loro telefono e ci lavorano.
**Requested by:** Fine di `NOW` per un `NOW` che punta a utenti reali; prontezza operativa da
`arch-choices.md` § Hosting e § Riepilogo costi.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

I primi utenti reali — famiglia e amici. Dopo questa riga usano il ricettario dal telefono senza che
nessuno gliel'apra, invece di guardarlo su un ambiente di prova.

## Includes

- App Fly di produzione con `suspend` e scale-to-zero, database di produzione e bucket R2 di
  produzione, separati da quelli dell'ambiente non pubblico.
- Credenziali OAuth Google di produzione con i redirect URI giusti e le persone del gruppo
  autorizzate come tester.
- Deploy della produzione da CI con le migrazioni applicate dal runner.
- Un ricettario reale con qualche decina di ricette vere caricate dalle prime persone.
- Lettura della spesa reale dopo il primo periodo d'uso: Fly, database, R2 e chiamate LLM ed
  embedding.

## Verification

- Ognuna delle prime persone entra con il proprio account Google dal telefono, senza assistenza,
  accetta l'invito e aggiunge almeno una ricetta da link.
- Una ricerca fatta da uno dei membri trova le ricette aggiunte dagli altri.
- La prima richiesta dopo un periodo di silenzio arriva a schermo in un tempo misurato e scritto, e
  la decisione se accendere `min_machines_running` è presa su quel numero.
- La spesa del primo periodo è letta dalle fatture ed è confrontata con i "pochi centesimi al mese"
  che questa mappa assume.
- Nessun segreto di produzione compare nel repository o nei log.

## Learning target

Se il bersaglio di costo tiene quando l'app è accesa per davvero, e se il risveglio della macchina è
un fastidio accettabile per chi apre l'app una volta ogni tanto — le due cose che solo l'uso reale
può dire.

## Excludes

- Dominio personalizzato, negozio di app e qualunque forma di distribuzione oltre l'URL: nessuna
  fonte le chiede.
- La macchina sempre calda: resta un candidato, ed è la leva che questa riga misura senza tirare.
- Pubblicazione dell'app Google fuori dalla modalità testing: fuori finché il gruppo sta dentro i
  tester autorizzati.
- IaC versionata e monitoraggio strutturato: nessuna fonte li chiede per l'MVP.

## Open questions

- Nessuna.
