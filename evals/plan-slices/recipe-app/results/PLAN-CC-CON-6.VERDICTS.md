# Verdicts — cycle CON-6

## Inputs

- **Candidate A:** `CANDIDATE-A.md`
- **Candidate B:** `CANDIDATE-B.md`
- **Rows verified:** 17

## R-001

- **Claim:** The plan places identity after the differentiator.
- **Candidate A:** `falsified`
  - **Citation:** `CANDIDATE-A.md:78`
  - **What it shows:** Slice 2 is «Accesso al primo ricettario privato *(Theme: A)*», with `Includes` «Login e sessione con Auth.js v5 e Google OAuth». Identity is therefore delivered at position 2, while the differentiator — multilingual semantic search, per `EVALUATION-BRIEF.md` § Hard constraints — is validated at slice 3 (`Pipeline embedding multilingue osservabile`) and slice 4 (`Ricerca semantica nel ricettario corrente`, `CANDIDATE-A.md:121`). Identity precedes the differentiator instead of following it.
- **Candidate B:** `holds`
  - **Citation:** `CANDIDATE-B.md:231`
  - **What it shows:** Slice 9 is «Accesso con Google *(Theme: G)*», carrying Auth.js/Google OAuth and the substitution of the configured scope with the authenticated user's cookbooks. The differentiator is validated at slice 3 (`CANDIDATE-B.md:98`) and slice 4 (`CANDIDATE-B.md:121`), both before it; `Ordering criteria` (`CANDIDATE-B.md:11`) states the ordering explicitly («Identità dopo cattura e ricerca»).
- **Watch for:** `no note on this row`

## R-002

- **Claim:** Every choice the plan declares open names the `NOW` slices it blocks, in whatever section it declares it.
- **Candidate A:** `holds`
  - **Citation:** `Open questions; entry «Quale provider/modello LLM economico soddisfa qualità, schema, latenza e costo?»`
  - **What it shows:** All three entries of `Open questions` name blocked slices: «Blocca le slice 1–12», «Blocca le slice 3–12», and the cited one «Blocca le slice 7, 8 e 12». The cited entry is the narrowest of the three and still names its slices, so no open choice is declared without its blocked `NOW` slices.
- **Candidate B:** `holds`
  - **Citation:** `Open questions; entry «Provider Postgres e driver»`
  - **What it shows:** The entry ends «Blocca la slice 1 e ogni verifica di connessione successiva» — a named `NOW` slice. The other three entries do the same («Blocca le slice 3 e 4»; «Blocca la slice 6 e il calcolo del costo per ricetta»; «Blocca la slice 4»). The cited one is the closest to failing, because it extends beyond a slice list, yet it still names slice 1.
- **Watch for:** `no note on this row`

## R-003

- **Claim:** No `NOW` slice depends on an external choice — provider, model, service, or adapter — that is not made by a citable source, or made by the plan among the alternatives the brief declares acceptable, or declared open together with the slice it blocks, in whatever section it declares it; a qualifying adjective — `cheap`, `multilingual`, `managed` — does not count as a choice.
- **Candidate A:** `holds`
  - **Citation:** `slice 1 Includes`
  - **What it shows:** The bullet «Postgres+pgvector sul provider e driver scelti» leaves the provider and driver unnamed — the point where an undeclared dependency would appear. It is covered by `Open questions` entry «Neon o Supabase, e quale driver/pooling TCP? Blocca le slice 1–12», which declares the choice open together with the slices it blocks. The same pattern covers the embedding model (slice 3 «API/modello multilingue selezionati», open question blocking slices 3–12) and the extraction model (slice 7 «provider/modello economico selezionato», open question blocking slices 7, 8 and 12). The remaining externals — Fly.io, Cloudflare R2, Auth.js + Google OAuth, Drizzle — are named by `sources/arch-choices.md` and `sources/tech-choices.md`.
