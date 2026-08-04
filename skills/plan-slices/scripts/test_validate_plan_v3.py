from __future__ import annotations

import unittest

from validate_plan import parse_plan, validate_structure


PLAN = """\
# Product — Delivery plan

## Ordering criteria

- Validate risk first.

## Themes

| Theme | Desired outcome | First validation |
|---|---|---|
| Search | Users find relevant content. | 1 |

## Cross-functional concerns

- **Authorization:** Scope reads.

## NOW

### 1. Search proof *(Theme: Search)*

---

**Includes**

- A real search path.

**Verification**

- Measure ranked relevance.

**Outcome**

- Testers find content.

## LATER

- None identified.

## OUT-OF-SCOPE

- None identified.
"""


class ValidatePlanV3Tests(unittest.TestCase):
    def test_accepts_numeric_first_validation(self) -> None:
        self.assertEqual(validate_structure(parse_plan(PLAN)), [])

    def test_rejects_missing_or_out_of_range_first_validation(self) -> None:
        missing = PLAN.replace("| 1 |", "| Search proof |")
        out_of_range = PLAN.replace("| 1 |", "| 4 |")

        self.assertTrue(any("must be a NOW slice number" in error for error in validate_structure(parse_plan(missing))))
        self.assertTrue(any("references missing NOW slice 4" in error for error in validate_structure(parse_plan(out_of_range))))

    def test_paraphrases_do_not_change_structural_result(self) -> None:
        paraphrase = PLAN.replace("Search proof", "Retrieval evidence").replace("Measure ranked relevance", "Observe relevance ordering")

        self.assertEqual(validate_structure(parse_plan(paraphrase)), [])


if __name__ == "__main__":
    unittest.main()
