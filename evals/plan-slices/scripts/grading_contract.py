#!/usr/bin/env python3
"""Validate evaluator contracts and derive deterministic scores."""

from __future__ import annotations

VERDICT_SCORES = {"pass": 4, "minor": 3, "material": 2, "severe": 1, "absent": 0}
DEFECT_SEVERITIES = frozenset(VERDICT_SCORES) - {"pass"}
CONFIDENCE_LEVELS = frozenset({"low", "medium", "high"})
DIRECTIONS = frozenset({"better", "same", "worse"})


def object_list(value: object, label: str) -> list[dict[str, object]]:
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise ValueError(f"{label}: expected a list of objects")
    return value


def string_list(value: object, label: str, *, nonempty: bool = False) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise ValueError(f"{label}: expected a list of non-empty strings")
    if nonempty and not value:
        raise ValueError(f"{label}: expected at least one item")
    return value


def required_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label}: expected a non-empty string")
    return value


def rubric_contract(
    rubric: dict[str, object],
) -> tuple[int, list[dict[str, object]], dict[str, tuple[str, str]], dict[str, int]]:
    version = rubric.get("version")
    if not isinstance(version, int):
        raise ValueError("rubric.version: expected an integer")
    if rubric.get("verdict_scores") != VERDICT_SCORES:
        raise ValueError("rubric.verdict_scores: must match the evaluator verdict mapping")

    axes = object_list(rubric.get("axes"), "rubric.axes")
    axis_ids: set[str] = set()
    criteria: dict[str, tuple[str, str]] = {}
    weights: dict[str, int] = {}
    for axis in axes:
        axis_id = required_string(axis.get("id"), "rubric axis id")
        if axis_id in axis_ids:
            raise ValueError(f"rubric.axes: duplicate id {axis_id}")
        axis_ids.add(axis_id)
        weight = axis.get("weight")
        if not isinstance(weight, int) or isinstance(weight, bool) or weight <= 0:
            raise ValueError(f"rubric axis {axis_id}: weight must be a positive integer")
        weights[axis_id] = weight
        for criterion in object_list(axis.get("criteria"), f"rubric axis {axis_id}.criteria"):
            criterion_id = required_string(
                criterion.get("id"), f"rubric axis {axis_id} criterion id"
            )
            if criterion_id in criteria:
                raise ValueError(f"rubric criteria: duplicate id {criterion_id}")
            criteria[criterion_id] = (
                axis_id,
                required_string(
                    criterion.get("text"), f"rubric criterion {criterion_id}.text"
                ),
            )
    if sum(weights.values()) != 100:
        raise ValueError("rubric.axes: weights must sum to 100")

    failure_caps: dict[str, int] = {}
    for failure in object_list(rubric.get("critical_failures"), "rubric.critical_failures"):
        failure_id = required_string(failure.get("id"), "rubric critical failure id")
        cap = failure.get("score_cap")
        if failure_id in failure_caps:
            raise ValueError(f"rubric.critical_failures: duplicate id {failure_id}")
        if not isinstance(cap, int) or isinstance(cap, bool) or not 0 <= cap <= 100:
            raise ValueError(f"rubric critical failure {failure_id}: invalid score_cap")
        failure_caps[failure_id] = cap
    return version, axes, criteria, failure_caps


