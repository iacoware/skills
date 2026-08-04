#!/usr/bin/env python3
"""Tests for grading-orchestrator planning and state transitions."""

from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from grader_runtime import sha256_file
from grading_contract import score_grade
from orchestrate_grading import (
    _expected_metadata,
    _paired_prerequisites,
    _validate_resume,
    build_parser,
    execute,
    materialize_run,
    preflight,
)
from test_compare_plans import valid_comparison
from test_grade_plan import RUBRIC, valid_grade


class GradingOrchestratorTests(unittest.TestCase):
    def _common_args(self, root: Path) -> list[str]:
        source = root / "source.md"
        reference = root / "reference.md"
        rubric = root / "rubric.json"
        source.write_text("SOURCE", encoding="utf-8")
        reference.write_text("REFERENCE", encoding="utf-8")
        rubric.write_text(json.dumps(RUBRIC), encoding="utf-8")
        return [
            "--source", str(source),
            "--reference", str(reference),
            "--rubric", str(rubric),
            "--output-dir", str(root / "results"),
        ]

    def test_compare_materializes_absolute_before_paired_in_stable_provider_order(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            before, after = root / "before.md", root / "after.md"
            before.write_text("BEFORE", encoding="utf-8")
            after.write_text("AFTER", encoding="utf-8")
            args = build_parser().parse_args(
                ["compare", str(before), str(after), "--provider", "both", *self._common_args(root)]
            )

            run = materialize_run(args)

        self.assertEqual(
            [unit.label for unit in run.units],
            [
                "absolute:before:codex",
                "absolute:before:claude",
                "absolute:after:codex",
                "absolute:after:claude",
                "paired:before-to-after:codex",
                "paired:before-to-after:claude",
                "adjudication:before-to-after",
            ],
        )
        self.assertEqual(run.providers[0].model, "gpt-5.6-sol")
        self.assertEqual(run.providers[1].model, "claude-opus-5")
        self.assertTrue(
            all(".v2." in target.name for unit in run.units[:4] for target in unit.targets)
        )

    def test_grade_deduplicates_identical_candidate_and_sources(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            plan = root / "plan.md"
            plan.write_text("PLAN", encoding="utf-8")
            common = self._common_args(root)
            source = common[1]
            args = build_parser().parse_args(
                [
                    "grade", str(plan), str(plan), "--provider", "codex",
                    *common, "--source", source,
                ]
            )

            run = materialize_run(args)

        self.assertEqual(run.candidates, (plan,))
        self.assertEqual(len(run.sources), 1)
        self.assertEqual(len(run.units), 1)

    def test_calibrate_always_materializes_both_providers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            fixture = root / "fixture.md"
            before = root / "before.md"
            after = root / "after.md"
            for path in (fixture, before, after):
                path.write_text(path.stem, encoding="utf-8")
            manifest = root / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "fixtures": [{"id": "fixture", "path": fixture.name}],
                        "paired": [{"id": "pair", "before": before.name, "after": after.name}],
                    }
                ),
                encoding="utf-8",
            )
            args = build_parser().parse_args(
                [
                    "calibrate", "--manifest", str(manifest),
                    "--report-output", str(root / "results" / "report.json"),
                    *self._common_args(root),
                ]
            )

            run = materialize_run(args)

        self.assertEqual([provider.name for provider in run.providers], ["codex", "claude"])
        self.assertEqual(sum(unit.kind == "absolute" for unit in run.units), 6)
        self.assertEqual(sum(unit.kind == "paired" for unit in run.units), 2)

    def test_dry_run_skips_provider_probe_and_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            plan = root / "plan.md"
            plan.write_text("PLAN", encoding="utf-8")
            args = build_parser().parse_args(
                ["grade", str(plan), "--provider", "both", *self._common_args(root), "--dry-run"]
            )
            run = materialize_run(args)

            with (
                patch("orchestrate_grading._validate_plans"),
                patch("orchestrate_grading.probe_provider") as probe,
                redirect_stdout(io.StringIO()),
            ):
                preflight(run)
                exit_code = execute(run)

            self.assertFalse((root / "results").exists())
            probe.assert_not_called()

        self.assertEqual(exit_code, 0)
        self.assertTrue(all(unit.status == "not-run" for unit in run.units))

    def test_first_execution_failure_marks_remaining_units_not_run(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            before, after = root / "before.md", root / "after.md"
            before.write_text("BEFORE", encoding="utf-8")
            after.write_text("AFTER", encoding="utf-8")
            args = build_parser().parse_args(
                [
                    "compare", str(before), str(after), "--provider", "both",
                    *self._common_args(root), "--confirm-send",
                ]
            )
            run = materialize_run(args)

            with patch(
                "orchestrate_grading._execute_provider_unit", side_effect=RuntimeError("boom")
            ):
                exit_code = execute(run)

        self.assertEqual(exit_code, 2)
        self.assertEqual(run.units[0].status, "failed")
        self.assertTrue(all(unit.status == "not-run" for unit in run.units[1:]))

    def test_completed_compare_resumes_without_reinvoking_leaf_commands(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            before, after = root / "before.md", root / "after.md"
            before.write_text("BEFORE", encoding="utf-8")
            after.write_text("AFTER", encoding="utf-8")
            arguments = [
                "compare",
                str(before),
                str(after),
                "--provider",
                "both",
                *self._common_args(root),
                "--confirm-send",
            ]
            run = materialize_run(build_parser().parse_args(arguments))
            run.rubric = RUBRIC
            run.cli_versions = {"codex": "codex 1", "claude": "claude 1"}

            def write_leaf(command: list[str], _timeout: int) -> None:
                provider = command[command.index("--provider") + 1]
                if command[1].endswith("grade_plan.py"):
                    candidate = Path(command[command.index("--plan") + 1])
                    unit = next(
                        item
                        for item in run.units
                        if item.kind == "absolute"
                        and item.candidates == (candidate,)
                        and item.provider is not None
                        and item.provider.name == provider
                    )
                    metadata = {
                        **_expected_metadata(run, unit),
                        "run_id": run.run_id,
                        "timestamp_utc": run.timestamp_utc,
                    }
                    grade = valid_grade(str(candidate))
                    grade["grader"] = metadata
                    score = score_grade(RUBRIC, grade)
                    score["grader"] = metadata
                    Path(command[command.index("--grade-output") + 1]).write_text(
                        json.dumps(grade), encoding="utf-8"
                    )
                    Path(command[command.index("--score-output") + 1]).write_text(
                        json.dumps(score), encoding="utf-8"
                    )
                    return
                unit = next(
                    item
                    for item in run.units
                    if item.kind == "paired"
                    and item.provider is not None
                    and item.provider.name == provider
                )
                comparison = valid_comparison()
                comparison["before_candidate"] = str(before)
                comparison["after_candidate"] = str(after)
                comparison["grader"] = {
                    **_expected_metadata(run, unit),
                    "run_id": run.run_id,
                    "timestamp_utc": run.timestamp_utc,
                }
                comparison["prerequisites"] = [
                    {"path": str(path), "sha256": sha256_file(path)}
                    for path in _paired_prerequisites(run, unit)
                ]
                Path(command[command.index("--comparison-output") + 1]).write_text(
                    json.dumps(comparison), encoding="utf-8"
                )

            with patch("orchestrate_grading._invoke", side_effect=write_leaf):
                exit_code = execute(run)

            resumed = materialize_run(
                build_parser().parse_args([*arguments, "--resume"])
            )
            resumed.rubric = RUBRIC
            resumed.cli_versions = {"codex": "codex 1", "claude": "claude 1"}
            resumed.store.check_targets(
                (target for unit in resumed.units for target in unit.targets), resume=True
            )
            _validate_resume(resumed)
            with patch("orchestrate_grading._invoke") as invoke:
                resumed_exit_code = execute(resumed)

        self.assertEqual(exit_code, 0)
        self.assertEqual(resumed_exit_code, 0)
        self.assertEqual(sum(unit.status == "completed" for unit in run.units), 6)
        self.assertEqual(sum(unit.status == "resumed" for unit in resumed.units), 6)
        self.assertEqual(resumed.units[-1].reason, "not-required")
        invoke.assert_not_called()


if __name__ == "__main__":
    unittest.main()
