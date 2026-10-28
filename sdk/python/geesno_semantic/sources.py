"""Non-copying views over accepted S2 Source and Binding records."""

from __future__ import annotations

from typing import Any

from .trust import _LifecycleHostView


class _IdentifiedRecordView(_LifecycleHostView):
    __slots__ = ()

    @property
    def identifier(self) -> str:
        """Return the record's explicit semantic ID."""

        return self._backing_record["id"]

class Source(_IdentifiedRecordView):
    """A live Source view with a read-only Mapping interface."""


class Binding(_IdentifiedRecordView):
    """A live Binding view with a read-only Mapping interface."""


__all__ = ["Binding", "Source"]
