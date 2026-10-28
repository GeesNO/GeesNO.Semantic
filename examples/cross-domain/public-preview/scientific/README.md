# Scientific Measurement

**Status:** NON-NORMATIVE LEARNING EXAMPLE; project-authored, synthetic and
fictional; planned for Public Preview release candidate `0.1.0-preview.1`.

## What This Represents

A fictional temperature observation Concept, one digital Representation and a
source-local observation key.

## What To Notice

The measured quantity includes an exact decimal magnitude and explicit unit.
Provenance identifies the fictional observation mechanism. Confidence remains
separate from both truth and measurement uncertainty.

## Core Concepts

`Concept`, `Representation`, `Source`, `Binding`, Type Assertion, Property
Assertion, quantity, unit, Provenance and Confidence.

## Domain Meaning

`science:*`, `unit:*` and `prov:*` are example-local explanatory terms. They do
not define normative scientific, unit or provenance Vocabularies.

## Validate

```shell
python conformance/runner/run.py examples/cross-domain/public-preview/scientific/example.json
```

Expected result: `valid` after S2 Layers 0-3.

## Boundaries

No sensor, laboratory format, dataset import or measurement adapter exists.
The numeric content is synthetic and is not a real scientific result.
