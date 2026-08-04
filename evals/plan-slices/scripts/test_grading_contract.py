#!/usr/bin/env python3
"""Tests for criterion contracts and deterministic scoring."""

from __future__ import annotations

import unittest

from grading_contract import absolute_grade_schema, score_grade
from test_grade_plan import RUBRIC, valid_grade


class GradingContractTests(unittest.TestCase):
    def test_derives_axis_score_from_worst_criterion(self) -> None:
        result = score_grade(RUBRIC, valid_grade())

        self.assertEqual([axis["score"] for axis in result["axes"]], [4, 2])
        self.assertEqual(result["raw_total"], 80.0)

    def test_derives_every_verdict_score(self) -> None:
        for verdict, expected in (("pass", 4), ("minor", 3), ("material", 2), ("severe", 1), ("absent", 0)):
            grade = valid_grade()
            criterion = grade["axes"][1]["criteria"][0]
            defect = grade["defects"][0]
            criterion["verdict"] = verdict
            defect["severity"] = "minor" if verdict == "pass" else verdict
            if verdict == "pass":
                criterion["defect_ids"] = []
                grade["axes"][1]["defects_regressions"] = []
                grade["axes"][1]["material_passes"] = ["slice_cut"]
                grade["defects"] = []

            self.assertEqual(score_grade(RUBRIC, grade)["axes"][1]["score"], expected)

    def test_applies_critical_failure_cap_independently(self) -> None:
        grade = valid_grade()
        grade["critical_failures"] = [{"id": "silent_conflict", "evidence": ["Omitted"]}]

        result = score_grade(RUBRIC, grade)

        self.assertEqual(result["raw_total"], 80.0)
        self.assertEqual(result["effective_total"], 59)

    def test_rejects_missing_axis(self) -> None:
        grade = valid_grade()
        grade["axes"] = grade["axes"][:1]

        with self.assertRaisesRegex(ValueError, "axes mismatch"):
            score_grade(RUBRIC, grade)

    def test_rejects_duplicate_criterion(self) -> None:
        grade = valid_grade()
        grade["axes"][1]["criteria"][0]["id"] = "theme_cut"

        with self.assertRaisesRegex(ValueError, "duplicate"):
            score_grade(RUBRIC, grade)

    def test_rejects_unknown_defect_axis_criterion_and_severity(self) -> None:
        mutations = (
            ("primary_axis", "unknown", "primary axis"),
            ("criterion_ids", ["unknown"], "unknown criteria"),
            ("severity", "catastrophic", "unknown severity"),
        )
        for field, value, message in mutations:
            grade = valid_grade()
            grade["defects"][0][field] = value

            with self.assertRaisesRegex(ValueError, message):
                score_grade(RUBRIC, grade)

    def test_rejects_dangling_defect_reference(self) -> None:
        grade = valid_grade()
        grade["axes"][1]["criteria"][0]["defect_ids"] = ["unknown"]

        with self.assertRaisesRegex(ValueError, "dangling"):
            score_grade(RUBRIC, grade)

    def test_rejects_defect_severity_that_disagrees_with_verdict(self) -> None:
        grade = valid_grade()
        grade["defects"][0]["severity"] = "severe"

        with self.assertRaisesRegex(ValueError, "severity must match"):
            score_grade(RUBRIC, grade)

    def test_rejects_non_material_secondary_effect(self) -> None:
        grade = valid_grade()
        grade["defects"][0]["criterion_ids"] = ["slice_cut", "theme_cut"]
        grade["axes"][0]["criteria"][0] = {
            "id": "theme_cut", "verdict": "minor", "evidence": ["Themes"], "defect_ids": ["split"]
        }
        grade["axes"][0]["material_passes"] = []
        grade["axes"][0]["defects_regressions"] = ["split"]

        with self.assertRaisesRegex(ValueError, "secondary defect effect"):
            score_grade(RUBRIC, grade)

    def test_schema_omits_model_selected_axis_score(self) -> None:
        schema = absolute_grade_schema(RUBRIC)
        axis_schema = schema["properties"]["axes"]["items"]["anyOf"][0]

        self.assertNotIn("score", axis_schema["properties"])


if __name__ == "__main__":
    unittest.main()
