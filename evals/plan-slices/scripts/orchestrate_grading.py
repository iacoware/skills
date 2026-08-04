#!/usr/bin/env python3
"""Plan and run reproducible v3 grading, adjudication, and calibration."""

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

from adjudication_contract import build_request, resolve_absolute, resolve_paired
from calibration_report import build_report, validate_manifest
from compare_plans import render_comparison_prompt
from evaluator_versions import MANIFEST_VERSION, versioned_artifact_name
from grade_plan import load_object, render_prompt
from grader_runtime import probe_provider, sha256_file, sha256_text
from grading_contract import rubric_contract, score_grade, validate_absolute_grade, validate_comparison
from orchestrator_artifacts import ArtifactStore, candidate_stem, load_object as load_artifact, validate_absolute_resume, validate_paired_resume


DEFAULT_CODEX_MODEL = "gpt-5.6-sol"
DEFAULT_CLAUDE_MODEL = "claude-opus-5"
DEFAULT_EFFORT = "high"
DEFAULT_TIMEOUT = 900
STATUSES = ("completed", "resumed", "pending-review", "failed", "not-run")


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
    run_number: int = 1
    status: str = "planned"
    reason: str | None = None


@dataclass
class Run:
    command: str
    run_id: str
    timestamp_utc: str
    sources: tuple[Path, ...]
    brief: Path
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
    manifest_value: dict[str, object] | None = None
    labels: dict[Path, object] = field(default_factory=dict)
    report_output: Path | None = None
    shard_count: int | None = None
    shard_index: int | None = None
    report_only: bool = False


def _add_common_options(parser: argparse.ArgumentParser, *, provider: bool) -> None:
    parser.add_argument("--source", action="append", required=True, type=Path)
    parser.add_argument("--brief", required=True, type=Path)
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
    grade = commands.add_parser("grade")
    grade.add_argument("plans", nargs="+", type=Path)
    _add_common_options(grade, provider=True)
    compare = commands.add_parser("compare")
    compare.add_argument("before", type=Path)
    compare.add_argument("after", type=Path)
    _add_common_options(compare, provider=True)
    calibrate = commands.add_parser("calibrate")
    calibrate.add_argument("--manifest", required=True, type=Path)
    calibrate.add_argument("--report-output", required=True, type=Path)
    calibrate.add_argument("--critical-subset", action="store_true")
    calibrate.add_argument("--shard-count", type=int)
    calibrate.add_argument("--shard-index", type=int)
    calibrate.add_argument("--report-only", action="store_true")
    _add_common_options(calibrate, provider=False)
    return parser


def _absolute(path: Path, base: Path | None = None) -> Path:
    return Path(os.path.abspath(path if path.is_absolute() else (base or Path.cwd()) / path))


def _deduplicate(paths: Sequence[Path]) -> tuple[Path, ...]:
    return tuple(dict.fromkeys(paths))


def _providers(args: argparse.Namespace) -> tuple[ProviderConfig, ...]:
    names = ("codex", "claude") if args.command == "calibrate" or args.provider == "both" else (args.provider,)
    configs = {
        "codex": ProviderConfig("codex", args.codex_model, args.codex_effort, tuple(args.codex_config)),
        "claude": ProviderConfig("claude", args.claude_model, args.claude_effort),
    }
    return tuple(configs[name] for name in names)


def _parse_commits(values: Sequence[str], candidates: Sequence[Path]) -> dict[Path, str]:
    result: dict[Path, str] = {}
    for value in values:
        name, separator, commit = value.partition("=")
        if not separator or not commit:
            raise ValueError(f"invalid candidate skill commit: {value!r}")
        path = _absolute(Path(name))
        if path not in candidates:
            matches = [candidate for candidate in candidates if candidate.name == Path(name).name]
            if len(matches) == 1:
                path = matches[0]
        if path not in candidates or path in result:
            raise ValueError(f"candidate skill commit does not match workload: {name}")
        result[path] = commit
    return result


