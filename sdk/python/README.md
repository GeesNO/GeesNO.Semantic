# Python Reference SDK

The `geesno_semantic` Python package is an optional, repository-local,
non-normative reference implementation of selected GeesNO.Semantic
contracts.

It provides explicit construction, inspection, serialization and
validation conveniences without defining new semantic rules.

The package is not published to a package registry, does not promise
stable public API compatibility and is not required for conformance.

```text
SDK
!= semantic authority

builder success
!= conformance

load
!= conformance claim

save
!= automatic validation or repair

deterministic SDK formatting
!= normative canonical JSON
```

## Package and Validation Surface

The package provides:

- `load_bytes`, `load_text` and `load_path` for strict Layer 0 parsing
  followed by exact Layer 1 version dispatch;
- `SemanticDocument`, a thin, non-copying mapping view over a
  loss-aware mapping/list/scalar backing tree;
- `dump_text`, `dump_bytes` and `save_path` for explicit serialization
  without implicit validation, repair or semantic normalization;
- `validate_bytes`, `validate_path` and `validate_document`, which
  expose the existing `fixture_runner.validate_bytes()` result mapping
  unchanged.

The backing tree retains exact `RawNumber` tokens, including forms
such as `1`, `1.0`, `1e0`, `1E+0` and `-0`, without binary-floating
conversion.

The backing tree remains the source of record. Views do not synthesize
absent members, defaults, identifiers or lifecycle state.

Parsing and version-dispatch failures use the existing:

- `RawInputError`
- `ResourceRefusal`
- `VersionError`
- `UnsupportedVersion`

Ordinary Python argument, path and serialization failures remain
ordinary Python exceptions, not conformance diagnostics.

Optional `ResourceLimits` are implementation safety controls rather
than additional semantic requirements.

The package reuses the existing deterministic Core conformance
implementation, including Layers 0-3. It does not define an
independent validation authority.

## Running Tests

From the repository root:

```shell
python -m unittest discover -s sdk/python/tests -v
```

The reference tests exercise the existing Core fixtures, including
the established 17-valid, 84-invalid and 101-expectation baseline.

They also cover loss-aware Extension round-trip, source non-mutation
and operation of the Core conformance runner without an SDK dependency.

## Document and Entity Construction

`SemanticDocument.create(...)` requires explicitly supplied:

- `spec_version`
- document `identifier`
- document `scope`

Optional `namespaces` and `profiles` are included only when supplied
by the caller.

Caller-owned construction inputs are copied into the new document
tree. The SDK does not infer identifiers, scopes, namespaces, Profiles,
Revisions or completeness values.

Explicit Entity construction is provided by:

- `add_concept(identifier=...)`
- `add_representation(identifier=...)`

These operations append minimal records to the canonical top-level
`entities` collection while preserving caller order and occurrences.

They do not automatically create assertions or
Concept-Representation associations.

The `entities`, `concepts` and `representations` properties return
fresh tuples of live `Concept` and `Representation` mapping views.

The Mapping interfaces are read-only. However, `backing_tree` and
`backing_record` intentionally expose live mutable JSON objects.

Direct modification through those handles is an explicit caller
mutation; the SDK does not automatically validate or repair it.

`new_uuid_urn()` is an optional helper for generating canonical
lowercase UUID URNs. Builders never call it implicitly.

Callers remain responsible for semantic identity continuity and
may provide any accepted explicit identifier.

```text
view creation
!= backing-record copy or normalization

explicit identifier
!= automatic identity validation
```

Identifier syntax, document-wide uniqueness and other Core
conformance requirements remain the responsibility of the
deterministic Layers 0-3 validator.

Duplicate explicit identifiers are preserved during construction
and reported by the applicable semantic validation rules, including
the `duplicate-id` diagnostic.

Adding an Entity does not modify unrelated loaded records,
unknown Extension payloads or exact `RawNumber` tokens.

## Sources, Bindings, Assertions and Values

`SemanticDocument` provides live views over:

- `sources`
- `bindings`
- `assertions`

Explicit construction operations include:

```text
add_source
add_binding
add_type_assertion
add_property_assertion
add_relation_assertion
add_concept_representation_assertion
```

Every construction operation requires a caller-supplied semantic
record identifier.

References use:

- `reference(target=..., location=...)`

Reference construction does not establish target availability
or perform dereferencing.

Binding Entity/Source anchors, locators and optional methods remain
distinct and are copied exactly as supplied.

Creating a Binding does not automatically create a semantic Assertion.

Supported value construction helpers include:

```text
string_value
boolean_value
integer_value
decimal_value
date_value
date_time_value
reference_value
quantity_value
list_value
set_value
structured_value
condition
```

Additional metadata helpers include:

- `descriptor`
- `fingerprint`

Quantities require explicit magnitudes and qualified units.
Decimal construction does not pass through Python `float`.

Qualified semantic terms retain caller-supplied `prefix:local`
spelling and are evaluated against explicit document namespace
declarations by the Core validator.

The four supported assertion kinds are exactly:

- `type`
- `property`
- `relation`
- `concept_representation`

The SDK does not automatically create inverse relations, implicit
Concept-Representation associations or content-based duplicate merges.

Construction success is not a conformance claim.

## Provenance, Confidence and Review

Entity, Source, Binding and Assertion views expose the supported
host-scoped trust metadata:

- `provenance`
- `confidence`
- `reviews`

Explicit operations include:

- `add_provenance`
- `add_confidence`
- `add_review`

`SemanticDocument.trust_hosts` also enumerates loaded Revision,
Tombstone and Change hosts, including recursively nested trust records.

The document root, scope, history envelope and historical-membership
records are not trust hosts.

`Provenance`, `Confidence` and `Review` are live views over their
existing backing records.

Trust record identifiers remain caller-supplied and optional unless
the applicable Core contract conditionally requires them.

The SDK does not promote anonymous records or mint identifiers.

Provenance source references, qualified terms and detail Values
reuse the supported Core representations.

Confidence supports exact integer/decimal scores without a
`float` shortcut. Applicable score-range checks remain within
Core semantic validation.

Trust metadata stays attached to the exact host it qualifies.

The SDK does not:

- propagate trust metadata between hosts;
- infer semantic truth, authority or permission;
- aggregate Confidence scores;
- vote or combine Reviews;
- create a global trust collection;
- infer missing identity from nesting or context.

## Lifecycle and Historical State

`SemanticDocument` exposes live views for:

- `Revision`
- `Change`
- `Tombstone`

Explicit lifecycle operations include:

```text
set_revision
set_history
add_history_revision
add_change
add_tombstone
add_history_membership
```

History completeness and definitions are caller-supplied.

A history envelope must be explicitly created before adding
historical records.

Current semantic state remains usable without history.

Changes are descriptive records: the SDK does not apply or replay
them automatically.

Supported hosts expose explicit:

- `set_validity`
- `add_supersedes`

only where the applicable Core schema permits those members.

Revision and Tombstone may host trust metadata but do not expose
Validity or supersession.

The SDK does not infer or generate identifiers, parents, targets,
categories, qualified terms or temporal bounds.

Graph cycles, duplicate references, live-target/Tombstone
contradictions, conditional identity and comparable validity
ordering remain Core semantic-validation responsibilities.

Lifecycle construction does not:

- remove or retarget existing records;
- automatically advance Revision;
- create Changes or Tombstones from absence;
- infer timestamps;
- propagate trust;
- reconstruct historical state.

## Extensions and Vocabulary Access

Supported Core Extension hosts expose a read-only `extensions`
mapping and explicit operations:

- `get_extension`
- `set_extension`
- `remove_extension`

These operations affect only the selected inert payload.

They do not create namespace declarations, trust records, Revisions,
Changes or Tombstones.

Extensions remain inert descriptive data. They cannot import,
dispatch or execute behavior.

Unknown nested payloads and exact `RawNumber` tokens remain
preserved within the loss-aware backing tree.

`SemanticDocument` provides:

- `namespaces`
- `namespace`
- `expand_term`

