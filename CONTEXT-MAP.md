# Context Map

Questo repo pubblica agent skill: ogni skill che sviluppa un vocabolario proprio tiene il suo
`CONTEXT.md` accanto ai documenti di design, non nel payload installato.

## Contexts

- [Roadmap](./design/roadmap/CONTEXT.md) — l'artefatto vivente che decide cosa fare dopo: roadmap,
  register, slice, candidate, orizzonti. Il razionale sta in
  [`ROADMAP-GOAL.md`](./design/roadmap/ROADMAP-GOAL.md), che è l'autorità; tre sessioni camminate per
  intero su `recipe-app` stanno in [`WORKFLOWS.md`](./design/roadmap/WORKFLOWS.md) e illustrano
  soltanto; [`PLAN-INPUTS.md`](./design/roadmap/PLAN-INPUTS.md) raccoglie ciò che appartiene al piano
  implementativo. La skill che lo parla è [`skills/roadmap`](./skills/roadmap): il router in
  [`SKILL.md`](./skills/roadmap/SKILL.md), le regole in
  [`references/`](./skills/roadmap/references), il validator in
  [`scripts/validate_roadmap.ts`](./skills/roadmap/scripts/validate_roadmap.ts).

## Relationships

- **Roadmap → catena installata**: la roadmap consegna una slice a `to-spec` attraverso una
  conversazione, non un file; `to-tickets` e `implement` seguono. I termini di quella catena — spec,
  issue, ticket, i cinque ruoli di `triage` — sono definiti dalle skill installate e non vanno
  ridefiniti qui.
- **Roadmap → `plan-slices`**: `plan-slices` è la skill che la roadmap sostituisce. Dal 2026-08-20 è
  marcata deprecata in `README.md` e nel corpo del suo `SKILL.md`; non è stata rimossa e resta
  installabile, e `evals/plan-slices/` resta il metro con cui si leggono le prime roadmap.
  Non ha un contesto proprio; la sua unità si chiama *plan slice* quando i due documenti si toccano.