def _calibration_partition(args: argparse.Namespace) -> tuple[int | None, int | None]:
    shard_count, shard_index = args.shard_count, args.shard_index
    if (shard_count is None) != (shard_index is None):
        raise ValueError("shard count and shard index must be provided together")
    if shard_count is None:
        return None, None
    if not args.critical_subset:
        raise ValueError("sharding is limited to critical-subset calibration")
    if args.report_only:
        raise ValueError("report-only cannot be combined with sharding")
    if shard_count <= 0 or not 1 <= shard_index <= shard_count:
        raise ValueError("shard index must be between 1 and shard count")
    return shard_count, shard_index


def _manifest_workload(path: Path, *, critical_subset: bool) -> tuple[tuple[Path, ...], tuple[tuple[Path, Path], ...], dict[Path, int], dict[tuple[Path, Path], int], dict[Path, object], dict[str, object]]:
    value = load_object(path)
    validate_manifest(value, path.parent)
    fixtures = [
        fixture
        for fixture in value["fixtures"]
        if not critical_subset or fixture["critical_subset"]
    ]
    if critical_subset and not fixtures:
        raise ValueError("manifest has no critical-subset fixtures")
    pairs = [] if critical_subset else value["paired"]
    fixture_runs: dict[Path, int] = {}
    labels: dict[Path, object] = {}
    for fixture in fixtures:
        candidate = _absolute(Path(fixture["path"]), path.parent)
        fixture_runs[candidate] = fixture["runs"]
        labels[candidate] = fixture["labels"]
    pair_runs: dict[tuple[Path, Path], int] = {}
    for pair in pairs:
        candidates = (
            _absolute(Path(pair["before"]), path.parent),
            _absolute(Path(pair["after"]), path.parent),
        )
        pair_runs[candidates] = pair["runs"]
    candidates = _deduplicate([*fixture_runs, *(candidate for pair in pair_runs for candidate in pair)])
    return candidates, tuple(pair_runs), fixture_runs, pair_runs, labels, value


