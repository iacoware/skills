# Router scenarios

Three cases that hold the router of `skills/roadmap/SKILL.md` — the half of the net that reads what a
session does to a map already standing, where [`../REVIEW-WORKFLOW.md`](../REVIEW-WORKFLOW.md) reads
one drawn from nothing. Run them after a change to § 2, § 4 or `references/slice-rules.md`, which is
where the router and the five operations live.

Each holds one input the router can read wrongly, in the two directions it can go wrong and on the
axis underneath. They are cheap because each starts from a map already standing, and that branch
proposes before it writes: what you are reading is what the session offered to do, not what it did.

Each scenario carries its own starting state, the sentence to send, the answer to give back, and the
verdict to read the proposal against. The verdict is answer key — it is off limits to a session, the
way `reference-roadmap/` is.

## Running one

**[`../REVIEW-WORKFLOW.md`](../REVIEW-WORKFLOW.md) § *Before any session* binds here too**: the
installed copy is the one you changed, the skill is invoked explicitly, model and effort come from
the session, every run gets its own directory under `results/` and keeps a `PROMPT.md`.

**Copy the starting state** into that directory with the scenario's command, run from the repository
root. Never point a session at `fixtures/` or at `reference-roadmap/`: both are frozen and a session
writes.

**The prompt** carries the author's opening sentence and nothing else — no verdict, no hint that the
input is a test. Replacing `<N>` and the scenario number:

```
/roadmap Treat evals/roadmap/recipe-app/results/ROUTER-1-CC-<N>/ as the project root; the roadmap is in its .roadmap/, and the documents it names as sources are in @evals/roadmap/recipe-app/sources/. <the author's opening sentence>. Read nothing else in this repository, in this session or in any session you delegate to: everything else under evals/ and under design/ is off limits.
```

`@` is Claude Code's file-reference syntax; on a harness that lacks it, drop the prefixes and change
nothing else.

**The session will ask what was delivered** — § 1 says it must, and a tracker cannot answer it. Each
scenario says what to answer, and the answer is part of the scenario. Answer that, and nothing more.

**Then read the proposed block against the verdict.** On scenarios 1 and 3, confirm once and run
`make validate-roadmap ROADMAP=<the run directory>/.roadmap`; on scenario 2 the correct session ends
in a question, and there is nothing to confirm — record the question and stop. Never confirm a
proposal that redraws the map: a redraw you let it write teaches nothing a proposal did not already
say.

The ids below are the ones the frozen states make correct. If a fixture's high-water mark moves, the
ids move with it and the scenario text is what gets corrected.

What a run does and does not license concluding is at the head of
[`../EVALUATION-RULES.md`](../EVALUATION-RULES.md), where the rules each scenario cites also live.

## 1. Sounds like a change of destination, is work

**Starting state:** `fixtures/mid-flight/` — the MVP map with `S0`–`S3` delivered and in `archive/`,
`NOW` holding `S4`–`S11`, and `LATER` still carrying *ricerca su tutti i ricettari di cui si è
membri*.

```bash
mkdir -p evals/roadmap/recipe-app/results/ROUTER-1-CC-<N>
cp -R evals/roadmap/recipe-app/fixtures/mid-flight/. evals/roadmap/recipe-app/results/ROUTER-1-CC-<N>/.roadmap/
```

**The author's opening sentence:** *Search has to work across every cookbook I belong to, not just
the current one.*

**When it asks what was delivered:** nothing since the last session.

**A correct session** reads a claim about the path. The `Goal` line is untouched, no theme is
recomputed, and nothing is redrawn. The capability is already a candidate, so it is **promoted**, not
admitted anew: the `LATER` line is gone, the register has one more row carrying the next free id —
`S12` — a document appears under `slices/`, and `Requested by` records where the candidate came from.
The cap is checked and holds at nine rows.

**The failure it watches for** is the map being redrawn because scope sounds structural, and the
weaker version of it: a question asked where nothing about the destination is in doubt. *Which*
cookbooks a search reaches is the reach of a promise the goal already makes.

