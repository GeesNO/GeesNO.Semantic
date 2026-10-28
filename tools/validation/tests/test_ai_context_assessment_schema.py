from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[3]
S2_RUNNER = ROOT / "conformance" / "runner"
if str(S2_RUNNER) not in sys.path:
    sys.path.insert(0, str(S2_RUNNER))

from semantic_validation import SemanticChecker, SemanticValidationError  # noqa: E402


SCHEMA_PATH = (
    ROOT
    / "profiles"
    / "ai-context"
    / "schema"
    / "v0.1"
    / "ai-context-assessment.schema.json"
)
S2_SCHEMA_PATH = ROOT / "schema" / "v0.1" / "geesno-semantic.schema.json"
S2_REFERENCE = "../../../../schema/v0.1/geesno-semantic.schema.json"


class AiContextAssessmentSchemaTests(unittest.TestCase):
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
    def local_reference(local_ref: str = "subject") -> dict[str, str]:
        return {"scope_ref": "assessment", "local_ref": local_ref}

    @staticmethod
    def stable_requirement_ref() -> dict[str, str]:
        return {
            "reference_strategy": "stable_requirement_reference",
            "requirement_id": "projection-baseline",
        }

    @classmethod
    def minimal_result(cls) -> dict[str, object]:
        return {
            "binding": {
                "family": (
                    "https://geesno.com/binding/ai-context-assessment-json"
                ),
                "version": "0.1.0",
            },
            "artifact_kind": "conformance_result_artifact",
            "profile_edition": {
                "profile_family": "https://geesno.com/profile/ai-context",
                "profile_version": "0.1.0",
            },
            "assessment_subject": {
                "subject_role": "projection_artifact",
                "reference_strategy": "stable_artifact_identity",
                "artifact_id": "https://example.invalid/projections/one",
            },
            "overall_outcome": "conformant",
            "requirement_results": [
                {
                    "requirement_ref": cls.stable_requirement_ref(),
                    "outcome": "satisfied",
                }
            ],
        }

    def assert_valid(self, instance: object) -> None:
        errors = self.validation_errors(instance)
        self.assertEqual([], errors, "\n".join(str(error) for error in errors))

    def assert_invalid(self, instance: object) -> None:
        self.assertNotEqual([], self.validation_errors(instance))

    def validation_errors(self, instance: object) -> list[Exception]:
        schema_errors = list(self.validator.iter_errors(instance))
        if schema_errors or not isinstance(instance, dict):
            return schema_errors

        metadata = instance.get("assessor_metadata")
        if not isinstance(metadata, dict):
            return []
        timestamp = metadata.get("assessment_timestamp")
        if not isinstance(timestamp, str):
            return []

        try:
            SemanticChecker({}).check_temporal("date_time", timestamp)
        except SemanticValidationError as error:
            return [error]
        return []

    def test_schema_meta_validates_and_uses_exact_binding(self) -> None:
        self.assertEqual(
            "https://json-schema.org/draft/2020-12/schema",
            self.schema["$schema"],
        )
        self.assertNotIn("$id", self.schema)
        self.assertEqual("s5-i2-implemented", self.schema["x-geesno-status"])
        self.assert_valid(self.minimal_result())

        for member, value in (
            ("family", "https://geesno.com/binding/ai-context-json"),
            ("version", "latest"),
        ):
            invalid = self.minimal_result()
            invalid["binding"][member] = value
            self.assert_invalid(invalid)

    def test_root_is_closed_and_has_exact_kind_profile_and_outcomes(self) -> None:
        result = self.minimal_result()
        result["assessment_result_id"] = (
            "https://example.invalid/assessment-results/one"
        )
        self.assert_valid(result)

        mutations = []
        for member, value in (
            ("artifact_kind", "projection_artifact"),
            ("overall_outcome", "passed"),
        ):
            invalid = copy.deepcopy(result)
            invalid[member] = value
            mutations.append(invalid)

        invalid = copy.deepcopy(result)
        invalid["profile_edition"]["profile_version"] = "latest"
        mutations.append(invalid)
        invalid = copy.deepcopy(result)
        invalid["unknown"] = True
        mutations.append(invalid)
        invalid = copy.deepcopy(result)
        invalid["assessment_result_id"] = "not an iri"
        mutations.append(invalid)

        for mutation in mutations:
            self.assert_invalid(mutation)

    def test_assessment_subject_variants_are_closed_and_exclusive(self) -> None:
        local = self.minimal_result()
        local["assessment_subject"] = {
            "subject_role": "semantic_document",
            "reference_strategy": "assessment_local_artifact_reference",
            "local_reference": self.local_reference(),
        }
        local["reference_scope"] = {
            "scope_ref": "assessment",
            "scope_kind": "assessment_package_scope",
        }
        self.assert_valid(local)

        coupled = copy.deepcopy(local)
        coupled["assessment_subject"] = {
            "subject_role": "profile_requirement_artifact",
            "reference_strategy": "coupled_subject",
            "coupled_occurrence_ref": self.local_reference(),
        }
        coupled["reference_scope"]["scope_kind"] = "explicit_coupling_scope"
        self.assert_valid(coupled)

        no_scope = copy.deepcopy(local)
        del no_scope["reference_scope"]
        self.assert_invalid(no_scope)
        wrong_coupling_scope = copy.deepcopy(coupled)
        wrong_coupling_scope["reference_scope"]["scope_kind"] = (
            "assessment_package_scope"
        )
        self.assert_invalid(wrong_coupling_scope)
        contradictory = copy.deepcopy(local)
        contradictory["assessment_subject"]["artifact_id"] = (
            "https://example.invalid/projections/two"
        )
        self.assert_invalid(contradictory)

    def test_profile_artifact_reference_variants_and_locator_context(self) -> None:
        stable = self.minimal_result()
        stable["profile_requirement_artifact_reference"] = {
            "reference_strategy": "stable_artifact_identity",
            "artifact_id": "https://example.invalid/profiles/artifact",
        }
        self.assert_valid(stable)

        locator = self.minimal_result()
        locator["requirement_results"][0]["requirement_ref"] = {
            "reference_strategy": "locator_occurrence_reference",
            "requirement_locator": "/requirements/0",
        }
        self.assert_invalid(locator)

        locator["profile_requirement_artifact_reference"] = copy.deepcopy(
            stable["profile_requirement_artifact_reference"]
        )
        self.assert_valid(locator)

        package_locator = copy.deepcopy(locator)
        del package_locator["profile_requirement_artifact_reference"]
        package_locator["reference_scope"] = {
            "scope_ref": "assessment",
            "scope_kind": "assessment_package_scope",
        }
        self.assert_valid(package_locator)

        local = copy.deepcopy(stable)
        local["profile_requirement_artifact_reference"] = {
            "reference_strategy": "assessment_local_artifact_reference",
            "local_reference": self.local_reference("profile"),
        }
        self.assert_invalid(local)
        local["reference_scope"] = package_locator["reference_scope"]
        self.assert_valid(local)

        coupled = copy.deepcopy(stable)
        coupled["profile_requirement_artifact_reference"] = {
            "reference_strategy": "coupled_profile_requirement_artifact",
            "coupled_occurrence_ref": self.local_reference("profile"),
        }
        coupled["reference_scope"] = {
            "scope_ref": "assessment",
            "scope_kind": "explicit_coupling_scope",
        }
        self.assert_valid(coupled)
        wrong_scope = copy.deepcopy(coupled)
        wrong_scope["reference_scope"]["scope_kind"] = "assessment_package_scope"
        self.assert_invalid(wrong_scope)
        contradictory = copy.deepcopy(coupled)
        contradictory["profile_requirement_artifact_reference"]["artifact_id"] = (
            "https://example.invalid/profiles/artifact"
        )
        self.assert_invalid(contradictory)

    def test_requirement_reference_union_is_closed_and_exclusive(self) -> None:
        stable = self.minimal_result()
        self.assert_valid(stable)

        locator = copy.deepcopy(stable)
        locator["requirement_results"][0]["requirement_ref"] = {
            "reference_strategy": "locator_occurrence_reference",
            "requirement_locator": "requirement:0",
        }
        locator["profile_requirement_artifact_reference"] = {
            "reference_strategy": "stable_artifact_identity",
            "artifact_id": "https://example.invalid/profiles/artifact",
        }
        self.assert_valid(locator)

        ambiguous = copy.deepcopy(locator)
        ambiguous["requirement_results"][0]["requirement_ref"][
            "requirement_id"
        ] = "projection-baseline"
        self.assert_invalid(ambiguous)
        empty_locator = copy.deepcopy(locator)
        empty_locator["requirement_results"][0]["requirement_ref"][
            "requirement_locator"
        ] = ""
        self.assert_invalid(empty_locator)

    def test_diagnostic_locator_requirement_needs_profile_context(self) -> None:
        result = self.minimal_result()
        result["diagnostics"] = [
            {
                "diagnostic_code": "unresolved_requirement_reference",
                "diagnostic_category": "requirement_reference",
                "requirement_ref": {
                    "reference_strategy": "locator_occurrence_reference",
                    "requirement_locator": "requirement:missing",
                },
            }
        ]
        self.assert_invalid(result)

        result["reference_scope"] = {
            "scope_ref": "assessment",
            "scope_kind": "assessment_package_scope",
        }
        self.assert_valid(result)

    def test_requirement_results_and_empty_enumeration_rule(self) -> None:
        outcomes = (
            "satisfied",
            "violated",
            "not_applicable",
            "unsupported",
            "unavailable",
        )
        for outcome in outcomes:
            result = self.minimal_result()
            result["requirement_results"][0]["outcome"] = outcome
            self.assert_valid(result)

        empty = self.minimal_result()
        empty["overall_outcome"] = "indeterminate"
        empty["requirement_results"] = []
        self.assert_invalid(empty)
        empty["diagnostics"] = [
            {
                "diagnostic_code": "assessment_input_uninterpretable",
                "diagnostic_category": "assessment_input",
            }
        ]
        self.assert_valid(empty)

        invalid = self.minimal_result()
        invalid["requirement_results"][0]["outcome"] = "failed"
        self.assert_invalid(invalid)
        invalid = self.minimal_result()
        invalid["requirement_results"][0]["requirement_mode"] = "required"
        self.assert_invalid(invalid)

    def test_result_local_references_require_scope_and_nonempty_arrays(self) -> None:
        result = self.minimal_result()
        result["requirement_results"][0]["requirement_result_ref"] = (
            self.local_reference("result")
        )
        result["requirement_results"][0]["diagnostic_refs"] = [
            self.local_reference("diagnostic")
        ]
        result["diagnostics"] = [
            {
                "diagnostic_ref": self.local_reference("diagnostic"),
                "diagnostic_code": "requirement_violated",
                "diagnostic_category": "requirement_evaluation",
            }
        ]
        self.assert_invalid(result)
        result["reference_scope"] = {
            "scope_ref": "assessment",
            "scope_kind": "result_artifact_scope",
        }
        self.assert_valid(result)

        for array_path in ("diagnostic_refs",):
            invalid = copy.deepcopy(result)
            invalid["requirement_results"][0][array_path] = []
            self.assert_invalid(invalid)
        invalid = copy.deepcopy(result)
        invalid["diagnostics"] = []
        self.assert_invalid(invalid)

    def test_diagnostic_taxonomy_pairs_and_severity_are_exact(self) -> None:
        pairs = (
            ("requirement_violated", "requirement_evaluation"),
            ("requirement_unsupported", "requirement_evaluation"),
            ("dependency_unavailable", "dependency_availability"),
            ("requirement_not_applicable", "requirement_evaluation"),
            ("invalid_binding_construct", "binding_structure"),
            ("unsupported_binding_construct", "binding_structure"),
            ("contradictory_projection_metadata", "binding_structure"),
            ("exact_vocabulary_unavailable", "dependency_availability"),
            (
                "profile_requirement_artifact_unavailable",
                "dependency_availability",
            ),
            ("unresolved_requirement_reference", "requirement_reference"),
            ("missing_namespace_expansion_context", "binding_structure"),
            (
                "invalid_reference_availability_consistency",
                "binding_structure",
            ),
            (
                "invalid_source_state_reference_preservation",
                "binding_structure",
            ),
            ("structural_validation_failed", "binding_structure"),
            ("assessment_input_uninterpretable", "assessment_input"),
        )
        for code, category in pairs:
            result = self.minimal_result()
            result["diagnostics"] = [
                {
                    "diagnostic_code": code,
                    "diagnostic_category": category,
                    "diagnostic_severity": "warning",
                }
            ]
            self.assert_valid(result)

            invalid = copy.deepcopy(result)
            invalid["diagnostics"][0]["diagnostic_category"] = "assessment_input"
            if category == "assessment_input":
                invalid["diagnostics"][0]["diagnostic_category"] = (
                    "binding_structure"
                )
            self.assert_invalid(invalid)

        invalid = self.minimal_result()
        invalid["diagnostics"] = [
            {
                "diagnostic_code": "requirement_violated",
                "diagnostic_category": "requirement_evaluation",
                "diagnostic_severity": "fatal",
            }
        ]
        self.assert_invalid(invalid)

    def test_subject_and_related_reference_unions_are_typed(self) -> None:
        result = self.minimal_result()
        result["diagnostics"] = [
            {
                "diagnostic_ref": self.local_reference("diagnostic"),
                "diagnostic_code": "requirement_violated",
                "diagnostic_category": "requirement_evaluation",
                "subject_ref": {
                    "reference_strategy": "stable_artifact_identity",
                    "artifact_id": "https://example.invalid/projections/one",
                },
                "related_refs": [
                    {
                        "related_ref_kind": "assessment_record",
                        "local_reference": self.local_reference("result"),
                    },
                    {
                        "related_ref_kind": "subject",
                        "subject_ref": {
                            "reference_strategy": "stable_artifact_identity",
                            "artifact_id": (
                                "https://example.invalid/projections/one"
                            ),
                        },
                    },
                    {
                        "related_ref_kind": "requirement",
                        "requirement_ref": self.stable_requirement_ref(),
                    },
                    {
                        "related_ref_kind": "requirement_result",
                        "requirement_result_ref": self.local_reference("result"),
                    },
                    {
                        "related_ref_kind": "diagnostic",
                        "diagnostic_ref": self.local_reference("diagnostic"),
                    },
                ],
            }
        ]
        result["reference_scope"] = {
            "scope_ref": "assessment",
            "scope_kind": "result_artifact_scope",
        }
        self.assert_valid(result)

        ambiguous = copy.deepcopy(result)
        ambiguous["diagnostics"][0]["related_refs"][0]["subject_ref"] = {
            "reference_strategy": "stable_artifact_identity",
            "artifact_id": "https://example.invalid/projections/one",
        }
        self.assert_invalid(ambiguous)
        strings = copy.deepcopy(result)
        strings["diagnostics"][0]["related_refs"] = ["result"]
        self.assert_invalid(strings)

    def test_local_subject_reference_requires_scope(self) -> None:
        result = self.minimal_result()
        result["diagnostics"] = [
            {
                "diagnostic_code": "assessment_input_uninterpretable",
                "diagnostic_category": "assessment_input",
                "subject_ref": {
                    "reference_strategy": "assessment_local_artifact_reference",
                    "local_reference": self.local_reference("subject"),
                },
            }
        ]
        self.assert_invalid(result)
        result["reference_scope"] = {
            "scope_ref": "assessment",
            "scope_kind": "assessment_package_scope",
        }
        self.assert_valid(result)
        invalid = copy.deepcopy(result)
        invalid["reference_scope"]["scope_kind"] = "result_artifact_scope"
        self.assert_invalid(invalid)

    def test_scope_token_equality_and_resolution_remain_semantic(self) -> None:
        result = self.minimal_result()
        result["assessment_subject"] = {
            "subject_role": "projection_artifact",
            "reference_strategy": "assessment_local_artifact_reference",
            "local_reference": {
                "scope_ref": "different-scope",
                "local_ref": "subject",
            },
        }
        result["reference_scope"] = {
            "scope_ref": "assessment",
            "scope_kind": "assessment_package_scope",
        }

        # Draft 2020-12 has no portable cross-instance equality/resolution rule.
        # The later deterministic semantic layer must reject this mismatch.
        self.assert_valid(result)

    def test_context_null_and_metadata_boundaries(self) -> None:
        result = self.minimal_result()
        result["assessment_context"] = {
            "context_entries": [
                {
                    "context_key": "selection-context",
                    "context_value": {"nested": None},
                }
            ]
        }
        result["assessor_metadata"] = {
            "assessor_id": "https://example.invalid/assessors/reference",
            "implementation_name": "repository checker",
            "implementation_version": "0.1.0-dev",
            "assessment_timestamp": "2026-10-03T12:34:56.123Z",
        }
        self.assert_valid(result)

        invalid = copy.deepcopy(result)
        invalid["assessment_context"]["context_entries"][0]["context_value"] = None
        self.assert_invalid(invalid)
        invalid = copy.deepcopy(result)
        invalid["assessment_context"]["context_entries"] = []
        self.assert_invalid(invalid)
        invalid = copy.deepcopy(result)
        invalid["assessor_metadata"] = {}
        self.assert_invalid(invalid)
        invalid = copy.deepcopy(result)
        invalid["assessor_metadata"]["assessment_timestamp"] = (
            "2026-10-03T12:34:56.120Z"
        )
        self.assert_invalid(invalid)

    def test_assessment_timestamp_reuses_s2_layered_validation(self) -> None:
        valid_timestamps = (
            "2024-02-29T12:34:56Z",
            "2026-10-03T12:34:56Z",
            "2026-10-03T12:34:56.123Z",
        )
        invalid_timestamps = (
            "2025-02-29T12:34:56Z",
            "2026-13-01T12:34:56Z",
            "2026-00-01T12:34:56Z",
            "2026-04-31T12:34:56Z",
            "2026-10-03T24:00:00Z",
            "2026-10-03T12:34:56.120Z",
        )

        for timestamp in valid_timestamps:
            with self.subTest(timestamp=timestamp):
                result = self.minimal_result()
                result["assessor_metadata"] = {
                    "assessment_timestamp": timestamp,
                }
                self.assert_valid(result)

        for timestamp in invalid_timestamps:
            with self.subTest(timestamp=timestamp):
                result = self.minimal_result()
                result["assessor_metadata"] = {
                    "assessment_timestamp": timestamp,
                }
                self.assert_invalid(result)

        for calendar_invalid in (
            "2025-02-29T12:34:56Z",
            "2026-13-01T12:34:56Z",
        ):
            result = self.minimal_result()
            result["assessor_metadata"] = {
                "assessment_timestamp": calendar_invalid,
            }
            self.assertEqual([], list(self.validator.iter_errors(result)))
            self.assert_invalid(result)


if __name__ == "__main__":
    unittest.main()
