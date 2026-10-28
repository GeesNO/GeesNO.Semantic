"""Facade over the approved S2 Layers 0-3 validation result."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ._s2 import validate_s2_bytes
from .document import SemanticDocument
from .io import dump_bytes


def validate_bytes(data: bytes) -> dict[str, Any]:
    """Return the existing S2 result/layer/category mapping unchanged."""

    return validate_s2_bytes(data)


def validate_path(path: str | Path) -> dict[str, Any]:
    """Validate a path without modifying its bytes."""

    return validate_bytes(Path(path).read_bytes())


def validate_document(document: SemanticDocument) -> dict[str, Any]:
    """Serialize the backing tree and explicitly run S2 Layers 0-3."""

    return validate_bytes(dump_bytes(document))
