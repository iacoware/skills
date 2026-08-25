# Metrics — ROADMAP-CC-3

Generato da `make run-metrics RUN=<dir>` leggendo `TRANSCRIPT.jsonl`. Nessun numero scritto a
mano: rigenerabile finché il transcript resta.

**Transcript:** 125 righe · **Modello:** `claude-opus-5` · **Sessione:** 2026-08-25T15:16:42.026Z → 2026-08-25T15:30:56.850Z

## Tempo

| | |
|---|---|
| Dal primo prompt all'ultimo evento | 13m 23s |
| Di cui attesa dell'utente | 0s |
| **Tempo attivo** | **13m 23s** |
| Chiamata più lenta | 4m 35s |
| Media per chiamata | 25s |

## Token

| Voce | Totale |
|---|---|
| input non-cache | 64 |
| cache creation | 184.412 |
| cache read | 2.563.287 |
| output | 130.487 |
| ↳ di cui thinking | 84.869 |

Thinking sull'output: **65%**. Cache read per chiamata: **80.103**.

## Turni

| | |
|---|---|
| Prompt dell'utente | 1 |
| Chiamate API | 32 |

## Tool

| Tool | Chiamate |
|---|---|
| `Bash` | 15 |
| `Skill (roadmap)` | 1 |
