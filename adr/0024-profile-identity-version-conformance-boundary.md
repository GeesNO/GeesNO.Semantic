# ADR-0024: Profile identity, version and conformance boundary

- **Status:** Accepted
- **Accepted by:** Explicit human architecture decision on 2026-09-18
- **Date:** 2026-09-18
- **Decision order:** First S4 architecture decision after S3 closure

## Context

S4 starts after S3 closure. S0, S1, S2 and S3 are Complete. ADR-0009 through
ADR-0023 are Accepted. The completed S2 JSON contract already contains a
`profiles` declaration shape and separates bare-core Layers 0-3 from future
profile validation, but it does not define what a GeesNO.Semantic Profile is,
how Profile editions are identified, what exact Profile versioning means, or
what a Profile conformance result asserts.

The Foundation makes the AI Context Profile a first-class project objective: a
compact, traceable, AI-readable context that preserves stable identity, material
semantics, provenance/confidence when material, source bindings and explicit
partial/omitted/continuation information. It also states that this is not a
prompt system, model routing system, RAG pipeline, tool-calling protocol or
execution runtime.

The central D1 question is:

> What is a GeesNO.Semantic Profile, how is an exact Profile edition identified
> and versioned, and what does evaluation against that edition mean without
> turning a Profile into Core, Vocabulary, an AI runtime, a prompt, a model, an
> agent, a tool definition or an execution mechanism?

This ADR accepts only the architecture needed for Profile identity, exact
edition identity and the conformance boundary. It does not define AI Context
projection rules, omission/continuation syntax, ordering, boundedness,
serialization, a profile artifact format, a profile schema, validation fixtures,
SDK behavior, model integration, registry lookup, resolver behavior or S4 D2+
decisions.

## Prerequisite review

No unresolved prerequisite blocks a D1 proposal:

1. Foundation separates Core, Vocabularies and Profiles and keeps the standard
   descriptive, domain-neutral, software-neutral, format-neutral,
   offline-capable and AI-provider-neutral.
2. ADR-0009 supplies exact absolute IRI-capable identity and no automatic
   dereference.
3. ADR-0015 separates specification version, Profile identity/version,
   Vocabulary identity/version, Source revision and semantic Revision.
4. ADR-0016 freezes S2 bare-core processing, the root `profiles` declaration
   shape, exact `spec_version: "0.1.0"`, and the distinction between Layers
   0-3 and future Profile validation.
5. ADR-0017 gives useful evidence for Vocabulary identity/version, but it does
   not automatically govern Profiles. S4 must make an explicit Profile
   decision.
6. ADR-0021 keeps discovery, authority and trust optional, attributed and
   offline-safe. A Profile identity cannot require a registry or network fetch.
7. ADR-0022 records human authority to use `geesno.com` for assigned
   GeesNO.Semantic identity paths when a specific decision assigns the path.
8. ADR-0023 defines D7 Profile-related compatibility claims over exact
   reproducible Profile requirement sets, but deliberately leaves concrete
   Profile identity/version and conformance binding to S4.

The repository already contains an AI Context Profile skeleton under
`profiles/ai-context/`. That skeleton is non-normative and contains no schema,
artifact, profile claim, resolver or implementation.

## Controlling distinctions

```text
Profile
!= GeesNO.Semantic Core
!= Vocabulary
!= SemanticDocument identity
!= SemanticDocument spec_version
!= repository/package version
!= Base Vocabulary version
!= Source
!= Binding
!= Extension payload
!= Profile artifact location
!= retrieval URL
!= model identity
!= model vendor
!= model configuration
!= prompt
!= system prompt
!= developer/user message
!= agent
!= tool definition
!= tool call
!= RAG pipeline
!= embedding index
!= model router
!= inference request
!= conversation memory
!= execution plan
!= authorization policy

Profile requirement
!= semantic truth
!= Vocabulary meaning
!= Source reliability
!= Review correctness
!= AI output correctness
!= AI output quality

Profile conformance
!= bare-core conformance
!= truth
!= trust
!= safety for every use
!= permission to execute anything
```

