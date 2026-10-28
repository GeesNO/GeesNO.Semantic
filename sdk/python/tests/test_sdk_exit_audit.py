from __future__ import annotations

import ast
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[3]
SDK_ROOT = ROOT / "sdk" / "python"
if str(SDK_ROOT) not in sys.path:
    sys.path.insert(0, str(SDK_ROOT))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from conformance.runner.fixture_runner import (  # noqa: E402
    CONFORMANCE,
    SCHEMA_PATH,
    fixture_files,
    validate_bytes as validate_s2_bytes,
)
from conformance.runner.schema_validation import load_schema  # noqa: E402
import geesno_semantic as sdk  # noqa: E402
import geesno_semantic.projection as projection_module  # noqa: E402
from tools.validation import ai_context_acceptance  # noqa: E402


S4_CORPUS = ROOT / "profiles" / "ai-context" / "conformance" / "v0.1"
S4_SOURCE = S4_CORPUS / "sources" / "source-context.json"

PUBLIC_API_BY_PHASE = {
    "I1": {
        "RawInputError",
        "RawNumber",
        "ResourceLimits",
        "ResourceRefusal",
        "SemanticDocument",
        "UnsupportedVersion",
        "VersionError",
        "dump_bytes",
        "dump_text",
        "load_bytes",
        "load_path",
        "load_text",
        "save_path",
        "validate_bytes",
        "validate_document",
        "validate_path",
    },
    "I2": {"Concept", "Representation", "new_uuid_urn"},
    "I3": {
        "Assertion",
        "Binding",
        "ConceptRepresentationAssertion",
        "PropertyAssertion",
        "RelationAssertion",
        "Source",
        "TypeAssertion",
        "boolean_value",
        "condition",
        "date_time_value",
        "date_value",
        "decimal_value",
        "descriptor",
        "fingerprint",
        "integer_value",
        "list_value",
        "quantity_value",
        "reference",
        "reference_value",
        "set_value",
        "string_value",
        "structured_value",
    },
    "I4": {"Confidence", "Provenance", "Review"},
    "I5": {"Change", "Revision", "Tombstone", "Validity"},
    "I6": {"VocabularyView", "expand_qualified_term", "split_qualified_term"},
    "I7": {
        "AI_CONTEXT_PROFILE_EDITION",
        "AI_CONTEXT_PROJECTION_BINDING",
        "DiagnosticInput",
        "ExactAssessmentContext",
        "MaterialContextFact",
        "Projection",
        "RequirementAssessment",
        "RequirementAssessmentRun",
        "assess_projection",
        "construct_projection_result",
        "create_projection",
        "dump_projection_bytes",
        "dump_projection_text",
        "load_projection_bytes",
        "load_projection_text",
        "projection_semantic_errors",
        "projection_structural_errors",
    },
}


def imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    return modules