- **Candidate B:** `holds`
  - **Citation:** `slice 6 Includes`
  - **What it shows:** The bullet «Estrattore LLM con modello cheap selezionato (decisione aperta)» uses the qualifying adjective `cheap`, which the claim excludes as a choice — but it annotates it «(decisione aperta)» and `Open questions` entry «Modello LLM per l'estrazione di fallback» names the blocked slice («Blocca la slice 6»). Slice 1 («provider Postgres selezionato (decisione aperta)») and slices 3–4 (embedding model, query-embedding path) are covered the same way; slice 3 closes the embedding-model choice on evidence (`CANDIDATE-B.md:119`), so slices 5 and 7 do not depend on an open one. R2, Fly.io and Auth.js/Google are source-decided.
- **Watch for:** `no note on this row`

## R-004

- **Claim:** No `NOW` slice delivers a behaviour the sources do not request.
- **Candidate A:** `holds`
  - **Citation:** `slice 8 Includes`
  - **What it shows:** The bullet «Il fallimento di un URL propone il canale copia-incolla senza duplicare ricette o pipeline» is the closest thing to an unrequested behaviour, since no source describes a UI that offers the paste channel. `sources/goal.md` § Visione does designate copy-paste as the fallback «usato anche quando il link non è leggibile (paywall, siti JS-heavy)», so the behaviour is the requested fallback rather than a new one. Every other `NOW` slice maps onto a requested capability: home list, three add entry points, semantic search scoped to the cookbook, edit form, multiple photos with cover, invitations with peer members.
- **Candidate B:** `holds`
  - **Citation:** `slice 5 Includes`
  - **What it shows:** The bullet «Generazione dell'embedding al salvataggio con retry automatico: se fallisce, la ricetta resta salvata, marcata come non indicizzata e ri-indicizzabile» introduces a non-indexed state the sources never name — the closest point to a violation. It is a recovery mechanism for a derived index that `sources/concepts.md` § Recipe already declares derived and regenerable, not a product behaviour added to the MVP; the save-without-mandatory-review rule it protects is requested by `sources/goal.md` § Aggiunta ricetta. Photo download from `og:image`/JSON-LD (slice 8) is explicitly requested by `sources/arch-choices.md` § Object storage foto.
- **Watch for:** `no note on this row`

## R-005

- **Claim:** If a `NOW` slice names a failure mode in its own `Verification` and another `NOW` slice is its remedy, no slice of a different theme is placed between the two.
- **Candidate A:** `holds`
  - **Citation:** `slice 6 Verification`
  - **What it shows:** Slice 6 (Theme D) names «Paywall, URL ostile, redirect anomalo, timeout…»; the remedy for paywall is slice 8, «Recupero tramite copia-incolla» (Theme E). The only slice between them is slice 7, «Fallback LLM automatico per URL *(Theme: D)*» — the same theme as the slice that names the failure, so no slice of a different theme intervenes. Slice 3's failure modes (retry, timeout, invalid output) are remedied inside slice 3 itself.
- **Candidate B:** `holds`
  - **Citation:** `slice 5 Verification`
  - **What it shows:** Slice 5 names «Paywall, timeout e assenza di JSON-LD producono tre messaggi distinti sul passo fallito»; slice 6 («Copia-incolla ed estrazione LLM», plus the automatic LLM fallback on the URL path) is the remedy and is adjacent, with nothing between. `Ordering criteria` (`CANDIDATE-B.md:9`) states the placement rule. The other failure named in slice 5 — a failed embedding — is remedied within slice 5 by the retry bullet, so no intervening slice is involved.
- **Watch for:** `no note on this row`

## R-006

- **Claim:** A pipeline or adapter shared by several paths is opened in the `Includes` of a single `NOW` slice.
- **Candidate A:** `holds`
  - **Citation:** `slice 7 Includes`
  - **What it shows:** The LLM extraction adapter is opened once, here: «In assenza di JSON-LD, contenuto pulito passa al provider/modello economico selezionato con output strutturato validato». Slice 8 treats it as already existing («adapter LLM stabiliti»), so it is not opened twice. The embedding pipeline is likewise opened once, in slice 3 `Includes`; the R2 photo path is first opened in slice 6 `Includes` and extended, not re-opened, by slice 10.
