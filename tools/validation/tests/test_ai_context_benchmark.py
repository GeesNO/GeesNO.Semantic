from __future__ import annotations

import json
import socket
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[3]
BENCHMARK_TOOL = ROOT / "tools" / "benchmark"
sys.path.insert(0, str(BENCHMARK_TOOL))

import ai_context_s4_exit as benchmark  # noqa: E402


class AiContextBenchmarkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with (
            patch.object(socket, "socket", side_effect=AssertionError("network access")),
            patch.object(
                socket,
                "create_connection",
                side_effect=AssertionError("network access"),
            ),
        ):
            cls.run_one = benchmark.build_benchmark_run()
            # Repeat generation and measurement without repeating the expensive
            # S2 validation already proven by run one. I2, I4 and benchmark
            # semantic checks still run on both generated Projection sets.
            cls.run_two = benchmark.build_benchmark_run(validate_source=False)

    def test_recipe_is_exact_finite_and_parseable(self) -> None:
        recipe = benchmark.load_recipe()
        self.assertEqual(recipe, self.run_one.recipe)
        self.assertEqual(
            {"id": "s4-ai-context-exit", "version": "0.1"},
            recipe["benchmark"],
        )
        self.assertEqual(
            {"id": "s4-ai-context-benchmark", "version": "0.1"},
            recipe["generator_recipe"],
        )
        self.assertEqual(benchmark.MEASUREMENT_SERIALIZATION, recipe["measurement_serialization"])
        self.assertEqual(
            {
                "source_minimum_addressable_records": 10000,
                "bounded_record_ratio_percent_max": 10,
                "bounded_byte_ratio_percent_max": 25,
            },
            recipe["thresholds"],
        )

    def test_source_scale_categories_and_s2_validation_are_proven(self) -> None:
        source = self.run_one.report["source"]
        self.assertEqual(
            {
                "entities": 5000,
                "sources": 50,
                "bindings": 50,
                "assertions": 5000,
            },
            source["record_counts_by_category"],
        )
        self.assertEqual(10100, source["total_addressable_semantic_records"])
        self.assertGreaterEqual(source["total_addressable_semantic_records"], 10000)
        self.assertEqual(
            {"provenance": 10, "confidence": 10, "reviews": 10},
            source["additional_nested_id_bearing_context_by_category"],
        )
        self.assertEqual(30, source["additional_nested_id_bearing_context_total"])
        self.assertEqual(10130, source["total_id_bearing_records_including_nested_context"])
        self.assertEqual(10100, source["benchmark_threshold_and_ratio_denominator"])

    def test_complete_projection_is_narrow_complete_and_traceable(self) -> None:
        projection = self.run_one.complete_projection
        report = self.run_one.report["complete_narrow_projection"]
        self.assertEqual("complete", projection["projection_completeness"])
        self.assertEqual(4, report["selected_record_count"])
        self.assertEqual(4, report["total_carried_semantic_records"])
        self.assertFalse(report["boundedness_present"])
        self.assertFalse(report["truncation_present"])
        self.assertEqual(0, report["descriptor_counts"]["omissions"])
        self.assertEqual(0, report["descriptor_counts"]["projection_continuations"])
        self.assertEqual("pass", report["identity_retention"]["result"])
        self.assertEqual("pass", report["reference_retention"]["result"])
        self.assertEqual("pass", report["material_provenance_retention"]["result"])
        self.assertEqual("pass", report["source_retention"]["result"])
        self.assertEqual("pass", report["binding_retention"]["result"])

    def test_bounded_projection_is_partial_truncated_and_continuable(self) -> None:
        projection = self.run_one.bounded_projection
        report = self.run_one.report["bounded_partial_projection"]
        self.assertEqual("partial", projection["projection_completeness"])
        self.assertTrue(report["boundedness_present"])
        self.assertEqual([True], report["bound_reached_states"])
        self.assertTrue(report["truncation_present"])
        self.assertTrue(report["truncation_established"])
        self.assertEqual(1, report["descriptor_counts"]["omissions"])
        self.assertEqual(1, report["descriptor_counts"]["projection_continuations"])
        self.assertEqual(0, report["descriptor_counts"]["dependency_continuations"])
        self.assertEqual("pass", report["identity_retention"]["result"])
        self.assertEqual("pass", report["reference_retention"]["result"])
        self.assertEqual("pass", report["material_provenance_retention"]["result"])
        self.assertEqual("pass", report["source_retention"]["result"])
        self.assertEqual("pass", report["binding_retention"]["result"])

    def test_integer_threshold_checks_pass_without_floating_point_authority(self) -> None:
        report = self.run_one.report
        source = report["source"]
        bounded = report["bounded_partial_projection"]
        thresholds = report["thresholds"]
        carried = bounded["total_carried_semantic_records"]
        source_records = source["total_addressable_semantic_records"]
        projection_bytes = bounded["serialized_utf8_bytes"]
        source_bytes = source["serialized_utf8_bytes"]
        self.assertLessEqual(carried * 100, source_records * 10)
        self.assertLessEqual(projection_bytes * 100, source_bytes * 25)
        self.assertTrue(thresholds["source_minimum_passed"])
        self.assertTrue(thresholds["bounded_record_ratio_passed"])
        self.assertTrue(thresholds["bounded_byte_ratio_passed"])
        self.assertFalse(thresholds["semantic_authority"])

    def test_expected_projections_and_report_regenerate_byte_for_byte(self) -> None:
        self.assertEqual([], benchmark.expected_mismatches(self.run_one))
        self.assertEqual(
            self.run_one.complete_bytes,
            benchmark.EXPECTED_COMPLETE_PATH.read_bytes(),
        )
        self.assertEqual(
            self.run_one.bounded_bytes,
            benchmark.EXPECTED_BOUNDED_PATH.read_bytes(),
        )
        self.assertEqual(
            self.run_one.report_bytes,
            benchmark.EXPECTED_REPORT_PATH.read_bytes(),
        )

    def test_two_runs_are_exactly_repeatable_and_provider_neutral(self) -> None:
        self.assertEqual(self.run_one.source_bytes, self.run_two.source_bytes)
        self.assertEqual(self.run_one.complete_bytes, self.run_two.complete_bytes)
        self.assertEqual(self.run_one.bounded_bytes, self.run_two.bounded_bytes)
        self.assertEqual(self.run_one.report_bytes, self.run_two.report_bytes)
        dependencies = self.run_one.report["dependencies"]
        self.assertEqual(
            {
                "offline": True,
                "network_dependency": False,
                "model_provider_dependency": False,
                "tokenizer_dependency": False,
                "external_resolver_dependency": False,
                "automatic_dereference": False,
            },
            dependencies,
        )

    def test_report_is_benchmark_evidence_not_a_d7_result(self) -> None:
        report = json.loads(benchmark.EXPECTED_REPORT_PATH.read_text(encoding="utf-8"))
        forbidden = {"overall_outcome", "requirement_results", "diagnostics"}
        normative_artifact_kinds = {
            "profile_requirement_artifact",
            "projection_artifact",
            "conformance_result_artifact",
        }

        def all_keys(value):
            if isinstance(value, dict):
                for key, child in value.items():
                    yield key
                    yield from all_keys(child)
            elif isinstance(value, list):
                for child in value:
                    yield from all_keys(child)

        self.assertTrue(forbidden.isdisjoint(set(all_keys(report))))
        self.assertEqual("non_normative_s4_benchmark_evidence", report["artifact_kind"])
        self.assertNotIn(report["artifact_kind"], normative_artifact_kinds)
        self.assertNotIn("binding", report)
        self.assertEqual(
            {
                "family": "https://geesno.com/binding/ai-context-json",
                "version": "0.1.0",
            },
            report["projection_binding_under_test"],
        )

    def test_milestone_thresholds_do_not_leak_into_normative_or_i4_artifacts(self) -> None:
        protected_paths = (
            benchmark.PROFILE_PATH,
            ROOT / "spec" / "ai-context-profile.md",
            benchmark.I2_SCHEMA_PATH,
            ROOT / "tools" / "validation" / "ai_context_acceptance.py",
        )
        for path in protected_paths:
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertNotIn("10,000", text)
                self.assertNotIn("10%", text)
                self.assertNotIn("25%", text)


if __name__ == "__main__":
    unittest.main()
