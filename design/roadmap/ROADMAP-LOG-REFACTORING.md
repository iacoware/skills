# Roadmap-log — altri decision-log: candidati

Il log (`.roadmap/log.md`, formato e regole in `drawing-the-map.md` § *Themes* e `SKILL.md`) è
atterrato con i soli verdetti di boundary (`09c37ea`…`3fc0293`, CC-7 verde su R-008, R-009, R-036,
R-037). Il perimetro del primo colpo è rimasto stretto perché partire stretto è reversibile. Ma la
domanda «quali altre decisioni del modello migliorano se scritte prima della mappa» ha risposte con
evidenza, e il formato — H2 per sessione, bullet «soggetto — verdetto — fatto» — è fatto per
riceverle un tipo alla volta, ciascuno col suo run. Il criterio di ammissione è lo stesso dei
verdetti: una decisione che la skill già impone, che oggi resta nel ragionamento e che i run
mostrano presa male o non presa. In ordine di evidenza, stato al 2026-09-04 (CC-2…CC-7):

1. **Le uscite dello sweep** (`drawing-the-map.md`, *What the map reports about its input*). Per
   ogni conflitto e ogni scelta non decisa: sorgente, lato preso, uscita (`Assumptions` / `Open
   questions` / spike). **R-015 è rossa in 7 run su 7** per C1; due commit l'hanno presa di mira
   (`8eb3a71`, poi `51a81eb` che fa del tell un lookup sulle sorgenti) e il secondo non ha ancora
   un run. Stesso meccanismo dei verdetti: lo sweep «is what has to be thought before the section is
   written», e niente obbliga a pensarlo. Scritto nel log prima di `Assumptions`, lo sweep avviene,
   e il lato preso in un bullet senza riga nella mappa diventa un diff (entry nel log senza uscita).
   Il reviewer guadagna la lista dello sweep, che oggi ricostruisce rifacendolo. Costo: 5–10 entry
   per disegno; azzerate dal redraw come i verdetti. Candidato più forte.
   **Non rende superfluo `51a81eb`**: i due coprono fallimenti diversi dello stesso passo. Il log
   vede solo le coppie che lo sweep ha trovato, e scatta su «coppia trovata, uscita non presa». Il
   fallimento di CC-7 è l'altro — «coppia non trovata»: la sessione ha letto le sorgenti come
   concordi su C1, e un log scritto da quella sessione non avrebbe avuto l'entry. Il lookup parte
   dai bullet della riga, dopo il primo taglio, e risale alle sorgenti; con il log ha un posto dove
   far atterrare quel che trova (un'entry nuova con la sua uscita). Diventa superfluo solo se
   scrivere le entry per comportamento rende lo sweep abbastanza attento da trovare C1 da solo:
   si vede nel run, R-015 verde con C1 nel log sotto lo sweep e non aggiunto dopo.
2. **Il test di sostituzione sugli archi** (*Hard dependencies*): per coppia candidata, `edge` /
   `order`, e lo stand-in nominato oppure il deliverable che nessun fixture fornisce. R-017 rossa in
   4 run su 6 (CC-2…CC-5), **verde in CC-6 e CC-7**: i quattro commit a bersaglio hanno attecchito e
   l'evidenza si è esaurita. Resta il secondo asse più rumoroso di `NOISE.md` (7/12, 8/8, 8/13), ed
   è la decisione che reshaping e reorder rileggono per costruzione. Costo: il più alto — le coppie
   sono molte; il perimetro andrebbe ristretto a quelle su cui la regola pone la domanda (dipendente
   il cui `Includes` o `Verification` tocca ciò che un'altra riga `NOW` consegna). Fermo finché
   R-017 non torna rossa.
3. **Ranking dichiarato e deroghe** (*Ordering for learning*), ovvero la reintroduzione di
   `Ordering criteria` nel log invece che nella mappa. La riga «the map declares its own ranking»
   non ha oggi nessun posto dove il ranking sia detto, e ogni deroga a breadth-before-depth deve
   essere una delle quattro. R-012 rossa in 2 run su 5 registrati (CC-4, CC-6), verde in CC-7 dove
   la deroga è argomentata con «required recovery»; nessun commit a bersaglio. `d805196` tolse la
   sezione dalla mappa perché misurata come copia della skill (946 caratteri di CC-3 ripetevano
   regole del payload) più due deroghe: nel log entra solo la parte che la mappa sola conosce — una
   riga per il ranking, una per deroga con la licenza invocata e la riga che la porta. Attenzione:
   R-012 «read from the rows, never from a statement about them» resta vero — il log serve alla
   decisione, non al reviewer.
4. **Lo sweep cross-funzionale**: cinque dimensioni, una riga ciascuna, «nulla» o la concern
   pubblicata. «The absence is information», ma un'assenza è indistinguibile da uno sweep non
   fatto. R-022 rossa in 3 run su 7, verde negli ultimi tre. Costo quasi zero; evidenza debole.
5. **La rilettura di `LATER` e delle righe aperte in un redraw** (*What carries*): ogni candidato
   riceve un verdetto — promosso, tenuto, ucciso — e oggi gli uccisi spariscono senza traccia.
   Nessuno scenario lo esercita (il fixture `redrawn/` è l'output di un redraw, non il suo test).
   Ultimo per evidenza.

Cosa **non** entra: il verdetto slice/spike all'admission (lo porta `kind`), la domanda di coverage
(R-031 vive nel transcript ed è «usually one line»), le retirement (git). Tutte «field nobody
re-reads». Nemmeno le altre rosse di CC-7: R-020 (4 run su 7, ma è la forma di `Verification`, e il
posto della decisione è il template — `d8bc79d`), R-024 e R-035 (comportamento di sessione, non una
decisione presa prima della mappa).

Vincolo che cresce con ogni tipo ammesso: la regola di dimensione del log. Il log è riletto a ogni
operazione; a due tipi si sta sotto le venti entry, al terzo serve un tetto complessivo o un fold
anche in scrittura (una sessione riscrive le entry superate della propria sezione, mai delle altre).
