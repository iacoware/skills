# S6 — Ricerca semantica nel ricettario corrente

← [Register](../roadmap.md#now)

**Outcome:** Si cerca a senso dalla home — "cena leggera", "pomodoro" — e si trovano le ricette del
ricettario corrente anche quando sono scritte in un'altra lingua, senza aver mai messo un tag e senza
che la ricerca chiami un'API a pagamento.

**Requested by:** `goal.md` (§ Ricerca (MVP: solo semantica); § Differenziatore), `concepts.md`
(§ Ricerca (MVP)) e la scelta di modello prodotta da S2.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi sviluppa e chi prova l'app sull'ambiente non pubblico. Dopo questa riga il ricettario smette di
essere un elenco da scorrere: è la prima volta che il prodotto fa qualcosa che le alternative
gratuite non fanno.

## Includes

- Adapter di embedding sul modello scelto da S2, con timeout e tentativi espliciti.
- Generazione dell'embedding in aggiunta e in modifica per tutti e tre i percorsi che producono una
  ricetta — a mano (S3), da link (S4), da LLM o testo incollato (S5) — da un unico punto: questa riga
  possiede la pipeline, e i percorsi che la alimentano non la riaprono.
- Testo indicizzato come dichiarato dalle fonti: `nome + ingredienti + preparazione`, più `tag` e
  `prepTime` quando esistono.
- Colonna vettoriale su `Recipe` con indice HNSW, e riempimento a ritroso delle ricette salvate prima
  di questa riga.
- Campo di ricerca nella home e risultati ordinati per similarità, confinati al ricettario corrente
  dal risolutore di scope di S3, con la soglia decisa a partire dai numeri di S2.
- Un embedding che non si genera non impedisce di salvare: la ricetta resta valida, segnata come da
  reindicizzare, e ritentabile.

## Verification

Con un ricettario che contiene ricette italiane e inglesi, la query "pomodoro" restituisce fra i
primi risultati una ricetta scritta in inglese che parla di pomodoro, e la query "light dinner"
restituisce una ricetta italiana coerente: la stessa cosa misurata in S2 sul seed, qui sul corpus
prodotto dai percorsi di aggiunta reali. Correggendo il testo di una ricetta e ricaricando, la
ricerca riflette il testo nuovo e non quello vecchio. Una ricetta di un altro ricettario configurato
non compare mai fra i risultati. La p95 della query di ricerca è misurata e scritta, e nessuna
chiamata all'API di embedding parte durante una ricerca: il contatore del provider resta fermo
mentre si cerca e si muove solo mentre si aggiunge. Spegnendo l'API di embedding, un'aggiunta va
comunque a buon fine e la ricetta risulta in attesa di indice; riaccendendola, la reindicizzazione la
recupera.

## Learning target

Il differenziatore regge sul corpus reale e non solo sul seed controllato di S2: su ricette entrate
dai percorsi veri, con testo sporco e lunghezze irregolari, la ricerca a senso cross-lingua trova
quello che una persona si aspetta di trovare — e lo fa a costo zero per query.

## Excludes

- Filtri strutturati su tag e tempo e ricerca ibrida con il full-text: candidati dichiarati fuori
  MVP. I campi si popolano già da S4 e S5, quindi diventeranno abilitabili senza migrazione.
- La ricerca su più ricettari: candidato dichiarato fuori MVP; lo scope resta il ricettario corrente.
- La sostituzione dello scope configurato con quello autenticato: è di S7, in quel solo punto.

## Open questions

- **Cosa mostra la ricerca quando niente è vicino.** Una ricerca vettoriale restituisce sempre i
  vicini più prossimi, quindi senza una soglia non dice mai "nessun risultato". Le fonti non ne
  parlano. La decisione — se esista una soglia, quale, e cosa si vede sotto quella soglia — si prende
  qui, sui numeri che S2 produce, ed è una scelta di prodotto: una soglia troppo alta nasconde
  ricette che ci sono.