- **Candidate B:** `holds`
  - **Citation:** `slice 6 Includes`
  - **What it shows:** «Fallback automatico a LLM sul path URL quando il JSON-LD manca: l'estrattore LLM ha un unico proprietario» declares single ownership at the point of opening, and the paste entry in the same slice «riusa lo stesso motore e lo stesso schema di output dell'aggiunta da link». Photos and object storage are opened in slice 8 for every add path, and `Ordering criteria` (`CANDIDATE-B.md:10`) names both owners.
- **Watch for:** `no note on this row`

## R-007

- **Claim:** No `Enabler` slice validates uncertainties across more than one subsystem: its `Verification` cannot fail for causes that, in the brief's `Material uncertainties`, belong to different `Subsystem`s. Several entries of the same subsystem are one uncertainty, even when the answer invalidates the choice being verified.
- **Candidate A:** `holds`
  - **Citation:** `slice 1 Verification`
  - **What it shows:** Slice 1 (`Enabler: delivery`) can fail for deploy/rollback, migration from an empty database, and the post-suspend round trip with cold-start latency — U1 and U2, both `Delivery infrastructure`, one subsystem. Slice 3 (`Enabler: ricerca semantica`) can fail only for cross-language ranking, embedding-provider errors and cost — U3, `Semantic engine`. Slice 0 exercises CI only and touches no listed uncertainty. No enabler mixes subsystems.
- **Candidate B:** `holds`
  - **Citation:** `slice 1 Verification`
  - **What it shows:** Slice 1 (`Enabler: delivery`) fails on the real-driver round trip, the applied migration and the first access after scale-to-zero — U1 and U2, both `Delivery infrastructure`. Slice 3 (`Enabler: ricerca semantica`) fails on cross-language recall and indexing cost — U3 alone; it closes the embedding-model choice, which is the same subsystem. Slice 0 covers CI only. No enabler spans two subsystems.
- **Watch for:** `no note on this row`

## R-008

- **Claim:** Every theme's `First validation` points to a slice whose `Outcome` covers the theme's entire desired outcome.
- **Candidate A:** `holds`
  - **Citation:** `slice 2 Outcome`
  - **What it shows:** This is the weakest pairing and the point where the violation would appear. Theme A wants «Una persona accede e opera solo nel ricettario corrente»; slice 2's `Outcome` is «Una persona autenticata dispone di uno scope privato persistente per le ricette future» — access plus the scope restriction, the two parts of the desired outcome, with «per le ricette future» pointing at content that later slices add rather than at an uncovered part of the theme. The remaining seven pairings restate the theme almost verbatim (e.g. Theme B «query cross-lingua» → slice 4 `Outcome` «per significato, indipendentemente dalla lingua e senza uscire dal proprio ricettario»).
- **Candidate B:** `holds`
  - **Citation:** `slice 7 Outcome`
  - **What it shows:** The closest pairing to failing: Theme E wants «Si inserisce a mano o si corregge una ricetta con lo stesso form», and slice 7's `Outcome` — «corregge un'estrazione imperfetta o inserisce da zero una ricetta che già conosce» — covers both halves, with the shared form stated in the same slice's `Includes` («Un solo form per inserimento manuale (campi vuoti) ed edit»). Themes F, G and H have outcomes copied word for word into the target slice's `Outcome`.
- **Watch for:** `no note on this row`

## R-009

- **Claim:** No `Outcome` of a `NOW` slice preceding identity promises a real user: every slice that precedes identity and delivers a behaviour names its own audience, developer or tester on the declared non-public environment.
- **Candidate A:** `holds`
  - **Citation:** `slice 1 Outcome`
  - **What it shows:** Identity lands at slice 2, so only slices 0 and 1 precede it, and both name their audience: «Gli sviluppatori osservano il runtime minimo deciso…» (slice 1) and «Gli sviluppatori hanno una base minima, ripetibile e revisionabile…» (slice 0). Neither delivers user-facing behaviour, and no `Outcome` before identity promises a real user.
