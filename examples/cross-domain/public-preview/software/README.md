# Software Project Structure

**Status:** NON-NORMATIVE LEARNING EXAMPLE; project-authored, synthetic and
fictional; planned for Public Preview release candidate `0.1.0-preview.1`.

## What This Represents

Two logical software-module Concepts, one source Representation and a
descriptive dependency relation in a specific semantic Revision.

## What To Notice

The file/symbol-like locator is source-relative and is not semantic identity.
The dependency is qualified domain meaning, not an execution instruction. The
optional history records that the relation was described in the current
Revision; consumers need no event replay.

## Core Concepts

`Concept`, `Representation`, `Source`, `Binding`, Type Assertion, Relation
Assertion, Provenance, Revision and Change history.

## Domain Meaning

`code:*` and `prov:*` are example-local explanatory terms. Module, symbol,
dependency and static analysis are not Core primitives or a normative
Vocabulary.

## Validate

```shell
python conformance/runner/run.py examples/cross-domain/public-preview/software/example.json
```

Expected result: `valid` after S2 Layers 0-3.

## Boundaries

This is not a Git, repository-host, language or build-system integration. It
defines no command, workflow, import resolver or automatic Change generation.
