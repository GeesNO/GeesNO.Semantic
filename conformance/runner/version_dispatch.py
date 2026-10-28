"""Layer 1: exact S2 contract dispatch."""

from __future__ import annotations

import re
from typing import Any


SEMVER = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-((?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)"
    r"(?:\.(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*))*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
)
SUPPORTED_VERSION = "0.1.0"


class VersionError(ValueError):
    def __init__(self, category: str, message: str) -> None:
        super().__init__(message)
        self.category = category


class UnsupportedVersion(ValueError):
    def __init__(self, version: str) -> None:
        super().__init__(f"unsupported specification version {version!r}")
        self.version = version
        self.category = "unsupported-version"


def dispatch(document: dict[str, Any]) -> str:
    if "spec_version" not in document:
        raise VersionError("missing-version", "spec_version is required")
    version = document["spec_version"]
    if not isinstance(version, str):
        raise VersionError("version-type", "spec_version must be a string")
    if not SEMVER.fullmatch(version):
        raise VersionError("version-syntax", "spec_version must be canonical SemVer 2.0.0")
    if version != SUPPORTED_VERSION:
        raise UnsupportedVersion(version)
    return version
