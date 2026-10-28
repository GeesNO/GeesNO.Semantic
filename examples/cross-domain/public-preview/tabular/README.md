# Tabular Information

**Status:** NON-NORMATIVE LEARNING EXAMPLE; project-authored, synthetic and
fictional; planned for Public Preview release candidate `0.1.0-preview.1`.

## What This Represents

A logical account Concept represented by one source-local tabular record.

## What To Notice

The semantic Entity keeps a stable ID while the Binding carries a separate
record-key locator. Boolean and exact integer property values are represented
without turning a row, cell or range into a Core primitive.

## Core Concepts

`Concept`, `Representation`, `Source`, `Binding`, Type Assertion and Property
Assertion with boolean and integer values.

## Domain Meaning

`table:*` and `biz:*` are example-local explanatory terms. They define no
normative tabular or business Vocabulary and require no dereference.

## Validate

```shell
python conformance/runner/run.py examples/cross-domain/public-preview/tabular/example.json
```

Expected result: `valid` after S2 Layers 0-3.

## Boundaries

This is not an Excel integration, spreadsheet parser or database adapter. The
record key is a locator value, not the Concept ID.
