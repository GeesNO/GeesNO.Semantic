# Core JSON Schema

GeesNO.Semantic defines an abstract semantic information model independently
of any particular serialization or validation technology.

JSON and JSON Schema provide the initial reference representation and
structural validation route. They do not define the universal semantic model.

```text
Concept
!= Representation

semantic specification
!= serialization

JSON Schema
!= semantic authority

schema-valid
!= complete conformance
```

## Core Schema 0.1

The Core JSON Schema is maintained under:

- [`v0.1/`](v0.1/README.md)

The corresponding machine-readable schema is:

- [`v0.1/geesno-semantic.schema.json`](v0.1/geesno-semantic.schema.json)

It uses JSON Schema Draft 2020-12 and expresses the supported structural
constraints of the GeesNO.Semantic Core 0.1 representation.

The schema implements the applicable requirements established by the
normative Core specification and accepted architectural decisions,
including ADR-0009 through ADR-0016.

Those decisions cover:

- semantic identifiers and references;
- qualified terms and namespace handling;
- assertion placement;
- value and unit representations;
- Source and Binding distinctions;
- lifecycle and semantic-integrity constraints.

The applicable specifications and accepted ADRs remain authoritative.
The schema is derived validation support, not an independent source of
semantic rules.

## Structural and Semantic Validation

JSON Schema validates supported structural representation constraints.

Other deterministic checks remain necessary for semantic integrity
and complete Core conformance.

The repository provides corresponding semantic-validation tooling
and conformance fixtures independently of any particular SDK.

A conforming implementation must apply the relevant normative
requirements rather than relying exclusively on successful JSON
Schema validation.

## Offline and Implementation Independence

Core validation does not require:

- a cloud service;
- an AI provider or language model;
- a central registry or resolver;
- runtime dereferencing of semantic identifiers;
- a particular SDK or application;
- GeesNO.Core.

GeesNO.Semantic remains descriptive, non-executable and usable offline.

## Authority and Documentation

The public architectural and normative references are:

- [Architecture](../ARCHITECTURE.md)
- [Core Specification](../spec/semantic-core.md)
- [Conformance Specification](../spec/conformance.md)
- [Accepted ADRs](../adr/README.md)
- [Conformance Guide](../docs/conformance-guide.md)
- [Public Preview](../PUBLIC_PREVIEW.md)

The schema edition and the repository release version are distinct.
Availability of Core schema `0.1` does not itself assert publication of
a stable `1.0` standard or certification of an implementation.
