# Reference SDK

The GeesNO.Semantic reference SDK is an optional, non-normative
implementation of selected published semantic contracts.

It is provided to demonstrate practical use of GeesNO.Semantic
artifacts without introducing implementation-specific behavior
into the universal standard.

The applicable specifications, accepted ADRs and exact Profile
and Vocabulary contracts remain the semantic authorities.

```text
SDK
!= semantic authority

SDK behavior
!= normative conformance rules

reference implementation
!= required implementation
```

## Python Reference Package

The initial reference implementation is maintained under:

- [`python/`](python/README.md)

The Python package is repository-local. Its API is not declared stable,
and no package-registry distribution is provided for the public preview.

The SDK is not required to implement, produce, inspect or validate
GeesNO.Semantic artifacts.

## Supported Capabilities

The reference SDK provides explicit, descriptive operations over
supported GeesNO.Semantic artifacts.

### Semantic Documents

- Loss-aware SemanticDocument loading and inspection.
- Explicit save operations.
- Repository-local reuse of the deterministic Core conformance
  validation model, including Layers 0-3.
- Explicit document and Entity construction.
- Typed, non-copying document and Entity views.
- Optional UUID URN generation.

### Semantic Relations and Values

- Explicit Source and Binding construction and inspection.
- Reference and assertion construction/read views.
- Construction and inspection of supported Core value types.
- Host-scoped Provenance, Confidence and Review views.
- Explicit state-first lifecycle construction and inspection.

### Vocabularies and Extensions

- Inert Extension construction and inspection within supported
  Core host constraints.
- Local semantic-term expansion.
- Caller-supplied Vocabulary lookup without an implicit
  remote registry or resolver.

Extensions remain data, not executable instructions.
Vocabulary lookup does not confer new semantic authority.

### AI Context

- Caller-explicit construction of projections using an exact
  AI Context Profile edition.
- Local read-only queries over supported artifacts.
- Reuse of repository-local Profile acceptance and
  assessment-result validation components.

AI Context remains an optional Profile, separate from the
universal GeesNO.Semantic Core.

Projection construction does not mutate the source and does
not create new semantic truth.

## Architectural Boundaries

The reference SDK does not define or require:

- a general application runtime;
- integration adapters for particular software products;
- GeesNO.Core;
- a specific AI provider, model or agent framework;
- prompt execution or tool execution;
- remote identifier dereferencing;
- a central registry or resolver;
- automatic network access;
- a package-registry release;
- certification or endorsement.

All supported construction and inspection operations remain
explicit and descriptive.

The SDK does not establish new semantic rules, validation
layers or conformance outcomes.

Implementation convenience does not create normative authority.

## Conformance

Implementations must evaluate conformance against the
applicable normative contracts, not against SDK behavior.

Schema validity alone does not establish complete semantic
conformance.

The repository includes deterministic validation tools and
conformance material independent of the reference SDK.

See:

- [Architecture](../ARCHITECTURE.md)
- [Conformance Guide](../docs/conformance-guide.md)
- [Specifications](../spec/README.md)
- [Public Preview](../PUBLIC_PREVIEW.md)

The reference SDK is provided as implementation assistance.
GeesNO.Semantic remains open, software-independent,
format-independent, domain-independent, AI-provider-neutral
and usable offline.
