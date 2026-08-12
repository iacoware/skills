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

    def test_accepts_first_validation_carrying_the_slice_title(self) -> None:
        for cell in ("1. Search proof", "1) Search proof", "NOW slice 1"):
            with self.subTest(cell=cell):
                self.assertEqual(validate_structure(parse_plan(PLAN.replace("| 1 |", f"| {cell} |"))), [])

    def test_rejects_missing_or_out_of_range_first_validation(self) -> None:
        missing = PLAN.replace("| 1 |", "| Search proof |")
        out_of_range = PLAN.replace("| 1 |", "| 4. Search proof |")

        self.assertTrue(any("must start with a NOW slice number" in error for error in validate_structure(parse_plan(missing))))
        self.assertTrue(any("references missing NOW slice 4" in error for error in validate_structure(parse_plan(out_of_range))))

    def test_rejects_enabler_first_validation_without_the_developer_outcome_marker(self) -> None:
        enabler = PLAN.replace("*(Theme: Search)*", "*(Enabler: search)*")

        errors = validate_structure(parse_plan(enabler))

        self.assertTrue(any("is an Enabler slice" in error for error in errors))

    def test_accepts_enabler_first_validation_when_the_desired_outcome_is_marked(self) -> None:
        marked = PLAN.replace("*(Theme: Search)*", "*(Enabler: search)*").replace(
            "Users find relevant content.",
            "Developers get executable evidence. *(Developer outcome)*",
        )

        self.assertEqual(validate_structure(parse_plan(marked)), [])

    def test_paraphrases_do_not_change_structural_result(self) -> None:
        paraphrase = PLAN.replace("Search proof", "Retrieval evidence").replace("Measure ranked relevance", "Observe relevance ordering")

        self.assertEqual(validate_structure(parse_plan(paraphrase)), [])


if __name__ == "__main__":
    unittest.main()
