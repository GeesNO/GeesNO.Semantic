# ADR-0028: Profile requirement expression semantics

- **Status:** Accepted
- **Accepted by:** Explicit human architecture decision on 2026-09-22
- **Date:** 2026-09-21
- **Decision order:** Fifth S4 architecture decision after ADR-0027 acceptance

## Context

ADR-0024 accepts exact AI Context Profile identity, exact Profile editions and
the bare-core/Profile conformance boundary. ADR-0025 accepts Projection as a
finite derived semantic view under an exact Profile edition and explicit
selection context. ADR-0026 accepts Projection completeness, omission,
boundedness, truncation, continuation and dependency-continuation semantics.
ADR-0027 accepts preservation and material-context semantics.

S4 D5 needs the abstract semantics of Profile requirements: what it means for
an exact Profile edition to require, allow or prohibit structures, terms,
projection properties, preservation obligations or materialization behavior.
That must be defined before any concrete AI Context Profile binding can encode
the requirements.

This ADR proposes abstract requirement semantics only. It does not define a
Profile document shape, JSON members, schema, fixture format, diagnostic result,
query language, selector language, expression language, SDK API, runtime
behavior, model integration, registry, resolver, network protocol or execution
behavior.

## Prerequisite review

1. The Foundation makes Profiles a way to define interoperable projection and
   conformance subsets without turning GeesNO.Semantic into execution.
2. The Foundation requires deterministic conformance; LLM judgment may assist
   authoring but cannot be required for syntactic/profile conformance.
3. ADR-0015 keeps Extensions inert and unable to redefine core semantics.
4. ADR-0016 separates bare-core Layers 0-3 from later Profile validation and
   requires local schema supply with no automatic network retrieval.
5. ADR-0017 separates Vocabulary identity, Vocabulary version, namespace
   expansion base and term identity.
6. ADR-0023 defines inert compatibility/profile-acceptability claims but does
   not create automatic compatibility resolution, substitution or conformance.
7. ADR-0024 defines exact Profile edition identity and separates bare-core
   conformance from Profile conformance.
8. ADR-0025 defines selection and Projection semantics without a selector or
   ranking language.
9. ADR-0026 defines completeness, omission, boundedness and continuation.
10. ADR-0027 defines material context and preservation without defining Profile
    requirement syntax.

## Controlling distinctions

```text
Profile != Core

Profile != Vocabulary

Profile requirement != semantic fact

Profile requirement != execution

Profile requirement != selection algorithm

Profile requirement != transformation rule

Profile requirement != serialization binding

Profile conformance != semantic truth

Profile conformance != Projection completeness

Profile allows omission
!= omission ceases to be omission

Profile requirement expression semantics
!= concrete Profile artifact syntax

Profile requirement expression semantics
!= Profile conformance result model

Profile requirement expression semantics
!= Profile composition policy

exact Profile edition = exact reproducible requirement set

Vocabulary identity != namespace expansion base

Vocabulary version != Profile version

Profile constrains Vocabulary use
!= Profile owns term meaning

required materialization != material dependency allowed by reference

allowed by reference != materialized

explicit omission != preservation

required != globally materialized unless the requirement says so

optional != unknown

not required != prohibited

prohibited != absent in source

cardinality != order

serialization order != priority

unsupported requirement != failed requirement

unknown Profile semantics != nonconformant document
```

No Profile requirement may depend on `latest`, moving aliases, implicit version
ranges, automatic resolution, automatic compatibility upgrade, automatic
Vocabulary substitution or automatic Profile substitution.

## Definitions

**Profile family identity** means the stable Profile family identity accepted by
ADR-0024.

**Profile version** means an exact Profile edition version under a Profile
family identity. A moving alias such as `latest` is not an exact Profile
version.

**Exact Profile edition** means the pair of Profile family identity and exact
Profile version, plus the reproducible requirement set normatively identified
by that pair.

**Profile requirement set** means the complete set of normative Profile
requirements identified by an exact Profile edition. The requirement set is the
semantic authority for Profile conformance; a concrete future binding may
represent, encode or transport it but does not originate it.

