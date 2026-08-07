# Verdicts — cycle CON-6

## Inputs

- **Candidate A:** `CANDIDATE-A.md`
- **Candidate B:** `CANDIDATE-B.md`
- **Rows verified:** 17

## R-001

- **Claim:** The plan places identity after the differentiator.
- **Candidate A:** `falsified`
  - **Citation:** `CANDIDATE-A.md:78-95; CANDIDATE-A.md:121-143`
  - **What it shows:** Google OAuth and the private identity scope ship in slice 2, before semantic-search product validation in slice 4.
- **Candidate B:** `holds`
  - **Citation:** `CANDIDATE-B.md:8-12`
  - **What it shows:** Ordering criteria explicitly defer identity until after capture and semantic search, with identity at slice 9.
- **Watch for:** `no note on this row`

## R-002

- **Claim:** Every choice the plan declares open names the `NOW` slices it blocks, in whatever section it declares it.
- **Candidate A:** `holds`
  - **Citation:** `CANDIDATE-A.md:351-355`
  - **What it shows:** Each open provider, model, and query-strategy choice names a numeric slice or slice range it blocks.
- **Candidate B:** `falsified`
  - **Citation:** `CANDIDATE-B.md:330-332`
  - **What it shows:** The Postgres/driver choice names slice 1, then says it blocks “every subsequent connection verification” instead of naming those `NOW` slices.
- **Watch for:** `no note on this row`

## R-003

- **Claim:** No `NOW` slice depends on an external choice — provider, model, service, or adapter — that is not made by a citable source, or made by the plan among the alternatives the brief declares acceptable, or declared open together with the slice it blocks, in whatever section it declares it; a qualifying adjective — `cheap`, `multilingual`, `managed` — does not count as a choice.
- **Candidate A:** `holds`
  - **Citation:** `CANDIDATE-A.md:345-355`
  - **What it shows:** Postgres/driver, embedding/query strategy, and extraction-LLM selections are assigned pre-slice selection work and declared open with blocked slices.
- **Candidate B:** `holds`
  - **Citation:** `CANDIDATE-B.md:330-335`
  - **What it shows:** Every unresolved external provider/model choice is declared open with the directly blocked `NOW` slice, including the separate runtime-query choice.
- **Watch for:** `no note on this row`

## R-004

- **Claim:** No `NOW` slice delivers a behaviour the sources do not request.
- **Candidate A:** `falsified`
  - **Citation:** `CANDIDATE-A.md:279-282`
  - **What it shows:** Slice 11 requires a reused invitation token to be rejected, introducing single-use invitation behavior not requested by the sources.
- **Candidate B:** `falsified`
  - **Citation:** `CANDIDATE-B.md:262-266`
  - **What it shows:** Slice 10 rejects an already consumed invitation token, introducing single-use invitation behavior not requested by the sources.
- **Watch for:** `no note on this row`

## R-005

- **Claim:** If a `NOW` slice names a failure mode in its own `Verification` and another `NOW` slice is its remedy, no slice of a different theme is placed between the two.
- **Candidate A:** `holds`
  - **Citation:** `CANDIDATE-A.md:11-12`
  - **What it shows:** Ordering criteria keep correction, automatic fallback, and copy-paste remedies contiguous after URL import before another theme opens.
- **Candidate B:** `holds`
  - **Citation:** `CANDIDATE-B.md:8-10`
  - **What it shows:** Ordering criteria explicitly place copy-paste/LLM slice 6 immediately after the URL failure modes in slice 5.
- **Watch for:** `no note on this row`

## R-006

- **Claim:** A pipeline or adapter shared by several paths is opened in the `Includes` of a single `NOW` slice.
- **Candidate A:** `holds`
  - **Citation:** `CANDIDATE-A.md:192-196; CANDIDATE-A.md:216-220`
  - **What it shows:** Slice 7 opens the selected LLM adapter and shared downstream flow; slice 8 explicitly reuses them rather than opening a second adapter.
- **Candidate B:** `holds`
  - **Citation:** `CANDIDATE-B.md:8-10`
  - **What it shows:** Ordering criteria assign each shared adapter one owner, specifically LLM extraction to slice 6 and photos/storage to slice 8.
- **Watch for:** `no note on this row`

## R-007

