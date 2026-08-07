# Improvement report — cycle CON-6

## Inputs

- **Candidate A:** `CANDIDATE-A.md`
- **Candidate B:** `CANDIDATE-B.md`

## Entries

### 1. An external adapter and the invariant it maintains are opened inside one slice and re-opened by a later slice, with other themes delivered in between

---

**Evidence — candidate A**

- `CANDIDATE-A.md:172` — slice 6 `Includes` opens the object-storage adapter and the cover
  invariant as a side effect of the import path: «Foto sorgente disponibili sono copiate su
  Cloudflare R2; la prima diventa cover.»
- `CANDIDATE-A.md:256-258` — slice 10 `Includes` re-opens the same adapter and the same invariant
  («Aggiunta e rimozione di più foto per ricetta su Cloudflare R2», «Prima foto come cover
  predefinita e selezione esplicita di un'altra cover», «Aggiornamenti DB/storage recuperabili
  mantengono esattamente una cover quando esistono foto»). Read: the adapter is named in the
  `Includes` of two slices. Inferred: ownership stays partial from slice 6 to slice 10, across
  slices 7, 8 and 9, which belong to three other themes; slice 7's `Verification` at
  `CANDIDATE-A.md:202` already has to reason about orphaned objects in that adapter.

**Evidence — candidate B**

- `not manifested` — B names the storage adapter and the cover invariant in the `Includes` of one
  slice only (`CANDIDATE-B.md:216-219`), and that slice retro-fits the image step onto the
  already-delivered capture paths («in tutti i path di aggiunta da link, con il passo "salvo foto"
  aggiunto al progress»); the earlier capture slice's `Includes` (`CANDIDATE-B.md:148-151`) names
  no storage at all.

**Existing rule that failed to prevent the defect**

- **Clause:** `SKILL.md:233-234` § `ANTI-PATTERNS` — «**Premature or split shared pipeline:** open a
  pipeline or adapter shared by several paths before its `NOW` producers exist, or let a second
  slice re-open what another slice already owns.»
- **Covering rows:** `R-006`, `R-016`

**Remedy**

- `reformulation`

**Change to the skill**

- **Section:** `ANTI-PATTERNS`
- **Change:** «**Premature or split shared pipeline:** open a pipeline or adapter shared by several
  paths before its `NOW` producers exist, or name that pipeline, that adapter, or the invariant it
  maintains in the `Includes` of a second `NOW` slice. Widening, deepening or completing what an
  earlier slice opened is re-opening it, whatever theme the second slice carries: the first slice
  that names a shared adapter owns every `NOW` use of it, and later slices name it as reuse only.»

**Binary test**

- No external adapter, shared pipeline, or invariant named in the `Includes` of a `NOW` slice is
  named again in the `Includes` of a later `NOW` slice other than as declared reuse.

**Cost**

- The invitation to split at `SKILL.md:159-160` loses `external adapters` from its list, which
  otherwise licenses exactly the split this anti-pattern forbids; `lifecycle operations` and
  `failure profiles` stay.

### 2. A `Verification` bullet names a failure mode and a cost unit that exist under only one branch of a choice the same plan publishes as open

---

**Evidence — candidate A**

- `CANDIDATE-A.md:354` — the plan declares open how the query vector is obtained («come conciliare
  "solo in add/edit" con la query che richiede `embedding(query)`? Blocca le slice 3–12»).
- `CANDIDATE-A.md:134-135` — slice 4's `Verification`, a slice that question blocks, asserts
  «provider lento o indisponibile restituisce uno stato recuperabile» and «latenza e costo per
  query». Read: both bullets are unconditional. Inferred: a per-query provider failure and a
  per-query cost exist only if the query is embedded by a call at search time; under a cached or
  precomputed resolution neither observation has a referent. The slice's `Includes`
  (`CANDIDATE-A.md:127`) does defer — «secondo la decisione aperta» — so the conditional wording
  was applied to the choice and not to what the bullets presuppose about it.

**Evidence — candidate B**

- `not manifested` — at the same slice B keeps both the mechanism and its failure mode conditional:
  «Path di embedding della query secondo la decisione aperta, con timeout e messaggio esplicito se
  quella modalità dipende da un servizio esterno indisponibile» (`CANDIDATE-B.md:128`) and «Latenza
  della ricerca misurata sul path effettivamente scelto» (`CANDIDATE-B.md:136`), with the choice
  declared open at `CANDIDATE-B.md:335`.

**Existing rule that failed to prevent the defect**

- **Clause:** `SKILL.md:56-57` § `§ 1 Build the evidence inventory` — «While an entry is open, no
  `Includes` or `Verification` bullet of a slice it blocks may assert a side: only conditional
  wording that defers to the pending decision is allowed.»