- **Candidate B:** `falsified`
  - **Citation:** `CANDIDATE-B.md:229`
  - **What it shows:** Slice 8 («Foto e cover della ricetta», Theme F) precedes identity at slice 9 and delivers behaviour — multiple upload, cover selection, photo re-hosting — yet its `Outcome` is «Le ricette sono riconoscibili a colpo d'occhio e le loro foto non si rompono nel tempo», which names no audience at all, developer or tester, and states the promise in the terms of whoever looks at the recipes. Every other pre-identity behavioural slice names one («Chi testa l'app…», slices 2, 4, 5, 6, 7), and `Ordering criteria` (`CANDIDATE-B.md:11`) asserts «l'audience dichiarata di ogni slice precedente è sviluppatore/tester sull'ambiente non pubblico», which slice 8 does not carry out.
- **Watch for:** `no note on this row`

## R-010

- **Claim:** No `Includes` or `Verification` bullet asserts in non-conditional form one side of an unresolved choice. Unresolved covers a conflict between the sources — those listed under `Known conflicts` in the brief, plus those demonstrable by citing two sources in disagreement — and, in the slices that choice blocks, any other choice the plan does not resolve by citing a selecting source. Declaring the choice under `Open questions` or assigning it a spike does not resolve it.
- **Candidate A:** `holds`
  - **Citation:** `slice 4 Includes`
  - **What it shows:** The query-embedding conflict (`EVALUATION-BRIEF.md` § Known conflicts, second entry) is the place where an assertion would appear, and the bullet keeps it conditional: «Campo di ricerca che genera il vettore query secondo la decisione aperta e interroga solo il ricettario corrente» — no per-query call, cache or precomputation is asserted. The blocked slices name the still-open externals by role rather than by side: «sul provider e driver scelti» (slice 1), «API/modello multilingue selezionati» (slice 3), «provider/modello economico selezionato» (slice 7). Slice 5 states the manual path without asserting either side of the manual-input/extraction conflict — it mentions the shared form and the embedding pipeline, never the extraction engine.
- **Candidate B:** `holds`
  - **Citation:** `slice 4 Includes`
  - **What it shows:** «Path di embedding della query secondo la decisione aperta, con timeout e messaggio esplicito se quella modalità dipende da un servizio esterno indisponibile» is doubly conditional — the path and the external dependency are both left open — and slice 4's `Verification` follows suit («Latenza della ricerca misurata sul path effettivamente scelto»). Slice 7 states the manual entry as a shared empty form without asserting whether it traverses or skips the extraction engine, so the first `Known conflicts` entry is not taken either.
- **Watch for:** The opposite failure — deferring so much that nothing verifiable is published — is not observed in either plan. Candidate A's slice 4 `Verification` still commits to «Un membro cerca in italiano e trova una ricetta inglese pertinente nel proprio ricettario», and Candidate B's slice 4 `Verification` to «Query come "cena leggera" e "pomodoro" restituiscono ricette pertinenti, incluse quelle scritte in inglese»; in both plans the deferral is confined to the mechanism, while the observable result stays asserted.

## R-011

- **Claim:** Every row of the `Themes` table has its `First validation` resolve to a `NOW` slice not annotated `*(Enabler: …)*`, unless its `Desired outcome` cell carries the `*(Developer outcome)*` marker.
- **Candidate A:** `holds`
  - **Citation:** `Themes, row «B. Ricerca semantica»`
  - **What it shows:** This is the row at risk, because the semantic engine has its own enabler at slice 3 («*(Enabler: ricerca semantica)*»). Its `First validation` is 4, the product slice «Ricerca semantica nel ricettario corrente *(Theme: B)*», not the enabler. The other seven rows point to 2, 5, 7, 8, 9, 10 and 11 — none of them among the enablers 0, 1 and 3.
- **Candidate B:** `holds`
  - **Citation:** `Themes, row «B. Ricerca semantica cross-lingua»`
  - **What it shows:** Same exposure, same result: `First validation` is 4 («Ricerca semantica nel ricettario corrente *(Theme: B)*»), while the semantic enabler sits at slice 3. The remaining rows point to 2, 5, 6, 7, 8, 9 and 10; enablers 0, 1 and 3 are pointed to by no theme.
- **Watch for:** The marker used as an escape hatch is not observed: neither `Themes` table carries a `*(Developer outcome)*` marker in any `Desired outcome` cell, and neither plan needed one, since no `First validation` resolves to an enabler.

