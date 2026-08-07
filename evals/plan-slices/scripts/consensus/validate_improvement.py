#!/usr/bin/env python3
"""Validate an `IMPROVEMENT` document entry by entry against the conformance contract.

The contract is `assets/improvement-template.md`; this is the half of it a tool can decide. A
non-conforming entry is **discarded on its own**: the entry falls, the document stands, and the
document is never regenerated. One attempt per cycle.

What the tool decides and what it cannot: it checks that a reference exists, not that it supports
the claim; that a merged claim is stated in the ledger's grammar, not that the merge stays decidable
in one reading; that a discarded reformulation was written down, not that the reason for discarding
it is admissible. Those residues are reading, and they belong to the human veto — the same
`validator`/`reading` seam the ledger rows are split along.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Sequence

REQUIRED_FIELDS = (
    "Evidence — candidate A",
    "Evidence — candidate B",
    "Existing rule that failed to prevent the defect",
    "Remedy",
    "Change to the skill",
    "Binary test",
    "Cost",
)
CONDITIONAL_FIELDS = ("Merged claim", "Reformulation attempted and discarded, and why")
REMEDIES = ("reformulation", "reach-change", "addition")
NOT_MANIFESTED = "not manifested"
NONE = "none"
UNCOVERED = "uncovered"

H2_PATTERN = re.compile(r"^## (?!#)(.+?)\s*$", re.MULTILINE)
H3_PATTERN = re.compile(r"^### (\d+)\.\s+(.+?)\s*$", re.MULTILINE)
NUMBERED_HEADING_PATTERN = re.compile(r"^#{2,3} (\d+)\.\s+(.+?)\s*$", re.MULTILINE)
HEADING_PATTERN = re.compile(r"^#{1,6} \S", re.MULTILINE)
FIELD_PATTERN = re.compile(r"^\*\*([^*]+?)\*\*\s*$", re.MULTILINE)
BULLET_PATTERN = re.compile(r"^\s*[-*+]\s+(.*)$")
LABELLED_PATTERN = re.compile(r"^\*\*([^*]+?):\*\*\s*(.*)$")
CANDIDATE_PATTERN = re.compile(r"^\s*[-*+]\s+\*\*Candidate ([AB]):\*\*\s*`([^`]+)`\s*$", re.MULTILINE)
LINE_REFERENCE_PATTERN = re.compile(r"^([\w.\-]+\.md):(\d+)(?:-(\d+))?$")
SLICE_REFERENCE_PATTERN = re.compile(r"^slice (\d+)\s+(.+?)$")
SITE_PATTERN = re.compile(r"`SKILL\.md:(\d+)(?:-(\d+))?`")
SECTION_QUOTE_PATTERN = re.compile(r"§\s*`([^`]+)`")
ROW_PATTERN = re.compile(r"\bR-\d{3}\b")
LEDGER_ROW_PATTERN = re.compile(r"^\|\s*(R-\d{3})\s*\|", re.MULTILINE)
SLICE_HEADING_PATTERN = re.compile(r"^### (\d+)\.", re.MULTILINE)

CLAIM_OPENERS = ("A", "An", "Each", "Every", "If", "No", "The", "When", "Where")
CLAIM_SUBJECTS = (
    "plan",
    "slice",
    "slices",
    "now",
    "later",
    "out-of-scope",
    "theme",
    "themes",
    "includes",
    "verification",
    "outcome",
    "learning / risk",
    "ordering criteria",
    "cross-functional concerns",
    "open questions",
    "decision checkpoints",
    "non-product work",
    "promotion trigger",
    "first validation",
    "enabler",
    "release",
)
CLAIM_VAGUENESS = (
    "adequate",
    "adequately",
    "appropriate",
    "appropriately",
    "better",
    "clear",
    "clearer",
    "clearly",
    "good",
    "improved",
    "meaningful",
    "ought",
    "properly",
    "reasonable",
    "should",
    "sufficient",
    "sufficiently",
)


@dataclass(frozen=True)
class Clause:
    id: str
    spans: tuple[tuple[int, int], ...]
    section: str
    rows: tuple[str, ...]

    def covers(self, start: int, end: int) -> bool:
        return any(start <= span_end and end >= span_start for span_start, span_end in self.spans)


@dataclass(frozen=True)
class Entry:
    number: int
    title: str
    fields: dict[str, str]
    declared: tuple[str, ...]


@dataclass(frozen=True)
class Discard:
    entry: int
    title: str
    field: str
    reason: str


@dataclass
class Result:
    document: str
    entries: int = 0
    conforming: list[int] = field(default_factory=list)
    discards: list[Discard] = field(default_factory=list)
    document_errors: list[str] = field(default_factory=list)


def load_clauses(tsv: str) -> tuple[Clause, ...]:
    clauses: list[Clause] = []
    for line in tsv.splitlines()[1:]:
        if not line.strip():
            continue
        cells = line.split("\t")
        spans = tuple(
            (int(part.split("-")[0]), int(part.split("-")[1])) for part in cells[1].split(",")
        )
        clauses.append(Clause(cells[0], spans, cells[2], tuple(ROW_PATTERN.findall(cells[4]))))
    return tuple(clauses)


def _sections(clauses: Iterable[Clause]) -> dict[str, str]:
    """Section names as the map states them, keyed by their comparable form."""
    return {_comparable(clause.section): clause.section for clause in clauses}


def _comparable(section: str) -> str:
    return " ".join(re.sub(r"[`§.]", " ", section).lower().split())


def _fields(body: str) -> tuple[dict[str, str], tuple[str, ...]]:
    """The fields by name, and the names in the order they were declared, duplicates included."""
    matches = list(FIELD_PATTERN.finditer(body))
    fields: dict[str, str] = {}
    declared: list[str] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        name = match.group(1).strip()
        declared.append(name)
        fields.setdefault(name, body[match.end() : end].strip())
    return fields, tuple(declared)


def _bullets(body: str) -> list[str]:
    bullets: list[str] = []
    for line in body.splitlines():
        if match := BULLET_PATTERN.match(line):
            bullets.append(match.group(1).strip())
        elif bullets and line.startswith("  ") and line.strip():
            bullets[-1] += " " + line.strip()
    return bullets


def _labelled(body: str) -> dict[str, str]:
    labelled: dict[str, str] = {}
    for bullet in _bullets(body):
        if match := LABELLED_PATTERN.match(bullet):
            labelled.setdefault(match.group(1).strip(), match.group(2).strip())
    return labelled


def parse_entries(text: str) -> tuple[dict[str, str], tuple[Entry, ...], list[str]]:
    errors: list[str] = []
    headings = list(H2_PATTERN.finditer(text))
    sections = {
        match.group(1): text[
            match.end() : headings[index + 1].start() if index + 1 < len(headings) else len(text)
        ]
        for index, match in enumerate(headings)
    }

    candidates: dict[str, str] = {}
    if "Inputs" not in sections:
        errors.append("missing `## Inputs`: the two candidates are not declared")
    else:
        candidates = {
            match.group(1): match.group(2)
            for match in CANDIDATE_PATTERN.finditer(sections["Inputs"])
        }
        for side in ("A", "B"):
            if side not in candidates:
                errors.append(f"`## Inputs` does not declare candidate {side}")

    if "Entries" in sections:
        entries = _entries(sections["Entries"], H3_PATTERN)
        if not entries:
            errors.append("`## Entries` holds no numbered entry")
    else:
        # Read the entries anyway: a document that numbers its entries somewhere else still owes a
        # per-entry discard log, and «no `## Entries`» and «no entries at all» are different facts.
        entries = _entries(text, NUMBERED_HEADING_PATTERN)
        errors.append(
            f"missing `## Entries`; read {len(entries)} numbered heading(s) as entries instead"
            if entries
            else "missing `## Entries`: no entry can be read from this document"
        )
    return candidates, entries, errors


def _entries(text: str, pattern: re.Pattern[str]) -> tuple[Entry, ...]:
    matches = list(pattern.finditer(text))
    bounds = [match.start() for match in HEADING_PATTERN.finditer(text)] + [len(text)]
    return tuple(
        Entry(
            int(match.group(1)),
            match.group(2),
            *_fields(text[match.end() : next(end for end in bounds if end > match.start())]),
        )
        for match in matches
    )


def _claim_errors(body: str) -> list[str]:
    """One row, one claim: the ledger's writing rule applied where the claim is written."""
    errors: list[str] = []
    bullets = _bullets(body)
    if len(bullets) > 1:
        return ["must state exactly one claim"]
    bare = re.sub(r"[`«»*]", "", bullets[0] if bullets else "").strip()
    if not bare:
        return ["is empty"]
    if not bare.endswith("."):
        errors.append("must be one claim ending in a full stop")
    opener = bare.split()[0].strip(",")
    if opener not in CLAIM_OPENERS:
        errors.append(f"must open with one of {', '.join(CLAIM_OPENERS)}, not {opener!r}")
    lowered = bare.lower()
    if not any(re.search(rf"\b{re.escape(term)}\b", lowered) for term in CLAIM_SUBJECTS):
        errors.append("must quantify over something a generated plan publishes")
    vague = [term for term in CLAIM_VAGUENESS if re.search(rf"\b{term}\b", lowered)]
    if vague:
        errors.append(f"states a judgement, not an observation: {', '.join(vague)}")
    return errors


