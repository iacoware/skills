# agent-skills

Agent skills installabili con la [Skills CLI](https://github.com/vercel-labs/skills), compatibili con Claude Code, Codex e gli altri agent supportati.

## Skills

| Skill | Descrizione |
| --- | --- |
| [`plan-slices`](skills/plan-slices) | Crea, rivede, splitta, unisce e riordina delivery plan per prodotti greenfield e capability rilevanti: slice verticali value-first e risk-first, con orizzonti NOW / LATER / OUT-OF-SCOPE. Si invoca esplicitamente (`/plan-slices`), l'agent non la attiva da solo. **Deprecata**: superata da [`roadmap`](skills/roadmap). Resta installabile e non viene rimossa. |
| [`roadmap`](skills/roadmap) | Tiene viva la roadmap di un progetto rispetto a un goal dichiarato: le slice verticali e gli spike che ci arrivano, aggiornati man mano che il lavoro viene consegnato, scoperto, rimodellato o abbandonato. Vive in `.roadmap/`. Si invoca esplicitamente (`/roadmap`), l'agent non la attiva da solo. |

## Installazione

```bash
# tutte le skill del repo
npx skills add iacoware/agent-skills

# una sola skill, su agent specifici
npx skills add iacoware/agent-skills -s plan-slices -a claude-code -a codex

# globale invece che nel progetto corrente
npx skills add iacoware/agent-skills -g
```

## Sviluppo locale

Dalla root del repo:

```bash
make add                      # installa tutte le skill del repo su claude-code e codex
make add-skill SKILL=plan-slices   # solo una
make list                     # elenca le skill scoperte, senza installare
```

`skills add` **copia** i file in `~/.agents/skills/`: rilancia `make add` dopo ogni modifica, e riavvia la sessione dell'agent perché la rilegga (obbligatorio quando cambi `name` o `description`: determinano come la skill viene invocata).

## Design

`design/<skill>/` contiene i documenti di progettazione ed evoluzione delle skill: obiettivi, decisioni, razionale e il glossario del contesto (`CONTEXT.md`, indicizzato da [`CONTEXT-MAP.md`](CONTEXT-MAP.md)). Sta fuori dalle cartelle delle skill per la stessa ragione degli evals — non è payload di runtime e non va installato sulle macchine target. Vedi [`design/roadmap`](design/roadmap).

## Evals

`evals/<skill>/<scenario>/` contiene gli scenari di valutazione, fuori dalle cartelle delle skill perché `skills add` copia solo il payload di runtime: input in `sources/`, oracolo alla root dello scenario, output generati in `results/`. Vedi [`evals/plan-slices/recipe-app`](evals/plan-slices/recipe-app).

## Test

```bash
make test                 # entrambe le suite
make test-plan-slices     # solo unittest Python
make test-roadmap         # solo node:test
```

## Validator

```bash
make validate PLAN=<plan.md>          # plan-slices
make validate-roadmap ROADMAP=<dir>   # roadmap, default .roadmap
```

Il validator di `roadmap` è TypeScript eseguito da Node senza build step: serve Node 23.6 o successivo,
oppure `--experimental-strip-types` fra 22.6 e 23.5.
