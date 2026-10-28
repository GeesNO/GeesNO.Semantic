# Universal Semantic Core 0.1

**Model:** serialization-independent  
**Architectural authority:** [ARCHITECTURE.md](../ARCHITECTURE.md) and accepted ADRs
**Applicable edition:** Core 0.1

This document defines the universal abstract semantic model. It establishes
conceptual responsibilities, relationships and invariants independently of
serialization.

It does not itself define JSON member names, nesting, ordering or encoding.
The applicable concrete representation is specified separately by the
accepted Core serialization contracts.

ADRs 0005–0008 establish fundamental abstract-model decisions.
Subsequent accepted ADRs define the corresponding concrete Core contracts.

## 1. Scope and interpretation

GeesNO.Semantic describes what exists, what it means, how it is related, where
the information came from and how its trust can be assessed. It does not
execute or prescribe operations on software.

The core contains mechanisms, not an ontology of industries. Domain classes,
properties and predicates belong to vocabularies; interoperable restrictions
belong to profiles; non-core data belongs to namespaced extensions.

The following terms are used deliberately:

- **responsibility**: meaning the abstract model must be able to express;
- **presence**: whether a particular document/entity must contain it;
- **cardinality**: conceptual participation, independent of serialization;
- **available**: supported by the model but not necessarily present;
- **OPEN**: not yet settled by an applicable accepted normative decision.

## 2. Core primitives

### 2.1 SemanticDocument

The boundary of one semantic dataset. It has one semantic document identity and
one explicit specification-version reference. It can contain/index entities,
declare sources and vocabulary/namespace context, describe revision context,
declare applicable profiles and carry extensions.

The responsibility to support these concerns does not make every collection
non-empty. A newly created, fully redacted or metadata-only document can have no
entities or sources. Embedded, sidecar and external storage remain equivalent
exposure patterns; they do not change model meaning.

Accepted ADR-0009 requires that this conceptual document identity be serialized
as one primary ID in the Core JSON representation. It occupies the same document-wide uniqueness domain
as all other addressable records. The shared domain does not make every
primitive addressable or require an ID where its own model has not done so.

### 2.2 Entity

The abstract identifiable semantic unit. Every Entity has one stable semantic
identity and exactly one core kind: Concept or Representation. Labels,
classifications, properties, relations, bindings, provenance/trust/lifecycle
context and extensions are optional capabilities.

Entity identity is not a label, collection position, memory address, locator,
content hash or source-native ID. Domain classification never creates another
core entity kind.

### 2.3 Concept

An Entity denoting a logical, semantic or real-world thing independently of a
particular digital occurrence. A Concept can exist without a Representation or
Binding and can be enriched over time.

### 2.4 Representation

An Entity denoting a particular digital occurrence or manifestation. A
Representation can exist with no known Concept and with an incomplete or absent
Binding. It can later be associated with zero or more Concepts. Allowing more
than one avoids assuming that one passage, region, record or signal segment can
represent only one semantic thing; profiles may impose tighter rules.

Under accepted ADR-0008, each Concept–Representation association is an
independent assertion. Multiple associations are not automatically equivalent,
simultaneously true, accepted or authoritative; each can carry the common
Provenance, Confidence, Review and lifecycle context accepted by ADR-0005.

Geometry, page regions, rows, paths, symbols and time segments are possible
representation/binding details, never mandatory core fields.

### 2.5 Source

A referenceable description of an origin resource or dataset against which
Bindings can be interpreted. A Source may be only partially described, but it
must have reference identity within the semantic dataset. Application, format,
location, revision and fingerprint metadata are optional and must not become
product-specific core requirements.

Source is not an Entity kind. A source resource may also be described by an
Entity when its semantics matter, but the two roles are not silently merged.

### 2.6 Binding

A correlation between one Entity and a location or native identity in one
Source context. Binding answers “where/how can this semantic unit be correlated
with source information?” It never establishes semantic identity or truth.

Bindings are optional and plural. A Concept may have none, a Representation may
have none while being enriched, and either may later gain multiple bindings.
The common semantics and locator alternatives are detailed in
[source-bindings.md](source-bindings.md), accepted ADR-0006 and accepted
ADR-0013. Every Source/Binding has a mandatory JSON ID; one qualified locator
is optional and Binding identity follows one specific correlation's continuity.

### 2.7 Type / Classification Assertion

