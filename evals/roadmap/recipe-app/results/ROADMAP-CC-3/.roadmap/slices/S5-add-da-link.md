# S5 — Aggiungi da link con estrazione JSON-LD e progresso reale

← [Register](../roadmap.md#now)

**Outcome:** Si incolla l'URL di una pagina di ricetta, si vedono i passi reali dell'estrazione
avanzare, e la ricetta risulta salvata nel ricettario senza nessun passaggio di conferma.

**Requested by:** `sources/goal.md` § Aggiunta ricetta, che chiede estrazione sincrona con
progresso sui passi reali e nessuna review obbligatoria; `sources/concepts.md` § Pipeline di
estrazione, ramo JSON-LD; `sources/arch-choices.md` § Estrazione contenuto, primo gradino della
cascata.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi sviluppa e chi collauda, sull'ambiente di staging non pubblico. Dopo questa riga aggiungere una
ricetta da un blog costa un incolla e un'attesa, invece di una trascrizione.

## Includes

- Campo per l'URL nella home e percorso di aggiunta che porta diritto alla ricetta salvata.
- Scaricamento della pagina con `HttpClient` di Effect: timeout, limite di dimensione della
  risposta, nessun redirect verso indirizzi di rete interna.
- Parse del `schema.org/Recipe` in JSON-LD e decodifica con `Schema`, mai un cast.
- Derivazione best-effort di tempo di preparazione e tag dal JSON-LD, e `sourceUrl` salvato.
- Salvataggio immediato: nessuna schermata di conferma, la correzione è il form che esiste già.
- Progresso in streaming sui passi effettivi — `Scarico pagina`, `Leggo ricetta`, `Salvo` — dove
  ogni passo cambia stato solo quando è davvero finito.
- Messaggi d'errore per passo: pagina irraggiungibile, risposta bloccata da paywall, nessuna
  ricetta strutturata nella pagina; quest'ultimo invita a incollare il testo, che è il percorso
  della riga successiva.

## Verification

Da un blog con JSON-LD la ricetta si salva con titolo, ingredienti e preparazione popolati e senza
che l'utente confermi nulla. Confrontando due URL con tempi di risposta diversi, i passi avanzano
in momenti diversi: la barra segue il lavoro e non un timer. Su una pagina senza dati strutturati
si legge «nessuna ricetta strutturata trovata» e non un errore generico; su una che va in timeout
si legge quale passo è fallito. L'embedding della ricetta importata viene generato e la ricetta è
cercabile subito dopo. Un URL che punta a un indirizzo di rete interna viene rifiutato. Su un
campione dichiarato di siti veri è registrata la quota di pagine il cui JSON-LD è utilizzabile, e i
tempi totali osservati.

## Learning target

Che l'estrazione sincrona con progresso reale sia sostenibile — che il tempo totale su siti veri
resti dentro l'attesa che una barra può reggere e che lo streaming del progresso arrivi davvero al
client attraverso la piattaforma — e quanto spesso il solo JSON-LD basti, che è ciò che decide
quanto peserà l'LLM.

## Excludes

- Ogni chiamata all'LLM, anche quando il JSON-LD manca: l'estrattore LLM è alimentato anche dal
  testo incollato, e appartiene per intero alla riga successiva, che lo possiede da sola.
- La foto presa dalla pagina, che apre l'object storage: è la riga delle foto a doverlo validare, e
  qui il passo non esiste.
- Ogni review prima del salvataggio, esclusa dalle sorgenti.

## Open questions

- —
