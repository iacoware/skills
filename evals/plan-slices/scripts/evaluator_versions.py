#!/usr/bin/env python3
"""Independent evaluator contract versions."""

RUBRIC_VERSION = 3
GRADE_SCHEMA_VERSION = 3
SCORING_VERSION = 3
ADJUDICATION_VERSION = 3
MANIFEST_VERSION = 3


def versioned_artifact_name(
    stem: str,
    provider: str | None,
    kind: str,
    *,
    run_number: int | None = None,
) -> str:
    if not stem or "/" in stem or "\\" in stem:
        raise ValueError(f"unsafe artifact stem: {stem!r}")
    parts = [stem]
    if provider:
        parts.append(provider)
    parts.append("v3")
    if run_number is not None:
        if run_number <= 0:
            raise ValueError("run number must be positive")
        parts.append(f"run-{run_number:02d}")
    parts.append(kind)
    return ".".join(parts) + ".json"
