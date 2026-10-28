from __future__ import annotations

from copy import deepcopy
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
    Change,
    Revision,
    SemanticDocument,
    Tombstone,
    Validity,
    date_value,
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
    return f"urn:uuid:40000000-0000-4000-8000-{number:012x}"


def new_document() -> SemanticDocument:
    return SemanticDocument.create(
        spec_version="0.1.0",
        identifier=identifier(1),
        scope={"completeness": "partial"},
        namespaces={"ex": "https://example.invalid/terms/"},
    )


def local(target: str) -> dict[str, str]:
    return reference(target=target, location="in-document")


def external(target: str) -> dict[str, str]:
    return reference(target=target, location="out-of-document")


class SdkLifecycleTests(unittest.TestCase):
    def test_current_revision_is_explicit_and_history_is_optional(self) -> None:
        document = new_document()
        revision = document.set_revision(identifier=identifier(10))

        self.assertIsInstance(revision, Revision)
        self.assertEqual(revision.identifier, identifier(10))
        self.assertNotIn("parents", revision)
        self.assertNotIn("history", document)
        self.assertEqual(validate_document(document), {"result": "valid"})

        before = deepcopy(revision.backing_record)
        document.add_concept(identifier=identifier(2))
        self.assertEqual(revision.backing_record, before)
        self.assertEqual(document.revision.identifier, identifier(10))

    def test_current_and_historical_revisions_remain_distinct(self) -> None:
        document = new_document()
        document.set_history(completeness="partial")
        historical = document.add_history_revision(identifier=identifier(10))
        current = document.set_revision(
            identifier=identifier(11),
            parents=[local(historical.identifier)],
        )

        self.assertIs(document.revision.backing_record, current.backing_record)
        self.assertIs(
            document.historical_revisions[0].backing_record,
            historical.backing_record,
        )
        self.assertNotEqual(current.identifier, historical.identifier)
        self.assertEqual(current.parents, (local(historical.identifier),))
        self.assertEqual(validate_document(document), {"result": "valid"})

    def test_revision_graph_rules_remain_layer_three_rules(self) -> None:
        self_parent = new_document()
        self_parent.set_revision(
            identifier=identifier(10),
            parents=[local(identifier(10))],
        )
        self.assertEqual(
            validate_document(self_parent),
            {"result": "invalid", "layer": 3, "category": "revision-self-parent"},
        )

        repeated = new_document()
        repeated.set_revision(
            identifier=identifier(10),
            parents=[external(identifier(12)), external(identifier(12))],
        )
        self.assertEqual(
            validate_document(repeated),
            {"result": "invalid", "layer": 3, "category": "repeated-reference"},
        )

        cycle = new_document()
        cycle.set_history(completeness="partial")
        cycle.set_revision(
            identifier=identifier(10),
            parents=[local(identifier(11))],
        )
        cycle.add_history_revision(
            identifier=identifier(11),
            parents=[local(identifier(10))],
        )
        self.assertEqual(
            validate_document(cycle),
            {"result": "invalid", "layer": 3, "category": "revision-cycle"},
        )

    def test_change_is_descriptive_and_never_replayed(self) -> None:
        document = new_document()
        entity = document.add_concept(identifier=identifier(2))
        revision = document.set_revision(identifier=identifier(10))
        document.set_history(completeness="partial")
        before = deepcopy(entity.backing_record)
        change = document.add_change(
            revision=local(revision.identifier),
            targets=[local(entity.identifier)],
            kind="ex:observed",
            details=string_value("descriptive only"),
        )

        self.assertIsInstance(change, Change)
        self.assertNotIn("id", change)
        self.assertEqual(entity.backing_record, before)
        self.assertFalse(hasattr(document, "apply_change"))
        self.assertFalse(hasattr(document, "replay_history"))
        self.assertEqual(validate_document(document), {"result": "valid"})

    def test_loaded_changes_do_not_mutate_current_state(self) -> None:
        document = load_path(
            ROOT / "conformance" / "valid" / "partial-history-changes.json"
        )
        before = dump_bytes(document)
        changes = document.changes

        self.assertEqual(len(changes), 2)
        self.assertIs(changes[0].backing_record, document["history"]["changes"][0])
        self.assertEqual(dump_bytes(document), before)

    def test_tombstone_is_explicit_and_does_not_remove_target(self) -> None:
        external_document = new_document()
        tombstone = external_document.add_tombstone(
            identifier=identifier(20),
            target=external(identifier(2)),
            target_category="entity",
            reason="ex:withdrawn",
        )
        self.assertIsInstance(tombstone, Tombstone)
        self.assertEqual(validate_document(external_document), {"result": "valid"})

        live_document = new_document()
        entity = live_document.add_concept(identifier=identifier(2))
        live_document.add_tombstone(
            identifier=identifier(20),
            target=local(entity.identifier),
            target_category="entity",
        )
        self.assertEqual(len(live_document.entities), 1)
        self.assertEqual(
            validate_document(live_document),
            {"result": "invalid", "layer": 3, "category": "live-tombstone"},
        )

    def test_absence_never_creates_deletion_metadata(self) -> None:
        document = new_document()
        document.add_concept(identifier=identifier(2))

        self.assertNotIn("tombstones", document)
        self.assertNotIn("history", document)
        self.assertEqual(document.tombstones, ())
        self.assertEqual(document.changes, ())

    def test_supersession_is_explicit_and_does_not_mutate_target(self) -> None:
        document = new_document()
        entity = document.add_concept(identifier=identifier(2))
        prior = document.add_property_assertion(
            identifier=identifier(30),
            subject=local(entity.identifier),
            property_term="ex:name",
            value="prior",
        )
        replacement = document.add_property_assertion(
            identifier=identifier(31),
            subject=local(entity.identifier),
            property_term="ex:name",
            value="replacement",
        )
        prior_before = deepcopy(prior.backing_record)
        reference_record = replacement.add_supersedes(local(prior.identifier))

        self.assertEqual(prior.backing_record, prior_before)
        self.assertEqual(reference_record, local(prior.identifier))
        self.assertEqual(replacement.supersedes, (local(prior.identifier),))
        self.assertEqual(validate_document(document), {"result": "valid"})

    def test_supersession_failures_remain_layer_three_rules(self) -> None:
        self_supersession = new_document()
        entity = self_supersession.add_concept(identifier=identifier(2))
        assertion = self_supersession.add_type_assertion(
            identifier=identifier(30),
            subject=local(entity.identifier),
            type_term="ex:asset",
        )
        assertion.add_supersedes(local(assertion.identifier))
        self.assertEqual(
            validate_document(self_supersession),
            {"result": "invalid", "layer": 3, "category": "self-supersession"},
        )

        repeated = new_document()
        repeated_entity = repeated.add_concept(identifier=identifier(2))
        prior = repeated.add_type_assertion(
            identifier=identifier(30),
            subject=local(repeated_entity.identifier),
            type_term="ex:asset",
        )
        replacement = repeated.add_type_assertion(
            identifier=identifier(31),
            subject=local(repeated_entity.identifier),
            type_term="ex:asset",
        )
        replacement.add_supersedes(local(prior.identifier))
        replacement.add_supersedes(local(prior.identifier))
        self.assertEqual(
            validate_document(repeated),
            {"result": "invalid", "layer": 3, "category": "repeated-reference"},
        )

        cycle = new_document()
        cycle_entity = cycle.add_concept(identifier=identifier(2))
        first = cycle.add_type_assertion(
            identifier=identifier(30),
            subject=local(cycle_entity.identifier),
            type_term="ex:asset",
        )
        second = cycle.add_type_assertion(
            identifier=identifier(31),
            subject=local(cycle_entity.identifier),
            type_term="ex:asset",
        )
        first.add_supersedes(local(second.identifier))
        second.add_supersedes(local(first.identifier))
        self.assertEqual(
            validate_document(cycle),
            {"result": "invalid", "layer": 3, "category": "supersession-cycle"},
        )

    def test_validity_preserves_exact_bounds_and_layer_three_ordering(self) -> None:
        document = new_document()
        entity = document.add_concept(identifier=identifier(2))
        validity = entity.set_validity(
            kind="ex:time",
            from_value=date_value("2026-01-01"),
            until=date_value("2026-12-31"),
        )

        self.assertIsInstance(validity, Validity)
        self.assertEqual(validity.from_value, date_value("2026-01-01"))
        self.assertEqual(validity.until, date_value("2026-12-31"))
        self.assertEqual(validate_document(document), {"result": "valid"})

        reversed_document = new_document()
        reversed_entity = reversed_document.add_concept(identifier=identifier(2))
        reversed_entity.set_validity(
            kind="ex:time",
            from_value=date_value("2026-12-31"),
            until=date_value("2026-01-01"),
        )
        self.assertEqual(
            validate_document(reversed_document),
            {"result": "invalid", "layer": 3, "category": "validity-order"},
        )

    def test_conditional_identity_is_preserved_for_change_and_trust(self) -> None:
        anonymous = new_document()
        entity = anonymous.add_concept(identifier=identifier(2))
        revision = anonymous.set_revision(identifier=identifier(10))
        anonymous.set_history(completeness="partial")
        change = anonymous.add_change(
            revision=local(revision.identifier),
            targets=[local(entity.identifier)],
            kind="ex:observed",
        )
        change.set_validity(kind="ex:time", from_value=date_value("2026-01-01"))
        self.assertNotIn("id", change)
        self.assertEqual(
            validate_document(anonymous),
            {"result": "invalid", "layer": 3, "category": "conditional-id"},
        )

        identified = new_document()
        identified_entity = identified.add_concept(identifier=identifier(2))
        identified_revision = identified.set_revision(identifier=identifier(10))
        identified.set_history(completeness="partial")
        identified_change = identified.add_change(
            identifier=identifier(20),
            revision=local(identified_revision.identifier),
            targets=[local(identified_entity.identifier)],
            kind="ex:observed",
        )
        identified_change.set_validity(
            kind="ex:time", from_value=date_value("2026-01-01")
        )
        self.assertEqual(identified_change.identifier, identifier(20))
        self.assertEqual(validate_document(identified), {"result": "valid"})

    def test_history_completeness_and_membership_remain_explicit(self) -> None:
        document = new_document()
        entity = document.add_concept(identifier=identifier(2))
        document.set_history(completeness="unknown")
        historical = document.add_history_revision(identifier=identifier(10))
        membership = document.add_history_membership(
            revision=local(historical.identifier),
            target=local(entity.identifier),
        )

        self.assertEqual(document["history"]["completeness"], "unknown")
        self.assertEqual(membership["target"], local(entity.identifier))
        self.assertNotIn("tombstones", document)
        self.assertEqual(validate_document(document), {"result": "valid"})

    def test_lifecycle_views_reuse_scoped_trust_without_propagation(self) -> None:
        document = new_document()
        revision = document.set_revision(identifier=identifier(10))
        revision.add_provenance(kind="ex:authored")
        document.set_history(completeness="partial")
        change = document.add_change(
            identifier=identifier(20),
            revision=local(revision.identifier),
            targets=[external(identifier(2))],
            kind="ex:observed",
        )
        change.add_review(disposition="ex:confirmed")
        tombstone = document.add_tombstone(
            identifier=identifier(30),
            target=external(identifier(3)),
            target_category="entity",
        )
        tombstone.add_confidence(score=integer_value("1"))

        self.assertIn("provenance", revision)
        self.assertNotIn("provenance", change)
        self.assertIn("reviews", change)
        self.assertNotIn("reviews", tombstone)
        self.assertIn("confidence", tombstone)
        self.assertEqual(validate_document(document), {"result": "valid"})

    def test_revision_and_tombstone_reject_non_schema_lifecycle_surface(self) -> None:
        document = new_document()
        revision = document.set_revision(identifier=identifier(10))
        tombstone = document.add_tombstone(
            identifier=identifier(20),
            target=external(identifier(2)),
            target_category="entity",
        )

        for host in (revision, tombstone):
            self.assertFalse(hasattr(host, "set_validity"))
            self.assertFalse(hasattr(host, "add_supersedes"))

    def test_rich_loaded_document_survives_i5_round_trip(self) -> None:
        document = load_path(ROOT / "conformance" / "valid" / "trust-records.json")
        extension_document = load_path(
            ROOT / "conformance" / "valid" / "unknown-extension-numbers.json"
        )
        document.backing_tree["namespaces"]["ext"] = (
            extension_document.backing_tree["namespaces"]["ext"]
        )
        document.backing_tree["extensions"] = extension_document.backing_tree[
            "extensions"
        ]
        trust = document.backing_tree["entities"][0]
        extensions = document.backing_tree["extensions"]
        numbers = extensions["ext:opaque"]["numbers"]
        tokens = [number.token for number in numbers]

        revision = document.set_revision(identifier=identifier(10))
        document.set_history(completeness="partial")
        document.add_change(
            revision=local(revision.identifier),
            targets=[local(trust["id"])],
            kind="ex:observed",
            details=decimal_value(coefficient="1", exponent="-1"),
        )

        self.assertIs(document.backing_tree["entities"][0], trust)
        self.assertIs(document.backing_tree["extensions"], extensions)
        self.assertTrue(all(isinstance(number, RawNumber) for number in numbers))
        self.assertEqual([number.token for number in numbers], tokens)
        self.assertEqual(validate_document(document), {"result": "valid"})

        reloaded = load_bytes(dump_bytes(document))
        reloaded_numbers = reloaded["extensions"]["ext:opaque"]["numbers"]
        self.assertEqual([number.token for number in reloaded_numbers], tokens)
        self.assertEqual(reloaded["entities"][0], trust)
        self.assertEqual(len(reloaded.changes), 1)
        self.assertEqual(validate_document(reloaded), {"result": "valid"})

    def test_i1_to_i4_builders_do_not_create_lifecycle(self) -> None:
        document = new_document()
        entity = document.add_concept(identifier=identifier(2))
        source = document.add_source(identifier=identifier(3))
        document.add_binding(
            identifier=identifier(4),
            entity=local(entity.identifier),
            source=local(source.identifier),
        )
        assertion = document.add_type_assertion(
            identifier=identifier(5),
            subject=local(entity.identifier),
            type_term="ex:asset",
        )
        assertion.add_provenance(kind="ex:authored")
        assertion.add_confidence(score=integer_value("1"))
        assertion.add_review(disposition="ex:confirmed")

        for member in ("revision", "history", "tombstones"):
            self.assertNotIn(member, document)
        for record in document.entities + document.sources + document.bindings + document.assertions:
            self.assertNotIn("validity", record)
            self.assertNotIn("supersedes", record)
        self.assertEqual(validate_document(document), {"result": "valid"})

    def test_i5_regression_has_no_i8_or_execution_surface(self) -> None:
        for name in (
            "ExtensionEditor",
            "VocabularyResolver",
            "VocabularyRegistry",
            "ProfileEvaluator",
            "CompositeProfile",
        ):
            self.assertFalse(hasattr(sdk, name), name)
        for name in (
            "apply_change",
            "replay_history",
            "restore_revision",
            "checkout_revision",
            "undo",
            "redo",
            "merge",
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
