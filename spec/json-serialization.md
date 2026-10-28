# JSON serialization architecture 0.1

**Core JSON contract:** `spec_version` `0.1.0` (normative representation).
**Architectural authority:** [ARCHITECTURE.md](../ARCHITECTURE.md) and accepted ADRs.

This document specifies the Core 0.1 JSON representation of the accepted
universal abstract model under ADR-0009 through ADR-0016. The schema,
Layers 0–3 checker and paired fixtures implement the accepted ID, qualified
term, assertion, value, Source/Binding, lifecycle, Extension, version and raw
processing rules. Provisional examples remain non-normative.

The governing order remains:

```text
accepted abstract model
    -> approved serialization decisions
    -> formal constraints
    -> JSON Schema
    -> conformance fixtures
```

The schema is a derived formalization of these accepted decisions, never an
independent source of semantics.

## Design goals

The approved serialization is:

- structurally canonical: one normative JSON placement for one semantic role;
- deterministic to validate without an LLM or network access;
- domain-neutral and independent of source applications;
- explicit about identifiers, references, terms, values, units and scope;
- state-first, with optional history that never requires replay;
- closed against accidental unknown core fields while preserving qualified
  Extensions through an explicit mechanism;
- safe to parse as untrusted data.

Byte-for-byte canonicalization is a separate future integrity decision.

## Accepted identifier/reference boundary

ADR-0009 requires one absolute IRI-capable primary-ID space, canonical
lowercase UUID URNs for UUID-based IDs, exact canonical-string equality and one
document-wide uniqueness domain for every addressable record. The top-level
`id` is therefore mandatory in the Core 0.1 JSON SemanticDocument.

A reference distinguishes `in-document` from `out-of-document` target
expectation. It does not encode `resolved` / `unresolved` processing state in
the minimal base reference. Accepted ADR-0016 fixes the reference members as
`target` and `location`; no ID or reference is automatically dereferenced.

## Minimal document shape

The following document is the minimum structural contract:

```json
{
  "spec_version": "0.1.0",
  "id": "urn:uuid:00000000-0000-4000-8000-000000000001",
  "scope": {
    "completeness": "partial"
  }
}
```

Under accepted ADR-0016, every optional empty collection/map, including
`revision` and `history` when absent, is omitted. `null` is not a semantic value
condition or optional-member shorthand.

## Canonical placement

| Semantic role | Canonical placement | Reason |
| --- | --- | --- |
| SemanticDocument metadata | Top-level members | One exchange boundary. |
| Entity state | `entities` collection | Stable indexing independent of assertion placement. |
| Source descriptions | `sources` collection | Source is referenceable and separate from Entity. |
| Bindings | `bindings` collection | A Binding has two required references and independent lifecycle. |
| All assertion categories | One `assertions` collection | Prevent inline/global semantic duplicates. |
| Relation | Assertion record with relation category | Relation shares the accepted assertion contract. |
| Concept–Representation association | Dedicated assertion category | Avoid a singular `concept_id` shortcut or a dependency on a specific Vocabulary edition. |
| Provenance, Confidence and Review | Nested only under the record they qualify | Scope is explicit; no competing global placement. |
| Current Revision | Optional top-level `revision` | Current state stays directly consumable. |
| Tombstones affecting declared state | Top-level `tombstones` | Explicit deletion is visible without history replay. |
| Optional history | Top-level `history` containing previous Revisions, descriptive Changes and historical membership references | Record bodies stay in canonical collections or separate revision documents; history cannot become a second state store. |
| Extensions | `extensions` on explicitly permitted hosts | Unknown qualified data remains inert and scoped. |

Accepted ADR-0011 requires every serialized Assertion to carry an ADR-0009 ID.
It does not require an ID on every nested Provenance, Confidence or Review
record. Trust remains in its single canonical host; a purely scoped occurrence
may be anonymous, while independent semantic targeting requires ADR-0009
addressability under accepted ADR-0014. JSON nesting, Pointer and array
position are not identity.

## Accepted assertion addressability

All Type, Property, Relation and Concept–Representation association records
carry an ID in the 0.1 reference serialization. This is stricter than the
minimum abstract-Core requirement but does not turn assertions into Entities.

Benefits:

- portable Review, correction, conflict and lifecycle targets;
- no JSON Pointer or array-index identity;
- simpler reference integrity and duplicate detection;
- one producer/consumer rule instead of conditional ID promotion.

The cost is additional bytes and minting work. The AI Context Profile defines
Projection semantics separately; the Core JSON contract prioritizes stable
interoperability.

## Accepted Source/Binding architecture

Accepted ADR-0013 requires mandatory ADR-0009 identity for every
Source and Binding in separate top-level collections. The minimum Source is
`id` only; optional universal roles are `locations [0..*]`, one qualified
external `revision`, `fingerprints [0..*]`, scoped trust and later
lifecycle/Extension hooks. Format, media, vendor and label do not become fixed
core fields.

The minimum Binding is `id + entity + source`; `locator [0..1]` and qualified
`method` are optional. One locator uses ADR-0010 `kind` plus ADR-0012 `value`,
including structured values for compound locations. Binding identity denotes
continuity of one specific correlation: locator correction/refinement may
retain the ID only for the same occurrence, while a changed Entity/Source
anchor or distinct/competing correlation requires a new Binding. Matching
Entity/Source/locator bodies do not derive identity. Details and eight-domain
evidence are in
[json-source-bindings.md](json-source-bindings.md).

## Accepted lifecycle architecture

Accepted ADR-0014 requires one document scope with tri-state completeness, an
optional inline current Revision independent from history, explicit
Tombstones, directed supersession, qualified validity and one optional
non-replay history envelope. Current state remains authoritative only for its
declared scope/Revision.

