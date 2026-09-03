# S8 — Modifica di una ricetta e inserimento a mano

← [Register](../roadmap.md#now)

**Outcome:** Si corregge una ricetta estratta male dal suo dettaglio, e con lo stesso form a campi
vuoti si scrive da zero una ricetta che non sta su nessun sito; in entrambi i casi la ricerca la
ritrova col testo nuovo.
**Requested by:** `goal.md` § Aggiunta ricetta ("stesso form per edit e inserimento manuale", "la
correzione è sempre disponibile dopo"); `concepts.md` § Pipeline di estrazione (ingresso manuale) e
nota sull'`embedding` rigenerato a ogni edit.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi usa il ricettario. Dopo questa riga può rimediare a un'estrazione imperfetta invece di
conviverci, ed è quello che rende accettabile il salvataggio senza review.

## Includes

- Un solo form, usato per la modifica di una ricetta esistente e per l'inserimento con campi vuoti:
  nome, ingredienti e preparazione come testo libero, senza parsing di quantità e unità.
- Campi opzionali marcati come opzionali; nessun campo obbligatorio oltre a quelli che rendono la
  ricetta una ricetta.
- Rigenerazione dell'`embedding` insieme al salvataggio, come già fa la pipeline di add, così che
  ricerca e testo non divergano.
- Il salvataggio passa dal resolver del ricettario corrente: si modifica solo dentro un ricettario di
  cui si è membri.

## Verification

- Correggendo il nome e gli ingredienti di una ricetta estratta male, il dettaglio mostra il testo
  nuovo e una ricerca su una parola presente solo nel testo nuovo la trova.
- Una ricetta scritta a mano, mai passata da un URL, compare in elenco, si apre in dettaglio e viene
  trovata dalla ricerca semantica come una qualsiasi altra.
- Una ricerca su una parola che c'era solo nel testo vecchio non la pesca più: l'indice derivato è
  stato rigenerato, non lasciato indietro.
- Il tentativo di modificare una ricetta di un ricettario di cui non si è membri viene rifiutato.
- Svuotando un campo opzionale la ricetta si salva lo stesso.

## Learning target

Se un solo form regge davvero i due usi che le fonti gli danno — correggere e creare — o se
l'inserimento a mano chiede qualcosa che la correzione non chiede.

## Excludes

- Le foto nel form: sono di S9, che possiede il caricamento e la copertina.
- Cancellazione di una ricetta: nessuna fonte la chiede.
- Cronologia delle modifiche e ripristino: nessuna fonte li chiede.
- Un passo di review dentro il flusso di add: escluso per decisione delle fonti; la correzione resta
  un'azione separata, disponibile dopo.

## Open questions

- Nessuna.
