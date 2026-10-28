"""Thin views over the accepted descriptive S2 lifecycle records."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from typing import Any

from .trust import _LifecycleHostView, _TrustHostView


class _MappingView(Mapping[str, Any]):
    __slots__ = ("_backing_record",)

    def __init__(self, backing_record: dict[str, Any]) -> None:
        if not isinstance(backing_record, dict):
            raise TypeError("backing_record must be a JSON object")
        self._backing_record = backing_record

    @property
    def backing_record(self) -> dict[str, Any]:
        return self._backing_record

    def __getitem__(self, key: str) -> Any:
        return self._backing_record[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._backing_record)

    def __len__(self) -> int:
        return len(self._backing_record)


class Validity(_MappingView):
    """Live view over one qualified S2 Validity descriptor."""

    __slots__ = ()

    @property
    def kind(self) -> str:
        return self._backing_record["kind"]

    @property
    def from_value(self) -> Any | None:
        return self._backing_record.get("from")

    @property
    def until(self) -> Any | None:
        return self._backing_record.get("until")


class Revision(_TrustHostView):
    """Live view over one identified current or historical Revision."""

    __slots__ = ()

    @property
    def identifier(self) -> str:
        return self._backing_record["id"]

    @property
    def parents(self) -> tuple[dict[str, Any], ...]:
        references = self._backing_record.get("parents", [])
        if not isinstance(references, list):
            raise TypeError("parents must be a JSON array before creating views")
        return tuple(references)


class Change(_LifecycleHostView):
    """Live view over one optional descriptive Change in history."""

    __slots__ = ()

    @property
    def revision(self) -> dict[str, Any]:
        return self._backing_record["revision"]

    @property
    def targets(self) -> tuple[dict[str, Any], ...]:
        references = self._backing_record["targets"]
        if not isinstance(references, list):
            raise TypeError("targets must be a JSON array before creating views")
        return tuple(references)

    @property
    def kind(self) -> str:
        return self._backing_record["kind"]


class Tombstone(_TrustHostView):
    """Live view over one explicit identified withdrawal statement."""

    __slots__ = ()

    @property
    def identifier(self) -> str:
        return self._backing_record["id"]

    @property
    def target(self) -> dict[str, Any]:
        return self._backing_record["target"]

    @property
    def target_category(self) -> str:
        return self._backing_record["target_category"]


class _HistoricalMembershipView(_MappingView):
    """Live structural view; membership is not a replay instruction."""

    __slots__ = ()


__all__ = ["Change", "Revision", "Tombstone", "Validity"]