`complete` is scoped rather than universal. It permits portable
absence/non-membership inference only when the consumer understands the
applicable qualified scope definition and profile rules; an unknown definition
is preserved without enabling that inference. Omission remains distinct from
deletion, whose portable representation is a Tombstone.

`history.completeness` covers its declared history scope without promising
embedded complete prior bodies or snapshots. Exact earlier state for one
continuing stable ID is exchanged as a separate SemanticDocument for that
Revision, and no completeness claim turns Changes into a replay log.

## Values and conditions

Accepted ADR-0012 uses a canonical hybrid value: native JSON only for
unambiguous string and boolean, and one tagged object for integer, decimal,
date, date-time, semantic reference, measured quantity, list, set and qualified
structured value. Raw JSON numbers/arrays/objects and `null` are not alternate
value encodings. Integer uses an arbitrary-precision decimal string; decimal
uses a normalized coefficient/exponent pair.

`unknown`, `not_applicable` and `redacted` are explicit conditions. Absence is
represented by no assertion. JSON `null` is not a semantic condition.
Source/display lexical metadata is descriptive only and cannot affect equality,
datatype, precision, scale or significant figures unless an explicit
profile/vocabulary contract says otherwise. It must not reveal a redacted value.

## Terms, vocabularies and Extensions

Accepted ADR-0010 requires one compact term form backed by a document namespace
map. The required expansion base, optional vocabulary identity and optional
vocabulary version are three separate roles. Expanded absolute term IRI controls
identity; no registry or dereference is required.

Accepted ADR-0015 uses an explicit `extensions` object keyed by qualified
terms only on SemanticDocument, Entity, Assertion, Source, Binding, Revision,
Tombstone, Change and scoped Provenance/Confidence/Review record hosts. Core
helper objects do not automatically gain an Extension point.

The accepted decision closes core objects for their declared supported specification
version: an unknown member outside `extensions` is invalid rather than silently
ignored. Extension payload may be arbitrary inert JSON data, distinct from an
ADR-0012 Property value. A semantically unknown Extension remains bare-core
valid when placement, key and payload are valid and no applicable profile
requires understanding.

Lossless round-trip tools preserve unknown Extension key identity and payload
semantics; a lossy projection must explicitly permit/report omission.
Extensions may add meaning but cannot provide, redefine or weaken core meaning.

## Version declarations

Accepted ADR-0015 makes `spec_version` a required exact SemVer contract
identifier. Profile/vocabulary versions, Source revision and semantic Revision
are separate and cannot substitute for it. The Core JSON instance contract
specified here is exactly `0.1.0`; `0.1.0-dev` is a distinct prerelease
token, not an alias for that contract.

During `0.x`, a processor uses only an exactly supported contract. An earlier
supported version uses its matching schema; a later unsupported `0.x`, another
unsupported major or unsupported prerelease fails clearly rather than being
validated with a nearby schema. Every incompatible transition needs a
documented migration. Post-1.0 range/forward compatibility remains open.

## Semantic versus byte canonicalization

Core 0.1 JSON uses a single semantic structure: one assertion collection, one
Binding collection, one value representation per datatype and one Extension
mechanism. These constraints do not require member ordering, whitespace rules
or a byte-canonical JSON algorithm.

Byte canonicalization should remain open until signatures, hashes or content
fingerprints have an approved threat model. Array order is semantic only for
tagged list values; other collections are semantically unordered unless a later
rule says otherwise.

Accepted ADR-0016 supplies the complete safe-byte-to-conformance
pipeline, exact unknown-Extension numeric-token preservation, role-specific
ordering, validation layers, lexical/member/token freeze and empty/null rules.
These rules are part of the accepted Core 0.1 JSON contract.

## Derived JSON Schema

The Core 0.1 JSON schema uses Draft 2020-12 with `$defs`, `$ref`, `oneOf`,
`unevaluatedProperties`, conditional constraints and recursive tagged values.
Exact lexical interoperability rules are expressed directly rather than relying
only on `format` annotations. The local schema intentionally has no `$id` and
requires no schema or vocabulary network access.

## Security boundary

Normative serialization requirements:

- UTF-8 JSON with no duplicate object member names;
- no executable content semantics;
- no automatic dereference of IDs, terms, Source locations or Extensions;
- exact canonical hybrid-value and qualified-term forms;
- structurally valid references under declared in-document/out-of-document
  expectation rules;
- Extensions cannot redefine core fields;
- non-finite numeric concepts are not silently accepted as JSON numbers.

Implementation guidance rather than universal semantic limits:

- configurable document-size, collection-size, string-length and nesting limits;
- recursion, allocation and processing-time limits;
- defensive URI/IRI handling and network isolation;
- safe diagnostics that do not disclose redacted content.

## Implementation and conformance correspondence

1. A local Draft 2020-12 schema derives from accepted ADR-0009 through
   ADR-0016.
2. `$defs` cover identifiers, references, qualified terms, values, trust
   records, Entity, Source, Binding, assertion categories and lifecycle.
3. The SemanticDocument root and versioned core objects are closed.
4. Strict raw parsing and exact version dispatch precede schema selection.
5. Deterministic document-wide semantic/integrity checks follow schema.
6. Normative valid/invalid/unsupported/resource-refusal fixtures have paired
   expected outcomes.
7. Repository, schema and conformance self-tests guard the accepted contract.

## Normative and implementation boundary

The Core 0.1 JSON representation is governed by accepted ADR-0009 through
ADR-0016 and the universal abstract Core model. The local JSON Schema,
deterministic checker and conformance fixtures implement or test the applicable
contract; they do not independently originate semantic rules.

Core `spec_version`, repository package version and public release identifiers
remain separate. Publication status does not change the exact Core JSON
instance contract `0.1.0` or imply any certification program.
