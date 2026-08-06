#!/usr/bin/env python3
"""Emit the machine-readable records of the clause → ledger row map.

`support/CLAUSE-ROW-MAP.md` mixes records with prose. `validate_improvement.py` needs only the
records, so this script writes them to `support/clause-row-map.tsv` and leaves counting rule,
unresolved anchors, sample verification and blame divergences in the Markdown, where no script
reads them.

What git can answer, and what it cannot:

- **`sites`** are regenerated: every span is checked against `SKILL.md` at `HEAD`, and a span that
  runs past the end of the file stops the extraction instead of being emitted.
- **`site_last`** is computed: the newest commit whose parent does not contain the span's
  whitespace-normalized text. It is what `git blame` reports, one clause at a time.
- **`last`** — the commit that last changed the clause's *wording* — is **not** computable at this
  granularity and is carried from the map. A clause is a normative sentence and a line often carries
  two of them: `SKILL.md:43` holds both `C-013` and the opening of `C-014`, so any span-based
  derivation attributes `C-014`'s rewrite to `C-013`. That is the failure the map records as its
  sixteen blame divergences, and a re-anchoring deduced from it would reset `×k` on rows nobody
  touched.

So `last` is verified instead of regenerated: a clause's wording cannot have changed *after* the
last change to the text around it, so `last` must be `site_last` or older. The check is mechanical
and catches a hand-written cell that claims a rewrite which never happened at that site.

**`in`** is not derivable either — it names the commit that introduced the *obligation*, which
survives a later reformulation — and neither is `anchoring`, which is the map's own inference.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

SKILL_PATH = "skills/plan-slices/SKILL.md"
SECTION_PATTERN = re.compile(r"^### (.+?) — `SKILL\.md:(\d+)-(\d+)`\s*$")
COMMIT_PATTERN = re.compile(r"\b([0-9a-f]{7,40})\b")
ROW_PATTERN = re.compile(r"\bR-\d{3}\b")
COLUMNS = ("id", "sites", "section", "clause", "rows", "anchoring", "in", "last", "site_last")
UNRESOLVED = "unresolved"


@dataclass(frozen=True)
class Record:
    id: str
    spans: tuple[tuple[int, int], ...]
    section: str
    clause: str
    rows: tuple[str, ...]
    anchoring: str
    introduced_in: str
    last: str


def _run(args: Sequence[str], repo: Path) -> str:
    result = subprocess.run(
        args, cwd=repo, capture_output=True, text=True, check=False, encoding="utf-8"
    )
    if result.returncode != 0:
        raise RuntimeError(f"{' '.join(args)}: {result.stderr.strip()}")
    return result.stdout


def _split_table_row(line: str) -> list[str] | None:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return None
    return [cell.strip() for cell in stripped.strip("|").split("|")]


def _parse_sites(cell: str) -> tuple[tuple[int, int], ...] | None:
    """A site cell holds one or more `SKILL.md:NN[-MM]` spans; two clauses are stated twice."""
    spans: list[tuple[int, int]] = []
    for part in cell.split(","):
        match = re.fullmatch(r"`SKILL\.md:(\d+)(?:-(\d+))?`", part.strip())
        if match is None:
            return None
        start = int(match.group(1))
        spans.append((start, int(match.group(2)) if match.group(2) else start))
    return tuple(spans)


def parse_map(text: str) -> list[Record]:
    records: list[Record] = []
    section = ""
    in_map = False
    for line in text.splitlines():
        if line.startswith("## "):
            in_map = line.strip() == "## The map"
            continue
        if not in_map:
            continue
        if header := SECTION_PATTERN.match(line):
            section = header.group(1)
            continue
        cells = _split_table_row(line)
        if cells is None or len(cells) != 7 or not re.fullmatch(r"C-\d+", cells[0]):
            continue
        spans = _parse_sites(cells[1])
        if spans is None:
            raise ValueError(f"{cells[0]}: unparseable site {cells[1]!r}")
        introduced = COMMIT_PATTERN.search(cells[3])
        rewritten = COMMIT_PATTERN.search(cells[4])
        if introduced is None or rewritten is None:
            raise ValueError(f"{cells[0]}: `In` and `Last` must each name a commit")
        records.append(
            Record(
                cells[0],
                spans,
                section,
                cells[2],
                tuple(dict.fromkeys(ROW_PATTERN.findall(cells[5]))),
                cells[6],
                introduced.group(1),
                rewritten.group(1),
            )
        )
    return records


def _normalize(text: str) -> str:
    return " ".join(text.split())


def _content_at(repo: Path, commit: str | None) -> str:
    if commit is None:
        return ""
    try:
        return _normalize(_run(["git", "show", f"{commit}:{SKILL_PATH}"], repo))
    except RuntimeError:
        return ""


def _parent_of(repo: Path, commit: str) -> str | None:
    parents = _run(["git", "rev-parse", f"{commit}^@"], repo).split()
    return parents[0] if parents else None


class History:
    """The commits that touched `SKILL.md`, newest first, with their normalized contents."""

    def __init__(self, repo: Path) -> None:
        self.commits = _run(["git", "log", "--format=%H", "--", SKILL_PATH], repo).split()
        self.short = {commit: commit[:7] for commit in self.commits}
        self._content = {commit: _content_at(repo, commit) for commit in self.commits}
        self._parent_content = {
            commit: _content_at(repo, _parent_of(repo, commit)) for commit in self.commits
        }
        self._age = {commit[:7]: index for index, commit in enumerate(self.commits)}

    def introducing(self, text: str) -> str | None:
        """The newest commit that made `text` appear; None when no revision ever held it."""
        for commit in self.commits:
            if text in self._content[commit] and text not in self._parent_content[commit]:
                return self.short[commit]
        return None

    def age(self, short_commit: str) -> int | None:
        """Distance from `HEAD` in this file's history; larger is older."""
        return self._age.get(short_commit)


