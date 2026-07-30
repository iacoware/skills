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

**Outcome**

- Developers receive CI feedback.

**Includes**

- Build, lint, typecheck, and tests.

**Verification**

- CI passes from a clean checkout.

### 1. Walking skeleton *(Enabler: delivery)*

**Outcome**

- Developers can inspect the deployed runtime.

**Includes**

- Build, deploy, and one real page.

**Verification**

- The dev URL returns the page.

### 2. Login *(Theme: A)*

**Outcome**

- A user signs in.

**Includes**

- One real identity provider.

**Verification**

- Login and logout work in dev.

### 3. Semantic search *(Theme: B)*

**Outcome**

- A user finds relevant content.

**Includes**

- Real query transformation and retrieval.

**Verification**

- A representative query returns the expected fixture.

## LATER

- **Advanced ranking**
  - **Promotion trigger:** Search evidence shows insufficient ordering.

## OUT-OF-SCOPE

- **Public catalog** — Not part of the private-product strategy.

## Hard dependencies

```text
Repository setup
└── Walking skeleton
```

## Sequencing notes

- **Priority preference:** Login before search — validates access conventions.

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
            "**Verification**\n\n- Login and logout work in dev.\n\n### 3.",
            "### 3.",
        )

        errors = validate_structure(parse_plan(invalid))

        self.assertTrue(any("NOW slice 2" in error and "Verification" in error for error in errors))

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


if __name__ == "__main__":
    unittest.main()