**Profile requirement** means an inert normative condition in a Profile
requirement set. A requirement can say what a conforming document, Projection,
record, relationship, term use, Extension payload or preservation policy must,
may or must not contain or declare. It is not a semantic assertion about the
source.

**Requirement applicability** means the abstract condition under which a
requirement applies. Applicability can be relative to a record category,
semantic role, declared Projection scope, selected content, contextual
condition, Profile-defined scope or exact Vocabulary use. Normative
applicability must be determinable from explicit assessable information
identified by the exact Profile edition. Applicability is not a query engine,
selection algorithm, transformation rule, retrieval process, ambient
implementation state or hidden runtime state.

**Requirement satisfaction** means that the material assessed under an exact
Profile edition meets the applicable requirement. D5 defines this abstract
concept only; D7 will own the concrete conformance result and diagnostic model.

**Unsupported requirement** means a requirement whose semantics are not
understood or evaluable by an assessor. Unsupported does not mean satisfied,
violated or a semantic failure of the document.

**Dependency unavailable** means a locally required dependency for assessment is
not available to the assessor. Dependency unavailability blocks a conformance
claim for the affected Profile requirement unless the exact Profile edition
defines an offline-safe alternative.

**Stable requirement identity** means an optional identity assigned by an exact
Profile edition to an individual requirement. When assigned, it must be stable
within that exact edition and must not be array-position identity.

## Alternatives

### Alternative A - Profile requirements as executable rules

A Profile could define scripts, callbacks, remote validators, tool calls,
prompts, query services or transformation programs. This is rejected. It would
make a Profile an execution system and would violate the Foundation boundary
between semantic description and operational capability.

### Alternative B - Profile requirements as a concrete schema language

D5 could choose JSON Schema, SHACL, OWL, CEL, JSONPath, Rego or another concrete
constraint language as the meaning of Profile requirements. This is rejected at
D5. A future binding may use a concrete representation, but the semantic model
must exist before a binding can encode it.

### Alternative C - Profile requirements as Vocabulary meaning

A Profile could own or redefine term meaning. This is rejected. Vocabularies
define term meaning. Profiles may constrain which exact Vocabulary editions,
terms or term combinations are acceptable for a use case.

### Alternative D - Abstract inert requirement semantics

An exact Profile edition identifies a reproducible inert requirement set. The
requirements can define what is required, optional or prohibited, where they
apply, and how Profile conformance is assessed conceptually, without selecting
syntax, execution, automatic resolution, schema, fixtures or diagnostics. This
is proposed.

## Proposed decision

D5 accepts an abstract, serialization-independent model for Profile requirement
semantics. An exact Profile edition is the semantic authority for its Profile
requirement set. A future concrete binding may represent, encode, package,
sign, transport or reference the requirement set, but representation is not
semantic authority.

```text
Profile edition / accepted semantic rule
= semantic authority for Profile requirements

future binding
= representation / encoding / transport of those requirements

representation != semantic authority
```

## Requirement set semantics

An exact Profile edition identifies exactly one reproducible Profile
requirement set for that edition. A consumer assessing Profile conformance MUST
assess against that exact set, not against a moving alias, latest edition,
compatible-looking edition, retrieved replacement or inferred future edition.

The requirement set may express requirements for:

- required, optional and prohibited structures;
- applicability conditions;
- cardinality;
- exact Vocabulary family, version, term and capability requirements;
- Projection scope and completeness requirements;
- preservation obligations;
- Source and Binding materialization;
- allowed-by-reference dependencies;
- omission and dependency-continuation declarations;
- boundedness and truncation declarations;
- required continuation presence;
- self-containment and closure.

This list defines semantic dimensions D5 permits at the abstract level. It does
not define concrete field names, tokens, expression grammar, schema keywords,
validation API, diagnostics or fixtures.

## Requirement statements

A Profile requirement can require, allow or prohibit material in the assessed
material. A requirement statement can concern:

- the SemanticDocument or Projection as a whole;
- Entity, Assertion, Source, Binding, Revision or Extension records;
- term usage and exact Vocabulary edition usage;
- relationship/association categories;
- declared Projection scope and selection context;
- preservation or material-context handling;
- continuation, omission, boundedness or truncation declarations; or
- metadata needed to make a Profile conformance claim.

