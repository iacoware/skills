# S4 — Aggiunta da link con JSON-LD e avanzamento reale

← [Register](../roadmap.md#now)

**Outcome:** Si incolla l'URL di una ricetta che espone `schema.org/Recipe` e la ricetta è salvata
senza compilare nulla, con un avanzamento che nomina i passi realmente eseguiti.

**Requested by:** `sources/goal.md` (Aggiunta ricetta — estrazione sincrona con progress bar sui
passi reali), `sources/arch-choices.md` (Estrazione contenuto — JSON-LD prima),
`sources/concepts.md` (Pipeline di estrazione).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi prova l'app sull'ambiente non pubblico: incolla il link di un food blog e si ritrova la ricetta
nel ricettario, senza toccare un campo.

## Includes

- Fetch della pagina con `HttpClient` di Effect, con timeout e retry per decorazione.
- Pulizia del contenuto, riusabile dalle righe che seguono.
- Parse del JSON-LD `schema.org/Recipe` validato con `Schema`, mai castato.
- Salvataggio di `sourceUrl`, e di `tags` e `prepTime` derivati best-effort quando il JSON-LD li
  porta: la loro assenza non blocca niente e non viene mai chiesta all'utente.
- Avanzamento sincrono `Scarico pagina → Leggo ricetta → Salvo`, con un messaggio preciso sul passo
  che fallisce.

## Verification

Su un elenco dichiarato di food blog che espongono JSON-LD si dichiara su quanti la ricetta si salva
senza alcun intervento, e la ricetta salvata si apre nel dettaglio di `S3`. Su una pagina a paywall
l'utente legge quale passo è fallito e perché — non un errore generico — e la ricetta non viene
salvata a metà. Una ricetta senza `tags` né `prepTime` si salva comunque. Lo stesso URL aggiunto due
volte produce due ricette, come le sorgenti chiedono.

## Learning target

Quanto lontano arriva il JSON-LD da solo, cioè quanto spesso il fallback a pagamento non serve.

## Excludes

- Pagine senza structured data: sono di `S5`, che è il recupero automatico dichiarato di questo path.
- Testo incollato: è di `S6`.
- Il passo "Salvo foto" e la copertina automatica: sono di `S10`, che possiede lo storage da solo.
  L'avanzamento qui mostra soltanto i passi che questa riga esegue davvero.
- Deduplica: esclusa dalla mappa.

## Open questions

- —
