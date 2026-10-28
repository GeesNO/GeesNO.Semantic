from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[3]
VALIDATION = ROOT / "tools" / "validation"
sys.path.insert(0, str(VALIDATION))

import check_repository  # noqa: E402


PROFILE_PATH = ROOT / check_repository.AI_CONTEXT_PROFILE
SCHEMA_PATH = ROOT / check_repository.AI_CONTEXT_SCHEMA
S2_SCHEMA_PATH = ROOT / "schema" / "v0.1" / "geesno-semantic.schema.json"
S2_REFERENCE = "../../../../schema/v0.1/geesno-semantic.schema.json"
PROFILE_SPECIFICATION = ROOT / "spec" / "ai-context-profile.md"


class AiContextProfileArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.s2_schema = json.loads(S2_SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(cls.schema)
        registry = Registry().with_resource(
            S2_REFERENCE,
            Resource.from_contents(cls.s2_schema),
        )
        cls.validator = Draft202012Validator(cls.schema, registry=registry)

    def test_artifact_is_schema_valid_offline(self) -> None:
        errors = list(self.validator.iter_errors(self.profile))
        self.assertEqual([], errors, "\n".join(error.message for error in errors))

    def test_artifact_matches_the_approved_exact_inventory(self) -> None:
        self.assertEqual([], check_repository.check_ai_context_profile(self.profile))

        requirements = self.profile["requirements"]
        requirement_ids = [
            requirement["requirement_id"] for requirement in requirements
        ]
        self.assertEqual(9, len(requirements))
        self.assertEqual(9, len(set(requirement_ids)))
        self.assertEqual(
            {
                "projection",
                "preservation",
                "source_binding",
                "closure",
            },
            {requirement["requirement_kind"] for requirement in requirements},
        )
        self.assertEqual([], self.profile["vocabulary_dependencies"])

    def test_requirement_array_order_is_not_semantic(self) -> None:
        reordered = copy.deepcopy(self.profile)
        reordered["requirements"].reverse()
        self.assertEqual([], check_repository.check_ai_context_profile(reordered))

    def test_projection_baseline_has_no_continuation_policy(self) -> None:
        requirements = {
            requirement["requirement_id"]: requirement
            for requirement in self.profile["requirements"]
        }
        self.assertEqual(
            {
                "scope_descriptor": "explicit_deterministic_scope",
                "completeness_policy": "partial_projection_allowed",
                "boundedness_policy": "optional_explicit_finite_bound",
                "truncation_policy": "declare_established_truncation",
            },
            requirements["projection-baseline"]["requirement_body"],
        )
        self.assertNotIn(
            "declare_known_remaining_in_scope",
            json.dumps(self.profile, sort_keys=True),
        )

    def test_inventory_mutations_are_rejected_without_changing_schema(self) -> None:
        mutations = []

        extra = copy.deepcopy(self.profile)
        extra["requirements"].append(copy.deepcopy(extra["requirements"][0]))
        extra["requirements"][-1]["requirement_id"] = "extra-requirement"
        mutations.append(extra)

        wrong_family = copy.deepcopy(self.profile)
        wrong_family["profile_edition"]["profile_family"] = (
            "https://example.invalid/profile"
        )
        mutations.append(wrong_family)

        wrong_version = copy.deepcopy(self.profile)
        wrong_version["profile_edition"]["profile_version"] = "0.2.0"
        mutations.append(wrong_version)

        wrong_body = copy.deepcopy(self.profile)
        wrong_body["requirements"][0]["requirement_body"][
            "scope_descriptor"
        ] = "different_scope"
        mutations.append(wrong_body)

        missing = copy.deepcopy(self.profile)
        missing["requirements"].pop()
        mutations.append(missing)

        for mutation in mutations:
            with self.subTest(mutation=mutation):
                self.assertNotEqual(
                    [],
                    check_repository.check_ai_context_profile(mutation),
                )

    def test_profile_defined_tokens_have_normative_semantics(self) -> None:
        specification = PROFILE_SPECIFICATION.read_text(encoding="utf-8")
        self.assertIn("## AI Context Profile edition 0.1.0", specification)
        for token in (
            "carry_required",
            "exact_reference_sufficient",
            "explicit_omission_required",
            "dependency_continuation_required",
            "explicit_deterministic_scope",
            "partial_projection_allowed",
            "unknown_completeness_allowed",
            "optional_explicit_finite_bound",
            "declare_established_truncation",
            "material_to_projection",
            "external_references_allowed",
        ):
            self.assertIn(token, specification)


if __name__ == "__main__":
    unittest.main()