class Candidates:
    """The two generated plans an entry cites. Resolving a reference is all this knows how to do."""

    def __init__(self, declared: dict[str, str], plans_dir: Path) -> None:
        self.declared = declared
        self.plans_dir = plans_dir
        self._cache: dict[str, list[str] | None] = {}

    def _lines(self, name: str) -> list[str] | None:
        if name not in self._cache:
            path = self.plans_dir / name
            self._cache[name] = (
                path.read_text(encoding="utf-8").splitlines() if path.is_file() else None
            )
        return self._cache[name]

    def evidence_errors(self, side: str, body: str) -> tuple[list[str], bool]:
        """Errors, and whether the cell declares that candidate free of the defect."""
        bullets = _bullets(body)
        if not bullets:
            return ["is empty"], False
        reference = re.match(r"^`([^`]+)`", bullets[0])
        raw = reference.group(1) if reference else bullets[0]
        if raw.strip().lower().startswith(NOT_MANIFESTED):
            rest = bullets[0][reference.end() :] if reference else raw[len(NOT_MANIFESTED) :]
            if not rest.strip(" \u2014-:"):
                return [f"`{NOT_MANIFESTED}` must say what that candidate does instead"], True
            return [], True
        if reference is None:
            return [f"must open with a reference in backticks or `{NOT_MANIFESTED}`"], False
        candidate = self.declared.get(side)
        if candidate is None:
            return [f"candidate {side} is not declared in `## Inputs`"], False
        return self._reference_errors(raw, candidate), False

    def _reference_errors(self, raw: str, candidate: str) -> list[str]:
        if line_reference := LINE_REFERENCE_PATTERN.match(raw):
            name, start = line_reference.group(1), int(line_reference.group(2))
            end = int(line_reference.group(3)) if line_reference.group(3) else start
            if name != candidate:
                return [f"cites `{name}`, which is not this side's candidate `{candidate}`"]
            lines = self._lines(name)
            if lines is None:
                return [f"cites `{name}`, which does not exist"]
            if not 1 <= start <= end <= len(lines):
                return [f"cites `{raw}`, outside its {len(lines)} lines"]
            return []
        if slice_reference := SLICE_REFERENCE_PATTERN.match(raw):
            return self._slice_errors(
                candidate, int(slice_reference.group(1)), slice_reference.group(2)
            )
        return [f"`{raw}` is neither `FILE.md:NN` nor `slice N <field>`"]

    def _slice_errors(self, candidate: str, number: int, field_name: str) -> list[str]:
        lines = self._lines(candidate)
        if lines is None:
            return [f"candidate `{candidate}` does not exist"]
        text = "\n".join(lines)
        headings = list(SLICE_HEADING_PATTERN.finditer(text))
        for index, heading in enumerate(headings):
            if int(heading.group(1)) != number:
                continue
            end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
            wanted = field_name.strip("` ").lower()
            if any(
                match.group(1).strip().lower() == wanted
                for match in FIELD_PATTERN.finditer(text[heading.end() : end])
            ):
                return []
            return [f"slice {number} of `{candidate}` has no `{field_name}` field"]
        return [f"`{candidate}` has no slice {number}"]


