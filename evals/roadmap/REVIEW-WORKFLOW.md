# Review workflow

How to run one review of `skills/roadmap/SKILL.md`, to notice that a change to it broke something it
used to get right. What to look for is in [`EVALUATION-RULES.md`](EVALUATION-RULES.md).

Two halves, and a change rarely needs both:

- **one drawing**, the five steps below — half an hour, one provider call. Run it after a change to
  § 1, § 3, § 5, to `references/drawing-the-map.md` or to either template;
- **three router scenarios** — ten minutes and one provider call each. Run them after a change to
  § 2, § 4 or `references/slice-rules.md`, which is where the router and the five operations live.

`references/slice-rules.md` is read on every session, so a change to it shows in both halves and the
router scenarios are the cheaper place to see it. § 6 shows in whichever half you run, and only if
the session gets as far as handing a row over.

Run either after a change you believe is substantive, not after every commit: a net you skip is worse
than a net you sized honestly. One run is a question, not a verdict — the same run twice with the
same answer is a verdict.

What this net does **not** cover, and how to conclude from a run, is in
[`OPEN-VERIFICATION.md`](OPEN-VERIFICATION.md). It carries one thing left to do and no more: a hole
is closed when a change to `SKILL.md` that real use asked for would have fallen through it, never
because it is a hole.

The steps use `recipe-app`, today's only scenario. With a second one, substitute its directory
everywhere; the rules do not change.

## Before any session

**Install the skill you mean to review.** `make add` copies the payload into `~/.agents/skills/`, and
the agent reads the copy. Skip it and you are reviewing the version before your change. Restart the
agent session afterwards, and check that the copy is the one you expect.

**The skill is invoked explicitly** — `/roadmap` on Claude Code, `$roadmap` on Codex. Neither harness
activates it on its own: `skills/roadmap/agents/openai.yaml` sets `allow_implicit_invocation: false`
and the frontmatter sets `disable-model-invocation: true`. Drop the prefix and the candidate is born
without the skill, which means you are reviewing the model instead.

**Model and effort are set in the session, never in the prompt.** Check what the session actually
says before sending, and write down what it said rather than what you intended.

**Every run gets its own directory** under `recipe-app/results/`, and the session is pointed at that
directory as if it were the project. Never point a session at `reference-roadmap/` or at
`fixtures/`: both are frozen and a session writes.

**Every run directory keeps a `PROMPT.md`** holding the exact text sent, every answer given back, and
the model and harness it ran on. Write it from what the session actually received, not from the
template above: a run driven any other way — through a sub-agent, on another harness, with a prompt
you adapted — is still evidence, but only if the adaptation is readable. `recipe-app/results/README.md`
carries the convention and what the 2026-08-20 runs departed from.

**What a session may read** is the sources, and its own copy of `.roadmap/`. Everything else in this
repository is off limits, and the prompt says so. Three things are off limits in particular:
`reference-roadmap/` and its rationale, which are the answer key to a drawing; `EVALUATION-RULES.md`
and `EVALUATION-BRIEF.md`, which are how it will be read; and the whole of `design/roadmap/`, whose
[`WORKFLOWS.md`](../../design/roadmap/WORKFLOWS.md) § 3 is the answer key to the three router
scenarios, verdicts and all.

## Drawing a map: the five steps

1. **Draw one map from `recipe-app/sources/` alone**, in a fresh session with no other context.

   **Claude Code**, one message, replacing `<N>`:

   ```
   /roadmap Read the markdown documents in @evals/roadmap/recipe-app/sources/, starting from @evals/roadmap/recipe-app/sources/goal.md, and draw the roadmap that reaches the goal they state. Treat evals/roadmap/recipe-app/results/ROADMAP-CC-<N>/ as the project root: write the map to evals/roadmap/recipe-app/results/ROADMAP-CC-<N>/.roadmap/. Read nothing else in this repository, in this session or in any session you delegate to: the sources are the only input, and everything else under evals/ and under design/ is off limits.
   ```

   **Codex**, one message:

   ```
   $roadmap Read the markdown documents in evals/roadmap/recipe-app/sources/, starting from evals/roadmap/recipe-app/sources/goal.md, and draw the roadmap that reaches the goal they state. Treat evals/roadmap/recipe-app/results/ROADMAP-CX-<N>/ as the project root: write the map to evals/roadmap/recipe-app/results/ROADMAP-CX-<N>/.roadmap/. Read nothing else in this repository, in this session or in any session you delegate to: the sources are the only input, and everything else under evals/ and under design/ is off limits.
   ```

   The two differ only in the `@` prefixes, Claude Code's file-reference syntax, which has no Codex
   equivalent.

   A first drawing writes unasked — there is no `.roadmap/` to lose — and the session argues with
   its own first cut in the same session, so what you read is what it did. Answer what it asks you
   and nothing else: answering more turns the run into a collaboration you cannot read. The four-part
   report it closes on — themes, register, open questions, path — is evidence too.

