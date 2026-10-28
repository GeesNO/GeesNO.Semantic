from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from tools.validation import check_repository


RUNNER = check_repository.ROOT / "conformance" / "runner"
if str(RUNNER) not in sys.path:
    sys.path.insert(0, str(RUNNER))

from fixture_runner import (  # noqa: E402
    CONFORMANCE,
    SCHEMA_PATH,
    run_suite,
    validate_bytes,
)
from raw_parse import RawInputError, RawNumber, dump_preserving_numbers, parse_bytes  # noqa: E402
from schema_validation import SchemaValidationError, load_schema, validate as schema_validate  # noqa: E402
from semantic_validation import SemanticChecker, SemanticValidationError  # noqa: E402


def raw_tokens(value: Any) -> list[str]:
    if isinstance(value, RawNumber):
        return [value.token]
    if isinstance(value, list):
        return [token for item in value for token in raw_tokens(item)]
    if isinstance(value, dict):
        return [token for item in value.values() for token in raw_tokens(item)]
    return []


class S2ConformanceBaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load_schema(SCHEMA_PATH)

    def test_schema_satisfies_draft_2020_12_metaschema(self) -> None:
        Draft202012Validator.check_schema(self.schema)

    def test_complete_fixture_suite_matches_expected_outcomes(self) -> None:
        valid, invalid, expected, errors = run_suite()
        self.assertEqual((valid, invalid, expected), (17, 84, 101))
        self.assertEqual(errors, [])

    def test_reference_array_target_uniqueness_is_caller_specific(self) -> None:
        target = "https://example.invalid/records/repeated"
        references = [
            {"target": target, "location": "out-of-document"},
            {"target": target, "location": "out-of-document"},
        ]
        checker = SemanticChecker(
            {
                "spec_version": "0.1.0",
                "id": "https://example.invalid/documents/reference-helper",
                "scope": {"completeness": "partial"},
            }
        )
        self.assertEqual(checker.check_reference_array(references), [target, target])
        with self.assertRaises(SemanticValidationError) as caught:
            checker.check_reference_array(references, unique_targets=True)
        self.assertEqual(caught.exception.category, "repeated-reference")

        explicit_fixture_cases = (
            "semantic-repeated-parent.json",
            "semantic-repeated-supersedes.json",
        )
        for name in explicit_fixture_cases:
            with self.subTest(role=name):
                outcome = validate_bytes(
                    (CONFORMANCE / "invalid" / name).read_bytes(), self.schema
                )
                self.assertEqual(
                    (outcome["result"], outcome["layer"], outcome["category"]),
                    ("invalid", 3, "repeated-reference"),
                )

        provenance_document = json.loads(
            (CONFORMANCE / "valid" / "sources-and-bindings.json").read_text(encoding="utf-8")
        )
        source_id = provenance_document["sources"][0]["id"]
        source_reference = {"target": source_id, "location": "in-document"}
        provenance_document["entities"][0]["provenance"] = [
            {
                "kind": "ex:observed",
                "sources": [source_reference, source_reference],
            }
        ]

        change_document = json.loads(
            (CONFORMANCE / "valid" / "partial-history-changes.json").read_text(encoding="utf-8")
        )
        change_target = change_document["history"]["changes"][0]["targets"][0]
        change_document["history"]["changes"][0]["targets"].append(change_target)

        for role, document in (
            ("Provenance.sources", provenance_document),
            ("Change.targets", change_document),
        ):
            with self.subTest(role=role):
                outcome = validate_bytes(json.dumps(document).encode("utf-8"), self.schema)
                self.assertEqual(
                    (outcome["result"], outcome["layer"], outcome["category"]),
                    ("invalid", 3, "repeated-reference"),
                )

    def test_anonymous_scoped_trust_without_addressability_remains_valid(self) -> None:
        document = {
            "spec_version": "0.1.0",
            "id": "https://example.invalid/documents/anonymous-scoped-trust",
            "scope": {"completeness": "partial"},
            "namespaces": {"ex": "https://example.invalid/terms/"},
            "entities": [
                {
                    "id": "https://example.invalid/entities/anonymous-scoped-trust",
                    "kind": "concept",
                    "reviews": [{"disposition": "ex:observed"}],
                }
            ],
        }
        self.assertEqual(
            validate_bytes(json.dumps(document).encode("utf-8"), self.schema),
            {"result": "valid"},
        )

    def test_id_based_graph_and_tombstone_rules_ignore_reference_location(self) -> None:
        cases = {
            "semantic-revision-self-parent.json": "revision-self-parent",
            "semantic-self-supersession.json": "self-supersession",
            "semantic-revision-cycle.json": "revision-cycle",
            "semantic-supersession-cycle.json": "supersession-cycle",
            "semantic-live-tombstone.json": "live-tombstone",
        }

        def mark_references_out_of_document(value: Any) -> None:
            if isinstance(value, dict):
                if "target" in value and "location" in value:
                    value["location"] = "out-of-document"
                for child in value.values():
                    mark_references_out_of_document(child)
            elif isinstance(value, list):
                for child in value:
                    mark_references_out_of_document(child)

        for name, category in cases.items():
            document = json.loads(
                (CONFORMANCE / "invalid" / name).read_text(encoding="utf-8")
            )
            mark_references_out_of_document(document)
            with self.subTest(path=name):
                outcome = validate_bytes(json.dumps(document).encode("utf-8"), self.schema)
                self.assertEqual(
                    (outcome["result"], outcome["layer"], outcome["category"]),
                    ("invalid", 3, category),
                )

    def test_iterative_cycle_check_accepts_1800_revision_parent_chain(self) -> None:
        revisions = []
        for index in range(1800):
            revision = {"id": f"https://example.invalid/revisions/{index}"}
            if index:
                revision["parents"] = [
                    {
                        "target": f"https://example.invalid/revisions/{index - 1}",
                        "location": "in-document",
                    }
                ]
            revisions.append(revision)
        document = {
            "spec_version": "0.1.0",
            "id": "https://example.invalid/documents/long-revision-chain",
            "scope": {"completeness": "partial"},
            "history": {"completeness": "partial", "revisions": revisions},
        }
        self.assertEqual(
            validate_bytes(json.dumps(document).encode("utf-8"), self.schema),
            {"result": "valid"},
        )

    def test_expected_suite_exercises_every_processing_layer(self) -> None:
        outcomes = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in (CONFORMANCE / "expected").glob("*.json")
        ]
        invalid_layers = {
            outcome["layer"]
            for outcome in outcomes
            if outcome["result"] in {"invalid", "unsupported-version", "resource-refusal"}
        }
        self.assertEqual(invalid_layers, {0, 1, 2, 3})
        self.assertTrue(any(outcome["result"] == "unsupported-version" for outcome in outcomes))
        self.assertTrue(any(outcome["result"] == "resource-refusal" for outcome in outcomes))

    def test_every_valid_fixture_passes_layers_zero_through_three(self) -> None:
        for path in sorted((CONFORMANCE / "valid").glob("*.json")):
            with self.subTest(path=path.name):
                self.assertEqual(
                    validate_bytes(path.read_bytes(), self.schema),
                    {"result": "valid"},
                )

    def test_every_layer_two_fixture_fails_at_layer_two(self) -> None:
        for expected_path in sorted((CONFORMANCE / "expected").glob("*.json")):
            expected = json.loads(expected_path.read_text(encoding="utf-8"))
            if expected.get("layer") != 2:
                continue
            fixture_path = CONFORMANCE / "invalid" / f"{expected_path.stem}.json"
            with self.subTest(path=fixture_path.name):
                self.assertEqual(validate_bytes(fixture_path.read_bytes(), self.schema)["layer"], 2)

    def test_composed_assertion_branches_and_unknown_members_are_closed(self) -> None:
        for name in (
            "schema-assertion-branch-leak.json",
            "schema-unknown-root.json",
            "schema-unknown-entity.json",
            "schema-inline-assertion-shortcut.json",
        ):
            with self.subTest(path=name):
                outcome = validate_bytes((CONFORMANCE / "invalid" / name).read_bytes(), self.schema)
                self.assertEqual((outcome["result"], outcome["layer"]), ("invalid", 2))

    def test_every_assertion_branch_rejects_members_from_another_branch(self) -> None:
        document = json.loads(
            (CONFORMANCE / "valid" / "assertions-and-values.json").read_text(encoding="utf-8")
        )
        leaks = {
            "type": ("property", "test:leak"),
            "property": ("predicate", "test:leak"),
            "relation": ("concept", document["assertions"][0]["subject"]),
            "concept_representation": ("type", "test:leak"),
        }
        exercised: set[str] = set()
        for index, assertion in enumerate(document["assertions"]):
            kind = assertion["kind"]
            if kind in exercised:
                continue
            exercised.add(kind)
            mutated = json.loads(json.dumps(document))
            member, value = leaks[kind]
            mutated["assertions"][index][member] = value
            with self.subTest(kind=kind):
                outcome = validate_bytes(json.dumps(mutated).encode("utf-8"), self.schema)
                self.assertEqual((outcome["result"], outcome["layer"]), ("invalid", 2))
        self.assertEqual(exercised, set(leaks))

    def test_extension_and_empty_container_boundaries(self) -> None:
        self.assertEqual(
            validate_bytes(
                (CONFORMANCE / "valid" / "unknown-extension-numbers.json").read_bytes(),
                self.schema,
            ),
            {"result": "valid"},
        )
        for name in (
            "schema-extension-forbidden-host.json",
            "schema-empty-extensions.json",
            "schema-empty-namespaces.json",
            "schema-empty-root-collection.json",
            "schema-empty-parents.json",
        ):
            with self.subTest(path=name):
                outcome = validate_bytes((CONFORMANCE / "invalid" / name).read_bytes(), self.schema)
                self.assertEqual((outcome["result"], outcome["layer"]), ("invalid", 2))

    def test_full_iri_validation_accepts_unicode_and_rejects_bad_syntax(self) -> None:
        valid = {
            "spec_version": "0.1.0",
            "id": "https://example.invalid/identidad/mañana",
            "scope": {"completeness": "partial"},
        }
        self.assertEqual(
            validate_bytes(json.dumps(valid, ensure_ascii=False).encode("utf-8"), self.schema),
            {"result": "valid"},
        )
        invalid = {**valid, "id": "https://example.invalid/[bad"}
        outcome = validate_bytes(json.dumps(invalid).encode("utf-8"), self.schema)
        self.assertEqual((outcome["result"], outcome["layer"]), ("invalid", 3))

    def test_schema_itself_requires_exact_instance_contract_version(self) -> None:
        document = {
            "spec_version": "0.1.0-dev",
            "id": "urn:uuid:00000000-0000-4000-8000-000000008000",
            "scope": {"completeness": "partial"},
        }
        with self.assertRaises(SchemaValidationError):
            schema_validate(document, self.schema)

    def test_unicode_surrogate_pair_and_decoded_duplicate_handling(self) -> None:
        valid = (
            '{"spec_version":"0.1.0",'
            '"id":"urn:uuid:00000000-0000-4000-8000-000000008100",'
            '"scope":{"completeness":"partial"},'
            '"namespaces":{"ext":"https://example.invalid/extensions/"},'
            '"extensions":{"ext:data":"\\ud834\\udd1e"}}'
        ).encode("ascii")
        self.assertEqual(validate_bytes(valid, self.schema), {"result": "valid"})

        duplicate = (
            '{"spec_version":"0.1.0",'
            '"id":"urn:uuid:00000000-0000-4000-8000-000000008101",'
            '"\\u0069d":"urn:uuid:00000000-0000-4000-8000-000000008102",'
            '"scope":{"completeness":"partial"}}'
        ).encode("ascii")
        with self.assertRaises(RawInputError) as caught:
            parse_bytes(duplicate)
        self.assertEqual(caught.exception.category, "duplicate-member")

    def test_unknown_extension_number_tokens_round_trip_exactly(self) -> None:
        path = CONFORMANCE / "valid" / "unknown-extension-numbers.json"
        first = parse_bytes(path.read_bytes())
        expected = ["1", "1.0", "1e0", "1E+0", "-0", "9007199254740993", "1e100000"]
        self.assertEqual(raw_tokens(first), expected)
        serialized = dump_preserving_numbers(first).encode("utf-8")
        second = parse_bytes(serialized)
        self.assertEqual(raw_tokens(second), expected)
        self.assertEqual(validate_bytes(serialized, self.schema), {"result": "valid"})

    def test_integer_and_decimal_with_equal_magnitude_are_distinct_set_values(self) -> None:
        document = {
            "spec_version": "0.1.0",
            "id": "urn:uuid:00000000-0000-4000-8000-000000009000",
            "scope": {"completeness": "partial"},
            "namespaces": {"test": "https://example.invalid/test/"},
            "entities": [
                {
                    "id": "urn:uuid:00000000-0000-4000-8000-000000009001",
                    "kind": "concept",
                }
            ],
            "assertions": [
                {
                    "id": "urn:uuid:00000000-0000-4000-8000-000000009002",
                    "kind": "property",
                    "subject": {
                        "target": "urn:uuid:00000000-0000-4000-8000-000000009001",
                        "location": "in-document",
                    },
                    "property": "test:values",
                    "value": {
                        "kind": "set",
                        "items": [
                            {"kind": "integer", "value": "42"},
                            {"kind": "decimal", "coefficient": "42", "exponent": "0"},
                        ],
                    },
                }
            ],
        }
        data = json.dumps(document, ensure_ascii=False).encode("utf-8")
        self.assertEqual(validate_bytes(data, self.schema), {"result": "valid"})

    def test_recursive_resource_policy_is_not_semantic_invalidity(self) -> None:
        path = CONFORMANCE / "invalid" / "raw-resource-refusal.raw"
        self.assertEqual(
            validate_bytes(path.read_bytes(), self.schema),
            {"result": "resource-refusal", "layer": 0, "category": "nesting-limit"},
        )

    def test_provisional_example_documents_remain_bare_core_valid(self) -> None:
        for relative in (
            "examples/json-provisional/cross-domain.md",
            "examples/json-provisional/minimal-cases.md",
        ):
            text = (check_repository.ROOT / relative).read_text(encoding="utf-8")
            for index, block in enumerate(check_repository.FENCED_JSON.findall(text), 1):
                with self.subTest(document=relative, block=index):
                    self.assertEqual(
                        validate_bytes(block.encode("utf-8"), self.schema),
                        {"result": "valid"},
                    )


if __name__ == "__main__":
    unittest.main()
