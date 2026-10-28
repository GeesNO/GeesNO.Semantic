# Open Normative Questions

This document records outstanding normative and interoperability
questions for future GeesNO.Semantic development.

It distinguishes accepted architectural decisions from areas
where additional specifications, bindings, interoperability
evidence or governance decisions may be required.

This register is informative. It does not introduce normative
requirements, override accepted ADRs or authorize changes to
existing Core, Vocabulary or Profile contracts.

## Authority and Scope

The public architectural baseline is
[ARCHITECTURE.md](../ARCHITECTURE.md).

Accepted ADRs and applicable normative specifications define
the established contracts.

This register identifies future work without treating
unresolved matters as implemented or standardized behavior.

```text
open question
!= accepted normative requirement

accepted architecture
!= implemented publication binding

schema-valid
!= complete conformance

SDK implementation
!= semantic authority
```

The universal Core remains descriptive, non-executable,
software-independent, format-independent, domain-independent,
AI-provider-neutral and usable offline.

## Established Architectural Decisions

The following areas have accepted architectural decisions
and must not be reopened implicitly through future tooling
or representation choices.

| Area | Established authority | Boundary |
| --- | --- | --- |
| Semantic identifiers and references | ADR-0009, ADR-0016 | Stable identity is separate from representation, locator and retrieval. |
| Qualified terms and namespace expansion | ADR-0010, ADR-0016 | Explicit namespace semantics remain independent of automatic discovery. |
| Assertion placement | ADR-0005, ADR-0011 | Serialized assertions use the established top-level collection and explicit identities. |
| Values and measured quantities | ADR-0012, ADR-0016 | Existing Core value and unit representation is established. |
| Source and Binding | ADR-0013, ADR-0016 | Source, Binding, Entity and semantic Assertion remain distinct. |
| Lifecycle | ADR-0007, ADR-0014, ADR-0016 | State-first, history-optional representation is established. |
| Extensions | ADR-0015, ADR-0016 | Extensions remain inert; existing representation and validation rules apply. |
| Core validation | ADR-0016 | Deterministic Layers 0-3 and their established boundaries remain applicable. |
| Vocabulary architecture | ADR-0017 through ADR-0021 | Identity, versioning, publication, lifecycle, authoring, discovery and governance have accepted abstract contracts. |
| Base Vocabulary | ADR-0022 | Identity, initial edition and two experimental terms are established. |
| Compatibility architecture | ADR-0023 | Abstract attributed compatibility claims have an accepted model. |
| AI Context | ADR-0024 through ADR-0029 | Applicable Profile, preservation, Projection and JSON binding decisions are established. |
| AI Context assessment | ADR-0030 | Assessment-result and diagnostics architecture is established. |
| Profile composition | ADR-0031 | Abstract composition and conflict-policy architecture is established. |

Acceptance of an abstract contract does not imply that every
possible concrete binding, publication artifact, integration
mechanism or operational implementation exists.

## Core and Cross-Document Semantics

### Identifier and Reference Interoperability

The established identifier and reference contracts remain
authoritative.

Potential future interoperability work includes:

- cross-document packaging conventions;
- optional discovery and resolution diagnostics;
- diagnostics for partially available reference graphs;
- reference availability reporting beyond existing exact
  binding contracts.

These questions do not authorize automatic dereferencing,
implicit network access or changes to identity semantics.

### Assertion and Association Patterns

Areas for future investigation include:

- multiple Confidence calibration and aggregation models;
- Review vocabulary, authority and transition semantics;
- n-ary relation Vocabulary and Profile patterns;
- specialized cross-document association conventions.

No automatic Confidence aggregation, Review voting or new
Core assertion category follows from these questions.

## Source and Binding

The Source and Binding model is already established by
the accepted Core contracts.

Potential subordinate work includes:

- lifecycle vocabularies for Source-description changes;
- Binding locator correction and staleness conventions;
- locator, location, revision, fingerprint and method terms;
- specialized Profile requirements for Source and Binding;
- diagnostics for unavailable Sources or unresolved locators.

These mechanisms must remain distinct from semantic
Binding state.

Future vocabularies may qualify Source and Binding concepts,
but must not replace their Core identities or introduce
automatic semantic Assertions.

## Values, Measurements and Extensions

The Core value representation and Extension mechanics are
already established.

Future work may investigate:

- significant figures and measurement precision;
- measurement uncertainty representations;
- repeated-value versus aggregate-value Profile constraints;
- specialized Vocabulary constraints;
- additional interoperability evidence for loss-aware
  representation handling.

Future work must preserve the accepted distinctions between
lexical representation and semantic value.

Unknown Extension data remains subject to the established
loss-aware representation and inertness boundaries.

## Vocabulary Publication and Discovery

The Vocabulary architecture is accepted through
ADR-0017 to ADR-0023.

The following concrete matters remain potential future work:

- machine-readable Vocabulary publication bindings;
- publication schema and media-type choices;
- term-definition constraint-language selection;
- optional catalog or discovery bindings;
- publication integrity and authenticity mechanisms;
- compatibility-claim representations and diagnostics;
- governance procedures for independently maintained
  Vocabulary families.

The abstract discovery architecture is optional and
offline-safe.

No global registry, remote resolver, automatic Vocabulary
edition selection or network fetch is required.

### Base Vocabulary

ADR-0022 establishes:

| Property | Established value |
| --- | --- |
| Family identity | `https://geesno.com/vocab/base` |
| Initial version | `0.1.0` |
| Expansion base | `https://geesno.com/vocab/base/` |
| Preferred prefix | `gbase` |
| Initial terms | `label`, `description` |
| Initial term lifecycle | `experimental` |

A machine-readable Base Vocabulary publication artifact
has not yet been provided by the repository.

