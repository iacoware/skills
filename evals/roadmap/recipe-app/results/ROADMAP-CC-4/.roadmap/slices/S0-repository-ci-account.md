# S0 — Repository, CI e account

← [Register](../roadmap.md#now)

**Outcome:** Il repository esiste con una CI che gira build, lint, typecheck e test, e tutti
gli account e i segreti che il resto della mappa spenderà sono aperti e raggiungibili.

**Requested by:** `tech-choices.md` § Linguaggio e framework, `arch-choices.md` § Riepilogo
costi, e la regola della mappa che separa il repository dal primo deploy.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi costruisce l'app: da qui in poi ogni riga può essere aperta, verificata da CI e
deployata senza fermarsi ad aprire un account.

## Includes

- Repository con Next.js App Router in TypeScript, Prettier e Vitest configurati secondo le
  convenzioni di progetto.
- CI su ogni push e ogni pull request: build, lint, typecheck, test.
- Account e credenziali: progetto Postgres su Neon con estensione `vector` disponibile;
  bucket Cloudflare R2 con chiavi; organizzazione e app su Fly.io; client OAuth su Google
  Cloud; chiave API per il modello di estrazione e per l'embedding.
- Segreti dichiarati in CI e su Fly, nessuno nel repository; un elenco versionato dei nomi
  dei segreti e di dove vivono.

## Verification

Una pull request fa girare la pipeline e diventa rossa se lint, typecheck o test falliscono.
Ogni servizio previsto risulta aperto sul piano assunto dal riepilogo costi, con i suoi
limiti annotati (piano Neon e disponibilità di `vector`, quota R2 e assenza di egress,
modalità a consumo di Fly): l'elenco è controllabile riga per riga contro quel riepilogo.
Nessun deploy parte da questa riga.

## Learning target

Che i servizi su cui il piano dei costi si appoggia si aprano davvero alle condizioni
assunte, senza approvazioni in attesa, carte a sorpresa o estensioni Postgres indisponibili.

## Excludes

- Provisioning di runtime, Dockerfile e deploy: sono di `S1`.
- Qualunque migrazione o tabella: la prima è di `S1`, quelle di dominio di `S3`.
- Configurazione del client OAuth dentro l'app: l'account si apre qui, l'integrazione è di
  `S9`.

## Open questions

- —
