#!/usr/bin/env python3
"""Tests for absolute prompt composition and execution."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from grade_plan import render_prompt, run_grader


RUBRIC = {
    "version": 2,
    "verdict_scores": {"pass": 4, "minor": 3, "material": 2, "severe": 1, "absent": 0},
    "axes": [
        {"id": "themes", "weight": 60, "criteria": [{"id": "theme_cut", "text": "Cut themes"}]},
        {"id": "slices", "weight": 40, "criteria": [{"id": "slice_cut", "text": "Cut slices"}]},
    ],
    "critical_failures": [{"id": "silent_conflict", "score_cap": 59}],
}


def valid_grade(candidate: str = "PLAN.md") -> dict[str, object]:
    return {
        "rubric_version": 2,
        "candidate": candidate,
        "axes": [
            {
                "id": "themes",
                "criteria": [{"id": "theme_cut", "verdict": "pass", "evidence": ["Themes"], "defect_ids": []}],
                "material_passes": ["theme_cut"],
                "defects_regressions": [],
                "net_rationale": "Complete",
                "confidence": "high",
            },
            {
                "id": "slices",
                "criteria": [{"id": "slice_cut", "verdict": "material", "evidence": ["NOW"], "defect_ids": ["split"]}],
                "material_passes": [],
                "defects_regressions": ["split"],
                "net_rationale": "One material defect",
                "confidence": "medium",
            },
        ],
        "defects": [
            {
                "id": "split",
                "primary_axis": "slices",
                "severity": "material",
                "criterion_ids": ["slice_cut"],
                "evidence": ["NOW"],
            }
        ],
        "critical_failures": [],
    }


class GradePlanTests(unittest.TestCase):
    def test_prompt_renders_all_reference_authority_classes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.md"
            reference = root / "reference.md"
            plan = root / "plan.md"
            source.write_text("SOURCE", encoding="utf-8")
            reference.write_text("HARD CONSTRAINTS\nPREFERRED DECOMPOSITION\nACCEPTED ALTERNATIVES\nEXAMPLE EVIDENCE", encoding="utf-8")
            plan.write_text("PLAN", encoding="utf-8")

            prompt = render_prompt(RUBRIC, reference, plan, [source])

        self.assertLess(prompt.index("Product sources define"), prompt.index("Reference HARD"))
        self.assertIn("PREFERRED DECOMPOSITION is advisory", prompt)
        self.assertIn("ACCEPTED ALTERNATIVES", prompt)
        self.assertIn("EXAMPLE EVIDENCE", prompt)
        self.assertNotIn('"score":', prompt)

    def test_prompt_states_defect_severity_invariant(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.md"
            reference = root / "reference.md"
            plan = root / "plan.md"
            for path in (source, reference, plan):
                path.write_text(path.stem, encoding="utf-8")

            prompt = render_prompt(RUBRIC, reference, plan, [source])

        self.assertIn("severity exactly to the lowest-scoring verdict", prompt)
        self.assertIn("criterion with that verdict must belong", prompt)

    def test_run_records_complete_reproducibility_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            rubric_path = root / "rubric.json"
            source = root / "source.md"
            reference = root / "reference.md"
            plan = root / "plan.md"
            rubric_path.write_text("{}", encoding="utf-8")
            source.write_text("SOURCE", encoding="utf-8")
            reference.write_text("REFERENCE", encoding="utf-8")
            plan.write_text("PLAN", encoding="utf-8")

            with patch(
                "grade_plan.run_provider",
                return_value=(valid_grade(str(plan)), "codex 1.2.3"),
            ):
                grade, score = run_grader(
                    "codex", RUBRIC, rubric_path, reference, plan, [source],
                    "gpt-5.6-sol", "high", ["foo=true"], 30,
                    "run-1", "2026-08-03T00:00:00+00:00", "abc123",
                )

        metadata = score["grader"]
        self.assertEqual(metadata["requested_model"], "gpt-5.6-sol")
        self.assertEqual(metadata["effort"], "high")
        self.assertEqual(metadata["configuration"], ["foo=true"])
        self.assertEqual(metadata["cli_version"], "codex 1.2.3")
        self.assertIn("prompt_sha256", metadata)
        self.assertIn("source_sha256", metadata)
        self.assertIn("reference_sha256", metadata)
        self.assertIn("rubric_sha256", metadata)
        self.assertEqual(metadata["candidates"][0]["path"], str(plan))
        self.assertEqual(metadata["candidates"][0]["skill_commit"], "abc123")
        self.assertEqual(metadata["run_id"], "run-1")
        self.assertEqual(grade["grader"], metadata)

    def test_run_rejects_provider_candidate_substitution(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paths = [root / name for name in ("rubric.json", "reference.md", "plan.md", "source.md")]
            for path in paths:
                path.write_text("{}" if path.suffix == ".json" else path.stem, encoding="utf-8")

            with (
                patch("grade_plan.run_provider", return_value=(valid_grade("other.md"), "codex 1")),
                self.assertRaisesRegex(ValueError, "candidate mismatch"),
            ):
                run_grader(
                    "codex",
                    RUBRIC,
                    paths[0],
                    paths[1],
                    paths[2],
                    [paths[3]],
                    "gpt-5.6-sol",
                    "high",
                    [],
                    30,
                )


if __name__ == "__main__":
    unittest.main()
