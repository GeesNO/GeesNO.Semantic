# GeesNO.Semantic Documentation Map

This page is a non-normative navigation index for GeesNO.Semantic.

It locates architectural, normative and supporting repository material. It does not define GeesNO.Semantic semantics.

```text
navigation/index != normative specification
README           != specification
implementation   != semantic contract
SDK behavior     != normative authority
```

## Start Here

For a first implementation:

1. Read the [architectural baseline](../ARCHITECTURE.md).
2. Read the [Core specification index](../spec/README.md) and the
   [consolidated abstract model](../spec/semantic-core.md).
3. Follow the language-neutral
   [Implementation Guide](implementation-guide.md).
4. Use the [Conformance Guide](conformance-guide.md) to select the applicable
   validation route and bounded conformance claim.
5. Read the normative [JSON serialization](../spec/json-serialization.md) and
   inspect the current
   [`spec_version` `0.1.0` schema](../schema/v0.1/geesno-semantic.schema.json).
6. Review the [Vocabulary architecture](../vocab/README.md) and
   [Extension rules](../spec/extensions.md).
7. Add an exact Profile only when required by the use case. The first published
   Profile family is documented under
   [AI Context](../profiles/ai-context/README.md).
8. Use the [Core conformance suite](../conformance/README.md) and any applicable
   exact Profile conformance material.
9. Study the
   [cross-domain examples](../examples/cross-domain/public-preview/README.md).
10. Optionally use the [reference SDK](../sdk/README.md). It is non-normative
    and is not required for a conforming implementation.

## Authority and document roles

GeesNO.Semantic separates architectural authority, normative specification,
machine-readable representation constraints, conformance evidence and
implementation guidance.

The intended reading hierarchy is:

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

Lower layers must not invent semantics absent from accepted architecture and
normative specification.

Useful document roles in this repository are:

| Role | Meaning |
| --- | --- |
| **ARCHITECTURAL BASELINE** | Defines universal project boundaries and architectural invariants. |
| **ACCEPTED ADR** | Records an accepted architectural decision and its consequences. |
| **NORMATIVE** | Defines an exact semantic or representational contract. |
| **CONFORMANCE MATERIAL** | Provides deterministic fixtures, expected outcomes or rules for assessing an exact contract. |
| **NON-NORMATIVE IMPLEMENTATION** | Implements accepted contracts without defining them. |
| **NON-NORMATIVE EXAMPLE** | Illustrates or stresses existing rules without creating new semantics. |
| **GOVERNANCE / PROJECT INFORMATION** | Describes contribution, security, licensing, roadmap or release information without defining semantic behavior. |

When explanatory material conflicts with normative specification, the normative
specification governs.

## Documentation taxonomy