Reading it differently is not automatically wrong — a session that admits it straight into `NOW`
without noticing the candidate got the altitude right and the operation wrong, which is a finding
against R-006 alone. Cite what actually failed.

**Rules:** R-003, R-006, R-002, R-025, R-030.

## 2. Sounds like work, is a change of destination

**Starting state:** the initial map, which is the oracle itself.

```bash
mkdir -p evals/roadmap/recipe-app/results/ROUTER-2-CC-<N>
cp -R evals/roadmap/recipe-app/reference-roadmap/. evals/roadmap/recipe-app/results/ROUTER-2-CC-<N>/.roadmap/
```

This is the one session that reads the oracle, and it is not leakage: what the oracle answers is
*how this map should be drawn*, and this scenario asks nothing of the sort. Copying it is what keeps
it frozen and keeps the session's writes out of it.

**The author's opening sentence:** *Let us add a `visibility=public` flag on Cookbook — it is already
modelled anyway, it is one column and an afternoon.*

**When it asks what was delivered:** nothing; the map has just been drawn.

**A correct session asks which of the two claims holds.** It states the goal on file — a cookbook
shared between family and friends — says what the input looks like from where the map sits: a
cookbook readable by anybody moves the product to the open web. It names what that contradicts: the
authorization invariant under `Cross-functional concerns`, where an id outside the caller's scope
answers 404, and the exclusion *ruoli e permessi granulari*, which is the licence for having no role
model at all. Then it asks, and stops. One question, one short answer, no inference.

**The failure it watches for** is a slice admitted on the strength of how cheap the change is. Cost
and altitude are unrelated, and only altitude is the roadmap's business.

**The trap under the trap:** *ricettari pubblici tematici* is sitting in `LATER` as a candidate,
which makes promotion look like the obvious move. It is not. Promotion asks whether the candidate
serves the goal, and this one replaces it — a candidate is a licence to schedule, never a licence to
skip the question.

**Rules:** R-004, R-005, R-006, R-031.

## 3. Sounds like a slice, is a spike

**Starting state:** `fixtures/redrawn/` — the map redrawn against the public-cookbooks goal, `S0`–`S11`
in `archive/`, `NOW` holding `S12`–`S16`, with `S13` being search across the whole public corpus. The
candidate that got promoted was *ricettari pubblici tematici*, which is the goal now; *ricerca su
tutti i ricettari di cui si è membri* stayed in `LATER` with a recorded verdict, because the set of
cookbooks you are a member of and the public corpus are not the same set.

```bash
mkdir -p evals/roadmap/recipe-app/results/ROUTER-3-CC-<N>
cp -R evals/roadmap/recipe-app/fixtures/redrawn/. evals/roadmap/recipe-app/results/ROUTER-3-CC-<N>/.roadmap/
```

**The author's opening sentence:** *Search has to work on the public corpus — thousands of recipes
across cookbooks nobody curated together.*

**When it asks what was delivered:** nothing since the redraw.

**A correct session mints a spike.** Nothing about the destination is in doubt, so no question is
asked and the spike is proposed in the block with everything else. The row carries `kind: spike`, the
next free id — `S17` — an empty `Audience`, and `S13` gains `S17` in `Depends on`. Its `Verification`
reads as a measurement: recall and latency for a shared index at that volume. The cap is checked and
holds at six rows.

`S13` already stands for search over the public corpus, which is what makes this scenario sharp: the
volume the sentence carries — thousands of recipes nobody curated together — is evidence the map did
not have, and widening `S13` on it is specifying an index shape nobody knows yet.

That the spike's id is higher than the row waiting on it is not a wrinkle: ids are identity, the
register's order is delivery order, and the spike is delivered first.

**The failure it watches for** is a slice admitted whose shape nobody can know yet — one shared index
or one index per cookbook are different slices, and specifying either now is specifying work the map
cannot know. The weaker failure is a spike minted with no dependent and no `theme: goal`, which the
validator catches, or one carrying a timebox, which nothing catches.

**Rules:** R-007, R-019, R-017, R-030, R-032.
