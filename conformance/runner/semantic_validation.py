"""Layer 3 deterministic semantic and cross-record integrity checks."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import re
from typing import Any, Iterable

from rfc3987_syntax2 import is_valid_syntax_iri
if __package__:
    from .raw_parse import ResourceRefusal
else:  # Preserve direct script/path-based runner use.
    from raw_parse import ResourceRefusal


UUID_URN = re.compile(r"^urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
DATE_TIME = re.compile(
    r"^(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})T"
    r"(?P<hour>[0-9]{2}):(?P<minute>[0-9]{2}):(?P<second>[0-9]{2})"
    r"(?:\.(?P<fraction>[0-9]+))?Z$"
)
MAX_EXACT_INTEGER_DIGITS = 4096
MAX_DECIMAL_EXPONENT_ABS = 999_999_999


def bounded_integer(lexical: str) -> int:
    digits = lexical.lstrip("-")
    if len(digits) > MAX_EXACT_INTEGER_DIGITS:
        raise ResourceRefusal(
            "semantic-numeric-limit",
            "exact integer exceeds the configured semantic comparison limit",
        )
    return int(lexical)


def bounded_exponent(lexical: str) -> int:
    exponent = bounded_integer(lexical)
    if abs(exponent) > MAX_DECIMAL_EXPONENT_ABS:
        raise ResourceRefusal(
            "semantic-numeric-limit",
            "decimal exponent exceeds the configured semantic comparison limit",
        )
    return exponent


class SemanticValidationError(ValueError):
    def __init__(self, category: str, message: str) -> None:
        super().__init__(message)
        self.category = category


@dataclass(frozen=True, slots=True)
class AddressableRecord:
    category: str
    value: dict[str, Any]


class SemanticChecker:
    def __init__(self, document: dict[str, Any]) -> None:
        self.document = document
        self.namespaces: dict[str, str] = document.get("namespaces", {})
        self.records: dict[str, AddressableRecord] = {}
        self.revision_edges: dict[str, list[str]] = {}
        self.supersession_edges: dict[str, list[str]] = {}

    def fail(self, category: str, message: str) -> None:
        raise SemanticValidationError(category, message)

    def check_iri(self, value: str) -> None:
        if value.lower().startswith("urn:uuid:"):
            if not UUID_URN.fullmatch(value):
                self.fail("identifier-iri", "UUID URN is not in the canonical lowercase form")
            return
        if not is_valid_syntax_iri(value):
            self.fail("identifier-iri", "identifier is not an absolute RFC 3987 IRI")

    def register(self, value: dict[str, Any], category: str) -> None:
        identifier = value.get("id")
        if identifier is None:
            return
        self.check_iri(identifier)
        if identifier in self.records:
            self.fail("duplicate-id", "addressable ID occurs more than once")
        self.records[identifier] = AddressableRecord(category, value)

    def register_trust(self, host: dict[str, Any]) -> None:
        for member, category in (
            ("provenance", "provenance"),
            ("confidence", "confidence"),
            ("reviews", "review"),
        ):
            for trust in host.get(member, []):
                self.register(trust, category)
                self.register_trust(trust)

    def build_index(self) -> None:
        self.register(self.document, "semantic-document")
        for entity in self.document.get("entities", []):
            self.register(entity, "entity")
            self.register_trust(entity)
        for source in self.document.get("sources", []):
            self.register(source, "source")
            self.register_trust(source)
        for binding in self.document.get("bindings", []):
            self.register(binding, "binding")
            self.register_trust(binding)
        for assertion in self.document.get("assertions", []):
            self.register(assertion, "assertion")
            self.register_trust(assertion)
        revision = self.document.get("revision")
        if revision:
            self.register(revision, "revision")
            self.register_trust(revision)
        for tombstone in self.document.get("tombstones", []):
            self.register(tombstone, "tombstone")
            self.register_trust(tombstone)
        history = self.document.get("history", {})
        for revision in history.get("revisions", []):
            self.register(revision, "revision")
            self.register_trust(revision)
        for change in history.get("changes", []):
            self.register(change, "change")
            self.register_trust(change)

    def check_namespaces(self) -> None:
        bases: dict[str, str] = {}
        for prefix, base in self.namespaces.items():
            self.check_iri(base)
            if base in bases:
                self.fail("namespace-alias", "two prefixes declare the same expansion base")
            bases[base] = prefix

    def expand(self, term: str) -> str:
        prefix, local = term.split(":", 1)
        if prefix not in self.namespaces:
            self.fail("undeclared-prefix", "qualified term uses an undeclared prefix")
        expanded = self.namespaces[prefix] + local
        self.check_iri(expanded)
        return expanded

    def check_extensions(self, host: dict[str, Any]) -> None:
        expanded: set[str] = set()
        for term in host.get("extensions", {}):
            identity = self.expand(term)
            if identity in expanded:
                self.fail("expanded-key-duplicate", "Extension keys expand to the same identity")
            expanded.add(identity)

    def check_reference(
        self,
        reference: dict[str, Any],
        expected_category: str | None = None,
        expected_entity_kind: str | None = None,
    ) -> AddressableRecord | None:
        target = reference["target"]
        self.check_iri(target)
        record = self.records.get(target)
        if reference["location"] == "in-document" and record is None:
            self.fail("unresolved-reference", "in-document target does not resolve")
        if record is not None:
            if expected_category and record.category != expected_category:
                self.fail("target-category", "locally available reference resolves to the wrong record category")
            if expected_entity_kind and record.value.get("kind") != expected_entity_kind:
                self.fail("target-category", "Entity reference resolves to the wrong fundamental kind")
        return record

    def check_reference_array(
        self,
        references: Iterable[dict[str, Any]],
        expected_category: str | None = None,
        unique_targets: bool = False,
    ) -> list[str]:
        targets: list[str] = []
        seen: set[str] = set()
        for reference in references:
            target = reference["target"]
            if unique_targets and target in seen:
                self.fail("repeated-reference", "unordered reference array repeats a target")
            seen.add(target)
            self.check_reference(reference, expected_category)
            targets.append(target)
        return targets

    def check_value(self, value: Any) -> None:
        if isinstance(value, (str, bool)):
            return
        kind = value["kind"]
        if kind == "condition":
            return
        if kind in ("date", "date_time"):
            self.check_temporal(kind, value["value"])
        elif kind == "reference":
            self.check_reference(value["reference"])
        elif kind == "quantity":
            self.expand(value["unit"])
            self.check_value(value["magnitude"])
        elif kind in ("list", "set"):
            for item in value["items"]:
                self.check_value(item)
            if kind == "set":
                seen: set[Any] = set()
                for item in value["items"]:
                    key = self.semantic_key(item)
                    if key in seen:
                        self.fail("set-duplicate", "set contains recursively equal semantic values")
                    seen.add(key)
        elif kind == "structured":
            self.expand(value["datatype"])
            expanded: set[str] = set()
            for term, item in value["members"].items():
                identity = self.expand(term)
                if identity in expanded:
                    self.fail("expanded-key-duplicate", "structured member keys expand to the same identity")
                expanded.add(identity)
                self.check_value(item)

    def semantic_key(self, value: Any) -> Any:
        if isinstance(value, str):
            return ("string", value)
        if isinstance(value, bool):
            return ("boolean", value)
        kind = value["kind"]
        if kind == "condition":
            return ("condition", value["value"])
        if kind == "integer":
            return ("integer", value["value"])
        if kind == "decimal":
            return ("decimal", value["coefficient"], value["exponent"])
        if kind in ("date", "date_time"):
            return (kind, value["value"])
        if kind == "reference":
            reference = value["reference"]
            return ("reference", reference["target"], reference["location"])
        if kind == "quantity":
            return ("quantity", self.semantic_key(value["magnitude"]), self.expand(value["unit"]))
        if kind == "list":
            return ("list", tuple(self.semantic_key(item) for item in value["items"]))
        if kind == "set":
            return ("set", frozenset(self.semantic_key(item) for item in value["items"]))
        if kind == "structured":
            return (
                "structured",
                self.expand(value["datatype"]),
                frozenset((self.expand(term), self.semantic_key(item)) for term, item in value["members"].items()),
            )
        raise AssertionError(f"unexpected value kind {kind!r}")

    def check_temporal(self, kind: str, lexical: str) -> None:
        try:
            if kind == "date":
                parsed = date.fromisoformat(lexical)
                if parsed.year == 0:
                    raise ValueError
            else:
                match = DATE_TIME.fullmatch(lexical)
                if not match:
                    raise ValueError
                parsed = date.fromisoformat(match.group("date"))
                if parsed.year == 0:
                    raise ValueError
        except ValueError as error:
            self.fail("temporal-calendar", "temporal lexical value is not a valid Gregorian date")

    def comparable(self, value: Any) -> tuple[str, Any] | None:
        if not isinstance(value, dict):
            return None
        kind = value.get("kind")
        if kind == "integer":
            return (kind, bounded_integer(value["value"]))
        if kind == "decimal":
            coefficient = value["coefficient"]
            exponent = value["exponent"]
            if len(coefficient.lstrip("-")) > MAX_EXACT_INTEGER_DIGITS:
                raise ResourceRefusal(
                    "semantic-numeric-limit",
                    "decimal coefficient exceeds the configured semantic comparison limit",
                )
            bounded_exponent(exponent)
            from decimal import Decimal

            return (kind, Decimal(f"{coefficient}e{exponent}"))
        if kind == "date":
            return (kind, date.fromisoformat(value["value"]))
        if kind == "date_time":
            match = DATE_TIME.fullmatch(value["value"])
            assert match
            fraction = (match.group("fraction") or "")
            return (
                kind,
                (
                    date.fromisoformat(match.group("date")),
                    int(match.group("hour")),
                    int(match.group("minute")),
                    int(match.group("second")),
                    fraction.rstrip("0").ljust(max(1, len(fraction)), "0"),
                ),
            )
        return None

    def check_validity(self, validity: dict[str, Any]) -> None:
        self.expand(validity["kind"])
        for member in ("from", "until"):
            if member in validity:
                self.check_value(validity[member])
        if "from" in validity and "until" in validity:
            start = self.comparable(validity["from"])
            end = self.comparable(validity["until"])
            if start is not None and end is not None and start[0] == end[0] and end[1] < start[1]:
                self.fail("validity-order", "known comparable validity end precedes start")

    def check_confidence_score(self, score: dict[str, Any]) -> None:
        kind = score["kind"]
        if kind == "integer":
            if score["value"] not in ("0", "1"):
                self.fail("confidence-range", "Confidence score is outside inclusive range 0..1")
            return
        coefficient = score["coefficient"]
        exponent = bounded_exponent(score["exponent"])
        if coefficient.startswith("-"):
            self.fail("confidence-range", "Confidence score is outside inclusive range 0..1")
        if coefficient == "0":
            return
        if not (len(coefficient) + exponent <= 0 or (coefficient == "1" and exponent == 0)):
            self.fail("confidence-range", "Confidence score is outside inclusive range 0..1")

    def check_host(self, host: dict[str, Any], host_id: str | None = None) -> None:
        self.check_extensions(host)
        if host_id is None and "reviews" in host:
            self.fail("conditional-id", "reviewed record requires an ID")
        if "validity" in host:
            if host_id is None:
                self.fail("conditional-id", "independently lifecycle-managed record requires an ID")
            self.check_validity(host["validity"])
        if "supersedes" in host:
            if host_id is None:
                self.fail("conditional-id", "superseding record requires an ID")
            targets = self.check_reference_array(host["supersedes"], unique_targets=True)
            if host_id in targets:
                self.fail("self-supersession", "record supersedes itself")
            self.supersession_edges.setdefault(host_id, []).extend(targets)
        for provenance in host.get("provenance", []):
            self.expand(provenance["kind"])
            if "sources" in provenance:
                self.check_reference_array(provenance["sources"], "source", unique_targets=True)
            if "details" in provenance:
                self.check_value(provenance["details"])
            self.check_host(provenance, provenance.get("id"))
        for confidence in host.get("confidence", []):
            self.check_confidence_score(confidence["score"])
            self.check_value(confidence["score"])
            if "method" in confidence:
                self.expand(confidence["method"])
            if "details" in confidence:
                self.check_value(confidence["details"])
            self.check_host(confidence, confidence.get("id"))
        for review in host.get("reviews", []):
            self.expand(review["disposition"])
            if "details" in review:
                self.check_value(review["details"])
            self.check_host(review, review.get("id"))

    def check_records(self) -> None:
        self.check_host(self.document, self.document["id"])
        scope = self.document["scope"]
        if "definition" in scope:
            self.expand(scope["definition"]["kind"])
            self.check_value(scope["definition"]["value"])

        profile_ids: set[str] = set()
        for profile in self.document.get("profiles", []):
            self.check_iri(profile["profile"])
            if profile["profile"] in profile_ids:
                self.fail("duplicate-profile", "profile identity is declared more than once")
            profile_ids.add(profile["profile"])

        for entity in self.document.get("entities", []):
            self.check_host(entity, entity["id"])

        for source in self.document.get("sources", []):
            for descriptor in source.get("locations", []):
                self.expand(descriptor["kind"])
                self.check_value(descriptor["value"])
            if "revision" in source:
                self.expand(source["revision"]["kind"])
                self.check_value(source["revision"]["value"])
            for fingerprint in source.get("fingerprints", []):
                self.expand(fingerprint["algorithm"])
            self.check_host(source, source["id"])

        for binding in self.document.get("bindings", []):
            self.check_reference(binding["entity"], "entity")
            self.check_reference(binding["source"], "source")
            if "locator" in binding:
                self.expand(binding["locator"]["kind"])
                self.check_value(binding["locator"]["value"])
            if "method" in binding:
                self.expand(binding["method"])
            self.check_host(binding, binding["id"])

        for assertion in self.document.get("assertions", []):
            kind = assertion["kind"]
            if kind == "concept_representation":
                self.check_reference(assertion["subject"], "entity", "representation")
                self.check_reference(assertion["concept"], "entity", "concept")
            else:
                self.check_reference(assertion["subject"], "entity")
                if kind == "type":
                    self.expand(assertion["type"])
                elif kind == "property":
                    self.expand(assertion["property"])
                    self.check_value(assertion.get("value", assertion.get("condition")))
                elif kind == "relation":
                    self.expand(assertion["predicate"])
                    self.check_reference(assertion["object"], "entity")
            self.check_host(assertion, assertion["id"])

        revisions: list[dict[str, Any]] = []
        if self.document.get("revision"):
            revisions.append(self.document["revision"])
        history = self.document.get("history", {})
        revisions.extend(history.get("revisions", []))
        for revision in revisions:
            targets = self.check_reference_array(
                revision.get("parents", []), "revision", unique_targets=True
            )
            if revision["id"] in targets:
                self.fail("revision-self-parent", "Revision is its own parent")
            self.revision_edges[revision["id"]] = targets
            self.check_host(revision, revision["id"])

        for tombstone in self.document.get("tombstones", []):
            record = self.check_reference(tombstone["target"])
            if record is not None:
                if record.category != tombstone["target_category"]:
                    self.fail("tombstone-category", "Tombstone category does not match its local target")
                self.fail("live-tombstone", "current record and current Tombstone contradict each other")
            if "reason" in tombstone:
                self.expand(tombstone["reason"])
            self.check_host(tombstone, tombstone["id"])

        if "definition" in history:
            self.expand(history["definition"]["kind"])
            self.check_value(history["definition"]["value"])
        for change in history.get("changes", []):
            change_id = change.get("id")
            if change_id is None and any(name in change for name in ("reviews", "supersedes", "validity")):
                self.fail("conditional-id", "independently lifecycle-managed Change requires an ID")
            self.check_reference(change["revision"], "revision")
            self.check_reference_array(change["targets"], unique_targets=True)
            self.expand(change["kind"])
            if "details" in change:
                self.check_value(change["details"])
            self.check_host(change, change_id)
        for membership in history.get("records", []):
            self.check_reference(membership["revision"], "revision")
            self.check_reference(membership["target"])

    def check_cycle(self, graph: dict[str, list[str]], category: str) -> None:
        state: dict[str, int] = {}

        for start in graph:
            if state.get(start, 0) == 2:
                continue
            stack: list[tuple[str, int]] = [(start, 0)]
            while stack:
                node, next_index = stack[-1]
                if state.get(node, 0) == 0:
                    state[node] = 1

                targets = graph.get(node, [])
                while next_index < len(targets):
                    target = targets[next_index]
                    next_index += 1
                    stack[-1] = (node, next_index)
                    if target not in graph:
                        continue
                    mark = state.get(target, 0)
                    if mark == 1:
                        self.fail(category, "closed local directed graph contains a cycle")
                    if mark == 0:
                        stack.append((target, 0))
                        break
                else:
                    state[node] = 2
                    stack.pop()

    def run(self) -> None:
        self.build_index()
        self.check_namespaces()
        self.check_records()
        self.check_cycle(self.revision_edges, "revision-cycle")
        self.check_cycle(self.supersession_edges, "supersession-cycle")


def validate(document: dict[str, Any]) -> None:
    SemanticChecker(document).run()
