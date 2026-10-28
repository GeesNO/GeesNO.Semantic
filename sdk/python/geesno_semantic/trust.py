"""Host-scoped views and explicit builders for accepted S2 trust records."""

from __future__ import annotations

from collections.abc import Iterator, Mapping, Sequence
from copy import deepcopy
from typing import Any

from .extensions import _ExtensionHostMixin


_MISSING = object()


class _TrustHostView(_ExtensionHostMixin, Mapping[str, Any]):
    """Live view over one S2 record that may host scoped trust metadata."""

    __slots__ = ("_backing_record",)

    def __init__(self, backing_record: dict[str, Any]) -> None:
        if not isinstance(backing_record, dict):
            raise TypeError("backing_record must be a JSON object")
        self._backing_record = backing_record

    @property
    def backing_record(self) -> dict[str, Any]:
        """Return the live record without copying or normalization."""

        return self._backing_record

    def _extension_host_record(self) -> dict[str, Any]:
        return self._backing_record

    @property
    def identifier(self) -> str | None:
        """Return an explicit ID, or ``None`` for an anonymous trust record."""

        return self._backing_record.get("id")

    @property
    def provenance(self) -> tuple[Provenance, ...]:
        """Return immediate Provenance records in serialized order."""

        return tuple(
            Provenance(record)
            for record in self._trust_collection("provenance")
        )

    @property
    def confidence(self) -> tuple[Confidence, ...]:
        """Return immediate Confidence records in serialized order."""

        return tuple(
            Confidence(record)
            for record in self._trust_collection("confidence")
        )

    @property
    def reviews(self) -> tuple[Review, ...]:
        """Return immediate Review records in serialized order."""

        return tuple(Review(record) for record in self._trust_collection("reviews"))

    def add_provenance(
        self,
        *,
        kind: str,
        identifier: str | None = None,
        sources: Sequence[Mapping[str, Any]] | None = None,
        details: Any = _MISSING,
    ) -> Provenance:
        """Append one scoped Provenance record from explicit caller values."""

        record: dict[str, Any] = {"kind": _string(kind, "kind")}
        _add_identifier(record, identifier)
        if sources is not None:
            record["sources"] = _mapping_sequence(sources, "sources")
        if details is not _MISSING:
            record["details"] = deepcopy(details)
        self._append_trust("provenance", record)
        return Provenance(record)

    def add_confidence(
        self,
        *,
        score: Mapping[str, Any],
        identifier: str | None = None,
        method: str | None = None,
        details: Any = _MISSING,
    ) -> Confidence:
        """Append one exact Confidence record without score interpretation."""

        record: dict[str, Any] = {"score": _mapping(score, "score")}
        _add_identifier(record, identifier)
        if method is not None:
            record["method"] = _string(method, "method")
        if details is not _MISSING:
            record["details"] = deepcopy(details)
        self._append_trust("confidence", record)
        return Confidence(record)

    def add_review(
        self,
        *,
        disposition: str,
        identifier: str | None = None,
        details: Any = _MISSING,
    ) -> Review:
        """Append one scoped Review without truth or permission inference."""

        record: dict[str, Any] = {
            "disposition": _string(disposition, "disposition")
        }
        _add_identifier(record, identifier)
        if details is not _MISSING:
            record["details"] = deepcopy(details)
        self._append_trust("reviews", record)
        return Review(record)

    def _trust_collection(self, member: str) -> list[dict[str, Any]]:
        records = self._backing_record.get(member, [])
        if not isinstance(records, list):
            raise TypeError(f"{member} must be a JSON array before creating views")
        return records

    def _append_trust(self, member: str, record: dict[str, Any]) -> None:
        records = self._backing_record.get(member)
        if records is None:
            records = []
            self._backing_record[member] = records
        elif not isinstance(records, list):
            raise TypeError(f"{member} must be a JSON array before appending")
        records.append(record)

    def __getitem__(self, key: str) -> Any:
        return self._backing_record[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._backing_record)

    def __len__(self) -> int:
        return len(self._backing_record)


class _LifecycleHostView(_TrustHostView):
    """Trust host that accepts S2 supersession and validity metadata."""

    __slots__ = ()

    @property
    def supersedes(self) -> tuple[dict[str, Any], ...]:
        """Return live supersession references in serialized order."""

        references = self._backing_record.get("supersedes", [])
        if not isinstance(references, list):
            raise TypeError("supersedes must be a JSON array before creating views")
        return tuple(references)

    @property
    def validity(self) -> Validity | None:
        """Return the live Validity descriptor when explicitly present."""

        from .lifecycle import Validity

        record = self._backing_record.get("validity")
        if record is None:
            return None
        if not isinstance(record, dict):
            raise TypeError("validity must be a JSON object before creating a view")
        return Validity(record)

    def add_supersedes(self, reference: Mapping[str, Any]) -> dict[str, Any]:
        """Append one explicit supersession reference without mutating targets."""

        copied = _mapping(reference, "reference")
        references = self._backing_record.get("supersedes")
        if references is None:
            references = []
            self._backing_record["supersedes"] = references
        elif not isinstance(references, list):
            raise TypeError("supersedes must be a JSON array before appending")
        references.append(copied)
        return copied

    def set_validity(
        self,
        *,
        kind: str,
        from_value: Any = _MISSING,
        until: Any = _MISSING,
    ) -> Validity:
        """Set one explicit S2 Validity descriptor without temporal inference."""

        from .lifecycle import Validity

        if from_value is _MISSING and until is _MISSING:
            raise TypeError("provide at least one of from_value or until")
        record: dict[str, Any] = {"kind": _string(kind, "kind")}
        if from_value is not _MISSING:
            record["from"] = deepcopy(from_value)
        if until is not _MISSING:
            record["until"] = deepcopy(until)
        self._backing_record["validity"] = record
        return Validity(record)


class Provenance(_LifecycleHostView):
    """Live view over one host-scoped S2 Provenance record."""

    __slots__ = ()

    @property
    def kind(self) -> str:
        return self._backing_record["kind"]


class Confidence(_LifecycleHostView):
    """Live view over one host-scoped S2 Confidence record."""

    __slots__ = ()

    @property
    def score(self) -> dict[str, Any]:
        return self._backing_record["score"]


class Review(_LifecycleHostView):
    """Live view over one host-scoped S2 Review record."""

    __slots__ = ()

    @property
    def disposition(self) -> str:
        return self._backing_record["disposition"]


def _nested_trust_views(host: _TrustHostView) -> tuple[_TrustHostView, ...]:
    views: list[_TrustHostView] = []
    for member, view_type in (
        ("provenance", Provenance),
        ("confidence", Confidence),
        ("reviews", Review),
    ):
        for record in host._trust_collection(member):
            view = view_type(record)
            views.append(view)
            views.extend(_nested_trust_views(view))
    return tuple(views)


def _add_identifier(record: dict[str, Any], identifier: str | None) -> None:
    if identifier is not None:
        record["id"] = _string(identifier, "identifier")


def _string(value: str, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    return value


def _mapping(value: Mapping[str, Any], name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{name} must be a mapping")
    return deepcopy(dict(value))


def _mapping_sequence(
    value: Sequence[Mapping[str, Any]],
    name: str,
) -> list[dict[str, Any]]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise TypeError(f"{name} must be a sequence of mappings")
    return [_mapping(item, f"{name} item") for item in value]


__all__ = ["Confidence", "Provenance", "Review"]