def materialize_run(args: argparse.Namespace) -> Run:
    if args.timeout <= 0:
        raise ValueError("timeout must be positive")
    run_id = str(uuid.uuid4())
    sources = _deduplicate([_absolute(path) for path in args.source])
    brief, rubric_path, output_dir = _absolute(args.brief), _absolute(args.rubric), _absolute(args.output_dir)
    providers = _providers(args)
    manifest = report_output = None
    manifest_value = None
    labels: dict[Path, object] = {}
    shard_count = shard_index = None
    report_only = False
    if args.command == "grade":
        candidates = _deduplicate([_absolute(path) for path in args.plans])
        pairs: tuple[tuple[Path, Path], ...] = ()
        fixture_runs = {candidate: 1 for candidate in candidates}
        pair_runs: dict[tuple[Path, Path], int] = {}
    elif args.command == "compare":
        pair = (_absolute(args.before), _absolute(args.after))
        if pair[0] == pair[1]:
            raise ValueError("compare requires distinct candidates")
        candidates, pairs = pair, (pair,)
        fixture_runs = {candidate: 1 for candidate in candidates}
        pair_runs = {pair: 1}
    else:
        shard_count, shard_index = _calibration_partition(args)
        report_only = args.report_only
        if report_only and not args.resume:
            raise ValueError("report-only requires resume")
        manifest = _absolute(args.manifest)
        candidates, pairs, fixture_runs, pair_runs, labels, manifest_value = _manifest_workload(
            manifest,
            critical_subset=args.critical_subset,
        )
        report_output = _absolute(args.report_output)
        if report_output.parent != output_dir:
            raise ValueError("report output must be directly inside output directory")
    commits = _parse_commits(args.candidate_skill_commit, candidates)
    store = ArtifactStore(output_dir, run_id)
    repeated = args.command == "calibrate"
    units: list[Unit] = []
    for candidate in candidates:
        for run_number in range(1, fixture_runs.get(candidate, 1) + 1):
            stem = candidate_stem(candidate)
            for provider in providers:
                units.append(Unit(
                    "absolute", f"absolute:{stem}:{provider.name}:run-{run_number:02d}",
                    (
                        store.machine_target(versioned_artifact_name(stem, provider.name, "GRADE", run_number=run_number if repeated else None)),
                        store.machine_target(versioned_artifact_name(stem, provider.name, "SCORE", run_number=run_number if repeated else None)),
                    ), (candidate,), provider, run_number,
                ))
            if len(providers) == 2 and not (
                args.command == "calibrate" and args.critical_subset
            ):
                suffix = f".run-{run_number:02d}" if repeated else ""
                units.append(Unit(
                    "absolute-adjudication", f"absolute-adjudication:{stem}:run-{run_number:02d}",
                    (
                        store.machine_target(f"{stem}.v3{suffix}.ADJUDICATION.REQUEST.json"),
                        store.machine_target(f"{stem}.v3{suffix}.ADJUDICATION.METADATA.json"),
                        store.machine_target(f"{stem}.v3{suffix}.RESOLVED.GRADE.json"),
                        store.machine_target(f"{stem}.v3{suffix}.RESOLVED.SCORE.json"),
                    ), (candidate,), run_number=run_number,
                ))
    for pair in pairs:
        for run_number in range(1, pair_runs[pair] + 1):
            stem = f"{candidate_stem(pair[0])}-to-{candidate_stem(pair[1])}"
            for provider in providers:
                units.append(Unit(
                    "paired", f"paired:{stem}:{provider.name}:run-{run_number:02d}",
                    (store.machine_target(versioned_artifact_name(stem, provider.name, "PAIRED", run_number=run_number if repeated else None)),),
                    pair, provider, run_number,
                ))
            if len(providers) == 2:
                suffix = f".run-{run_number:02d}" if repeated else ""
                units.append(Unit(
                    "paired-adjudication", f"paired-adjudication:{stem}:run-{run_number:02d}",
                    (
                        store.machine_target(f"{stem}.v3{suffix}.ADJUDICATION.REQUEST.json"),
                        store.machine_target(f"{stem}.v3{suffix}.ADJUDICATION.METADATA.json"),
                        store.machine_target(f"{stem}.v3{suffix}.RESOLVED.PAIRED.json"),
                    ), pair, run_number=run_number,
                ))
    if shard_count is not None:
        ordered_labels = sorted(unit.label for unit in units if unit.provider)
        if shard_count > len(ordered_labels):
            raise ValueError("shard count exceeds provider unit count")
        selected_labels = {
            label
            for position, label in enumerate(ordered_labels)
            if position % shard_count == shard_index - 1
        }
        units = [unit for unit in units if unit.label in selected_labels]
    elif report_output:
        units.append(Unit("calibration", "calibration-report", (store.report_target(report_output.name),)))
    return Run(
        args.command, run_id, datetime.now(timezone.utc).isoformat(), sources, brief, rubric_path,
        output_dir, args.timeout, args.dry_run, args.resume, args.confirm_send, commits, providers,
        candidates, pairs, units, store, manifest=manifest, manifest_value=manifest_value,
        labels=labels, report_output=report_output, shard_count=shard_count,
        shard_index=shard_index, report_only=report_only,
    )


def _require_file(path: Path, label: str) -> None:
    if not path.is_file() or not os.access(path, os.R_OK):
        raise ValueError(f"{label} is not a readable regular file: {path}")


def _absolute_unit(run: Run, candidate: Path, provider: str, run_number: int) -> Unit:
    return next(unit for unit in run.units if unit.kind == "absolute" and unit.candidates == (candidate,) and unit.provider and unit.provider.name == provider and unit.run_number == run_number)


def _absolute_adjudication(run: Run, candidate: Path, run_number: int) -> Unit:
    return next(unit for unit in run.units if unit.kind == "absolute-adjudication" and unit.candidates == (candidate,) and unit.run_number == run_number)


def _paired_units(run: Run, pair: tuple[Path, Path], run_number: int) -> list[Unit]:
    return [unit for unit in run.units if unit.kind == "paired" and unit.candidates == pair and unit.run_number == run_number]


def _paired_prerequisites(run: Run, unit: Unit) -> tuple[Path, ...]:
    if len(run.providers) == 2:
        return tuple(
            path
            for candidate in unit.candidates
            for path in _absolute_adjudication(run, candidate, 1 if run.command != "calibrate" else min(unit.run_number, max(item.run_number for item in run.units if item.kind == "absolute-adjudication" and item.candidates == (candidate,)))).targets[2:]
        )
    assert unit.provider
    return tuple(path for candidate in unit.candidates for path in _absolute_unit(run, candidate, unit.provider.name, 1).targets)


