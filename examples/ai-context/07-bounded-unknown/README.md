# Bounded Projection with unknown completeness

**NON-NORMATIVE ILLUSTRATIVE EXAMPLE**

## Purpose

Show a bound when scope-relative completeness has not been established.

## Source scope

The source is a small stand-in for an open-ended generic dataset view.

## Selection context

One anchor record is selected from the current source state.

## Projection scope

The anchor is explicit, but coverage beyond it is recorded as not established.

## Completeness

`unknown`. The Projection is bounded and the bound was reached, but there is no
established truncation and no known required omission.

## Material context decision

No additional material context is established for the carried anchor.

## Key distinction

`bounded != truncated` and `unknown != partial`.

## Files

- `source.json`: valid S2 open-ended dataset source.
- `projection.json`: bounded Projection with unknown completeness.

## Validation

Tests assert the absence of truncation and omissions as well as the presence of
the explicit bound.

## What this example does NOT mean

It does not use `unknown` to hide known incompleteness or establish that the
source has more records.
