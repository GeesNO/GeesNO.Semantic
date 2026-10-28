"""Exact local qualified-term and caller-supplied Vocabulary access."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from typing import Any


def split_qualified_term(term: str) -> tuple[str, str]:
    """Split one S2 qualified term without normalization or case folding.

    Full lexical conformance remains owned by the existing S2 validator.
    """

    if not isinstance(term, str):
        raise TypeError("term must be a string")
    prefix, separator, local = term.partition(":")
    if not separator or not prefix or not local or ":" in local:
        raise ValueError("term must contain one non-empty prefix and local part")
    return prefix, local


def expand_qualified_term(term: str, namespaces: Mapping[str, str]) -> str:
    """Apply the accepted direct-concatenation algorithm entirely locally."""

    if not isinstance(namespaces, Mapping):
        raise TypeError("namespaces must be a mapping")
    prefix, local = split_qualified_term(term)
    base = namespaces[prefix]
    if not isinstance(base, str):
        raise TypeError("namespace expansion base must be a string")
    return base + local


class _TermsView(Mapping[str, Any]):
    __slots__ = ("_terms",)

    def __init__(self, terms: Mapping[str, Any]) -> None:
        self._terms = terms

    def __getitem__(self, key: str) -> Any:
        return self._terms[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._terms)

    def __len__(self) -> int:
        return len(self._terms)


class VocabularyView:
    """Read-only exact lookup over one caller-supplied local inventory.

    The mapping is an SDK input, not a normative Vocabulary artifact or
    serialization binding. Records remain opaque and are never dereferenced.
    """

    __slots__ = ("_identity", "_version", "_terms")

    def __init__(
        self,
        *,
        identity: str,
        version: str,
        terms: Mapping[str, Any],
    ) -> None:
        if not isinstance(identity, str):
            raise TypeError("identity must be a string")
        if not isinstance(version, str):
            raise TypeError("version must be a string")
        if not isinstance(terms, Mapping):
            raise TypeError("terms must be a mapping")
        self._identity = identity
        self._version = version
        self._terms = terms

    @property
    def identity(self) -> str:
        return self._identity

    @property
    def version(self) -> str:
        return self._version

    @property
    def edition(self) -> tuple[str, str]:
        return self._identity, self._version

    @property
    def terms(self) -> Mapping[str, Any]:
        return _TermsView(self._terms)

    def has_term(self, exact_term: str) -> bool:
        if not isinstance(exact_term, str):
            raise TypeError("exact_term must be a string")
        return exact_term in self._terms

    def get_term(self, exact_term: str) -> Any:
        if not isinstance(exact_term, str):
            raise TypeError("exact_term must be a string")
        return self._terms[exact_term]

    def list_terms(self) -> tuple[str, ...]:
        return tuple(self._terms)


__all__ = ["VocabularyView", "expand_qualified_term", "split_qualified_term"]