These interfaces inspect document-local declarations and perform
the accepted direct `base + local` expansion.

Expansion does not perform case folding, normalization, rewriting,
discovery or identifier dereferencing.

Namespace mutation is not provided by this interface.
Namespaces and Extensions remain separate concepts.

`VocabularyView` supports exact read-only lookup over one explicitly
caller-supplied local mapping, identified by an exact Vocabulary
identity and version.

It is an SDK view, not a normative Vocabulary artifact or
serialization binding.

The SDK does not reproduce the Base Vocabulary term inventory
as an independent authority.

Vocabulary lookup does not imply:

- a central registry;
- a remote resolver;
- automatic network access;
- fuzzy term matching;
- AI-derived meaning;
- automatic Vocabulary edition substitution.

```text
semantic identifier
!= retrieval instruction

VocabularyView
!= Vocabulary authority

Extension
!= executable behavior
```

## AI Context Projection

The SDK supports caller-explicit AI Context Projection construction
through:

- `SemanticDocument.create_projection(...)`
- `create_projection(...)`

These operations construct one `ai-context-json/0.1.0` Projection
using the exact AI Context Profile edition `0.1.0`.

The caller supplies the applicable:

- selection context;
- Projection scope;
- completeness state;
- selected record IDs by category;
- reference availability;
- optional omission descriptors;
- optional bounds and truncation descriptors;
- optional continuation descriptors;
- optional material-context descriptors.

The SDK copies only explicitly selected records.

It does not expand relationships automatically or interpret
unselected source content as omitted, deleted or false.

The resulting `Projection` has an independent loss-aware
backing artifact.

Selected identifiers, qualified terms, trust and lifecycle data,
unknown Extensions and exact `RawNumber` tokens are preserved.

Projection construction does not mutate its source.

`projection_artifact_id` remains absent unless explicitly supplied.

A current source Revision identifier is carried exactly when present.
Otherwise, the caller must supply an explicit
`source_state_descriptor`.

Namespace declarations are caller-selected and must exactly match
the corresponding source declarations.

## Local Projection Queries

Read-only query operations include:

- `get_record(...)`
- `find_assertions(...)`

These operate through exact comparisons over carried content only.

They do not perform:

- source fallback;
- graph traversal;
- relevance ranking;
- similarity searching;
- AI inference;
- continuation execution;
- Vocabulary resolution;
- identifier dereferencing.

Projection serialization remains local and loss-aware.

Structural and semantic validation reuse the existing repository
AI Context validation components.

Assessment and result construction are exposed through:

- `assess_projection(...)`
- `construct_projection_result(...)`

These delegate to the existing exact Profile assessment and
assessment-result construction components.

The SDK does not define a parallel validator or a general
Profile execution engine.

```text
Projection
!= source mutation

Projection
!= new semantic truth

Profile declaration
!= proof of Profile conformance
```

## Implementation Boundaries

This reference package does not define or require:

- a stable public Python API;
- a package-registry distribution;
- a general Profile composition engine;
- a runtime for executing semantic artifacts;
- product-specific integration adapters;
- GeesNO.Core;
- AI model or provider integration;
- prompt or tool execution;
- automatic retrieval or continuation execution;
- a remote registry or resolver;
- runtime network access;
- certification or endorsement.

The SDK is an optional implementation convenience and cannot
extend the normative meaning of GeesNO.Semantic.

## Authority and Documentation

The applicable semantic contracts remain defined by the
public architecture, accepted ADRs, normative specifications
and exact Profile or Vocabulary editions.

Relevant documentation:

- [Architecture](../../ARCHITECTURE.md)
- [Specifications](../../spec/README.md)
- [Conformance Guide](../../docs/conformance-guide.md)
- [AI Context Profile](../../profiles/ai-context/README.md)
- [Reference SDK Overview](../README.md)
- [Public Preview](../../PUBLIC_PREVIEW.md)

GeesNO.Semantic remains universal, open, descriptive,
software-independent, format-independent, domain-independent,
AI-provider-neutral and usable offline.
