#!/usr/bin/env python3
"""Validate v3 rubric, absolute-grade, and paired-grade contracts."""

from __future__ import annotations

from evaluator_versions import GRADE_SCHEMA_VERSION, RUBRIC_VERSION
from scoring import SCORING_STRATEGIES, SCORING_VERSION, VERDICT_SCORES, apply_caps, score_components


DEFECT_SEVERITIES = frozenset(VERDICT_SCORES) - {"pass"}
CONFIDENCE_LEVELS = frozenset({"low", "medium", "high"})
DIRECTIONS = frozenset({"better", "same", "worse"})
MATERIAL_VERDICTS = frozenset({"material", "severe", "absent"})


def object_list(value: object, label: str) -> list[dict[str, object]]:
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise ValueError(f"{label}: expected a list of objects")
    return value


def string_list(value: object, label: str, *, nonempty: bool = False) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        raise ValueError(f"{label}: expected a list of non-empty strings")
    if nonempty and not value:
        raise ValueError(f"{label}: expected at least one item")
    return value


def required_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label}: expected a non-empty string")
    return value


def rubric_versions(rubric: dict[str, object]) -> dict[str, object]:
    versions = {
        "rubric_version": rubric.get("rubric_version"),
        "grade_schema_version": rubric.get("grade_schema_version"),
        "scoring_version": rubric.get("scoring_version"),
        "scoring_strategy": rubric.get("scoring_strategy"),
    }
    expected = {
        "rubric_version": RUBRIC_VERSION,
        "grade_schema_version": GRADE_SCHEMA_VERSION,
        "scoring_version": SCORING_VERSION,
    }
    for key, value in expected.items():
        if versions[key] != value:
            raise ValueError(f"rubric.{key}: expected {value}")
    if versions["scoring_strategy"] not in SCORING_STRATEGIES:
        raise ValueError("rubric.scoring_strategy: unsupported strategy")
    return versions


def rubric_contract(
    rubric: dict[str, object],
) -> tuple[int, list[dict[str, object]], dict[str, tuple[str, str]], dict[str, int]]:
    versions = rubric_versions(rubric)
    if rubric.get("verdict_scores") != VERDICT_SCORES:
        raise ValueError("rubric.verdict_scores: must match the evaluator mapping")
    verdicts = rubric.get("verdicts")
    if not isinstance(verdicts, dict) or set(verdicts) != set(VERDICT_SCORES):
        raise ValueError("rubric.verdicts: every verdict requires an operational definition")
    for verdict, definition in verdicts.items():
        if not isinstance(definition, dict):
            raise ValueError(f"rubric.verdicts.{verdict}: expected an object")
        for field in ("definition", "conditions", "boundary_examples"):
            value = definition.get(field)
            if field == "definition":
                required_string(value, f"rubric.verdicts.{verdict}.{field}")
            else:
                string_list(value, f"rubric.verdicts.{verdict}.{field}", nonempty=True)

    axes = object_list(rubric.get("axes"), "rubric.axes")
    criteria: dict[str, tuple[str, str]] = {}
    weights: dict[str, int] = {}
    for axis in axes:
        axis_id = required_string(axis.get("id"), "rubric axis id")
        if axis_id in weights:
            raise ValueError(f"rubric.axes: duplicate id {axis_id}")
        weight = axis.get("weight")
        if not isinstance(weight, int) or isinstance(weight, bool) or weight <= 0:
            raise ValueError(f"rubric axis {axis_id}: weight must be a positive integer")
        weights[axis_id] = weight
        for criterion in object_list(axis.get("criteria"), f"rubric axis {axis_id}.criteria"):
            criterion_id = required_string(criterion.get("id"), f"rubric axis {axis_id} criterion id")
            if criterion_id in criteria:
                raise ValueError(f"rubric criteria: duplicate id {criterion_id}")
            criteria[criterion_id] = (
                axis_id,
                required_string(criterion.get("text"), f"rubric criterion {criterion_id}.text"),
            )
    if sum(weights.values()) != 100:
        raise ValueError("rubric.axes: weights must sum to 100")

    failure_caps: dict[str, int] = {}
    for failure in object_list(rubric.get("critical_failures"), "rubric.critical_failures"):
        failure_id = required_string(failure.get("id"), "rubric critical failure id")
        if failure_id in failure_caps:
            raise ValueError(f"rubric.critical_failures: duplicate id {failure_id}")
        cap = failure.get("score_cap")
        if not isinstance(cap, int) or isinstance(cap, bool) or not 0 <= cap <= 100:
            raise ValueError(f"rubric critical failure {failure_id}: invalid score_cap")
        for field in ("sufficient_conditions", "exclusions", "candidate_citations", "controlling_citations"):
            string_list(failure.get(field), f"rubric critical failure {failure_id}.{field}", nonempty=True)
        failure_caps[failure_id] = cap
    return int(versions["rubric_version"]), axes, criteria, failure_caps


