# Cross-domain provisional JSON review

**Status: PROVISIONAL / NON-NORMATIVE — CANDIDATE JSON ONLY**

All six examples use the same top-level collections and assertion envelope.
Domain-specific meaning appears only in qualified terms and locator values.
Source/Binding and lifecycle/scope roles follow accepted ADR-0013/0014, while
the exact S2 spelling follows accepted ADR-0016. The examples remain
non-normative stress cases.

## 1. Engineering-like object graph

```json
{
  "spec_version": "0.1.0",
  "id": "urn:uuid:10000000-0000-4000-8000-000000000001",
  "scope": {"completeness": "partial"},
  "namespaces": {
    "eng": "https://example.invalid/terms/engineering/",
    "units": "https://example.invalid/vocab/units/"
  },
  "sources": [
    {"id": "urn:uuid:10000000-0000-4000-8000-000000000002"}
  ],
  "entities": [
    {"id": "urn:uuid:10000000-0000-4000-8000-000000000010", "kind": "concept"},
    {"id": "urn:uuid:10000000-0000-4000-8000-000000000011", "kind": "representation"}
  ],
  "bindings": [
    {
      "id": "urn:uuid:10000000-0000-4000-8000-000000000020",
      "entity": {"target": "urn:uuid:10000000-0000-4000-8000-000000000011", "location": "in-document"},
      "source": {"target": "urn:uuid:10000000-0000-4000-8000-000000000002", "location": "in-document"},
      "locator": {
        "kind": "eng:object-key",
        "value": "object-42"
      }
    }
  ],
  "assertions": [
    {
      "id": "urn:uuid:10000000-0000-4000-8000-000000000030",
      "kind": "concept_representation",
      "subject": {"target": "urn:uuid:10000000-0000-4000-8000-000000000011", "location": "in-document"},
      "concept": {"target": "urn:uuid:10000000-0000-4000-8000-000000000010", "location": "in-document"}
    },
    {
      "id": "urn:uuid:10000000-0000-4000-8000-000000000031",
      "kind": "property",
      "subject": {"target": "urn:uuid:10000000-0000-4000-8000-000000000010", "location": "in-document"},
      "property": "eng:height",
      "value": {
        "kind": "quantity",
        "magnitude": {
          "kind": "decimal",
          "coefficient": "32",
          "exponent": "-1",
          "source_lexical": "3.20"
        },
        "unit": "units:metre"
      }
    }
  ]
}
```

Validates semantic/native identity separation and measured units without a
geometry or product field in core.

## 2. Spreadsheet/table dataset

```json
{
  "spec_version": "0.1.0",
  "id": "urn:uuid:20000000-0000-4000-8000-000000000001",
  "scope": {"completeness": "partial"},
  "namespaces": {
    "table": "https://example.invalid/vocab/table/",
    "sales": "https://example.invalid/vocab/sales/"
  },
  "sources": [
    {"id": "urn:uuid:20000000-0000-4000-8000-000000000002"}
  ],
  "entities": [
    {"id": "urn:uuid:20000000-0000-4000-8000-000000000010", "kind": "representation"},
    {"id": "urn:uuid:20000000-0000-4000-8000-000000000011", "kind": "concept"}
  ],
  "bindings": [
    {
      "id": "urn:uuid:20000000-0000-4000-8000-000000000020",
      "entity": {"target": "urn:uuid:20000000-0000-4000-8000-000000000010", "location": "in-document"},
      "source": {"target": "urn:uuid:20000000-0000-4000-8000-000000000002", "location": "in-document"},
      "locator": {
        "kind": "table:record-key",
        "value": "customer-17"
      }
    }
  ],
  "assertions": [
    {
      "id": "urn:uuid:20000000-0000-4000-8000-000000000030",
      "kind": "concept_representation",
      "subject": {"target": "urn:uuid:20000000-0000-4000-8000-000000000010", "location": "in-document"},
      "concept": {"target": "urn:uuid:20000000-0000-4000-8000-000000000011", "location": "in-document"}
    },
    {
      "id": "urn:uuid:20000000-0000-4000-8000-000000000031",
      "kind": "property",
      "subject": {"target": "urn:uuid:20000000-0000-4000-8000-000000000011", "location": "in-document"},
      "property": "sales:account-status",
      "value": "active"
    }
  ]
}
```