A Profile requirement is not itself a semantic assertion. If a document fails a
Profile requirement, the failed requirement does not make the source assertion
false. If a document satisfies a Profile requirement, satisfaction does not make
the source assertion true.

## Requirement applicability

Requirement applicability may be scoped by:

- document kind or Profile-defined scope;
- record category;
- semantic role;
- exact term, term set or Vocabulary edition;
- selected content;
- declared Projection scope;
- explicit selection context;
- material-context state;
- Source or Binding participation;
- lifecycle state;
- other explicitly declared Profile-defined assessment context.

Applicability does not select source content by itself. It does not define a
query language, ranking algorithm, embedding search, LLM relevance judgment,
retrieval algorithm, transformation or generation process.

Normative applicability must be determinable from explicit assessable
information. A contextual condition defined by the exact Profile edition may
depend on the assessed SemanticDocument or Projection content, record category,
semantic role, exact term or Vocabulary edition, declared Projection scope,
explicit selection context, material-context state, Source or Binding
participation, lifecycle state or other explicitly declared Profile-defined
assessment context.

```text
requirement applicability
must be determinable from explicit assessable information

ambient implementation state
!= normative applicability context

hidden runtime state
!= normative applicability
```

Normative applicability MUST NOT depend on undeclared ambient state such as:

- current software session;
- consumer implementation quirks;
- user identity or user state not represented explicitly;
- GUI state;
- environment variables;
- filesystem state;
- network state;
- remote service responses;
- hidden resolver state;
- model output;
- current wall-clock time unless an accepted future rule supplies an explicit
  evaluation context with defined semantics;
- any other undeclared runtime condition.

If additional assessment context is required, it must be explicit,
identifiable, Profile-defined and deterministically assessable. D5 does not
define the concrete representation for such context.

An implementation may use tooling to find candidate material, but Profile
conformance depends on whether the assessed material meets the exact Profile
requirements, not on which tool suggested it.

## Required, optional and prohibited

Profile requirements may distinguish:

- **required**: the applicable material must be present, declared, carried,
  referenced, omitted explicitly or otherwise handled exactly as the requirement
  states;
- **optional**: the material may be present when otherwise valid, but absence
  alone does not violate that requirement;
- **prohibited**: the material must not be present or used in the applicable
  scope.

These distinctions preserve:

```text
optional != unknown
not required != prohibited
prohibited != absent in source
required != globally materialized unless the requirement says so
```

A requirement can require a declaration rather than materialization. A
requirement can require materialization. A requirement can allow reference
instead of materialization. The exact Profile edition must make that distinction
normative; a binding must not invent it.

## Cardinality

Profile requirements may express cardinality at the abstract level:

- exactly one;
- zero or one;
- one or more;
- zero or more;
- bounded finite counts when the exact Profile edition justifies a concrete
  limit.

Cardinality is not ordering, priority, importance, preference, trust,
semantic truth or source frequency. D5 does not define a concrete cardinality
syntax.

## Exact Vocabulary requirements

A Profile may require exact Vocabulary families, exact Vocabulary versions,
specific absolute term identities or explicitly declared alternatives. A Profile
may require that a record use terms from a specific exact Vocabulary edition.
A Profile may require or allow an ADR-0023 profile-acceptability claim or exact
compatibility claim only when the exact Profile edition says so.

These constraints preserve:

```text
Profile != Vocabulary
Vocabulary identity != namespace expansion base
Vocabulary version != Profile version
```

A Profile MUST NOT infer acceptability from:

- local prefix spelling;
- namespace expansion base similarity;
- Vocabulary family identity without exact version where exact version is
  required;
- Profile version similarity;
- `latest`;
- implicit version ranges;
- automatic resolver output;
- automatic compatibility upgrade;
- unlisted ADR-0023 compatibility claims;
- AI similarity or embedding closeness.

These constraints also preserve:

```text
built-in support for exact edition
!= automatic Vocabulary substitution

known similar Vocabulary
!= exact Vocabulary semantics

newer edition
!= required edition

AI understanding
!= deterministic Vocabulary understanding
```

A Profile constrains Vocabulary use for a purpose. It does not own term meaning,
change term meaning, redefine third-party Vocabulary authority or make GeesNO
Base Vocabulary higher priority than any third-party Vocabulary unless the
exact Profile edition explicitly requires a Base Vocabulary term.

