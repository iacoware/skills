# Miglioramenti consigliati a `plan-slices`

- Rendere obbligatorio un audit interno split/merge per ogni coppia di capability, registrando quali possono essere rinviate indipendentemente.
- Costruire una matrice interna `comportamento → tema → orizzonte → slice proprietaria`; bloccare fusioni, duplicazioni e scope leakage.
- Aggiungere un audit di adiacenza: enabler e validatore devono restare vicini; un tema non deve essere riaperto dopo temi indipendenti senza motivazione.
- Rendere esplicita la distinzione tra primo enabler tecnico e prima validazione di prodotto di ciascun tema.
- Aggiungere una ricerca sistematica di affermazioni incompatibili e decisioni ancora placeholder; ogni conflitto deve diventare domanda o spike prima delle slice coinvolte.
- Richiedere un ledger interno “fuori dalla slice” per impedire adapter anticipati e funzionalità `LATER` introdotte in `NOW`.
- Estendere il validatore con controlli semantici configurabili: temi interrotti, first validation inesistente, adapter duplicati, domande dichiarate ma ignorate dalle slice.
- Ridurre il dettaglio implementativo pubblicato: privilegiare outcome, rischio, confini ed evidenza capace di cambiare una decisione.
