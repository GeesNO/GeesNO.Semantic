from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[3]
SDK_ROOT = ROOT / "sdk" / "python"
if str(SDK_ROOT) not in sys.path:
    sys.path.insert(0, str(SDK_ROOT))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import geesno_semantic as sdk  # noqa: E402
from tools.validation import ai_context_acceptance  # noqa: E402


CORPUS = ROOT / "profiles" / "ai-context" / "conformance" / "v0.1"
SOURCE = CORPUS / "sources" / "source-context.json"

A101 = "urn:uuid:00000000-0000-4000-8000-00000000a101"
A102 = "urn:uuid:00000000-0000-4000-8000-00000000a102"
A103 = "urn:uuid:00000000-0000-4000-8000-00000000a103"
A201 = "urn:uuid:00000000-0000-4000-8000-00000000a201"
A301 = "urn:uuid:00000000-0000-4000-8000-00000000a301"
A401 = "urn:uuid:00000000-0000-4000-8000-00000000a401"
A402 = "urn:uuid:00000000-0000-4000-8000-00000000a402"
A404 = "urn:uuid:00000000-0000-4000-8000-00000000a404"


class SdkProjectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = sdk.load_path(SOURCE)

    @staticmethod
    def selection_context(*record_ids: str) -> dict:
        return {
            "selection_context_kind": "fixture-explicit-records",
            "selection_descriptor": {"record_ids": list(record_ids)},
        }

    @staticmethod
    def projection_scope(*record_ids: str) -> dict:
        return {
            "scope_kind": "fixture-record-set",
            "scope_descriptor": {"record_ids": list(record_ids)},
            "requirement_reference": "projection-baseline",
        }

    def projection(
        self,
        *,
        selected: dict[str, list[str]] | None = None,
        record_ids: tuple[str, ...] = (A103,),
        completeness: str = "complete",
        **kwargs: object,
    ) -> sdk.Projection:
        return self.source.create_projection(
            selection_context=self.selection_context(*record_ids),
            projection_scope=self.projection_scope(*record_ids),
            projection_completeness=completeness,
            carried_content_selection=selected or {"entities": list(record_ids)},
            reference_availability=[],
            source_state_descriptor="fixture-state-r1",
            **kwargs,
        )

    def test_minimal_projection_uses_exact_contract_and_passes_s4(self) -> None:
        projection = self.projection()

        self.assertEqual("projection_artifact", projection["artifact_kind"])
        self.assertEqual(
            {
                "family": "https://geesno.com/binding/ai-context-json",
                "version": "0.1.0",
            },
            projection["binding"],
        )
        self.assertEqual(
            {
                "profile_family": "https://geesno.com/profile/ai-context",
                "profile_version": "0.1.0",
            },
            projection["profile_edition"],
        )
        self.assertNotIn("projection_artifact_id", projection)
        self.assertEqual([], sdk.projection_structural_errors(projection))
        self.assertEqual(
            [], sdk.projection_semantic_errors(projection, self.source)
        )

        explicit = self.projection(
            projection_artifact_id="https://example.invalid/projections/explicit"
        )
        self.assertEqual(
            "https://example.invalid/projections/explicit",
            explicit["projection_artifact_id"],
        )

    def test_source_state_revision_and_scope_are_explicitly_distinct(self) -> None:
        source = sdk.SemanticDocument.create(
            spec_version="0.1.0",
            identifier="https://example.invalid/documents/revisioned",
            scope={"completeness": "complete"},
        )
        source.set_revision(identifier="https://example.invalid/revisions/r1")
        projection = source.create_projection(
            selection_context={
                "selection_context_kind": "explicit-test-selection",
                "selection_descriptor": "selection-context",
            },
            projection_scope={
                "scope_kind": "explicit-test-scope",
                "scope_descriptor": "projection-scope",
            },
            projection_completeness="unknown",
            carried_content_selection={},
            reference_availability=[],
            include_source_scope=True,
            include_revision=True,
        )

        self.assertEqual(
            "https://example.invalid/revisions/r1",
            projection["source_state"]["semantic_revision_id"],
        )
        self.assertNotIn("source_state_descriptor", projection["source_state"])
        self.assertEqual(
            {"completeness": "complete"}, projection["source_state"]["source_scope"]
        )
        self.assertEqual(
            "selection-context",
            projection["selection_context"]["selection_descriptor"],
        )
        self.assertEqual(
            "projection-scope", projection["projection_scope"]["scope_descriptor"]
        )
        self.assertEqual(
            "https://example.invalid/revisions/r1",
            projection.revision.identifier,
        )
        self.assertEqual([], sdk.projection_structural_errors(projection))

        without_revision = sdk.SemanticDocument.create(
            spec_version="0.1.0",
            identifier="https://example.invalid/documents/unrevisioned",
            scope={"completeness": "unknown"},
        )
        with self.assertRaisesRegex(ValueError, "source_state_descriptor"):
            without_revision.create_projection(
                selection_context={
                    "selection_context_kind": "explicit-test-selection",
                    "selection_descriptor": "selection-context",
                },
                projection_scope={
                    "scope_kind": "explicit-test-scope",
                    "scope_descriptor": "projection-scope",
                },
                projection_completeness="unknown",
                carried_content_selection={},
                reference_availability=[],
            )

    def test_completeness_and_empty_carried_content_are_caller_declared(self) -> None:
        for completeness in ("complete", "partial", "unknown"):
            with self.subTest(completeness=completeness):
                projection = self.projection(
                    selected={},
                    record_ids=(),
                    completeness=completeness,
                )
                self.assertEqual(completeness, projection["projection_completeness"])
                self.assertEqual({}, projection["carried_content"])
                self.assertNotIn("omissions", projection)
                self.assertEqual([], sdk.projection_structural_errors(projection))
                self.assertEqual(
                    [], sdk.projection_semantic_errors(projection, self.source)
                )

    def test_selection_has_no_hidden_closure_or_omission_semantics(self) -> None:
        projection = self.projection(
            selected={"entities": [A101]},
            record_ids=(A101,),
            namespaces={
                "test": "https://example.invalid/terms/",
                "ext": "https://example.invalid/extensions/",
            },
        )

        self.assertEqual([A101], [entity.identifier for entity in projection.entities])
        self.assertEqual((), projection.assertions)
        self.assertEqual((), projection.sources)
        self.assertEqual((), projection.bindings)
        self.assertEqual((), projection.tombstones)
        self.assertIsNone(projection.get_record(A102))
        self.assertNotIn("omissions", projection)
        self.assertNotIn("tombstones", projection.carried_content)

    def test_projection_and_source_are_independent_and_records_remain_exact(self) -> None:
        before = copy.deepcopy(self.source.backing_tree)
        availability = [
            {
                "reference_target": target,
                "availability_state": "carried",
            }
            for target in (A101, A102, A201)
        ]
        projection = self.source.create_projection(
            selection_context=self.selection_context(A101, A102, A201, A301, A401),
            projection_scope=self.projection_scope(A101, A102, A201, A301, A401),
            projection_completeness="complete",
            carried_content_selection={
                "entities": [A101, A102],
                "sources": [A201],
                "bindings": [A301],
                "assertions": [A401],
            },
            reference_availability=availability,
            source_state_descriptor="fixture-state-r1",
            namespaces={
                "test": "https://example.invalid/terms/",
                "ext": "https://example.invalid/extensions/",
            },
        )

        self.assertEqual(before, self.source.backing_tree)
        self.assertEqual(A301, projection.bindings[0].identifier)
        self.assertEqual(A401, projection.assertions[0].identifier)
        self.assertEqual("test:related", projection.assertions[0]["predicate"])
        self.assertEqual(
            [
                "urn:uuid:00000000-0000-4000-8000-00000000a111",
            ],
            [item.identifier for item in projection.entities[0].provenance],
        )
        self.assertEqual("test:interval", projection.entities[0].validity.kind)
        self.assertEqual([], sdk.projection_structural_errors(projection))
        self.assertEqual(
            [], sdk.projection_semantic_errors(projection, self.source)
        )

        projection.entities[0].backing_record["kind"] = "representation"
        self.assertEqual("concept", self.source.entities[0].kind)
        self.source.entities[1].backing_record["kind"] = "concept"
        self.assertEqual("representation", projection.entities[1].kind)

    def test_namespace_extensions_and_raw_numbers_survive_round_trip(self) -> None:
        projection = self.projection(
            selected={"entities": [A101]},
            record_ids=(A101,),
            namespaces={
                "test": "https://example.invalid/terms/",
                "ext": "https://example.invalid/extensions/",
            },
            material_context=[
                {
                    "descriptor_id": "material-extension-host-a101",
                    "context_target": A101,
                    "preservation_state": "carried",
                    "carried_record_reference": A101,
                    "requirement_reference": "material-context-carry",
                }
            ],
        )
        token = projection.entities[0]["extensions"]["ext:opaque"]["nested"][0]
        self.assertIsInstance(token, sdk.RawNumber)
        self.assertEqual("1", token.token)
        self.assertEqual(
            {
                "test": "https://example.invalid/terms/",
                "ext": "https://example.invalid/extensions/",
            },
            projection.namespaces,
        )
        reloaded = sdk.load_projection_bytes(sdk.dump_projection_bytes(projection))
        reloaded_token = reloaded.entities[0]["extensions"]["ext:opaque"]["nested"][0]
        self.assertIsInstance(reloaded_token, sdk.RawNumber)
        self.assertEqual("1", reloaded_token.token)
        self.assertEqual([], sdk.projection_structural_errors(reloaded))
        self.assertEqual([], sdk.projection_semantic_errors(reloaded, self.source))

        with self.assertRaisesRegex(ValueError, "does not match"):
            self.projection(
                selected={"entities": [A101]},
                record_ids=(A101,),
                namespaces={"test": "https://wrong.invalid/"},
            )

    def test_omission_continuation_and_material_context_remain_inert(self) -> None:
        valid = json.loads(
            (CORPUS / "valid" / "v07-omission-dependency-continuation.json").read_text(
                encoding="utf-8"
            )
        )
        before = copy.deepcopy(self.source.backing_tree)

        with mock.patch("socket.socket", side_effect=AssertionError("network used")), mock.patch(
            "urllib.request.urlopen", side_effect=AssertionError("URL opened")
        ), mock.patch("builtins.open", side_effect=AssertionError("file opened")):
            projection = self.source.create_projection(
                selection_context=valid["selection_context"],
                projection_scope=valid["projection_scope"],
                projection_completeness=valid["projection_completeness"],
                carried_content_selection={
                    "entities": [A101],
                    "assertions": [A404],
                },
                reference_availability=valid["reference_availability"],
                source_state_descriptor="fixture-state-r1",
                namespaces={
                    **valid["namespaces"],
                    "ext": "https://example.invalid/extensions/",
                },
                omissions=valid["omissions"],
                dependency_continuations=valid["dependency_continuations"],
                material_context=valid["material_context"],
            )
            self.assertEqual(A404, projection.get_record(A404).identifier)
            self.assertEqual((), projection.tombstones)

        self.assertEqual(before, self.source.backing_tree)
        self.assertEqual([], sdk.projection_structural_errors(projection))
        self.assertEqual([], sdk.projection_semantic_errors(projection, self.source))

    def test_bounds_truncation_and_projection_continuation_are_caller_metadata(self) -> None:
        bounded = json.loads(
            (CORPUS / "valid" / "v02-bounded-partial-truncation.json").read_text(
                encoding="utf-8"
            )
        )
        projection = self.source.create_projection(
            selection_context=bounded["selection_context"],
            projection_scope=bounded["projection_scope"],
            projection_completeness=bounded["projection_completeness"],
            carried_content_selection={"entities": [A103]},
            reference_availability=[],
            source_state_descriptor="fixture-state-r1",
            boundedness=bounded["boundedness"],
            truncation=bounded["truncation"],
        )
        self.assertEqual(bounded["boundedness"], projection["boundedness"])
        self.assertEqual(bounded["truncation"], projection["truncation"])
        self.assertEqual([], sdk.projection_structural_errors(projection))
        self.assertEqual([], sdk.projection_semantic_errors(projection, self.source))

        continued = json.loads(
            (CORPUS / "valid" / "v08-projection-continuation.json").read_text(
                encoding="utf-8"
            )
        )
        projection = self.source.create_projection(
            selection_context=continued["selection_context"],
            projection_scope=continued["projection_scope"],
            projection_completeness=continued["projection_completeness"],
            carried_content_selection={"entities": [A103]},
            reference_availability=[],
            source_state_descriptor="fixture-state-r1",
            projection_continuations=continued["projection_continuations"],
        )
        self.assertEqual(
            continued["projection_continuations"],
            projection["projection_continuations"],
        )
        self.assertEqual([], sdk.projection_structural_errors(projection))
        self.assertEqual([], sdk.projection_semantic_errors(projection, self.source))

    def test_local_queries_are_exact_and_never_fall_back_to_source(self) -> None:
        projection = self.source.create_projection(
            selection_context=self.selection_context(A101, A401, A402),
            projection_scope=self.projection_scope(A101, A401, A402),
            projection_completeness="complete",
            carried_content_selection={
                "entities": [A101],
                "assertions": [A401, "urn:uuid:00000000-0000-4000-8000-00000000a402"],
            },
            reference_availability=[
                {"reference_target": A101, "availability_state": "carried"},
                {"reference_target": A102, "availability_state": "external"},
            ],
            source_state_descriptor="fixture-state-r1",
            namespaces={
                "test": "https://example.invalid/terms/",
                "ext": "https://example.invalid/extensions/",
            },
        )

        self.assertEqual(A101, projection.get_record(A101, category="entities").identifier)
        self.assertIsNone(projection.get_record(A103))
        self.assertEqual(
            [A401],
            [
                assertion.identifier
                for assertion in projection.find_assertions(
                    subject_target=A101,
                    kind="relation",
                    term="test:related",
                )
            ],
        )
        self.assertEqual((), projection.find_assertions(term="test:RELAted"))
        self.assertFalse(hasattr(projection, "search"))
        self.assertFalse(hasattr(projection, "traverse"))
        self.assertFalse(hasattr(projection, "rank"))

    def test_s4_and_s5_tooling_are_reused_without_parallel_semantics(self) -> None:
        projection = self.projection()
        run = sdk.assess_projection(projection, self.source)
        self.assertTrue(run.enumeration_available)
        self.assertEqual(9, len(run.results))

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
        result = sdk.construct_projection_result(
            satisfied,
            assessment_subject={
                "subject_role": "projection_artifact",
                "reference_strategy": "stable_artifact_identity",
                "artifact_id": "https://example.invalid/projections/one",
            },
            requirement_references=references,
        )
        self.assertEqual("conformant", result["overall_outcome"])
        self.assertEqual("conformance_result_artifact", result["artifact_kind"])

        corpus = ai_context_acceptance.run_corpus()
        self.assertEqual((12, 4, 18), (
            corpus.valid_passed,
            corpus.structural_invalid_rejected,
            corpus.semantic_invalid_rejected,
        ))
        self.assertEqual((), corpus.errors)

    def test_public_surface_has_no_d8_or_general_profile_engine(self) -> None:
        public = set(sdk.__all__)
        forbidden_fragments = (
            "composite",
            "composition",
            "conflict",
            "registry",
            "resolver",
            "latest_profile",
            "embedding",
            "prompt",
        )
        self.assertFalse(
            {
                name
                for name in public
                if any(fragment in name.casefold() for fragment in forbidden_fragments)
            }
        )


if __name__ == "__main__":
    unittest.main()
