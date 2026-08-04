#!/usr/bin/env python3
"""Tests for distinct adjudication artifacts."""

from __future__ import annotations

import json
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from adjudicate import main
from test_compare_plans import valid_comparison


class AdjudicateTests(unittest.TestCase):
    def test_writes_distinct_pending_request(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            left = root / "left.PAIRED.json"
            right = root / "right.PAIRED.json"
            output = root / "pair.ADJUDICATION.json"
            left_value = valid_comparison()
            right_value = valid_comparison()
            left_value["axes"][1]["criteria"][0]["confidence"] = "low"
            left.write_text(json.dumps(left_value), encoding="utf-8")
            right.write_text(json.dumps(right_value), encoding="utf-8")

            with redirect_stdout(io.StringIO()):
                exit_code = main(
                    ["--comparison", str(left), "--comparison", str(right), "--output", str(output)]
                )
            artifact = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(exit_code, 0)
        self.assertTrue(artifact["required"])
        self.assertEqual(artifact["status"], "pending-blind-review")
        self.assertEqual(len(artifact["comparison_inputs"]), 2)


if __name__ == "__main__":
    unittest.main()