class Coverage:
    """The skill's clauses and the ledger rows over them: what a declared clause is checked against."""

    def __init__(self, clauses: Sequence[Clause], ledger_rows: Iterable[str]) -> None:
        self.clauses = tuple(clauses)
        self.sections = _sections(self.clauses)
        self.ledger_rows = frozenset(ledger_rows)

    def clause_errors(self, body: str) -> tuple[list[str], bool]:
        """Errors, and whether the entry names a clause at all."""
        labelled = _labelled(body)
        missing = [label for label in ("Clause", "Covering rows") if label not in labelled]
        if missing:
            return [f"missing sub-field {', '.join(missing)}"], False

        clause, rows = labelled["Clause"], labelled["Covering rows"]
        if clause.strip().strip("`").lower() == NONE:
            if rows.strip().strip("`").lower() != NONE:
                return ["`Clause: none` requires `Covering rows: none`"], False
            return [], False

        site = SITE_PATTERN.search(clause)
        if site is None:
            return ["`Clause` must name a site as `SKILL.md:NN` or `SKILL.md:NN-MM`"], True
        start = int(site.group(1))
        end = int(site.group(2)) if site.group(2) else start
        covering = [record for record in self.clauses if record.covers(start, end)]
        if not covering:
            return [f"`SKILL.md:{start}-{end}` holds no normative clause"], True
        # A site copied verbatim from the index names the clause whose span it is: answering for
        # everything that span overlaps would demand the rows of its neighbours, and one line of
        # `SKILL.md` often carries two clauses. Only a span that matches none falls back to overlap.
        covering = [record for record in covering if (start, end) in record.spans] or covering

        errors = self._section_errors(clause, covering)
        errors.extend(self._row_errors(rows, covering))
        return errors, True

    def _section_errors(self, clause: str, covering: Sequence[Clause]) -> list[str]:
        quoted = SECTION_QUOTE_PATTERN.search(clause)
        if quoted is None:
            return ["`Clause` must name its section as \u00a7 `section title`"]
        declared = _comparable(quoted.group(1))
        expected = {_comparable(record.section) for record in covering}
        if declared not in expected:
            return [
                f"names section `{quoted.group(1)}`, but that site is in "
                + " or ".join(sorted(self.sections[name] for name in expected))
            ]
        return []

    def _row_errors(self, rows: str, covering: Sequence[Clause]) -> list[str]:
        expected = {row for record in covering for row in record.rows}
        declared = set(ROW_PATTERN.findall(rows))
        says_uncovered = rows.strip().strip("`").lower() == UNCOVERED
        if not declared and not says_uncovered:
            return [f"must list covering rows or state `{UNCOVERED}`"]
        unknown = sorted(declared - self.ledger_rows)
        if unknown:
            return [f"names rows the ledger does not hold: {', '.join(unknown)}"]
        sites = ", ".join(record.id for record in covering)
        if says_uncovered and expected:
            return [
                f"declares `{UNCOVERED}`, but the map covers {sites} "
                f"with {', '.join(sorted(expected))}"
            ]
        if declared != expected:
            return [
                f"declares {', '.join(sorted(declared)) or UNCOVERED}, but the map covers {sites} "
                f"with {', '.join(sorted(expected)) or UNCOVERED}"
            ]
        return []

    def change_errors(self, body: str) -> list[str]:
        labelled = _labelled(body)
        missing = [label for label in ("Section", "Change") if label not in labelled]
        if missing:
            return [f"missing sub-field {', '.join(missing)}"]
        errors: list[str] = []
        if _comparable(labelled["Section"]) not in self.sections:
            errors.append(f"`{labelled['Section']}` is not a section of `SKILL.md`")
        if not labelled["Change"].strip():
            errors.append("`Change` is empty")
        return errors


