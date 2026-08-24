# Review workflow

How to run one review of a fresh drawing by `skills/roadmap/SKILL.md`, to notice that a change to it
broke something it used to get right. What to look for is in
[`EVALUATION-RULES.md`](EVALUATION-RULES.md).

This is one half of the net, and a change rarely needs both:

- **one drawing**, the five steps below — half an hour, one provider call. Run it after a change to
  § 1, § 3, § 5, to `references/drawing-the-map.md` or to either template;
- **[three router scenarios](recipe-app/ROUTER-SCENARIOS.md)** — ten minutes and one provider call
  each. Run them after a change to § 2, § 4 or `references/slice-rules.md`, which is where the router
  and the five operations live.

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
everywhere; the steps do not change.

## Before any session

Binding on both halves: the router scenarios start their sessions the same way.

**Install the skill you mean to review.** `make add` copies the payload into `~/.agents/skills/`, and
the agent reads the copy. Skip it and you are reviewing the version before your change. Restart the
agent session afterwards, and check that the copy is the one you expect.

**The skill is invoked explicitly**, as `/roadmap`. It never activates on its own — the frontmatter
sets `disable-model-invocation: true`. Drop the prefix and the candidate is born without the skill,
which means you are reviewing the model instead.

**Model and effort are set in the session, never in the prompt.** Check what the session actually
says before sending, and write down what it said rather than what you intended.

**Every run gets its own directory** under `recipe-app/results/`, and the session is pointed at that
directory as if it were the project. Never point a session at `reference-roadmap/` or at
`fixtures/`: both are frozen and a session writes.

**Every run directory keeps a `PROMPT.md`** holding the exact text sent, every answer given back, and
the model and harness it ran on. Write it from what the session actually received, not from the
template below: a run driven any other way — through a sub-agent, on another harness, with a prompt
you adapted — is still evidence, but only if the adaptation is readable. `recipe-app/results/README.md`
carries the convention and what the 2026-08-20 runs departed from.

**What a session may read** is the sources, and its own copy of `.roadmap/`. Everything else in this
repository is off limits, and the prompt says so. Three things are off limits in particular:
`reference-roadmap/` and its rationale, which are the answer key to a drawing; `EVALUATION-RULES.md`,
`EVALUATION-BRIEF.md` and `recipe-app/ROUTER-SCENARIOS.md`, which are how it will be read; and the
whole of `design/roadmap/`, whose [`WORKFLOWS.md`](../../design/roadmap/WORKFLOWS.md) § 3 is the
answer key to the three router scenarios, verdicts and all.

## Drawing a map: the five steps

1. **Draw one map from `recipe-app/sources/` alone**, in a fresh session with no other context. Send
   the most up-to-date drawing prompt in `PROMPTS.md`, with this run's directory substituted for the
   one it names. What it carries beyond the request is the read restriction the run depends on: the
   sources as the only input, no search that ranges over the rest of the repository, and the same
   restriction on anything the session delegates to.

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
