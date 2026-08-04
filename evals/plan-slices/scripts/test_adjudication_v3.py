from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from adjudication_contract import build_request, material_grade_disagreements, resolve_absolute, validate_resolution
from v3_test_support import RUBRIC, passing_grade, set_nonpass


class AdjudicationV3Tests(unittest.TestCase):
    def _paths(self, root: Path, grades: list[dict[str, object]]) -> list[Path]:
        paths = [root / "grader-one.json", root / "grader-two.json"]
        for path, grade in zip(paths, grades, strict=True):
            path.write_text(json.dumps(grade), encoding="utf-8")
        return paths

    def test_pass_minor_does_not_trigger_material_review(self) -> None:
        left, right = passing_grade(), passing_grade()
        set_nonpass(right, "content_failure_quality", "minor")

        self.assertEqual(material_grade_disagreements([left, right]), ([], []))

    def test_request_contains_only_disagreement_and_no_identity(self) -> None:
        left, right = passing_grade(), passing_grade()
        set_nonpass(right, "slice_cohesive_cut", "material")
        left["grader"] = {"provider": "codex", "alias_mapping": {"candidate-A": "/secret/one"}}
        right["grader"] = {"provider": "claude", "alias_mapping": {"candidate-A": "/secret/two"}}
        with tempfile.TemporaryDirectory() as directory:
            paths = self._paths(Path(directory), [left, right])

            request, metadata = build_request("absolute", paths, [left, right])

        self.assertEqual([item["id"] for item in request["discordant_criteria"]], ["slice_cohesive_cut"])
        blind = json.dumps(request)
        self.assertNotIn("codex", blind)
        self.assertNotIn("claude", blind)
        self.assertNotIn("/secret", blind)
        self.assertIn("provider", json.dumps(metadata))

    def test_resolution_cannot_modify_agreed_criterion(self) -> None:
        left, right = passing_grade(), passing_grade()
        with tempfile.TemporaryDirectory() as directory:
            request, _ = build_request("absolute", self._paths(Path(directory), [left, right]), [left, right])
        resolution = {
            "adjudication_version": 3,
            "type": "absolute",
            "input_sha256": request["input_sha256"],
            "criteria": [{"id": "theme_split_merge"}],
            "critical_failures": [],
            "rationale": "Override",
        }

        with self.assertRaisesRegex(ValueError, "only materially discordant"):
            validate_resolution(request, resolution)

    def test_automatic_resolution_derives_one_grade_and_score(self) -> None:
        left, right = passing_grade(), passing_grade()
        set_nonpass(right, "content_failure_quality", "minor")
        with tempfile.TemporaryDirectory() as directory:
            request, _ = build_request("absolute", self._paths(Path(directory), [left, right]), [left, right])

            grade, score = resolve_absolute(RUBRIC, [left, right], request, None)

        self.assertEqual(score["candidate"], "candidate-A")
        verdict = next(entry["verdict"] for axis in grade["axes"] for entry in axis["criteria"] if entry["id"] == "content_failure_quality")
        self.assertEqual(verdict, "minor")


if __name__ == "__main__":
    unittest.main()