## Alternatives

### Alternative A - Profile as a new Core primitive

A Profile could become a new universal core record or object kind, with Profile
requirements embedded in the core model. This is rejected. Profiles are
additional conformance/projection contracts over existing SemanticDocument,
Entity, Assertion, Source, Binding, lifecycle, Extension and Vocabulary
mechanics. Making Profile a core primitive would enlarge the universal core and
risk a second semantic model.

### Alternative B - Profile as AI/runtime configuration

A Profile could identify prompts, model IDs, tokenizer IDs, context-window
sizes, temperature, tools, function schemas, retrieval indexes, RAG pipelines,
agent loops or model routers. This is rejected. Those are implementation or
integration concerns. The AI Context Profile may describe semantic context for
AI-oriented consumption, but it does not operate an AI system.

### Alternative C - Profile as an identified additional conformance and projection requirement set

A Profile is an identified family of additional requirements that can be
assessed against a bare-core-valid SemanticDocument or, in later decisions, an
explicit projection derived from the same accepted Semantic model. The Profile
selects additional constraints and preservation/projection obligations without
changing core meaning. This is proposed.

Conceptually:

```text
SemanticDocument or accepted future Semantic projection
+ exact Profile edition
+ Profile-specific requirements
= Profile assessment result
```

The formula is conceptual only. This ADR does not define projection mechanics,
assessment result serialization or diagnostics.

## Proposed decision

### Profile definition

A **GeesNO.Semantic Profile** is a named, versioned family of additional
requirements, constraints or projection obligations over the accepted
GeesNO.Semantic model. A Profile may constrain or require use of existing core
structures, qualified Vocabulary terms, Extensions, lifecycle/scope information,
Source/Binding data, provenance/confidence/review data or projection metadata.

A Profile does not create new core identity, new Entity kinds, new Assertion
categories, new trust semantics or a second semantic model. In particular, D1
rejects creating universal primitives such as:

```text
AIEntity
AIAssertion
AIConcept
AIRepresentation
AIProvenance
AIContextEntity
AIContextDocument
```

A future AI Context Profile must reuse the accepted model unless a later ADR
proves a genuinely universal need and explicitly changes the architecture.

### Profile family identity

A Profile family identity is a stable absolute IRI identifying the Profile
family across exact editions.

It is not versioned and is not a retrieval location, artifact location, model
identity, vendor identity, registry entry or network dependency. It is compared
by the same exact IRI principles accepted for GeesNO.Semantic identifiers.

```text
Profile family identity
!= Profile edition
!= Profile version
!= requirement set alone
!= retrieval URL
!= artifact location
!= model identity
!= model vendor
!= network dependency
```

Generic processing MUST NOT dereference the Profile IRI merely because it is an
IRI. A Profile artifact may later be published at some location, but artifact
location remains separate from Profile identity.

### Profile version and exact edition

A Profile version is a non-empty exact opaque token scoped to one Profile
family. The exact Profile edition identity is:

```text
(Profile family identity, exact Profile version)
```

Generic processing compares the version token exactly. It MUST NOT infer any of
the following from version spelling:

```text
SemVer ordering
numeric ordering
recency
compatibility range
latest
newest
upgrade
replacement
forward compatibility
backward compatibility
```

A publisher may document a versioning policy, and a future compatibility claim
may describe relationships between Profile editions, but a generic processor
infers none of that from the token alone.

### Edition immutability

One exact Profile edition pair identifies one immutable normative requirement
set. A material normative change to Profile requirements requires a new Profile
version. Material normative changes include adding, removing or changing a
mandatory requirement, altering conformance conditions, changing projection
obligations, changing required preservation of identity/provenance/trust/source
information, or changing permitted omission/continuation semantics after those
are defined.

Purely editorial changes do not require a new Profile version when they do not
change normative requirements, examples are clearly non-normative, and no
conformance outcome changes.

This ADR does not define content hashes, signatures, canonical bytes or
content-addressed Profile artifacts.