- **Claim:** No `Enabler` slice validates uncertainties across more than one subsystem: its `Verification` cannot fail for causes that, in the brief's `Material uncertainties`, belong to different `Subsystem`s. Several entries of the same subsystem are one uncertainty, even when the answer invalidates the choice being verified.
- **Candidate A:** `holds`
  - **Citation:** `slice 1 Verification; slice 3 Verification`
  - **What it shows:** Slice 1 tests only delivery-infrastructure concerns; slice 3 tests only semantic-engine quality, latency, cost, and provider failure.
- **Candidate B:** `holds`
  - **Citation:** `slice 1 Verification; slice 3 Verification`
  - **What it shows:** The delivery enabler combines only delivery-infrastructure checks, while the semantic enabler confines verification to semantic-engine behavior and economics.
- **Watch for:** `no note on this row`

## R-008

- **Claim:** Every theme's `First validation` points to a slice whose `Outcome` covers the theme's entire desired outcome.
- **Candidate A:** `falsified`
  - **Citation:** `Themes, row «A. Accesso e scope»; slice 2 Outcome`
  - **What it shows:** Theme A promises that a person accesses and operates only in the current cookbook, but slice 2’s outcome promises only an authenticated person’s persistent private scope for future recipes.
- **Candidate B:** `holds`
  - **Citation:** `Themes, row «D. Estrazione senza structured data»; slice 6 Outcome`
  - **What it shows:** The broadest first-validation mapping resolves: slice 6’s outcome covers saving recipes from sites the link path cannot read, matching the whole extraction-without-structured-data outcome.
- **Watch for:** `no note on this row`

## R-009

- **Claim:** No `Outcome` of a `NOW` slice preceding identity promises a real user: every slice that precedes identity and delivers a behaviour names its own audience, developer or tester on the declared non-public environment.
- **Candidate A:** `holds`
  - **Citation:** `CANDIDATE-A.md:51-95`
  - **What it shows:** Only delivery enablers precede identity in slice 2, and their outcomes name developers rather than real users.
- **Candidate B:** `holds`
  - **Citation:** `CANDIDATE-B.md:8-12`
  - **What it shows:** Ordering criteria explicitly assign all pre-identity evidence to developers/testers on the non-public environment with a configured cookbook scope.
- **Watch for:** `no note on this row`

## R-010

- **Claim:** No `Includes` or `Verification` bullet asserts in non-conditional form one side of an unresolved choice. Unresolved covers a conflict between the sources — those listed under `Known conflicts` in the brief, plus those demonstrable by citing two sources in disagreement — and, in the slices that choice blocks, any other choice the plan does not resolve by citing a selecting source. Declaring the choice under `Open questions` or assigning it a spike does not resolve it.
- **Candidate A:** `holds`
  - **Citation:** `CANDIDATE-A.md:125-135`
  - **What it shows:** Search generates the query vector “according to the open decision”; verification requires cross-language behavior without asserting runtime calls, caching, or precomputation.
- **Candidate B:** `holds`
  - **Citation:** `CANDIDATE-B.md:125-136`
  - **What it shows:** The query path is explicitly conditional on the open decision, and verification measures whichever path is selected without asserting one disputed implementation.
- **Watch for:** `not observed` — `CANDIDATE-A.md:131-135; CANDIDATE-B.md:132-136` still publish concrete relevance, isolation, failure, latency, and cost verification despite the deferred query decision.

## R-011

- **Claim:** Every row of the `Themes` table has its `First validation` resolve to a `NOW` slice not annotated `*(Enabler: …)*`, unless its `Desired outcome` cell carries the `*(Developer outcome)*` marker.
- **Candidate A:** `holds`
  - **Citation:** `CANDIDATE-A.md:14-25`
  - **What it shows:** All eight first validations point to theme slices 2, 4, 5, and 7–11; none points to an enabler.
- **Candidate B:** `holds`
  - **Citation:** `CANDIDATE-B.md:14-25`
  - **What it shows:** All eight first validations point to theme slices 2 and 4–10; none points to an enabler.
- **Watch for:** `not observed` — `CANDIDATE-A.md:16-25; CANDIDATE-B.md:16-25` contain no `*(Developer outcome)*` marker, so neither plan uses it to bypass the rule.

