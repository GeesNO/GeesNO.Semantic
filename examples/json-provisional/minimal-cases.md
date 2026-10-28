# Minimal provisional JSON cases

**Status: PROVISIONAL / NON-NORMATIVE — CANDIDATE JSON ONLY**

Each independent snippet exercises one S1 cardinality or S2 serialization
decision. Optional empty collections are omitted where they add no information.
Source/Binding and lifecycle fragments follow accepted ADR-0013/0014
architecture. The examples remain non-normative; Extension/version fragments
exercise accepted ADR-0015 and ADR-0016.

## Empty/minimal SemanticDocument

```json
{
  "spec_version": "0.1.0",
  "id": "urn:uuid:70000000-0000-4000-8000-000000000001",
  "scope": {"completeness": "unknown"}
}
```

Validates that empty semantic state is possible, still identified/versioned
and carries no empty optional containers under accepted ADR-0016.

## Concept-only document

```json
{
  "spec_version": "0.1.0",
  "id": "urn:uuid:70000000-0000-4000-8000-000000000002",
  "scope": {"completeness": "partial"},
  "entities": [
    {"id": "urn:uuid:70000000-0000-4000-8000-000000000010", "kind": "concept"}
  ]
}
```

Validates Concept without Representation, Binding or assertion.

## Representation without Concept

```json
{
  "spec_version": "0.1.0",
  "id": "urn:uuid:70000000-0000-4000-8000-000000000003",
  "scope": {"completeness": "partial"},
  "entities": [
    {"id": "urn:uuid:70000000-0000-4000-8000-000000000011", "kind": "representation"}
  ]
}
```

Validates incremental enrichment and `0` Concept associations.

## Representation with Source and Binding

```json
{
  "spec_version": "0.1.0",
  "id": "urn:uuid:70000000-0000-4000-8000-000000000004",
  "scope": {"completeness": "partial"},
  "namespaces": {
    "loc": "https://example.invalid/vocab/locator/"
  },
  "sources": [
    {"id": "urn:uuid:70000000-0000-4000-8000-000000000020"}
  ],
  "entities": [
    {"id": "urn:uuid:70000000-0000-4000-8000-000000000021", "kind": "representation"}
  ],
  "bindings": [
    {
      "id": "urn:uuid:70000000-0000-4000-8000-000000000022",
      "entity": {"target": "urn:uuid:70000000-0000-4000-8000-000000000021", "location": "in-document"},
      "source": {"target": "urn:uuid:70000000-0000-4000-8000-000000000020", "location": "in-document"},
      "locator": {"kind": "loc:native-key", "value": "42"}
    }
  ]
}
```

Validates the common Binding envelope and source-scoped locator.

## Concept with multiple Representations

```json
{
  "spec_version": "0.1.0",
  "id": "urn:uuid:70000000-0000-4000-8000-000000000005",
  "scope": {"completeness": "partial"},
  "entities": [
    {"id": "urn:uuid:70000000-0000-4000-8000-000000000030", "kind": "concept"},
    {"id": "urn:uuid:70000000-0000-4000-8000-000000000031", "kind": "representation"},
    {"id": "urn:uuid:70000000-0000-4000-8000-000000000032", "kind": "representation"}
  ],
  "assertions": [
    {
      "id": "urn:uuid:70000000-0000-4000-8000-000000000033",
      "kind": "concept_representation",
      "subject": {"target": "urn:uuid:70000000-0000-4000-8000-000000000031", "location": "in-document"},
      "concept": {"target": "urn:uuid:70000000-0000-4000-8000-000000000030", "location": "in-document"}
    },
    {
      "id": "urn:uuid:70000000-0000-4000-8000-000000000034",
      "kind": "concept_representation",
      "subject": {"target": "urn:uuid:70000000-0000-4000-8000-000000000032", "location": "in-document"},
      "concept": {"target": "urn:uuid:70000000-0000-4000-8000-000000000030", "location": "in-document"}
    }
  ]
}
```

Validates one Concept with several independently asserted occurrences.

## Representation with competing Concepts