def _label_set(run: Run, candidates: Sequence[Path]) -> object | None:
    values = {str(candidate): run.labels[candidate] for candidate in candidates if candidate in run.labels}
    return values or None


def _expected_metadata(run: Run, unit: Unit) -> dict[str, object]:
    assert unit.provider
    aliases = {f"candidate-{chr(65 + index)}": str(candidate) for index, candidate in enumerate(unit.candidates)}
    prompt = render_prompt(run.rubric, run.brief, unit.candidates[0], run.sources) if unit.kind == "absolute" else render_comparison_prompt(run.rubric, run.brief, unit.candidates[0], unit.candidates[1], run.sources)
    return {
        "provider": unit.provider.name,
        "requested_model": unit.provider.model,
        "effort": unit.provider.effort,
        "configuration": list(unit.provider.configuration),
        "cli_version": run.cli_versions.get(unit.provider.name),
        "prompt_sha256": sha256_text(prompt),
        "source_sha256": {str(path): sha256_file(path) for path in run.sources},
        "brief_sha256": sha256_file(run.brief),
        "rubric_sha256": sha256_file(run.rubric_path),
        "candidates": [
            {"path": str(candidate), "sha256": sha256_file(candidate), "skill_commit": run.commits.get(candidate, "unknown")}
            for candidate in unit.candidates
        ],
        "alias_mapping": aliases,
        "manifest_sha256": sha256_file(run.manifest) if run.manifest else None,
        "label_set_sha256": sha256_text(json.dumps(_label_set(run, unit.candidates), sort_keys=True)) if _label_set(run, unit.candidates) is not None else None,
    }


def _validate_plans(run: Run) -> None:
    validator = Path(__file__).resolve().parents[3] / "skills/plan-slices/scripts/validate_plan.py"
    for candidate in run.candidates:
        result = subprocess.run([sys.executable, str(validator), str(candidate)], capture_output=True, text=True, check=False)
        if result.returncode:
            raise ValueError(f"plan validation failed for {candidate}: {result.stderr.strip()}")


def _validate_resume(run: Run) -> None:
    for unit in run.units:
        if unit.kind == "absolute":
            try:
                validate_absolute_resume(unit.targets[0], unit.targets[1], run.rubric, "candidate-A", _expected_metadata(run, unit))
            except FileNotFoundError:
                continue
            unit.status = "resumed"
        elif unit.kind == "paired" and unit.targets[0].exists():
            validate_paired_resume(unit.targets[0], run.rubric, _paired_prerequisites(run, unit), _expected_metadata(run, unit))
            unit.status = "resumed"
        elif unit.kind.endswith("adjudication"):
            request_exists, metadata_exists = unit.targets[0].exists(), unit.targets[1].exists()
            resolved = unit.targets[2:]
            if request_exists != metadata_exists:
                raise ValueError(f"partial adjudication request: {unit.label}")
            if all(path.exists() for path in resolved):
                unit.status = "resumed"
            elif any(path.exists() for path in resolved):
                raise ValueError(f"partial adjudication resolution: {unit.label}")
        elif unit.kind == "calibration" and unit.targets[0].exists():
            if any(item.status not in {"resumed"} for item in run.units if item is not unit):
                raise ValueError("calibration report has incomplete prerequisites")
            unit.status = "resumed"


def preflight(run: Run) -> None:
    for candidate in run.candidates:
        _require_file(candidate, "candidate")
    for source in run.sources:
        _require_file(source, "source")
    _require_file(run.brief, "brief")
    _require_file(run.rubric_path, "rubric")
    if run.manifest:
        _require_file(run.manifest, "manifest")
    run.rubric = load_object(run.rubric_path)
    rubric_contract(run.rubric)
    _validate_plans(run)
    run.store.check_targets((target for unit in run.units for target in unit.targets), resume=run.resume)
    run.cli_versions = {
        provider.name: None if run.dry_run or run.report_only else probe_provider(provider.name)
        for provider in run.providers
    }
    if run.resume:
        _validate_resume(run)
    if run.report_only and any(unit.provider and unit.status != "resumed" for unit in run.units):
        raise ValueError("report-only requires every provider artifact to resume successfully")
    print_preflight(run)


