# S14 — Pagine pubbliche indicizzabili e condivisibili

← [Register](../roadmap.md#now)

**Outcome:** La pagina di un ricettario o di una ricetta pubblica è servita in modo che un motore di
ricerca la indicizzi e che il link incollato in una chat mostri di cosa parla; le pagine private non
compaiono da nessuna parte.

**Requested by:** La nuova meta dichiarata dall'autore (chiunque li trova), `sources/arch-choices.md`
(Estrazione contenuto — `schema.org/Recipe`, che qui si scrive invece di leggerlo),
`sources/tech-choices.md` (Next.js App Router).
**Spec:** —
**Tickets:** —
**ADRs:** —

## Audience

Chi non parte da noi: cerca un piatto su un motore di ricerca, o riceve un link in una chat, e arriva
su una ricetta pubblica sapendo già cosa troverà.

## Includes

- Rendering lato server delle pagine pubbliche, con titolo e descrizione presi dalla ricetta e dal
  ricettario.
- Metadati Open Graph per l'anteprima del link, e `schema.org/Recipe` in JSON-LD sulla pagina
  pubblica: la stessa cosa che la pipeline di cattura legge dagli altri.
- URL canonici stabili, che non cambiano quando la ricetta viene corretta.
- Sitemap dei ricettari e delle ricette pubbliche, che segue la visibilità quando cambia.
- `robots` che apre il pubblico e chiude tutto il resto.

## Verification

La pagina pubblica passa il test di structured data del motore senza errori, e compare nella
copertura della console di ricerca entro la finestra dichiarata dalla riga. Il link incollato in una
chat mostra titolo e immagine dell'anteprima. La sitemap non contiene una sola URL privata, e un
crawler che chiede una pagina privata riceve un rifiuto. Una ricetta tolta dal pubblico esce dalla
sitemap e la sua pagina smette di rispondere all'anonimo. L'URL di una ricetta corretta è lo stesso
di prima.

## Learning target

Se "chiunque la trova" regge davvero quando chi cerca non parte dalla nostra home — cioè se una
pagina pubblica è raggiungibile da fuori, o se resta un link che qualcuno deve conoscere.

## Excludes

- Che cosa la pagina pubblica può mostrare, l'immagine estratta in particolare: lo decide `S12`, e
  l'anteprima qui mostra quello che quella riga stabilisce.
- Ottimizzazione dei contenuti, testi per i motori, parole chiave: non richiesti, e non sono un
  esito che qualcuno possa esercitare.
- La cache delle pagine anonime e il costo del traffico dei crawler: sono di `S16`.

## Open questions

- —