def site_commits(history: History, records: Sequence[Record], skill_lines: Sequence[str]) -> dict[str, str]:
    resolved: dict[str, str] = {}
    for record in records:
        found = [
            commit
            for commit in (
                history.introducing(_normalize("\n".join(skill_lines[start - 1 : end])))
                for start, end in record.spans
            )
            if commit is not None
        ]
        if len(found) == len(record.spans):
            resolved[record.id] = min(found, key=lambda commit: history.age(commit) or 0)
    return resolved


def wording_errors(history: History, records: Sequence[Record], site_last: dict[str, str]) -> list[str]:
    errors: list[str] = []
    for record in records:
        computed = site_last.get(record.id)
        if computed is None:
            continue
        declared_age, computed_age = history.age(record.last), history.age(computed)
        if declared_age is None:
            errors.append(f"{record.id}: `Last` commit {record.last} never touched {SKILL_PATH}")
        elif declared_age < computed_age:
            errors.append(
                f"{record.id}: `Last` is {record.last}, newer than the last change to its site "
                f"({computed}); a clause cannot be rewritten after the text around it"
            )
    return errors


def emit(records: Sequence[Record], site_last: dict[str, str]) -> str:
    lines = ["\t".join(COLUMNS)]
    for record in records:
        lines.append(
            "\t".join(
                (
                    record.id,
                    ",".join(f"{start}-{end}" for start, end in record.spans),
                    record.section,
                    record.clause,
                    ",".join(record.rows),
                    record.anchoring,
                    record.introduced_in,
                    record.last,
                    site_last.get(record.id, UNRESOLVED),
                )
            )
        )
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    here = Path(__file__).resolve()
    parser = argparse.ArgumentParser(description="Emit support/clause-row-map.tsv.")
    parser.add_argument("--repo", type=Path, default=here.parents[4])
    parser.add_argument("--map", type=Path, default=here.parents[2] / "support/CLAUSE-ROW-MAP.md")
    parser.add_argument("--output", type=Path, default=here.parents[2] / "support/clause-row-map.tsv")
    args = parser.parse_args(argv)

    records = parse_map(args.map.read_text(encoding="utf-8"))
    skill_lines = (args.repo / SKILL_PATH).read_text(encoding="utf-8").splitlines()

    overrun = [
        record.id for record in records if any(end > len(skill_lines) for _, end in record.spans)
    ]
    if overrun:
        print(f"ERROR: sites past the end of SKILL.md: {', '.join(overrun)}", file=sys.stderr)
        return 1

    history = History(args.repo)
    site_last = site_commits(history, records, skill_lines)
    errors = wording_errors(history, records, site_last)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    args.output.write_text(emit(records, site_last), encoding="utf-8")
    unresolved = [record.id for record in records if record.id not in site_last]
    if unresolved:
        print(
            f"WARNING: no revision ever held the exact site text of {', '.join(unresolved)}; "
            "`site_last` is unresolved and `last` is unverified there",
            file=sys.stderr,
        )
    print(f"OK: {len(records)} clauses → {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