def _evidence(value: dict[str, object], label: str, *, controlling_required: bool) -> None:
    string_list(value.get("candidate_evidence"), f"{label}.candidate_evidence", nonempty=True)
    string_list(
        value.get("controlling_evidence"),
        f"{label}.controlling_evidence",
        nonempty=controlling_required,
    )


def validate_absolute_grade(
    rubric: dict[str, object], grade: dict[str, object]
) -> tuple[list[dict[str, object]], list[tuple[str, int]]]:
    version, rubric_axes, criteria, failure_caps = rubric_contract(rubric)
    if grade.get("rubric_version") != version:
        raise ValueError(f"grade.rubric_version must equal {version}")
    if grade.get("grade_schema_version") != GRADE_SCHEMA_VERSION:
        raise ValueError(f"grade.grade_schema_version must equal {GRADE_SCHEMA_VERSION}")
    candidate = required_string(grade.get("candidate"), "grade.candidate")
    if not candidate.startswith("candidate-"):
        raise ValueError("grade.candidate must use a neutral candidate alias")

    defects: dict[str, dict[str, object]] = {}
    for defect in object_list(grade.get("defects"), "grade.defects"):
        defect_id = required_string(defect.get("id"), "grade defect id")
        if defect_id in defects:
            raise ValueError(f"grade.defects: duplicate id {defect_id}")
        primary = required_string(defect.get("primary_criterion"), f"grade defect {defect_id}.primary_criterion")
        if primary not in criteria:
            raise ValueError(f"grade defect {defect_id}: unknown primary criterion {primary}")
        severity = defect.get("severity")
        if severity not in DEFECT_SEVERITIES:
            raise ValueError(f"grade defect {defect_id}: unknown severity {severity}")
        if not isinstance(defect.get("element_absent"), bool):
            raise ValueError(f"grade defect {defect_id}.element_absent: expected a boolean")
        if (severity == "absent") != bool(defect["element_absent"]):
            raise ValueError(f"grade defect {defect_id}: absent is only valid for a totally missing element")
        required_string(defect.get("consequence"), f"grade defect {defect_id}.consequence")
        _evidence(defect, f"grade defect {defect_id}", controlling_required=True)
        defects[defect_id] = defect

    rubric_axis_ids = {str(axis["id"]) for axis in rubric_axes}
    seen_axes: set[str] = set()
    seen_criteria: dict[str, dict[str, object]] = {}
    references: dict[str, str] = {}
    ordered_axes: list[dict[str, object]] = []
    for axis in object_list(grade.get("axes"), "grade.axes"):
        axis_id = required_string(axis.get("id"), "grade axis id")
        if axis_id not in rubric_axis_ids or axis_id in seen_axes:
            raise ValueError(f"grade.axes: unknown or duplicate id {axis_id}")
        entries = object_list(axis.get("criteria"), f"grade axis {axis_id}.criteria")
        for entry in entries:
            criterion_id = required_string(entry.get("id"), f"grade axis {axis_id} criterion id")
            if criterion_id in seen_criteria or criteria.get(criterion_id, (None,))[0] != axis_id:
                raise ValueError(f"grade criterion: unknown or duplicate id {criterion_id}")
            verdict = entry.get("verdict")
            if verdict not in VERDICT_SCORES:
                raise ValueError(f"grade criterion {criterion_id}: unknown verdict {verdict}")
            _evidence(entry, f"grade criterion {criterion_id}", controlling_required=verdict != "pass")
            defect_ids = string_list(entry.get("defect_ids"), f"grade criterion {criterion_id}.defect_ids")
            if len(defect_ids) != len(set(defect_ids)):
                raise ValueError(f"grade criterion {criterion_id}: duplicate defect reference")
            if verdict == "pass" and defect_ids:
                raise ValueError(f"grade criterion {criterion_id}: pass cannot cite defects")
            if verdict != "pass" and not defect_ids:
                raise ValueError(f"grade criterion {criterion_id}: non-pass requires a defect")
            for defect_id in defect_ids:
                if defect_id not in defects:
                    raise ValueError(f"grade criterion {criterion_id}: dangling defect {defect_id}")
                if defects[defect_id]["primary_criterion"] != criterion_id:
                    raise ValueError(f"grade defect {defect_id}: may be charged only to its primary criterion")
                if defect_id in references:
                    raise ValueError(f"grade defect {defect_id}: charged more than once")
                references[defect_id] = criterion_id
            if defect_ids:
                worst = min(
                    (str(defects[defect_id]["severity"]) for defect_id in defect_ids),
                    key=lambda severity: VERDICT_SCORES[severity],
                )
                if verdict != worst:
                    raise ValueError(f"grade criterion {criterion_id}: verdict must equal worst defect severity")
            seen_criteria[criterion_id] = entry
        required_string(axis.get("rationale"), f"grade axis {axis_id}.rationale")
        if axis.get("confidence") not in CONFIDENCE_LEVELS:
            raise ValueError(f"grade axis {axis_id}.confidence: invalid level")
        seen_axes.add(axis_id)
        ordered_axes.append(axis)

    if seen_axes != rubric_axis_ids or set(seen_criteria) != set(criteria):
        raise ValueError("grade: missing or unknown axis/criterion ids")
    if set(references) != set(defects):
        raise ValueError(f"grade.defects: unreferenced defects {sorted(set(defects) - set(references))}")

    caps: list[tuple[str, int]] = []
    seen_failures: set[str] = set()
    for failure in object_list(grade.get("critical_failures"), "grade.critical_failures"):
        failure_id = required_string(failure.get("id"), "grade critical failure id")
        if failure_id not in failure_caps or failure_id in seen_failures:
            raise ValueError(f"grade.critical_failures: unknown or duplicate id {failure_id}")
        string_list(failure.get("conditions_met"), f"critical failure {failure_id}.conditions_met", nonempty=True)
        string_list(failure.get("exclusions_checked"), f"critical failure {failure_id}.exclusions_checked", nonempty=True)
        _evidence(failure, f"critical failure {failure_id}", controlling_required=True)
        seen_failures.add(failure_id)
        caps.append((failure_id, failure_caps[failure_id]))
    return ordered_axes, caps


