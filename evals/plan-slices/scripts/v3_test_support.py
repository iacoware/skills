from __future__ import annotations

import json
from pathlib import Path


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


def set_nonpass(
    grade: dict[str, object],
    criterion_id: str,
    verdict: str,
    defect_id: str = "defect-1",
) -> None:
    for axis in grade["axes"]:
        for entry in axis["criteria"]:
            if entry["id"] == criterion_id:
                entry.update(
                    {
                        "verdict": verdict,
                        "candidate_evidence": ["Candidate A, NOW: defective behavior"],
                        "controlling_evidence": ["Source 1, required behavior"],
                        "defect_ids": [defect_id],
                    }
                )
                grade["defects"].append(
                    {
                        "id": defect_id,
                        "primary_criterion": criterion_id,
                        "consequence": "The delivery decision is invalid.",
                        "severity": verdict,
                        "element_absent": verdict == "absent",
                        "candidate_evidence": ["Candidate A, NOW: defective behavior"],
                        "controlling_evidence": ["Source 1, required behavior"],
                    }
                )
                return
    raise AssertionError(f"unknown criterion: {criterion_id}")