```json
{
  "spec_version": "0.1.0",
  "id": "urn:uuid:70000000-0000-4000-8000-000000000006",
  "scope": {"completeness": "partial"},
  "namespaces": {"trust": "https://example.invalid/vocab/trust/"},
  "entities": [
    {"id": "urn:uuid:70000000-0000-4000-8000-000000000040", "kind": "representation"},
    {"id": "urn:uuid:70000000-0000-4000-8000-000000000041", "kind": "concept"},
    {"id": "urn:uuid:70000000-0000-4000-8000-000000000042", "kind": "concept"}
  ],
  "assertions": [
    {
      "id": "urn:uuid:70000000-0000-4000-8000-000000000043",
      "kind": "concept_representation",
      "subject": {"target": "urn:uuid:70000000-0000-4000-8000-000000000040", "location": "in-document"},
      "concept": {"target": "urn:uuid:70000000-0000-4000-8000-000000000041", "location": "in-document"},
      "confidence": [
        {
          "score": {
            "kind": "decimal",
            "coefficient": "61",
            "exponent": "-2"
          }
        }
      ]
    },
    {
      "id": "urn:uuid:70000000-0000-4000-8000-000000000044",
      "kind": "concept_representation",
      "subject": {"target": "urn:uuid:70000000-0000-4000-8000-000000000040", "location": "in-document"},
      "concept": {"target": "urn:uuid:70000000-0000-4000-8000-000000000042", "location": "in-document"},
      "reviews": [
        {
          "disposition": "trust:rejected"
        }
      ]
    }
  ]
}
```

Validates many-to-many claims without selecting a winner from Confidence/Review.

## Property with unknown value

```json
{
  "spec_version": "0.1.0",
  "id": "urn:uuid:70000000-0000-4000-8000-000000000007",
  "scope": {"completeness": "partial"},
  "namespaces": {"ex": "https://example.invalid/vocab/example/"},
  "entities": [{"id": "urn:uuid:70000000-0000-4000-8000-000000000050", "kind": "concept"}],
  "assertions": [
    {
      "id": "urn:uuid:70000000-0000-4000-8000-000000000051",
      "kind": "property",
      "subject": {"target": "urn:uuid:70000000-0000-4000-8000-000000000050", "location": "in-document"},
      "property": "ex:status",
      "condition": {"kind": "condition", "value": "unknown"}
    }
  ]
}
```

Validates that unknown is explicit and not JSON `null` or absence.

## Measured quantity

```json
{
  "spec_version": "0.1.0",
  "id": "urn:uuid:70000000-0000-4000-8000-000000000008",
  "scope": {"completeness": "partial"},
  "namespaces": {
    "measure": "https://example.invalid/vocab/measure/",
    "units": "https://example.invalid/vocab/units/"
  },
  "entities": [{"id": "urn:uuid:70000000-0000-4000-8000-000000000060", "kind": "concept"}],
  "assertions": [
    {
      "id": "urn:uuid:70000000-0000-4000-8000-000000000061",
      "kind": "property",
      "subject": {"target": "urn:uuid:70000000-0000-4000-8000-000000000060", "location": "in-document"},
      "property": "measure:length",
      "value": {
        "kind": "quantity",
        "magnitude": {
          "kind": "decimal",
          "coefficient": "125",
          "exponent": "-1",
          "source_lexical": "12.50"
        },
        "unit": "units:metre"
      }
    }
  ]
}
```

Validates exact decimal and explicit unit identity. `source_lexical` is
descriptive only: it changes neither the value, datatype, precision nor scale.

## Conflicting assertions

```json
{
  "spec_version": "0.1.0",
  "id": "urn:uuid:70000000-0000-4000-8000-000000000009",
  "scope": {"completeness": "partial"},
  "namespaces": {"ex": "https://example.invalid/vocab/example/"},
  "entities": [{"id": "urn:uuid:70000000-0000-4000-8000-000000000070", "kind": "concept"}],
  "assertions": [
    {
      "id": "urn:uuid:70000000-0000-4000-8000-000000000071",
      "kind": "property",
      "subject": {"target": "urn:uuid:70000000-0000-4000-8000-000000000070", "location": "in-document"},
      "property": "ex:state",
      "value": "A"
    },
    {
      "id": "urn:uuid:70000000-0000-4000-8000-000000000072",
      "kind": "property",
      "subject": {"target": "urn:uuid:70000000-0000-4000-8000-000000000070", "location": "in-document"},
      "property": "ex:state",
      "value": "B"
    }
  ]
}
```

