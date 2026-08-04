from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from grade_plan import render_prompt
from grading_contract import absolute_grade_schema, score_grade, validate_absolute_grade
from scoring import score_components
from v3_test_support import RUBRIC, passing_grade, set_nonpass


class ContractsV3Tests(unittest.TestCase):
    def test_score_keeps_current_axis_worst_formula_and_is_fully_versioned(self) -> None:
        grade = passing_grade()
        set_nonpass(grade, "slice_cohesive_cut", "material")

        score = score_grade(RUBRIC, grade)

        component = next(item for item in score["components"] if item["id"] == "slice_cohesion_verticality")
        self.assertEqual(component["axis_score"], 2.0)
        self.assertEqual(score["scoring_version"], 3)
        self.assertEqual(score["scoring_strategy"], "axis_worst")

    def test_cap_is_derived_from_critical_failure(self) -> None:
        grade = passing_grade()
        grade["critical_failures"] = [
            {
                "id": "unsafe_scope_boundary",
                "conditions_met": ["Persistence is unscoped."],
                "exclusions_checked": ["Not a single-scope diagnostic."],
                "candidate_evidence": ["Candidate A, NOW 1"],
                "controlling_evidence": ["Source 1, Condivisione"],
            }
        ]

        score = score_grade(RUBRIC, grade)

        self.assertEqual(score["effective_total"], 49.0)
        self.assertEqual(score["applied_caps"], [{"id": "unsafe_scope_boundary", "cap": 49}])

    def test_rejects_critical_failure_without_conditions_or_citations(self) -> None:
        failure = {
            "id": "unsafe_scope_boundary",
            "conditions_met": ["Persistence is unscoped."],
            "exclusions_checked": ["Not a single-scope diagnostic."],
            "candidate_evidence": ["Candidate A, NOW 1"],
            "controlling_evidence": ["Source 1, Condivisione"],
        }
        required_fields = (
            "conditions_met",
            "exclusions_checked",
            "candidate_evidence",
            "controlling_evidence",
        )

        for field in required_fields:
            with self.subTest(field=field):
                grade = passing_grade()
                grade["critical_failures"] = [{**failure, field: []}]

                with self.assertRaisesRegex(ValueError, "expected at least one"):
                    validate_absolute_grade(RUBRIC, grade)

    def test_schema_requires_complete_defect_and_critical_failure_evidence(self) -> None:
        schema = absolute_grade_schema(RUBRIC)

        defect_schema = schema["properties"]["defects"]["items"]
        failure_schema = schema["properties"]["critical_failures"]["items"]

        for evidence_schema in (defect_schema, failure_schema):
            with self.subTest(schema=evidence_schema):
                properties = evidence_schema["properties"]
                self.assertEqual(properties["candidate_evidence"]["minItems"], 1)
                self.assertEqual(properties["controlling_evidence"]["minItems"], 1)

    def test_rejects_defect_without_controlling_evidence(self) -> None:
        grade = passing_grade()
        set_nonpass(grade, "slice_cohesive_cut", "material")
        grade["defects"][0]["controlling_evidence"] = []

        with self.assertRaisesRegex(ValueError, "expected at least one"):
            validate_absolute_grade(RUBRIC, grade)

    def test_rejects_absent_as_generic_severe(self) -> None:
        grade = passing_grade()
        set_nonpass(grade, "slice_cohesive_cut", "absent")
        grade["defects"][0]["element_absent"] = False

        with self.assertRaisesRegex(ValueError, "totally missing"):
            validate_absolute_grade(RUBRIC, grade)

    def test_schema_never_asks_model_for_scores(self) -> None:
        schema = absolute_grade_schema(RUBRIC)

        self.assertNotIn("score", str(schema).lower())

    def test_prompt_is_path_and_generator_anonymous(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "PLAN-CX-codex.md"
            brief = root / "REFERENCE-PLAN.md"
            plan = root / "PLAN-CC-claude.md"
            source.write_text("Product truth", encoding="utf-8")
            brief.write_text("# Authority\n\n- Rule", encoding="utf-8")
            plan.write_text("Candidate content", encoding="utf-8")

            prompt = render_prompt(RUBRIC, brief, plan, [source])

        self.assertNotIn(str(root), prompt)
        self.assertNotIn("PLAN-CX", prompt)
        self.assertNotIn("codex", prompt.lower())
        self.assertNotIn("claude", prompt.lower())
        self.assertIn("## Source 1", prompt)
        self.assertIn("## Evaluation brief", prompt)
        self.assertIn("## Candidate A", prompt)

    def test_scoring_rounding_is_deterministic(self) -> None:
        components, total = score_components(
            [{"id": "axis", "weight": 100, "criteria": [{"id": "a", "verdict": "minor"}, {"id": "b", "verdict": "material"}, {"id": "c", "verdict": "pass"}]}],
            "criterion_mean",
        )

        self.assertEqual(components[0]["axis_score"], 3.0)
        self.assertEqual(total, 75.0)


if __name__ == "__main__":
    unittest.main()