Validates that a row index is not identity and table semantics stay qualified.

## 3. Technical/legal document

```json
{
  "spec_version": "0.1.0",
  "id": "urn:uuid:30000000-0000-4000-8000-000000000001",
  "scope": {"completeness": "partial"},
  "namespaces": {
    "doc": "https://example.invalid/vocab/document/",
    "legal": "https://example.invalid/vocab/legal/",
    "review": "https://example.invalid/vocab/review/"
  },
  "sources": [{"id": "urn:uuid:30000000-0000-4000-8000-000000000002"}],
  "entities": [
    {"id": "urn:uuid:30000000-0000-4000-8000-000000000010", "kind": "representation"},
    {"id": "urn:uuid:30000000-0000-4000-8000-000000000011", "kind": "concept"}
  ],
  "bindings": [
    {
      "id": "urn:uuid:30000000-0000-4000-8000-000000000020",
      "entity": {"target": "urn:uuid:30000000-0000-4000-8000-000000000010", "location": "in-document"},
      "source": {"target": "urn:uuid:30000000-0000-4000-8000-000000000002", "location": "in-document"},
      "locator": {
        "kind": "doc:text-region",
        "value": "clause-4.2"
      }
    }
  ],
  "assertions": [
    {
      "id": "urn:uuid:30000000-0000-4000-8000-000000000030",
      "kind": "concept_representation",
      "subject": {"target": "urn:uuid:30000000-0000-4000-8000-000000000010", "location": "in-document"},
      "concept": {"target": "urn:uuid:30000000-0000-4000-8000-000000000011", "location": "in-document"},
      "reviews": [
        {
          "disposition": "review:accepted"
        }
      ]
    },
    {
      "id": "urn:uuid:30000000-0000-4000-8000-000000000031",
      "kind": "type",
      "subject": {"target": "urn:uuid:30000000-0000-4000-8000-000000000011", "location": "in-document"},
      "type": "legal:requirement"
    }
  ]
}
```

Validates scoped Review and document-region locator without making page/clause
fields universal.

## 4. Software repository structure

```json
{
  "spec_version": "0.1.0",
  "id": "urn:uuid:40000000-0000-4000-8000-000000000001",
  "scope": {"completeness": "partial"},
  "namespaces": {
    "code": "https://example.invalid/vocab/code/"
  },
  "sources": [{"id": "urn:uuid:40000000-0000-4000-8000-000000000002"}],
  "entities": [
    {"id": "urn:uuid:40000000-0000-4000-8000-000000000010", "kind": "concept"},
    {"id": "urn:uuid:40000000-0000-4000-8000-000000000011", "kind": "representation"}
  ],
  "bindings": [
    {
      "id": "urn:uuid:40000000-0000-4000-8000-000000000020",
      "entity": {"target": "urn:uuid:40000000-0000-4000-8000-000000000011", "location": "in-document"},
      "source": {"target": "urn:uuid:40000000-0000-4000-8000-000000000002", "location": "in-document"},
      "locator": {
        "kind": "code:symbol",
        "value": "module/example#process"
      }
    }
  ],
  "assertions": [
    {
      "id": "urn:uuid:40000000-0000-4000-8000-000000000030",
      "kind": "concept_representation",
      "subject": {"target": "urn:uuid:40000000-0000-4000-8000-000000000011", "location": "in-document"},
      "concept": {"target": "urn:uuid:40000000-0000-4000-8000-000000000010", "location": "in-document"}
    }
  ],
  "revision": {
    "id": "urn:uuid:40000000-0000-4000-8000-000000000040",
    "parents": [
      {"target": "urn:uuid:40000000-0000-4000-8000-000000000041", "location": "out-of-document"},
      {"target": "urn:uuid:40000000-0000-4000-8000-000000000042", "location": "out-of-document"}
    ]
  }
}
```

Validates symbol/path as locator and multiple-parent lineage without Git or merge
semantics.

## 5. Scientific dataset

