# Metrics — ROADMAP-CC-2

Generato da `make run-metrics RUN=<dir>` leggendo `TRANSCRIPT.jsonl`. Nessun numero scritto a
mano: rigenerabile finché il transcript resta.

**Transcript:** 150 righe · **Modello:** `claude-opus-5` · **Sessione:** 2026-08-25T10:43:36.386Z → 2026-08-25T10:57:13.324Z

## Tempo

| | |
|---|---|
| Dal primo prompt all'ultimo evento | 12m 22s |
| Di cui attesa dell'utente | 0s |
| **Tempo attivo** | **12m 22s** |
| Chiamata più lenta | 2m 58s |
| Media per chiamata | 20s |

## Token

| Voce | Totale |
|---|---|
| input non-cache | 74 |
| cache creation | 151.421 |
| cache read | 2.905.751 |
| output | 93.087 |
| ↳ di cui thinking | 58.932 |

Thinking sull'output: **63%**. Cache read per chiamata: **78.534**.

## Turni

| | |
|---|---|
| Prompt dell'utente | 1 |
| Chiamate API | 37 |

## Tool

| Tool | Chiamate |
|---|---|
| `Bash` | 22 |
| `Skill (roadmap)` | 1 |
