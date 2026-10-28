from __future__ import annotations

import copy
import hashlib
import json
import socket
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[3]
VALIDATION = ROOT / "tools" / "validation"
if str(VALIDATION) not in sys.path:
    sys.path.insert(0, str(VALIDATION))

import ai_context_assessment_corpus as corpus  # noqa: E402
import check_repository  # noqa: E402


class AiContextAssessmentCorpusTests(unittest.TestCase):
    def load(self, directory: str, name: str) -> object:
        return json.loads(
            (corpus.CORPUS / directory / name).read_text(encoding="utf-8")
        )

    def test_inventory_is_exact_and_separate_from_s4(self) -> None:
        self.assertEqual([], corpus.corpus_inventory_errors())
        self.assertEqual(12, len(corpus.VALID_FIXTURES))
        self.assertEqual(18, len(corpus.LAYER_A_INVALID_FIXTURES))
        self.assertEqual(1, len(corpus.TEMPORAL_INVALID_FIXTURES))
        self.assertEqual(3, len(corpus.LAYER_B_INVALID_FIXTURES))
        self.assertEqual(
            34,
            len(
                corpus.VALID_FIXTURES
                + corpus.LAYER_A_INVALID_FIXTURES
                + corpus.TEMPORAL_INVALID_FIXTURES
                + corpus.LAYER_B_INVALID_FIXTURES
            ),
        )
        self.assertNotEqual(
            corpus.CORPUS,
            ROOT / "profiles" / "ai-context" / "conformance" / "v0.1",
        )
        self.assertEqual([], list(corpus.CORPUS.rglob("s[0-9][0-9]-*.json")))

    def test_all_valid_fixtures_pass_i4_layers(self) -> None:
        for name in corpus.VALID_FIXTURES:
            artifact = self.load("valid", name)
            with self.subTest(name=name):
                self.assertEqual([], corpus.layer_a_errors(artifact))
                self.assertEqual([], corpus.temporal_errors(artifact))
                self.assertEqual([], corpus.layer_b_errors(artifact))

    def test_invalid_fixtures_fail_at_the_approved_first_layer(self) -> None:
        for name in corpus.LAYER_A_INVALID_FIXTURES:
            with self.subTest(name=name, layer="A"):
                self.assertNotEqual(
                    [], corpus.layer_a_errors(self.load("invalid", name))
                )

        for name in corpus.TEMPORAL_INVALID_FIXTURES:
            artifact = self.load("invalid", name)
            with self.subTest(name=name, layer="S2 Layer 3"):
                self.assertEqual([], corpus.layer_a_errors(artifact))
                self.assertNotEqual([], corpus.temporal_errors(artifact))

        for name in corpus.LAYER_B_INVALID_FIXTURES:
            artifact = self.load("invalid", name)
            with self.subTest(name=name, layer="B"):
                self.assertEqual([], corpus.layer_a_errors(artifact))
                self.assertEqual([], corpus.temporal_errors(artifact))
                self.assertNotEqual([], corpus.layer_b_errors(artifact))

    def test_duplicate_locator_occurrence_uses_the_same_i21_rule(self) -> None:
        artifact = self.load(
            "valid", "v08-stable-profile-artifact-locator.json"
        )
        duplicate = copy.deepcopy(artifact["requirement_results"][0])
        duplicate["outcome"] = "unsupported"
        artifact["requirement_results"].append(duplicate)
        self.assertEqual([], corpus.layer_a_errors(artifact))
        self.assertTrue(
            any("reported 2 times" in error for error in corpus.layer_b_errors(artifact))
        )

    def test_i22_is_local_ambiguity_not_global_identity(self) -> None:
        artifact = self.load(
            "invalid", "i22-ambiguous-local-reference-declaration.json"
        )
        errors = corpus.layer_b_errors(artifact)
        self.assertTrue(any("declared 2 times" in error for error in errors))
        self.assertTrue(all("global" not in error for error in errors))

    def test_runner_is_deterministic_and_offline(self) -> None:
        first = corpus.run_corpus()
        second = corpus.run_corpus()
        self.assertEqual(first, second)
        self.assertEqual((), first.errors)
        self.assertEqual((12, 18, 1, 3), (
            first.valid_passed,
            first.layer_a_rejected,
            first.temporal_rejected,
            first.layer_b_rejected,
        ))
        with (
            patch.object(socket, "socket", side_effect=AssertionError("network access")),
            patch.object(
                socket,
                "create_connection",
                side_effect=AssertionError("network access"),
            ),
        ):
            self.assertEqual((), corpus.run_corpus().errors)

    def test_i2_schema_remains_the_human_approved_artifact(self) -> None:
        self.assertEqual(
            check_repository.S5_I2_SCHEMA_SHA256,
            hashlib.sha256(corpus.SCHEMA_PATH.read_bytes()).hexdigest(),
        )


if __name__ == "__main__":
    unittest.main()
