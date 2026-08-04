#!/usr/bin/env python3
"""Tests for provider isolation and reproducibility controls."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from subprocess import CompletedProcess
from unittest.mock import patch

from grader_runtime import (
    ensure_new_outputs,
    parse_provider_response,
    probe_provider,
    provider_command,
    require_reproducibility,
    require_owned_staging,
    run_provider,
)


class GraderRuntimeTests(unittest.TestCase):
    def test_codex_command_passes_model_effort_and_configuration(self) -> None:
        root = Path("/tmp/grader")

        command = provider_command(
            "codex", root / "schema.json", "{}", root, "gpt-5.6-sol", "high", ["foo=true"]
        )

        self.assertIn("gpt-5.6-sol", command)
        self.assertIn('model_reasoning_effort="high"', command)
        self.assertIn("foo=true", command)
        self.assertIn("--ignore-user-config", command)

    def test_claude_command_passes_model_and_effort(self) -> None:
        root = Path("/tmp/grader")

        command = provider_command(
            "claude", root / "schema.json", "{}", root, "claude-opus-5", "high"
        )

        self.assertIn("claude-opus-5", command)
        self.assertEqual(command[command.index("--effort") + 1], "high")

    def test_parses_direct_structured_and_nested_json(self) -> None:
        value = {"axes": []}

        self.assertEqual(parse_provider_response("codex", json.dumps(value)), value)
        self.assertEqual(parse_provider_response("claude", json.dumps({"structured_output": value})), value)
        self.assertEqual(parse_provider_response("claude", json.dumps({"result": json.dumps(value)})), value)

    def test_rejects_missing_reproducibility_metadata(self) -> None:
        with self.assertRaisesRegex(ValueError, "explicit"):
            require_reproducibility(None, None, exploratory=False)

    def test_baseline_requires_v2_artifact_names(self) -> None:
        with self.assertRaisesRegex(ValueError, "v2"):
            require_reproducibility(
                "gpt-5.6-sol", "high", exploratory=False,
                output_paths=[Path("plan.GRADE.json")],
            )

    def test_exploratory_defaults_require_distinct_names(self) -> None:
        with self.assertRaisesRegex(ValueError, "exploratory outputs"):
            require_reproducibility(None, None, exploratory=True, output_paths=[Path("plan.GRADE.json")])

        self.assertEqual(
            require_reproducibility(
                None, None, exploratory=True, output_paths=[Path("plan.exploratory.GRADE.json")]
            ),
            ("cli-default", "cli-default"),
        )

    def test_rejects_output_collision(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "existing.json"
            output.write_text("{}", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "overwrite"):
                ensure_new_outputs([output])

    def test_orchestrated_staging_requires_owned_restrictive_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            staging = root / ".run-1.random.plan.codex.v2.GRADE.json"
            staging.touch(mode=0o600)

            require_owned_staging([staging], "run-1")

            final = root / "plan.codex.v2.GRADE.json"
            final.touch(mode=0o600)
            with self.assertRaisesRegex(ValueError, "unsafe"):
                require_owned_staging([final], "run-1")

    def test_provider_runs_in_isolated_directory(self) -> None:
        response = CompletedProcess(args=[], returncode=0, stdout='{"axes": []}', stderr="")
        version = CompletedProcess(args=[], returncode=0, stdout="codex 1.2.3", stderr="")

        with patch("grader_runtime.subprocess.run", side_effect=[response, version]) as run:
            parsed, cli_version = run_provider(
                "codex", "PROMPT", {"type": "object"}, "gpt-5.6-sol", "high", 30
            )

        grader_cwd = Path(run.call_args_list[0].kwargs["cwd"])
        command = run.call_args_list[0].args[0]
        self.assertEqual(parsed, {"axes": []})
        self.assertEqual(cli_version, "codex 1.2.3")
        self.assertIn("--skip-git-repo-check", command)
        self.assertNotEqual(grader_cwd, Path.cwd())

    def test_provider_probe_requires_binary_version_and_authentication(self) -> None:
        version = CompletedProcess(args=[], returncode=0, stdout="codex 1.2.3", stderr="")
        authenticated = CompletedProcess(args=[], returncode=0, stdout="Logged in", stderr="")

        with (
            patch("grader_runtime.shutil.which", return_value="/usr/bin/codex"),
            patch("grader_runtime.subprocess.run", side_effect=[version, authenticated]) as run,
        ):
            result = probe_provider("codex")

        self.assertEqual(result, "codex 1.2.3")
        self.assertEqual(run.call_args_list[1].args[0], ["codex", "login", "status"])

    def test_provider_probe_rejects_missing_authentication(self) -> None:
        version = CompletedProcess(args=[], returncode=0, stdout="claude 1", stderr="")
        unauthenticated = CompletedProcess(args=[], returncode=1, stdout="", stderr="login")

        with (
            patch("grader_runtime.shutil.which", return_value="/usr/bin/claude"),
            patch("grader_runtime.subprocess.run", side_effect=[version, unauthenticated]),
            self.assertRaisesRegex(RuntimeError, "not authenticated"),
        ):
            probe_provider("claude")


if __name__ == "__main__":
    unittest.main()
