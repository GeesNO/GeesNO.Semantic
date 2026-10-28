# GeesNO.Semantic Implementation Guide

**Status:** NON-NORMATIVE implementation guidance for the planned Public Preview
`0.1.0-preview.1`.

**License:** [CC BY 4.0](../LICENSE-SPECIFICATION), as assigned by the
[repository license map](../LICENSES.md).

This guide is non-normative. If it conflicts with an authoritative
specification or artifact, the authoritative source wins. It explains how to
implement existing contracts; it creates no semantic, serialization or
conformance rule.

The route is language-, software-, format-, domain- and AI-provider-neutral.
It is usable offline. You do not need the Python reference SDK, a GeesNO
service, or network dereference to implement GeesNO.Semantic.

## 1. Authority and Layers

Start with [ARCHITECTURE.md](../ARCHITECTURE.md), the
[Accepted ADR index](../adr/README.md) and the
[Core specification index](../spec/README.md). The public
[Documentation Map](README.md) identifies each authoritative artifact.

```text
Core           universal semantic mechanics
Vocabulary     qualified meaning outside Core
Profile        exact requirements for a use case
Serialization  one concrete representation of the abstract model
Conformance    deterministic assessment of an exact contract
Reference SDK  optional non-normative implementation
```

Keep these boundaries visible in every implementation:

```text
Core != Vocabulary
Core != Profile
Profile != Vocabulary

semantic meaning != execution
semantic identity != digital representation
semantic identity != source locator
Source != Entity
Binding != semantic truth
Assertion != Entity

SDK != specification
```

GeesNO.Semantic describes information. LLM calls, prompts, agents, tool calls,
RAG, embeddings, vector databases, ranking, automatic relevance, application
commands, transactions, permissions and workflow orchestration are outside the
standard. External software may use semantic data for those purposes without
making those mechanisms part of GeesNO.Semantic.

## 2. Producer Route

A producer writes an exact supported contract. The current reference JSON
contract is `spec_version` `0.1.0`; the repository itself remains pre-1.0 and
unreleased. Follow the [JSON serialization specification](../spec/json-serialization.md)
and [schema](../schema/v0.1/geesno-semantic.schema.json).

1. Choose stable semantic identities under the
   [identity contract](../spec/identity.md). Do not derive them from collection
   position, memory address, native ID, locator or file path.
2. Set the exact `spec_version`; do not use `latest`, `current`, `auto` or a
   nearby supported version.
3. Give the SemanticDocument its own identity and declare explicit
   [scope completeness](../spec/json-lifecycle.md).
4. Declare the [namespace map](../spec/json-qualified-terms.md) needed by every
   compact qualified term.
5. Add [Entities](../spec/entities.md) with explicit identity and exactly one
   Core kind: Concept or Representation.
6. Add separately identified [Sources and Bindings](../spec/source-bindings.md)
   when source correlation is available. A Binding correlates exactly one
   Entity with exactly one Source.
7. Add identified [Assertions](../spec/assertions.md) in the canonical global
   collection: Type, Property, Relation or Concept-Representation association.
8. Encode [values and units](../spec/json-values-and-units.md) using the one
   accepted representation for each datatype. Never infer a unit.
9. Attach Provenance, Confidence and Review only to the record they qualify,
   following the [trust model](../spec/provenance.md).
10. Add explicit [Revision, Change, Tombstone, Validity, supersession or
    history](../spec/revisions.md) only when that lifecycle information is
    actually known.
11. Place qualified inert data only at accepted
    [Extension points](../spec/extensions.md). Do not hide required Core
    meaning in an Extension.
12. Serialize as UTF-8 JSON without inventing alternate placements, defaults
    or byte-canonical ordering.
13. Validate the result through the applicable exact conformance layers before
    claiming conformance.
14. Optionally produce an exact AI Context Projection as a separate artifact;
    do not mutate the source SemanticDocument.

An implementation may build these records in any internal form. Its internal
classes, tables or objects do not become part of the standard.

## 3. Consumer Route

A consumer treats every input as untrusted and preserves explicit distinctions.

1. Read bytes under implementation-defined resource limits and parse strict
   UTF-8 JSON without silently losing significant numeric or duplicate-member
   information required by the [conformance processing contract](../spec/conformance.md).
