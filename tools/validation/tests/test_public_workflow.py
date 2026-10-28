from __future__ import annotations

import hashlib
import re
import unittest
from pathlib import Path

from tools.validation import check_repository


ROOT = check_repository.ROOT
LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


class PublicWorkflowTests(unittest.TestCase):
    def test_policies_are_discoverable_and_release_remains_open(self) -> None:
        for relative in ("README.md", "docs/README.md", "PUBLIC_PREVIEW.md"):
            text = (ROOT / relative).read_text(encoding="utf-8")
            with self.subTest(relative=relative):
                self.assertIn("CONTRIBUTING.md", text)
                self.assertIn("SECURITY.md", text)
                self.assertNotIn("S7 Complete", text)
        preview = (ROOT / check_repository.PUBLIC_PREVIEW).read_text(encoding="utf-8")
        notes = (ROOT / check_repository.RELEASE_NOTES).read_text(encoding="utf-8")
        self.assertIn("0.1.0-preview.1", preview)
        self.assertIn("does not itself publish a release", preview)
        self.assertIn("The preview has not yet been released", notes)
        self.assertEqual(
            [],
            check_repository.public_document_contract_errors(
                check_repository.PUBLIC_PREVIEW,
                preview,
            ),
        )
        self.assertEqual(
            [],
            check_repository.public_document_contract_errors(
                check_repository.RELEASE_NOTES,
                notes,
            ),
        )
        contributing = (ROOT / check_repository.CONTRIBUTING_POLICY).read_text(
            encoding="utf-8"
        )
        self.assertIn("Public contribution endpoint: not established by this distribution", contributing)

    def test_contribution_policy_has_target_license_dco_and_no_cla(self) -> None:
        text = (ROOT / check_repository.CONTRIBUTING_POLICY).read_text(
            encoding="utf-8"
        )
        for marker in check_repository.CONTRIBUTING_POLICY_MARKERS:
            self.assertIn(marker, text)
        self.assertIn("https://developercertificate.org/", text)
        self.assertIn("Contributors retain copyright", text)
        self.assertIn("does not adopt a\nCLA", text)
        self.assertFalse(any(ROOT.glob("DCO*")))
        for invented_entity in (
            "GeesNO Foundation",
            "GeesNO Inc.",
            "GeesNO Association",
        ):
            self.assertNotIn(invented_entity, text)

    def test_security_policy_preserves_pending_private_channel_boundary(self) -> None:
        text = (ROOT / check_repository.SECURITY_POLICY).read_text(encoding="utf-8")
        self.assertEqual(
            [],
            check_repository.public_document_contract_errors(
                check_repository.SECURITY_POLICY,
                text,
            ),
        )
        self.assertNotRegex(text, r"[A-Za-z0-9._%+-]+@geesno\.com")
        self.assertNotIn("Private reporting channel active: yes", text)
        self.assertIn(
            "A private vulnerability-reporting route is not verified by this source distribution",
            text,
        )
        self.assertNotRegex(text, r"\b(?:24 hours|7 days|30 days)\b")
        self.assertIn("syntactic validity\n!= semantic truth", text)
        self.assertIn("semantic data\n!= executable instruction", text)

    def test_issue_template_inventory_is_exact_and_not_security_public(self) -> None:
        expected = {Path(relative).name for relative in check_repository.ISSUE_TEMPLATES}
        directory = ROOT / ".github" / "ISSUE_TEMPLATE"
        actual = {path.name for path in directory.iterdir() if path.is_file()}
        self.assertEqual(expected, actual)
        self.assertFalse(
            any(
                token in name.casefold()
                for name in actual
                for token in ("security", "vulnerab")
            )
        )
        for relative in check_repository.ISSUE_TEMPLATES:
            text = (ROOT / relative).read_text(encoding="utf-8")
            front_matter = text.split("---", 2)[1]
            with self.subTest(relative=relative):
                self.assertTrue(text.startswith("---\n"))
                for key in ("name:", "about:", "title:", "labels:", "assignees:"):
                    self.assertIn(key, front_matter)
                self.assertIn("[SECURITY.md](../../SECURITY.md)", text)
                self.assertIsNone(check_repository.LOCAL_ABSOLUTE_PATH.search(text))

    def test_templates_cover_four_routes_and_pull_request_boundary(self) -> None:
        expected_markers = {
            "documentation.md": "## Normative impact",
            "tooling-bug.md": "SDK or tool bug is not automatically a specification bug",
            "conformance-discrepancy.md": "reference runner does not automatically override",
            "specification-proposal.md": "## Cross-domain implications",
        }
        for name, marker in expected_markers.items():
            text = (ROOT / ".github" / "ISSUE_TEMPLATE" / name).read_text(
                encoding="utf-8"
            )
            with self.subTest(name=name):
                self.assertIn(marker, text)
        pull_request = (ROOT / check_repository.PULL_REQUEST_TEMPLATE).read_text(
            encoding="utf-8"
        )
        for marker in (
            "Normative impact",
            "DCO 1.1 `Signed-off-by`",
            "submission != acceptance",
            "merged code != certification",
        ):
            self.assertIn(marker, pull_request)

    def test_policy_relative_links_resolve(self) -> None:
        files = (
            check_repository.CONTRIBUTING_POLICY,
            check_repository.SECURITY_POLICY,
            check_repository.PULL_REQUEST_TEMPLATE,
            *check_repository.ISSUE_TEMPLATES,
        )
        for relative in files:
            path = ROOT / relative
            text = path.read_text(encoding="utf-8")
            for target in LINK.findall(text):
                if "://" in target or target.startswith("#"):
                    continue
                target_path = (path.parent / target.split("#", 1)[0]).resolve()
                with self.subTest(relative=relative, target=target):
                    self.assertTrue(target_path.exists())
                    self.assertTrue(target_path.is_relative_to(ROOT))

    def test_normative_frozen_artifacts_are_unchanged(self) -> None:
        expected = {
            "PROJECT_FOUNDATION.md": check_repository.FOUNDATION_SHA256,
            "schema/v0.1/geesno-semantic.schema.json": "aeac3413ac1ea70060994dee4e6fa1858ea48e16691e08f56932a5d06cef4002",
            "profiles/ai-context/v0.1/profile.json": "63ea4aadc65ad042eddf376b48761b2549f1e3ea76fd84c1a075753d55f6a90b",
            "profiles/ai-context/schema/v0.1/ai-context.schema.json": "9522cd77d7db90abc94e855f534b5559617709dc7a3d98ce09ee73e269ab1129",
            "benchmarks/ai-context/v0.1/expected-report.json": "948df7918465676640d898dae568b7845e9722f0a999f97479e977e62730e331",
            "profiles/ai-context/schema/v0.1/ai-context-assessment.schema.json": "aec4f4e42267e8486b3420e0590f976aac1a3a07c61c2ba8d7a5776e57c5346a",
        }
        for relative, digest in expected.items():
            with self.subTest(relative=relative):
                self.assertEqual(
                    digest,
                    hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(),
                )


if __name__ == "__main__":
    unittest.main()