def _leaf_command(run: Run, unit: Unit, staging: Sequence[Path]) -> list[str]:
    assert unit.provider
    scripts = Path(__file__).resolve().parent
    common = [
        "--provider", unit.provider.name, "--rubric", str(run.rubric_path), "--brief", str(run.brief),
        "--sources", *(str(path) for path in run.sources), "--model", unit.provider.model,
        "--effort", unit.provider.effort, "--timeout", str(run.timeout), "--run-id", run.run_id,
        "--timestamp-utc", run.timestamp_utc,
    ]
    if run.manifest:
        common.extend(["--manifest", str(run.manifest)])
    configuration = [item for value in unit.provider.configuration for item in ("--configuration", value)]
    if unit.kind == "absolute":
        candidate = unit.candidates[0]
        return [
            sys.executable, str(scripts / "grade_plan.py"), "run", *common, *configuration,
            "--plan", str(candidate), "--grade-output", str(staging[0]), "--score-output", str(staging[1]),
            "--candidate-skill-commit", run.commits.get(candidate, "unknown"), "--orchestrated-staging",
        ]
    prerequisites = _paired_prerequisites(run, unit)
    return [
        sys.executable, str(scripts / "compare_plans.py"), *common, *configuration,
        "--before", str(unit.candidates[0]), "--after", str(unit.candidates[1]),
        "--comparison-output", str(staging[0]),
        "--before-skill-commit", run.commits.get(unit.candidates[0], "unknown"),
        "--after-skill-commit", run.commits.get(unit.candidates[1], "unknown"),
        "--before-grade", str(prerequisites[0]), "--before-score", str(prerequisites[1]),
        "--after-grade", str(prerequisites[2]), "--after-score", str(prerequisites[3]),
        "--orchestrated-staging",
    ]


def print_preflight(run: Run) -> None:
    absolute_calls = sum(unit.kind == "absolute" for unit in run.units)
    paired_calls = sum(unit.kind == "paired" for unit in run.units)
    adjudications = sum(unit.kind.endswith("adjudication") for unit in run.units)
    print(
        f"external_provider_calls: {absolute_calls + paired_calls}\n"
        f"absolute_provider_calls: {absolute_calls}\n"
        f"paired_provider_calls: {paired_calls}\n"
        f"adjudication_units: {adjudications}"
    )
    if run.shard_count is not None:
        print(f"shard: {run.shard_index}/{run.shard_count}")
    print(f"run_id: {run.run_id}\noutput_dir: {run.output_dir}\nfiles sent:")
    for unit in run.units:
        if unit.provider:
            print(f"  {unit.label}: sources + brief + rubric + {', '.join(map(str, unit.candidates))}")
            print(f"    command: {shlex.join(_leaf_command(run, unit, unit.targets))}")
        print(f"  {unit.label} -> {', '.join(map(str, unit.targets))} [{unit.status}]")


def _confirm(run: Run) -> None:
    if run.confirm_send:
        return
    if not sys.stdin.isatty() or input("Type SEND to authorize external provider calls: ") != "SEND":
        raise ValueError("provider send was not confirmed")


def _invoke(command: Sequence[str], timeout: int) -> None:
    result = subprocess.run(command, capture_output=True, text=True, timeout=timeout + 30, check=False)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())


def _execute_provider(run: Run, unit: Unit) -> None:
    staging = [run.store.create_staging(target) for target in unit.targets]
    try:
        _invoke(_leaf_command(run, unit, staging), run.timeout)
        if unit.kind == "absolute":
            validate_absolute_resume(staging[0], staging[1], run.rubric, "candidate-A", _expected_metadata(run, unit))
        else:
            validate_paired_resume(staging[0], run.rubric, _paired_prerequisites(run, unit), _expected_metadata(run, unit))
        run.store.publish(dict(zip(staging, unit.targets, strict=True)))
    except Exception:
        run.store.cleanup(staging)
        raise


