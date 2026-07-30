# Recipe App — Scelte architetturali

Scelte di infrastruttura e servizi, tutte guidate dal vincolo **budget bassissimo**
(target ~$0/mese in free tier + centesimi di LLM). Per le scelte di stack/librerie vedi
`tech-choices.md`.

## Datastore — Postgres + pgvector

**Un solo datastore** per dato normalizzato *e* indice vettoriale.

- Provider: **Neon** o **Supabase** (free tier, pgvector incluso).
- Regge ampiamente la scala prevista (**≤10k ricette**, centinaia per ricettario): a questi
  numeri lo scan vettoriale è già in pochi ms; con indice **HNSW** resta istantaneo anche
  a 100k+.
- Non serve un **vector DB dedicato** (Pinecone/Qdrant/Weaviate): sarebbe infra e costo in
  più senza beneficio a questa scala. Tenere dati + vettori insieme permette query uniche
  (filtri esatti + similarità) in transazione singola.

## Object storage foto — Cloudflare R2

- Le foto **non** stanno nel DB: nel DB solo l'`url`.
- **Cloudflare R2**: free tier ~10GB, **zero egress** (a differenza di S3).
- All'add da link si scarica l'immagine (`og:image` / `schema.org/Recipe`) e la si
  ricarica sul proprio storage per evitare hotlinking che si rompe.

## Embeddings — API cloud multilingue

- **API cloud** (es. OpenAI `text-embedding-3-small`), **non** self-host.
- Costo ~$0.02 / 1M token → 10k ricette ≈ $0.10 **una tantum**; le query sono irrilevanti.
  Self-host risparmierebbe centesimi caricandoti di infra: pessimo rapporto costo/beneficio.
- Deve essere **multilingue** (vincolo per la ricerca cross-lingua: "pomodoro" trova una
  ricetta in inglese senza tradurre nulla).
- Usato **solo in fase di add** e all'edit, mai a runtime sulle query di ricerca.

## Estrazione contenuto — JSON-LD prima, LLM in fallback

Strategia a cascata per minimizzare le chiamate LLM a pagamento:

1. **JSON-LD `schema.org/Recipe`** presente nella pagina → parse diretto, **gratis**,
   zero allucinazioni. Hit-rate alto sui food blog.
2. **Fallback LLM** (modello cheap, Haiku-class, con output strutturato validato) solo
   quando il JSON-LD manca. Costo: frazioni di cent per ricetta, solo all'add.
3. **Copia-incolla / manuale**: saltano il JSON-LD, riusano lo stesso motore e schema.

## Hosting — Fly.io (container Docker)

- **Fly.io** con container Docker: runtime Node completo, **nessun limite architetturale**
  (no bundle size, TCP raw verso Postgres, moduli nativi, processi long-running, streaming).
- **Scale-to-zero** via `auto_stop`. Cold start alla prima richiesta dopo inattività:
  - `suspend` (snapshot RAM): risveglio **sub-secondo** — riparte calda, consigliato.
  - `stop` (spegnimento pieno): riavvio ~**1–4s** (boot macchina + avvio Next).
  - Impatto reale: solo il **primo utente** dopo un periodo di silenzio; poi istantaneo.
    Fastidio minore per un'app di famiglia, non un limite architetturale.
- **Costo**: Fly **non ha più un free tier vero** (a consumo dal 2024).
  - Con `suspend` + scale-to-zero e traffico quasi nullo: **pochi centesimi/mese** (~$0).
  - Sempre-calda (`min_machines_running=1`, nessun cold start): `shared-cpu-1x` 512MB,
    taglia realistica per Next.js → **~$3/mese**. È un flag in `fly.toml`, reversibile.
- Strategia consigliata: partire con **`suspend` + scale-to-zero**; passare a macchina
  calda solo se la latenza iniziale desse fastidio.
- Container **stateless**: foto su R2, dati su Neon → nessun volume, scale-to-zero pulito.
- **Scartato Vercel**: oltre l'Hobby i costi salgono rapidamente.
- **Scartato Cloudflare Workers + OpenNext**: pur più economico, il modello fat-worker
  introduce vincoli (bundle size ~10MB, runtime `workerd` con `nodejs_compat` da verificare,
  driver Postgres serverless/Hyperdrive) → costo di debugging e rischio problemi maggiori.
  Il container dà runtime identico in dev e prod.
- **Scartato AWS Fargate**: nessuno scale-to-zero nativo → costo h24.
- **IaC**: per l'MVP basta `fly.toml` + CLI Fly. SST (ha senso solo su AWS) e Terraform
  (multi-cloud) sarebbero over-engineering; si valuteranno se servirà IaC versionata.

## Riepilogo costi

| Voce | Servizio | Costo alla scala prevista |
|---|---|---|
| DB + vettori | Neon / Supabase free tier | $0 |
| Foto | Cloudflare R2 free tier | $0 |
| Embeddings | OpenAI `text-embedding-3-small` | ~$0.10 una tantum |
| Estrazione | LLM cheap, solo fallback | frazioni di cent/ricetta |
| Hosting | Fly.io | centesimi/mese (suspend+scale-to-zero) — ~$3/mese se sempre-calda |
| Auth | Google OAuth (vedi `tech-choices.md`) | $0 |

Totale realistico: **centesimi/mese** (Fly a consumo con suspend+scale-to-zero) + centesimi
di LLM in fase di add. Se si tiene la macchina Fly sempre-calda: **~$3/mese**.
