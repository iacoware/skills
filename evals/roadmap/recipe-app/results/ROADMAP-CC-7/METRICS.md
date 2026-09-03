# Metrics — ROADMAP-CC-7

Generato da `make run-metrics RUN=<dir>` leggendo `TRANSCRIPT.jsonl`. Nessun numero scritto a
mano: rigenerabile finché il transcript resta.

**Transcript:** 118 righe · **Modello:** `claude-opus-5` · **Sessione:** 2026-09-03T11:05:23.992Z → 2026-09-03T11:19:58.491Z

L'unità è la **richiesta al provider**, non la riga di transcript: una richiesta arriva come una
entry per blocco di contenuto — thinking, testo, chiamata di tool — e ognuna ripete lo stesso
`usage`. Il raggruppamento è per `requestId`.

## Tempo

| | |
|---|---|
| Dal primo prompt all'ultimo evento | 14m 34s |
| Di cui attesa dell'utente | 0s |
| **Tempo attivo** | **14m 34s** |
| Richiesta più lenta | 9m 03s |
| Media per richiesta | 42s |

## Dove va il tempo

Il tempo di ogni richiesta è ripartito fra il pensiero e il lavoro che ha prodotto, in proporzione
ai token emessi; la fase di una richiesta è la cosa più forte che ha fatto, e `Parola all'autore` è
il turno che non ha chiamato nessun tool. Le righe sommano al tempo attivo. Le richieste di un
sub-agent corrono accanto alla sessione e non entrano nelle fasi: quel che costano al driver è
l'attesa del tool, che sta nell'ultima riga.

| Fase | Tempo | Quota |
|---|---|---|
| Thinking | 9m 27s | 65% |
| Scrittura dei documenti | 4m 07s | 28% |
| Lettura | 33s | 4% |
| Validazione | 6s | 1% |
| Parola all'autore | 15s | 2% |
| Altro | 2s | 0% |
| Tool, sub-agent e I/O | 4s | 0% |

Token di output al secondo, sul main: **74**.

## Token

| Voce | Totale |
|---|---|
| input non-cache | 42 |
| cache creation | 114.003 |
| cache read | 1.681.475 |
| output | 64.844 |
| ↳ di cui thinking | 40.171 |

Thinking sull'output: **62%**. Cache read per richiesta: **80.070**.

## Turni

| | |
|---|---|
| Prompt dell'utente | 1 |
| Richieste al provider | 21 |

## Tool

| Tool | Chiamate |
|---|---|
| `Bash` | 23 |
| `Skill (roadmap)` | 1 |