## Structural, semantic and policy requirements

A Profile requirement may be structural, semantic or policy-like:

- structural requirements concern record shape, required associations,
  cardinality or metadata presence;
- semantic requirements concern exact term use, scope, identity preservation or
  accepted abstract semantic distinctions;
- policy-like requirements concern Profile conformance rules such as requiring
  self-containment or allowing partial Projections.

Policy-like requirements are still inert semantic requirements. They do not
grant permissions, trigger actions, execute workflow, retrieve dependencies,
mutate source data or change the truth of any semantic assertion.

## Preservation requirements

A Profile requirement may define preservation obligations for material context
consistent with ADR-0027. It may require one or more of these abstract outcomes:

- context required to be carried;
- exact reference sufficient;
- materialization required;
- omission allowed;
- partial Projection allowed;
- self-containment required;
- trust/context closure required;
- dependency continuation declaration required.

These outcomes preserve:

```text
allowed by reference != materialized
explicit omission != preservation
Profile allows omission != Projection complete
Profile conformance != Projection completeness
required materialization != material dependency allowed by reference
```

If an exact Profile edition establishes in advance that an exact reference
satisfies the applicable requirement and the referenced record may remain
outside the Projection, the referenced record is not automatically classified as
omitted required in-scope materialized content.

If a requirement instead requires materialization and known required in-scope
material context is omitted, the Projection is partial under ADR-0026 even if
the Profile allows partial or explicitly omitted Projections to be conforming to
that Profile.

A Profile may allow omission, require explicit omission metadata or require
dependency continuation. That allowance does not preserve the omitted content
and does not make the omission disappear.

## Projection requirements

A Profile requirement may define requirements for:

- declared Projection scope;
- selection context metadata;
- completeness declarations;
- boundedness declarations;
- truncation declarations;
- continuation metadata;
- dependency continuation metadata;
- material context preservation;
- whether self-containment or closure is required.

A Profile requirement does not imply one unique Projection for the same source.
Different Projections can conform to the same exact Profile edition when the
Profile permits those scopes, selections and preservation choices.

D5 does not define a selector language, ranking language, token policy, item
count syntax, byte count syntax, continuation token syntax or concrete
projection serialization.

## Deterministic assessment

Profile conformance assessment must be deterministic for an assessor that
understands the exact Profile requirements and has the locally supplied
dependencies required by that Profile.

Assessment MUST NOT require:

- LLM judgment;
- embedding similarity;
- probabilistic relevance scoring;
- model-specific tokenization;
- prompts;
- network access;
- automatic dereference;
- remote registry lookup;
- remote evaluator execution;
- tool calls;
- source mutation;
- hidden resolver policy;
- hidden ambient implementation state;
- undeclared runtime context.

An assessment may depend on semantics for the exact identified Vocabulary
edition when those semantics are locally supplied or explicitly built into /
supported by the assessor for that exact edition. Built-in support for one
exact edition does not permit automatic Vocabulary substitution. Known similar
Vocabulary semantics, newer editions, retrieved alternatives or AI
understanding do not count as deterministic understanding of the required exact
Vocabulary edition.

D5 distinguishes the concepts of understood/evaluable, unsupported, dependency
unavailable and violated. D7 will define concrete result categories,
diagnostic payloads and reporting.

## Unknown, unsupported and unavailable requirements

If a requirement's semantics are not understood by an assessor, the assessor
MUST NOT claim that the assessed material conforms to that requirement. That
does not make the document semantically false or automatically nonconformant as
a document.

If a required dependency is unavailable, the assessor MUST NOT silently treat
the dependency as satisfied or violated unless the exact Profile edition defines
an offline-safe rule for that case.

If an assessor supports only a similar or newer Vocabulary edition, but not the
exact required edition or an exact alternative explicitly allowed by the
Profile, the exact requirement is not satisfied through substitution.

The abstract states remain distinct:

```text
understood and evaluable
unsupported
dependency unavailable
violated
```

D5 does not define diagnostic names, severity levels, machine-readable result
shape or reporting syntax.

## Requirement identity

An exact Profile edition identifies the requirement set. Individual requirement
identity is optional in the universal abstract model.

