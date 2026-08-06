# Perché il ciclo è fatto così

Le ragioni delle decisioni prese, non la procedura. **Nessuna fase ha bisogno di aprire questo file
per lavorare:** si apre quando una decisione sembra sbagliata e si vuole sapere su cosa poggia. Ciò
che è normativo sta in `../CONSENSUS-WORKFLOW.md` e negli altri file di questa directory.

## L'obiettivo

Poter modificare `SKILL.md` e accorgersi quando la modifica ha **peggiorato** lo skill. Serve un
**segno con un errore noto**, non un numero: soglie, formula di aggregazione e score calibrato non
sono sul percorso di questa decisione.

L'obiettivo si regge su **due meccanismi disgiunti, con due prove diverse**. Confonderli era
l'errore della stesura precedente, e rendeva irrisolvibili le domande aperte del piano.

- **`REGRESSION-LEDGER.md` rileva il peggioramento, ex-post, sulle dimensioni che copre.** Ogni
  modifica applicata implica una previsione falsificabile; il registro la conserva e il ciclo la
  ricontrolla. È l'unico rilevatore in servizio. Che le sue righe siano falsificabili non è
  un'ipotesi: due lo sono state. Che la copertura sia parziale nemmeno — diciassette righe contro 417
  righe di skill, e le diciassette coprono le stesse clausole delle undici da cui vengono: lo split
  del 2026-08-06 ha separato affermazioni, non aggiunto previsioni.
- **L'intersezione fra `improve` e `review` previene il peggioramento, ex-ante, su una classe sola:
  le regole false.** Non guarda mai la modifica del giro precedente. È un generatore di proposte con
  un filtro di precisione sulle proposte. Che il filtro sia preciso è **un'ipotesi non ancora
  verificata**, e CON-6 è il suo primo test.

Ne discende la conseguenza che il piano prima negava: **una falsificazione dell'ipotesi non fa cadere
l'obiettivo.** Fa cadere l'economia con cui si decide cosa applicare. Il registro funzionerebbe senza
il filtro; il filtro senza il registro non si accorgerebbe di niente.

L'obiettivo è asimmetrico per costruzione, e la formulazione precedente — *«sapere se la modifica ha
migliorato o peggiorato»* — prometteva più di quanto lo strumento dia. Il ciclo decide su **una
generazione per modello per ciclo**, e la regola di decisione del registro è *«un'affermazione regge
solo se regge su entrambi»*: basta **1 violazione su 2** per falsificare, servono **0 su 2** per
confermare. Il primo lato è solido — un controesempio è un controesempio. Il secondo è assenza di
controesempio su un campione di due.

Che il campione di due non basti non è teoria. Nel ciclo CON-5 `R-002` è violata su `CC` e non su
`CX`; `R-008` è violata su `CX` e non su `CC`. Due generazioni dello stesso ciclo, sulla stessa
regola, esito opposto: è la misura diretta della varianza del generatore, ed è dello stesso ordine di
grandezza dell'effetto che si sta cercando.

Da qui la semantica del registro: lo stato non è `tiene` ma **`non smentita ×k`**, con `k` il numero
di cicli consecutivi in cui la riga non è stata smentita su entrambi i piani. Una riga `×1` e una
`×5` non sono la stessa cosa, e la parola non deve più promettere ciò che il campione non dà. Il
miglioramento si inferisce solo dall'assenza cumulata di smentite, mai da un singolo giro.

La leva economica scelta è il **tempo, non il campione**: rigenerare k volte per lato moltiplica il
costo del ciclo e contraddice la proporzionalità che è la ragione stessa per cui il grading è stato
abbandonato. L'accumulo su cicli successivi dà lo stesso segnale gratis, con il ritardo come prezzo.

## Perché il grading system è abbandonato

Nessun miglioramento allo `SKILL.md` è mai derivato da uno score. Il più sostanzioso — `2c89e7f`,
separazione fra confine di scope e identità — nasce da un umano che ha letto un piano generato,
formulato un sospetto, verificato contro le fonti e scoperto che il difetto vero era un altro: la
giunzione non dichiarata. Nessuno dei 26 criteri della rubric conteneva quella proprietà, perché non
esisteva prima che la lettura la producesse. La lettura umana produce conoscenza nuova; il grading
system misura conoscenza già codificata.

A questo si aggiungono due proprietà che nessuna calibrazione corregge: **non è sostenibile** per il
ritmo di evoluzione di uno skill — 3.477 righe di Python e una matrice di calibrazione da
ricollezionare a ogni cambio di rubric, contro un `SKILL.md` che cambia più volte a settimana — e
**non è preciso** al livello a cui servirebbe, con un agreement inter-grader di 0,56.

Lo strumento decisionale alternativo è l'**intersezione fra due modelli indipendenti sulle modifiche
proposte allo skill**. Su uno `SKILL.md`, dove ogni regola aggiunta è debito permanente che
condiziona ogni generazione futura, un filtro che manca qualcosa costa meno di uno che applica
qualcosa di falso. Ne discende che l'**adjudication è superflua**: risolvere un disaccordo con un
terzo giudizio è più caro e meno sicuro che rimandarlo alla lettura di chi decide.

Lo stesso principio si applica a se stesso: il filtro va tarato per mancare, non per applicare. Da qui
lo scarto per voce con un solo tentativo, la regola dei due lati su `review`, e il fatto che il ciclo
applichi da sé **solo** ciò che il filtro licenzia.

**Abbandonato il 2026-08-06. Non sospeso, non dietro un gate: non torna.** Il codice e i documenti
restano in git e sono recuperabili dalla storia; non sono mantenuti.