### Requirement-set identity

For D1, the exact Profile edition pair is the reproducible identity of the
normative Profile requirement set:

```text
(Profile family identity, exact Profile version)
= exact Profile requirement-set identity
```

No parallel requirement-set identity is introduced. A future binding may give a
serialized artifact its own ID, fingerprint or publication location, but that
artifact identity does not replace the exact Profile edition identity.

This resolves the D7 placeholder "exact reproducible profile requirement set"
for ordinary GeesNO.Semantic Profiles. If a later external system needs a
sub-profile, selected subset or composed requirement set, that is future Profile
composition work and is not inferred here.

### AI Context Profile family identity

The GeesNO AI Context Profile family identity is:

```text
https://geesno.com/profile/ai-context
```

Rationale:

- `https://geesno.com/` is the controlled institutional identity base already
  authorized for assigned GeesNO.Semantic identity paths.
- `/profile/` separates Profile family identities from `/vocab/` Vocabulary
  identities and from future documentation or artifact paths.
- `ai-context` names the Profile family without embedding a version token.
- no `www` host is used;
- the IRI is not an endpoint requirement and does not imply network access.

Alternative path shapes such as `/profiles/ai-context`, `/ai/context-profile`,
`/vocab/ai-context` or a GitHub/CDN URL are rejected for D1 because they either
blur Profile/Vocabulary separation, encode hosting/location, or add avoidable
path churn.

### Initial Profile version

The initial exact AI Context Profile version is:

```text
0.1.0
```

This token belongs only to the AI Context Profile edition. Its spelling matches
the early project maturity by convention but remains independent:

```text
AI Context Profile version
!= SemanticDocument spec_version
!= GeesNO Base Vocabulary version
!= repository/package version
```

Generic processing MUST NOT infer compatibility from identical spelling across
these independent version spaces.

### Profile conformance target and boundary

A Profile assessment evaluates whether a candidate target satisfies the
requirements of one exact Profile edition. For D1, the target is an existing
SemanticDocument instance that has already passed or been separately evaluated
for bare-core S2 conformance.

Later S4 decisions may define an explicit projection derived from the accepted
Semantic model as a valid AI Context target. This ADR does not define that
projection.

Profile assessment is additional to bare-core conformance:

```text
bare-core/S2 conformance
!= Profile conformance
```

A document may be valid bare core and fail the AI Context Profile without
contradiction. A Profile failure does not retroactively make the bare-core
result invalid.

### Relationship to S2 Layers 0-3

S2 Layers 0-3 remain unchanged:

```text
Layer 0 - raw input
Layer 1 - exact spec_version dispatch
Layer 2 - schema validation
Layer 3 - semantic/integrity checks
```

Profile assessment is conceptually the later Profile layer already reserved by
ADR-0016. This ADR does not renumber Layers 0-3, freeze public diagnostics or
implement a validator. A future S4/S5 decision may define concrete Layer 4
inputs, outputs and diagnostics.

### Profile conformance is not semantic truth

A claim that a document conforms to Profile edition P means only that the
document satisfied P's normative requirements under a future supported binding
and assessment process. It does not mean:

- assertions are true;
- Sources are reliable;
- Reviews are correct;
- Confidence is calibrated;
- the context is sufficient for a task;
- an AI will understand it;
- an AI will answer correctly;
- the document is safe for every use;
- any tool may be executed;
- any authorization has been granted.

### Relationship to Vocabularies

A Profile may eventually require an exact Vocabulary edition, permit specific
terms, impose cardinality or require additional metadata. That does not change
Vocabulary meaning.

```text
Profile requirement
!= Vocabulary meaning
```

A Profile must not redefine `gbase:label`, `gbase:description` or any other
Vocabulary term. If a Profile requires a term, forbids a term, requires review,
requires localization or constrains cardinality, those are Profile conformance
rules rather than changed term definitions.

### Relationship to ADR-0023 / D7

