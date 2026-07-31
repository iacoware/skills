#!/usr/bin/env python3
"""Validate delivery-plan structure and optional scenario expectations."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


REQUIRED_H2 = (
    "Ordering criteria",
    "Themes",
    "Cross-functional concerns",
    "NOW",
    "LATER",
    "OUT-OF-SCOPE",
)
LIST_ONLY_H2 = (
    "Ordering criteria",
    "Cross-functional concerns",
    "LATER",
    "OUT-OF-SCOPE",
    "Decision checkpoints",
    "Non-product work",
    "Open questions",
)
LEGACY_H2 = (
    "Cross-cutting baseline",
    "Recommended order and weak constraints",
    "Hard dependencies",
    "Sequencing notes",
)
REQUIRED_SLICE_FIELDS = ("Includes", "Verification", "Outcome")
STANDARD_SLICE_FIELDS = ("Includes", "Verification", "Learning / risk", "Outcome")
LEGACY_SLICE_FIELDS = ("Why now",)
SLICE_RULE = "---"
H2_PATTERN = re.compile(r"^## (?!#)(.+?)\s*$", re.MULTILINE)
H3_PATTERN = re.compile(r"^### (\d+)\.\s+(.+?)\s*$", re.MULTILINE)
FIELD_PATTERN = re.compile(r"^\*\*([^*]+?)\*\*\s*$", re.MULTILINE)
LIST_ITEM_PATTERN = re.compile(r"^\s*(?:[-+*]|\d+\.)\s+")
CONTINUATION_PATTERN = re.compile(r"^\s{2,}\S")


@dataclass(frozen=True)
class Section:
    name: str
    body: str
    position: int


@dataclass(frozen=True)
class Slice:
    number: int
    title: str
    body: str


@dataclass(frozen=True)
class Plan:
    text: str
    sections: dict[str, Section]
    slices: tuple[Slice, ...]
    themes: tuple[str, ...]


def _parse_sections(text: str) -> dict[str, Section]:
    matches = list(H2_PATTERN.finditer(text))
    sections: dict[str, Section] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        name = match.group(1)
        sections[name] = Section(name=name, body=text[match.end() : end], position=match.start())
    return sections


def _parse_slices(now_body: str) -> tuple[Slice, ...]:
    matches = list(H3_PATTERN.finditer(now_body))
    slices: list[Slice] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(now_body)
        slices.append(
            Slice(
                number=int(match.group(1)),
                title=match.group(2),
                body=now_body[match.end() : end],
            )
        )
    return tuple(slices)


def _parse_themes(themes_body: str) -> tuple[str, ...]:
    rows: list[str] = []
    for line in themes_body.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 3 or cells[0].lower() == "theme":
            continue
        if all(re.fullmatch(r":?-+:?", cell) for cell in cells):
            continue
        rows.append(cells[0])
    return tuple(rows)


def parse_plan(text: str) -> Plan:
    sections = _parse_sections(text)
    now = sections.get("NOW")
    themes = sections.get("Themes")
    return Plan(
        text=text,
        sections=sections,
        slices=_parse_slices(now.body) if now else (),
        themes=_parse_themes(themes.body) if themes else (),
    )


def _list_only_errors(section: Section) -> list[str]:
    errors: list[str] = []
    in_fence = False
    for line_number, line in enumerate(section.body.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if LIST_ITEM_PATTERN.match(line) or CONTINUATION_PATTERN.match(line):
            continue
        errors.append(
            f"{section.name}: line {line_number} must be a list item or an indented continuation"
        )
    return errors


def _preamble_errors(slice_: Slice, preamble: str) -> list[str]:
    lines = [line.strip() for line in preamble.splitlines() if line.strip()]
    if lines[:1] != [SLICE_RULE]:
        return [f"NOW slice {slice_.number}: title must be followed by a '{SLICE_RULE}' rule"]
    if lines[1:]:
        return [f"NOW slice {slice_.number}: only the '{SLICE_RULE}' rule may precede the fields"]
    return []


def _order_errors(slice_: Slice, fields: Sequence[str]) -> list[str]:
    errors: list[str] = []
    standard_positions = [
        STANDARD_SLICE_FIELDS.index(field) for field in fields if field in STANDARD_SLICE_FIELDS
    ]
    if standard_positions != sorted(standard_positions):
        errors.append(
            f"NOW slice {slice_.number}: fields must follow the order "
            f"{', '.join(STANDARD_SLICE_FIELDS)}"
        )

    last_standard = max(
        (index for index, field in enumerate(fields) if field in STANDARD_SLICE_FIELDS),
        default=-1,
    )
    for index, field in enumerate(fields):
        if field not in STANDARD_SLICE_FIELDS and index < last_standard:
            errors.append(
                f"NOW slice {slice_.number}: annotation '{field}' must follow the standard fields"
            )
    return errors


def _field_errors(slice_: Slice) -> list[str]:
    errors: list[str] = []
    matches = list(FIELD_PATTERN.finditer(slice_.body))
    fields = [match.group(1).strip() for match in matches]

    for required in REQUIRED_SLICE_FIELDS:
        count = fields.count(required)
        if count != 1:
            errors.append(
                f"NOW slice {slice_.number}: expected one '{required}' field, found {count}"
            )

    if fields.count("Learning / risk") > 1:
        errors.append(f"NOW slice {slice_.number}: 'Learning / risk' is declared more than once")

    for legacy in LEGACY_SLICE_FIELDS:
        if legacy in fields:
            errors.append(f"NOW slice {slice_.number}: legacy field is forbidden: {legacy}")

    preamble = slice_.body[: matches[0].start()] if matches else slice_.body
    errors.extend(_preamble_errors(slice_, preamble))
    errors.extend(_order_errors(slice_, fields))

    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(slice_.body)
        field = fields[index]
        content = slice_.body[match.end() : end]
        nonblank = [line for line in content.splitlines() if line.strip()]
        if not nonblank:
            errors.append(f"NOW slice {slice_.number}: '{field}' is empty")
            continue
        if not any(LIST_ITEM_PATTERN.match(line) for line in nonblank):
            errors.append(f"NOW slice {slice_.number}: '{field}' must contain a list")
        for line in nonblank:
            if not (LIST_ITEM_PATTERN.match(line) or CONTINUATION_PATTERN.match(line)):
                errors.append(
                    f"NOW slice {slice_.number}: '{field}' contains prose outside a list"
                )
                break

    return errors


def validate_structure(plan: Plan) -> list[str]:
    errors: list[str] = []

    if not re.search(r"^# (?!#)\S", plan.text, re.MULTILINE):
        errors.append("missing H1 title")

    missing = [name for name in REQUIRED_H2 if name not in plan.sections]
    errors.extend(f"missing required section: {name}" for name in missing)

    positions = [
        plan.sections[name].position for name in REQUIRED_H2 if name in plan.sections
    ]
    if positions != sorted(positions):
        errors.append("required sections are not in template order")

    for legacy in LEGACY_H2:
        if legacy in plan.sections:
            errors.append(f"legacy section is forbidden: {legacy}")

    for name in LIST_ONLY_H2:
        section = plan.sections.get(name)
        if section:
            errors.extend(_list_only_errors(section))

    themes = plan.sections.get("Themes")
    if themes:
        if "| Theme | Desired outcome | First validation |" not in themes.body:
            errors.append("Themes: expected columns Theme, Desired outcome, First validation")
        if not plan.themes:
            errors.append("Themes: expected at least one data row")

    if not plan.slices:
        errors.append("NOW: expected at least one numbered H3 slice")
    else:
        numbers = [slice_.number for slice_ in plan.slices]
        expected = list(range(numbers[0], numbers[0] + len(numbers)))
        if numbers not in (expected,) or numbers[0] not in (0, 1):
            errors.append("NOW: slice numbers must be contiguous and start at 0 or 1")

    release_numbers: list[int] = []
    for slice_ in plan.slices:
        if not re.search(
            r"\*\((?:(?:Theme|Enabler):\s*[^)]+|Release:\s*delivery)\)\*",
            slice_.title,
        ):
            errors.append(
                f"NOW slice {slice_.number}: title must declare Theme, Enabler, or Release: delivery"
            )
        if re.search(r"\*\(Release:\s*delivery\)\*", slice_.title):
            release_numbers.append(slice_.number)
        errors.extend(_field_errors(slice_))

    if len(release_numbers) > 1:
        errors.append("NOW: expected at most one Release slice")
    if release_numbers and release_numbers[-1] != plan.slices[-1].number:
        errors.append("NOW: Release slice must be last")

    for horizon in ("LATER", "OUT-OF-SCOPE"):
        section = plan.sections.get(horizon)
        if section and not any(LIST_ITEM_PATTERN.match(line) for line in section.body.splitlines()):
            errors.append(f"{horizon}: expected a list or '- None identified.'")

    return errors


def _require_patterns(label: str, value: str, patterns: Sequence[str]) -> list[str]:
    errors: list[str] = []
    for pattern in patterns:
        if not re.search(pattern, value, re.IGNORECASE | re.MULTILINE):
            errors.append(f"{label}: missing expected pattern /{pattern}/")
    return errors


def _validate_order(titles: Sequence[str], patterns: Sequence[str]) -> list[str]:
    cursor = 0
    errors: list[str] = []
    for pattern in patterns:
        for index in range(cursor, len(titles)):
            if re.search(pattern, titles[index], re.IGNORECASE):
                cursor = index + 1
                break
        else:
            errors.append(f"NOW order: missing /{pattern}/ after position {cursor}")
    return errors


def _validate_adjacencies(titles: Sequence[str], pairs: Sequence[object]) -> list[str]:
    errors: list[str] = []
    for pair in pairs:
        if not isinstance(pair, list) or len(pair) != 2:
            errors.append("adjacent_now_titles: each entry must contain two patterns")
            continue
        predecessor, successor = (str(pattern) for pattern in pair)
        if any(
            re.search(predecessor, titles[index], re.IGNORECASE)
            and re.search(successor, titles[index + 1], re.IGNORECASE)
            for index in range(len(titles) - 1)
        ):
            continue
        errors.append(f"NOW adjacency: /{predecessor}/ must be followed by /{successor}/")
    return errors


def _validate_slice_rules(slices: Sequence[Slice], rules: Sequence[object]) -> list[str]:
    errors: list[str] = []
    for rule in rules:
        if not isinstance(rule, dict) or not isinstance(rule.get("title"), str):
            errors.append("slice_rules: each entry must contain a title pattern")
            continue
        title_pattern = rule["title"]
        matches = [
            slice_ for slice_ in slices if re.search(title_pattern, slice_.title, re.IGNORECASE)
        ]
        if len(matches) != 1:
            errors.append(f"slice_rules: /{title_pattern}/ matched {len(matches)} NOW slices")
            continue
        slice_ = matches[0]
        value = f"{slice_.title}\n{slice_.body}"
        label = f"NOW slice {slice_.number}"

        required = rule.get("required_patterns", [])
        if isinstance(required, list):
            errors.extend(_require_patterns(label, value, [str(pattern) for pattern in required]))

        forbidden = rule.get("forbidden_patterns", [])
        if isinstance(forbidden, list):
            for pattern in forbidden:
                if re.search(str(pattern), value, re.IGNORECASE | re.MULTILINE):
                    errors.append(f"{label}: forbidden pattern present /{pattern}/")
    return errors


def validate_expectations(plan: Plan, expectations: dict[str, object]) -> list[str]:
    errors: list[str] = []

    theme_count = expectations.get("theme_count")
    if isinstance(theme_count, int) and len(plan.themes) != theme_count:
        errors.append(f"expected {theme_count} themes, found {len(plan.themes)}")

    themes_contain = expectations.get("themes_contain", [])
    if isinstance(themes_contain, list):
        errors.extend(
            _require_patterns("Themes", "\n".join(plan.themes), [str(item) for item in themes_contain])
        )

    now_title_count = expectations.get("now_title_count")
    if isinstance(now_title_count, int) and len(plan.slices) != now_title_count:
        errors.append(f"expected {now_title_count} NOW slices, found {len(plan.slices)}")

    now_order = expectations.get("now_titles_in_order", [])
    if isinstance(now_order, list):
        errors.extend(_validate_order([slice_.title for slice_ in plan.slices], now_order))

    adjacent = expectations.get("adjacent_now_titles", [])
    if isinstance(adjacent, list):
        errors.extend(_validate_adjacencies([slice_.title for slice_ in plan.slices], adjacent))

    slice_rules = expectations.get("slice_rules", [])
    if isinstance(slice_rules, list):
        errors.extend(_validate_slice_rules(plan.slices, slice_rules))

    later = plan.sections.get("LATER")
    later_contains = expectations.get("later_contains", [])
    if isinstance(later_contains, list):
        errors.extend(
            _require_patterns(
                "LATER", later.body if later else "", [str(item) for item in later_contains]
            )
        )

    out_of_scope = plan.sections.get("OUT-OF-SCOPE")
    out_contains = expectations.get("out_of_scope_contains", [])
    if isinstance(out_contains, list):
        errors.extend(
            _require_patterns(
                "OUT-OF-SCOPE",
                out_of_scope.body if out_of_scope else "",
                [str(item) for item in out_contains],
            )
        )

    required_patterns = expectations.get("required_patterns", [])
    if isinstance(required_patterns, list):
        errors.extend(
            _require_patterns("Plan", plan.text, [str(item) for item in required_patterns])
        )

    forbidden_patterns = expectations.get("forbidden_patterns", [])
    if isinstance(forbidden_patterns, list):
        for pattern in forbidden_patterns:
            if re.search(str(pattern), plan.text, re.IGNORECASE | re.MULTILINE):
                errors.append(f"Plan: forbidden pattern present /{pattern}/")

    return errors


def _load_expectations(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("expectations root must be a JSON object")
    return value


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate the deterministic plan structure. Optional JSON expectations support "
            "scenario-specific evals with keys: theme_count, themes_contain, now_title_count, "
            "now_titles_in_order, adjacent_now_titles, slice_rules, later_contains, "
            "out_of_scope_contains, required_patterns, forbidden_patterns."
        )
    )
    parser.add_argument("plan", type=Path)
    parser.add_argument("--expectations", type=Path)
    args = parser.parse_args(argv)

    try:
        plan = parse_plan(args.plan.read_text(encoding="utf-8"))
        errors = validate_structure(plan)
        if args.expectations:
            errors.extend(validate_expectations(plan, _load_expectations(args.expectations)))
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1

    print(f"PASS: {args.plan} ({len(plan.slices)} NOW slices, {len(plan.themes)} themes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
