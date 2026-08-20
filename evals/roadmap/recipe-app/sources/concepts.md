# Recipe App — Concetti e modellazione

## Modello di condivisione: cookbook-centrico

La collaborazione si aggrega **attorno al ricettario**, non attorno a una famiglia.
È il pattern di collaborazione classico (repo GitHub, doc Notion): la membership è legata
alla risorsa condivisa.

- Un ricettario ha un **creator** che invita gli altri tramite link/codice.
- La membership è **N:N**: un utente può stare in più ricettari, un ricettario ha più membri.
- Dentro un ricettario tutti i membri sono **pari** (leggono ed editano tutto).
- **Svantaggio accettato**: se un gruppo crea più ricettari deve ri-invitare i membri in
  ognuno. Minore; risolvibile in futuro con un concetto di "gruppo" sopra i cookbook,
  in modo additivo.

## Entità principali

### User

Identità dell'utente. Auth gestita da Auth.js con **Google OAuth** (nessuna password,
nessun invio email, recupero account delegato a Google).

```
User {
  id
  email
}
```

### Cookbook

Il ricettario: unità di condivisione e di scope della ricerca.

```
Cookbook {
  id
  creatorId        -> User        // chi l'ha creato; unico "ruolo" nell'MVP
  name
  visibility        // private (MVP) | public (futuro, ricettari tematici)
}
```

### Membership (N:N User ↔ Cookbook)

Appartenenza di un utente a un ricettario. Essere membro = poter leggere ed editare.

```
Membership {
  cookbookId  -> Cookbook
  userId      -> User
}
```

> Nessun campo `role` nell'MVP: il creator è identificato da `Cookbook.creatorId`,
> tutti gli altri membri sono pari.

### Invitation

Invito condivisibile a un ricettario (link/codice). Chi lo apre da loggato ottiene una
`Membership`.

```
Invitation {
  cookbookId  -> Cookbook
  token
  expiresAt?
}
```

### Recipe

La ricetta, **source of truth**. Appartiene a un Cookbook. Normalizzazione deliberatamente
minima (vedi "Attrito minimo in aggiunta" in `goal.md`): la ricerca è semantica e chi legge
interpreta il testo, quindi non c'è modello di ingrediente né di step.

```
Recipe {
  id
  cookbookId   -> Cookbook
  name
  ingredients   // testo libero (righe), non parsato in quantità/unità
  steps         // testo libero (preparazione)
  prepTime?     // derivato best-effort, mai richiesto all'utente
  tags          // derivati best-effort, mai richiesti all'utente
  sourceUrl?    // presente se aggiunta da link
  embedding     // vector (pgvector), indice semantico derivato
}
```

`prepTime` e `tags` esistono solo per alimentare embedding e futuri filtri: si popolano da
JSON-LD o LLM, sono opzionali e la loro assenza non blocca nulla.

Il campo `embedding` è un **indice derivato**, non dato canonico: rigenerato a ogni edit
a partire da `nome + ingredients + steps` più `tags + prepTime` se presenti. Modello
embedding **multilingue** per ricerca cross-lingua.

### Photo (N Photo ↔ 1 Recipe)

Foto della ricetta su object storage; nel DB solo l'URL.

```
Photo {
  id
  recipeId  -> Recipe
  url
  isCover   // una sola cover per ricetta: la prima foto per default, cambiabile
}
```

## Relazioni

```
User ──N:N (Membership)── Cookbook ──1:N── Recipe ──1:N── Photo
                             │
                             └── creatorId ─> User
                             └── 1:N ─> Invitation
```

## Pipeline di estrazione (fase di add)

Due ingressi, **un solo motore di estrazione**. Sincrona, con progress sui passi reali.

```
[Input URL]         → fetch → HTML ─┐
[Input testo incollato] ────────────┤
[Input manuale] → (form vuoto) ──────┘   (salta l'estrazione)
                                     ↓
                            pulizia contenuto
                                     ↓
                JSON-LD schema.org/Recipe presente?   (solo path URL)
                  ├─ sì → parse diretto (nessun LLM, gratis)
                  └─ no → LLM structured output (schema Recipe)
                                     ↓
                            Recipe  ──> salva
                                     ↓
                embedding multilingue (pgvector)  +  foto su object storage
                                     ↓
                        (opzionale, in qualsiasi momento) edit
```

- Il **copia-incolla** salta il JSON-LD e va sempre su LLM; riusa lo stesso schema di
  output. È anche il **fallback** per siti JS-heavy/paywall.
- L'**inserimento manuale** usa lo stesso form dell'edit con campi vuoti.
- **Nessun passo di review nel flusso di add**: si salva subito, la correzione avviene
  dopo tramite edit. Un'estrazione imperfetta è un costo accettabile; bloccare l'utente
  su un form a ogni aggiunta non lo è.

## Ricerca (MVP)

Una query su Postgres, **solo semantica**:

```
similarity( Recipe.embedding, embedding(query) )   scoped a cookbookId corrente
```

Cross-lingua garantito dall'embedder multilingue. Filtri strutturati (tag, tempo) e
ricerca ibrida sono fuori scope MVP.

## Note sulla persistenza

- **Duplicati consentiti**: due membri possono linkare la stessa ricetta nello stesso
  ricettario senza dedup.
- **Un solo datastore**: Postgres (dati normalizzati + pgvector). Foto su storage esterno,
  referenziate per URL.
```

