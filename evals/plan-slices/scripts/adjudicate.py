#!/usr/bin/env python3
"""Create and resolve blind v3 absolute or paired adjudications."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from adjudication_contract import build_request, resolve_absolute, resolve_paired
from grade_plan import load_object
from grader_runtime import ensure_new_outputs, sha256_file


def _write(path: Path, value: dict[str, object]) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _inputs_from_metadata(metadata: dict[str, object]) -> tuple[list[Path], list[dict[str, object]]]:
    records = metadata.get("inputs")
    if not isinstance(records, list):
        raise ValueError("adjudication metadata has no inputs")
    paths: list[Path] = []
    values: list[dict[str, object]] = []
    for record in records:
        if not isinstance(record, dict) or not isinstance(record.get("path"), str):
            raise ValueError("invalid adjudication input metadata")
        path = Path(record["path"])
        if sha256_file(path) != record.get("sha256"):
            raise ValueError(f"stale adjudication input: {path}")
        paths.append(path)
        values.append(load_object(path))
    return paths, values


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    request = commands.add_parser("request")
    request.add_argument("--type", required=True, choices=("absolute", "paired"))
    request.add_argument("--input", action="append", required=True, type=Path)
    request.add_argument("--request-output", required=True, type=Path)
    request.add_argument("--metadata-output", required=True, type=Path)
    resolve = commands.add_parser("resolve")
    resolve.add_argument("--request", required=True, type=Path)
    resolve.add_argument("--metadata", required=True, type=Path)
    resolve.add_argument("--resolution", type=Path)
    resolve.add_argument("--rubric", required=True, type=Path)
    resolve.add_argument("--grade-output", type=Path)
    resolve.add_argument("--score-output", type=Path)
    resolve.add_argument("--paired-output", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "request":
            if len(args.input) != 2:
                raise ValueError("request requires exactly two inputs")
            ensure_new_outputs([args.request_output, args.metadata_output])
            values = [load_object(path) for path in args.input]
            request, metadata = build_request(args.type, args.input, values)
            _write(args.request_output, request)
            _write(args.metadata_output, metadata)
            print(request["status"])
            return 3 if request["status"] == "pending-review" else 0

        request = load_object(args.request)
        metadata = load_object(args.metadata)
        paths, values = _inputs_from_metadata(metadata)
        if request.get("input_sha256") != [sha256_file(path) for path in paths]:
            raise ValueError("request input hashes are stale")
        resolution = load_object(args.resolution) if args.resolution else None
        rubric = load_object(args.rubric)
        if request.get("type") == "absolute":
            if args.grade_output is None or args.score_output is None or args.paired_output:
                raise ValueError("absolute resolve requires grade and score outputs")
            if not args.grade_output.name.endswith(".v3.RESOLVED.GRADE.json"):
                raise ValueError("resolved grade output has an invalid name")
            if not args.score_output.name.endswith(".v3.RESOLVED.SCORE.json"):
                raise ValueError("resolved score output has an invalid name")
            ensure_new_outputs([args.grade_output, args.score_output])
            grade, score = resolve_absolute(rubric, values, request, resolution)
            _write(args.grade_output, grade)
            _write(args.score_output, score)
        else:
            if args.paired_output is None or args.grade_output or args.score_output:
                raise ValueError("paired resolve requires one paired output")
            if not args.paired_output.name.endswith(".v3.RESOLVED.PAIRED.json"):
                raise ValueError("resolved paired output has an invalid name")
            ensure_new_outputs([args.paired_output])
            _write(args.paired_output, resolve_paired(rubric, values, request, resolution))
        return 0
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 3 if str(error) == "pending-review" else 2


if __name__ == "__main__":
    raise SystemExit(main())
