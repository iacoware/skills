# Metrics — ROADMAP-CC-3

Generato da `make run-metrics RUN=<dir>` leggendo `TRANSCRIPT.jsonl`. Nessun numero scritto a
mano: rigenerabile finché il transcript resta.

**Transcript:** 125 righe · **Modello:** `claude-opus-5` · **Sessione:** 2026-08-25T15:16:42.026Z → 2026-08-25T15:30:56.850Z

L'unità è la **richiesta al provider**, non la riga di transcript: una richiesta arriva come una
entry per blocco di contenuto — thinking, testo, chiamata di tool — e ognuna ripete lo stesso
`usage`. Il raggruppamento è per `requestId`.

## Tempo

| | |
|---|---|
| Dal primo prompt all'ultimo evento | 13m 23s |
| Di cui attesa dell'utente | 0s |
| **Tempo attivo** | **13m 23s** |
| Richiesta più lenta | 4m 35s |
| Media per richiesta | 50s |

## Dove va il tempo

Il tempo di ogni richiesta è ripartito fra il pensiero e il lavoro che ha prodotto, in proporzione
ai token emessi; la fase di una richiesta è la cosa più forte che ha fatto, e `Parola all'autore` è
il turno che non ha chiamato nessun tool. Le righe sommano al tempo attivo. Le richieste di un
sub-agent corrono accanto alla sessione e non entrano nelle fasi: quel che costano al driver è
l'attesa del tool, che sta nell'ultima riga.

| Fase | Tempo | Quota |
|---|---|---|
| Thinking | 8m 14s | 61% |
| Scrittura dei documenti | 4m 24s | 33% |
| Lettura | 23s | 3% |
| Validazione | 3s | 0% |
| Parola all'autore | 15s | 2% |
| Altro | 3s | 0% |
| Tool, sub-agent e I/O | 2s | 0% |

Token di output al secondo, sul main: **72**.

## Token

| Voce | Totale |
|---|---|
| input non-cache | 32 |
| cache creation | 105.936 |
| cache read | 1.332.316 |
| output | 58.147 |
| ↳ di cui thinking | 34.859 |

Thinking sull'output: **60%**. Cache read per richiesta: **83.270**.

## Turni

| | |
|---|---|
| Prompt dell'utente | 1 |
| Richieste al provider | 16 |

## Tool

| Tool | Chiamate |
|---|---|
| `Bash` | 15 |
| `Skill (roadmap)` | 1 |
