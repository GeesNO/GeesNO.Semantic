# AI Context Profile

The AI Context Profile is an optional GeesNO.Semantic Profile for producing a
compact, descriptive projection of a larger semantic dataset.

Its purpose is to retain the semantic context needed by a bounded consumer while
preserving stable identity, relevant types, properties and relations, material
provenance and confidence, traceable source bindings, and explicit information
about omitted, partial or continued context.

AI Context is AI-provider-neutral. It does not define prompting, RAG,
retrieval algorithms, embeddings, vector databases, model routing, tool calling,
agents or software execution.

## Architectural Boundary

AI Context is a Profile of GeesNO.Semantic, not part of the universal Core.

```text
AI Context Profile
!= GeesNO.Semantic Core

Projection
!= source mutation

Projection
!= new semantic truth

Profile declaration
!= proof of Profile conformance
```

The Profile remains descriptive and non-executable.

Use of an AI Context artifact does not require a cloud service, model provider,
registry, resolver or network connection.

Semantic identifiers under `https://geesno.com/` are stable identities. Their use
does not require runtime dereferencing.

The public architectural baseline is
[ARCHITECTURE.md](../../ARCHITECTURE.md). The normative Profile semantics are
defined by:

- [AI Context Profile](../../spec/ai-context-profile.md);
- [AI Context JSON binding](../../spec/ai-context-json-binding.md);
- [AI Context Assessment JSON binding](../../spec/ai-context-assessment-json-binding.md).

Accepted ADRs provide the architectural decisions behind those specifications.

## Profile Identity and Edition

The current Profile family identity is:

```text
https://geesno.com/profile/ai-context
```

The repository contains Profile edition `0.1.0` at:

- [`v0.1/profile.json`](v0.1/profile.json)

The repository path is organization and distribution metadata. It is not the
Profile identity and does not create a runtime dependency on the repository.

The `0.1.0` Profile artifact contains exactly nine requirements and has no
Vocabulary dependencies.

Profile identity, Profile version, repository path and retrieval location remain
separate concepts.

## Profile and Projection JSON Binding

The Profile requirement and Projection representation is defined by the
`ai-context-json` binding family.

Its stable binding identity is:

```text
https://geesno.com/binding/ai-context-json
```

The `0.1.0` JSON representation is supported by the Draft 2020-12 schemas under:

- [`schema/v0.1/`](schema/v0.1/)
- [`schema/README.md`](schema/README.md)

JSON Schema validates the supported representation. It does not originate or
override Profile semantics.

## Profile Conformance

Deterministic Profile acceptance material is available under:

- [`conformance/v0.1/`](conformance/v0.1/README.md)

The conformance material separates structural JSON validity from semantic Profile
acceptance.

```text
schema-valid
!= complete Profile conformance
```

The repository-local reference checker is:

- [`tools/validation/ai_context_acceptance.py`](../../tools/validation/ai_context_acceptance.py)

See the public
[Conformance Guide](../../docs/conformance-guide.md)
for the applicable validation routes and bounded claim rules.

## Assessment Result Model

Assessment of an explicit subject against an exact AI Context Profile edition is
defined separately from Profile and Projection representation.

The assessment-result binding has the stable identity:

```text
https://geesno.com/binding/ai-context-assessment-json
```

Its specification is:

- [AI Context Assessment JSON binding](../../spec/ai-context-assessment-json-binding.md)

Its Draft 2020-12 structural schema is:

- [`schema/v0.1/ai-context-assessment.schema.json`](schema/v0.1/ai-context-assessment.schema.json)

Its deterministic assessment-result corpus is isolated under:

- [`assessment-conformance/v0.1/`](assessment-conformance/v0.1/README.md)

Reference validation components include:

- [`ai_context_requirement_assessment.py`](../../tools/validation/ai_context_requirement_assessment.py)
- [`ai_context_result_construction.py`](../../tools/validation/ai_context_result_construction.py)

Assessment preserves the distinction between:

```text
conformant
nonconformant
indeterminate
```

and between requirement-level outcomes such as:

```text
satisfied
violated
not_applicable
unsupported
unavailable
```

Assessment results are reporting artifacts. They do not create semantic truth,
Review, permission or execution authorization.

## Examples

Non-normative AI Context examples are available under:

- [`examples/ai-context/`](../../examples/ai-context/)

Examples illustrate supported semantics and representation patterns.

```text
example
!= conformance fixture
```

## Reproducibility Benchmark

The repository includes a deterministic AI Context benchmark under:

- [`benchmarks/ai-context/v0.1/`](../../benchmarks/ai-context/v0.1/)

The benchmark is reproducibility and measurement material. It does not define
Profile semantics or conformance.

## Reference SDK

The optional non-normative reference SDK is documented separately under:

- [`sdk/`](../../sdk/README.md)

The SDK may demonstrate use of GeesNO.Semantic artifacts, but it is not semantic
authority and is not required to implement or validate AI Context.

## Implementation Boundary

This Profile does not require or define:

- automatic network access;
- identifier dereferencing;
- a central registry or resolver;
- a specific programming language;
- a specific application or file format;
- a specific AI provider or model;
- prompt execution;
- tool execution;
- source-file mutation;
- a general Profile composition runtime;
- certification or endorsement.

Profile composition, when applicable, remains distinct from the identity and
semantics of an individual exact Profile edition.

For public-preview scope and claim boundaries, see
[PUBLIC_PREVIEW.md](../../PUBLIC_PREVIEW.md).