def _validate_defects(
    grade: dict[str, object], criteria: dict[str, tuple[str, str]], axis_ids: set[str]
) -> dict[str, dict[str, object]]:
    defects: dict[str, dict[str, object]] = {}
    for defect in object_list(grade.get("defects"), "grade.defects"):
        defect_id = required_string(defect.get("id"), "grade defect id")
        primary_axis = required_string(
            defect.get("primary_axis"), f"grade defect {defect_id}.primary_axis"
        )
        severity = defect.get("severity")
        criterion_ids = string_list(
            defect.get("criterion_ids"), f"grade defect {defect_id}.criterion_ids", nonempty=True
        )
        if defect_id in defects:
            raise ValueError(f"grade.defects: duplicate id {defect_id}")
        if primary_axis not in axis_ids:
            raise ValueError(f"grade defect {defect_id}: unknown primary axis {primary_axis}")
        if severity not in DEFECT_SEVERITIES:
            raise ValueError(f"grade defect {defect_id}: unknown severity {severity}")
        unknown = sorted(set(criterion_ids) - set(criteria))
        if unknown:
            raise ValueError(f"grade defect {defect_id}: unknown criteria {unknown}")
        if not any(criteria[criterion_id][0] == primary_axis for criterion_id in criterion_ids):
            raise ValueError(
                f"grade defect {defect_id}: no criterion belongs to primary axis {primary_axis}"
            )
        string_list(defect.get("evidence"), f"grade defect {defect_id}.evidence", nonempty=True)
        defects[defect_id] = defect
    return defects


