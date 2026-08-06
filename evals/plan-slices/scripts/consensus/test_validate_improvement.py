"""The contract's tool-decidable half, and the asymmetry the CON-4 artifacts already carry."""

from __future__ import annotations

import unittest
from pathlib import Path

from consensus.validate_improvement import LEDGER_ROW_PATTERN, load_clauses, validate

TOOL_DIR = Path(__file__).resolve().parents[2]
RESULTS_DIR = TOOL_DIR / "recipe-app/results"
CLAUSES = load_clauses((TOOL_DIR / "support/clause-row-map.tsv").read_text(encoding="utf-8"))
LEDGER_ROWS = LEDGER_ROW_PATTERN.findall(
    (TOOL_DIR / "REGRESSION-LEDGER.md").read_text(encoding="utf-8")
)

CONFORMING_FIELDS = {
    "Evidence — candidate A": "- `PLAN-CC-CON-5.md:130` — the bullet asserts one side of the conflict",
    "Evidence — candidate B": "- `slice 4 Includes` — the same assertion, without the condition",
    "Existing rule that failed to prevent the defect": (
        "- **Clause:** `SKILL.md:56-57` § `§ 1 Build the evidence inventory` — «no `Includes` "
        "bullet may assert a side»\n"
        "- **Covering rows:** `R-010`"
    ),
    "Remedy": "- `reformulation`",
    "Change to the skill": (
        "- **Section:** `§ 1 Build the evidence inventory`\n"
        "- **Change:** name the horizons the prohibition reaches, not only the slice fields"
    ),
    "Binary test": "- No `NOW` slice asserts a side of an open choice in any horizon.",
    "Cost": "- Nothing is removed; the existing prohibition is restated once.",
}


def document(*entries: dict[str, str], candidates: bool = True) -> str:
    inputs = (
        "- **Candidate A:** `PLAN-CC-CON-5.md`\n- **Candidate B:** `PLAN-CX-CON-5.md`\n"
        if candidates
        else "- none\n"
    )
    body = ["# Improvement report — cycle CON-6", "", "## Inputs", "", inputs, "## Entries", ""]
    for number, overrides in enumerate(entries or ({},), start=1):
        fields = {**CONFORMING_FIELDS, **overrides}
        body.append(f"### {number}. A defect worth a rule")
        body.append("")
        body.append("---")
        body.append("")
        for name, value in fields.items():
            if value is None:
                continue
            body.extend([f"**{name}**", "", value, ""])
    return "\n".join(body)


def run(text: str):
    return validate("test.IMPROVEMENT.md", text, CLAUSES, LEDGER_ROWS, RESULTS_DIR)


def reasons(result, field_name: str) -> list[str]:
    return [discard.reason for discard in result.discards if discard.field == field_name]


class ConformingEntry(unittest.TestCase):
    def test_an_entry_that_fills_the_contract_is_kept(self):
        result = run(document())

        self.assertEqual(result.conforming, [1])
        self.assertEqual(result.discards, [])
        self.assertEqual(result.document_errors, [])

    def test_a_failing_entry_falls_alone(self):
        result = run(document({}, {"Cost": None}, {}))

        self.assertEqual(result.conforming, [1, 3])
        self.assertEqual(reasons(result, "Cost"), ["missing required field"])


class DeclaredFields(unittest.TestCase):
    def test_a_field_declared_twice_is_discarded(self):
        entry = {"Cost": "- Nothing is removed.\n\n**Cost**\n\n- And nothing is merged."}

        result = run(document(entry))

        self.assertEqual(reasons(result, "Cost"), ["declared more than once"])


class Evidence(unittest.TestCase):
    def test_a_line_past_the_end_of_the_candidate_is_discarded(self):
        result = run(document({"Evidence — candidate A": "- `PLAN-CC-CON-5.md:9000` — invented"}))

        self.assertIn("outside its 346 lines", reasons(result, "Evidence — candidate A")[0])

    def test_citing_the_other_side_s_candidate_is_discarded(self):
        result = run(document({"Evidence — candidate A": "- `PLAN-CX-CON-5.md:12` — wrong side"}))

        self.assertIn("not this side's candidate", reasons(result, "Evidence — candidate A")[0])

    def test_a_slice_the_candidate_does_not_have_is_discarded(self):
        result = run(document({"Evidence — candidate B": "- `slice 99 Includes` — invented"}))

        self.assertEqual(
            reasons(result, "Evidence — candidate B"),
            ["`PLAN-CX-CON-5.md` has no slice 99"],
        )

    def test_a_field_the_cited_slice_does_not_have_is_discarded(self):
        result = run(document({"Evidence — candidate B": "- `slice 4 Prerequisites` — invented"}))

        self.assertIn("has no `Prerequisites` field", reasons(result, "Evidence — candidate B")[0])

    def test_a_defect_neither_candidate_manifests_is_discarded(self):
        absent = {
            "Evidence — candidate A": "- `not manifested` — the slice defers to the spike",
            "Evidence — candidate B": "- `not manifested` — the slice defers to the spike",
        }

        result = run(document(absent))

        self.assertIn("neither candidate manifests", reasons(result, "Evidence — candidate A")[0])

    def test_not_manifested_must_say_what_the_candidate_does_instead(self):
        result = run(document({"Evidence — candidate B": "- `not manifested`"}))

        self.assertIn("what that candidate does instead", reasons(result, "Evidence — candidate B")[0])


