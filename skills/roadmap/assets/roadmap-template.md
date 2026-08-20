[The readable overview, at `.roadmap/roadmap.md`.]

# Roadmap — [Product or capability]

**Goal:** [The declared goal this map serves, in the words the author would use to say where the
project is going.]

**Sources:** [The documents the map was drawn from.]

**Current state:** [What has been delivered so far and what this drawing stands on; on a first draw,
that nothing has been.]

## Ordering criteria

1. **[Criterion, in a phrase.]** [What it decides about order, and where it loses to another
   criterion.]

[Numbered, because the ranking between the criteria is itself a decision this map takes.]

## Themes

| Theme | Promise | First validator |
|---|---|---|
| `[theme-slug]` | [The promise, in product language: what somebody can do once it holds.] | `[Id of the NOW row that first validates it]` |

## Assumptions

- `[theme or id]` — [Something taken as true in order to draw the map, and that asks to be
  corrected; where the sources contradict each other, which reading was taken and why.]

## Open questions

- `[theme or id]` — [Something that could not be settled and that asks to be answered; it belongs
  here rather than on a row when the answer changes the shape of the map.]

## Cross-functional concerns

- **Authorization.** [Shared rule.]
- **Validation and errors.** [Shared rule.]
- **Operability.** [Logging, observability, timeout, and failure expectations.]
- **Accessibility and security.** [Shared rule.]
- **Data integrity and recovery.** [Invariants, derived data, and partial-failure recovery.]

[Keep all five. Add a further concern — cost, privacy, compliance, latency, auditability, data
migration — only when a source makes it a constraint that several rows must respect; a concern one
row owns stays in it.]

## NOW

| Id | Title | Theme | Kind | Size | Readiness | Executor | Depends on |
|---|---|---|---|---|---|---|---|
| `S<id>` | [Row title](slices/S<id>-<slug>.md) | `[theme-slug]` | `[kind]` | `[size]` | `[readiness]` | `[executor]` | `[ids]` |

[One row per open slice or spike, in delivery order. `Kind` is `product`, `enabler`, `release` or
`spike`; `Size` is `small`, `medium` or `large`; `Readiness` is `ready`, `needs-decision` or
`needs-info`; `Executor` is `agent`, `human` or `mixed`. `Theme` is `—` on a row that serves every
promise and can be cancelled with none, and `goal` on a `kind: spike` row that declares it validates
the goal's feasibility — the one way a spike stands without a dependent naming it in `Depends on`.
`Depends on` holds ids, comma-separated, or `—`. Ids stay plain text in `Id` and in `Depends on`;
the title is the only link, and it is the way into the row's document.]

## LATER

- [One line per candidate: what it would be, and nothing more. No id, no columns, no document.]

## OUT-OF-SCOPE

- **[Excluded capability.]** [Written as the licence it gives: because this is declared unsolved,
  the solution may do without X, and the price it pays for that.]