## R-012

- **Claim:** The plan declares under `Cross-functional concerns` the single seam from which the current scope resolves.
- **Candidate A:** `holds`
  - **Citation:** `Cross-functional concerns`
  - **What it shows:** The `Authorization` entry declares «Ogni lettura e modifica usa membership e `cookbookId` risolto centralmente; nessuna query ricetta o ricerca è globale» — a single central resolution point for the current scope, stated in the required section. It is the thinnest admissible form, since the word «resolver» appears only in `Ordering criteria` and slice 2 `Includes`, but the central seam itself is declared where the claim requires it.
- **Candidate B:** `holds`
  - **Citation:** `Cross-functional concerns`
  - **What it shows:** The `Authorization` entry declares «Ogni lettura e scrittura passa da un unico risolutore del ricettario corrente; alla slice 9 quel risolutore è il seam in cui lo scope configurato viene sostituito dai ricettari dell'utente autenticato» — the single seam is named, and the slice at which it switches is named with it.
- **Watch for:** `no note on this row`

## R-013

- **Claim:** Every `LATER` entry states a `Promotion trigger`.
- **Candidate A:** `holds`
  - **Citation:** `LATER, entry «Passkeys»`
  - **What it shows:** All six entries carry a `Promotion trigger`; the cited one is the only entry whose trigger is not tied to a slice number, and it still states one: «Auth.js offre supporto maturo e gli utenti richiedono accesso ricorrente senza Google». The other five name the slice whose evidence would promote them (slices 4 and 12, 12, 11, 11, and observed collaborations).
- **Candidate B:** `holds`
  - **Citation:** `LATER, entry «Macchina Fly sempre calda (`min_machines_running=1`)»`
  - **What it shows:** All five entries carry a `Promotion trigger`; the cited one states «il cold start misurato nelle slice 1 e 11 risulta fastidioso all'uso», tying promotion to the measurement those slices produce. The other four do the same against slices 4–7 and 10.
- **Watch for:** `no note on this row`

## R-014

- **Claim:** Every `OUT-OF-SCOPE` entry states an exclusion rationale.
- **Candidate A:** `holds`
  - **Citation:** `OUT-OF-SCOPE`
  - **What it shows:** Each of the six entries appends a reason after the em dash — e.g. «Deduplicazione ricette — Le fonti consentono esplicitamente duplicati nello stesso ricettario» and «IaC Terraform/SST nell'MVP — Sovradimensionato rispetto a `fly.toml` e CLI». The bare-restatement risk («Le fonti consentono…») still gives the ground for exclusion rather than repeating the item.
- **Candidate B:** `holds`
  - **Citation:** `OUT-OF-SCOPE`
  - **What it shows:** Each of the eight entries carries a rationale, including the compound one that gives a distinct reason per alternative: «Hosting alternativi (Vercel, Cloudflare Workers + OpenNext, AWS Fargate) — rispettivamente costi crescenti oltre l'Hobby, vincoli del modello fat-worker, assenza di scale-to-zero».
- **Watch for:** `no note on this row`

## R-015

- **Claim:** A `NOW` slice that reuses a pipeline or adapter opened by an earlier slice declares it as reuse.
- **Candidate A:** `falsified`
  - **Citation:** `CANDIDATE-A.md:171`
  - **What it shows:** Slice 6 `Includes` states «Titolo, ingredienti, preparazione, metadati disponibili ed embedding sono salvati subito», using the embedding pipeline opened in slice 3 without declaring the reuse — while slice 5 does declare it («Creazione ed edit rigenerano l'embedding mediante la pipeline stabilita», `CANDIDATE-A.md:153`) and slice 8 declares the extraction reuse («riusa pulizia, schema validato e adapter LLM stabiliti»). The same omission recurs at slice 10 `Includes` («Aggiunta e rimozione di più foto per ricetta su Cloudflare R2»), which reuses the R2 path opened in slice 6 `Includes` with no reuse statement.
- **Candidate B:** `falsified`
  - **Citation:** `CANDIDATE-B.md:151`
  - **What it shows:** Slice 5 `Includes` states «Generazione dell'embedding al salvataggio con retry automatico…», consuming the embedding generation opened in slice 3 `Includes` («generazione degli embedding del corpus seedato tramite API cloud reale») without declaring it as reuse. Slice 7 repeats the omission («Rigenerazione dell'embedding a ogni salvataggio», `CANDIDATE-B.md:197`). The plan does declare reuse elsewhere — slice 6 «riusa lo stesso motore e lo stesso schema di output dell'aggiunta da link» and slice 8 «dal form condiviso» — so the embedding pipeline is the uncovered case.
