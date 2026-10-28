from __future__ import annotations

import contextlib
import io
import json
import unittest
from pathlib import Path

from tools.validation import check_repository
from tools.validation import public_preview_examples as examples


ROOT = check_repository.ROOT
EXPECTED_DOMAINS = {
    "engineering",
    "tabular",
    "document",
    "software",
    "product",
    "scientific",
}


def load_documents() -> dict[str, dict[str, object]]:
    return {
        name: json.loads(
            (examples.EXAMPLES / name / "example.json").read_text(encoding="utf-8")
        )
        for name in examples.EXAMPLE_NAMES
    }


def assertions(document: dict[str, object]) -> list[dict[str, object]]:
    value = document.get("assertions", [])
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


class PublicPreviewExampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.documents = load_documents()

    def test_inventory_is_exact_small_and_separate(self) -> None:
        self.assertEqual(7, len(examples.EXAMPLE_NAMES))
        self.assertEqual(EXPECTED_DOMAINS, set(examples.EXAMPLE_NAMES) - {"minimal"})
        self.assertFalse(examples.EXAMPLES.is_relative_to(ROOT / "conformance"))
        self.assertFalse(
            examples.EXAMPLES.is_relative_to(ROOT / "profiles" / "ai-context")
        )
        for name in examples.EXAMPLE_NAMES:
            directory = examples.EXAMPLES / name
            with self.subTest(name=name):
                self.assertEqual(
                    examples.EXAMPLE_FILES,
                    {path.name for path in directory.iterdir() if path.is_file()},
                )
                self.assertLess((directory / "example.json").stat().st_size, 10000)

    def test_readmes_are_non_normative_synthetic_and_portable(self) -> None:
        manifest = (examples.EXAMPLES / "README.md").read_text(encoding="utf-8")
        self.assertIn("NON-NORMATIVE LEARNING EXAMPLES", manifest)
        self.assertIn("project-authored, synthetic and fictional", manifest)
        self.assertIn("learning example\n!= conformance fixture", manifest)
        self.assertIn("0.1.0-preview.1", manifest)
        self.assertIn("release not finalized", manifest)
        self.assertIsNone(check_repository.LOCAL_ABSOLUTE_PATH.search(manifest))
        for name in examples.EXAMPLE_NAMES:
            readme = (examples.EXAMPLES / name / "README.md").read_text(
                encoding="utf-8"
            )
            with self.subTest(name=name):
                for marker in examples.README_MARKERS:
                    self.assertIn(marker, readme)
                self.assertIsNone(check_repository.LOCAL_ABSOLUTE_PATH.search(readme))

    def test_all_documents_pass_existing_s2_layers_zero_through_three(self) -> None:
        results, errors = examples.validate_inventory()
        self.assertEqual(7, len(results))
        self.assertEqual((), errors)

    def test_validation_is_deterministic_and_offline(self) -> None:
        self.assertEqual(examples.validate_inventory(), examples.validate_inventory())
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(0, examples.main())
        self.assertIn("PASS (7 Core documents, offline)", output.getvalue())

    def test_shared_core_mechanics_are_distributed_across_domains(self) -> None:
        all_assertions = {
            name: assertions(document) for name, document in self.documents.items()
        }
        assertion_kinds = {
            item.get("kind") for items in all_assertions.values() for item in items
        }
        self.assertTrue({"type", "property", "relation"}.issubset(assertion_kinds))
        self.assertGreaterEqual(
            sum(any(item.get("kind") == "relation" for item in items) for items in all_assertions.values()),
            2,
        )
        self.assertGreaterEqual(
            sum(any("provenance" in item for item in items) for items in all_assertions.values()),
            2,
        )
        self.assertTrue(any("reviews" in item for item in all_assertions["document"]))
        self.assertTrue(any("confidence" in item for item in all_assertions["scientific"]))
        self.assertIn("revision", self.documents["software"])
        self.assertIn("history", self.documents["software"])
        self.assertIn("extensions", self.documents["product"])

    def test_concept_representation_and_source_identity_remain_distinct(self) -> None:
        product = self.documents["product"]
        concept_links = [
            item for item in assertions(product) if item.get("kind") == "concept_representation"
        ]
        self.assertEqual(2, len(concept_links))
        self.assertEqual(
            1,
            len({item["concept"]["target"] for item in concept_links}),  # type: ignore[index]
        )
        for name in EXPECTED_DOMAINS:
            document = self.documents[name]
            entity_ids = {item["id"] for item in document.get("entities", [])}  # type: ignore[index]
            source_ids = {item["id"] for item in document.get("sources", [])}  # type: ignore[index]
            locator_values = {
                item["locator"]["value"]
                for item in document.get("bindings", [])  # type: ignore[union-attr]
                if "locator" in item
            }
            with self.subTest(name=name):
                self.assertTrue(entity_ids.isdisjoint(source_ids))
                self.assertTrue(entity_ids.isdisjoint(locator_values))

    def test_example_namespaces_are_local_explanatory_identifiers(self) -> None:
        for name, document in self.documents.items():
            namespaces = document.get("namespaces", {})
            if not isinstance(namespaces, dict):
                self.fail(f"{name} namespaces must be an object")
            for iri in namespaces.values():
                with self.subTest(name=name, iri=iri):
                    self.assertIsInstance(iri, str)
                    self.assertTrue(iri.startswith("https://example.invalid/geesno-learning/"))

    def test_no_profile_adapter_sdk_or_runtime_surface_is_introduced(self) -> None:
        script = Path(examples.__file__).read_text(encoding="utf-8")
        self.assertNotIn("sdk/python", script)
        self.assertNotIn("geesno_semantic", script)
        self.assertNotIn("ai_context", script)
        self.assertFalse(any(examples.EXAMPLES.rglob("*.py")))
        self.assertFalse(any(examples.EXAMPLES.rglob("projection.json")))
        self.assertFalse(any("adapter" in path.name.lower() for path in examples.EXAMPLES.rglob("*")))


if __name__ == "__main__":
    unittest.main()
