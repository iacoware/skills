#!/usr/bin/env python3
"""Plan and run reproducible grading workflows without overwriting artifacts."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

from calibration_report import build_report
from compare_plans import render_comparison_prompt
from grade_plan import load_object, render_prompt
from grader_runtime import probe_provider, sha256_file, sha256_text
from grading_contract import adjudication_reasons, rubric_contract
from orchestrator_artifacts import (
    ArtifactStore,
    candidate_stem,
    load_object as load_artifact,
    validate_absolute_resume,
    validate_adjudication_resume,
    validate_paired_resume,
)

DEFAULT_CODEX_MODEL = "gpt-5.6-sol"
DEFAULT_CLAUDE_MODEL = "claude-opus-5"
DEFAULT_EFFORT = "high"
DEFAULT_TIMEOUT = 900
STATUSES = ("completed", "resumed", "failed", "not-run")


@dataclass(frozen=True)
class ProviderConfig:
    name: str
    model: str
    effort: str
    configuration: tuple[str, ...] = ()


@dataclass
class Unit:
    kind: str
    label: str
    targets: tuple[Path, ...]
    candidates: tuple[Path, ...] = ()
    provider: ProviderConfig | None = None
    status: str = "planned"
    reason: str | None = None


@dataclass
class Run:
    command: str
    run_id: str
    timestamp_utc: str
    sources: tuple[Path, ...]
    reference: Path
    rubric_path: Path
    output_dir: Path
    timeout: int
    dry_run: bool
    resume: bool
    confirm_send: bool
    commits: dict[Path, str]
    providers: tuple[ProviderConfig, ...]
    candidates: tuple[Path, ...]
    pairs: tuple[tuple[Path, Path], ...]
    units: list[Unit]
    store: ArtifactStore
    rubric: dict[str, object] = field(default_factory=dict)
    cli_versions: dict[str, str | None] = field(default_factory=dict)
    manifest: Path | None = None
    report_output: Path | None = None


def _add_common_options(parser: argparse.ArgumentParser, *, provider: bool) -> None:
    parser.add_argument("--source", action="append", required=True, type=Path)
    parser.add_argument("--reference", required=True, type=Path)
    parser.add_argument("--rubric", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    if provider:
        parser.add_argument("--provider", required=True, choices=("codex", "claude", "both"))
    parser.add_argument("--codex-model", default=DEFAULT_CODEX_MODEL)
    parser.add_argument("--codex-effort", default=DEFAULT_EFFORT)
    parser.add_argument("--codex-config", action="append", default=[])
    parser.add_argument("--claude-model", default=DEFAULT_CLAUDE_MODEL)
    parser.add_argument("--claude-effort", default=DEFAULT_EFFORT)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--candidate-skill-commit", action="append", default=[])
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--confirm-send", action="store_true")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    grade = commands.add_parser("grade", help="grade one or more plans")
    grade.add_argument("plans", nargs="+", type=Path)
    _add_common_options(grade, provider=True)

    compare = commands.add_parser("compare", help="grade and compare BEFORE with AFTER")
    compare.add_argument("before", type=Path)
    compare.add_argument("after", type=Path)
    _add_common_options(compare, provider=True)

    calibrate = commands.add_parser("calibrate", help="run the complete fixture matrix")
    calibrate.add_argument("--manifest", required=True, type=Path)
    calibrate.add_argument("--report-output", required=True, type=Path)
    _add_common_options(calibrate, provider=False)
    return parser


def _absolute(path: Path, *, base: Path | None = None) -> Path:
    candidate = path if path.is_absolute() else (base or Path.cwd()) / path
    return Path(os.path.abspath(candidate))


def _deduplicate(paths: Sequence[Path]) -> tuple[Path, ...]:
    return tuple(dict.fromkeys(paths))


def _parse_commits(values: Sequence[str], candidates: Sequence[Path]) -> dict[Path, str]:
    commits: dict[Path, str] = {}
    for value in values:
        plan, separator, commit = value.partition("=")
        if not separator or not plan or not commit:
            raise ValueError(f"invalid candidate skill commit: {value!r}; expected PLAN=SHA")
        plan_path = Path(plan)
        path = _absolute(plan_path)
        if path not in candidates and plan_path.parent == Path("."):
            matches = [candidate for candidate in candidates if candidate.name == plan_path.name]
            if len(matches) == 1:
                path = matches[0]
        if path in commits:
            raise ValueError(f"duplicate candidate skill commit: {path}")
        commits[path] = commit
    return commits


def _provider_configs(args: argparse.Namespace) -> tuple[ProviderConfig, ...]:
    names = (
        ("codex", "claude")
        if args.command == "calibrate" or args.provider == "both"
        else (args.provider,)
    )
    configs = {
        "codex": ProviderConfig(
            "codex", args.codex_model, args.codex_effort, tuple(args.codex_config)
        ),
        "claude": ProviderConfig("claude", args.claude_model, args.claude_effort),
    }
    return tuple(configs[name] for name in names)


def _manifest_workload(
    manifest_path: Path,
) -> tuple[tuple[Path, ...], tuple[tuple[Path, Path], ...]]:
    manifest = load_object(manifest_path)
    base = manifest_path.parent
    fixture_values = manifest.get("fixtures")
    pair_values = manifest.get("paired")
    if not isinstance(fixture_values, list) or not isinstance(pair_values, list):
        raise ValueError("manifest fixtures and paired must be arrays")
    fixtures: list[Path] = []
    for fixture in fixture_values:
        if not isinstance(fixture, dict) or not isinstance(fixture.get("path"), str):
            raise ValueError("manifest fixture requires a path")
        fixtures.append(_absolute(Path(fixture["path"]), base=base))
    pairs: list[tuple[Path, Path]] = []
    for pair in pair_values:
        if not isinstance(pair, dict):
            raise ValueError("manifest paired entry must be an object")
        before, after = pair.get("before"), pair.get("after")
        if not isinstance(before, str) or not isinstance(after, str):
            raise ValueError("manifest paired entry requires before and after")
        resolved = (_absolute(Path(before), base=base), _absolute(Path(after), base=base))
        if resolved[0] == resolved[1]:
            raise ValueError(f"manifest contains a self-pair: {resolved[0]}")
        pairs.append(resolved)
    candidates = _deduplicate([*fixtures, *(item for pair in pairs for item in pair)])
    if not candidates and not pairs:
        raise ValueError("manifest has no grading workload")
    return candidates, tuple(pairs)


def materialize_run(args: argparse.Namespace) -> Run:
    if args.timeout <= 0:
        raise ValueError("timeout must be positive")
    run_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()
    sources = _deduplicate([_absolute(path) for path in args.source])
    reference = _absolute(args.reference)
    rubric_path = _absolute(args.rubric)
    output_dir = _absolute(args.output_dir)
    providers = _provider_configs(args)
    manifest: Path | None = None
    report_output: Path | None = None

    if args.command == "grade":
        candidates = _deduplicate([_absolute(path) for path in args.plans])
        pairs: tuple[tuple[Path, Path], ...] = ()
    elif args.command == "compare":
        before, after = _absolute(args.before), _absolute(args.after)
        if before == after:
            raise ValueError("compare requires two distinct candidates")
        candidates, pairs = (before, after), ((before, after),)
    else:
        manifest = _absolute(args.manifest)
        candidates, pairs = _manifest_workload(manifest)
        report_output = _absolute(args.report_output)

    commits = _parse_commits(args.candidate_skill_commit, candidates)

    stems: dict[str, Path] = {}
    for candidate in candidates:
        stem = candidate_stem(candidate)
        if stem in stems and stems[stem] != candidate:
            raise ValueError(f"duplicate candidate stem {stem}: {stems[stem]}, {candidate}")
        stems[stem] = candidate
    unknown_commits = set(commits) - set(candidates)
    if unknown_commits:
        unknown = sorted(map(str, unknown_commits))
        raise ValueError(f"candidate skill commit does not match workload: {unknown}")

    store = ArtifactStore(output_dir, run_id)
    units: list[Unit] = []
    absolute_units: dict[tuple[Path, str], Unit] = {}
    for candidate in candidates:
        for provider in providers:
            stem = candidate_stem(candidate)
            targets = (
                store.target(f"{stem}.{provider.name}.v2.GRADE.json"),
                store.target(f"{stem}.{provider.name}.v2.SCORE.json"),
            )
            unit = Unit(
                "absolute", f"absolute:{stem}:{provider.name}", targets, (candidate,), provider
            )
            units.append(unit)
            absolute_units[(candidate, provider.name)] = unit
    for before, after in pairs:
        pair_name = f"{candidate_stem(before)}-to-{candidate_stem(after)}"
        for provider in providers:
            units.append(
                Unit(
                    "paired",
                    f"paired:{pair_name}:{provider.name}",
                    (store.target(f"{pair_name}.{provider.name}.PAIRED.json"),),
                    (before, after),
                    provider,
                )
            )
        if {provider.name for provider in providers} == {"codex", "claude"}:
            units.append(
                Unit(
                    "adjudication",
                    f"adjudication:{pair_name}",
                    (store.target(f"{pair_name}.ADJUDICATION.json"),),
                    (before, after),
                )
            )
    if args.command == "calibrate":
        assert report_output is not None
        if report_output.parent != output_dir:
            raise ValueError("report output must be directly inside output directory")
        units.append(Unit("calibration", "calibration-report", (store.target(report_output.name),)))

    return Run(
        args.command,
        run_id,
        timestamp,
        sources,
        reference,
        rubric_path,
        output_dir,
        args.timeout,
        args.dry_run,
        args.resume,
        args.confirm_send,
        commits,
        providers,
        candidates,
        pairs,
        units,
        store,
        manifest=manifest,
        report_output=report_output,
    )


def _require_regular_readable(path: Path, label: str) -> None:
    if not path.exists() or not path.is_file():
        raise ValueError(f"{label} is not a regular file: {path}")
    if not os.access(path, os.R_OK):
        raise ValueError(f"{label} is not readable: {path}")


def _validate_plans(run: Run) -> None:
    validator = Path(__file__).resolve().parents[3] / "skills/plan-slices/scripts/validate_plan.py"
    _require_regular_readable(validator, "plan validator")
    for candidate in run.candidates:
        result = subprocess.run(
            [sys.executable, str(validator), str(candidate)],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            detail = result.stderr.strip() or result.stdout.strip()
            raise ValueError(f"plan validation failed for {candidate}: {detail}")


def _expected_metadata(run: Run, unit: Unit) -> dict[str, object]:
    assert unit.provider is not None
    if unit.kind == "absolute":
        prompt = render_prompt(run.rubric, run.reference, unit.candidates[0], run.sources)
    else:
        prompt = render_comparison_prompt(
            run.rubric, run.reference, unit.candidates[0], unit.candidates[1], run.sources
        )
    return {
        "provider": unit.provider.name,
        "requested_model": unit.provider.model,
        "effort": unit.provider.effort,
        "configuration": list(unit.provider.configuration),
        "cli_version": run.cli_versions.get(unit.provider.name),
        "prompt_sha256": sha256_text(prompt),
        "source_sha256": {str(path): sha256_file(path) for path in run.sources},
        "reference_sha256": sha256_file(run.reference),
        "rubric_sha256": sha256_file(run.rubric_path),
        "candidates": [
            {
                "path": str(candidate),
                "sha256": sha256_file(candidate),
                "skill_commit": run.commits.get(candidate, "unknown"),
            }
            for candidate in unit.candidates
        ],
    }


def _absolute_unit(run: Run, candidate: Path, provider: str) -> Unit:
    return next(
        unit
        for unit in run.units
        if unit.kind == "absolute"
        and unit.candidates == (candidate,)
        and unit.provider is not None
        and unit.provider.name == provider
    )


def _paired_units(run: Run, pair: tuple[Path, Path]) -> list[Unit]:
    return [unit for unit in run.units if unit.kind == "paired" and unit.candidates == pair]


def _paired_prerequisites(run: Run, unit: Unit) -> tuple[Path, ...]:
    assert unit.provider is not None
    before = _absolute_unit(run, unit.candidates[0], unit.provider.name)
    after = _absolute_unit(run, unit.candidates[1], unit.provider.name)
    return (*before.targets, *after.targets)


def _adjudication_inputs(run: Run, unit: Unit) -> tuple[list[Path], list[tuple[Path, Path]]]:
    paired = _paired_units(run, unit.candidates)
    comparisons = [item.targets[0] for item in paired]
    provider_names = [item.provider.name for item in paired if item.provider is not None]
    scores = [
        tuple(
            _absolute_unit(run, candidate, provider_name).targets[1]
            for provider_name in provider_names
        )
        for candidate in unit.candidates
    ]
    if any(len(pair) != 2 for pair in scores):
        raise ValueError("adjudication requires exactly two providers")
    return comparisons, scores


def _validate_resume(run: Run) -> None:
    for unit in run.units:
        if unit.kind == "absolute":
            try:
                validate_absolute_resume(
                    unit.targets[0],
                    unit.targets[1],
                    run.rubric,
                    unit.candidates[0],
                    _expected_metadata(run, unit),
                )
            except FileNotFoundError:
                continue
            unit.status = "resumed"
        elif unit.kind == "paired" and unit.targets[0].exists():
            validate_paired_resume(
                unit.targets[0],
                run.rubric,
                unit.candidates[0],
                unit.candidates[1],
                _paired_prerequisites(run, unit),
                _expected_metadata(run, unit),
            )
            unit.status = "resumed"
        elif unit.kind == "adjudication" and unit.targets[0].exists():
            comparisons, scores = _adjudication_inputs(run, unit)
            validate_adjudication_resume(unit.targets[0], comparisons, scores)
            unit.status = "resumed"
        elif unit.kind == "adjudication":
            comparisons, scores = _adjudication_inputs(run, unit)
            inputs = [*comparisons, *(path for pair in scores for path in pair)]
            if all(path.exists() for path in inputs):
                comparison_values = [load_artifact(path) for path in comparisons]
                score_values = [
                    (load_artifact(left), load_artifact(right)) for left, right in scores
                ]
                if not adjudication_reasons(comparison_values, score_values):
                    unit.status = "not-run"
                    unit.reason = "not-required"
        elif unit.kind == "calibration" and unit.targets[0].exists():
            if any(
                item.status != "resumed"
                and not (item.status == "not-run" and item.reason == "not-required")
                for item in run.units
                if item is not unit
            ):
                raise ValueError("calibration report cannot resume with incomplete prerequisites")
            assert run.manifest is not None
            artifacts = [
                target
                for item in run.units
                if item.kind in {"absolute", "paired"}
                for target in item.targets
            ]
            if load_artifact(unit.targets[0]) != build_report(load_object(run.manifest), artifacts):
                raise ValueError("calibration report does not match its inputs")
            unit.status = "resumed"


def preflight(run: Run) -> None:
    for candidate in run.candidates:
        _require_regular_readable(candidate, "candidate")
    for source in run.sources:
        _require_regular_readable(source, "source")
    _require_regular_readable(run.reference, "reference")
    _require_regular_readable(run.rubric_path, "rubric")
    if run.manifest is not None:
        _require_regular_readable(run.manifest, "manifest")
    run.rubric = load_object(run.rubric_path)
    rubric_contract(run.rubric)
    _validate_plans(run)
    run.store.check_targets(
        (target for unit in run.units for target in unit.targets), resume=run.resume
    )
    for provider in run.providers:
        run.cli_versions[provider.name] = None if run.dry_run else probe_provider(provider.name)
    if run.resume:
        _validate_resume(run)
    print_preflight(run)


def _leaf_command(run: Run, unit: Unit, staging: Sequence[Path]) -> list[str]:
    scripts = Path(__file__).resolve().parent
    assert unit.provider is not None
    common = [
        "--provider", unit.provider.name,
        "--rubric", str(run.rubric_path),
        "--reference", str(run.reference),
        "--sources", *(str(path) for path in run.sources),
        "--model", unit.provider.model,
        "--effort", unit.provider.effort,
        "--timeout", str(run.timeout),
        "--run-id", run.run_id,
        "--timestamp-utc", run.timestamp_utc,
    ]
    configuration = [
        item
        for value in unit.provider.configuration
        for item in ("--configuration", value)
    ]
    if unit.kind == "absolute":
        candidate = unit.candidates[0]
        return [
            sys.executable,
            str(scripts / "grade_plan.py"),
            "run",
            *common,
            *configuration,
            "--plan", str(candidate),
            "--grade-output", str(staging[0]),
            "--score-output", str(staging[1]),
            "--candidate-skill-commit", run.commits.get(candidate, "unknown"),
            "--orchestrated-staging",
        ]
    before, after = unit.candidates
    prerequisites = _paired_prerequisites(run, unit)
    return [
        sys.executable,
        str(scripts / "compare_plans.py"),
        *common,
        *configuration,
        "--before", str(before),
        "--after", str(after),
        "--comparison-output", str(staging[0]),
        "--before-skill-commit", run.commits.get(before, "unknown"),
        "--after-skill-commit", run.commits.get(after, "unknown"),
        "--before-grade", str(prerequisites[0]),
        "--before-score", str(prerequisites[1]),
        "--after-grade", str(prerequisites[2]),
        "--after-score", str(prerequisites[3]),
        "--orchestrated-staging",
    ]


def print_preflight(run: Run) -> None:
    print(f"run_id: {run.run_id}")
    print(f"timestamp_utc: {run.timestamp_utc}")
    print(f"output_dir: {run.output_dir}")
    for provider in run.providers:
        print(
            f"provider: {provider.name} model={provider.model} effort={provider.effort} "
            f"timeout={run.timeout} configuration={list(provider.configuration)}"
        )
    print("files sent:")
    for unit in run.units:
        if unit.provider is not None:
            files = [*run.sources, run.reference, run.rubric_path, *unit.candidates]
            print(f"  {unit.label}: {', '.join(map(str, files))}")
            command = _leaf_command(run, unit, unit.targets)
            print(f"    command: {shlex.join(command)} < prompt-via-stdin")
        print(f"  {unit.label} -> {', '.join(map(str, unit.targets))} [{unit.status}]")


def _confirm(run: Run) -> None:
    if run.confirm_send:
        return
    if not sys.stdin.isatty():
        raise ValueError("non-interactive runs require --confirm-send")
    response = input("Type SEND to authorize external provider calls: ")
    if response != "SEND":
        raise ValueError("provider send was not confirmed")


def _invoke(command: Sequence[str], timeout: int) -> None:
    result = subprocess.run(
        command, capture_output=True, text=True, timeout=timeout + 30, check=False
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"subprocess failed ({result.returncode}): {detail}")


def _execute_provider_unit(run: Run, unit: Unit) -> None:
    staging = [run.store.create_staging(target) for target in unit.targets]
    try:
        _invoke(_leaf_command(run, unit, staging), run.timeout)
        if unit.kind == "absolute":
            validate_absolute_resume(
                staging[0],
                staging[1],
                run.rubric,
                unit.candidates[0],
                _expected_metadata(run, unit),
            )
        else:
            validate_paired_resume(
                staging[0],
                run.rubric,
                unit.candidates[0],
                unit.candidates[1],
                _paired_prerequisites(run, unit),
                _expected_metadata(run, unit),
            )
        run.store.publish(dict(zip(staging, unit.targets, strict=True)))
    except Exception:
        run.store.cleanup(staging)
        raise


def _execute_adjudication(run: Run, unit: Unit) -> None:
    comparisons, scores = _adjudication_inputs(run, unit)
    comparison_values = [load_artifact(path) for path in comparisons]
    score_values = [(load_artifact(left), load_artifact(right)) for left, right in scores]
    if not adjudication_reasons(comparison_values, score_values):
        unit.status = "not-run"
        unit.reason = "not-required"
        return
    staging = run.store.create_staging(unit.targets[0])
    command = [sys.executable, str(Path(__file__).resolve().parent / "adjudicate.py")]
    for comparison in comparisons:
        command.extend(["--comparison", str(comparison)])
    for left, right in scores:
        command.extend(["--score-pair", str(left), str(right)])
    command.extend(
        [
            "--output", str(staging),
            "--run-id", run.run_id,
            "--timestamp-utc", run.timestamp_utc,
            "--orchestrated-staging",
        ]
    )
    try:
        _invoke(command, run.timeout)
        validate_adjudication_resume(staging, comparisons, scores)
        run.store.publish({staging: unit.targets[0]})
    except Exception:
        run.store.cleanup([staging])
        raise


def _execute_calibration(run: Run, unit: Unit) -> None:
    assert run.manifest is not None
    artifacts = [
        target
        for item in run.units
        if item.kind in {"absolute", "paired"}
        for target in item.targets
    ]
    command = [
        sys.executable,
        str(Path(__file__).resolve().parent / "calibration_report.py"),
        "--manifest",
        str(run.manifest),
        *(str(path) for path in artifacts),
    ]
    result = subprocess.run(
        command, capture_output=True, text=True, timeout=run.timeout, check=False
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "calibration report failed")
    report = json.loads(result.stdout)
    if not isinstance(report, dict) or report.get("thresholds_enforced") is not False:
        raise ValueError("invalid calibration report")
    staging = run.store.create_staging(unit.targets[0])
    try:
        staging.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        run.store.publish({staging: unit.targets[0]})
    except Exception:
        run.store.cleanup([staging])
        raise


def execute(run: Run) -> int:
    if run.dry_run:
        for unit in run.units:
            if unit.status == "planned":
                unit.status = "not-run"
                unit.reason = "dry-run"
        return 0
    _confirm(run)
    failed = False
    for unit in run.units:
        if unit.status != "planned":
            continue
        if failed:
            unit.status = "not-run"
            unit.reason = "fail-fast"
            continue
        try:
            if unit.kind in {"absolute", "paired"}:
                _execute_provider_unit(run, unit)
            elif unit.kind == "adjudication":
                _execute_adjudication(run, unit)
            else:
                _execute_calibration(run, unit)
            if unit.status == "planned":
                unit.status = "completed"
        except (
            OSError,
            json.JSONDecodeError,
            RuntimeError,
            subprocess.SubprocessError,
            ValueError,
        ) as error:
            unit.status = "failed"
            unit.reason = str(error)
            failed = True
    return 2 if failed else 0


def print_summary(run: Run) -> None:
    print("summary:")
    for status in STATUSES:
        matching = [unit for unit in run.units if unit.status == status]
        print(f"  {status}: {len(matching)}")
        for unit in matching:
            suffix = f" ({unit.reason})" if unit.reason else ""
            print(f"    {unit.label}{suffix}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    run: Run | None = None
    try:
        run = materialize_run(parser.parse_args(argv))
        preflight(run)
        return execute(run)
    except (
        OSError,
        json.JSONDecodeError,
        RuntimeError,
        subprocess.SubprocessError,
        ValueError,
    ) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        if run is not None:
            for unit in run.units:
                if unit.status == "planned":
                    unit.status = "not-run"
                    unit.reason = "preflight-failed"
        return 2
    finally:
        if run is not None:
            print_summary(run)


if __name__ == "__main__":
    raise SystemExit(main())