If a requirement needs citation, diagnostics, composition, exception handling or
cross-reference, the exact Profile edition MAY assign a stable requirement
identity. When assigned, requirement identity MUST NOT be based on array
position, display order, file line number or binding-specific location.

Future D7 diagnostics may reference exact Profile edition plus stable
requirement identity when available. If a requirement has no stable identity,
a future binding may still report a binding-specific location, but that
location is not universal requirement identity.

Future D8 composition may rely on stable requirement identities only if D8
accepts rules for doing so.

## Requirement order

Requirement order is not priority, precedence, override, importance or truth.
Serialization order is not semantic order. First/last position does not change
the meaning of a requirement.

D5 does not define cascades, overrides, inheritance, precedence or conflict
resolution between requirements.

## Profile composition boundary

Combining two exact Profile editions is not defined by D5.

```text
Profile P1 + Profile P2
!= merged Profile P3
```

A document may be assessed separately against two exact Profile editions, but
D5 defines no merge operation, conflict policy, override rule, inheritance,
extension relation or compatibility implication between them. D8 remains open
for Profile composition and conflict policy if S4 later needs it.

## Vocabulary/Profile policy boundary

Vocabularies define term meaning. Profiles define requirement policy for a
purpose. A Profile may say that a conforming AI Context Projection must use a
specific term, must not use a term, may use one of several exact term
alternatives, or must include a specific compatibility claim.

That policy does not:

- change the Vocabulary's term meaning;
- create a new Vocabulary edition;
- prove semantic equivalence;
- make unlisted terms false;
- define a migration;
- execute mapping;
- grant trust;
- establish Profile conformance for another Profile.

## Extensions

A Profile may require, allow or prohibit known Extension data for Profile
conformance. Doing so does not make the Extension a core member, a universal
requirement or executable behavior.

Unknown Extension handling for bare-core conformance remains unchanged by a
Profile requirement. A Profile assessor that does not understand a Profile-
required Extension requirement must treat that requirement as unsupported for
Profile assessment, not as a bare-core failure.

D5 defines no new Extension syntax.

## Artifact and serialization boundary

D5 does not define:

- Profile artifact packaging;
- Profile file names;
- media types;
- canonical Profile serialization;
- JSON members;
- JSON Schema;
- SHACL;
- OWL;
- CEL;
- JSONPath;
- Rego;
- query languages;
- selector languages;
- expression languages;
- schema publication locations;
- fixture layout;
- conformance result shape.

D6 owns concrete AI Context/Profile serialization binding. D7 owns Profile
conformance result and diagnostics. D8 owns composition and conflict policy if
needed.

## Non-executable requirements

Profile requirements are inert. They MUST NOT be scripts, callbacks, arbitrary
code, tool calls, remote evaluator invocations, prompts, agents, transforms,
patches, commands, source mutations, transactions or workflow steps.

A system may implement a validator, generator or checker externally, but that
implementation does not become part of the Profile requirement semantics unless
a later accepted ADR defines a non-executable binding for the relevant
semantics.

## Offline behavior

Profile assessment must be possible from locally supplied or already known
artifacts and explicit assessment context required by the exact Profile
edition. No conformance claim may depend on automatic fetch from `geesno.com`,
a registry, resolver, cloud service, Vocabulary server, Profile server, AI
service, network endpoint or hidden ambient runtime state.

An exact IRI remains identity, not an automatic dereference instruction.

## D6 boundary

D6 may define how a concrete binding represents, encodes or transports Profile
requirements and related metadata. D6 MUST NOT become independent semantic
authority for requirements such as self-containment, boundedness,
continuation, completeness, materialization or omission. Those requirements must
come from an exact Profile edition or accepted semantic rule.

```text
D5 requirement meaning
!= D6 representation
```

## D7 boundary

D7 may define the concrete Profile conformance result, diagnostics, severity,
machine-readable result categories, fixture expectations and reporting shape.
D7 MUST NOT redefine the meaning of Profile requirements accepted by D5.

```text
D5 requirement semantics
!= D7 diagnostic/result syntax
```

## D8 boundary

