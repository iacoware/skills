#!/usr/bin/env python3
"""Run grading providers reproducibly in an isolated directory."""

from __future__ import annotations

import hashlib
import json
import shutil
import stat
import subprocess
import tempfile
from pathlib import Path
from typing import Sequence


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_provider_response(provider: str, output: str) -> dict[str, object]:
    value = json.loads(output)
    if not isinstance(value, dict):
        raise ValueError(f"{provider} grader returned a non-object response")
    if isinstance(value.get("axes"), list):
        return value
    structured = value.get("structured_output")
    if isinstance(structured, dict):
        return structured
    result = value.get("result")
    if isinstance(result, dict):
        return result
    if isinstance(result, str):
        parsed = json.loads(result)
        if isinstance(parsed, dict):
            return parsed
    raise ValueError(f"{provider} grader response does not contain structured output")


def provider_command(
    provider: str,
    schema_path: Path,
    schema_text: str,
    working_directory: Path,
    model: str,
    effort: str,
    configuration: Sequence[str] = (),
) -> list[str]:
    if provider == "codex":
        command = [
            "codex", "exec", "--ephemeral", "--ignore-user-config", "--sandbox", "read-only",
            "--skip-git-repo-check", "--cd", str(working_directory), "--output-schema",
            str(schema_path), "--color", "never", "--model", model,
            "--config", f'model_reasoning_effort="{effort}"',
        ]
        for item in configuration:
            command.extend(["--config", item])
        return [*command, "-"]
    if provider == "claude":
        if configuration:
            raise ValueError("claude: arbitrary configuration overrides are unsupported")
        return [
            "claude", "--safe-mode", "--print", "--no-session-persistence", "--tools", "",
            "--output-format", "json", "--json-schema", schema_text, "--model", model,
            "--effort", effort,
        ]
    raise ValueError(f"unsupported grader provider: {provider}")


def cli_version(provider: str) -> str:
    result = subprocess.run(
        [provider, "--version"], capture_output=True, text=True, timeout=10, check=False
    )
    version = (result.stdout or result.stderr).strip()
    if result.returncode != 0 or not version:
        raise RuntimeError(f"cannot capture {provider} CLI version")
    return version


def probe_provider(provider: str) -> str:
    if provider not in {"codex", "claude"}:
        raise ValueError(f"unsupported grader provider: {provider}")
    if shutil.which(provider) is None:
        raise RuntimeError(f"{provider} CLI is not available")

    version = cli_version(provider)
    auth_command = (
        [provider, "login", "status"]
        if provider == "codex"
        else [provider, "auth", "status"]
    )
    result = subprocess.run(
        auth_command, capture_output=True, text=True, timeout=10, check=False
    )
    if result.returncode != 0:
        raise RuntimeError(f"{provider} CLI is not authenticated")
    return version


def require_reproducibility(
    model: str | None,
    effort: str | None,
    *,
    exploratory: bool,
    output_paths: Sequence[Path] = (),
) -> tuple[str, str]:
    if not exploratory:
        if not model or not effort or model == "cli-default" or effort == "cli-default":
            raise ValueError("explicit non-default model and effort are required")
        if any(".v3." not in path.name for path in output_paths):
            raise ValueError("baseline outputs must include '.v3.' in each artifact name")
        return model, effort
    if any(".exploratory." not in path.name for path in output_paths):
        raise ValueError("exploratory outputs must include '.exploratory.' in each artifact name")
    return model or "cli-default", effort or "cli-default"


def ensure_new_outputs(paths: Sequence[Path]) -> None:
    existing = [str(path) for path in paths if path.exists()]
    if existing:
        raise ValueError(f"refusing to overwrite existing artifacts: {existing}")


def require_owned_staging(paths: Sequence[Path], run_id: str | None) -> None:
    if not run_id:
        raise ValueError("orchestrated staging requires a run ID")
    if len(paths) != len(set(paths)) or len({path.parent for path in paths}) != 1:
        raise ValueError("orchestrated staging outputs must be distinct and co-located")
    prefix = f".{run_id}."
    for path in paths:
        try:
            mode = path.lstat().st_mode
        except FileNotFoundError as error:
            raise ValueError(f"missing orchestrated staging file: {path}") from error
        if not path.name.startswith(prefix) or not stat.S_ISREG(mode) or mode & 0o077:
            raise ValueError(f"unsafe orchestrated staging file: {path}")


def run_provider(
    provider: str,
    prompt: str,
    schema: dict[str, object],
    model: str,
    effort: str,
    timeout: int,
    configuration: Sequence[str] = (),
) -> tuple[dict[str, object], str]:
    schema_text = json.dumps(schema, ensure_ascii=False)
    with tempfile.TemporaryDirectory(prefix="plan-grader-") as directory:
        working_directory = Path(directory)
        schema_path = working_directory / "response.schema.json"
        schema_path.write_text(schema_text, encoding="utf-8")
        command = provider_command(
            provider, schema_path, schema_text, working_directory, model, effort, configuration
        )
        result = subprocess.run(
            command,
            input=prompt,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
            cwd=working_directory,
        )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"{provider} grader failed ({result.returncode}): {detail}")
    return parse_provider_response(provider, result.stdout), cli_version(provider)


def reproducibility_metadata(
    *,
    provider: str,
    model: str,
    effort: str,
    configuration: Sequence[str],
    cli_version_value: str,
    prompt: str,
    sources: Sequence[Path],
    brief: Path,
    rubric: Path,
    candidates: Sequence[Path],
    run_id: str,
    timestamp_utc: str,
    candidate_skill_commits: dict[str, str] | None = None,
    alias_mapping: dict[str, str] | None = None,
    manifest: Path | None = None,
    label_set: object | None = None,
) -> dict[str, object]:
    commits = candidate_skill_commits or {}
    return {
        "provider": provider,
        "requested_model": model,
        "effort": effort,
        "configuration": list(configuration),
        "cli_version": cli_version_value,
        "prompt_sha256": sha256_text(prompt),
        "source_sha256": {str(path): sha256_file(path) for path in sources},
        "brief_sha256": sha256_file(brief),
        "rubric_sha256": sha256_file(rubric),
        "candidates": [
            {
                "path": str(candidate),
                "sha256": sha256_file(candidate),
                "skill_commit": commits.get(str(candidate), "unknown"),
            }
            for candidate in candidates
        ],
        "run_id": run_id,
        "timestamp_utc": timestamp_utc,
        "alias_mapping": alias_mapping or {},
        "manifest_sha256": sha256_file(manifest) if manifest else None,
        "label_set_sha256": sha256_text(json.dumps(label_set, sort_keys=True)) if label_set is not None else None,
    }
