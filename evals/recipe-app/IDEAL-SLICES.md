Queste sono le slice e l'ordine ideale da un punto di vista di valore di business e rischio tecnico. Anticipano il prima possibile la validazione del valore di business e del rischio tecnico.
Inoltre le slice seguenti sono organizzate in modo da essere molto piccole all'inizio dove il check dell'umano è più frequente per assicurarsi che la costruzione della codebase proceda come vuole lui. Man mano che si va avanti le slice diventano anche più cicciotte perché alcuni pattern sono stati stabiliti e presenti enlla codebase. LLM può attingere alla codebase per capire come scrivere codice in modo soddisfacente.

## ELENCO SLICE

### NOW (Può essere messa in mano a utenti selezionati)

-   0. Setup del repo e CI
-   1. Walking skeleton: visualizza home con provisioning e deploy in ambiente dev. Nienete login, niente promozione in prod
-   2. Login (prima vera slice)
-   3. Creazione e view di un ricettario in home nell'elenco dei ricettari. Detail del ricettario che ovviamente è vuoto. I ricettari sono privati, senza condivisione gli
       utenti non si vedono i ricettari a vicenda
-   4. Costruzione della pipeline di processazione delle ricette. Data una ricetta "normalizzata" ne estrae gli embedding e li salva su PG. Aggiungere la possibilità di
       fare il seed di 3 ricette fixture. Passo necessario per testare la ricerca
-   5. Ricerca semantica cross-lingua (pomodoro, ricetta veloce vegetariana)
-   6. Inserimento e modifica manuale con review. Ci permette di costruire la form di review che sarà poi usata nei passi successivi
-   7. Import URL con JSON-LD
-   8. Fallback LLM da URL
-   9. Estrazione di tutte le foto da uno URL con possibilità per l'utente di scegliere quale tenere. Possibilità di aggiungere foto durante inserimento manuale. La cover è la prima dell'elenco.
-   10. Estrazione da testo incollato
-   11. Invito e accesso a un ricettario

### LATER (Funzionalità che forse dovranno essere inmplementate ma sono dipendenti dal feedback ricevuto dalla versione precedente)

- Scelta foto cover

## CROSS-CUTTING CONCERNS

Ogni slice deve contenere il minimo necessario a rendere questa applicazione usabile in prod:

- Logging
- Gestione degli errori
- Validazione degli oggetti in input non completamente fidati (http, db)
- UI accessibile
- Operazioni esterne con timeout e fallimenti espliciti
