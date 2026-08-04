#!/usr/bin/env python3
"""Tests for secure orchestrator artifact handling."""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

from grading_contract import score_grade
from orchestrator_artifacts import (
    ArtifactStore,
    candidate_stem,
    validate_absolute_resume,
)
from test_grade_plan import RUBRIC, valid_grade


class OrchestratorArtifactTests(unittest.TestCase):
    def test_derives_safe_candidate_stem(self) -> None:
        self.assertEqual(candidate_stem(Path("PLAN-5.md")), "PLAN-5")

        with self.assertRaisesRegex(ValueError, "unsafe"):
            candidate_stem(Path(".md"))

    def test_rejects_collision_before_staging(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            store = ArtifactStore(root, "run-1")
            target = store.target("plan.codex.v2.GRADE.json")
            target.write_text("historical", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "overwrite"):
                store.check_targets([target], resume=False)

            self.assertEqual(target.read_text(encoding="utf-8"), "historical")

    def test_publishes_without_replacing_racing_target(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            store = ArtifactStore(root, "run-1")
            target = store.target("plan.codex.v2.GRADE.json")
            staging = store.create_staging(target)
            staging.write_text("new", encoding="utf-8")
            target.write_text("racer", encoding="utf-8")

            with self.assertRaises(FileExistsError):
                store.publish({staging: target})

            self.assertEqual(target.read_text(encoding="utf-8"), "racer")
            store.cleanup([staging])

    def test_rejects_symlink_target(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            destination = root / "destination"
            destination.write_text("data", encoding="utf-8")
            os.symlink(destination, root / "artifact.json")
            store = ArtifactStore(root, "run-1")

            with self.assertRaisesRegex(ValueError, "symlink"):
                store.target("artifact.json")

    def test_resume_recalculates_score_and_ignores_only_run_identity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            candidate = root / "plan.md"
            candidate.write_text("PLAN", encoding="utf-8")
            grade_path = root / "plan.codex.v2.GRADE.json"
            score_path = root / "plan.codex.v2.SCORE.json"
            grade = valid_grade(str(candidate))
            metadata = {
                "provider": "codex",
                "requested_model": "gpt-5.6-sol",
                "effort": "high",
                "configuration": [],
                "cli_version": "codex 1",
                "prompt_sha256": "prompt",
                "source_sha256": {},
                "reference_sha256": "reference",
                "rubric_sha256": "rubric",
                "candidates": [
                    {"path": str(candidate), "sha256": "candidate", "skill_commit": "unknown"}
                ],
                "run_id": "old-run",
                "timestamp_utc": "2026-08-01T00:00:00+00:00",
            }
            grade["grader"] = metadata
            score = score_grade(RUBRIC, grade)
            score["grader"] = metadata
            grade_path.write_text(json.dumps(grade), encoding="utf-8")
            score_path.write_text(json.dumps(score), encoding="utf-8")
            expected = {
                key: value
                for key, value in metadata.items()
                if key not in {"run_id", "timestamp_utc"}
            }

            validate_absolute_resume(grade_path, score_path, RUBRIC, candidate, expected)

            score["effective_total"] = 99
            score_path.write_text(json.dumps(score), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "does not match"):
                validate_absolute_resume(grade_path, score_path, RUBRIC, candidate, expected)


if __name__ == "__main__":
    unittest.main()
