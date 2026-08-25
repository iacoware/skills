# Context Map

Questo repo pubblica agent skill: ogni skill che sviluppa un vocabolario proprio tiene il suo
`CONTEXT.md` accanto ai documenti di design, non nel payload installato.

## Contexts

- [Roadmap](./design/roadmap/CONTEXT.md) — l'artefatto vivente che decide cosa fare dopo: roadmap,
  register, slice, candidate, orizzonti. Il razionale sta in
  [`ROADMAP-GOAL.md`](./design/roadmap/ROADMAP-GOAL.md), che è l'autorità. La skill che lo parla è
  [`skills/roadmap`](./skills/roadmap): il router in [`SKILL.md`](./skills/roadmap/SKILL.md), dove
  *Choose the door* dice quale ramo prende una sessione, le regole in
  [`references/`](./skills/roadmap/references), il validator in
  [`scripts/validate_roadmap.ts`](./skills/roadmap/scripts/validate_roadmap.ts).

## Relationships

- **Roadmap → catena installata**: la roadmap consegna una slice a `to-spec` attraverso una
  conversazione, non un file; `to-tickets` e `implement` seguono. I termini di quella catena — spec,
  issue, ticket, i cinque ruoli di `triage` — sono definiti dalle skill installate e non vanno
  ridefiniti qui.
