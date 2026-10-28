from __future__ import annotations

import json
import socket
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[3]
EXAMPLES = ROOT / "examples" / "ai-context"
VALIDATION = ROOT / "tools" / "validation"
RUNNER = ROOT / "conformance" / "runner"
sys.path.insert(0, str(VALIDATION))
sys.path.insert(0, str(RUNNER))

import ai_context_acceptance as acceptance  # noqa: E402
from fixture_runner import validate_bytes  # noqa: E402
from schema_validation import load_schema  # noqa: E402


EXAMPLE_NAMES = (
    "01-small-complete",
    "02-medium-traceable",
    "03-bounded-partial",
    "04-projection-continuation",
    "05-external-dependency",
    "06-unknown-extension",
    "07-bounded-unknown",
)
EXAMPLE_FILES = {"README.md", "source.json", "projection.json"}
README_SECTIONS = (
    "## Purpose",
    "## Source scope",
    "## Selection context",
    "## Projection scope",
    "## Completeness",
    "## Material context decision",
    "## Key distinction",
    "## Files",
    "## Validation",
    "## What this example does NOT mean",
)
TEST_ONLY_KEYS = {
    "expected_result",
    "expected_error",
    "expected_errors",
    "expected_diagnostic",
    "expected_diagnostics",
    "fixture_name",
    "test_metadata",
}


def _load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _walk(value: object):
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def _top_record_ids(document: dict[str, object]) -> set[str]:
    record_ids: set[str] = set()
    for collection in acceptance.RECORD_COLLECTIONS:
        records = document.get(collection, [])
        if not isinstance(records, list):
            continue
        for record in records:
            if isinstance(record, dict) and isinstance(record.get("id"), str):
                record_ids.add(record["id"])
    revision = document.get("revision")
    if isinstance(revision, dict) and isinstance(revision.get("id"), str):
        record_ids.add(revision["id"])
    return record_ids


class AiContextExampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.s2_schema = load_schema(acceptance.S2_SCHEMA_PATH)

    def pairs(self):
        for name in EXAMPLE_NAMES:
            directory = EXAMPLES / name
            yield name, _load(directory / "source.json"), _load(
                directory / "projection.json"
            )

    def validate_examples(self) -> tuple[tuple[str, tuple[str, ...]], ...]:
        results: list[tuple[str, tuple[str, ...]]] = []
        for name, source, projection in self.pairs():
            source_result = validate_bytes(
                (EXAMPLES / name / "source.json").read_bytes(),
                self.s2_schema,
            )
            errors = [] if source_result == {"result": "valid"} else [
                f"source failed S2 validation: {source_result}"
            ]
            errors.extend(acceptance.structural_errors(projection))
            if not errors:
                errors = acceptance.semantic_errors(projection, source)
            results.append((name, tuple(errors)))
        return tuple(results)

    def test_inventory_and_visible_non_normative_labels_are_exact(self) -> None:
        directories = {
            path.name for path in EXAMPLES.iterdir() if path.is_dir()
        }
        self.assertEqual(set(EXAMPLE_NAMES), directories)
        for name in EXAMPLE_NAMES:
            directory = EXAMPLES / name
            with self.subTest(name=name):
                self.assertEqual(
                    EXAMPLE_FILES,
                    {path.name for path in directory.iterdir() if path.is_file()},
                )
                readme = (directory / "README.md").read_text(encoding="utf-8")
                self.assertIn("NON-NORMATIVE ILLUSTRATIVE EXAMPLE", readme)
                for section in README_SECTIONS:
                    self.assertIn(section, readme)

    def test_all_sources_pass_s2_layers_zero_through_three(self) -> None:
        for name in EXAMPLE_NAMES:
            source_path = EXAMPLES / name / "source.json"
            with self.subTest(name=name):
                self.assertEqual(
                    {"result": "valid"},
                    validate_bytes(source_path.read_bytes(), self.s2_schema),
                )

    def test_all_projections_pass_i2_and_i4_checks(self) -> None:
        for name, source, projection in self.pairs():
            with self.subTest(name=name):
                self.assertEqual(acceptance.PROFILE_EDITION, projection["profile_edition"])
                self.assertEqual([], acceptance.structural_errors(projection))
                self.assertEqual([], acceptance.semantic_errors(projection, source))

    def test_illustrative_record_sets_are_explicit_and_consistent(self) -> None:
        for name, source, projection in self.pairs():
            scope = projection["projection_scope"]
            if scope["scope_kind"] != "illustrative-record-set":
                continue
            scope_ids = set(scope["scope_descriptor"]["record_ids"])
            source_ids = _top_record_ids(source)
            carried_ids = _top_record_ids(projection["carried_content"])
            with self.subTest(name=name):
                self.assertTrue(scope_ids)
                self.assertLessEqual(scope_ids, source_ids)
                self.assertLessEqual(carried_ids, scope_ids)
                if projection["projection_completeness"] == "complete":
                    self.assertEqual(scope_ids, carried_ids)

    def test_collection_covers_the_declared_semantic_distinctions(self) -> None:
        artifacts = {
            name: projection for name, _, projection in self.pairs()
        }
        self.assertEqual(
            {"complete", "partial", "unknown"},
            {item["projection_completeness"] for item in artifacts.values()},
        )

        bounded_partial = artifacts["03-bounded-partial"]
        self.assertEqual("partial", bounded_partial["projection_completeness"])
        self.assertTrue(bounded_partial["boundedness"])
        self.assertTrue(bounded_partial["truncation"]["truncation_established"])
        self.assertTrue(bounded_partial["omissions"])

        same_scope = artifacts["04-projection-continuation"]
        self.assertTrue(same_scope["projection_continuations"])
        self.assertNotIn("dependency_continuations", same_scope)

        dependency = artifacts["05-external-dependency"]
        self.assertTrue(dependency["dependency_continuations"])
        self.assertNotIn("projection_continuations", dependency)
        self.assertIn(
            "external",
            {
                item["availability_state"]
                for item in dependency["reference_availability"]
            },
        )

        extension_source = _load(EXAMPLES / "06-unknown-extension" / "source.json")
        extension_projection = artifacts["06-unknown-extension"]
        self.assertEqual(
            extension_source["entities"][0],
            extension_projection["carried_content"]["entities"][0],
        )

        bounded_unknown = artifacts["07-bounded-unknown"]
        self.assertEqual("unknown", bounded_unknown["projection_completeness"])
        self.assertTrue(bounded_unknown["boundedness"])
        self.assertNotIn("truncation", bounded_unknown)
        self.assertNotIn("omissions", bounded_unknown)

    def test_artifacts_contain_no_test_only_metadata(self) -> None:
        for name, source, projection in self.pairs():
            for artifact_name, artifact in (("source", source), ("projection", projection)):
                keys = {
                    key
                    for value in _walk(artifact)
                    if isinstance(value, dict)
                    for key in value
                }
                with self.subTest(name=name, artifact=artifact_name):
                    self.assertTrue(TEST_ONLY_KEYS.isdisjoint(keys))

    def test_validation_is_deterministic_and_offline(self) -> None:
        with (
            patch.object(socket, "socket", side_effect=AssertionError("network access")),
            patch.object(
                socket,
                "create_connection",
                side_effect=AssertionError("network access"),
            ),
        ):
            first = self.validate_examples()
            second = self.validate_examples()
        self.assertEqual(first, second)
        self.assertEqual(
            tuple((name, ()) for name in EXAMPLE_NAMES),
            first,
        )


if __name__ == "__main__":
    unittest.main()
