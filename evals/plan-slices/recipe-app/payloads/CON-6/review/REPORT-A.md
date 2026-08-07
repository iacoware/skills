# Improvement report — cycle CON-6

## Inputs

- **Candidate A:** `CANDIDATE-A.md`
- **Candidate B:** `CANDIDATE-B.md`

## Entries

### 1. A slice asserts one side of a behaviour two sources describe incompatibly, because the sweep never listed that behaviour

---

**Evidence — candidate A**

- `CANDIDATE-A.md:151` — slice 5 `Includes` reads «Un unico form accessibile per inserimento manuale
  ed edit di titolo, ingredienti e preparazione come testo libero»: the manual path reaches
  persistence through a plain form, unconditionally, with no wording deferring to a pending decision.
  Read at `CANDIDATE-A.md:351-355`: the published open entries are the Postgres provider, the
  embedding model with the query vector, and the extraction model — the manual path is not among
  them. The brief declares the two sources incompatible on exactly this behaviour.

**Evidence — candidate B**

- `CANDIDATE-B.md:196` — slice 7 `Includes` reads «Un solo form per inserimento manuale (campi vuoti)
  ed edit, con nome, ingredienti e preparazione come testo libero, senza parsing di quantità e
  unità»: same side asserted, same unconditional form. Read at `CANDIDATE-B.md:332-335`: four open
  entries are published — Postgres provider, embedding model, extraction model, query embedding at
  runtime — and none is the manual path.

**Existing rule that failed to prevent the defect**

- **Clause:** `SKILL.md:56-57` § `1 Build the evidence inventory` — «While an entry is open, no
  `Includes` or `Verification` bullet of a slice it blocks may assert a side: only conditional
  wording that defers to the pending decision is allowed.»
- **Covering rows:** `R-010`

**Remedy**

- `reformulation`

**Change to the skill**

- **Section:** `1 Build the evidence inventory`
- **Change:** «No `Includes` or `Verification` bullet may assert one side of a behaviour the sources
  leave open, whether or not the sweep listed it. Two sources that describe the same behaviour, path,
  or invariant incompatibly leave it open even when neither names a provider, model, service, or
  adapter: sweep per behaviour the plan will slice, not per component named. A bullet that touches
  such a behaviour uses conditional wording that defers to the pending decision, and the plan lists
  that behaviour among its open entries with the slices it blocks.»

**Binary test**

- No `Includes` or `Verification` bullet asserts in non-conditional form one side of a behaviour that
  two sources describe incompatibly, whether or not the plan lists that behaviour among its open
  entries.

**Cost**

- `none` — the clause keeps its reach and `R-010` stays anchored to it; the reformulation only
  removes the precondition that made the prohibition apply solely to entries the sweep had already
  listed, which is the precondition both candidates satisfied vacuously.

### 2. A `Learning / risk` claim states a measure that no `Verification` bullet of the same slice measures

---

**Evidence — candidate A**

- `CANDIDATE-A.md:182` — slice 6 `Learning / risk` reads «Misura hit-rate, durata e affidabilità del
  percorso gratuito sul caso d'uso più frequente». Read at `CANDIDATE-A.md:176-178`, that slice's
  `Verification` holds one successful single-page case («Un food blog con JSON-LD produce una ricetta
  ricercabile…») and a list of handled error cases; no bullet states a rate, a duration, or the set
  of cases either is measured over.

**Evidence — candidate B**

- `CANDIDATE-B.md:162` — slice 5 `Learning / risk` reads «L'hit-rate reale del JSON-LD sui siti
  effettivamente usati determina quanto peserà il fallback a pagamento». Read at
  `CANDIDATE-B.md:155-158`, that slice's `Verification` holds one successful single-blog case and
  three error or rejection cases; no bullet states a hit-rate or the set of sites it is measured
  over.

**Existing rule that failed to prevent the defect**

- **Clause:** `SKILL.md:208-209` § `3 Cut valuable vertical slices` — «Every material claim under
  `Learning / risk` must map to an observation in `Verification`. Checking that data exists does not
  demonstrate its quality, usability, latency, or cost.»
- **Covering rows:** `uncovered`

**Remedy**

- `reformulation`

**Change to the skill**

- **Section:** `3 Cut valuable vertical slices`
- **Change:** «Every claim under `Learning / risk` has its observation in the same slice's
  `Verification`. When the claim is a rate, a proportion, a cost, a latency, or a quality judgement,
  that `Verification` bullet states the measurement and the set of cases it is measured over. One
  successful case, a list of handled failure cases, or the existence of the data is not that
  observation: they decide whether the behaviour works, not what the claimed measure is worth.»

**Binary test**

