"""Explicit construction of the accepted S2 reference representation."""

from __future__ import annotations


def reference(*, target: str, location: str) -> dict[str, str]:
    """Return a closed S2 reference without resolving or locating its target."""

    if not isinstance(target, str):
        raise TypeError("target must be a string")
    if not isinstance(location, str):
        raise TypeError("location must be a string")
    return {"target": target, "location": location}


__all__ = ["reference"]
