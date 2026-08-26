# Metrics — ROADMAP-CC-4

Generato da `make run-metrics RUN=<dir>` leggendo `TRANSCRIPT.jsonl`. Nessun numero scritto a
mano: rigenerabile finché il transcript resta.

**Transcript:** 107 righe · **Modello:** `claude-opus-5` · **Sessione:** 2026-08-26T14:59:11.651Z → 2026-08-26T15:10:20.893Z

L'unità è la **richiesta al provider**, non la riga di transcript: una richiesta arriva come una
entry per blocco di contenuto — thinking, testo, chiamata di tool — e ognuna ripete lo stesso
`usage`. Il raggruppamento è per `requestId`.

## Tempo

| | |
|---|---|
| Dal primo prompt all'ultimo evento | 11m 09s |
| Di cui attesa dell'utente | 0s |
| **Tempo attivo** | **11m 09s** |
| Richiesta più lenta | 7m 26s |
| Media per richiesta | 33s |

## Dove va il tempo

Il tempo di ogni richiesta è ripartito fra il pensiero e il lavoro che ha prodotto, in proporzione
ai token emessi; la fase di una richiesta è la cosa più forte che ha fatto, e `Parola all'autore` è
il turno che non ha chiamato nessun tool. Le righe sommano al tempo attivo. Le richieste di un
sub-agent corrono accanto alla sessione e non entrano nelle fasi: quel che costano al driver è
l'attesa del tool, che sta nell'ultima riga.

| Fase | Tempo | Quota |
|---|---|---|
| Thinking | 6m 30s | 58% |
| Scrittura dei documenti | 3m 45s | 34% |
| Lettura | 27s | 4% |
| Validazione | 6s | 1% |
| Parola all'autore | 15s | 2% |
| Altro | 3s | 0% |
| Tool, sub-agent e I/O | 3s | 0% |

Token di output al secondo, sul main: **71**.

## Token

| Voce | Totale |
|---|---|
| input non-cache | 40 |
| cache creation | 110.922 |
| cache read | 1.351.610 |
| output | 47.220 |
| ↳ di cui thinking | 26.987 |

Thinking sull'output: **57%**. Cache read per richiesta: **67.581**.

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
