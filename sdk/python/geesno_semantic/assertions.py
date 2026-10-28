"""Non-copying views over the four accepted S2 assertion kinds."""

from __future__ import annotations

from typing import Any

from .trust import _LifecycleHostView


class Assertion(_LifecycleHostView):
    """Base live view for an identified S2 assertion record."""

    __slots__ = ()

    kind_token: str | None = None

    def __init__(self, backing_record: dict[str, Any]) -> None:
        super().__init__(backing_record)
        if (
            self.kind_token is not None
            and self._backing_record.get("kind") != self.kind_token
        ):
            raise ValueError(
                f"{type(self).__name__} requires kind {self.kind_token!r}"
            )

    @property
    def identifier(self) -> str:
        """Return the assertion's explicit semantic ID."""

        return self._backing_record["id"]

    @property
    def kind(self) -> str:
        """Return the accepted assertion kind token."""

        return self._backing_record["kind"]

class TypeAssertion(Assertion):
    kind_token = "type"


class PropertyAssertion(Assertion):
    kind_token = "property"


class RelationAssertion(Assertion):
    kind_token = "relation"


class ConceptRepresentationAssertion(Assertion):
    kind_token = "concept_representation"


def assertion_view(record: dict[str, Any]) -> Assertion:
    """Create the matching typed assertion view without changing the record."""

    if not isinstance(record, dict):
        raise TypeError("Assertion records must be JSON objects")
    view_type = {
        "type": TypeAssertion,
        "property": PropertyAssertion,
        "relation": RelationAssertion,
        "concept_representation": ConceptRepresentationAssertion,
    }.get(record.get("kind"))
    if view_type is None:
        raise ValueError(f"unsupported Assertion kind for an I3 view: {record.get('kind')!r}")
    return view_type(record)


__all__ = [
    "Assertion",
    "ConceptRepresentationAssertion",
    "PropertyAssertion",
    "RelationAssertion",
    "TypeAssertion",
]