| Area | Purpose | Role | Main entry | Primary audience |
| --- | --- | --- | --- | --- |
| Core semantic model | Define the serialization-independent universal semantic model and invariants. | **NORMATIVE** | [Core specification index](../spec/README.md#core-semantic-model) | Producers, consumers and reviewers |
| JSON serialization and schema | Define the `0.1.0` JSON representation and its structural constraints. | **NORMATIVE** where explicitly specified | [JSON serialization](../spec/json-serialization.md) and [schema index](../schema/README.md) | JSON implementers and validators |
| Vocabularies and Extensions | Keep qualified domain or organization meaning outside the universal Core. | Accepted architecture plus normative specifications where identified | [Vocabulary index](../vocab/README.md) and [Extension rules](../spec/extensions.md) | Vocabulary authors and extensibility implementers |
| Profiles | Apply exact, versioned requirements to explicitly identified use cases. | Exact Profile artifacts and bindings may be **NORMATIVE**; indexes remain navigation | [AI Context Profile](../profiles/ai-context/README.md) | Profile producers, consumers and assessors |
| Conformance | Provide deterministic validation routes, fixtures and expected outcomes. | Mixed normative conformance material and non-normative tooling | [Conformance Guide](conformance-guide.md) and [Core conformance](../conformance/README.md) | Implementers and test authors |
| Reference SDK | Provide one optional implementation of accepted contracts. | **NON-NORMATIVE IMPLEMENTATION** | [SDK index](../sdk/README.md) | Python users and other SDK authors |
| Examples | Explain and stress existing contracts across different domains. | **NON-NORMATIVE EXAMPLE**, unless explicitly identified as a conformance fixture | [Examples index](../examples/README.md) | Learners, implementers and reviewers |
| Licensing and project policy | Explain licensing, contribution and security policy. | **GOVERNANCE / PROJECT INFORMATION** | [License map](../LICENSES.md), [Contribution policy](../CONTRIBUTING.md) and [Security policy](../SECURITY.md) | Contributors and redistributors |
| Architecture and roadmap | Explain architectural decisions and future direction. | Architectural authority plus non-normative planning | [Architecture](../ARCHITECTURE.md), [ADR index](../adr/README.md) and [Roadmap](../ROADMAP.md) | Implementers and architectural reviewers |

## Normative-source map

| Question | Authoritative document or artifact |
| --- | --- |
| What are the universal project boundaries and architectural invariants? | [ARCHITECTURE.md](../ARCHITECTURE.md) and the [ADR index](../adr/README.md). |
| What does the universal semantic model mean? | [Core semantic model](../spec/semantic-core.md) and its topic specifications: [identity](../spec/identity.md), [entities](../spec/entities.md), [Source/Binding](../spec/source-bindings.md), [assertions](../spec/assertions.md), [values and units](../spec/values-and-units.md), [relations](../spec/relations.md), [trust metadata](../spec/provenance.md), [lifecycle](../spec/revisions.md) and [Extensions](../spec/extensions.md). |
| How is Core represented in JSON? | [JSON serialization `0.1`](../spec/json-serialization.md) plus the [Draft 2020-12 schema](../schema/v0.1/geesno-semantic.schema.json). |
| How are identifiers and references represented? | [JSON identifiers and references](../spec/json-identifiers-and-references.md) plus the Core schema. |
| How are namespaces and qualified terms represented? | [JSON qualified terms](../spec/json-qualified-terms.md), the [Vocabulary architecture](../vocab/README.md) and Accepted ADR-0017 through ADR-0023. |
| What defines AI Context Projection semantics? | [AI Context Profile specification](../spec/ai-context-profile.md), exact [Profile edition `0.1.0`](../profiles/ai-context/v0.1/profile.json), [JSON binding](../spec/ai-context-json-binding.md) and [Profile schema](../profiles/ai-context/schema/v0.1/ai-context.schema.json). |
| What defines AI Context assessment-result representation? | [Assessment JSON binding](../spec/ai-context-assessment-json-binding.md) and [assessment schema](../profiles/ai-context/schema/v0.1/ai-context-assessment.schema.json). |
| Where is bare-Core validation defined and exercised? | [Conformance specification](../spec/conformance.md), [Core schema](../schema/v0.1/geesno-semantic.schema.json), [fixtures and expected outcomes](../conformance/README.md), and the non-normative runner. |
| Where is exact AI Context Profile acceptance exercised? | [Profile acceptance corpus](../profiles/ai-context/conformance/v0.1/README.md), [assessment conformance corpus](../profiles/ai-context/assessment-conformance/v0.1/README.md), and repository-local validation tooling. |

A successful schema validation establishes only the constraints represented by
that schema.

Complete Core conformance also applies the deterministic semantic checks defined
by the applicable conformance specification.

```text
schema-valid != complete semantic conformance
```

## Core, Vocabulary and Profile boundaries

```text
Core != Vocabulary != Profile
```

Core supplies universal semantic mechanics.

Vocabularies supply qualified domain, organization or application meaning
without expanding the universal Core.

Profiles define exact requirements for an explicitly identified use case.

The [Base Vocabulary documentation](../vocab/base/README.md) records the
accepted Base Vocabulary identity, terms and architecture. Availability of a
Vocabulary representation or discovery mechanism does not create automatic
semantic authority or substitution.

Third-party and custom Vocabulary examples appear in the
[cross-domain material](../examples/cross-domain/model-review.md) and
[JSON examples](../examples/json-provisional/README.md).

## Identity and resolution

Semantic identity is distinct from representation and location.

```text
semantic identity
!= representation
!= locator

IRI
!= retrieval instruction
```

GeesNO.Semantic identifiers under `https://geesno.com/` identify semantic
families, editions or other published semantic resources as defined by the
applicable specification.

An implementation does not need to dereference those identifiers during normal
semantic processing.

Exact locally supplied artifacts and exact locally supported semantics are
sufficient for the offline-capable processing routes defined by the standard.

## AI Context Profile navigation

The AI Context Profile is optional and does not make the universal Core
AI-specific.

Key artifacts are:

- Profile identity and exact edition:
  [`profile.json`](../profiles/ai-context/v0.1/profile.json)
- Human-readable Profile semantics:
  [`ai-context-profile.md`](../spec/ai-context-profile.md)
- Profile and Projection JSON representation:
  [`ai-context-json-binding.md`](../spec/ai-context-json-binding.md)
- Profile/Projection schema:
  [`ai-context.schema.json`](../profiles/ai-context/schema/v0.1/ai-context.schema.json)
- Profile acceptance corpus:
  [`profiles/ai-context/conformance/v0.1/`](../profiles/ai-context/conformance/v0.1/README.md)
- Reproducibility benchmark:
  [`benchmarks/ai-context/v0.1/`](../benchmarks/ai-context/v0.1/README.md)
- Assessment-result representation:
  [binding](../spec/ai-context-assessment-json-binding.md) and
  [schema](../profiles/ai-context/schema/v0.1/ai-context-assessment.schema.json)
- Assessment conformance corpus:
  [`profiles/ai-context/assessment-conformance/v0.1/`](../profiles/ai-context/assessment-conformance/v0.1/README.md)
- Human-readable AI Context assessment corpus catalogue:
  [`conformance/ai-context-assessment-corpus.md`](../conformance/ai-context-assessment-corpus.md)
- Repository validation tooling:
  [`ai_context_acceptance.py`](../tools/validation/ai_context_acceptance.py) and
  [`integrated_conformance.py`](../tools/validation/integrated_conformance.py)

These routes use explicit exact artifacts and support offline assessment.

They do not define:

- latest-edition resolution;
- implicit version substitution;
- registry lookup;
- automatic network retrieval;
- model-provider arbitration;
- model invocation;
- tool execution.

## Conformance locations

### Core

- Valid fixtures: [`conformance/valid/`](../conformance/valid/README.md)
- Invalid fixtures: [`conformance/invalid/`](../conformance/invalid/README.md)
- Expected results: [`conformance/expected/`](../conformance/expected/README.md)
- Runner: [`conformance/runner/`](../conformance/runner/README.md)

### AI Context Profile

- Profile acceptance:
  [`profiles/ai-context/conformance/v0.1/`](../profiles/ai-context/conformance/v0.1/README.md)
- Assessment conformance:
  [`profiles/ai-context/assessment-conformance/v0.1/`](../profiles/ai-context/assessment-conformance/v0.1/README.md)
- AI Context assessment corpus catalogue:
  [`conformance/ai-context-assessment-corpus.md`](../conformance/ai-context-assessment-corpus.md)
- Integrated validation:
  [`integrated_conformance.py`](../tools/validation/integrated_conformance.py)
- Reference command-line validation:
  [`reference_cli.py`](../tools/validation/reference_cli.py)

```text
validation/conformance != certification
```

Passing repository validation supports only the bounded factual conformance
claim defined by the exact assessed artifact and applicable contract.

It does not create endorsement or an official certification program.

## SDK

The [reference SDK](../sdk/README.md) is optional and non-normative.

The initial reference implementation is written in Python, but Python has no
semantic privilege.

Any language or software stack may implement GeesNO.Semantic provided it
preserves the applicable normative contracts.

```text
reference SDK behavior != semantic authority
```

## Examples

The [examples index](../examples/README.md) contains learning and design-review
material.

The
[cross-domain example set](../examples/cross-domain/public-preview/README.md)
contains standalone synthetic Core documents intended to demonstrate that the
same universal model can describe materially different domains without adding
domain-specific primitives to Core.

Examples are non-normative unless an individual artifact is explicitly
identified as a conformance fixture.

Conformance fixtures differ from tutorials because they have exact expected
outcomes.

## Benchmarks

[Benchmark material](../benchmarks/README.md) provides reproducible,
non-normative evidence about selected characteristics of the standard and its
reference artifacts.

Benchmarks do not define:

- semantic validity;
- Profile conformance;
- serialization semantics;
- certification requirements.

Benchmark inputs, measurement rules and expected outputs should be explicit
enough to reproduce locally without model invocation or network access.

## Licensing, contribution and security

- [License applicability map](../LICENSES.md)
- [CC BY 4.0 specification license](../LICENSE-SPECIFICATION)
- [Apache-2.0 code license](../LICENSE-CODE)
- [Contribution policy](../CONTRIBUTING.md)
- [Security policy](../SECURITY.md)

The licensor and copyright holder identified by the repository is
`GENARO ESCUDERO NOGALES`.

Release-specific scope and claim boundaries are documented separately in
[PUBLIC_PREVIEW.md](../PUBLIC_PREVIEW.md) and
[RELEASE_NOTES.md](../RELEASE_NOTES.md).

This documentation map does not itself establish release status.

## Architecture, governance and project direction

- [ARCHITECTURE.md](../ARCHITECTURE.md) — public architectural baseline
- [ADR index](../adr/README.md) — architectural decisions
- [ROADMAP.md](../ROADMAP.md) — non-normative future direction
- [GOVERNANCE.md](../GOVERNANCE.md) — governance policy
- [CHANGELOG.md](../CHANGELOG.md) — repository evolution
- [PUBLIC_PREVIEW.md](../PUBLIC_PREVIEW.md) — preview scope and claim boundary
- [RELEASE_NOTES.md](../RELEASE_NOTES.md) — release-specific information

These documents are not substitutes for the normative Core, serialization,
Vocabulary, Profile or conformance specifications.

## Implementation principle

A conforming implementation should be able to determine the meaning of the
exact semantic artifacts it supports without requiring GeesNO-specific runtime
services.

```text
open semantic contract
+ explicit exact identity
+ local artifacts
+ deterministic rules
= independently implementable semantics
```

Software integrations, source-format adapters, model integrations and execution
systems may consume GeesNO.Semantic, but they remain outside the universal
semantic layer unless explicitly standardized by a future architectural
decision.

## Validate this source distribution

This source distribution does not require Git metadata or access to another
checkout. Its public architectural authorities are ARCHITECTURE.md and the
Accepted ADRs; exact specifications and binding artifacts define conformance.
The foundational design background preserves initial rationale without acting
as an additional current conformance contract.

`MANIFEST.sha256` records the bytes of every other distributed file.
`tools/validation/public-artifacts.json` additionally pins the public contracts,
fixtures, reference implementations and expected benchmark artifacts.
Digests provide integrity checks, not semantic identity or certification.

With the declared Python dependencies already available, run from the root:

```shell
python -B tools/validation/check_repository.py
python -B tools/validation/publication_hygiene.py
python -B tools/validation/reference_cli.py validate-repository
python -B conformance/runner/run.py
python -B -m unittest discover -s tools/validation/tests -v
python -B -m unittest discover -s sdk/python/tests -v
```

Changes to a source distribution require review and regeneration of its manifests;
a hash mismatch must not be bypassed by treating an altered artifact as approved.
A public hosting endpoint and a verified private vulnerability-reporting route
must be designated separately before public release. See SECURITY.md.