2. **`make validate-roadmap ROADMAP=evals/roadmap/recipe-app/results/ROADMAP-CC-<N>/.roadmap`** from
   the repository root — structural, deterministic, free. `ROADMAP` is the directory holding
   `roadmap.md`, not a file. If it is red, stop and fix before reading.

   The session runs the validator itself at § 5, and its run is not this one: § 5 resolves `.roadmap`
   against the author's project, which here is the run directory and not the repository root. A
   session that changes directory first gets a real result; one that does not gets nothing, and that
   is an artifact of this layout rather than a defect. What R-033 reads is that it ran the validator
   at all and what it did with the `WARNING`s, never where it pointed.

3. **Read the map against `recipe-app/EVALUATION-BRIEF.md`**, opening `sources/` only to verify a
   citation. **The brief is the authority**, not the sources: it decides which conflicts exist, which
   alternatives are accepted, and which uncertainties are material. Its entries carry ids — cite
   them, in notes and in reports, instead of paraphrasing what they say.

   Read the register and the slice documents together. A row whose document contradicts it is a
   defect the register alone cannot show, and half the rules below are about a field the table does
   not carry.

4. **Walk `EVALUATION-RULES.md`**, keeping the brief's uncertainty table open for R-016. On a first
   drawing, skip *Re-truing an existing map*, R-006 and R-018; on a redraw all three come back.

5. **Only now** open `recipe-app/reference-roadmap/`, and
   `recipe-app/REFERENCE-ROADMAP-RATIONALE.md`, and compare. Forming your verdict first is what keeps
   the reference a memory aid instead of a diff target — the order is the whole discipline. What you
   are hunting is what you forgot, not what you did differently.

   The reference was hand-written from the sources before any candidate existed, and is frozen: it is
   rewritten only when the sources change, never because a candidate convinced. How binding each part
   of it is:

   - Where reference and `sources/` diverge, the defect is in the reference.
   - **Ids, titles, slugs, theme count, row count and register order may all differ.** The reference's
     ids are the order it happened to draw in and mean nothing else. On each difference, ask which of
     the two has the better reason — the rationale file holds the reference's.
   - Each `Verification` shows how a row could be demonstrated; it is one way, not the only one. The
     same holds for the wording of `Cross-functional concerns`, whose five headings are owed but not
     their content.
   - A source may support a `LATER` or `OUT-OF-SCOPE` classification other than the reference's, and
     the brief says where.
   - The reference takes one door out of the sweep for each conflict and each undecided choice. Another
     door is a different choice and not a defect; **no** door is R-015.

## The three router scenarios

Each holds one input the router can read wrongly, in the two directions it can go wrong and on the
axis underneath. They are cheap because each starts from a map already standing, and that branch
proposes before it writes: what you are reading is what the session offered to do, not what it did.

**Setting one up**, replacing `<N>` and the fixture:

```bash
mkdir -p evals/roadmap/recipe-app/results/ROUTER-1-CC-<N>
cp -R evals/roadmap/recipe-app/fixtures/mid-flight/. evals/roadmap/recipe-app/results/ROUTER-1-CC-<N>/.roadmap/
```

**The prompt** carries the author's opening sentence and nothing else — no verdict, no hint that the
input is a test:

```
/roadmap Treat evals/roadmap/recipe-app/results/ROUTER-1-CC-<N>/ as the project root; the roadmap is in its .roadmap/, and the documents it names as sources are in @evals/roadmap/recipe-app/sources/. <the author's opening sentence>. Read nothing else in this repository, in this session or in any session you delegate to: everything else under evals/ and under design/ is off limits.
```

On Codex, `$roadmap` and no `@`.

**The session will ask what was delivered** — § 1 says it must, and a tracker cannot answer it. Each
scenario below says what to answer, and the answer is part of the scenario. Answer that, and nothing
more.

**Then read the proposed block against the verdict.** On scenarios 1 and 3, confirm once and run
`make validate-roadmap` on the run directory; on scenario 2 the correct session ends in a question,
and there is nothing to confirm — record the question and stop. Never confirm a proposal that
redraws the map: a redraw you let it write teaches nothing a proposal did not already say.

The ids below are the ones the frozen states make correct. If a fixture's high-water mark moves, the
ids move with it and the scenario text is what gets corrected.

### 1. Sounds like a change of destination, is work

**Starting state:** `fixtures/mid-flight/` — the MVP map with `S0`–`S3` delivered and in `archive/`,
`NOW` holding `S4`–`S11`, and `LATER` still carrying *ricerca su tutti i ricettari di cui si è
membri*.

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

### 2. Sounds like work, is a change of destination

**Starting state:** the initial map. Copy `reference-roadmap/` into the run directory rather than
pointing a session at it:

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

### 3. Sounds like a slice, is a spike

**Starting state:** `fixtures/redrawn/` — the map redrawn against the public-cookbooks goal, `S0`–`S11`
in `archive/`, `NOW` holding `S12`–`S16`, with `S13` being search across the whole public corpus. The
candidate that got promoted was *ricettari pubblici tematici*, which is the goal now; *ricerca su
tutti i ricettari di cui si è membri* stayed in `LATER` with a recorded verdict, because the set of
cookbooks you are a member of and the public corpus are not the same set.

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
