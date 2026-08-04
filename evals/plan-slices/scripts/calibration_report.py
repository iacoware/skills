#!/usr/bin/env python3
"""Report calibration agreement without enforcing provisional thresholds."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Sequence

from grade_plan import load_object
from grading_contract import VERDICT_SCORES, object_list


def criterion_verdicts(grade: dict[str, object]) -> dict[str, str]:
    return {
        str(criterion["id"]): str(criterion["verdict"])
        for axis in object_list(grade.get("axes"), "grade.axes")
        for criterion in object_list(axis.get("criteria"), "grade axis.criteria")
    }


def build_report(manifest: dict[str, object], artifacts: Sequence[Path]) -> dict[str, object]:
    fixtures = object_list(manifest.get("fixtures"), "manifest.fixtures")
    fixture_ids = {str(fixture["id"]) for fixture in fixtures}
    fixture_by_name = {Path(str(fixture["path"])).name: str(fixture["id"]) for fixture in fixtures}
    paired_entries = object_list(manifest.get("paired"), "manifest.paired")
    paired_by_candidates = {
        (Path(str(pair["before"])).name, Path(str(pair["after"])).name): str(pair["id"])
        for pair in paired_entries
    }
    grades: dict[str, list[dict[str, object]]] = defaultdict(list)
    scores: dict[str, list[dict[str, object]]] = defaultdict(list)
    comparisons: dict[str, list[dict[str, object]]] = defaultdict(list)
    for artifact in artifacts:
        value = load_object(artifact)
        candidate = value.get("candidate")
        fixture_id = value.get("fixture_id") or (
            fixture_by_name.get(Path(candidate).name) if isinstance(candidate, str) else None
        )
        paired_id = value.get("paired_fixture_id")
        if not isinstance(paired_id, str):
            before = value.get("before_candidate")
            after = value.get("after_candidate")
            if isinstance(before, str) and isinstance(after, str):
                paired_id = paired_by_candidates.get((Path(before).name, Path(after).name))
        if isinstance(fixture_id, str) and fixture_id in fixture_ids:
            axes = object_list(value.get("axes"), "artifact.axes")
            if axes and "criteria" in axes[0]:
                grades[fixture_id].append(value)
            elif axes and "score" in axes[0]:
                scores[fixture_id].append(value)
        elif isinstance(paired_id, str):
            comparisons[paired_id].append(value)

    exact = 0
    adjacent = 0
    compared = 0
    critical_agreements = 0
    critical_compared = 0
    for fixture_grades in grades.values():
        for left_index, left in enumerate(fixture_grades):
            for right in fixture_grades[left_index + 1 :]:
                left_verdicts = criterion_verdicts(left)
                right_verdicts = criterion_verdicts(right)
                for criterion_id in set(left_verdicts) & set(right_verdicts):
                    difference = abs(
                        VERDICT_SCORES[left_verdicts[criterion_id]]
                        - VERDICT_SCORES[right_verdicts[criterion_id]]
                    )
                    compared += 1
                    exact += difference == 0
                    adjacent += difference <= 1
                left_failures = {str(item["id"]) for item in object_list(left.get("critical_failures"), "critical_failures")}
                right_failures = {str(item["id"]) for item in object_list(right.get("critical_failures"), "critical_failures")}
                critical_compared += 1
                critical_agreements += left_failures == right_failures

    total_spreads = [
        max(float(score["effective_total"]) for score in fixture_scores)
        - min(float(score["effective_total"]) for score in fixture_scores)
        for fixture_scores in scores.values()
        if len(fixture_scores) > 1
    ]
    paired_expected = {
        str(pair["id"]): pair.get("expected_directions", {})
        for pair in paired_entries
    }
    paired_checks = 0
    paired_correct = 0
    for paired_id, results in comparisons.items():
        expected = paired_expected.get(paired_id, {})
        if not isinstance(expected, dict):
            continue
        for result in results:
            actual = {
                str(criterion["id"]): criterion.get("direction")
                for axis in object_list(result.get("axes"), "comparison.axes")
                for criterion in object_list(axis.get("criteria"), "comparison axis.criteria")
            }
            for criterion_id, direction in expected.items():
                paired_checks += 1
                paired_correct += actual.get(criterion_id) == direction

    return {
        "criterion_pairs": compared,
        "exact_agreement": round(exact / compared, 4) if compared else None,
        "within_one_severity": round(adjacent / compared, 4) if compared else None,
        "critical_failure_pairs": critical_compared,
        "critical_failure_agreement": (
            round(critical_agreements / critical_compared, 4) if critical_compared else None
        ),
        "maximum_total_score_spread": max(total_spreads) if total_spreads else None,
        "paired_checks": paired_checks,
        "paired_direction_accuracy": round(paired_correct / paired_checks, 4) if paired_checks else None,
        "thresholds_enforced": False,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("artifacts", nargs="*", type=Path)
    args = parser.parse_args(argv)

    print(json.dumps(build_report(load_object(args.manifest), args.artifacts), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
