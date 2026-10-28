"""Internal imports from the approved repository-local S2 implementation."""

from conformance.runner.fixture_runner import validate_bytes as validate_s2_bytes
from conformance.runner.raw_parse import (
    RawInputError,
    RawNumber,
    ResourceLimits,
    ResourceRefusal,
    dump_preserving_numbers,
    parse_bytes,
    parse_path,
)
from conformance.runner.version_dispatch import (
    UnsupportedVersion,
    VersionError,
    dispatch,
)

__all__ = [
    "RawInputError",
    "RawNumber",
    "ResourceLimits",
    "ResourceRefusal",
    "UnsupportedVersion",
    "VersionError",
    "dispatch",
    "dump_preserving_numbers",
    "parse_bytes",
    "parse_path",
    "validate_s2_bytes",
]