def score_grade(rubric: dict[str, object], grade: dict[str, object]) -> dict[str, object]:
    grade_axes, caps = validate_absolute_grade(rubric, grade)
    _, rubric_axes, _, _ = rubric_contract(rubric)
    grade_by_id = {str(axis["id"]): axis for axis in grade_axes}
    scoring_axes = [
        {"id": axis["id"], "weight": axis["weight"], "criteria": grade_by_id[str(axis["id"])]["criteria"]}
        for axis in rubric_axes
    ]
    strategy = str(rubric["scoring_strategy"])
    components, raw_total = score_components(scoring_axes, strategy)
    effective_total, applied_caps = apply_caps(raw_total, caps)
    return {
        "rubric_version": rubric["rubric_version"],
        "grade_schema_version": rubric["grade_schema_version"],
        "scoring_version": rubric["scoring_version"],
        "scoring_strategy": strategy,
        "candidate": grade["candidate"],
        "components": components,
        "raw_total": raw_total,
        "effective_total": effective_total,
        "applied_caps": applied_caps,
    }


def _string_array_schema(*, minimum: int = 0) -> dict[str, object]:
    return {"type": "array", "items": {"type": "string", "minLength": 1}, "minItems": minimum}


def _evidence_properties(*, controlling_minimum: int = 0) -> dict[str, object]:
    return {
        "candidate_evidence": _string_array_schema(minimum=1),
        "controlling_evidence": _string_array_schema(minimum=controlling_minimum),
    }


def absolute_grade_schema(rubric: dict[str, object]) -> dict[str, object]:
    version, axes, criteria, failures = rubric_contract(rubric)
    criterion_schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "id": {"type": "string", "enum": list(criteria)},
            "verdict": {"type": "string", "enum": list(VERDICT_SCORES)},
            **_evidence_properties(),
            "defect_ids": _string_array_schema(),
        },
        "required": ["id", "verdict", "candidate_evidence", "controlling_evidence", "defect_ids"],
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "rubric_version": {"type": "integer", "const": version},
            "grade_schema_version": {"type": "integer", "const": GRADE_SCHEMA_VERSION},
            "candidate": {"type": "string", "pattern": "^candidate-[A-Z]$"},
            "axes": {
                "type": "array",
                "minItems": len(axes),
                "maxItems": len(axes),
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "id": {"type": "string", "enum": [axis["id"] for axis in axes]},
                        "criteria": {"type": "array", "items": criterion_schema},
                        "rationale": {"type": "string", "minLength": 1},
                        "confidence": {"type": "string", "enum": sorted(CONFIDENCE_LEVELS)},
                    },
                    "required": ["id", "criteria", "rationale", "confidence"],
                },
            },
            "defects": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "id": {"type": "string", "minLength": 1},
                        "primary_criterion": {"type": "string", "enum": list(criteria)},
                        "consequence": {"type": "string", "minLength": 1},
                        "severity": {"type": "string", "enum": sorted(DEFECT_SEVERITIES)},
                        "element_absent": {"type": "boolean"},
                        **_evidence_properties(controlling_minimum=1),
                    },
                    "required": ["id", "primary_criterion", "consequence", "severity", "element_absent", "candidate_evidence", "controlling_evidence"],
                },
            },
            "critical_failures": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "id": {"type": "string", "enum": list(failures)},
                        "conditions_met": _string_array_schema(minimum=1),
                        "exclusions_checked": _string_array_schema(minimum=1),
                        **_evidence_properties(controlling_minimum=1),
                    },
                    "required": ["id", "conditions_met", "exclusions_checked", "candidate_evidence", "controlling_evidence"],
                },
            },
        },
        "required": ["rubric_version", "grade_schema_version", "candidate", "axes", "defects", "critical_failures"],
    }


