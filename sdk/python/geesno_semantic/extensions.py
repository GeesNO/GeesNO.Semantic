"""Explicit, inert access to Extensions on the accepted S2 host matrix."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from copy import deepcopy
from typing import Any


class _ExtensionMapView(Mapping[str, Any]):
    __slots__ = ("_backing_extensions",)

    def __init__(self, backing_extensions: Mapping[str, Any]) -> None:
        self._backing_extensions = backing_extensions

    def __getitem__(self, key: str) -> Any:
        return self._backing_extensions[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._backing_extensions)

    def __len__(self) -> int:
        return len(self._backing_extensions)


class _ExtensionHostMixin:
    """Shared explicit Extension operations for only schema-approved hosts."""

    __slots__ = ()

    def _extension_host_record(self) -> dict[str, Any]:
        raise NotImplementedError

    @property
    def extensions(self) -> Mapping[str, Any]:
        """Return a read-only live map whose payload objects are not copied."""

        extensions = self._extension_host_record().get("extensions")
        if extensions is None:
            return _ExtensionMapView({})
        if not isinstance(extensions, dict):
            raise TypeError("extensions must be a JSON object before creating a view")
        return _ExtensionMapView(extensions)

    def get_extension(self, term: str) -> Any:
        """Return one exact Extension payload without interpreting it."""

        if not isinstance(term, str):
            raise TypeError("term must be a string")
        return self.extensions[term]

    def set_extension(self, term: str, payload: Any) -> Any:
        """Explicitly add or replace one inert payload without other effects."""

        if not isinstance(term, str):
            raise TypeError("term must be a string")
        record = self._extension_host_record()
        extensions = record.get("extensions")
        if extensions is None:
            extensions = {}
            record["extensions"] = extensions
        elif not isinstance(extensions, dict):
            raise TypeError("extensions must be a JSON object before mutation")
        copied = deepcopy(payload)
        extensions[term] = copied
        return copied

    def remove_extension(self, term: str) -> Any:
        """Explicitly remove one payload and no lifecycle or namespace data."""

        if not isinstance(term, str):
            raise TypeError("term must be a string")
        record = self._extension_host_record()
        extensions = record.get("extensions")
        if not isinstance(extensions, dict):
            raise KeyError(term)
        removed = extensions.pop(term)
        if not extensions:
            del record["extensions"]
        return removed


__all__: list[str] = []
