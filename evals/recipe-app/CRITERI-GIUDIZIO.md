# Criteri di giudizio dei piani generati

Appunti informali per confrontare i piani in questa cartella e iterare sulla skill `plan-slices`.
Riferimento di verità: [`IDEAL-SLICES.md`](IDEAL-SLICES.md).

Quando la skill si stabilizza, questi criteri diventano `expectations.json` in questa cartella.
La colonna *Chiave expectations* anticipa la traduzione meccanica; `—` significa che il criterio
per ora resta valutabile solo a occhio.

## Criteri

| # | Criterio | Segnale di fallimento | Chiave expectations |
| --- | --- | --- | --- |
| 1 | Il differenziatore (ricerca semantica cross-lingua) è validato presto | ricerca dopo import, foto, inviti | `now_titles_in_order` |
| 2 | Walking skeleton sottile: deploy in dev senza login, tenancy, CRUD | skeleton che ingloba login o primo CRUD | `now_titles_in_order`, `forbidden_patterns` |
| 3 | Enabler verticale e adiacente al suo successore | pipeline embedding senza la slice di ricerca subito dopo | `now_titles_in_order` |
| 4 | Slice piccole all'inizio, più grandi dopo che i pattern esistono | slice iniziali larghe, o slice grandi solo perché tardive | — |
| 5 | Verticalità reale, non simulata | fixture che iniettano embedding già calcolati invece di attraversare la pipeline | `forbidden_patterns` |
| 6 | Capability indipendenti separate (URL JSON-LD, fallback LLM, foto, testo incollato) | tutte le fonti di import in una sola slice | `now_title_count`, `themes_contain` |
| 7 | Nessuna atomizzazione | inserimento e modifica manuale spezzati senza motivo | `now_title_count` |
| 8 | Orizzonti esclusivi, `LATER` con trigger | scelta cover in NOW, o LATER senza condizione di promozione | `later_contains` |
| 9 | Cross-functional concerns dichiarati una volta e inclusi nelle slice | slice generica di hardening/observability/accessibilità | `forbidden_patterns` |
| 10 | Copertura rispetto a `IDEAL-SLICES.md` | slice mancanti o inventate | `themes_contain` |
| 11 | Forma: bullet e tabelle, sezioni del template rispettate | blocchi di prosa, sezioni mancanti | validazione strutturale |

## Sintesi per piano

Legenda: `ok` / `ko` / `~` (parziale) / vuoto (non ancora valutato).

| # | CC-CON | CC-SENZA | CX-CON | CX-CON-2 | CX-CON-3 | CX-SENZA |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |
| 4 | | | | | | |
| 5 | | | | | | |
| 6 | | | | | | |
| 7 | | | | | | |
| 8 | | | | | | |
| 9 | | | | | | |
| 10 | | | | | | |
| 11 | | | | | | |

## Note per piano

### PLAN-CC-CON

### PLAN-CC-SENZA

### PLAN-CX-CON

### PLAN-CX-CON-2

### PLAN-CX-CON-3

### PLAN-CX-SENZA

## Modifiche alla skill da valutare

Annota qui i comportamenti sbagliati ricorrenti e la modifica alle istruzioni che dovrebbe
correggerli, così l'iterazione successiva parte da evidenza e non da memoria.

| Comportamento osservato | Piani | Modifica ipotizzata a `SKILL.md` | Esito |
| --- | --- | --- | --- |
| | | | |
