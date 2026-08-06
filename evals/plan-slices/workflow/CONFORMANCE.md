# Il contratto di conformità

Il gate del passo 4 del ciclo: perché esiste, che forma impone, cosa fa di una voce non conforme e
cosa non misura. La forma da riempire è `assets/improvement-template.md`; il controllo è
`scripts/consensus/validate_improvement.py`. Il ciclo sta in `../CONSENSUS-WORKFLOW.md`.

Lo legge chi scrive i prompt (Fase 1b-i), chi esegue il ciclo a mano (Fase 2) e chi scrive
l'orchestratore (Fase 5).

## Perché un contratto in prosa non è bastato

Il documento in precedenza affermava che l'output è markdown libero e che quindi il modo di
fallimento del grading system — risposta sintatticamente valida ma non conforme a un contratto
rigido, sei scarti su diciannove — qui non esiste. **L'affermazione è ritirata: la premessa e la
conclusione sono entrambe false.**

Un contratto c'era già, descritto in prosa nel prompt di CON-4 — `472233d:PROMPTS.md`
§ *CREATE IMPROVEMENTS*, rimosso dal working tree il 2026-08-07 quando `prompts/improve.prompt.md`
lo ha sostituito: titolo, `## Inputs`, una sezione per miglioramento con otto campi obbligatori e
`## Verifica finale`. Nell'unica esecuzione mai fatta:

| | `CC` | `CX` |
|---|---|---|
| Titolo richiesto | no | no |
| `## Inputs` | assente | assente |
| Sezione per miglioramento | sì, 10 | **nessuna**: 8 bullet |
| Otto campi obbligatori | parziale | **zero** |
| `## Verifica finale` | assente | assente |

La disparità 246 contro 10 righe non è differenza di qualità fra modelli: è non-conformità, grave su
un lato. E la differenza con il grading system è a sfavore del ciclo: là la non-conformità produceva
uno **scarto visibile**; qui ha prodotto un artefatto **accettato**, propagato in `review` e da lì in
sette righe di registro. Il modo di fallimento non è stato eliminato, è stato reso silenzioso.

**Un contratto descritto in prosa dentro un prompt è ciò che entrambi i lati hanno ignorato.** Il
rimedio non è ripetere la prosa: è la stessa architettura che lo skill usa già e che funziona —
`assets/plan-template.md` dà la forma, `scripts/validate_plan.py` la controlla, e le righe del registro
si dividono in `validator` e `lettura` lungo quella cucitura. `CC` rispetta il template dei piani da
cinque cicli.

Quindi: **`assets/improvement-template.md` + `scripts/consensus/validate_improvement.py`.**

## La specificità è una forma, non un giudizio

Un gate che conta i campi non si accorge del difetto di CON-4. Otto sezioni con otto campi ciascuna,
tutte scritte come *«rendere obbligatorio un audit interno split/merge per ogni coppia di
capability»*, lo passerebbero. La genericità sta nel contenuto dei campi.

Il template la esclude **per forma**:

1. **`Evidenza — candidato A`** e **`Evidenza — candidato B`** sono due celle separate. O contengono
   un riferimento localizzabile — `PLAN-…-CON-N.md:NN`, oppure `slice N` più il nome del campo — o la
   dichiarazione esplicita che quel candidato non manifesta il difetto. Un bullet generico non riempie
   due celle di evidenza.
2. **`Regola esistente che non ha impedito il difetto`** nomina una clausola di `SKILL.md` con la sua
   sezione, oppure dichiara `nessuna`.
3. **`Test binario`** è scritto nella grammatica delle righe del registro — `Nessuna slice NOW…`,
   `Ogni voce LATER…` — cioè decidibile su un piano generato.

Il punto 3 elimina una cucitura mai dichiarata: oggi qualcuno traduce prosa in affermazione
falsificabile, a mano, al momento di applicare. Con il template la riga la scrive il modello che ha
trovato il difetto, e l'umano accetta o rifiuta.

**Non servono soglie.** Misurare la specificità con una quota e una soglia era ragionamento
confermazionista dentro un documento costruito su `non smentita ×k`. Senza soglia il criterio è
descrittivo: quante voci sopravvivono al gate per lato. `CX` a 0 e `CC` a 9 falsifica l'ipotesi senza
che nessuno si sia impegnato su un numero arbitrario; 7 e 9 non conferma niente — è un ciclo `×1`.

