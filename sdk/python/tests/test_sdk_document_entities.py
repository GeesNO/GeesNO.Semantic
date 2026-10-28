from __future__ import annotations

import re
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[3]
SDK_ROOT = ROOT / "sdk" / "python"
if str(SDK_ROOT) not in sys.path:
    sys.path.insert(0, str(SDK_ROOT))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from conformance.runner.fixture_runner import run_suite  # noqa: E402
from conformance.runner.raw_parse import RawNumber  # noqa: E402
from geesno_semantic import (  # noqa: E402
    Concept,
    Representation,
    SemanticDocument,
    dump_bytes,
    load_bytes,
    load_path,
    new_uuid_urn,
    validate_document,
)


DOCUMENT_ID = "urn:uuid:10000000-0000-4000-8000-000000000001"
CONCEPT_ID = "urn:uuid:10000000-0000-4000-8000-000000000002"
REPRESENTATION_ID = "urn:uuid:10000000-0000-4000-8000-000000000003"


def new_document() -> SemanticDocument:
    return SemanticDocument.create(
        spec_version="0.1.0",
        identifier=DOCUMENT_ID,
        scope={"completeness": "partial"},
    )


class SdkDocumentEntityTests(unittest.TestCase):
    def test_minimal_document_builder_validates_and_round_trips(self) -> None:
        scope = {"completeness": "partial"}
        document = SemanticDocument.create(
            spec_version="0.1.0",
            identifier=DOCUMENT_ID,
            scope=scope,
        )

        self.assertEqual(
            document.backing_tree,
            {
                "spec_version": "0.1.0",
                "id": DOCUMENT_ID,
                "scope": {"completeness": "partial"},
            },
        )
        self.assertIsNot(document["scope"], scope)
        scope["completeness"] = "unknown"
        self.assertEqual(document["scope"]["completeness"], "partial")
        self.assertEqual(validate_document(document), {"result": "valid"})

        reloaded = load_bytes(dump_bytes(document))
        self.assertEqual(reloaded.backing_tree, document.backing_tree)

    def test_concept_builder_uses_only_canonical_entity_placement(self) -> None:
        document = new_document()
        concept = document.add_concept(identifier=CONCEPT_ID)

        self.assertIsInstance(concept, Concept)
        self.assertEqual((concept.identifier, concept.kind), (CONCEPT_ID, "concept"))
        self.assertEqual(document.backing_tree["entities"], [concept.backing_record])
        self.assertNotIn("concepts", document.backing_tree)
        self.assertEqual(validate_document(document), {"result": "valid"})

    def test_representation_builder_uses_only_canonical_entity_placement(self) -> None:
        document = new_document()
        representation = document.add_representation(identifier=REPRESENTATION_ID)

        self.assertIsInstance(representation, Representation)
        self.assertEqual(
            (representation.identifier, representation.kind),
            (REPRESENTATION_ID, "representation"),
        )
        self.assertNotIn("representations", document.backing_tree)
        self.assertEqual(validate_document(document), {"result": "valid"})

    def test_concept_and_representation_remain_independent(self) -> None:
        document = new_document()
        document.add_concept(identifier=CONCEPT_ID)
        document.add_representation(identifier=REPRESENTATION_ID)

        self.assertNotIn("assertions", document.backing_tree)
        self.assertEqual(len(document.concepts), 1)
        self.assertEqual(len(document.representations), 1)
        self.assertEqual(validate_document(document), {"result": "valid"})

    def test_multiple_entities_keep_ids_kinds_order_and_occurrences(self) -> None:
        second_concept = "urn:uuid:10000000-0000-4000-8000-000000000004"
        document = new_document()
        document.add_concept(identifier=CONCEPT_ID)
        document.add_representation(identifier=REPRESENTATION_ID)
        document.add_concept(identifier=second_concept)

        self.assertEqual(
            [(entity.identifier, entity.kind) for entity in document.entities],
            [
                (CONCEPT_ID, "concept"),
                (REPRESENTATION_ID, "representation"),
                (second_concept, "concept"),
            ],
        )
        self.assertEqual(validate_document(document), {"result": "valid"})

    def test_duplicate_id_is_reported_by_existing_layer_three(self) -> None:
        document = new_document()
        document.add_concept(identifier=CONCEPT_ID)
        document.add_representation(identifier=CONCEPT_ID)

        self.assertEqual(len(document.entities), 2)
        self.assertEqual(
            validate_document(document),
            {"result": "invalid", "layer": 3, "category": "duplicate-id"},
        )

    def test_uuid_helper_is_canonical_distinct_and_explicit_only(self) -> None:
        document = new_document()
        self.assertNotIn("entities", document.backing_tree)
        with self.assertRaises(TypeError):
            SemanticDocument.create(  # type: ignore[call-arg]
                spec_version="0.1.0",
                scope={"completeness": "partial"},
            )

        first = new_uuid_urn()
        second = new_uuid_urn()
        pattern = re.compile(
            r"^urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-"
            r"[0-9a-f]{4}-[0-9a-f]{12}$"
        )
        self.assertRegex(first, pattern)
        self.assertRegex(second, pattern)
        self.assertNotEqual(first, second)
        self.assertNotIn("entities", document.backing_tree)

    def test_richer_loaded_document_preserves_unknown_extensions_and_raw_numbers(self) -> None:
        source = ROOT / "conformance" / "valid" / "unknown-extension-numbers.json"
        document = load_path(source)
        extensions = document.backing_tree["extensions"]
        payload = extensions["ext:opaque"]
        numbers = payload["numbers"]
        number_identities = [id(number) for number in numbers]
        tokens = [number.token for number in numbers]

        document.add_concept(identifier=CONCEPT_ID)

        self.assertIs(document.backing_tree["extensions"], extensions)
        self.assertIs(document.backing_tree["extensions"]["ext:opaque"], payload)
        self.assertEqual([id(number) for number in numbers], number_identities)
        self.assertTrue(all(isinstance(number, RawNumber) for number in numbers))
        self.assertEqual([number.token for number in numbers], tokens)
        self.assertEqual(validate_document(document), {"result": "valid"})

        reloaded = load_bytes(dump_bytes(document))
        reloaded_numbers = reloaded["extensions"]["ext:opaque"]["numbers"]
        self.assertEqual([number.token for number in reloaded_numbers], tokens)

    def test_view_creation_is_non_copying_and_does_not_mutate(self) -> None:
        source = ROOT / "conformance" / "valid" / "assertions-and-values.json"
        document = load_path(source)
        before = dump_bytes(document)

        entities = document.entities
        concepts = document.concepts
        representations = document.representations

        self.assertEqual(dump_bytes(document), before)
        self.assertIs(entities[0].backing_record, document.backing_tree["entities"][0])
        self.assertIs(concepts[0].backing_record, entities[0].backing_record)
        self.assertIs(representations[0].backing_record, entities[1].backing_record)

    def test_i2_builders_do_not_create_i3_records(self) -> None:
        document = new_document()
        document.add_concept(identifier=CONCEPT_ID)
        document.add_representation(identifier=REPRESENTATION_ID)

        self.assertNotIn("sources", document.backing_tree)
        self.assertNotIn("bindings", document.backing_tree)
        self.assertNotIn("assertions", document.backing_tree)

    def test_s2_regression_totals_remain_unchanged(self) -> None:
        valid, invalid, expected, errors = run_suite()
        self.assertEqual((valid, invalid, expected), (17, 84, 101))
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
