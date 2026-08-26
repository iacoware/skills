# Scenarios — recipe-app

Four starting states the skill is run against: one map drawn from nothing, and three inputs the router
can read wrongly, each in the two directions it can go wrong. Every card carries its starting state,
the answer to give back, and what to read the result against. The text sent is not here: it is one
file per card in [`prompts/`](prompts/), so that a card can be read without reading the input and the
input has exactly one copy.

**Answer key.** Off limits to a generation session, the way `reference-roadmap/` is. How to run a card
is in [`../REVIEW-WORKFLOW.md`](../REVIEW-WORKFLOW.md); what a run does and does not license
concluding is at the head of [`../EVALUATION-RULES.md`](../EVALUATION-RULES.md).

**Each prompt** carries the request, the read restriction and the author's opening sentence, and
nothing else — no verdict, no hint that the input is a test. `{{RUN_DIR}}` is this run's directory and
`render_prompt.ts` resolves it. `@` is Claude Code's file-reference syntax; on a harness that lacks it,
drop the prefixes and change nothing else.

**Commands run from the repository root**, and the ids below are the ones the frozen states make
correct. If a fixture's high-water mark moves, the ids move with it and this text is what gets
corrected — never the fixture, and never to make a card pass.

## 0. Drawing from nothing

**Starting state:** an empty run directory. This is the map as it stands the first time it is drawn,
and the only state anybody can write an oracle for honestly.

```bash
mkdir -p evals/roadmap/recipe-app/results/ROADMAP-CC-<N>
```

**The prompt** is [`prompts/run.prompt.md`](prompts/run.prompt.md), with `{{RUN_DIR}}` resolved to
this run's directory. That file is the text word for word and this card no longer repeats it: it used
to carry a second version, which had already drifted from the one every run was actually sent.
`make eval-run` renders it and sends it; `mkdir` above is what a run driven by hand still needs.

**It writes unasked** — there is no `.roadmap/` to lose — and argues with its own first cut in the
same session. Whatever it asks, answer only what it needs to proceed.

**The verdict is three documents, in this order and no other:** `EVALUATION-BRIEF.md`, then
`../EVALUATION-RULES.md`, then `reference-roadmap/` with `REFERENCE-NOTES.md`.
[`../REVIEW-WORKFLOW.md`](../REVIEW-WORKFLOW.md), *Reading a run: a drawing*, says why the order is the
whole discipline and how binding the reference is.

**Rules:** all of them except *Revising an existing map*, R-006 and R-018.

## 1. Sounds like a change of destination, is work

**Starting state:** `fixtures/mid-flight/` — the MVP map with `S0`–`S3` delivered and in `archive/`,
`NOW` holding `S4`–`S11`, and `LATER` still carrying *ricerca su tutti i ricettari di cui si è
membri*.

```bash
mkdir -p evals/roadmap/recipe-app/results/ROUTER-1-CC-<N>
cp -R evals/roadmap/recipe-app/fixtures/mid-flight/. evals/roadmap/recipe-app/results/ROUTER-1-CC-<N>/.roadmap/
```

**The prompt:** [`prompts/router-1.prompt.md`](prompts/router-1.prompt.md).

**When it asks what was delivered:** nothing since the last session.

**A correct session** reads a claim about the path: `Goal` untouched, no theme recomputed, nothing
redrawn. The capability is already a candidate, so it is **promoted**, not admitted anew — the `LATER`
line goes, the register gains one row with the next free id, `S12`, a document appears under `slices/`,
and `Requested by` records where the candidate came from. The cap is checked and holds at nine rows.

**The failure it watches for** is the map being redrawn because scope sounds structural, and the
weaker version: a question asked where nothing about the destination is in doubt. *Which* cookbooks a
search reaches is the reach of a promise the goal already makes. Admitting it straight into `NOW`
without noticing the candidate gets the altitude right and the operation wrong — a finding against
R-006 alone.

**Rules:** R-003, R-006, R-002, R-025, R-030, R-031.