def validate_absolute_grade(
    rubric: dict[str, object], grade: dict[str, object]
) -> tuple[list[dict[str, object]], dict[str, int], list[int]]:
    version, rubric_axes, criteria, failure_caps = rubric_contract(rubric)
    if grade.get("rubric_version") != version:
        raise ValueError(f"grade.rubric_version must equal {version}")
    required_string(grade.get("candidate"), "grade.candidate")

    axis_ids = {str(axis["id"]) for axis in rubric_axes}
    defects = _validate_defects(grade, criteria, axis_ids)
    grade_axes = object_list(grade.get("axes"), "grade.axes")
    axes_by_id: dict[str, dict[str, object]] = {}
    criterion_entries: dict[str, dict[str, object]] = {}
    referenced_defects: set[str] = set()
    for axis in grade_axes:
        axis_id = required_string(axis.get("id"), "grade axis id")
        if axis_id in axes_by_id:
            raise ValueError(f"grade.axes: duplicate id {axis_id}")
        if axis_id not in axis_ids:
            raise ValueError(f"grade.axes: unknown id {axis_id}")
        entries = object_list(axis.get("criteria"), f"grade axis {axis_id}.criteria")
        for entry in entries:
            criterion_id = required_string(entry.get("id"), f"grade axis {axis_id} criterion id")
            if criterion_id in criterion_entries:
                raise ValueError(f"grade criteria: duplicate id {criterion_id}")
            if criterion_id not in criteria or criteria[criterion_id][0] != axis_id:
                raise ValueError(f"grade axis {axis_id}: unknown criterion {criterion_id}")
            verdict = entry.get("verdict")
            if verdict not in VERDICT_SCORES:
                raise ValueError(f"grade criterion {criterion_id}: unknown verdict {verdict}")
            string_list(entry.get("evidence"), f"grade criterion {criterion_id}.evidence", nonempty=True)
            defect_ids = string_list(entry.get("defect_ids"), f"grade criterion {criterion_id}.defect_ids")
            unknown_defects = sorted(set(defect_ids) - set(defects))
            if unknown_defects:
                raise ValueError(
                    f"grade criterion {criterion_id}: dangling defect references {unknown_defects}"
                )
            if verdict == "pass" and defect_ids:
                raise ValueError(f"grade criterion {criterion_id}: pass cannot cite defects")
            if verdict != "pass" and not defect_ids:
                raise ValueError(f"grade criterion {criterion_id}: non-pass verdict requires a defect")
            for defect_id in defect_ids:
                defect = defects[defect_id]
                if criterion_id not in defect["criterion_ids"]:
                    raise ValueError(
                        f"grade criterion {criterion_id}: defect {defect_id} omits the criterion"
                    )
                if defect["primary_axis"] != axis_id and VERDICT_SCORES[str(verdict)] > 2:
                    raise ValueError(
                        f"grade criterion {criterion_id}: secondary defect effect must be material or worse"
                    )
            referenced_defects.update(defect_ids)
            criterion_entries[criterion_id] = entry

        material_passes = string_list(
            axis.get("material_passes"), f"grade axis {axis_id}.material_passes"
        )
        for criterion_id in material_passes:
            entry = criterion_entries.get(criterion_id)
            if entry is None or criteria.get(criterion_id, (None,))[0] != axis_id:
                raise ValueError(f"grade axis {axis_id}: unknown material pass {criterion_id}")
            if entry.get("verdict") != "pass":
                raise ValueError(f"grade axis {axis_id}: material pass {criterion_id} did not pass")
        axis_defects = string_list(
            axis.get("defects_regressions"), f"grade axis {axis_id}.defects_regressions"
        )
        expected_axis_defects = {
            defect_id
            for defect_id, defect in defects.items()
            if any(criteria[criterion_id][0] == axis_id for criterion_id in defect["criterion_ids"])
        }
        if set(axis_defects) != expected_axis_defects:
            raise ValueError(
                f"grade axis {axis_id}.defects_regressions mismatch: "
                f"expected={sorted(expected_axis_defects)} actual={sorted(set(axis_defects))}"
            )
        required_string(axis.get("net_rationale"), f"grade axis {axis_id}.net_rationale")
        if axis.get("confidence") not in CONFIDENCE_LEVELS:
            raise ValueError(f"grade axis {axis_id}.confidence: invalid level")
        axes_by_id[axis_id] = axis

    if set(axes_by_id) != axis_ids:
        raise ValueError(
            f"grade.axes mismatch: missing={sorted(axis_ids - set(axes_by_id))}, "
            f"unknown={sorted(set(axes_by_id) - axis_ids)}"
        )
    if set(criterion_entries) != set(criteria):
        raise ValueError(
            f"grade.criteria mismatch: missing={sorted(set(criteria) - set(criterion_entries))}, "
            f"unknown={sorted(set(criterion_entries) - set(criteria))}"
        )
    if referenced_defects != set(defects):
        raise ValueError(f"grade.defects: unreferenced defects {sorted(set(defects) - referenced_defects)}")
    for defect_id, defect in defects.items():
        cited = [criterion_entries[criterion_id] for criterion_id in defect["criterion_ids"]]
        worst_score = min(VERDICT_SCORES[str(entry["verdict"])] for entry in cited)
        severity_score = VERDICT_SCORES[str(defect["severity"])]
        if severity_score != worst_score:
            raise ValueError(f"grade defect {defect_id}: severity must match its worst criterion verdict")
        if not any(
            criteria[str(entry["id"])][0] == defect["primary_axis"]
            and VERDICT_SCORES[str(entry["verdict"])] == worst_score
            for entry in cited
        ):
            raise ValueError(f"grade defect {defect_id}: worst effect must belong to its primary axis")

    scores: dict[str, int] = {}
    ordered_axes: list[dict[str, object]] = []
    for rubric_axis in rubric_axes:
        axis_id = str(rubric_axis["id"])
        verdicts = [
            str(criterion_entries[criterion_id]["verdict"])
            for criterion_id, (criterion_axis, _) in criteria.items()
            if criterion_axis == axis_id
        ]
        scores[axis_id] = min(VERDICT_SCORES[verdict] for verdict in verdicts)
        ordered_axes.append(axes_by_id[axis_id])

    caps: list[int] = []
    seen_failures: set[str] = set()
    for failure in object_list(grade.get("critical_failures"), "grade.critical_failures"):
        failure_id = required_string(failure.get("id"), "grade critical failure id")
        if failure_id not in failure_caps:
            raise ValueError(f"grade.critical_failures: unknown id {failure_id}")
        if failure_id in seen_failures:
            raise ValueError(f"grade.critical_failures: duplicate id {failure_id}")
        string_list(failure.get("evidence"), f"critical failure {failure_id}.evidence", nonempty=True)
        seen_failures.add(failure_id)
        caps.append(failure_caps[failure_id])
    return ordered_axes, scores, caps


