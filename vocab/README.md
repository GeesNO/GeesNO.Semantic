# Vocabularies

GeesNO.Semantic Vocabularies provide qualified domain-specific,
organization-specific or community-defined meaning above the
universal semantic Core.

The Core remains deliberately small and does not require GeesNO
to define or control the vocabularies of every domain.

```text
Core
!= Vocabulary

Vocabulary
!= Profile

semantic identity
!= retrieval location

Vocabulary declaration
!= automatic semantic validation
```

Vocabularies extend the available semantic terminology without
changing the structural meaning of the universal Core.

## Vocabulary Architecture

The accepted Vocabulary architecture defines:

- Vocabulary identity and exact versioning;
- publication and machine-readable artifact boundaries;
- term lifecycle and compatibility;
- Extension payload and Vocabulary authoring separation;
- optional discovery, authority and governance;
- the deliberately small GeesNO Base Vocabulary;
- cross-Vocabulary and Profile compatibility conventions.

These architectural decisions are recorded in:

- [ADR-0017 - Vocabulary Identity and Version](../adr/0017-vocabulary-identity-version-model.md)
- [ADR-0018 - Vocabulary Publication Artifact](../adr/0018-vocabulary-publication-artifact.md)
- [ADR-0019 - Vocabulary Term Lifecycle](../adr/0019-vocabulary-term-lifecycle.md)
- [ADR-0020 - Extension and Vocabulary Compatibility](../adr/0020-extension-vocabulary-authoring-payload-compatibility.md)
- [ADR-0021 - Optional Discovery and Governance](../adr/0021-optional-vocabulary-discovery-authority-governance.md)
- [ADR-0022 - GeesNO Base Vocabulary](../adr/0022-geesno-base-vocabulary.md)
- [ADR-0023 - Cross-Vocabulary and Profile Compatibility](../adr/0023-cross-vocabulary-profile-compatibility-model.md)

Accepted ADRs and applicable normative specifications remain
authoritative over this explanatory README.

## GeesNO Base Vocabulary

The accepted Base Vocabulary family has the stable semantic identity:

```text
https://geesno.com/vocab/base
```

Its initial defined version is:

```text
0.1.0
```

Its qualified-term expansion base is:

```text
https://geesno.com/vocab/base/
```

Its preferred prefix is:

```text
gbase
```

The initial experimental terms are:

- `label`
- `description`

These terms provide a deliberately limited initial vocabulary
rather than a general domain ontology.

The Base Vocabulary architecture and initial term decisions are
documented at:

- [Base Vocabulary](base/README.md)
- [ADR-0022](../adr/0022-geesno-base-vocabulary.md)

Definition of this Vocabulary family and its terms does not
mean that a machine-readable Vocabulary artifact has already
been published.

## Identity and Namespace Expansion

Vocabulary identities and versions remain distinct from:

- repository directory paths;
- serialization formats;
- publication locations;
- retrieval mechanisms;
- namespace-prefix aliases.

Qualified-term expansion follows the applicable Core namespace
contract.

An IRI is a semantic identifier, not an instruction to access
a network resource.

```text
IRI
!= runtime dereference requirement
```

GeesNO.Semantic does not require access to `geesno.com`
to interpret an already available exact Vocabulary contract.

## Optional Discovery and Governance

Vocabulary discovery is optional.

The architecture does not impose a mandatory centralized
registry, global resolver or network service.

Vocabulary identity, publication, authority and governance
remain distinct concerns.

Implementations may use locally available Vocabulary
definitions and must not infer semantic authority merely
from a discovery or retrieval mechanism.

## Cross-Vocabulary and Profile Compatibility

Cross-Vocabulary compatibility and compatibility with
Profiles are governed by the accepted architectural model.

Compatibility semantics do not automatically:

- add new Base Vocabulary terms;
- modify the universal Core;
- create an implicit Profile composition runtime;
- establish a published compatibility artifact;
- authorize software execution.

Profile and Vocabulary contracts remain independently
identifiable and versioned.

See:

- [ADR-0023](../adr/0023-cross-vocabulary-profile-compatibility-model.md)

## Publication Status

The repository currently documents the accepted abstract
Vocabulary architecture and the initial Base Vocabulary
design.

It does not yet publish:

- a machine-readable Vocabulary artifact;
- a Vocabulary discovery catalog;
- a central Vocabulary registry;
- a standalone compatibility artifact.

The [`base/`](base/README.md) directory contains the
architectural documentation for the Base Vocabulary, not
a published machine-readable Vocabulary distribution.

A future publication artifact must comply with the
applicable accepted Vocabulary contract.

## Architectural References

For the wider GeesNO.Semantic architecture and publication
boundaries, see:

- [Architecture](../ARCHITECTURE.md)
- [Specifications](../spec/README.md)
- [Accepted ADRs](../adr/README.md)
- [Public Preview](../PUBLIC_PREVIEW.md)

GeesNO.Semantic remains universal, open, descriptive,
software-independent, format-independent,
domain-independent, AI-provider-neutral and usable offline.