def _resolution_path(unit: Unit) -> Path:
    return unit.targets[0].with_name(unit.targets[0].name.replace("REQUEST", "RESOLUTION"))


def _execute_adjudication(run: Run, unit: Unit) -> None:
    if unit.kind == "absolute-adjudication":
        paths = [_absolute_unit(run, unit.candidates[0], provider.name, unit.run_number).targets[0] for provider in run.providers]
        kind = "absolute"
    else:
        paths = [paired.targets[0] for paired in _paired_units(run, unit.candidates, unit.run_number)]
        kind = "paired"
    values = [load_artifact(path) for path in paths]
    if unit.targets[0].exists():
        request, metadata = load_artifact(unit.targets[0]), load_artifact(unit.targets[1])
        if request.get("input_sha256") != [sha256_file(path) for path in paths]:
            raise ValueError("stale adjudication request")
    else:
        request, metadata = build_request(kind, paths, values)
        staging = [run.store.create_staging(target) for target in unit.targets[:2]]
        try:
            for path, value in zip(staging, (request, metadata), strict=True):
                path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            run.store.publish(dict(zip(staging, unit.targets[:2], strict=True)))
        except Exception:
            run.store.cleanup(staging)
            raise
    resolution_file = _resolution_path(unit)
    resolution = load_artifact(resolution_file) if resolution_file.exists() else None
    if request["status"] == "pending-review" and resolution is None:
        unit.status = "pending-review"
        unit.reason = str(resolution_file)
        return
    staging = [run.store.create_staging(target) for target in unit.targets[2:]]
    try:
        if kind == "absolute":
            grade, score = resolve_absolute(run.rubric, values, request, resolution)
            outputs = (grade, score)
        else:
            outputs = (resolve_paired(run.rubric, values, request, resolution),)
        for path, value in zip(staging, outputs, strict=True):
            path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        run.store.publish(dict(zip(staging, unit.targets[2:], strict=True)))
    except Exception:
        run.store.cleanup(staging)
        raise


def _execute_calibration(run: Run, unit: Unit) -> None:
    assert run.manifest_value is not None
    artifact_paths = [target for item in run.units if item.kind in {"absolute", "paired", "absolute-adjudication", "paired-adjudication"} for target in item.targets if target.exists()]
    report = build_report(run.manifest_value, artifact_paths)
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
                unit.status, unit.reason = "not-run", "dry-run"
        return 0
    if any(unit.status == "planned" and unit.provider for unit in run.units):
        _confirm(run)
    for index, unit in enumerate(run.units):
        if unit.status != "planned":
            continue
        try:
            if unit.kind in {"absolute", "paired"}:
                _execute_provider(run, unit)
            elif unit.kind.endswith("adjudication"):
                _execute_adjudication(run, unit)
            else:
                _execute_calibration(run, unit)
            if unit.status == "planned":
                unit.status = "completed"
            if unit.status == "pending-review":
                for remaining in run.units[index + 1 :]:
                    if remaining.status == "planned":
                        remaining.status, remaining.reason = "not-run", "pending-review"
                return 3
        except (OSError, json.JSONDecodeError, RuntimeError, subprocess.SubprocessError, ValueError) as error:
            unit.status, unit.reason = "failed", str(error)
            for remaining in run.units[index + 1 :]:
                if remaining.status == "planned":
                    remaining.status, remaining.reason = "not-run", "fail-fast"
            return 2
    return 0


def print_summary(run: Run) -> None:
    print("summary:")
    for status in STATUSES:
        matches = [unit for unit in run.units if unit.status == status]
        print(f"  {status}: {len(matches)}")
        for unit in matches:
            print(f"    {unit.label}{f' ({unit.reason})' if unit.reason else ''}")


def main(argv: Sequence[str] | None = None) -> int:
    run: Run | None = None
    try:
        run = materialize_run(build_parser().parse_args(argv))
        preflight(run)
        return execute(run)
    except (OSError, json.JSONDecodeError, RuntimeError, subprocess.SubprocessError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    finally:
        if run:
            print_summary(run)


if __name__ == "__main__":
    raise SystemExit(main())