class CoveringRows(unittest.TestCase):
    def test_declaring_uncovered_where_the_map_covers_is_discarded(self):
        entry = {
            "Existing rule that failed to prevent the defect": (
                "- **Clause:** `SKILL.md:56-57` § `§ 1 Build the evidence inventory` — «…»\n"
                "- **Covering rows:** `uncovered`"
            )
        }

        result = run(document(entry))

        self.assertIn(
            "declares `uncovered`, but the map covers C-019 with R-010",
            reasons(result, "Existing rule that failed to prevent the defect")[0],
        )

    def test_a_row_the_ledger_does_not_hold_is_discarded(self):
        entry = {
            "Existing rule that failed to prevent the defect": (
                "- **Clause:** `SKILL.md:56-57` § `§ 1 Build the evidence inventory` — «…»\n"
                "- **Covering rows:** `R-999`"
            )
        }

        result = run(document(entry))

        self.assertEqual(
            reasons(result, "Existing rule that failed to prevent the defect"),
            ["names rows the ledger does not hold: R-999"],
        )

    def test_a_site_that_holds_no_clause_is_discarded(self):
        entry = {
            "Existing rule that failed to prevent the defect": (
                "- **Clause:** `SKILL.md:1-2` § `Preamble` — «frontmatter»\n"
                "- **Covering rows:** `uncovered`"
            )
        }

        result = run(document(entry))

        self.assertEqual(
            reasons(result, "Existing rule that failed to prevent the defect"),
            ["`SKILL.md:1-2` holds no normative clause"],
        )

    def test_naming_the_wrong_section_for_the_site_is_discarded(self):
        entry = {
            "Existing rule that failed to prevent the defect": (
                "- **Clause:** `SKILL.md:56-57` § `§ 5 Publish and audit` — «…»\n"
                "- **Covering rows:** `R-010`"
            )
        }

        result = run(document(entry))

        self.assertIn(
            "but that site is in § 1 Build the evidence inventory",
            reasons(result, "Existing rule that failed to prevent the defect")[0],
        )

    def test_naming_no_clause_requires_naming_no_rows(self):
        entry = {
            "Existing rule that failed to prevent the defect": (
                "- **Clause:** `none`\n- **Covering rows:** `R-010`"
            ),
            "Remedy": "- `addition`",
        }

        result = run(document(entry))

        self.assertEqual(
            reasons(result, "Existing rule that failed to prevent the defect"),
            ["`Clause: none` requires `Covering rows: none`"],
        )


class BinaryTest(unittest.TestCase):
    def test_a_judgement_is_not_a_binary_test(self):
        result = run(document({"Binary test": "- The plan is clearer about open choices."}))

        self.assertIn("states a judgement", reasons(result, "Binary test")[0])

    def test_a_claim_that_prescribes_instead_of_observing_is_discarded(self):
        result = run(document({"Binary test": "- Every `NOW` slice should cite a source."}))

        self.assertIn("states a judgement, not an observation: should", reasons(result, "Binary test")[0])

    def test_a_claim_that_quantifies_over_nothing_the_plan_publishes_is_discarded(self):
        result = run(document({"Binary test": "- Every author names a reason."}))

        self.assertIn("must quantify over something a generated plan publishes", reasons(result, "Binary test"))

    def test_the_ledger_s_own_claims_pass_the_grammar(self):
        claims = (
            "- No `NOW` slice delivers a behaviour the sources do not request.",
            "- Every `LATER` entry states a `Promotion trigger`.",
            "- The plan places identity after the differentiator.",
            "- If more than two `NOW` slices deliver behaviour to an end user before identity, "
            "`Ordering criteria` justifies the residual deferral once.",
            "- A `NOW` slice that reuses a pipeline opened by an earlier slice declares it as reuse.",
        )

        for claim in claims:
            with self.subTest(claim=claim):
                self.assertEqual(run(document({"Binary test": claim})).conforming, [1])


