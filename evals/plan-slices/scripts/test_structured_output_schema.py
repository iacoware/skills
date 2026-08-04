#!/usr/bin/env python3
"""Tests for provider-compatible structured-output schemas."""

from __future__ import annotations

import unittest

from grading_contract import absolute_grade_schema, comparison_schema
from test_grade_plan import RUBRIC


def schema_nodes(value: object) -> list[dict[str, object]]:
    if isinstance(value, dict):
        return [value, *(node for child in value.values() for node in schema_nodes(child))]
    if isinstance(value, list):
        return [node for child in value for node in schema_nodes(child)]
    return []


class StructuredOutputSchemaTests(unittest.TestCase):
    def test_generated_schemas_use_supported_composition_keyword(self) -> None:
        schemas = [absolute_grade_schema(RUBRIC), comparison_schema(RUBRIC)]

        unsupported_nodes = [
            node for schema in schemas for node in schema_nodes(schema) if "oneOf" in node
        ]

        self.assertEqual(unsupported_nodes, [])

    def test_generated_enum_and_const_schemas_declare_types(self) -> None:
        schemas = [absolute_grade_schema(RUBRIC), comparison_schema(RUBRIC)]

        constrained_nodes = [
            node
            for schema in schemas
            for node in schema_nodes(schema)
            if "enum" in node or "const" in node
        ]

        self.assertTrue(constrained_nodes)
        self.assertTrue(all("type" in node for node in constrained_nodes))


if __name__ == "__main__":
    unittest.main()