D8 may define Profile composition and conflict policy if S4 later accepts that
scope. D5 defines no merge, inheritance, override, precedence, conflict
resolution or combined Profile identity.

```text
D5 exact Profile edition requirement set
!= D8 composition policy
```

## Cross-domain validation

| Domain | Stress case | Result |
| --- | --- | --- |
| Engineering-like object graph | A Projection carries selected components and exact references to omitted source-context records. | The Profile can require materialization or allow exact reference without making the binding the semantic authority. |
| Spreadsheet/table dataset | A Profile requires one label Vocabulary edition for column concepts and allows a second exact edition only through explicit profile policy. | Exact Vocabulary requirements avoid local-prefix and latest-version inference. |
| Technical/legal document | A Profile requires quoted clauses to carry Provenance, Validity and Review context, while allowing some background definitions by reference. | Required materialization and allowed-by-reference remain distinct. |
| Software repository/source code | A Profile requires source file assertions to include exact Revision context but does not execute build tools or static analyzers. | Profile conformance remains deterministic and non-executable. |
| Scientific dataset | A Profile requires measured values to preserve exact unit terms and uncertainty context when selected. | Requirements constrain term use and preservation without changing the measured-value model. |
| Generic product/asset data | A Profile allows partial product Projections with explicit omission and continuation for supplier metadata. | Profile conformance can allow partial Projection without redefining Projection completeness. |

## Adversarial cases

| # | Case | Required interpretation | Must not infer |
| --- | --- | --- | --- |
| 1 | Profile declares `latest` as a required edition | Not an exact Profile edition requirement. | Moving alias conformance. |
| 2 | Profile version resembles Vocabulary version | Distinct identity dimensions. | Vocabulary version from Profile version. |
| 3 | Namespace expansion base matches a Vocabulary family | Expansion base is not Vocabulary identity. | Vocabulary acceptability. |
| 4 | Local prefix matches a preferred prefix | Prefix spelling is local. | Exact term identity or compatibility. |
| 5 | Requirement says a term is required | Term use is required for conformance. | Source fact truth. |
| 6 | Requirement is optional | Absence does not violate that requirement. | Unknown source content. |
| 7 | Requirement is not required | It is not required by that rule. | It is prohibited. |
| 8 | Requirement prohibits a term in Projection scope | Conforming material must not use it there. | The source lacks that term. |
| 9 | Requirement says exactly one Source is required | Cardinality condition applies. | Source priority or truth. |
| 10 | Requirements appear in a serialized list | Order is presentation/binding order. | Priority, override or cascade. |
| 11 | First requirement conflicts with later requirement | D5 defines no conflict policy. | First/last wins. |
| 12 | Profile P1 and P2 are both declared | They may be assessed separately if supported. | A merged Profile exists. |
| 13 | Profile requires exact Vocabulary edition A | A must be used unless Profile permits alternatives. | Edition B is acceptable because it is newer. |
| 14 | Edition B has ADR-0023 compatibility claim | Claim is inert evidence/policy input. | Automatic Profile satisfaction. |
| 15 | Profile explicitly permits A or B | Listed alternatives may satisfy that requirement. | Any similar edition is acceptable. |
| 16 | AI model judges two terms equivalent | External suggestion only. | Deterministic Profile conformance. |
| 17 | Requirement needs unavailable Vocabulary artifact | Dependency unavailable. | Satisfied or violated by network failure alone. |
| 18 | Assessor does not understand a requirement | Unsupported requirement. | Failed document requirement. |
| 19 | Unknown Profile semantics | No conformance claim for that requirement. | Document is semantically false. |
| 20 | Binding encodes a self-containment flag | Representation may carry the requirement. | Binding originated semantic authority. |
| 21 | Binding defines byte count syntax | Binding may represent an accepted bound dimension. | Binding defines bound semantics independently. |
| 22 | Profile allows partial Projection | Profile conformance may allow partiality. | Projection is complete. |
| 23 | Profile allows omission | Omission may be conforming. | Omitted content is preserved. |
| 24 | Exact reference satisfies requirement | Referenced record may remain outside Projection. | Referenced record is materialized. |
| 25 | Materialization is required and content is omitted | Projection is partial under ADR-0026. | Profile allowance erases omission. |
| 26 | Continuation metadata is required | Inert metadata must be present. | Fetch or cursor execution. |
| 27 | Dependency continuation is declared | External dependency remains outside Projection. | Dependency content is preserved locally. |
| 28 | Truncation is declared | Known incomplete relative to declared Projection scope. | Unknown completeness. |
| 29 | Bound is reached without established truncation | Boundedness exists. | Known truncation. |
| 30 | Profile requires self-containment | Closure requirement applies. | Network dereference or source mutation. |
| 31 | Requirement requires Review context | Review context must satisfy Profile policy. | Review is universal approval. |
| 32 | Requirement requires Confidence context | Confidence context must satisfy Profile policy. | Confidence is truth. |
| 33 | Requirement requires Source materialization | Source record must be carried. | Source is authority. |
| 34 | Requirement requires Binding locator retention | Binding locator must be preserved. | Locator is semantic identity. |
| 35 | Extension required by Profile | Profile conformance may require it. | Extension becomes Core. |
| 36 | Unknown Extension in bare-core document | Bare-core Extension policy still applies. | Profile failure unless Profile requires understanding it. |
| 37 | Validator uses local cached Profile edition | Allowed if it is the exact edition. | Need for automatic registry fetch. |
| 38 | `geesno.com` is unreachable | Identity remains exact IRI. | Conformance must fail from network unavailability alone. |
| 39 | Tool generates a conforming-looking Projection | It may be assessed against the exact Profile. | Tool output is automatically conforming. |
| 40 | Requirement has no stable identity | Exact Profile edition still identifies the set. | Array position is universal identity. |
| 41 | Applicability depends on current GUI selection | Not normative unless represented as explicit Profile-defined assessment context. | Hidden GUI state determines applicability. |
| 42 | Two assessors have different environment variables | Normative applicability must be the same from explicit assessable information. | Different ambient state changes Profile requirements. |
| 43 | Assessor has exact Vocabulary edition built in | It may use that exact built-in edition support. | Need for network fetch or automatic substitution. |
| 44 | Assessor knows only similar or newer Vocabulary edition | Exact requirement remains unsupported/unavailable unless Profile explicitly permits that alternative. | Similar/newer edition satisfies the exact requirement. |

