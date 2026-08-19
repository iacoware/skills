# Roadmap workflows — worked examples

Three sessions of the `roadmap` skill, walked end to end on the `recipe-app` scenario. They exist
because prose hides decisions that a story forces into the open: writing the redraw below is what
produced the rule that an exclusion contradicted by a new goal has to be lifted deliberately, and the
observation that the id counter does not restart. Neither was in the design document until an example
went looking for them.

Three things about how to read and maintain this file:

**`ROADMAP-GOAL.md` is the authority; this file illustrates.** Where the two disagree, the design
document wins and the disagreement is a bug in the example. Nothing here is normative, and no rule
should exist only here — if an example needs a rule the design document does not state, the rule goes
there first.

**These are examples of decisions, not of syntax.** No register tables, no rendered slice documents,
no file listings. An example that draws the artifact breaks on the first column that changes; an
example that says *`S9` keeps its id, `S12` is retired, and here is why* survives almost any change of
format. The format contract lives in the template, and the template is checked by the validator.

**The scenario material is `evals/plan-slices/recipe-app/sources/`** — `goal.md`, `concepts.md`,
`arch-choices.md`, `tech-choices.md` — and not `REFERENCE-PLAN.md`, which is `plan-slices` output and
dies with it. Where an example needs a starting state, it recaps it in a few lines rather than
pointing at that plan. When `evals/roadmap/` lands with its own `sources/` and `results/`, these three
examples are the seed its scenarios are derived from.

The slice ids below are roadmap ids, minted in the order the map was drawn. They are not the position
numbers `plan-slices` used, even where the underlying work is recognisably the same.

## 1. A session of re-truing

**Where we are.** The goal is the MVP one: a cookbook shared between family and friends, where a
recipe is found by describing it, across languages. `S0`–`S7` are delivered and archived — repository
and CI, walking skeleton, the embedding pipeline, cross-language semantic search, reading a recipe,
Google sign-in, manual entry, import from a URL with JSON-LD. `NOW` holds `S8`–`S13`, and `S8` — the
LLM fallback for pages without structured data — has just been finished but not yet closed out.

**The author arrives with a situation, not a verb**: *S8 is done. The JSON-LD hit rate on the sites we
actually use came out at 55%, far below what we assumed. And I want recipes extracted from a
screenshot — nobody had thought of it.*

Three operations are in there. The skill finds them; the author does not name them.

**Close-out runs first**, because everything else is decided against a register that is already true.
`S8`'s row leaves the register, its document moves to `.roadmap/archive/`, and its `ADRs` reference is
filled if the work produced a decision that cleared the bar — hard to reverse, surprising without
context, the result of a real trade-off.

Then *absorb the evidence*, which is the vaguest phrase in the design document and means three
specific things, none of them a summary:

- **Does it settle an open assumption?** `Assumptions and gaps` carried *assumed — JSON-LD covers the
  sites the pilot users actually paste*. Delivery refuted it at 55%. The line does not get annotated,
  it dies: it has been answered.
- **Does it change another row?** This is where the value is. `S9` was sized `small` on the assumption
  the LLM fallback was an edge case. At 55% it is the main path, so its size is wrong and its
  readiness is now questionable.
- **Does it unblock anything?** A `needs-decision` elsewhere that this delivery just decided, a
  `Depends on` that is now moot.

Absorption is a state change on other rows. When it produces no state change anywhere, it produced
nothing, and writing a paragraph to prove otherwise is the ceremony this tool refuses.

**Revision, second**, because close-out just exposed it. `S8`'s learning target was *does JSON-LD
carry the sites we care about*, and the answer reshapes `S9`. `S9` bundled two things that were one
thing while the fallback looked marginal: LLM extraction from unstructured HTML, and the paste path
for pages that cannot be fetched at all — paywalls, JS-heavy sites. Split. `S9` **keeps its id**,
because it keeps the learning target — *an LLM extracts a recipe from unstructured HTML within
budget* — and the paste path is minted as `S14`. Anything pointing at `S9` in a `Depends on` still
resolves, which is the whole reason identity follows the learning target rather than the split.

**Admission, last.** Screenshot extraction. Two questions, in order.

*Does it serve the goal?* Yes — it is a fourth way to get a recipe in, next to URL, paste and manual
entry. If it did not, it would be an `OUT-OF-SCOPE` line or nothing at all.

*Is it on the path, or is it speculation?* The goal is already reachable without it: URL import and
paste cover adding a recipe. So it enters `LATER`, as **a line with no id and no document**. The pull
to give it a document is exactly what the rule forbids — a document invites specifying, and a
candidate is vague on purpose. It has no `Requested by` either, because it has nothing to carry one:
provenance is recorded when it is promoted, not before.

The other branch is worth seeing, because it is the same input with different evidence. Had the author
said *the pilot users photograph pages out of paper cookbooks and paste is useless to them*, the
capability would be on the path, and it would be admitted straight into `NOW`: next id `S15`, and
`Requested by: S8`, since what made it visible was a delivered slice and not a source document. Then
the cap gets checked — `NOW` would go from six rows to seven, comfortably inside it, so nothing is
forced out. Had it been at nineteen, something would have had to merge or go back to `LATER`, and that
pressure is the point.

**One block, one confirmation.** The three operations are proposed together — close `S8`, kill the
JSON-LD assumption, resize and split `S9` into `S9` + `S14`, file screenshot extraction as a
candidate — and the author confirms once. Not five files written one at a time with a question
between each.

