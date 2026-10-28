# Final Cross-Domain Learning Examples

**Status:** NON-NORMATIVE LEARNING EXAMPLES; Public Preview
`0.1.0-preview.1` release candidate; controlled release not finalized.

**License:** [CC BY 4.0](../../../LICENSE-SPECIFICATION), as assigned by the
[repository license map](../../../LICENSES.md).

This collection contains small, project-authored, synthetic and fictional
SemanticDocuments for learning. It demonstrates existing Core mechanics across
unrelated domains without defining new semantics, Vocabularies, Profiles,
fixtures, adapters or interoperability claims.

```text
learning example
!= conformance fixture
!= normative authority
!= proof of universal interoperability
```

The authoritative model and JSON contract remain in the
[specification index](../../../spec/README.md). Start with the
[Implementation Guide](../../../docs/implementation-guide.md), then use the
[Conformance Guide](../../../docs/conformance-guide.md) to interpret validation
results.

## Manifest

| Example | Domain | Primary learning purpose | File | Core Layers 0-3 | Data |
| --- | --- | --- | --- | --- | --- |
| Minimal | Domain-neutral | Envelope, explicit identity and one Concept | [`minimal/example.json`](minimal/example.json) | PASS | Synthetic |
| Engineering | Physical object graph | Concept/Representation, measured property and relation | [`engineering/example.json`](engineering/example.json) | PASS | Synthetic |
| Tabular | Tabular information | Source/Binding, locator, boolean and integer values | [`tabular/example.json`](tabular/example.json) | PASS | Synthetic |
| Document | Technical document | Text Representation, provenance and Review | [`document/example.json`](document/example.json) | PASS | Synthetic |
| Software | Software project structure | Qualified relation, source locator and lifecycle context | [`software/example.json`](software/example.json) | PASS | Synthetic |
| Product | Generic product/asset | One Concept, multiple Representations and inert Extension | [`product/example.json`](product/example.json) | PASS | Synthetic |
| Scientific | Measurement dataset | Quantity, explicit unit, provenance and Confidence | [`scientific/example.json`](scientific/example.json) | PASS | Synthetic |

Each directory contains a short explanation of its example-local terms and
boundaries. The namespace IRIs use the reserved `.invalid` domain and are
identifiers only; validation never dereferences them.

## Shared Lessons

Several examples deliberately show:

```text
semantic Entity identity
!= Source identity
!= native object key
!= locator

Concept
!= Representation
```

Domain terms such as component, record key, text region, source symbol,
catalog item and observation remain qualified example-local terms. None is a
Core primitive. The product Extension is inert data, not a plugin or executable
instruction. Provenance does not establish truth, Confidence is not measurement
uncertainty, and Review is not permission.

## Validation

Run the dedicated repository-local checker:

```shell
python tools/validation/public_preview_examples.py
```

Or validate any document directly through the same approved S2 Layers 0-3:

```shell
python conformance/runner/run.py examples/cross-domain/public-preview/minimal/example.json
```

The dedicated checker enumerates this exact manifest and delegates validation
to the existing S2 runner. These examples are intentionally excluded from
`conformance/valid/`, the S4/S5 corpora and frozen baseline counts.

## Collection Boundaries

- All content is synthetic and contains no customer, project or third-party
  data, schema, screenshot or asset.
- No SDK is required to read or validate the documents.
- No network, resolver, registry, model or AI provider is required.
- No native format parser, connector or adapter is included.
- No AI Context Projection companion is included in P5; Profile examples remain
  in [`examples/ai-context/`](../../ai-context/).
- S8 interoperability hardening has not started.

**Planned for Public Preview `0.1.0-preview.1`; release not finalized.**
