from __future__ import annotations

import unittest

from grading_contract import score_grade, validate_absolute_grade
from v3_test_support import (
    RUBRIC,
    charge_defect,
    criterion_entry,
    declare_defect,
    passing_grade,
    set_nonpass,
)


class DefectChargingRejectionTests(unittest.TestCase):
    def test_rejects_defect_without_primary_criterion(self) -> None:
        grade = passing_grade()
        set_nonpass(grade, "content_failure_quality", "material")
        del grade["defects"][0]["primary_criterion"]

        with self.assertRaisesRegex(ValueError, "primary_criterion: expected a non-empty string"):
            validate_absolute_grade(RUBRIC, grade)

    def test_rejects_defect_whose_primary_criterion_is_not_in_the_rubric(self) -> None:
        grade = passing_grade()
        set_nonpass(grade, "content_failure_quality", "material")
        grade["defects"][0]["primary_criterion"] = "content_backup_coverage"

        with self.assertRaisesRegex(ValueError, "unknown primary criterion"):
            validate_absolute_grade(RUBRIC, grade)

    def test_rejects_criterion_citing_an_undeclared_defect(self) -> None:
        grade = passing_grade()
        charge_defect(grade, "content_failure_quality", "missing-backup", verdict="material")

        with self.assertRaisesRegex(ValueError, "dangling defect missing-backup"):
            validate_absolute_grade(RUBRIC, grade)

    def test_rejects_defect_no_criterion_charges(self) -> None:
        grade = passing_grade()
        declare_defect(grade, "missing-backup", "content_failure_quality", "material")

        with self.assertRaisesRegex(ValueError, r"unreferenced defects \['missing-backup'\]"):
            validate_absolute_grade(RUBRIC, grade)

    def test_rejects_two_defects_sharing_one_id(self) -> None:
        grade = passing_grade()
        set_nonpass(grade, "content_failure_quality", "material", defect_id="missing-backup")
        declare_defect(grade, "missing-backup", "horizon_coherent_now", "minor")

        with self.assertRaisesRegex(ValueError, "duplicate id missing-backup"):
            validate_absolute_grade(RUBRIC, grade)

    def test_rejects_the_same_defect_cited_twice_by_one_criterion(self) -> None:
        grade = passing_grade()
        set_nonpass(grade, "content_failure_quality", "material", defect_id="missing-backup")
        charge_defect(grade, "content_failure_quality", "missing-backup")

        with self.assertRaisesRegex(ValueError, "duplicate defect reference"):
            validate_absolute_grade(RUBRIC, grade)

    def test_rejects_defect_charged_to_a_second_criterion(self) -> None:
        grade = passing_grade()
        set_nonpass(grade, "content_failure_quality", "material", defect_id="missing-backup")
        charge_defect(grade, "horizon_coherent_now", "missing-backup")

        with self.assertRaisesRegex(ValueError, "only to its primary criterion"):
            validate_absolute_grade(RUBRIC, grade)

    def test_rejects_verdict_milder_than_the_worst_charged_defect(self) -> None:
        grade = passing_grade()
        set_nonpass(grade, "content_failure_quality", "minor", defect_id="missing-backup-check")
        declare_defect(grade, "missing-restore-drill", "content_failure_quality", "material")
        charge_defect(grade, "content_failure_quality", "missing-restore-drill", verdict="minor")

        with self.assertRaisesRegex(ValueError, "verdict must equal worst defect severity"):
            validate_absolute_grade(RUBRIC, grade)


class RootDefectScopeTests(unittest.TestCase):
    def test_missing_guardrails_lower_one_criterion_each(self) -> None:
        grade = passing_grade()
        set_nonpass(grade, "content_failure_quality", "material", defect_id="missing-backup")
        set_nonpass(grade, "horizon_coherent_now", "material", defect_id="missing-spend-guardrail")

        validate_absolute_grade(RUBRIC, grade)

        charged = {
            defect["id"]: criterion_entry(grade, str(defect["primary_criterion"]))["defect_ids"]
            for defect in grade["defects"]
        }
        self.assertEqual(charged, {"missing-backup": ["missing-backup"], "missing-spend-guardrail": ["missing-spend-guardrail"]})
        self.assertEqual(criterion_entry(grade, "content_right_detail")["verdict"], "pass")
        self.assertEqual(criterion_entry(grade, "horizon_exclusive")["verdict"], "pass")

    def test_consultation_write_merge_lowers_only_its_primary_criterion(self) -> None:
        grade = passing_grade()
        set_nonpass(grade, "theme_split_merge", "material", defect_id="consultation-write-merge")

        validate_absolute_grade(RUBRIC, grade)

        for criterion_id in ("slice_cohesive_cut", "content_single_result"):
            self.assertEqual(criterion_entry(grade, criterion_id)["verdict"], "pass")

    def test_consultation_write_merge_cannot_lower_three_criteria(self) -> None:
        grade = passing_grade()
        set_nonpass(grade, "theme_split_merge", "material", defect_id="consultation-write-merge")
        charge_defect(grade, "slice_cohesive_cut", "consultation-write-merge")
        charge_defect(grade, "content_single_result", "consultation-write-merge")

        with self.assertRaisesRegex(ValueError, "only to its primary criterion"):
            validate_absolute_grade(RUBRIC, grade)

    def test_distinct_defects_on_one_criterion_stay_valid_and_the_worst_sets_the_verdict(self) -> None:
        grade = passing_grade()
        set_nonpass(grade, "content_failure_quality", "minor", defect_id="missing-backup-check")
        declare_defect(
            grade,
            "missing-restore-drill",
            "content_failure_quality",
            "material",
            consequence="A restore is never exercised before the NOW release.",
        )
        charge_defect(grade, "content_failure_quality", "missing-restore-drill")

        score = score_grade(RUBRIC, grade)

        self.assertEqual(criterion_entry(grade, "content_failure_quality")["verdict"], "material")
        component = next(item for item in score["components"] if item["id"] == "slice_content_evidence")
        self.assertEqual(component["axis_score"], 2.0)


if __name__ == "__main__":
    unittest.main()
