from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
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
from conformance.runner.raw_parse import RawNumber  # noqa: E402
from conformance.runner.schema_validation import load_schema  # noqa: E402
from geesno_semantic import (  # noqa: E402
    RawInputError,
    ResourceLimits,
    ResourceRefusal,
    UnsupportedVersion,
    dump_bytes,
    dump_text,
    load_bytes,
    load_path,
    save_path,
    validate_bytes,
    validate_document,
    validate_path,
)


class SdkIoValidationTests(unittest.TestCase):
    def test_every_s2_fixture_matches_the_existing_validation_facade(self) -> None:
        schema = load_schema(SCHEMA_PATH)
        valid = fixture_files(CONFORMANCE / "valid")
        invalid = fixture_files(CONFORMANCE / "invalid")
        expected = sorted((CONFORMANCE / "expected").glob("*.json"))

        self.assertEqual((len(valid), len(invalid), len(expected)), (17, 84, 101))
        for fixture in valid + invalid:
            with self.subTest(fixture=fixture.name):
                data = fixture.read_bytes()
                approved = validate_s2_bytes(data, schema)
                sdk_result = validate_bytes(data)
                recorded = json.loads(
                    (CONFORMANCE / "expected" / f"{fixture.stem}.json").read_text(
                        encoding="utf-8"
                    )
                )
                self.assertEqual(sdk_result, approved)
                self.assertEqual(sdk_result, recorded)

    def test_unsupported_version_is_not_upgraded_or_substituted(self) -> None:
        fixture = CONFORMANCE / "invalid" / "version-future.json"
        self.assertEqual(
            validate_bytes(fixture.read_bytes()),
            {
                "result": "unsupported-version",
                "layer": 1,
                "category": "unsupported-version",
            },
        )
        with self.assertRaises(UnsupportedVersion) as raised:
            load_path(fixture)
        self.assertEqual(raised.exception.version, "0.2.0")

    def test_load_is_not_a_conformance_claim(self) -> None:
        fixture = CONFORMANCE / "invalid" / "schema-unknown-root.json"
        document = load_path(fixture)
        self.assertEqual(document.spec_version, "0.1.0")
        self.assertEqual(validate_document(document)["layer"], 2)

    def test_representative_valid_documents_round_trip(self) -> None:
        fixture_names = (
            "minimal-document.json",
            "assertions-and-values.json",
            "sources-and-bindings.json",
            "unknown-extension-numbers.json",
        )
        for fixture_name in fixture_names:
            with self.subTest(fixture=fixture_name), tempfile.TemporaryDirectory() as temp:
                source = CONFORMANCE / "valid" / fixture_name
                original = load_path(source)
                destination = Path(temp) / fixture_name
                save_path(original, destination)
                reloaded = load_path(destination)

                self.assertEqual(reloaded.backing_tree, original.backing_tree)
                self.assertEqual(reloaded["id"], original["id"])
                self.assertEqual(validate_path(destination), {"result": "valid"})

    def test_unknown_extension_preserves_nested_payload_and_number_tokens(self) -> None:
        source = CONFORMANCE / "valid" / "unknown-extension-numbers.json"
        document = load_path(source)
        payload = document["extensions"]["ext:opaque"]
        numbers = payload["numbers"]

        self.assertEqual(
            [number.token for number in numbers],
            ["1", "1.0", "1e0", "1E+0", "-0", "9007199254740993", "1e100000"],
        )
        self.assertTrue(all(isinstance(number, RawNumber) for number in numbers))
        self.assertEqual(payload["nested"], {"array": []})
        self.assertIn(
            '"numbers":[1,1.0,1e0,1E+0,-0,9007199254740993,1e100000]',
            dump_text(document),
        )

        reloaded = load_bytes(dump_bytes(document))
        reloaded_numbers = reloaded["extensions"]["ext:opaque"]["numbers"]
        self.assertEqual([number.token for number in reloaded_numbers], [number.token for number in numbers])
        self.assertNotIn("opaque", reloaded.backing_tree)

    def test_load_validate_and_save_elsewhere_do_not_mutate_source(self) -> None:
        source = CONFORMANCE / "valid" / "unknown-extension-numbers.json"
        before = source.read_bytes()
        before_sha = hashlib.sha256(before).hexdigest()

        document = load_path(source)
        self.assertEqual(validate_path(source), {"result": "valid"})
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "saved.json"
            save_path(document, destination)
            self.assertTrue(destination.is_file())

        after = source.read_bytes()
        self.assertEqual(after, before)
        self.assertEqual(hashlib.sha256(after).hexdigest(), before_sha)

    def test_duplicate_member_remains_a_layer_zero_rejection(self) -> None:
        fixture = CONFORMANCE / "invalid" / "raw-duplicate-extension-payload.raw"
        data = fixture.read_bytes()
        self.assertEqual(validate_bytes(data), validate_s2_bytes(data))
        self.assertEqual(
            validate_bytes(data),
            {"result": "invalid", "layer": 0, "category": "duplicate-member"},
        )
        with self.assertRaises(RawInputError) as raised:
            load_bytes(data)
        self.assertEqual(raised.exception.category, "duplicate-member")

    def test_resource_limits_are_load_safety_controls(self) -> None:
        data = (CONFORMANCE / "valid" / "minimal-document.json").read_bytes()
        with self.assertRaises(ResourceRefusal) as raised:
            load_bytes(data, limits=ResourceLimits(max_bytes=len(data) - 1))
        self.assertEqual(raised.exception.category, "byte-limit")
        self.assertEqual(validate_bytes(data), {"result": "valid"})

    def test_i1_operations_remain_offline(self) -> None:
        data = (CONFORMANCE / "valid" / "minimal-document.json").read_bytes()
        with mock.patch("socket.socket", side_effect=AssertionError("network used")):
            document = load_bytes(data)
            self.assertEqual(validate_document(document), {"result": "valid"})
            self.assertTrue(dump_bytes(document))

    def test_existing_runner_remains_independent_of_the_sdk(self) -> None:
        for path in (ROOT / "conformance" / "runner").glob("*.py"):
            self.assertNotIn("geesno_semantic", path.read_text(encoding="utf-8"))

        environment = os.environ.copy()
        environment.pop("PYTHONPATH", None)
        completed = subprocess.run(
            [sys.executable, "conformance/runner/run.py"],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("17 valid, 84 invalid, 101 expected fixtures", completed.stdout)


if __name__ == "__main__":
    unittest.main()