- **Covering rows:** `R-010`

**Remedy**

- `reach-change`

**Change to the skill**

- **Section:** `§ 1 Build the evidence inventory`
- **Change:** «While an entry is open, no `Includes` or `Verification` bullet of a slice it blocks
  may assert or presuppose a side. A bullet presupposes a side when it names a step, dependency,
  failure mode, cost unit, or measurement that exists under only one of the pending alternatives.
  Only wording that holds under every pending alternative, or that defers explicitly to the pending
  decision, is allowed — including in the bullets that name what the slice will observe.»

**Merged claim**

- No `Includes` or `Verification` bullet of a slice blocked by an unresolved choice asserts or
  presupposes one side of it; a bullet presupposes a side when it names a step, dependency, failure
  mode, cost unit, or measurement that exists under only one of the pending alternatives.
  Unresolved covers a conflict between the sources — those listed under `Known conflicts` in the
  brief, plus those demonstrable by citing two sources in disagreement — and, in the slices that
  choice blocks, any other choice the plan does not resolve by citing a selecting source. Declaring
  the choice under `Open questions` or assigning it a spike does not resolve it.

**Binary test**

- No `Includes` or `Verification` bullet of a `NOW` slice blocked by a choice the plan leaves
  unresolved names a step, dependency, failure mode, cost unit, or measurement that exists under
  only one of the pending alternatives.

**Cost**

- `R-010` is replaced by the merged claim above. No clause is removed: the anti-pattern at
  `SKILL.md:237-238` states the same prohibition negatively and remains the index entry for it.

### 3. A `Learning / risk` claim about a rate over a population maps to a `Verification` that observes one successful instance

---

**Evidence — candidate A**

- `CANDIDATE-A.md:182` — slice 6 `Learning / risk`: «Misura hit-rate, durata e affidabilità del
  percorso gratuito sul caso d'uso più frequente.»
- `CANDIDATE-A.md:177-178` — the same slice's `Verification` observes one page that works («Un food
  blog con JSON-LD produce una ricetta ricercabile…») and a list of error cases. Read: no bullet
  names a rate, a duration, or the set of pages over which either would be measured. Inferred: the
  claim's quantity has no observation, so the decision at `CANDIDATE-A.md:342` consumes evidence
  the plan never schedules.

**Evidence — candidate B**

- `CANDIDATE-B.md:162` — slice 5 `Learning / risk`: «L'hit-rate reale del JSON-LD sui siti
  effettivamente usati determina quanto peserà il fallback a pagamento.»
- `CANDIDATE-B.md:155-158` — the same slice's `Verification` observes one blog that works, three
  distinct error messages, a retry, and a rejected host; no bullet observes a rate over the sites
  the claim quantifies over, while the checkpoint at `CANDIDATE-B.md:325` reads that rate back out
  of the slice.

**Existing rule that failed to prevent the defect**

- **Clause:** `SKILL.md:208-209` § `§ 3 Cut valuable vertical slices` — «Every material claim under
  `Learning / risk` must map to an observation in `Verification`. Checking that data exists does not
  demonstrate its quality, usability, latency, or cost.»
- **Covering rows:** `uncovered`

**Remedy**

- `reformulation`

**Change to the skill**

- **Section:** `§ 3 Cut valuable vertical slices`
- **Change:** «Every material claim under `Learning / risk` must map to an observation in
  `Verification` that measures the quantity the claim names, over the population the claim
  quantifies over. A claim about a rate, coverage, latency, quality, or cost is not met by one
  successful instance, and checking that data exists does not demonstrate any of them; a
  `Decision checkpoints` entry may read back only quantities some slice's `Verification` observes.»

**Binary test**

- Every quantity a `NOW` slice names under `Learning / risk` — rate, coverage, latency, cost, or
  quality — is named by a bullet of the same slice's `Verification`.

**Cost**

- The clause's second sentence stops standing alone: «Checking that data exists does not
  demonstrate its quality, usability, latency, or cost» is absorbed into the first as one of the
  cases where the observation does not measure the claimed quantity.

### 4. A spike is scheduled for an uncertainty that the slice it precedes already observes in its own `Verification`

---

**Evidence — candidate A**

- `CANDIDATE-A.md:348` — non-product entry before slice 3: «Selezionare API/modello multilingue e
  risolvere il conflitto sul vettore query con corpus, latenza e costo». Slice 3's own
  `Verification` (`CANDIDATE-A.md:109-111`) observes exactly that: cross-language ranking on a
  representative corpus, and «qualità relativa, latenza e costo per decidere se il differenziatore
  è sostenibile».
