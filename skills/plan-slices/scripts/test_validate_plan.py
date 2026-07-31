#!/usr/bin/env python3
"""Regression tests for validate_plan.py."""

from __future__ import annotations

import unittest

from validate_plan import parse_plan, validate_expectations, validate_structure


VALID_PLAN = """\
# Example — Delivery plan

- **Sources:** goal.md
- **Current state:** Documentation only.

## Ordering criteria

- Validate delivery before domain work.

## Themes

| Theme | Desired outcome | First validation |
|---|---|---|
| A. Access | User enters the product. | Login |
| B. Search | User finds relevant content. | Semantic search |

## Cross-functional concerns

- **Authorization:** Enforce access at every boundary.
- **Operability:** Log failures.

## NOW

### 0. Repository setup *(Enabler: delivery)*

---

**Includes**

- Build, lint, typecheck, and tests.

**Verification**

- CI passes from a clean checkout.

**Outcome**

- Developers receive CI feedback.

### 1. Walking skeleton *(Enabler: delivery)*

---

**Includes**

- Build, deploy, and one real page.

**Verification**

- The dev URL returns the page.

**Outcome**

- Developers can inspect the deployed runtime.

### 2. Login *(Theme: A)*

---

**Includes**

- One real identity provider.

**Verification**

- Login and logout work in dev.

**Outcome**

- A user signs in.

### 3. Semantic search *(Theme: B)*

---

**Includes**

- Real query transformation and retrieval.

**Verification**

- A representative query returns the expected fixture.

**Learning / risk**

- Retrieval quality decides the product differentiator.

**Outcome**

- A user finds relevant content.

**Cost**

- One embedding call per indexed document.

## LATER

- **Advanced ranking**
  - **Promotion trigger:** Search evidence shows insufficient ordering.

## OUT-OF-SCOPE

- **Public catalog** — Not part of the private-product strategy.

## Decision checkpoints

- **After semantic search:** Quality evidence → change the retrieval model.
"""


class ValidatePlanTests(unittest.TestCase):
    def test_accepts_valid_plan(self) -> None:
        errors = validate_structure(parse_plan(VALID_PLAN))

        self.assertEqual(errors, [])

    def test_rejects_prose_in_cross_functional_concerns(self) -> None:
        invalid = VALID_PLAN.replace(
            "- **Authorization:** Enforce access at every boundary.",
            "Authorization applies at every boundary.",
        )

        errors = validate_structure(parse_plan(invalid))

        self.assertTrue(any("Cross-functional concerns" in error for error in errors))

    def test_rejects_missing_slice_field(self) -> None:
        invalid = VALID_PLAN.replace(
            "**Verification**\n\n- Login and logout work in dev.\n\n",
            "",
        )

        errors = validate_structure(parse_plan(invalid))

        self.assertTrue(any("NOW slice 2" in error and "Verification" in error for error in errors))

    def test_rejects_missing_rule_after_slice_title(self) -> None:
        invalid = VALID_PLAN.replace("### 2. Login *(Theme: A)*\n\n---\n", "### 2. Login *(Theme: A)*\n")

        errors = validate_structure(parse_plan(invalid))

        self.assertTrue(any("NOW slice 2" in error and "rule" in error for error in errors))

    def test_rejects_out_of_order_slice_fields(self) -> None:
        invalid = VALID_PLAN.replace(
            "**Includes**\n\n- One real identity provider.\n\n"
            "**Verification**\n\n- Login and logout work in dev.\n",
            "**Verification**\n\n- Login and logout work in dev.\n\n"
            "**Includes**\n\n- One real identity provider.\n",
        )

        errors = validate_structure(parse_plan(invalid))

        self.assertTrue(any("NOW slice 2" in error and "order" in error for error in errors))

    def test_rejects_annotation_before_standard_fields(self) -> None:
        invalid = VALID_PLAN.replace(
            "**Includes**\n\n- One real identity provider.\n",
            "**Cost**\n\n- None.\n\n**Includes**\n\n- One real identity provider.\n",
        )

        errors = validate_structure(parse_plan(invalid))

        self.assertTrue(any("annotation 'Cost'" in error for error in errors))

    def test_rejects_removed_why_now_field(self) -> None:
        invalid = VALID_PLAN.replace(
            "**Outcome**\n\n- A user signs in.\n",
            "**Outcome**\n\n- A user signs in.\n\n**Why now**\n\n- Access precedes search.\n",
        )

        errors = validate_structure(parse_plan(invalid))

        self.assertTrue(
            any("NOW slice 2" in error and "Why now" in error for error in errors)
        )

    def test_rejects_removed_dependency_sections(self) -> None:
        invalid = VALID_PLAN + "\n## Hard dependencies\n\n```text\nA\n```\n"

        errors = validate_structure(parse_plan(invalid))

        self.assertTrue(any("legacy section is forbidden: Hard dependencies" in error for error in errors))

    def test_accepts_release_slice(self) -> None:
        plan = VALID_PLAN.replace("*(Theme: B)*", "*(Release: delivery)*")

        errors = validate_structure(parse_plan(plan))

        self.assertEqual(errors, [])

    def test_rejects_non_final_release_slice(self) -> None:
        plan = VALID_PLAN.replace("*(Theme: A)*", "*(Release: delivery)*")

        errors = validate_structure(parse_plan(plan))

        self.assertTrue(any("Release slice must be last" in error for error in errors))

    def test_rejects_unknown_release_type(self) -> None:
        plan = VALID_PLAN.replace("*(Theme: B)*", "*(Release: production)*")

        errors = validate_structure(parse_plan(plan))

        self.assertTrue(any("Release: delivery" in error for error in errors))

    def test_checks_scenario_expectations(self) -> None:
        expectations = {
            "theme_count": 2,
            "themes_contain": ["Access", "Search"],
            "now_title_count": 4,
            "now_titles_in_order": [
                "Repository setup",
                "Walking skeleton",
                "Login",
                "Semantic search",
            ],
            "adjacent_now_titles": [["Login", "Semantic search"]],
            "slice_rules": [
                {
                    "title": "Walking skeleton",
                    "required_patterns": ["deploy"],
                    "forbidden_patterns": ["database"],
                }
            ],
            "later_contains": ["Advanced ranking"],
            "out_of_scope_contains": ["Public catalog"],
            "required_patterns": ["real query transformation"],
            "forbidden_patterns": ["Cross-cutting baseline"],
        }

        errors = validate_expectations(parse_plan(VALID_PLAN), expectations)

        self.assertEqual(errors, [])

    def test_reports_scenario_order_regression(self) -> None:
        expectations = {
            "now_titles_in_order": ["Semantic search", "Login"],
        }

        errors = validate_expectations(parse_plan(VALID_PLAN), expectations)

        self.assertTrue(any("NOW order" in error for error in errors))

    def test_reports_scenario_adjacency_regression(self) -> None:
        expectations = {
            "adjacent_now_titles": [["Walking skeleton", "Semantic search"]],
        }

        errors = validate_expectations(parse_plan(VALID_PLAN), expectations)

        self.assertTrue(any("NOW adjacency" in error for error in errors))

    def test_reports_slice_scoped_regression(self) -> None:
        expectations = {
            "slice_rules": [
                {
                    "title": "Walking skeleton",
                    "forbidden_patterns": ["deploy"],
                }
            ],
        }

        errors = validate_expectations(parse_plan(VALID_PLAN), expectations)

        self.assertTrue(any("NOW slice 1" in error and "forbidden" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