ADR-0023 remains controlling for compatibility claims. A D7 compatibility claim
is not Profile conformance. A Profile does not automatically accept Vocabulary
edition B because some issuer claims B is compatible with A.

If a Profile permits alternatives, mapping assumptions or compatibility claims,
that permission must be an explicit Profile requirement or policy in the exact
Profile edition. No `latest`, version range, third-party compatibility claim or
moving alias becomes Profile conformance automatically.

### Projection boundaries deferred

This ADR does not close context selection or projection semantics. Future S4
work must preserve these candidate invariants unless an accepted ADR supersedes
them:

```text
projection
!= source mutation
!= new semantic truth

omission by projection
!= deletion

omitted
!= Tombstone

context ordering
!= semantic priority unless explicitly defined
```

### AI/runtime/execution boundary

The AI Context Profile name does not authorize AI-provider-specific or runtime
semantics. D1 excludes the following from universal Profile identity and
conformance semantics:

```text
OpenAI / Anthropic / Gemini / Claude / GPT model IDs
tokenizer IDs
token budgets
context-window sizes
temperature / top_p / seed
system/developer/user messages
prompt templates
function calling / tool schemas
agent loops
RAG pipelines
embedding indexes
vector databases
model routing
inference requests
conversation memory
```

If a future integration wants to use those concepts, it belongs outside the
universal Profile contract or in a separate implementation layer that treats
GeesNO.Semantic data as inert input.

### Offline behavior

A Profile can be identified, selected and assessed from locally supplied
artifacts and rules. Generic Profile identity does not require:

- network access;
- `geesno.com` availability;
- registry lookup;
- resolver lookup;
- model API access;
- an LLM;
- an embedding service;
- a vector database.

Unavailability of a retrieval location means unavailable evidence or artifact,
not invalid Profile identity.

### Security and inertness

All semantic text, labels, descriptions, URLs, Source content, Extension
payloads, mapping claims and future AI Context content remain untrusted inert
semantic data.

```text
semantic text
!= prompt instruction
```

A Profile cannot make text executable, grant permission, load plugins, call
models, call tools, fetch URLs, route requests or authorize operations. Any
processor that chooses to interpret semantic text as instructions does so
outside GeesNO.Semantic and must apply its own security policy.

## Cross-domain validation

| Domain | Profile edition stress case | Result under the proposal |
| --- | --- | --- |
| Engineering-like objects | A context profile requires element identity, type and source binding for selected components. | The Profile constrains existing Entity/Assertion/Binding data without CAD/BIM core fields or execution. |
| Spreadsheet/table data | A profile requires column concepts, row representations and provenance for computed values. | Requirements are additional conformance rules over ordinary semantic records, not spreadsheet-specific core. |
| Technical/legal documents | A profile requires clause identity, cited Source regions and review state. | Profile conformance can require preservation of Provenance/Review without asserting legal truth. |
| Software/source repositories | A profile requires symbols, modules and revision context. | Profile identity/version applies without Git becoming universal lifecycle semantics. |
| Scientific datasets | A profile requires measured quantities with units and uncertainty/provenance when material. | It constrains accepted value/provenance mechanics without model-provider or discipline-specific core. |
| Generic product/asset data | A profile requires labels/descriptions and source traceability for product attributes. | Base and third-party Vocabulary terms can be required without redefining their meanings. |

The same Profile family, exact edition and additional conformance model works
across all six domains. None requires adapters, execution behavior, model
configuration, a registry, network access or a second semantic model.

## Adversarial cases

