# Reference plan — why each slice sits where it sits

`SKILL.md` § 5 forbids publishing per-slice ordering rationale, so this reasoning cannot live in
`REFERENCE-PLAN.md`: there, the slice order and `Ordering criteria` carry it silently. It lives here
because step 5 of `../MANUAL-REVIEW.md` asks, on every difference between candidate and reference,
which of the two has the better reason — and a reason you have to re-derive from the sources is a
reason you will not weigh.

Read it after the reference, never before the candidate. Where this table and `sources/` diverge,
the defect is here.

| Slice | Why there |
|---|---|
| 0. Repository e CI | Establishes the review cadence before there is any code to review. |
| 1. Walking skeleton | Proves the decided infrastructure is connected on the thinnest possible path, before a connection failure can be mistaken for a domain failure. |
| 2. Contesto del ricettario | First persistence, and first human review of domain, scope, ORM, UI and test conventions on minimal behaviour; Postgres is already proven by slice 1, and this slice is not a dependency of search. |
| 3. Pipeline di indicizzazione | The cheapest input capable of validating the risky engine, without waiting for the add slices. |
| 4. Ricerca semantica | The existential risk, validated as soon as the pipeline makes it observable. |
| 5. Lettura della ricetta | Completes the Consultazione theme on real content and serves every later theme, while staying tiny. |
| 6. Accesso Google | The scope resolver moves from configured to authenticated before the product reaches real users; from here every slice is shippable. |
| 7. Inserimento manuale | Establishes the shared form and the save-and-reindex path that every import slice reuses as its correction surface. |
| 8. Import da URL | The most frequent acquisition case and the free path, before any variable cost. |
| 9. Fallback LLM | The second differentiator, right after the free path that bounds its use. |
| 10. Testo incollato | Closes the Import automatico theme by reusing the engine and schema of slice 9, opening no new adapter. |
| 11. Foto | Several inputs into one media pipeline, opened once, when text acquisition is closed. |
| 12. Invito | Last theme, and the only one that requires identity to already exist. |
| 13. Rilascio | Without it NOW never reaches the users it names, and the cost constraint is never measured in the field. |