## Consequences

- S4 D5 can distinguish abstract Profile requirement meaning from concrete
  Profile/Profile-binding representation.
- Exact Profile editions remain reproducible requirement sets with no latest
  alias, version range or automatic resolver semantics.
- Requirement applicability must be determinable from explicit assessable
  information and cannot depend on hidden ambient implementation state.
- Profile requirements can cover preservation, closure, self-containment,
  omission, continuation, boundedness, truncation, Source/Binding
  materialization and exact Vocabulary use without defining concrete syntax.
- Deterministic assessment may use locally supplied or explicitly built-in
  semantics for the exact identified Vocabulary edition, without automatic
  Vocabulary substitution.
- Profile conformance remains separate from semantic truth, bare-core
  conformance and Projection completeness.
- Unsupported and unavailable requirements block conformance claims without
  turning into semantic document falsehood.
- D6 can encode requirements but cannot originate semantic authority.
- D7 can report assessment outcomes but cannot redefine requirement meaning.
- D8 remains open for composition and conflict policy.
- No schema, fixture, SDK, runtime, query engine, registry, resolver, artifact
  or publication follows from this ADR.

## Remains open

- concrete AI Context/Profile serialization binding;
- concrete Profile artifact format and packaging;
- exact requirement expression syntax;
- concrete omission, bound, continuation and preservation metadata syntax;
- concrete Profile conformance result and diagnostics;
- fixture design for Profile conformance;
- Profile composition and conflict policy;
- official conformance/certification policy;
- token/size benchmark methodology;
- SDK/tooling behavior.

## Acceptance boundary

**Decision status: Accepted**

ADR-0028 is Accepted by explicit human architecture decision on 2026-09-22.
Acceptance closes S4 D5 only: abstract Profile requirement expression semantics
and the Profile/Vocabulary policy boundary. It does not accept D6 concrete
serialization, D7 conformance-result diagnostics, D8 composition, Profile
artifacts, schemas, fixtures, SDK APIs, registry/resolver behavior, publication,
model integration or execution behavior.
