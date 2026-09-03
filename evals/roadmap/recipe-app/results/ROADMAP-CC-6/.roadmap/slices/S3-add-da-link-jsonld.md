# S3 — Aggiungi da link con JSON-LD, elenco e dettaglio

← [Register](../roadmap.md#now)

**Outcome:** Si incolla l'URL di una ricetta con structured data, si vede la barra di avanzamento
passare per i passi reali, e a fine corsa la ricetta è salvata, compare in elenco e si apre in
dettaglio con nome, ingredienti e preparazione.
**Requested by:** `goal.md` § Cosa fa (MVP) → Home e Aggiunta ricetta; `concepts.md` § Pipeline di
estrazione (ramo JSON-LD) e § Recipe.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi sviluppa e chi prova il prodotto, sull'ambiente non pubblico di S1. Dopo questa riga può
trasformare un link in una ricetta consultabile senza toccare il database a mano, ed è la prima volta
che qualcuno vede il prodotto invece dell'infrastruttura.

## Includes

- Tabella `Recipe` con `cookbookId`, `name`, `ingredients` e `steps` come testo libero, `prepTime` e
  `tags` opzionali, `sourceUrl`, `embedding`; migrazione applicata dal runner di S1.
- Il confine di scope: un unico resolver del ricettario corrente, che qui restituisce un cookbook
  seminato da configurazione, e da cui passa ogni lettura e scrittura di `Recipe`.
- Fetch della pagina con l'`HttpClient` di Effect, con limiti su schema, dimensione e timeout, e
  senza seguire redirect verso indirizzi interni.
- Estrazione da JSON-LD `schema.org/Recipe`: parse, validazione con `Schema`, mappatura sui campi
  della ricetta, `prepTime` e `tags` popolati best-effort quando ci sono.
- Calcolo e scrittura dell'`embedding` col modello scelto in S2, come passo della stessa pipeline,
  nella stessa scrittura della ricetta.
- Form di aggiunta con un solo campo URL e barra di avanzamento sui passi che la pipeline esegue
  davvero, ciascuno con il proprio messaggio di fallimento.
- Elenco delle ricette del ricettario corrente e pagina di dettaglio.
- Errori tipizzati per passo con `Data.TaggedError`, tradotti in messaggio all'utente al boundary.

## Verification

- Incollando l'URL di un food blog con JSON-LD, la ricetta compare in elenco e il dettaglio mostra
  nome, ingredienti e preparazione presi dalla pagina.
- La barra di avanzamento cambia quando cambia il passo davvero in corso: fermando la rete a metà
  scaricamento l'utente resta sul passo "scarico la pagina" e vede quel fallimento, non un errore
  generico.
- Su una pagina senza JSON-LD l'aggiunta fallisce con un messaggio che dice che in quella pagina non
  è stata trovata una ricetta — è il fallimento che S4 rimedia.
- Su una pagina dietro paywall il messaggio distingue "non ho potuto leggere la pagina" da "la pagina
  non contiene una ricetta".
- Il tempo che intercorre dall'invio dell'URL al salvataggio è misurato su una decina di siti reali e
  sta dentro il tempo di una richiesta HTTP sull'ambiente di S1, macchina fredda inclusa.
- Una ricetta salvata ha un `embedding` non nullo, e una riga scritta con un `cookbookId` diverso da
  quello configurato non compare in elenco.

## Learning target

Se una pipeline di add tutta sincrona — scarico, leggo, embeddo, salvo — sta dentro una richiesta
HTTP su una macchina che si sospende, e se i suoi passi reali sono abbastanza distinti da poter dire
all'utente cosa è andato storto.

## Excludes

- L'estrazione LLM e il testo incollato: sono di S4, che è il rimedio del fallimento verificato qui.
- Le foto, compreso il passo "salvo foto" della barra di avanzamento e il download di `og:image`: è
  tutto di S9, che possiede l'adapter R2 da solo.
- La ricerca: è di S5. Qui l'`embedding` si scrive e non si legge.
- Modifica e inserimento a mano: sono di S8.
- Autenticazione, utenti e ricettari veri: sono di S6, che sostituisce il cookbook configurato al
  resolver introdotto qui.

## Open questions

- Nessuna.
