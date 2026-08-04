#!/usr/bin/env python3
"""Build the labeled v3 calibration report without enforcing thresholds."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from itertools import combinations, product
from pathlib import Path
from typing import Iterable, Sequence

from evaluator_versions import GRADE_SCHEMA_VERSION, MANIFEST_VERSION, RUBRIC_VERSION
from grade_plan import load_object
from grading_contract import VERDICT_SCORES, object_list
from scoring import SCORING_VERSION, score_strategies


def _metric(numerator: int, denominator: int) -> dict[str, object]:
    return {
        "numerator": numerator,
        "denominator": denominator,
        "value": round(numerator / denominator, 4) if denominator else None,
    }


def _resolved_fixture_labels(manifest: dict[str, object], labels: dict[str, object]) -> dict[str, object]:
    profiles = manifest.get("label_profiles", {})
    profile_name = labels.get("profile")
    base = profiles.get(profile_name, {}) if isinstance(profiles, dict) else {}
    if not isinstance(base, dict):
        raise ValueError(f"unknown fixture label profile: {profile_name}")
    criteria = dict(base)
    overrides = labels.get("criteria", {})
    if not isinstance(overrides, dict):
        raise ValueError("fixture criteria overrides must be an object")
    criteria.update(overrides)
    return {**labels, "criteria": criteria}


def _resolved_pair_labels(manifest: dict[str, object], labels: dict[str, object]) -> dict[str, object]:
    profiles = manifest.get("pair_profiles", {})
    profile_name = labels.get("profile")
    base = profiles.get(profile_name, {}) if isinstance(profiles, dict) else {}
    if not isinstance(base, dict):
        raise ValueError(f"unknown paired label profile: {profile_name}")
    directions = dict(base)
    overrides = labels.get("directions", {})
    if not isinstance(overrides, dict):
        raise ValueError("paired direction overrides must be an object")
    directions.update(overrides)
    return {**labels, "directions": directions}


def validate_manifest(manifest: dict[str, object], base: Path) -> None:
    expected_versions = {
        "manifest_version": MANIFEST_VERSION,
        "rubric_version": RUBRIC_VERSION,
        "grade_schema_version": GRADE_SCHEMA_VERSION,
        "scoring_version": SCORING_VERSION,
    }
    for field, expected in expected_versions.items():
        if manifest.get(field) != expected:
            raise ValueError(f"manifest.{field}: expected {expected}")
    criterion_ids = manifest.get("criterion_ids")
    if not isinstance(criterion_ids, list) or not criterion_ids or len(criterion_ids) != len(set(criterion_ids)) or not all(isinstance(item, str) and item for item in criterion_ids):
        raise ValueError("manifest.criterion_ids must be a unique non-empty string list")
    seen_ids: set[str] = set()
    seen_paths: set[Path] = set()
    for group in ("fixtures", "paired"):
        for entry in object_list(manifest.get(group), f"manifest.{group}"):
            entry_id = entry.get("id")
            if not isinstance(entry_id, str) or not entry_id or entry_id in seen_ids:
                raise ValueError(f"manifest.{group}: duplicate or invalid id {entry_id}")
            seen_ids.add(entry_id)
            runs = entry.get("runs")
            if not isinstance(runs, int) or isinstance(runs, bool) or runs <= 0:
                raise ValueError(f"manifest {entry_id}: runs must be positive")
            if group == "fixtures" and not isinstance(entry.get("critical_subset"), bool):
                raise ValueError(f"manifest {entry_id}: critical_subset must be boolean")
            paths = [entry.get("path")] if group == "fixtures" else [entry.get("before"), entry.get("after")]
            for value in paths:
                if not isinstance(value, str):
                    raise ValueError(f"manifest {entry_id}: missing path")
                path = (base / value).resolve()
                if group == "fixtures" and path in seen_paths:
                    raise ValueError(f"manifest fixtures: duplicate path {value}")
                if not path.is_file():
                    raise ValueError(f"manifest {entry_id}: missing fixture {value}")
                if group == "fixtures":
                    seen_paths.add(path)
            labels = entry.get("labels")
            if not isinstance(labels, dict):
                raise ValueError(f"manifest {entry_id}: labels must be an object")
            provenance = labels.get("provenance")
            if not isinstance(provenance, dict) or not all(provenance.get(key) for key in ("reviewer", "reviewed_at", "method")):
                raise ValueError(f"manifest {entry_id}: label provenance is incomplete")
            if group == "fixtures":
                labels = _resolved_fixture_labels(manifest, labels)
                criteria = labels.get("criteria")
                if not isinstance(criteria, dict) or set(criteria) != set(criterion_ids):
                    raise ValueError(f"manifest {entry_id}: criterion labels are incomplete")
                for criterion_id, allowed in criteria.items():
                    if not isinstance(allowed, list) or not allowed or not set(allowed) <= set(VERDICT_SCORES):
                        raise ValueError(f"manifest {entry_id}: invalid verdict labels for {criterion_id}")
                critical = labels.get("critical_failures")
                if not isinstance(critical, dict) or not isinstance(critical.get("expected"), list) or not isinstance(critical.get("absent"), list):
                    raise ValueError(f"manifest {entry_id}: incomplete critical-failure labels")
                primary = labels.get("primary_criteria")
                if not isinstance(primary, list) or not all(item in criterion_ids for item in primary):
                    raise ValueError(f"manifest {entry_id}: invalid primary-criterion labels")
            else:
                labels = _resolved_pair_labels(manifest, labels)
                directions = labels.get("directions")
                invariant = labels.get("invariant_criteria")
                if not isinstance(directions, dict) or not isinstance(invariant, list):
                    raise ValueError(f"manifest {entry_id}: incomplete paired labels")
                if set(directions) | set(invariant) != set(criterion_ids):
                    raise ValueError(f"manifest {entry_id}: paired criterion labels are incomplete")


def criterion_verdicts(grade: dict[str, object]) -> dict[str, str]:
    return {
        str(entry["id"]): str(entry["verdict"])
        for axis in object_list(grade.get("axes"), "grade.axes")
        for entry in object_list(axis.get("criteria"), "grade axis.criteria")
    }


def _candidate_path(value: dict[str, object]) -> str | None:
    grader = value.get("grader")
    if not isinstance(grader, dict):
        return None
    mapping = grader.get("alias_mapping")
    candidate = value.get("candidate")
    if isinstance(mapping, dict) and isinstance(candidate, str) and isinstance(mapping.get(candidate), str):
        return str(mapping[candidate])
    return None


def _provider(value: dict[str, object]) -> str | None:
    grader = value.get("grader")
    return str(grader["provider"]) if isinstance(grader, dict) and isinstance(grader.get("provider"), str) else None


def _pair_paths(value: dict[str, object]) -> tuple[str, str] | None:
    grader = value.get("grader")
    if not isinstance(grader, dict) or not isinstance(grader.get("alias_mapping"), dict):
        return None
    mapping = grader["alias_mapping"]
    before, after = mapping.get("candidate-A"), mapping.get("candidate-B")
    return (str(before), str(after)) if isinstance(before, str) and isinstance(after, str) else None


def _agreement(pairs: Iterable[tuple[dict[str, object], dict[str, object]]]) -> dict[str, object]:
    exact = total = within_one = 0
    by_criterion: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for left, right in pairs:
        left_verdicts, right_verdicts = criterion_verdicts(left), criterion_verdicts(right)
        for criterion_id in set(left_verdicts) & set(right_verdicts):
            difference = abs(VERDICT_SCORES[left_verdicts[criterion_id]] - VERDICT_SCORES[right_verdicts[criterion_id]])
            total += 1
            exact += difference == 0
            within_one += difference <= 1
            by_criterion[criterion_id][1] += 1
            by_criterion[criterion_id][0] += difference == 0
    return {
        "exact": _metric(exact, total),
        "within_one": _metric(within_one, total),
        "by_criterion": {criterion_id: _metric(*counts) for criterion_id, counts in sorted(by_criterion.items())},
    }


def build_report(manifest: dict[str, object], artifacts: Sequence[Path]) -> dict[str, object]:
    fixtures = object_list(manifest.get("fixtures"), "manifest.fixtures")
    pairs = object_list(manifest.get("paired"), "manifest.paired")
    fixture_by_name = {Path(str(entry["path"])).name: entry for entry in fixtures}
    pair_by_names = {(Path(str(entry["before"])).name, Path(str(entry["after"])).name): entry for entry in pairs}
    grades: dict[str, list[dict[str, object]]] = defaultdict(list)
    comparisons: dict[str, list[dict[str, object]]] = defaultdict(list)
    scores: list[dict[str, object]] = []
    for path in artifacts:
        try:
            value = load_object(path)
        except (OSError, json.JSONDecodeError, ValueError):
            continue
        candidate_path = _candidate_path(value)
        if candidate_path and (fixture := fixture_by_name.get(Path(candidate_path).name)):
            if "defects" in value:
                grades[str(fixture["id"])].append(value)
            elif "components" in value:
                scores.append(value)
            continue
        pair_paths = _pair_paths(value)
        if pair_paths and (pair := pair_by_names.get((Path(pair_paths[0]).name, Path(pair_paths[1]).name))):
            comparisons[str(pair["id"])].append(value)

    accuracy_hits = accuracy_total = 0
    accuracy_by_criterion: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    accuracy_by_provider: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    critical_tp = critical_fp = critical_fn = 0
    primary_hits = primary_total = 0
    for fixture in fixtures:
        fixture_id = str(fixture["id"])
        labels = _resolved_fixture_labels(manifest, fixture["labels"])
        for grade in grades[fixture_id]:
            provider = _provider(grade) or "unknown"
            for criterion_id, verdict in criterion_verdicts(grade).items():
                hit = verdict in labels["criteria"][criterion_id]
                accuracy_hits += hit
                accuracy_total += 1
                accuracy_by_criterion[criterion_id][0] += hit
                accuracy_by_criterion[criterion_id][1] += 1
                accuracy_by_provider[provider][0] += hit
                accuracy_by_provider[provider][1] += 1
            actual_failures = {str(item["id"]) for item in object_list(grade.get("critical_failures"), "critical_failures")}
            expected = set(labels["critical_failures"]["expected"])
            critical_tp += len(actual_failures & expected)
            critical_fp += len(actual_failures - expected)
            critical_fn += len(expected - actual_failures)
            for defect in object_list(grade.get("defects"), "grade.defects"):
                primary_total += 1
                primary_hits += defect.get("primary_criterion") in labels["primary_criteria"]

    intra_pairs: list[tuple[dict[str, object], dict[str, object]]] = []
    inter_pairs: list[tuple[dict[str, object], dict[str, object]]] = []
    for fixture_grades in grades.values():
        by_provider: dict[str, list[dict[str, object]]] = defaultdict(list)
        for grade in fixture_grades:
            by_provider[_provider(grade) or "unknown"].append(grade)
        for provider_grades in by_provider.values():
            intra_pairs.extend(combinations(provider_grades, 2))
        provider_names = sorted(by_provider)
        for left_provider, right_provider in combinations(provider_names, 2):
            inter_pairs.extend(product(by_provider[left_provider], by_provider[right_provider]))

    paired_hits = paired_total = invariant_hits = invariant_total = 0
    paired_by_provider: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for pair in pairs:
        labels = _resolved_pair_labels(manifest, pair["labels"])
        for comparison in comparisons[str(pair["id"])]:
            provider = _provider(comparison) or "unknown"
            actual = {str(item["id"]): str(item["direction"]) for item in object_list(comparison.get("criteria"), "comparison.criteria")}
            for criterion_id, allowed in labels["directions"].items():
                accepted = allowed if isinstance(allowed, list) else [allowed]
                hit = actual.get(criterion_id) in accepted
                paired_hits += hit
                paired_total += 1
                paired_by_provider[provider][0] += hit
                paired_by_provider[provider][1] += 1
            for criterion_id in labels["invariant_criteria"]:
                invariant_total += 1
                invariant_hits += actual.get(criterion_id) == "same"

    shadow: dict[str, list[float]] = defaultdict(list)
    for score in scores:
        axes = [
            {
                "id": component["id"],
                "weight": component["weight"],
                "criteria": [
                    {"id": criterion_id, "verdict": verdict}
                    for criterion_id, verdict in component["criterion_verdicts"].items()
                ],
            }
            for component in score.get("components", [])
        ]
        caps = [(str(item["id"]), int(item["cap"])) for item in score.get("applied_caps", [])]
        for strategy, result in score_strategies(axes, caps).items():
            shadow[strategy].append(float(result["effective_total"]))

    precision_denominator = critical_tp + critical_fp
    recall_denominator = critical_tp + critical_fn
    return {
        "versions": {
            "manifest_version": manifest["manifest_version"],
            "rubric_version": manifest["rubric_version"],
            "grade_schema_version": manifest["grade_schema_version"],
            "scoring_version": manifest["scoring_version"],
        },
        "accuracy": {
            "overall": _metric(accuracy_hits, accuracy_total),
            "by_criterion": {key: _metric(*value) for key, value in sorted(accuracy_by_criterion.items())},
            "by_provider": {key: _metric(*value) for key, value in sorted(accuracy_by_provider.items())},
        },
        "intra_grader": _agreement(intra_pairs),
        "inter_grader": _agreement(inter_pairs),
        "critical_failures": {
            "precision": _metric(critical_tp, precision_denominator),
            "recall": _metric(critical_tp, recall_denominator),
            "true_positive": critical_tp,
            "false_positive": critical_fp,
            "false_negative": critical_fn,
        },
        "primary_criterion": _metric(primary_hits, primary_total),
        "paired_direction": {
            "overall": _metric(paired_hits, paired_total),
            "by_provider": {key: _metric(*value) for key, value in sorted(paired_by_provider.items())},
        },
        "invariant_stability": _metric(invariant_hits, invariant_total),
        "scoring_shadow": {
            strategy: {
                "count": len(values),
                "minimum": min(values) if values else None,
                "maximum": max(values) if values else None,
                "spread": max(values) - min(values) if values else None,
            }
            for strategy, values in sorted(shadow.items())
        },
        "thresholds_enforced": False,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("artifacts", nargs="*", type=Path)
    args = parser.parse_args(argv)
    try:
        manifest = load_object(args.manifest)
        validate_manifest(manifest, args.manifest.parent)
        print(json.dumps(build_report(manifest, args.artifacts), indent=2))
        return 0
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
