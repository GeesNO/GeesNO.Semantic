# Generic Product Or Asset

**Status:** NON-NORMATIVE LEARNING EXAMPLE; project-authored, synthetic and
fictional; planned for Public Preview release candidate `0.1.0-preview.1`.

## What This Represents

One logical asset Concept with two independent source Representations and two
source-local catalog keys.

## What To Notice

One Concept may have multiple Representations. Neither catalog key is the
semantic ID. String and list properties describe the Concept. The namespaced
`learn-ext:display-hint` Extension is opaque inert data.

## Core Concepts

`Concept`, multiple `Representation` records, plural `Source`/`Binding`
records, Type Assertion, Property Assertion, list value and Extension.

## Domain Meaning

`catalog:*` and `learn-ext:*` are example-local explanatory terms. They do not
publish a product Vocabulary, Extension contract or registry.

## Validate

```shell
python conformance/runner/run.py examples/cross-domain/public-preview/product/example.json
```

Expected result: `valid` after S2 Layers 0-3.

## Boundaries

The Extension is not a plugin, executable instruction or Core redefinition. A
consumer that does not understand it still treats it according to the accepted
opaque Extension rules; it does not execute it.
