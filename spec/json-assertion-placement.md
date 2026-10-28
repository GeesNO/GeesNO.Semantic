# JSON assertion placement and addressability analysis

**Scope:** Core JSON assertion placement and addressability (`spec_version` `0.1.0`).
**Architectural authority:** [ARCHITECTURE.md](../ARCHITECTURE.md) and accepted ADRs.

Accepted ADR-0005 supplies the hybrid abstract assertion contract. Accepted
ADR-0011 maps that contract to one JSON location without making its mixed
abstract responsibilities into mixed serialized placement.

## Canonicality rule

> **One semantic assertion category has one canonical serialized placement.**

All Type, Property, Relation and Concept–Representation assertions are records
in the document-level `assertions` collection. Entity state does not contain
parallel `types`, `properties`, `relations`, association arrays or a singular
`concept_id` assertion shortcut.

Derived views may group claims by Entity, but those views are not a second
normative GeesNO.Semantic JSON representation.

## Placement comparison

| Alternative | Locality/size | Addressability/lifecycle | Canonicality | Result |
| --- | --- | --- | --- | --- |
| Inline | Best local reading and fewer subject references | Path-sensitive; awkward for Relations, conflicts and later correction | Encourages category-specific locations and endpoint duplication | Not recommended |
| Global | More explicit references and IDs | One stable index for Review, supersession and conflict | One processing path and no privileged endpoint | **Recommended** |
| Mixed | Can optimize each example independently | Conditional promotion and multiple indexes | Same fact can have two normative forms | Rejected |

The [AI Context Profile](ai-context-profile.md) governs descriptive Projection
semantics without changing canonical Core JSON placement.
Canonical exchange itself is optimized for interoperability, not exclusively
for token count.

## Accepted common envelope

The accepted assertion roles below are formally expressed by the Core 0.1 JSON contract.
Accepted ADR-0014/0015/0016 supply the lifecycle, Extension and exact-name
freeze without permitting a second placement:

```json
{
  "id": "urn:uuid:00000000-0000-4000-8000-000000000101",
  "kind": "property",
  "subject": {
    "target": "urn:uuid:00000000-0000-4000-8000-000000000010",
    "location": "in-document"
  },
  "property": "core:label",
  "value": "Example"
}
```

Accepted ADR-0016 requires empty optional members to be omitted. Its
exact requiredness and omission freeze cannot create an alternate assertion
location.

Common responsibilities are:

- mandatory ADR-0009 record ID;
- exactly one explicit Entity subject;
- one category discriminator and specialized claim body;
- scoped Provenance, Confidence and Review;
- lifecycle/validity context under accepted ADR-0014; and
- qualified Extensions at approved points.

Assertion identity does not add an Entity kind. `Entity.kind` remains Concept
or Representation.

## Type / Classification Assertion

```json
{
  "id": "urn:uuid:00000000-0000-4000-8000-000000000111",
  "kind": "type",
  "subject": {
    "target": "urn:uuid:00000000-0000-4000-8000-000000000010",
    "location": "in-document"
  },
  "type": "domain:component"
}
```

`type` is an ADR-0010 qualified term. Several Type Assertions, including
conflicting ones, can target one Entity. `entity.type` is not a shortcut.

## Property Assertion

```json
{
  "id": "urn:uuid:00000000-0000-4000-8000-000000000112",
  "kind": "property",
  "subject": {
    "target": "urn:uuid:00000000-0000-4000-8000-000000000010",
    "location": "in-document"
  },
  "property": "domain:status",
  "condition": {
    "kind": "condition",
    "value": "unknown"
  }
}
```

Exactly one of `value` and `condition` is present. Both branches reuse accepted
ADR-0012 semantics. Multiple same-property assertions are repeated claims;
one list/set value is an aggregate claim. A profile may constrain them, but
core processing does not collapse one into the other.

## Relation

```json
{
  "id": "urn:uuid:00000000-0000-4000-8000-000000000113",
  "kind": "relation",
  "subject": {
    "target": "urn:uuid:00000000-0000-4000-8000-000000000010",
    "location": "in-document"
  },
  "predicate": "domain:connected-to",
  "object": {
    "target": "urn:uuid:00000000-0000-4000-8000-000000000020",
    "location": "in-document"
  }
}
```

Subject and object are ADR-0009 Entity references; predicate is an ADR-0010
qualified term. The record is not repeated at either endpoint. Incoming and
outgoing indexes are derived.

## Concept–Representation association

```json
{
  "id": "urn:uuid:00000000-0000-4000-8000-000000000114",
  "kind": "concept_representation",
  "subject": {
    "target": "urn:uuid:00000000-0000-4000-8000-000000000030",
    "location": "in-document"
  },
  "concept": {
    "target": "urn:uuid:00000000-0000-4000-8000-000000000040",
    "location": "in-document"
  }
}
```