- If a `NOW` slice's `Learning / risk` names a rate, proportion, cost, latency, or quality measure,
  one `Verification` bullet of that same slice states that measure and the set of cases it is
  measured over.

**Cost**

- `none` — no rule and no row is removed; the clause's second sentence is absorbed into the
  reformulated wording, which states the same exclusion over the fields a plan actually publishes.

### 3. A `Decision checkpoints` entry names evidence that the slice it follows does not produce

---

**Evidence — candidate A**

- `CANDIDATE-A.md:342` — «**After slice 8:** Copertura, qualità, errori e costo dei tre ingressi →
  cambiare cascata, soglie o priorità dei flussi restanti». Read at `CANDIDATE-A.md:224-225`, slice
  8's `Verification` holds one successful case and one list of distinct failure outcomes: neither
  coverage nor cost across the three entry points is stated there.

**Evidence — candidate B**

- `CANDIDATE-B.md:325` — «**Dopo 5:** hit-rate reale del JSON-LD sui siti effettivamente usati →
  dimensionare il peso del fallback LLM e il budget di estrazione». Read at `CANDIDATE-B.md:155-158`,
  slice 5's `Verification` states no hit-rate and no set of sites; the checkpoint's decision therefore
  arrives with nothing to decide on.

**Existing rule that failed to prevent the defect**

- **Clause:** `SKILL.md:309-310` § `4 Assign horizons and order for learning` — «Add checkpoints only
  where evidence can cancel, promote from `LATER`, reorder, split, or change unfinished work.»
- **Covering rows:** `uncovered`

**Remedy**

- `reformulation`

**Change to the skill**

- **Section:** `4 Assign horizons and order for learning`
- **Change:** «Add a checkpoint only where a `Verification` bullet of the slice it follows produces
  the evidence the checkpoint names, and that evidence can cancel, promote from `LATER`, reorder,
  split, or change unfinished work. A checkpoint whose evidence no slice produces is dropped, or
  moved behind the slice that measures it; naming the evidence in the checkpoint does not make a
  slice produce it.»

**Binary test**

- Every `Decision checkpoints` entry names evidence that a `Verification` bullet of the slice it
  follows states.

**Cost**

- `none` — the existing condition on the checkpoint's decision is kept and a second condition is
  added on the same clause; no other rule is narrowed and no row is displaced.

### 4. A published spike carries no time box and no decision its answer enables, so nothing can end it

---

**Evidence — candidate A**

- `CANDIDATE-A.md:347-349` — all three entries under `Non-product work` are spikes placed before a
  slice («Prima della slice 1 — scelta Postgres», «Prima della slice 3 — spike embedding», «Prima
  della slice 7 — spike estrazione LLM»). Each states an activity and an exit («uscita: …,
  esperimenti eliminati o assorbiti nella slice N»); read at those three lines, none states a time
  box, and `CANDIDATE-A.md:348` states the activity («Selezionare API/modello multilingue e risolvere
  il conflitto sul vettore query con corpus, latenza e costo») without naming the decision the answer
  enables. Inferred, and marked as such: an unbounded spike sitting before slice 1 and slice 3 has no
  point at which the plan continues without its answer.

**Evidence — candidate B**

- `not manifested` — B publishes no spike and no `Non-product work` section; the same three undecided
  choices are exposed only as open entries naming the slices they block (`CANDIDATE-B.md:332-334`),
  and the embedding-model choice is closed inside a real slice, whose `Includes` compares candidates
  on the corpus (`CANDIDATE-B.md:105`).

**Existing rule that failed to prevent the defect**

- **Clause:** `SKILL.md:306-307` § `4 Assign horizons and order for learning` — «When a real slice
  cannot resolve a material uncertainty, define a time-boxed spike with question, evidence, enabled
  decision, exit criterion, and treatment of experimental code.»
- **Covering rows:** `uncovered`

**Remedy**

- `reformulation`

**Change to the skill**

- **Section:** `4 Assign horizons and order for learning`
- **Change:** «When a real slice cannot resolve a material uncertainty, define a spike and publish
  it with all of: its time box, the question it answers, the evidence it collects, the decision that
  answer enables, its exit criterion, and what happens to its experimental code. A spike published
  without its time box and without the decision it enables cannot be ended, cancelled, or judged to
  have failed, and the slice it precedes inherits the uncertainty it was meant to remove.»

**Binary test**

- Every spike the plan publishes states a time box, the question it answers, the decision its answer
  enables, its exit criterion, and the treatment of its experimental code.

**Cost**

- `none` — the fields are the ones the clause already names; the reformulation only requires them
  where the spike is published, and no other rule, section, or row changes.