Il gate di ripresa che il documento portava fino al 2026-08-06 era anche **irraggiungibile per
costruzione**: prevedeva la ripresa solo se il ciclo avesse lasciato sfuggire una regressione reale,
scoperta in ritardo — ma l'unico rilevatore in servizio è il ciclo stesso, e la classe di regressioni
per cui il grading era stato costruito è proprio quella su dimensioni che nessuna riga del registro
copre. Nessuno strumento la guardava, quindi non poteva mai far scattare il gate. La **recidiva**
sopravvive a quel gate, con scopo diverso: non è una porta di rientro al grading, è il segnale di
convergenza del ciclo di consenso.

## Il cricchetto

Il ciclo **genera** miglioramenti e non **verifica** miglioramenti. Ogni giro produce una lista
fresca di difetti e non dice mai se la modifica del giro precedente ha funzionato. Il rischio è il
cricchetto: si aggiusta A rompendo B, il ciclo dopo si trova B, si aggiusta B rompendo A, e lo
`SKILL.md` cresce senza convergere.

**Non è un rischio emergente: è la funzione di trasferimento dello strumento.** Un difetto entra in
`improve`, esce come regola nuova, arriva nello `SKILL.md`, diventa riga di registro. Fino al ciclo
CON-6 non esisteva nessun percorso per cui un difetto uscisse come *«questa regola esistente è
formulata male»*. La firma è misurabile:

```
2026-07-30  c001780   247 righe   Add plan-slices skill
2026-07-31  2c89e7f   264
2026-07-31  745192f   312
2026-08-02  d977043   354
2026-08-02  8c7fe34   352   ← unico commit sottrattivo, -7 righe
2026-08-04  9aa2586   382
2026-08-04  eb926bb   389
2026-08-06  28b5460   417 righe
```

**+69% in sette giorni, 18 commit, un solo commit che toglie qualcosa.**

`R-010` e `R-011` sembravano i due esempi della firma. Verificato sui diff il 2026-08-06, **non lo
sono: sono riformulazioni in loco.** `87150d3` riscrive il paragrafo di § 1 su cui `R-002` era nata —
`+7/-3`, `close` spaccato in *expose* e *resolve*; `eb926bb` riscrive la frase di § 2 su cui era nata
`R-008` — `+4/-2`, il marcatore `*(Developer outcome)*` inserito dentro la stessa frase. Ciò che è
entrato come aggiunta non è la regola: è la **riga di registro**. Lo skill ha preso +4 e +2 righe, il
registro +2 righe su 9.

Va corretta di conseguenza anche l'affermazione che fino a CON-6 non esistesse nessun percorso per cui
un difetto uscisse come *«questa regola esistente è formulata male»*. Il percorso non esisteva **nel
workflow**; fuori dal workflow un umano l'ha percorso due volte nella stessa sera. Il rimedio non è
inventare una mossa mai fatta: è renderla disponibile a `improve`, che oggi non ha modo di proporla,
e impedire che il costo si scarichi sul registro come è già successo.

Il principio mancante era già scritto, nel posto sbagliato. `REGRESSION-LEDGER.md`: *«La sequenza di
regressioni sullo stesso tema è il segnale che la regola è formulata male, non che va riscritta
ancora.»* Il registro sapeva che un difetto ricorrente accusa una regola esistente; il prompt che
genera i rimedi non lo sapeva, e non aveva modo di dirlo.

Quattro rimedi, tutti a costo zero di chiamate:

- **`improve` bidirezionale con regola dura**, in `CYCLE.md`, resa applicabile dalla mappa clausola →
  riga.
- **Righe di registro sottrattive.** Una riga può nascere `Origine: potatura`, con l'affermazione
  «la rimozione di X non fa ricomparire il difetto Y». Prima il registro poteva registrare solo
  crescita, quindi anche la sua storia era cieca al fenomeno.
- **Contatori in testa al report.** Il passaggio da *«leggo i report e scrivo io la modifica»* a
  *«leggo il diff e pongo il veto»* è più sostenibile, ma inverte il default: autorare-prima ha per
  default l'inazione, vetare-dopo ha per default l'accettazione. E la patologia misurata è l'accumulo.
  Un veto è debole contro un diff di otto righe di regola plausibile — diciotto volte in una settimana
  e sei di nuovo a +69%. I contatori in testa lo rendono forte perché mordono sull'accumulo invece che
  sul merito: `0 riformulazioni su 5 aggiunte` è già il verdetto, e non richiede di leggere le regole.
- **Recidiva**, passo 7. Se è sistematicamente maggiore di zero, il registro sta dichiarando chiuso ciò
  che non lo è. Se è zero mentre lo `SKILL.md` continua a crescere, il ciclo trova cose genuinamente
  nuove — legittimo, ma prima o poi va chiesto se quella crescita sia sostenibile.

## Cosa il ciclo eredita dal grading system

Costruito, pagato e riusato subito: il validator strutturale `validate_plan.py`;
`recipe-app/EVALUATION-BRIEF.md`, che sostituisce il confronto con un piano ideale — confrontare con
un piano ideale misura la somiglianza a quel piano, non la qualità; l'anonimizzazione dei candidati;
la tassonomia dei sette assi di lettura, che coincide con quella della rubric v3; l'hashing di
prompt, fonti e brief con artefatti immutabili, che tiene i cicli confrontabili; la disciplina di
`NOTES.md`. Non serve la scala a cinque verdetti, non serve lo score.

Va aggiunta l'architettura template + validator, ereditata dallo skill invece che dal grading: è la
sola parte del sistema che ha retto cinque cicli senza degradare.
