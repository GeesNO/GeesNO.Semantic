# External material dependency

**NON-NORMATIVE ILLUSTRATIVE EXAMPLE**

## Purpose

Show an exact external reference whose target is material but not carried.

## Source scope

The source contains one digital module concept and a relation to an exact
external method-catalog identity.

## Selection context

The module and dependency relation are selected.

## Projection scope

The carried source records and their material dependency are explicitly
described. The external target remains outside the Projection.

## Completeness

`partial`, because the material dependency is known to be omitted.

## Material context decision

The target reference remains exact and is marked `external`. Omission metadata
declares that its content is not preserved, while dependency continuation
describes that missing dependency without retrieving it.

## Key distinction

`exact reference preservation != materialization`, and dependency continuation
is not Projection continuation or automatic dereference.

## Files

- `source.json`: valid S2 digital-resource source.
- `projection.json`: external-reference Projection with omission and dependency continuation.

## Validation

Validation is fully offline; the external URN does not need to resolve.

## What this example does NOT mean

It does not define URL fetching, guarantee target availability or turn
continuation metadata into an executable request.
