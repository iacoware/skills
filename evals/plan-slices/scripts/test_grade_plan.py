#!/usr/bin/env python3
"""Tests for grade_plan.py."""

from __future__ import annotations

import tempfile
import unittest
from json import dumps
from pathlib import Path
from subprocess import CompletedProcess
from unittest.mock import patch

from grade_plan import (
    _grader_command,
    _parse_grader_response,
    grader_schema,
    render_prompt,
    run_grader,
    score_grade,
)


RUBRIC = {
    "version": 1,
    "scale": {"minimum": 0, "maximum": 4},
    "axes": [
        {"id": "themes", "weight": 60},
        {"id": "slices", "weight": 40},
    ],
    "critical_failures": [
        {"id": "silent_conflict", "score_cap": 59},
    ],
}


def valid_grade() -> dict[str, object]:
    return {
        "rubric_version": 1,
        "candidate": "PLAN.md",
        "axes": [
            {
                "id": "themes",
                "score": 4,
                "evidence": ["Themes table"],
                "findings": [],
                "confidence": "high",
            },
            {
                "id": "slices",
                "score": 2,
                "evidence": ["NOW slice 2"],
                "findings": ["One split warning"],
                "confidence": "medium",
            },
        ],
        "critical_failures": [],
    }


class ScoreGradeTests(unittest.TestCase):
    def test_calculates_weighted_total(self) -> None:
        result = score_grade(RUBRIC, valid_grade())

        self.assertEqual(result["raw_total"], 80.0)
        self.assertEqual(result["effective_total"], 80.0)

    def test_applies_critical_failure_cap(self) -> None:
        grade = valid_grade()
        grade["critical_failures"] = [
            {"id": "silent_conflict", "evidence": ["Open question omitted"]}
        ]

        result = score_grade(RUBRIC, grade)

        self.assertEqual(result["raw_total"], 80.0)
        self.assertEqual(result["effective_total"], 59)

    def test_rejects_missing_axis(self) -> None:
        grade = valid_grade()
        grade["axes"] = grade["axes"][:1]

        with self.assertRaisesRegex(ValueError, "mismatch"):
            score_grade(RUBRIC, grade)

    def test_renders_reference_sources_and_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.md"
            reference = root / "reference.md"
            plan = root / "plan.md"
            source.write_text("SOURCE CONTENT", encoding="utf-8")
            reference.write_text("REFERENCE CONTENT", encoding="utf-8")
            plan.write_text("PLAN CONTENT", encoding="utf-8")

            prompt = render_prompt(RUBRIC, reference, plan, [source])

        self.assertIn("SOURCE CONTENT", prompt)
        self.assertIn("REFERENCE CONTENT", prompt)
        self.assertIn("PLAN CONTENT", prompt)
        self.assertIn('"rubric_version": 1', prompt)

    def test_builds_provider_specific_commands(self) -> None:
        root = Path("/tmp/grader")
        schema = root / "schema.json"

        codex = _grader_command("codex", schema, "{}", root, "codex-model")
        claude = _grader_command("claude", schema, "{}", root, "claude-model")

        self.assertEqual(codex[:2], ["codex", "exec"])
        self.assertIn("--output-schema", codex)
        self.assertIn("read-only", codex)
        self.assertEqual(codex[-1], "-")
        self.assertEqual(claude[0], "claude")
        self.assertIn("--json-schema", claude)
        self.assertIn("--safe-mode", claude)
        self.assertIn("--no-session-persistence", claude)

    def test_parses_claude_structured_output(self) -> None:
        output = dumps({"structured_output": valid_grade()})

        grade = _parse_grader_response("claude", output)

        self.assertEqual(grade, valid_grade())

    def test_generates_schema_from_rubric(self) -> None:
        schema = grader_schema(RUBRIC)
        properties = schema["properties"]

        self.assertEqual(properties["rubric_version"]["enum"], [1])
        self.assertEqual(properties["axes"]["minItems"], 2)

    def test_runs_codex_in_an_isolated_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.md"
            reference = root / "reference.md"
            plan = root / "plan.md"
            source.write_text("SOURCE", encoding="utf-8")
            reference.write_text("REFERENCE", encoding="utf-8")
            plan.write_text("PLAN", encoding="utf-8")
            grader_result = CompletedProcess(
                args=[], returncode=0, stdout=dumps(valid_grade()), stderr=""
            )
            version_result = CompletedProcess(
                args=[], returncode=0, stdout="codex-cli 1.2.3\n", stderr=""
            )

            with patch(
                "grade_plan.subprocess.run", side_effect=[grader_result, version_result]
            ) as run:
                grade, score = run_grader(
                    "codex", RUBRIC, reference, plan, [source], None, 30
                )

        command = run.call_args_list[0].args[0]
        grader_cwd = run.call_args_list[0].kwargs["cwd"]
        self.assertEqual(grade, valid_grade())
        self.assertEqual(score["grader"]["provider"], "codex")
        self.assertIn("--skip-git-repo-check", command)
        self.assertNotEqual(grader_cwd, root)


if __name__ == "__main__":
    unittest.main()
