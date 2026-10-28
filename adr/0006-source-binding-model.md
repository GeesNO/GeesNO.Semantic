# ADR-0006: Layered Source and Binding model

- **Status:** Accepted
- **Date:** 2026-08-30
- **Accepted by:** Explicit human architecture decision, 2026-08-30
- **Scope:** Abstract Source/Binding contract only; exact shape remains open

## Context

Native correlation must support records, regions, ranges, symbols, keys,
resources and temporal segments without importing one domain's locator fields.
A totally opaque payload, however, leaves no shared correlation or trust
semantics.

## Decision

1. Source is a separately referenceable origin context.
2. Binding correlates exactly one Entity with exactly one Source context.
3. Binding is optional and plural for Concept and Representation.
4. Binding provides a common conceptual envelope for locator kind/payload,
   correlation state/method, Provenance, Confidence, Review, lifecycle and
   Extensions.
5. Locator details are qualified/extensible rather than a fixed universal field
   list.
6. A source-level Binding may omit a narrower locator.
7. Exact shape, namespace syntax and locator vocabularies remain open.
8. A locator has meaning only within its Source context.
9. Binding does not prove semantic truth, grant permissions, trigger
   dereferencing or execute behavior.
10. Profiles may restrict locator families without changing universal core.

## Consequences

- Concepts can remain purely semantic and Representations can be incrementally
  bound.
- Native identity never becomes semantic identity.
- Common trust/lifecycle semantics are interoperable across locator families.
- S2/S3 must define qualified locator preservation and resolution constraints.
- Profiles can require particular locator families without changing core.

## Remains open

Source/global identity syntax, Binding identity, incomplete/unresolved state
vocabulary, exact payload shape, cross-source compound locators and external
dereference behavior beyond the closed no-automatic-dereference rule.
