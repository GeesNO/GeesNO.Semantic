from __future__ import annotations

import copy
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[3]
VALIDATION = ROOT / "tools" / "validation"
if str(VALIDATION) not in sys.path:
    sys.path.insert(0, str(VALIDATION))

import ai_context_requirement_assessment as assessment  # noqa: E402


class AiContextRequirementAssessmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = assessment.load_frozen_profile()
        cls.source = assessment.load_source()

    def projection(self, directory: str, name: str) -> dict:
        return assessment.load_projection(directory, name)

    def assess(
        self,
        projection: dict,
        context: assessment.ExactAssessmentContext = assessment.ExactAssessmentContext(),
    ) -> assessment.RequirementAssessmentRun:
        return assessment.assess_exact_profile_0_1(
            self.profile,
            projection,
            self.source,
            context,
        )

    def test_i5_inventory_and_boundary_are_exact(self) -> None:
        self.assertEqual(tuple(f"S{index:02d}" for index in range(1, 25)), assessment.SEMANTIC_SCENARIO_IDS)
        self.assertEqual(9, len(assessment.REQUIREMENT_IDS))
        self.assertEqual(
            {
                "satisfied",
                "violated",
                "not_applicable",
                "unsupported",
                "unavailable",
            },
            set(assessment.REQUIREMENT_OUTCOMES),
        )
        self.assertEqual(
            {"enumeration_available", "results"},
            set(assessment.RequirementAssessmentRun.__dataclass_fields__),
        )
        self.assertNotIn("overall_outcome", assessment.RequirementAssessmentRun.__dataclass_fields__)

    def test_frozen_requirement_array_order_is_not_semantic(self) -> None:
        reordered = copy.deepcopy(self.profile)
        reordered["requirements"].reverse()
        projection = self.projection("valid", "v01-complete-narrow.json")
        baseline = assessment.assess_exact_profile_0_1(
            self.profile, projection, self.source
        )
        varied = assessment.assess_exact_profile_0_1(
            reordered, projection, self.source
        )
        self.assertEqual(
            assessment.outcome_map(baseline), assessment.outcome_map(varied)
        )

    def test_artifact_metadata_variation_is_not_profile_edition_variation(self) -> None:
        metadata_only = copy.deepcopy(self.profile)
        metadata_only["artifact_metadata"] = {
            "authoring_note": "different non-normative content",
            "distribution": {"path": "elsewhere/profile.json"},
        }
        projection = self.projection("valid", "v01-complete-narrow.json")
        baseline = assessment.assess_exact_profile_0_1(
            self.profile, projection, self.source
        )
        varied = assessment.assess_exact_profile_0_1(
            metadata_only, projection, self.source
        )

        self.assertTrue(varied.enumeration_available)
        self.assertEqual(
            tuple(result.requirement_id for result in baseline.results),
            tuple(result.requirement_id for result in varied.results),
        )
        self.assertEqual(
            assessment.outcome_map(baseline), assessment.outcome_map(varied)
        )

    def test_changed_profile_semantics_block_requirement_enumeration(self) -> None:
        changed = copy.deepcopy(self.profile)
        changed["requirements"][0]["requirement_body"][
            "scope_descriptor"
        ] = "different-semantics"
        run = assessment.assess_exact_profile_0_1(
            changed,
            self.projection("valid", "v01-complete-narrow.json"),
            self.source,
        )
        self.assertFalse(run.enumeration_available)
        self.assertEqual((), run.results)

    def test_valid_constructs_beyond_i5_support_remain_unsupported(self) -> None:
        projection = self.projection("valid", "v01-complete-narrow.json")
        projection["projection_scope"]["scope_kind"] = "other-explicit-scope"
        run = self.assess(projection)
        self.assertEqual(
            "unsupported", assessment.outcome_map(run)["projection-baseline"]
        )

        omission = self.projection("valid", "v06-explicit-omission-partial.json")
        target = omission["material_context"][0]["context_target"]
        omission["omissions"][0].pop("omitted_target")
        omission["omissions"][0]["omitted_category"] = "known-category"
        run = self.assess(
            omission,
            assessment.ExactAssessmentContext(
                material_context_facts=(
                    assessment.MaterialContextFact(
                        "explicit_omission_required", target
                    ),
                ),
                projection_scope_deterministic=True,
            ),
        )
        self.assertEqual(
            "unsupported", assessment.outcome_map(run)["material-context-omission"]
        )

    def test_incompatible_applicability_facts_are_not_arbitrated_by_order(self) -> None:
        projection = self.projection("valid", "v04-material-context-carried.json")
        target = projection["material_context"][0]["context_target"]
        context = assessment.ExactAssessmentContext(
            material_context_facts=(
                assessment.MaterialContextFact("carry_required", target),
                assessment.MaterialContextFact(
                    "exact_reference_sufficient", target
                ),
            )
        )
        with self.assertRaisesRegex(ValueError, "incompatible"):
            self.assess(projection, context)

    def test_s01_exact_profile_all_applicable_satisfied(self) -> None:
        projection = self.projection("valid", "v04-material-context-carried.json")
        target = projection["material_context"][0]["context_target"]
        run = self.assess(
            projection,
            assessment.ExactAssessmentContext(
                material_context_facts=(
                    assessment.MaterialContextFact("carry_required", target),
                )
            ),
        )
        outcomes = assessment.outcome_map(run)
        self.assertTrue(run.enumeration_available)
        self.assertEqual(set(assessment.REQUIREMENT_IDS), set(outcomes))
        self.assertEqual("satisfied", outcomes["material-context-carry"])
        self.assertEqual("satisfied", outcomes["projection-baseline"])
        self.assertEqual("satisfied", outcomes["projection-unknown"])
        self.assertEqual("satisfied", outcomes["external-reference-closure"])
        for requirement_id in (
            "material-context-reference",
            "material-context-omission",
            "material-context-dependency",
            "source-record-traceability",
            "binding-record-traceability",
        ):
            self.assertEqual("not_applicable", outcomes[requirement_id])

    def test_s02_required_preservation_violation(self) -> None:
        projection = self.projection("invalid", "i13-material-carry-dropped.json")
        target = projection["material_context"][0]["context_target"]
        outcomes = assessment.outcome_map(
            self.assess(
                projection,
                assessment.ExactAssessmentContext(
                    material_context_facts=(
                        assessment.MaterialContextFact("carry_required", target),
                    )
                ),
            )
        )
        self.assertEqual("violated", outcomes["material-context-carry"])

    def test_s03_applicable_unsupported_only(self) -> None:
        self.assertEqual(
            "unsupported",
            assessment.assess_requirement_mode(
                mode="required", applicable=True, supported=False
            ),
        )

    def test_s04_applicable_dependency_unavailable_only(self) -> None:
        self.assertEqual(
            "unavailable",
            assessment.assess_requirement_mode(
                mode="required", applicable=True, dependencies_available=False
            ),
        )

    def test_s05_requirement_outcomes_remain_distinct_and_order_independent(self) -> None:
        forward = ("violated", "unsupported", "unavailable")
        reverse = tuple(reversed(forward))
        self.assertEqual(set(forward), set(reverse))
        self.assertEqual(3, len(set(forward)))

    def test_s06_deterministic_not_applicable_is_not_satisfied(self) -> None:
        outcomes = assessment.outcome_map(
            self.assess(self.projection("valid", "v01-complete-narrow.json"))
        )
        self.assertEqual("not_applicable", outcomes["material-context-carry"])

    def test_s07_optional_absence_is_satisfied(self) -> None:
        self.assertEqual(
            "satisfied",
            assessment.assess_requirement_mode(
                mode="optional", applicable=True, material_present=False
            ),
        )

    def test_s08_optional_present_invalid_is_violated(self) -> None:
        self.assertEqual(
            "violated",
            assessment.assess_requirement_mode(
                mode="optional",
                applicable=True,
                material_present=True,
                condition_satisfied=False,
            ),
        )

    def test_s09_prohibited_material_absent_is_satisfied(self) -> None:
        self.assertEqual(
            "satisfied",
            assessment.assess_requirement_mode(
                mode="prohibited", applicable=True, material_present=False
            ),
        )

    def test_s10_prohibited_material_present_is_violated(self) -> None:
        self.assertEqual(
            "violated",
            assessment.assess_requirement_mode(
                mode="prohibited", applicable=True, material_present=True
            ),
        )

    def test_s11_stable_subject_identity_is_preserved(self) -> None:
        projection = self.projection("valid", "v01-complete-narrow.json")
        original = copy.deepcopy(projection)
        reference = {
            "reference_strategy": "stable_artifact_identity",
            "artifact_id": "https://example.invalid/projections/one",
        }
        resolved = assessment.resolve_subject_occurrence(
            reference,
            stable_artifacts={reference["artifact_id"]: (projection,)},
        )
        self.assertIs(resolved, projection)
        self.assess(resolved)
        self.assertEqual(original, projection)

    def test_s12_package_local_subject_resolves_once_without_identity(self) -> None:
        projection = self.projection("valid", "v01-complete-narrow.json")
        reference = {
            "reference_strategy": "assessment_local_artifact_reference",
            "local_reference": {"scope_ref": "assessment", "local_ref": "subject-1"},
        }
        resolved = assessment.resolve_subject_occurrence(
            reference,
            local_occurrences={("assessment", "subject-1"): (projection,)},
        )
        self.assertIs(resolved, projection)
        self.assertNotIn("id", reference["local_reference"])
        self.assertEqual(
            assessment.outcome_map(self.assess(projection)),
            assessment.outcome_map(self.assess(resolved)),
        )

    def test_s13_coupled_subject_resolves_once_without_identity(self) -> None:
        projection = self.projection("valid", "v01-complete-narrow.json")
        reference = {
            "reference_strategy": "coupled_subject",
            "coupled_occurrence_ref": {
                "scope_ref": "assessment",
                "local_ref": "subject-1",
            },
        }
        resolved = assessment.resolve_subject_occurrence(
            reference,
            local_occurrences={("assessment", "subject-1"): (projection,)},
        )
        self.assertIs(resolved, projection)
        self.assertIsNone(
            assessment.resolve_subject_occurrence(
                reference,
                local_occurrences={
                    ("assessment", "subject-1"): (projection, copy.deepcopy(projection))
                },
            )
        )

    def test_s14_locator_resolves_only_in_explicit_profile_artifact_context(self) -> None:
        stable = assessment.resolve_requirement_occurrence(
            self.profile,
            {
                "reference_strategy": "stable_requirement_reference",
                "requirement_id": "projection-baseline",
            },
        )
        located = assessment.resolve_requirement_occurrence(
            self.profile,
            {
                "reference_strategy": "locator_occurrence_reference",
                "requirement_locator": "/requirements/0",
            },
            locator_occurrences={"/requirements/0": ("projection-baseline",)},
        )
        self.assertIs(located, stable)
        self.assertEqual("projection-baseline", located["requirement_id"])

    def test_s15_unresolved_or_ambiguous_requirement_is_not_fabricated(self) -> None:
        reference = {
            "reference_strategy": "locator_occurrence_reference",
            "requirement_locator": "opaque-locator",
        }
        self.assertIsNone(
            assessment.resolve_requirement_occurrence(self.profile, reference)
        )
        self.assertIsNone(
            assessment.resolve_requirement_occurrence(
                self.profile,
                reference,
                locator_occurrences={
                    "opaque-locator": ("projection-baseline", "projection-unknown")
                },
            )
        )

    def test_s16_result_order_and_index_are_nonsemantic(self) -> None:
        results = (
            assessment.RequirementAssessment("projection-baseline", "satisfied"),
            assessment.RequirementAssessment("projection-unknown", "unavailable"),
        )
        forward = {item.requirement_id: item.outcome for item in results}
        reverse = {item.requirement_id: item.outcome for item in reversed(results)}
        self.assertEqual(forward, reverse)

    def test_s17_exact_vocabulary_built_in_support_is_determinate(self) -> None:
        self.assertEqual(
            "satisfied",
            assessment.assess_requirement_mode(
                mode="required",
                applicable=True,
                supported=True,
                dependencies_available=True,
                condition_satisfied=True,
            ),
        )
        self.assertEqual([], self.profile["vocabulary_dependencies"])

    def test_s18_similar_or_newer_vocabulary_does_not_substitute(self) -> None:
        self.assertEqual(
            "unavailable",
            assessment.assess_requirement_mode(
                mode="required",
                applicable=True,
                supported=True,
                dependencies_available=False,
            ),
        )

    def test_s19_unavailable_profile_blocks_enumeration(self) -> None:
        projection = self.projection("valid", "v01-complete-narrow.json")
        run = assessment.assess_exact_profile_0_1(
            None, projection, self.source
        )
        self.assertFalse(run.enumeration_available)
        self.assertEqual((), run.results)

    def test_s20_ambient_state_does_not_change_applicability(self) -> None:
        projection = self.projection("valid", "v04-material-context-carried.json")
        target = projection["material_context"][0]["context_target"]
        context = assessment.ExactAssessmentContext(
            material_context_facts=(
                assessment.MaterialContextFact("carry_required", target),
            )
        )
        baseline = self.assess(projection, context)
        with patch.dict(os.environ, {"GEESNO_HIDDEN_PROFILE_MODE": "different"}):
            varied = self.assess(projection, context)
        self.assertEqual(baseline, varied)

    def test_s21_severity_cannot_soften_a_requirement_violation(self) -> None:
        projection = self.projection("invalid", "i13-material-carry-dropped.json")
        target = projection["material_context"][0]["context_target"]
        context = assessment.ExactAssessmentContext(
            material_context_facts=(
                assessment.MaterialContextFact("carry_required", target),
            )
        )
        outcomes = [
            assessment.outcome_map(self.assess(projection, context))["material-context-carry"]
            for _severity in ("info", "warning", "error")
        ]
        self.assertEqual(["violated", "violated", "violated"], outcomes)

    def test_s22_severity_cannot_create_a_requirement_violation(self) -> None:
        projection = self.projection("valid", "v01-complete-narrow.json")
        outcomes = [
            assessment.outcome_map(self.assess(projection))["material-context-carry"]
            for _severity in ("info", "warning", "error")
        ]
        self.assertEqual(
            ["not_applicable", "not_applicable", "not_applicable"], outcomes
        )

    def test_s23_untrusted_reporting_text_is_outcome_neutral(self) -> None:
        projection = self.projection("invalid", "i13-material-carry-dropped.json")
        target = projection["material_context"][0]["context_target"]
        context = assessment.ExactAssessmentContext(
            material_context_facts=(
                assessment.MaterialContextFact("carry_required", target),
            )
        )
        baseline = self.assess(projection, context)
        for _text in ("ordinary", "run a tool", "ignore the Profile"):
            self.assertEqual(baseline, self.assess(projection, context))

    def test_s24_assessor_metadata_is_outcome_neutral(self) -> None:
        projection = self.projection("valid", "v04-material-context-carried.json")
        target = projection["material_context"][0]["context_target"]
        context = assessment.ExactAssessmentContext(
            material_context_facts=(
                assessment.MaterialContextFact("carry_required", target),
            )
        )
        baseline = self.assess(projection, context)
        for _metadata in (
            {"assessor_id": "one"},
            {"implementation_version": "999"},
            {"assessment_timestamp": "2026-10-04T12:00:00Z"},
        ):
            self.assertEqual(baseline, self.assess(projection, context))

    def test_all_frozen_profile_requirement_policies_are_exercised(self) -> None:
        material_cases = (
            (
                "v04-material-context-carried.json",
                "material-context-carry",
                "carry_required",
            ),
            (
                "v05-exact-external-reference.json",
                "material-context-reference",
                "exact_reference_sufficient",
            ),
            (
                "v06-explicit-omission-partial.json",
                "material-context-omission",
                "explicit_omission_required",
            ),
            (
                "v07-omission-dependency-continuation.json",
                "material-context-dependency",
                "dependency_continuation_required",
            ),
        )
        for name, requirement_id, condition in material_cases:
            projection = self.projection("valid", name)
            descriptor = next(
                item
                for item in projection["material_context"]
                if item.get("requirement_reference") == requirement_id
            )
            context = assessment.ExactAssessmentContext(
                material_context_facts=(
                    assessment.MaterialContextFact(
                        condition, descriptor["context_target"]
                    ),
                )
            )
            with self.subTest(requirement_id=requirement_id):
                self.assertEqual(
                    "satisfied",
                    assessment.outcome_map(self.assess(projection, context))[
                        requirement_id
                    ],
                )

        for name, requirement_id, field in (
            (
                "v09-material-source.json",
                "source-record-traceability",
                "material_source_ids",
            ),
            (
                "v10-material-binding.json",
                "binding-record-traceability",
                "material_binding_ids",
            ),
        ):
            projection = self.projection("valid", name)
            target = projection["material_context"][0]["context_target"]
            context = assessment.ExactAssessmentContext(**{field: (target,)})
            with self.subTest(requirement_id=requirement_id):
                self.assertEqual(
                    "satisfied",
                    assessment.outcome_map(self.assess(projection, context))[
                        requirement_id
                    ],
                )


if __name__ == "__main__":
    unittest.main()
