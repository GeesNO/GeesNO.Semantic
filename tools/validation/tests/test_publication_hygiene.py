from __future__ import annotations

import contextlib
import hashlib
import io
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.validation import check_repository, publication_hygiene

ROOT = check_repository.ROOT


class PublicationHygieneTests(unittest.TestCase):

    def test_current_tracked_tree_passes_redacted_hygiene_audit(self) -> None:
            report = publication_hygiene.audit_current_tree()
            self.assertEqual(set(report.tracked_paths), set(check_repository.REQUIRED_FILES))
            self.assertEqual((), report.errors)
            self.assertEqual((), report.machine_local_files)
            self.assertEqual((), report.secret_candidate_files)

    def test_portable_path_and_repository_mechanics_are_clean(self) -> None:
            report = publication_hygiene.audit_current_tree()
            self.assertEqual((), report.case_collisions)
            self.assertEqual((), report.unsafe_paths)
            self.assertEqual((), report.junk_paths)
            self.assertEqual((), report.symlink_paths)
            self.assertEqual((), report.submodule_paths)
            self.assertFalse(report.lfs_required)

    def test_only_the_exact_raw_conformance_fixtures_are_binary_evidence(self) -> None:
            report = publication_hygiene.audit_current_tree()
            self.assertEqual(
                publication_hygiene.RAW_FIXTURES,
                frozenset(report.raw_fixture_paths),
            )
            self.assertEqual((), report.unexpected_binary_or_archive_paths)

    def test_reference_dependencies_are_declared_without_packaging_semantics(self) -> None:
            requirements = {
                line.strip()
                for line in (ROOT / "requirements-conformance.txt")
                .read_text(encoding="utf-8")
                .splitlines()
                if line.strip() and not line.startswith("#")
            }
            self.assertEqual(
                {"jsonschema==4.26.0", "rfc3987-syntax2==1.3.2"},
                requirements,
            )
            self.assertFalse((ROOT / "pyproject.toml").exists())
            self.assertFalse((ROOT / "setup.py").exists())

    def test_dco_is_linked_not_vendored_and_examples_remain_synthetic(self) -> None:
            contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
            examples = (
                ROOT / "examples/cross-domain/public-preview/README.md"
            ).read_text(encoding="utf-8")
            self.assertIn("https://developercertificate.org/", contributing)
            self.assertFalse(any(ROOT.glob("DCO*")))
            self.assertIn("project-authored, synthetic and fictional", examples)
            self.assertIn("no customer, project or third-party", examples)
            example_urls: list[str] = []
            for path in (ROOT / "examples/cross-domain/public-preview").rglob("*.json"):
                example_urls.extend(
                    re.findall(r"https?://[^\"\s]+", path.read_text(encoding="utf-8"))
                )
            self.assertTrue(example_urls)
            self.assertTrue(
                all(url.startswith("https://example.invalid/") for url in example_urls)
            )

    def test_frozen_public_artifacts_are_unchanged(self) -> None:
            expected_hashes = {
                "PROJECT_FOUNDATION.md": check_repository.FOUNDATION_SHA256,
                "schema/v0.1/geesno-semantic.schema.json": "aeac3413ac1ea70060994dee4e6fa1858ea48e16691e08f56932a5d06cef4002",
                "profiles/ai-context/v0.1/profile.json": "63ea4aadc65ad042eddf376b48761b2549f1e3ea76fd84c1a075753d55f6a90b",
                "profiles/ai-context/schema/v0.1/ai-context.schema.json": "9522cd77d7db90abc94e855f534b5559617709dc7a3d98ce09ee73e269ab1129",
                "benchmarks/ai-context/v0.1/expected-report.json": "948df7918465676640d898dae568b7845e9722f0a999f97479e977e62730e331",
                "profiles/ai-context/schema/v0.1/ai-context-assessment.schema.json": "aec4f4e42267e8486b3420e0590f976aac1a3a07c61c2ba8d7a5776e57c5346a",
            }
            for relative, expected in expected_hashes.items():
                with self.subTest(relative=relative):
                    self.assertEqual(
                        expected,
                        hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(),
                    )


class PublicHygieneRegressionTests(unittest.TestCase):
    def report_for(self, content: bytes, filename: str = "sample.txt"):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".gitattributes").write_text("* text=auto eol=lf\n", encoding="utf-8")
            (root / filename).write_bytes(content)
            with patch.object(publication_hygiene, "ROOT", root):
                return publication_hygiene.audit_current_tree()

    def test_clean_public_text_has_no_private_candidates(self):
        report = self.report_for(b"Public technical description.\n")
        self.assertEqual((), report.secret_candidate_files)
        self.assertEqual((), report.machine_local_files)

    def test_multiple_public_contributor_attributions_are_not_secrets(self):
        report = self.report_for(b"Fictional One and Fictional Two contributed.\n")
        self.assertEqual((), report.secret_candidate_files)

    def test_private_key_is_detected_without_recording_value(self):
        value = b"-----BEGIN " + b"PRIVATE KEY-----"
        report = self.report_for(value)
        self.assertEqual(("sample.txt",), report.secret_candidate_files)
        self.assertNotIn(value.decode(), repr(report))

    def test_token_is_detected_without_recording_value(self):
        value = b"gh" + b"p_" + b"A" * 30
        report = self.report_for(value)
        self.assertEqual(("sample.txt",), report.secret_candidate_files)
        self.assertNotIn(value.decode(), repr(report))

    def test_local_path_is_detected_without_recording_value(self):
        value = "C:" + "/Us" + "ers/fictional/private/document.txt"
        report = self.report_for(value.encode())
        self.assertEqual(("sample.txt",), report.machine_local_files)
        self.assertNotIn(value, repr(report))

    def test_diagnostics_do_not_print_sensitive_content(self):
        value = "gh" + "p_" + "B" * 30
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".gitattributes").write_text("* text=auto eol=lf\n", encoding="utf-8")
            (root / "sample.txt").write_text(value, encoding="utf-8")
            output = io.StringIO()
            with patch.object(publication_hygiene, "ROOT", root), contextlib.redirect_stdout(output):
                result = publication_hygiene.main()
            self.assertEqual(1, result)
            self.assertNotIn(value, output.getvalue())
            self.assertIn("Sensitive candidate values are intentionally redacted", output.getvalue())

    def test_unexpected_binary_is_rejected(self):
        report = self.report_for(b"binary", "sample.zip")
        self.assertEqual(("sample.zip",), report.unexpected_binary_or_archive_paths)

    def test_generated_file_is_rejected(self):
        report = self.report_for(b"temporary", "sample.bak")
        self.assertEqual(("sample.bak",), report.junk_paths)

    def test_no_git_executable_is_needed(self):
        self.assertNotIn("subprocess", publication_hygiene.__dict__)
        report = self.report_for(b"Offline public material.\n")
        self.assertIn("sample.txt", report.tracked_paths)


if __name__ == "__main__":
    unittest.main()