RULE_FIELD = "Existing rule that failed to prevent the defect"


class Contract:
    """One entry against the contract: what is present, what resolves, what the remedy implies."""

    def __init__(self, candidates: Candidates, coverage: Coverage) -> None:
        self.candidates = candidates
        self.coverage = coverage

    def entry_discards(self, entry: Entry) -> list[Discard]:
        def discard(field_name: str, reasons: Iterable[str]) -> list[Discard]:
            return [Discard(entry.number, entry.title, field_name, reason) for reason in reasons]

        discards = self._declaration_discards(entry, discard)
        if discards:
            return discards

        discards.extend(self._evidence_discards(entry, discard))
        clause_errors, names_clause = self.coverage.clause_errors(entry.fields[RULE_FIELD])
        discards.extend(discard(RULE_FIELD, clause_errors))

        remedy = entry.fields["Remedy"].strip().strip("-* `")
        if remedy not in REMEDIES:
            discards.extend(discard("Remedy", [f"must be one of {', '.join(REMEDIES)}"]))
        discards.extend(
            discard("Change to the skill", self.coverage.change_errors(entry.fields["Change to the skill"]))
        )
        discards.extend(discard("Binary test", _claim_errors(entry.fields["Binary test"])))
        discards.extend(self._conditional_discards(entry, remedy, names_clause, discard))
        return discards

    @staticmethod
    def _declaration_discards(entry: Entry, discard) -> list[Discard]:
        discards: list[Discard] = []
        for name in REQUIRED_FIELDS:
            if name not in entry.fields:
                discards.extend(discard(name, ["missing required field"]))
            elif not entry.fields[name].strip():
                discards.extend(discard(name, ["is empty"]))
        duplicates = sorted({name for name in entry.declared if entry.declared.count(name) > 1})
        return discards + [
            item for name in duplicates for item in discard(name, ["declared more than once"])
        ]

    def _evidence_discards(self, entry: Entry, discard) -> list[Discard]:
        discards: list[Discard] = []
        absent_sides = 0
        for side in ("A", "B"):
            name = f"Evidence \u2014 candidate {side}"
            errors, absent = self.candidates.evidence_errors(side, entry.fields[name])
            discards.extend(discard(name, errors))
            absent_sides += absent
        if absent_sides == 2:
            discards.extend(
                discard(
                    "Evidence \u2014 candidate A",
                    ["neither candidate manifests the defect, so this cycle did not observe it"],
                )
            )
        return discards

    def _conditional_discards(self, entry: Entry, remedy: str, names_clause: bool, discard) -> list[Discard]:
        discards: list[Discard] = []
        merged, reformulation = CONDITIONAL_FIELDS

        if remedy == "reach-change":
            if merged not in entry.fields:
                discards.extend(discard(merged, ["required when the remedy changes a rule's reach"]))
            else:
                discards.extend(discard(merged, _claim_errors(entry.fields[merged])))
                covering = _labelled(entry.fields[RULE_FIELD]).get("Covering rows", "")
                if not ROW_PATTERN.search(covering):
                    discards.extend(
                        discard(merged, ["a merge that names no absorbed row is not verifiable"])
                    )
        elif merged in entry.fields:
            discards.extend(discard(merged, [f"forbidden when the remedy is `{remedy}`"]))

        if remedy == "addition" and names_clause:
            if reformulation not in entry.fields:
                discards.extend(
                    discard(reformulation, ["required when an entry adds rules next to a named clause"])
                )
            else:
                labelled = _labelled(entry.fields[reformulation])
                for label in ("Reformulation attempted", "Discarded because"):
                    if not labelled.get(label, "").strip():
                        discards.extend(discard(reformulation, [f"missing sub-field {label}"]))
        elif reformulation in entry.fields:
            discards.extend(
                discard(reformulation, ["forbidden: this entry does not add rules next to a named clause"])
            )
        return discards


