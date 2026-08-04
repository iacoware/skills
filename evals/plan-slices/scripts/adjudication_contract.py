#!/usr/bin/env python3
"""Blind, hash-bound v3 adjudication contracts."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

from evaluator_versions import ADJUDICATION_VERSION
from grader_runtime import sha256_file
from grading_contract import MATERIAL_VERDICTS, VERDICT_SCORES, object_list, score_grade, validate_absolute_grade, validate_comparison


def criterion_entries(grade: dict[str, object]) -> dict[str, dict[str, object]]:
    return {
        str(entry["id"]): entry
        for axis in object_list(grade.get("axes"), "grade.axes")
        for entry in object_list(axis.get("criteria"), "grade axis.criteria")
    }


def material_grade_disagreements(grades: Sequence[dict[str, object]]) -> tuple[list[str], list[str]]:
    if len(grades) != 2:
        raise ValueError("absolute adjudication requires exactly two grades")
    entries = [criterion_entries(grade) for grade in grades]
    if set(entries[0]) != set(entries[1]):
        raise ValueError("grade criteria differ")
    criteria = [
        criterion_id
        for criterion_id in sorted(entries[0])
        if entries[0][criterion_id]["verdict"] != entries[1][criterion_id]["verdict"]
        and bool(
            {str(entries[0][criterion_id]["verdict"]), str(entries[1][criterion_id]["verdict"])}
            & MATERIAL_VERDICTS
        )
    ]
    failure_sets = [
        {str(failure["id"]) for failure in object_list(grade.get("critical_failures"), "critical_failures")}
        for grade in grades
    ]
    return criteria, sorted(failure_sets[0] ^ failure_sets[1])


def paired_disagreements(comparisons: Sequence[dict[str, object]]) -> tuple[list[str], list[str]]:
    if len(comparisons) != 2:
        raise ValueError("paired adjudication requires exactly two comparisons")
    entries = [
        {str(entry["id"]): entry for entry in object_list(comp.get("criteria"), "comparison.criteria")}
        for comp in comparisons
    ]
    criteria = [
        criterion_id
        for criterion_id in sorted(entries[0])
        if entries[0][criterion_id]["direction"] != entries[1][criterion_id]["direction"]
    ]
    states = []
    for comparison in comparisons:
        states.append(
            {
                str(failure["id"]): (failure["before_present"], failure["after_present"])
                for failure in object_list(comparison.get("critical_failures"), "critical_failures")
            }
        )
    failures = [failure_id for failure_id in sorted(set(states[0]) | set(states[1])) if states[0].get(failure_id) != states[1].get(failure_id)]
    return criteria, failures


def _aliased_input(entry: dict[str, object], alias: str, fields: Sequence[str]) -> dict[str, object]:
    return {"grader": alias, **{field: entry.get(field) for field in fields}}


def build_request(kind: str, paths: Sequence[Path], values: Sequence[dict[str, object]]) -> tuple[dict[str, object], dict[str, object]]:
    if kind == "absolute":
        criteria, failures = material_grade_disagreements(values)
        criterion_maps = [criterion_entries(value) for value in values]
        failure_maps = [
            {str(item["id"]): item for item in object_list(value.get("critical_failures"), "critical_failures")}
            for value in values
        ]
        request_criteria = [
            {
                "id": criterion_id,
                "inputs": [
                    _aliased_input(mapping[criterion_id], f"grader-{index}", ("verdict", "candidate_evidence", "controlling_evidence", "defect_ids"))
                    for index, mapping in enumerate(criterion_maps, start=1)
                ],
            }
            for criterion_id in criteria
        ]
    elif kind == "paired":
        criteria, failures = paired_disagreements(values)
        criterion_maps = [
            {str(item["id"]): item for item in object_list(value.get("criteria"), "comparison.criteria")}
            for value in values
        ]
        failure_maps = [
            {str(item["id"]): item for item in object_list(value.get("critical_failures"), "critical_failures")}
            for value in values
        ]
        request_criteria = [
            {
                "id": criterion_id,
                "inputs": [
                    _aliased_input(mapping[criterion_id], f"grader-{index}", ("direction", "consequence", "before_evidence", "after_evidence", "controlling_evidence"))
                    for index, mapping in enumerate(criterion_maps, start=1)
                ],
            }
            for criterion_id in criteria
        ]
    else:
        raise ValueError(f"unknown adjudication type: {kind}")
    request_failures = [
        {
            "id": failure_id,
            "inputs": [
                _aliased_input(mapping.get(failure_id, {"present": False}), f"grader-{index}", tuple(mapping.get(failure_id, {"present": False}).keys()))
                for index, mapping in enumerate(failure_maps, start=1)
            ],
        }
        for failure_id in failures
    ]
    input_hashes = [sha256_file(path) for path in paths]
    request = {
        "adjudication_version": ADJUDICATION_VERSION,
        "type": kind,
        "status": "pending-review" if criteria or failures else "automatic",
        "input_sha256": input_hashes,
        "discordant_criteria": request_criteria,
        "discordant_critical_failures": request_failures,
    }
    metadata = {
        "adjudication_version": ADJUDICATION_VERSION,
        "type": kind,
        "inputs": [
            {
                "path": str(path),
                "sha256": digest,
                "grader": value.get("grader"),
            }
            for path, digest, value in zip(paths, input_hashes, values, strict=True)
        ],
    }
    return request, metadata


def validate_resolution(request: dict[str, object], resolution: dict[str, object]) -> None:
    if resolution.get("adjudication_version") != ADJUDICATION_VERSION:
        raise ValueError("resolution adjudication version mismatch")
    if resolution.get("type") != request.get("type"):
        raise ValueError("resolution type mismatch")
    if resolution.get("input_sha256") != request.get("input_sha256"):
        raise ValueError("resolution input hashes are stale")
    expected_criteria = {str(item["id"]) for item in object_list(request.get("discordant_criteria"), "request.discordant_criteria")}
    actual_criteria = {str(item["id"]) for item in object_list(resolution.get("criteria"), "resolution.criteria")}
    if actual_criteria != expected_criteria:
        raise ValueError("resolution may modify only materially discordant criteria")
    expected_failures = {str(item["id"]) for item in object_list(request.get("discordant_critical_failures"), "request.discordant_critical_failures")}
    actual_failures = {str(item["id"]) for item in object_list(resolution.get("critical_failures"), "resolution.critical_failures")}
    if actual_failures != expected_failures:
        raise ValueError("resolution may modify only discordant critical failures")
    if not isinstance(resolution.get("rationale"), str) or not resolution["rationale"]:
        raise ValueError("resolution requires a rationale")


def _merge_evidence(entries: Sequence[dict[str, object]], field: str) -> list[str]:
    return [
        f"grader-{index}: {item}"
        for index, entry in enumerate(entries, start=1)
        for item in entry.get(field, [])
        if isinstance(item, str)
    ]


def resolve_absolute(
    rubric: dict[str, object],
    grades: Sequence[dict[str, object]],
    request: dict[str, object],
    resolution: dict[str, object] | None,
) -> tuple[dict[str, object], dict[str, object]]:
    for grade in grades:
        validate_absolute_grade(rubric, grade)
    material_criteria, material_failures = material_grade_disagreements(grades)
    if (material_criteria or material_failures) and resolution is None:
        raise ValueError("pending-review")
    resolution = resolution or {
        "adjudication_version": ADJUDICATION_VERSION,
        "type": "absolute",
        "input_sha256": request["input_sha256"],
        "criteria": [],
        "critical_failures": [],
        "rationale": "No material disagreement; merged deterministically.",
    }
    validate_resolution(request, resolution)
    resolved_criteria = {str(item["id"]): item for item in object_list(resolution.get("criteria"), "resolution.criteria")}
    resolved_failures = {str(item["id"]): item for item in object_list(resolution.get("critical_failures"), "resolution.critical_failures")}
    grade_entries = [criterion_entries(grade) for grade in grades]
    defects_by_grade = [
        {str(item["id"]): item for item in object_list(grade.get("defects"), "grade.defects")}
        for grade in grades
    ]
    final_defects: list[dict[str, object]] = []
    final_entries: dict[str, dict[str, object]] = {}
    for criterion_id in grade_entries[0]:
        competing = [entries[criterion_id] for entries in grade_entries]
        if criterion_id in resolved_criteria:
            choice = resolved_criteria[criterion_id]
            verdict = choice.get("verdict")
            defects = object_list(choice.get("defects"), f"resolution criterion {criterion_id}.defects")
            if any(defect.get("primary_criterion") != criterion_id for defect in defects):
                raise ValueError(f"resolution criterion {criterion_id}: defect has wrong primary criterion")
            candidate_evidence = choice.get("candidate_evidence")
            controlling_evidence = choice.get("controlling_evidence")
        else:
            selected_index = min(
                range(len(competing)),
                key=lambda index: VERDICT_SCORES[str(competing[index]["verdict"])],
            )
            selected = competing[selected_index]
            verdict = selected["verdict"]
            defects = []
            for defect_id in selected["defect_ids"]:
                defect = dict(defects_by_grade[selected_index][str(defect_id)])
                defect["id"] = f"grader-{selected_index + 1}:{defect_id}"
                defects.append(defect)
            candidate_evidence = _merge_evidence(competing, "candidate_evidence")
            controlling_evidence = _merge_evidence(competing, "controlling_evidence")
        final_defects.extend(defects)
        final_entries[criterion_id] = {
            "id": criterion_id,
            "verdict": verdict,
            "candidate_evidence": candidate_evidence,
            "controlling_evidence": controlling_evidence,
            "defect_ids": [defect["id"] for defect in defects],
        }
    failure_maps = [
        {str(item["id"]): item for item in object_list(grade.get("critical_failures"), "critical_failures")}
        for grade in grades
    ]
    all_failure_ids = sorted(set(failure_maps[0]) | set(failure_maps[1]))
    final_failures: list[dict[str, object]] = []
    for failure_id in all_failure_ids:
        if failure_id in resolved_failures:
            if resolved_failures[failure_id].get("present"):
                final_failures.append(dict(resolved_failures[failure_id]["failure"]))
        elif failure_id in failure_maps[0] and failure_id in failure_maps[1]:
            entries = [failure_maps[0][failure_id], failure_maps[1][failure_id]]
            final_failures.append(
                {
                    **entries[0],
                    "candidate_evidence": _merge_evidence(entries, "candidate_evidence"),
                    "controlling_evidence": _merge_evidence(entries, "controlling_evidence"),
                }
            )
    final_axes = []
    for axis in grades[0]["axes"]:
        final_axes.append(
            {
                "id": axis["id"],
                "criteria": [final_entries[str(entry["id"])] for entry in axis["criteria"]],
                "rationale": "Resolved from two aliased graders.",
                "confidence": "high" if not material_criteria else "medium",
            }
        )
    grade = {
        "rubric_version": rubric["rubric_version"],
        "grade_schema_version": rubric["grade_schema_version"],
        "candidate": grades[0]["candidate"],
        "axes": final_axes,
        "defects": final_defects,
        "critical_failures": final_failures,
        "adjudication": {"input_sha256": request["input_sha256"], "rationale": resolution["rationale"]},
    }
    validate_absolute_grade(rubric, grade)
    return grade, score_grade(rubric, grade)


def resolve_paired(
    rubric: dict[str, object],
    comparisons: Sequence[dict[str, object]],
    request: dict[str, object],
    resolution: dict[str, object] | None,
) -> dict[str, object]:
    for comparison in comparisons:
        validate_comparison(rubric, comparison)
    criteria, failures = paired_disagreements(comparisons)
    if (criteria or failures) and resolution is None:
        raise ValueError("pending-review")
    resolution = resolution or {
        "adjudication_version": ADJUDICATION_VERSION,
        "type": "paired",
        "input_sha256": request["input_sha256"],
        "criteria": [],
        "critical_failures": [],
        "rationale": "No disagreement; merged deterministically.",
    }
    validate_resolution(request, resolution)
    resolved = {str(item["id"]): item for item in object_list(resolution.get("criteria"), "resolution.criteria")}
    maps = [{str(item["id"]): item for item in object_list(comp.get("criteria"), "criteria")} for comp in comparisons]
    final_criteria = []
    for criterion_id, first in maps[0].items():
        if criterion_id in resolved:
            final_criteria.append(dict(resolved[criterion_id]))
        else:
            entries = [first, maps[1][criterion_id]]
            final_criteria.append(
                {
                    **first,
                    "before_evidence": _merge_evidence(entries, "before_evidence"),
                    "after_evidence": _merge_evidence(entries, "after_evidence"),
                    "controlling_evidence": _merge_evidence(entries, "controlling_evidence"),
                }
            )
    directions = [str(item["direction"]) for item in final_criteria]
    overall = "same" if all(item == "same" for item in directions) else (
        "better" if directions.count("better") >= directions.count("worse") else "worse"
    )
    result = {
        "rubric_version": rubric["rubric_version"],
        "grade_schema_version": rubric["grade_schema_version"],
        "before_candidate": "candidate-A",
        "after_candidate": "candidate-B",
        "criteria": final_criteria,
        "critical_failures": [],
        "overall_direction": overall,
        "rationale": resolution["rationale"],
    }
    validate_comparison(rubric, result)
    return result
