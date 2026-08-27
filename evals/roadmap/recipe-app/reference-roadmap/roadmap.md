# Roadmap — Recipe App

**Goal:** un ricettario condiviso fra famiglia e amici in cui una ricetta si trova descrivendola, anche
quando è scritta in un'altra lingua.

**Sources:** `sources/goal.md`, `sources/concepts.md`, `sources/arch-choices.md`,
`sources/tech-choices.md`.

**Current state:** niente di consegnato. `.roadmap/archive/` è vuoto, nessuna riga è stata chiusa e
questa è la mappa come è stata disegnata la prima volta contro il goal.

## Themes

| Theme | Promise | First validator |
|---|---|---|
| `ricerca-semantica` | Descrivi quello che vuoi mangiare e la ricetta esce, in qualunque lingua sia scritta | `S4` |
| `consultazione` | Le ricette del ricettario si sfogliano e si leggono mentre si cucina | `S5` |
| `autenticazione` | Si entra senza password e senza aspettare un'email | `S6` |
| `inserimento-manuale` | Una ricetta che già conosci la scrivi tu, e la correggi quando vuoi | `S7` |
| `import-automatico` | Incolli un link e la ricetta è dentro, senza riscriverla | `S8` |
| `foto` | Una ricetta si riconosce dalla foto prima che dal nome | `S11` |
| `condivisione` | Il ricettario è di tutti quelli che il creatore invita | `S12` |

## NOW

| Id | Title | Theme | Kind | Size | Readiness | Executor | Depends on |
|---|---|---|---|---|---|---|---|
| `S0` | [Repository, CI e segreti](slices/S0-repository-ci-segreti.md) | — | `enabler` | `small` | `ready` | `mixed` | — |
| `S1` | [Walking skeleton in produzione](slices/S1-walking-skeleton.md) | — | `release` | `medium` | `needs-decision` | `mixed` | — |
| `S2` | [Spike: quale embedding regge la ricerca cross-lingua](slices/S2-spike-embedding-cross-lingua.md) | `ricerca-semantica` | `spike` | `small` | `needs-info` | `agent` | — |
| `S3` | [Indicizzazione semantica delle ricette](slices/S3-indicizzazione-semantica.md) | `ricerca-semantica` | `enabler` | `medium` | `ready` | `agent` | `S2` |
| `S4` | [Ricerca semantica cross-lingua](slices/S4-ricerca-semantica.md) | `ricerca-semantica` | `product` | `medium` | `ready` | `agent` | `S3` |
| `S5` | [Elenco e lettura di una ricetta](slices/S5-elenco-e-lettura.md) | `consultazione` | `product` | `small` | `ready` | `agent` | `S3` |
| `S6` | [Accesso con Google](slices/S6-accesso-google.md) | `autenticazione` | `product` | `medium` | `ready` | `mixed` | — |
| `S7` | [Scrittura e correzione a mano](slices/S7-scrittura-a-mano.md) | `inserimento-manuale` | `product` | `medium` | `ready` | `agent` | `S3` |
| `S8` | [Import da URL con JSON-LD](slices/S8-import-da-url.md) | `import-automatico` | `product` | `large` | `ready` | `agent` | `S3` |
| `S9` | [Fallback LLM per le pagine senza dati strutturati](slices/S9-fallback-llm.md) | `import-automatico` | `product` | `medium` | `ready` | `agent` | `S3` |
| `S10` | [Copia-incolla del testo di una pagina](slices/S10-copia-incolla.md) | `import-automatico` | `product` | `small` | `ready` | `agent` | `S9` |
| `S11` | [Foto della ricetta](slices/S11-foto.md) | `foto` | `product` | `medium` | `ready` | `agent` | `S8` |
| `S12` | [Ricettario condiviso su invito](slices/S12-ricettario-condiviso.md) | `condivisione` | `product` | `large` | `ready` | `agent` | `S6` |
| `S13` | [Tag e tempo derivati per la ricerca](slices/S13-tag-e-tempo-derivati.md) | `ricerca-semantica` | `enabler` | `small` | `ready` | `agent` | `S9` |
| `S14` | [Messa in mano ai primi utenti](slices/S14-primi-utenti.md) | — | `release` | `small` | `ready` | `mixed` | `S12` |

## LATER

- Ricettari pubblici tematici (`visibility=public`), abilitabili senza migrazione.
- Ricerca su tutti i ricettari di cui si è membri, non solo su quello corrente.
- Filtri strutturati per tag e tempo, e ricerca ibrida semantica più full-text.
- Un concetto di gruppo sopra i ricettari, se ri-invitare le stesse persone in ognuno diventasse
  fastidioso.
