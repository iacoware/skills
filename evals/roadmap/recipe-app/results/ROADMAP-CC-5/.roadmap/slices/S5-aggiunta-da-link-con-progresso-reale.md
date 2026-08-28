# S5 — Aggiunta da link con progresso reale

← [Register](../roadmap.md#now)

**Outcome:** Si incolla l'URL di una ricetta, si guardano i passi che il server sta davvero facendo,
e la ricetta è salvata senza aver dovuto rivedere niente.

**Requested by:** `goal.md` (*Visione — Da link*, *Aggiunta ricetta*) e `concepts.md`
(*Pipeline di estrazione*), con la strategia a cascata di `arch-choices.md`
(*Estrazione contenuto*).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi prova l'app su staging: aggiungere una ricetta trovata su un blog smette di essere copiatura a
mano e diventa un incollaggio, che è il caso che le fonti dichiarano più frequente.

## Includes

- Ingresso "aggiungi da link" in Home: si incolla l'URL e l'estrazione parte in modo sincrono.
- Fetch della pagina con l'`HttpClient` di Effect, con timeout, tetto alla dimensione del corpo e al
  numero di redirect, e URL trattato come ingresso ostile: solo schema `http(s)`, nessun indirizzo
  di rete privata. Ogni fallimento è un `Data.TaggedError` distinto — irraggiungibile, timeout,
  403 o paywall, corpo troppo grande.
- Pulizia del contenuto.
- Parse del JSON-LD `schema.org/Recipe` decodificato con `Schema` e mai castato, verso la stessa
  forma di `Recipe` che S3 persiste, riempiendo `prepTime` e `tags` quando la pagina li porta.
- Progresso riportato sugli stadi in cui il server è davvero entrato — scarico la pagina, leggo la
  ricetta, salvo — dove uno stadio si annuncia solo una volta iniziato e ogni fallimento porta il
  messaggio del proprio stadio, non un errore generico.
- `sourceUrl` salvato; salvataggio immediato, nessun passo di revisione; si atterra sulla ricetta
  salvata, da cui il form di correzione di S3 è a un clic.
- Quando il JSON-LD non c'è, il flusso si ferma sullo stadio di lettura con un messaggio che lo dice
  e rimanda al copia-incolla, che S6 fa funzionare.

## Verification

Tre URL veri di blog di cucina che espongono JSON-LD producono ricette che una persona rilegge come
corrette in titolo, ingredienti e preparazione. Un URL dietro paywall fallisce sullo stadio di
fetch con un messaggio che nomina il fetch, e non un errore generico. Un URL senza JSON-LD fallisce
sullo stadio di lettura nominando quello. Il progresso mostrato corrisponde agli stadi che i log del
server registrano come entrati, nell'ordine e nei tempi. L'intera aggiunta si chiude dentro il
budget di richiesta che la configurazione Fly deployata concede, misurato sull'URL più lento dei tre.
Un URL che punta a un indirizzo di rete privata viene rifiutato prima del fetch. Le ricette salvate
qui compaiono nella ricerca di S4.

## Learning target

Se una richiesta sincrona regge fetch, parse e salvataggio con un progresso onesto per stadio dentro
il budget della piattaforma, e se il solo JSON-LD copre abbastanza pagine reali da valere come il
percorso gratuito che le fonti assumono.

## Excludes

- Nessuna chiamata LLM e nessun copia-incolla: sono di S6, che è il ripiego dichiarato di questo
  percorso e la riga subito successiva.
- Nessuna foto e nessuno stadio "salvo foto": lo storage foto è di S7, che aggiunge quello stadio a
  questo flusso.
- Nessun passo di revisione prima del salvataggio: le fonti lo escludono, e sta in `OUT-OF-SCOPE`.
- Nessuna deduplica: lo stesso URL incollato due volte produce due ricette, ed è escluso per sempre.

## Open questions

- —
