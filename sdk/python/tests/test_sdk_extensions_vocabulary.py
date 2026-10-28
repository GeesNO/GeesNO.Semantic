from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch


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
    SemanticDocument,
    VocabularyView,
    dump_bytes,
    expand_qualified_term,
    integer_value,
    load_bytes,
    load_path,
    reference,
    split_qualified_term,
    validate_document,
)


def identifier(number: int) -> str:
    return f"urn:uuid:50000000-0000-4000-8000-{number:012x}"


def new_document(*, namespaces: dict[str, str] | None = None) -> SemanticDocument:
    return SemanticDocument.create(
        spec_version="0.1.0",
        identifier=identifier(1),
        scope={"completeness": "partial"},
        namespaces=namespaces,
    )


def local(target: str) -> dict[str, str]:
    return reference(target=target, location="in-document")


def external(target: str) -> dict[str, str]:
    return reference(target=target, location="out-of-document")


class SdkExtensionsVocabularyTests(unittest.TestCase):
    def test_unknown_extension_view_is_live_and_reading_is_nonmutating(self) -> None:
        document = load_path(
            ROOT / "conformance" / "valid" / "unknown-extension-numbers.json"
        )
        before = dump_bytes(document)
        backing_payload = document.backing_tree["extensions"]["ext:opaque"]

        self.assertIs(document.extensions["ext:opaque"], backing_payload)
        self.assertIs(document.get_extension("ext:opaque"), backing_payload)
        self.assertEqual(tuple(document.extensions), ("ext:opaque",))
        self.assertEqual(dump_bytes(document), before)

    def test_raw_number_tokens_survive_access_edit_and_round_trip(self) -> None:
        document = load_path(
            ROOT / "conformance" / "valid" / "unknown-extension-numbers.json"
        )
        numbers = document.get_extension("ext:opaque")["numbers"]
        tokens = [number.token for number in numbers]

        document.set_extension(
            "ext:second",
            {"nested": [RawNumber("1e-999"), {"value": RawNumber("-0")}]},
        )
        reloaded = load_bytes(dump_bytes(document))

        reloaded_numbers = reloaded.get_extension("ext:opaque")["numbers"]
        self.assertEqual([number.token for number in reloaded_numbers], tokens)
        self.assertEqual(
            reloaded.get_extension("ext:second")["nested"][0].token,
            "1e-999",
        )
        self.assertEqual(
            reloaded.get_extension("ext:second")["nested"][1]["value"].token,
            "-0",
        )

    def test_explicit_add_creates_no_namespace_trust_or_lifecycle(self) -> None:
        document = new_document()
        document.set_extension("ext:opaque", {"command": "do nothing"})

        self.assertNotIn("namespaces", document)
        for member in (
            "revision",
            "history",
            "tombstones",
            "provenance",
            "confidence",
            "reviews",
        ):
            self.assertNotIn(member, document)
        self.assertEqual(
            validate_document(document),
            {"result": "invalid", "layer": 3, "category": "undeclared-prefix"},
        )

    def test_explicit_replace_changes_only_the_selected_payload(self) -> None:
        document = new_document(
            namespaces={"ext": "https://example.invalid/extensions/"}
        )
        document.set_extension("ext:first", {"value": "old"})
        document.set_extension("ext:second", {"value": "untouched"})
        untouched = document.get_extension("ext:second")

        replacement = document.set_extension("ext:first", {"value": "new"})

        self.assertEqual(replacement, {"value": "new"})
        self.assertEqual(document.get_extension("ext:first"), replacement)
        self.assertIs(document.get_extension("ext:second"), untouched)
        self.assertEqual(validate_document(document), {"result": "valid"})

    def test_explicit_remove_has_no_lifecycle_side_effect(self) -> None:
        document = new_document(
            namespaces={"ext": "https://example.invalid/extensions/"}
        )
        document.set_extension("ext:only", {"value": True})

        removed = document.remove_extension("ext:only")

        self.assertEqual(removed, {"value": True})
        self.assertNotIn("extensions", document)
        for member in ("revision", "history", "tombstones"):
            self.assertNotIn(member, document)
        self.assertEqual(validate_document(document), {"result": "valid"})

    def test_extension_api_matches_the_exact_s2_host_matrix(self) -> None:
        document = new_document(
            namespaces={"ext": "https://example.invalid/extensions/"}
        )
        entity = document.add_concept(identifier=identifier(2))
        source = document.add_source(identifier=identifier(3))
        binding = document.add_binding(
            identifier=identifier(4),
            entity=local(entity.identifier),
            source=local(source.identifier),
        )
        assertion = document.add_type_assertion(
            identifier=identifier(5),
            subject=local(entity.identifier),
            type_term="ext:type",
        )
        revision = document.set_revision(identifier=identifier(6))
        document.set_history(completeness="partial")
        change = document.add_change(
            identifier=identifier(7),
            revision=local(revision.identifier),
            targets=[local(entity.identifier)],
            kind="ext:observed",
        )
        tombstone = document.add_tombstone(
            identifier=identifier(8),
            target=external(identifier(9)),
            target_category="entity",
        )
        provenance = entity.add_provenance(
            identifier=identifier(10), kind="ext:authored"
        )
        confidence = entity.add_confidence(
            identifier=identifier(11), score=integer_value("1")
        )
        review = entity.add_review(
            identifier=identifier(12), disposition="ext:confirmed"
        )
        hosts = (
            document,
            entity,
            assertion,
            source,
            binding,
            revision,
            tombstone,
            change,
            provenance,
            confidence,
            review,
        )

        for index, host in enumerate(hosts):
            host.set_extension("ext:opaque", {"host": str(index)})

        def backing_identity(host: object) -> int:
            if host is document:
                return id(document.backing_tree)
            return id(host.backing_record)  # type: ignore[attr-defined]

        self.assertEqual(
            {backing_identity(host) for host in document.extension_hosts},
            {backing_identity(host) for host in hosts},
        )
        self.assertFalse(hasattr(document["scope"], "set_extension"))
        self.assertFalse(hasattr(local(entity.identifier), "set_extension"))
        self.assertFalse(hasattr(document.history_memberships, "set_extension"))
        self.assertEqual(validate_document(document), {"result": "valid"})

    def test_extension_payload_cannot_redefine_core(self) -> None:
        document = new_document(
            namespaces={"ext": "https://example.invalid/extensions/"}
        )
        entity = document.add_concept(identifier=identifier(2))
        entity.set_extension(
            "ext:override",
            {
                "kind": "representation",
                "id": identifier(99),
                "subject": "not a core subject",
            },
        )

        self.assertEqual(entity.kind, "concept")
        self.assertEqual(entity.identifier, identifier(2))
        self.assertEqual(validate_document(document), {"result": "valid"})

    def test_unknown_identifiers_never_trigger_network_or_file_access(self) -> None:
        document = new_document(
            namespaces={"remote": "https://unavailable.invalid/vocabulary/"}
        )
        with (
            patch("socket.socket", side_effect=AssertionError("network access")),
            patch(
                "socket.create_connection",
                side_effect=AssertionError("network access"),
            ),
            patch(
                "urllib.request.urlopen",
                side_effect=AssertionError("network access"),
            ),
            patch("builtins.open", side_effect=AssertionError("file access")),
        ):
            document.set_extension("remote:opaque", {"url": "file:///do/not/open"})
            self.assertEqual(
                document.expand_term("remote:opaque"),
                "https://unavailable.invalid/vocabulary/opaque",
            )
            self.assertEqual(document.get_extension("remote:opaque")["url"], "file:///do/not/open")

    def test_namespace_and_extension_operations_remain_independent(self) -> None:
        document = new_document(
            namespaces={"ex": "https://example.invalid/terms/"}
        )

        self.assertEqual(document.namespace("ex"), "https://example.invalid/terms/")
        self.assertEqual(document.expand_term("ex:item"), "https://example.invalid/terms/item")
        self.assertNotIn("extensions", document)

        no_namespace = new_document()
        no_namespace.set_extension("ex:item", None)
        self.assertNotIn("namespaces", no_namespace)

    def test_two_vocabularies_and_exact_term_lookup_do_not_collide(self) -> None:
        document = new_document(
            namespaces={
                "a": "https://a.example/terms/",
                "b": "https://b.example/terms/",
            }
        )
        a_term = document.expand_term("a:label")
        b_term = document.expand_term("b:label")
        a_record = {"definition": "A label"}
        b_record = {"definition": "B label"}
        vocabulary_a = VocabularyView(
            identity="https://a.example/vocabulary",
            version="edition-a",
            terms={a_term: a_record},
        )
        vocabulary_b = VocabularyView(
            identity="https://b.example/vocabulary",
            version="edition-b",
            terms={b_term: b_record},
        )

        self.assertNotEqual(a_term, b_term)
        self.assertIs(vocabulary_a.get_term(a_term), a_record)
        self.assertIs(vocabulary_b.get_term(b_term), b_record)
        self.assertFalse(vocabulary_a.has_term(b_term))
        with self.assertRaises(KeyError):
            vocabulary_a.get_term(b_term)

    def test_term_helpers_are_exact_case_sensitive_and_non_normalizing(self) -> None:
        namespaces = {"Ex": "https://example.invalid/base"}

        self.assertEqual(split_qualified_term("Ex:Item"), ("Ex", "Item"))
        self.assertEqual(
            expand_qualified_term("Ex:Item", namespaces),
            "https://example.invalid/baseItem",
        )
        with self.assertRaises(KeyError):
            expand_qualified_term("ex:Item", namespaces)

    def test_base_vocabulary_is_not_duplicated_as_sdk_authority(self) -> None:
        vocabulary_module = (
            SDK_ROOT / "geesno_semantic" / "terms.py"
        ).read_text(encoding="utf-8")
        base_files = [
            path
            for path in (ROOT / "vocab" / "base").rglob("*")
            if path.is_file()
        ]

        self.assertEqual(base_files, [ROOT / "vocab" / "base" / "README.md"])
        self.assertNotIn("https://geesno.com/vocab/base", vocabulary_module)
        self.assertFalse(hasattr(sdk, "BaseVocabulary"))

    def test_rich_document_preserves_trust_lifecycle_and_opaque_neighbors(self) -> None:
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
        original_payload = document.get_extension("ext:opaque")
        original_numbers = original_payload["numbers"]
        original_tokens = [number.token for number in original_numbers]
        original_trust = deepcopy(document.backing_tree["entities"][0])

        revision = document.set_revision(identifier=identifier(20))
        document.set_history(completeness="partial")
        document.add_change(
            revision=local(revision.identifier),
            targets=[local(document.entities[0].identifier)],
            kind="ex:observed",
        )
        document.entities[0].set_extension("ext:edited", {"value": "explicit"})

        self.assertIs(document.get_extension("ext:opaque"), original_payload)
        self.assertEqual([number.token for number in original_numbers], original_tokens)
        self.assertEqual(
            {key: value for key, value in document.backing_tree["entities"][0].items() if key != "extensions"},
            original_trust,
        )
        self.assertEqual(validate_document(document), {"result": "valid"})

        reloaded = load_bytes(dump_bytes(document))
        reloaded_numbers = reloaded.get_extension("ext:opaque")["numbers"]
        self.assertEqual([number.token for number in reloaded_numbers], original_tokens)
        self.assertEqual(reloaded.entities[0].get_extension("ext:edited"), {"value": "explicit"})
        self.assertEqual(validate_document(reloaded), {"result": "valid"})

    def test_i6_regression_has_no_registry_resolver_i8_or_execution_surface(self) -> None:
        for name in (
            "VocabularyRegistry",
            "VocabularyResolver",
            "ExtensionPlugin",
            "ProfileEvaluator",
            "AiContextBuilder",
            "CompositeProfile",
        ):
            self.assertFalse(hasattr(sdk, name), name)

    def test_s2_regression_totals_remain_unchanged(self) -> None:
        valid, invalid, expected, errors = run_suite()
        self.assertEqual((valid, invalid, expected), (17, 84, 101))
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