def comparison_schema(rubric: dict[str, object]) -> dict[str, object]:
    version, axes, criteria, failures = rubric_contract(rubric)
    evidence = {
        "before_evidence": _string_array_schema(minimum=1),
        "after_evidence": _string_array_schema(minimum=1),
        "controlling_evidence": _string_array_schema(minimum=1),
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "rubric_version": {"type": "integer", "const": version},
            "grade_schema_version": {"type": "integer", "const": GRADE_SCHEMA_VERSION},
            "before_candidate": {"type": "string", "const": "candidate-A"},
            "after_candidate": {"type": "string", "const": "candidate-B"},
            "criteria": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "id": {"type": "string", "enum": list(criteria)},
                        "direction": {"type": "string", "enum": sorted(DIRECTIONS)},
                        "consequence": {"type": "string", "minLength": 1},
                        **evidence,
                        "confidence": {"type": "string", "enum": sorted(CONFIDENCE_LEVELS)},
                    },
                    "required": ["id", "direction", "consequence", "before_evidence", "after_evidence", "controlling_evidence", "confidence"],
                },
            },
            "critical_failures": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "id": {"type": "string", "enum": list(failures)},
                        "before_present": {"type": "boolean"},
                        "after_present": {"type": "boolean"},
                        **evidence,
                    },
                    "required": ["id", "before_present", "after_present", "before_evidence", "after_evidence", "controlling_evidence"],
                },
            },
            "overall_direction": {"type": "string", "enum": sorted(DIRECTIONS)},
            "rationale": {"type": "string", "minLength": 1},
        },
        "required": ["rubric_version", "grade_schema_version", "before_candidate", "after_candidate", "criteria", "critical_failures", "overall_direction", "rationale"],
    }


def validate_comparison(rubric: dict[str, object], comparison: dict[str, object]) -> None:
    version, _, criteria, failures = rubric_contract(rubric)
    if comparison.get("rubric_version") != version or comparison.get("grade_schema_version") != GRADE_SCHEMA_VERSION:
        raise ValueError("comparison versions are incompatible")
    if comparison.get("before_candidate") != "candidate-A" or comparison.get("after_candidate") != "candidate-B":
        raise ValueError("comparison candidates must use neutral aliases")
    seen: set[str] = set()
    for entry in object_list(comparison.get("criteria"), "comparison.criteria"):
        criterion_id = required_string(entry.get("id"), "comparison criterion id")
        if criterion_id not in criteria or criterion_id in seen:
            raise ValueError(f"comparison criterion: unknown or duplicate id {criterion_id}")
        if entry.get("direction") not in DIRECTIONS or entry.get("confidence") not in CONFIDENCE_LEVELS:
            raise ValueError(f"comparison criterion {criterion_id}: invalid direction or confidence")
        required_string(entry.get("consequence"), f"comparison criterion {criterion_id}.consequence")
        for field in ("before_evidence", "after_evidence", "controlling_evidence"):
            string_list(entry.get(field), f"comparison criterion {criterion_id}.{field}", nonempty=True)
        seen.add(criterion_id)
    if seen != set(criteria):
        raise ValueError("comparison: missing criterion ids")
    seen_failures: set[str] = set()
    for failure in object_list(comparison.get("critical_failures"), "comparison.critical_failures"):
        failure_id = required_string(failure.get("id"), "comparison critical failure id")
        if failure_id not in failures or failure_id in seen_failures:
            raise ValueError(f"comparison critical failure: unknown or duplicate id {failure_id}")
        if not isinstance(failure.get("before_present"), bool) or not isinstance(failure.get("after_present"), bool):
            raise ValueError(f"comparison critical failure {failure_id}: invalid presence")
        for field in ("before_evidence", "after_evidence", "controlling_evidence"):
            string_list(failure.get(field), f"comparison critical failure {failure_id}.{field}", nonempty=True)
        seen_failures.add(failure_id)
    if comparison.get("overall_direction") not in DIRECTIONS:
        raise ValueError("comparison.overall_direction: invalid direction")
    required_string(comparison.get("rationale"), "comparison.rationale")