A claim that one Entity is classified by one qualified type from a vocabulary.
An Entity can have zero or more classifications, including classifications from
different vocabularies or conflicting classifications. Accepted ADR-0010 uses
one compact qualified spelling whose expanded absolute term IRI controls
identity; accepted ADR-0016 establishes the applicable Core JSON lexical
and namespace-map syntax.

### 2.8 Property Assertion

A claim associating one Entity with one qualified property and either a value
or an explicit semantic value condition. Datatype interpretation is required
when it is not inherent. Accepted ADR-0012 fixes the Core value architecture:
native JSON string/boolean, tagged exact forms for all other core datatypes,
explicit conditions and measured quantities whose canonical exchange form
always materializes an ADR-0010 qualified unit. Accepted ADR-0016 freezes the
subordinate JSON names of the accepted Core JSON representation. See
[values-and-units.md](values-and-units.md).

### 2.9 Relation

A semantic claim with exactly one subject Entity, one qualified predicate and
one object Entity. Relation mechanics are universal; domain predicates are not.
A Concept–Representation association is a semantic claim in this family.
Accepted ADR-0011 fixes it as a dedicated assertion category rather than a
qualified base-vocabulary predicate.

### 2.10 Provenance

Traceability for a scoped claim or record. It distinguishes at least
source-authored, imported/native, deterministic derivation, AI inference, user
authorship, mapping and external curation. Provenance can describe origin,
source/evidence, actor or process, time, method and tool/model version without
requiring personal identity.

### 2.11 Confidence

An optional scoped assessment of certainty, independent from Provenance and
Review. Accepted ADR-0016 fixes exact integer/decimal encoding and the
inclusive `0..1` range; calibration and aggregation remain profile work.
Missing confidence never means `1.0`, and a high score
does not establish truth.

### 2.12 Review

A scoped human or controlled-process disposition, independent from Confidence.
The minimal conceptual distinctions are unreviewed, accepted, rejected and
corrected, but the normative state vocabulary and transition rules are OPEN.

### 2.13 Revision / Change

Lifecycle context preserving stable identity across semantic evolution. It must
be able to describe document revision, entity/assertion/binding addition or
change, removal/tombstone and supersession. Snapshot, event and hybrid models
are compared in [revisions.md](revisions.md). Accepted ADR-0007 establishes a
state-first, history-optional hybrid: the state contained in a SemanticDocument
is the authoritative representation of its declared scope for the declared
Revision, and consumers never need to replay Changes.

### 2.14 Extensions

Namespaced, inert data attached at explicitly permitted extension points.
Unknown extensions do not invalidate otherwise conforming core content unless
an applicable profile requires them. Extensions cannot redefine core meaning,
weaken core invariants or execute as plugins.

## 3. Supporting semantic roles, not additional primitives

The model relies on supporting types such as SemanticIdentity, QualifiedTerm,
Value, MeasuredQuantity, VocabularyReference and ProfileReference. These are
value/reference roles, not new independently lifecycle-managed Entity kinds.
Accepted ADR-0012 does not turn a reference, quantity, list, set, structured
value or condition into an Entity.

Accepted ADR-0005 defines an abstract **Assertion contract** shared by Type
Assertions, Property Assertions, Relations and Concept–Representation
associations. It is a consistency rule, not a new Entity kind. Accepted
ADR-0011 later requires an ID on every serialized Assertion but does not
universally require identity for nested trust metadata.

## 4. Shared assertion semantics

Every assertion category has:

1. one claim subject;
2. category-specific claim content (type, property/value, or predicate/object);
3. zero or more provenance records;
4. zero or more confidence assessments;
5. zero or more reviews;
6. optional lifecycle/validity context;
7. zero or more namespaced extensions.

Competing assertions may coexist. Syntactic validity does not choose the true
claim. Provenance, review and lifecycle/supersession provide the evidence needed
for a consumer to make a policy decision.

The hybrid abstract direction and ADR-0011 JSON mapping are Accepted. Every
serialized assertion has an ADR-0009 ID and appears in the single top-level
`assertions` collection; Concept–Representation has a dedicated category.
Trust records remain nested and are not universally identified merely because
they occur.

## 5. Universal invariants

The universal semantic model preserves these invariants:

1. Semantic identity and source/native identity are distinct.
2. Concept and Representation are distinct, independently optional and
   many-to-many capable at the abstract level.
3. No Entity requires classification, properties, relations, Binding,
   Provenance, Confidence, Review or Representation for its existence.
