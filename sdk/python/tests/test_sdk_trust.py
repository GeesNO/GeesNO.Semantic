from __future__ import annotations

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
import geesno_semantic as sdk  # noqa: E402
from geesno_semantic import (  # noqa: E402
    Confidence,
    Provenance,
    Review,
    SemanticDocument,
    decimal_value,
    dump_bytes,
    integer_value,
    load_bytes,
    load_path,
    reference,
    string_value,
    validate_document,
)


def identifier(number: int) -> str:
    return f"urn:uuid:30000000-0000-4000-8000-{number:012x}"


def new_document() -> SemanticDocument:
    return SemanticDocument.create(
        spec_version="0.1.0",
        identifier=identifier(1),
        scope={"completeness": "partial"},
        namespaces={"ex": "https://example.invalid/terms/"},
    )


class SdkTrustTests(unittest.TestCase):
    def test_provenance_is_host_scoped_anonymous_or_explicitly_identified(self) -> None:
        document = new_document()
        entity = document.add_concept(identifier=identifier(2))

        anonymous = entity.add_provenance(kind="ex:authored")
        identified = entity.add_provenance(
            identifier=identifier(20),
            kind="ex:generated",
            details=string_value("declared evidence"),
        )

        self.assertIsInstance(anonymous, Provenance)
        self.assertNotIn("id", anonymous)
        self.assertEqual(identified.identifier, identifier(20))
        self.assertIs(
            identified.backing_record,
            entity.backing_record["provenance"][1],
        )
        self.assertEqual(validate_document(document), {"result": "valid"})

    def test_provenance_sources_are_explicit_and_existing_validator_checks_category(self) -> None:
        document = new_document()
        entity = document.add_concept(identifier=identifier(2))
        source = document.add_source(identifier=identifier(10))
        source_reference = reference(
            target=source.identifier,
            location="in-document",
        )
        provenance = entity.add_provenance(
            kind="ex:derived",
            sources=[source_reference],
        )

        self.assertEqual(provenance["sources"], [source_reference])
        self.assertIsNot(provenance["sources"][0], source_reference)
        self.assertEqual(validate_document(document), {"result": "valid"})

        invalid = new_document()
        invalid_entity = invalid.add_concept(identifier=identifier(2))
        invalid_entity.add_provenance(
            kind="ex:derived",
            sources=[reference(target=identifier(2), location="in-document")],
        )
        self.assertEqual(
            validate_document(invalid),
            {"result": "invalid", "layer": 3, "category": "target-category"},
        )

    def test_confidence_preserves_exact_score_and_layer_three_owns_range(self) -> None:
        document = new_document()
        entity = document.add_concept(identifier=identifier(2))
        score = decimal_value(coefficient="9", exponent="-1")
        confidence = entity.add_confidence(score=score, method="ex:calibrated")

        self.assertIsInstance(confidence, Confidence)
        self.assertEqual(confidence.score, score)
        self.assertIsNot(confidence.score, score)
        self.assertNotIn("reviews", entity)
        self.assertEqual(validate_document(document), {"result": "valid"})

        with self.assertRaises(TypeError):
            entity.add_confidence(score=0.9)  # type: ignore[arg-type]

        invalid = new_document()
        invalid_entity = invalid.add_concept(identifier=identifier(2))
        invalid_entity.add_confidence(score=integer_value("2"))
        self.assertEqual(
            validate_document(invalid),
            {"result": "invalid", "layer": 3, "category": "confidence-range"},
        )

    def test_review_creates_no_truth_permission_or_confidence(self) -> None:
        document = new_document()
        entity = document.add_concept(identifier=identifier(2))
        review = entity.add_review(
            disposition="ex:reviewed",
            details=string_value("checked"),
        )

        self.assertIsInstance(review, Review)
        self.assertEqual(review.disposition, "ex:reviewed")
        for name in ("accepted", "true", "authoritative", "approved", "safe"):
            self.assertNotIn(name, review)
            self.assertNotIn(name, entity)
        self.assertNotIn("confidence", entity)
        self.assertEqual(validate_document(document), {"result": "valid"})

    def test_assertion_provenance_creates_no_truth_or_assertion(self) -> None:
        document = new_document()
        entity = document.add_concept(identifier=identifier(2))
        assertion = document.add_type_assertion(
            identifier=identifier(30),
            subject=reference(target=entity.identifier, location="in-document"),
            type_term="ex:asset",
        )
        assertion.add_provenance(kind="ex:authored")

        self.assertEqual(len(document.assertions), 1)
        self.assertNotIn("assertions", assertion)
        for name in ("accepted", "true", "authoritative", "approved"):
            self.assertNotIn(name, assertion)
        self.assertNotIn("trust_records", document.backing_tree)
        self.assertNotIn("provenance_records", document.backing_tree)
        self.assertEqual(validate_document(document), {"result": "valid"})

    def test_conditional_identity_remains_a_layer_three_rule(self) -> None:
        document = new_document()
        entity = document.add_concept(identifier=identifier(2))
        provenance = entity.add_provenance(kind="ex:generated")
        provenance.add_review(disposition="ex:confirmed")

        self.assertNotIn("id", provenance)
        self.assertEqual(
            validate_document(document),
            {"result": "invalid", "layer": 3, "category": "conditional-id"},
        )

        valid = new_document()
        valid_entity = valid.add_concept(identifier=identifier(2))
        identified = valid_entity.add_provenance(
            identifier=identifier(20),
            kind="ex:generated",
        )
        nested_review = identified.add_review(disposition="ex:confirmed")
        self.assertEqual(identified.identifier, identifier(20))
        self.assertNotIn("id", nested_review)
        self.assertEqual(validate_document(valid), {"result": "valid"})

    def test_nested_trust_remains_nested_without_propagation(self) -> None:
        document = new_document()
        entity = document.add_concept(identifier=identifier(2))
        provenance = entity.add_provenance(kind="ex:generated")
        confidence = provenance.add_confidence(score=integer_value("1"))

        self.assertIsInstance(confidence, Confidence)
        self.assertIn("confidence", provenance)
        self.assertNotIn("confidence", entity)
        self.assertNotIn("confidence", document.backing_tree)
        self.assertEqual(len(entity.provenance), 1)
        self.assertEqual(len(entity.provenance[0].confidence), 1)
        self.assertEqual(validate_document(document), {"result": "valid"})

    def test_binding_trust_does_not_create_truth_or_propagate(self) -> None:
        document = new_document()
        entity = document.add_concept(identifier=identifier(2))
        source = document.add_source(identifier=identifier(10))
        binding = document.add_binding(
            identifier=identifier(11),
            entity=reference(target=entity.identifier, location="in-document"),
            source=reference(target=source.identifier, location="in-document"),
        )
        provenance = binding.add_provenance(kind="ex:correlated")

        self.assertIsInstance(provenance, Provenance)
        self.assertIn("provenance", binding)
        self.assertNotIn("provenance", entity)
        self.assertNotIn("provenance", source)
        self.assertNotIn("assertions", document.backing_tree)
        self.assertEqual(validate_document(document), {"result": "valid"})

    def test_loaded_trust_views_are_live_and_do_not_mutate_the_tree(self) -> None:
        document = load_path(ROOT / "conformance" / "valid" / "trust-records.json")
        before = dump_bytes(document)
        hosts = document.trust_hosts

        self.assertEqual(dump_bytes(document), before)
        self.assertEqual(len(hosts), 7)
        self.assertEqual(sum(isinstance(host, Provenance) for host in hosts), 2)
        self.assertEqual(sum(isinstance(host, Confidence) for host in hosts), 2)
        self.assertEqual(sum(isinstance(host, Review) for host in hosts), 2)
        expected_ids: set[int] = set()

        def collect(record: dict[str, object]) -> None:
            expected_ids.add(id(record))
            for member in ("provenance", "confidence", "reviews"):
                for child in record.get(member, []):  # type: ignore[union-attr]
                    collect(child)

        collect(document.backing_tree["entities"][0])
        self.assertEqual(
            {id(host.backing_record) for host in hosts},
            expected_ids,
        )

    def test_loaded_revision_is_an_accepted_host_without_lifecycle_api(self) -> None:
        document = load_path(ROOT / "conformance" / "valid" / "current-revision.json")
        document.backing_tree["namespaces"] = {
            "ex": "https://example.invalid/terms/"
        }
        revision = document.backing_tree["revision"]
        revision_host = next(
            host for host in document.trust_hosts if host.backing_record is revision
        )
        revision_host.add_provenance(kind="ex:authored")

        self.assertIn("provenance", revision)
        self.assertIsInstance(revision_host, sdk.Revision)
        self.assertFalse(hasattr(revision_host, "set_validity"))
        self.assertFalse(hasattr(revision_host, "add_supersedes"))
        self.assertEqual(validate_document(document), {"result": "valid"})

    def test_loaded_tombstone_and_change_are_hosts_without_root_trust(self) -> None:
        tombstone_document = load_path(
            ROOT / "conformance" / "valid" / "tombstone-external.json"
        )
        tombstone_document.backing_tree["namespaces"] = {
            "ex": "https://example.invalid/terms/"
        }
        tombstone = tombstone_document.backing_tree["tombstones"][0]
        tombstone_host = next(
            host
            for host in tombstone_document.trust_hosts
            if host.backing_record is tombstone
        )
        tombstone_host.add_review(disposition="ex:confirmed")

        change_document = load_path(
            ROOT / "conformance" / "valid" / "partial-history-changes.json"
        )
        change = change_document.backing_tree["history"]["changes"][0]
        change_host = next(
            host
            for host in change_document.trust_hosts
            if host.backing_record is change
        )
        change_host.add_provenance(kind="ex:observed")

        self.assertNotIn(
            id(tombstone_document.backing_tree),
            {id(host.backing_record) for host in tombstone_document.trust_hosts},
        )
        self.assertIsInstance(tombstone_host, sdk.Tombstone)
        self.assertFalse(hasattr(tombstone_host, "set_validity"))
        self.assertFalse(hasattr(tombstone_host, "add_supersedes"))
        self.assertIsInstance(change_host, sdk.Change)
        self.assertTrue(hasattr(change_host, "set_validity"))
        self.assertTrue(hasattr(change_host, "add_supersedes"))
        self.assertEqual(validate_document(tombstone_document), {"result": "valid"})
        self.assertEqual(validate_document(change_document), {"result": "valid"})

    def test_round_trip_preserves_trust_extensions_and_raw_numbers(self) -> None:
        document = load_path(
            ROOT / "conformance" / "valid" / "unknown-extension-numbers.json"
        )
        document.backing_tree["namespaces"]["ex"] = (
            "https://example.invalid/terms/"
        )
        numbers = document.backing_tree["extensions"]["ext:opaque"]["numbers"]
        tokens = [number.token for number in numbers]
        entity = document.add_concept(identifier=identifier(2))
        provenance = entity.add_provenance(
            identifier=identifier(20),
            kind="ex:authored",
        )

        self.assertTrue(all(isinstance(number, RawNumber) for number in numbers))
        self.assertEqual(validate_document(document), {"result": "valid"})
        reloaded = load_bytes(dump_bytes(document))
        reloaded_numbers = reloaded["extensions"]["ext:opaque"]["numbers"]
        self.assertEqual([number.token for number in reloaded_numbers], tokens)
        self.assertEqual(
            reloaded["entities"][0]["provenance"][0]["id"],
            provenance.identifier,
        )
        self.assertEqual(validate_document(reloaded), {"result": "valid"})

    def test_i4_regression_has_no_resolver_i8_or_execution_surface(self) -> None:
        for name in (
            "ExtensionEditor",
            "VocabularyResolver",
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
