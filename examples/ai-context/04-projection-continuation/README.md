# Projection continuation

**NON-NORMATIVE ILLUSTRATIVE EXAMPLE**

## Purpose

Show known remaining content from the same declared Projection scope.

## Source scope

The source describes three identified sections of a structured technical note.

## Selection context

All three sections and their headings are selected.

## Projection scope

The explicit six-record scope is represented only by the first section and its
heading in this Projection artifact.

## Completeness

`partial`, because known same-scope records remain outside this artifact.

## Material context decision

No external material dependency is involved. A Projection continuation records
the remaining same-scope context and repeats the controlling source state and
Profile edition.

## Key distinction

Projection continuation is descriptive metadata about remaining projected
scope. It is not dependency continuation, a retrieval command, cursor
execution or tool call.

## Files

- `source.json`: valid S2 structured-document source.
- `projection.json`: partial Projection with one Projection continuation.

## Validation

The explicit scope and continuation anchors are checked offline.

## What this example does NOT mean

It does not require every partial Projection to declare continuation or promise
that remaining content can be retrieved.