**Then the coverage question**, which runs every session: does what is left in `NOW` still reach the
goal? Here yes, and the answer takes one line. It is asked anyway, because it is also the trigger that
catches the case in example 3.

## 2. A redraw

**Where we are.** The MVP goal is reached. `S0`–`S13` are delivered and archived, `NOW` is empty.

**The author arrives with:** *public themed cookbooks are the product — anyone should be able to
discover and read one without being invited.*

This is a claim about the destination, not the path. It contradicts the recorded goal on two points
that are not details: *scope: the current cookbook only*, and *being a member means reading and
editing everything*. So the map is drawn again.

**Redrawn from nothing.** The `Goal` line, replaced. The **themes**: the seven MVP themes — semantic
search, automatic import, browsing, manual entry, photos, authentication, sharing — are promises that
were *kept*, not promises left open, so they do not carry. The new ones are different: *discovery*
(finding a cookbook that is not mine), *publication* (making a cookbook public without losing control
of it), each with its first validator recomputed. The **ordering criteria**: the old ones read
*minimum delivery path first, then conventions, then existential risk*, which are greenfield criteria,
and repository, CI and skeleton now exist; the new ones start from a different risk, the public read
boundary, which is a security surface that did not exist before. The **register**: emptied, refilled
with the slices that reach the new goal — and the first of them is **`S14`, not `S0`**, because the
archive reaches `S13` and the counter does not go back. **`Assumptions and gaps`**: recomputed. The
old entries died of delivery — *query embedding at runtime*, *Postgres provider* — and new ones
appear, such as *assumed: a public cookbook is read-only for non-members*, which the new goal does not
say.

**Carried over, and this is where a redraw earns its keep over deleting the directory.**

`archive/` is untouched. It is the only durable record that CI, the skeleton and semantic search
already exist, because the tracker has no notion of *done*. Drawing without it means drawing as if the
project had never started.

`OUT-OF-SCOPE` carries, and one of its entries now has to move. It reads *granular roles and
permissions: for the MVP `creatorId` is enough and all members are equal* — and that exclusion was the
**licence** for a trade-off that is already in production. The new goal contradicts it: a public
cookbook needs at least a non-member who can read. So it is lifted **explicitly**, and lifting it is
what makes visible that there is a bill to pay on shipped code. Redraw blind and you reinvent a
permission model without noticing you are contradicting a decision that was made on purpose.
Meanwhile *structured ingredients* stays excluded, untouched: the new goal does not reach it.

`Cross-functional concerns` carries for the same reason. Its authorization invariant says *an id out
of scope answers 404*, and the new goal breaks it — a public cookbook must answer 200 to a stranger.
It survives as a constraint to be amended deliberately, not as something to rediscover.

`LATER` survives as a file and not as a reading. Every candidate is re-read, one at a time, and gets a
verdict:

- *public themed cookbooks* — no longer a candidate; it **is** the goal;
- *cross-cookbook search* — was speculation about someone with several private cookbooks; under a
  discovery goal it is central, and it is **promoted**;
- *always-warm Fly machine* — the cold-start argument changes under public, anonymous traffic;
  **re-decided**, possibly into `NOW`;
- *group concept above cookbooks*, *passkeys* — **kept** as candidates;
- *manual cover choice*, *which photos to keep on import* — refinements of delivered work that the new
  goal does not need; kept or killed, but **somebody decides**.

A candidate that survives without being re-read is one nobody chose, and `LATER` is a focus tool whose
focus is relative to a goal.

**The variant mid-flight.** Had the goal changed with `NOW` still full — say after `S9`, with
`S10`–`S13` open — one thing differs: those four do not carry automatically. Each is re-justified
against the new goal. *Invitation and equal collaboration* still serves publication, so it stays and
**keeps its id**; whatever does not serve the new goal is retired, dead or demoted to candidate.

## 3. Two inputs the router can get wrong

The rule is that a claim about **where we are going** redraws the map and a claim about **how we get
there** is work, with work as the default. These two are the cases where reading the rule off the
input is hardest, and they are the ones the eval scenarios exist to hold.

**Sounds like a change of destination, is work.** *Search has to work across every cookbook I belong
to, not just the current one.* It reads like a scope change, and scope changes sound structural. But
the recorded goal is that a recipe is found by describing it; **which** cookbooks are in scope is a
detail of the path, not a different destination. And this exact capability is already sitting in
`LATER` as a candidate. So it is a promotion, and nothing about the goal moves.

**Sounds like work, is a change of destination.** *Let us add a `visibility=public` flag on Cookbook —
it is already modelled anyway.* One column, one afternoon, and `concepts.md` really does say the model
is ready for it. Admitting it as a slice would be the natural move. It is also wrong: it moves the
product from an invited group to the open web, and it contradicts both the authorization invariant and
the granular-permissions exclusion, neither of which a one-line feature is entitled to overrule.

The tell is worth stating plainly, because it is the trap: **how cheap something is to implement says
nothing about whether it moves the destination.** The cost of the change and the altitude of the
change are unrelated, and the roadmap only cares about the second.

**In both cases the skill does not decide.** It states the goal it has on file, says what the input
looks like from where it sits, and asks which of the two holds. The coverage question is what surfaces
it: when what the author brings cannot be reconciled with the recorded goal — it does not serve it,
and it is not an exclusion either — that is the moment to ask, and the answer is one sentence long.

And when the router does get it wrong, the cost is bounded. Every branch ends in a proposed block of
changes and a single confirmation, so a wrong turn costs a proposal, not a record: the author reads a
whole new map where three adjustments were wanted, and says no.
