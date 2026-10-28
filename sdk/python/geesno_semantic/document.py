"""Thin view over a loss-aware parsed SemanticDocument tree."""

from __future__ import annotations

from collections.abc import Iterator, Mapping, Sequence
from copy import deepcopy
from typing import Any

from .assertions import (
    Assertion,
    ConceptRepresentationAssertion,
    PropertyAssertion,
    RelationAssertion,
    TypeAssertion,
    assertion_view,
)
from .entities import Concept, Representation, entity_view
from .extensions import _ExtensionHostMixin
from .lifecycle import (
    Change,
    Revision,
    Tombstone,
    _HistoricalMembershipView,
)
from .sources import Binding, Source
from .terms import expand_qualified_term
from .trust import _TrustHostView, _nested_trust_views


_MISSING = object()


class SemanticDocument(_ExtensionHostMixin, Mapping[str, Any]):
    """A live view whose backing tree remains the source of record.

    Reading the document or creating Entity views never mutates the tree.
    ``add_concept`` and ``add_representation`` are explicit in-place
    mutations; callers can validate the result with the existing S2 facade.
    """

    __slots__ = ("_backing_tree",)

    def __init__(self, backing_tree: dict[str, Any]) -> None:
        if not isinstance(backing_tree, dict):
            raise TypeError("backing_tree must be a parsed JSON object")
        self._backing_tree = backing_tree

    @classmethod
    def create(
        cls,
        *,
        spec_version: str,
        identifier: str,
        scope: Mapping[str, Any],
        namespaces: Mapping[str, str] | None = None,
        profiles: Sequence[Mapping[str, Any]] | None = None,
    ) -> SemanticDocument:
        """Create an owned S2 document tree from explicit caller values.

        This builder fixes no defaults and makes no conformance claim. Optional
        members are included only when explicitly supplied.
        """

        if not isinstance(spec_version, str):
            raise TypeError("spec_version must be a string")
        if not isinstance(identifier, str):
            raise TypeError("identifier must be a string")
        if not isinstance(scope, Mapping):
            raise TypeError("scope must be a mapping")
        if namespaces is not None and not isinstance(namespaces, Mapping):
            raise TypeError("namespaces must be a mapping")
        if profiles is not None and (
            isinstance(profiles, (str, bytes)) or not isinstance(profiles, Sequence)
        ):
            raise TypeError("profiles must be a sequence of mappings")

        tree: dict[str, Any] = {
            "spec_version": spec_version,
            "id": identifier,
            "scope": deepcopy(dict(scope)),
        }
        if namespaces is not None:
            tree["namespaces"] = deepcopy(dict(namespaces))
        if profiles is not None:
            copied_profiles: list[dict[str, Any]] = []
            for profile in profiles:
                if not isinstance(profile, Mapping):
                    raise TypeError("each profile must be a mapping")
                copied_profiles.append(deepcopy(dict(profile)))
            tree["profiles"] = copied_profiles
        return cls(tree)

    @property
    def backing_tree(self) -> dict[str, Any]:
        """Return the loss-aware mapping/list/scalar tree without copying it."""

        return self._backing_tree

    def _extension_host_record(self) -> dict[str, Any]:
        return self._backing_tree

    @property
    def namespaces(self) -> Mapping[str, str]:
        """Return exact document-local namespace declarations read-only."""

        namespaces = self._backing_tree.get("namespaces", {})
        if not isinstance(namespaces, dict):
            raise TypeError("namespaces must be a JSON object before creating a view")
        return namespaces.copy()

    def namespace(self, prefix: str) -> str:
        """Return one exact expansion base without discovery or dereference."""

        if not isinstance(prefix, str):
            raise TypeError("prefix must be a string")
        return self.namespaces[prefix]

    def expand_term(self, term: str) -> str:
        """Expand one qualified term by direct local concatenation only."""

        return expand_qualified_term(term, self.namespaces)

    def create_projection(
        self,
        *,
        selection_context: Mapping[str, Any],
        projection_scope: Mapping[str, Any],
        projection_completeness: str,
        carried_content_selection: Mapping[str, Sequence[str]],
        reference_availability: Sequence[Mapping[str, Any]],
        **explicit_projection_inputs: Any,
    ) -> Any:
        """Materialize a caller-selected exact Profile 0.1 Projection."""

        from .projection import create_projection

        return create_projection(
            self,
            selection_context=selection_context,
            projection_scope=projection_scope,
            projection_completeness=projection_completeness,
            carried_content_selection=carried_content_selection,
            reference_availability=reference_availability,
            **explicit_projection_inputs,
        )

    @property
    def spec_version(self) -> str:
        """Return the exact supported version selected during load."""

        return self._backing_tree["spec_version"]

    @property
    def entities(self) -> tuple[Concept | Representation, ...]:
        """Return a fresh tuple of live views in serialized Entity order."""

        records = self._backing_tree.get("entities", [])
        if not isinstance(records, list):
            raise TypeError("entities must be a JSON array before creating views")
        return tuple(entity_view(record) for record in records)

    @property
    def concepts(self) -> tuple[Concept, ...]:
        """Return the Concept views without changing or reordering records."""

        return tuple(
            entity for entity in self.entities if isinstance(entity, Concept)
        )

    @property
    def representations(self) -> tuple[Representation, ...]:
        """Return the Representation views without changing records."""

        return tuple(
            entity
            for entity in self.entities
            if isinstance(entity, Representation)
        )

    @property
    def sources(self) -> tuple[Source, ...]:
        """Return live Source views in serialized order."""

        return tuple(Source(record) for record in self._record_collection("sources"))

    @property
    def bindings(self) -> tuple[Binding, ...]:
        """Return live Binding views in serialized order."""

        return tuple(Binding(record) for record in self._record_collection("bindings"))

    @property
    def assertions(self) -> tuple[Assertion, ...]:
        """Return typed live Assertion views in serialized order."""

        return tuple(
            assertion_view(record) for record in self._record_collection("assertions")
        )

    @property
    def revision(self) -> Revision | None:
        """Return the explicit current Revision without consulting history."""

        record = self._backing_tree.get("revision")
        if record is None:
            return None
        return Revision(self._mapping_record(record, "revision"))

    @property
    def historical_revisions(self) -> tuple[Revision, ...]:
        """Return previous or otherwise historical Revision views."""

        return tuple(
            Revision(record) for record in self._history_collection("revisions")
        )

    @property
    def changes(self) -> tuple[Change, ...]:
        """Return descriptive Changes without applying or replaying them."""

        return tuple(Change(record) for record in self._history_collection("changes"))

    @property
    def tombstones(self) -> tuple[Tombstone, ...]:
        """Return explicit current Tombstone views in serialized order."""

        return tuple(
            Tombstone(record) for record in self._record_collection("tombstones")
        )

    @property
    def history_memberships(self) -> tuple[Mapping[str, Any], ...]:
        """Return historical membership edges without reconstructing state."""

        return tuple(
            _HistoricalMembershipView(record)
            for record in self._history_collection("records")
        )

    @property
    def trust_hosts(self) -> tuple[_TrustHostView, ...]:
        """Enumerate exactly the S2 records that may host trust metadata."""

        hosts: list[_TrustHostView] = [
            *self.entities,
            *self.sources,
            *self.bindings,
            *self.assertions,
        ]
        revision = self.revision
        if revision is not None:
            hosts.append(revision)
        hosts.extend(self.tombstones)
        hosts.extend(self.historical_revisions)
        hosts.extend(self.changes)

        all_hosts: list[_TrustHostView] = []
        for host in hosts:
            all_hosts.append(host)
            all_hosts.extend(_nested_trust_views(host))
        return tuple(all_hosts)

    @property
    def extension_hosts(self) -> tuple[_ExtensionHostMixin, ...]:
        """Enumerate exactly the S2 Extension hosts represented by SDK views."""

        return (self, *self.trust_hosts)

    def set_revision(
        self,
        *,
        identifier: str,
        parents: Sequence[Mapping[str, Any]] | None = None,
    ) -> Revision:
        """Set the explicit current Revision without deriving lineage."""

        record = self._revision_record(identifier, parents)
        self._backing_tree["revision"] = record
        return Revision(record)

    def set_history(
        self,
        *,
        completeness: str,
        definition: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create one explicit history envelope without inferring coverage."""

        if "history" in self._backing_tree:
            raise ValueError("history already exists")
        history: dict[str, Any] = {
            "completeness": self._string(completeness, "completeness")
        }
        if definition is not None:
            history["definition"] = self._mapping(definition, "definition")
        self._backing_tree["history"] = history
        return history

    def add_history_revision(
        self,
        *,
        identifier: str,
        parents: Sequence[Mapping[str, Any]] | None = None,
    ) -> Revision:
        """Append one explicit historical Revision to an existing history."""

        record = self._revision_record(identifier, parents)
        self._append_history_record("revisions", record)
        return Revision(record)

    def add_change(
        self,
        *,
        revision: Mapping[str, Any],
        targets: Sequence[Mapping[str, Any]],
        kind: str,
        identifier: str | None = None,
        details: Any = _MISSING,
    ) -> Change:
        """Append a descriptive Change without applying it to current state."""

        record: dict[str, Any] = {
            "revision": self._mapping(revision, "revision"),
            "targets": self._mapping_sequence(targets, "targets"),
            "kind": self._string(kind, "kind"),
        }
        if identifier is not None:
            record["id"] = self._string(identifier, "identifier")
        if details is not _MISSING:
            record["details"] = deepcopy(details)
        self._append_history_record("changes", record)
        return Change(record)

    def add_tombstone(
        self,
        *,
        identifier: str,
        target: Mapping[str, Any],
        target_category: str,
        reason: str | None = None,
    ) -> Tombstone:
        """Append one explicit Tombstone without removing its target."""

        record: dict[str, Any] = {
            "id": self._string(identifier, "identifier"),
            "target": self._mapping(target, "target"),
            "target_category": self._string(target_category, "target_category"),
        }
        if reason is not None:
            record["reason"] = self._string(reason, "reason")
        self._append_record("tombstones", record)
        return Tombstone(record)

    def add_history_membership(
        self,
        *,
        revision: Mapping[str, Any],
        target: Mapping[str, Any],
    ) -> Mapping[str, Any]:
        """Append one membership edge without copying or reconstructing records."""

        record = {
            "revision": self._mapping(revision, "revision"),
            "target": self._mapping(target, "target"),
        }
        self._append_history_record("records", record)
        return _HistoricalMembershipView(record)

    def add_concept(self, *, identifier: str) -> Concept:
        """Append one minimal Concept to the canonical ``entities`` array."""

        record = self._append_entity(identifier, "concept")
        return Concept(record)

    def add_representation(self, *, identifier: str) -> Representation:
        """Append one minimal Representation to the canonical ``entities`` array."""

        record = self._append_entity(identifier, "representation")
        return Representation(record)

    def add_source(
        self,
        *,
        identifier: str,
        locations: Sequence[Mapping[str, Any]] | None = None,
        revision: Mapping[str, Any] | None = None,
        fingerprints: Sequence[Mapping[str, Any]] | None = None,
    ) -> Source:
        """Append one explicit Source without deriving identity or metadata."""

        record: dict[str, Any] = {"id": self._string(identifier, "identifier")}
        if locations is not None:
            record["locations"] = self._mapping_sequence(locations, "locations")
        if revision is not None:
            record["revision"] = self._mapping(revision, "revision")
        if fingerprints is not None:
            record["fingerprints"] = self._mapping_sequence(
                fingerprints, "fingerprints"
            )
        self._append_record("sources", record)
        return Source(record)

    def add_binding(
        self,
        *,
        identifier: str,
        entity: Mapping[str, Any],
        source: Mapping[str, Any],
        locator: Mapping[str, Any] | None = None,
        method: str | None = None,
    ) -> Binding:
        """Append one explicit Entity-to-Source correlation record."""

        record: dict[str, Any] = {
            "id": self._string(identifier, "identifier"),
            "entity": self._mapping(entity, "entity"),
            "source": self._mapping(source, "source"),
        }
        if locator is not None:
            record["locator"] = self._mapping(locator, "locator")
        if method is not None:
            record["method"] = self._string(method, "method")
        self._append_record("bindings", record)
        return Binding(record)

    def add_type_assertion(
        self,
        *,
        identifier: str,
        subject: Mapping[str, Any],
        type_term: str,
    ) -> TypeAssertion:
        """Append one explicit Type Assertion in canonical placement."""

        record = self._assertion_record(identifier, "type", subject)
        record["type"] = self._string(type_term, "type_term")
        self._append_record("assertions", record)
        return TypeAssertion(record)

    def add_property_assertion(
        self,
        *,
        identifier: str,
        subject: Mapping[str, Any],
        property_term: str,
        value: Any = _MISSING,
        condition: Mapping[str, Any] | object = _MISSING,
    ) -> PropertyAssertion:
        """Append one Property Assertion with exactly one explicit branch."""

        if (value is _MISSING) == (condition is _MISSING):
            raise TypeError("provide exactly one of value or condition")
        record = self._assertion_record(identifier, "property", subject)
        record["property"] = self._string(property_term, "property_term")
        if value is not _MISSING:
            record["value"] = deepcopy(value)
        else:
            record["condition"] = self._mapping(condition, "condition")
        self._append_record("assertions", record)
        return PropertyAssertion(record)

    def add_relation_assertion(
        self,
        *,
        identifier: str,
        subject: Mapping[str, Any],
        predicate: str,
        object_reference: Mapping[str, Any],
    ) -> RelationAssertion:
        """Append one directed Relation without creating an inverse."""

        record = self._assertion_record(identifier, "relation", subject)
        record["predicate"] = self._string(predicate, "predicate")
        record["object"] = self._mapping(object_reference, "object_reference")
        self._append_record("assertions", record)
        return RelationAssertion(record)

    def add_concept_representation_assertion(
        self,
        *,
        identifier: str,
        representation: Mapping[str, Any],
        concept: Mapping[str, Any],
    ) -> ConceptRepresentationAssertion:
        """Append one caller-requested Representation-to-Concept association."""

        record = self._assertion_record(
            identifier, "concept_representation", representation
        )
        record["concept"] = self._mapping(concept, "concept")
        self._append_record("assertions", record)
        return ConceptRepresentationAssertion(record)

    def _append_entity(self, identifier: str, kind: str) -> dict[str, Any]:
        if not isinstance(identifier, str):
            raise TypeError("identifier must be a string")
        records = self._backing_tree.get("entities")
        if records is None:
            records = []
            self._backing_tree["entities"] = records
        elif not isinstance(records, list):
            raise TypeError("entities must be a JSON array before appending")
        record = {"id": identifier, "kind": kind}
        records.append(record)
        return record

    def _assertion_record(
        self,
        identifier: str,
        kind: str,
        subject: Mapping[str, Any],
    ) -> dict[str, Any]:
        return {
            "id": self._string(identifier, "identifier"),
            "kind": kind,
            "subject": self._mapping(subject, "subject"),
        }

    def _record_collection(self, name: str) -> list[dict[str, Any]]:
        records = self._backing_tree.get(name, [])
        if not isinstance(records, list):
            raise TypeError(f"{name} must be a JSON array before creating views")
        return records

    def _history_collection(self, name: str) -> list[dict[str, Any]]:
        history = self._backing_tree.get("history", {})
        if not isinstance(history, dict):
            raise TypeError("history must be a JSON object before creating views")
        records = history.get(name, [])
        if not isinstance(records, list):
            raise TypeError(f"history.{name} must be a JSON array before views")
        return records

    @staticmethod
    def _mapping_record(value: Any, name: str) -> dict[str, Any]:
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be a JSON object before creating views")
        return value

    def _append_record(self, collection: str, record: dict[str, Any]) -> None:
        records = self._backing_tree.get(collection)
        if records is None:
            records = []
            self._backing_tree[collection] = records
        elif not isinstance(records, list):
            raise TypeError(f"{collection} must be a JSON array before appending")
        records.append(record)

    def _append_history_record(self, collection: str, record: dict[str, Any]) -> None:
        history = self._backing_tree.get("history")
        if not isinstance(history, dict):
            raise ValueError("set_history must be called explicitly before adding history")
        records = history.get(collection)
        if records is None:
            records = []
            history[collection] = records
        elif not isinstance(records, list):
            raise TypeError(
                f"history.{collection} must be a JSON array before appending"
            )
        records.append(record)

    def _revision_record(
        self,
        identifier: str,
        parents: Sequence[Mapping[str, Any]] | None,
    ) -> dict[str, Any]:
        record: dict[str, Any] = {
            "id": self._string(identifier, "identifier")
        }
        if parents is not None:
            record["parents"] = self._mapping_sequence(parents, "parents")
        return record

    @staticmethod
    def _string(value: str, name: str) -> str:
        if not isinstance(value, str):
            raise TypeError(f"{name} must be a string")
        return value

    @staticmethod
    def _mapping(value: Mapping[str, Any] | object, name: str) -> dict[str, Any]:
        if not isinstance(value, Mapping):
            raise TypeError(f"{name} must be a mapping")
        return deepcopy(dict(value))

    @classmethod
    def _mapping_sequence(
        cls,
        value: Sequence[Mapping[str, Any]],
        name: str,
    ) -> list[dict[str, Any]]:
        if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
            raise TypeError(f"{name} must be a sequence of mappings")
        return [cls._mapping(item, f"{name} item") for item in value]

    def __getitem__(self, key: str) -> Any:
        return self._backing_tree[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._backing_tree)

    def __len__(self) -> int:
        return len(self._backing_tree)