class ConditionalFields(unittest.TestCase):
    def test_a_reach_change_without_a_merged_claim_is_discarded(self):
        result = run(document({"Remedy": "- `reach-change`"}))

        self.assertEqual(
            reasons(result, "Merged claim"),
            ["required when the remedy changes a rule's reach"],
        )

    def test_a_reach_change_states_the_merged_claim_and_the_rows_it_absorbs(self):
        entry = {
            "Remedy": "- `reach-change`",
            "Merged claim": "- No `NOW` slice asserts a side of an open choice, in any horizon.",
        }

        result = run(document(entry))

        self.assertEqual(result.conforming, [1])

    def test_a_merged_claim_without_a_reach_change_is_discarded(self):
        entry = {"Merged claim": "- No `NOW` slice asserts a side of an open choice."}

        result = run(document(entry))

        self.assertEqual(reasons(result, "Merged claim"), ["forbidden when the remedy is `reformulation`"])

    def test_a_merge_that_absorbs_no_declared_row_is_discarded(self):
        entry = {
            "Existing rule that failed to prevent the defect": (
                "- **Clause:** `SKILL.md:339` § `§ 5 Publish and audit` — «…»\n"
                "- **Covering rows:** `uncovered`"
            ),
            "Remedy": "- `reach-change`",
            "Merged claim": "- Every `Themes` row resolves its `First validation` to a `NOW` slice.",
        }

        result = run(document(entry))

        self.assertIn("names no absorbed row", reasons(result, "Merged claim")[0])

    def test_adding_rules_next_to_a_named_clause_requires_the_discarded_reformulation(self):
        result = run(document({"Remedy": "- `addition`"}))

        self.assertEqual(
            reasons(result, "Reformulation attempted and discarded, and why"),
            ["required when an entry adds rules next to a named clause"],
        )

    def test_an_addition_on_uncovered_ground_needs_no_discarded_reformulation(self):
        entry = {
            "Existing rule that failed to prevent the defect": (
                "- **Clause:** `none`\n- **Covering rows:** `none`"
            ),
            "Remedy": "- `addition`",
        }

        result = run(document(entry))

        self.assertEqual(result.conforming, [1])

    def test_a_half_written_discarded_reformulation_is_discarded(self):
        entry = {
            "Remedy": "- `addition`",
            "Reformulation attempted and discarded, and why": "- **Discarded because:** covered by `R-010`",
        }

        result = run(document(entry))

        self.assertEqual(
            reasons(result, "Reformulation attempted and discarded, and why"),
            ["missing sub-field Reformulation attempted"],
        )


class Document(unittest.TestCase):
    def test_candidates_that_are_not_declared_stop_the_reference_check(self):
        result = run(document(candidates=False))

        self.assertIn("`## Inputs` does not declare candidate A", result.document_errors)
        self.assertIn("is not declared in `## Inputs`", reasons(result, "Evidence — candidate A")[0])

    def test_the_template_declares_every_field_the_validator_requires(self):
        template = (TOOL_DIR / "assets/improvement-template.md").read_text(encoding="utf-8")

        for name in (*CONFORMING_FIELDS, "Merged claim", "Reformulation attempted and discarded, and why"):
            with self.subTest(field=name):
                self.assertIn(f"**{name}**", template)


class CommittedRecords(unittest.TestCase):
    def test_the_committed_records_cover_every_clause_of_the_map(self):
        from consensus.extract_clause_map import parse_map

        records = parse_map((TOOL_DIR / "support/CLAUSE-ROW-MAP.md").read_text(encoding="utf-8"))

        self.assertEqual([clause.id for clause in CLAUSES], [record.id for record in records])
        self.assertEqual(
            [clause.rows for clause in CLAUSES], [record.rows for record in records]
        )


class Con4Artifacts(unittest.TestCase):
    """The fixture pair the project already owns: one side has entries, the other has none."""

    def _validate(self, name: str):
        path = RESULTS_DIR / name
        return validate(name, path.read_text(encoding="utf-8"), CLAUSES, LEDGER_ROWS, RESULTS_DIR)

    def test_the_cc_report_yields_entries_and_none_of_them_conforms(self):
        result = self._validate("PLAN-CC-CON-4.IMPROVEMENT.md")

        self.assertEqual(result.entries, 10)
        self.assertEqual(result.conforming, [])
        self.assertEqual(len({discard.entry for discard in result.discards}), 10)

    def test_the_cx_report_yields_no_entry_at_all(self):
        result = self._validate("PLAN-CX-CON-4.IMPROVEMENT.md")

        self.assertEqual(result.entries, 0)
        self.assertEqual(result.conforming, [])
        self.assertIn(
            "missing `## Entries`: no entry can be read from this document", result.document_errors
        )


if __name__ == "__main__":
    unittest.main()
