# GeesNO.Semantic Specifications

This directory contains the human-readable specifications that define GeesNO.Semantic semantics and its accepted representation contracts.

For the external reading route, start with the [Documentation Map](../docs/README.md).

For the project-wide architectural baseline, read [ARCHITECTURE.md](../ARCHITECTURE.md) and the [Accepted ADR index](../adr/README.md).

The [Implementation Guide](../docs/implementation-guide.md) and [Conformance Guide](../docs/conformance-guide.md) are non-normative guidance derived from the authoritative material in this repository.

## Authority and reading order

GeesNO.Semantic separates architecture, normative specification, representation constraints, conformance material and implementation guidance.

```text
ARCHITECTURE.md
+ Accepted ADRs
        ↓
normative specifications
        ↓
normative representation artifacts where explicitly assigned
        ↓
deterministic conformance material
        ↓
reference SDK, examples and explanatory documentation
```

A lower layer must not create semantic rules absent from accepted architecture and normative specification.

In particular:

```text
schema != complete semantic authority

schema-valid
!= automatically semantically conformant

reference SDK behavior
!= normative semantics
```

## Specification navigation

| Topic | Entry |
| --- | --- |
| Universal Core | [semantic-core.md](semantic-core.md) |
| Identity and references | [identity.md](identity.md) and [json-identifiers-and-references.md](json-identifiers-and-references.md) |
| Entity / Concept / Representation | [entities.md](entities.md) |
| Source and Binding | [source-bindings.md](source-bindings.md) |
| Assertions | [assertions.md](assertions.md) |
| Properties, values and units | [properties.md](properties.md) and [values-and-units.md](values-and-units.md) |
| Relations | [relations.md](relations.md) |
| Provenance, Confidence and Review | [provenance.md](provenance.md) |
| Revision and Change | [revisions.md](revisions.md) |
| Extensions | [extensions.md](extensions.md) |
| JSON serialization | [json-serialization.md](json-serialization.md) |
| JSON qualified terms | [json-qualified-terms.md](json-qualified-terms.md) |
| JSON assertions | [json-assertion-placement.md](json-assertion-placement.md) |
| JSON values and units | [json-values-and-units.md](json-values-and-units.md) |
| JSON Source and Binding | [json-source-bindings.md](json-source-bindings.md) |
| JSON lifecycle | [json-lifecycle.md](json-lifecycle.md) |
| Core conformance | [conformance.md](conformance.md) and [conformance suite](../conformance/README.md) |
| AI Context Profile | [ai-context-profile.md](ai-context-profile.md) |
| AI Context Profile / Projection JSON binding | [ai-context-json-binding.md](ai-context-json-binding.md) |
| AI Context assessment-result JSON binding | [ai-context-assessment-json-binding.md](ai-context-assessment-json-binding.md) |

## Universal Core

The serialization-independent Core is defined primarily by:

- [semantic-core.md](semantic-core.md) — integrated universal model and invariants;
- [model-cardinalities.md](model-cardinalities.md) — responsibility and cardinality matrix;
- [identity.md](identity.md) — semantic identity and reference semantics;
- [entities.md](entities.md) — Entity, Concept and Representation;
- [source-bindings.md](source-bindings.md) — Source, Binding and source-location boundaries;
- [assertions.md](assertions.md) — semantic assertions and their identity;
- [properties.md](properties.md) — property semantics;
- [values-and-units.md](values-and-units.md) — values, datatypes and measured quantities;
- [relations.md](relations.md) — qualified semantic relationships;
- [provenance.md](provenance.md) — Provenance, Confidence and Review;
- [revisions.md](revisions.md) — Revision, Change and lifecycle semantics;
- [extensions.md](extensions.md) — inert extension boundaries;
- [conformance.md](conformance.md) — Core conformance requirements.

The Core remains universal and domain-neutral.

```text
Core
!= domain ontology
!= application object model
!= execution framework
```

Domain, organization and application meaning should normally be expressed through explicit Vocabularies, Profiles or external integration layers rather than by expanding the universal Core.

## Fundamental distinctions

The specifications preserve these architectural distinctions:

```text
Concept != Representation

semantic identity
!= representation
!= locator

Source != Entity

Binding != semantic truth

Profile != Core != Vocabulary

Projection != source mutation

Extension != executable instruction

IRI != retrieval instruction
```