4. Partial semantic enrichment is valid and must not be mistaken for invalidity.
5. A measured magnitude never receives a silently inferred unit unless an
   explicitly applicable profile defines the default.
6. Absent, unknown, not applicable and intentionally redacted are not
   semantically interchangeable.
7. Important derived claims can carry Provenance and Confidence; Review remains
   independent.
8. Qualified terms permit multiple vocabularies; no domain ontology is built
   into the core. Under accepted ADR-0010 their identity is the expanded
   absolute term IRI; expansion base, optional vocabulary identity and optional
   vocabulary version are distinct.
9. Extensions are namespaced data and cannot alter core semantics or execute.
10. References are not automatically dereferenced. Their `in-document` or
    `out-of-document` target expectation is independent of the processor's
    `resolved` or `unresolved` observation under accepted ADR-0009.
11. Conformance is deterministic and exact-versioned, never dependent on an LLM.
12. No application, format, cloud or AI provider is privileged.
13. Missing content does not mean deletion unless explicit scope,
    completeness or profile semantics establish that meaning; a portable
    deletion claim uses an explicit tombstone/removal statement.
14. Revision parents are `0..*` lineage references only. They define no branch,
    merge, synchronization or conflict-resolution behavior.
15. Entity, Assertion, Binding, Concept–Representation association and Source
    description lifecycle are separable; lifecycle records are descriptive and
    untrusted.
16. Under accepted ADR-0012, canonical Core JSON values have one representation per
    datatype, exact integer/decimal semantics, explicit non-null conditions and
    explicit qualified units for quantities. Descriptive lexical metadata
    cannot change value equality or reveal a redacted value.

## 6. Conceptual pseudomodel

> **NON-NORMATIVE / PROVISIONAL.** This notation expresses roles and
> cardinalities only. It is not JSON, a schema or a class design.

```text
SemanticDocument
  identity: SemanticIdentity [1]
  specificationVersion: VersionReference [1]
  entities: Entity [0..*]
  sources: Source [0..*]
  vocabularyContext: VocabularyReference [0..*]
  revisionContext: RevisionContext [0..1]
  declaredProfiles: ProfileReference [0..*]
  extensions: Extension [0..*]

Entity (abstract)
  identity: SemanticIdentity [1]
  kind: Concept | Representation [1]
  labels: HumanReadableText [0..*]
  classifications: TypeAssertion [0..*]
  properties: PropertyAssertion [0..*]
  bindings: Binding [0..*]
  extensions: Extension [0..*]

Concept extends Entity
  representationAssociations: RepresentationAssociation [0..*]

Representation extends Entity
  conceptAssociations: ConceptAssociation [0..*]

Relation
  subject: EntityReference [1]
  predicate: QualifiedTerm [1]
  object: EntityReference [1]
  assertionContext: Provenance/Confidence/Review/Lifecycle/Extensions [0..*]
```

This conceptual pseudomodel intentionally omits collection/index shape,
assertion placement, identifier syntax, exact locator shape and serialized
reference details. Those matters are governed by the applicable concrete
Core serialization specifications and accepted ADRs.

## 7. Cardinalities and adversarial evidence

The complete primitive-by-primitive responsibility and cardinality matrix is in
[model-cardinalities.md](model-cardinalities.md). Six-domain counterexamples
are documented in
[`examples/cross-domain/model-review.md`](../examples/cross-domain/model-review.md).

No mandatory domain-specific field or new universal Entity kind survived that
review.

## 8. Architectural and Representation Boundary

This specification defines the abstract, serialization-independent
Universal Semantic Core 0.1.

Accepted ADR-0005 through ADR-0008 establish its foundational
assertion, Source/Binding, lifecycle and Concept-Representation
architectural decisions.

Accepted ADR-0009 through ADR-0016 establish the corresponding
Core identity, reference, qualified-term, assertion-placement,
value/unit, Source/Binding, lifecycle, Extension, serialization
and validation requirements.

These accepted decisions remain authoritative within their
respective scopes. A concrete serialization or implementation
cannot independently redefine the abstract semantic model.

The applicable public references are:

- [Architecture](../ARCHITECTURE.md)
- [Accepted ADRs](../adr/README.md)
- [JSON Serialization](json-serialization.md)
- [Conformance](conformance.md)
- [Open Normative Questions](open-questions.md)

Unresolved future interoperability matters are tracked separately.
They do not reopen accepted Core contracts or authorize new
semantic requirements through schemas, SDKs or tooling.