The subject must be a Representation and `concept` must reference a Concept.
The dedicated category is preferred because the many-to-many association is an
accepted universal Core mechanic. Encoding it as a generic Relation weakens
category/cardinality validation; requiring a `represents` predicate would
depend on a Vocabulary-specific predicate; `concept_id` suggests singular ownership. Both sides remain
`0..*`, and every pair has independent trust/lifecycle.

## Assertion ID and stability

Every assertion ID is mandatory from first serialization. Optional identity
would require unsafe promotion when an anonymous claim later needs review or
correction. A derived ID based on position, order, body or hash is unstable or
prematurely depends on byte canonicalization.

The claim body is stable for one assertion ID. A changed subject, category,
type/property/predicate/target or Property value/condition creates a new
assertion ID. Accepted ADR-0014 defines the encoding for how
that new claim corrects or supersedes the old one. Trust/lifecycle envelope
state can evolve while the claim ID remains the same.

Two IDs with identical claim bodies remain structurally valid: they may be
independent claims or semantic duplicates with distinct Provenance. The same
ID twice, or the same ID with different claim bodies, is invalid. Automatic
content deduplication is forbidden.

## Trust-record placement and addressability

Provenance, Confidence and Review are nested only in the exact record they
qualify. There is no competing global trust-record collection. If a Review
qualifies a previous Review, it is nested in that Review rather than becoming a
peer with ambiguous scope.

A Provenance, Confidence or Review record may omit `id` while it is purely
scoped nested metadata. ADR-0011 does not impose identity on every trust
occurrence. When a trust record needs independent citation, correction,
supersession or lifecycle targeting, it requires stable ADR-0009 addressability
and any declared ID participates in the document-wide uniqueness domain. This
does not make it an Entity. Array index and JSON Pointer are never identity.

Repeated use of evidence references the same Source/evidence resource from
separate scoped Provenance records. Canonical JSON does not share one
Provenance object globally merely to save bytes. The AI Context Profile
governs Projection preservation without changing Core trust scope.

## Order and references

The order of `assertions` has no semantic meaning and cannot establish
identity, priority, truth or conflict resolution. `in-document` subjects and
targets resolve exactly once under ADR-0009; `out-of-document` expectation does
not imply successful resolution or dereference. Byte ordering belongs to
ADR-0016.

## Minimal impact

| Dataset | Additional assertion structure |
| --- | --- |
| Concept-only | None |
| Representation-only | None |
| One type | One assertion ID + subject reference + type body |
| One property | One assertion ID + subject reference + property/value body |
| One Relation | One assertion ID + subject/object references + predicate |
| One association | One assertion ID + Representation subject + Concept target |

The overhead is deliberate: every first claim is already correctable,
reviewable and lifecycle-addressable.

## Cross-domain result

- Engineering uses the same Type/Property/Relation collection for component
  classification, dimensions and connectivity.
- Spreadsheet repeated values remain separate claims, while an aggregate list
  stays one explicit ADR-0012 value.
- Legal interpretations and Reviews coexist without forcing one truth.
- Software dependency Relations have one direction/place; corrected
  classifications get new claim IDs.
- Scientific quantities keep exact magnitude/unit and scoped Provenance.
- Product Representations map many-to-many to Concepts through dedicated
  association assertions.

No case needs an inline assertion or product/domain-specific core member.

## Adversarial classification

| Case | Accepted result |
| --- | --- |
| Assertion inline and global | Invalid |
| Duplicate assertion ID | Invalid |
| Same claim body, different IDs | Structurally valid; not automatically deduplicated |
| Same ID, different body | Invalid identity continuity |
| Review of assertion | Nested and valid; its own ID is optional unless independently targeted |
| Review of previous Review | Nested in that Review and valid; independent portable targeting requires the reviewed Review to have an ID |
| Supersession target | Supported by accepted ADR-0014's replacement-to-prior form |
| Relation at both endpoints | Invalid duplicate placement |
| Association as `concept_id` | Invalid shortcut |
| Property with both/neither value and condition | Invalid |
| Anonymous assertion | Invalid |
| Trust record with independent lifecycle/targeting | Requires ADR-0009 addressability under accepted ADR-0014's conditional trigger |

## Streaming boundary

Global placement does not make collection order semantic. Consumers can build
an ID index incrementally and finish closed-graph checks after parsing. A
future framed or streaming transport can map the same assertion records; it
must not change canonical JSON placement prematurely.

## Normative authority boundary

Accepted ADR-0011 establishes global identified assertions, a dedicated
Concept–Representation category, nested-only trust scope, stable claim
bodies and no semantic array ordering. It does not universally require
identity for nested trust records.

Accepted ADR-0013, ADR-0014, ADR-0015 and ADR-0016 govern the related
Source/Binding, lifecycle, Extension and serialization constraints.

JSON Schema and conformance fixtures implement and test the accepted
Core 0.1 JSON contract; they do not originate normative semantics.