def validate(
    document: str,
    text: str,
    clauses: Sequence[Clause],
    ledger_rows: Iterable[str],
    plans_dir: Path,
) -> Result:
    candidates, entries, document_errors = parse_entries(text)
    result = Result(document, len(entries), document_errors=document_errors)
    contract = Contract(Candidates(candidates, plans_dir), Coverage(clauses, ledger_rows))
    for entry in entries:
        discards = contract.entry_discards(entry)
        if discards:
            result.discards.extend(discards)
        else:
            result.conforming.append(entry.number)
    return result


def render(result: Result) -> str:
    discarded = sorted({discard.entry for discard in result.discards})
    lines = [
        result.document,
        f"entries      {result.entries:>3}",
        f"conforming   {len(result.conforming):>3}",
        f"discarded    {len(discarded):>3}",
    ]
    for error in result.document_errors:
        lines.append(f"\nDOCUMENT: {error}")
    for number in discarded:
        reasons = [discard for discard in result.discards if discard.entry == number]
        lines.append(f"\nDISCARD {number}. {reasons[0].title}")
        lines.extend(f"  {discard.field}: {discard.reason}" for discard in reasons)
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    here = Path(__file__).resolve()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("document", type=Path)
    parser.add_argument("--map", type=Path, default=here.parents[2] / "support/clause-row-map.tsv")
    parser.add_argument("--ledger", type=Path, default=here.parents[2] / "REGRESSION-LEDGER.md")
    parser.add_argument(
        "--plans-dir",
        type=Path,
        help="where the cited candidates live; defaults to the document's own directory",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        result = validate(
            args.document.name,
            args.document.read_text(encoding="utf-8"),
            load_clauses(args.map.read_text(encoding="utf-8")),
            LEDGER_ROW_PATTERN.findall(args.ledger.read_text(encoding="utf-8")),
            args.plans_dir or args.document.parent,
        )
    except OSError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    if args.json:
        print(
            json.dumps(
                {
                    "document": result.document,
                    "entries": result.entries,
                    "conforming": result.conforming,
                    "document_errors": result.document_errors,
                    "discards": [vars(discard) for discard in result.discards],
                },
                indent=2,
                ensure_ascii=False,
            )
        )
    else:
        print(render(result))
    # Discarded entries are a result, not a failure: a side at zero conforming entries does not
    # block the cycle. Only a document that cannot be read as a set of entries is an error.
    return 1 if result.document_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