2. Read `spec_version` and dispatch only to the exact supported contract.
   Reject unsupported versions clearly; do not substitute an older, newer or
   similar version.
3. Validate structure and deterministic integrity before relying on record
   shape. Loading or parsing alone is not conformance.
4. Compare identities by the accepted canonical identity rules. Do not
   normalize, remint, merge or infer identity from location or nesting.
5. Keep Concept and Representation distinct. Read their association only from
   the dedicated assertion category; never infer parentage.
6. Read Source and Binding as descriptive correlation. Do not open, fetch or
   resolve anything merely because a location, locator or reference exists.
7. Read assertions by explicit subject, predicate/property/type and object or
   value roles. Do not convert absence into an implicit claim.
8. Decode each value by its explicit form and retain exact integer/decimal,
   list/set and unit semantics.
9. Expand qualified terms mechanically from the document namespace map when
   required; unknown Vocabulary meaning remains unknown.
10. Read Provenance, Confidence, Review and lifecycle metadata only at their
    declared scope. Do not propagate or aggregate them automatically.
11. Preserve unknown Extensions when making a lossless round trip. Never
    execute them or treat them as plugins or hidden Core members.
12. If an exact Profile applies, obtain its exact identified artifact locally
    or through caller-supplied context. Do not select a latest edition or fetch
    it automatically.
13. Preserve unknown, absent, redacted and not-applicable states separately and
    never invent missing meaning.

## 4. Minimal SemanticDocument

