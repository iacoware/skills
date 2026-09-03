# Metrics — ROADMAP-CC-6C

Generato da `make run-metrics RUN=<dir>` leggendo `TRANSCRIPT.jsonl`. Nessun numero scritto a
mano: rigenerabile finché il transcript resta.

**Transcript:** 103 righe · **Modello:** `claude-opus-5` · **Sessione:** 2026-09-01T16:17:32.569Z → 2026-09-01T16:29:59.807Z

L'unità è la **richiesta al provider**, non la riga di transcript: una richiesta arriva come una
entry per blocco di contenuto — thinking, testo, chiamata di tool — e ognuna ripete lo stesso
`usage`. Il raggruppamento è per `requestId`.

## Tempo

| | |
|---|---|
| Dal primo prompt all'ultimo evento | 12m 27s |
| Di cui attesa dell'utente | 0s |
| **Tempo attivo** | **12m 27s** |
| Richiesta più lenta | 8m 02s |
| Media per richiesta | 47s |

## Dove va il tempo

Il tempo di ogni richiesta è ripartito fra il pensiero e il lavoro che ha prodotto, in proporzione
ai token emessi; la fase di una richiesta è la cosa più forte che ha fatto, e `Parola all'autore` è
il turno che non ha chiamato nessun tool. Le righe sommano al tempo attivo. Le richieste di un
sub-agent corrono accanto alla sessione e non entrano nelle fasi: quel che costano al driver è
l'attesa del tool, che sta nell'ultima riga.

| Fase | Tempo | Quota |
|---|---|---|
| Thinking | 8m 08s | 65% |
| Scrittura dei documenti | 3m 38s | 29% |
| Lettura | 20s | 3% |
| Validazione | 3s | 0% |
| Parola all'autore | 15s | 2% |
| Altro | 1s | 0% |
| Tool, sub-agent e I/O | 2s | 0% |

Token di output al secondo, sul main: **74**.

## Token

| Voce | Totale |
|---|---|
| input non-cache | 32 |
| cache creation | 103.502 |
| cache read | 1.133.998 |
| output | 55.299 |
| ↳ di cui thinking | 34.173 |

Thinking sull'output: **62%**. Cache read per richiesta: **70.875**.

## Turni

| | |
|---|---|
| Prompt dell'utente | 1 |
| Richieste al provider | 16 |

## Tool

| Tool | Chiamate |
|---|---|
| `Bash` | 18 |
| `Skill (roadmap)` | 1 |