def score_grade(rubric: dict[str, object], grade: dict[str, object]) -> dict[str, object]:
    axes, scores, caps = validate_absolute_grade(rubric, grade)
    version, rubric_axes, _, _ = rubric_contract(rubric)
    scored_axes: list[dict[str, object]] = []
    raw_total = 0.0
    for rubric_axis in rubric_axes:
        axis_id = str(rubric_axis["id"])
        weight = int(rubric_axis["weight"])
        score = scores[axis_id]
        weighted_score = score / 4 * weight
        raw_total += weighted_score
        scored_axes.append(
            {
                "id": axis_id,
                "score": score,
                "weight": weight,
                "weighted_score": round(weighted_score, 2),
                "criterion_verdicts": {
                    str(entry["id"]): entry["verdict"] for entry in axes[len(scored_axes)]["criteria"]
                },
            }
        )
    rounded_total = round(raw_total, 2)
    return {
        "rubric_version": version,
        "candidate": grade["candidate"],
        "axes": scored_axes,
        "raw_total": rounded_total,
        "effective_total": min([rounded_total, *caps]),
        "applied_caps": sorted(caps),
        "critical_failure_ids": sorted(
            str(failure["id"])
            for failure in object_list(grade.get("critical_failures"), "grade.critical_failures")
        ),
    }


def _string_array_schema(*, min_items: int = 0) -> dict[str, object]:
    return {"type": "array", "items": {"type": "string"}, "minItems": min_items}


def absolute_grade_schema(rubric: dict[str, object]) -> dict[str, object]:
    version, axes, criteria, failures = rubric_contract(rubric)
    axis_schemas = []
    for axis in axes:
        axis_id = str(axis["id"])
        criterion_ids = [criterion_id for criterion_id, (owner, _) in criteria.items() if owner == axis_id]
        axis_schemas.append(
            {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "id": {"type": "string", "const": axis_id},
                    "criteria": {
                        "type": "array",
                        "minItems": len(criterion_ids),
                        "maxItems": len(criterion_ids),
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "id": {"type": "string", "enum": criterion_ids},
                                "verdict": {"type": "string", "enum": list(VERDICT_SCORES)},
                                "evidence": _string_array_schema(min_items=1),
                                "defect_ids": _string_array_schema(),
                            },
                            "required": ["id", "verdict", "evidence", "defect_ids"],
                        },
                    },
                    "material_passes": _string_array_schema(),
                    "defects_regressions": _string_array_schema(),
                    "net_rationale": {"type": "string", "minLength": 1},
                    "confidence": {"type": "string", "enum": sorted(CONFIDENCE_LEVELS)},
                },
                "required": [
                    "id", "criteria", "material_passes", "defects_regressions",
                    "net_rationale", "confidence",
                ],
            }
        )
    defect_schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "id": {"type": "string", "minLength": 1},
            "primary_axis": {"type": "string", "enum": [axis["id"] for axis in axes]},
            "severity": {"type": "string", "enum": sorted(DEFECT_SEVERITIES)},
            "criterion_ids": _string_array_schema(min_items=1),
            "evidence": _string_array_schema(min_items=1),
        },
        "required": ["id", "primary_axis", "severity", "criterion_ids", "evidence"],
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "rubric_version": {"type": "integer", "const": version},
            "candidate": {"type": "string"},
            "axes": {"type": "array", "minItems": len(axes), "maxItems": len(axes), "items": {"anyOf": axis_schemas}},
            "defects": {"type": "array", "items": defect_schema},
            "critical_failures": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {"id": {"type": "string", "enum": list(failures)}, "evidence": _string_array_schema(min_items=1)},
                    "required": ["id", "evidence"],
                },
            },
        },
        "required": ["rubric_version", "candidate", "axes", "defects", "critical_failures"],
    }


