# agent-skills

Agent skills installabili con la [Skills CLI](https://github.com/vercel-labs/skills), compatibili con Claude Code, Codex e gli altri agent supportati.

## Skills

| Skill | Descrizione |
| --- | --- |
| [`plan-slices`](skills/plan-slices) | Crea, rivede, splitta, unisce e riordina delivery plan per prodotti greenfield e capability rilevanti: slicing verticale risk-first con orizzonti NOW / LATER / OUT-OF-SCOPE. |

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

Installa dal path locale: la CLI crea symlink, quindi le modifiche al repo sono immediatamente visibili agli agent.

```bash
npx skills add ./path/a/agent-skills -g -a claude-code -a codex
```

Riavvia la sessione dell'agent dopo aver modificato il frontmatter di un `SKILL.md` (`name` e `description` determinano l'attivazione).

## Test

```bash
cd skills/plan-slices/scripts && python3 test_validate_plan.py
```
