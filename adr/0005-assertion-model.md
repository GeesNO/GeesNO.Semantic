# ADR-0005: Common hybrid assertion contract

- **Status:** Accepted
- **Date:** 2026-08-30
- **Accepted by:** Explicit human architecture decision, 2026-08-30
- **Scope:** Abstract assertion contract only; no serialization or identifier syntax

## Context

Type Assertions, Property Assertions, Relations and Concept–Representation
associations all need consistent Provenance, Confidence, Review, lifecycle and
Extension semantics. Inline records are compact, while universally first-class
objects provide strong identity and targeting at substantial complexity and
size cost.

The full comparison is in [`spec/assertions.md`](../spec/assertions.md).

## Decision

Adopt a hybrid abstract model:

1. assertion categories remain specialized by claim body;
2. all obey one common conceptual contract for subject, claim body,
   Provenance, Confidence, Review, lifecycle and Extensions;
3. a claim can be independently addressable when another record must cite,
   review, conflict with or supersede it;
4. addressability does not yet determine JSON nesting or an always-required ID;
5. S2 must define one canonical representation so inline and referenced forms
   cannot become ambiguous dialects.

## Consequences

- Trust and lifecycle behavior remains consistent across claim categories.
- Simple data and AI Context projections can stay compact.
- Fine-grained review/conflict/supersession becomes possible.
- S2 must define assertion identity/addressability, canonical placement and
  reference integrity.
- Implementations bear moderate complexity rather than either extreme.

Provenance, Confidence and Review are first-class capabilities under this
contract. They are not Entity kinds, and acceptance does not require every
occurrence to have independent identity.

## Remains open

Identifier syntax, which claims require independent identity, exact serialized
envelope, placement, deduplication, Concept–Representation predicate/shortcut
and lifecycle targeting are not decided here.
