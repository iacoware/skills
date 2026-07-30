# Recipe App — Obiettivi

## Visione

App per **memorizzare e ricercare ricette**, condivisa tra membri di una famiglia e
amici. Due modi per aggiungere una ricetta:

1. **Da link** (caso più frequente): incolli l'URL di un sito/blog, il sistema estrae
   automaticamente il contenuto.
2. **A mano** (meno frequente): la conosci e la inserisci tu.
3. **Copia-incolla** (fallback): incolli il testo di una pagina che il sistema ripulisce
   e analizza — usato anche quando il link non è leggibile (paywall, siti JS-heavy).

## Posizionamento (alternative esistenti)

Il mercato dell'import-da-URL + condivisione in famiglia è **maturo e affollato**. Le
alternative gratuite più vicine:

| App | Tipo | Import URL | Condivisione | Note |
|---|---|---|---|---|
| **[Mealie](https://mealie.io/)** ⭐ | self-hosted OSS | sì (scraper) | gruppi/household | benchmark: copre ~80% del nostro MVP |
| **[Tandoor](https://awesome-selfhosted.net/tags/recipe-management.html)** | self-hosted OSS | sì + file (Paprika…) | sì | ricerca strutturata potente, più complesso |
| **[RecipeSage](https://recipesage.com/)** | hosted + OSS | sì (web/foto/PDF/testo) | sì | copre lo scenario copia-incolla/OCR |
| **[KitchenOwl](https://awesome-selfhosted.net/tags/recipe-management.html)** | self-hosted | limitato | household | focus collaborazione/liste spesa |
| **[Recipe Keeper](https://recipekeeperonline.com/) / [My Recipe Box](https://www.myrecipebox.app/en)** | hosted free | sì (siti supportati) | email/social | UX consumer curata, non self-host |

### Differenziatore

Tutte usano **ricerca keyword + filtri per tag**. Nessuna delle mainstream gratuite offre:

- **Ricerca semantica cross-lingua** via embeddings ("cena leggera"; "pomodoro" trova
  anche ricette in inglese). I progetti AI/RAG esistenti sono demo o generatori, non
  ricettari condivisi maturi.
- **Estrazione LLM come fallback** quando manca lo `schema.org/Recipe` (Mealie fallisce
  sui siti senza structured data → il nostro copia-incolla + LLM lo copre).

> ⚠️ Nota strategica: la ricerca semantica cross-lingua è il vero elemento distintivo.
> Senza di essa staremmo in gran parte **riscrivendo Mealie**. Va tenuto come nord.

## Principi guida

- **Budget bassissimo**: ogni scelta tecnica privilegia il costo minimo. Target
  realistico ~$0/mese (free tier) + centesimi di LLM.
- **Semplicità sopra tutto**: un solo datastore, un solo concetto di condivisione,
  nessun permesso granulare.
- **Attrito minimo in aggiunta**: aggiungere una ricetta deve costare all'utente il minimo
  indispensabile. La ricerca è semantica (embeddings su Postgres+pgvector) e chi legge
  interpreta il testo da sé, quindi non serve normalizzazione fine: **titolo, ingredienti,
  preparazione, foto** bastano. Campi accessori (tag, tempo) sono derivati
  automaticamente, best-effort, mai richiesti. Nessun passo obbligatorio prima del
  salvataggio: si salva subito, si corregge dopo.
  - Trade-off accettato: senza ingredienti strutturati (quantità/unità) restano preclusi
    lista della spesa e scaling porzioni. Entrambi già fuori scope.
- **Slice verticali**: ogni incremento attraversa tutti i layer e produce comportamento
  verificabile.

## Cosa fa (MVP)

### Home

- **Elenco** delle ricette del ricettario corrente.
- **Aggiungi** ricetta: da link, a mano, o copia-incolla.
- **Ricerca** semantica.

### Aggiunta ricetta

- Estrazione **sincrona** con **progress bar sui passi reali**
  (`Scarico pagina → Leggo ricetta → Trovo ingredienti → Salvo foto`), non fake:
  se uno step fallisce (es. paywall) il messaggio è preciso.
- **Nessuna review obbligatoria**: l'estratto si salva subito. La correzione è sempre
  disponibile dopo (edit), non è un passo del flusso di add.
- Stesso form per edit e inserimento manuale (campi vuoti): titolo, ingredienti,
  preparazione come **testo libero**, nessun parsing di quantità e unità.
- **Foto multiple** per ricetta; la **cover** è la prima foto per default, cambiabile.

### Ricerca (MVP: solo semantica)

- **Ricerca semantica** con embeddings **multilingue**: linki una ricetta in inglese
  ma cerchi "pomodoro" e la trova (cross-lingua senza tradurre nulla).
- Scope: **solo il ricettario corrente**.
- Testo indicizzato: `nome + ingredienti + preparazione`, più `tag + tempo` quando derivati
  (best-effort: i tag portano segnale che il testo non contiene, es. "vegano").
- Filtri strutturati (tag, tempo) **rimandati** a dopo l'MVP: i campi si popolano da subito
  in automatico, così i filtri diventano abilitabili senza migrazione né lavoro retroattivo.

### Condivisione

- La collaborazione si **aggrega attorno al ricettario** (cookbook-centrico), non attorno
  a una "famiglia".
- Ogni ricettario ha un **creator** che invita gli altri tramite link/codice condivisibile.
- Dentro un ricettario **tutti i membri sono pari**: possono leggere ed editare tutto.
- Un utente può appartenere a **più ricettari**.

## Scelte tecniche (guidate dal costo)

Le decisioni tecniche sono documentate a parte:

- **`arch-choices.md`** — infrastruttura e servizi: Postgres+pgvector, object storage,
  embeddings, strategia di estrazione, hosting, riepilogo costi.
- **`tech-choices.md`** — stack: Next.js, Effect, Auth.js + Google OAuth, React Query, ORM,
  convenzioni UI.

In sintesi: tutto entro **free tier** (Fly.io scale-to-zero, Neon/Supabase, Cloudflare R2),
un solo datastore Postgres, LLM/embedding solo in fase di add → target **~$0/mese**.

## Vincoli e scala

- **≤ 10.000 ricette** totali previste; **centinaia per ricettario**. Non serve un vector
  DB dedicato: Postgres+pgvector con indice HNSW è più che sufficiente.
- LLM/embedding usati **solo in fase di add** (una tantum per ricetta), mai a runtime
  sulle query di ricerca.

## Auth — decisione presa: Google OAuth

**Google OAuth** via Auth.js. Elimina in un colpo invio email, password/hashing e flusso
reset: Google gestisce identità e recupero account. Costo $0.

- Scartato **email+password**: il reset password richiede comunque invio email, in
  conflitto con "niente provider email in MVP".
- Scartato **magic-link**: costerebbe uguale (richiede provider email) e resta più
  macchinoso per l'utente (uscire dall'app, aprire la casella).
- **Passkeys** fuori dall'MVP: easy per l'utente ricorrente ma il recupero account
  (dispositivo perso) è complesso e supporto Auth.js ancora acerbo.
- Trade-off accettati: dipendenza da Google; gli utenti devono avere un account Google
  (per famiglia/amici quasi sempre vero).

## Fuori scope MVP (sviluppi futuri)

- Ricettari **pubblici tematici** (vegano, giapponese, ecc.): abilitabili in futuro come
  Cookbook con `visibility=public`, senza migrazione.
- Filtri di ricerca strutturati (tag, tempo) e ricerca ibrida (semantica + full-text).
- Concetto di "gruppo/team" sopra i ricettari, se ri-invitare per ogni ricettario
  diventasse fastidioso.
- Ricerca cross-ricettario.
- Ruoli/permessi granulari (per ora basta `creatorId`).
