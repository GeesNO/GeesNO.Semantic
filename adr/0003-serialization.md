# ADR-0003: Serialization-independent model with an initial JSON route

- **Status:** Accepted (records Foundation decisions)
- **Date:** 2026-08-30
- **Source:** `PROJECT_FOUNDATION.md` sections 4.9, 4.10, 9, 19 and 24

## Context

Interoperability needs a machine-validatable reference representation, while a
universal semantic model must not be shaped by one programming language or
wire format.

## Decision

The abstract semantic model is serialization-independent. The initial reference
serialization/validation route will be UTF-8 JSON plus JSON Schema. Development
order is conceptual model, specification, schema/formal constraints,
conformance tests and only then non-normative SDK/tooling. Future mappings must
represent the same abstract model rather than create incompatible semantics.

## Consequences

- The Python SDK cannot become the specification.
- S0/S1 examples must not accidentally freeze JSON object shapes.
- Exact canonical JSON, identifiers, namespaces, units and binding/assertion
  encodings remain open and require later ADRs.
- Other serializations can be explored after demonstrated need without changing
  core meaning.