- **Watch for:** `no note on this row`

## R-016

- **Claim:** The `NOW` slice that opens a pipeline or adapter shared by several paths follows every `NOW` slice that feeds it input, except when it validates controlled inputs that traverse the production computation and the scenario's brief admits early validation.
- **Candidate A:** `falsified`
  - **Citation:** `CANDIDATE-A.md:194`
  - **What it shows:** Slice 7 `Includes` opens the LLM extraction adapter («contenuto pulito passa al provider/modello economico selezionato con output strutturato validato»), but one of the paths that feeds it input comes later: slice 8 `Includes` («Input testo riusa pulizia, schema validato e adapter LLM stabiliti, saltando fetch e JSON-LD», `CANDIDATE-A.md:218`) is the paste entry point. The opener therefore does not follow every `NOW` slice that feeds it, and the exception does not apply — slice 7 validates real pages, not controlled inputs. The embedding pipeline at slice 3 is a different matter and does fall under the exception (see the watch-for note below).
- **Candidate B:** `holds`
  - **Citation:** `slice 6 Includes`
  - **What it shows:** The LLM extractor is opened at slice 6, after its two feeding paths are in place: the URL path at slice 5 and the paste entry inside slice 6 itself («Ingresso "incolla testo" che, dopo pulizia del contenuto, riusa lo stesso motore…»). The photo/R2 pipeline is opened at slice 8, after the add-from-link path (slice 5) and the shared form (slice 7) that feed it. `Ordering criteria` (`CANDIDATE-B.md:10`) states the rule the slices follow.
- **Watch for:** The early-opening exception is exercised by both plans for the embedding pipeline, and in both it resolves to `EVALUATION-BRIEF.md` § Accepted alternatives — «Controlled inputs may validate extraction, embeddings, or search before their final user entry point when they traverse the production computation» — not to any statement of the skill's own. Candidate A's slice 3 `Includes` reads «Fixture normalizzate attraversano API/modello multilingue selezionati, Drizzle, Postgres e pgvector reali», and Candidate B's slice 3 `Includes` «generazione degli embedding del corpus seedato tramite API cloud reale» over a controlled seed introduced at slice 2: controlled inputs, production computation, in both cases.

## R-017

- **Claim:** If more than two `NOW` slices deliver behaviour to an end user before identity, `Ordering criteria` justifies the residual deferral once, naming the evidence that requires it.
- **Candidate A:** `holds`
  - **Citation:** `slice 1 Outcome`
  - **What it shows:** The condition never arises. Identity is at slice 2, and the only slices before it are 0 and 1, both `*(Enabler: delivery)*` with outcomes addressed to developers («Gli sviluppatori osservano il runtime minimo deciso…»); neither delivers behaviour to an end user. With zero such slices before identity, no residual deferral is left for `Ordering criteria` to justify.
- **Candidate B:** `holds`
  - **Citation:** `Ordering criteria`
  - **What it shows:** Six behavioural slices (2, 4, 5, 6, 7, 8) precede identity at slice 9, and the deferral is justified once, in the entry «Identità dopo cattura e ricerca: nessuna delle loro evidenze dipende da proprietà o membership reale. Fino alla slice 9 lo scope è un ricettario configurato risolto da un unico risolutore, e l'audience dichiarata di ogni slice precedente è sviluppatore/tester sull'ambiente non pubblico» — it names the evidence (that of capture and search) and states why it does not require real ownership or membership. The justification appears once and nowhere else in the section.
- **Watch for:** `no note on this row`
