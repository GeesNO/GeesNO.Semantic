# Draft Release Notes — GeesNO.Semantic 0.1.0-preview.1

These are draft release notes for the planned first pre-1.0 Public Preview of GeesNO.Semantic.

The preview has not yet been released.

## Included in the planned preview

The planned preview includes:

- the serialization-independent universal Core specification;
- JSON `0.1` serialization and Draft 2020-12 schemas;
- explicit identity and reference semantics;
- Source and Binding semantics;
- assertions, values, units and relations;
- Provenance, Confidence and Review semantics;
- Revision, Change and lifecycle semantics;
- inert Extensions;
- Vocabulary architecture and the initial GeesNO Base Vocabulary;
- the optional AI Context Profile `0.1.0`;
- AI Context Profile and Projection JSON binding;
- AI Context assessment-result JSON binding;
- deterministic conformance fixtures and offline validation tooling;
- cross-domain examples;
- reproducibility benchmark material;
- a non-normative Python reference SDK distributed as repository source;
- implementation and conformance guidance.

## Architectural boundary

GeesNO.Semantic remains:

- software-neutral;
- format-neutral;
- domain-neutral;
- AI-provider-neutral;
- descriptive rather than executable.

Neither the semantic standard nor its deterministic validation paths require:

- a cloud service;
- a network resolver;
- a model provider;
- runtime dereferencing of `geesno.com` identifiers.

```text
semantic identity
!= network dependency
```

## Pre-1.0 status

`0.1.0-preview.1` is a pre-1.0 preview.

It does not promise compatibility with a future stable `1.0`.

Normative changes before 1.0 remain possible and must be explicit, documented and versioned.

The reference SDK is non-normative and does not define GeesNO.Semantic semantics.

## Conformance and certification

The repository includes deterministic conformance material for supported contracts.

Passing an applicable conformance route supports only the bounded technical claim defined by that exact contract and assessed subject.

```text
conformance
!= certification
```

This preview does not establish a certification program or official certification mark.

## Feedback and security

Contribution requirements are documented in [CONTRIBUTING.md](CONTRIBUTING.md). A public contribution endpoint is not established by this source distribution.

The versioned Public Preview is not finalized. This source distribution does not publish a release.

Suspected vulnerabilities must follow [SECURITY.md](SECURITY.md) and must not be disclosed through a public issue or other public repository content.

## Distribution

No package-registry release is planned for this preview.

The intended distribution surfaces are:

- the public source repository;
- versioned source archives;
- human-readable specifications;
- schemas and machine-readable semantic artifacts;
- conformance material;
- examples;
- benchmark material;
- reference SDK source.

See [PUBLIC_PREVIEW.md](PUBLIC_PREVIEW.md) for the preview scope and claim boundary.
