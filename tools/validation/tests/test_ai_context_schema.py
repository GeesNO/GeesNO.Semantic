from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[3]
SCHEMA_PATH = (
    ROOT / "profiles" / "ai-context" / "schema" / "v0.1" / "ai-context.schema.json"
)
S2_SCHEMA_PATH = ROOT / "schema" / "v0.1" / "geesno-semantic.schema.json"
S2_REFERENCE = "../../../../schema/v0.1/geesno-semantic.schema.json"


class AiContextSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.s2_schema = json.loads(S2_SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(cls.schema)
        registry = Registry().with_resource(
            S2_REFERENCE,
            Resource.from_contents(cls.s2_schema),
        )
        cls.validator = Draft202012Validator(cls.schema, registry=registry)

    @staticmethod
    def binding() -> dict[str, object]:
        return {
            "family": "https://geesno.com/binding/ai-context-json",
            "version": "0.1.0",
        }

    @staticmethod
    def profile_edition() -> dict[str, object]:
        return {
            "profile_family": "https://geesno.com/profile/ai-context",
            "profile_version": "0.1.0",
        }

    @classmethod
    def profile_artifact(cls) -> dict[str, object]:
        return {
            "artifact_kind": "profile_requirement_artifact",
            "binding": cls.binding(),
            "profile_edition": cls.profile_edition(),
            "vocabulary_dependencies": [],
            "requirements": [],
        }

    @classmethod
    def projection_artifact(cls) -> dict[str, object]:
        return {
            "artifact_kind": "projection_artifact",
            "binding": cls.binding(),
            "profile_edition": cls.profile_edition(),
            "source_state": {
                "semantic_document_id": "https://example.invalid/documents/source",
                "source_state_descriptor": {},
            },
            "selection_context": {
                "selection_context_kind": "explicit",
                "selection_descriptor": {},
            },
            "projection_scope": {
                "scope_kind": "selected-records",
                "scope_descriptor": {},
            },
            "projection_completeness": "unknown",
            "carried_content": {},
            "reference_availability": [],
        }

    @staticmethod
    def requirement(kind: str, body: dict[str, object]) -> dict[str, object]:
        return {
            "requirement_kind": kind,
            "requirement_mode": "required",
            "applicability": {
                "subject_category": "projection_artifact",
                "basis_kind": "always",
            },
            "requirement_body": body,
        }

    def assert_valid(self, instance: object) -> None:
        errors = list(self.validator.iter_errors(instance))
        self.assertEqual([], errors, "\n".join(error.message for error in errors))

    def assert_invalid(self, instance: object) -> None:
        self.assertNotEqual([], list(self.validator.iter_errors(instance)))

    def test_schema_compiles_and_omits_unapproved_identifier(self) -> None:
        self.assertEqual(
            self.schema["$schema"],
            "https://json-schema.org/draft/2020-12/schema",
        )
        self.assertNotIn("$id", self.schema)
        self.assertEqual(self.schema["x-geesno-status"], "s4-i2-implemented")

    def test_minimal_profile_and_projection_roots_are_valid(self) -> None:
        self.assert_valid(self.profile_artifact())
        self.assert_valid(self.projection_artifact())

    def test_projection_reuses_s2_entity_definition_offline(self) -> None:
        projection = self.projection_artifact()
        projection["carried_content"] = {
            "entities": [
                {
                    "id": "https://example.invalid/entities/one",
                    "kind": "concept",
                }
            ]
        }
        self.assert_valid(projection)

        invalid = copy.deepcopy(projection)
        invalid["carried_content"]["entities"][0]["kind"] = "invented-kind"
        self.assert_invalid(invalid)

    def test_all_eight_requirement_kinds_have_valid_structural_forms(self) -> None:
        bodies = {
            "structure": {"record_category": "entity"},
            "cardinality": {
                "count_target": "entities",
                "count_scope": {},
                "min_count": "0",
            },
            "vocabulary": {
                "term_identity": "https://example.invalid/vocabulary/term"
            },
            "projection": {"completeness_policy": "partial_projection_allowed"},
            "preservation": {
                "preservation_target": {},
                "material_context_policy": "dependency_continuation",
                "dependency_continuation_reference": "profile-rule:dependency",
            },
            "source_binding": {"source_participation": "source_state"},
            "extension": {
                "extension_term": "https://example.invalid/extensions/test",
                "host_category": "entity",
                "extension_handling": "presence",
            },
            "closure": {
                "closure_scope": {},
                "closure_policy": "self_contained",
            },
        }
        artifact = self.profile_artifact()
        artifact["requirements"] = [
            self.requirement(kind, body) for kind, body in bodies.items()
        ]
        self.assert_valid(artifact)

    def test_root_dispatch_and_closed_binding_objects_reject_dialects(self) -> None:
        cases = []

        wrong_family = self.profile_artifact()
        wrong_family["binding"]["family"] = "https://example.invalid/binding"
        cases.append(wrong_family)

        wrong_version = self.profile_artifact()
        wrong_version["binding"]["version"] = "0.2.0"
        cases.append(wrong_version)

        wrong_profile_family = self.profile_artifact()
        wrong_profile_family["profile_edition"]["profile_family"] = (
            "https://example.invalid/profile"
        )
        cases.append(wrong_profile_family)

        unknown_root = self.profile_artifact()
        unknown_root["artifact_kind"] = "unknown_artifact"
        cases.append(unknown_root)

        extra_root_member = self.profile_artifact()
        extra_root_member["overall_outcome"] = "conformant"
        cases.append(extra_root_member)

        composition_member = self.profile_artifact()
        composition_member["components"] = []
        cases.append(composition_member)

        composition_disposition = self.profile_artifact()
        composition_disposition["dispositions"] = []
        cases.append(composition_disposition)

        null_member = self.profile_artifact()
        null_member["artifact_metadata"] = None
        cases.append(null_member)

        latest = self.profile_artifact()
        latest["profile_edition"]["profile_version"] = "latest"
        cases.append(latest)

        for case in cases:
            with self.subTest(case=case):
                self.assert_invalid(case)

    def test_requirement_dispatch_rejects_unknown_or_mismatched_bodies(self) -> None:
        cases = []

        unknown_kind = self.profile_artifact()
        unknown_kind["requirements"] = [self.requirement("unknown", {})]
        cases.append(unknown_kind)

        mismatched = self.profile_artifact()
        mismatched["requirements"] = [
            self.requirement("closure", {"record_category": "entity"})
        ]
        cases.append(mismatched)

        unknown_body_member = self.profile_artifact()
        unknown_body_member["requirements"] = [
            self.requirement("structure", {"record_category": "entity", "extra": True})
        ]
        cases.append(unknown_body_member)

        bad_mode = self.profile_artifact()
        requirement = self.requirement("structure", {"record_category": "entity"})
        requirement["requirement_mode"] = "recommended"
        bad_mode["requirements"] = [requirement]
        cases.append(bad_mode)

        for case in cases:
            with self.subTest(case=case):
                self.assert_invalid(case)

    def test_requirement_body_conditionals_are_enforced(self) -> None:
        cases = []

        exact_and_min = self.profile_artifact()
        exact_and_min["requirements"] = [
            self.requirement(
                "cardinality",
                {
                    "count_target": "entities",
                    "count_scope": {},
                    "min_count": "0",
                    "exact_count": "1",
                },
            )
        ]
        cases.append(exact_and_min)

        incomplete_vocabulary = self.profile_artifact()
        incomplete_vocabulary["requirements"] = [
            self.requirement(
                "vocabulary",
                {"vocabulary_family": "https://example.invalid/vocabulary"},
            )
        ]
        cases.append(incomplete_vocabulary)

        empty_alternatives = self.profile_artifact()
        empty_alternatives["requirements"] = [
            self.requirement(
                "vocabulary",
                {
                    "term_identity": "https://example.invalid/vocabulary/term",
                    "allowed_alternative_exact_edition": [],
                },
            )
        ]
        cases.append(empty_alternatives)

        descriptor_instead_of_profile_token = self.profile_artifact()
        descriptor_instead_of_profile_token["requirements"] = [
            self.requirement(
                "preservation",
                {
                    "preservation_target": {},
                    "material_context_policy": "dependency_continuation",
                    "dependency_continuation_reference": {"descriptor_id": "d1"},
                },
            )
        ]
        cases.append(descriptor_instead_of_profile_token)

        misplaced_payload_constraint = self.profile_artifact()
        misplaced_payload_constraint["requirements"] = [
            self.requirement(
                "extension",
                {
                    "extension_term": "https://example.invalid/extensions/test",
                    "host_category": "entity",
                    "extension_handling": "presence",
                    "payload_constraint_reference": "constraint:one",
                },
            )
        ]
        cases.append(misplaced_payload_constraint)

        for case in cases:
            with self.subTest(case=case):
                self.assert_invalid(case)

    def test_projection_structural_conditionals_are_enforced(self) -> None:
        cases = []

        missing_state_anchor = self.projection_artifact()
        missing_state_anchor["source_state"].pop("source_state_descriptor")
        cases.append(missing_state_anchor)

        invalid_completeness = self.projection_artifact()
        invalid_completeness["projection_completeness"] = "bounded"
        cases.append(invalid_completeness)

        truncated_unknown = self.projection_artifact()
        truncated_unknown["truncation"] = {
            "truncation_established": True,
            "affected_scope": {},
        }
        cases.append(truncated_unknown)

        empty_descriptor_group = self.projection_artifact()
        empty_descriptor_group["boundedness"] = []
        cases.append(empty_descriptor_group)

        untargeted_omission = self.projection_artifact()
        untargeted_omission["omissions"] = [{"omission_category": "material-context"}]
        cases.append(untargeted_omission)

        unknown_descriptor_group = self.projection_artifact()
        unknown_descriptor_group["diagnostics"] = []
        cases.append(unknown_descriptor_group)

        profile_requirements_in_projection = self.projection_artifact()
        profile_requirements_in_projection["requirements"] = []
        cases.append(profile_requirements_in_projection)

        for case in cases:
            with self.subTest(case=case):
                self.assert_invalid(case)

    def test_descriptor_references_are_restricted_to_their_named_groups(self) -> None:
        valid = self.projection_artifact()
        valid["projection_completeness"] = "partial"
        valid["boundedness"] = [
            {
                "descriptor_id": "bound-one",
                "bound_dimension": "records",
                "bound_rule": "maximum",
                "limit_value": "100",
                "bound_reached": True,
            }
        ]
        valid["truncation"] = {
            "truncation_established": True,
            "affected_scope": {},
            "bound_reference": {
                "descriptor_group": "boundedness",
                "descriptor_id": "bound-one",
            },
        }
        self.assert_valid(valid)

        wrong_bound_group = copy.deepcopy(valid)
        wrong_bound_group["truncation"]["bound_reference"][
            "descriptor_group"
        ] = "omissions"
        self.assert_invalid(wrong_bound_group)

        wrong_dependency_group = self.projection_artifact()
        wrong_dependency_group["omissions"] = [
            {
                "omitted_category": "context",
                "omission_category": "material-context",
                "dependency_continuation_reference": {
                    "descriptor_group": "projection_continuations",
                    "descriptor_id": "continuation-one",
                },
            }
        ]
        self.assert_invalid(wrong_dependency_group)

        unknown_group = copy.deepcopy(wrong_dependency_group)
        unknown_group["omissions"][0]["dependency_continuation_reference"][
            "descriptor_group"
        ] = "unknown_group"
        self.assert_invalid(unknown_group)

    def test_profile_defined_values_are_non_null_but_may_contain_null(self) -> None:
        valid = self.profile_artifact()
        requirement = self.requirement("structure", {"record_category": "entity"})
        requirement["applicability"]["expected_value"] = {"nested": None}
        valid["requirements"] = [requirement]
        self.assert_valid(valid)

        invalid = copy.deepcopy(valid)
        invalid["requirements"][0]["applicability"]["expected_value"] = None
        self.assert_invalid(invalid)


if __name__ == "__main__":
    unittest.main()
