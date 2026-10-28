# Technical Document Structure

**Status:** NON-NORMATIVE LEARNING EXAMPLE; project-authored, synthetic and
fictional; planned for Public Preview release candidate `0.1.0-preview.1`.

## What This Represents

A fictional technical requirement Concept and the text region that represents
it in a synthetic Source.

## What To Notice

The Binding locates a text region without making page or section a Core field.
The Concept/Representation association carries human-authored Provenance and an
accepted Review disposition. Provenance does not establish truth, and Review
does not grant permission.

## Core Concepts

`Concept`, textual `Representation`, `Source`, `Binding`, Type Assertion,
Property Assertion, Provenance and Review.

## Domain Meaning

`doc:*`, `spec:*`, `prov:*` and `review:*` are example-local explanatory terms,
not a normative document, legal, provenance or review Vocabulary.

## Validate

```shell
python conformance/runner/run.py examples/cross-domain/public-preview/document/example.json
```

Expected result: `valid` after S2 Layers 0-3.

## Boundaries

No PDF, page model, document parser or adapter is required. The sentence is
fictional and does not state a real requirement.
