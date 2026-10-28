# GeesNO.Semantic

GeesNO.Semantic is an open, universal and descriptive semantic standard. It
describes what information exists, what it means, how it relates, where it
originates, and the provenance, confidence, review and lifecycle context around
it.

The standard is software-neutral, format-neutral, domain-neutral and
AI-provider-neutral. It is designed for deterministic, offline-capable use by
conventional software and AI systems.

## Scope

GeesNO.Semantic covers semantic identity, concepts and representations,
assertions, values, provenance, confidence, review, sources, bindings,
lifecycle context, vocabularies, extensions and exact Profile contracts.

It is not an execution runtime, agent framework, workflow engine, tool-calling
protocol or application-control API. It is independent of GeesNO.Core and does
not define application execution semantics:

```text
GeesNO.Semantic = understanding / meaning / context
GeesNO.Core     = operations / capabilities / execution / traceability
```

Published GeesNO.Semantic namespace identifiers use `https://geesno.com/` as a
stable identity authority. These identifiers are not retrieval instructions:
conforming processing does not require network access or automatic
dereferencing.

## Architecture

```text
Universal Core
    -> serialization-independent semantic concepts

JSON serialization + schema
    -> reference representation and structural validation

Vocabularies + Extensions
    -> qualified domain or organization meaning outside the universal Core

Profiles
    -> exact, versioned requirements and projections for a defined use case

Conformance
    -> deterministic assessment against an exact contract

Reference SDK
    -> optional, non-normative implementation support
```

These layers do not replace one another:

```text
Concept != Representation
semantic identity != representation != source locator
Source != Entity
Binding != semantic truth
Profile != Core != Vocabulary
IRI != retrieval instruction
schema validation != complete conformance
validation/conformance != certification
SDK behavior != normative authority
```

## Implement GeesNO.Semantic

1. Use the [Documentation Map](docs/README.md) to identify authoritative and
   explanatory material.
2. Read the [Core specification index](spec/README.md) and the
   [abstract Core model](spec/semantic-core.md).
3. Follow the [JSON serialization specification](spec/json-serialization.md)
   and the [JSON Schema for `spec_version` `0.1.0`](schema/v0.1/geesno-semantic.schema.json).
4. Use [Vocabulary and Extension guidance](vocab/README.md) for qualified
   meaning outside the universal Core.
5. For AI projection use cases, read the optional
   [AI Context Profile](profiles/ai-context/README.md).
6. Validate artifacts with the [conformance suite](conformance/README.md) and
   the [Conformance Guide](docs/conformance-guide.md).
7. Study the [cross-domain examples](examples/cross-domain/public-preview/README.md).
8. Optionally use the [reference SDK](sdk/README.md); it does not define the
   standard.

The language-neutral [Implementation Guide](docs/implementation-guide.md)
provides a producer and consumer route without requiring the Python SDK.

## Repository Map

| Area | Purpose |
| --- | --- |
| [`spec/`](spec/README.md) | Core, serialization, Profile and conformance specifications |
| [`schema/`](schema/README.md) | Core JSON Schema artifacts |
| [`vocab/`](vocab/README.md) | Base Vocabulary and extension guidance |
| [`profiles/ai-context/`](profiles/ai-context/README.md) | AI Context Profile, schemas and conformance material |
| [`conformance/`](conformance/README.md) | Deterministic Core fixtures and runner |
| [`examples/`](examples/cross-domain/public-preview/README.md) | Non-normative cross-domain learning examples |
| [`sdk/`](sdk/README.md) | Non-normative reference SDK |
| [`docs/`](docs/README.md) | Public implementation and conformance navigation |

## Current Status

This source distribution is preparing its first pre-1.0 Public Preview,
`0.1.0-preview.1`. Until the corresponding release tag and GitHub Release exist,
this distribution remains development state. The project remains on the `0.x`
line, where documented breaking changes are possible.

See [Public Preview Status](PUBLIC_PREVIEW.md) and the draft
[release notes](RELEASE_NOTES.md) for the exact current boundary.

## Licensing

Human-readable specifications and documentation are licensed under
[CC BY 4.0](LICENSE-SPECIFICATION). Code, schemas, tests, fixtures and other
implementation artifacts are licensed under
[Apache-2.0](LICENSE-CODE). The detailed functional allocation is in
[LICENSES.md](LICENSES.md).

The licensor and copyright holder is `GENARO ESCUDERO NOGALES`.

## Contributing and Security

Read [CONTRIBUTING.md](CONTRIBUTING.md) before proposing changes. Normative
changes follow the repository's specification-first governance and cannot be
created by an SDK, schema, fixture or passing test alone.

Potential vulnerabilities must not be disclosed through public issues. Follow
[SECURITY.md](SECURITY.md) for the current reporting instructions before
sharing sensitive details.

This repository does not establish a certification program or grant trademark
rights beyond the applicable license terms.
