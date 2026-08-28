# Metrics — ROADMAP-CC-5

Generato da `make run-metrics RUN=<dir>` leggendo `TRANSCRIPT.jsonl`. Nessun numero scritto a
mano: rigenerabile finché il transcript resta.

**Transcript:** 133 righe · **Modello:** `claude-opus-5` · **Sessione:** 2026-08-27T16:51:46.963Z → 2026-08-27T17:05:07.108Z

L'unità è la **richiesta al provider**, non la riga di transcript: una richiesta arriva come una
entry per blocco di contenuto — thinking, testo, chiamata di tool — e ognuna ripete lo stesso
`usage`. Il raggruppamento è per `requestId`.

## Tempo

| | |
|---|---|
| Dal primo prompt all'ultimo evento | 13m 20s |
| Di cui attesa dell'utente | 0s |
| **Tempo attivo** | **13m 20s** |
| Richiesta più lenta | 4m 56s |
| Media per richiesta | 31s |

## Dove va il tempo

Il tempo di ogni richiesta è ripartito fra il pensiero e il lavoro che ha prodotto, in proporzione
ai token emessi; la fase di una richiesta è la cosa più forte che ha fatto, e `Parola all'autore` è
il turno che non ha chiamato nessun tool. Le righe sommano al tempo attivo. Le richieste di un
sub-agent corrono accanto alla sessione e non entrano nelle fasi: quel che costano al driver è
l'attesa del tool, che sta nell'ultima riga.

| Fase | Tempo | Quota |
|---|---|---|
| Thinking | 7m 56s | 59% |
| Scrittura dei documenti | 4m 14s | 32% |
| Lettura | 39s | 5% |
| Validazione | 6s | 1% |
| Parola all'autore | 15s | 2% |
| Altro | 6s | 1% |
| Tool, sub-agent e I/O | 4s | 0% |

Token di output al secondo, sul main: **72**.

## Token

| Voce | Totale |
|---|---|
| input non-cache | 52 |
| cache creation | 116.296 |
| cache read | 1.967.686 |
| output | 57.658 |
| ↳ di cui thinking | 33.617 |

Thinking sull'output: **58%**. Cache read per richiesta: **75.680**.

## Turni

| | |
|---|---|
| Prompt dell'utente | 1 |
| Richieste al provider | 26 |

## Tool

| Tool | Chiamate |
|---|---|
| `Bash` | 24 |
| `Skill (roadmap)` | 1 |
