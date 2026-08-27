Leggi @{{RUN_DIR}}/REVIEW.md, che è il report di questo run, e poi ogni altro REVIEW.md sotto evals/roadmap/recipe-app/results/, che sono i run precedenti: servono a sapere quali violazioni ricorrono e quali sono comparse una volta sola.

Poi ricostruisci la storia della skill. I REVIEW.md dicono che cosa ogni run ha sbagliato, mai che cosa era cambiato in skills/roadmap/ fra un run e il successivo, e senza quello una violazione che manca da un run e torna in quello dopo non si distingue dal rumore. Da git:

- **L'ancoraggio delimita, non seleziona.** Non c'è un commit *del* run da cui leggere la skill: serve solo a sapere dove ogni run cade nella storia, perché fra due run i commit possono essere molti e vanno letti tutti. Il `PROMPT.md` del run lo dichiara — riga `Commit` e riga `skills/roadmap` — ed è la fonte da preferire. Un run che non lo dichiara, e i più vecchi non lo fanno, si ancora al commit che ne aggiunge la mappa: `git log --diff-filter=A --format='%h %ad %s' --date=short -- evals/roadmap/recipe-app/results/<run>/.roadmap`. Quello è un'inferenza e non un dato — un run committato dopo una modifica alla skill sposterebbe il confine — quindi dove ci fondi una regressione, dillo.
- **Dentro l'intervallo, tutti.** `git log -p <ancoraggio del run precedente>..<ancoraggio di questo> -- skills/roadmap` dà per intero i cambiamenti che quel run ha messo alla prova. Sono pochi commit e diff corti: leggili tutti, non campionarli. Se due run dichiarano lo stesso tree la skill non è cambiata fra loro, quanti che siano i commit in mezzo, e il secondo non mette alla prova nessun fix nuovo.

Poi, con quelli in mano: @design/roadmap/ROADMAP-GOAL.md, che resta l'autorità sull'intento, e @design/roadmap/CONTEXT.md sul vocabolario; il preambolo di @evals/roadmap/EVALUATION-RULES.md, fino alla prima regola; e skills/roadmap/ per intero — SKILL.md, references/, assets/, scripts/.

## Le tre categorie

Ogni violazione che proponi di chiudere sta in una sola di queste, e quale sia dipende dalla storia dei commit, non dalla gravità.

- **Regressione.** Un commit identificabile la prende di mira, almeno un run dopo di lui la dà verde, e poi ricompare. La causa più probabile è un refactor che ha cancellato il fix senza accorgersene: i commit che spostano, ripuntano o rimuovono sono i primi da guardare.
- **Fix che non ha preso.** Un commit identificabile la prende di mira e nessun run dopo di lui la dà mai verde. Qui il difetto non è solo nel piano, è nell'intervento.
- **Mai risolta.** Nessun commit fra gli ancoraggi l'ha mai presa di mira. Ci sta dentro anche la violazione nuova, vista in un run solo.

Le tre sono disgiunte. Un'assenza in un run intermedio che nessun commit spiega non è una regressione: è varianza fra due generazioni, e la violazione resta *mai risolta*.

Per ogni voce delle prime due categorie cita l'hash e di' come l'hai attribuita — id di violazione nel messaggio del commit, oppure letta dal diff. Un'attribuzione letta dal diff non è debole; è che chi legge deve poterla rifare.

## Quante

- **Regressioni e fix che non hanno preso: tutte.** Sono poche per costruzione — non possono superare i fix tentati — e non vanno ordinate.
- **Mai risolte: tre**, quelle che faresti tu per prime, nell'ordine in cui le faresti. Non un catalogo di tutto il migliorabile. Il criterio è la ricorrenza, non la gravità: il preambolo delle regole dice che un run registra e due dicono che la clausola non sta facendo il suo lavoro, quindi una violazione comparsa in due o più run pesa più di una peggiore vista una volta sola. Una vista una volta sola entra fra le tre solo se dici perché non conviene aspettare il secondo run.
- **Una categoria vuota si chiude con una riga che dice che è vuota.** Non raschiare proposte per riempirla.

## Per ciascuna proposta

- quale file cambia, e che cosa ci scrivi al posto di che cosa. Il fix atterra nell'artefatto che lo possiede — una regola applicata male è un difetto di references/, un campo che nessuno riesce a riempire è un difetto del template. Mai in SKILL.md per default: è così che un router ricresce in un monolite.
- quali violazioni chiude, per id (R-xxx, o H/C del brief) e in quali run le hai viste.
- che cosa rischia di rompere, e quale regola di EVALUATION-RULES.md o quale voce di EVALUATION-BRIEF.md se ne accorgerebbe se si materializzasse.
- come si misura dopo: quale metà di @evals/roadmap/REVIEW-WORKFLOW.md, e se serve un run nuovo.

E, per una regressione o un fix che non ha preso, in più: **perché il fix precedente ha mancato** — cancellato da un refactor, scritto nell'artefatto sbagliato, giusto ma senza forza, o costruito su una diagnosi sbagliata della violazione. Senza questo la proposta è un secondo tentativo alla cieca.

## Vincoli

- ROADMAP-GOAL.md dice che cosa il tool non deve diventare. Nessuna proposta può comprare qualità aggiungendo campi, cerimonia o precisione finta.
- Il fix atterra sempre dentro skills/roadmap/. Una violazione la cui cura cadrebbe fuori — nel brief, nell'oracolo, nei fixture, nel prompt del run — non è materia di questo report: nominala e scartala.
- Non toccare i fixture, l'oracolo, EVALUATION-RULES.md, il brief né alcunché sotto evals/: cambiare la rete per far passare uno scenario è ciò che distrugge una eval.
- Git si legge e basta: nessun commit, nessun checkout, nessun branch, nessuno stash.
- Non implementare niente in questa sessione e non modificare skills/. Produci proposte.
- Nessuna provider call.

Scrivi il report in @{{RUN_DIR}}/IMPROVEMENTS.md, in italiano come il resto della directory; è l'unico file che scrivi. Una sezione per categoria, nell'ordine in cui sono elencate qui: prima quelle dove un commit ha già provato e mancato, poi il resto. Dove segni l'esito di una violazione run per run, scrivi `ok` per verde, `ko` per rosso e `·` per non registrata — mai un segno di spunta o una croce. Se fra le violazioni ricorrenti mai risolte ce n'è una che hai scartato dalle tre, chiudi con una riga che dice quale e perché.
