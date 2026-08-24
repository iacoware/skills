# agent-skills

Agent skills installabili con la [Skills CLI](https://github.com/vercel-labs/skills), compatibili con Claude Code, Codex e gli altri agent supportati.

## Skills

| Skill | Descrizione |
| --- | --- |
| [`roadmap`](skills/roadmap) | Tiene viva la roadmap di un progetto rispetto a un goal dichiarato: le slice verticali e gli spike che ci arrivano, aggiornati man mano che il lavoro viene consegnato, scoperto, rimodellato o abbandonato. Vive in `.roadmap/`. Si invoca esplicitamente (`/roadmap`), l'agent non la attiva da solo. |

## Installazione

```bash
# tutte le skill del repo
npx skills add iacoware/agent-skills

# una sola skill, su agent specifici
npx skills add iacoware/agent-skills -s roadmap -a claude-code -a codex

# globale invece che nel progetto corrente
npx skills add iacoware/agent-skills -g
```

## Sviluppo locale

Dalla root del repo:

```bash
make add                      # installa tutte le skill del repo su claude-code e codex
make add-skill SKILL=roadmap  # solo una
make list                     # elenca le skill scoperte, senza installare
```

`skills add` **copia** i file in `~/.agents/skills/`: rilancia `make add` dopo ogni modifica, e riavvia la sessione dell'agent perché la rilegga (obbligatorio quando cambi `name` o `description`: determinano come la skill viene invocata).

## Design

`design/<skill>/` contiene i documenti di progettazione ed evoluzione delle skill: obiettivi, decisioni, razionale e il glossario del contesto (`CONTEXT.md`, indicizzato da [`CONTEXT-MAP.md`](CONTEXT-MAP.md)). Sta fuori dalle cartelle delle skill per la stessa ragione degli evals — non è payload di runtime e non va installato sulle macchine target. Vedi [`design/roadmap`](design/roadmap).

## Evals

`evals/<skill>/<scenario>/` contiene gli scenari di valutazione, fuori dalle cartelle delle skill perché `skills add` copia solo il payload di runtime: input in `sources/`, oracolo alla root dello scenario, output generati in `results/`. Vedi [`evals/roadmap/recipe-app`](evals/roadmap/recipe-app).

## Test

```bash
make test          # alias di test-roadmap
make test-roadmap  # node:test
```

## Validator

```bash
make validate-roadmap ROADMAP=<dir>   # default .roadmap
```

Il validator di `roadmap` è TypeScript eseguito da Node senza build step: serve Node 23.6 o successivo,
oppure `--experimental-strip-types` fra 22.6 e 23.5.
