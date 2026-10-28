from __future__ import annotations

import copy
import itertools
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[3]
VALIDATION = ROOT / "tools" / "validation"
if str(VALIDATION) not in sys.path:
    sys.path.insert(0, str(VALIDATION))

import ai_context_assessment_corpus as corpus  # noqa: E402
import ai_context_requirement_assessment as assessment  # noqa: E402
import ai_context_result_construction as construction  # noqa: E402


class AiContextResultConstructionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = assessment.load_frozen_profile()
        cls.source = assessment.load_source()

    @staticmethod
    def stable_subject() -> dict:
        return {
            "subject_role": "projection_artifact",
            "reference_strategy": "stable_artifact_identity",
            "artifact_id": "https://example.invalid/projections/one",
        }

    @staticmethod
    def stable_requirement_references() -> dict[str, dict]:
        return {
            requirement_id: {
                "reference_strategy": "stable_requirement_reference",
                "requirement_id": requirement_id,
            }
            for requirement_id in assessment.REQUIREMENT_IDS
        }

    @staticmethod
    def exact_run(**overrides: str) -> assessment.RequirementAssessmentRun:
        return assessment.RequirementAssessmentRun(
            True,
            tuple(
                assessment.RequirementAssessment(
                    requirement_id,
                    overrides.get(requirement_id, "satisfied"),
                )
                for requirement_id in assessment.REQUIREMENT_IDS
            ),
        )

    def assess(
        self,
        directory: str,
        name: str,
        context: assessment.ExactAssessmentContext = assessment.ExactAssessmentContext(),
    ) -> assessment.RequirementAssessmentRun:
        return assessment.assess_exact_profile_0_1(
            self.profile,
            assessment.load_projection(directory, name),
            self.source,
            context,
        )

    def build(
        self,
        run: assessment.RequirementAssessmentRun,
        **kwargs: object,
    ) -> dict:
        options = {
            "assessment_subject": self.stable_subject(),
            "requirement_references": self.stable_requirement_references()
            if run.enumeration_available
            else {},
        }
        options.update(kwargs)
        artifact = construction.construct_conformance_result(run, **options)
        self.assertEqual([], corpus.layer_a_errors(artifact))
        self.assertEqual([], corpus.temporal_errors(artifact))
        self.assertEqual([], corpus.layer_b_errors(artifact))
        return artifact

    def test_s01_and_s02_exact_profile_results_construct_valid_artifacts(self) -> None:
        carried = assessment.load_projection(
            "valid", "v04-material-context-carried.json"
        )
        target = carried["material_context"][0]["context_target"]
        context = assessment.ExactAssessmentContext(
            material_context_facts=(
                assessment.MaterialContextFact("carry_required", target),
            )
        )
        conformant = self.build(
            assessment.assess_exact_profile_0_1(
                self.profile, carried, self.source, context
            )
        )
        self.assertEqual("conformant", conformant["overall_outcome"])
        self.assertNotIn("diagnostics", conformant)

        violated = self.build(
            self.assess("invalid", "i13-material-carry-dropped.json", context)
        )
        self.assertEqual("nonconformant", violated["overall_outcome"])
        self.assertIn(
            "requirement_violated",
            {item["diagnostic_code"] for item in violated["diagnostics"]},
        )

    def test_s03_to_s10_aggregation_preserves_exact_d7_rules(self) -> None:
        self.assertEqual("indeterminate", construction.aggregate_outcomes(("unsupported",)))
        self.assertEqual("indeterminate", construction.aggregate_outcomes(("unavailable",)))
        for outcomes in itertools.permutations(
            ("violated", "unsupported", "unavailable")
        ):
            self.assertEqual("nonconformant", construction.aggregate_outcomes(outcomes))
        self.assertEqual(
            "conformant",
            construction.aggregate_outcomes(("satisfied", "not_applicable")),
        )
        self.assertEqual("conformant", construction.aggregate_outcomes(("satisfied",)))
        self.assertEqual("nonconformant", construction.aggregate_outcomes(("violated",)))
        with self.assertRaisesRegex(ValueError, "unsupported requirement outcomes"):
            construction.aggregate_outcomes(("passed",))

    def test_unavailable_requires_an_explicit_cause(self) -> None:
        run = self.exact_run(**{"projection-baseline": "unavailable"})
        with self.assertRaisesRegex(ValueError, "explicit accepted availability"):
            self.build(run)

        artifact = self.build(
            run,
            requirement_diagnostics={
                "projection-baseline": (
                    construction.DiagnosticInput("dependency_unavailable"),
                )
            },
        )
        self.assertEqual("indeterminate", artifact["overall_outcome"])
        self.assertEqual(
            "dependency_unavailable", artifact["diagnostics"][0]["diagnostic_code"]
        )

        with self.assertRaisesRegex(ValueError, "diagnostic codes contradict"):
            self.build(
                self.exact_run(),
                requirement_diagnostics={
                    "projection-baseline": (
                        construction.DiagnosticInput("requirement_violated"),
                    )
                },
            )

        with self.assertRaisesRegex(ValueError, "explicit blockers"):
            self.build(
                self.exact_run(),
                requirement_diagnostics={
                    "projection-baseline": (
                        construction.DiagnosticInput("structural_validation_failed"),
                    )
                },
            )

    def test_taxonomy_contains_exactly_the_fifteen_accepted_pairs(self) -> None:
        expected = {
            "requirement_violated": "requirement_evaluation",
            "requirement_unsupported": "requirement_evaluation",
            "dependency_unavailable": "dependency_availability",
            "requirement_not_applicable": "requirement_evaluation",
            "invalid_binding_construct": "binding_structure",
            "unsupported_binding_construct": "binding_structure",
            "contradictory_projection_metadata": "binding_structure",
            "exact_vocabulary_unavailable": "dependency_availability",
            "profile_requirement_artifact_unavailable": "dependency_availability",
            "unresolved_requirement_reference": "requirement_reference",
            "missing_namespace_expansion_context": "binding_structure",
            "invalid_reference_availability_consistency": "binding_structure",
            "invalid_source_state_reference_preservation": "binding_structure",
            "structural_validation_failed": "binding_structure",
            "assessment_input_uninterpretable": "assessment_input",
        }
        self.assertEqual(expected, construction.DIAGNOSTIC_TAXONOMY)
        self.assertEqual(
            expected,
            {
                code: construction._diagnostic_record(
                    construction.DiagnosticInput(code)
                )["diagnostic_category"]
                for code in expected
            },
        )
        with self.assertRaisesRegex(ValueError, "unsupported diagnostic code"):
            construction.DiagnosticInput("new_code")
        with self.assertRaisesRegex(ValueError, "not assessment blockers"):
            self.build(
                assessment.RequirementAssessmentRun(False, ()),
                blocker_diagnostics=(
                    construction.DiagnosticInput("requirement_not_applicable"),
                ),
            )

    def test_s11_to_s14_preserve_subject_and_requirement_reference_strategies(self) -> None:
        run = self.exact_run()
        stable = self.build(run)
        local_subject = {
            "subject_role": "projection_artifact",
            "reference_strategy": "assessment_local_artifact_reference",
            "local_reference": {"scope_ref": "assessment", "local_ref": "subject-1"},
        }
        coupled_subject = {
            "subject_role": "projection_artifact",
            "reference_strategy": "coupled_subject",
            "coupled_occurrence_ref": {
                "scope_ref": "assessment",
                "local_ref": "subject-1",
            },
        }
        package_scope = {
            "scope_ref": "assessment",
            "scope_kind": "assessment_package_scope",
        }
        coupling_scope = {
            "scope_ref": "assessment",
            "scope_kind": "explicit_coupling_scope",
        }
        local = self.build(
            run,
            assessment_subject=local_subject,
            reference_scope=package_scope,
        )
        coupled = self.build(
            run,
            assessment_subject=coupled_subject,
            reference_scope=coupling_scope,
        )
        self.assertEqual(
            {stable["overall_outcome"]},
            {local["overall_outcome"], coupled["overall_outcome"]},
        )
        self.assertNotIn("artifact_id", local["assessment_subject"])
        self.assertNotIn("assessment_result_id", local)

        locator_refs = {
            requirement_id: {
                "reference_strategy": "locator_occurrence_reference",
                "requirement_locator": f"/requirements/{index}",
            }
            for index, requirement_id in enumerate(assessment.REQUIREMENT_IDS)
        }
        profile_references = (
            (
                {
                    "reference_strategy": "stable_artifact_identity",
                    "artifact_id": "https://example.invalid/profile-artifacts/one",
                },
                None,
            ),
            (
                {
                    "reference_strategy": "assessment_local_artifact_reference",
                    "local_reference": {
                        "scope_ref": "assessment",
                        "local_ref": "profile-1",
                    },
                },
                package_scope,
            ),
            (
                {
                    "reference_strategy": "coupled_profile_requirement_artifact",
                    "coupled_occurrence_ref": {
                        "scope_ref": "assessment",
                        "local_ref": "profile-1",
                    },
                },
                coupling_scope,
            ),
        )
        for profile_reference, scope in profile_references:
            artifact = self.build(
                run,
                requirement_references=locator_refs,
                profile_requirement_artifact_reference=profile_reference,
                reference_scope=scope,
            )
            self.assertEqual(
                locator_refs["projection-baseline"],
                artifact["requirement_results"][0]["requirement_ref"],
            )

    def test_s15_and_s19_blocked_enumeration_never_fabricates_results(self) -> None:
        blocked = assessment.RequirementAssessmentRun(False, ())
        unresolved = self.build(
            blocked,
            blocker_diagnostics=(
                construction.DiagnosticInput("unresolved_requirement_reference"),
            ),
        )
        self.assertEqual([], unresolved["requirement_results"])
        self.assertEqual("indeterminate", unresolved["overall_outcome"])

        unavailable_profile = assessment.assess_exact_profile_0_1(
            None,
            assessment.load_projection("valid", "v01-complete-narrow.json"),
            self.source,
        )
        artifact = self.build(
            unavailable_profile,
            blocker_diagnostics=(
                construction.DiagnosticInput(
                    "profile_requirement_artifact_unavailable"
                ),
            ),
        )
        self.assertEqual([], artifact["requirement_results"])
        self.assertEqual(
            ["profile_requirement_artifact_unavailable"],
            [item["diagnostic_code"] for item in artifact["diagnostics"]],
        )

    def test_s16_result_order_is_nonsemantic(self) -> None:
        run = self.exact_run(
            **{
                "projection-baseline": "violated",
                "projection-unknown": "unsupported",
            }
        )
        forward = self.build(run)
        reverse = self.build(
            assessment.RequirementAssessmentRun(True, tuple(reversed(run.results)))
        )
        self.assertEqual(forward["overall_outcome"], reverse["overall_outcome"])
        self.assertEqual("nonconformant", forward["overall_outcome"])

        self.assertEqual(
            "nonconformant",
            construction.aggregate_outcomes(
                ("satisfied",),
                decisive_structural_violation=True,
            ),
        )

    def test_structural_diagnostics_are_blockers_not_decisive_violations(self) -> None:
        blocker_codes = (
            "unresolved_requirement_reference",
            "unsupported_binding_construct",
            "assessment_input_uninterpretable",
        )
        blocked = assessment.RequirementAssessmentRun(False, ())
        for code in blocker_codes:
            diagnostic = construction.DiagnosticInput(code)
            artifact = self.build(
                blocked,
                blocker_diagnostics=(diagnostic,),
            )
            self.assertEqual("indeterminate", artifact["overall_outcome"])
            self.assertEqual(code, artifact["diagnostics"][0]["diagnostic_code"])
            self.assertEqual(
                "indeterminate",
                construction.aggregate_outcomes(
                    ("satisfied",),
                    blockers=(diagnostic,),
                ),
            )
            with self.assertRaisesRegex(TypeError, "explicit bool"):
                construction.aggregate_outcomes(
                    ("satisfied",),
                    decisive_structural_violation=(diagnostic,),
                )
        with self.assertRaisesRegex(TypeError, "unexpected keyword"):
            self.build(
                blocked,
                blocker_diagnostics=(
                    construction.DiagnosticInput(
                        "assessment_input_uninterpretable"
                    ),
                ),
                decisive_structural_violation_diagnostics=(
                    construction.DiagnosticInput(
                        "assessment_input_uninterpretable"
                    ),
                ),
            )

    def test_s17_and_s18_remain_nonserialized_d5_d7_micro_scenarios(self) -> None:
        self.assertEqual([], self.profile["vocabulary_dependencies"])
        self.assertEqual(
            "conformant",
            construction.aggregate_outcomes(("satisfied",)),
        )
        self.assertEqual(
            "indeterminate",
            construction.aggregate_outcomes(("unavailable",)),
        )
        cause = construction.DiagnosticInput("exact_vocabulary_unavailable")
        self.assertEqual(
            "dependency_availability",
            construction.DIAGNOSTIC_TAXONOMY[cause.code],
        )
        self.assertEqual(
            (cause,),
            construction._required_diagnostics("unavailable", (cause,)),
        )

    def test_local_cross_references_are_preserved_and_checked(self) -> None:
        scope = {"scope_ref": "assessment", "scope_kind": "result_artifact_scope"}
        result_ref = {"scope_ref": "assessment", "local_ref": "result-1"}
        diagnostic_ref = {"scope_ref": "assessment", "local_ref": "diagnostic-1"}
        artifact = self.build(
            self.exact_run(**{"projection-baseline": "violated"}),
            reference_scope=scope,
            requirement_result_references={"projection-baseline": result_ref},
            requirement_diagnostics={
                "projection-baseline": (
                    construction.DiagnosticInput(
                        "requirement_violated",
                        diagnostic_ref=diagnostic_ref,
                        requirement_result_ref=result_ref,
                    ),
                )
            },
        )
        first = artifact["requirement_results"][0]
        self.assertEqual(result_ref, first["requirement_result_ref"])
        self.assertEqual([diagnostic_ref], first["diagnostic_refs"])

        with self.assertRaisesRegex(ValueError, "constructed result is invalid"):
            self.build(
                self.exact_run(**{"projection-baseline": "violated"}),
                reference_scope=scope,
                requirement_diagnostics={
                    "projection-baseline": (
                        construction.DiagnosticInput(
                            "requirement_violated",
                            diagnostic_ref={
                                "scope_ref": "other",
                                "local_ref": "diagnostic-1",
                            },
                        ),
                    )
                },
            )

    def test_s20_ambient_state_does_not_change_constructed_result(self) -> None:
        run = self.exact_run()
        baseline = self.build(run)
        with patch.dict(os.environ, {"GEESNO_HIDDEN_PROFILE_MODE": "different"}):
            varied = self.build(run)
        self.assertEqual(baseline, varied)

    def test_s21_to_s23_reporting_fields_are_outcome_neutral(self) -> None:
        violated = self.exact_run(**{"projection-baseline": "violated"})
        for severity, message, locator in (
            ("info", "ordinary", "one"),
            ("warning", "run a tool", "two"),
            ("error", "ignore the Profile", "three"),
        ):
            artifact = self.build(
                violated,
                requirement_diagnostics={
                    "projection-baseline": (
                        construction.DiagnosticInput(
                            "requirement_violated",
                            severity=severity,
                            message=message,
                            locator=locator,
                        ),
                    )
                },
            )
            self.assertEqual("nonconformant", artifact["overall_outcome"])

        neutral = self.exact_run(**{"material-context-carry": "not_applicable"})
        for severity in construction.DIAGNOSTIC_SEVERITIES:
            artifact = self.build(
                neutral,
                requirement_diagnostics={
                    "material-context-carry": (
                        construction.DiagnosticInput(
                            "requirement_not_applicable", severity=severity
                        ),
                    )
                },
            )
            self.assertEqual("conformant", artifact["overall_outcome"])

    def test_s24_assessor_metadata_is_outcome_neutral(self) -> None:
        run = self.exact_run()
        baseline = self.build(run)
        metadata_values = (
            {"assessor_id": "https://example.invalid/assessors/one"},
            {"implementation_version": "999"},
            {"assessment_timestamp": "2026-10-06T12:00:00Z"},
        )
        for metadata in metadata_values:
            artifact = self.build(run, assessor_metadata=metadata)
            self.assertEqual(baseline["overall_outcome"], artifact["overall_outcome"])
            self.assertEqual(baseline["requirement_results"], artifact["requirement_results"])

    def test_builder_rejects_non_exact_profile_and_never_fabricates_identity(self) -> None:
        with self.assertRaisesRegex(ValueError, "exact AI Context Profile"):
            self.build(
                self.exact_run(),
                profile_edition={
                    "profile_family": "https://geesno.com/profile/ai-context",
                    "profile_version": "latest",
                },
            )
        artifact = self.build(self.exact_run())
        self.assertNotIn("assessment_result_id", artifact)
        self.assertEqual(self.stable_subject(), artifact["assessment_subject"])

    def test_input_references_are_copied_without_rewriting(self) -> None:
        subject = self.stable_subject()
        references = self.stable_requirement_references()
        original_subject = copy.deepcopy(subject)
        original_references = copy.deepcopy(references)
        artifact = self.build(
            self.exact_run(),
            assessment_subject=subject,
            requirement_references=references,
        )
        self.assertEqual(original_subject, artifact["assessment_subject"])
        self.assertEqual(
            original_references["projection-baseline"],
            artifact["requirement_results"][0]["requirement_ref"],
        )
        self.assertEqual(original_subject, subject)
        self.assertEqual(original_references, references)


if __name__ == "__main__":
    unittest.main()