The absence of such an artifact does not invalidate
Bare-Core documents or create a mandatory network dependency.

The accepted term meanings remain governed by ADR-0022.

## Cross-Vocabulary Compatibility

ADR-0023 establishes the abstract compatibility model for
attributed claims concerning:

- semantic equivalence;
- mapping and correspondence;
- substitutability;
- edition compatibility;
- Profile acceptability;
- migration correspondence.

Outstanding concrete questions include:

- compatibility-claim serialization;
- Profile requirement-set representations where applicable;
- diagnostic and integrity-evidence bindings;
- selection of optional mapping or constraint languages;
- interoperable expressions of compatibility ranges.

These questions do not create a reasoner, AI matcher,
automatic equivalence mechanism, resolver or migration engine.

Executable migrations, if developed by external software,
remain outside the descriptive GeesNO.Semantic Core.

## AI Context and Profile Interoperability

The established AI Context Profile, Projection and
assessment-result contracts remain authoritative.

Future work may investigate:

- composition-specific diagnostic representations;
- exact binding and grammar for composite Profile artifacts;
- interoperability conventions for multiple Profile editions;
- additional Profile-level cardinality and completeness rules;
- richer non-normative diagnostic presentation;
- public SDK API stabilization.

Profile composition is architecturally distinct from
the identity and semantics of an individual exact Profile
edition.

```text
Profile declaration
!= proof of Profile conformance

Projection
!= source mutation

Projection
!= new semantic truth
```

Future implementation choices must not silently expand
the existing AI Context binding contracts.

## Conformance and Diagnostics

The existing deterministic Core conformance boundaries
and exact AI Context Profile/assessment contracts are
established.

Potential future work includes:

- additional progressive conformance Profiles;
- cross-document diagnostic conventions;
- specialized domain- and Vocabulary-aware validation;
- richer, interoperable diagnostic taxonomies;
- integrity evidence for conformance claims;
- reproducible implementation interoperability testing.

A schema or SDK must not originate semantic rules.

Conformance and certification are separate concepts.

No certification program is established by this register.

## Lifecycle and Historical State

The accepted state-first lifecycle model is established by
ADR-0007, ADR-0014 and ADR-0016.

Potential subordinate work includes:

- qualified scope and lifecycle Vocabularies;
- specialized Change and Validity terminology;
- Profile-specific completeness and history requirements;
- retention and history-packaging conventions;
- optional recorded, authored, observed and event timestamp
  terminology and precision;
- diagnostics for partial cross-document histories;
- privacy retention and erasure policies beyond established
  identity and non-disclosure boundaries.

Historical completeness remains scoped and does not imply
the availability of prior snapshots or automatic replay.

Omission and deletion remain distinct.

## Temporal Projection Interpretation

The established semantic model must preserve this distinction:

```text
semantic state asserted at time T
!= guaranteed live operational state at time T+n
```

A Projection containing temporal or mutable information
must be interpreted according to its applicable Provenance,
Validity, Revision and lifecycle context.

A historical assertion or interval-scoped semantic statement
does not automatically establish current operational state.

This boundary does not introduce or require:

- polling;
- subscriptions;
- event streams;
- live telemetry;
- freshness protocols;
- automatic source synchronization;
- a new live-state primitive.

Any future operational mechanism belongs to an explicitly
separate integration or runtime concern.

## Serialization and Integrity

The accepted Core JSON representation distinguishes
semantic requirements from serialization details.

Established lexical and numeric-token preservation rules
must not be confused with cryptographic canonicalization.

Questions remaining for future specification include:

- byte-level canonical JSON rules;
- cryptographic canonicalization;
- digital signatures;
- signature scope and verification evidence;
- integrity threat models;
- interactions between signatures, Profiles and
  representation-preserving transformations.

No signature algorithm or canonical byte representation
is selected by this register.

## Additional Representation Conventions

Potential future interoperability work includes:

- sidecar naming conventions;
- cross-document packaging;
- exact Profile declaration conventions where not already
  fixed by an applicable contract;
- metadata-only document constraints;
- specialized retention and completeness representations.

These matters must be evaluated against the already
accepted Core and Profile contracts.

They do not authorize new implicit schema semantics.

## Governance and Legal Policy

Further governance and legal review may be appropriate
before substantial external contribution or a stable
major-version standard.

Potential subjects include:

- mature patent and contributor policy;
- Vocabulary stewardship and authority delegation;
- long-term compatibility and deprecation governance;
- publication and integrity responsibilities.

Any future changes must follow the applicable project
governance and licensing framework.

This register does not establish a new license,
contributor agreement or certification mechanism.

## Explicitly Outside the Universal Core

The following are not requirements of the universal
GeesNO.Semantic Core:

- application-specific adapters;
- GeesNO.Core runtime functionality;
- automatic tool or prompt execution;
- AI-provider integration;
- retrieval algorithms and vector databases;
- remote registries or resolvers;
- mandatory network services;
- automatic migration execution;
- live operational monitoring;
- certification services.

External consumers may implement their own behavior
without transferring execution responsibilities into
the descriptive semantic standard.

## References

- [Architecture](../ARCHITECTURE.md)
- [Accepted ADRs](../adr/README.md)
- [Specification Index](README.md)
- [Core Specification](semantic-core.md)
- [Conformance Specification](conformance.md)
- [AI Context Profile](ai-context-profile.md)
- [AI Context JSON Binding](ai-context-json-binding.md)
- [AI Context Assessment Binding](ai-context-assessment-json-binding.md)
- [Vocabulary Overview](../vocab/README.md)
- [Base Vocabulary](../vocab/base/README.md)
- [Public Preview](../PUBLIC_PREVIEW.md)