```json
{
  "spec_version": "0.1.0",
  "id": "urn:uuid:50000000-0000-4000-8000-000000000001",
  "scope": {"completeness": "partial"},
  "namespaces": {
    "science": "https://example.invalid/vocab/science/",
    "units": "https://example.invalid/vocab/units/"
  },
  "sources": [{"id": "urn:uuid:50000000-0000-4000-8000-000000000002"}],
  "entities": [{"id": "urn:uuid:50000000-0000-4000-8000-000000000010", "kind": "concept"}],
  "assertions": [
    {
      "id": "urn:uuid:50000000-0000-4000-8000-000000000030",
      "kind": "property",
      "subject": {"target": "urn:uuid:50000000-0000-4000-8000-000000000010", "location": "in-document"},
      "property": "science:derived-temperature",
      "value": {
        "kind": "quantity",
        "magnitude": {
          "kind": "decimal",
          "coefficient": "29315",
          "exponent": "-2",
          "source_lexical": "293.150"
        },
        "unit": "units:kelvin"
      },
      "provenance": [
        {
          "kind": "science:recalculation"
        }
      ],
      "confidence": [
        {
          "score": {
            "kind": "decimal",
            "coefficient": "98",
            "exponent": "-2"
          }
        }
      ]
    }
  ]
}
```

Validates exact quantity, unit, derivation and Confidence without treating
Confidence as measurement uncertainty.

## 6. Generic product/asset dataset

```json
{
  "spec_version": "0.1.0",
  "id": "urn:uuid:60000000-0000-4000-8000-000000000001",
  "scope": {"completeness": "unknown"},
  "namespaces": {
    "catalog": "https://example.invalid/vocab/catalog/"
  },
  "sources": [
    {"id": "urn:uuid:60000000-0000-4000-8000-000000000002"},
    {"id": "urn:uuid:60000000-0000-4000-8000-000000000003"}
  ],
  "entities": [
    {"id": "urn:uuid:60000000-0000-4000-8000-000000000010", "kind": "concept"},
    {"id": "urn:uuid:60000000-0000-4000-8000-000000000011", "kind": "representation"},
    {"id": "urn:uuid:60000000-0000-4000-8000-000000000012", "kind": "representation"}
  ],
  "bindings": [
    {
      "id": "urn:uuid:60000000-0000-4000-8000-000000000020",
      "entity": {"target": "urn:uuid:60000000-0000-4000-8000-000000000011", "location": "in-document"},
      "source": {"target": "urn:uuid:60000000-0000-4000-8000-000000000002", "location": "in-document"},
      "locator": {"kind": "catalog:item-key", "value": "SKU-A"}
    },
    {
      "id": "urn:uuid:60000000-0000-4000-8000-000000000021",
      "entity": {"target": "urn:uuid:60000000-0000-4000-8000-000000000012", "location": "in-document"},
      "source": {"target": "urn:uuid:60000000-0000-4000-8000-000000000003", "location": "in-document"},
      "locator": {"kind": "catalog:item-key", "value": "ITEM-77"}
    }
  ],
  "assertions": [
    {
      "id": "urn:uuid:60000000-0000-4000-8000-000000000030",
      "kind": "concept_representation",
      "subject": {"target": "urn:uuid:60000000-0000-4000-8000-000000000011", "location": "in-document"},
      "concept": {"target": "urn:uuid:60000000-0000-4000-8000-000000000010", "location": "in-document"}
    },
    {
      "id": "urn:uuid:60000000-0000-4000-8000-000000000031",
      "kind": "concept_representation",
      "subject": {"target": "urn:uuid:60000000-0000-4000-8000-000000000012", "location": "in-document"},
      "concept": {"target": "urn:uuid:60000000-0000-4000-8000-000000000010", "location": "in-document"}
    }
  ]
}
```

Validates federation of source-specific identifiers without making SKU a
semantic ID or mandatory core field.

## Review conclusion

The same candidate collections and envelopes express all six domains. Page,
cell, row, path, symbol, object key, measurement and catalog identifiers appear
only as qualified terms/values. Accepted ADR-0011 additionally confirms
that engineering Type/Property/connectivity claims, spreadsheet repeated versus
aggregate values, competing legal Reviews, software dependency/correction,
scientific quantity Provenance and product many-to-many mappings need no second
assertion location. No domain-specific core field is required.
