#!/usr/bin/env python3
"""Tests for paired-comparison contracts and prompt behavior."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from compare_plans import _reject_absolute_names, render_comparison_prompt
from grading_contract import adjudication_reasons, validate_comparison
from test_grade_plan import RUBRIC


def valid_comparison() -> dict[str, object]:
    return {
        "rubric_version": 2,
        "before_candidate": "before.md",
        "after_candidate": "after.md",
        "axes": [
            {
                "id": "themes",
                "criteria": [
                    {
                        "id": "theme_cut",
                        "direction": "same",
                        "resolved_defects": [],
                        "introduced_defects": [],
                        "preserved_passes": ["Independent themes"],
                        "before_evidence": ["Before themes"],
                        "after_evidence": ["After themes"],
                        "confidence": "high",
                    }
                ],
                "net_direction": "same",
                "confidence": "high",
            },
            {
                "id": "slices",
                "criteria": [
                    {
                        "id": "slice_cut",
                        "direction": "better",
                        "resolved_defects": ["adapter-reopened"],
                        "introduced_defects": [],
                        "preserved_passes": [],
                        "before_evidence": ["Split ownership"],
                        "after_evidence": ["Single owner"],
                        "confidence": "high",
                    }
                ],
                "net_direction": "better",
                "confidence": "high",
            },
        ],
        "critical_failures": [],
        "overall_direction": "better",
        "net_rationale": "One isolated defect resolved.",
    }


class ComparePlansTests(unittest.TestCase):
    def test_validates_complete_paired_response(self) -> None:
        validate_comparison(RUBRIC, valid_comparison())

    def test_rejects_missing_criterion(self) -> None:
        comparison = valid_comparison()
        comparison["axes"][1]["criteria"] = []

        with self.assertRaisesRegex(ValueError, "missing"):
            validate_comparison(RUBRIC, comparison)

    def test_prompt_requires_metamorphic_invariance(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paths = [root / name for name in ("source.md", "reference.md", "before.md", "after.md")]
            for path in paths:
                path.write_text(path.stem, encoding="utf-8")

            prompt = render_comparison_prompt(RUBRIC, paths[1], paths[2], paths[3], [paths[0]])

        self.assertIn("Renaming, renumbering", prompt)
        self.assertIn("justified", prompt)
        self.assertIn("only independently affected secondary criteria", prompt)

    def test_rejects_absolute_or_existing_output_names(self) -> None:
        with self.assertRaisesRegex(ValueError, "absolute artifact"):
            _reject_absolute_names([Path("comparison.GRADE.json")])

        with self.assertRaisesRegex(ValueError, "absolute artifact"):
            _reject_absolute_names([Path("comparison.SCORE.old.json")])

        with self.assertRaisesRegex(ValueError, "PAIRED"):
            _reject_absolute_names([Path("comparison.json")])

    def test_adjudication_triggers_cover_documented_thresholds(self) -> None:
        left_comparison = valid_comparison()
        left_comparison["critical_failures"] = [
            {"id": "silent_conflict", "before_present": True, "after_present": False, "evidence": ["Changed"]}
        ]
        left_comparison["axes"][1]["criteria"][0]["confidence"] = "low"
        right_comparison = valid_comparison()
        left_score = {"axes": [{"id": "themes", "score": 1}], "effective_total": 50}
        right_score = {"axes": [{"id": "themes", "score": 3}], "effective_total": 56}

        reasons = adjudication_reasons(
            [left_comparison, right_comparison], [(left_score, right_score)]
        )

        self.assertTrue(any("critical-failure" in reason for reason in reasons))
        self.assertTrue(any("low confidence" in reason for reason in reasons))
        self.assertTrue(any("axis score" in reason for reason in reasons))
        self.assertTrue(any("total-score" in reason for reason in reasons))


if __name__ == "__main__":
    unittest.main()
