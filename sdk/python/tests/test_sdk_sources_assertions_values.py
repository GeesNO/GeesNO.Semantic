from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import sys
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[3]
SDK_ROOT = ROOT / "sdk" / "python"
if str(SDK_ROOT) not in sys.path:
    sys.path.insert(0, str(SDK_ROOT))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from conformance.runner.fixture_runner import run_suite  # noqa: E402
from conformance.runner.raw_parse import RawNumber  # noqa: E402
import geesno_semantic as sdk  # noqa: E402
from geesno_semantic import (  # noqa: E402
    Binding,
    ConceptRepresentationAssertion,
    PropertyAssertion,
    RelationAssertion,
    SemanticDocument,
    Source,
    TypeAssertion,
    boolean_value,
    condition,
    date_time_value,
    date_value,
    decimal_value,
    descriptor,
    dump_bytes,
    fingerprint,
    integer_value,
    list_value,
    load_bytes,
    load_path,
    quantity_value,
    reference,
    reference_value,
    set_value,
    string_value,
    structured_value,
    validate_document,
)


def identifier(number: int) -> str:
    return f"urn:uuid:20000000-0000-4000-8000-{number:012x}"


def new_document() -> SemanticDocument:
    return SemanticDocument.create(
        spec_version="0.1.0",
        identifier=identifier(1),
        scope={"completeness": "partial"},
        namespaces={"ex": "https://example.invalid/terms/"},
    )


