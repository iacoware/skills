# S7 — Entri con Google: il ricettario è tuo

← [Register](../roadmap.md#now)

**Outcome:** Si entra con Google e si vedono le proprie ricette; chi non è entrato non vede niente, e
il ricettario corrente smette di essere configurato e comincia a essere quello dell'utente
autenticato — nello stesso punto di prima.

**Requested by:** `sources/goal.md`, «Auth — decisione presa: Google OAuth»;
`sources/tech-choices.md`, Auth.js con provider Google; `sources/concepts.md`, `User` e `Membership`;
il seam consegnato da `S3`.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Le prime persone vere: chi ha costruito l'app e una seconda persona con un account Google. Dopo
questa riga entrano con il loro account e vedono le proprie ricette, e nessuno che non sia entrato
vede niente.

## Includes

- Auth.js con provider Google, sessioni su Postgres attraverso l'adapter Drizzle, e la tabella `User`.
- Il client OAuth su Google Cloud configurato con la callback URL dell'ambiente deployato.
- Il risolutore del ricettario corrente commutato dal ricettario configurato a quello risolto dalla
  appartenenza dell'utente entrato — nello stesso punto che la riga a mano ha istituito.
- La `Membership` scritta per chi crea un ricettario, e `creatorId` valorizzato.
- Ogni pagina e ogni rotta dietro la sessione, e la rimozione del percorso a ricettario configurato.
- Il primo accesso gestito secondo la decisione ancora aperta qui sotto: la riga non pubblica nessuna
  delle due strade finché non è presa.

## Verification

Una richiesta anonima a una qualunque pagina o rotta è rifiutata, non servita e poi nascosta: la
risposta non contiene mai una ricetta. Un utente entrato vede solo le ricette di un ricettario di cui
è membro; un secondo account entrato sullo stesso deploy non ne vede nessuna. Le ricette scritte
prima di questa riga sono ancora raggiungibili dal loro proprietario: la commutazione al seam non le
ha orfanate. L'accesso funziona sull'URL Fly reale con la callback vera, e la sessione sopravvive a
una sospensione della macchina. Nessun segreto raggiunge il bundle client. Si riporta quanti file
sono stati toccati per commutare il risolutore, che è la verifica dell'affermazione fatta dalla riga
che ha istituito il seam.

## Learning target

Sostituire uno scope configurato con uno autenticato in un solo punto nominato costa un posto solo e
non rompe niente di quanto è già stato consegnato.

## Excludes

- Nessun invito e nessuna appartenenza al ricettario di qualcun altro: è la riga della condivisione.
- Nessun ruolo e nessun permesso granulare: è un'esclusione dichiarata, non un rinvio.
- Nessuna passkey, nessuna password, nessun magic link, nessun invio di email.

## Open questions

- Cosa incontra un utente al primo accesso: un ricettario personale creato d'ufficio con il suo nome,
  oppure una schermata vuota che chiede di crearne uno? Le fonti descrivono il ricettario come unità
  di condivisione ma non dicono come nasce il primo. La scelta decide se questa riga consegna già un
  risultato usabile da sola o se resta in attesa della riga degli inviti, e finché è aperta la riga
  non ne pubblica nessuna delle due.
