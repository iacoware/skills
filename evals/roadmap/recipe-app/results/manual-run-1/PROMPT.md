# Prompt — `manual-run-1` (parziale)

Questo file non è il record che `run_cycle.ts` scrive prima di inviare: di quel run non c'è né
transcript né record, e quasi tutto quel che gli altri `PROMPT.md` dichiarano qui è perduto. Tiene
una cosa sola — **l'ancoraggio nella storia della skill** — perché è l'unica che ogni ciclo di
miglioramento deve ricavarsi da capo, e ricavarsela da capo significa rifare ogni volta la stessa
inferenza, con lo stesso margine di errore e senza il margine scritto da nessuna parte.

| | |
|---|---|
| Harness | Claude Code CLI, sessione interattiva guidata da una persona |
| Modello | non registrato |
| Effort | non registrato |
| Session id | non registrato — nessun `TRANSCRIPT.jsonl` |
| Commit | `dcf783d` — *test(roadmap): keep the manual run of the drawing branch* — **inferito** |
| `skills/roadmap` | tree `ed75429` — **inferito** |
| Testo inviato | il prompt di disegno che allora stava in [`../../../PROMPTS.md`](../../../PROMPTS.md) e oggi è [`../../prompts/run.prompt.md`](../../prompts/run.prompt.md); nessuna copia di quella versione sopravvive |

## Perché l'ancoraggio è inferito, e quanto regge

**L'inferenza a buon mercato**: il commit che aggiunge la mappa,
`git log --diff-filter=A -- evals/roadmap/recipe-app/results/manual-run-1/.roadmap` → `dcf783d`, e
`skills/roadmap` a quel commit è `ed75429`. Non è un dato preso al momento dell'invio: è la data in
cui il run è stato committato, non la versione su cui ha girato.

**Un indizio in più, che l'inferenza nuda non ha.** La mappa *come committata* legge `Themes`, `NOW`,
`LATER`, `OUT-OF-SCOPE`, `Ordering criteria`, `Assumptions`, `Open questions`,
`Cross-functional concerns` — esattamente il template di `ed75429`. La versione immediatamente
precedente, `981ed3a` (commit `c0656da`), mette `Ordering criteria` per primo e porta `Themes`,
`Assumptions`, `Open questions` e `Cross-functional concerns` *sopra* `NOW`. Le due sono
distinguibili a occhio, e la mappa combacia con una sola. Va letta al commit, non nel working tree:
`d805196` ha tolto `Ordering criteria` dal formato e, con esso, da questa mappa.

    git show dcf783d:evals/roadmap/recipe-app/results/manual-run-1/.roadmap/roadmap.md | grep '^## '
    git show e3df104:skills/roadmap/assets/roadmap-template.md | grep '^## '   # ed75429
    git show c0656da:skills/roadmap/assets/roadmap-template.md | grep '^## '   # 981ed3a

**Che cosa lo falsificherebbe, ed è il motivo per cui resta inferito.** `c0656da` e `e3df104` sono
stati committati alle 18:27 del 2026-08-21, **un minuto prima** di `dcf783d` alle 18:28, e `e3df104`
*è* il cambio di layout: il suo messaggio dice che migra a mano l'oracolo, i fixture e i result tree
allora tenuti. La mappa di questo run in quel momento non era ancora tracciata, quindi una sua
migrazione a mano nello stesso passaggio non lascerebbe traccia in nessun diff. Se è andata così, la
versione che ha girato è `981ed3a` o una precedente, e l'indizio del layout non vale niente.

**Che cosa ci pende.** Solo il confine con `ROADMAP-CC-2`, e nel caso normale non cambia nulla:
`dcf783d..666566d` ed `e3df104..666566d` contengono gli stessi commit di `skills/roadmap` —
`18968aa`, `524e180`, `676b580`, `666566d` — quindi scegliere fra il commit che aggiunge il run e il
commit che introduce il tree è indifferente. Cambia solo nello scenario di falsificazione: allora
`c0656da` (*write a first map instead of proposing it*) ed `e3df104` entrano nell'intervallo, e
diventano due fix che `ROADMAP-CC-2` mette alla prova invece che due commit su cui `manual-run-1` ha
girato.

**Come leggerlo.** Le due righe della tabella restano *inferite* e vanno citate come tali: dove una
regressione o un fix che non ha preso si regge su questo confine, va detto — è la stessa clausola che
[`../../prompts/improve.prompt.md`](../../prompts/improve.prompt.md) impone a chi l'ancoraggio se lo
deve inferire. Quel che questo file toglie è il lavoro, non il dubbio.
