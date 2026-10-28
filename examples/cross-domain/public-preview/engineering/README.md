# Engineering Object Graph

**Status:** NON-NORMATIVE LEARNING EXAMPLE; project-authored, synthetic and
fictional; planned for Public Preview release candidate `0.1.0-preview.1`.

## What This Represents

A logical physical component, one digital Representation, a source-local
object occurrence and a relation to a logical assembly.

## What To Notice

The Concept identity, Representation identity, Source identity, Binding
identity and locator value are all different. The measured height carries an
explicit decimal magnitude and unit. The component-to-assembly relation is a
qualified semantic assertion, not an action.

## Core Concepts

`Concept`, `Representation`, `Source`, `Binding`, Type Assertion, Property
Assertion, Relation Assertion and measured quantity.

## Domain Meaning

`eng:*` and `unit:*` are example-local explanatory terms. Component, assembly,
object key, height and metre are not new Core fields or a normative Vocabulary.

## Validate

```shell
python conformance/runner/run.py examples/cross-domain/public-preview/engineering/example.json
```

Expected result: `valid` after S2 Layers 0-3.

## Boundaries

No geometry, CAD/BIM model, native parser or adapter exists here. The locator
does not become semantic identity, and the quantity does not imply a default
unit.