class SdkSourcesAssertionsValuesTests(unittest.TestCase):
    def test_i3_builders_require_every_record_id_explicitly(self) -> None:
        document = new_document()
        subject = reference(target=identifier(2), location="in-document")

        with self.assertRaises(TypeError):
            document.add_source()  # type: ignore[call-arg]
        with self.assertRaises(TypeError):
            document.add_binding(  # type: ignore[call-arg]
                entity=subject,
                source=reference(target=identifier(10), location="in-document"),
            )
        with self.assertRaises(TypeError):
            document.add_type_assertion(  # type: ignore[call-arg]
                subject=subject,
                type_term="ex:asset",
            )

        self.assertNotIn("sources", document.backing_tree)
        self.assertNotIn("bindings", document.backing_tree)
        self.assertNotIn("assertions", document.backing_tree)

    def test_minimal_source_uses_canonical_placement_and_explicit_id(self) -> None:
        document = new_document()
        source = document.add_source(identifier=identifier(10))

        self.assertIsInstance(source, Source)
        self.assertEqual(source.backing_record, {"id": identifier(10)})
        self.assertIs(source.backing_record, document.backing_tree["sources"][0])
        self.assertNotIn("source", document.backing_tree)
        self.assertEqual(validate_document(document), {"result": "valid"})

    def test_source_and_binding_preserve_explicit_descriptors_without_io(self) -> None:
        document = new_document()
        document.add_concept(identifier=identifier(2))
        location = descriptor(kind="ex:path", value="C:/not-opened/source.dat")
        source = document.add_source(
            identifier=identifier(10),
            locations=[location],
            revision=descriptor(kind="ex:edition", value="r1"),
            fingerprints=[fingerprint(algorithm="ex:digest", value="abc")],
        )
        locator = descriptor(
            kind="ex:record",
            value=structured_value(
                datatype="ex:key",
                members={"ex:part": string_value("A")},
            ),
        )

        with mock.patch("pathlib.Path.open", side_effect=AssertionError("file opened")):
            binding = document.add_binding(
                identifier=identifier(11),
                entity=reference(target=identifier(2), location="in-document"),
                source=reference(target=identifier(10), location="in-document"),
                locator=locator,
                method="ex:mapped",
            )

        self.assertIsInstance(binding, Binding)
        self.assertNotEqual(binding.identifier, source.identifier)
        self.assertEqual(binding["entity"]["target"], identifier(2))
        self.assertEqual(binding["source"]["target"], identifier(10))
        self.assertEqual(binding["locator"], locator)
        self.assertIsNot(binding["locator"], locator)
        self.assertNotIn("assertions", document.backing_tree)
        self.assertEqual(validate_document(document), {"result": "valid"})

    def test_reference_helper_does_not_resolve_and_validator_owns_integrity(self) -> None:
        document = new_document()
        document.add_source(identifier=identifier(10))
        unresolved = reference(target=identifier(999), location="in-document")
        source_reference = reference(target=identifier(10), location="in-document")
        document.add_binding(
            identifier=identifier(11),
            entity=unresolved,
            source=source_reference,
        )

        self.assertEqual(unresolved["target"], identifier(999))
        self.assertEqual(
            validate_document(document),
            {"result": "invalid", "layer": 3, "category": "unresolved-reference"},
        )

    def test_type_and_every_accepted_value_shape_validate(self) -> None:
        document = new_document()
        document.add_concept(identifier=identifier(2))
        document.add_representation(identifier=identifier(3))
        subject = reference(target=identifier(2), location="in-document")
        target = reference(target=identifier(3), location="in-document")

        type_assertion = document.add_type_assertion(
            identifier=identifier(20),
            subject=subject,
            type_term="ex:asset",
        )
        values = (
            string_value("text"),
            boolean_value(True),
            integer_value("9007199254740993"),
            decimal_value(coefficient="123", exponent="-2"),
            date_value("2026-10-11"),
            date_time_value("2026-10-11T12:34:56.123Z"),
            reference_value(target),
            quantity_value(magnitude=decimal_value(coefficient="25", exponent="-1"), unit="ex:metre"),
            list_value(["first", "second", "second"]),
            set_value(["red", "blue"]),
            structured_value(
                datatype="ex:record",
                members={"ex:part": integer_value("1")},
            ),
        )
        for offset, value in enumerate(values, start=21):
            assertion = document.add_property_assertion(
                identifier=identifier(offset),
                subject=subject,
                property_term=f"ex:p{offset}",
                value=value,
            )
            self.assertIsInstance(assertion, PropertyAssertion)
            self.assertEqual(assertion["value"], value)
            if isinstance(value, (dict, list)):
                self.assertIsNot(assertion["value"], value)
        document.add_property_assertion(
            identifier=identifier(40),
            subject=subject,
            property_term="ex:unknown",
            condition=condition("unknown"),
        )

        self.assertIsInstance(type_assertion, TypeAssertion)
        self.assertEqual(validate_document(document), {"result": "valid"})
        self.assertTrue(
            all(
                view.backing_record is document.backing_tree["assertions"][index]
                for index, view in enumerate(document.assertions)
            )
        )

    def test_property_builder_requires_one_branch_and_quantity_requires_unit(self) -> None:
        document = new_document()
        document.add_concept(identifier=identifier(2))
        subject = reference(target=identifier(2), location="in-document")

        with self.assertRaises(TypeError):
            document.add_property_assertion(
                identifier=identifier(20),
                subject=subject,
                property_term="ex:p",
            )
        with self.assertRaises(TypeError):
            document.add_property_assertion(
                identifier=identifier(21),
                subject=subject,
                property_term="ex:p",
                value="x",
                condition=condition("unknown"),
            )
        with self.assertRaises(TypeError):
            quantity_value(magnitude=integer_value("1"))  # type: ignore[call-arg]

        self.assertNotIn("assertions", document.backing_tree)

    def test_set_builder_preserves_duplicates_for_s2_validation(self) -> None:
        document = new_document()
        document.add_concept(identifier=identifier(2))
        repeated = set_value([string_value("same"), string_value("same")])
        document.add_property_assertion(
            identifier=identifier(20),
            subject=reference(target=identifier(2), location="in-document"),
            property_term="ex:tags",
            value=repeated,
        )

        self.assertEqual(repeated["items"], ["same", "same"])
        self.assertEqual(
            document.assertions[0]["value"]["items"], ["same", "same"]
        )
        self.assertEqual(
            validate_document(document),
            {"result": "invalid", "layer": 3, "category": "set-duplicate"},
        )

    def test_relation_is_directed_and_does_not_create_an_inverse(self) -> None:
        document = new_document()
        document.add_concept(identifier=identifier(2))
        document.add_representation(identifier=identifier(3))
        relation = document.add_relation_assertion(
            identifier=identifier(20),
            subject=reference(target=identifier(2), location="in-document"),
            predicate="ex:related",
            object_reference=reference(
                target=identifier(3), location="in-document"
            ),
        )

        self.assertIsInstance(relation, RelationAssertion)
        self.assertEqual(len(document.assertions), 1)
        self.assertEqual(document.assertions[0]["object"]["target"], identifier(3))
        self.assertEqual(validate_document(document), {"result": "valid"})

    def test_concept_representation_is_only_created_explicitly(self) -> None:
        document = new_document()
        document.add_concept(identifier=identifier(2))
        document.add_representation(identifier=identifier(3))
        self.assertNotIn("assertions", document.backing_tree)

        association = document.add_concept_representation_assertion(
            identifier=identifier(20),
            representation=reference(
                target=identifier(3), location="in-document"
            ),
            concept=reference(target=identifier(2), location="in-document"),
        )

        self.assertIsInstance(association, ConceptRepresentationAssertion)
        self.assertEqual(len(document.assertions), 1)
        self.assertEqual(validate_document(document), {"result": "valid"})

    def test_many_to_many_associations_are_explicit_and_not_deduplicated(self) -> None:
        document = new_document()
        concept_ids = (identifier(2), identifier(4))
        representation_ids = (identifier(3), identifier(5))
        for concept_id in concept_ids:
            document.add_concept(identifier=concept_id)
        for representation_id in representation_ids:
            document.add_representation(identifier=representation_id)

        pairs = (
            (representation_ids[0], concept_ids[0]),
            (representation_ids[0], concept_ids[1]),
            (representation_ids[1], concept_ids[0]),
            (representation_ids[1], concept_ids[0]),
        )
        for offset, (representation_id, concept_id) in enumerate(pairs, start=20):
            document.add_concept_representation_assertion(
                identifier=identifier(offset),
                representation=reference(
                    target=representation_id, location="in-document"
                ),
                concept=reference(target=concept_id, location="in-document"),
            )

        self.assertEqual(len(document.assertions), 4)
        self.assertEqual(document.assertions[-1]["concept"], document.assertions[-2]["concept"])
        self.assertEqual(document.assertions[-1]["subject"], document.assertions[-2]["subject"])
        self.assertNotEqual(document.assertions[-1].identifier, document.assertions[-2].identifier)
        self.assertEqual(validate_document(document), {"result": "valid"})

    def test_source_and_entity_ids_are_not_merged(self) -> None:
        document = new_document()
        document.add_concept(identifier=identifier(2))
        source = document.add_source(identifier=identifier(2))

        self.assertEqual(len(document.entities), 1)
        self.assertEqual(len(document.sources), 1)
        self.assertIs(source.backing_record, document.backing_tree["sources"][0])
        self.assertEqual(
            validate_document(document),
            {"result": "invalid", "layer": 3, "category": "duplicate-id"},
        )

    def test_binding_creation_adds_no_truth_assertion(self) -> None:
        document = new_document()
        document.add_concept(identifier=identifier(2))
        document.add_source(identifier=identifier(10))
        document.add_binding(
            identifier=identifier(11),
            entity=reference(target=identifier(2), location="in-document"),
            source=reference(target=identifier(10), location="in-document"),
        )

        self.assertNotIn("assertions", document.backing_tree)
        self.assertEqual(validate_document(document), {"result": "valid"})

    def test_rich_loaded_document_preserves_trust_lifecycle_extensions_and_numbers(self) -> None:
        document = load_path(ROOT / "conformance" / "valid" / "trust-records.json")
        extension_document = load_path(
            ROOT / "conformance" / "valid" / "unknown-extension-numbers.json"
        )
        revision_document = load_path(
            ROOT / "conformance" / "valid" / "current-revision.json"
        )
        document.backing_tree["namespaces"]["ext"] = (
            extension_document.backing_tree["namespaces"]["ext"]
        )
        document.backing_tree["extensions"] = extension_document.backing_tree[
            "extensions"
        ]
        document.backing_tree["revision"] = deepcopy(
            revision_document.backing_tree["revision"]
        )
        trust = document.backing_tree["entities"][0]
        lifecycle = document.backing_tree["revision"]
        extensions = document.backing_tree["extensions"]
        numbers = extensions["ext:opaque"]["numbers"]
        tokens = [number.token for number in numbers]

        self.assertEqual(validate_document(document), {"result": "valid"})
        document.add_source(identifier=identifier(10))

        self.assertIs(document.backing_tree["entities"][0], trust)
        self.assertIs(document.backing_tree["revision"], lifecycle)
        self.assertIs(document.backing_tree["extensions"], extensions)
        self.assertTrue(all(isinstance(number, RawNumber) for number in numbers))
        self.assertEqual([number.token for number in numbers], tokens)
        self.assertEqual(validate_document(document), {"result": "valid"})

        reloaded = load_bytes(dump_bytes(document))
        reloaded_numbers = reloaded["extensions"]["ext:opaque"]["numbers"]
        self.assertEqual([number.token for number in reloaded_numbers], tokens)
        self.assertEqual(reloaded["entities"][0], trust)
        self.assertEqual(reloaded["revision"], lifecycle)

    def test_i3_regression_has_no_resolver_i8_or_execution_surface(self) -> None:
        for name in (
            "VocabularyResolver",
            "ExtensionEditor",
            "CompositeProfile",
        ):
            self.assertFalse(hasattr(sdk, name), name)
        for name in (
            "add_extension",
            "add_projection",
        ):
            self.assertFalse(hasattr(SemanticDocument, name), name)

    def test_s2_regression_totals_remain_unchanged(self) -> None:
        valid, invalid, expected, errors = run_suite()
        self.assertEqual((valid, invalid, expected), (17, 84, 101))
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
