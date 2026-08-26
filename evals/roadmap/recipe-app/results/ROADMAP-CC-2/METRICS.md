# Metrics — ROADMAP-CC-2

Generato da `make run-metrics RUN=<dir>` leggendo `TRANSCRIPT.jsonl`. Nessun numero scritto a
mano: rigenerabile finché il transcript resta.

**Transcript:** 150 righe · **Modello:** `claude-opus-5` · **Sessione:** 2026-08-25T10:43:36.386Z → 2026-08-25T10:57:13.324Z

L'unità è la **richiesta al provider**, non la riga di transcript: una richiesta arriva come una
entry per blocco di contenuto — thinking, testo, chiamata di tool — e ognuna ripete lo stesso
`usage`. Il raggruppamento è per `requestId`.

## Tempo

| | |
|---|---|
| Dal primo prompt all'ultimo evento | 12m 22s |
| Di cui attesa dell'utente | 0s |
| **Tempo attivo** | **12m 22s** |
| Richiesta più lenta | 2m 59s |
| Media per richiesta | 31s |

## Dove va il tempo

Il tempo di ogni richiesta è ripartito fra il pensiero e il lavoro che ha prodotto, in proporzione
ai token emessi; la fase di una richiesta è la cosa più forte che ha fatto, e `Parola all'autore` è
il turno che non ha chiamato nessun tool. Le righe sommano al tempo attivo. Le richieste di un
sub-agent corrono accanto alla sessione e non entrano nelle fasi: quel che costano al driver è
l'attesa del tool, che sta nell'ultima riga.

| Fase | Tempo | Quota |
|---|---|---|
| Thinking | 5m 39s | 46% |
| Scrittura dei documenti | 5m 46s | 47% |
| Lettura | 28s | 4% |
| Validazione | 3s | 0% |
| Parola all'autore | 17s | 2% |
| Altro | 6s | 1% |
| Tool, sub-agent e I/O | 3s | 0% |

Token di output al secondo, sul main: **70**.

## Token

| Voce | Totale |
|---|---|
| input non-cache | 48 |
| cache creation | 97.661 |
| cache read | 1.967.259 |
| output | 51.594 |
| ↳ di cui thinking | 23.488 |

Thinking sull'output: **46%**. Cache read per richiesta: **81.969**.

## Turni

| | |
|---|---|
| Prompt dell'utente | 1 |
| Richieste al provider | 24 |

## Tool

| Tool | Chiamate |
|---|---|
| `Bash` | 22 |
| `Skill (roadmap)` | 1 |
