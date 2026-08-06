"""The projection from the map's Markdown to the records the validator reads."""

from __future__ import annotations

import unittest
from pathlib import Path

from consensus.extract_clause_map import COLUMNS, Record, emit, parse_map, wording_errors

TOOL_DIR = Path(__file__).resolve().parents[2]
MAP = (TOOL_DIR / "support/CLAUSE-ROW-MAP.md").read_text(encoding="utf-8")


def record(identifier: str, sites: str, last: str) -> Record:
    spans = tuple(
        (int(part.split("-")[0]), int(part.split("-")[-1])) for part in sites.split(",")
    )
    return Record(identifier, spans, "§ 1 Build the evidence inventory", "a clause", (), "—", "c001780", last)


class FakeHistory:
    """`SKILL.md`'s commits, newest first; `age` is the distance from `HEAD`."""

    def __init__(self, *commits: str) -> None:
        self._age = {commit: index for index, commit in enumerate(commits)}

    def age(self, commit: str) -> int | None:
        return self._age.get(commit)


class ParseMap(unittest.TestCase):
    def test_every_clause_of_the_map_becomes_a_record(self):
        records = parse_map(MAP)

        self.assertEqual(len(records), 205)
        self.assertEqual(records[0].id, "C-001")
        self.assertEqual(records[-1].id, "C-205")

    def test_a_clause_stated_at_two_sites_keeps_both_spans(self):
        records = {item.id: item for item in parse_map(MAP)}

        self.assertEqual(records["C-033"].spans, ((87, 87), (90, 90)))
        self.assertEqual(records["C-033"].rows, ("R-008", "R-011"))

    def test_a_restatement_marker_does_not_become_part_of_the_row_id(self):
        records = {item.id: item for item in parse_map(MAP)}

        self.assertEqual(records["C-103"].rows, ("R-006", "R-016"))

    def test_every_record_is_emitted_as_one_line_of_named_columns(self):
        records = parse_map(MAP)

        lines = emit(records, {}).splitlines()

        self.assertEqual(lines[0].split("\t"), list(COLUMNS))
        self.assertEqual(len(lines), len(records) + 1)
        self.assertEqual(
            lines[1].split("\t")[:2], [records[0].id, "10-11"]
        )


class WordingCommitCheck(unittest.TestCase):
    """`last` is carried from the map, so what git can still answer is that it is not too new."""

    def test_a_wording_commit_older_than_the_last_change_to_its_site_is_accepted(self):
        history = FakeHistory("87150d3", "d977043", "745192f")
        records = [record("C-013", "43-43", "745192f")]

        self.assertEqual(wording_errors(history, records, {"C-013": "d977043"}), [])

    def test_a_wording_commit_newer_than_the_last_change_to_its_site_is_an_error(self):
        history = FakeHistory("87150d3", "d977043", "745192f")
        records = [record("C-013", "43-43", "87150d3")]

        errors = wording_errors(history, records, {"C-013": "d977043"})

        self.assertIn("newer than the last change to its site", errors[0])

    def test_a_wording_commit_that_never_touched_the_skill_is_an_error(self):
        history = FakeHistory("87150d3", "d977043")
        records = [record("C-013", "43-43", "deadbee")]

        errors = wording_errors(history, records, {"C-013": "d977043"})

        self.assertIn("never touched", errors[0])

    def test_an_unresolved_site_leaves_its_wording_commit_unverified(self):
        history = FakeHistory("87150d3")
        records = [record("C-013", "43-43", "deadbee")]

        self.assertEqual(wording_errors(history, records, {}), [])


if __name__ == "__main__":
    unittest.main()
