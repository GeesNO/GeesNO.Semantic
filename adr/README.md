# Architecture Decision Records

Architecture Decision Records (ADRs) capture architectural decisions that define or refine GeesNO.Semantic.

The public architectural baseline is defined in [ARCHITECTURE.md](../ARCHITECTURE.md). Accepted ADRs refine that baseline and record the rationale and consequences of specific architectural choices.

Normative specifications implement accepted architecture. Schemas, conformance tooling and reference SDK behavior do not override accepted architectural decisions.

## ADR lifecycle

An ADR uses an explicit status such as:

- `Proposed` — under architectural consideration and not yet authoritative;
- `Accepted` — part of the accepted architecture;
- `Superseded` — replaced by a later explicit architectural decision when applicable.

A new normative architectural choice requires its own ADR or an explicit superseding ADR. Existing accepted semantics must not be changed implicitly through schema, tests, implementation behavior or documentation.

## Architectural baseline

ADR-0001 through ADR-0008 establish the initial project boundary, semantic/execution separation, serialization strategy, licensing approach and abstract-model architecture.

These decisions preserve the central constraints that GeesNO.Semantic remains universal, descriptive, software-neutral, format-neutral, domain-neutral and AI-provider-neutral.

## Identity, JSON representation and Core serialization

ADR-0009 through ADR-0016 define the initial JSON representation and related Core architecture.

- **ADR-0009** — identifier and reference model.
- **ADR-0010** — qualified-term and namespace model.
- **ADR-0011** — canonical JSON assertion placement and addressability, including mandatory Assertion identity and conditional trust-record identity.
- **ADR-0012** — value, datatype and measured-quantity model.
- **ADR-0013** — Source and Binding JSON serialization, including Binding identity as continuity of one specific correlation record.
- **ADR-0014** — lifecycle, scope and completeness serialization.
- **ADR-0015** — version, Extension and unknown-core-field policy, including numeric-token behavior.
- **ADR-0016** — JSON processing, schema draft and canonicalization boundary.

Together these decisions define how accepted Core semantics are represented without making JSON, JSON Schema or a particular implementation the source of semantic authority.

## Vocabulary architecture

ADR-0017 through ADR-0023 define Vocabulary identity, publication, lifecycle, extension use, discovery and compatibility.

- **ADR-0017** — Vocabulary identity and immutable edition-version model.
- **ADR-0018** — Vocabulary publication artifact and minimum metadata contract.
- **ADR-0019** — Vocabulary and term lifecycle semantics.
- **ADR-0020** — Extension Vocabulary authoring and payload-compatibility conventions.
- **ADR-0021** — optional Vocabulary discovery, authority and governance model.
- **ADR-0022** — GeesNO Base Vocabulary admission and initial term set.
- **ADR-0023** — cross-Vocabulary and Profile compatibility model.

The GeesNO Base Vocabulary established by ADR-0022 uses:

```text
Vocabulary family: https://geesno.com/vocab/base
Edition:           0.1.0
Expansion base:    https://geesno.com/vocab/base/
Preferred prefix:  gbase
```

Initial experimental terms include `label` and `description`.

Vocabulary identity and compatibility remain explicit. Discovery does not imply authority, automatic resolution or semantic substitution.

## Profile and AI Context architecture

ADR-0024 through ADR-0031 define Profile identity, Projection semantics, Profile requirements, AI Context bindings, assessment results and Profile composition.

- **ADR-0024** — Profile identity, exact version and conformance boundary.
- **ADR-0025** — AI Context selection and Projection semantics.
- **ADR-0026** — Projection omission, boundedness and continuation semantics.
- **ADR-0027** — Projection preservation and material-context semantics.
- **ADR-0028** — Profile requirement expression semantics.
- **ADR-0029** — AI Context Profile and Projection serialization binding.
- **ADR-0030** — AI Context Profile conformance result and diagnostics.
- **ADR-0031** — AI Context Profile composition and conflict policy.

These decisions preserve several architectural boundaries:

```text
Profile != Core != Vocabulary

Projection != source mutation

Profile requirement != execution instruction

conformance result != semantic truth

multiple Profile references != merged Profile

IRI != retrieval instruction
```

Profile editions are exact and immutable as normative requirement sets. Implementations must not silently substitute `latest`, newer-looking, similar or inferred-compatible editions.

AI Context artifacts and requirements remain inert semantic data. They do not define model invocation, tool execution, workflow behavior, automatic retrieval or provider-specific runtime semantics.

## Authority and implementation

ADRs define architectural decisions; detailed normative behavior is specified under [`spec/`](../spec/).

The intended authority relationship is:

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
reference SDK and explanatory documentation
```

Lower layers must not invent semantics absent from accepted architecture and specification.

## Index use

When implementing or reviewing GeesNO.Semantic:

1. start with [ARCHITECTURE.md](../ARCHITECTURE.md);
2. consult the ADR relevant to the architectural question;
3. use the corresponding normative specification for exact semantics;
4. use schemas and conformance artifacts for representation and deterministic validation;
5. treat the reference SDK as non-normative implementation guidance.

An Accepted ADR remains authoritative until an explicit later architectural decision supersedes it.
