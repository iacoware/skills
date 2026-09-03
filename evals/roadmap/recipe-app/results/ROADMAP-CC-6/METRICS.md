# Metrics — ROADMAP-CC-6

Generato da `make run-metrics RUN=<dir>` leggendo `TRANSCRIPT.jsonl`. Nessun numero scritto a
mano: rigenerabile finché il transcript resta.

**Transcript:** 97 righe · **Modello:** `claude-opus-5` · **Sessione:** 2026-09-01T15:39:11.146Z → 2026-09-01T15:49:13.523Z

L'unità è la **richiesta al provider**, non la riga di transcript: una richiesta arriva come una
entry per blocco di contenuto — thinking, testo, chiamata di tool — e ognuna ripete lo stesso
`usage`. Il raggruppamento è per `requestId`.

## Tempo

| | |
|---|---|
| Dal primo prompt all'ultimo evento | 10m 02s |
| Di cui attesa dell'utente | 0s |
| **Tempo attivo** | **10m 02s** |
| Richiesta più lenta | 4m 17s |
| Media per richiesta | 38s |

## Dove va il tempo

Il tempo di ogni richiesta è ripartito fra il pensiero e il lavoro che ha prodotto, in proporzione
ai token emessi; la fase di una richiesta è la cosa più forte che ha fatto, e `Parola all'autore` è
il turno che non ha chiamato nessun tool. Le righe sommano al tempo attivo. Le richieste di un
sub-agent corrono accanto alla sessione e non entrano nelle fasi: quel che costano al driver è
l'attesa del tool, che sta nell'ultima riga.

| Fase | Tempo | Quota |
|---|---|---|
| Thinking | 5m 06s | 51% |
| Scrittura dei documenti | 4m 15s | 42% |
| Lettura | 22s | 4% |
| Validazione | 3s | 0% |
| Parola all'autore | 12s | 2% |
| Altro | 1s | 0% |
| Tool, sub-agent e I/O | 3s | 1% |

Token di output al secondo, sul main: **73**.

## Token

| Voce | Totale |
|---|---|
| input non-cache | 32 |
| cache creation | 90.982 |
| cache read | 1.048.482 |
| output | 43.950 |
| ↳ di cui thinking | 22.082 |

Thinking sull'output: **50%**. Cache read per richiesta: **65.530**.

## Turni

| | |
|---|---|
| Prompt dell'utente | 1 |
| Richieste al provider | 16 |

## Tool

| Tool | Chiamate |
|---|---|
| `Bash` | 16 |
| `Skill (roadmap)` | 1 |