## R-012

- **Claim:** The plan declares under `Cross-functional concerns` the single seam from which the current scope resolves.
- **Candidate A:** `holds`
  - **Citation:** `CANDIDATE-A.md:27-30`
  - **What it shows:** Authorization declares centrally resolved `cookbookId` and membership as the path used by every read and modification.
- **Candidate B:** `holds`
  - **Citation:** `CANDIDATE-B.md:27-30`
  - **What it shows:** Authorization explicitly declares one current-cookbook resolver and identifies it as the seam replaced when authentication arrives.
- **Watch for:** `no note on this row`

## R-013

- **Claim:** Every `LATER` entry states a `Promotion trigger`.
- **Candidate A:** `holds`
  - **Citation:** `CANDIDATE-A.md:308-327`
  - **What it shows:** Each of the six `LATER` entries has its own `Promotion trigger`.
- **Candidate B:** `holds`
  - **Citation:** `CANDIDATE-B.md:292-308`
  - **What it shows:** Each of the five `LATER` entries has its own `Promotion trigger`.
- **Watch for:** `no note on this row`

## R-014

- **Claim:** Every `OUT-OF-SCOPE` entry states an exclusion rationale.
- **Candidate A:** `holds`
  - **Citation:** `CANDIDATE-A.md:329-336`
  - **What it shows:** Every excluded item includes a reason based on scope, accepted duplicates, cost, runtime choice, or proportionality.
- **Candidate B:** `holds`
  - **Citation:** `CANDIDATE-B.md:310-319`
  - **What it shows:** Every excluded item states why it is unnecessary, deliberately rejected, or incompatible with MVP constraints.
- **Watch for:** `no note on this row`

## R-015

- **Claim:** A `NOW` slice that reuses a pipeline or adapter opened by an earlier slice declares it as reuse.
- **Candidate A:** `falsified`
  - **Citation:** `CANDIDATE-A.md:168-173; CANDIDATE-A.md:254-258`
  - **What it shows:** Slice 6 opens Cloudflare R2 for imported photos; slice 10 later uses Cloudflare R2 for photo operations without declaring reuse of that adapter.
- **Candidate B:** `falsified`
  - **Citation:** `CANDIDATE-B.md:102-106; CANDIDATE-B.md:146-157`
  - **What it shows:** Slice 3 opens the real cloud embedding path; slice 5 later generates embeddings and verifies retry behavior without declaring reuse of that earlier adapter/pipeline.
- **Watch for:** `no note on this row`

## R-016

- **Claim:** The `NOW` slice that opens a pipeline or adapter shared by several paths follows every `NOW` slice that feeds it input, except when it validates controlled inputs that traverse the production computation and the scenario's brief admits early validation.
- **Candidate A:** `falsified`
  - **Citation:** `CANDIDATE-A.md:188-220`
  - **What it shows:** Slice 7 opens the shared LLM extraction adapter for URL fallback before slice 8 introduces the pasted-text input that also feeds it; that later input is product behavior, not controlled early validation.
- **Candidate B:** `holds`
  - **Citation:** `CANDIDATE-B.md:8-10; CANDIDATE-B.md:102-106`
  - **What it shows:** Shared owners are ordered after their product input producers; the only early opening is semantic computation on controlled seeded inputs traversing the real cloud and persistence path.
- **Watch for:** The early semantic exception is used only for controlled production-path inputs in `CANDIDATE-B.md:102-106`; A’s violation is a later pasted-text product input in `CANDIDATE-A.md:212-220`.

## R-017

- **Claim:** If more than two `NOW` slices deliver behaviour to an end user before identity, `Ordering criteria` justifies the residual deferral once, naming the evidence that requires it.
- **Candidate A:** `holds`
  - **Citation:** `CANDIDATE-A.md:37-95`
  - **What it shows:** Identity arrives in slice 2 after only two developer-facing delivery enablers, so the more-than-two-behavior threshold is not reached.
- **Candidate B:** `holds`
  - **Citation:** `CANDIDATE-B.md:8-12`
  - **What it shows:** Ordering criteria justify identity’s deferral once: pre-identity evidence does not require real ownership or membership and runs for testers against a configured cookbook on a non-public environment.
- **Watch for:** `no note on this row`