## Cosa fa il gate quando una voce non è conforme

**Scarto per voce, un solo tentativo.** La voce cade, il resto del documento resta. Ogni scarto è
registrato nel report con il campo mancante e il motivo.

Perché un tentativo e non due: una voce scartata non è persa. `improve` rigenera una lista fresca ogni
ciclo, quindi il difetto ricompare al giro dopo a costo marginale zero, mentre la rigenerazione paga
subito, può non convergere, e mette nel record un artefatto ottenuto con più tentativi degli altri.
Vale la regola generale — *«un filtro che manca qualcosa costa meno di uno che applica qualcosa di
falso»*.

Due precisazioni che tengono pulito il dato:

- **Un errore di trasporto o una risposta vuota non è un tentativo di conformità.** Si ritenta la
  *chiamata*. Si rigenera il *documento* mai. Sono due contatori diversi e solo il secondo dice
  qualcosa sull'ipotesi.
- **Un lato che produce zero voci conformi non blocca il ciclo.** `review` gira lo stesso, con l'esito
  ovvio: nessuna intersezione possibile, quindi nessuna applicazione automatica. «`CX` ha prodotto 0
  voci conformi in CON-6» è un dato del ciclo, non un guasto da riparare; se era transitorio, CON-7 lo
  mostra.

Il log degli scarti è anche la diagnosi quando un lato collassa: scarti concentrati **tutti sullo
stesso campo** accusano il template, e si corregge quel campo. Scarti **sparsi** accusano il modello,
e l'ipotesi prende una smentita `×1`.

Lo scarto registrato è il rimedio al degrado silenzioso, che è il difetto storico: un warning su un
artefatto che nessuno ha guardato per due cicli è esattamente ciò che è già successo.

**Codice di uscita.** Una voce scartata **non è un errore**. Lo script esce con `1` solo quando il
documento non è leggibile come insieme di voci; un lato a zero voci conformi esce con `0`, coerente
con «un lato a zero voci conformi non blocca il ciclo». E il gate legge le voci **anche fuori da
`## Entries`**: un documento che le numera altrove deve comunque un log degli scarti per voce, perché
«nessun `## Entries`» e «nessuna voce» sono due fatti diversi e collassarli avrebbe reso invisibile
proprio l'asimmetria di CON-4.

## Cosa il gate ha misurato su CON-4

La tabella qui sopra è lettura umana del 2026-08-06. Lo stesso dato ottenuto dallo strumento, quando
la Fase 1a lo ha consegnato:

| | voci lette | conformi |
|---|---|---|
| `PLAN-CC-CON-4.IMPROVEMENT.md` | **10** | **0**, ognuna con l'elenco dei campi mancanti |
| `PLAN-CX-CON-4.IMPROVEMENT.md` | **0** | — non ne contiene nessuna |

L'asimmetria attesa è riprodotta da uno strumento invece che da una lettura. Precisazione sul senso
di «parzialmente conformi» nella riga *Otto campi obbligatori*: **nessuna** voce di `CC` supera il
contratto, perché il documento di CON-4 non ha nessuno dei campi nuovi. La conformità parziale sta
nell'essere leggibile **come voce**, cioè nel produrre uno scarto diagnosticabile invece di sparire.

## Cosa il gate non misura

Tre residui, tutti sulla stessa spaccatura `validator`/`lettura` lungo cui si dividono le righe del
registro. Sono la parte che resta al veto umano, e sono debito dichiarato, non svista:

- il validator verifica **che** un riferimento esista, non che **sostenga** l'affermazione;
- verifica che una fusione sia scritta nella grammatica delle righe, non che resti **decidibile in
  una lettura**;
- verifica che una riformulazione scartata sia stata scritta, non che la ragione sia **ammissibile**.
  Il divieto — «la clausola è coperta da una riga del registro» non è una ragione — vive in
  `assets/improvement-template.md` e sta al veto. La forma lo rende costoso da violare: il campo
  chiede la riformulazione *effettivamente scritta*, e una dichiarazione di copertura non riempie
  quella cella.
