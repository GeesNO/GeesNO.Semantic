"""Non-copying views over accepted S2 Entity records."""

from __future__ import annotations

from typing import Any

from .trust import _LifecycleHostView


class _EntityView(_LifecycleHostView):
    __slots__ = ()

    kind_token: str

    def __init__(self, backing_record: dict[str, Any]) -> None:
        super().__init__(backing_record)
        if self._backing_record.get("kind") != self.kind_token:
            raise ValueError(
                f"{type(self).__name__} requires kind {self.kind_token!r}"
            )

    @property
    def identifier(self) -> str:
        """Return the record's explicit semantic ID."""

        return self._backing_record["id"]

    @property
    def kind(self) -> str:
        """Return the accepted fundamental Entity kind token."""

        return self._backing_record["kind"]

class Concept(_EntityView):
    """A live Concept view with a read-only Mapping interface."""

    kind_token = "concept"


class Representation(_EntityView):
    """A live Representation view with a read-only Mapping interface."""

    kind_token = "representation"


def entity_view(record: dict[str, Any]) -> Concept | Representation:
    """Create the matching typed view without changing the record."""

    if not isinstance(record, dict):
        raise TypeError("Entity records must be JSON objects")
    kind = record.get("kind")
    if kind == "concept":
        return Concept(record)
    if kind == "representation":
        return Representation(record)
    raise ValueError(f"unsupported Entity kind for an I2 view: {kind!r}")


__all__ = ["Concept", "Representation"]