def comparison_schema(rubric: dict[str, object]) -> dict[str, object]:
    version, axes, criteria, failures = rubric_contract(rubric)
    criterion_schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "id": {"type": "string", "enum": list(criteria)},
            "direction": {"type": "string", "enum": sorted(DIRECTIONS)},
            "resolved_defects": _string_array_schema(),
            "introduced_defects": _string_array_schema(),
            "preserved_passes": _string_array_schema(),
            "before_evidence": _string_array_schema(min_items=1),
            "after_evidence": _string_array_schema(min_items=1),
            "confidence": {"type": "string", "enum": sorted(CONFIDENCE_LEVELS)},
        },
        "required": [
            "id", "direction", "resolved_defects", "introduced_defects", "preserved_passes",
            "before_evidence", "after_evidence", "confidence",
        ],
    }
    axis_schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "id": {"type": "string", "enum": [axis["id"] for axis in axes]},
            "criteria": {"type": "array", "items": criterion_schema},
            "net_direction": {"type": "string", "enum": sorted(DIRECTIONS)},
            "confidence": {"type": "string", "enum": sorted(CONFIDENCE_LEVELS)},
        },
        "required": ["id", "criteria", "net_direction", "confidence"],
    }
    failure_schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "id": {"type": "string", "enum": list(failures)},
            "before_present": {"type": "boolean"},
            "after_present": {"type": "boolean"},
            "evidence": _string_array_schema(min_items=1),
        },
        "required": ["id", "before_present", "after_present", "evidence"],
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "rubric_version": {"type": "integer", "const": version},
            "before_candidate": {"type": "string"},
            "after_candidate": {"type": "string"},
            "axes": {"type": "array", "minItems": len(axes), "maxItems": len(axes), "items": axis_schema},
            "critical_failures": {"type": "array", "items": failure_schema},
            "overall_direction": {"type": "string", "enum": sorted(DIRECTIONS)},
            "net_rationale": {"type": "string", "minLength": 1},
        },
        "required": [
            "rubric_version", "before_candidate", "after_candidate", "axes",
            "critical_failures", "overall_direction", "net_rationale",
        ],
    }


def validate_comparison(rubric: dict[str, object], comparison: dict[str, object]) -> None:
    version, rubric_axes, criteria, failures = rubric_contract(rubric)
    if comparison.get("rubric_version") != version:
        raise ValueError(f"comparison.rubric_version must equal {version}")
    required_string(comparison.get("before_candidate"), "comparison.before_candidate")
    required_string(comparison.get("after_candidate"), "comparison.after_candidate")
    required_string(comparison.get("net_rationale"), "comparison.net_rationale")
    if comparison.get("overall_direction") not in DIRECTIONS:
        raise ValueError("comparison.overall_direction: invalid direction")

    expected_axes = {str(axis["id"]) for axis in rubric_axes}
    seen_axes: set[str] = set()
    seen_criteria: set[str] = set()
    for axis in object_list(comparison.get("axes"), "comparison.axes"):
        axis_id = required_string(axis.get("id"), "comparison axis id")
        if axis_id not in expected_axes or axis_id in seen_axes:
            raise ValueError(f"comparison.axes: unknown or duplicate id {axis_id}")
        if axis.get("net_direction") not in DIRECTIONS:
            raise ValueError(f"comparison axis {axis_id}: invalid net_direction")
        if axis.get("confidence") not in CONFIDENCE_LEVELS:
            raise ValueError(f"comparison axis {axis_id}: invalid confidence")
        for entry in object_list(axis.get("criteria"), f"comparison axis {axis_id}.criteria"):
            criterion_id = required_string(entry.get("id"), f"comparison axis {axis_id} criterion id")
            if criterion_id in seen_criteria or criteria.get(criterion_id, (None,))[0] != axis_id:
                raise ValueError(f"comparison axis {axis_id}: unknown or duplicate criterion {criterion_id}")
            if entry.get("direction") not in DIRECTIONS:
                raise ValueError(f"comparison criterion {criterion_id}: invalid direction")
            for field in ("resolved_defects", "introduced_defects", "preserved_passes"):
                string_list(entry.get(field), f"comparison criterion {criterion_id}.{field}")
            for field in ("before_evidence", "after_evidence"):
                string_list(entry.get(field), f"comparison criterion {criterion_id}.{field}", nonempty=True)
            if entry.get("confidence") not in CONFIDENCE_LEVELS:
                raise ValueError(f"comparison criterion {criterion_id}: invalid confidence")
            seen_criteria.add(criterion_id)
        seen_axes.add(axis_id)
    if seen_axes != expected_axes or seen_criteria != set(criteria):
        raise ValueError("comparison: missing or unknown axis/criterion ids")

    seen_failures: set[str] = set()
    for failure in object_list(comparison.get("critical_failures"), "comparison.critical_failures"):
        failure_id = required_string(failure.get("id"), "comparison critical failure id")
        if failure_id not in failures or failure_id in seen_failures:
            raise ValueError(f"comparison.critical_failures: unknown or duplicate id {failure_id}")
        if not isinstance(failure.get("before_present"), bool) or not isinstance(failure.get("after_present"), bool):
            raise ValueError(f"comparison critical failure {failure_id}: presence flags must be booleans")
        string_list(failure.get("evidence"), f"comparison critical failure {failure_id}.evidence", nonempty=True)
        seen_failures.add(failure_id)


