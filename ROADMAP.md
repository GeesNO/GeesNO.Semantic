# GeesNO.Semantic Roadmap

GeesNO.Semantic is being developed toward a stable, universal semantic standard that remains software-neutral, format-neutral, domain-neutral and AI-provider-neutral.

The architectural baseline is defined in [ARCHITECTURE.md](ARCHITECTURE.md). This roadmap is non-normative and describes intended development direction only.

## Current — Public Preview

The current objective is the first controlled public preview:

`0.1.0-preview.1`

The preview establishes a usable external baseline including:

- the universal semantic Core;
- JSON serialization and schema;
- identity and reference semantics;
- Source and Binding semantics;
- assertions, values, units and relations;
- provenance, confidence and review;
- revision, change and lifecycle semantics;
- inert Extensions;
- Vocabulary architecture and the initial GeesNO Base Vocabulary;
- the AI Context Profile and its JSON bindings;
- deterministic offline conformance material;
- cross-domain examples;
- a non-normative reference SDK;
- implementation and conformance guidance.

The preview is not a promise of 1.0 API or representation stability. Normative changes remain explicitly versioned.

## Next — Interoperability Hardening

After the initial preview, development will focus on validating the standard outside the scenarios that shaped its first implementation.

Priorities include:

- independent implementations;
- additional programming languages;
- unrelated-domain interoperability tests;
- alternative storage and serialization experiments;
- external Vocabulary and Profile authoring;
- round-trip and loss-awareness testing;
- clearer compatibility rules where implementation experience identifies ambiguity;
- broader conformance coverage;
- security and privacy review;
- implementation feedback from external users.

Hardening must not introduce product-, vendor-, file-format- or domain-specific semantics into the universal Core.

## Toward 1.0

A stable `1.0` requires evidence that the architecture can remain unchanged across materially different implementations and domains.

Before 1.0, the project should demonstrate:

- stable universal semantic boundaries;
- deterministic and offline-capable conformance;
- explicit version and compatibility behavior;
- independent implementation feasibility;
- durable Vocabulary and Profile mechanisms;
- clear separation between semantic identity, representation and location;
- no dependency on a particular SDK, runtime, model provider or network service;
- successful cross-domain interoperability;
- documented security, privacy and governance expectations;
- a stable public namespace under `https://geesno.com/`.

The 1.0 standard must remain descriptive rather than executable.

## Beyond 1.0

Post-1.0 work may expand the ecosystem without expanding the universal Core unnecessarily.

Possible areas include:

- additional Vocabularies;
- additional Profiles;
- additional serialization bindings;
- additional language SDKs;
- independent conformance implementations;
- discovery and publication infrastructure;
- governance maturation;
- ecosystem tooling.

Adapters and product-specific integrations belong in separate projects unless a future architectural decision establishes a genuinely universal requirement.

## Architectural constraint

Roadmap work must preserve the central project boundary:

```text
GeesNO.Semantic
= semantic meaning and context

GeesNO.Semantic
!= application runtime
!= execution framework
!= adapter collection
!= proprietary file format
!= domain-specific ontology
```

Roadmap priority never overrides accepted architecture or normative specification.
