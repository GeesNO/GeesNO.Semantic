from __future__ import annotations
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from tools.validation import (
    ai_context_acceptance,
    ai_context_assessment_corpus,
    ai_context_requirement_assessment,
    ai_context_result_construction,
    check_repository,
)


class RepositoryBaselineTests(unittest.TestCase):

    def test_repository_passes_baseline_guards(self) -> None:
        self.assertEqual(check_repository.check_repository(), [])

    def test_public_documentation_navigation_from_root(self) -> None:
        root = check_repository.ROOT
        readme = (root / "README.md").read_text(encoding="utf-8")
        documentation_map = (root / check_repository.DOCUMENTATION_MAP).read_text(
            encoding="utf-8"
        )

        self.assertIn("[Documentation Map](docs/README.md)", readme)
        self.assertEqual(
            [],
            check_repository.missing_contract_markers(
                documentation_map,
                check_repository.DOCUMENTATION_MAP_MARKERS,
            ),
        )
        navigation_targets = check_repository.repository_link_targets(
            root / check_repository.DOCUMENTATION_MAP,
            root,
        )
        for relative in check_repository.PUBLIC_NAVIGATION_TARGETS:
            self.assertIn(relative, navigation_targets)
            self.assertTrue((root / relative).is_file(), relative)
        self.assertNotIn("PROJECT_FOUNDATION.md", documentation_map)
        self.assertNotIn(check_repository.S7_P9_RECORD, documentation_map)

        for relative in check_repository.PUBLIC_ENTRY_DOCS:
            text = (root / relative).read_text(encoding="utf-8")
            self.assertIsNone(
                check_repository.LOCAL_ABSOLUTE_PATH.search(text), relative
            )
            for marker in check_repository.README_FORBIDDEN_PUBLIC_CLAIMS:
                self.assertNotIn(marker, text)

    def test_implementation_guide_is_language_neutral_and_traceable(self) -> None:
        root = check_repository.ROOT
        guide = (root / check_repository.IMPLEMENTATION_GUIDE).read_text(
            encoding="utf-8"
        )

        self.assertEqual(
            [],
            check_repository.missing_contract_markers(
                guide,
                check_repository.IMPLEMENTATION_GUIDE_MARKERS,
            ),
        )
        guide_targets = check_repository.repository_link_targets(
            root / check_repository.IMPLEMENTATION_GUIDE,
            root,
        )
        for relative in check_repository.IMPLEMENTATION_GUIDE_TRACE_TARGETS:
            self.assertIn(relative, guide_targets)
            self.assertTrue((root / relative).is_file(), relative)
        for token in check_repository.IMPLEMENTATION_GUIDE_FORBIDDEN_TOKENS:
            self.assertNotIn(token, guide)
        self.assertIsNone(check_repository.LOCAL_ABSOLUTE_PATH.search(guide))
        for marker in check_repository.README_FORBIDDEN_PUBLIC_CLAIMS:
            self.assertNotIn(marker, guide)

    def test_conformance_guide_is_bounded_offline_and_traceable(self) -> None:
        root = check_repository.ROOT
        guide = (root / check_repository.CONFORMANCE_GUIDE).read_text(
            encoding="utf-8"
        )

        self.assertEqual(
            [],
            check_repository.missing_contract_markers(
                guide,
                check_repository.CONFORMANCE_GUIDE_MARKERS,
            ),
        )
        guide_targets = check_repository.repository_link_targets(
            root / check_repository.CONFORMANCE_GUIDE,
            root,
        )
        for relative in check_repository.CONFORMANCE_GUIDE_TRACE_TARGETS:
            self.assertIn(relative, guide_targets)
            self.assertTrue((root / relative).is_file(), relative)
        for token in check_repository.CONFORMANCE_GUIDE_FORBIDDEN_TOKENS:
            self.assertNotIn(token, guide)
        self.assertIsNone(check_repository.LOCAL_ABSOLUTE_PATH.search(guide))
        self.assertIn("reference repository workflows, not normative APIs", guide)
        self.assertIn("The reference runner is Python; the conformance contract is not", guide)
        self.assertIn("conformance\n!= semantic truth", guide)
        self.assertIn("diagnostic\n!= semantic Assertion", guide)
        self.assertIn("AI Context assessment corpus catalogue", guide)

    def test_public_adr_index_covers_accepted_architecture(self) -> None:
        adr_index = (check_repository.ROOT / "adr" / "README.md").read_text(
            encoding="utf-8"
        )
        self.assertEqual(
            [],
            check_repository.missing_contract_markers(
                adr_index,
                check_repository.ADR_INDEX_ARCHITECTURE_MARKERS,
            ),
        )
        for boundary in (
            "ADR-0001 through ADR-0008",
            "ADR-0009 through ADR-0016",
            "ADR-0017 through ADR-0023",
            "ADR-0024 through ADR-0031",
        ):
            self.assertIn(boundary, adr_index)
        for marker in check_repository.ADR_INDEX_FORBIDDEN_OPERATIONAL_MARKERS:
            self.assertNotIn(marker, adr_index)

    def test_i5_i6_implementation_and_tests_are_required_repository_files(self) -> None:
        self.assertIn(
            "tools/validation/ai_context_requirement_assessment.py",
            check_repository.REQUIRED_FILES,
        )
        self.assertIn(
            "tools/validation/tests/test_ai_context_requirement_assessment.py",
            check_repository.REQUIRED_FILES,
        )
        self.assertIn(
            "tools/validation/ai_context_result_construction.py",
            check_repository.REQUIRED_FILES,
        )
        self.assertIn(
            "tools/validation/tests/test_ai_context_result_construction.py",
            check_repository.REQUIRED_FILES,
        )

    def test_i7_integration_cli_and_tests_are_required_repository_files(self) -> None:
        for relative in (
            "tools/validation/integration_boundaries.py",
            "tools/validation/integrated_conformance.py",
            "tools/validation/reference_cli.py",
            "tools/validation/tests/test_integrated_conformance.py",
        ):
            self.assertIn(relative, check_repository.REQUIRED_FILES)

    def test_local_markdown_target_resolution(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / "target.md"
            source = root / "source.md"
            target.write_text("# Target\n", encoding="utf-8")
            source.write_text("[Target](target.md#section)\n", encoding="utf-8")
            self.assertEqual(
                check_repository.local_markdown_targets(source),
                [target.resolve()],
            )

    def test_markdown_link_checker_rejects_broken_and_escaping_links(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = base / "repository"
            root.mkdir()
            outside = base / "outside.md"
            outside.write_text("# Outside\n", encoding="utf-8")
            (root / "source.md").write_text(
                "[Missing](missing.md)\n[Outside](../outside.md)\n",
                encoding="utf-8",
            )
            errors = check_repository.markdown_link_errors(root)
            self.assertTrue(any("broken local link" in error for error in errors))
            self.assertTrue(any("escapes repository" in error for error in errors))

    def test_public_contract_checks_reject_missing_authority_and_false_claims(self) -> None:
        docs = (
            check_repository.ROOT / check_repository.DOCUMENTATION_MAP
        ).read_text(encoding="utf-8")
        missing_authority = docs.replace("ARCHITECTURE.md", "MISSING.md")
        self.assertTrue(
            check_repository.public_document_contract_errors(
                check_repository.DOCUMENTATION_MAP,
                missing_authority,
            )
        )
        internal_authority = docs + "\nPROJECT_FOUNDATION.md\n"
        self.assertTrue(
            any(
                "internal record" in error
                for error in check_repository.public_document_contract_errors(
                    check_repository.DOCUMENTATION_MAP,
                    internal_authority,
                )
            )
        )

        preview = (check_repository.ROOT / check_repository.PUBLIC_PREVIEW).read_text(
            encoding="utf-8"
        )
        self.assertTrue(
            any(
                "improper certification claim" in error
                for error in check_repository.public_document_contract_errors(
                    check_repository.PUBLIC_PREVIEW,
                    preview + "\nOfficial certification program is established.\n",
                )
            )
        )

    def test_publication_claim_detection_rejects_only_affirmative_claims(self) -> None:
        preview = (check_repository.ROOT / check_repository.PUBLIC_PREVIEW).read_text(
            encoding="utf-8"
        )
        misleading_claims = (
            "Public Preview 0.1.0-preview.1 was published.",
            "Public Preview `0.1.0-preview.1` is released.",
            "Public Preview 0.1.0-preview.1 - published 2026-10-18.",
            "The public preview has been finalized.",
            "The preview has been released.",
            "The release has been published.",
            "We released Public Preview 0.1.0-preview.1.",
        )
        for claim in misleading_claims:
            with self.subTest(claim=claim):
                self.assertTrue(
                    any(
                        "unverified publication claim" in error
                        for error in check_repository.public_document_contract_errors(
                            check_repository.PUBLIC_PREVIEW,
                            preview + f"\n{claim}\n",
                        )
                    )
                )

        permitted_statements = (
            "Public Preview 0.1.0-preview.1 is not published.",
            "The preview has not yet been released.",
            "The planned Public Preview is pending.",
            "The release will not be considered published until verified.",
            (
                "Do not claim that Public Preview 0.1.0-preview.1 was published "
                "before verification."
            ),
            (
                "Historical records may quote the forbidden statement "
                '"Public Preview 0.1.0-preview.1 was published."'
            ),
            (
                "If Public Preview 0.1.0-preview.1 was published, "
                "a tag would exist."
            ),
            (
                "A statement that Public Preview 0.1.0-preview.1 was published "
                "would be misleading."
            ),
        )
        for statement in permitted_statements:
            with self.subTest(statement=statement):
                errors = check_repository.public_document_contract_errors(
                    check_repository.PUBLIC_PREVIEW,
                    preview + f"\n{statement}\n",
                )
                self.assertFalse(
                    any("unverified publication claim" in error for error in errors)
                )

    def test_publication_context_exception_cannot_hide_real_claim(self) -> None:
        preview = (check_repository.ROOT / check_repository.PUBLIC_PREVIEW).read_text(
            encoding="utf-8"
        )
        statements = (
            (
                "Historical records may quote the forbidden statement "
                '"Public Preview 0.1.0-preview.1 was published." '
                "The release has been published."
            ),
            (
                "Example: Public Preview 0.1.0-preview.1 was published. "
                "We released Public Preview 0.1.0-preview.1."
            ),
        )
        for statement in statements:
            with self.subTest(statement=statement):
                errors = check_repository.public_document_contract_errors(
                    check_repository.PUBLIC_PREVIEW,
                    preview + f"\n{statement}\n",
                )
                self.assertTrue(
                    any("unverified publication claim" in error for error in errors)
                )

    def test_publication_status_mutation_is_rejected(self) -> None:
        release_notes = (
            check_repository.ROOT / check_repository.RELEASE_NOTES
        ).read_text(encoding="utf-8")
        negative = "The preview has not yet been released."
        self.assertIn(negative, release_notes)
        mutated = release_notes.replace(
            negative,
            "The preview has been released.",
            1,
        )
        errors = check_repository.public_document_contract_errors(
            check_repository.RELEASE_NOTES,
            mutated,
        )
        self.assertTrue(any("unverified publication claim" in error for error in errors))

    def test_public_contract_checks_preserve_security_and_non_execution(self) -> None:
        security = (
            check_repository.ROOT / check_repository.SECURITY_POLICY
        ).read_text(encoding="utf-8")
        without_inertness = security.replace(
            "Extensions are inert semantic data, not executable plugins.",
            "Extensions may execute plugins.",
        )
        errors = check_repository.public_document_contract_errors(
            check_repository.SECURITY_POLICY,
            without_inertness,
        )
        self.assertTrue(any("Extensions are inert" in error for error in errors))
        active_channel = security + "\nPrivate reporting channel active: yes\n"
        self.assertTrue(
            any(
                "unverified private channel" in error
                for error in check_repository.public_document_contract_errors(
                    check_repository.SECURITY_POLICY,
                    active_channel,
                )
            )
        )

    def test_public_assessment_catalog_is_exact_and_regressions_are_rejected(self) -> None:
        catalog = (
            check_repository.ROOT / check_repository.AI_CONTEXT_ASSESSMENT_CATALOG
        ).read_text(encoding="utf-8")
        inventory = (
            check_repository.ROOT / check_repository.S5_CORPUS_INVENTORY
        ).read_text(encoding="utf-8")
        self.assertEqual(
            [],
            check_repository.assessment_catalog_contract_errors(
                catalog,
                inventory,
            ),
        )
        changed = catalog.replace("| `V01` |", "| `V99` |", 1)
        self.assertTrue(
            check_repository.assessment_catalog_contract_errors(changed, inventory)
        )
        changed_expectation = catalog.replace(
            "| Pass. | `satisfied` / `conformant`. |",
            "| Reject. | `violated` / `nonconformant`. |",
            1,
        )
        self.assertTrue(
            any(
                "literal copies" in error
                for error in check_repository.assessment_catalog_contract_errors(
                    changed_expectation,
                    inventory,
                )
            )
        )

    def test_schema_is_the_closed_s2_baseline(self) -> None:
        schema_path = (
            check_repository.ROOT
            / "schema"
            / "v0.1"
            / "geesno-semantic.schema.json"
        )
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        self.assertEqual(
            schema["$schema"],
            "https://json-schema.org/draft/2020-12/schema",
        )
        self.assertEqual(schema["x-geesno-status"], "s2-complete")
        self.assertNotIn("$id", schema)
        self.assertNotEqual(schema.get("not"), {})
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(set(schema["required"]), {"spec_version", "id", "scope"})
        self.assertEqual(schema["properties"]["spec_version"]["const"], "0.1.0")
        self.assertGreaterEqual(len(schema["$defs"]), 40)
        for definition in (
            "identifier",
            "qualifiedTerm",
            "reference",
            "value",
            "entity",
            "assertion",
            "source",
            "binding",
            "revision",
            "tombstone",
            "change",
            "history",
        ):
            self.assertIn(definition, schema["$defs"])

    def test_all_architecture_adrs_are_accepted(self) -> None:
        for relative in check_repository.ACCEPTED_ARCHITECTURE_ADRS:
            text = (check_repository.ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("- **Status:** Accepted", text, relative)

        processing = (
            check_repository.ROOT
            / "adr"
            / "0016-json-processing-canonicalization.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "- **Accepted by:** Explicit human architecture decision on 2026-09-04",
            processing,
        )
        for marker in check_repository.PROCESSING_ACCEPTANCE_MARKERS:
            self.assertIn(marker, processing)

        vocabulary_identity = (
            check_repository.ROOT
            / "adr"
            / "0017-vocabulary-identity-version-model.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "- **Accepted by:** Explicit human architecture decision on 2026-09-10",
            vocabulary_identity,
        )
        for marker in check_repository.ACCEPTED_VOCABULARY_IDENTITY_MARKERS:
            self.assertIn(marker, vocabulary_identity)

    def test_foundational_background_matches_public_digest(self) -> None:
        digest = hashlib.sha256(
            (check_repository.ROOT / "PROJECT_FOUNDATION.md").read_bytes()
        ).hexdigest()
        self.assertEqual(digest, check_repository.FOUNDATION_SHA256)

    def test_fixtures_are_nonempty_and_exactly_paired(self) -> None:
        valid = sorted((check_repository.ROOT / "conformance" / "valid").glob("*.json"))
        invalid = sorted(
            path
            for path in (check_repository.ROOT / "conformance" / "invalid").iterdir()
            if path.is_file() and path.suffix in {".json", ".raw"}
        )
        expected = sorted(
            (check_repository.ROOT / "conformance" / "expected").glob("*.json")
        )
        self.assertGreater(len(valid), 0)
        self.assertGreater(len(invalid), 0)
        self.assertEqual(
            {path.stem for path in valid + invalid},
            {path.stem for path in expected},
        )

    def test_scope_boundaries_remain_intact(self) -> None:
        self.assertFalse((check_repository.ROOT / "adapters").exists())
        self.assertFalse((check_repository.ROOT / "SCC-CAD-Adapter-1.0.zip").exists())
        sdk_files = {
            path.relative_to(check_repository.ROOT).as_posix()
            for path in (check_repository.ROOT / "sdk").rglob("*")
            if path.is_file() and "__pycache__" not in path.parts
        }
        self.assertEqual(
            sdk_files,
            set(check_repository.SDK_I1_REQUIRED_FILES)
            | set(check_repository.SDK_I2_REQUIRED_FILES)
            | set(check_repository.SDK_I3_REQUIRED_FILES)
            | set(check_repository.SDK_I4_REQUIRED_FILES)
            | set(check_repository.SDK_I5_REQUIRED_FILES)
            | set(check_repository.SDK_I6_REQUIRED_FILES)
            | set(check_repository.SDK_I7_REQUIRED_FILES)
            | set(check_repository.SDK_I8_REQUIRED_FILES),
        )

        vocabulary_artifacts = [
            path
            for path in (check_repository.ROOT / "vocab").rglob("*")
            if path.is_file() and path.name != "README.md"
        ]
        self.assertEqual(vocabulary_artifacts, [])

        profile_artifacts = [
            path
            for path in (check_repository.ROOT / "profiles").rglob("*")
            if path.is_file() and path.name != "README.md"
        ]
        expected_profile_artifacts = {
            check_repository.AI_CONTEXT_SCHEMA,
            check_repository.AI_CONTEXT_ASSESSMENT_SCHEMA,
            check_repository.AI_CONTEXT_PROFILE,
            *(
                f"{check_repository.AI_CONTEXT_CORPUS}/valid/{name}"
                for name in ai_context_acceptance.VALID_FIXTURES
            ),
            *(
                f"{check_repository.AI_CONTEXT_CORPUS}/invalid/{name}"
                for name in (
                    ai_context_acceptance.STRUCTURAL_INVALID_FIXTURES
                    + ai_context_acceptance.SEMANTIC_INVALID_FIXTURES
                )
            ),
            f"{check_repository.AI_CONTEXT_CORPUS}/sources/source-context.json",
            *(
                f"{check_repository.AI_CONTEXT_ASSESSMENT_CORPUS}/valid/{name}"
                for name in ai_context_assessment_corpus.VALID_FIXTURES
            ),
            *(
                f"{check_repository.AI_CONTEXT_ASSESSMENT_CORPUS}/invalid/{name}"
                for name in (
                    ai_context_assessment_corpus.LAYER_A_INVALID_FIXTURES
                    + ai_context_assessment_corpus.TEMPORAL_INVALID_FIXTURES
                    + ai_context_assessment_corpus.LAYER_B_INVALID_FIXTURES
                )
            ),
        }
        self.assertEqual(
            {path.relative_to(check_repository.ROOT).as_posix() for path in profile_artifacts},
            expected_profile_artifacts,
        )

    def test_public_artifact_digest_mutation_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "artifact.json").write_text("{}\n", encoding="utf-8")
            expected = hashlib.sha256((root / "artifact.json").read_bytes()).hexdigest()
            self.assertEqual([], check_repository.artifact_digest_errors(
                root, {"artifact.json": expected}))
            (root / "artifact.json").write_text("[]\n", encoding="utf-8")
            self.assertTrue(check_repository.artifact_digest_errors(
                root, {"artifact.json": expected}))

    def test_missing_public_artifact_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            self.assertTrue(check_repository.artifact_digest_errors(
                Path(directory), {"missing.json": "0" * 64}))

    def test_distribution_checks_do_not_require_git(self) -> None:
        self.assertNotIn("subprocess", check_repository.__dict__)
        self.assertEqual([], check_repository.check_repository())


if __name__ == "__main__":
    unittest.main()