The minimum current JSON document has exactly the required roles described by
the [minimal document section](../spec/json-serialization.md#minimal-document-shape):

- exact `spec_version` `0.1.0`;
- one SemanticDocument `id`; and
- `scope.completeness` with an allowed explicit state.

See the existing normative
[`minimal-document.json`](../conformance/valid/minimal-document.json) fixture
and its [`valid` expected result](../conformance/expected/minimal-document.json).
Optional empty collections and maps are omitted, and `null` is not a shorthand
for absence or an unknown value. The fixture is conformance input, not an API
template or a source of additional semantics.

## 5. Identity and References

The [identity specification](../spec/identity.md) and
[JSON identifier/reference contract](../spec/json-identifiers-and-references.md)
define one absolute IRI-capable identity space and exact canonical-string
comparison. UUID URNs are permitted when canonical, but UUID use is not
mandatory.

```text
semantic identity != array position
semantic identity != runtime object address
semantic identity != source/native ID
semantic identity != locator
semantic identity != file path
```

References carry an explicit target and in-document/out-of-document location
expectation. They do not carry permission or an instruction to resolve:

```text
reference != resolution
reference location semantics != permission to fetch
stable identity != required dereference
```

An implementation may expose resolution as an external application feature,
but conformance and semantic interpretation cannot depend on hidden network,
filesystem or service state.

## 6. Concept and Representation

The only Core Entity kinds are defined in
[Entity, Concept and Representation](../spec/entities.md).

- A **Concept** denotes a logical, semantic or real-world thing independently
  of a particular digital occurrence.
- A **Representation** denotes one digital occurrence or manifestation.
- Either can exist without the other.
- Their cardinality is many-to-many (`0..*` in both directions).
- Each association is an independently identified semantic assertion.

Do not nest a Representation as an implicit Concept child, merge their
identities, or infer an association from matching properties or Bindings.

## 7. Source and Binding

[Source and Binding](../spec/source-bindings.md) separates origin context from
semantic identity:

```text
Source  = separately referenceable origin context
Binding = one identified Entity-to-Source correlation
Locator = Source-relative correlation detail
```

Source is not an Entity. A Binding is not semantic truth. A native ID or
locator is not semantic identity. A Binding can identify correlation with a
Source as a whole, so no artificial locator is required. Sources and Bindings
are optional/plural where the Core permits them, and neither grants access,
permission or retrieval behavior.

Use the normative [JSON Source/Binding representation](../spec/json-source-bindings.md)
for exact placement and members.

## 8. Assertions, Values and Relations

All serialized assertions are identified records in one canonical collection,
but an Assertion is not an Entity. The
[assertion specification](../spec/assertions.md) defines four categories:

- Type / Classification Assertion;
- Property Assertion;
- Relation Assertion; and
- Concept-Representation association.

Do not serialize parallel inline shortcuts or infer claims from Entity fields.
Equal claim bodies with different IDs remain distinct assertion occurrences.

A [Property Assertion](../spec/values-and-units.md) contains either an explicit
value or an explicit allowed condition. The
[JSON value contract](../spec/json-values-and-units.md) admits:

- native JSON string and boolean;
- tagged integer and exact decimal;
- tagged date and UTC date-time;
- tagged semantic reference;
- tagged measured quantity with explicit qualified unit;
- tagged list and set; and
- tagged qualified structured value.

Raw JSON numbers, arrays, objects and `null` are not alternate Core value
encodings. Integers use arbitrary-precision canonical decimal strings. Decimals
use normalized exact coefficient/exponent pairs and must not pass through
binary floating point when that would change value. List order and duplicates
are semantic; set order is not and duplicate canonical values are invalid.

[Relations](../spec/relations.md) are directed subject-predicate-object claims.
Preserve predicate identity and direction. Do not infer symmetry, inverse,
transitivity, containment or equivalence unless the applicable Vocabulary or
Profile defines it.

## 9. Namespaces and Vocabularies

The [qualified-term contract](../spec/json-qualified-terms.md) serializes a term
as `prefix:local`. The document map supplies the exact expansion base:

```text
prefix -> expansion base IRI
expansion base IRI + local -> absolute term IRI
```

Expansion is direct concatenation with no inserted delimiter, normalization,
network request or fuzzy matching. The expanded absolute term IRI is semantic
identity; prefix spelling is not. Preserve case and exact term identity.

Core provides mechanics; a Vocabulary supplies qualified meaning. Third
parties may use their own Vocabularies under the accepted namespace and version
rules. The [Vocabulary index](../vocab/README.md) records the architecture and
the current Base Vocabulary decision. No machine-readable Base Vocabulary,
central registry, latest-version resolver or mandatory discovery service is
published.

Unknown declared Vocabulary terms can be parsed, preserved, expanded and
compared mechanically without pretending their meaning is understood.

## 10. Provenance, Confidence and Review

The [trust specification](../spec/provenance.md) keeps three responsibilities
separate:

- **Provenance** describes origin, method or evidence context.
- **Confidence** describes an assessment of certainty.
- **Review** describes an explicit review record/state at its declared scope.

```text
Provenance != truth
Confidence != truth
Review != permission
```

Do not propagate trust metadata to related records, aggregate confidence,
convert review into authorization, or treat an `accepted` review as permission
to execute. Nested placement identifies scope; it does not create global state.

## 11. Lifecycle

Use the [lifecycle specification](../spec/revisions.md) and
[JSON lifecycle representation](../spec/json-lifecycle.md) only for explicit
known lifecycle information:

- Revision identifies semantic state/edition and optional lineage;
- Change is a descriptive change record;
- Tombstone explicitly represents retirement/removal where applicable;
- Validity supplies qualified temporal bounds;
- supersession is a directed explicit relationship; and
- history is optional, scoped and never required for current-state use.

```text
semantic Revision != Source revision
Change != executable patch
Tombstone != absence
absence != deletion
supersedes != target mutation
Validity != inferred current state
```

State is authoritative only for the document's declared scope and Revision.
Do not implement lifecycle as replay, event sourcing, undo/redo, Git semantics
or transaction processing.

## 12. Extensions and Explicit Conditions

[Extensions](../spec/extensions.md) are qualified, host-scoped inert data. They
cannot redefine or weaken Core semantics and are never executable plugins. An
unknown Extension remains bare-Core valid when placement, key and payload obey
the exact contract and no applicable Profile requires its meaning.

A lossless round-trip implementation preserves unknown Extension key identity
and payload semantics, including relevant numeric token spelling. A lossy
projection may omit only under its applicable explicit rules; dropping content
does not become a claim that it never existed.

The [value/condition contract](../spec/json-values-and-units.md#conditions-and-null)
distinguishes:

```text
absent       no assertion/value occurrence
unknown      an explicit condition
redacted     an explicit withheld-value condition
not_applicable an explicit condition
```

These states are not equivalent. Do not synthesize defaults or expose a
redacted value through auxiliary text, diagnostics or Extensions.

## 13. Serialization and Validation Boundary

The [abstract Core](../spec/semantic-core.md) is serialization-independent.
The [JSON `0.1` specification](../spec/json-serialization.md) and
[Draft 2020-12 schema](../schema/v0.1/geesno-semantic.schema.json) define the
current reference representation. JSON mechanics do not become universal
abstract semantics unless the accepted architecture says so.

The JSON document is UTF-8 and uses one canonical semantic placement per role.
No normative byte-canonical JSON, member order, whitespace rule, signature or
hashing algorithm is currently defined. Do not invent one.

```text
parsing/loading != conformance
schema validation != complete Layers 0-3 conformance
```

The [conformance specification](../spec/conformance.md) separates:

1. safe raw-byte/JSON processing;
2. exact version dispatch;
3. Draft 2020-12 schema validation; and
4. deterministic semantic/integrity checks.

Resource bounds are implementation safety controls, not hidden semantic
invalidity. Diagnostics and library exception types remain non-normative.

## 14. How to Validate What You Produced

Use the exact artifacts for the claimed contract:

- [Core schema](../schema/v0.1/geesno-semantic.schema.json);
- [valid fixtures](../conformance/valid/README.md);
- [invalid fixtures](../conformance/invalid/README.md);
- [expected outcomes](../conformance/expected/README.md); and
- [offline Core conformance runner](../conformance/runner/README.md)

For AI Context, also use the exact
[Profile acceptance corpus](../profiles/ai-context/conformance/v0.1/README.md)
and [assessment corpus](../profiles/ai-context/assessment-conformance/v0.1/README.md).

For the complete public validation route, result interpretation and bounded
claim guidance, continue to the non-normative
[Conformance Guide](conformance-guide.md).

```text
validation/conformance != certification
```

## 15. Optional: Producing an AI Context Projection

AI Context is an optional exact Profile, separate from Core. Read the
[Profile semantics](../spec/ai-context-profile.md), exact
[Profile edition `0.1.0`](../profiles/ai-context/v0.1/profile.json),
[JSON binding](../spec/ai-context-json-binding.md) and
[schema](../profiles/ai-context/schema/v0.1/ai-context.schema.json).

A producer supplies explicit source-state identity/revision context, declared
Projection scope/selection and the applicable exact Profile edition. It derives
a separate Projection artifact without mutating the source SemanticDocument.

```text
Projection != SemanticDocument
Projection != new truth
unselected != omitted
bounded != necessarily truncated
continuation metadata != execution instruction
```

Projection completeness is explicit relative to declared scope. Established
truncation or known required in-scope omission is partial; an unselected record
outside declared scope is not automatically omitted content. Projection and
material-dependency continuations remain distinct inert metadata. References
remain non-dereferencing.

Do not turn Profile processing into RAG, prompt construction, model routing,
automatic relevance, retrieval execution or source mutation.

## 16. Language-Neutral Pseudocode

Producer:

```text
create an empty document representation
set exact supported spec_version
set explicit SemanticDocument identity
set explicit scope completeness
declare every namespace needed by compact terms
add explicitly identified records and assertions
serialize the exact JSON contract as UTF-8
run the authoritative conformance process
report only the result actually assessed
```

Consumer:

```text
read bytes under defensive resource limits
parse strict JSON without silent semantic loss
dispatch by exact supported spec_version
run schema and deterministic integrity validation
index records by explicit semantic identity
preserve unknown inert Extensions when round-tripping
never infer, fetch or execute missing meaning
apply an exact Profile only from explicit local assessment context
```

These algorithms intentionally avoid implementation-language data types and
library APIs.

## 17. Error Handling

- Reject unsupported versions explicitly.
- Treat input and Extension payloads as untrusted data.
- Apply defensive byte, nesting, collection and numeric limits without
  presenting those local limits as new semantic rules.
- Reject malformed or ambiguous identity/reference structures rather than
  silently normalizing them.
- Preserve explicit unknown Extension data for a claimed lossless round trip.
- Do not include redacted content in diagnostics.
- Keep library-specific exceptions and messages outside normative claims.

## 18. Common Anti-Patterns

- Using a source/native ID, array index, memory address or locator as semantic
  identity.
- Merging Concept and Representation or inferring their association.
- Treating Binding, Provenance, Confidence or Review as semantic truth.
- Assuming missing content means deleted.
- Dropping unknown Extensions during a claimed lossless round trip.
- Resolving references, namespace IRIs, Vocabulary IRIs or Profile IRIs
  automatically.
- Inventing units, values, inverse relations, defaults or missing assertions.
- Treating Profile requirements as universal Core rules.
- Treating SDK behavior as normative.
- Calling a conformance result certification or endorsement.

## 19. Reference SDK Relationship

The [reference SDK](../sdk/README.md) is an optional worked implementation. It
is not required, is not normative and has no semantic privilege. A conforming
producer or consumer may be implemented in any language without inspecting SDK
source code. Implementation convenience never overrides specification,
schema, Profile or conformance authority.

## 20. Traceability Matrix

| Concern | Authoritative source | Machine-readable or validation support |
| --- | --- | --- |
| Project boundary and precedence | [Architecture](../ARCHITECTURE.md), [Accepted ADRs](../adr/README.md) | Not applicable |
| Core model | [semantic-core.md](../spec/semantic-core.md) | [Core schema](../schema/v0.1/geesno-semantic.schema.json) for JSON only |
| Identity and references | [identity.md](../spec/identity.md), [JSON reference rules](../spec/json-identifiers-and-references.md) | [Core schema](../schema/v0.1/geesno-semantic.schema.json) |
| Entity / Concept / Representation | [entities.md](../spec/entities.md) | [Core schema](../schema/v0.1/geesno-semantic.schema.json) |
| Source / Binding | [source-bindings.md](../spec/source-bindings.md), [JSON binding rules](../spec/json-source-bindings.md) | [Core schema](../schema/v0.1/geesno-semantic.schema.json) |
| Assertions | [assertions.md](../spec/assertions.md), [JSON placement](../spec/json-assertion-placement.md) | [Core schema](../schema/v0.1/geesno-semantic.schema.json) |
| Values and units | [values-and-units.md](../spec/values-and-units.md), [JSON values](../spec/json-values-and-units.md) | [Core schema](../schema/v0.1/geesno-semantic.schema.json) |
| Relations | [relations.md](../spec/relations.md) | [Core schema](../schema/v0.1/geesno-semantic.schema.json) |
| Provenance / Confidence / Review | [provenance.md](../spec/provenance.md) | [Core schema](../schema/v0.1/geesno-semantic.schema.json) |
| Lifecycle | [revisions.md](../spec/revisions.md), [JSON lifecycle](../spec/json-lifecycle.md) | [Core schema](../schema/v0.1/geesno-semantic.schema.json) |
| Extensions | [extensions.md](../spec/extensions.md), [JSON serialization](../spec/json-serialization.md#terms-vocabularies-and-extensions) | [Core schema](../schema/v0.1/geesno-semantic.schema.json) |
| Namespaces / Vocabulary | [JSON qualified terms](../spec/json-qualified-terms.md), [Vocabulary architecture](../vocab/README.md) | Namespace map in the [Core schema](../schema/v0.1/geesno-semantic.schema.json) |
| JSON serialization | [json-serialization.md](../spec/json-serialization.md) | [Draft 2020-12 schema](../schema/v0.1/geesno-semantic.schema.json) |
| Core conformance | [conformance.md](../spec/conformance.md) | [fixtures, expected results and runner](../conformance/README.md) |
| AI Context Profile | [Profile semantics](../spec/ai-context-profile.md), [JSON binding](../spec/ai-context-json-binding.md) | [exact Profile](../profiles/ai-context/v0.1/profile.json), [schema](../profiles/ai-context/schema/v0.1/ai-context.schema.json) |

## 21. Learn From Examples

[cross-domain learning examples](../examples/cross-domain/public-preview/README.md)
provide seven small standalone Core documents across unrelated domains; they
are learning material, not conformance fixtures. Start with the minimal case,
then choose a domain example by the Core mechanics you want to inspect. Every
document can be validated without the reference SDK.

## 22. Documentation Boundaries

Use the [Conformance Guide](conformance-guide.md) for the complete validation
route and bounded claim guidance.

No official certification or endorsement workflow is defined by this guide.

For preview scope, release status and claim boundaries, see
[PUBLIC_PREVIEW.md](../PUBLIC_PREVIEW.md).

This guide remains non-normative and does not override accepted architecture,
specification, schema or conformance material.
