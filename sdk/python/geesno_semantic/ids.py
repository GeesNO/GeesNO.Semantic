"""Explicit semantic-ID conveniences for SDK callers."""

from __future__ import annotations

from uuid import uuid4


def new_uuid_urn() -> str:
    """Return a canonical lowercase UUID URN when explicitly requested."""

    return f"urn:uuid:{uuid4()}"


__all__ = ["new_uuid_urn"]
