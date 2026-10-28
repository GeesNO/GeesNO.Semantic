# Minimal SemanticDocument

**Status:** NON-NORMATIVE LEARNING EXAMPLE; project-authored, synthetic and
fictional; planned for Public Preview release candidate `0.1.0-preview.1`.

## What This Represents

A deliberately small partial SemanticDocument containing one logical Concept.

## What To Notice

The document declares its exact `spec_version`, stable document identity,
scope completeness and one explicit Entity identity. It invents no defaults
and does not require a Source, Binding, assertion or Representation.

## Core Concepts

`SemanticDocument`, partial scope, `Entity` and `Concept`.

## Domain Meaning

None. This example is domain-neutral and defines no Vocabulary.

## Validate

```shell
python conformance/runner/run.py examples/cross-domain/public-preview/minimal/example.json
```

Expected result: `valid` after S2 Layers 0-3.

## Boundaries

Omitted metadata is only absent. It is not automatically unknown, deleted,
redacted or not applicable. This file is a learning example, not a conformance
fixture or normative minimum profile.
