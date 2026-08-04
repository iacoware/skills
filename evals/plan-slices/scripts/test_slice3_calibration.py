from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from calibration_report import validate_manifest
from grading_contract import score_grade
from orchestrator_artifacts import ArtifactStore
from orchestrate_grading import _expected_metadata, build_parser, execute, materialize_run, preflight
from v3_test_support import RUBRIC, passing_grade


def calibration_arguments(output_dir: Path, *extra: str) -> list[str]:
    evaluation_root = Path(__file__).resolve().parent.parent
    scenario = evaluation_root / "recipe-app"
    return [
        "calibrate",
        "--manifest",
        str(evaluation_root / "fixtures/manifest.v3.json"),
        "--report-output",
        str(output_dir / "CALIBRATION-CRITICAL.v3.json"),
        "--source",
        str(scenario / "sources/goal.md"),
        "--source",
        str(scenario / "sources/concepts.md"),
        "--source",
        str(scenario / "sources/arch-choices.md"),
        "--source",
        str(scenario / "sources/tech-choices.md"),
        "--brief",
        str(scenario / "EVALUATION-BRIEF.md"),
        "--rubric",
        str(evaluation_root / "grader-rubric.v3.json"),
        "--output-dir",
        str(output_dir),
        *extra,
    ]


class Slice3CalibrationTests(unittest.TestCase):
    def test_critical_subset_materializes_only_absolute_provider_calls(self) -> None:
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as directory:
            args = build_parser().parse_args(
                calibration_arguments(Path(directory), "--critical-subset", "--dry-run")
            )

            run = materialize_run(args)

        self.assertEqual(len(run.candidates), 6)
        self.assertEqual(sum(unit.kind == "absolute" for unit in run.units), 36)
        self.assertEqual(sum(unit.kind == "paired" for unit in run.units), 0)
        self.assertEqual(sum(unit.kind.endswith("adjudication") for unit in run.units), 0)
        self.assertEqual(sum(unit.kind == "calibration" for unit in run.units), 1)
        target_names = {target.name for unit in run.units for target in unit.targets}
        self.assertIn("boundary-pass.codex.v3.run-01.GRADE.json", target_names)
        self.assertIn("boundary-absent.claude.v3.run-03.SCORE.json", target_names)
        machine_targets = [target for unit in run.units if unit.provider for target in unit.targets]
        report_target = next(unit.targets[0] for unit in run.units if unit.kind == "calibration")
        self.assertTrue(all(target.parent == Path(directory).resolve() / "raw" for target in machine_targets))
        self.assertEqual(report_target.parent, Path(directory).resolve())

    def test_critical_subset_shards_are_disjoint_complete_and_report_free(self) -> None:
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as directory:
            output_dir = Path(directory)
            full_run = materialize_run(
                build_parser().parse_args(
                    calibration_arguments(output_dir, "--critical-subset", "--dry-run")
                )
            )
            full_targets = {
                target
                for unit in full_run.units
                if unit.provider
                for target in unit.targets
            }
            shard_targets: list[set[Path]] = []
            shard_labels: list[set[str]] = []
            for shard_index in range(1, 5):
                run = materialize_run(
                    build_parser().parse_args(
                        calibration_arguments(
                            output_dir,
                            "--critical-subset",
                            "--dry-run",
                            "--shard-count",
                            "4",
                            "--shard-index",
                            str(shard_index),
                        )
                    )
                )

                self.assertEqual(sum(unit.kind == "absolute" for unit in run.units), 9)
                self.assertFalse(any(unit.kind == "calibration" for unit in run.units))
                shard_targets.append({target for unit in run.units for target in unit.targets})
                shard_labels.append({unit.label for unit in run.units})

        self.assertEqual(set().union(*shard_targets), full_targets)
        self.assertEqual(sum(len(targets) for targets in shard_targets), len(full_targets))
        self.assertEqual(sum(len(labels) for labels in shard_labels), 36)

    def test_machine_staging_is_confined_to_raw_and_report_staging_to_root(self) -> None:
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as directory:
            store = ArtifactStore(Path(directory), "run-1")
            machine_target = store.machine_target("fixture.codex.v3.run-01.GRADE.json")
            report_target = store.report_target("CALIBRATION-CRITICAL.v3.json")

            machine_staging = store.create_staging(machine_target)
            report_staging = store.create_staging(report_target)

            self.assertEqual(machine_staging.parent, Path(directory).resolve() / "raw")
            self.assertEqual(report_staging.parent, Path(directory).resolve())
            store.cleanup([machine_staging, report_staging])

    def test_report_only_requires_complete_resumable_raw_artifacts(self) -> None:
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as directory:
            output_dir = Path(directory) / "calibration-v3"
            run = materialize_run(
                build_parser().parse_args(
                    calibration_arguments(
                        output_dir,
                        "--critical-subset",
                        "--report-only",
                        "--resume",
                    )
                )
            )

            with patch("orchestrate_grading.probe_provider") as probe:
                with self.assertRaisesRegex(ValueError, "every provider artifact"):
                    preflight(run)

            probe.assert_not_called()
            self.assertFalse(output_dir.exists())

    def test_report_only_resumes_raw_matrix_and_publishes_report_offline(self) -> None:
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as directory:
            output_dir = Path(directory) / "calibration-v3"
            run = materialize_run(
                build_parser().parse_args(
                    calibration_arguments(
                        output_dir,
                        "--critical-subset",
                        "--report-only",
                        "--resume",
                    )
                )
            )
            run.rubric = RUBRIC
            run.cli_versions = {"codex": "codex test", "claude": "claude test"}
            for unit in (unit for unit in run.units if unit.provider):
                metadata = {
                    **_expected_metadata(run, unit),
                    "run_id": "collected-shard-run",
                    "timestamp_utc": "2026-08-04T00:00:00+00:00",
                }
                grade = passing_grade()
                grade["grader"] = metadata
                score = score_grade(RUBRIC, grade)
                score["grader"] = metadata
                unit.targets[0].parent.mkdir(parents=True, exist_ok=True)
                unit.targets[0].write_text(json.dumps(grade), encoding="utf-8")
                unit.targets[1].write_text(json.dumps(score), encoding="utf-8")

            with (
                patch("orchestrate_grading.probe_provider") as probe,
                patch("orchestrate_grading._invoke") as invoke,
                redirect_stdout(io.StringIO()),
            ):
                preflight(run)
                exit_code = execute(run)

            report_target = next(unit.targets[0] for unit in run.units if unit.kind == "calibration")
            self.assertEqual(exit_code, 0)
            self.assertTrue(all(unit.status == "resumed" for unit in run.units if unit.provider))
            self.assertTrue(report_target.is_file())
            self.assertEqual(report_target.parent, output_dir.resolve())
            probe.assert_not_called()
            invoke.assert_not_called()

    def test_critical_subset_dry_run_reports_counts_without_invoking_providers(self) -> None:
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as directory:
            output_dir = Path(directory) / "results"
            args = build_parser().parse_args(
                calibration_arguments(output_dir, "--critical-subset", "--dry-run")
            )
            run = materialize_run(args)

            with patch("orchestrate_grading._invoke") as invoke, redirect_stdout(io.StringIO()) as output:
                preflight(run)
                exit_code = execute(run)

            self.assertEqual(exit_code, 0)
            invoke.assert_not_called()
            self.assertIn("external_provider_calls: 36", output.getvalue())
            self.assertIn("paired_provider_calls: 0", output.getvalue())
            self.assertIn("adjudication_units: 0", output.getvalue())
            self.assertFalse(output_dir.exists())

    def test_manifest_rejects_non_boolean_critical_subset_marker(self) -> None:
        fixtures_root = Path(__file__).resolve().parent.parent / "fixtures"
        manifest = json.loads((fixtures_root / "manifest.v3.json").read_text(encoding="utf-8"))
        manifest["fixtures"][0]["critical_subset"] = "yes"

        with self.assertRaisesRegex(ValueError, "critical_subset must be boolean"):
            validate_manifest(manifest, fixtures_root)


if __name__ == "__main__":
    unittest.main()
