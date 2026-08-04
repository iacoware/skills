#!/usr/bin/env python3
"""Secure artifact naming, resume validation, staging, and publication."""

from __future__ import annotations

import json
import os
import stat
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

from grader_runtime import sha256_file
from grading_contract import adjudication_reasons, score_grade, validate_comparison


def candidate_stem(path: Path) -> str:
    stem = path.stem
    if not stem or stem.startswith(".") or stem in {".", ".."} or Path(stem).name != stem:
        raise ValueError(f"unsafe candidate name: {path.name}")
    if any(separator in stem for separator in ("/", "\\")):
        raise ValueError(f"unsafe candidate name: {path.name}")
    return stem


def load_object(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


@dataclass(frozen=True)
class ArtifactStore:
    root: Path
    run_id: str

    def __post_init__(self) -> None:
        root = Path(os.path.abspath(self.root))
        object.__setattr__(self, "root", root)
        self._validate_path_chain(root)
        if root.exists() and not root.is_dir():
            raise ValueError(f"output root is not a directory: {root}")

    @staticmethod
    def _validate_path_chain(path: Path) -> None:
        current = path
        while True:
            try:
                mode = os.lstat(current).st_mode
            except FileNotFoundError:
                pass
            else:
                if stat.S_ISLNK(mode):
                    raise ValueError(f"symlink is forbidden in output path: {current}")
            if current.parent == current:
                return
            current = current.parent

    def target(self, name: str) -> Path:
        if not name or Path(name).name != name or name in {".", ".."}:
            raise ValueError(f"unsafe artifact name: {name!r}")
        target = self.root / name
        if target.parent != self.root:
            raise ValueError(f"artifact escapes output root: {target}")
        self._reject_symlink(target)
        return target

    @staticmethod
    def _reject_symlink(path: Path) -> None:
        try:
            mode = os.lstat(path).st_mode
        except FileNotFoundError:
            return
        if stat.S_ISLNK(mode):
            raise ValueError(f"artifact target is a symlink: {path}")

    def check_targets(self, targets: Iterable[Path], *, resume: bool) -> None:
        target_list = list(targets)
        if len(target_list) != len(set(target_list)):
            raise ValueError("multiple units resolve to the same artifact")
        for target in target_list:
            if target.parent != self.root:
                raise ValueError(f"artifact escapes output root: {target}")
            self._reject_symlink(target)
            if target.exists() and not resume:
                raise ValueError(f"refusing to overwrite existing artifact: {target}")

    def create_staging(self, target: Path) -> Path:
        self._validate_path_chain(self.root)
        self.root.mkdir(parents=True, exist_ok=True)
        self._validate_path_chain(self.root)
        descriptor, name = tempfile.mkstemp(
            prefix=f".{self.run_id}.", suffix=f".{target.name}", dir=self.root
        )
        os.fchmod(descriptor, 0o600)
        os.close(descriptor)
        return Path(name)

    def publish(self, staging_targets: Mapping[Path, Path]) -> None:
        for staging in staging_targets:
            try:
                mode = os.lstat(staging).st_mode
            except FileNotFoundError as error:
                raise ValueError(f"missing staging artifact: {staging}") from error
            if (
                staging.parent != self.root
                or not staging.name.startswith(f".{self.run_id}.")
                or not stat.S_ISREG(mode)
            ):
                raise ValueError(f"unsafe staging artifact: {staging}")
            with staging.open("rb") as stream:
                os.fsync(stream.fileno())
        for target in staging_targets.values():
            self._reject_symlink(target)
            if target.exists():
                raise FileExistsError(f"artifact appeared after preflight: {target}")
        for staging, target in staging_targets.items():
            os.link(staging, target, follow_symlinks=False)
            staging.unlink()
        directory_descriptor = os.open(self.root, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)

    def cleanup(self, paths: Iterable[Path]) -> None:
        prefix = f".{self.run_id}."
        for path in paths:
            if path.parent == self.root and path.name.startswith(prefix):
                try:
                    path.unlink()
                except FileNotFoundError:
                    pass


def _metadata(artifact: dict[str, object], label: str) -> dict[str, object]:
    metadata = artifact.get("grader")
    if not isinstance(metadata, dict):
        raise ValueError(f"{label}: missing grader metadata")
    if not isinstance(metadata.get("run_id"), str) or not metadata["run_id"]:
        raise ValueError(f"{label}: missing run_id")
    if not isinstance(metadata.get("timestamp_utc"), str) or not metadata["timestamp_utc"]:
        raise ValueError(f"{label}: missing timestamp_utc")
    return metadata


def validate_metadata(
    artifact: dict[str, object], expected: Mapping[str, object], label: str
) -> None:
    metadata = _metadata(artifact, label)
    for key, value in expected.items():
        if key == "cli_version" and value is None:
            if not isinstance(metadata.get(key), str) or not metadata[key]:
                raise ValueError(f"{label}: missing {key}")
            continue
        if key == "candidates":
            _validate_candidates(metadata.get(key), value, label)
            continue
        if metadata.get(key) != value:
            raise ValueError(f"{label}: incompatible {key}")


def _validate_candidates(actual: object, expected: object, label: str) -> None:
    if (
        not isinstance(actual, list)
        or not isinstance(expected, list)
        or len(actual) != len(expected)
    ):
        raise ValueError(f"{label}: incompatible candidates")
    for actual_item, expected_item in zip(actual, expected, strict=True):
        if not isinstance(actual_item, dict) or not isinstance(expected_item, dict):
            raise ValueError(f"{label}: invalid candidate metadata")
        for key in ("path", "sha256"):
            if actual_item.get(key) != expected_item.get(key):
                raise ValueError(f"{label}: incompatible candidate {key}")
        expected_commit = expected_item.get("skill_commit")
        if expected_commit != "unknown" and actual_item.get("skill_commit") != expected_commit:
            raise ValueError(f"{label}: incompatible candidate skill_commit")


def validate_absolute_resume(
    grade_path: Path,
    score_path: Path,
    rubric: dict[str, object],
    candidate: Path,
    expected_metadata: Mapping[str, object],
) -> None:
    if grade_path.exists() != score_path.exists():
        raise ValueError(f"partial absolute artifact pair: {grade_path}, {score_path}")
    if not grade_path.exists():
        raise FileNotFoundError
    grade = load_object(grade_path)
    score = load_object(score_path)
    if grade.get("candidate") != str(candidate) or score.get("candidate") != str(candidate):
        raise ValueError(f"absolute artifact candidate mismatch: {candidate}")
    derived = score_grade(rubric, grade)
    actual_derived = {key: value for key, value in score.items() if key != "grader"}
    if actual_derived != derived:
        raise ValueError(f"score does not match grade: {score_path}")
    validate_metadata(grade, expected_metadata, str(grade_path))
    validate_metadata(score, expected_metadata, str(score_path))
    if grade["grader"] != score["grader"]:
        raise ValueError(f"grade/score metadata mismatch: {grade_path}, {score_path}")


def validate_paired_resume(
    paired_path: Path,
    rubric: dict[str, object],
    before: Path,
    after: Path,
    prerequisites: Sequence[Path],
    expected_metadata: Mapping[str, object],
) -> None:
    comparison = load_object(paired_path)
    validate_comparison(rubric, comparison)
    if comparison.get("before_candidate") != str(before):
        raise ValueError(f"paired before candidate mismatch: {paired_path}")
    if comparison.get("after_candidate") != str(after):
        raise ValueError(f"paired after candidate mismatch: {paired_path}")
    expected_inputs = [
        {"path": str(path), "sha256": sha256_file(path)} for path in prerequisites
    ]
    if comparison.get("prerequisites") != expected_inputs:
        raise ValueError(f"paired prerequisite mismatch: {paired_path}")
    validate_metadata(comparison, expected_metadata, str(paired_path))


def validate_adjudication_resume(
    path: Path,
    comparison_paths: Sequence[Path],
    score_pairs: Sequence[tuple[Path, Path]],
) -> None:
    artifact = load_object(path)
    if not isinstance(artifact.get("run_id"), str) or not artifact["run_id"]:
        raise ValueError(f"adjudication missing run_id: {path}")
    if not isinstance(artifact.get("timestamp_utc"), str) or not artifact["timestamp_utc"]:
        raise ValueError(f"adjudication missing timestamp_utc: {path}")
    comparisons = [load_object(item) for item in comparison_paths]
    scores = [(load_object(left), load_object(right)) for left, right in score_pairs]
    reasons = adjudication_reasons(comparisons, scores)
    if not reasons:
        raise ValueError(f"adjudication exists but is not required: {path}")
    if artifact.get("required") is not True or artifact.get("status") != "pending-blind-review":
        raise ValueError(f"invalid adjudication state: {path}")
    if artifact.get("resolution") is not None or artifact.get("triggers") != reasons:
        raise ValueError(f"incompatible adjudication: {path}")
    _validate_input_records(artifact.get("comparison_inputs"), comparison_paths, path)
    flattened_scores = [item for pair in score_pairs for item in pair]
    actual_score_groups = artifact.get("score_inputs")
    if not isinstance(actual_score_groups, list):
        raise ValueError(f"invalid adjudication score inputs: {path}")
    actual_scores = [
        item for group in actual_score_groups if isinstance(group, list) for item in group
    ]
    _validate_input_records(actual_scores, flattened_scores, path)


def _validate_input_records(actual: object, inputs: Sequence[Path], artifact: Path) -> None:
    if not isinstance(actual, list) or len(actual) != len(inputs):
        raise ValueError(f"input metadata mismatch: {artifact}")
    for record, input_path in zip(actual, inputs, strict=True):
        expected = {"path": str(input_path), "sha256": sha256_file(input_path)}
        if not isinstance(record, dict) or any(
            record.get(key) != value for key, value in expected.items()
        ):
            raise ValueError(f"input hash mismatch: {artifact}")
