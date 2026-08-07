# Ledger rows — the claims to verify this cycle

Every row here is one falsifiable claim about a generated delivery plan. Verify **exactly** these:
add none, skip none, merge none. Each claim is stated over a generated plan, never over the text of
the skill that produced it, so it is decided by reading the plan — not by judging it.

The claims are copied verbatim from the ledger. Nothing else of the row travels with them: no
state, no counter, no history, no origin.

`Watch for` is a second thing to look at on that row alone, often the opposite failure from the one
the claim describes. It is reported in its own field, with its own citation, and it **never changes
the verdict**. `—` means the row carries no note.

| Row | Claim | Watch for |
|---|---|---|
| R-001 | The plan places identity after the differentiator. | — |
| R-002 | Every choice the plan declares open names the `NOW` slices it blocks, in whatever section it declares it. | — |
| R-003 | No `NOW` slice depends on an external choice — provider, model, service, or adapter — that is not made by a citable source, or made by the plan among the alternatives the brief declares acceptable, or declared open together with the slice it blocks, in whatever section it declares it; a qualifying adjective — `cheap`, `multilingual`, `managed` — does not count as a choice. | — |
| R-004 | No `NOW` slice delivers a behaviour the sources do not request. | — |
| R-005 | If a `NOW` slice names a failure mode in its own `Verification` and another `NOW` slice is its remedy, no slice of a different theme is placed between the two. | — |
| R-006 | A pipeline or adapter shared by several paths is opened in the `Includes` of a single `NOW` slice. | — |
| R-007 | No `Enabler` slice validates uncertainties across more than one subsystem: its `Verification` cannot fail for causes that, in the brief's `Material uncertainties`, belong to different `Subsystem`s. Several entries of the same subsystem are one uncertainty, even when the answer invalidates the choice being verified. | — |
| R-008 | Every theme's `First validation` points to a slice whose `Outcome` covers the theme's entire desired outcome. | — |
| R-009 | No `Outcome` of a `NOW` slice preceding identity promises a real user: every slice that precedes identity and delivers a behaviour names its own audience, developer or tester on the declared non-public environment. | — |
| R-010 | No `Includes` or `Verification` bullet asserts in non-conditional form one side of an unresolved choice. Unresolved covers a conflict between the sources — those listed under `Known conflicts` in the brief, plus those demonstrable by citing two sources in disagreement — and, in the slices that choice blocks, any other choice the plan does not resolve by citing a selecting source. Declaring the choice under `Open questions` or assigning it a spike does not resolve it. | The failure to look for is not the return of assertive wording but its opposite: a plan that defers everything to a pending decision and publishes nothing verifiable any more. Report it if it appears, with its citation. |
| R-011 | Every row of the `Themes` table has its `First validation` resolve to a `NOW` slice not annotated `*(Enabler: …)*`, unless its `Desired outcome` cell carries the `*(Developer outcome)*` marker. | The marker is declarative: a plan can attach it to a desired outcome that is not a developer's. The failure to look for is the marker attached to get past the rule, not its absence. |
| R-012 | The plan declares under `Cross-functional concerns` the single seam from which the current scope resolves. | — |
| R-013 | Every `LATER` entry states a `Promotion trigger`. | — |
| R-014 | Every `OUT-OF-SCOPE` entry states an exclusion rationale. | — |
| R-015 | A `NOW` slice that reuses a pipeline or adapter opened by an earlier slice declares it as reuse. | — |
| R-016 | The `NOW` slice that opens a pipeline or adapter shared by several paths follows every `NOW` slice that feeds it input, except when it validates controlled inputs that traverse the production computation and the scenario's brief admits early validation. | The exception resolves to `EVALUATION-BRIEF.md` § `Accepted alternatives`, not to the skill's own text. |
| R-017 | If more than two `NOW` slices deliver behaviour to an end user before identity, `Ordering criteria` justifies the residual deferral once, naming the evidence that requires it. | — |

Rows in this file: **17**.
