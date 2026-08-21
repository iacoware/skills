# S10 — In mano a famiglia e amici

← [Register](../roadmap.md#now)

**Outcome:** Il rilascio coerente gira nel suo ambiente di produzione e le persone per cui è stato
fatto lo usano davvero, sulle loro ricette, al costo che l'obiettivo dichiara.

**Requested by:** `references/drawing-the-map.md`, la riga con cui `NOW` finisce quando punta a utenti
finali; il riepilogo costi di `sources/arch-choices.md`.
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

La famiglia e gli amici a cui il prodotto è destinato. Dopo questa riga hanno l'app, ci mettono le
loro ricette e la usano senza che nessuno stia loro accanto.

## Includes

- L'app di produzione su Fly, con il suo database Neon e il suo bucket R2 separati da quelli usati
  fin qui.
- Il client Google OAuth configurato con la callback di produzione.
- Il primo ricettario creato e i link d'invito consegnati.
- Un backup del database, e un ripristino eseguito una volta per davvero.
- La lettura del conto reale dopo una settimana di esercizio, estrapolata al mese e confrontata con
  il bersaglio.

## Verification

Tre persone che non hanno costruito l'app entrano sull'URL di produzione, aggiungono una ricetta
ciascuna — una da link, una incollata, una a mano — la cercano e la ritrovano, senza che nessuno le
aiuti e senza istruzioni scritte a parte l'invito. Il primo tempo di risposta dopo una notte di
silenzio è misurato e riportato. Un ripristino del backup su un database vuoto riporta indietro le
ricette e le foto restano raggiungibili. Il conto della prima settimana, estrapolato al mese, è
riportato contro il bersaglio dei centesimi al mese, voce per voce. Nessuna credenziale
dell'ambiente di prova è presente in produzione, e nessun dato di prova è nel database di produzione.

## Learning target

L'insieme è usabile da persone che non l'hanno costruito, al costo che l'obiettivo dichiara, e quello
che può ancora andare storto è operativo e non funzionale.

## Excludes

- Nessun servizio di analytics e nessun servizio di error reporting oltre i log della piattaforma.
- Nessun dominio personalizzato, nessun impacchettamento come app mobile o PWA.
- Nessun onboarding guidato: l'invito e la home sono tutto quello che le fonti chiedono.

## Open questions

—
