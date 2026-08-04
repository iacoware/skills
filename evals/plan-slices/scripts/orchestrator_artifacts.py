#!/usr/bin/env python3
"""Secure v3 artifact naming, resume validation, staging, and publication."""

from __future__ import annotations

import json
import os
import stat
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

from grader_runtime import sha256_file
from grading_contract import score_grade, validate_comparison


def candidate_stem(path: Path) -> str:
    stem = path.stem
    if not stem or stem.startswith(".") or Path(stem).name != stem or any(char in stem for char in "/\\"):
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
        self._validate_path_chain(self.raw_root)
        if root.exists() and not root.is_dir():
            raise ValueError(f"output root is not a directory: {root}")

    @property
    def raw_root(self) -> Path:
        return self.root / "raw"

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

    @staticmethod
    def _validate_name(name: str) -> None:
        if not name or Path(name).name != name or name in {".", ".."}:
            raise ValueError(f"unsafe artifact name: {name!r}")

    def machine_target(self, name: str) -> Path:
        self._validate_name(name)
        target = self.raw_root / name
        self._reject_symlink(target)
        return target

    def report_target(self, name: str) -> Path:
        self._validate_name(name)
        target = self.root / name
        self._reject_symlink(target)
        return target

    def _validate_target(self, target: Path) -> None:
        if target.parent not in {self.root, self.raw_root}:
            raise ValueError(f"artifact escapes output layout: {target}")
        self._reject_symlink(target)

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
            self._validate_target(target)
            if target.exists() and not resume:
                raise ValueError(f"refusing to overwrite existing artifact: {target}")

    def create_staging(self, target: Path) -> Path:
        self._validate_target(target)
        self._validate_path_chain(target.parent)
        target.parent.mkdir(parents=True, exist_ok=True)
        descriptor, name = tempfile.mkstemp(
            prefix=f".{self.run_id}.", suffix=f".{target.name}", dir=target.parent
        )
        os.fchmod(descriptor, 0o600)
        os.close(descriptor)
        return Path(name)

    def publish(self, staging_targets: Mapping[Path, Path]) -> None:
        for staging, target in staging_targets.items():
            self._validate_target(target)
            mode = os.lstat(staging).st_mode
            if (
                staging.parent != target.parent
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
        for parent in {target.parent for target in staging_targets.values()}:
            descriptor = os.open(parent, os.O_RDONLY)
            try:
                os.fsync(descriptor)
            finally:
                os.close(descriptor)

    def cleanup(self, paths: Iterable[Path]) -> None:
        prefix = f".{self.run_id}."
        for path in paths:
            if path.parent in {self.root, self.raw_root} and path.name.startswith(prefix):
                try:
                    path.unlink()
                except FileNotFoundError:
                    pass


def _metadata(artifact: dict[str, object], label: str) -> dict[str, object]:
    metadata = artifact.get("grader")
    if not isinstance(metadata, dict):
        raise ValueError(f"{label}: missing grader metadata")
    for field in ("run_id", "timestamp_utc"):
        if not isinstance(metadata.get(field), str) or not metadata[field]:
            raise ValueError(f"{label}: missing {field}")
    return metadata


def validate_metadata(artifact: dict[str, object], expected: Mapping[str, object], label: str) -> None:
    metadata = _metadata(artifact, label)
    for key, value in expected.items():
        if key == "cli_version" and value is None:
            if not isinstance(metadata.get(key), str) or not metadata[key]:
                raise ValueError(f"{label}: missing cli_version")
        elif metadata.get(key) != value:
            raise ValueError(f"{label}: incompatible {key}")


def validate_absolute_resume(
    grade_path: Path,
    score_path: Path,
    rubric: dict[str, object],
    candidate_alias: str,
    expected_metadata: Mapping[str, object],
) -> None:
    if grade_path.exists() != score_path.exists():
        raise ValueError(f"partial absolute artifact pair: {grade_path}, {score_path}")
    if not grade_path.exists():
        raise FileNotFoundError
    grade, score = load_object(grade_path), load_object(score_path)
    if grade.get("candidate") != candidate_alias or score.get("candidate") != candidate_alias:
        raise ValueError("absolute artifact candidate alias mismatch")
    derived = score_grade(rubric, grade)
    if {key: value for key, value in score.items() if key != "grader"} != derived:
        raise ValueError(f"score does not match grade: {score_path}")
    validate_metadata(grade, expected_metadata, str(grade_path))
    validate_metadata(score, expected_metadata, str(score_path))
    if grade["grader"] != score["grader"]:
        raise ValueError("grade/score metadata mismatch")


def validate_paired_resume(
    paired_path: Path,
    rubric: dict[str, object],
    prerequisites: Sequence[Path],
    expected_metadata: Mapping[str, object],
) -> None:
    comparison = load_object(paired_path)
    validate_comparison(rubric, comparison)
    expected_inputs = [{"path": str(path), "sha256": sha256_file(path)} for path in prerequisites]
    if comparison.get("prerequisites") != expected_inputs:
        raise ValueError(f"paired prerequisite mismatch: {paired_path}")
    validate_metadata(comparison, expected_metadata, str(paired_path))
