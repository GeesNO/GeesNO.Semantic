# GeesNO.Semantic Public Preview

GeesNO.Semantic is preparing its first public preview:

`0.1.0-preview.1`

This document defines the intended scope and claim boundary of that preview. It is non-normative and does not itself publish a release, create certification or change GeesNO.Semantic semantics.

## Pre-1.0 status

GeesNO.Semantic remains pre-1.0.

The public preview is intended to provide an externally implementable baseline while allowing explicitly versioned change before stable `1.0`.

```text
public preview
!= stable 1.0
!= compatibility promise for all future versions
```

Breaking changes may occur before 1.0. Normative changes must remain explicit, documented and versioned.

The reference SDK is non-normative and does not define the standard or promise a stable implementation API.

## Preview scope

The planned preview includes:

- the universal semantic Core;
- JSON `0.1` serialization and schema;
- semantic identity and reference rules;
- Entity, Concept and Representation semantics;
- Source and Binding semantics;
- assertions, values, units and relations;
- Provenance, Confidence and Review;
- Revision, Change and lifecycle semantics;
- inert Extensions;
- Vocabulary architecture;
- the initial GeesNO Base Vocabulary;
- the optional AI Context Profile;
- AI Context Profile and Projection JSON binding;
- AI Context assessment-result JSON binding;
- deterministic offline conformance material;
- cross-domain examples;
- reproducibility benchmark material;
- a non-normative reference SDK;
- implementation and conformance guidance.

The architectural baseline is defined in [ARCHITECTURE.md](ARCHITECTURE.md).

Detailed normative semantics are defined by the applicable specifications and Accepted ADRs.

## Release identity

The planned first preview version is:

```text
0.1.0-preview.1
```

Until the corresponding versioned release is published, this identifier describes the planned preview rather than an already released distribution.

Individual semantic contracts may use their own exact versions independently from the repository release version.

For example, a SemanticDocument may declare:

```text
spec_version = 0.1.0
```

without implying that the repository itself has published a stable `0.1.0` release.

```text
semantic contract version
!= repository release version
```

## Exact conformance claims

A conformance claim must identify the exact assessed subject and the exact applicable contract.

A valid claim must be based on the deterministic conformance process defined for that contract.

Examples of appropriately bounded claims include:

```text
Conforms to GeesNO.Semantic spec_version 0.1.0
```

when the exact SemanticDocument has passed all applicable Core conformance requirements.

For the AI Context Profile:

```text
Conforms to AI Context Profile
https://geesno.com/profile/ai-context
exact edition 0.1.0
```

is appropriate only for the exact assessed subject whose applicable assessment establishes a `conformant` result for that exact Profile edition.

A conformance claim must not silently broaden:

- from one artifact to an entire product;
- from one exact version to unspecified versions;
- from one Profile edition to another edition;
- from schema validity to complete semantic conformance.

```text
schema-valid
!= complete semantic conformance

artifact conformance
!= product-wide conformance
```

## Conformance is not certification

Repository conformance tooling supports bounded technical assessment.

It does not create:

- certification;
- endorsement;
- an approved-implementation status;
- a certification badge;
- permission to use a certification mark.

```text
conformance
!= certification

passing repository conformance tests
!= official certification

reference SDK behavior
!= certification
```

No certification program is established by this preview.

## Name and trademark boundary

The repository's open licenses do not grant trademark rights in:

- `GeesNO`;
- `GeesNO.Semantic`;
- project logos or visual identity;
- future official certification or conformance marks.

See [TRADEMARKS.md](TRADEMARKS.md) for the applicable repository policy.

Trademark policy is separate from semantic conformance and from the copyright licenses applied to repository material.

## Namespace and offline behavior

Published GeesNO.Semantic identifiers use the stable semantic namespace:

```text
https://geesno.com/
```

These identifiers establish semantic identity where the corresponding specification assigns that role.

They do not require runtime dereferencing.

```text
semantic identity URL
!= required network resource
!= retrieval instruction
```

Conforming implementations must be able to use exact locally supplied artifacts and exact locally supported semantics without requiring:

- network access;
- registry lookup;
- automatic Profile download;
- automatic Vocabulary download;
- remote resolver services;
- model invocation.

Web resources under `geesno.com` may provide documentation, discovery or published representations without becoming a runtime dependency of the semantic standard.

## Implementation independence

The preview is intended to be implementable independently from the reference SDK.

A conforming implementation may use any programming language, software stack, storage system or deployment model provided that it preserves the applicable normative contracts.

```text
reference implementation
!= normative authority
```

Adapters, execution systems and product integrations may consume GeesNO.Semantic but remain outside the universal semantic layer unless explicitly standardized by a future architectural decision.

## Public documentation

Related public material includes:

- [Architecture](ARCHITECTURE.md)
- [Documentation Map](docs/README.md)
- [Specifications](spec/README.md)
- [ADR index](adr/README.md)
- [Implementation Guide](docs/implementation-guide.md)
- [Conformance Guide](docs/conformance-guide.md)
- [License applicability](LICENSES.md)
- [Contribution policy](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Release notes](RELEASE_NOTES.md)
- [Roadmap](ROADMAP.md)

This document describes the preview boundary. It does not override normative specifications or Accepted ADRs.