| # | Case | Generic processing may infer | Generic processing MUST NOT infer |
| --- | --- | --- | --- |
| 1 | Bare-core-valid document fails AI Context Profile. | Bare-core result and Profile result differ. | Bare core invalidity or semantic falsehood. |
| 2 | Two Profile versions under one family identity. | They are two exact editions of one Profile family. | Ordering, compatibility or replacement. |
| 3 | Same version spelling under different Profile identities. | Tokens are scoped to different Profile families. | Same requirements or compatibility. |
| 4 | Profile family identity without exact version. | Profile family may be identified. | Reproducible Profile conformance. |
| 5 | `latest` Profile alias. | It is not an exact edition unless fixed as an immutable literal token. | Moving current-edition semantics. |
| 6 | Profile URL returns 404. | Retrieval failed or artifact unavailable. | Invalid Profile identity. |
| 7 | Network unavailable. | Locally supplied Profile rules may still be used. | Network requirement or automatic failure. |
| 8 | Profile version `2.0` versus `1.9`. | Exact tokens differ. | Newer, greater or compatible. |
| 9 | Document uses no Base Vocabulary terms. | Bare core may remain valid. | Profile failure unless exact Profile requires Base terms. |
| 10 | Document uses third-party Vocabulary. | Terms are identified by absolute IRIs. | Profile acceptance unless exact Profile permits them. |
| 11 | Compatibility claim says Vocabulary B compatible with A but Profile requires exact A. | Both claims may coexist. | B satisfies Profile automatically. |
| 12 | Malicious text inside `description`. | It is inert semantic text. | Prompt instruction or tool command. |
| 13 | Model-specific prompt embedded as semantic text. | It may be represented as data if valid. | Universal Profile runtime behavior. |
| 14 | Profile attempts to grant permission to execute a tool. | The statement is inert or outside allowed Profile semantics. | Authorization or execution permission. |
| 15 | Profile attempts to redefine a Vocabulary term meaning. | Profile may impose use constraints. | Changed Vocabulary meaning. |
| 16 | Profile requirement changes without version change. | Governance violation/inconsistent artifact. | Same immutable exact edition. |
| 17 | Purely editorial Profile documentation change. | Same edition can remain valid if requirements unchanged. | New version requirement solely from editorial text. |
| 18 | Exact Profile edition supplied locally with no registry. | It can be assessed offline if the consumer supports it. | Need for central registry. |
| 19 | Two Profiles apply to the same SemanticDocument. | Separate Profile assessments may exist. | Merged Profile, precedence or conflict resolution. |
| 20 | Profile conformance result treated as semantic truth. | The result reports requirement satisfaction. | Truth, trust, AI quality or safety. |

## Consequences

- S4 has an explicit accepted D1 Profile model without opening projection,
  serialization or implementation work.
- Profile family identity and exact Profile edition identity become separate
  from Core, Vocabulary, SemanticDocument identity, `spec_version`, repository
  version, model identity and artifact location.
- The accepted AI Context Profile family identity is
  `https://geesno.com/profile/ai-context`.
- The accepted initial AI Context Profile version is `0.1.0`.
- The exact Profile edition pair is the ordinary identity of the normative
  requirement set; no parallel requirement-set identity is introduced.
- Bare-core conformance and Profile conformance remain separate outcomes.
- Profile conformance does not establish truth, trust, AI correctness, safety
  or execution permission.
- No S2 schema, S2 fixture, AI Context schema, Profile artifact, projection
  format, registry, resolver, SDK, model integration or execution behavior
  follows from this Accepted ADR.

## Remains open

- concrete AI Context selection and projection semantics;
- omission, boundedness and continuation semantics;
- preservation requirements for identity, provenance, confidence, review,
  validity, Source and Binding data;
- ordering and priority semantics, if any;
- Profile requirement expression and concrete Profile binding/artifact format;
- concrete AI Context serialization and schema;
- Profile conformance result model and diagnostics;
- Profile composition, multiple Profile application, conflict and precedence;
- Vocabulary/Profile compatibility policy beyond explicit Profile requirements;
- validation fixtures and S5 diagnostic governance;
- token/size benchmark methodology that remains AI-provider-neutral;
- SDK and tooling behavior; and
- public release, tag/ZIP and hosting/publication process.

## Acceptance record

**Decision status: Accepted**

Accepted by explicit human architecture decision on 2026-09-18. Acceptance closes
S4 D1 only. It does not implement AI Context projection, publish a Profile
artifact or schema, create a registry or resolver, modify S2, accept D2, open
S5, implement an SDK or add execution behavior.
