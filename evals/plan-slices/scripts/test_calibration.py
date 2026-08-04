#!/usr/bin/env python3
"""Tests for immutable fixtures and non-gating calibration reports."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

from calibration_report import build_report
from grade_plan import load_object


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "skills" / "plan-slices" / "scripts"))
from validate_plan import parse_plan, validate_expectations, validate_structure  # noqa: E402


class CalibrationTests(unittest.TestCase):
    def test_manifest_paths_exist_and_ids_are_unique(self) -> None:
        fixture_dir = Path(__file__).resolve().parents[1] / "fixtures"
        manifest = load_object(fixture_dir / "manifest.json")
        fixtures = manifest["fixtures"]
        ids = [fixture["id"] for fixture in fixtures]

        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all((fixture_dir / fixture["path"]).is_file() for fixture in fixtures))

    def test_reference_aligned_and_alternative_fixtures_are_structurally_valid(self) -> None:
        fixture_dir = Path(__file__).resolve().parents[1] / "fixtures"
        for name in ("strong-reference-aligned.md", "source-supported-alternative.md"):
            plan = parse_plan((fixture_dir / name).read_text(encoding="utf-8"))

            self.assertEqual(validate_structure(plan), [], name)

    def test_source_supported_alternative_passes_hard_expectations(self) -> None:
        eval_dir = Path(__file__).resolve().parents[1]
        plan = parse_plan(
            (eval_dir / "fixtures" / "source-supported-alternative.md").read_text(encoding="utf-8")
        )
        expectations = load_object(eval_dir / "recipe-app" / "expectations.json")

        self.assertEqual(validate_expectations(plan, expectations), [])

    def test_calibration_reports_metrics_without_gating(self) -> None:
        manifest = {"fixtures": [], "paired": []}

        report = build_report(manifest, [])

        self.assertIsNone(report["exact_agreement"])
        self.assertFalse(report["thresholds_enforced"])

    def test_calibration_infers_fixture_and_reports_agreement_and_spread(self) -> None:
        manifest = {
            "fixtures": [{"id": "case", "path": "case.md"}],
            "paired": [],
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            artifacts = []
            for provider, verdict, total in (("a", "pass", 80), ("b", "minor", 86)):
                grade = {
                    "candidate": "case.md",
                    "axes": [{"id": "axis", "criteria": [{"id": "criterion", "verdict": verdict}]}],
                    "critical_failures": [],
                }
                score = {
                    "candidate": "case.md",
                    "axes": [{"id": "axis", "score": 4}],
                    "effective_total": total,
                }
                for suffix, value in (("GRADE", grade), ("SCORE", score)):
                    path = root / f"case.{provider}.{suffix}.json"
                    path.write_text(json.dumps(value), encoding="utf-8")
                    artifacts.append(path)

            report = build_report(manifest, artifacts)

        self.assertEqual(report["exact_agreement"], 0.0)
        self.assertEqual(report["within_one_severity"], 1.0)
        self.assertEqual(report["maximum_total_score_spread"], 6.0)

    def test_skill_clarifications_remain_scenario_generic(self) -> None:
        skill = (ROOT / "skills" / "plan-slices" / "SKILL.md").read_text(encoding="utf-8")

        self.assertNotIn("recipe-app", skill)
        self.assertIn("unpublished ledger", skill)
        self.assertIn("partial ownership", skill)


if __name__ == "__main__":
    unittest.main()
