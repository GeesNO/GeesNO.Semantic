# ADR-0008: Optional many-to-many Concept–Representation association

- **Status:** Accepted
- **Date:** 2026-08-30
- **Accepted by:** Explicit human architecture decision, 2026-08-30
- **Scope:** Abstract cardinality and assertion semantics only

## Context

The Foundation requires multiple Representations per Concept and permits a
Representation before its Concept is known. A one-Concept-per-Representation
assumption also fails for a paragraph containing several requirements, a table
record describing several semantic things, or one observed region/segment with
competing interpretations.

## Decision

At universal-core level:

- Concept to Representation cardinality is `0..*`;
- Representation to Concept cardinality is `0..*`;
- every association is a semantic claim capable of trust/review/lifecycle
  metadata;
- profiles may impose tighter cardinality for interoperable use cases.

The many-to-many cardinality permits multiple Concept–Representation
associations, but does not mean they are all simultaneously true, equivalent,
accepted or authoritative. Each association is an independent semantic
assertion capable of carrying Provenance, Confidence, Review and lifecycle
metadata under ADR-0005.

> **NON-NORMATIVE conceptual example**
>
> ```text
> Representation R1
>   -> Concept C1  accepted
>   -> Concept C2  inferred / confidence 0.61
>   -> Concept C3  rejected
> ```

## Consequences

- Pure Concepts and unassociated Representations remain valid.
- Many occurrences can share one Concept.
- One occurrence can support several Concepts or competing mappings.
- Consumers cannot assume a single `concept_id`; S2 must represent association
  claims without a one-to-one shortcut becoming normative.

## Remains open

Whether the association is a core Relation, a base-vocabulary predicate or a
canonical shortcut governed by Relation/assertion semantics.
