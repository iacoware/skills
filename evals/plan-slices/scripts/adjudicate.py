#!/usr/bin/env python3
"""Create an auditable blind-adjudication request from independent grader artifacts."""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

from grade_plan import load_object
from grader_runtime import ensure_new_outputs, require_owned_staging, sha256_file
from grading_contract import adjudication_reasons


def _input_record(path: Path, value: dict[str, object]) -> dict[str, object]:
    return {"path": str(path), "sha256": sha256_file(path), "grader": value.get("grader")}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--comparison", action="append", required=True, type=Path)
    parser.add_argument("--score-pair", action="append", nargs=2, default=[], type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--run-id")
    parser.add_argument("--timestamp-utc")
    parser.add_argument("--orchestrated-staging", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)

    try:
        if not args.output.name.endswith(".ADJUDICATION.json"):
            raise ValueError("adjudication output must end with .ADJUDICATION.json")
        if args.orchestrated_staging:
            require_owned_staging([args.output], args.run_id)
        else:
            ensure_new_outputs([args.output])
        comparisons = [load_object(path) for path in args.comparison]
        candidate_pairs = {
            (comparison.get("before_candidate"), comparison.get("after_candidate"))
            for comparison in comparisons
        }
        if len(candidate_pairs) != 1:
            raise ValueError("comparison inputs must evaluate the same before/after candidates")
        before_candidate, after_candidate = next(iter(candidate_pairs))
        score_values = [
            (load_object(left), load_object(right)) for left, right in args.score_pair
        ]
        if any(left.get("candidate") != right.get("candidate") for left, right in score_values):
            raise ValueError("each score pair must evaluate the same candidate")
        reasons = adjudication_reasons(comparisons, score_values)
        artifact = {
            "required": bool(reasons),
            "triggers": reasons,
            "status": "pending-blind-review" if reasons else "not-required",
            "resolution": None,
            "before_candidate": before_candidate,
            "after_candidate": after_candidate,
            "run_id": args.run_id or str(uuid.uuid4()),
            "timestamp_utc": args.timestamp_utc or datetime.now(timezone.utc).isoformat(),
            "blind_review": {
                "aliases": [f"grader-{index}" for index in range(1, len(comparisons) + 1)],
                "instruction": (
                    "Adjudicator reviews aliased payloads before audit metadata is revealed."
                ),
            },
            "comparison_inputs": [
                _input_record(path, value)
                for path, value in zip(args.comparison, comparisons, strict=True)
            ],
            "score_inputs": [
                [_input_record(path, value) for path, value in zip(paths, values, strict=True)]
                for paths, values in zip(args.score_pair, score_values, strict=True)
            ],
        }
        args.output.write_text(
            json.dumps(artifact, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(json.dumps(artifact, indent=2, ensure_ascii=False))
        return 0
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
