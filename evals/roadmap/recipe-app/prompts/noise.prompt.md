Leggi {{RUN_DIR}}/noise/residual.json. Contiene, per ogni coppia di run gemelli e per tre assi (themes, rows, outOfScope), i record che il match meccanico non ha accoppiato: gli stessi documenti disegnati due volte, dove le stringhe non coincidono alla lettera.

Il tuo compito è solo l'allineamento, mai il giudizio di qualità: non decidi chi ha ragione, decidi se due record sono lo stesso elemento espresso con altre parole. Per ogni record di sinistra la domanda è binaria, sul record intero (nome o titolo, promessa o razionale, campi strutturati): esiste a destra uno e un solo record che è lo stesso elemento? Se sì, è una coppia allineata. Se non ha controparte, o se ne avrebbe due plausibili, è non allineabile: lo lasci fuori dalle coppie e non lo forzi. Un campo strutturato diverso (kind, size, tema) non impedisce l'allineamento se l'identità è la stessa: la divergenza sui campi la misura il codice, non tu.

Scrivi {{RUN_DIR}}/noise/alignment.json, esattamente questa forma:

```json
{
  "pairs": [
    {
      "left": "<nome del run di sinistra, come in residual.json>",
      "right": "<nome del run di destra>",
      "themes": [{ "left": "<key>", "right": "<key>" }],
      "rows": [{ "left": "<key>", "right": "<key>" }],
      "outOfScope": [{ "left": "<key>", "right": "<key>" }]
    }
  ]
}
```

Vincoli:

- Una entry in `pairs` per ogni coppia di run presente in residual.json, nello stesso ordine, anche quando tutti i suoi assi restano vuoti.
- Le chiavi sono il campo `key` dei record di residual.json, copiate alla lettera; ogni chiave usata al più una volta per lato. I record che non allinei non compaiono: non esiste una lista dei non allineabili, la calcola il codice per differenza.
- Non leggere e non scrivere nient'altro: il record nel JSON è tutta l'evidenza. Non aprire le mappe dei run, le review, o altri file del repository.