Validates that semantic conflict can remain structurally valid.

## Reviewed assertion

```json
{
  "spec_version": "0.1.0",
  "id": "urn:uuid:70000000-0000-4000-8000-00000000000a",
  "scope": {"completeness": "partial"},
  "namespaces": {"ex": "https://example.invalid/vocab/example/"},
  "entities": [{"id": "urn:uuid:70000000-0000-4000-8000-000000000080", "kind": "concept"}],
  "assertions": [
    {
      "id": "urn:uuid:70000000-0000-4000-8000-000000000081",
      "kind": "type",
      "subject": {"target": "urn:uuid:70000000-0000-4000-8000-000000000080", "location": "in-document"},
      "type": "ex:candidate",
      "reviews": [
        {
          "disposition": "ex:accepted"
        }
      ]
    }
  ]
}
```

Validates an anonymous, purely scoped Review without making acceptance
objective truth. An ID becomes necessary only if later content targets this
Review independently.

## Tombstoned Entity

```json
{
  "spec_version": "0.1.0",
  "id": "urn:uuid:70000000-0000-4000-8000-00000000000b",
  "scope": {"completeness": "partial"},
  "tombstones": [
    {
      "id": "urn:uuid:70000000-0000-4000-8000-000000000091",
      "target": {"target": "urn:uuid:70000000-0000-4000-8000-000000000090", "location": "out-of-document"},
      "target_category": "entity"
    }
  ]
}
```

Validates explicit withdrawal and retained identity without contradictorily
including the same target as current live state; omission alone is not used.

## Revision with multiple parents

```json
{
  "spec_version": "0.1.0",
  "id": "urn:uuid:70000000-0000-4000-8000-00000000000c",
  "scope": {"completeness": "unknown"},
  "revision": {
    "id": "urn:uuid:70000000-0000-4000-8000-0000000000a0",
    "parents": [
      {"target": "urn:uuid:70000000-0000-4000-8000-0000000000a1", "location": "out-of-document"},
      {"target": "urn:uuid:70000000-0000-4000-8000-0000000000a2", "location": "out-of-document"}
    ]
  }
}
```

Validates lineage only; no branch or merge behavior follows.

## Partial SemanticDocument

```json
{
  "spec_version": "0.1.0",
  "id": "urn:uuid:70000000-0000-4000-8000-00000000000d",
  "scope": {"completeness": "partial"},
  "namespaces": {"ex": "https://example.invalid/vocab/example/"},
  "entities": [{"id": "urn:uuid:70000000-0000-4000-8000-0000000000b0", "kind": "concept"}],
  "assertions": [
    {
      "id": "urn:uuid:70000000-0000-4000-8000-0000000000b1",
      "kind": "relation",
      "subject": {"target": "urn:uuid:70000000-0000-4000-8000-0000000000b0", "location": "in-document"},
      "predicate": "ex:related-to",
      "object": {"target": "urn:uuid:70000000-0000-4000-8000-0000000000b2", "location": "out-of-document"}
    }
  ]
}
```

Validates explicit partiality and an out-of-document target without making a
processing-resolution claim, inferring deletion or using chunk position as
identity.

## Unknown qualified Extension with opaque JSON

```json
{
  "spec_version": "0.1.0",
  "id": "urn:uuid:70000000-0000-4000-8000-00000000000e",
  "scope": {"completeness": "unknown"},
  "namespaces": {
    "vendor": "https://example.invalid/extensions/vendor/"
  },
  "entities": [
    {
      "id": "urn:uuid:70000000-0000-4000-8000-0000000000c0",
      "kind": "representation",
      "extensions": {
        "vendor:analysis": {
          "score": 0.875,
          "note": null,
          "samples": [1, 2, 3]
        }
      }
    }
  ]
}
```

Exercises accepted ADR-0015: a valid declared qualified key can carry
arbitrary inert JSON at an authorized host. The raw number and `null` are
opaque Extension data, not ADR-0012 core values or conditions. This is not a
normative fixture; the S2 candidate self-tests nevertheless revalidate its JSON
against bare-core Layers 0–3.
