from __future__ import annotations

import json
from pathlib import Path

from scoring import VERDICT_SCORES


RUBRIC_PATH = Path(__file__).resolve().parent.parent / "grader-rubric.v3.json"
RUBRIC = json.loads(RUBRIC_PATH.read_text(encoding="utf-8"))


def passing_grade(candidate: str = "candidate-A") -> dict[str, object]:
    return {
        "rubric_version": 3,
        "grade_schema_version": 3,
        "candidate": candidate,
        "axes": [
            {
                "id": axis["id"],
                "criteria": [
                    {
                        "id": criterion["id"],
                        "verdict": "pass",
                        "candidate_evidence": [f"Candidate: {criterion['id']}"],
                        "controlling_evidence": [],
                        "defect_ids": [],
                    }
                    for criterion in axis["criteria"]
                ],
                "rationale": "All criteria pass.",
                "confidence": "high",
            }
            for axis in RUBRIC["axes"]
        ],
        "defects": [],
        "critical_failures": [],
    }


def criterion_entry(grade: dict[str, object], criterion_id: str) -> dict[str, object]:
    for axis in grade["axes"]:
        for entry in axis["criteria"]:
            if entry["id"] == criterion_id:
                return entry
    raise AssertionError(f"unknown criterion: {criterion_id}")


def declare_defect(
    grade: dict[str, object],
    defect_id: str,
    primary_criterion: str,
    severity: str,
    consequence: str = "The delivery decision is invalid.",
) -> dict[str, object]:
    defect = {
        "id": defect_id,
        "primary_criterion": primary_criterion,
        "consequence": consequence,
        "severity": severity,
        "element_absent": severity == "absent",
        "candidate_evidence": [f"Candidate A, NOW: {defect_id}"],
        "controlling_evidence": [f"Source 1, required behavior for {defect_id}"],
    }
    grade["defects"].append(defect)
    return defect


def charge_defect(
    grade: dict[str, object],
    criterion_id: str,
    defect_id: str,
    verdict: str | None = None,
) -> None:
    """Cite a defect from a criterion; the verdict defaults to the worst cited severity."""
    entry = criterion_entry(grade, criterion_id)
    defect_ids = [*entry["defect_ids"], defect_id]
    severities = [
        str(defect["severity"]) for defect in grade["defects"] if defect["id"] in defect_ids
    ]
    entry.update(
        {
            "verdict": verdict or min(severities, key=lambda severity: VERDICT_SCORES[severity]),
            "candidate_evidence": ["Candidate A, NOW: defective behavior"],
            "controlling_evidence": ["Source 1, required behavior"],
            "defect_ids": defect_ids,
        }
    )


def set_nonpass(
    grade: dict[str, object],
    criterion_id: str,
    verdict: str,
    defect_id: str = "defect-1",
) -> None:
    criterion_entry(grade, criterion_id)
    declare_defect(grade, defect_id, criterion_id, verdict)
    charge_defect(grade, criterion_id, defect_id)