## 2. Sounds like work, is a change of destination

**Starting state:** the initial map, which is the oracle itself — the one session that reads it, and
not leakage, since the oracle answers *how this map should be drawn* and this card asks nothing of the
sort. Copying is what keeps it frozen.

```bash
mkdir -p evals/roadmap/recipe-app/results/ROUTER-2-CC-<N>
cp -R evals/roadmap/recipe-app/reference-roadmap/. evals/roadmap/recipe-app/results/ROUTER-2-CC-<N>/.roadmap/
```

**The prompt:** [`prompts/router-2.prompt.md`](prompts/router-2.prompt.md) — scenario 1's frame, with
the opening sentence that makes this card: *Let us add a `visibility=public` flag on Cookbook — it is
already modelled anyway, it is one column and an afternoon.*

**When it asks what was delivered:** nothing; the map has just been drawn.

**A correct session asks which of the two claims holds.** It states the goal on file — a cookbook
shared between family and friends — and what the input looks like from where the map sits: a cookbook
readable by anybody moves the product to the open web. It names what that contradicts: the
authorization invariant under `Cross-functional concerns`, where an id outside the caller's scope
answers 404, and the exclusion *ruoli e permessi granulari*, which is the licence for having no role
model at all. Then it asks, and stops. One question, one short answer, no inference — and nothing to
confirm.

**The failure it watches for** is a slice admitted on the strength of how cheap the change is. Cost
and altitude are unrelated, and only altitude is the roadmap's business.

**The trap under the trap:** *ricettari pubblici tematici* is sitting in `LATER`, which makes
promotion look like the obvious move. Promotion asks whether the candidate serves the goal, and this
one replaces it.

**Rules:** R-004, R-005, R-006.

## 3. Sounds like a slice, is a spike

**Starting state:** `fixtures/redrawn/` — the map redrawn against the public-cookbooks goal, `S0`–`S11`
in `archive/`, `NOW` holding `S12`–`S16`, with `S13` being search across the whole public corpus. The
candidate promoted at the redraw was *ricettari pubblici tematici*, which is the goal now; *ricerca su
tutti i ricettari di cui si è membri* stayed in `LATER` with a recorded verdict, because the set of
cookbooks you are a member of and the public corpus are not the same set.

```bash
mkdir -p evals/roadmap/recipe-app/results/ROUTER-3-CC-<N>
cp -R evals/roadmap/recipe-app/fixtures/redrawn/. evals/roadmap/recipe-app/results/ROUTER-3-CC-<N>/.roadmap/
```

**The prompt:** [`prompts/router-3.prompt.md`](prompts/router-3.prompt.md) — scenario 1's frame, with
the opening sentence that makes this card: *Search has to work on the public corpus — thousands of
recipes across cookbooks nobody curated together.*

**When it asks what was delivered:** nothing since the redraw.

**A correct session mints a spike.** Nothing about the destination is in doubt, so no question is
asked and the spike is proposed in the block with everything else. The row carries `kind: spike`, the
next free id — `S17` — an empty `Audience`, and `S13` gains `S17` in `Depends on`. Its `Verification`
reads as a measurement: recall and latency for a shared index at that volume. The cap is checked and
holds at six rows. That the spike's id is higher than the row waiting on it is not a wrinkle: ids are
identity, the register's order is delivery order, and the spike is delivered first.

**The failure it watches for** is a slice admitted whose shape nobody can know yet — one shared index
or one index per cookbook are different slices. `S13` already stands for search over the public
corpus, which is what makes this card sharp: the volume the sentence carries is evidence the map did
not have, and widening `S13` on it is specifying an index shape nobody knows yet. The weaker failure
is a spike minted with no dependent and no `theme: goal`, which the validator catches, or one carrying
a timebox, which nothing catches.

**Do not run this card.** It has gone red three times out of three and the fix is written but not
revalidated; R-007 says why a fourth run buys nothing.

**Rules:** R-007, R-019, R-017, R-030, R-032.
