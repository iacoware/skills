#!/usr/bin/env python3
"""Validate only the published structure of a delivery plan."""

from __future__ import annotations

import argparse
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
FIRST_VALIDATION_PATTERN = re.compile(
    r"^(?:NOW\s+)?(?:slice\s+)?(\d+)(?:[.)]\s+\S.*)?$", re.IGNORECASE
)


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
class Theme:
    name: str
    desired_outcome: str
    first_validation: str


@dataclass(frozen=True)
class Plan:
    text: str
    sections: dict[str, Section]
    slices: tuple[Slice, ...]
    themes: tuple[str, ...]
    theme_rows: tuple[Theme, ...]


def _parse_sections(text: str) -> dict[str, Section]:
    matches = list(H2_PATTERN.finditer(text))
    sections: dict[str, Section] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        name = match.group(1)
        sections[name] = Section(name, text[match.end() : end], match.start())
    return sections


def _parse_slices(now_body: str) -> tuple[Slice, ...]:
    matches = list(H3_PATTERN.finditer(now_body))
    return tuple(
        Slice(
            int(match.group(1)),
            match.group(2),
            now_body[
                match.end() : matches[index + 1].start()
                if index + 1 < len(matches)
                else len(now_body)
            ],
        )
        for index, match in enumerate(matches)
    )


def _parse_themes(themes_body: str) -> tuple[Theme, ...]:
    rows: list[Theme] = []
    for line in themes_body.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 3 or cells[0].lower() == "theme":
            continue
        if all(re.fullmatch(r":?-+:?", cell) for cell in cells):
            continue
        rows.append(Theme(cells[0], cells[1], cells[2]))
    return tuple(rows)


def parse_plan(text: str) -> Plan:
    sections = _parse_sections(text)
    now = sections.get("NOW")
    themes = sections.get("Themes")
    theme_rows = _parse_themes(themes.body) if themes else ()
    return Plan(
        text,
        sections,
        _parse_slices(now.body) if now else (),
        tuple(theme.name for theme in theme_rows),
        theme_rows,
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
        if in_fence or LIST_ITEM_PATTERN.match(line) or CONTINUATION_PATTERN.match(line):
            continue
        errors.append(
            f"{section.name}: line {line_number} must be a list item or an indented continuation"
        )
    return errors


def _field_errors(slice_: Slice) -> list[str]:
    errors: list[str] = []
    matches = list(FIELD_PATTERN.finditer(slice_.body))
    fields = [match.group(1).strip() for match in matches]
    for required in REQUIRED_SLICE_FIELDS:
        count = fields.count(required)
        if count != 1:
            errors.append(f"NOW slice {slice_.number}: expected one '{required}' field, found {count}")
    if fields.count("Learning / risk") > 1:
        errors.append(f"NOW slice {slice_.number}: 'Learning / risk' is declared more than once")
    for legacy in LEGACY_SLICE_FIELDS:
        if legacy in fields:
            errors.append(f"NOW slice {slice_.number}: legacy field is forbidden: {legacy}")

    preamble = slice_.body[: matches[0].start()] if matches else slice_.body
    preamble_lines = [line.strip() for line in preamble.splitlines() if line.strip()]
    if preamble_lines[:1] != [SLICE_RULE]:
        errors.append(f"NOW slice {slice_.number}: title must be followed by a '{SLICE_RULE}' rule")
    elif preamble_lines[1:]:
        errors.append(f"NOW slice {slice_.number}: only the '{SLICE_RULE}' rule may precede the fields")

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

    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(slice_.body)
        field = fields[index]
        nonblank = [line for line in slice_.body[match.end() : end].splitlines() if line.strip()]
        if not nonblank:
            errors.append(f"NOW slice {slice_.number}: '{field}' is empty")
        elif not any(LIST_ITEM_PATTERN.match(line) for line in nonblank):
            errors.append(f"NOW slice {slice_.number}: '{field}' must contain a list")
        elif any(
            not (LIST_ITEM_PATTERN.match(line) or CONTINUATION_PATTERN.match(line))
            for line in nonblank
        ):
            errors.append(f"NOW slice {slice_.number}: '{field}' contains prose outside a list")
    return errors


def _theme_reference_errors(plan: Plan) -> list[str]:
    errors: list[str] = []
    slice_numbers = {slice_.number for slice_ in plan.slices}
    for theme in plan.theme_rows:
        match = FIRST_VALIDATION_PATTERN.fullmatch(theme.first_validation.strip())
        if match is None:
            errors.append(
                f"Themes: first validation for '{theme.name}' must start with a NOW slice number"
            )
        elif int(match.group(1)) not in slice_numbers:
            errors.append(
                f"Themes: first validation for '{theme.name}' references missing NOW slice "
                f"{match.group(1)}"
            )
    return errors


def validate_structure(plan: Plan) -> list[str]:
    errors: list[str] = []
    if not re.search(r"^# (?!#)\S", plan.text, re.MULTILINE):
        errors.append("missing H1 title")
    missing = [name for name in REQUIRED_H2 if name not in plan.sections]
    errors.extend(f"missing required section: {name}" for name in missing)
    positions = [plan.sections[name].position for name in REQUIRED_H2 if name in plan.sections]
    if positions != sorted(positions):
        errors.append("required sections are not in template order")
    for legacy in LEGACY_H2:
        if legacy in plan.sections:
            errors.append(f"legacy section is forbidden: {legacy}")
    for name in LIST_ONLY_H2:
        if section := plan.sections.get(name):
            errors.extend(_list_only_errors(section))

    if themes := plan.sections.get("Themes"):
        if "| Theme | Desired outcome | First validation |" not in themes.body:
            errors.append("Themes: expected columns Theme, Desired outcome, First validation")
        if not plan.themes:
            errors.append("Themes: expected at least one data row")
        errors.extend(_theme_reference_errors(plan))

    if not plan.slices:
        errors.append("NOW: expected at least one numbered H3 slice")
    else:
        numbers = [slice_.number for slice_ in plan.slices]
        if numbers != list(range(numbers[0], numbers[0] + len(numbers))) or numbers[0] not in (0, 1):
            errors.append("NOW: slice numbers must be contiguous and start at 0 or 1")

    release_numbers: list[int] = []
    for slice_ in plan.slices:
        if not re.search(
            r"\*\((?:(?:Theme|Enabler):\s*[^)]+|Release:\s*delivery)\)\*", slice_.title
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
        if section := plan.sections.get(horizon):
            if not any(LIST_ITEM_PATTERN.match(line) for line in section.body.splitlines()):
                errors.append(f"{horizon}: expected a list or '- None identified.'")
    return errors


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    args = parser.parse_args(argv)
    try:
        errors = validate_structure(parse_plan(args.plan.read_text(encoding="utf-8")))
    except OSError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK: {args.plan}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