def adjudication_reasons(
    comparisons: list[dict[str, object]],
    score_pairs: list[tuple[dict[str, object], dict[str, object]]],
) -> list[str]:
    reasons: list[str] = []
    comparison_failure_states: list[dict[str, tuple[bool, bool]]] = []
    for comparison in comparisons:
        states: dict[str, tuple[bool, bool]] = {}
        for failure in object_list(
            comparison.get("critical_failures"), "comparison.critical_failures"
        ):
            states[str(failure["id"])] = (
                bool(failure["before_present"]),
                bool(failure["after_present"]),
            )
        comparison_failure_states.append(states)
        for axis in object_list(comparison.get("axes"), "comparison.axes"):
            for criterion in object_list(
                axis.get("criteria"), f"comparison axis {axis.get('id')}.criteria"
            ):
                material = bool(
                    criterion.get("resolved_defects") or criterion.get("introduced_defects")
                )
                if material and criterion.get("confidence") == "low":
                    reasons.append(f"low confidence on material verdict: {criterion['id']}")
    failure_ids = set().union(*(states.keys() for states in comparison_failure_states))
    for failure_id in sorted(failure_ids):
        observed = {
            states.get(failure_id, (False, False)) for states in comparison_failure_states
        }
        if len(observed) > 1:
            reasons.append(f"critical-failure disagreement: {failure_id}")

    for pair_number, (left_score, right_score) in enumerate(score_pairs, start=1):
        left_axes = {
            str(axis["id"]): int(axis["score"])
            for axis in object_list(left_score.get("axes"), "left_score.axes")
        }
        right_axes = {
            str(axis["id"]): int(axis["score"])
            for axis in object_list(right_score.get("axes"), "right_score.axes")
        }
        for axis_id in sorted(set(left_axes) & set(right_axes)):
            if abs(left_axes[axis_id] - right_axes[axis_id]) >= 2:
                reasons.append(f"score pair {pair_number} axis score difference >= 2: {axis_id}")
        left_total = left_score.get("effective_total")
        right_total = right_score.get("effective_total")
        if isinstance(left_total, (int, float)) and isinstance(right_total, (int, float)):
            if abs(left_total - right_total) > 5:
                reasons.append(f"score pair {pair_number} total-score difference > 5")
    return reasons
