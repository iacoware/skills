#!/usr/bin/env python3
"""Derive scenario expectations from a JSON block in a reference plan."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Sequence


EXPECTATIONS_PATTERN = re.compile(
    r"^## Machine-readable expectations[^\n]*\n.*?^```json\s*(\{.*?\})\s*^```",
    re.MULTILINE | re.DOTALL,
)
PREFERRED_ONLY_KEYS = frozenset(
    {"theme_count", "theme_rules", "now_title_count", "now_titles_in_order", "adjacent_now_titles"}
)
REQUIRED_HARD_RULES = {
    "precedence_rules": ("before", "after"),
    "slice_rules": ("title", "required_patterns"),
    "section_rules": ("section", "required_patterns"),
    "horizon_rules": ("pattern", "horizon"),
}


def _validate_hard_expectations(expectations: dict[str, object]) -> None:
    if expectations.get("schema_version") != 1:
        raise ValueError("machine-readable expectations require schema_version 1")
    forbidden = sorted(PREFERRED_ONLY_KEYS & expectations.keys())
    if forbidden:
        raise ValueError(f"preferred-only expectations are forbidden: {forbidden}")
    for field, required_fields in REQUIRED_HARD_RULES.items():
        rules = expectations.get(field)
        if not isinstance(rules, list) or not rules:
            raise ValueError(f"hard constraints require a non-empty {field} list")
        for rule in rules:
            if not isinstance(rule, dict) or any(
                required not in rule for required in required_fields
            ):
                raise ValueError(f"malformed hard constraint in {field}")


def derive_expectations(reference: Path) -> str:
    text = reference.read_text(encoding="utf-8")
    match = EXPECTATIONS_PATTERN.search(text)
    if match is None:
        raise ValueError("missing '## Machine-readable expectations' JSON block")

    expectations = json.loads(match.group(1))
    if not isinstance(expectations, dict):
        raise ValueError("machine-readable expectations must be a JSON object")
    _validate_hard_expectations(expectations)

    generated = {
        "_meta": {
            "generated_from": reference.name,
            "reference_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        },
        **expectations,
    }
    return json.dumps(generated, indent=2, ensure_ascii=False) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate or check expectations.json derived from REFERENCE-PLAN.md."
    )
    parser.add_argument("reference", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)

    try:
        generated = derive_expectations(args.reference)
        if args.check:
            current = args.output.read_text(encoding="utf-8")
            if current != generated:
                print(f"FAIL: {args.output} is stale", file=sys.stderr)
                return 1
            print(f"PASS: {args.output} matches {args.reference}")
            return 0

        args.output.write_text(generated, encoding="utf-8")
        print(f"WROTE: {args.output}")
        return 0
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
