# S5 — Ricerca semantica cross-lingua nel ricettario

← [Register](../roadmap.md#now)

**Outcome:** Scrivi a parole tue nella barra di ricerca e vedi le ricette del ricettario corrente
ordinate per somiglianza, anche quando sono scritte in un'altra lingua.

**Requested by:** `goal.md` §§ Differenziatore, Ricerca; `concepts.md` § Ricerca (MVP).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Gli sviluppatori e un tester sullo staging: è la riga che porta il differenziatore dentro l'app,
ancora su un ricettario configurato.

## Includes

- Indice HNSW sulla colonna `embedding` e la sua migrazione.
- Barra di ricerca in home, sopra l'elenco.
- Embedding della query a runtime con lo stesso modello di `S3`: una chiamata da pochi token, la
  sola che la ricerca fa fuori dal database.
- Query di similarità su pgvector, scoped da `currentCookbook`.
- Risultati con titolo, copertina se c'è e un estratto; stato vuoto distinto fra "il ricettario è
  vuoto" e "nessun risultato abbastanza vicino".
- Fallimento della chiamata di embedding gestito con un messaggio esplicito.

## Verification

- Caricato il corpus di `S2` nel ricettario, la query "pomodoro" restituisce ricette scritte in
  inglese che non contengono quella parola, e "cena leggera" restituisce risultati plausibili senza
  nessuna corrispondenza lessicale.
- Il recall@10 misurato dentro l'app sulle query di `S2` è confrontato con quello misurato fuori:
  la differenza è scritta.
- Una ricetta che sta in un secondo ricettario non compare mai fra i risultati del primo, nemmeno
  quando è la corrispondenza migliore in assoluto.
- Il tempo di risposta della ricerca è misurato e scomposto fra chiamata di embedding e query SQL,
  su un ricettario da qualche centinaio di ricette.
- Con il servizio di embedding irraggiungibile l'utente legge un errore che lo dice, non un elenco
  vuoto.

## Learning target

Se la qualità cross-lingua misurata in laboratorio da `S2` sopravvive dentro l'app su pgvector con
indice HNSW, e quanto la chiamata di embedding sulla query pesa sulla latenza percepita, col cold
start di Fly sopra.

## Excludes

- Filtri per tag e tempo e ricerca ibrida: candidati in `LATER`; i campi si popolano già da `S3`,
  quindi si abiliteranno senza migrazione.
- Ricerca che attraversa più ricettari: candidato in `LATER`.
- Ricerca full-text come ripiego: fuori, l'MVP è solo semantico per scelta dichiarata.

## Open questions

- —
