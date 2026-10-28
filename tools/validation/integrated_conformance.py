"""Deterministic offline orchestration of repository conformance checks.

This module is reference repository tooling. It composes existing validators;
it is not a semantic authority, public API, or normative artifact producer.
"""

from __future__ import annotations

import io
import socket
import sys
import unittest
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterator, Sequence
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
VALIDATION = ROOT / "tools" / "validation"
S2_RUNNER = ROOT / "conformance" / "runner"
BENCHMARK = ROOT / "tools" / "benchmark"
TESTS = VALIDATION / "tests"
for path in (VALIDATION, S2_RUNNER, BENCHMARK):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import ai_context_acceptance as s4_acceptance  # noqa: E402
import ai_context_assessment_corpus as s5_corpus  # noqa: E402
import ai_context_s4_exit as s4_benchmark  # noqa: E402
import check_repository  # noqa: E402
import integration_boundaries  # noqa: E402
from fixture_runner import run_suite as run_s2_suite  # noqa: E402


class IntegratedCheckError(RuntimeError):
    """Raised when one integrated component reports a conformance failure."""


@dataclass(frozen=True)
class Component:
    name: str
    run: Callable[[], str]


@dataclass(frozen=True)
class ComponentResult:
    name: str
    passed: bool
    summary: str


@dataclass(frozen=True)
class IntegratedRun:
    results: tuple[ComponentResult, ...]

    @property
    def passed(self) -> bool:
        return all(result.passed for result in self.results)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise IntegratedCheckError(message)


def _repository_guard() -> str:
    errors = check_repository.check_repository()
    _require(not errors, "; ".join(errors))
    return "repository structure, documentation, scope and frozen baselines"


def _s2_core() -> str:
    valid, invalid, expected, errors = run_s2_suite()
    _require(not errors, "; ".join(errors))
    return f"{valid} valid, {invalid} invalid, {expected} expected fixtures"


def _integration_boundaries() -> str:
    run = integration_boundaries.run_checks()
    failed = [result for result in run.results if not result.passed]
    _require(
        not failed,
        "; ".join(f"{result.name}: {result.detail}" for result in failed),
    )
    return f"{len(run.results)} Core/Profile/Extension/version checks"


def _s4_acceptance() -> str:
    run = s4_acceptance.run_corpus()
    _require(not run.errors, "; ".join(run.errors))
    return (
        f"{run.valid_passed} valid, "
        f"{run.structural_invalid_rejected} structural invalid, "
        f"{run.semantic_invalid_rejected} semantic invalid"
    )


def _s4_frozen_benchmark() -> str:
    run = s4_benchmark.build_benchmark_run()
    mismatches = s4_benchmark.expected_mismatches(run)
    _require(not mismatches, "; ".join(mismatches))
    return "frozen source, Projections, metrics and report reproduced"


def _s5_result_corpus() -> str:
    run = s5_corpus.run_corpus()
    _require(not run.errors, "; ".join(run.errors))
    return (
        f"{run.valid_passed} valid, {run.layer_a_rejected} Layer A invalid, "
        f"{run.temporal_rejected} temporal invalid, "
        f"{run.layer_b_rejected} Layer B invalid"
    )


def _focused_unit_tests(pattern: str) -> str:
    suite = unittest.TestLoader().discover(str(TESTS), pattern=pattern)
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=0).run(suite)
    if not result.wasSuccessful():
        details = stream.getvalue().strip().replace("\n", " | ")
        raise IntegratedCheckError(details)
    return f"{result.testsRun} focused tests"


def _i5_assessment() -> str:
    return _focused_unit_tests("test_ai_context_requirement_assessment.py")


def _i6_result_construction() -> str:
    return _focused_unit_tests("test_ai_context_result_construction.py")


DEFAULT_COMPONENTS = (
    Component("repository-guard", _repository_guard),
    Component("s2-core-conformance", _s2_core),
    Component("core-profile-extension-version", _integration_boundaries),
    Component("s4-profile-acceptance", _s4_acceptance),
    Component("s4-frozen-benchmark", _s4_frozen_benchmark),
    Component("s5-assessment-result-corpus", _s5_result_corpus),
    Component("s5-i5-requirement-assessment", _i5_assessment),
    Component("s5-i6-result-construction", _i6_result_construction),
)


def _network_disabled(*_args: object, **_kwargs: object) -> None:
    raise IntegratedCheckError("network access is disabled for integrated conformance")


@contextmanager
def offline_network_guard() -> Iterator[None]:
    """Reject socket creation and name resolution while the suite runs."""

    with (
        patch.object(socket, "socket", side_effect=_network_disabled),
        patch.object(socket, "create_connection", side_effect=_network_disabled),
        patch.object(socket, "getaddrinfo", side_effect=_network_disabled),
        patch.object(socket, "gethostbyname", side_effect=_network_disabled),
        patch.object(socket, "gethostbyname_ex", side_effect=_network_disabled),
        patch.object(socket, "gethostbyaddr", side_effect=_network_disabled),
        patch.object(socket, "getnameinfo", side_effect=_network_disabled),
        patch.object(socket, "getfqdn", side_effect=_network_disabled),
    ):
        yield


def run_integrated_suite(
    components: Sequence[Component] = DEFAULT_COMPONENTS,
) -> IntegratedRun:
    """Run every required component offline and preserve all component results."""

    results: list[ComponentResult] = []
    with offline_network_guard():
        for component in components:
            try:
                summary = component.run()
            except Exception as error:  # component failures must not hide later checks
                summary = f"{type(error).__name__}: {error}"
                results.append(ComponentResult(component.name, False, summary))
            else:
                results.append(ComponentResult(component.name, True, summary))
    return IntegratedRun(results=tuple(results))