Implementations must preserve these distinctions even when their internal object models use different terminology.

## JSON serialization

The initial reference serialization is JSON.

The normative JSON material includes:

- [json-serialization.md](json-serialization.md) — overall JSON representation;
- [json-identifiers-and-references.md](json-identifiers-and-references.md) — identifiers and references;
- [json-qualified-terms.md](json-qualified-terms.md) — qualified terms and namespace expansion;
- [json-values-and-units.md](json-values-and-units.md) — values, exact numeric representation, collections and measured quantities;
- [json-assertion-placement.md](json-assertion-placement.md) — assertion placement and addressability;
- [json-source-bindings.md](json-source-bindings.md) — Source, Binding and locator representation;
- [json-lifecycle.md](json-lifecycle.md) — scope, completeness, Revision, Change and tombstones.

The corresponding Core JSON Schema is published under:

[`schema/v0.1/geesno-semantic.schema.json`](../schema/v0.1/geesno-semantic.schema.json)

JSON is a representation of the semantic model, not the definition of the model itself.

```text
semantic model
!= JSON
!= JSON Schema
```

Future serializations may represent the same accepted semantics without changing the universal Core merely because their syntax differs.

## Identity and resolution

Identity and retrieval remain separate concerns.

An IRI may identify an exact semantic family, edition or artifact without requiring network dereferencing.

```text
identity
!= locator

IRI
!= fetch command
```

GeesNO.Semantic processing must remain possible from explicit locally supplied artifacts and exact locally supported semantics.

The standard does not require automatic:

- registry lookup;
- network retrieval;
- latest-version discovery;
- version substitution;
- resolver invocation.

## Vocabularies

Vocabulary architecture is defined by the accepted Vocabulary ADRs and corresponding repository material under [`vocab/`](../vocab/README.md).

Vocabularies provide qualified semantic terms without expanding the universal Core.

Vocabulary family, edition and term identity remain explicit.

Matching labels, similar terms, namespace prefixes or newer-looking versions do not automatically establish equivalence or compatibility.

The initial GeesNO Base Vocabulary is published under:

[`vocab/base/`](../vocab/base/README.md)

with family identity:

```text
https://geesno.com/vocab/base
```

Vocabulary discovery does not itself establish semantic authority.

## Profiles

Profiles define exact, versioned semantic requirements for identified use cases.

Profiles remain distinct from Core and Vocabulary semantics.

```text
Profile != Core
Profile != Vocabulary
Profile requirement != execution instruction
```

A Profile edition is an exact normative requirement set.

Implementations must not silently substitute:

- `latest`;
- version ranges;
- newer-looking editions;
- structurally similar editions;
- inferred-compatible editions.

The first Profile family provided by this repository is the optional AI Context Profile.

Its repository entry point is:

[`profiles/ai-context/README.md`](../profiles/ai-context/README.md)

## AI Context Profile

The abstract AI Context Profile and Projection semantics are defined by:

[ai-context-profile.md](ai-context-profile.md)

The exact Profile edition is published at:

[`profiles/ai-context/v0.1/profile.json`](../profiles/ai-context/v0.1/profile.json)

The Profile and Projection JSON binding is defined by:

[ai-context-json-binding.md](ai-context-json-binding.md)

and represented structurally by:

[`profiles/ai-context/schema/v0.1/ai-context.schema.json`](../profiles/ai-context/schema/v0.1/ai-context.schema.json)

AI Context remains semantic context, not execution behavior.

It does not define:

- model invocation;
- prompt execution;
- tool calls;
- agent workflow;
- provider-specific runtime behavior;
- automatic retrieval;
- source mutation.

## AI Context assessment results

Assessment-result representation is separate from Profile/Projection representation.

The assessment-result JSON binding is defined by:

[ai-context-assessment-json-binding.md](ai-context-assessment-json-binding.md)

Its structural schema is:

[`profiles/ai-context/schema/v0.1/ai-context-assessment.schema.json`](../profiles/ai-context/schema/v0.1/ai-context-assessment.schema.json)

A conformance result reports an assessment. It is not semantic truth, a Review record, execution authorization or mutation of the assessed subject.

```text
conformance result
!= semantic truth
!= Review
!= permission
!= execution authorization
```

The assessment machinery distinguishes established conformance, established non-conformance and cases where conformance cannot be concluded from the available exact local material.

