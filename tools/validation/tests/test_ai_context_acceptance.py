from __future__ import annotations

import json
import socket
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[3]
VALIDATION = ROOT / "tools" / "validation"
RUNNER = ROOT / "conformance" / "runner"
sys.path.insert(0, str(VALIDATION))
sys.path.insert(0, str(RUNNER))

import ai_context_acceptance as acceptance  # noqa: E402
import check_repository  # noqa: E402
from fixture_runner import validate_bytes  # noqa: E402
from schema_validation import load_schema  # noqa: E402


class AiContextAcceptanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = json.loads(acceptance.SOURCE_PATH.read_text(encoding="utf-8"))

    def test_corpus_inventory_is_exact_and_separate_from_s2(self) -> None:
        self.assertEqual([], acceptance.corpus_inventory_errors())
        self.assertEqual(12, len(acceptance.VALID_FIXTURES))
        self.assertEqual(4, len(acceptance.STRUCTURAL_INVALID_FIXTURES))
        self.assertEqual(18, len(acceptance.SEMANTIC_INVALID_FIXTURES))
        self.assertNotEqual(acceptance.CORPUS.parent, ROOT / "conformance")

    def test_all_valid_projection_fixtures_pass_both_layers(self) -> None:
        for name in acceptance.VALID_FIXTURES:
            artifact = json.loads(
                (acceptance.CORPUS / "valid" / name).read_text(encoding="utf-8")
            )
            with self.subTest(name=name):
                self.assertEqual([], acceptance.structural_errors(artifact))
                self.assertEqual(
                    [],
                    acceptance.semantic_errors(
                        artifact,
                        self.source,
                        fixture_name=name,
                    ),
                )

    def test_invalid_fixtures_fail_the_expected_layer(self) -> None:
        for name in acceptance.STRUCTURAL_INVALID_FIXTURES:
            artifact = json.loads(
                (acceptance.CORPUS / "invalid" / name).read_text(encoding="utf-8")
            )
            with self.subTest(name=name, layer="structural"):
                self.assertNotEqual([], acceptance.structural_errors(artifact))
        for name in acceptance.SEMANTIC_INVALID_FIXTURES:
            artifact = json.loads(
                (acceptance.CORPUS / "invalid" / name).read_text(encoding="utf-8")
            )
            with self.subTest(name=name, layer="semantic"):
                self.assertEqual([], acceptance.structural_errors(artifact))
                self.assertNotEqual(
                    [],
                    acceptance.semantic_errors(
                        artifact,
                        self.source,
                        fixture_name=name,
                    ),
                )

    def test_schema_references_resolve_locally_for_every_valid_artifact(self) -> None:
        for name in acceptance.VALID_FIXTURES:
            artifact = json.loads(
                (acceptance.CORPUS / "valid" / name).read_text(encoding="utf-8")
            )
            with self.subTest(name=name):
                self.assertEqual([], acceptance.structural_errors(artifact))

    def test_profile_artifact_remains_the_exact_approved_edition(self) -> None:
        profile = json.loads(acceptance.PROFILE_PATH.read_text(encoding="utf-8"))
        self.assertEqual([], check_repository.check_ai_context_profile(profile))
        self.assertEqual(acceptance.PROFILE_EDITION, profile["profile_edition"])
        self.assertEqual(9, len(profile["requirements"]))

    def test_source_companions_pass_s2_layers_zero_through_three(self) -> None:
        schema = load_schema(acceptance.S2_SCHEMA_PATH)
        for source_path in sorted((acceptance.CORPUS / "sources").glob("*.json")):
            with self.subTest(name=source_path.name):
                self.assertEqual(
                    {"result": "valid"},
                    validate_bytes(source_path.read_bytes(), schema),
                )

    def test_checker_is_deterministic(self) -> None:
        first = acceptance.run_corpus()
        second = acceptance.run_corpus()
        self.assertEqual(first, second)
        self.assertEqual((), first.errors)
        self.assertEqual((12, 4, 18), (
            first.valid_passed,
            first.structural_invalid_rejected,
            first.semantic_invalid_rejected,
        ))

    def test_checker_requires_no_network(self) -> None:
        with (
            patch.object(socket, "socket", side_effect=AssertionError("network access")),
            patch.object(
                socket,
                "create_connection",
                side_effect=AssertionError("network access"),
            ),
        ):
            result = acceptance.run_corpus()
        self.assertEqual((), result.errors)


if __name__ == "__main__":
    unittest.main()
