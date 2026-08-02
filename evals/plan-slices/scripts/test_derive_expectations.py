#!/usr/bin/env python3
"""Tests for derive_expectations.py."""

from __future__ import annotations

import hashlib
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path

from derive_expectations import derive_expectations, main


class DeriveExpectationsTests(unittest.TestCase):
    def test_derives_expectations_and_reference_hash(self) -> None:
        reference_text = """\
# Reference

## Machine-readable expectations

```json
{"schema_version": 1, "theme_count": 2}
```
"""
        with tempfile.TemporaryDirectory() as directory:
            reference = Path(directory) / "REFERENCE-PLAN.md"
            reference.write_text(reference_text, encoding="utf-8")

            derived = json.loads(derive_expectations(reference))

        self.assertEqual(derived["theme_count"], 2)
        self.assertEqual(derived["_meta"]["generated_from"], "REFERENCE-PLAN.md")
        self.assertEqual(
            derived["_meta"]["reference_sha256"],
            hashlib.sha256(reference_text.encode("utf-8")).hexdigest(),
        )

    def test_check_detects_stale_output(self) -> None:
        reference_text = """\
# Reference

## Machine-readable expectations

```json
{"schema_version": 1}
```
"""
        with tempfile.TemporaryDirectory() as directory:
            reference = Path(directory) / "REFERENCE-PLAN.md"
            output = Path(directory) / "expectations.json"
            reference.write_text(reference_text, encoding="utf-8")
            output.write_text("{}\n", encoding="utf-8")

            with redirect_stderr(io.StringIO()):
                exit_code = main([str(reference), str(output), "--check"])

        self.assertEqual(exit_code, 1)

    def test_rejects_missing_machine_readable_block(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            reference = Path(directory) / "REFERENCE-PLAN.md"
            reference.write_text("# Reference\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "missing"):
                derive_expectations(reference)


if __name__ == "__main__":
    unittest.main()
