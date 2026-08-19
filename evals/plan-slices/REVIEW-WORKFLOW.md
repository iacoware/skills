# Review workflow

How to run one review of a plan produced by `skills/plan-slices/SKILL.md`, to notice that a change
to the skill broke something it used to get right. What to look for is in `EVALUATION-RULES.md`.

Half an hour, one provider call. Run it after a change you believe is substantive — not after every
commit, since a net you skip is worse than a net you sized honestly.

The steps below use `recipe-app`, today's only scenario. With a second one, substitute its directory
everywhere; the rules do not change.

1. Generate one plan from `recipe-app/sources/` alone, in a fresh session with no other context.

   The skill is **invoked explicitly** — `/plan-slices` on Claude Code, `$plan-slices` on Codex.
   Neither harness activates it on its own: `skills/plan-slices/agents/openai.yaml` sets
   `allow_implicit_invocation: false` and the skill's frontmatter sets
   `disable-model-invocation: true`. Drop the prefix and the candidate is born without the skill,
   which means you are reviewing the model instead.

   **Claude Code**, one message, replacing `<N>`:

   ```
   /plan-slices Read the markdown documents in @evals/plan-slices/recipe-app/sources/, starting from @evals/plan-slices/recipe-app/sources/goal.md, and produce a high-level delivery plan cut into slices. Write it to evals/plan-slices/recipe-app/results/PLAN-CC-<N>.md. Read nothing else in this repository, in this session or in any session you delegate to: the sources are the only input, and the existing plans under results/ are off limits.
   ```

   **Codex**, one message:

   ```
   $plan-slices Read the markdown documents in evals/plan-slices/recipe-app/sources/, starting from evals/plan-slices/recipe-app/sources/goal.md, and produce a high-level delivery plan cut into slices. Write it to evals/plan-slices/recipe-app/results/PLAN-CX-<N>.md. Read nothing else in this repository, in this session or in any session you delegate to: the sources are the only input, and the existing plans under results/ are off limits.
   ```

   The two differ only in the `@` prefixes, Claude Code's file-reference syntax, which has no Codex
   equivalent. Model and effort are set in the session, never in the prompt: check what the session
   actually says before sending, and write down what it said rather than what you intended.
2. `make validate PLAN=<path>` from the repository root — structural, deterministic, free. `PLAN`
   is a path, not a bare filename: `make validate PLAN=evals/plan-slices/recipe-app/results/PLAN-CC-CON-7.md`.
   If it is red, stop and fix before reading.
3. Read the plan against `recipe-app/EVALUATION-BRIEF.md`, opening `sources/` only to verify a
   citation. **The brief is the authority**, not the sources: it decides which conflicts exist,
   which alternatives are accepted, which uncertainties are material. Skipping this step is how the
   retired ledger used to produce false positives. Its entries carry ids — cite them, in notes and
   in the report, instead of paraphrasing what they say.
4. Walk `EVALUATION-RULES.md`, keeping the brief's uncertainty table open for R-007.
5. **Only now** open `recipe-app/REFERENCE-PLAN.md`, and its rationale, and compare. Forming your
   verdict first is what keeps the reference a memory aid instead of a diff target — the order is
   the whole discipline. What you are hunting is what you forgot, not what you did differently.

   The reference was hand-written from the sources before any candidate existed, and is frozen: it
   is rewritten only when the sources change, never because a candidate convinced. How binding each
   part of it is:

   - Where reference and `sources/` diverge, the defect is in the reference.
   - Titles, numbering, theme count, order and worked detail may all differ. On each difference, ask
     which of the two has the better reason — the rationale file holds the reference's.
   - Each `Verification` bullet illustrates how a slice could be demonstrated; it is one way, not
     the only one. The same holds for the operational detail of `Cross-functional concerns`, whose
     six entries are owed but not their wording, and for `Decision checkpoints`, which are advice
     rather than an exact precedence.
   - A source may support a `LATER` or `OUT-OF-SCOPE` classification other than the reference's.