- Passkey come secondo modo di entrare.
- Macchina Fly sempre calda, se il cold start del primo utente desse davvero fastidio.

## OUT-OF-SCOPE

- **Ruoli e permessi granulari.** Il creatore è identificato da `creatorId` e tutti i membri sono
  pari. È la licenza per non avere un modello di ruolo e per non scrivere controlli oltre
  l'appartenenza.
- **Ingredienti strutturati.** Ingredienti e preparazione restano testo libero, senza quantità né
  unità. È la licenza per non avere un modello di ingrediente, e il prezzo è che lista della spesa e
  scaling delle porzioni restano preclusi.
- **Deduplicazione.** Due membri possono salvare la stessa ricetta nello stesso ricettario e il
  sistema non se ne accorge. È la licenza per non avere né chiavi naturali né confronto fra ricette.
- **Password, recupero account ed email.** L'identità è delegata a Google e l'app non manda email. È
  la licenza per non avere alcuna infrastruttura di posta.

## Assumptions

- `ricerca-semantica`, `S4` — «mai embedding a runtime» nei sorgenti è un vincolo di costo, non di
  architettura: la query si embedda a ogni ricerca. I sorgenti si contraddicono su questo punto e la
  mappa sceglie la lettura economica.
- `inserimento-manuale`, `S7` — `concepts.md` fa saltare l'estrazione all'inserimento manuale,
  `arch-choices.md` gli fa riusare «lo stesso motore e schema». La mappa legge il diagramma: il form
  manuale non attraversa l'estrattore, e «stesso schema» vale per la forma della `Recipe` che si
  salva, non per un motore che quel percorso non tocca.
- `S1` — Neon e Supabase sono intercambiabili ai fini della mappa: quale dei due si scelga non
  aggiunge né toglie righe.
- `import-automatico`, `S9` — il JSON-LD copre i siti che i primi utenti incollano davvero.
- `S3`, `S4` — un corpus di seed di poche decine di ricette reali, italiane e inglesi, basta a
  giudicare la ricerca prima che esistano utenti che ne aggiungono.
- `condivisione`, `S12` — fino a `S12` esiste un solo ricettario implicito per utente, e le righe
  precedenti possono ignorare il concetto senza dover essere riscritte.

## Open questions

- `ricerca-semantica`, `import-automatico` — se `S2` dice che nessun modello cloud multilingue trova
  una ricetta inglese da una query italiana, il differenziatore va cercato altrove e la forma della
  mappa cambia da `S3` in poi. La ricerca ibrida, oggi in `LATER`, sarebbe la prima candidata a
  rientrare.
- `import-automatico` — i sorgenti non dicono cosa succede quando l'estrazione fallisce del tutto: si
  salva una ricetta parziale o non si salva niente. La risposta decide se serve una riga per il
  recupero dopo un import fallito o se basta la correzione a mano di `S7`.
- `condivisione` — i sorgenti non dicono se una ricetta possa essere spostata o copiata fra ricettari
  di cui si è membri. Se sì è una riga in più, se no è un'esclusione.

## Cross-functional concerns

- **Authorization.** L'appartenenza al ricettario è l'unico diritto: chi è membro legge e modifica
  tutto, chi non lo è non esiste per quel ricettario. Un id fuori dallo scope del chiamante risponde
  404 e mai 403 — l'esistenza di una ricetta altrui non si rivela.
- **Validation and errors.** Quello che arriva da fuori si decodifica con Schema e non si casta mai:
  l'output dell'estrazione LLM, il JSON-LD di una pagina, le risposte delle API. Gli errori attesi
  sono valori tipizzati e diventano un messaggio che dice quale passo è fallito.
- **Operability.** La macchina si spegne: nessuno stato locale, nessun volume, niente processi in
  background che debbano sopravvivere alla richiesta. Un fallimento in fase di aggiunta si vede
  nell'interfaccia, non solo nei log.
- **Accessibility and security.** I campi obbligatori non si marcano, si marcano gli opzionali; i
  segreti stanno fuori dal repository; le foto si servono dal proprio storage e mai in hotlink dal
  sito d'origine.
- **Data integrity and recovery.** La ricetta è il dato canonico, l'embedding è un indice derivato e
  si rigenera a ogni salvataggio: una perdita dell'indice è un ricalcolo, non una perdita di dati. Le
  foto stanno fuori dal database e il database va salvato.
