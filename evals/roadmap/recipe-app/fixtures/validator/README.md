# Validator fixtures

One minimal mutation of the reference roadmap per check in
[`skills/roadmap/scripts/validate_roadmap.ts`](../../../../../skills/roadmap/scripts/validate_roadmap.ts).
`validate_roadmap.test.ts` reads them, applies each one to the oracle in memory, and asserts that the
validator goes red and says why.

A fixture is the mutation, not a copy of the map. A copy would drift the moment the oracle changed
and would keep passing for the wrong reason; a mutation cannot, because every `find` has to match the
oracle exactly once or the test fails on the fixture itself.

```jsonc
{
  "check": "what the fixture breaks, in a phrase",
  "edits": [{ "in": "roadmap.md", "find": "…", "replace": "…" }],  // optional
  "remove": ["slices/S5-elenco-e-lettura.md"],                     // optional
  "add": { "archive/S3-…md": "…" },                                // optional
  "expect": "the substring every reported error has to carry"
}
```

`expect` is asserted against **every** error the mutation produces, which is what keeps the mutations
minimal: a fixture that breaks two things at once fails here.