class SdkExitAuditTests(unittest.TestCase):
    def test_public_api_is_exactly_classified_by_i1_through_i7(self) -> None:
        classified = set().union(*PUBLIC_API_BY_PHASE.values())
        self.assertEqual(classified, set(sdk.__all__))
        self.assertEqual(
            sum(len(symbols) for symbols in PUBLIC_API_BY_PHASE.values()),
            len(classified),
        )
        for phase, symbols in PUBLIC_API_BY_PHASE.items():
            for symbol in symbols:
                with self.subTest(phase=phase, symbol=symbol):
                    self.assertTrue(hasattr(sdk, symbol))

        forbidden_fragments = (
            "adapter",
            "agent",
            "command",
            "composite",
            "embedding",
            "execution",
            "permission",
            "plugin",
            "prompt",
            "rag",
            "registry",
            "resolver",
            "retrieval",
            "transaction",
            "vector",
        )
        self.assertFalse(
            {
                name
                for name in sdk.__all__
                if any(fragment in name.casefold() for fragment in forbidden_fragments)
            }
        )

    def test_authority_dependency_and_runtime_boundaries_are_one_way(self) -> None:
        authority_files = list((ROOT / "conformance" / "runner").glob("*.py"))
        authority_files.extend((ROOT / "tools" / "validation").glob("*.py"))
        for path in authority_files:
            with self.subTest(authority=path.relative_to(ROOT)):
                self.assertFalse(
                    {
                        module
                        for module in imported_modules(path)
                        if module == "geesno_semantic"
                        or module.startswith("geesno_semantic.")
                    }
                )

        projection_imports = imported_modules(
            SDK_ROOT / "geesno_semantic" / "projection.py"
        )
        self.assertIn("tools.validation", projection_imports)

        forbidden_dependencies = {
            "aiohttp",
            "anthropic",
            "boto3",
            "faiss",
            "google.generativeai",
            "httpx",
            "langchain",
            "openai",
            "requests",
            "socket",
            "urllib.request",
        }
        forbidden_domains = {
            "autocad",
            "bim",
            "excel",
            "ifc",
            "pdf",
            "revit",
            "sqlalchemy",
        }
        for path in (SDK_ROOT / "geesno_semantic").glob("*.py"):
            imports = imported_modules(path)
            roots = {module.casefold() for module in imports}
            with self.subTest(sdk_module=path.name):
                self.assertFalse(roots & forbidden_dependencies)
                self.assertFalse(roots & forbidden_domains)

    def test_all_s2_valid_fixtures_round_trip_without_semantic_loss(self) -> None:
        valid = fixture_files(CONFORMANCE / "valid")
        self.assertEqual(17, len(valid))
        for fixture in valid:
            with self.subTest(fixture=fixture.name):
                document = sdk.load_bytes(fixture.read_bytes())
                before = copy.deepcopy(document.backing_tree)
                reloaded = sdk.load_bytes(sdk.dump_bytes(document))
                self.assertEqual(before, document.backing_tree)
                self.assertEqual(before, reloaded.backing_tree)
                self.assertEqual({"result": "valid"}, sdk.validate_document(reloaded))

    def test_all_s2_invalid_and_resource_boundaries_match_approved_results(self) -> None:
        schema = load_schema(SCHEMA_PATH)
        invalid = fixture_files(CONFORMANCE / "invalid")
        self.assertEqual(84, len(invalid))
        for fixture in invalid:
            with self.subTest(fixture=fixture.name):
                data = fixture.read_bytes()
                expected = json.loads(
                    (CONFORMANCE / "expected" / f"{fixture.stem}.json").read_text(
                        encoding="utf-8"
                    )
                )
                self.assertEqual(expected, validate_s2_bytes(data, schema))
                self.assertEqual(expected, sdk.validate_bytes(data))
                self.assertNotEqual("valid", expected["result"])

        representative_boundaries = {
            "raw-duplicate-root": (0, "duplicate-member"),
            "raw-invalid-utf8": (0, "invalid-utf8"),
            "raw-resource-refusal": (0, "nesting-limit"),
            "schema-property-raw-number": (2, "schema"),
            "semantic-confidence-above": (3, "confidence-range"),
            "version-future": (1, "unsupported-version"),
        }
        for name, (layer, category) in representative_boundaries.items():
            with self.subTest(boundary=name):
                recorded = json.loads(
                    (CONFORMANCE / "expected" / f"{name}.json").read_text(
                        encoding="utf-8"
                    )
                )
                self.assertEqual(layer, recorded["layer"])
                self.assertEqual(category, recorded["category"])

    def test_all_s4_valid_projections_round_trip_and_outcomes_remain_exact(self) -> None:
        source = sdk.load_path(S4_SOURCE)
        source_before = copy.deepcopy(source.backing_tree)
        valid = sorted((S4_CORPUS / "valid").glob("*.json"))
        self.assertEqual(12, len(valid))
        for fixture in valid:
            with self.subTest(fixture=fixture.name):
                projection = sdk.load_projection_bytes(fixture.read_bytes())
                before = copy.deepcopy(projection.backing_artifact)

                tuple(projection.entities)
                tuple(projection.sources)
                tuple(projection.bindings)
                tuple(projection.assertions)
                tuple(projection.tombstones)
                projection.revision
                projection.namespaces
                projection.find_assertions()

                reloaded = sdk.load_projection_bytes(
                    sdk.dump_projection_bytes(projection)
                )
                self.assertEqual(before, projection.backing_artifact)
                self.assertEqual(before, reloaded.backing_artifact)
                self.assertEqual([], sdk.projection_structural_errors(reloaded))
                self.assertEqual(
                    [],
                    sdk.projection_semantic_errors(
                        reloaded, source, fixture_name=fixture.name
                    ),
                )

        self.assertEqual(source_before, source.backing_tree)
        run = ai_context_acceptance.run_corpus()
        self.assertEqual(
            (12, 4, 18, ()),
            (
                run.valid_passed,
                run.structural_invalid_rejected,
                run.semantic_invalid_rejected,
                run.errors,
            ),
        )

    def test_read_validation_projection_and_assessment_are_offline_and_nonmutating(self) -> None:
        source = sdk.load_path(S4_SOURCE)
        projection = sdk.load_projection_bytes(
            (S4_CORPUS / "valid" / "v07-omission-dependency-continuation.json").read_bytes()
        )
        source_before = copy.deepcopy(source.backing_tree)
        projection_before = copy.deepcopy(projection.backing_artifact)
        local_terms = {"test:related": {"label": "related"}}
        vocabulary = sdk.VocabularyView(
            identity="https://example.invalid/vocabulary/test",
            version="1.0.0",
            terms=local_terms,
        )

        network_failure = AssertionError("network access attempted")
        with (
            mock.patch("socket.socket", side_effect=network_failure),
            mock.patch("socket.create_connection", side_effect=network_failure),
            mock.patch("socket.getaddrinfo", side_effect=network_failure),
            mock.patch("urllib.request.urlopen", side_effect=network_failure),
        ):
            self.assertEqual({"result": "valid"}, sdk.validate_document(source))
            tuple(source.entities)
            tuple(source.sources)
            tuple(source.bindings)
            tuple(source.assertions)
            tuple(source.trust_hosts)
            tuple(source.extension_hosts)
            source.entities[0].get_extension("ext:opaque")
            self.assertEqual(
                "https://example.invalid/terms/related",
                source.expand_term("test:related"),
            )
            self.assertTrue(vocabulary.has_term("test:related"))
            self.assertEqual({"label": "related"}, vocabulary.get_term("test:related"))
            projection.get_record(
                "urn:uuid:00000000-0000-4000-8000-00000000a101"
            )
            projection.find_assertions()
            self.assertEqual([], sdk.projection_structural_errors(projection))
            self.assertEqual([], sdk.projection_semantic_errors(projection, source))
            assessment = sdk.assess_projection(projection, source)
            self.assertEqual(9, len(assessment.results))

        self.assertEqual(source_before, source.backing_tree)
        self.assertEqual(projection_before, projection.backing_artifact)
        self.assertEqual({"test:related": {"label": "related"}}, local_terms)

    def test_projection_validation_and_assessment_are_exact_thin_delegations(self) -> None:
        source = sdk.load_path(S4_SOURCE)
        projection = sdk.load_projection_bytes(
            (S4_CORPUS / "valid" / "v01-complete-narrow.json").read_bytes()
        )
        with mock.patch.object(
            projection_module._s4_acceptance,
            "structural_errors",
            wraps=projection_module._s4_acceptance.structural_errors,
        ) as structural:
            self.assertEqual([], sdk.projection_structural_errors(projection))
            structural.assert_called_once()
        with mock.patch.object(
            projection_module._s4_acceptance,
            "semantic_errors",
            wraps=projection_module._s4_acceptance.semantic_errors,
        ) as semantic:
            self.assertEqual([], sdk.projection_semantic_errors(projection, source))
            semantic.assert_called_once()
        with mock.patch.object(
            projection_module._s5_assessment,
            "assess_exact_profile_0_1",
            wraps=projection_module._s5_assessment.assess_exact_profile_0_1,
        ) as assessor:
            run = sdk.assess_projection(projection, source)
            assessor.assert_called_once()

        satisfied = sdk.RequirementAssessmentRun(
            True,
            tuple(
                sdk.RequirementAssessment(result.requirement_id, "satisfied")
                for result in run.results
            ),
        )
        references = {
            result.requirement_id: {
                "reference_strategy": "stable_requirement_reference",
                "requirement_id": result.requirement_id,
            }
            for result in satisfied.results
        }
        with mock.patch.object(
            projection_module._s5_results,
            "construct_conformance_result",
            wraps=projection_module._s5_results.construct_conformance_result,
        ) as constructor:
            result = sdk.construct_projection_result(
                satisfied,
                assessment_subject={
                    "subject_role": "projection_artifact",
                    "reference_strategy": "stable_artifact_identity",
                    "artifact_id": "https://example.invalid/projections/exit-audit",
                },
                requirement_references=references,
            )
            constructor.assert_called_once()
        self.assertEqual("conformant", result["overall_outcome"])

    def test_clean_process_smoke_covers_core_projection_and_exact_assessment(self) -> None:
        script = r'''
from pathlib import Path
from unittest import mock
import geesno_semantic as sdk

blocked = AssertionError("network access attempted")
with mock.patch("socket.socket", side_effect=blocked), mock.patch(
    "socket.getaddrinfo", side_effect=blocked
), mock.patch("urllib.request.urlopen", side_effect=blocked):
    document = sdk.SemanticDocument.create(
        spec_version="0.1.0",
        identifier="urn:uuid:00000000-0000-4000-8000-00000000b000",
        scope={"completeness": "partial"},
        namespaces={"test": "https://example.invalid/terms/"},
    )
    concept = document.add_concept(
        identifier="urn:uuid:00000000-0000-4000-8000-00000000b001"
    )
    representation = document.add_representation(
        identifier="urn:uuid:00000000-0000-4000-8000-00000000b002"
    )
    document.add_concept_representation_assertion(
        identifier="urn:uuid:00000000-0000-4000-8000-00000000b003",
        representation=sdk.reference(
            target=representation.identifier, location="in-document"
        ),
        concept=sdk.reference(target=concept.identifier, location="in-document"),
    )
    reloaded = sdk.load_bytes(sdk.dump_bytes(document))
    assert sdk.validate_document(reloaded) == {"result": "valid"}

    source = sdk.load_path(
        Path("profiles/ai-context/conformance/v0.1/sources/source-context.json")
    )
    selected = "urn:uuid:00000000-0000-4000-8000-00000000a103"
    projection = source.create_projection(
        selection_context={
            "selection_context_kind": "fixture-explicit-records",
            "selection_descriptor": {"record_ids": [selected]},
        },
        projection_scope={
            "scope_kind": "fixture-record-set",
            "scope_descriptor": {"record_ids": [selected]},
            "requirement_reference": "projection-baseline",
        },
        projection_completeness="complete",
        carried_content_selection={"entities": [selected]},
        reference_availability=[],
        source_state_descriptor="fixture-state-r1",
    )
    assert projection.get_record(selected).identifier == selected
    assert sdk.projection_structural_errors(projection) == []
    assert sdk.projection_semantic_errors(projection, source) == []
    assert len(sdk.assess_projection(projection, source).results) == 9
print("S6-SDK-SMOKE-PASS")
'''
        environment = os.environ.copy()
        environment["PYTHONPATH"] = os.pathsep.join((str(SDK_ROOT), str(ROOT)))
        completed = subprocess.run(
            [sys.executable, "-c", script],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        self.assertEqual("S6-SDK-SMOKE-PASS", completed.stdout.strip())


if __name__ == "__main__":
    unittest.main()