- `CANDIDATE-A.md:349` — non-product entry before slice 7: «Confrontare modelli economici su pagine
  senza JSON-LD e output malformati», against slice 7's `Verification` at `CANDIDATE-A.md:201`,
  «Corpus rappresentativo confronta completezza utile, errori, latenza e costo dei due percorsi».
  Read: the two entries and the two slices name the same measurements. Inferred: the same
  uncertainty is scheduled twice, and the same choice is additionally exposed under `Open questions`
  (`CANDIDATE-A.md:354-355`), so the plan takes both branches of an alternative the skill offers as
  a choice.

**Evidence — candidate B**

- `not manifested` — B publishes no scheduled investigation at all and exposes the same three
  undecided choices once, under `Open questions` naming the slices they block
  (`CANDIDATE-B.md:332-334`), leaving the slice itself to close the choice on evidence
  («Confronto dei candidati multilingue sullo stesso corpus, senza preselezione, per chiudere la
  scelta del modello», `CANDIDATE-B.md:105`).

**Existing rule that failed to prevent the defect**

- **Clause:** `SKILL.md:306-307` § `§ 4 Assign horizons and order for learning` — «When a real slice
  cannot resolve a material uncertainty, define a time-boxed spike with question, evidence, enabled
  decision, exit criterion, and treatment of experimental code.»
- **Covering rows:** `uncovered`

**Remedy**

- `reformulation`

**Change to the skill**

- **Section:** `§ 4 Assign horizons and order for learning`
- **Change:** «Define a time-boxed spike only for a material uncertainty that no `NOW` slice's own
  `Verification` observes. When a slice observes it, expose the uncertainty under `Open questions`
  naming that slice and schedule nothing before it; a spike whose question a slice already answers
  buys the same evidence twice and moves the decision off the slice that produces it. A spike states
  its question, the evidence it produces, the decision it enables, its exit criterion, and the
  treatment of its experimental code.»

**Binary test**

- No spike the plan schedules names an uncertainty that a `NOW` slice's own `Verification` already
  observes.

**Cost**

- The free choice at `SKILL.md:50-52` narrows: a spike stops being an interchangeable alternative to
  an `Open questions` item, and remains available only for uncertainties no slice observes.

### 5. A behaviour whose exclusion the plan itself makes conditional is published under `OUT-OF-SCOPE`, where no promotion trigger is recorded

---

**Evidence — candidate A**

- `CANDIDATE-A.md:336` — `OUT-OF-SCOPE` entry: «**IaC Terraform/SST nell'MVP** — Sovradimensionato
  rispetto a `fly.toml` e CLI; rivalutabile solo con futura esigenza multi-cloud/versionata.» Read:
  the rationale names the future condition under which the behaviour returns. Inferred: this is a
  `LATER` entry with its trigger written into an exclusion rationale, so the condition is never
  reachable as a promotion trigger and never named as evidence — while the same plan does use
  `LATER` for a maturity condition of the same shape at `CANDIDATE-A.md:325-327`.

**Evidence — candidate B**

- `not manifested` — B's eight `OUT-OF-SCOPE` entries (`CANDIDATE-B.md:312-319`) each state only why
  the behaviour is excluded; the nearest case, passkeys at `CANDIDATE-B.md:314`, gives current
  tooling immaturity as part of the reason and names no condition returning the behaviour, and the
  behaviour whose exclusion is conditional sits in `LATER` with a trigger
  (`CANDIDATE-B.md:306-308`).

**Existing rule that failed to prevent the defect**

- **Clause:** `SKILL.md:256-257` § `§ 4 Assign horizons and order for learning` — «Admission test:
  `NOW` requires a source that asks for the behaviour, `LATER` a promotion trigger, `OUT-OF-SCOPE` a
  declared exclusion.»
- **Covering rows:** `R-004`

**Remedy**

- `reformulation`

**Change to the skill**

- **Section:** `§ 4 Assign horizons and order for learning`
- **Change:** «Admission test: `NOW` requires a source that asks for the behaviour, `LATER` a
  promotion trigger, `OUT-OF-SCOPE` an exclusion that names no condition for return. When a source,
  or the plan's own rationale, excludes a behaviour while naming a condition, evidence, or future
  state under which it comes back, the behaviour is `LATER` and that condition is its promotion
  trigger; a rationale that names such a condition under `OUT-OF-SCOPE` is a misfiled `LATER` entry.»

**Binary test**

- No `OUT-OF-SCOPE` entry names a condition, evidence, or future state under which the excluded
  behaviour would be reconsidered.

**Cost**

- `none` — the sentence keeps its three branches and gains no fourth, and the horizon definitions at
  `SKILL.md:252-253` and `SKILL.md:254` stand unchanged; the change only makes the third branch
  exclusive of the second.
