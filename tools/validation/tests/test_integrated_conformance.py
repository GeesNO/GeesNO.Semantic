from __future__ import annotations

import hashlib
import io
import os
import socket
import subprocess
import sys
import unittest
from contextlib import redirect_stderr
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
VALIDATION = ROOT / "tools" / "validation"
if str(VALIDATION) not in sys.path:
    sys.path.insert(0, str(VALIDATION))

import integrated_conformance as integrated  # noqa: E402
import integration_boundaries  # noqa: E402
import reference_cli  # noqa: E402


ARTIFACT_ROOTS = (
    ROOT / "schema",
    ROOT / "conformance",
    ROOT / "profiles",
    ROOT / "benchmarks",
)
ARTIFACT_SUFFIXES = {".json", ".raw", ".md"}


def artifact_digest() -> str:
    digest = hashlib.sha256()
    for root in ARTIFACT_ROOTS:
        for path in sorted(
            item
            for item in root.rglob("*")
            if item.is_file() and item.suffix in ARTIFACT_SUFFIXES
        ):
            digest.update(path.relative_to(ROOT).as_posix().encode("utf-8"))
            digest.update(b"\0")
            digest.update(path.read_bytes())
            digest.update(b"\0")
    return digest.hexdigest()


class IntegratedConformanceTests(unittest.TestCase):
    @staticmethod
    def run_cli(*arguments: str) -> subprocess.CompletedProcess[str]:
        environment = dict(os.environ)
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [sys.executable, "tools/validation/reference_cli.py", *arguments],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
            timeout=600,
            check=False,
        )

    @classmethod
    def setUpClass(cls) -> None:
        before = artifact_digest()
        cls.integrated_run = integrated.run_integrated_suite()
        cls.cli = cls.run_cli("validate-repository")
        cls.after = artifact_digest()
        cls.before = before

    def test_integrated_runner_success_and_required_regressions(self) -> None:
        self.assertTrue(self.integrated_run.passed)
        self.assertEqual(
            (
                "repository-guard",
                "s2-core-conformance",
                "core-profile-extension-version",
                "s4-profile-acceptance",
                "s4-frozen-benchmark",
                "s5-assessment-result-corpus",
                "s5-i5-requirement-assessment",
                "s5-i6-result-construction",
            ),
            tuple(result.name for result in self.integrated_run.results),
        )

    def test_integrated_runner_propagates_component_failure(self) -> None:
        def fail() -> str:
            raise integrated.IntegratedCheckError("expected failure")

        run = integrated.run_integrated_suite(
            (
                integrated.Component("passing", lambda: "ok"),
                integrated.Component("failing", fail),
                integrated.Component("later", lambda: "still checked"),
            )
        )
        self.assertFalse(run.passed)
        self.assertEqual((True, False, True), tuple(item.passed for item in run.results))
        self.assertIn("expected failure", run.results[1].summary)

    def test_cli_runs_as_third_party_from_repository_root(self) -> None:
        self.assertEqual(0, self.cli.returncode, self.cli.stderr + self.cli.stdout)
        self.assertEqual(
            reference_cli.format_run(self.integrated_run), self.cli.stdout.strip()
        )

    def test_cli_returns_nonzero_for_conformance_failure(self) -> None:
        failed = integrated.IntegratedRun(
            (integrated.ComponentResult("fixture", False, "expected failure"),)
        )
        output = io.StringIO()
        status = reference_cli.main(
            ["validate-repository"], runner=lambda: failed, output=output
        )
        self.assertEqual(1, status)
        self.assertIn("Integrated conformance suite: FAIL", output.getvalue())

    def test_cli_returns_nonzero_for_invocation_error(self) -> None:
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as raised:
            reference_cli.main([])
        self.assertEqual(2, raised.exception.code)

    def test_cli_validates_external_semantic_documents_without_mutation(self) -> None:
        cases = (
            (ROOT / "conformance/valid/minimal-document.json", 0, "result-valid"),
            (
                ROOT / "conformance/invalid/schema-missing-document-id.json",
                1,
                "result=invalid",
            ),
            (
                ROOT / "conformance/invalid/version-future.json",
                1,
                "result=unsupported-version",
            ),
        )
        for path, expected_status, output_marker in cases:
            with self.subTest(path=path.name):
                before = path.read_bytes()
                result = self.run_cli("validate-document", str(path))
                self.assertEqual(
                    expected_status,
                    result.returncode,
                    result.stderr + result.stdout,
                )
                if output_marker == "result-valid":
                    self.assertIn("SemanticDocument VALID", result.stdout)
                else:
                    self.assertIn(output_marker, result.stdout)
                self.assertEqual(before, path.read_bytes())

    def test_cli_missing_document_path_is_configuration_error(self) -> None:
        missing = ROOT / "conformance" / "does-not-exist.json"
        result = self.run_cli("validate-document", str(missing))
        self.assertEqual(2, result.returncode)
        self.assertIn("ERROR: cannot read", result.stdout)

    def test_repeated_execution_is_deterministic(self) -> None:
        self.assertEqual(
            reference_cli.format_run(self.integrated_run), self.cli.stdout.strip()
        )

    def test_integrated_execution_does_not_mutate_artifacts(self) -> None:
        self.assertEqual(self.before, self.after)

    def test_network_attempt_is_blocked_and_reported(self) -> None:
        run = integrated.run_integrated_suite(
            (
                integrated.Component(
                    "network-attempt",
                    lambda: str(socket.create_connection(("example.invalid", 443))),
                ),
            )
        )
        self.assertFalse(run.passed)
        self.assertIn("network access is disabled", run.results[0].summary)

    def test_name_resolution_attempt_is_blocked_and_reported(self) -> None:
        run = integrated.run_integrated_suite(
            (
                integrated.Component(
                    "name-resolution-attempt",
                    lambda: socket.gethostbyname("example.invalid"),
                ),
            )
        )
        self.assertFalse(run.passed)
        self.assertIn("network access is disabled", run.results[0].summary)

    def test_i7_sources_have_no_network_model_or_runtime_dependency(self) -> None:
        source = "\n".join(
            (VALIDATION / name).read_text(encoding="utf-8").lower()
            for name in (
                "integration_boundaries.py",
                "integrated_conformance.py",
                "reference_cli.py",
            )
        )
        for forbidden in (
            "urllib.request",
            "http.client",
            "import requests",
            "import httpx",
            "import openai",
            "import anthropic",
            "import ollama",
            "import transformers",
            "import subprocess",
            "geesno.core",
        ):
            self.assertNotIn(forbidden, source)

    def test_core_profile_extension_and_exact_version_boundaries(self) -> None:
        run = integration_boundaries.run_checks()
        self.assertTrue(run.passed)
        self.assertEqual(
            {
                "core-bare-valid",
                "core-not-profile",
                "core-unknown-extension-inert",
                "s4-extension-preservation",
                "s2-exact-version-boundary",
                "s4-exact-binding-version",
                "s4-exact-profile-edition",
                "s5-exact-assessment-binding-version",
            },
            {result.name for result in run.results},
        )


if __name__ == "__main__":
    unittest.main()
