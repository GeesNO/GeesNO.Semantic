"""Explicit loss-aware load and save operations."""

from __future__ import annotations

from pathlib import Path

from ._s2 import (
    ResourceLimits,
    dispatch,
    dump_preserving_numbers,
    parse_bytes,
    parse_path,
)
from .document import SemanticDocument


def load_bytes(
    data: bytes,
    *,
    limits: ResourceLimits | None = None,
) -> SemanticDocument:
    """Parse bytes and perform exact version dispatch without validating."""

    tree = parse_bytes(data, limits)
    dispatch(tree)
    return SemanticDocument(tree)


def load_text(
    text: str,
    *,
    limits: ResourceLimits | None = None,
) -> SemanticDocument:
    """Encode text as UTF-8, then apply the same load boundary as bytes."""

    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return load_bytes(text.encode("utf-8"), limits=limits)


def load_path(
    path: str | Path,
    *,
    limits: ResourceLimits | None = None,
) -> SemanticDocument:
    """Read a caller-selected path without modifying it, then load it."""

    tree = parse_path(Path(path), limits)
    dispatch(tree)
    return SemanticDocument(tree)


def dump_text(document: SemanticDocument) -> str:
    """Serialize the backing tree without validation or semantic repair."""

    if not isinstance(document, SemanticDocument):
        raise TypeError("document must be a SemanticDocument")
    return dump_preserving_numbers(document.backing_tree)


def dump_bytes(document: SemanticDocument) -> bytes:
    """Serialize to UTF-8 bytes using deterministic SDK formatting."""

    return dump_text(document).encode("utf-8")


def save_path(document: SemanticDocument, path: str | Path) -> Path:
    """Write only to the explicitly selected destination path."""

    destination = Path(path)
    destination.write_bytes(dump_bytes(document))
    return destination
