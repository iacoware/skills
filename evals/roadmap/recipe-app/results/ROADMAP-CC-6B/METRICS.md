# Metrics — ROADMAP-CC-6B

Generato da `make run-metrics RUN=<dir>` leggendo `TRANSCRIPT.jsonl`. Nessun numero scritto a
mano: rigenerabile finché il transcript resta.

**Transcript:** 109 righe · **Modello:** `claude-opus-5` · **Sessione:** 2026-09-01T16:17:32.569Z → 2026-09-01T16:28:34.718Z

L'unità è la **richiesta al provider**, non la riga di transcript: una richiesta arriva come una
entry per blocco di contenuto — thinking, testo, chiamata di tool — e ognuna ripete lo stesso
`usage`. Il raggruppamento è per `requestId`.

## Tempo

| | |
|---|---|
| Dal primo prompt all'ultimo evento | 11m 02s |
| Di cui attesa dell'utente | 0s |
| **Tempo attivo** | **11m 02s** |
| Richiesta più lenta | 5m 19s |
| Media per richiesta | 33s |

## Dove va il tempo

Il tempo di ogni richiesta è ripartito fra il pensiero e il lavoro che ha prodotto, in proporzione
ai token emessi; la fase di una richiesta è la cosa più forte che ha fatto, e `Parola all'autore` è
il turno che non ha chiamato nessun tool. Le righe sommano al tempo attivo. Le richieste di un
sub-agent corrono accanto alla sessione e non entrano nelle fasi: quel che costano al driver è
l'attesa del tool, che sta nell'ultima riga.

| Fase | Tempo | Quota |
|---|---|---|
| Thinking | 6m 01s | 54% |
| Scrittura dei documenti | 4m 08s | 37% |
| Lettura | 26s | 4% |
| Validazione | 6s | 1% |
| Parola all'autore | 15s | 2% |
| Altro | 4s | 1% |
| Tool, sub-agent e I/O | 4s | 1% |

Token di output al secondo, sul main: **72**.

## Token

| Voce | Totale |
|---|---|
| input non-cache | 40 |
| cache creation | 95.634 |
| cache read | 1.284.334 |
| output | 47.926 |
| ↳ di cui thinking | 26.006 |

Thinking sull'output: **54%**. Cache read per richiesta: **64.217**.

## Turni

| | |
|---|---|
| Prompt dell'utente | 1 |
| Richieste al provider | 20 |

## Tool

| Tool | Chiamate |
|---|---|
| `Bash` | 18 |
| `Skill (roadmap)` | 1 |