## Projection semantics

A Projection selects semantic context without redefining or mutating the source semantic document.

Projection semantics include explicit rules for:

- selection;
- omission;
- boundedness;
- continuation;
- preservation;
- material context;
- exact Profile requirements.

A partial Projection is not automatically non-conformant.

A complete Projection is not automatically conformant.

```text
Projection completeness
!= Profile conformance
```

## Profile composition

Multiple Profile references do not automatically form a composite Profile.

```text
multiple Profile references
!= merged Profile

multiple assessments
!= composite conformance
```

Where composition is defined, component editions, resolved requirements, provenance and conflict handling must remain explicit and reproducible.

Profile composition must not depend on array order, model judgment, semantic similarity, hidden precedence or automatic remote resolution.

## Extensions

Extensions are inert semantic material.

They allow additional information to be carried without silently modifying Core semantics.

An Extension must not become a mechanism for:

- hidden execution;
- application commands;
- provider-specific control;
- undeclared Core replacement.

Unknown extension material remains distinguishable from accepted Core semantics.

## Conformance

Core conformance is defined by [conformance.md](conformance.md) and exercised through the repository-local conformance suite under [`conformance/`](../conformance/README.md).

AI Context Profile conformance material is published under:

- [`profiles/ai-context/conformance/v0.1/`](../profiles/ai-context/conformance/v0.1/README.md)
- [`profiles/ai-context/assessment-conformance/v0.1/`](../profiles/ai-context/assessment-conformance/v0.1/README.md)
- [AI Context assessment corpus catalogue](../conformance/ai-context-assessment-corpus.md)

Conformance assessment is deterministic and offline-capable for the exact supported contracts.

Schema validation is one validation layer only.

```text
schema-valid
!= complete semantic conformance
```

Reference validation tooling may automate accepted rules, but tooling does not create those rules.

## Schemas

Machine-readable schemas are published under:

- [`schema/`](../schema/README.md) for Core representation;
- [`profiles/ai-context/schema/`](../profiles/ai-context/schema/README.md) for AI Context artifacts.

A schema may constrain an accepted representation.

A schema must not invent semantic meaning, normative fields or normative tokens absent from accepted architecture and specification.

## Conformance fixtures and examples

Conformance fixtures have explicit expected outcomes and form part of deterministic validation routes where the corresponding specification assigns them that role.

Examples are different.

Examples illustrate existing semantics and are non-normative unless explicitly identified as conformance fixtures.

See:

- [Core conformance](../conformance/README.md)
- [Examples](../examples/README.md)
- [Cross-domain examples](../examples/cross-domain/public-preview/README.md)

```text
example != conformance fixture
```

## Reference SDK

The reference SDK is published under [`sdk/`](../sdk/README.md).

It is optional and non-normative.

The current reference implementation may provide convenient parsing, validation, construction and query APIs, but those APIs do not define GeesNO.Semantic semantics.

Other languages and independent implementations may implement the same contracts without using the reference SDK.

## Offline behavior

The semantic standard is designed to remain usable without network access.

Conforming interpretation and assessment must not require:

- automatic Profile download;
- automatic Vocabulary download;
- registry access;
- remote resolver services;
- model invocation;
- external arbitration.

When required exact semantic material is unavailable locally, that condition is handled explicitly rather than by silent substitution.

## Versioning

Normative contracts use explicit editions or versions.

Changes to accepted semantic or representational contracts require explicit versioned change.

Compatibility must not be inferred solely from:

- version ordering;
- structural similarity;
- matching labels;
- implementation convenience.

The repository's release version and the version of an individual semantic contract are separate concepts.

## Implementer reading route

A new implementation should normally proceed in this order:

1. [ARCHITECTURE.md](../ARCHITECTURE.md)
2. [ADR index](../adr/README.md)
3. [semantic-core.md](semantic-core.md)
4. the applicable topic specifications in this directory
5. [json-serialization.md](json-serialization.md), if implementing the JSON representation
6. the applicable exact schema
7. [conformance.md](conformance.md) and the corresponding conformance suite
8. the exact Vocabulary or Profile specifications required by the use case
9. the non-normative [Implementation Guide](../docs/implementation-guide.md)
10. optionally, the non-normative [reference SDK](../sdk/README.md)

The semantic contract must remain independently implementable from the specifications and explicit artifacts in this repository.
